"""Data models for Renaissance music adaptation system."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

import numpy as np


class RenaissanceMode(Enum):
    """The eight church modes used in Renaissance music."""
    DORIAN = "dorian"
    PHRYGIAN = "phrygian"
    LYDIAN = "lydian"
    MIXOLYDIAN = "mixolydian"
    HYPODORIAN = "hypodorian"
    HYPOPHRYGIAN = "hypophrygian"
    HYPOLYDIAN = "hypolydian"
    HYPOMIXOLYDIAN = "hypomixolydian"


class Mensuration(Enum):
    """Rhythmic modes (mensurations) in Renaissance music."""
    PERFECT_TEMPUS = "perfect_tempus"  # 3/4
    IMPERFECT_TEMPUS = "imperfect_tempus"  # 2/4
    PERFECT_PROLATION = "perfect_prolation"  # 3/2
    IMPERFECT_PROLATION = "imperfect_prolation"  # 2/2


class MusicalForm(Enum):
    """Common Renaissance musical forms."""
    BASSE_DANSE = "basse_danse"
    PAVANE = "pavane"
    GALLIARD = "galliard"
    CHANSON = "chanson"
    MADRIGAL = "madrigal"
    MOTET = "motet"
    ISORHYTHMIC = "isorhythmic"
    FANTASIA = "fantasia"


class InstrumentType(Enum):
    """Types of mechanical instruments in Leonardo's ensemble."""
    MECHANICAL_DRUM = "mechanical_drum"
    MECHANICAL_ORGAN = "mechanical_organ"
    VIOLA_ORGANISTA = "viola_organista"
    PROGRAMMABLE_FLUTE = "programmable_flute"
    MECHANICAL_CARILLON = "mechanical_carillon"
    MECHANICAL_TRUMPETER = "mechanical_trumpeter"


