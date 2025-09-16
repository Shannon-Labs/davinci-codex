"""Aerial screw rotor modernization module."""

from __future__ import annotations

import csv
import importlib.util
import math
from pathlib import Path
from typing import Dict, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation, patches
import numpy as np

from ..artifacts import ensure_artifact_dir

SLUG = "aerial_screw"
TITLE = "Aerial Screw Rotor Lab"
STATUS = "in_progress"
SUMMARY = "Momentum-theory lift estimates for a composite helical rotor and torque-balanced frame."

RHO_AIR = 1.225  # kg/m^3 at sea level
ROTOR_RADIUS = 2.0  # meters
ROTOR_INNER_RADIUS = 1.6  # meters
HELICAL_PITCH = 3.5  # meters per revolution
ROTOR_TURNS = 2.5
SLIP_FACTOR = 0.42  # effective axial velocity fraction relative to geometric pitch speed
DRAG_COEFFICIENT = 1.15  # effective profile drag coefficient for broad wooden ribbon
TARGET_PAYLOAD_MASS = 180.0  # kg (pilot + structure and transmission)
STRUCTURE_MASS = 65.0  # kg composite + mast assembly estimate
GRAVITY = 9.80665  # m/s^2


def _cad_module():
    root = Path(__file__).resolve().parents[2]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Unable to locate CAD module for aerial screw")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    required_lift = (TARGET_PAYLOAD_MASS + STRUCTURE_MASS) * GRAVITY
    return {
        "origin": {
            "folio": "Codex Atlanticus, 869r",
            "summary": "Helical rotor envisioned to 'screw' into air for vertical lift.",
            "sources": [
                {
                    "title": "Biblioteca Ambrosiana Digital Archive",
                    "link": "https://www.leonardodigitale.com/opera/ca-869-r/",
                }
            ],
            "missing_elements": [
                "No specification for counter-torque or pilot restraint system",
                "Material selection limited to linen, leaves power density unresolved",
                "No quantified lift estimates or drive power requirements",
            ],
        },
        "goals": [
            "Estimate achievable lift with a composite helical rotor and axial downwash.",
            "Size a human-safe torque-balancing frame using modern materials.",
            "Deliver parametric CAD and simulation scripts for reproducible studies.",
        ],
        "assumptions": {
            "air_density_kg_m3": RHO_AIR,
            "rotor_radius_m": ROTOR_RADIUS,
            "helical_pitch_m": HELICAL_PITCH,
            "turns": ROTOR_TURNS,
            "slip_factor": SLIP_FACTOR,
            "drag_coefficient": DRAG_COEFFICIENT,
            "payload_mass_kg": TARGET_PAYLOAD_MASS,
            "structure_mass_kg": STRUCTURE_MASS,
        },
        "governing_equations": [
            "T = 2 * rho * A * v_i^2 (actuator disk thrust)",
            "v_i = slip_factor * pitch * rpm / 60 (axial inflow approximation)",
            "Q = 0.5 * rho * A * C_d * v_tip^2 * R (drag-derived torque)",
        ],
        "metrics_of_interest": [
            "Hover RPM - rotor speed where thrust equals weight",
            "Power demand vs. available human or engine output",
            "Blade tip Mach number to ensure subsonic operation",
        ],
        "validation_plan": [
            "Wind tunnel downwash mapping with scaled rotor",
            "Instrumented spin tests verifying torque and vibration",
            "Structural FEA of composite mast and blade root",
        ],
    }


def _performance_curve() -> Dict[str, np.ndarray]:
    rpm = np.linspace(20.0, 160.0, 40)
    area = math.pi * ROTOR_RADIUS**2
    v_tip = (rpm * 2.0 * math.pi / 60.0) * ROTOR_RADIUS
    axial_velocity = SLIP_FACTOR * HELICAL_PITCH * rpm / 60.0
    thrust = 2.0 * RHO_AIR * area * axial_velocity**2
    torque = 0.5 * RHO_AIR * area * DRAG_COEFFICIENT * v_tip**2 * ROTOR_RADIUS
    power = torque * (rpm * 2.0 * math.pi / 60.0)
    return {
        "rpm": rpm,
        "thrust": thrust,
        "torque": torque,
        "power": power,
        "tip_speed": v_tip,
    }


