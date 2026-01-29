"""Tests for the physics-based instrument timbre engine and reverb."""

import numpy as np
import pytest

from davinci_codex.core.timbre import (
    ADSREnvelope,
    INSTRUMENT_TIMBRES,
    get_timbre,
    synthesize_note,
    synthesize_percussive,
)
from davinci_codex.core.reverb import apply_hall_reverb


# ---------------------------------------------------------------------------
# ADSREnvelope tests
# ---------------------------------------------------------------------------

class TestADSREnvelope:
    def test_shape_length(self):
        env = ADSREnvelope(attack_s=0.01, decay_s=0.01, sustain_level=0.7, release_s=0.01)
        samples = env.generate(0.1, 44100)
        expected = int(0.1 * 44100)
        assert samples.shape == (expected,)

    def test_attack_rises_to_one(self):
        env = ADSREnvelope(attack_s=0.1, decay_s=0.0, sustain_level=1.0, release_s=0.0)
        samples = env.generate(0.2, 44100)
        attack_end = int(0.1 * 44100)
        # The envelope should reach ~1.0 at end of attack
        assert samples[attack_end - 1] > 0.9

    def test_sustain_level(self):
        env = ADSREnvelope(attack_s=0.01, decay_s=0.01, sustain_level=0.6, release_s=0.01)
        samples = env.generate(1.0, 44100)
        # Mid-point should be near sustain level
        mid = len(samples) // 2
        assert abs(samples[mid] - 0.6) < 0.05

    def test_release_ends_near_zero(self):
        env = ADSREnvelope(attack_s=0.01, decay_s=0.01, sustain_level=0.8, release_s=0.05)
        samples = env.generate(0.2, 44100)
        assert samples[-1] < 0.05

    def test_very_short_duration(self):
        env = ADSREnvelope(attack_s=0.1, decay_s=0.1, sustain_level=0.5, release_s=0.1)
        # Duration shorter than attack+decay+release
        samples = env.generate(0.05, 44100)
        assert samples.shape[0] == int(0.05 * 44100)
        assert np.all(np.isfinite(samples))

    def test_envelope_bounded(self):
        env = ADSREnvelope(attack_s=0.02, decay_s=0.03, sustain_level=0.9, release_s=0.05)
        samples = env.generate(0.5, 44100)
        assert np.all(samples >= 0.0)
        assert np.all(samples <= 1.01)  # small tolerance


# ---------------------------------------------------------------------------
# synthesize_note tests
# ---------------------------------------------------------------------------

class TestSynthesizeNote:
    def test_output_length(self):
        timbre = INSTRUMENT_TIMBRES["viola_organista"]
        wave = synthesize_note(440.0, 0.5, 0.8, timbre, sample_rate=44100)
        expected = int(0.5 * 44100)
        assert wave.shape == (expected,)

    def test_amplitude_bounded(self):
        timbre = INSTRUMENT_TIMBRES["mechanical_organ"]
        wave = synthesize_note(440.0, 0.5, 1.0, timbre, sample_rate=44100)
        assert np.all(np.abs(wave) <= 1.05)

    def test_deterministic_with_same_seed(self):
        timbre = INSTRUMENT_TIMBRES["programmable_flute"]
        w1 = synthesize_note(440.0, 0.3, 0.7, timbre, seed_hint=42.0)
        w2 = synthesize_note(440.0, 0.3, 0.7, timbre, seed_hint=42.0)
        np.testing.assert_array_equal(w1, w2)

    def test_different_seeds_differ(self):
        timbre = INSTRUMENT_TIMBRES["programmable_flute"]
        w1 = synthesize_note(440.0, 0.3, 0.7, timbre, seed_hint=1.0)
        w2 = synthesize_note(440.0, 0.3, 0.7, timbre, seed_hint=2.0)
        # They should differ due to noise component
        assert not np.array_equal(w1, w2)

    def test_fundamental_frequency_in_spectrum(self):
        timbre = INSTRUMENT_TIMBRES["mechanical_organ"]
        freq = 440.0
        sr = 44100
        wave = synthesize_note(freq, 1.0, 1.0, timbre, sample_rate=sr)
        fft = np.abs(np.fft.rfft(wave))
        freqs = np.fft.rfftfreq(wave.size, d=1.0 / sr)
        # The peak should be near 440 Hz
        peak_freq = freqs[np.argmax(fft)]
        assert abs(peak_freq - freq) < 5.0  # within 5 Hz

    @pytest.mark.parametrize("slug", list(INSTRUMENT_TIMBRES.keys()))
    def test_all_timbres_render_without_error(self, slug):
        timbre = INSTRUMENT_TIMBRES[slug]
        wave = synthesize_note(440.0, 0.3, 0.7, timbre, sample_rate=22050)
        assert wave.size > 0
        assert np.all(np.isfinite(wave))


# ---------------------------------------------------------------------------
# synthesize_percussive tests
# ---------------------------------------------------------------------------

class TestSynthesizePercussive:
    def test_output_length(self):
        timbre = INSTRUMENT_TIMBRES["mechanical_drum"]
        wave = synthesize_percussive(200.0, 0.4, 0.9, timbre, sample_rate=44100)
        expected = int(0.4 * 44100)
        assert wave.shape == (expected,)

    def test_amplitude_bounded(self):
        timbre = INSTRUMENT_TIMBRES["mechanical_drum"]
        wave = synthesize_percussive(200.0, 0.5, 1.0, timbre, sample_rate=44100)
        assert np.all(np.abs(wave) <= 1.05)

    def test_deterministic(self):
        timbre = INSTRUMENT_TIMBRES["mechanical_drum"]
        w1 = synthesize_percussive(200.0, 0.3, 0.7, timbre, seed_hint=10.0)
        w2 = synthesize_percussive(200.0, 0.3, 0.7, timbre, seed_hint=10.0)
        np.testing.assert_array_equal(w1, w2)


# ---------------------------------------------------------------------------
# get_timbre tests
# ---------------------------------------------------------------------------

class TestGetTimbre:
    def test_known_slug(self):
        t = get_timbre("viola_organista")
        assert t is not None
        assert t.name == "Viola Organista"

    def test_unknown_slug_returns_none(self):
        assert get_timbre("nonexistent_instrument") is None


# ---------------------------------------------------------------------------
# Reverb tests
# ---------------------------------------------------------------------------

class TestHallReverb:
    def test_output_same_length(self):
        signal = np.random.default_rng(0).standard_normal(44100)
        result = apply_hall_reverb(signal, sample_rate=44100, wet_mix=0.3)
        assert result.shape == signal.shape

    def test_dry_passthrough(self):
        signal = np.random.default_rng(0).standard_normal(44100)
        result = apply_hall_reverb(signal, sample_rate=44100, wet_mix=0.0)
        np.testing.assert_array_equal(result, signal)

    def test_wet_changes_signal(self):
        signal = np.random.default_rng(0).standard_normal(44100)
        result = apply_hall_reverb(signal, sample_rate=44100, wet_mix=0.5)
        assert not np.array_equal(result, signal)

    def test_output_finite(self):
        signal = np.random.default_rng(0).standard_normal(44100)
        result = apply_hall_reverb(signal, sample_rate=44100, wet_mix=0.4)
        assert np.all(np.isfinite(result))
