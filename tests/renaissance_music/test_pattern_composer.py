"""Tests for the Renaissance music pattern composer module."""

import pytest

from src.davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalPattern,
    Note,
    RenaissanceMode,
)
from src.davinci_codex.renaissance_music.pattern_composer import PatternBasedComposer


@pytest.fixture
def pattern_composer():
    """Create a pattern composer for testing."""
    return PatternBasedComposer()


@pytest.fixture
def instrument_assignments():
    """Create instrument assignments for testing."""
    return {
        0: InstrumentType.PROGRAMMABLE_FLUTE,
        1: InstrumentType.VIOLA_ORGANISTA,
        2: InstrumentType.MECHANICAL_ORGAN,
    }


@pytest.fixture
def sample_pattern():
    """Create a sample pattern for testing."""
    notes = [
        Note(pitch=440.0, duration=0.5, velocity=0.7, start_time=0.0),
        Note(pitch=493.88, duration=0.5, velocity=0.7, start_time=0.5),
        Note(pitch=523.25, duration=1.0, velocity=0.7, start_time=1.0),
    ]

    return MusicalPattern(
        name="sample_pattern",
        pattern_type="dance_figure",
        mode=RenaissanceMode.LYDIAN,
        notes=notes,
        voice_leading=[(440.0, 493.88), (493.88, 523.25)],
        rhythm_profile=[0.5, 0.5, 1.0],
        context_tags=["sample", "test"],
        source_reference="Test pattern"
    )


