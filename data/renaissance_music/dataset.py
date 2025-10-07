"""Dataset of Renaissance music pieces for training and inspiration."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from src.davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


class DatasetCategory(Enum):
    """Categories of Renaissance music in the dataset."""
    DANCE = "dance"
    VOCAL = "vocal"
    SACRED = "sacred"
    INSTRUMENTAL = "instrumental"
    ISORHYTHMIC = "isorhythmic"


@dataclass
class DatasetEntry:
    """Represents a single entry in the Renaissance music dataset."""
    title: str
    composer: str
    year: Optional[int]
    mode: RenaissanceMode
    form: MusicalForm
    category: DatasetCategory
    score: MusicalScore
    metadata: Dict[str, Union[str, int, float, bool]] = field(default_factory=dict)
    source_reference: str = ""
    difficulty_level: int = 1  # 1-5 scale of complexity
    instrumentation: List[InstrumentType] = field(default_factory=list)


class RenaissanceMusicDataset:
    """Dataset of Renaissance music pieces for training and inspiration."""

    def __init__(self, data_path: Optional[Path] = None) -> None:
        """Initialize the dataset.

        Args:
            data_path: Optional path to load data from
        """
        self.data_path = data_path or Path(__file__).parent
        self.entries: List[DatasetEntry] = []

        # Initialize with example pieces if no data path provided
        if not data_path or not data_path.exists():
            self._initialize_example_dataset()
        else:
            self._load_dataset()

    def _initialize_example_dataset(self) -> None:
        """Initialize the dataset with example Renaissance pieces."""
        # Create example basse danse
        basse_danse = self._create_example_basse_danse()
        self.entries.append(basse_danse)

        # Create example pavane
        pavane = self._create_example_pavane()
        self.entries.append(pavane)

        # Create example galliard
        galliard = self._create_example_galliard()
        self.entries.append(galliard)

        # Create example chanson
        chanson = self._create_example_chanson()
        self.entries.append(chanson)

        # Create example motet
        motet = self._create_example_motet()
        self.entries.append(motet)

        # Create example isorhythmic piece
        isorhythmic = self._create_example_isorhythmic()
        self.entries.append(isorhythmic)

    def _create_example_basse_danse(self) -> DatasetEntry:
        """Create an example basse danse."""
        # Create bass voice
        bass_notes = [
            Note(pitch=196.00, duration=2.0, velocity=0.7, start_time=0.0),   # G3
            Note(pitch=220.00, duration=1.0, velocity=0.7, start_time=2.0),   # A3
            Note(pitch=246.94, duration=1.0, velocity=0.7, start_time=3.0),   # B3
            Note(pitch=261.63, duration=2.0, velocity=0.7, start_time=4.0),   # C4
            Note(pitch=293.66, duration=2.0, velocity=0.7, start_time=6.0),   # D4
            Note(pitch=329.63, duration=2.0, velocity=0.7, start_time=8.0),   # E4
            Note(pitch=392.00, duration=2.0, velocity=0.7, start_time=10.0),  # G4
            Note(pitch=261.63, duration=2.0, velocity=0.7, start_time=12.0),  # C4
        ]
        bass_voice = Voice(name="Bass", notes=bass_notes, instrument=InstrumentType.VIOLA_ORGANISTA)

        # Create tenor voice
        tenor_notes = [
            Note(pitch=392.00, duration=1.0, velocity=0.6, start_time=0.0),   # G4
            Note(pitch=440.00, duration=1.0, velocity=0.6, start_time=1.0),   # A4
            Note(pitch=392.00, duration=1.0, velocity=0.6, start_time=2.0),   # G4
            Note(pitch=349.23, duration=1.0, velocity=0.6, start_time=3.0),   # F4
            Note(pitch=392.00, duration=2.0, velocity=0.6, start_time=4.0),   # G4
            Note(pitch=493.88, duration=2.0, velocity=0.6, start_time=6.0),   # B4
            Note(pitch=523.25, duration=2.0, velocity=0.6, start_time=8.0),   # C5
            Note(pitch=392.00, duration=2.0, velocity=0.6, start_time=10.0),  # G4
        ]
        tenor_voice = Voice(name="Tenor", notes=tenor_notes, instrument=InstrumentType.MECHANICAL_ORGAN)

        # Create score
        score = MusicalScore(
            title="La Basse Danse",
            composer="Example Composer",
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.BASSE_DANSE,
            tempo_bpm=70.0
        )
        score.add_voice(bass_voice)
        score.add_voice(tenor_voice)

        return DatasetEntry(
            title="La Basse Danse",
            composer="Example Composer",
            year=1500,
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.BASSE_DANSE,
            category=DatasetCategory.DANCE,
            score=score,
            source_reference="Example based on Arbeau's Orchésographie (1588)",
            difficulty_level=2,
            instrumentation=[InstrumentType.VIOLA_ORGANISTA, InstrumentType.MECHANICAL_ORGAN]
        )

    def _create_example_pavane(self) -> DatasetEntry:
        """Create an example pavane."""
        # Create soprano voice
        soprano_notes = [
            Note(pitch=523.25, duration=1.0, velocity=0.6, start_time=0.0),   # C5
            Note(pitch=587.33, duration=0.5, velocity=0.6, start_time=1.0),   # D5
            Note(pitch=523.25, duration=0.5, velocity=0.6, start_time=1.5),   # C5
            Note(pitch=659.25, duration=1.0, velocity=0.6, start_time=2.0),   # E5
            Note(pitch=698.46, duration=2.0, velocity=0.6, start_time=3.0),   # F5
            Note(pitch=783.99, duration=2.0, velocity=0.6, start_time=5.0),   # G5
            Note(pitch=698.46, duration=2.0, velocity=0.6, start_time=7.0),   # F5
            Note(pitch=659.25, duration=2.0, velocity=0.6, start_time=9.0),   # E5
        ]
        soprano_voice = Voice(name="Soprano", notes=soprano_notes, instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Create alto voice
        alto_notes = [
            Note(pitch=392.00, duration=1.0, velocity=0.5, start_time=0.0),   # G4
            Note(pitch=440.00, duration=0.5, velocity=0.5, start_time=1.0),   # A4
            Note(pitch=392.00, duration=0.5, velocity=0.5, start_time=1.5),   # G4
            Note(pitch=493.88, duration=1.0, velocity=0.5, start_time=2.0),   # B4
            Note(pitch=523.25, duration=2.0, velocity=0.5, start_time=3.0),   # C5
            Note(pitch=587.33, duration=2.0, velocity=0.5, start_time=5.0),   # D5
            Note(pitch=523.25, duration=2.0, velocity=0.5, start_time=7.0),   # C5
            Note(pitch=493.88, duration=2.0, velocity=0.5, start_time=9.0),   # B4
        ]
        alto_voice = Voice(name="Alto", notes=alto_notes, instrument=InstrumentType.VIOLA_ORGANISTA)

        # Create tenor voice
        tenor_notes = [
            Note(pitch=261.63, duration=1.0, velocity=0.5, start_time=0.0),   # C4
            Note(pitch=293.66, duration=0.5, velocity=0.5, start_time=1.0),   # D4
            Note(pitch=261.63, duration=0.5, velocity=0.5, start_time=1.5),   # C4
            Note(pitch=329.63, duration=1.0, velocity=0.5, start_time=2.0),   # E4
            Note(pitch=349.23, duration=2.0, velocity=0.5, start_time=3.0),   # F4
            Note(pitch=392.00, duration=2.0, velocity=0.5, start_time=5.0),   # G4
            Note(pitch=349.23, duration=2.0, velocity=0.5, start_time=7.0),   # F4
            Note(pitch=329.63, duration=2.0, velocity=0.5, start_time=9.0),   # E4
        ]
        tenor_voice = Voice(name="Tenor", notes=tenor_notes, instrument=InstrumentType.MECHANICAL_ORGAN)

        # Create bass voice
        bass_notes = [
            Note(pitch=130.81, duration=1.0, velocity=0.6, start_time=0.0),   # C3
            Note(pitch=146.83, duration=0.5, velocity=0.6, start_time=1.0),   # D3
            Note(pitch=130.81, duration=0.5, velocity=0.6, start_time=1.5),   # C3
            Note(pitch=164.81, duration=1.0, velocity=0.6, start_time=2.0),   # E3
            Note(pitch=174.61, duration=2.0, velocity=0.6, start_time=3.0),   # F3
            Note(pitch=196.00, duration=2.0, velocity=0.6, start_time=5.0),   # G3
            Note(pitch=174.61, duration=2.0, velocity=0.6, start_time=7.0),   # F3
            Note(pitch=164.81, duration=2.0, velocity=0.6, start_time=9.0),   # E3
        ]
        bass_voice = Voice(name="Bass", notes=bass_notes, instrument=InstrumentType.MECHANICAL_CARILLON)

        # Create score
        score = MusicalScore(
            title="Pavane pour une Infante Défunte",
            composer="Example Composer",
            mode=RenaissanceMode.LYDIAN,
            form=MusicalForm.PAVANE,
            tempo_bpm=95.0
        )
        score.add_voice(soprano_voice)
        score.add_voice(alto_voice)
        score.add_voice(tenor_voice)
        score.add_voice(bass_voice)

        return DatasetEntry(
            title="Pavane pour une Infante Défunte",
            composer="Example Composer",
            year=1520,
            mode=RenaissanceMode.LYDIAN,
            form=MusicalForm.PAVANE,
            category=DatasetCategory.DANCE,
            score=score,
            source_reference="Example pavane in the style of early 16th century",
            difficulty_level=3,
            instrumentation=[
                InstrumentType.PROGRAMMABLE_FLUTE,
                InstrumentType.VIOLA_ORGANISTA,
                InstrumentType.MECHANICAL_ORGAN,
                InstrumentType.MECHANICAL_CARILLON
            ]
        )

    def _create_example_galliard(self) -> DatasetEntry:
        """Create an example galliard."""
        # Create melody voice
        melody_notes = [
            Note(pitch=440.00, duration=0.5, velocity=0.7, start_time=0.0),   # A4
            Note(pitch=493.88, duration=0.5, velocity=0.7, start_time=0.5),   # B4
            Note(pitch=523.25, duration=1.0, velocity=0.7, start_time=1.0),   # C5
            Note(pitch=440.00, duration=0.5, velocity=0.7, start_time=2.0),   # A4
            Note(pitch=493.88, duration=0.5, velocity=0.7, start_time=2.5),   # B4
            Note(pitch=523.25, duration=1.0, velocity=0.7, start_time=3.0),   # C5
            Note(pitch=587.33, duration=0.5, velocity=0.7, start_time=4.0),   # D5
            Note(pitch=523.25, duration=0.5, velocity=0.7, start_time=4.5),   # C5
            Note(pitch=493.88, duration=0.5, velocity=0.7, start_time=5.0),   # B4
            Note(pitch=440.00, duration=0.5, velocity=0.7, start_time=5.5),   # A4
            Note(pitch=392.00, duration=1.0, velocity=0.7, start_time=6.0),   # G4
        ]
        melody_voice = Voice(name="Melody", notes=melody_notes, instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Create harmony voice
        harmony_notes = [
            Note(pitch=261.63, duration=0.5, velocity=0.6, start_time=0.0),   # C4
            Note(pitch=293.66, duration=0.5, velocity=0.6, start_time=0.5),   # D4
            Note(pitch=329.63, duration=1.0, velocity=0.6, start_time=1.0),   # E4
            Note(pitch=261.63, duration=0.5, velocity=0.6, start_time=2.0),   # C4
            Note(pitch=293.66, duration=0.5, velocity=0.6, start_time=2.5),   # D4
            Note(pitch=329.63, duration=1.0, velocity=0.6, start_time=3.0),   # E4
            Note(pitch=349.23, duration=0.5, velocity=0.6, start_time=4.0),   # F4
            Note(pitch=329.63, duration=0.5, velocity=0.6, start_time=4.5),   # E4
            Note(pitch=293.66, duration=0.5, velocity=0.6, start_time=5.0),   # D4
            Note(pitch=261.63, duration=0.5, velocity=0.6, start_time=5.5),   # C4
            Note(pitch=246.94, duration=1.0, velocity=0.6, start_time=6.0),   # B3
        ]
        harmony_voice = Voice(name="Harmony", notes=harmony_notes, instrument=InstrumentType.VIOLA_ORGANISTA)

        # Create bass voice
        bass_notes = [
            Note(pitch=130.81, duration=1.0, velocity=0.7, start_time=0.0),   # C3
            Note(pitch=146.83, duration=1.0, velocity=0.7, start_time=1.0),   # D3
            Note(pitch=130.81, duration=1.0, velocity=0.7, start_time=2.0),   # C3
            Note(pitch=146.83, duration=1.0, velocity=0.7, start_time=3.0),   # D3
            Note(pitch=174.61, duration=0.5, velocity=0.7, start_time=4.0),   # F3
            Note(pitch=164.81, duration=0.5, velocity=0.7, start_time=4.5),   # E3
            Note(pitch=146.83, duration=1.0, velocity=0.7, start_time=5.0),   # D3
            Note(pitch=130.81, duration=1.0, velocity=0.7, start_time=6.0),   # C3
        ]
        bass_voice = Voice(name="Bass", notes=bass_notes, instrument=InstrumentType.MECHANICAL_DRUM)

        # Create score
        score = MusicalScore(
            title="Gaillarde joyeuse",
            composer="Example Composer",
            mode=RenaissanceMode.MIXOLYDIAN,
            form=MusicalForm.GALLIARD,
            tempo_bpm=130.0
        )
        score.add_voice(melody_voice)
        score.add_voice(harmony_voice)
        score.add_voice(bass_voice)

        return DatasetEntry(
            title="Gaillarde joyeuse",
            composer="Example Composer",
            year=1510,
            mode=RenaissanceMode.MIXOLYDIAN,
            form=MusicalForm.GALLIARD,
            category=DatasetCategory.DANCE,
            score=score,
            source_reference="Example galliard in the style of early 16th century",
            difficulty_level=3,
            instrumentation=[
                InstrumentType.PROGRAMMABLE_FLUTE,
                InstrumentType.VIOLA_ORGANISTA,
                InstrumentType.MECHANICAL_DRUM
            ]
        )

    def _create_example_chanson(self) -> DatasetEntry:
        """Create an example chanson."""
        # Create soprano voice
        soprano_notes = [
            Note(pitch=523.25, duration=1.0, velocity=0.6, start_time=0.0),   # C5
            Note(pitch=587.33, duration=1.0, velocity=0.6, start_time=1.0),   # D5
            Note(pitch=659.25, duration=1.0, velocity=0.6, start_time=2.0),   # E5
            Note(pitch=698.46, duration=1.0, velocity=0.6, start_time=3.0),   # F5
            Note(pitch=659.25, duration=1.0, velocity=0.6, start_time=4.0),   # E5
            Note(pitch=587.33, duration=1.0, velocity=0.6, start_time=5.0),   # D5
            Note(pitch=523.25, duration=2.0, velocity=0.6, start_time=6.0),   # C5
        ]
        soprano_voice = Voice(name="Soprano", notes=soprano_notes, instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Create alto voice
        alto_notes = [
            Note(pitch=392.00, duration=1.0, velocity=0.5, start_time=0.0),   # G4
            Note(pitch=440.00, duration=1.0, velocity=0.5, start_time=1.0),   # A4
            Note(pitch=493.88, duration=1.0, velocity=0.5, start_time=2.0),   # B4
            Note(pitch=523.25, duration=1.0, velocity=0.5, start_time=3.0),   # C5
            Note(pitch=493.88, duration=1.0, velocity=0.5, start_time=4.0),   # B4
            Note(pitch=440.00, duration=1.0, velocity=0.5, start_time=5.0),   # A4
            Note(pitch=392.00, duration=2.0, velocity=0.5, start_time=6.0),   # G4
        ]
        alto_voice = Voice(name="Alto", notes=alto_notes, instrument=InstrumentType.VIOLA_ORGANISTA)

        # Create tenor voice
        tenor_notes = [
            Note(pitch=261.63, duration=1.0, velocity=0.5, start_time=0.0),   # C4
            Note(pitch=293.66, duration=1.0, velocity=0.5, start_time=1.0),   # D4
            Note(pitch=329.63, duration=1.0, velocity=0.5, start_time=2.0),   # E4
            Note(pitch=349.23, duration=1.0, velocity=0.5, start_time=3.0),   # F4
            Note(pitch=329.63, duration=1.0, velocity=0.5, start_time=4.0),   # E4
            Note(pitch=293.66, duration=1.0, velocity=0.5, start_time=5.0),   # D4
            Note(pitch=261.63, duration=2.0, velocity=0.5, start_time=6.0),   # C4
        ]
        tenor_voice = Voice(name="Tenor", notes=tenor_notes, instrument=InstrumentType.MECHANICAL_ORGAN)

        # Create score
        score = MusicalScore(
            title="Chanson d'Amour",
            composer="Example Composer",
            mode=RenaissanceMode.LYDIAN,
            form=MusicalForm.CHANSON,
            tempo_bpm=100.0
        )
        score.add_voice(soprano_voice)
        score.add_voice(alto_voice)
        score.add_voice(tenor_voice)

        return DatasetEntry(
            title="Chanson d'Amour",
            composer="Example Composer",
            year=1530,
            mode=RenaissanceMode.LYDIAN,
            form=MusicalForm.CHANSON,
            category=DatasetCategory.VOCAL,
            score=score,
            source_reference="Example chanson in the style of early 16th century French composers",
            difficulty_level=2,
            instrumentation=[
                InstrumentType.PROGRAMMABLE_FLUTE,
                InstrumentType.VIOLA_ORGANISTA,
                InstrumentType.MECHANICAL_ORGAN
            ]
        )

    def _create_example_motet(self) -> DatasetEntry:
        """Create an example motet."""
        # Create first voice
        voice1_notes = [
            Note(pitch=392.00, duration=1.0, velocity=0.6, start_time=0.0),   # G4
            Note(pitch=440.00, duration=1.0, velocity=0.6, start_time=1.0),   # A4
            Note(pitch=493.88, duration=1.0, velocity=0.6, start_time=2.0),   # B4
            Note(pitch=523.25, duration=1.0, velocity=0.6, start_time=3.0),   # C5
            Note(pitch=493.88, duration=1.0, velocity=0.6, start_time=4.0),   # B4
            Note(pitch=440.00, duration=1.0, velocity=0.6, start_time=5.0),   # A4
            Note(pitch=392.00, duration=1.0, velocity=0.6, start_time=6.0),   # G4
            Note(pitch=349.23, duration=1.0, velocity=0.6, start_time=7.0),   # F4
        ]
        voice1 = Voice(name="Voice 1", notes=voice1_notes, instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Create second voice
        voice2_notes = [
            Note(pitch=261.63, duration=1.0, velocity=0.5, start_time=0.0),   # C4
            Note(pitch=293.66, duration=1.0, velocity=0.5, start_time=1.0),   # D4
            Note(pitch=329.63, duration=1.0, velocity=0.5, start_time=2.0),   # E4
            Note(pitch=349.23, duration=1.0, velocity=0.5, start_time=3.0),   # F4
            Note(pitch=329.63, duration=1.0, velocity=0.5, start_time=4.0),   # E4
            Note(pitch=293.66, duration=1.0, velocity=0.5, start_time=5.0),   # D4
            Note(pitch=261.63, duration=1.0, velocity=0.5, start_time=6.0),   # C4
            Note(pitch=246.94, duration=1.0, velocity=0.5, start_time=7.0),   # B3
        ]
        voice2 = Voice(name="Voice 2", notes=voice2_notes, instrument=InstrumentType.VIOLA_ORGANISTA)

        # Create third voice
        voice3_notes = [
            Note(pitch=196.00, duration=2.0, velocity=0.6, start_time=0.0),   # G3
            Note(pitch=220.00, duration=2.0, velocity=0.6, start_time=2.0),   # A3
            Note(pitch=246.94, duration=2.0, velocity=0.6, start_time=4.0),   # B3
            Note(pitch=261.63, duration=2.0, velocity=0.6, start_time=6.0),   # C4
        ]
        voice3 = Voice(name="Voice 3", notes=voice3_notes, instrument=InstrumentType.MECHANICAL_ORGAN)

        # Create score
        score = MusicalScore(
            title="Motet de la Vierge",
            composer="Example Composer",
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.MOTET,
            tempo_bpm=80.0
        )
        score.add_voice(voice1)
        score.add_voice(voice2)
        score.add_voice(voice3)

        return DatasetEntry(
            title="Motet de la Vierge",
            composer="Example Composer",
            year=1490,
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.MOTET,
            category=DatasetCategory.SACRED,
            score=score,
            source_reference="Example motet in the style of late 15th century Franco-Flemish composers",
            difficulty_level=4,
            instrumentation=[
                InstrumentType.PROGRAMMABLE_FLUTE,
                InstrumentType.VIOLA_ORGANISTA,
                InstrumentType.MECHANICAL_ORGAN
            ]
        )

    def _create_example_isorhythmic(self) -> DatasetEntry:
        """Create an example isorhythmic piece."""
        # Create talea (rhythmic pattern)
        talea = [1.0, 0.5, 0.5, 1.0, 0.5, 0.5]

        # Create color (melodic pattern)
        color_pitches = [392.00, 440.00, 493.88, 523.25, 493.88, 440.00]

        # Create first voice with isorhythmic pattern
        current_time = 0.0
        voice1_notes = []
        for _i in range(3):  # Repeat three times
            for j, duration in enumerate(talea):
                pitch = color_pitches[j % len(color_pitches)]
                voice1_notes.append(
                    Note(pitch=pitch, duration=duration, velocity=0.6, start_time=current_time)
                )
                current_time += duration

        voice1 = Voice(name="Voice 1", notes=voice1_notes, instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Create second voice with different color but same talea
        color_pitches_2 = [261.63, 293.66, 329.63, 349.23, 329.63, 293.66]
        current_time = 0.0
        voice2_notes = []
        for _i in range(3):  # Repeat three times
            for j, duration in enumerate(talea):
                pitch = color_pitches_2[j % len(color_pitches_2)]
                voice2_notes.append(
                    Note(pitch=pitch, duration=duration, velocity=0.5, start_time=current_time)
                )
                current_time += duration

        voice2 = Voice(name="Voice 2", notes=voice2_notes, instrument=InstrumentType.VIOLA_ORGANISTA)

        # Create third voice with slower talea
        talea_3 = [2.0, 1.0, 1.0, 2.0]
        color_pitches_3 = [196.00, 220.00, 246.94, 261.63]
        current_time = 0.0
        voice3_notes = []
        for _i in range(2):  # Repeat twice
            for j, duration in enumerate(talea_3):
                pitch = color_pitches_3[j % len(color_pitches_3)]
                voice3_notes.append(
                    Note(pitch=pitch, duration=duration, velocity=0.6, start_time=current_time)
                )
                current_time += duration

        voice3 = Voice(name="Voice 3", notes=voice3_notes, instrument=InstrumentType.MECHANICAL_ORGAN)

        # Create score
        score = MusicalScore(
            title="Isorhythmic Motet",
            composer="Example Composer",
            mode=RenaissanceMode.PHRYGIAN,
            form=MusicalForm.ISORHYTHMIC,
            tempo_bpm=70.0
        )
        score.add_voice(voice1)
        score.add_voice(voice2)
        score.add_voice(voice3)

        return DatasetEntry(
            title="Isorhythmic Motet",
            composer="Example Composer",
            year=1420,
            mode=RenaissanceMode.PHRYGIAN,
            form=MusicalForm.ISORHYTHMIC,
            category=DatasetCategory.ISORHYTHMIC,
            score=score,
            source_reference="Example isorhythmic motet in the style of early 15th century composers",
            difficulty_level=5,
            instrumentation=[
                InstrumentType.PROGRAMMABLE_FLUTE,
                InstrumentType.VIOLA_ORGANISTA,
                InstrumentType.MECHANICAL_ORGAN
            ]
        )

    def _load_dataset(self) -> None:
        """Load dataset from file."""
        dataset_file = self.data_path / "renaissance_music_dataset.json"

        if not dataset_file.exists():
            self._initialize_example_dataset()
            return

        try:
            with dataset_file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            for entry_data in data:
                entry = self._deserialize_entry(entry_data)
                self.entries.append(entry)

        except Exception as e:
            print(f"Error loading dataset: {e}")
            self._initialize_example_dataset()

    def _deserialize_entry(self, data: Dict) -> DatasetEntry:
        """Deserialize a dataset entry from JSON data.

        Args:
            data: JSON data

        Returns:
            DatasetEntry
        """
        # This is a simplified deserialization
        # In a full implementation, this would properly reconstruct all objects

        score = MusicalScore(
            title=data.get("title", ""),
            composer=data.get("composer", ""),
            mode=RenaissanceMode(data.get("mode", "dorian")),
            form=MusicalForm(data.get("form", "fantasia")),
            tempo_bpm=data.get("tempo_bpm", 120.0)
        )

        return DatasetEntry(
            title=data.get("title", ""),
            composer=data.get("composer", ""),
            year=data.get("year"),
            mode=RenaissanceMode(data.get("mode", "dorian")),
            form=MusicalForm(data.get("form", "fantasia")),
            category=DatasetCategory(data.get("category", "instrumental")),
            score=score,
            metadata=data.get("metadata", {}),
            source_reference=data.get("source_reference", ""),
            difficulty_level=data.get("difficulty_level", 1),
            instrumentation=[InstrumentType(i) for i in data.get("instrumentation", [])]
        )

    def save_dataset(self) -> None:
        """Save dataset to file."""
        dataset_file = self.data_path / "renaissance_music_dataset.json"

        # Ensure directory exists
        dataset_file.parent.mkdir(parents=True, exist_ok=True)

        # Serialize entries
        data = []
        for entry in self.entries:
            entry_data = {
                "title": entry.title,
                "composer": entry.composer,
                "year": entry.year,
                "mode": entry.mode.value,
                "form": entry.form.value,
                "category": entry.category.value,
                "tempo_bpm": entry.score.tempo_bpm,
                "metadata": entry.metadata,
                "source_reference": entry.source_reference,
                "difficulty_level": entry.difficulty_level,
                "instrumentation": [i.value for i in entry.instrumentation]
            }
            data.append(entry_data)

        # Write to file
        with dataset_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def query_by_mode(self, mode: RenaissanceMode) -> List[DatasetEntry]:
        """Query entries by mode.

        Args:
            mode: The Renaissance mode to filter by

        Returns:
            List of entries in the specified mode
        """
        return [entry for entry in self.entries if entry.mode == mode]

    def query_by_form(self, form: MusicalForm) -> List[DatasetEntry]:
        """Query entries by form.

        Args:
            form: The musical form to filter by

        Returns:
            List of entries in the specified form
        """
        return [entry for entry in self.entries if entry.form == form]

    def query_by_category(self, category: DatasetCategory) -> List[DatasetEntry]:
        """Query entries by category.

        Args:
            category: The category to filter by

        Returns:
            List of entries in the specified category
        """
        return [entry for entry in self.entries if entry.category == category]

    def query_by_instrument(self, instrument: InstrumentType) -> List[DatasetEntry]:
        """Query entries that use a specific instrument.

        Args:
            instrument: The instrument to filter by

        Returns:
            List of entries that use the specified instrument
        """
        return [entry for entry in self.entries if instrument in entry.instrumentation]

    def query_by_difficulty(self, min_level: int, max_level: int = 5) -> List[DatasetEntry]:
        """Query entries by difficulty level.

        Args:
            min_level: Minimum difficulty level
            max_level: Maximum difficulty level

        Returns:
            List of entries within the difficulty range
        """
        return [entry for entry in self.entries
                if min_level <= entry.difficulty_level <= max_level]

    def get_random_entry(self,
                        mode: Optional[RenaissanceMode] = None,
                        form: Optional[MusicalForm] = None,
                        category: Optional[DatasetCategory] = None,
                        difficulty: Optional[Tuple[int, int]] = None) -> DatasetEntry:
        """Get a random entry, optionally filtered by criteria.

        Args:
            mode: Optional mode filter
            form: Optional form filter
            category: Optional category filter
            difficulty: Optional difficulty range filter

        Returns:
            Random entry matching criteria
        """
        import random

        # Start with all entries
        candidates = self.entries

        # Apply filters
        if mode:
            candidates = [e for e in candidates if e.mode == mode]

        if form:
            candidates = [e for e in candidates if e.form == form]

        if category:
            candidates = [e for e in candidates if e.category == category]

        if difficulty:
            min_level, max_level = difficulty
            candidates = [e for e in candidates
                         if min_level <= e.difficulty_level <= max_level]

        # Return random entry
        if not candidates:
            raise ValueError("No entries match the specified criteria")

        return random.choice(candidates)

    def get_all_entries(self) -> List[DatasetEntry]:
        """Get all entries in the dataset.

        Returns:
            List of all entries
        """
        return self.entries.copy()

    def add_entry(self, entry: DatasetEntry) -> None:
        """Add an entry to the dataset.

        Args:
            entry: The entry to add
        """
        self.entries.append(entry)

    def get_statistics(self) -> Dict[str, Union[int, Dict[str, int]]]:
        """Get statistics about the dataset.

        Returns:
            Dictionary with dataset statistics
        """
        stats = {
            "total_entries": len(self.entries),
            "modes": {},
            "forms": {},
            "categories": {},
            "difficulty_levels": {},
        }

        for entry in self.entries:
            # Count modes
            mode_name = entry.mode.value
            stats["modes"][mode_name] = stats["modes"].get(mode_name, 0) + 1

            # Count forms
            form_name = entry.form.value
            stats["forms"][form_name] = stats["forms"].get(form_name, 0) + 1

            # Count categories
            category_name = entry.category.value
            stats["categories"][category_name] = stats["categories"].get(category_name, 0) + 1

            # Count difficulty levels
            level = entry.difficulty_level
            stats["difficulty_levels"][str(level)] = stats["difficulty_levels"].get(str(level), 0) + 1

        return stats
