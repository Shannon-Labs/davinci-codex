"""Integration tests for the full concert pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from scipy.io import wavfile

from davinci_codex.core.audio import render_score_to_wav
from davinci_codex.core.concert import perform_concert


@pytest.fixture
def concert_dir(tmp_path: Path) -> Path:
    return tmp_path / "concert_output"


class TestConcertPipeline:
    def test_produces_wav_file(self, concert_dir: Path):
        result = perform_concert(
            form="pavane",
            seed=42,
            measures=4,
            tempo_bpm=80.0,
            reverb_wet=0.1,
            output_dir=concert_dir,
            visualize=False,
        )
        wav_path = concert_dir / "concert_audio.wav"
        assert wav_path.exists()
        assert str(wav_path) in result["artifacts"]

    def test_wav_is_valid(self, concert_dir: Path):
        perform_concert(
            form="pavane",
            seed=42,
            measures=4,
            tempo_bpm=80.0,
            output_dir=concert_dir,
            visualize=False,
        )
        wav_path = concert_dir / "concert_audio.wav"
        sr, data = wavfile.read(wav_path)
        assert sr == 44100
        assert data.size > 0
        # Audio should not be all-zero
        assert np.any(data != 0)

    def test_score_json_has_instruments(self, concert_dir: Path):
        result = perform_concert(
            form="pavane",
            seed=42,
            measures=4,
            output_dir=concert_dir,
            visualize=False,
        )
        score_path = concert_dir / "concert_score.json"
        assert score_path.exists()

        with score_path.open() as f:
            payload = json.load(f)

        score = payload["score"]
        assert isinstance(score, dict)
        assert len(score) > 0
        # Should have at least some instruments represented
        assert result["total_events"] > 0

    def test_deterministic_same_seed(self, concert_dir: Path):
        dir1 = concert_dir / "run1"
        dir2 = concert_dir / "run2"
        perform_concert(seed=99, measures=4, output_dir=dir1, visualize=False)
        perform_concert(seed=99, measures=4, output_dir=dir2, visualize=False)

        sr1, data1 = wavfile.read(dir1 / "concert_audio.wav")
        sr2, data2 = wavfile.read(dir2 / "concert_audio.wav")
        assert sr1 == sr2
        np.testing.assert_array_equal(data1, data2)

    def test_different_seeds_differ(self, concert_dir: Path):
        dir1 = concert_dir / "run_a"
        dir2 = concert_dir / "run_b"
        perform_concert(seed=1, measures=4, output_dir=dir1, visualize=False)
        perform_concert(seed=2, measures=4, output_dir=dir2, visualize=False)

        _, data1 = wavfile.read(dir1 / "concert_audio.wav")
        _, data2 = wavfile.read(dir2 / "concert_audio.wav")
        # Different seeds should produce different audio
        assert not np.array_equal(data1, data2)

    def test_galliard_form(self, concert_dir: Path):
        result = perform_concert(
            form="galliard",
            seed=7,
            measures=4,
            output_dir=concert_dir,
            visualize=False,
        )
        assert result["form"] == "galliard"
        wav_path = concert_dir / "concert_audio.wav"
        assert wav_path.exists()

    def test_result_metadata(self, concert_dir: Path):
        result = perform_concert(
            form="pavane",
            mode="mixolydian",
            seed=0,
            measures=8,
            tempo_bpm=90.0,
            reverb_wet=0.15,
            output_dir=concert_dir,
            visualize=False,
        )
        assert result["form"] == "pavane"
        assert result["mode"] == "mixolydian"
        assert result["seed"] == 0
        assert result["measures"] == 8
        assert result["tempo_bpm"] == 90.0
        assert result["reverb_wet"] == 0.15
        assert isinstance(result["instruments"], list)
        assert isinstance(result["total_events"], int)

    def test_visualizations_generated(self, concert_dir: Path):
        result = perform_concert(
            form="pavane",
            seed=42,
            measures=4,
            output_dir=concert_dir,
            visualize=True,
        )
        # Check that PNG files were generated
        waveform = concert_dir / "waveform.png"
        spectrogram = concert_dir / "spectrogram.png"
        score_roll = concert_dir / "score_roll.png"
        assert waveform.exists()
        assert spectrogram.exists()
        assert score_roll.exists()


class TestBackwardCompatibility:
    """Verify that the original render_score_to_wav works unchanged."""

    def test_render_without_timbres(self, tmp_path: Path):
        score = {
            "test_instrument": [
                {"time_s": 0.0, "frequency_hz": 440.0, "intensity": 8.0, "kind": "pitched"},
                {"time_s": 0.5, "frequency_hz": 550.0, "intensity": 6.0, "kind": "pitched"},
            ],
            "test_drum": [
                {"time_s": 0.25, "intensity": 10.0, "kind": "percussive"},
            ],
        }
        out = tmp_path / "test.wav"
        render_score_to_wav(score, 120.0, 4, out)
        assert out.exists()
        sr, data = wavfile.read(out)
        assert sr == 44100
        assert data.size > 0

    def test_render_with_timbres_and_slug(self, tmp_path: Path):
        score = {
            "viola_organista": [
                {
                    "time_s": 0.0,
                    "frequency_hz": 440.0,
                    "intensity": 8.0,
                    "kind": "pitched",
                    "slug": "viola_organista",
                    "duration_s": 0.5,
                },
            ],
        }
        out = tmp_path / "timbre_test.wav"
        render_score_to_wav(score, 120.0, 4, out, use_timbres=True)
        assert out.exists()
        sr, data = wavfile.read(out)
        assert sr == 44100
        assert data.size > 0

    def test_render_with_reverb(self, tmp_path: Path):
        score = {
            "organ": [
                {"time_s": 0.0, "frequency_hz": 440.0, "intensity": 8.0, "kind": "pitched"},
            ],
        }
        out = tmp_path / "reverb_test.wav"
        render_score_to_wav(score, 120.0, 4, out, reverb_wet=0.3)
        assert out.exists()
