"""Audio synthesis utilities for pseudo-ensemble playback."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import numpy as np
from numpy.typing import NDArray
from scipy.io import wavfile

DEFAULT_SAMPLE_RATE = 44100
_MAX_INT16 = 32767.0
_BEAT_FRACTION = 0.9
_PERCUSSIVE_DECAY = 6.0


def _deterministic_rng(seed_hint: float) -> np.random.Generator:
    seed = int(abs(seed_hint) * 1000) % (2**32 - 1)
    return np.random.default_rng(seed)


def _pitched_wave(
    frequency_hz: float,
    duration_s: float,
    sample_rate: int,
    amplitude: float,
) -> NDArray[np.float64]:
    samples = max(int(duration_s * sample_rate), 1)
    t = np.arange(samples, dtype=np.float64) / sample_rate
    envelope_phase = np.clip(t / max(duration_s, 1e-6), 0.0, 1.0)
    envelope = np.sin(np.pi * envelope_phase) ** 2
    wave = np.sin(2.0 * np.pi * frequency_hz * t)
    return amplitude * envelope * wave


def _percussive_wave(
    duration_s: float,
    sample_rate: int,
    amplitude: float,
    seed_hint: float,
) -> NDArray[np.float64]:
    samples = max(int(duration_s * sample_rate), 1)
    t = np.arange(samples, dtype=np.float64) / sample_rate
    envelope = np.exp(-_PERCUSSIVE_DECAY * t / max(duration_s, 1e-6))
    noise = _deterministic_rng(seed_hint).normal(0.0, 1.0, samples)
    return amplitude * 0.6 * envelope * noise


def render_score_to_wav(
    score: Mapping[str, Iterable[Mapping[str, float | str]]],
    tempo_bpm: float,
    beats_per_measure: int,
    output_path: Path,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    use_timbres: bool = False,
    reverb_wet: float = 0.0,
) -> Path:
    """Render a pseudo-score dictionary into a WAV file.

    When *use_timbres* is ``True``, events carrying a ``"slug"`` key are
    routed through the physics-based timbre engine (``core.timbre``) for
    harmonic synthesis with ADSR envelopes and per-instrument character.
    Events without a recognised slug fall back to the original sine/noise
    synthesis, preserving full backward compatibility.

    When *reverb_wet* > 0, a Schroeder hall reverb is applied to the
    final mix.
    """

    seconds_per_beat = 60.0 / max(tempo_bpm, 1e-6)
    total_time = 0.0
    for events in score.values():
        for event in events:
            total_time = max(total_time, float(event.get("time_s", 0.0)))
    total_time += seconds_per_beat * 1.5
    total_samples = max(int(total_time * sample_rate) + 1, 1)
    audio = np.zeros(total_samples, dtype=np.float64)

    # Lazy-import timbre engine only when needed
    _timbre_mod = None
    if use_timbres:
        from . import timbre as _timbre_mod  # noqa: F811

    for slug, events in score.items():
        slug_length = len(slug)
        for idx, event in enumerate(events):
            start_time = float(event.get("time_s", 0.0))
            start_index = int(start_time * sample_rate)
            intensity = float(event.get("intensity", 1.0))
            amplitude = min(max(intensity, 0.0), 12.0) / 12.0
            duration = seconds_per_beat * _BEAT_FRACTION
            seed_hint = start_time + idx + slug_length
            is_percussive = str(event.get("kind", "pitched")) == "percussive"

            # Prefer per-event duration when available
            event_duration = event.get("duration_s")
            if event_duration is not None:
                duration = max(float(event_duration), 0.01)
            elif is_percussive:
                duration = max(seconds_per_beat * 0.5, 0.05)

            # Route through timbre engine when enabled
            event_slug = str(event.get("slug", slug))
            timbre = (
                _timbre_mod.INSTRUMENT_TIMBRES.get(event_slug)
                if _timbre_mod is not None
                else None
            )

            if timbre is not None and _timbre_mod is not None:
                frequency = float(event.get("frequency_hz", 220.0)) or 220.0
                if timbre.is_percussive or is_percussive:
                    wave = _timbre_mod.synthesize_percussive(
                        frequency, duration, amplitude, timbre, sample_rate, seed_hint
                    )
                else:
                    wave = _timbre_mod.synthesize_note(
                        frequency, duration, amplitude, timbre, sample_rate, seed_hint
                    )
            elif is_percussive:
                wave = _percussive_wave(duration, sample_rate, amplitude, seed_hint)
            else:
                frequency = float(event.get("frequency_hz", 220.0)) or 220.0
                wave = _pitched_wave(frequency, duration, sample_rate, amplitude)

            end_index = start_index + wave.size
            if start_index >= audio.size:
                continue
            if end_index > audio.size:
                wave = wave[: audio.size - start_index]
                end_index = start_index + wave.size
            audio[start_index:end_index] += wave

    # Apply reverb before normalization
    if reverb_wet > 0:
        from .reverb import apply_hall_reverb
        audio = apply_hall_reverb(audio, sample_rate=sample_rate, wet_mix=reverb_wet)

    peak = float(np.max(np.abs(audio)))
    if peak > 0:
        audio = audio / (peak * 1.05)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wav_data = (audio * _MAX_INT16).astype(np.int16)
    wavfile.write(output_path, sample_rate, wav_data)
    return output_path
