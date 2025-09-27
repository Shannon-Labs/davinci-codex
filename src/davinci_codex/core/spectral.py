"""Spectral profiling utilities for mechanical instruments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

import numpy as np
from numpy.typing import NDArray


@dataclass
class SpectralProfile:
    """Compact summary of an instrument's spectrum."""

    fundamental_hz: float
    centroid_hz: float
    bandwidth_hz: float
    harmonics_hz: List[float]
    weights: List[float]
    loudness_db: float
    decay_slope_db_per_harmonic: float


_DEF_EPS = 1e-12


def _normalize_weights(weights: NDArray[np.float64]) -> NDArray[np.float64]:
    total = float(weights.sum())
    if total <= _DEF_EPS:
        return np.ones_like(weights, dtype=float) / max(weights.size, 1)
    return (weights / total).astype(float)


def _estimate_decay_slope(weights: NDArray[np.float64]) -> float:
    mask = weights > _DEF_EPS
    if mask.sum() <= 1:
        return 0.0
    indices = np.arange(weights.size, dtype=float)[mask]
    log_weights = 20.0 * np.log10(weights[mask])
    slope, _ = np.polyfit(indices, log_weights, deg=1)
    return float(slope)


def profile_from_frequencies(
    frequencies_hz: Sequence[float],
    weights: Sequence[float] | None = None,
    fundamental_hint_hz: float | None = None,
) -> SpectralProfile:
    """Compute a simple spectral profile from frequency bins."""

    freqs = np.array([f for f in frequencies_hz if f > 0], dtype=float)
    if freqs.size == 0:
        return SpectralProfile(0.0, 0.0, 0.0, [], [], -np.inf, 0.0)

    if weights is None:
        weights_arr = np.ones_like(freqs, dtype=float)
    else:
        weights_arr = np.array(weights, dtype=float)
        if weights_arr.size != freqs.size:
            weights_arr = np.resize(weights_arr, freqs.size)

    weights_arr = _normalize_weights(weights_arr.astype(float))
    centroid = float(np.sum(freqs * weights_arr))
    variance = float(np.sum(((freqs - centroid) ** 2) * weights_arr))
    bandwidth = float(np.sqrt(max(variance, 0.0)))
    fundamental = float(fundamental_hint_hz or freqs.min())

    loudness_db = float(20.0 * np.log10(max(weights_arr.sum(), _DEF_EPS)))
    decay_slope = _estimate_decay_slope(weights_arr)

    sorted_idx = np.argsort(freqs)
    sorted_freqs = freqs[sorted_idx]
    sorted_weights = weights_arr[sorted_idx]

    return SpectralProfile(
        fundamental_hz=fundamental,
        centroid_hz=centroid,
        bandwidth_hz=bandwidth,
        harmonics_hz=sorted_freqs.tolist(),
        weights=sorted_weights.tolist(),
        loudness_db=loudness_db,
        decay_slope_db_per_harmonic=decay_slope,
    )


def profile_from_intervals(intervals_s: Sequence[float]) -> SpectralProfile:
    """Estimate the spectral profile of a periodic pattern from intervals."""

    intervals = np.array([v for v in intervals_s if v > 0], dtype=float)
    if intervals.size == 0:
        return SpectralProfile(0.0, 0.0, 0.0, [], [], -np.inf, 0.0)

    freqs = 1.0 / intervals
    weights = np.ones_like(freqs, dtype=float)
    return profile_from_frequencies(freqs, weights)


def combine_profiles(profiles: Iterable[SpectralProfile]) -> SpectralProfile:
    """Aggregate multiple spectral profiles into a composite view."""

    prof_list = [p for p in profiles if p.fundamental_hz > 0]
    if not prof_list:
        return SpectralProfile(0.0, 0.0, 0.0, [], [], -np.inf, 0.0)

    freqs: List[float] = []
    weights: List[float] = []
    for prof in prof_list:
        freqs.extend(prof.harmonics_hz)
        weights.extend(prof.weights)
    combined = profile_from_frequencies(freqs, weights)
    return combined
