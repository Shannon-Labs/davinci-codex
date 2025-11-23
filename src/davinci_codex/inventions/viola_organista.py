"""Viola organista wheel-bowed string ensemble modeling."""

from __future__ import annotations

import csv
import importlib.util
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml
from numpy.typing import NDArray

from ..artifacts import ensure_artifact_dir

SLUG = "viola_organista"
TITLE = "Viola Organista"
STATUS = "concept_reconstruction"
SUMMARY = "Continuous wheel-bowed keyboard capable of polyphonic string performance."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"


@dataclass
class ViolaParameters:
    string_lengths_m: List[float]
    string_tensions_n: List[float]
    string_linear_density_kg_per_m: List[float]
    wheel_surface_speed_m_per_s: float
    bow_contact_time_s: float
    key_velocity_profile: List[float]
    note_sequence: List[int]
    bow_noise_std: float
    bow_pressure_profile: List[float] = field(default_factory=list)


def _load_params() -> ViolaParameters:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    if "bow_pressure_profile" not in data:
        key_profile = data.get("key_velocity_profile", [0.8])
        data["bow_pressure_profile"] = [0.75 for _ in key_profile]
    return ViolaParameters(**data)


def _cad_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError("Failed to load viola organista CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def _fundamental_frequency(lengths: NDArray[np.float64], tensions: NDArray[np.float64], densities: NDArray[np.float64]) -> NDArray[np.float64]:
    return (1.0 / (2.0 * lengths)) * np.sqrt(tensions / densities)


def plan() -> Dict[str, object]:
    params = _load_params()
    lengths = np.asarray(params.string_lengths_m, dtype=float)  # type: NDArray[np.float64]
    tensions = np.asarray(params.string_tensions_n, dtype=float)  # type: NDArray[np.float64]
    densities = np.asarray(params.string_linear_density_kg_per_m, dtype=float)  # type: NDArray[np.float64]
    if not (lengths.size and tensions.size and densities.size):
        raise ValueError("Viola organista parameters must include string properties")
    if not (tensions.size == lengths.size and densities.size == lengths.size):
        raise ValueError("String arrays must be the same length")
    fundamentals = _fundamental_frequency(lengths, tensions, densities)
    sequence_len = max(len(params.note_sequence), 1)
    return {
        "origin": {
            "folio": "Codex Atlanticus, f.93v",
            "summary": "Keyboard instrument with rosined wheel bowing multiple strings.",
            "sources": [
                {"title": "Codex Atlanticus Digital Archive", "link": "https://www.leonardodigitale.com/"},
                {"title": "Krakow Exhibition Catalogue", "link": "https://mnk.pl/"},
            ],
            "missing_elements": [
                "Rosin composition for continuous wheel contact",
                "Key escapement spring rates",
                "String alloy selection for mixed timbre",
            ],
        },
        "goals": [
            "Predict pitch stability under wheel speed variations.",
            "Assess key attack shaping of sustained tones.",
            "Produce CAD concept for wheel, carriage, and string rail.",
        ],
        "assumptions": {
            "string_count": int(lengths.size),
            "fundamental_range_hz": [float(fundamentals.min()), float(fundamentals.max())],
            "wheel_surface_speed_m_per_s": params.wheel_surface_speed_m_per_s,
            "bow_contact_time_s": params.bow_contact_time_s,
            "sequence_length": sequence_len,
        },
        "governing_equations": [
            "f0 = (1 / 2L) * sqrt(T / mu)",
            "amplitude = key_velocity * wheel_speed_scaling",
            "contact_time = bow_contact_time_s",
        ],
        "validation_plan": [
            "Spin test the wheel to confirm surface speed tolerance.",
            "Measure attack envelopes on prototype string bank.",
            "Compare spectral content against viola da gamba references.",
        ],
    }


def _simulate(params: ViolaParameters, seed: int) -> Dict[str, np.ndarray]:
    lengths = np.asarray(params.string_lengths_m, dtype=float)  # type: NDArray[np.float64]
    tensions = np.asarray(params.string_tensions_n, dtype=float)  # type: NDArray[np.float64]
    densities = np.asarray(params.string_linear_density_kg_per_m, dtype=float)  # type: NDArray[np.float64]
    if lengths.size == 0 or tensions.size != lengths.size or densities.size != lengths.size:
        return {
            "time_s": np.array([], dtype=float),
            "string_index": np.array([], dtype=float),
            "ideal_frequency_hz": np.array([], dtype=float),
            "amplitude": np.array([], dtype=float),
            "surface_speed_m_per_s": np.array([], dtype=float),
        }

    fundamentals = _fundamental_frequency(lengths, tensions, densities)
    sequence = np.asarray(params.note_sequence, dtype=int)
    if sequence.size == 0:
        sequence = np.arange(lengths.size, dtype=int)
    indices = np.clip(sequence, 0, lengths.size - 1)
    key_profile = np.asarray(params.key_velocity_profile, dtype=float)
    if key_profile.size == 0:
        key_profile = np.ones_like(indices, dtype=float)
    if key_profile.size != indices.size:
        key_profile = np.resize(key_profile, indices.size)

    pressure_profile = np.asarray(params.bow_pressure_profile, dtype=float)
    if pressure_profile.size == 0:
        pressure_profile = np.ones_like(indices, dtype=float)
    if pressure_profile.size != indices.size:
        pressure_profile = np.resize(pressure_profile, indices.size)

    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, params.bow_noise_std, size=indices.size)
    ideal_frequency = fundamentals[indices]
    amplitude = np.clip(key_profile * pressure_profile * (1.0 + noise), 0.0, 1.5)
    time_axis = np.arange(indices.size, dtype=float) * params.bow_contact_time_s
    surface_speed = np.full_like(time_axis, params.wheel_surface_speed_m_per_s, dtype=float)
    return {
        "time_s": time_axis,
        "string_index": indices.astype(float),
        "ideal_frequency_hz": ideal_frequency,
        "amplitude": amplitude,
        "surface_speed_m_per_s": surface_speed,
    }


