"""Mechanized trumpet automaton modeling and CAD integration."""

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

SLUG = "mechanical_trumpeter"
TITLE = "Mechanical Trumpeter"
STATUS = "concept_reconstruction"
SUMMARY = "Automated trumpeter automaton with programmable fingering and bellows-driven breath."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"
SPEED_OF_SOUND = 343.0  # m/s at 20 C


@dataclass
class TrumpeterParameters:
    bore_length_m: float
    bell_diameter_m: float
    mouthpiece_length_m: float
    plenum_pressure_kpa: float
    valve_latencies_s: List[float]
    note_sequence: List[int]
    breath_profile: List[float]
    timbre_noise_std: float


def _load_params() -> TrumpeterParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    return TrumpeterParameters(**data)


def _cad_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Failed to load trumpeter CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def _fundamental_frequency(length: float) -> float:
    # Quarter-wave approximation for brass instrument with bell flare correction.
    effective_length = length * 0.92
    return SPEED_OF_SOUND / (4.0 * effective_length)


def plan() -> Dict[str, object]:
    params = _load_params()
    fundamental = _fundamental_frequency(params.bore_length_m + params.mouthpiece_length_m)
    sequence_len = max(len(params.note_sequence), 1)
    latencies = np.array(params.valve_latencies_s, dtype=float)
    latency_bounds = [float(latencies.min()), float(latencies.max())] if latencies.size else [0.0, 0.0]
    return {
        "origin": {
            "folio": "Codex Atlanticus, f.194r",
            "summary": "Clockwork trumpeter automaton using programmable valves and bellows breath.",
            "sources": [
                {"title": "Codex Atlanticus Digital Archive", "link": "https://www.leonardodigitale.com/"},
                {"title": "Milan Court Festival Annals", "link": "https://lombardiadigitale.it/"},
            ],
            "missing_elements": [
                "Valve spring constants for rapid passages",
                "Bell alloy composition for partial control",
                "Programmable barrel pin geometry beyond three valves",
            ],
        },
        "goals": [
            "Simulate register changes across the programmed fanfare.",
            "Quantify breath pressure variation from bellows duty cycle.",
            "Deliver CAD for trumpet body, valves, and crank linkage.",
        ],
        "assumptions": {
            "fundamental_frequency_hz": fundamental,
            "plenum_pressure_kpa": params.plenum_pressure_kpa,
            "sequence_length": sequence_len,
            "valve_latency_bounds_s": latency_bounds,
        },
        "governing_equations": [
            "f0 = c / (4 * effective_length)",
            "pressure = plenum_pressure * breath_profile",
            "latency_adjusted_time = valve_latency + program_step",
        ],
        "validation_plan": [
            "Prototype valve actuation timing with spring-loaded followers.",
            "Measure bellows pressure waveform versus simulated profile.",
            "Compare harmonic spectrum against period trumpets.",
        ],
    }


def _simulate(params: TrumpeterParameters, seed: int) -> Dict[str, np.ndarray]:
    note_sequence = np.array(params.note_sequence, dtype=int)
    if note_sequence.size == 0:
        note_sequence = np.array([0, 2, 4, 5], dtype=int)
    breath = np.array(params.breath_profile, dtype=float)
    if breath.size == 0:
        breath = np.ones_like(note_sequence, dtype=float)
    if breath.size != note_sequence.size:
        breath = np.resize(breath, note_sequence.size)
    latencies = np.array(params.valve_latencies_s, dtype=float)
    if latencies.size == 0:
        latencies = np.full(note_sequence.size, 0.08)
    if latencies.size != note_sequence.size:
        latencies = np.resize(latencies, note_sequence.size)

    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, params.timbre_noise_std, size=note_sequence.size)
    fundamental = _fundamental_frequency(params.bore_length_m + params.mouthpiece_length_m)
    partials = 1.0 + note_sequence.astype(float) / 12.0
    ideal_frequency = fundamental * partials
    noisy_frequency = ideal_frequency * (1.0 + 0.002 * noise)
    pressure_profile = params.plenum_pressure_kpa * breath * (1.0 + 0.05 * noise)
    time_axis = np.cumsum(latencies)
    return {
        "time_s": time_axis,
        "partial_index": note_sequence.astype(float),
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


def _plot_profile(path: Path, data: Dict[str, np.ndarray]) -> None:
    fig, ax1 = plt.subplots(figsize=(6.0, 3.5))
    ax1.step(data["time_s"], data["ideal_frequency_hz"], where="post", color="tab:orange", label="Ideal frequency")
    ax1.step(data["time_s"], data["noisy_frequency_hz"], where="post", color="tab:blue", linestyle="--", label="With noise")
    ax1.set_xlabel("Cumulative time (s)")
    ax1.set_ylabel("Frequency (Hz)")
    ax1.grid(True, linestyle=":", alpha=0.4)
    ax2 = ax1.twinx()
    ax2.step(data["time_s"], data["pressure_kpa"], where="post", color="tab:green", label="Pressure")
    ax2.set_ylabel("Plenum pressure (kPa)")
    fig.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed)
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    csv_path = artifacts_dir / "fanfare_schedule.csv"
    plot_path = artifacts_dir / "frequency_pressure_profile.png"
    artifacts: List[str] = []
    if data["time_s"].size:
        _write_csv(csv_path, data)
        _plot_profile(plot_path, data)
        artifacts = [str(csv_path), str(plot_path)]
    mean_frequency = float(np.mean(data["ideal_frequency_hz"])) if data["ideal_frequency_hz"].size else 0.0
    pressure_std = float(np.std(data["pressure_kpa"])) if data["pressure_kpa"].size else 0.0
    return {
        "artifacts": artifacts,
        "mean_frequency_hz": mean_frequency,
        "pressure_std_kpa": pressure_std,
        "notes": "Tune valve cam offsets for tonguing articulation.",
    }


def build() -> None:
    params = asdict(_load_params())
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    cad_module.export_mesh(artifacts_dir / "mechanical_trumpeter.stl", params)


def evaluate() -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed=512)
    if not data["time_s"].size:
        mean_frequency = 0.0
        pressure_std = 0.0
        frequency_error = 0.0
    else:
        mean_frequency = float(np.mean(data["ideal_frequency_hz"]))
        pressure_std = float(np.std(data["pressure_kpa"]))
        frequency_error = float(np.mean(np.abs(data["noisy_frequency_hz"] - data["ideal_frequency_hz"])))
    return {
        "practicality": {
            "mean_frequency_hz": mean_frequency,
            "pressure_std_kpa": pressure_std,
            "frequency_error_hz": frequency_error,
        },
        "ethics": {
            "risk": "Low-risk performance automaton.",
            "mitigations": [
                "Guard rotating cranks to protect nearby performers.",
                "Limit peak sound pressure for indoor venues.",
            ],
        },
        "validated": {
            "stable_pitch": frequency_error < 2.0,
            "next_actions": [
                "Prototype valve clusters with interchangeable springs.",
            ],
        },
    }
