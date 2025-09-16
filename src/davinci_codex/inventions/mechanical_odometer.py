"""Mechanical odometer accuracy study and CAD integration."""

from __future__ import annotations

import csv
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml

from ..artifacts import ensure_artifact_dir

SLUG = "mechanical_odometer"
TITLE = "Mechanical Odometer Cart"
STATUS = "prototype_ready"
SUMMARY = "Distance-measuring cart with pebble-drop counter and error modeling."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"


@dataclass
class OdometerParameters:
    wheel_radius_m: float
    wheel_width_m: float
    drive_gear_teeth: int
    counter_gear_teeth: int
    bucket_capacity: int
    pebbles_per_drop: int
    slip_std_percent: float
    calibration_error_percent: float
    distance_grid_m: List[float]


def _load_params() -> OdometerParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    return OdometerParameters(**data)


def _cad_module():
    root = Path(__file__).resolve().parents[2]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Failed to load odometer CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    params = _load_params()
    circumference = 2.0 * np.pi * params.wheel_radius_m
    gear_ratio = params.drive_gear_teeth / params.counter_gear_teeth
    drop_distance = circumference * gear_ratio * params.pebbles_per_drop
    return {
        "origin": {
            "folio": "Codex Atlanticus, 1r",
            "summary": "Two-wheeled cart that drops pebbles to measure road distance via geared drums.",
            "sources": [
                {
                    "title": "Royal Collection Trust (public domain drawing)",
                    "link": "https://www.rct.uk/collection/912278",
                }
            ],
            "missing_elements": [
                "Exact tooth counts for the cascaded gears",
                "Pebble hopper capacity and reset mechanism",
                "Tolerances for wheel diameter and slip",
            ],
        },
        "goals": [
            "Quantify measurement error across 50–1000 m distances.",
            "Deliver build-ready CAD for wheel and gear housing.",
            "Publish calibration scripts for modern reproducibility.",
        ],
        "assumptions": {
            "wheel_radius_m": params.wheel_radius_m,
            "gear_ratio": gear_ratio,
            "bucket_capacity": params.bucket_capacity,
            "drop_distance_m": drop_distance,
            "slip_std_percent": params.slip_std_percent,
        },
        "governing_equations": [
            "distance_per_drop = 2πR * (drive_teeth / counter_teeth) * pebbles_per_drop",
            "recorded_distance = distance_per_drop * drops",
            "error_percent = (recorded_distance - actual_distance) / actual_distance * 100",
        ],
        "validation_plan": [
            "Push tests over surveyed tracks to measure accumulated error.",
            "Use laser rangefinder to validate per-drop distance calibration.",
            "3D scan wheel circumference after wear cycles.",
        ],
    }


def _simulate(params: OdometerParameters, seed: int) -> Dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    circumference = 2.0 * np.pi * params.wheel_radius_m
    gear_ratio = params.drive_gear_teeth / params.counter_gear_teeth
    distance_per_drop = circumference * gear_ratio * params.pebbles_per_drop
    actual = np.array(params.distance_grid_m, dtype=float)
    calibration_error = 1.0 + params.calibration_error_percent / 100.0
    noise = rng.normal(loc=0.0, scale=params.slip_std_percent / 100.0, size=actual.shape)
    measured_distance = actual * calibration_error * (1.0 + noise)
    drops_recorded = np.floor(measured_distance / distance_per_drop)
    recorded_distance = drops_recorded * distance_per_drop
    error_percent = (recorded_distance - actual) / actual * 100.0
    return {
        "actual_m": actual,
        "drops": drops_recorded,
        "recorded_m": recorded_distance,
        "error_percent": error_percent,
    }


def _write_csv(path: Path, data: Dict[str, np.ndarray]) -> None:
    keys = list(data.keys())
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(keys)
        for row in zip(*(data[key] for key in keys)):
            writer.writerow([f"{value:.6f}" for value in row])


def _plot_error(path: Path, data: Dict[str, np.ndarray]) -> None:
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.plot(data["actual_m"], data["error_percent"], marker="o", color="tab:purple")
    ax.axhline(0.0, color="black", linewidth=1.0)
    ax.fill_between(data["actual_m"], -1.0, 1.0, color="tab:green", alpha=0.15, label="±1% target")
    ax.set_xlabel("Actual distance (m)")
    ax.set_ylabel("Error (%)")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed)
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    csv_path = artifacts_dir / "measurement_error.csv"
    plot_path = artifacts_dir / "error_curve.png"
    _write_csv(csv_path, data)
    _plot_error(plot_path, data)
    return {
        "artifacts": [str(csv_path), str(plot_path)],
        "max_percent_error": float(np.abs(data["error_percent"]).max()),
        "distance_per_drop_m": float((2.0 * np.pi * params.wheel_radius_m) * (params.drive_gear_teeth / params.counter_gear_teeth) * params.pebbles_per_drop),
        "notes": "Calibrate wheel circumference seasonally to maintain <1% error.",
    }


def build() -> None:
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    cad_module.export_mesh(artifacts_dir / "mechanical_odometer.stl")


def evaluate() -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed=123)
    within_target = np.all(np.abs(data["error_percent"]) <= 2.0)
    return {
        "practicality": {
            "max_error_percent": float(np.abs(data["error_percent"]).max()),
            "drop_capacity_distance_m": float(data["drops"].max() * (2.0 * np.pi * params.wheel_radius_m) * (params.drive_gear_teeth / params.counter_gear_teeth)),
            "distance_grid_m": list(map(float, data["actual_m"])),
        },
        "ethics": {
            "risk": "Very low — passive measuring device.",
            "mitigations": [
                "Use rounded pebble edges to avoid projectile hazard.",
                "Ensure gears are covered to prevent pinch injuries.",
            ],
        },
        "validated": {
            "within_two_percent": bool(within_target),
            "next_actions": [
                "Field-validate on surveyed kilometer course.",
                "Swap pebbles for steel bearings to reduce bounce error.",
            ],
        },
    }
