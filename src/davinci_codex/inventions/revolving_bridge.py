"""Revolving bridge modernization module."""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path
from typing import Dict, List, cast

import matplotlib

matplotlib.use("Agg")
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from ..artifacts import ensure_artifact_dir

SLUG = "revolving_bridge"
TITLE = "Self-Supporting Revolving Bridge"
STATUS = "in_progress"
SUMMARY = "Portable rotating bridge with counterweight balance for rapid deployment."


def _cad_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Unable to locate CAD module for revolving bridge")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def _rotation_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "sims" / SLUG / "rotation_profile.py"
    spec = importlib.util.spec_from_file_location(f"sims.{SLUG}.rotation_profile", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Unable to locate rotation profile module for revolving bridge")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


_rotation = _rotation_module()
_PARAMS = _rotation.load_parameters()

SPAN_LENGTH_M = _PARAMS.span_length_m
LOAD_CAPACITY_KG = _PARAMS.load_capacity_kg
ROTATION_TIME_LIMIT_S = _PARAMS.rotation_time_limit_s
STRUCTURE_MASS_KG = _PARAMS.structure_mass_kg
COUNTERWEIGHT_TANK_VOLUME_M3 = _PARAMS.counterweight_tank_volume_m3
COUNTERWEIGHT_FLUID_DENSITY_KG_M3 = _PARAMS.counterweight_fluid_density_kg_m3
GRAVITY = _PARAMS.gravity_m_s2
YOUNGS_MODULUS_PA = _PARAMS.youngs_modulus_pa
MOMENT_OF_INERTIA_M4 = _PARAMS.moment_of_inertia_m4
TRUSS_DEPTH_M = _PARAMS.truss_depth_m
DECK_WIDTH_M = _PARAMS.deck_width_m
TARGET_SAFETY_FACTOR = _PARAMS.safety_factor_target


def plan() -> Dict[str, object]:
    """Outline modernization plan for the revolving bridge."""
    counterweight_mass = COUNTERWEIGHT_TANK_VOLUME_M3 * COUNTERWEIGHT_FLUID_DENSITY_KG_M3
    required_moment = 0.25 * LOAD_CAPACITY_KG * GRAVITY * SPAN_LENGTH_M
    available_counterweight_moment = counterweight_mass * GRAVITY * (SPAN_LENGTH_M / 2.0)

    return {
        "origin": {
            "folio": "Codex Atlanticus, folio 855r",
            "summary": "Swing bridge rotating about a central pivot for rapid river crossings.",
            "obstacles": [
                "Rope and timber limited stiffness and precision balance",
                "Manual rotation lacked predictable timing",
                "Counterweight calibration undocumented",
            ],
        },
        "modern_assumptions": {
            "span_length_m": SPAN_LENGTH_M,
            "load_capacity_kg": LOAD_CAPACITY_KG,
            "rotation_time_limit_s": ROTATION_TIME_LIMIT_S,
            "materials": "Warren truss using ASTM A992 steel with FRP decking",
            "counterweight": "Water-fillable tanks with automated pumping",
        },
        "governing_equations": [
            "Moment balance: M_bridge = M_counterweight",
            "Deflection: δ = (5 * W * L^4) / (384 * E * I)",
            "Rotation torque: T = I * α",
        ],
        "counterweight_plan": {
            "tank_volume_m3": COUNTERWEIGHT_TANK_VOLUME_M3,
            "fluid_density_kg_m3": COUNTERWEIGHT_FLUID_DENSITY_KG_M3,
            "counterweight_mass_kg": counterweight_mass,
            "moment_balance_ratio": available_counterweight_moment / required_moment,
        },
        "deployment_objectives": {
            "crew_size": 2,
            "deployment_time_min": 30,
            "power_source_kw": 10,
            "locking_mechanisms": ["0° slewing lock", "90° deployed lock", "hydraulic check valves"],
        },
    }


def _rotation_profile() -> Dict[str, np.ndarray]:
    rotation = _rotation.compute_rotation_profile(_PARAMS)
    return cast(Dict[str, np.ndarray], rotation)


def _load_capacity_curve() -> Dict[str, np.ndarray]:
    spans = np.linspace(8.0, 18.0, 20)
    base_capacity = LOAD_CAPACITY_KG
    capacity = base_capacity * (SPAN_LENGTH_M / spans) ** 1.8
    return {"span_m": spans, "capacity_kg": capacity}


def _write_rotation_csv(path: Path, rotation: Dict[str, np.ndarray]) -> None:
    headers = [
        "angle_deg",
        "moment_kNm",
        "stress_MPa",
        "deflection_mm",
        "torque_kNm",
        "stability_margin_kNm",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for idx in range(len(rotation["angles_deg"])):
            writer.writerow(
                [
                    f"{rotation['angles_deg'][idx]:.1f}",
                    f"{rotation['moment_Nm'][idx] / 1000.0:.2f}",
                    f"{rotation['stress_Pa'][idx] / 1e6:.2f}",
                    f"{rotation['deflection_m'][idx] * 1000.0:.2f}",
                    f"{rotation['rotation_torque_Nm'][idx] / 1000.0:.2f}",
                    f"{rotation['stability_margin_Nm'][idx] / 1000.0:.2f}",
                ]
            )


def _render_plots(base_dir: Path, rotation: Dict[str, np.ndarray], load_curve: Dict[str, np.ndarray]) -> List[Path]:
    artifacts: List[Path] = []

    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax2 = ax1.twinx()
    ax1.plot(rotation["angles_deg"], rotation["stress_Pa"] / 1e6, marker="o", color="tab:red", label="Stress (MPa)")
    ax2.plot(rotation["angles_deg"], rotation["deflection_m"] * 1000.0, marker="s", color="tab:blue", label="Deflection (mm)")
    ax1.set_xlabel("Bridge angle (deg)")
    ax1.set_ylabel("Stress (MPa)", color="tab:red")
    ax2.set_ylabel("Deflection (mm)", color="tab:blue")
    ax1.grid(True, linestyle=":", alpha=0.4)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    stress_plot = base_dir / "stress_deflection.png"
    fig.tight_layout()
    fig.savefig(stress_plot, dpi=220)
    plt.close(fig)
    artifacts.append(stress_plot)

    fig2, ax = plt.subplots(figsize=(6, 4))
    ax.plot(load_curve["span_m"], load_curve["capacity_kg"], color="tab:green", linewidth=2)
    ax.axvline(SPAN_LENGTH_M, color="tab:orange", linestyle="--", label="Design span")
    ax.set_xlabel("Span (m)")
    ax.set_ylabel("Load capacity (kg)")
    ax.set_title("Load capacity vs span length")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend()
    capacity_plot = base_dir / "load_capacity.png"
    fig2.tight_layout()
    fig2.savefig(capacity_plot, dpi=220)
    plt.close(fig2)
    artifacts.append(capacity_plot)

    fig3, ax = plt.subplots(figsize=(6, 4))
    ax.plot(rotation["angles_deg"], rotation["stability_margin_Nm"] / 1000.0, marker="^", color="tab:purple")
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_xlabel("Bridge angle (deg)")
    ax.set_ylabel("Stability margin (kNm)")
    ax.set_title("Dynamic stability margin during rotation")
    ax.grid(True, linestyle=":", alpha=0.4)
    stability_plot = base_dir / "stability_margin.png"
    fig3.tight_layout()
    fig3.savefig(stability_plot, dpi=220)
    plt.close(fig3)
    artifacts.append(stability_plot)

    return artifacts


def _render_animation(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-7, 7)
    ax.set_ylim(-1, 7)
    ax.set_aspect("equal")
    ax.axis("off")
    pivot = np.array([0.0, 0.0])
    deck_length = SPAN_LENGTH_M / 2.0
    line, = ax.plot([pivot[0], deck_length], [pivot[1], 0.0], linewidth=6, color="tab:blue")
    counterweight = plt.Circle((-2.0, 0.0), 0.6, color="tab:orange")
    ax.add_patch(counterweight)

    def _update(frame: int):
        angle = math.radians(frame * (90.0 / 40.0))
        x = deck_length * math.cos(angle)
        y = deck_length * math.sin(angle)
        line.set_data([pivot[0], x], [pivot[1], y])
        counterweight.center = (-2.0 * math.cos(angle / 2.0), -2.0 * math.sin(angle / 2.0))
        return line, counterweight

    anim = animation.FuncAnimation(fig, _update, frames=41, interval=70, blit=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(path, writer=animation.PillowWriter(fps=20))
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    """Generate structural curves, CSV data, and rotation animation."""
    del seed  # deterministic simulation
    sim_dir = ensure_artifact_dir(SLUG, subdir="sim")

    rotation = _rotation_profile()
    load_curve = _load_capacity_curve()
    csv_path = sim_dir / "rotation_metrics.csv"
    _write_rotation_csv(csv_path, rotation)

    artifacts = _render_plots(sim_dir, rotation, load_curve)
    animation_path = sim_dir / "rotation_animation.gif"
    _render_animation(animation_path)
    artifacts.append(animation_path)
    artifacts.append(csv_path)

    stress_peak = float(rotation["stress_Pa"].max() / 1e6)
    deflection_peak_mm = float(rotation["deflection_m"].max() * 1000.0)
    stability_min = float(rotation["stability_margin_Nm"].min() / 1000.0)

    return {
        "max_stress_MPa": stress_peak,
        "max_deflection_mm": deflection_peak_mm,
        "stability_margin_min_kNm": stability_min,
        "torque_requirement_kNm": float(rotation["rotation_torque_Nm"][0] / 1000.0),
        "load_capacity_curve": {
            "span_m": load_curve["span_m"].tolist(),
            "capacity_kg": load_curve["capacity_kg"].tolist(),
        },
        "artifacts": [str(p) for p in artifacts],
    }


def build() -> None:
    """Export parametric CAD mesh of the revolving bridge."""
    cad_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    mesh_path = cad_dir / "revolving_bridge_mesh.stl"
    cad_module.export_mesh(
        mesh_path,
        span=SPAN_LENGTH_M,
        deck_width=DECK_WIDTH_M,
        truss_height=TRUSS_DEPTH_M,
    )


def evaluate() -> Dict[str, object]:
    """Assess safety, deployment, and feasibility metrics."""
    wind_speed_design_kmh = 100.0
    wind_speed_design_ms = wind_speed_design_kmh / 3.6
    wind_pressure = 0.613 * wind_speed_design_ms**2
    projected_area = SPAN_LENGTH_M * TRUSS_DEPTH_M
    wind_force = wind_pressure * projected_area

    structural_capacity_N = LOAD_CAPACITY_KG * GRAVITY * TARGET_SAFETY_FACTOR
    bending_capacity = structural_capacity_N * (SPAN_LENGTH_M / 4.0)
    rotation_results = _rotation_profile()
    moment_demand = float(rotation_results["moment_Nm"].max())
    structural_fos = bending_capacity / moment_demand

    deployment_time_minutes = 30.0
    traditional_bailey_setup_hours = 6.0

    counterweight_mass = COUNTERWEIGHT_TANK_VOLUME_M3 * COUNTERWEIGHT_FLUID_DENSITY_KG_M3

    return {
        "safety": {
            "max_operational_wind_kmh": wind_speed_design_kmh,
            "wind_force_kN": wind_force / 1000.0,
            "structural_factor_of_safety": structural_fos,
            "locking_features": ["Automatic slewing lock", "Hydraulic over-center latch", "Manual brake"]
        },
        "deployment": {
            "crew_size": 2,
            "deployment_time_minutes": deployment_time_minutes,
            "traditional_temporary_bridge_hours": traditional_bailey_setup_hours,
            "time_savings_percent": (1.0 - (deployment_time_minutes / 60.0) / traditional_bailey_setup_hours) * 100.0,
            "power_requirement_kw": 8.5,
        },
        "economics": {
            "estimated_cost_million_usd": 2.1,
            "bailey_bridge_cost_million_usd": 2.6,
            "annual_maintenance_percent": 2.5,
        },
        "operational_scenarios": {
            "flood_response": "Deploy upstream of damaged crossings within 30 minutes.",
            "earthquake_relief": "Bypass collapsed road segments with minimal groundwork.",
            "wildland_fire_support": "Enable tanker truck access across small ravines.",
            "peacekeeping": "Provide civilian evacuation route without permanent works.",
            "counterweight_mass_kg": counterweight_mass,
        },
    }
