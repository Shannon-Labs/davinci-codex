"""Ornithopter modernization module."""

from __future__ import annotations

import csv
import importlib.util
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, cast

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml

from ..artifacts import ensure_artifact_dir

SLUG = "ornithopter"
TITLE = "Ornithopter Flight Lab"
STATUS = "planning"
SUMMARY = "Flapping-wing flight modernization with composite spars and electric actuation."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"
RHO_AIR = 1.225  # kg/m^3 at sea level
GRAVITY = 9.80665  # m/s^2


@dataclass
class OrnithopterParameters:
    total_mass_kg: float
    wing_area_m2: float
    stroke_amplitude_m: float
    flap_frequency_hz: float
    forward_speed_ms: float
    base_alpha_deg: float
    alpha_amplitude_deg: float
    cl_alpha_per_rad: float
    base_power_w: float
    power_variation_w: float
    battery_capacity_wh: float
    controller_power_w: float


@dataclass
class FlightSimulation:
    time: np.ndarray
    altitude: np.ndarray
    vertical_velocity: np.ndarray
    lift: np.ndarray
    power: np.ndarray
    energy_used_wh: float
    endurance_hours: float


def _load_parameters() -> OrnithopterParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        raw = yaml.safe_load(stream)
    return OrnithopterParameters(**raw)


def _cad_module():
    root = Path(__file__).resolve().parents[2]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Unable to locate Ornithopter CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    params = _load_parameters()
    base_alpha_rad = math.radians(params.base_alpha_deg)
    cl_base = params.cl_alpha_per_rad * base_alpha_rad
    cruise_lift = 0.5 * RHO_AIR * params.wing_area_m2 * params.forward_speed_ms**2 * cl_base
    gross_weight = params.total_mass_kg * GRAVITY
    lift_margin = cruise_lift / gross_weight - 1.0
    power_density = params.base_power_w / params.total_mass_kg

    return {
        "origin": {
            "folios": [
                {
                    "reference": "Codex Atlanticus, 846r",
                    "notes": "Planform with pilot cradle, crank drive, and feather articulation sketches.",
                },
                {
                    "reference": "Manuscript B (Institut de France), 70r",
                    "notes": "Side elevation indicating torsion springs and harness geometry.",
                },
                {
                    "reference": "Codex on the Flight of Birds, 12v",
                    "notes": "Qualitative lift observations informing wing camber assumptions.",
                },
            ],
            "missing_elements": [
                "Quantified power requirements for sustained flapping",
                "Materials capable of surviving cyclic bending stresses",
                "Control surfaces for roll/yaw damping",
            ],
        },
        "goals": [
            "Model flapping lift margin with modern composite spars and electric actuation.",
            "Quantify drivetrain torque and energy needs for 10-minute sorties.",
            "Define control architecture combining differential flapping and tailplane surfaces.",
        ],
        "assumptions": {
            "total_mass_kg": params.total_mass_kg,
            "wing_area_m2": params.wing_area_m2,
            "stroke_amplitude_m": params.stroke_amplitude_m,
            "flap_frequency_hz": params.flap_frequency_hz,
            "forward_speed_ms": params.forward_speed_ms,
            "base_alpha_deg": params.base_alpha_deg,
            "alpha_amplitude_deg": params.alpha_amplitude_deg,
            "cl_alpha_per_rad": params.cl_alpha_per_rad,
        },
        "viability_metrics": {
            "cruise_lift_N": cruise_lift,
            "gross_weight_N": gross_weight,
            "lift_margin": lift_margin,
            "power_density_w_per_kg": power_density,
            "battery_capacity_wh": params.battery_capacity_wh,
        },
        "validation_plan": [
            "Aeroelastic FEM of carbon spar + FlexLam skin",
            "MuJoCo-based flapping dynamics with PX4 controller loop",
            "Hardware-in-loop drivetrain torque verification",
        ],
    }


def _simulate_profile(params: OrnithopterParameters, seed: int, duration_s: float = 30.0, dt: float = 0.02) -> FlightSimulation:
    rng = np.random.default_rng(seed)
    steps = int(duration_s / dt) + 1
    time = np.linspace(0.0, duration_s, steps)
    altitude = np.zeros_like(time)
    vertical_velocity = np.zeros_like(time)
    lift = np.zeros_like(time)
    power = np.zeros_like(time)
    energy_used_wh = 0.0

    base_alpha_rad = math.radians(params.base_alpha_deg)
    alpha_amp_rad = math.radians(params.alpha_amplitude_deg)
    gross_weight = params.total_mass_kg * GRAVITY
    damping = 0.55  # aerodynamic/heave damping coefficient

    for i in range(1, steps):
        t = time[i]
        phase = 2.0 * math.pi * params.flap_frequency_hz * t
        alpha = base_alpha_rad + alpha_amp_rad * math.sin(phase + 0.35)
        cl = float(np.clip(params.cl_alpha_per_rad * alpha, 0.0, 2.1))
        induced_velocity = params.stroke_amplitude_m * 2.0 * math.pi * params.flap_frequency_hz * math.cos(phase)
        effective_speed = math.sqrt(
            params.forward_speed_ms**2 + (0.35 * induced_velocity) ** 2
        )
        turbulence = 1.0 + rng.normal(0.0, 0.015)
        lift[i] = max(0.5 * RHO_AIR * params.wing_area_m2 * effective_speed**2 * cl * turbulence, 0.0)
        accel = (lift[i] - gross_weight) / params.total_mass_kg
        vertical_velocity[i] = vertical_velocity[i - 1] + (accel - damping * vertical_velocity[i - 1]) * dt
        altitude_candidate = altitude[i - 1] + vertical_velocity[i] * dt
        altitude[i] = max(altitude_candidate, 0.0)

        harmonic = 0.5 * (1.0 + math.sin(phase) ** 2)
        power[i] = params.base_power_w + params.power_variation_w * harmonic + params.controller_power_w
        energy_used_wh += power[i] * dt / 3600.0

    avg_power = float(np.mean(power)) if steps > 0 else params.base_power_w
    endurance_hours = params.battery_capacity_wh / avg_power

    return FlightSimulation(time, altitude, vertical_velocity, lift, power, energy_used_wh, endurance_hours)


