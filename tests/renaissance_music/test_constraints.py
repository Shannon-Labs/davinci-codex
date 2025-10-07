"""Tests for Renaissance music constraint engine."""


from src.davinci_codex.renaissance_music.constraints import MechanicalConstraintValidator
from src.davinci_codex.renaissance_music.models import (
    AdaptationResult,
    InstrumentConstraints,
    InstrumentType,
    MusicalScore,
    Note,
    Voice,
)


class TestMechanicalConstraintValidator:
    """Test the MechanicalConstraintValidator class."""

    def test_validator_creation(self) -> None:
        """Test creating a constraint validator."""
        validator = MechanicalConstraintValidator()
        assert validator is not None
        assert len(validator.constraints) > 0
        assert InstrumentType.MECHANICAL_DRUM in validator.constraints

    def test_set_constraints(self) -> None:
        """Test setting custom constraints."""
        validator = MechanicalConstraintValidator()

        custom_constraints = InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_ORGAN,
            pitch_range=(100.0, 1000.0),
            max_polyphony=6
        )

        validator.set_constraints(InstrumentType.MECHANICAL_ORGAN, custom_constraints)

        retrieved = validator.get_constraints(InstrumentType.MECHANICAL_ORGAN)
        assert retrieved.pitch_range == (100.0, 1000.0)
        assert retrieved.max_polyphony == 6

    def test_get_constraints_default(self) -> None:
        """Test getting default constraints."""
        validator = MechanicalConstraintValidator()

        constraints = validator.get_constraints(InstrumentType.MECHANICAL_ORGAN)
        assert constraints.instrument_type == InstrumentType.MECHANICAL_ORGAN
        assert constraints.pitch_range[0] > 0
        assert constraints.pitch_range[1] > constraints.pitch_range[0]

    def test_validate_score_empty(self) -> None:
        """Test validating an empty score."""
        validator = MechanicalConstraintValidator()
        score = MusicalScore()
        instrument_assignments = {}

        result = validator.validate_score(score, instrument_assignments)
        assert isinstance(result, AdaptationResult)
        assert result.original_score == score
        assert result.adapted_score == score

    def test_validate_score_no_assignment(self) -> None:
        """Test validating a score with no instrument assignments."""
        validator = MechanicalConstraintValidator()

        voice = Voice()
        note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {}  # No assignments

        result = validator.validate_score(score, instrument_assignments)
        assert result.adaptation_success is False
        assert len(result.constraint_violations) > 0
        assert any("no instrument assignment" in violation for violation in result.constraint_violations)

    def test_validate_score_pitch_range_violation(self) -> None:
        """Test validating a score with pitch range violations."""
        validator = MechanicalConstraintValidator()

        voice = Voice()
        # Note outside drum's range
        note = Note(pitch=2000.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = validator.validate_score(score, instrument_assignments)
        assert result.adaptation_success is False
        assert len(result.constraint_violations) > 0
        assert any("outside instrument range" in violation for violation in result.constraint_violations)

    def test_validate_score_duration_violation(self) -> None:
        """Test validating a score with duration violations."""
        validator = MechanicalConstraintValidator()

        voice = Voice()
        # Very short note
        note = Note(pitch=440.0, duration=0.01, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = validator.validate_score(score, instrument_assignments)
        assert result.adaptation_success is False
        assert len(result.constraint_violations) > 0
        assert any("outside the valid range" in violation for violation in result.constraint_violations)

    def test_validate_score_rapid_passage_violation(self) -> None:
        """Test validating a score with rapid passage violations."""
        validator = MechanicalConstraintValidator()

        voice = Voice()

        # Create rapid notes
        for i in range(20):  # More than max_rapid_passages for drum
            note = Note(pitch=440.0, duration=0.1, velocity=0.7, start_time=float(i * 0.05))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = validator.validate_score(score, instrument_assignments)
        assert result.adaptation_success is False
        assert len(result.constraint_violations) > 0
        assert any("Rapid passage" in violation for violation in result.constraint_violations)

    def test_validate_score_polyphony_violation(self) -> None:
        """Test validating a score with polyphony violations."""
        validator = MechanicalConstraintValidator()

        # Create multiple voices with simultaneous notes
        voices = []
        for _voice_idx in range(3):  # More than drum's max_polyphony of 1
            voice = Voice()
            note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
            voice.add_note(note)
            voices.append(voice)

        score = MusicalScore()
        for voice in voices:
            score.add_voice(voice)

        # Assign all voices to drum (max_polyphony=1)
        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM,
                                 1: InstrumentType.MECHANICAL_DRUM,
                                 2: InstrumentType.MECHANICAL_DRUM}

        result = validator.validate_score(score, instrument_assignments)
        assert result.adaptation_success is False
        assert len(result.constraint_violations) > 0
        assert any("simultaneous notes" in violation for violation in result.constraint_violations)

    def test_validate_score_successful(self) -> None:
        """Test validating a score that should pass all constraints."""
        validator = MechanicalConstraintValidator()

        voice = Voice()

        # Create notes within drum's constraints
        for i in range(4):
            note = Note(pitch=200.0, duration=0.5, velocity=0.7, start_time=float(i * 0.6))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        result = validator.validate_score(score, instrument_assignments)
        assert result.adaptation_success is True
        assert len(result.constraint_violations) == 0

    def test_validate_voice_empty(self) -> None:
        """Test validating an empty voice."""
        validator = MechanicalConstraintValidator()

        voice = Voice()
        constraints = validator.get_constraints(InstrumentType.MECHANICAL_DRUM)

        result = validator.validate_voice(voice, constraints)
        assert isinstance(result, AdaptationResult)
        assert result.adaptation_success is True

    def test_validate_voice_pitch_range(self) -> None:
        """Test validating a voice with pitch range issues."""
        validator = MechanicalConstraintValidator()

        voice = Voice()
        # Note outside drum's range
        note = Note(pitch=2000.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        constraints = validator.get_constraints(InstrumentType.MECHANICAL_DRUM)

        result = validator.validate_voice(voice, constraints)
        assert result.adaptation_success is False
        assert len(result.constraint_violations) > 0

    def test_suggest_adaptations(self) -> None:
        """Test suggesting adaptations for a score."""
        validator = MechanicalConstraintValidator()

        voice = Voice()
        # Note outside drum's range
        note = Note(pitch=2000.0, duration=0.01, velocity=0.7, start_time=0.0)
        voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        suggestions = validator.suggest_adaptations(score, instrument_assignments)
        assert len(suggestions) > 0
        assert any("transpose" in suggestion.lower() for suggestion in suggestions)

    def test_suggest_adaptations_feasibility_scores(self) -> None:
        """Test suggesting adaptations based on feasibility scores."""
        validator = MechanicalConstraintValidator()

        voice = Voice()
        # Multiple issues with the voice
        for i in range(20):
            note = Note(pitch=2000.0, duration=0.01, velocity=0.7, start_time=float(i * 0.01))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        instrument_assignments = {0: InstrumentType.MECHANICAL_DRUM}

        suggestions = validator.suggest_adaptations(score, instrument_assignments)
        assert len(suggestions) > 0
        assert any("different instrument" in suggestion.lower() for suggestion in suggestions)
