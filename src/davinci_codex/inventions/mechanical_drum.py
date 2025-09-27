"""Mechanical drum rhythm simulation and CAD integration."""

from __future__ import annotations

import csv
import importlib.util
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml

from ..artifacts import ensure_artifact_dir

SLUG = "mechanical_drum"
TITLE = "Mechanical Drum"
STATUS = "prototype_ready"
SUMMARY = "Programmable percussion device with cam barrels for rhythm patterns."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"


@dataclass
class DrumParameters:
    drum_radius_m: float
    drum_length_m: float
    pin_count: int
    rotation_speed_rpm: float
    gear_ratio: float
    beat_angles_deg: List[float]
    noise_std: float


def _load_params() -> DrumParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    return DrumParameters(**data)


def _cad_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Failed to load drum CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    params = _load_params()
    active_pin_count = len(params.beat_angles_deg)
    nominal_pin_count = max(params.pin_count, active_pin_count)
    rotation_period = 60.0 / params.rotation_speed_rpm if params.rotation_speed_rpm else float("inf")
    surface_speed = 2.0 * np.pi * params.drum_radius_m * params.rotation_speed_rpm / 60.0
    pin_density = active_pin_count / params.drum_length_m if params.drum_length_m else 0.0
    return {
        "origin": {
            "folio": "Codex Atlanticus, f.837r",
            "summary": "Programmable mechanical drum with pinned barrels for automated percussion.",
            "sources": [
                {
                    "title": "Codex Atlanticus Digital Archive",
                    "link": "https://www.leonardodigitale.com/",
                }
            ],
            "missing_elements": [
                "Exact pin patterns for specific rhythms",
                "Power source details (hand crank or spring)",
                "Material tolerances for sound quality",
            ],
        },
        "goals": [
            "Simulate rhythm patterns and timing accuracy.",
            "Generate CAD for drum barrel and frame.",
            "Evaluate sound production consistency.",
        ],
        "assumptions": {
            "drum_radius_m": params.drum_radius_m,
            "drum_length_m": params.drum_length_m,
            "rotation_speed_rpm": params.rotation_speed_rpm,
            "rotation_period_s": rotation_period,
            "surface_speed_m_per_s": surface_speed,
            "gear_ratio": params.gear_ratio,
            "nominal_pin_count": nominal_pin_count,
            "active_pin_count": active_pin_count,
            "pin_density_per_meter": pin_density,
        },
        "governing_equations": [
            "rotation_period = 60 / rotation_speed_rpm",
            "beat_interval_s = rotation_period / active_pin_count",
            "surface_speed_m_per_s = 2 * pi * drum_radius_m * rotation_speed_rpm / 60",
        ],
        "validation_plan": [
            "Compare simulated rhythms to audio recordings.",
            "3D print and test physical model for timing.",
        ],
    }


def _simulate(params: DrumParameters, seed: int) -> Dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    time_per_rotation = 60.0 / params.rotation_speed_rpm if params.rotation_speed_rpm else float("inf")
    beat_angles = np.array(params.beat_angles_deg, dtype=float)
    if beat_angles.size == 0 or not np.isfinite(time_per_rotation):
        return {
            "ideal_times_s": np.array([], dtype=float),
            "noisy_times_s": np.array([], dtype=float),
            "ideal_intervals_s": np.array([], dtype=float),
            "noisy_intervals_s": np.array([], dtype=float),
        }

    angles_rad = np.deg2rad(beat_angles % 360.0)
    beat_times = np.sort(angles_rad / (2.0 * np.pi) * time_per_rotation)
    noise = rng.normal(0.0, params.noise_std, size=beat_times.shape)
    noisy_times = np.clip(beat_times + noise, 0.0, time_per_rotation)
    ideal_intervals = np.diff(np.append(beat_times, time_per_rotation))
    noisy_intervals = np.diff(np.append(noisy_times, time_per_rotation))
    return {
        "ideal_times_s": beat_times,
        "noisy_times_s": noisy_times,
        "ideal_intervals_s": ideal_intervals,
        "noisy_intervals_s": noisy_intervals,
    }


def _write_csv(path: Path, data: Dict[str, np.ndarray]) -> None:
    keys = list(data.keys())
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(keys)
        for row in zip(*(data[key] for key in keys)):
            writer.writerow([f"{value:.6f}" for value in row])


def _plot_rhythm(path: Path, data: Dict[str, np.ndarray]) -> None:
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.vlines(data["ideal_times_s"], 0, 1, colors="blue", label="Ideal")
    ax.vlines(data["noisy_times_s"], 0, 0.5, colors="red", label="Noisy")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Beat")
    ax.set_yticks([])
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed)
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    csv_path = artifacts_dir / "rhythm_times.csv"
    plot_path = artifacts_dir / "rhythm_plot.png"
    if data["ideal_times_s"].size:
        _write_csv(csv_path, data)
        _plot_rhythm(plot_path, data)
        artifacts = [str(csv_path), str(plot_path)]
    else:
        artifacts = []
    mean_interval = float(np.mean(data["ideal_intervals_s"])) if data["ideal_intervals_s"].size else 0.0
    timing_jitter = float(np.std(data["noisy_intervals_s"] - data["ideal_intervals_s"])) if data["ideal_intervals_s"].size else 0.0
    surface_speed = 2.0 * np.pi * params.drum_radius_m * params.rotation_speed_rpm / 60.0
    return {
        "artifacts": artifacts,
        "mean_interval_s": mean_interval,
        "timing_jitter_s": timing_jitter,
        "surface_speed_m_per_s": surface_speed,
        "notes": "Add more patterns for complex rhythms.",
    }


def build() -> None:
    params = asdict(_load_params())
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    cad_module.export_mesh(artifacts_dir / "mechanical_drum.stl", params)


def evaluate() -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed=123)
    timing_error = float(np.mean(np.abs(data["noisy_times_s"] - data["ideal_times_s"]))) if data["ideal_times_s"].size else 0.0
    jitter = float(np.std(data["noisy_intervals_s"] - data["ideal_intervals_s"])) if data["ideal_intervals_s"].size else 0.0
    mean_interval = float(np.mean(data["ideal_intervals_s"])) if data["ideal_intervals_s"].size else 0.0
    surface_speed = 2.0 * np.pi * params.drum_radius_m * params.rotation_speed_rpm / 60.0
    return {
        "practicality": {
            "mean_interval_s": mean_interval,
            "timing_error_s": timing_error,
            "timing_jitter_s": jitter,
            "surface_speed_m_per_s": surface_speed,
        },
        "ethics": {
            "risk": "Low-risk entertainment device.",
            "mitigations": [
                "Enclose moving parts to prevent injury.",
            ],
        },
        "validated": {
            "low_error": timing_error < 0.1,
            "next_actions": [
                "Test with actual sound generation.",
            ],
        },
    }
