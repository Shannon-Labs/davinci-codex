"""Tests for Renaissance music data models."""

import pytest

from src.davinci_codex.renaissance_music.models import (
    AdaptationResult,
    InstrumentConstraints,
    InstrumentType,
    MusicalPattern,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


class TestNote:
    """Test the Note dataclass."""

    def test_note_creation(self) -> None:
        """Test creating a valid note."""
        note = Note(
            pitch=440.0,  # A4
            duration=1.0,
            velocity=0.7,
            start_time=0.0
        )
        assert note.pitch == 440.0
        assert note.duration == 1.0
        assert note.velocity == 0.7
        assert note.start_time == 0.0
        assert note.voice == 0
        assert note.is_rest is False

    def test_note_validation_invalid_pitch(self) -> None:
        """Test that invalid pitch raises ValueError."""
        with pytest.raises(ValueError, match="Pitch frequency must be non-negative"):
            Note(pitch=-1.0, duration=1.0, velocity=0.5, start_time=0.0)

    def test_note_validation_invalid_duration(self) -> None:
        """Test that invalid duration raises ValueError."""
        with pytest.raises(ValueError, match="Duration must be positive"):
            Note(pitch=440.0, duration=0.0, velocity=0.5, start_time=0.0)

    def test_note_validation_invalid_velocity(self) -> None:
        """Test that invalid velocity raises ValueError."""
        with pytest.raises(ValueError, match="Velocity must be between 0.0 and 1.0"):
            Note(pitch=440.0, duration=1.0, velocity=1.5, start_time=0.0)

    def test_note_validation_invalid_start_time(self) -> None:
        """Test that invalid start time raises ValueError."""
        with pytest.raises(ValueError, match="Start time must be non-negative"):
            Note(pitch=440.0, duration=1.0, velocity=0.5, start_time=-1.0)

    def test_rest_note(self) -> None:
        """Test creating a rest note."""
        rest = Note(
            pitch=0.0,
            duration=1.0,
            velocity=0.0,
            start_time=0.0,
            is_rest=True
        )
        assert rest.is_rest is True


class TestVoice:
    """Test the Voice dataclass."""

    def test_voice_creation(self) -> None:
        """Test creating a voice."""
        voice = Voice(name="Tenor", instrument=InstrumentType.MECHANICAL_ORGAN)
        assert voice.name == "Tenor"
        assert voice.instrument == InstrumentType.MECHANICAL_ORGAN
        assert voice.notes == []

    def test_add_note(self) -> None:
        """Test adding a note to a voice."""
        voice = Voice()
        note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        voice.add_note(note)
        assert len(voice.notes) == 1
        assert voice.notes[0] == note

    def test_get_pitch_range_empty(self) -> None:
        """Test getting pitch range of empty voice."""
        voice = Voice()
        pitch_range = voice.get_pitch_range()
        assert pitch_range == (0.0, 0.0)

    def test_get_pitch_range_only_rests(self) -> None:
        """Test getting pitch range of voice with only rests."""
        voice = Voice()
        rest = Note(pitch=0.0, duration=1.0, velocity=0.0, start_time=0.0, is_rest=True)
        voice.add_note(rest)
        pitch_range = voice.get_pitch_range()
        assert pitch_range == (0.0, 0.0)

    def test_get_pitch_range_with_notes(self) -> None:
        """Test getting pitch range of voice with notes."""
        voice = Voice()
        note1 = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        note2 = Note(pitch=880.0, duration=1.0, velocity=0.7, start_time=1.0)
        voice.add_note(note1)
        voice.add_note(note2)
        pitch_range = voice.get_pitch_range()
        assert pitch_range == (440.0, 880.0)


class TestMusicalScore:
    """Test the MusicalScore dataclass."""

    def test_score_creation(self) -> None:
        """Test creating a musical score."""
        score = MusicalScore(
            title="Test Piece",
            composer="Test Composer",
            mode=RenaissanceMode.DORIAN,
            tempo_bpm=120.0
        )
        assert score.title == "Test Piece"
        assert score.composer == "Test Composer"
        assert score.mode == RenaissanceMode.DORIAN
        assert score.tempo_bpm == 120.0
        assert score.voices == []

    def test_add_voice(self) -> None:
        """Test adding a voice to a score."""
        score = MusicalScore()
        voice = Voice(name="Tenor")
        score.add_voice(voice)
        assert len(score.voices) == 1
        assert score.voices[0] == voice

    def test_get_duration_empty(self) -> None:
        """Test getting duration of empty score."""
        score = MusicalScore()
        duration = score.get_duration()
        assert duration == 0.0

    def test_get_duration_with_voices(self) -> None:
        """Test getting duration of score with voices."""
        score = MusicalScore()
        voice1 = Voice()
        note1 = Note(pitch=440.0, duration=2.0, velocity=0.7, start_time=0.0)
        voice1.add_note(note1)
        score.add_voice(voice1)

        voice2 = Voice()
        note2 = Note(pitch=880.0, duration=3.0, velocity=0.7, start_time=0.0)
        voice2.add_note(note2)
        score.add_voice(voice2)

        duration = score.get_duration()
        assert duration == 3.0  # The longer voice determines the duration

    def test_get_voice_count(self) -> None:
        """Test getting voice count."""
        score = MusicalScore()
        assert score.get_voice_count() == 0

        score.add_voice(Voice())
        assert score.get_voice_count() == 1

        score.add_voice(Voice())
        assert score.get_voice_count() == 2

    def test_get_notes_at_time(self) -> None:
        """Test getting notes sounding at a specific time."""
        score = MusicalScore()
        voice = Voice()

        # Add notes at different times
        note1 = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0)
        note2 = Note(pitch=880.0, duration=1.0, velocity=0.7, start_time=0.5)
        voice.add_note(note1)
        voice.add_note(note2)
        score.add_voice(voice)

        # At time 0.75, both notes should be sounding
        sounding_notes = score.get_notes_at_time(0.75)
        assert len(sounding_notes) == 2
        assert sounding_notes[0][1] == note1
        assert sounding_notes[1][1] == note2

        # At time 1.5, no notes should be sounding
        sounding_notes = score.get_notes_at_time(1.5)
        assert len(sounding_notes) == 0