def _write_csv(path: Path, result: FlightSimulation) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["time_s", "altitude_m", "vertical_velocity_ms", "lift_N", "power_W"])
        for row in zip(result.time, result.altitude, result.vertical_velocity, result.lift, result.power):
            writer.writerow([f"{value:.6f}" for value in row])


def _plot_profiles(path: Path, result: FlightSimulation, gross_weight: float) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    axes[0].plot(result.time, result.altitude, color="tab:blue", label="Altitude")
    axes[0].set_ylabel("Altitude (m)")
    axes[0].grid(True, linestyle=":", alpha=0.4)
    axes[0].legend(loc="upper right")

    axes[1].plot(result.time, result.lift, color="tab:orange", label="Lift")
    axes[1].axhline(gross_weight, color="tab:green", linestyle="--", label="Weight")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Lift (N)")
    axes[1].grid(True, linestyle=":", alpha=0.4)
    axes[1].legend(loc="upper right")

    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    params = _load_parameters()
    result = _simulate_profile(params, seed)
    artifacts = ensure_artifact_dir(SLUG, subdir="sim")
    csv_path = artifacts / "flight_profile.csv"
    plot_path = artifacts / "lift_profile.png"
    _write_csv(csv_path, result)
    _plot_profiles(plot_path, result, params.total_mass_kg * GRAVITY)

    gross_weight = params.total_mass_kg * GRAVITY
    avg_lift = float(np.mean(result.lift))
    lift_ratio = avg_lift / gross_weight if gross_weight else 0.0
    peak_altitude = float(np.max(result.altitude))
    rms_velocity = float(np.sqrt(np.mean(result.vertical_velocity**2)))
    avg_power = float(np.mean(result.power))

    return {
        "duration_s": float(result.time[-1]),
        "avg_lift_N": avg_lift,
        "lift_margin": lift_ratio - 1.0,
        "peak_altitude_m": peak_altitude,
        "vertical_velocity_rms_ms": rms_velocity,
        "avg_power_W": avg_power,
        "energy_used_wh": result.energy_used_wh,
        "estimated_endurance_min": result.endurance_hours * 60.0,
        "artifacts": {
            "profile_csv": str(csv_path),
            "lift_plot": str(plot_path),
        },
    }


def build() -> None:
    try:
        cad = _cad_module()
        cad.generate_ornithopter_frame(span_m=10.5, chord_m=1.4, output_dir=ensure_artifact_dir(SLUG, subdir="cad"))
    except Exception as exc:  # pragma: no cover - CAD is optional in CI
        artifact_dir = ensure_artifact_dir(SLUG, subdir="cad")
        placeholder = artifact_dir / "cad_placeholder.txt"
        with placeholder.open("w", encoding="utf-8") as handle:
            handle.write("Ornithopter CAD generation placeholder\n")
            handle.write("Span: 10.5 m, chord: 1.4 m\n")
            handle.write(f"Error: {exc}\n")


def evaluate() -> Dict[str, object]:
    plan_data = plan()
    sim_data = simulate(seed=42)

    lift_margin = cast(float, sim_data["lift_margin"])
    endurance = cast(float, sim_data["estimated_endurance_min"])
    origin = cast(Dict[str, Any], plan_data["origin"])
    folios = cast(List[Dict[str, str]], origin["folios"])
    artifacts = cast(Dict[str, str], sim_data["artifacts"])

    return {
        "feasibility": {
            "lift_margin": lift_margin,
            "endurance_min": endurance,
            "meets_lift_requirement": lift_margin > 0.1,
            "meets_endurance_target": endurance >= 10.0,
        },
        "risks": {
            "structure": "Verify fatigue life of composite spars under 2.4 Hz flapping.",
            "controls": "PX4 mixing for differential amplitude needs HITL validation.",
            "powertrain": "Thermal limits on 2 kW outrunners during sustained climbs.",
        },
        "priorities": [
            "Fabricate subscale wing section for wind-tunnel validation",
            "Integrate battery thermal model with TVA power draws",
            "Draft defensive publication outlining composite + servo architecture",
        ],
        "artifacts": artifacts,
        "references": folios,
    }