def _write_csv(path: Path, data: Dict[str, np.ndarray]) -> None:
    keys = list(data.keys())
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for i in range(len(next(iter(data.values())))):
            row = [f"{data[key][i]:.6f}" for key in keys]
            writer.writerow(row)


def _plot_performance(path: Path, data: Dict[str, np.ndarray]) -> None:
    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax2 = ax1.twinx()
    ax1.plot(data["rpm"], data["thrust"] / 1000.0, label="Lift (kN)", color="tab:blue")
    ax2.plot(data["rpm"], data["power"] / 1000.0, label="Power (kW)", color="tab:red")
    required_lift_kN = (TARGET_PAYLOAD_MASS + STRUCTURE_MASS) * GRAVITY / 1000.0
    ax1.axhline(required_lift_kN, color="tab:green", linestyle="--", label="Required lift (kN)")
    ax1.set_xlabel("Rotor speed (RPM)")
    ax1.set_ylabel("Lift (kN)")
    ax2.set_ylabel("Power (kW)")
    ax1.grid(True, linestyle=":", alpha=0.4)
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def _render_animation(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    blade = patches.Wedge((0, 0), 1.0, 0, 70, width=0.45, facecolor="tab:blue", alpha=0.75)
    ax.add_patch(blade)

    def _update(frame: int):
        angle = (frame / 40.0) * 360.0
        blade.set_theta1(angle)
        blade.set_theta2(angle + 70.0)
        return (blade,)

    anim = animation.FuncAnimation(fig, _update, frames=40, interval=50, blit=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(path, writer=animation.PillowWriter(fps=20))
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    del seed  # deterministic by design
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    data = _performance_curve()
    csv_path = artifacts_dir / "performance.csv"
    _write_csv(csv_path, data)
    plot_path = artifacts_dir / "performance.png"
    _plot_performance(plot_path, data)
    gif_path = artifacts_dir / "rotor_demo.gif"
    _render_animation(gif_path)

    thrust = data["thrust"]
    rpm = data["rpm"]
    power = data["power"]
    required_lift = (TARGET_PAYLOAD_MASS + STRUCTURE_MASS) * GRAVITY
    hover_rpm: Optional[float] = None
    for speed, lift in zip(rpm, thrust):
        if lift >= required_lift:
            hover_rpm = float(speed)
            break

    tip_speed = data["tip_speed"][-1]
    mach = tip_speed / 343.0

    power_at_hover = float(np.interp(hover_rpm, rpm, power)) if hover_rpm is not None else None
    return {
        "artifacts": [str(csv_path), str(plot_path), str(gif_path)],
        "max_lift_N": float(thrust.max()),
        "hover_rpm": hover_rpm,
        "power_at_hover_W": power_at_hover,
        "tip_mach_at_max_rpm": float(mach),
        "notes": "Lift remains marginal for crewed flight; suggests need for lighter frame or multi-rotor array.",
    }


def build() -> None:
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    mesh_path = artifacts_dir / "aerial_screw_mesh.stl"
    cad_module.export_mesh(mesh_path)


def evaluate() -> Dict[str, object]:
    required_lift = (TARGET_PAYLOAD_MASS + STRUCTURE_MASS) * GRAVITY
    sim = _performance_curve()
    hover_lift = float(sim["thrust"][sim["rpm"] >= 80].max())
    torque_at_100 = float(np.interp(100.0, sim["rpm"], sim["torque"]))
    return {
        "practicality": {
            "hover_lift_margin_N": hover_lift - required_lift,
            "torque_at_100rpm_Nm": torque_at_100,
            "power_requirement_kW": float(np.interp(100.0, sim["rpm"], sim["power"]) / 1000.0),
        },
        "ethics": {
            "risk": "Low direct misuse potential; primary hazards are mechanical (blade failure, tip strike).",
            "mitigations": [
                "Use composite layups with redundant safety factor > 2 on centrifugal loads.",
                "Add differential counter-rotating rotor or reaction wheel to cancel torque.",
                "Enclose observers behind protective cage during testing.",
            ],
        },
        "speculative": {
            "validation_steps": [
                "Scaled rotor tests in controlled airflow to verify slip factor assumption.",
                "Sensorized mast to capture torsional vibration during spin-up.",
                "Material coupon testing for flax-carbon hybrid laminates.",
            ],
            "open_questions": [
                "Can geared crank systems or lightweight electric motors deliver >30 kW continuously?",
                "What is the optimal helical pitch to maximize lift without overloading structure?",
            ],
        },
    }
