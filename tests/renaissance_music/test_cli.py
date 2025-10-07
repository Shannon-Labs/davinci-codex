"""Tests for the Renaissance music CLI module."""

import json
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from src.davinci_codex.renaissance_music.cli import (
    app,
    get_form,
    get_instrument_mapping,
    get_mode,
    load_from_json,
    save_as_json,
)
from src.davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path


@pytest.fixture
def sample_score():
    """Create a sample musical score for testing."""
    # Create a simple score with two voices
    voice1_notes = [
        Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0),
        Note(pitch=493.88, duration=1.0, velocity=0.7, start_time=1.0),
        Note(pitch=523.25, duration=2.0, velocity=0.7, start_time=2.0),
    ]

    voice2_notes = [
        Note(pitch=261.63, duration=1.0, velocity=0.6, start_time=0.0),
        Note(pitch=293.66, duration=1.0, velocity=0.6, start_time=1.0),
        Note(pitch=329.63, duration=2.0, velocity=0.6, start_time=2.0),
    ]

    voice1 = Voice(name="Voice 1", notes=voice1_notes, instrument=InstrumentType.PROGRAMMABLE_FLUTE)
    voice2 = Voice(name="Voice 2", notes=voice2_notes, instrument=InstrumentType.VIOLA_ORGANISTA)

    score = MusicalScore(
        title="Test Score",
        composer="Test Composer",
        mode=RenaissanceMode.LYDIAN,
        form=MusicalForm.PAVANE,
        tempo_bpm=100.0
    )
    score.add_voice(voice1)
    score.add_voice(voice2)

    return score


class TestCLIHelpers:
    """Test CLI helper functions."""

    def test_get_instrument_mapping(self):
        """Test parsing instrument mapping string."""
        mapping_str = "0:flute,1:viola,2:organ"
        mapping = get_instrument_mapping(mapping_str)

        assert mapping == {
            0: InstrumentType.PROGRAMMABLE_FLUTE,
            1: InstrumentType.VIOLA_ORGANISTA,
            2: InstrumentType.MECHANICAL_ORGAN,
        }

    def test_get_instrument_mapping_invalid(self):
        """Test parsing invalid instrument mapping string."""
        with pytest.raises(SystemExit):
            get_instrument_mapping("0:invalid_instrument")

    def test_get_mode(self):
        """Test parsing mode string."""
        assert get_mode("dorian") == RenaissanceMode.DORIAN
        assert get_mode("phrygian") == RenaissanceMode.PHRYGIAN
        assert get_mode("lydian") == RenaissanceMode.LYDIAN
        assert get_mode("mixolydian") == RenaissanceMode.MIXOLYDIAN

    def test_get_mode_invalid(self):
        """Test parsing invalid mode string."""
        with pytest.raises(SystemExit):
            get_mode("invalid_mode")

    def test_get_form(self):
        """Test parsing form string."""
        assert get_form("pavane") == MusicalForm.PAVANE
        assert get_form("galliard") == MusicalForm.GALLIARD
        assert get_form("basse_danse") == MusicalForm.BASSE_DANSE
        assert get_form("chanson") == MusicalForm.CHANSON

    def test_get_form_invalid(self):
        """Test parsing invalid form string."""
        with pytest.raises(SystemExit):
            get_form("invalid_form")

    def test_save_as_json(self, sample_score, temp_dir):
        """Test saving a score as JSON."""
        output_path = temp_dir / "test_score.json"
        save_as_json(sample_score, output_path)

        # Check that file was created
        assert output_path.exists()

        # Check content
        with output_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["title"] == "Test Score"
        assert data["composer"] == "Test Composer"
        assert data["mode"] == "lydian"
        assert data["form"] == "pavane"
        assert data["tempo_bpm"] == 100.0
        assert len(data["voices"]) == 2

    def test_load_from_json(self, sample_score, temp_dir):
        """Test loading a score from JSON."""
        # First save the score
        output_path = temp_dir / "test_score.json"
        save_as_json(sample_score, output_path)

        # Then load it
        loaded_score = load_from_json(output_path)

        # Check that properties match
        assert loaded_score.title == sample_score.title
        assert loaded_score.composer == sample_score.composer
        assert loaded_score.mode == sample_score.mode
        assert loaded_score.form == sample_score.form
        assert loaded_score.tempo_bpm == sample_score.tempo_bpm
        assert len(loaded_score.voices) == len(sample_score.voices)