@dataclass
class Note:
    """Represents a single musical note."""
    pitch: float  # Frequency in Hz
    duration: float  # Duration in seconds
    velocity: float  # Amplitude/velocity (0.0 to 1.0)
    start_time: float  # Start time in seconds
    voice: int = 0  # Voice/part number (0-based)
    is_rest: bool = False  # Whether this is a rest

    def __post_init__(self) -> None:
        """Validate note parameters."""
        if self.pitch < 0:
            raise ValueError("Pitch frequency must be non-negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not 0.0 <= self.velocity <= 1.0:
            raise ValueError("Velocity must be between 0.0 and 1.0")
        if self.start_time < 0:
            raise ValueError("Start time must be non-negative")


@dataclass
class Voice:
    """Represents a single voice or part in a polyphonic composition."""
    notes: List[Note] = field(default_factory=list)
    name: str = ""
    instrument: Optional[InstrumentType] = None
    range_low: float = 110.0  # Lowest pitch in Hz (A2)
    range_high: float = 880.0  # Highest pitch in Hz (A5)

    def add_note(self, note: Note) -> None:
        """Add a note to this voice."""
        self.notes.append(note)

    def get_pitch_range(self) -> Tuple[float, float]:
        """Get the actual pitch range of notes in this voice."""
        if not self.notes or all(note.is_rest for note in self.notes):
            return (0.0, 0.0)

        pitches = [note.pitch for note in self.notes if not note.is_rest]
        if not pitches:
            return (0.0, 0.0)

        return (min(pitches), max(pitches))


@dataclass
class MusicalScore:
    """Represents a complete musical score with multiple voices."""
    title: str = ""
    composer: str = ""
    mode: Optional[RenaissanceMode] = None
    mensuration: Optional[Mensuration] = None
    form: Optional[MusicalForm] = None
    tempo_bpm: float = 120.0
    voices: List[Voice] = field(default_factory=list)
    metadata: Dict[str, Union[str, int, float, bool]] = field(default_factory=dict)

    def add_voice(self, voice: Voice) -> None:
        """Add a voice to the score."""
        self.voices.append(voice)

    def get_duration(self) -> float:
        """Get the total duration of the score in seconds."""
        if not self.voices:
            return 0.0

        max_duration = 0.0
        for voice in self.voices:
            if not voice.notes:
                continue

            voice_end = max(note.start_time + note.duration for note in voice.notes)
            max_duration = max(max_duration, voice_end)

        return max_duration

    def get_voice_count(self) -> int:
        """Get the number of voices in the score."""
        return len(self.voices)

    def get_notes_at_time(self, time: float) -> List[Tuple[int, Note]]:
        """Get all notes sounding at a specific time."""
        sounding_notes = []
        for voice_idx, voice in enumerate(self.voices):
            for note in voice.notes:
                if note.start_time <= time < note.start_time + note.duration:
                    sounding_notes.append((voice_idx, note))
        return sounding_notes


@dataclass
class InstrumentConstraints:
    """Mechanical and musical constraints for an instrument."""
    instrument_type: InstrumentType
    pitch_range: Tuple[float, float]  # Min and max frequencies in Hz
    max_polyphony: int = 1  # Maximum simultaneous notes
    min_note_duration: float = 0.1  # Shortest note duration in seconds
    max_note_duration: float = 10.0  # Longest note duration in seconds
    max_rapid_passages: int = 8  # Maximum notes in rapid succession
    rapid_passage_threshold: float = 0.25  # Time threshold for rapid passages
    mechanical_delay: float = 0.05  # Mechanical response delay in seconds
    can_play_legato: bool = True  # Can play connected notes
    can_play_staccato: bool = True  # Can play detached notes
    preferred_modes: List[RenaissanceMode] = field(default_factory=list)
    suitable_forms: List[MusicalForm] = field(default_factory=list)

    def can_play_pitch(self, pitch: float) -> bool:
        """Check if the instrument can play a given pitch."""
        return self.pitch_range[0] <= pitch <= self.pitch_range[1]

    def can_play_duration(self, duration: float) -> bool:
        """Check if the instrument can sustain a note for given duration."""
        return self.min_note_duration <= duration <= self.max_note_duration

    def calculate_mechanical_feasibility(self, notes: List[Note]) -> float:
        """Calculate mechanical feasibility score (0.0 to 1.0) for a sequence."""
        if not notes:
            return 1.0

        score = 1.0

        # Check pitch constraints
        for note in notes:
            if not self.can_play_pitch(note.pitch):
                score -= 0.2

        # Check duration constraints
        for note in notes:
            if not self.can_play_duration(note.duration):
                score -= 0.1

        # Check rapid passages
        rapid_count = 0
        for i in range(1, len(notes)):
            if notes[i].start_time - notes[i-1].start_time < self.rapid_passage_threshold:
                rapid_count += 1

        if rapid_count > self.max_rapid_passages:
            score -= 0.3

        return max(0.0, score)


@dataclass
class MusicalPattern:
    """Represents a Renaissance musical pattern or motif."""
    name: str
    pattern_type: str  # "cadence", "ornament", "dance_figure", etc.
    mode: RenaissanceMode
    notes: List[Note]
    voice_leading: List[Tuple[float, float]]  # Pitch transitions
    rhythm_profile: List[float]  # Rhythmic values
    context_tags: List[str] = field(default_factory=list)
    source_reference: str = ""

    def get_interval_pattern(self) -> List[float]:
        """Get the interval pattern in semitones."""
        if len(self.notes) < 2:
            return []

        intervals = []
        for i in range(1, len(self.notes)):
            if not self.notes[i].is_rest and not self.notes[i-1].is_rest:
                ratio = self.notes[i].pitch / self.notes[i-1].pitch
                semitones = 12 * np.log2(ratio)
                intervals.append(semitones)

        return intervals

    def get_rhythmic_pattern(self) -> List[float]:
        """Get the rhythmic pattern as duration ratios."""
        if len(self.notes) < 2:
            return []

        base_duration = self.notes[0].duration
        return [note.duration / base_duration for note in self.notes]


@dataclass
class AdaptationResult:
    """Tracks changes made during music adaptation."""
    original_score: MusicalScore
    adapted_score: MusicalScore
    adaptation_log: List[str] = field(default_factory=list)
    constraint_violations: List[str] = field(default_factory=list)
    pattern_substitutions: Dict[str, str] = field(default_factory=dict)
    feasibility_scores: Dict[InstrumentType, float] = field(default_factory=dict)
    adaptation_success: bool = False

    def add_log_entry(self, entry: str) -> None:
        """Add an entry to the adaptation log."""
        self.adaptation_log.append(entry)

    def add_violation(self, violation: str) -> None:
        """Add a constraint violation to the report."""
        self.constraint_violations.append(violation)

    def add_pattern_substitution(self, original: str, replacement: str) -> None:
        """Record a pattern substitution."""
        self.pattern_substitutions[original] = replacement

    def set_feasibility_score(self, instrument: InstrumentType, score: float) -> None:
        """Set the feasibility score for an instrument."""
        self.feasibility_scores[instrument] = score

    def get_overall_feasibility(self) -> float:
        """Get the overall feasibility score across all instruments."""
        if not self.feasibility_scores:
            return 0.0

        return sum(self.feasibility_scores.values()) / len(self.feasibility_scores)
