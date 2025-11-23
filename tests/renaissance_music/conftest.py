"""Pytest fixtures for Renaissance music tests."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalPattern,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


@pytest.fixture
def sample_notes():
    """Create sample notes for testing."""
    return [
        Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0),
        Note(pitch=493.88, duration=1.0, velocity=0.7, start_time=1.0),
        Note(pitch=523.25, duration=2.0, velocity=0.7, start_time=2.0),
    ]


@pytest.fixture
def sample_voice(sample_notes):
    """Create a sample voice for testing."""
    return Voice(
        name="Test Voice",
        notes=sample_notes,
        instrument=InstrumentType.PROGRAMMABLE_FLUTE
    )


@pytest.fixture
def sample_score(sample_voice):
    """Create a sample musical score for testing."""
    score = MusicalScore(
        title="Test Score",
        composer="Test Composer",
        mode=RenaissanceMode.LYDIAN,
        form=MusicalForm.PAVANE,
        tempo_bpm=100.0
    )
    score.add_voice(sample_voice)
    return score


@pytest.fixture
def sample_pattern(sample_notes):
    """Create a sample musical pattern for testing."""
    return MusicalPattern(
        name="test_pattern",
        pattern_type="dance_figure",
        mode=RenaissanceMode.LYDIAN,
        notes=sample_notes,
        voice_leading=[(440.0, 493.88), (493.88, 523.25)],
        rhythm_profile=[1.0, 1.0, 2.0],
        context_tags=["test"],
        source_reference="Test pattern"
    )


@pytest.fixture
def instrument_assignments():
    """Create instrument assignments for testing."""
    return {
        0: InstrumentType.PROGRAMMABLE_FLUTE,
        1: InstrumentType.VIOLA_ORGANISTA,
        2: InstrumentType.MECHANICAL_ORGAN,
    }


@pytest.fixture
def all_instrument_types():
    """Create a list of all instrument types for testing."""
    return [
        InstrumentType.MECHANICAL_DRUM,
        InstrumentType.MECHANICAL_ORGAN,
        InstrumentType.VIOLA_ORGANISTA,
        InstrumentType.PROGRAMMABLE_FLUTE,
        InstrumentType.MECHANICAL_CARILLON,
        InstrumentType.MECHANICAL_TRUMPETER,
    ]


@pytest.fixture
def all_musical_forms():
    """Create a list of all musical forms for testing."""
    return [
        MusicalForm.BASSE_DANSE,
        MusicalForm.PAVANE,
        MusicalForm.GALLIARD,
        MusicalForm.CHANSON,
        MusicalForm.MADRIGAL,
        MusicalForm.MOTET,
        MusicalForm.ISORHYTHMIC,
        MusicalForm.FANTASIA,
    ]


@pytest.fixture
def all_renaissance_modes():
    """Create a list of all Renaissance modes for testing."""
    return [
        RenaissanceMode.DORIAN,
        RenaissanceMode.PHRYGIAN,
        RenaissanceMode.LYDIAN,
        RenaissanceMode.MIXOLYDIAN,
        RenaissanceMode.HYPODORIAN,
        RenaissanceMode.HYPOPHRYGIAN,
        RenaissanceMode.HYPOLYDIAN,
        RenaissanceMode.HYPOMIXOLYDIAN,
    ]
