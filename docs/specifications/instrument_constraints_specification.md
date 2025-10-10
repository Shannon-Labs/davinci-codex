# Instrument Constraints and Capabilities Data Structures

## Overview

This document defines the detailed data structures for representing the constraints and capabilities of Leonardo's mechanical instruments. These structures form the foundation for the adaptation system, ensuring that music is properly adapted to match what each instrument can physically perform.

## Core Data Structures

### 1. InstrumentConstraints

```python
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Union
from enum import Enum
import numpy as np

class InstrumentRole(Enum):
    """Musical roles an instrument can effectively perform"""
    MELODY = "melody"
    HARMONY = "harmony"
    BASS = "bass"
    RHYTHM = "rhythm"
    ACCOMPANIMENT = "accompaniment"
    ORNAMENTATION = "ornamentation"

class PitchConstraintType(Enum):
    """Types of pitch constraints"""
    FIXED_PITCHES = "fixed_pitches"  # Can only play specific pitches
    CONTINUOUS_RANGE = "continuous_range"  # Can play any pitch in range
    DIATONIC_ONLY = "diatonic_only"  # Can only play diatonic pitches
    PENTATONIC_ONLY = "pentatonic_only"  # Can only play pentatonic scales

@dataclass
class InstrumentConstraints:
    """Comprehensive constraints and capabilities for a mechanical instrument"""
    
    # Basic identification
    slug: str  # Unique identifier matching existing code
    name: str  # Human-readable name
    category: str  # "percussion", "wind", "string", "keyboard"
    
    # Pitch capabilities
    pitch_constraint_type: PitchConstraintType
    pitch_range: Tuple[int, int]  # (min_midi, max_midi)
    fixed_pitches: List[int]  # For FIXED_PITCHES type
    preferred_ranges: List[Tuple[int, int]]  # Optimal ranges within overall range
    
    # Polyphony and voice management
    max_simultaneous_notes: int  # Maximum polyphony
    min_note_duration: float  # Shortest sustainable note (seconds)
    max_note_duration: float  # Longest sustainable note (seconds)
    note_transition_time: float  # Minimum time between notes (seconds)
    
    # Dynamic capabilities
    velocity_range: Tuple[int, int]  # (min_velocity, max_velocity)
    dynamic_response: str  # "linear", "exponential", "limited"
    attack_time: float  # Time to reach full volume (seconds)
    decay_time: float  # Time for sound to decay (seconds)
    
    # Timing and rhythm
    tempo_range: Tuple[float, float]  # (min_bpm, max_bpm)
    rhythm_precision: float  # Timing accuracy (0-1, higher is better)
    suitable_rhythms: List[str]  # "simple", "complex", "syncopated", "ornamented"
    
    # Musical roles
    suitable_roles: List[InstrumentRole]
    preferred_role: InstrumentRole
    voice_range: Tuple[int, int]  # (min_voice, max_voice) in ensemble context
    
    # Mechanical characteristics
    noise_characteristics: Dict[str, float]  # Various noise factors
    power_requirements: Dict[str, float]  # Power consumption metrics
    mechanical_delay: float  # Inherent mechanical delay (seconds)
    
    # Historical/musical context
    historical_period: str  # "Renaissance"
    musical_context: List[str]  # "court", "sacred", "dance", "outdoor"
    typical_ensemble_size: Tuple[int, int]  # (min_players, max_players)
    
    # Adaptation preferences
    transposition_preference: List[int]  # Preferred transpositions in semitones
    ornamentation_capability: float  # 0-1, ability to add ornaments
    improvisation_capability: float  # 0-1, ability to improvise
```

### 2. InstrumentProfile

```python
@dataclass
class InstrumentProfile:
    """Extended profile including acoustic and performance characteristics"""
    
    constraints: InstrumentConstraints
    
    # Acoustic properties
    fundamental_frequency: float  # Hz
    harmonic_series: List[float]  # Harmonic frequencies
    spectral_centroid: float  # Brightness indicator
    spectral_bandwidth: float  # Frequency spread
    
    # Timbral characteristics
    timbre_class: str  # "bright", "warm", "nasal", "hollow", "metallic"
    articulation_types: List[str]  # "staccato", "legato", "pizzicato", etc.
    special_effects: List[str]  # "tremolo", "trill", "vibrato", etc.
    
    # Performance characteristics
    technical_difficulty: float  # 0-1, relative difficulty to play
    maintenance_requirement: float  # 0-1, maintenance intensity
    reliability_factor: float  # 0-1, mechanical reliability
    
    # Ensemble interaction
    blend_factor: float  # 0-1, how well it blends with others
    presence_factor: float  # 0-1, how much it stands out
    masking_threshold: float  # 0-1, resistance to being masked
```