class TestInstrumentConstraints:
    """Test the InstrumentConstraints dataclass."""

    def test_constraints_creation(self) -> None:
        """Test creating instrument constraints."""
        constraints = InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_ORGAN,
            pitch_range=(100.0, 1000.0),
            max_polyphony=4
        )
        assert constraints.instrument_type == InstrumentType.MECHANICAL_ORGAN
        assert constraints.pitch_range == (100.0, 1000.0)
        assert constraints.max_polyphony == 4

    def test_can_play_pitch(self) -> None:
        """Test checking if instrument can play a pitch."""
        constraints = InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_ORGAN,
            pitch_range=(200.0, 800.0)
        )

        # Within range
        assert constraints.can_play_pitch(400.0) is True

        # Below range
        assert constraints.can_play_pitch(100.0) is False

        # Above range
        assert constraints.can_play_pitch(1000.0) is False

    def test_can_play_duration(self) -> None:
        """Test checking if instrument can play a duration."""
        constraints = InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_ORGAN,
            pitch_range=(100.0, 1000.0),
            min_note_duration=0.2,
            max_note_duration=5.0
        )

        # Within range
        assert constraints.can_play_duration(1.0) is True

        # Too short
        assert constraints.can_play_duration(0.1) is False

        # Too long
        assert constraints.can_play_duration(10.0) is False

    def test_calculate_mechanical_feasibility_empty(self) -> None:
        """Test calculating feasibility for empty note list."""
        constraints = InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_ORGAN,
            pitch_range=(100.0, 1000.0)
        )
        feasibility = constraints.calculate_mechanical_feasibility([])
        assert feasibility == 1.0

    def test_calculate_mechanical_feasibility(self) -> None:
        """Test calculating mechanical feasibility."""
        constraints = InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_ORGAN,
            pitch_range=(200.0, 800.0),
            min_note_duration=0.2,
            max_note_duration=5.0,
            max_rapid_passages=4,
            rapid_passage_threshold=0.3
        )

        # Create notes with some issues
        notes = [
            Note(pitch=100.0, duration=1.0, velocity=0.7, start_time=0.0),  # Too low
            Note(pitch=1000.0, duration=1.0, velocity=0.7, start_time=1.0), # Too high
            Note(pitch=0.1, duration=1.0, velocity=0.7, start_time=2.0),     # Too short
        ]

        feasibility = constraints.calculate_mechanical_feasibility(notes)
        assert feasibility < 1.0
        assert feasibility >= 0.0


