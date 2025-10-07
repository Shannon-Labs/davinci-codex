"""Tests for the Renaissance music dataset module."""

import pytest

from data.renaissance_music.dataset import (
    DatasetCategory,
    DatasetEntry,
    RenaissanceMusicDataset,
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


@pytest.fixture
def sample_entry(sample_score):
    """Create a sample dataset entry for testing."""
    return DatasetEntry(
        title="Test Entry",
        composer="Test Composer",
        year=1500,
        mode=RenaissanceMode.LYDIAN,
        form=MusicalForm.PAVANE,
        category=DatasetCategory.DANCE,
        score=sample_score,
        metadata={"test": True},
        source_reference="Test source",
        difficulty_level=2,
        instrumentation=[InstrumentType.PROGRAMMABLE_FLUTE, InstrumentType.VIOLA_ORGANISTA]
    )


@pytest.fixture
def temp_dataset_dir(tmp_path):
    """Create a temporary directory for dataset testing."""
    dataset_dir = tmp_path / "test_dataset"
    dataset_dir.mkdir()
    return dataset_dir


class TestDatasetEntry:
    """Test the DatasetEntry class."""

    def test_initialization(self, sample_entry):
        """Test that a dataset entry initializes correctly."""
        assert sample_entry.title == "Test Entry"
        assert sample_entry.composer == "Test Composer"
        assert sample_entry.year == 1500
        assert sample_entry.mode == RenaissanceMode.LYDIAN
        assert sample_entry.form == MusicalForm.PAVANE
        assert sample_entry.category == DatasetCategory.DANCE
        assert sample_entry.score is not None
        assert sample_entry.metadata["test"] is True
        assert sample_entry.source_reference == "Test source"
        assert sample_entry.difficulty_level == 2
        assert len(sample_entry.instrumentation) == 2


class TestRenaissanceMusicDataset:
    """Test the RenaissanceMusicDataset class."""

    def test_initialization_with_example_data(self):
        """Test that the dataset initializes with example data."""
        dataset = RenaissanceMusicDataset()

        # Should have example entries
        assert len(dataset.entries) > 0

        # Check that entries have expected properties
        for entry in dataset.entries:
            assert entry.title is not None
            assert entry.composer is not None
            assert entry.mode is not None
            assert entry.form is not None
            assert entry.category is not None
            assert entry.score is not None
            assert 1 <= entry.difficulty_level <= 5

    def test_save_and_load_dataset(self, temp_dataset_dir, sample_entry):
        """Test saving and loading a dataset."""
        # Create dataset with sample entry
        dataset = RenaissanceMusicDataset()
        dataset.entries = [sample_entry]

        # Save dataset
        dataset.data_path = temp_dataset_dir
        dataset.save_dataset()

        # Check that file was created
        dataset_file = temp_dataset_dir / "renaissance_music_dataset.json"
        assert dataset_file.exists()

        # Load dataset
        loaded_dataset = RenaissanceMusicDataset(data_path=temp_dataset_dir)

        # Check that entry was loaded
        assert len(loaded_dataset.entries) == 1
        loaded_entry = loaded_dataset.entries[0]

        # Check that properties match
        assert loaded_entry.title == sample_entry.title
        assert loaded_entry.composer == sample_entry.composer
        assert loaded_entry.mode == sample_entry.mode
        assert loaded_entry.form == sample_entry.form
        assert loaded_entry.category == sample_entry.category
        assert loaded_entry.difficulty_level == sample_entry.difficulty_level

    def test_query_by_mode(self):
        """Test querying entries by mode."""
        dataset = RenaissanceMusicDataset()

        # Query for Dorian mode
        dorian_entries = dataset.query_by_mode(RenaissanceMode.DORIAN)

        # Check that all returned entries are in Dorian mode
        for entry in dorian_entries:
            assert entry.mode == RenaissanceMode.DORIAN

    def test_query_by_form(self):
        """Test querying entries by form."""
        dataset = RenaissanceMusicDataset()

        # Query for Pavane form
        pavane_entries = dataset.query_by_form(MusicalForm.PAVANE)

        # Check that all returned entries are Pavane
        for entry in pavane_entries:
            assert entry.form == MusicalForm.PAVANE

    def test_query_by_category(self):
        """Test querying entries by category."""
        dataset = RenaissanceMusicDataset()

        # Query for Dance category
        dance_entries = dataset.query_by_category(DatasetCategory.DANCE)

        # Check that all returned entries are Dance
        for entry in dance_entries:
            assert entry.category == DatasetCategory.DANCE

    def test_query_by_instrument(self):
        """Test querying entries by instrument."""
        dataset = RenaissanceMusicDataset()

        # Query for Flute instrument
        flute_entries = dataset.query_by_instrument(InstrumentType.PROGRAMMABLE_FLUTE)

        # Check that all returned entries use Flute
        for entry in flute_entries:
            assert InstrumentType.PROGRAMMABLE_FLUTE in entry.instrumentation

    def test_query_by_difficulty(self):
        """Test querying entries by difficulty level."""
        dataset = RenaissanceMusicDataset()

        # Query for difficulty levels 1-2
        easy_entries = dataset.query_by_difficulty(1, 2)

        # Check that all returned entries are within difficulty range
        for entry in easy_entries:
            assert 1 <= entry.difficulty_level <= 2

    def test_get_random_entry(self):
        """Test getting a random entry."""
        dataset = RenaissanceMusicDataset()

        # Get a random entry
        random_entry = dataset.get_random_entry()

        # Check that it's a valid entry
        assert random_entry is not None
        assert random_entry.title is not None
        assert random_entry.composer is not None

        # Get a random entry with filters
        filtered_entry = dataset.get_random_entry(
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.BASSE_DANSE
        )

        # Check that filters were applied
        assert filtered_entry.mode == RenaissanceMode.DORIAN
        assert filtered_entry.form == MusicalForm.BASSE_DANSE

    def test_get_random_entry_no_matches(self):
        """Test getting a random entry with no matching criteria."""
        dataset = RenaissanceMusicDataset()

        # Try to get an entry with impossible criteria
        with pytest.raises(ValueError):
            dataset.get_random_entry(
                mode=RenaissanceMode.DORIAN,
                form=MusicalForm.PAVANE,
                category=DatasetCategory.SACRED,
                difficulty=(5, 5)
            )

    def test_add_entry(self, sample_entry):
        """Test adding an entry to the dataset."""
        dataset = RenaissanceMusicDataset()
        initial_count = len(dataset.entries)

        # Add entry
        dataset.add_entry(sample_entry)

        # Check that entry was added
        assert len(dataset.entries) == initial_count + 1
        assert sample_entry in dataset.entries

    def test_get_statistics(self):
        """Test getting dataset statistics."""
        dataset = RenaissanceMusicDataset()

        # Get statistics
        stats = dataset.get_statistics()

        # Check that statistics are valid
        assert "total_entries" in stats
        assert "modes" in stats
        assert "forms" in stats
        assert "categories" in stats
        assert "difficulty_levels" in stats

        # Check that counts add up
        assert stats["total_entries"] == len(dataset.entries)

        mode_total = sum(stats["modes"].values())
        form_total = sum(stats["forms"].values())
        category_total = sum(stats["categories"].values())
        difficulty_total = sum(stats["difficulty_levels"].values())

        assert mode_total == stats["total_entries"]
        assert form_total == stats["total_entries"]
        assert category_total == stats["total_entries"]
        assert difficulty_total == stats["total_entries"]

    def test_get_all_entries(self):
        """Test getting all entries from the dataset."""
        dataset = RenaissanceMusicDataset()

        # Get all entries
        all_entries = dataset.get_all_entries()

        # Check that all entries are returned
        assert len(all_entries) == len(dataset.entries)

        # Check that modifying the returned list doesn't affect the dataset
        all_entries.clear()
        assert len(dataset.entries) > 0
