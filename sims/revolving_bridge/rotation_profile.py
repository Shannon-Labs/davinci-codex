"""Rotation profile generator for the revolving bridge simulations.

This script loads geometric and material parameters from ``parameters.yaml`` and
produces rotation metrics (moment, stress, deflection, torque, and stability
margin) across the deployment sweep. It writes a CSV table and lightweight plots
that can be embedded in reports.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml


@dataclass
class RotationParameters:
    span_length_m: float
    load_capacity_kg: float
    rotation_time_limit_s: float
    structure_mass_kg: float
    counterweight_tank_volume_m3: float
    counterweight_fluid_density_kg_m3: float
    youngs_modulus_pa: float
    moment_of_inertia_m4: float
    truss_depth_m: float
    deck_width_m: float
    angle_samples_deg: Sequence[float]
    gravity_m_s2: float
    safety_factor_target: float
    counterweight_arm_fraction: float
    load_distribution_factor: float


def load_parameters(path: Path | None = None) -> RotationParameters:
    """Load rotation parameters from YAML."""
    if path is None:
        path = Path(__file__).with_name("parameters.yaml")
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    return RotationParameters(
        span_length_m=float(raw["span_length_m"]),
        load_capacity_kg=float(raw["load_capacity_kg"]),
        rotation_time_limit_s=float(raw["rotation_time_limit_s"]),
        structure_mass_kg=float(raw["structure_mass_kg"]),
        counterweight_tank_volume_m3=float(raw["counterweight_tank_volume_m3"]),
        counterweight_fluid_density_kg_m3=float(raw["counterweight_fluid_density_kg_m3"]),
        youngs_modulus_pa=float(raw["youngs_modulus_pa"]),
        moment_of_inertia_m4=float(raw["moment_of_inertia_m4"]),
        truss_depth_m=float(raw["truss_depth_m"]),
        deck_width_m=float(raw["deck_width_m"]),
        angle_samples_deg=[float(angle) for angle in raw["angle_samples_deg"]],
        gravity_m_s2=float(raw["gravity_m_s2"]),
        safety_factor_target=float(raw["safety_factor_target"]),
        counterweight_arm_fraction=float(raw["counterweight_arm_fraction"]),
        load_distribution_factor=float(raw.get("load_distribution_factor", 1.0)),
    )


def compute_rotation_profile(params: RotationParameters) -> Dict[str, np.ndarray]:
    """Return rotation curves for the deployment sweep."""
    angles_deg = np.array(params.angle_samples_deg, dtype=float)
    angles_rad = np.deg2rad(angles_deg)

    load_force = params.load_capacity_kg * params.gravity_m_s2
    distributed_load = load_force / params.span_length_m * params.load_distribution_factor
    base_moment = distributed_load * params.span_length_m**2 / 8.0
    moment = base_moment * (np.cos(angles_rad) * 0.85 + 0.15)

    neutral_axis = params.truss_depth_m / 2.0
    stress = moment * neutral_axis / params.moment_of_inertia_m4

    deflection = (
        5
        * distributed_load
        * params.span_length_m**4
        / (384.0 * params.youngs_modulus_pa * params.moment_of_inertia_m4)
    )
    deflection_scaled = deflection * (np.cos(angles_rad) * 0.9 + 0.1)

    counterweight_mass = (
        params.counterweight_tank_volume_m3 * params.counterweight_fluid_density_kg_m3
    )
    inertia = (
        (params.structure_mass_kg + counterweight_mass)
        * (params.span_length_m * params.counterweight_arm_fraction) ** 2
    )
    theta_target = np.deg2rad(angles_deg[-1])
    alpha = 4.0 * theta_target / (params.rotation_time_limit_s**2)
    torque = inertia * alpha

    stability_margin = (
        counterweight_mass
        * params.gravity_m_s2
        * params.span_length_m
        * params.counterweight_arm_fraction
        - moment
    )

    return {
        "angles_deg": angles_deg,
        "moment_Nm": moment,
        "stress_Pa": stress,
        "deflection_m": deflection_scaled,
        "rotation_torque_Nm": np.full_like(moment, torque, dtype=float),
        "stability_margin_Nm": stability_margin,
    }


def acceptance_metrics(params: RotationParameters, rotation: Dict[str, np.ndarray]) -> Dict[str, float]:
    """Calculate acceptance metrics for test coverage."""
    span = params.span_length_m
    max_deflection = float(np.max(rotation["deflection_m"]))
    safety_factor = (
        params.load_capacity_kg
        * params.gravity_m_s2
        * (span / 4.0)
        * params.safety_factor_target
        / float(np.max(rotation["moment_Nm"]))
    )
    stability_margin = float(np.min(rotation["stability_margin_Nm"]))
    rotation_time = params.rotation_time_limit_s
    midspan_limit = span / 800.0

    return {
        "rotation_time_s": rotation_time,
        "max_deflection_m": max_deflection,
        "midspan_deflection_limit_m": midspan_limit,
        "safety_factor": safety_factor,
        "stability_margin_min_Nm": stability_margin,
    }


def write_rotation_csv(path: Path, rotation: Dict[str, np.ndarray]) -> None:
    headers = [
        "angle_deg",
        "moment_kNm",
        "stress_MPa",
        "deflection_mm",
        "torque_kNm",
        "stability_margin_kNm",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
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


def _plot_quantity(
    base_dir: Path,
    angles: np.ndarray,
    series: Iterable[np.ndarray],
    labels: Sequence[str],
    ylabel: str,
    filename: str,
) -> Path:
    fig, ax = plt.subplots(figsize=(6, 4))
    for values, label in zip(series, labels):
        ax.plot(angles, values, marker="o", label=label)
    ax.set_xlabel("Bridge angle (deg)")
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend(loc="best")
    fig.tight_layout()
    target = base_dir / filename
    fig.savefig(target, dpi=220)
    plt.close(fig)
    return target


def render_figures(base_dir: Path, rotation: Dict[str, np.ndarray]) -> List[Path]:
    """Render quick-look plots for documentation."""
    base_dir.mkdir(parents=True, exist_ok=True)
    angles = rotation["angles_deg"]
    plots: List[Path] = []
    plots.append(
        _plot_quantity(
            base_dir,
            angles,
            [rotation["stress_Pa"] / 1e6, rotation["deflection_m"] * 1000.0],
            ["Stress (MPa)", "Deflection (mm)"],
            "Stress / Deflection",
            "stress_deflection.png",
        )
    )
    plots.append(
        _plot_quantity(
            base_dir,
            angles,
            [rotation["rotation_torque_Nm"] / 1000.0],
            ["Torque (kNm)"],
            "Torque (kNm)",
            "rotation_torque.png",
        )
    )
    plots.append(
        _plot_quantity(
            base_dir,
            angles,
            [rotation["stability_margin_Nm"] / 1000.0],
            ["Stability margin (kNm)"],
            "Stability margin (kNm)",
            "stability_margin.png",
        )
    )
    return plots


def generate(output_dir: Path | None = None) -> Dict[str, object]:
    """Generate rotation artifacts and return metrics."""
    params = load_parameters()
    rotation = compute_rotation_profile(params)
    metrics = acceptance_metrics(params, rotation)

    if output_dir is None:
        output_dir = Path(__file__).with_name("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "rotation_metrics.csv"
    write_rotation_csv(csv_path, rotation)
    plots = render_figures(output_dir, rotation)

    return {
        "csv": csv_path,
        "plots": plots,
        "metrics": metrics,
        "parameters": params,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate revolving bridge rotation profile artifacts.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Directory to place generated CSVs and plots (default: sims/revolving_bridge/outputs)",
    )
    args = parser.parse_args()
    result = generate(args.output)

    csv_path = result["csv"]
    plots = result["plots"]
    metrics = result["metrics"]
    print(f"Wrote rotation metrics to {csv_path}")
    for plot in plots:
        print(f"Created plot {plot}")
    print("Acceptance metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
