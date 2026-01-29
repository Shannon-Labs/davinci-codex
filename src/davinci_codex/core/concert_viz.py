"""Visualization helpers for the mechanical concert pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Mapping

import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram as scipy_spectrogram

# Instrument colour palette (warm Renaissance tones)
_INSTRUMENT_COLORS: Dict[str, str] = {
    "viola_organista": "#8B4513",
    "mechanical_organ": "#4B0082",
    "programmable_flute": "#006400",
    "mechanical_carillon": "#DAA520",
    "mechanical_trumpeter": "#B22222",
    "mechanical_drum": "#2F4F4F",
}

_DEFAULT_COLOR = "#555555"


def _color_for(slug: str) -> str:
    return _INSTRUMENT_COLORS.get(slug, _DEFAULT_COLOR)


def plot_waveform(wav_path: Path, output_path: Path) -> Path:
    """Plot amplitude vs. time from a WAV file.

    Args:
        wav_path: Path to the input WAV file.
        output_path: Path to write the PNG.

    Returns:
        The output path.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sr, data = wavfile.read(wav_path)
    if data.ndim > 1:
        data = data[:, 0]
    samples = data.astype(np.float64)
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples /= peak
    t = np.arange(samples.size) / sr

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(t, samples, linewidth=0.3, color="#4B0082")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Mechanical Concert -- Waveform")
    ax.set_xlim(0, t[-1] if t.size > 0 else 1)
    ax.set_ylim(-1.05, 1.05)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_spectrogram(wav_path: Path, output_path: Path) -> Path:
    """Plot a frequency-vs-time spectrogram from a WAV file.

    Args:
        wav_path: Path to the input WAV file.
        output_path: Path to write the PNG.

    Returns:
        The output path.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sr, data = wavfile.read(wav_path)
    if data.ndim > 1:
        data = data[:, 0]
    samples = data.astype(np.float64)

    nperseg = min(2048, samples.size)
    f, t, Sxx = scipy_spectrogram(samples, fs=sr, nperseg=nperseg)

    fig, ax = plt.subplots(figsize=(12, 5))
    Sxx_db = 10 * np.log10(Sxx + 1e-12)
    ax.pcolormesh(t, f, Sxx_db, shading="gouraud", cmap="inferno")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_xlabel("Time (s)")
    ax.set_title("Mechanical Concert -- Spectrogram")
    ax.set_ylim(0, min(4000, sr / 2))
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_score_roll(
    ensemble_events: Mapping[str, Iterable[Mapping[str, float | str]]],
    output_path: Path,
) -> Path:
    """Plot a piano-roll view coloured by instrument.

    Each note is a horizontal bar at its frequency, with width equal to its
    duration (or a default 0.3s if ``duration_s`` is absent).

    Args:
        ensemble_events: Dict mapping instrument slugs to event lists.
        output_path: Path to write the PNG.

    Returns:
        The output path.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(figsize=(14, 6))
    legend_entries: Dict[str, str] = {}

    for slug, events in ensemble_events.items():
        color = _color_for(slug)
        for event in events:
            time_s = float(event.get("time_s", 0.0))
            freq = float(event.get("frequency_hz", 0.0))
            dur = float(event.get("duration_s", 0.3))
            intensity = float(event.get("intensity", 1.0))
            alpha = max(0.3, min(1.0, intensity / 12.0 if intensity > 1 else intensity))

            rect = Rectangle(
                (time_s, freq - 5),
                dur,
                10,
                linewidth=0,
                edgecolor="none",
                facecolor=color,
                alpha=alpha,
            )
            ax.add_patch(rect)

            if slug not in legend_entries:
                legend_entries[slug] = color

    # Build legend
    legend_patches: List[Rectangle] = []
    for slug, color in sorted(legend_entries.items()):
        legend_patches.append(
            Rectangle((0, 0), 1, 1, fc=color, label=slug.replace("_", " ").title())
        )
    if legend_patches:
        ax.legend(handles=legend_patches, loc="upper right", fontsize=8)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Mechanical Concert -- Score Roll")
    ax.autoscale_view()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
