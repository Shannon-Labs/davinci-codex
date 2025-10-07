"""AI Composition Generator for Renaissance-style music adapted for mechanical instruments."""

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from .models import (
    InstrumentType,
    MusicalForm,
    MusicalPattern,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)
from .patterns import RenaissancePatternLibrary


class RenaissanceCompositionGenerator:
    """Generates Renaissance-style compositions adapted for mechanical instruments."""

    def __init__(self, pattern_library: Optional[RenaissancePatternLibrary] = None) -> None:
        """Initialize the composition generator.

        Args:
            pattern_library: Optional pattern library to use
        """
        self.pattern_library = pattern_library or RenaissancePatternLibrary()

        # Mode characteristics for generation
        self._mode_pitches = {
            RenaissanceMode.DORIAN: [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25],  # D Dorian
            RenaissanceMode.PHRYGIAN: [293.66, 311.13, 349.23, 369.99, 415.30, 440.00, 493.88, 554.37],  # E Phrygian
            RenaissanceMode.LYDIAN: [329.63, 369.99, 415.30, 440.00, 493.88, 554.37, 622.25, 659.25],  # F Lydian
            RenaissanceMode.MIXOLYDIAN: [392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 739.99, 783.99],  # G Mixolydian
            RenaissanceMode.HYPODORIAN: [196.00, 220.00, 246.94, 261.63, 293.66, 329.63, 369.99, 392.00],  # G Hypodorian
            RenaissanceMode.HYPOPHRYGIAN: [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 392.00, 440.00],  # A Hypophrygian
            RenaissanceMode.HYPOLYDIAN: [246.94, 277.18, 311.13, 329.63, 369.99, 415.30, 466.16, 493.88],  # B Hypolydian
            RenaissanceMode.HYPOMIXOLYDIAN: [293.66, 329.63, 369.99, 392.00, 440.00, 493.88, 554.37, 587.33],  # C Hypomixolydian
        }

        # Form characteristics
        self._form_characteristics = {
            MusicalForm.BASSE_DANSE: {
                "tempo_range": (60, 80),
                "typical_length": (32, 64),  # measures
                "meter": "duple",
                "voice_count": (3, 4),
            },
            MusicalForm.PAVANE: {
                "tempo_range": (80, 110),
                "typical_length": (32, 64),
                "meter": "duple",
                "voice_count": (4, 5),
            },
            MusicalForm.GALLIARD: {
                "tempo_range": (120, 140),
                "typical_length": (24, 48),
                "meter": "triple",
                "voice_count": (3, 4),
            },
            MusicalForm.CHANSON: {
                "tempo_range": (90, 120),
                "typical_length": (48, 96),
                "meter": "duple",
                "voice_count": (3, 4),
            },
            MusicalForm.MADRIGAL: {
                "tempo_range": (80, 120),
                "typical_length": (64, 128),
                "meter": "variable",
                "voice_count": (4, 6),
            },
            MusicalForm.MOTET: {
                "tempo_range": (60, 100),
                "typical_length": (64, 128),
                "meter": "variable",
                "voice_count": (3, 5),
            },
            MusicalForm.ISORHYTHMIC: {
                "tempo_range": (60, 90),
                "typical_length": (48, 96),
                "meter": "variable",
                "voice_count": (2, 4),
            },
            MusicalForm.FANTASIA: {
                "tempo_range": (80, 120),
                "typical_length": (64, 128),
                "meter": "variable",
                "voice_count": (3, 5),
            },
        }

        # Voice leading rules for Renaissance polyphony
        self._voice_leading_rules = {
            "max_parallel_interval": 3,  # Thirds
            "preferred_intervals": [3, 6],  # Thirds and sixths
            "avoid_parallel": [5, 8],  # Parallel fifths and octaves
            "max_leap": 12,  # Maximum leap in semitones
        }

    def generate_composition(self,
                           form: MusicalForm,
                           mode: RenaissanceMode,
                           instrument_assignments: Dict[int, InstrumentType],
                           measures: int = 32,
                           seed: Optional[int] = None) -> MusicalScore:
        """Generate a Renaissance-style composition.

        Args:
            form: The musical form to generate
            mode: The Renaissance mode to use
            instrument_assignments: Mapping of voice indices to instrument types
            measures: Number of measures to generate
            seed: Random seed for reproducible generation

        Returns:
            A generated musical score
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Get form characteristics
        form_chars = self._form_characteristics[form]

        # Determine tempo based on form
        min_tempo, max_tempo = form_chars["tempo_range"]
        tempo = random.uniform(min_tempo, max_tempo)

        # Determine voice count based on form and instrument assignments
        min_voices, max_voices = form_chars["voice_count"]
        voice_count = max(min_voices, min(len(instrument_assignments), max_voices))

        # Create score
        score = MusicalScore(
            title=f"Generated {form.value.replace('_', ' ').title()}",
            composer="AI Composition Generator",
            mode=mode,
            form=form,
            tempo_bpm=tempo
        )

        # Generate scale for the mode
        mode_scale = self._generate_mode_scale(mode)

        # Generate harmonic progression
        harmonic_progression = self._generate_harmonic_progression(form, mode, measures)

        # Generate each voice
        for voice_idx in range(voice_count):
            instrument = instrument_assignments.get(voice_idx)
            if not instrument:
                continue

            voice = self._generate_voice(
                voice_idx, instrument, form, mode, mode_scale,
                harmonic_progression, measures, tempo
            )
            score.add_voice(voice)

        return score

    def _generate_mode_scale(self, mode: RenaissanceMode) -> List[float]:
        """Generate a scale for the specified mode.

        Args:
            mode: The Renaissance mode

        Returns:
            List of pitch frequencies for the mode
        """
        return self._mode_pitches.get(mode, self._mode_pitches[RenaissanceMode.DORIAN])

    def _generate_harmonic_progression(self,
                                     form: MusicalForm,
                                     mode: RenaissanceMode,
                                     measures: int) -> List[Tuple[int, List[float]]]:
        """Generate a harmonic progression for the composition.

        Args:
            form: The musical form
            mode: The Renaissance mode
            measures: Number of measures

        Returns:
            List of (measure, chord) tuples
        """
        # Get mode scale
        mode_scale = self._generate_mode_scale(mode)

        # Define chord functions based on mode
        if mode in [RenaissanceMode.DORIAN, RenaissanceMode.HYPODORIAN]:
            # Dorian: i-ii-III-IV-v-vi°-VII-i
            chord_functions = [
                (0, 2, 4),  # i
                (1, 3, 5),  # ii
                (2, 4, 6),  # III
                (3, 5, 0),  # IV
                (4, 6, 1),  # v
                (5, 0, 2),  # vi°
                (6, 1, 3),  # VII
            ]
        elif mode in [RenaissanceMode.PHRYGIAN, RenaissanceMode.HYPOPHRYGIAN]:
            # Phrygian: i-II-III-iv-v°-VI-vii-i
            chord_functions = [
                (0, 2, 4),  # i
                (1, 3, 5),  # II
                (2, 4, 6),  # III
                (3, 5, 0),  # iv
                (4, 6, 1),  # v°
                (5, 0, 2),  # VI
                (6, 1, 3),  # vii
            ]
        elif mode in [RenaissanceMode.LYDIAN, RenaissanceMode.HYPOLYDIAN]:
            # Lydian: I-II-iii-IV-v-vi°-vii°-I
            chord_functions = [
                (0, 2, 4),  # I
                (1, 3, 5),  # II
                (2, 4, 6),  # iii
                (3, 5, 0),  # IV
                (4, 6, 1),  # v
                (5, 0, 2),  # vi°
                (6, 1, 3),  # vii°
            ]
        else:  # Mixolydian modes
            # Mixolydian: I-ii-iii°-IV-v-vi-VII-I
            chord_functions = [
                (0, 2, 4),  # I
                (1, 3, 5),  # ii
                (2, 4, 6),  # iii°
                (3, 5, 0),  # IV
                (4, 6, 1),  # v
                (5, 0, 2),  # vi
                (6, 1, 3),  # VII
            ]

        # Generate progression based on form
        progression = []

        # Standard cadence patterns
        if form in [MusicalForm.BASSE_DANSE, MusicalForm.PAVANE]:
            # Slow dances typically end with authentic cadences
            for measure in range(measures - 4):
                # Use mostly tonic and predominant chords
                chord_idx = random.choice([0, 3, 4, 0, 3, 0])  # i-IV-v-i-IV-i
                chord = [mode_scale[i] for i in chord_functions[chord_idx]]
                progression.append((measure, chord))

            # Add cadence
            progression.extend([
                (measures - 4, [mode_scale[i] for i in chord_functions[4]]),  # v
                (measures - 3, [mode_scale[i] for i in chord_functions[4]]),  # v
                (measures - 2, [mode_scale[i] for i in chord_functions[0]]),  # i
                (measures - 1, [mode_scale[i] for i in chord_functions[0]]),  # i
            ])

        elif form == MusicalForm.GALLIARD:
            # Fast dances with more harmonic rhythm
            for measure in range(measures):
                if measure % 4 == 0:
                    chord_idx = 0  # i
                elif measure % 4 == 1:
                    chord_idx = random.choice([3, 4])  # IV or v
                elif measure % 4 == 2:
                    chord_idx = 0  # i
                else:
                    chord_idx = 4  # v

                chord = [mode_scale[i] for i in chord_functions[chord_idx]]
                progression.append((measure, chord))

        else:
            # Other forms with more varied harmony
            for measure in range(measures):
                if measure == 0 or measure == measures - 1:
                    chord_idx = 0  # Start and end on tonic
                elif measure in [measures // 2, measures // 2 - 1]:
                    chord_idx = 4  # Dominant at midpoint
                else:
                    chord_idx = random.choice([0, 3, 4, 1, 0])  # Common progression

                chord = [mode_scale[i] for i in chord_functions[chord_idx]]
                progression.append((measure, chord))

        return progression

    def _generate_voice(self,
                       voice_idx: int,
                       instrument: InstrumentType,
                       form: MusicalForm,
                       mode: RenaissanceMode,
                       mode_scale: List[float],
                       harmonic_progression: List[Tuple[int, List[float]]],
                       measures: int,
                       tempo: float) -> Voice:
        """Generate a single voice for the composition.

        Args:
            voice_idx: Index of the voice
            instrument: Type of instrument for this voice
            form: Musical form
            mode: Renaissance mode
            mode_scale: Scale pitches for the mode
            harmonic_progression: Harmonic progression
            measures: Number of measures
            tempo: Tempo in BPM

        Returns:
            Generated voice
        """
        # Determine voice characteristics based on instrument
        instrument_chars = self._get_instrument_characteristics(instrument)

        # Create voice
        voice = Voice(
            name=f"Voice {voice_idx + 1} ({instrument.value})",
            instrument=instrument,
            range_low=instrument_chars["range_low"],
            range_high=instrument_chars["range_high"]
        )

        # Determine voice role (soprano, alto, tenor, bass)
        voice_roles = ["soprano", "alto", "tenor", "bass"]
        voice_role = voice_roles[voice_idx % len(voice_roles)]

        # Generate notes based on voice role
        notes = []
        current_time = 0.0
        seconds_per_measure = 60.0 / tempo * 4.0  # Assuming 4/4 time

        for _measure_idx, (_measure_num, chord) in enumerate(harmonic_progression):
            # Generate notes for this measure
            measure_notes = self._generate_measure_notes(
                voice_role, instrument, form, mode, mode_scale,
                chord, current_time, seconds_per_measure, voice_idx
            )
            notes.extend(measure_notes)
            current_time += seconds_per_measure

        voice.notes = notes
        return voice

    def _get_instrument_characteristics(self, instrument: InstrumentType) -> Dict[str, Union[float, List[float]]]:
        """Get characteristics for an instrument type.

        Args:
            instrument: The instrument type

        Returns:
            Dictionary of instrument characteristics
        """
        characteristics = {
            InstrumentType.MECHANICAL_DRUM: {
                "range_low": 80.0,
                "range_high": 400.0,
                "preferred_durations": [0.25, 0.5, 1.0],
                "max_rapid_notes": 8,
                "complexity": "low",
            },
            InstrumentType.MECHANICAL_ORGAN: {
                "range_low": 65.41,
                "range_high": 2093.0,
                "preferred_durations": [0.5, 1.0, 2.0],
                "max_rapid_notes": 12,
                "complexity": "high",
            },
            InstrumentType.VIOLA_ORGANISTA: {
                "range_low": 130.81,
                "range_high": 1046.5,
                "preferred_durations": [0.5, 1.0, 1.5],
                "max_rapid_notes": 10,
                "complexity": "medium",
            },
            InstrumentType.PROGRAMMABLE_FLUTE: {
                "range_low": 261.63,
                "range_high": 1568.0,
                "preferred_durations": [0.25, 0.5, 1.0],
                "max_rapid_notes": 20,
                "complexity": "high",
            },
            InstrumentType.MECHANICAL_CARILLON: {
                "range_low": 196.0,
                "range_high": 3920.0,
                "preferred_durations": [1.0, 2.0],
                "max_rapid_notes": 6,
                "complexity": "low",
            },
            InstrumentType.MECHANICAL_TRUMPETER: {
                "range_low": 164.81,
                "range_high": 987.77,
                "preferred_durations": [0.5, 1.0],
                "max_rapid_notes": 8,
                "complexity": "medium",
            },
        }

        return characteristics.get(instrument, characteristics[InstrumentType.MECHANICAL_ORGAN])

    def _generate_measure_notes(self,
                               voice_role: str,
                               instrument: InstrumentType,
                               form: MusicalForm,
                               mode: RenaissanceMode,
                               mode_scale: List[float],
                               chord: List[float],
                               start_time: float,
                               duration: float,
                               voice_idx: int) -> List[Note]:
        """Generate notes for a single measure.

        Args:
            voice_role: Role of the voice (soprano, alto, tenor, bass)
            instrument: Type of instrument
            form: Musical form
            mode: Renaissance mode
            mode_scale: Scale pitches for the mode
            chord: Chord for this measure
            start_time: Start time of the measure
            duration: Duration of the measure
            voice_idx: Index of the voice

        Returns:
            List of notes for the measure
        """
        notes = []
        instrument_chars = self._get_instrument_characteristics(instrument)

        # Determine rhythmic pattern based on form
        if form == MusicalForm.GALLIARD:
            # Triple meter rhythm
            beat_duration = duration / 3
            rhythmic_pattern = [beat_duration, beat_duration, beat_duration]
        elif form in [MusicalForm.BASSE_DANSE, MusicalForm.PAVANE]:
            # Duple meter with characteristic rhythms
            beat_duration = duration / 4
            rhythmic_pattern = [beat_duration, beat_duration, beat_duration * 2, beat_duration]
        else:
            # Default duple meter
            beat_duration = duration / 4
            rhythmic_pattern = [beat_duration, beat_duration, beat_duration, beat_duration]

        # Select appropriate patterns from the library
        patterns = self.pattern_library.query_patterns_by_instrument(instrument)
        patterns = [p for p in patterns if p.mode == mode]

        # If no suitable patterns, generate based on chord
        if not patterns:
            notes = self._generate_chordal_notes(
                voice_role, instrument, chord, start_time, rhythmic_pattern
            )
        else:
            # Use a pattern from the library
            pattern = random.choice(patterns)
            notes = self._adapt_pattern_to_measure(
                pattern, voice_role, instrument, chord, start_time, duration
            )

        # Adjust notes to fit instrument range
        notes = self._adjust_notes_to_range(notes, instrument_chars["range_low"], instrument_chars["range_high"])

        # Apply voice leading rules
        if voice_idx > 0:
            notes = self._apply_voice_leading(notes, voice_role, chord)

        return notes

    def _generate_chordal_notes(self,
                               voice_role: str,
                               instrument: InstrumentType,
                               chord: List[float],
                               start_time: float,
                               rhythmic_pattern: List[float]) -> List[Note]:
        """Generate notes based on chord tones.

        Args:
            voice_role: Role of the voice
            instrument: Type of instrument
            chord: Chord pitches
            start_time: Start time
            rhythmic_pattern: Rhythmic pattern for the measure

        Returns:
            List of notes
        """
        notes = []
        current_time = start_time

        # Select chord tone based on voice role
        if voice_role == "bass":
            chord_tone = chord[0]  # Root
        elif voice_role == "tenor" or voice_role == "alto":
            chord_tone = chord[1]  # Third
        else:  # soprano
            chord_tone = chord[2]  # Fifth

        # Generate notes with rhythmic pattern
        for i, duration in enumerate(rhythmic_pattern):
            # Add some melodic movement
            if i > 0 and random.random() < 0.3:
                # Move to another chord tone
                chord_tone = random.choice(chord)

            note = Note(
                pitch=chord_tone,
                duration=duration,
                velocity=0.7,
                start_time=current_time,
                voice=0
            )
            notes.append(note)
            current_time += duration

        return notes

    def _adapt_pattern_to_measure(self,
                                 pattern: MusicalPattern,
                                 voice_role: str,
                                 instrument: InstrumentType,
                                 chord: List[float],
                                 start_time: float,
                                 duration: float) -> List[Note]:
        """Adapt a pattern to fit the current measure.

        Args:
            pattern: Pattern to adapt
            voice_role: Role of the voice
            instrument: Type of instrument
            chord: Chord for this measure
            start_time: Start time of the measure
            duration: Duration of the measure

        Returns:
            List of adapted notes
        """
        # Get pattern notes
        pattern_notes = pattern.notes

        # Calculate time scaling factor
        pattern_duration = max(note.start_time + note.duration for note in pattern_notes)
        time_scale = duration / pattern_duration

        # Adapt notes
        adapted_notes = []
        for note in pattern_notes:
            # Scale timing
            adapted_start = start_time + note.start_time * time_scale
            adapted_duration = note.duration * time_scale

            # Adapt pitch to fit chord
            adapted_pitch = self._adapt_pitch_to_chord(note.pitch, chord, voice_role)

            adapted_note = Note(
                pitch=adapted_pitch,
                duration=adapted_duration,
                velocity=note.velocity,
                start_time=adapted_start,
                voice=note.voice,
                is_rest=note.is_rest
            )
            adapted_notes.append(adapted_note)

        return adapted_notes

    def _adapt_pitch_to_chord(self, pitch: float, chord: List[float], voice_role: str) -> float:
        """Adapt a pitch to fit within the chord.

        Args:
            pitch: Original pitch
            chord: Chord pitches
            voice_role: Role of the voice

        Returns:
            Adapted pitch
        """
        # Find closest chord tone
        closest_chord_tone = min(chord, key=lambda x: abs(x - pitch))

        # If the pitch is close to a chord tone, use it
        if abs(pitch - closest_chord_tone) < pitch * 0.05:  # Within 5%
            return closest_chord_tone

        # Otherwise, adjust by octaves to fit
        octave_factor = 1.0
        while pitch * octave_factor < closest_chord_tone * 0.8:
            octave_factor *= 2.0
        while pitch * octave_factor > closest_chord_tone * 1.2:
            octave_factor *= 0.5

        return pitch * octave_factor

    def _adjust_notes_to_range(self, notes: List[Note], range_low: float, range_high: float) -> List[Note]:
        """Adjust notes to fit within instrument range.

        Args:
            notes: List of notes to adjust
            range_low: Lowest pitch
            range_high: Highest pitch

        Returns:
            Adjusted notes
        """
        adjusted_notes = []

        for note in notes:
            if note.is_rest:
                adjusted_notes.append(note)
                continue

            adjusted_pitch = note.pitch

            # Adjust by octaves if needed
            while adjusted_pitch < range_low:
                adjusted_pitch *= 2.0
            while adjusted_pitch > range_high:
                adjusted_pitch *= 0.5

            # If still out of range, clamp to nearest
            if adjusted_pitch < range_low:
                adjusted_pitch = range_low
            elif adjusted_pitch > range_high:
                adjusted_pitch = range_high

            adjusted_note = Note(
                pitch=adjusted_pitch,
                duration=note.duration,
                velocity=note.velocity,
                start_time=note.start_time,
                voice=note.voice,
                is_rest=note.is_rest
            )
            adjusted_notes.append(adjusted_note)

        return adjusted_notes

    def _apply_voice_leading(self, notes: List[Note], voice_role: str, chord: List[float]) -> List[Note]:
        """Apply Renaissance voice leading rules.

        Args:
            notes: List of notes to adjust
            voice_role: Role of the voice
            chord: Current chord

        Returns:
            Adjusted notes with proper voice leading
        """
        if len(notes) < 2:
            return notes

        adjusted_notes = [notes[0]]

        for i in range(1, len(notes)):
            prev_note = adjusted_notes[-1]
            curr_note = notes[i]

            if curr_note.is_rest:
                adjusted_notes.append(curr_note)
                continue

            # Check for large leaps
            semitone_diff = abs(12 * math.log2(curr_note.pitch / prev_note.pitch))

            if semitone_diff > self._voice_leading_rules["max_leap"]:
                # Reduce the leap by moving in steps
                direction = 1 if curr_note.pitch > prev_note.pitch else -1
                step_size = 2 ** (self._voice_leading_rules["max_leap"] / 12)

                # Create intermediate notes
                intermediate_pitch = prev_note.pitch * step_size * direction
                intermediate_note = Note(
                    pitch=intermediate_pitch,
                    duration=curr_note.duration / 2,
                    velocity=curr_note.velocity,
                    start_time=prev_note.start_time + prev_note.duration,
                    voice=curr_note.voice,
                    is_rest=False
                )
                adjusted_notes.append(intermediate_note)

                # Adjust current note timing
                adjusted_curr_note = Note(
                    pitch=curr_note.pitch,
                    duration=curr_note.duration / 2,
                    velocity=curr_note.velocity,
                    start_time=intermediate_note.start_time + intermediate_note.duration,
                    voice=curr_note.voice,
                    is_rest=False
                )
                adjusted_notes.append(adjusted_curr_note)
            else:
                adjusted_notes.append(curr_note)

        return adjusted_notes
