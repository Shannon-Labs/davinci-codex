"""Automatic pipe organ modeling and CAD integration."""

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

SLUG = "mechanical_organ"
TITLE = "Automatic Pipe Organ"
STATUS = "concept_reconstruction"
SUMMARY = "Self-playing pipe organ driven by pinned barrels and dual bellows."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"
SPEED_OF_SOUND = 343.0  # m/s at 20 C


@dataclass
class OrganParameters:
    pipe_lengths_m: List[float]
    pipe_diameters_m: List[float]
    bellows_pressure_kpa: float
    wind_chest_volume_l: float
    barrel_rotation_rpm: float
    note_schedule: List[int]
    airflow_noise_std: float


def _load_params() -> OrganParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    return OrganParameters(**data)


def _cad_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Failed to load organ CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    params = _load_params()
    pipe_lengths = np.array(params.pipe_lengths_m, dtype=float)
    if pipe_lengths.size == 0:
        raise ValueError("Organ parameters must include at least one pipe length")
    frequencies = SPEED_OF_SOUND / (2.0 * pipe_lengths)
    rotation_period = 60.0 / params.barrel_rotation_rpm if params.barrel_rotation_rpm else float("inf")
    schedule_steps = max(len(params.note_schedule), 1)
    step_duration = rotation_period / schedule_steps if np.isfinite(rotation_period) else float("inf")
    return {
        "origin": {
            "folio": "Codex Atlanticus, f.80r",
            "summary": "Pinned-barrel organ with dual bellows and programmable stops.",
            "sources": [
                {"title": "Codex Atlanticus Digital Archive", "link": "https://www.leonardodigitale.com/"},
                {"title": "Barcelona Codices Exhibition Notes", "link": "https://museunacional.cat/"},
            ],
            "missing_elements": [
                "Exact tooth count on the pin barrel drive",
                "Bellows leather composition and layering",
                "Acoustic lining specifications for the wind chest",
            ],
        },
        "goals": [
            "Validate pitch stability across the pinned program.",
            "Estimate bellows cadence needed for steady pressure.",
            "Provide CAD solid for organ chest, pipes, and barrel core.",
        ],
        "assumptions": {
            "pipe_count": int(pipe_lengths.size),
            "frequency_range_hz": [float(frequencies.min()), float(frequencies.max())],
            "bellows_pressure_kpa": params.bellows_pressure_kpa,
            "rotation_period_s": rotation_period,
            "step_duration_s": step_duration,
            "wind_chest_volume_l": params.wind_chest_volume_l,
        },
        "governing_equations": [
            "f0 = speed_of_sound / (2 * pipe_length)",
            "wind_flow = pressure * orifice_area / bellows_resistance",
            "step_duration = 60 / (rpm * program_steps)",
        ],
        "validation_plan": [
            "Bench-test bellows pressure against simulated duty cycle.",
            "Scan fabricated pipes for bore tolerance versus model.",
            "Audio spectrum comparison with historic organ stop samples.",
        ],
    }


def _simulate(params: OrganParameters, seed: int) -> Dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    pipe_lengths = np.array(params.pipe_lengths_m, dtype=float)
    if pipe_lengths.size == 0 or params.barrel_rotation_rpm <= 0:
        return {
            "time_s": np.array([], dtype=float),
            "note_index": np.array([], dtype=float),
            "ideal_frequency_hz": np.array([], dtype=float),
            "noisy_frequency_hz": np.array([], dtype=float),
            "pressure_kpa": np.array([], dtype=float),
        }

    fundamental = SPEED_OF_SOUND / (2.0 * pipe_lengths)
    schedule = np.array(params.note_schedule, dtype=int)
    if schedule.size == 0:
        schedule = np.array([0], dtype=int)
    indices = np.clip(schedule, 0, pipe_lengths.size - 1)
    rotation_period = 60.0 / params.barrel_rotation_rpm
    step_duration = rotation_period / schedule.size
    time_axis = np.arange(schedule.size, dtype=float) * step_duration
    pressure_noise = rng.normal(0.0, params.airflow_noise_std, size=schedule.size)
    ideal_frequency = fundamental[indices]
    noisy_frequency = ideal_frequency * (1.0 + 0.003 * pressure_noise)
    pressure_profile = params.bellows_pressure_kpa * (1.0 + 0.05 * pressure_noise)
    return {
        "time_s": time_axis,
        "note_index": indices.astype(float),
        "ideal_frequency_hz": ideal_frequency,
        "noisy_frequency_hz": noisy_frequency,
        "pressure_kpa": pressure_profile,
    }


def _write_csv(path: Path, data: Dict[str, np.ndarray]) -> None:
    keys = list(data.keys())
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(keys)
        for row in zip(*(data[key] for key in keys)):
            writer.writerow([f"{float(value):.6f}" for value in row])


def _plot_schedule(path: Path, data: Dict[str, np.ndarray]) -> None:
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    ax.step(data["time_s"], data["ideal_frequency_hz"], where="post", label="Ideal", color="tab:blue")
    ax.step(data["time_s"], data["noisy_frequency_hz"], where="post", label="With pressure noise", color="tab:orange")
    ax.set_xlabel("Program time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed)
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    csv_path = artifacts_dir / "program_schedule.csv"
    plot_path = artifacts_dir / "frequency_profile.png"
    artifacts: List[str] = []
    if data["time_s"].size:
        _write_csv(csv_path, data)
        _plot_schedule(plot_path, data)
        artifacts = [str(csv_path), str(plot_path)]
    return {
        "artifacts": artifacts,
        "mean_frequency_hz": float(np.mean(data["ideal_frequency_hz"])) if data["ideal_frequency_hz"].size else 0.0,
        "pressure_variation_kpa": float(np.std(data["pressure_kpa"])) if data["pressure_kpa"].size else 0.0,
        "notes": "Tune pipe scaling to match target temperaments.",
    }


def build() -> None:
    params = asdict(_load_params())
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    cad_module.export_mesh(artifacts_dir / "mechanical_organ.stl", params)


def evaluate() -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed=123)
    if not data["time_s"].size:
        mean_frequency = 0.0
        frequency_error = 0.0
        pressure_variation = 0.0
    else:
        mean_frequency = float(np.mean(data["ideal_frequency_hz"]))
        frequency_error = float(np.mean(np.abs(data["noisy_frequency_hz"] - data["ideal_frequency_hz"])))
        pressure_variation = float(np.std(data["pressure_kpa"]))
    return {
        "practicality": {
            "mean_frequency_hz": mean_frequency,
            "frequency_error_hz": frequency_error,
            "pressure_std_kpa": pressure_variation,
        },
        "ethics": {
            "risk": "Low-risk cultural instrument.",
            "mitigations": [
                "Limit sound pressure levels for indoor performance.",
                "Include emergency stop on bellows drive.",
            ],
        },
        "validated": {
            "stable_pitch": frequency_error < 1.5,
            "next_actions": [
                "Prototype bellows linkage with adjustable valves.",
            ],
        },
    }
