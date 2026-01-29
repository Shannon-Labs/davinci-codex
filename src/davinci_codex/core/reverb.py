"""Algorithmic reverb simulating a Renaissance hall (Schroeder reverb)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def _comb_filter(
    signal: NDArray[np.float64],
    delay_samples: int,
    feedback: float,
    damping: float,
) -> NDArray[np.float64]:
    """Apply a feedback comb filter with high-frequency damping."""
    n = signal.size
    output = np.zeros(n, dtype=np.float64)
    prev_filtered = 0.0
    for i in range(n):
        delayed_idx = i - delay_samples
        delayed = output[delayed_idx] if delayed_idx >= 0 else 0.0
        # One-pole low-pass for damping
        filtered = (1.0 - damping) * delayed + damping * prev_filtered
        prev_filtered = filtered
        output[i] = signal[i] + feedback * filtered
    return output


def _allpass_filter(
    signal: NDArray[np.float64],
    delay_samples: int,
    gain: float,
) -> NDArray[np.float64]:
    """Apply a Schroeder allpass filter."""
    n = signal.size
    output = np.zeros(n, dtype=np.float64)
    buffer = np.zeros(n + delay_samples, dtype=np.float64)
    for i in range(n):
        delayed_idx = i - delay_samples
        delayed = buffer[delayed_idx] if delayed_idx >= 0 else 0.0
        buffer[i] = signal[i] + gain * delayed
        output[i] = -gain * buffer[i] + delayed
    return output


def apply_hall_reverb(
    signal: NDArray[np.float64],
    sample_rate: int = 44100,
    room_size: float = 0.7,
    damping: float = 0.5,
    wet_mix: float = 0.2,
) -> NDArray[np.float64]:
    """Apply Schroeder reverb simulating a Renaissance hall.

    Uses 4 parallel comb filters feeding into 2 series allpass filters.
    Inspired by the acoustics of Santa Maria delle Grazie / Sforza court halls.

    Args:
        signal: Mono audio signal (float64).
        sample_rate: Sample rate in Hz.
        room_size: Room size factor (0..1). Scales comb filter delays.
        damping: High-frequency damping (0..1). Higher = more damping.
        wet_mix: Wet/dry mix (0..1). 0 = fully dry, 1 = fully wet.

    Returns:
        Processed audio signal with reverb applied.
    """
    if wet_mix <= 0.0:
        return signal.copy()

    # Pre-delay (~20ms for a Renaissance hall)
    pre_delay_samples = int(0.02 * sample_rate)
    padded = np.zeros(signal.size + pre_delay_samples, dtype=np.float64)
    padded[pre_delay_samples:] = signal

    # Comb filter delay times (in samples), scaled by room size
    # Base delays chosen to be mutually prime for smooth decay
    base_delays_ms = [29.7, 37.1, 41.1, 43.7]
    comb_delays = [int(d * 0.001 * sample_rate * room_size) for d in base_delays_ms]
    comb_feedback = 0.84 * room_size

    # Run 4 parallel comb filters
    comb_outputs = np.zeros(padded.size, dtype=np.float64)
    for delay in comb_delays:
        if delay < 1:
            delay = 1
        comb_outputs += _comb_filter(padded, delay, comb_feedback, damping)

    # Normalize comb sum
    comb_outputs /= len(comb_delays)

    # Allpass filter delays
    allpass_delays_ms = [5.0, 1.7]
    allpass_gain = 0.7

    # Run 2 series allpass filters
    wet = comb_outputs
    for delay_ms in allpass_delays_ms:
        delay_samples = max(int(delay_ms * 0.001 * sample_rate * room_size), 1)
        wet = _allpass_filter(wet, delay_samples, allpass_gain)

    # Trim to match original length
    wet = wet[: signal.size]
    if wet.size < signal.size:
        wet = np.pad(wet, (0, signal.size - wet.size))

    # Mix dry and wet
    return (1.0 - wet_mix) * signal + wet_mix * wet