### 3. EnsembleConfiguration

```python
@dataclass
class EnsembleConfiguration:
    """Configuration for the complete mechanical ensemble"""
    
    # Instrument collection
    instruments: Dict[str, InstrumentProfile]  # slug -> profile mapping
    
    # Ensemble constraints
    max_total_voices: int  # Maximum polyphony across all instruments
    tempo_sync_tolerance: float  # Allowed tempo variation between instruments
    power_budget: float  # Total available power
    
    # Spatial arrangement
    layout_type: str  # "linear", "circular", "scattered", "theatrical"
    instrument_positions: Dict[str, Tuple[float, float, float]]  # 3D positions
    
    # Performance context
    performance_space: str  # "chamber", "court", "outdoor", "processional"
    audience_size: Tuple[int, int]  # (min_audience, max_audience)
    acoustic_environment: str  # "reverberant", "dry", "outdoor", "intimate"
```

## Specific Instrument Constraint Definitions

### Mechanical Drum

```python
mechanical_drum_constraints = InstrumentConstraints(
    slug="mechanical_drum",
    name="Mechanical Drum",
    category="percussion",
    
    pitch_constraint_type=PitchConstraintType.FIXED_PITCHES,
    pitch_range=(36, 36),  # Single pitch (C2)
    fixed_pitches=[36],  # Only C2
    preferred_ranges=[(36, 36)],
    
    max_simultaneous_notes=1,
    min_note_duration=0.1,
    max_note_duration=2.0,
    note_transition_time=0.05,
    
    velocity_range=(60, 127),
    dynamic_response="limited",
    attack_time=0.01,
    decay_time=0.5,
    
    tempo_range=(40, 120),
    rhythm_precision=0.8,
    suitable_rhythms=["simple", "repetitive"],
    
    suitable_roles=[InstrumentRole.RHYTHM],
    preferred_role=InstrumentRole.RHYTHM,
    voice_range=(4, 4),
    
    noise_characteristics={
        "timing_jitter": 0.02,
        "pitch_variation": 0.0,
        "velocity_variation": 0.1
    },
    power_requirements={
        "steady_state": 5.0,
        "peak": 15.0
    },
    mechanical_delay=0.01,
    
    historical_period="Renaissance",
    musical_context=["dance", "outdoor", "processional"],
    typical_ensemble_size=(1, 3),
    
    transposition_preference=[0],
    ornamentation_capability=0.2,
    improvisation_capability=0.1
)
```

### Mechanical Organ

```python
mechanical_organ_constraints = InstrumentConstraints(
    slug="mechanical_organ",
    name="Automatic Pipe Organ",
    category="wind",
    
    pitch_constraint_type=PitchConstraintType.DIATONIC_ONLY,
    pitch_range=(48, 72),  # C3 to C5
    fixed_pitches=[],
    preferred_ranges=[(48, 60), (60, 72)],  # Lower and upper registers
    
    max_simultaneous_notes=3,
    min_note_duration=0.5,
    max_note_duration=8.0,
    note_transition_time=0.2,
    
    velocity_range=(50, 100),
    dynamic_response="limited",
    attack_time=0.1,
    decay_time=2.0,
    
    tempo_range=(40, 100),
    rhythm_precision=0.6,
    suitable_rhythms=["simple", "sustained"],
    
    suitable_roles=[InstrumentRole.HARMONY, InstrumentRole.ACCOMPANIMENT],
    preferred_role=InstrumentRole.HARMONY,
    voice_range=(2, 3),
    
    noise_characteristics={
        "timing_jitter": 0.05,
        "pitch_variation": 0.01,
        "velocity_variation": 0.15
    },
    power_requirements={
        "steady_state": 20.0,
        "peak": 50.0
    },
    mechanical_delay=0.1,
    
    historical_period="Renaissance",
    musical_context=["sacred", "court", "indoor"],
    typical_ensemble_size=(1, 2),
    
    transposition_preference=[0, -5, 5],
    ornamentation_capability=0.3,
    improvisation_capability=0.2
)
```

### Mechanical Trumpeter

