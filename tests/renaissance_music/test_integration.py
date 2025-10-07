"""Tests for Renaissance music integration module."""

from unittest.mock import Mock, patch

from src.davinci_codex.renaissance_music.integration import MechanicalEnsembleIntegrator
from src.davinci_codex.renaissance_music.models import (
    AdaptationResult,
    InstrumentType,
    MusicalScore,
    Note,
    Voice,
)


class TestMechanicalEnsembleIntegrator:
    """Test the MechanicalEnsembleIntegrator class."""

    def test_integrator_creation(self) -> None:
        """Test creating a mechanical ensemble integrator."""
        integrator = MechanicalEnsembleIntegrator()
        assert integrator is not None
        assert hasattr(integrator, 'analyzer')
        assert hasattr(integrator, 'validator')
        assert hasattr(integrator, 'pattern_library')
        assert hasattr(integrator, 'instrument_modules')
        assert len(integrator.instrument_modules) == 6

    def test_adapt_score_for_ensemble_no_adaptation_needed(self) -> None:
        """Test adapting a score that doesn't need adaptation."""
        integrator = MechanicalEnsembleIntegrator()

        # Create a simple score that should be mechanically feasible
        voice = Voice()
        note = Note(pitch=200.0, duration=0.5, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = integrator.adapt_score_for_ensemble(score, instrument_assignments)

        assert isinstance(result, AdaptationResult)
        assert result.original_score == score
        assert result.adaptation_success is True
        assert len(result.adaptation_log) > 0
        assert any("mechanically feasible" in log for log in result.adaptation_log)

    def test_adapt_score_for_ensemble_with_adaptation(self) -> None:
        """Test adapting a score that needs adaptation."""
        integrator = MechanicalEnsembleIntegrator()

        # Create a score with issues that need adaptation
        voice = Voice()
        # Note outside drum's range and very short
        note = Note(pitch=2000.0, duration=0.01, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = integrator.adapt_score_for_ensemble(score, instrument_assignments)

        assert isinstance(result, AdaptationResult)
        assert result.original_score == score
        assert len(result.adaptation_log) > 0
        assert any("requires adaptation" in log for log in result.adaptation_log)

    def test_convert_to_ensemble_format(self) -> None:
        """Test converting a score to ensemble format."""
        integrator = MechanicalEnsembleIntegrator()

        # Create a simple score
        voice = Voice()
        note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_ORGAN}

        ensemble_score = integrator.convert_to_ensemble_format(
            score, instrument_assignments, tempo_bpm=120.0, measures=2
        )

        assert "mechanical_organ" in ensemble_score
        assert len(ensemble_score["mechanical_organ"]) > 0

        # Check the structure of the events
        event = ensemble_score["mechanical_organ"][0]
        assert "measure" in event or "index" in event
        assert "time_s" in event
        assert "frequency_hz" in event
        assert "intensity" in event
        assert "kind" in event
        assert event["kind"] == "pitched"

    def test_validate_with_simulation_no_assignment(self) -> None:
        """Test validation with simulation when no instrument assignment."""
        integrator = MechanicalEnsembleIntegrator()

        voice = Voice()
        note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {}  # No assignments

        result = integrator.validate_with_simulation(score, instrument_assignments)

        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert any("no instrument assignment" in error for error in result["errors"])

    @patch('src.davinci_codex.renaissance_music.integration.MechanicalEnsembleIntegrator._check_voice_simulation_compatibility')
    def test_validate_with_simulation_compatible(self, mock_check_compatibility) -> None:
        """Test validation with simulation when compatible."""
        integrator = MechanicalEnsembleIntegrator()

        # Mock the compatibility check to return compatible
        mock_check_compatibility.return_value = {
            "compatible": True,
            "errors": [],
            "warnings": []
        }

        voice = Voice()
        note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_ORGAN}

        result = integrator.validate_with_simulation(score, instrument_assignments)

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        mock_check_compatibility.assert_called_once()

    def test_check_voice_simulation_compatibility_empty_voice(self) -> None:
        """Test checking voice compatibility with empty voice."""
        integrator = MechanicalEnsembleIntegrator()

        voice = Voice()
        simulation_data = {"ideal_frequency_hz": [440.0, 880.0]}

        result = integrator._check_voice_simulation_compatibility(
            voice, simulation_data, InstrumentType.MECHANICAL_ORGAN
        )

        assert result["compatible"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) > 0
        assert "no sounding notes" in result["warnings"][0]

    def test_check_voice_simulation_compatibility_pitch_range(self) -> None:
        """Test checking voice compatibility with pitch range issues."""
        integrator = MechanicalEnsembleIntegrator()

        voice = Voice()
        # Add a note with very high pitch
        note = Note(pitch=10000.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        # Simulation data with much lower frequency range
        simulation_data = {"ideal_frequency_hz": [440.0, 880.0]}

        result = integrator._check_voice_simulation_compatibility(
            voice, simulation_data, InstrumentType.MECHANICAL_ORGAN
        )

        assert result["compatible"] is False
        assert len(result["errors"]) > 0
        assert any("outside simulation range" in error for error in result["errors"])

    def test_check_voice_simulation_compatibility_timing(self) -> None:
        """Test checking voice compatibility with timing issues."""
        integrator = MechanicalEnsembleIntegrator()

        voice = Voice()
        # Add a very short note
        note = Note(pitch=440.0, duration=0.01, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        # Simulation data with longer minimum interval
        simulation_data = {
            "ideal_frequency_hz": [440.0, 880.0],
            "ideal_times_s": [0.0, 0.5, 1.0, 1.5]
        }

        result = integrator._check_voice_simulation_compatibility(
            voice, simulation_data, InstrumentType.MECHANICAL_ORGAN
        )

        assert result["compatible"] is True  # Timing issues are warnings, not errors
        assert len(result["warnings"]) > 0
        assert any("very short notes" in warning for warning in result["warnings"])

    def test_extract_voice_events(self) -> None:
        """Test extracting events from a voice."""
        integrator = MechanicalEnsembleIntegrator()

        voice = Voice()
        note1 = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        note2 = Note(pitch=880.0, duration=1.0, velocity=0.7, start_time=1.0)
        voice.add_note(note1)
        voice.add_note(note2)

        events = integrator._extract_voice_events(voice, InstrumentType.MECHANICAL_ORGAN)

        assert len(events) == 2
        assert events[0]["frequency_hz"] == 440.0
        assert events[0]["intensity"] == 0.7
        assert events[0]["kind"] == "pitched"
        assert events[1]["frequency_hz"] == 880.0
        assert events[1]["intensity"] == 0.7
        assert events[1]["kind"] == "pitched"

    def test_extract_voice_events_with_rests(self) -> None:
        """Test extracting events from a voice with rests."""
        integrator = MechanicalEnsembleIntegrator()

        voice = Voice()
        note1 = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        rest = Note(pitch=0.0, duration=0.5, velocity=0.0, start_time=1.0, is_rest=True)
        note2 = Note(pitch=880.0, duration=1.0, velocity=0.7, start_time=1.5)
        voice.add_note(note1)
        voice.add_note(rest)
        voice.add_note(note2)

        events = integrator._extract_voice_events(voice, InstrumentType.MECHANICAL_ORGAN)

        assert len(events) == 2  # Rests should be excluded
        assert events[0]["frequency_hz"] == 440.0
        assert events[1]["frequency_hz"] == 880.0

    def test_extract_voice_events_percussive(self) -> None:
        """Test extracting events from a percussive instrument."""
        integrator = MechanicalEnsembleIntegrator()

        voice = Voice()
        note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        events = integrator._extract_voice_events(voice, InstrumentType.MECHANICAL_DRUM)

        assert len(events) == 1
        assert events[0]["kind"] == "percussive"

    @patch('src.davinci_codex.renaissance_music.integration.ensure_artifact_dir')
    @patch('src.davinci_codex.renaissance_music.integration.MechanicalEnsembleIntegrator.validate_with_simulation')
    def test_generate_ensemble_demo(self, mock_validate, mock_ensure_dir) -> None:
        """Test generating an ensemble demo."""
        integrator = MechanicalEnsembleIntegrator()

        # Mock the artifact directory
        mock_dir = Mock()
        mock_dir.__truediv__ = Mock(return_value=Mock())
        mock_ensure_dir.return_value = mock_dir

        # Mock validation to succeed
        mock_validate.return_value = {
            "valid": True,
            "warnings": [],
            "errors": []
        }

        # Create a simple score
        voice = Voice()
        note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_ORGAN}

        result = integrator.generate_ensemble_demo(
            score, instrument_assignments, tempo_bpm=120.0, measures=2
        )

        assert "artifacts" in result
        assert "tempo_bpm" in result
        assert "measures" in result
        assert "valid" in result
        assert "warnings" in result
        assert "errors" in result

        assert result["tempo_bpm"] == 120.0
        assert result["measures"] == 2
        assert result["valid"] is True
        assert len(result["artifacts"]) > 0
        assert len(result["warnings"]) == 0
        assert len(result["errors"]) == 0

    def test_adapt_pitch_ranges(self) -> None:
        """Test adapting pitch ranges."""
        integrator = MechanicalEnsembleIntegrator()

        # Create a voice with notes outside drum range
        voice = Voice()
        # Note too high
        note1 = Note(pitch=2000.0, duration=1.0, velocity=0.7, start_time=0.0)
        # Note too low
        note2 = Note(pitch=10.0, duration=1.0, velocity=0.7, start_time=1.0)
        voice.add_note(note1)
        voice.add_note(note2)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = AdaptationResult(
            original_score=score,
            adapted_score=score,
            adaptation_success=False
        )

        adapted_score = integrator._adapt_pitch_ranges(
            score, instrument_assignments, result
        )

        # Check that pitches were transposed into range
        adapted_voice = adapted_score.voices[0]
        for note in adapted_voice.notes:
            if not note.is_rest:
                constraints = integrator.validator.get_constraints(InstrumentType.MECHANICAL_DRUM)
                assert constraints.can_play_pitch(note.pitch)

        # Check that adaptation log was updated
        assert len(result.adaptation_log) > 0
        assert any("Transposed note" in log for log in result.adaptation_log)

    def test_adapt_note_durations(self) -> None:
        """Test adapting note durations."""
        integrator = MechanicalEnsembleIntegrator()

        # Create a voice with notes outside drum duration range
        voice = Voice()
        # Note too short
        note1 = Note(pitch=200.0, duration=0.01, velocity=0.7, start_time=0.0)
        # Note too long
        note2 = Note(pitch=200.0, duration=20.0, velocity=0.7, start_time=1.0)
        voice.add_note(note1)
        voice.add_note(note2)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = AdaptationResult(
            original_score=score,
            adapted_score=score,
            adaptation_success=False
        )

        adapted_score = integrator._adapt_note_durations(
            score, instrument_assignments, result
        )

        # Check that durations were adjusted
        adapted_voice = adapted_score.voices[0]
        constraints = integrator.validator.get_constraints(InstrumentType.MECHANICAL_DRUM)

        for note in adapted_voice.notes:
            if not note.is_rest:
                assert constraints.can_play_duration(note.duration)

        # Check that adaptation log was updated
        assert len(result.adaptation_log) > 0
        assert any("Lengthened note" in log or "Shortened note" in log
                  for log in result.adaptation_log)

    def test_adapt_rapid_passages(self) -> None:
        """Test adapting rapid passages."""
        integrator = MechanicalEnsembleIntegrator()

        # Create a voice with rapid passages
        voice = Voice()
        for i in range(20):  # More than max_rapid_passages for drum
            note = Note(pitch=200.0, duration=0.1, velocity=0.7, start_time=float(i * 0.05))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = AdaptationResult(
            original_score=score,
            adapted_score=score,
            adaptation_success=False
        )

        adapted_score = integrator._adapt_rapid_passages(
            score, instrument_assignments, result
        )

        # Check that rests were added between rapid notes
        adapted_voice = adapted_score.voices[0]
        rest_count = sum(1 for note in adapted_voice.notes if note.is_rest)
        assert rest_count > 0

        # Check that adaptation log was updated
        assert len(result.adaptation_log) > 0
        assert any("Simplified rapid passage" in log for log in result.adaptation_log)
