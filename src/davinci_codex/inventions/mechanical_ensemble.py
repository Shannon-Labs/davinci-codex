"""Leonardo''s mechanical instrument ensemble orchestrator."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np

from ..artifacts import ensure_artifact_dir
from ..core.audio import render_score_to_wav
from ..core.spectral import (
    SpectralProfile,
    combine_profiles,
    profile_from_frequencies,
    profile_from_intervals,
)
from . import (
    mechanical_carillon,
    mechanical_drum,
    mechanical_organ,
    mechanical_trumpeter,
    programmable_flute,
    viola_organista,
)

SLUG = "mechanical_ensemble"
TITLE = "Leonardo Mechanical Ensemble"
STATUS = "concept_reconstruction"
SUMMARY = "Coordinated simulations for Leonardo''s automated musical inventions."

_INSTRUMENTS = (
    ("mechanical_drum", mechanical_drum),
    ("mechanical_organ", mechanical_organ),
    ("viola_organista", viola_organista),
    ("programmable_flute", programmable_flute),
    ("mechanical_carillon", mechanical_carillon),
    ("mechanical_trumpeter", mechanical_trumpeter),
)

_BEATS_PER_MEASURE = 4
_SECONDS_EPS = 1e-6


def _empty_profile() -> SpectralProfile:
    return SpectralProfile(0.0, 0.0, 0.0, [], [], -np.inf, 0.0)


@dataclass
class InstrumentSpectralSummary:
    slug: str
    profile: SpectralProfile
    notes: str


def _profile_for_module(slug: str, module) -> InstrumentSpectralSummary:
    """Derive a spectral profile from an instrument module."""

    notes = ""
    try:
        params = module._load_params()  # type: ignore[attr-defined]
    except Exception as exc:  # pragma: no cover - catastrophic failure
        return InstrumentSpectralSummary(slug, _empty_profile(), f"parameter load failed: {exc}")

    profile = _empty_profile()
    try:
        data = module._simulate(params, seed=0)  # type: ignore[attr-defined]
        if "ideal_intervals_s" in data:
            intervals = np.asarray(data["ideal_intervals_s"], dtype=float)
            profile = profile_from_intervals(intervals)
            notes = "Derived from beat intervals"
        elif "ideal_frequency_hz" in data:
            freqs = np.asarray(data["ideal_frequency_hz"], dtype=float)
            weights = None
            if "pressure_kpa" in data:
                weights = np.asarray(data["pressure_kpa"], dtype=float)
            elif "impact_energy_j" in data:
                weights = np.asarray(data["impact_energy_j"], dtype=float)
            elif "amplitude" in data:
                weights = np.asarray(data["amplitude"], dtype=float)
            profile = profile_from_frequencies(freqs, weights)
            notes = "Derived from simulated pitch track"
    except Exception as exc:  # pragma: no cover - simulation failure
        notes = f"spectral extraction failed: {exc}"

    return InstrumentSpectralSummary(slug, profile, notes)


def plan() -> Dict[str, object]:
    """Assemble a high-level plan across all instruments."""

    components: Dict[str, Dict[str, object]] = {}
    for slug, module in _INSTRUMENTS:
        instrument_plan = module.plan()
        components[slug] = {
            "title": getattr(module, "TITLE", slug.replace("_", " ").title()),
            "status": getattr(module, "STATUS", "unknown"),
            "goals": instrument_plan.get("goals", []),
            "assumptions": instrument_plan.get("assumptions", {}),
        }

    return {
        "origin": {
            "folio": "Composite from Codex Atlanticus folios",
            "summary": "Workflow to synchronize da Vinci''s automated musical inventions into a single ensemble.",
            "sources": [
                {"title": "Codex Atlanticus Digital Archive", "link": "https://www.leonardodigitale.com/"},
                {"title": "Festival Records of the Sforza Court", "link": "https://milanofestival.org/"},
            ],
            "missing_elements": [
                "Common tempo reference between instruments",
                "Shared power transmission layout",
                "Acoustic staging and reflection management",
            ],
        },
        "goals": [
            "Align tempo and cadence across percussive, wind, and string automata.",
            "Balance spectral energy for blended court performances.",
            "Bundle CAD exports for a single stage deployment.",
        ],
        "components": components,
    }


def _gather_spectral_profiles() -> List[InstrumentSpectralSummary]:
    return [_profile_for_module(slug, module) for slug, module in _INSTRUMENTS]


def _write_spectral_csv(path: Path, summaries: List[InstrumentSpectralSummary]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "slug",
                "fundamental_hz",
                "centroid_hz",
                "bandwidth_hz",
                "loudness_db",
                "decay_slope_db_per_harmonic",
                "harmonics_hz",
                "weights",
                "notes",
            ]
        )
        for summary in summaries:
            profile = summary.profile
            writer.writerow(
                [
                    summary.slug,
                    f"{profile.fundamental_hz:.4f}",
                    f"{profile.centroid_hz:.4f}",
                    f"{profile.bandwidth_hz:.4f}",
                    f"{profile.loudness_db:.2f}",
                    f"{profile.decay_slope_db_per_harmonic:.4f}",
                    " ".join(f"{h:.4f}" for h in profile.harmonics_hz[:8]),
                    " ".join(f"{w:.4f}" for w in profile.weights[:8]),
                    summary.notes,
                ]
            )


def simulate(seed: int = 0) -> Dict[str, object]:
    """Run each instrument simulation and aggregate spectral summaries."""

    ensemble_dir = ensure_artifact_dir(SLUG, subdir="sim")
    individual_results: Dict[str, Dict[str, object]] = {}
    for slug, module in _INSTRUMENTS:
        individual_results[slug] = module.simulate(seed=seed)

    summaries = _gather_spectral_profiles()
    combined = combine_profiles(summary.profile for summary in summaries)
    csv_path = ensemble_dir / "spectral_summary.csv"
    _write_spectral_csv(csv_path, summaries)

    artifact_paths: List[str] = []
    for result in individual_results.values():
        artifacts = result.get("artifacts")
        if isinstance(artifacts, (list, tuple)):
            artifact_paths.extend(str(item) for item in artifacts)
    return {
        "artifacts": [str(csv_path)] + artifact_paths,
        "spectral_centroid_hz": combined.centroid_hz,
        "spectral_bandwidth_hz": combined.bandwidth_hz,
        "spectral_loudness_db": combined.loudness_db,
        "decay_slope_db_per_harmonic": combined.decay_slope_db_per_harmonic,
        "mean_fundamental_hz": combined.fundamental_hz,
    }


def build() -> None:
    """Build all instrument CAD exports and catalog them for deployment."""

    ensemble_dir = ensure_artifact_dir(SLUG, subdir="cad")
    manifest_path = ensemble_dir / "ensemble_manifest.txt"
    exported_paths: List[str] = []
    for _, module in _INSTRUMENTS:
        module.build()
        instrument_dir = ensure_artifact_dir(module.SLUG, subdir="cad")
        exported_paths.extend(str(p) for p in instrument_dir.glob("*.stl"))

    with manifest_path.open("w", encoding="utf-8") as fh:
        fh.write("# Mechanical Ensemble CAD Manifest\n")
        for path in sorted(exported_paths):
            fh.write(f"{path}\n")


def _extract_events(slug: str, module, seed: int) -> List[Dict[str, float | str]]:
    try:
        params = module._load_params()  # type: ignore[attr-defined]
        raw = module._simulate(params, seed=seed)  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover - defensive
        return []

    events: List[Dict[str, float | str]] = []
    times: np.ndarray | None = None
    if "time_s" in raw:
        times_arr = np.asarray(raw["time_s"], dtype=float)
        if times_arr.size:
            times = times_arr
    elif "ideal_times_s" in raw:
        times_arr = np.asarray(raw["ideal_times_s"], dtype=float)
        if times_arr.size:
            times = times_arr
    elif "ideal_intervals_s" in raw:
        intervals = np.asarray(raw["ideal_intervals_s"], dtype=float)
        if intervals.size:
            times = np.cumsum(intervals) - intervals[0]

    freqs: np.ndarray | None = None
    if "ideal_frequency_hz" in raw:
        freq_arr = np.asarray(raw["ideal_frequency_hz"], dtype=float)
        if freq_arr.size:
            freqs = freq_arr

    intensities: np.ndarray | None = None
    for key in ("pressure_kpa", "impact_energy_j", "amplitude"):
        if key in raw:
            arr = np.asarray(raw[key], dtype=float)
            if arr.size:
                intensities = arr
                break

    if times is None:
        count = max(len(freqs or []), 8)
        times = np.arange(count, dtype=float)
    if freqs is None:
        freqs = np.zeros_like(times)
    if intensities is None:
        intensities = np.ones_like(times)

    if freqs.size != times.size:
        freqs = np.resize(freqs, times.size)
    if intensities.size != times.size:
        intensities = np.resize(intensities, times.size)

    for idx, (time_s, freq_hz, intensity) in enumerate(zip(times, freqs, intensities)):
        events.append(
            {
                "index": float(idx),
                "time_s": float(time_s),
                "frequency_hz": float(freq_hz),
                "intensity": float(intensity),
                "kind": "percussive" if slug == "mechanical_drum" else "pitched",
            }
        )
    return events


def _repeat_events(events: List[Dict[str, float | str]], measures: int, seconds_per_measure: float) -> List[Dict[str, float | str]]:
    if not events:
        return []
    times = np.array([event["time_s"] for event in events], dtype=float)
    base_start = float(times.min())
    base_length = float(times.max() - base_start)
    if base_length <= _SECONDS_EPS:
        base_length = seconds_per_measure
    scale = seconds_per_measure / base_length
    repeated: List[Dict[str, float | str]] = []
    for measure_idx in range(measures):
        offset = measure_idx * seconds_per_measure
        for event in events:
            normalized_time = (float(event["time_s"]) - base_start) * scale
            repeated.append(
                {
                    "measure": int(measure_idx),
                    "beat": normalized_time / max(seconds_per_measure / _BEATS_PER_MEASURE, _SECONDS_EPS),
                    "time_s": normalized_time + offset,
                    "frequency_hz": float(event["frequency_hz"]),
                    "intensity": float(event["intensity"]),
                    "kind": event["kind"],
                }
            )
    return repeated


def demo(
    seed: int = 0,
    tempo_bpm: float = 96.0,
    measures: int = 4,
    render_audio: bool = False,
    sample_rate: int = 44100,
) -> Dict[str, object]:
    """Generate a pseudo-score and spectral overview for the ensemble."""

    seconds_per_beat = 60.0 / max(tempo_bpm, 1e-3)
    seconds_per_measure = seconds_per_beat * _BEATS_PER_MEASURE

    demo_dir = ensure_artifact_dir(SLUG, subdir="demo")
    summaries = _gather_spectral_profiles()
    combined = combine_profiles(summary.profile for summary in summaries)

    score: Dict[str, List[Dict[str, float | str]]] = {}
    for slug, module in _INSTRUMENTS:
        base_events = _extract_events(slug, module, seed)
        score[slug] = _repeat_events(base_events, measures=measures, seconds_per_measure=seconds_per_measure)

    json_path = demo_dir / "ensemble_score.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "tempo_bpm": tempo_bpm,
                "measures": measures,
                "beats_per_measure": _BEATS_PER_MEASURE,
                "score": score,
            },
            handle,
            indent=2,
        )

    artifacts = [str(json_path)]
    if render_audio:
        audio_path = demo_dir / "ensemble_audio.wav"
        render_score_to_wav(score, tempo_bpm, _BEATS_PER_MEASURE, audio_path, sample_rate=sample_rate)
        artifacts.append(str(audio_path))

    return {
        "artifacts": artifacts,
        "tempo_bpm": tempo_bpm,
        "measures": measures,
        "spectral_centroid_hz": combined.centroid_hz,
        "spectral_loudness_db": combined.loudness_db,
        "decay_slope_db_per_harmonic": combined.decay_slope_db_per_harmonic,
    }


def evaluate() -> Dict[str, object]:
    """Aggregate evaluation metrics with spectral balance insights."""

    evaluations: Dict[str, Dict[str, object]] = {}
    for slug, module in _INSTRUMENTS:
        evaluations[slug] = module.evaluate()

    summaries = _gather_spectral_profiles()
    combined = combine_profiles(summary.profile for summary in summaries)
    balance_ratio = combined.bandwidth_hz / (combined.centroid_hz + 1e-6)

    return {
        "instruments": evaluations,
        "spectral": {
            "fundamental_hz": combined.fundamental_hz,
            "centroid_hz": combined.centroid_hz,
            "bandwidth_hz": combined.bandwidth_hz,
            "loudness_db": combined.loudness_db,
            "decay_slope_db_per_harmonic": combined.decay_slope_db_per_harmonic,
            "balance_ratio": balance_ratio,
        },
        "validated": {
            "balanced_spectrum": balance_ratio < 0.6,
            "next_actions": [
                "Fine-tune bellows and bow pressures for better timbre blend.",
                "Align percussive tempo with organ rotation drive.",
            ],
        },
    }