```python
mechanical_trumpeter_constraints = InstrumentConstraints(
    slug="mechanical_trumpeter",
    name="Mechanical Trumpeter",
    category="wind",
    
    pitch_constraint_type=PitchConstraintType.CONTINUOUS_RANGE,
    pitch_range=(52, 72),  # E3 to C5
    fixed_pitches=[],
    preferred_ranges=[(55, 70)],  # Most stable range
    
    max_simultaneous_notes=1,
    min_note_duration=0.2,
    max_note_duration=4.0,
    note_transition_time=0.15,
    
    velocity_range=(70, 120),
    dynamic_response="exponential",
    attack_time=0.05,
    decay_time=1.0,
    
    tempo_range=(50, 110),
    rhythm_precision=0.7,
    suitable_rhythms=["simple", "military", "fanfare"],
    
    suitable_roles=[InstrumentRole.MELODY, InstrumentRole.ORNAMENTATION],
    preferred_role=InstrumentRole.MELODY,
    voice_range=(1, 1),
    
    noise_characteristics={
        "timing_jitter": 0.03,
        "pitch_variation": 0.02,
        "velocity_variation": 0.2
    },
    power_requirements={
        "steady_state": 15.0,
        "peak": 35.0
    },
    mechanical_delay=0.08,
    
    historical_period="Renaissance",
    musical_context=["court", "military", "outdoor"],
    typical_ensemble_size=(1, 2),
    
    transposition_preference=[0, -2, 2],
    ornamentation_capability=0.6,
    improvisation_capability=0.4
)
```

### Viola Organista

```python
viola_organista_constraints = InstrumentConstraints(
    slug="viola_organista",
    name="Viola Organista",
    category="string",
    
    pitch_constraint_type=PitchConstraintType.CONTINUOUS_RANGE,
    pitch_range=(48, 84),  # C3 to C6
    fixed_pitches=[],
    preferred_ranges=[(55, 75)],  # Most expressive range
    
    max_simultaneous_notes=2,
    min_note_duration=0.3,
    max_note_duration=6.0,
    note_transition_time=0.1,
    
    velocity_range=(40, 100),
    dynamic_response="linear",
    attack_time=0.15,
    decay_time=3.0,
    
    tempo_range=(40, 90),
    rhythm_precision=0.8,
    suitable_rhythms=["simple", "sustained", "ornamented"],
    
    suitable_roles=[InstrumentRole.MELODY, InstrumentRole.HARMONY],
    preferred_role=InstrumentRole.MELODY,
    voice_range=(1, 2),
    
    noise_characteristics={
        "timing_jitter": 0.02,
        "pitch_variation": 0.01,
        "velocity_variation": 0.1
    },
    power_requirements={
        "steady_state": 25.0,
        "peak": 40.0
    },
    mechanical_delay=0.05,
    
    historical_period="Renaissance",
    musical_context=["court", "chamber", "indoor"],
    typical_ensemble_size=(1, 2),
    
    transposition_preference=[0, -3, 3],
    ornamentation_capability=0.8,
    improvisation_capability=0.6
)
```

### Mechanical Carillon

```python
mechanical_carillon_constraints = InstrumentConstraints(
    slug="mechanical_carillon",
    name="Mechanical Carillon",
    category="percussion",
    
    pitch_constraint_type=PitchConstraintType.FIXED_PITCHES,
    pitch_range=(48, 72),  # C3 to C5
    fixed_pitches=[48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72],
    preferred_ranges=[(55, 70)],  # Central bells
    
    max_simultaneous_notes=2,
    min_note_duration=0.5,
    max_note_duration=5.0,
    note_transition_time=0.2,
    
    velocity_range=(60, 110),
    dynamic_response="limited",
    attack_time=0.02,
    decay_time=4.0,
    
    tempo_range=(30, 80),
    rhythm_precision=0.9,
    suitable_rhythms=["simple", "chordal", "sustained"],
    
    suitable_roles=[InstrumentRole.HARMONY, InstrumentRole.RHYTHM],
    preferred_role=InstrumentRole.HARMONY,
    voice_range=(2, 3),
    
    noise_characteristics={
        "timing_jitter": 0.01,
        "pitch_variation": 0.0,
        "velocity_variation": 0.05
    },
    power_requirements={
        "steady_state": 30.0,
        "peak": 60.0
    },
    mechanical_delay=0.02,
    
    historical_period="Renaissance",
    musical_context=["outdoor", "civic", "ceremonial"],
    typical_ensemble_size=(1, 1),
    
    transposition_preference=[0],
    ornamentation_capability=0.2,
    improvisation_capability=0.1
)
```

### Programmable Flute