def _write_csv(path: Path, data: Dict[str, np.ndarray]) -> None:
    keys = list(data.keys())
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(keys)
        for row in zip(*(data[key] for key in keys)):
            writer.writerow([f"{float(value):.6f}" for value in row])


def _plot_sequence(path: Path, data: Dict[str, np.ndarray]) -> None:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.0, 5.0), sharex=True)
    ax1.step(data["time_s"], data["ideal_frequency_hz"], where="post", color="tab:purple")
    ax1.set_ylabel("Frequency (Hz)")
    ax1.grid(True, linestyle=":", alpha=0.4)

    ax2.step(data["time_s"], data["amplitude"], where="post", color="tab:green")
    ax2.set_xlabel("Program time (s)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True, linestyle=":", alpha=0.4)

    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed)
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    csv_path = artifacts_dir / "performance_profile.csv"
    plot_path = artifacts_dir / "amplitude_timeline.png"
    artifacts: List[str] = []
    if data["time_s"].size:
        _write_csv(csv_path, data)
        _plot_sequence(plot_path, data)
        artifacts = [str(csv_path), str(plot_path)]
    return {
        "artifacts": artifacts,
        "mean_frequency_hz": float(np.mean(data["ideal_frequency_hz"])) if data["ideal_frequency_hz"].size else 0.0,
        "amplitude_std": float(np.std(data["amplitude"])) if data["amplitude"].size else 0.0,
        "notes": "Explore alternate wheel surfaces for varied timbre.",
    }


def build() -> None:
    params = asdict(_load_params())
    artifacts_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    cad_module.export_mesh(artifacts_dir / "viola_organista.stl", params)


def evaluate() -> Dict[str, object]:
    params = _load_params()
    data = _simulate(params, seed=321)
    if not data["time_s"].size:
        mean_frequency = 0.0
        amplitude_variation = 0.0
    else:
        mean_frequency = float(np.mean(data["ideal_frequency_hz"]))
        amplitude_variation = float(np.std(data["amplitude"]))
    return {
        "practicality": {
            "mean_frequency_hz": mean_frequency,
            "amplitude_std": amplitude_variation,
            "wheel_surface_speed_m_per_s": params.wheel_surface_speed_m_per_s,
        },
        "ethics": {
            "risk": "Low-risk performance instrument.",
            "mitigations": [
                "Shield rotating wheel to avoid finger pinch points.",
                "Provide acoustic limits for hearing protection.",
            ],
        },
        "validated": {
            "expressive_control": amplitude_variation < 0.4,
            "next_actions": [
                "Prototype wheel bow with adjustable tensioning.",
            ],
        },
    }