class TestCLICommands:
    """Test CLI commands."""

    @patch("src.davinci_codex.renaissance_music.cli.RenaissanceCompositionGenerator")
    def test_generate_command(self, mock_generator, runner, temp_dir):
        """Test the generate command."""
        # Mock the generator
        mock_instance = MagicMock()
        mock_generator.return_value = mock_instance

        # Mock the score
        mock_score = MagicMock()
        mock_score.title = "Generated Score"
        mock_score.tempo_bpm = 100.0
        mock_score.voices = []
        mock_instance.generate_composition.return_value = mock_score

        # Run the command
        output_path = temp_dir / "generated_score.json"
        result = runner.invoke(app, [
            "generate",
            "--form", "pavane",
            "--mode", "lydian",
            "--instruments", "0:flute,1:viola,2:organ",
            "--measures", "16",
            "--output", str(output_path),
            "--seed", "42"
        ])

        # Check that command succeeded
        assert result.exit_code == 0

        # Check that generator was called with correct arguments
        mock_instance.generate_composition.assert_called_once()
        call_args = mock_instance.generate_composition.call_args
        assert call_args.kwargs["form"] == MusicalForm.PAVANE
        assert call_args.kwargs["mode"] == RenaissanceMode.LYDIAN
        assert call_args.kwargs["measures"] == 16
        assert call_args.kwargs["seed"] == 42

    @patch("src.davinci_codex.renaissance_music.cli.MechanicalEnsembleIntegrator")
    def test_adapt_command(self, mock_integrator, runner, temp_dir, sample_score):
        """Test the adapt command."""
        # Save the sample score
        input_path = temp_dir / "input_score.json"
        save_as_json(sample_score, input_path)

        # Mock the integrator
        mock_instance = MagicMock()
        mock_integrator.return_value = mock_instance

        # Mock the adaptation result
        mock_result = MagicMock()
        mock_result.adaptation_success = True
        mock_result.adaptation_log = ["Log entry 1", "Log entry 2"]
        mock_result.adapted_score = sample_score
        mock_result.feasibility_scores = {}
        mock_instance.adapt_score_for_ensemble.return_value = mock_result

        # Run the command
        output_path = temp_dir / "adapted_score.json"
        result = runner.invoke(app, [
            "adapt",
            "--input-file", str(input_path),
            "--instruments", "0:flute,1:viola,2:organ",
            "--output", str(output_path)
        ])

        # Check that command succeeded
        assert result.exit_code == 0

        # Check that integrator was called
        mock_instance.adapt_score_for_ensemble.assert_called_once()

    @patch("src.davinci_codex.renaissance_music.cli.RenaissanceCompositionGenerator")
    @patch("src.davinci_codex.renaissance_music.cli.MechanicalEnsembleIntegrator")
    def test_demo_command(self, mock_integrator, mock_generator, runner):
        """Test the demo command."""
        # Mock the generator
        mock_generator_instance = MagicMock()
        mock_generator.return_value = mock_generator_instance

        # Mock the score
        mock_score = MagicMock()
        mock_score.title = "Demo Score"
        mock_score.tempo_bpm = 100.0
        mock_score.voices = []
        mock_score.get_duration.return_value = 30.0
        mock_generator_instance.generate_composition.return_value = mock_score

        # Mock the integrator
        mock_integrator_instance = MagicMock()
        mock_integrator.return_value = mock_integrator_instance

        # Mock the adaptation result
        mock_result = MagicMock()
        mock_result.adaptation_success = True
        mock_result.adapted_score = mock_score
        mock_integrator_instance.adapt_score_for_ensemble.return_value = mock_result

        # Mock the demo result
        mock_demo_result = {
            "valid": True,
            "artifacts": ["artifact1.wav", "artifact2.json"],
            "errors": [],
            "warnings": []
        }
        mock_integrator_instance.generate_ensemble_demo.return_value = mock_demo_result

        # Run the command
        result = runner.invoke(app, [
            "demo",
            "--form", "pavane",
            "--mode", "lydian",
            "--measures", "16",
            "--render-audio",
            "--seed", "42"
        ])

        # Check that command succeeded
        assert result.exit_code == 0

        # Check that generator and integrator were called
        mock_generator_instance.generate_composition.assert_called_once()
        mock_integrator_instance.adapt_score_for_ensemble.assert_called_once()
        mock_integrator_instance.generate_ensemble_demo.assert_called_once()

    @patch("src.davinci_codex.renaissance_music.cli.RenaissancePatternLibrary")
    def test_patterns_command(self, mock_library, runner):
        """Test the patterns command."""
        # Mock the pattern library
        mock_instance = MagicMock()
        mock_library.return_value = mock_instance

        # Mock patterns
        mock_pattern = MagicMock()
        mock_pattern.name = "test_pattern"
        mock_pattern.pattern_type = "dance_figure"
        mock_pattern.mode = RenaissanceMode.LYDIAN
        mock_pattern.notes = []
        mock_pattern.context_tags = ["test"]
        mock_instance.get_all_patterns.return_value = [mock_pattern]

        # Run the command
        result = runner.invoke(app, [
            "patterns"
        ])

        # Check that command succeeded
        assert result.exit_code == 0

        # Check that library was called
        mock_instance.get_all_patterns.assert_called_once()

    @patch("src.davinci_codex.renaissance_music.cli.RenaissanceMusicDataset")
    def test_dataset_stats_command(self, mock_dataset, runner):
        """Test the dataset stats command."""
        # Mock the dataset
        mock_instance = MagicMock()
        mock_dataset.return_value = mock_instance

        # Mock statistics
        mock_stats = {
            "total_entries": 10,
            "modes": {"dorian": 3, "lydian": 4, "mixolydian": 3},
            "forms": {"pavane": 5, "galliard": 3, "basse_danse": 2},
            "categories": {"dance": 6, "vocal": 4},
            "difficulty_levels": {"1": 2, "2": 3, "3": 3, "4": 2}
        }
        mock_instance.get_statistics.return_value = mock_stats

        # Run the command
        result = runner.invoke(app, [
            "dataset",
            "--action", "stats"
        ])

        # Check that command succeeded
        assert result.exit_code == 0

        # Check that dataset was called
        mock_instance.get_statistics.assert_called_once()

    @patch("src.davinci_codex.renaissance_music.cli.RenaissanceMusicDataset")
    def test_dataset_list_command(self, mock_dataset, runner):
        """Test the dataset list command."""
        # Mock the dataset
        mock_instance = MagicMock()
        mock_dataset.return_value = mock_instance

        # Mock entries
        mock_entry = MagicMock()
        mock_entry.title = "Test Entry"
        mock_entry.composer = "Test Composer"
        mock_entry.year = 1500
        mock_entry.mode = RenaissanceMode.LYDIAN
        mock_entry.form = MusicalForm.PAVANE
        mock_entry.category = "dance"
        mock_entry.difficulty_level = 2
        mock_instance.get_all_entries.return_value = [mock_entry]

        # Run the command
        result = runner.invoke(app, [
            "dataset",
            "--action", "list"
        ])

        # Check that command succeeded
        assert result.exit_code == 0

        # Check that dataset was called
        mock_instance.get_all_entries.assert_called_once()

    @patch("src.davinci_codex.renaissance_music.cli.RenaissanceMusicDataset")
    def test_dataset_query_command(self, mock_dataset, runner):
        """Test the dataset query command."""
        # Mock the dataset
        mock_instance = MagicMock()
        mock_dataset.return_value = mock_instance

        # Mock entry
        mock_entry = MagicMock()
        mock_entry.title = "Test Entry"
        mock_entry.composer = "Test Composer"
        mock_entry.year = 1500
        mock_entry.mode = RenaissanceMode.LYDIAN
        mock_entry.form = MusicalForm.PAVANE
        mock_entry.category = "dance"
        mock_entry.difficulty_level = 2
        mock_entry.score = MagicMock()
        mock_entry.score.tempo_bpm = 100.0
        mock_entry.score.voices = []
        mock_entry.score.get_duration.return_value = 30.0
        mock_entry.source_reference = "Test source"
        mock_instance.get_random_entry.return_value = mock_entry

        # Run the command
        result = runner.invoke(app, [
            "dataset",
            "--action", "query",
            "--mode", "lydian",
            "--form", "pavane"
        ])

        # Check that command succeeded
        assert result.exit_code == 0

        # Check that dataset was called
        mock_instance.get_random_entry.assert_called_once()