```python
programmable_flute_constraints = InstrumentConstraints(
    slug="programmable_flute",
    name="Programmable Flute",
    category="wind",
    
    pitch_constraint_type=PitchConstraintType.DIATONIC_ONLY,
    pitch_range=(60, 84),  # C4 to C6
    fixed_pitches=[],
    preferred_ranges=[(65, 80)],  # Most stable range
    
    max_simultaneous_notes=1,
    min_note_duration=0.2,
    max_note_duration=3.0,
    note_transition_time=0.1,
    
    velocity_range=(50, 100),
    dynamic_response="exponential",
    attack_time=0.05,
    decay_time=0.8,
    
    tempo_range=(50, 120),
    rhythm_precision=0.7,
    suitable_rhythms=["simple", "ornamented", "dance"],
    
    suitable_roles=[InstrumentRole.MELODY, InstrumentRole.ORNAMENTATION],
    preferred_role=InstrumentRole.MELODY,
    voice_range=(1, 1),
    
    noise_characteristics={
        "timing_jitter": 0.03,
        "pitch_variation": 0.02,
        "velocity_variation": 0.15
    },
    power_requirements={
        "steady_state": 10.0,
        "peak": 25.0
    },
    mechanical_delay=0.05,
    
    historical_period="Renaissance",
    musical_context=["court", "chamber", "dance"],
    typical_ensemble_size=(1, 3),
    
    transposition_preference=[0, -2, 2],
    ornamentation_capability=0.9,
    improvisation_capability=0.7
)
```

## Constraint Validation Functions

```python
def validate_pitch_range(constraints: InstrumentConstraints, pitch: int) -> bool:
    """Validate if a pitch is within instrument constraints"""
    if constraints.pitch_constraint_type == PitchConstraintType.FIXED_PITCHES:
        return pitch in constraints.fixed_pitches
    else:
        return constraints.pitch_range[0] <= pitch <= constraints.pitch_range[1]

def validate_duration(constraints: InstrumentConstraints, duration: float) -> bool:
    """Validate if a duration is within instrument capabilities"""
    return (constraints.min_note_duration <= duration <= constraints.max_note_duration)

def validate_voice_count(constraints: InstrumentConstraints, voice_count: int) -> bool:
    """Validate if voice count is within instrument limits"""
    return voice_count <= constraints.max_simultaneous_notes

def validate_tempo(constraints: InstrumentConstraints, tempo: float) -> bool:
    """Validate if tempo is suitable for instrument"""
    return constraints.tempo_range[0] <= tempo <= constraints.tempo_range[1]

def calculate_ensemble_constraints(ensemble: EnsembleConfiguration) -> Dict[str, float]:
    """Calculate overall ensemble constraints"""
    return {
        "max_total_voices": ensemble.max_total_voices,
        "min_tempo": min(inst.constraints.tempo_range[0] for inst in ensemble.instruments.values()),
        "max_tempo": max(inst.constraints.tempo_range[1] for inst in ensemble.instruments.values()),
        "total_power_requirement": sum(inst.constraints.power_requirements["steady_state"] 
                                     for inst in ensemble.instruments.values())
    }
```

## Usage Examples

```python
# Create instrument profiles
drum_profile = InstrumentProfile(constraints=mechanical_drum_constraints, ...)
organ_profile = InstrumentProfile(constraints=mechanical_organ_constraints, ...)

# Configure ensemble
ensemble_config = EnsembleConfiguration(
    instruments={
        "mechanical_drum": drum_profile,
        "mechanical_organ": organ_profile,
        # ... other instruments
    },
    max_total_voices=6,
    tempo_sync_tolerance=0.1,
    power_budget=200.0,
    layout_type="circular",
    performance_space="court"
)

# Validate music against constraints
def validate_music_for_instrument(notes: List[MusicalNote], 
                                 constraints: InstrumentConstraints) -> List[str]:
    """Validate a musical passage against instrument constraints"""
    violations = []
    
    for note in notes:
        if not validate_pitch_range(constraints, note.pitch):
            violations.append(f"Pitch {note.pitch} out of range")
        
        if not validate_duration(constraints, note.duration):
            violations.append(f"Duration {note.duration} not playable")
    
    # Check voice count
    voice_count = max(1, len(set(note.voice for note in notes)))
    if not validate_voice_count(constraints, voice_count):
        violations.append(f"Voice count {voice_count} exceeds limit")
    
    return violations
```

These data structures provide a comprehensive foundation for representing the mechanical constraints and capabilities of Leonardo's instruments, enabling the adaptation system to make intelligent decisions about how to modify Renaissance music for mechanical performance.