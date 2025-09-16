"""Self-propelled cart reconstruction with spring-drive analysis."""

from __future__ import annotations

import csv
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib import animation

from ..artifacts import ensure_artifact_dir

SLUG = "self_propelled_cart"
TITLE = "Self-Propelled Cart"
STATUS = "prototype_ready"
SUMMARY = "Spring-driven cart with escapement control for autonomous straight-line travel."

RHO_AIR = 1.225  # kg/m^3

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"


@dataclass
class CartParameters:
    mass_kg: float
    wheel_radius_m: float
    drag_coefficient: float
    frontal_area_m2: float
    spring_k_Nm: float
    spring_max_theta_rad: float
    rolling_coeff: float
    gear_efficiency: float
    timestep_s: float
    duration_s: float


def _load_parameters() -> CartParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        raw = yaml.safe_load(stream)
    return CartParameters(**raw)


def _cad_module():
    root = Path(__file__).resolve().parents[2]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Unable to import cart CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    params = _load_parameters()
    return {
        "origin": {
            "folio": "Codex Atlanticus, 812r",
            "summary": "Spring-driven cart with steering cams and differential gearing for theatrical motion.",
            "sources": [
                {
                    "title": "Biblioteca Ambrosiana Digital Archive",
                    "link": "https://www.leonardodigitale.com/opera/ca-812-r/",
                }
            ],
            "missing_elements": [
                "Exact spring force specification",
                "Friction coefficients across gear train",
                "Control over timing drums for route programming",
            ],
        },
        "goals": [
            "Quantify run distance achievable with laminated torsion springs.",
            "Validate escapement-driven straight-line stability via simplified dynamics.",
            "Deliver CAD suitable for CNC or 3D-printed demonstrators.",
        ],
        "assumptions": {
            "mass_kg": params.mass_kg,
            "wheel_radius_m": params.wheel_radius_m,
            "torsion_constant_Nm_per_rad": params.spring_k_Nm,
            "rolling_coeff": params.rolling_coeff,
            "gear_efficiency": params.gear_efficiency,
        },
        "governing_equations": [
            "F_drive = (tau_spring * gear_efficiency) / wheel_radius",
            "F_drag = 0.5 * rho * C_d * A * v^2",
            "a = (F_drive - F_drag - \\mu_r * m * g) / m",
        ],
        "validation_plan": [
            "Instrumented chassis measuring wheel slip and speed vs. programmed cam",
            "Material coupon testing for spring laminations (clock spring steel vs. composites)",
            "Field trials on level ground documenting path deviation",
        ],
    }


@dataclass
class SimulationResult:
    time: np.ndarray
    position: np.ndarray
    velocity: np.ndarray
    spring_theta: np.ndarray
    drive_force: np.ndarray


def _simulate_dynamics(params: CartParameters) -> SimulationResult:
    steps = int(params.duration_s / params.timestep_s) + 1
    time = np.linspace(0.0, params.duration_s, steps)
    position = np.zeros_like(time)
    velocity = np.zeros_like(time)
    spring_theta = np.zeros_like(time)
    drive_force = np.zeros_like(time)

    theta_available = params.spring_max_theta_rad
    g = 9.80665

    for i in range(1, steps):
        theta = max(theta_available - spring_theta[i - 1], 0.0)
        torque = params.spring_k_Nm * theta
        thrust = (torque * params.gear_efficiency) / params.wheel_radius_m
        drag = 0.5 * RHO_AIR * params.drag_coefficient * params.frontal_area_m2 * velocity[i - 1] ** 2
        rolling = params.rolling_coeff * params.mass_kg * g
        net_force = thrust - drag - rolling
        accel = net_force / params.mass_kg
        velocity[i] = max(velocity[i - 1] + accel * params.timestep_s, 0.0)
        position[i] = position[i - 1] + velocity[i] * params.timestep_s
        spring_theta[i] = spring_theta[i - 1] + velocity[i] * params.timestep_s / params.wheel_radius_m
        drive_force[i] = thrust
        if theta <= 0.0 and velocity[i] <= 0.01:
            time = time[: i + 1]
            position = position[: i + 1]
            velocity = velocity[: i + 1]
            spring_theta = spring_theta[: i + 1]
            drive_force = drive_force[: i + 1]
            break

    return SimulationResult(time, position, velocity, spring_theta, drive_force)


def _write_csv(path: Path, result: SimulationResult) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["time_s", "position_m", "velocity_m_s", "spring_theta_rad", "drive_force_N"])
        for row in zip(result.time, result.position, result.velocity, result.spring_theta, result.drive_force):
            writer.writerow([f"{value:.6f}" for value in row])


def _plot_profiles(path: Path, result: SimulationResult) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(6, 6), sharex=True)
    axes[0].plot(result.time, result.position, label="Position", color="tab:blue")
    axes[0].set_ylabel("Distance (m)")
    axes[0].grid(True, linestyle=":", alpha=0.4)
    axes[1].plot(result.time, result.velocity, label="Velocity", color="tab:orange")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Speed (m/s)")
    axes[1].grid(True, linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def _render_motion(path: Path, result: SimulationResult) -> None:
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.set_xlim(0, max(result.position[-1] * 1.05, 1.5))
    ax.set_ylim(-0.3, 0.3)
    ax.axis("off")
    chassis = plt.Rectangle((0, -0.1), 0.4, 0.2, color="tab:green", alpha=0.8)
    ax.add_patch(chassis)

    def update(frame: int):
        x = result.position[min(frame, len(result.position) - 1)]
        chassis.set_x(float(x))
        return (chassis,)

    anim = animation.FuncAnimation(fig, update, frames=len(result.time), interval=40, blit=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(path, writer=animation.PillowWriter(fps=24))
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    del seed
    params = _load_parameters()
    result = _simulate_dynamics(params)
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    csv_path = artifacts_dir / "trajectory.csv"
    plot_path = artifacts_dir / "profiles.png"
    motion_gif = artifacts_dir / "motion.gif"
    _write_csv(csv_path, result)
    _plot_profiles(plot_path, result)
    _render_motion(motion_gif, result)

    travel_distance = float(result.position[-1])
    positive_velocities = result.velocity[result.velocity > 0]
    average_speed = float(np.mean(positive_velocities)) if positive_velocities.size else 0.0

    return {
        "artifacts": [str(csv_path), str(plot_path), str(motion_gif)],
        "distance_m": travel_distance,
        "runtime_s": float(result.time[-1]),
        "average_speed_m_s": average_speed,
        "notes": "Cart travels steadily with decreasing torque; ensure surface friction remains low for full range.",
    }


def build() -> None:
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad = _cad_module()
    cad.export_mesh(artifacts_dir / "self_propelled_cart.stl")


def evaluate() -> Dict[str, object]:
    params = _load_parameters()
    result = _simulate_dynamics(params)
    travel_distance = float(result.position[-1])
    stability_margin = params.spring_k_Nm * params.spring_max_theta_rad * params.gear_efficiency
    return {
        "practicality": {
            "distance_m": travel_distance,
            "runtime_s": float(result.time[-1]),
            "peak_velocity_m_s": float(result.velocity.max()) if result.velocity.size else 0.0,
            "energy_stored_J": stability_margin,
        },
        "ethics": {
            "risk": "Low — educational automation demo with minimal kinetic energy.",
            "mitigations": [
                "Add emergency stop pin to arrest spring drum.",
                "Shield gear train to prevent finger entanglement.",
            ],
        },
        "validated": {
            "ready_for_workshop": travel_distance > 10.0,
            "recommended_surface": "Smooth wood or linoleum floors",
        },
    }
