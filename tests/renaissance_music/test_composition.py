"""Tests for the Renaissance music composition module."""

import pytest

from src.davinci_codex.renaissance_music.composition import RenaissanceCompositionGenerator
from src.davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    RenaissanceMode,
)


@pytest.fixture
def composition_generator():
    """Create a composition generator for testing."""
    return RenaissanceCompositionGenerator()


@pytest.fixture
def instrument_assignments():
    """Create instrument assignments for testing."""
    return {
        0: InstrumentType.PROGRAMMABLE_FLUTE,
        1: InstrumentType.VIOLA_ORGANISTA,
        2: InstrumentType.MECHANICAL_ORGAN,
    }


class TestRenaissanceCompositionGenerator:
    """Test the RenaissanceCompositionGenerator class."""

    def test_initialization(self, composition_generator):
        """Test that the composition generator initializes correctly."""
        assert composition_generator is not None
        assert composition_generator.pattern_library is not None
        assert len(composition_generator._mode_pitches) == 8
        assert len(composition_generator._form_characteristics) == 8

    def test_generate_pavane(self, composition_generator, instrument_assignments):
        """Test generation of a pavane."""
        score = composition_generator.generate_composition(
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

    def test_generate_galliard(self, composition_generator, instrument_assignments):
        """Test generation of a galliard."""
        score = composition_generator.generate_composition(
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

    def test_generate_basse_danse(self, composition_generator, instrument_assignments):
        """Test generation of a basse danse."""
        score = composition_generator.generate_composition(
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

    def test_generate_chanson(self, composition_generator, instrument_assignments):
        """Test generation of a chanson."""
        score = composition_generator.generate_composition(
            form=MusicalForm.CHANSON,
            mode=RenaissanceMode.PHRYGIAN,
            instrument_assignments=instrument_assignments,
            measures=16,
            seed=789
        )

        assert score is not None
        assert score.form == MusicalForm.CHANSON
        assert score.mode == RenaissanceMode.PHRYGIAN
        assert len(score.voices) == len(instrument_assignments)
        assert 90 <= score.tempo_bpm <= 120  # Chanson tempo range

    def test_voice_characteristics(self, composition_generator, instrument_assignments):
        """Test that generated voices have appropriate characteristics."""
        score = composition_generator.generate_composition(
            form=MusicalForm.PAVANE,
            mode=RenaissanceMode.LYDIAN,
            instrument_assignments=instrument_assignments,
            measures=8,
            seed=42
        )

        for voice_idx, voice in enumerate(score.voices):
            instrument = instrument_assignments[voice_idx]

            # Check that voice has notes
            assert len(voice.notes) > 0

            # Check that notes are within instrument range
            instrument_chars = composition_generator._get_instrument_characteristics(instrument)
            for note in voice.notes:
                if not note.is_rest:
                    assert instrument_chars["range_low"] <= note.pitch <= instrument_chars["range_high"]

    def test_different_modes(self, composition_generator, instrument_assignments):
        """Test generation with different modes."""
        modes = [
            RenaissanceMode.DORIAN,
            RenaissanceMode.PHRYGIAN,
            RenaissanceMode.LYDIAN,
            RenaissanceMode.MIXOLYDIAN,
        ]

        for mode in modes:
            score = composition_generator.generate_composition(
                form=MusicalForm.FANTASIA,
                mode=mode,
                instrument_assignments=instrument_assignments,
                measures=8,
                seed=42
            )

            assert score is not None
            assert score.mode == mode

    def test_different_forms(self, composition_generator, instrument_assignments):
        """Test generation with different forms."""
        forms = [
            MusicalForm.PAVANE,
            MusicalForm.GALLIARD,
            MusicalForm.BASSE_DANSE,
            MusicalForm.CHANSON,
        ]

        for form in forms:
            score = composition_generator.generate_composition(
                form=form,
                mode=RenaissanceMode.LYDIAN,
                instrument_assignments=instrument_assignments,
                measures=8,
                seed=42
            )

            assert score is not None
            assert score.form == form

    def test_reproducible_generation(self, composition_generator, instrument_assignments):
        """Test that generation is reproducible with the same seed."""
        score1 = composition_generator.generate_composition(
            form=MusicalForm.PAVANE,
            mode=RenaissanceMode.LYDIAN,
            instrument_assignments=instrument_assignments,
            measures=8,
            seed=42
        )

        score2 = composition_generator.generate_composition(
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
        """Test generation with a custom pattern library."""
        from src.davinci_codex.renaissance_music.patterns import RenaissancePatternLibrary

        custom_library = RenaissancePatternLibrary()
        generator = RenaissanceCompositionGenerator(pattern_library=custom_library)

        score = generator.generate_composition(
            form=MusicalForm.PAVANE,
            mode=RenaissanceMode.LYDIAN,
            instrument_assignments=instrument_assignments,
            measures=8,
            seed=42
        )

        assert score is not None
        assert score.form == MusicalForm.PAVANE
        assert score.mode == RenaissanceMode.LYDIAN