class TestPatternBasedComposer:
    """Test the PatternBasedComposer class."""

    def test_initialization(self, pattern_composer):
        """Test that the pattern composer initializes correctly."""
        assert pattern_composer is not None
        assert pattern_composer.pattern_library is not None
        assert len(pattern_composer._transition_rules) > 0
        assert len(pattern_composer._mode_transitions) > 0

    def test_compose_pavane(self, pattern_composer, instrument_assignments):
        """Test composition of a pavane."""
        score = pattern_composer.compose_by_patterns(
            form=MusicalForm.PAVANE,
            mode=RenaissanceMode.LYDIAN,
            instrument_assignments=instrument_assignments,
            measures=16,
            seed=42
        )

        assert score is not None
        assert score.form == MusicalForm.PAVANE
        assert score.mode == RenaissanceMode.LYDIAN
        assert len(score.voices) == len(instrument_assignments)
        assert 80 <= score.tempo_bpm <= 110  # Pavane tempo range

    def test_compose_galliard(self, pattern_composer, instrument_assignments):
        """Test composition of a galliard."""
        score = pattern_composer.compose_by_patterns(
            form=MusicalForm.GALLIARD,
            mode=RenaissanceMode.MIXOLYDIAN,
            instrument_assignments=instrument_assignments,
            measures=12,
            seed=123
        )

        assert score is not None
        assert score.form == MusicalForm.GALLIARD
        assert score.mode == RenaissanceMode.MIXOLYDIAN
        assert len(score.voices) == len(instrument_assignments)
        assert 120 <= score.tempo_bpm <= 140  # Galliard tempo range

    def test_compose_basse_danse(self, pattern_composer, instrument_assignments):
        """Test composition of a basse danse."""
        score = pattern_composer.compose_by_patterns(
            form=MusicalForm.BASSE_DANSE,
            mode=RenaissanceMode.DORIAN,
            instrument_assignments=instrument_assignments,
            measures=16,
            seed=456
        )

        assert score is not None
        assert score.form == MusicalForm.BASSE_DANSE
        assert score.mode == RenaissanceMode.DORIAN
        assert len(score.voices) == len(instrument_assignments)
        assert 60 <= score.tempo_bpm <= 80  # Basse danse tempo range

    def test_transform_pattern_to_mode(self, pattern_composer, sample_pattern):
        """Test transformation of a pattern to a different mode."""
        target_mode = RenaissanceMode.DORIAN

        transformed_pattern = pattern_composer.transform_pattern_to_mode(
            sample_pattern, target_mode
        )

        assert transformed_pattern is not None
        assert transformed_pattern.mode == target_mode
        assert transformed_pattern.pattern_type == sample_pattern.pattern_type
        assert len(transformed_pattern.notes) == len(sample_pattern.notes)

    def test_create_variation_diminution(self, pattern_composer, sample_pattern):
        """Test creation of a diminution variation."""
        variation = pattern_composer.create_variation(
            sample_pattern, variation_type="diminution"
        )

        assert variation is not None
        assert variation.pattern_type == sample_pattern.pattern_type
        assert variation.mode == sample_pattern.mode

        # Diminution should have more notes
        assert len(variation.notes) >= len(sample_pattern.notes)

    def test_create_variation_ornamentation(self, pattern_composer, sample_pattern):
        """Test creation of an ornamentation variation."""
        variation = pattern_composer.create_variation(
            sample_pattern, variation_type="ornamentation"
        )

        assert variation is not None
        assert variation.pattern_type == sample_pattern.pattern_type
        assert variation.mode == sample_pattern.mode

        # Ornamentation should have more notes
        assert len(variation.notes) >= len(sample_pattern.notes)

    def test_create_variation_rhythmic(self, pattern_composer, sample_pattern):
        """Test creation of a rhythmic variation."""
        variation = pattern_composer.create_variation(
            sample_pattern, variation_type="rhythmic"
        )

        assert variation is not None
        assert variation.pattern_type == sample_pattern.pattern_type
        assert variation.mode == sample_pattern.mode

    def test_ensure_smooth_transitions(self, pattern_composer):
        """Test ensuring smooth transitions between patterns."""
        # Create two patterns with a smooth transition
        pattern1_notes = [
            Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0),
            Note(pitch=493.88, duration=1.0, velocity=0.7, start_time=1.0),
        ]

        pattern2_notes = [
            Note(pitch=523.25, duration=1.0, velocity=0.7, start_time=0.0),
            Note(pitch=587.33, duration=1.0, velocity=0.7, start_time=1.0),
        ]

        pattern1 = MusicalPattern(
            name="pattern1",
            pattern_type="dance_figure",
            mode=RenaissanceMode.LYDIAN,
            notes=pattern1_notes,
            voice_leading=[(440.0, 493.88)],
            rhythm_profile=[1.0, 1.0],
            context_tags=["test"],
            source_reference="Test pattern 1"
        )

        pattern2 = MusicalPattern(
            name="pattern2",
            pattern_type="dance_figure",
            mode=RenaissanceMode.LYDIAN,
            notes=pattern2_notes,
            voice_leading=[(523.25, 587.33)],
            rhythm_profile=[1.0, 1.0],
            context_tags=["test"],
            source_reference="Test pattern 2"
        )

        smooth_patterns = pattern_composer.ensure_smooth_transitions(
            [pattern1, pattern2], RenaissanceMode.LYDIAN
        )

        assert len(smooth_patterns) >= 2  # Should have at least the original patterns

    def test_voice_role_assignment(self, pattern_composer, instrument_assignments):
        """Test that voice roles are assigned correctly."""
        score = pattern_composer.compose_by_patterns(
            form=MusicalForm.PAVANE,
            mode=RenaissanceMode.LYDIAN,
            instrument_assignments=instrument_assignments,
            measures=8,
            seed=42
        )

        # Check that each voice has a different role
        voice_roles = []
        for voice_idx, _voice in enumerate(score.voices):
            role = pattern_composer._determine_voice_role(voice_idx)
            voice_roles.append(role)

        # Should have different roles for different voices
        assert len(set(voice_roles)) == len(voice_roles)

    def test_instrument_adaptation(self, pattern_composer, sample_pattern):
        """Test adaptation of patterns for different instruments."""
        instruments = [
            InstrumentType.PROGRAMMABLE_FLUTE,
            InstrumentType.VIOLA_ORGANISTA,
            InstrumentType.MECHANICAL_ORGAN,
            InstrumentType.MECHANICAL_DRUM,
        ]

        for instrument in instruments:
            adapted_pattern = pattern_composer._adapt_pattern_for_instrument(
                sample_pattern, instrument
            )

            assert adapted_pattern is not None
            assert adapted_pattern.pattern_type == sample_pattern.pattern_type

            # Check that notes are within instrument range
            instrument_chars = pattern_composer._get_instrument_characteristics(instrument)
            for note in adapted_pattern.notes:
                if not note.is_rest:
                    assert instrument_chars["range_low"] <= note.pitch <= instrument_chars["range_high"]

    def test_reproducible_composition(self, pattern_composer, instrument_assignments):
        """Test that composition is reproducible with the same seed."""
        score1 = pattern_composer.compose_by_patterns(
            form=MusicalForm.PAVANE,
            mode=RenaissanceMode.LYDIAN,
            instrument_assignments=instrument_assignments,
            measures=8,
            seed=42
        )

        score2 = pattern_composer.compose_by_patterns(
            form=MusicalForm.PAVANE,
            mode=RenaissanceMode.LYDIAN,
            instrument_assignments=instrument_assignments,
            measures=8,
            seed=42
        )

        # Check that scores have the same basic properties
        assert score1.tempo_bpm == score2.tempo_bpm
        assert len(score1.voices) == len(score2.voices)

        # Check that voices have the same number of notes
        for voice1, voice2 in zip(score1.voices, score2.voices):
            assert len(voice1.notes) == len(voice2.notes)

    def test_custom_pattern_library(self, instrument_assignments):
        """Test composition with a custom pattern library."""
        from src.davinci_codex.renaissance_music.patterns import RenaissancePatternLibrary

        custom_library = RenaissancePatternLibrary()
        composer = PatternBasedComposer(pattern_library=custom_library)

        score = composer.compose_by_patterns(
            form=MusicalForm.PAVANE,
            mode=RenaissanceMode.LYDIAN,
            instrument_assignments=instrument_assignments,
            measures=8,
            seed=42
        )

        assert score is not None
        assert score.form == MusicalForm.PAVANE
        assert score.mode == RenaissanceMode.LYDIAN
