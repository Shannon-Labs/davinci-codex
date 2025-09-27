"""Programmable flute mechanism modeling and CAD integration."""

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

SLUG = "programmable_flute"
TITLE = "Programmable Flute"
STATUS = "concept_reconstruction"
SUMMARY = "Cam-driven recorder with automatic fingering and regulated airflow."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"
SPEED_OF_SOUND = 343.0  # m/s at standard conditions


@dataclass
class FluteParameters:
    pipe_lengths_m: List[float]
    hole_positions_m: List[float]
    barrel_rotation_rpm: float
    cam_lobe_count: int
    airflow_rate_lps: float
    valve_latency_s: float
    note_sequence: List[int]
    air_noise_std: float


def _load_params() -> FluteParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    return FluteParameters(**data)


def _cad_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError("Failed to load programmable flute CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    params = _load_params()
    pipe_lengths = np.asarray(params.pipe_lengths_m, dtype=float)
    if pipe_lengths.size == 0:
        raise ValueError("Programmable flute requires pipe lengths")
    frequencies = SPEED_OF_SOUND / (2.0 * pipe_lengths)
    rotation_period = 60.0 / params.barrel_rotation_rpm if params.barrel_rotation_rpm else float("inf")
    program_steps = max(len(params.note_sequence), 1)
    step_duration = rotation_period / program_steps if np.isfinite(rotation_period) else float("inf")
    return {
        "origin": {
            "folio": "Codex Atlanticus, f.572r",
            "summary": "Automated flute with cam-controlled finger holes and bellows regulation.",
            "sources": [
                {"title": "Codex Atlanticus Digital Archive", "link": "https://www.leonardodigitale.com/"},
                {"title": "Madrid Codices Commentary", "link": "https://bibliotecadigitalhispanica.bne.es/"},
            ],
            "missing_elements": [
                "Precise cam timing for ornamented passages",
                "Valve leather thickness and spring preload",
                "Recorder bore taper data",
            ],
        },
        "goals": [
            "Quantify pitch drift under airflow fluctuations.",
            "Check cam timing against valve latency margins.",
            "Deliver CAD reference for cam barrel and flute body.",
        ],
        "assumptions": {
            "pipe_count": int(pipe_lengths.size),
            "frequency_range_hz": [float(frequencies.min()), float(frequencies.max())],
            "rotation_period_s": rotation_period,
            "step_duration_s": step_duration,
            "airflow_rate_lps": params.airflow_rate_lps,
        },
        "governing_equations": [
            "f0 = speed_of_sound / (2 * pipe_length)",
            "step_duration = 60 / (rpm * program_steps)",
            "latency_adjusted_time = contact_time + valve_latency_s",
        ],
        "validation_plan": [
            "Prototype valve timing with adjustable cams.",
            "Measure airflow stability across bellows strokes.",
            "Record audio comparison versus human-played recorder.",
        ],
    }


def _simulate(params: FluteParameters, seed: int) -> Dict[str, np.ndarray]:
    pipe_lengths = np.asarray(params.pipe_lengths_m, dtype=float)
    if pipe_lengths.size == 0 or params.barrel_rotation_rpm <= 0:
        return {
            "time_s": np.array([], dtype=float),
            "note_index": np.array([], dtype=float),
            "ideal_frequency_hz": np.array([], dtype=float),
            "noisy_frequency_hz": np.array([], dtype=float),
            "valve_delay_s": np.array([], dtype=float),
        }

    schedule = np.asarray(params.note_sequence, dtype=int)
    if schedule.size == 0:
        schedule = np.arange(pipe_lengths.size, dtype=int)
    indices = np.clip(schedule, 0, pipe_lengths.size - 1)
    rotation_period = 60.0 / params.barrel_rotation_rpm
    step_duration = rotation_period / schedule.size
    time_axis = np.arange(schedule.size, dtype=float) * step_duration

    rng = np.random.default_rng(seed)
    airflow_noise = rng.normal(0.0, params.air_noise_std, size=schedule.size)
    fundamental = SPEED_OF_SOUND / (2.0 * pipe_lengths)
    ideal_frequency = fundamental[indices]
    noisy_frequency = ideal_frequency * (1.0 + 0.0025 * airflow_noise)
    valve_delay = params.valve_latency_s * (1.0 + 0.1 * airflow_noise)
    adjusted_time = time_axis + valve_delay
    return {
        "time_s": adjusted_time,
        "note_index": indices.astype(float),
        "ideal_frequency_hz": ideal_frequency,
        "noisy_frequency_hz": noisy_frequency,
        "valve_delay_s": valve_delay,
    }


def _write_csv(path: Path, data: Dict[str, np.ndarray]) -> None:
    keys = list(data.keys())
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(keys)
        for row in zip(*(data[key] for key in keys)):
            writer.writerow([f"{float(value):.6f}" for value in row])


def _plot_program(path: Path, data: Dict[str, np.ndarray]) -> None:
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    ax.step(data["time_s"], data["ideal_frequency_hz"], where="post", label="Ideal", color="tab:blue")
    ax.step(data["time_s"], data["noisy_frequency_hz"], where="post", label="With airflow noise", color="tab:red")
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
    plot_path = artifacts_dir / "frequency_timeline.png"
    artifacts: List[str] = []
    if data["time_s"].size:
        _write_csv(csv_path, data)
        _plot_program(plot_path, data)
        artifacts = [str(csv_path), str(plot_path)]
    return {
        "artifacts": artifacts,
        "mean_frequency_hz": float(np.mean(data["ideal_frequency_hz"])) if data["ideal_frequency_hz"].size else 0.0,
        "valve_delay_std_s": float(np.std(data["valve_delay_s"])) if data["valve_delay_s"].size else 0.0,
        "notes": "Tune cam lobes for ornamented passages.",
    }


def build() -> None:
    params = asdict(_load_params())
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    cad_module.export_mesh(artifacts_dir / "programmable_flute.stl", params)


def evaluate() -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed=222)
    if not data["time_s"].size:
        mean_frequency = 0.0
        frequency_error = 0.0
        valve_variation = 0.0
    else:
        mean_frequency = float(np.mean(data["ideal_frequency_hz"]))
        frequency_error = float(np.mean(np.abs(data["noisy_frequency_hz"] - data["ideal_frequency_hz"])))
        valve_variation = float(np.std(data["valve_delay_s"]))
    return {
        "practicality": {
            "mean_frequency_hz": mean_frequency,
            "frequency_error_hz": frequency_error,
            "valve_delay_std_s": valve_variation,
        },
        "ethics": {
            "risk": "Low-risk programmed instrument.",
            "mitigations": [
                "Limit airflow pressure to reduce acoustic fatigue.",
                "Provide manual override for performer intervention.",
            ],
        },
        "validated": {
            "stable_pitch": frequency_error < 1.0,
            "next_actions": [
                "Prototype cam barrel with adjustable followers.",
            ],
        },
    }
