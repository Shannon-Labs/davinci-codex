"""Modern ornithopter flapping dynamics prototype."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml

from davinci_codex.artifacts import ensure_artifact_dir
from davinci_codex.inventions import ornithopter


@dataclass
class AeroelasticParameters:
    mass_total_kg: float = 92.0
    wing_area_m2: float = 14.0
    stroke_amplitude_m: float = 2.2
    flap_frequency_hz: float = 2.4
    aerodynamic_damping: float = 0.55
    structural_stiffness: float = 4800.0  # Nm/rad equivalent torsional stiffness
    spar_damping: float = 120.0  # Nm*s/rad
    control_torque_limit_nm: float = 350.0
    battery_capacity_wh: float = 11800.0
    efficiency: float = 0.78


@dataclass
class FlappingState:
    time: np.ndarray
    stroke_angle_rad: np.ndarray
    stroke_rate_rad_s: np.ndarray
    twist_rad: np.ndarray
    lift_N: np.ndarray
    torque_nm: np.ndarray
    control_torque_nm: np.ndarray
    energy_wh: float
    endurance_min: float


def simulate(duration_s: float = 30.0, dt: float = 0.01, seed: int | None = None,
             params: AeroelasticParameters | None = None) -> FlappingState:
    """Simulate coupled stroke/twist dynamics with quasi-steady aerodynamics."""
    rng = np.random.default_rng(seed)
    p = params or AeroelasticParameters()

    steps = int(duration_s / dt) + 1
    time = np.linspace(0.0, duration_s, steps)
    stroke = np.zeros_like(time)
    stroke_rate = np.zeros_like(time)
    twist = np.zeros_like(time)
    lift = np.zeros_like(time)
    torque = np.zeros_like(time)
    control_torque_series = np.zeros_like(time)

    inertia = 0.35 * p.mass_total_kg * (p.stroke_amplitude_m / 2) ** 2
    base_alpha = math.radians(8.0)
    cl_alpha = 5.6
    rho = 1.225

    with ornithopter.PARAM_FILE.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    forward_speed = float(data["forward_speed_ms"])

    for i in range(1, steps):
        t = time[i]
        target_stroke = (p.stroke_amplitude_m / 2) * math.sin(2.0 * math.pi * p.flap_frequency_hz * t)
        control_error = target_stroke - stroke[i - 1]
        control_torque = np.clip(220.0 * control_error - 35.0 * stroke_rate[i - 1],
                                 -p.control_torque_limit_nm, p.control_torque_limit_nm)
        control_torque_series[i] = control_torque

        structural_torque = -p.structural_stiffness * twist[i - 1] - p.spar_damping * (twist[i - 1] - stroke_rate[i - 1])
        aerodynamic_torque = -p.aerodynamic_damping * stroke_rate[i - 1]
        total_torque = control_torque + structural_torque + aerodynamic_torque
        angular_accel = total_torque / inertia

        stroke_rate[i] = stroke_rate[i - 1] + angular_accel * dt
        stroke[i] = stroke[i - 1] + stroke_rate[i] * dt
        twist[i] = 0.6 * stroke[i]

        effective_alpha = base_alpha + twist[i]
        effective_cl = max(cl_alpha * effective_alpha, 0.0)
        flapping_speed = stroke_rate[i] * (p.stroke_amplitude_m / 2)
        effective_velocity = math.sqrt(forward_speed**2 + flapping_speed**2)
        turbulence = 1.0 + rng.normal(0.0, 0.012)
        lift[i] = max(0.5 * rho * p.wing_area_m2 * effective_velocity**2 * effective_cl * turbulence, 0.0)
        torque[i] = total_torque

    mech_power = torque * stroke_rate
    energy_wh = float(np.trapezoid(np.abs(mech_power) / p.efficiency, time) / 3600.0)
    avg_power = float(np.mean(np.abs(mech_power))) / p.efficiency
    endurance_min = (p.battery_capacity_wh / avg_power * 60.0) if avg_power else float("inf")

    artifacts = ensure_artifact_dir(ornithopter.SLUG, subdir="synthesis_sim")
    _write_outputs(artifacts, time, stroke, stroke_rate, twist, lift, torque, control_torque_series)

    return FlappingState(time, stroke, stroke_rate, twist, lift, torque, control_torque_series, energy_wh, endurance_min)


def _write_outputs(directory: Path, time: np.ndarray, stroke: np.ndarray, stroke_rate: np.ndarray,
                   twist: np.ndarray, lift: np.ndarray, torque: np.ndarray, control_torque: np.ndarray) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    csv_path = directory / "flapping_state.csv"
    with csv_path.open("w", encoding="utf-8") as handle:
        handle.write("time_s,stroke_rad,stroke_rate_rad_s,twist_rad,lift_N,torque_Nm,control_torque_Nm\n")
        for i in range(time.size):
            handle.write(f"{time[i]:.3f},{stroke[i]:.6f},{stroke_rate[i]:.6f},{twist[i]:.6f},{lift[i]:.2f},{torque[i]:.2f},{control_torque[i]:.2f}\n")

    summary_path = directory / "summary.txt"
    summary_path.write_text(
        (
            f"Samples: {time.size}\n"
            f"Stroke range (deg): {math.degrees(np.min(stroke)):.1f} -> {math.degrees(np.max(stroke)):.1f}\n"
            f"Max lift (N): {np.max(lift):.1f}\n"
            f"Max torque (Nm): {np.max(np.abs(torque)):.1f}\n"
            f"Control torque limit (Nm): {np.max(np.abs(control_torque)):.1f}\n"
        ),
        encoding="utf-8",
    )
