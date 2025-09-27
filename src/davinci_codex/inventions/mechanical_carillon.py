"""Mechanical carillon timing simulation and CAD integration."""

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

SLUG = "mechanical_carillon"
TITLE = "Mechanical Carillon"
STATUS = "concept_reconstruction"
SUMMARY = "Rotating drum that indexes bell strikers for programmable chimes."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"
GRAVITY = 9.80665


@dataclass
class CarillonParameters:
    bell_masses_kg: List[float]
    bell_frequencies_hz: List[float]
    striker_mass_kg: float
    striker_arm_length_m: float
    drum_radius_m: float
    rotation_speed_rpm: float
    strike_sequence: List[int]
    timing_noise_std: float


def _load_params() -> CarillonParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    return CarillonParameters(**data)


def _cad_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Failed to load carillon CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    params = _load_params()
    masses = np.array(params.bell_masses_kg, dtype=float)
    if masses.size == 0:
        raise ValueError("Carillon parameters require at least one bell mass")
    freqs = np.array(params.bell_frequencies_hz, dtype=float)
    if freqs.size != masses.size:
        raise ValueError("Bell mass and frequency arrays must align")
    rotation_period = 60.0 / params.rotation_speed_rpm if params.rotation_speed_rpm else float("inf")
    sequence_len = max(len(params.strike_sequence), 1)
    step_interval = rotation_period / sequence_len if np.isfinite(rotation_period) else float("inf")
    striker_tip_speed = 2.0 * np.pi * params.drum_radius_m * params.rotation_speed_rpm / 60.0
    return {
        "origin": {
            "folio": "Codex Atlanticus, f.30r",
            "summary": "Clockwork-driven carillon with rotating drum that deploys bell strikers.",
            "sources": [
                {"title": "Codex Atlanticus Digital Archive", "link": "https://www.leonardodigitale.com/"},
                {"title": "Madrid Codices Performance Notes", "link": "https://bibliotecadigitalhispanica.bne.es/"},
            ],
            "missing_elements": [
                "Exact hammer cam profiles",
                "Tower mounting clearances",
                "Bell bronze composition for tuned partials",
            ],
        },
        "goals": [
            "Simulate strike timing and impact energy across the sequence.",
            "Generate CAD for drum, bell rack, and striker assembly.",
            "Assess practical cadence for civic chime programming.",
        ],
        "assumptions": {
            "bell_count": int(masses.size),
            "frequency_range_hz": [float(freqs.min()), float(freqs.max())],
            "rotation_period_s": rotation_period,
            "step_interval_s": step_interval,
            "striker_tip_speed_m_per_s": striker_tip_speed,
        },
        "governing_equations": [
            "rotation_period = 60 / rotation_speed_rpm",
            "tip_speed = 2 * pi * drum_radius * rotation_speed_rpm / 60",
            "impact_energy = 0.5 * striker_mass * tip_speed^2",
        ],
        "validation_plan": [
            "Time strikes on prototype drum to compare with simulations.",
            "Measure bell decay envelopes versus reference chimes.",
            "Verify striker arm strength with finite element checks.",
        ],
    }


def _simulate(params: CarillonParameters, seed: int) -> Dict[str, np.ndarray]:
    masses = np.array(params.bell_masses_kg, dtype=float)
    freqs = np.array(params.bell_frequencies_hz, dtype=float)
    if masses.size == 0 or freqs.size != masses.size or params.rotation_speed_rpm <= 0:
        return {
            "time_s": np.array([], dtype=float),
            "bell_index": np.array([], dtype=float),
            "ideal_frequency_hz": np.array([], dtype=float),
            "impact_energy_j": np.array([], dtype=float),
        }

    rotation_period = 60.0 / params.rotation_speed_rpm
    sequence = np.array(params.strike_sequence, dtype=int)
    if sequence.size == 0:
        sequence = np.arange(masses.size, dtype=int)
    indices = np.clip(sequence, 0, masses.size - 1)
    step_interval = rotation_period / sequence.size
    time_axis = np.arange(sequence.size, dtype=float) * step_interval
    rng = np.random.default_rng(seed)
    jitter = rng.normal(0.0, params.timing_noise_std, size=sequence.size)
    time_with_noise = np.clip(time_axis + jitter, 0.0, rotation_period)
    tip_speed = 2.0 * np.pi * params.drum_radius_m * params.rotation_speed_rpm / 60.0
    impact_energy = 0.5 * params.striker_mass_kg * tip_speed**2 * np.ones_like(time_axis)
    return {
        "time_s": time_with_noise,
        "bell_index": indices.astype(float),
        "ideal_frequency_hz": freqs[indices],
        "impact_energy_j": impact_energy,
    }


def _write_csv(path: Path, data: Dict[str, np.ndarray]) -> None:
    keys = list(data.keys())
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(keys)
        for row in zip(*(data[key] for key in keys)):
            writer.writerow([f"{float(value):.6f}" for value in row])


def _plot_sequence(path: Path, data: Dict[str, np.ndarray]) -> None:
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    ax.scatter(data["time_s"], data["ideal_frequency_hz"], c=data["bell_index"], cmap="viridis", s=40)
    ax.set_xlabel("Program time (s)")
    ax.set_ylabel("Bell frequency (Hz)")
    ax.grid(True, linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed)
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    csv_path = artifacts_dir / "strike_schedule.csv"
    plot_path = artifacts_dir / "frequency_scatter.png"
    artifacts: List[str] = []
    if data["time_s"].size:
        _write_csv(csv_path, data)
        _plot_sequence(plot_path, data)
        artifacts = [str(csv_path), str(plot_path)]
    mean_energy = float(np.mean(data["impact_energy_j"])) if data["impact_energy_j"].size else 0.0
    timing_std = float(np.std(data["time_s"])) if data["time_s"].size else 0.0
    return {
        "artifacts": artifacts,
        "mean_impact_energy_j": mean_energy,
        "timing_std_s": timing_std,
        "notes": "Tune cam lobes to vary bell dynamics.",
    }


def build() -> None:
    params = asdict(_load_params())
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    cad_module.export_mesh(artifacts_dir / "mechanical_carillon.stl", params)


def evaluate() -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed=321)
    if not data["time_s"].size:
        timing_std = 0.0
        mean_energy = 0.0
    else:
        timing_std = float(np.std(data["time_s"]))
        mean_energy = float(np.mean(data["impact_energy_j"]))
    gravity_load = params.striker_mass_kg * GRAVITY * params.striker_arm_length_m
    return {
        "practicality": {
            "mean_impact_energy_j": mean_energy,
            "timing_std_s": timing_std,
            "gravity_load_n": gravity_load,
        },
        "ethics": {
            "risk": "Low-risk civic signaling instrument.",
            "mitigations": [
                "Shield rotating drum mechanisms from public contact.",
                "Provide manual brake for tower maintenance crews.",
            ],
        },
        "validated": {
            "consistent_timing": timing_std < 0.2,
            "next_actions": [
                "Prototype hammer spring with adjustable damping.",
            ],
        },
    }