class TestMusicalPattern:
    """Test the MusicalPattern dataclass."""

    def test_pattern_creation(self) -> None:
        """Test creating a musical pattern."""
        notes = [
            Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0),
            Note(pitch=880.0, duration=1.0, velocity=0.7, start_time=1.0),
        ]

        pattern = MusicalPattern(
            name="test_pattern",
            pattern_type="test",
            mode=RenaissanceMode.DORIAN,
            notes=notes,
            voice_leading=[(440.0, 880.0)],
            rhythm_profile=[1.0, 1.0]
        )

        assert pattern.name == "test_pattern"
        assert pattern.pattern_type == "test"
        assert pattern.mode == RenaissanceMode.DORIAN
        assert pattern.notes == notes
        assert pattern.voice_leading == [(440.0, 880.0)]
        assert pattern.rhythm_profile == [1.0, 1.0]

    def test_get_interval_pattern(self) -> None:
        """Test getting interval pattern."""
        notes = [
            Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0),  # A4
            Note(pitch=880.0, duration=1.0, velocity=0.7, start_time=1.0),  # A5 (octave up)
            Note(pitch=660.0, duration=1.0, velocity=0.7, start_time=2.0),  # E5 (perfect fifth down)
        ]

        pattern = MusicalPattern(
            name="test_pattern",
            pattern_type="test",
            mode=RenaissanceMode.DORIAN,
            notes=notes,
            voice_leading=[],
            rhythm_profile=[]
        )

        intervals = pattern.get_interval_pattern()
        assert len(intervals) == 2
        assert abs(intervals[0] - 12.0) < 0.1  # Octave
        # The interval calculation is based on frequency ratios, not simple semitone differences
        # 660/880 = 0.75, which is approximately a perfect fourth down (5 semitones)
        assert abs(intervals[1] - -5.0) < 0.5  # Perfect fourth down (approximately)

    def test_get_rhythmic_pattern(self) -> None:
        """Test getting rhythmic pattern."""
        notes = [
            Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0),
            Note(pitch=880.0, duration=0.5, velocity=0.7, start_time=1.0),
            Note(pitch=660.0, duration=2.0, velocity=0.7, start_time=1.5),
        ]

        pattern = MusicalPattern(
            name="test_pattern",
            pattern_type="test",
            mode=RenaissanceMode.DORIAN,
            notes=notes,
            voice_leading=[],
            rhythm_profile=[]
        )

        rhythm = pattern.get_rhythmic_pattern()
        assert rhythm == [1.0, 0.5, 2.0]


class TestAdaptationResult:
    """Test the AdaptationResult dataclass."""

    def test_adaptation_result_creation(self) -> None:
        """Test creating an adaptation result."""
        original_score = MusicalScore(title="Original")
        adapted_score = MusicalScore(title="Adapted")

        result = AdaptationResult(
            original_score=original_score,
            adapted_score=adapted_score
        )

        assert result.original_score == original_score
        assert result.adapted_score == adapted_score
        assert result.adaptation_log == []
        assert result.constraint_violations == []
        assert result.pattern_substitutions == {}
        assert result.feasibility_scores == {}
        assert result.adaptation_success is False

    def test_add_log_entry(self) -> None:
        """Test adding log entries."""
        original_score = MusicalScore()
        adapted_score = MusicalScore()

        result = AdaptationResult(
            original_score=original_score,
            adapted_score=adapted_score
        )

        result.add_log_entry("Test log entry")
        assert len(result.adaptation_log) == 1
        assert result.adaptation_log[0] == "Test log entry"

    def test_add_violation(self) -> None:
        """Test adding constraint violations."""
        original_score = MusicalScore()
        adapted_score = MusicalScore()

        result = AdaptationResult(
            original_score=original_score,
            adapted_score=adapted_score
        )

        result.add_violation("Test violation")
        assert len(result.constraint_violations) == 1
        assert result.constraint_violations[0] == "Test violation"

    def test_add_pattern_substitution(self) -> None:
        """Test adding pattern substitutions."""
        original_score = MusicalScore()
        adapted_score = MusicalScore()

        result = AdaptationResult(
            original_score=original_score,
            adapted_score=adapted_score
        )

        result.add_pattern_substitution("original", "replacement")
        assert result.pattern_substitutions["original"] == "replacement"

    def test_set_feasibility_score(self) -> None:
        """Test setting feasibility scores."""
        original_score = MusicalScore()
        adapted_score = MusicalScore()

        result = AdaptationResult(
            original_score=original_score,
            adapted_score=adapted_score
        )

        result.set_feasibility_score(InstrumentType.MECHANICAL_ORGAN, 0.8)
        assert result.feasibility_scores[InstrumentType.MECHANICAL_ORGAN] == 0.8

    def test_get_overall_feasibility_empty(self) -> None:
        """Test getting overall feasibility with no scores."""
        original_score = MusicalScore()
        adapted_score = MusicalScore()

        result = AdaptationResult(
            original_score=original_score,
            adapted_score=adapted_score
        )

        feasibility = result.get_overall_feasibility()
        assert feasibility == 0.0

    def test_get_overall_feasibility(self) -> None:
        """Test getting overall feasibility with scores."""
        original_score = MusicalScore()
        adapted_score = MusicalScore()

        result = AdaptationResult(
            original_score=original_score,
            adapted_score=adapted_score
        )

        result.set_feasibility_score(InstrumentType.MECHANICAL_ORGAN, 0.8)
        result.set_feasibility_score(InstrumentType.MECHANICAL_DRUM, 0.6)

        feasibility = result.get_overall_feasibility()
        assert feasibility == 0.7  # (0.8 + 0.6) / 2
