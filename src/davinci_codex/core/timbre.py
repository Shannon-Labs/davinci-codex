"""Physics-based instrument timbre synthesis for Leonardo's mechanical ensemble."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
from numpy.typing import NDArray


@dataclass
class ADSREnvelope:
    """Attack-Decay-Sustain-Release envelope parameters."""

    attack_s: float = 0.05
    decay_s: float = 0.05
    sustain_level: float = 0.8
    release_s: float = 0.1

    def generate(self, duration_s: float, sample_rate: int) -> NDArray[np.float64]:
        """Generate an ADSR envelope for the given duration and sample rate."""
        total_samples = max(int(duration_s * sample_rate), 1)
        envelope = np.zeros(total_samples, dtype=np.float64)

        attack_samples = int(self.attack_s * sample_rate)
        decay_samples = int(self.decay_s * sample_rate)
        release_samples = int(self.release_s * sample_rate)

        # Clamp so attack+decay+release don't exceed total
        total_adr = attack_samples + decay_samples + release_samples
        if total_adr > total_samples:
            scale = total_samples / max(total_adr, 1)
            attack_samples = int(attack_samples * scale)
            decay_samples = int(decay_samples * scale)
            release_samples = max(total_samples - attack_samples - decay_samples, 0)

        sustain_samples = max(total_samples - attack_samples - decay_samples - release_samples, 0)

        idx = 0
        # Attack: 0 -> 1
        if attack_samples > 0:
            envelope[idx : idx + attack_samples] = np.linspace(0.0, 1.0, attack_samples, endpoint=False)
            idx += attack_samples

        # Decay: 1 -> sustain_level
        if decay_samples > 0:
            envelope[idx : idx + decay_samples] = np.linspace(1.0, self.sustain_level, decay_samples, endpoint=False)
            idx += decay_samples

        # Sustain: constant
        if sustain_samples > 0:
            envelope[idx : idx + sustain_samples] = self.sustain_level
            idx += sustain_samples

        # Release: sustain_level -> 0
        if release_samples > 0:
            envelope[idx : idx + release_samples] = np.linspace(self.sustain_level, 0.0, release_samples)
            idx += release_samples

        return envelope


@dataclass
class InstrumentTimbre:
    """Complete timbre definition for a mechanical instrument."""

    name: str
    harmonic_ratios: List[float] = field(default_factory=lambda: [1.0])
    harmonic_weights: List[float] = field(default_factory=lambda: [1.0])
    envelope: ADSREnvelope = field(default_factory=ADSREnvelope)
    noise_level: float = 0.0
    noise_color: str = "white"  # "white", "pink", "breath"
    vibrato_rate_hz: float = 0.0
    vibrato_depth_cents: float = 0.0
    is_percussive: bool = False


# ---------------------------------------------------------------------------
# Instrument definitions
# ---------------------------------------------------------------------------

INSTRUMENT_TIMBRES: Dict[str, InstrumentTimbre] = {
    "viola_organista": InstrumentTimbre(
        name="Viola Organista",
        harmonic_ratios=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        harmonic_weights=[1.0, 0.3, 0.7, 0.15, 0.5, 0.1, 0.35, 0.08],
        envelope=ADSREnvelope(attack_s=0.08, decay_s=0.06, sustain_level=0.75, release_s=0.15),
        noise_level=0.03,
        noise_color="pink",
        vibrato_rate_hz=5.0,
        vibrato_depth_cents=12.0,
    ),
    "mechanical_organ": InstrumentTimbre(
        name="Mechanical Organ",
        harmonic_ratios=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        harmonic_weights=[1.0, 0.5, 0.33, 0.25, 0.2, 0.167, 0.143, 0.125],
        envelope=ADSREnvelope(attack_s=0.05, decay_s=0.03, sustain_level=0.95, release_s=0.08),
        noise_level=0.02,
        noise_color="breath",
        vibrato_rate_hz=0.0,
        vibrato_depth_cents=0.0,
    ),
    "programmable_flute": InstrumentTimbre(
        name="Programmable Flute",
        harmonic_ratios=[1.0, 2.0, 3.0, 4.0, 5.0],
        harmonic_weights=[1.0, 0.35, 0.15, 0.08, 0.03],
        envelope=ADSREnvelope(attack_s=0.04, decay_s=0.05, sustain_level=0.70, release_s=0.12),
        noise_level=0.08,
        noise_color="breath",
        vibrato_rate_hz=4.5,
        vibrato_depth_cents=8.0,
    ),
    "mechanical_carillon": InstrumentTimbre(
        name="Mechanical Carillon",
        # Bell-like inharmonic partials
        harmonic_ratios=[1.0, 2.4, 3.9, 5.4, 6.7, 8.2],
        harmonic_weights=[1.0, 0.6, 0.4, 0.25, 0.15, 0.08],
        envelope=ADSREnvelope(attack_s=0.001, decay_s=0.3, sustain_level=0.15, release_s=1.5),
        noise_level=0.0,
        noise_color="white",
        vibrato_rate_hz=0.0,
        vibrato_depth_cents=0.0,
    ),
    "mechanical_trumpeter": InstrumentTimbre(
        name="Mechanical Trumpeter",
        harmonic_ratios=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        harmonic_weights=[1.0, 0.8, 0.6, 0.55, 0.5, 0.4, 0.3, 0.2],
        envelope=ADSREnvelope(attack_s=0.03, decay_s=0.04, sustain_level=0.85, release_s=0.10),
        noise_level=0.04,
        noise_color="breath",
        vibrato_rate_hz=5.5,
        vibrato_depth_cents=15.0,
    ),
    "mechanical_drum": InstrumentTimbre(
        name="Mechanical Drum",
        # Drumhead vibration modes (Bessel function zeros)
        harmonic_ratios=[1.0, 1.59, 2.14, 2.30, 2.65, 2.92],
        harmonic_weights=[1.0, 0.7, 0.5, 0.35, 0.2, 0.1],
        envelope=ADSREnvelope(attack_s=0.002, decay_s=0.15, sustain_level=0.0, release_s=0.2),
        noise_level=0.60,
        noise_color="white",
        vibrato_rate_hz=0.0,
        vibrato_depth_cents=0.0,
        is_percussive=True,
    ),
}


def _pink_noise(rng: np.random.Generator, n: int) -> NDArray[np.float64]:
    """Generate approximate pink noise (1/f) using the Voss-McCartney algorithm."""
    num_rows = 16
    array = rng.standard_normal((num_rows, n))
    # Each row is updated at different rates
    result = np.zeros(n, dtype=np.float64)
    for row in range(num_rows):
        step = 2**row
        held = array[row, 0]
        for i in range(n):
            if i % step == 0 and i < n:
                held = array[row, min(i, n - 1)]
            result[i] += held
    # Normalize
    peak = np.max(np.abs(result))
    if peak > 0:
        result /= peak
    return result


def _breath_noise(rng: np.random.Generator, n: int, sample_rate: int) -> NDArray[np.float64]:
    """Generate breath-like noise: low-pass filtered white noise."""
    white = rng.standard_normal(n)
    # Simple first-order IIR low-pass (cutoff ~2kHz)
    alpha = 1.0 - np.exp(-2.0 * np.pi * 2000.0 / sample_rate)
    result = np.zeros(n, dtype=np.float64)
    result[0] = white[0]
    for i in range(1, n):
        result[i] = result[i - 1] + alpha * (white[i] - result[i - 1])
    # Normalize
    peak = np.max(np.abs(result))
    if peak > 0:
        result /= peak
    return result


def _generate_noise(
    rng: np.random.Generator, n: int, sample_rate: int, color: str
) -> NDArray[np.float64]:
    """Generate colored noise."""
    if color == "pink":
        return _pink_noise(rng, n)
    elif color == "breath":
        return _breath_noise(rng, n, sample_rate)
    else:  # white
        noise = rng.standard_normal(n)
        peak = np.max(np.abs(noise))
        if peak > 0:
            noise /= peak
        return noise


def synthesize_note(
    frequency_hz: float,
    duration_s: float,
    amplitude: float,
    timbre: InstrumentTimbre,
    sample_rate: int = 44100,
    seed_hint: float = 0.0,
) -> NDArray[np.float64]:
    """Synthesize a pitched note with physics-based timbre.

    Args:
        frequency_hz: Fundamental frequency in Hz.
        duration_s: Note duration in seconds.
        amplitude: Amplitude scaling (0..1).
        timbre: Instrument timbre definition.
        sample_rate: Audio sample rate.
        seed_hint: Seed hint for deterministic noise generation.

    Returns:
        Audio samples as a float64 array.
    """
    n_samples = max(int(duration_s * sample_rate), 1)
    t = np.arange(n_samples, dtype=np.float64) / sample_rate

    # Sum harmonic partials
    signal = np.zeros(n_samples, dtype=np.float64)
    ratios = np.array(timbre.harmonic_ratios, dtype=np.float64)
    weights = np.array(timbre.harmonic_weights, dtype=np.float64)

    # Normalize weights so fundamental peak = 1
    if weights.size > 0 and weights[0] > 0:
        weights = weights / weights[0]

    # Vibrato modulation
    vibrato = np.zeros(n_samples, dtype=np.float64)
    if timbre.vibrato_rate_hz > 0 and timbre.vibrato_depth_cents > 0:
        depth_ratio = 2.0 ** (timbre.vibrato_depth_cents / 1200.0) - 1.0
        vibrato = depth_ratio * np.sin(2.0 * np.pi * timbre.vibrato_rate_hz * t)

    for ratio, weight in zip(ratios, weights):
        partial_freq = frequency_hz * ratio
        # Apply vibrato to each partial
        phase = 2.0 * np.pi * partial_freq * t * (1.0 + vibrato)
        signal += weight * np.sin(phase)

    # Normalize harmonic sum
    peak = np.max(np.abs(signal))
    if peak > 0:
        signal /= peak

    # Apply ADSR envelope
    envelope = timbre.envelope.generate(duration_s, sample_rate)

    # Add noise component
    if timbre.noise_level > 0:
        rng_seed = int(abs(seed_hint) * 1000) % (2**32 - 1)
        rng = np.random.default_rng(rng_seed)
        noise = _generate_noise(rng, n_samples, sample_rate, timbre.noise_color)
        signal = (1.0 - timbre.noise_level) * signal + timbre.noise_level * noise

    return amplitude * envelope * signal


def synthesize_percussive(
    frequency_hz: float,
    duration_s: float,
    amplitude: float,
    timbre: InstrumentTimbre,
    sample_rate: int = 44100,
    seed_hint: float = 0.0,
) -> NDArray[np.float64]:
    """Synthesize a percussive hit with tuned resonance + noise burst.

    Args:
        frequency_hz: Fundamental tuning frequency in Hz.
        duration_s: Total duration in seconds.
        amplitude: Amplitude scaling (0..1).
        timbre: Instrument timbre definition.
        sample_rate: Audio sample rate.
        seed_hint: Seed hint for deterministic noise generation.

    Returns:
        Audio samples as a float64 array.
    """
    n_samples = max(int(duration_s * sample_rate), 1)
    t = np.arange(n_samples, dtype=np.float64) / sample_rate

    # Tuned resonance from drumhead modes
    tonal = np.zeros(n_samples, dtype=np.float64)
    ratios = np.array(timbre.harmonic_ratios, dtype=np.float64)
    weights = np.array(timbre.harmonic_weights, dtype=np.float64)

    if weights.size > 0 and weights[0] > 0:
        weights = weights / weights[0]

    for ratio, weight in zip(ratios, weights):
        partial_freq = frequency_hz * ratio
        # Each partial decays at a different rate (higher partials decay faster)
        decay_rate = 4.0 + ratio * 2.0
        partial_envelope = np.exp(-decay_rate * t)
        tonal += weight * partial_envelope * np.sin(2.0 * np.pi * partial_freq * t)

    # Normalize tonal component
    peak = np.max(np.abs(tonal))
    if peak > 0:
        tonal /= peak

    # Noise burst
    rng_seed = int(abs(seed_hint) * 1000) % (2**32 - 1)
    rng = np.random.default_rng(rng_seed)
    noise = rng.standard_normal(n_samples)
    # Noise envelope: rapid exponential decay
    noise_envelope = np.exp(-20.0 * t)
    noise = noise * noise_envelope
    noise_peak = np.max(np.abs(noise))
    if noise_peak > 0:
        noise /= noise_peak

    # Mix tonal and noise
    noise_mix = timbre.noise_level
    signal = (1.0 - noise_mix) * tonal + noise_mix * noise

    # Apply ADSR envelope
    envelope = timbre.envelope.generate(duration_s, sample_rate)

    return amplitude * envelope * signal


def get_timbre(slug: str) -> Optional[InstrumentTimbre]:
    """Look up an instrument timbre by slug.

    Returns None if the slug is not recognized.
    """
    return INSTRUMENT_TIMBRES.get(slug)
