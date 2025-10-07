"""Pattern-based composer for Renaissance music adaptation."""

from __future__ import annotations

import math
import random
from copy import deepcopy
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


class PatternBasedComposer:
    """Composes Renaissance music by selecting and combining patterns."""

    def __init__(self, pattern_library: Optional[RenaissancePatternLibrary] = None) -> None:
        """Initialize the pattern-based composer.

        Args:
            pattern_library: Optional pattern library to use
        """
        self.pattern_library = pattern_library or RenaissancePatternLibrary()

        # Pattern transition rules for musical coherence
        self._transition_rules = {
            "cadence_to_dance": ["basse_danse", "pavane", "galliard"],
            "dance_to_cadence": ["cadence"],
            "dance_to_dance": ["basse_danse", "pavane", "galliard"],
            "ornament_to_cadence": ["cadence"],
            "cadence_to_ornament": ["ornament"],
            "isorhythmic_to_isorhythmic": ["isorhythmic"],
            "isorhythmic_to_cadence": ["cadence"],
        }

        # Mode transition probabilities
        self._mode_transitions = {
            # Same mode transitions are most likely
            RenaissanceMode.DORIAN: {
                RenaissanceMode.DORIAN: 0.7,
                RenaissanceMode.PHRYGIAN: 0.1,
                RenaissanceMode.LYDIAN: 0.1,
                RenaissanceMode.MIXOLYDIAN: 0.1,
            },
            RenaissanceMode.PHRYGIAN: {
                RenaissanceMode.PHRYGIAN: 0.7,
                RenaissanceMode.DORIAN: 0.1,
                RenaissanceMode.LYDIAN: 0.1,
                RenaissanceMode.MIXOLYDIAN: 0.1,
            },
            RenaissanceMode.LYDIAN: {
                RenaissanceMode.LYDIAN: 0.7,
                RenaissanceMode.DORIAN: 0.1,
                RenaissanceMode.PHRYGIAN: 0.1,
                RenaissanceMode.MIXOLYDIAN: 0.1,
            },
            RenaissanceMode.MIXOLYDIAN: {
                RenaissanceMode.MIXOLYDIAN: 0.7,
                RenaissanceMode.DORIAN: 0.1,
                RenaissanceMode.PHRYGIAN: 0.1,
                RenaissanceMode.LYDIAN: 0.1,
            },
        }

        # Diminution and ornamentation rules
        self._diminution_rules = {
            "max_divisions": 4,  # Maximum number of divisions
            "min_duration": 0.1,  # Minimum duration for divisions
            "preferred_intervals": [2, 3, 4],  # Preferred intervals for diminution
        }

    def compose_by_patterns(self,
                           form: MusicalForm,
                           mode: RenaissanceMode,
                           instrument_assignments: Dict[int, InstrumentType],
                           measures: int = 32,
                           seed: Optional[int] = None) -> MusicalScore:
        """Compose a Renaissance piece using pattern-based approach.

        Args:
            form: The musical form to compose
            mode: The Renaissance mode to use
            instrument_assignments: Mapping of voice indices to instrument types
            measures: Number of measures to generate
            seed: Random seed for reproducible composition

        Returns:
            A composed musical score
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # Determine tempo based on form
        tempo = self._determine_tempo(form)

        # Create score
        score = MusicalScore(
            title=f"Pattern-based {form.value.replace('_', ' ').title()}",
            composer="Pattern-Based Composer",
            mode=mode,
            form=form,
            tempo_bpm=tempo
        )

        # Generate pattern sequence
        pattern_sequence = self._generate_pattern_sequence(form, mode, measures)

        # Create voices from pattern sequence
        for voice_idx, instrument in instrument_assignments.items():
            voice = self._create_voice_from_patterns(
                voice_idx, instrument, pattern_sequence, mode, tempo
            )
            score.add_voice(voice)

        return score

    def transform_pattern_to_mode(self,
                                 pattern: MusicalPattern,
                                 target_mode: RenaissanceMode,
                                 instrument: Optional[InstrumentType] = None) -> MusicalPattern:
        """Transform a pattern to fit a different mode.

        Args:
            pattern: The pattern to transform
            target_mode: The target mode
            instrument: Optional instrument for adaptation

        Returns:
            Transformed pattern
        """
        # Use the pattern library's built-in adaptation
        transformed_pattern = self.pattern_library.adapt_pattern_to_mode(pattern, target_mode)

        # Further adapt for instrument if specified
        if instrument:
            transformed_pattern = self._adapt_pattern_for_instrument(
                transformed_pattern, instrument
            )

        return transformed_pattern

    def create_variation(self,
                        base_pattern: MusicalPattern,
                        variation_type: str = "diminution",
                        instrument: Optional[InstrumentType] = None) -> MusicalPattern:
        """Create a variation of a pattern.

        Args:
            base_pattern: The base pattern to vary
            variation_type: Type of variation ("diminution", "ornamentation", "rhythmic")
            instrument: Optional instrument for adaptation

        Returns:
            Varied pattern
        """
        if variation_type == "diminution":
            varied_pattern = self._apply_diminution(base_pattern)
        elif variation_type == "ornamentation":
            varied_pattern = self._apply_ornamentation(base_pattern)
        elif variation_type == "rhythmic":
            varied_pattern = self._apply_rhythmic_variation(base_pattern)
        else:
            varied_pattern = deepcopy(base_pattern)

        # Adapt for instrument if specified
        if instrument:
            varied_pattern = self._adapt_pattern_for_instrument(varied_pattern, instrument)

        return varied_pattern

    def ensure_smooth_transitions(self,
                                 patterns: List[MusicalPattern],
                                 mode: RenaissanceMode) -> List[MusicalPattern]:
        """Ensure smooth transitions between patterns.

        Args:
            patterns: List of patterns to connect
            mode: The Renaissance mode

        Returns:
            List of patterns with smooth transitions
        """
        if len(patterns) <= 1:
            return patterns

        smooth_patterns = [patterns[0]]

        for i in range(1, len(patterns)):
            prev_pattern = smooth_patterns[-1]
            curr_pattern = patterns[i]

            # Check if transition is smooth
            if self._is_smooth_transition(prev_pattern, curr_pattern):
                smooth_patterns.append(curr_pattern)
            else:
                # Insert transition pattern
                transition_pattern = self._create_transition_pattern(
                    prev_pattern, curr_pattern, mode
                )
                smooth_patterns.append(transition_pattern)
                smooth_patterns.append(curr_pattern)

        return smooth_patterns

    def _determine_tempo(self, form: MusicalForm) -> float:
        """Determine appropriate tempo for a form.

        Args:
            form: The musical form

        Returns:
            Tempo in BPM
        """
        tempo_ranges = {
            MusicalForm.BASSE_DANSE: (60, 80),
            MusicalForm.PAVANE: (80, 110),
            MusicalForm.GALLIARD: (120, 140),
            MusicalForm.CHANSON: (90, 120),
            MusicalForm.MADRIGAL: (80, 120),
            MusicalForm.MOTET: (60, 100),
            MusicalForm.ISORHYTHMIC: (60, 90),
            MusicalForm.FANTASIA: (80, 120),
        }

        min_tempo, max_tempo = tempo_ranges.get(form, (80, 120))
        return random.uniform(min_tempo, max_tempo)

    def _generate_pattern_sequence(self,
                                  form: MusicalForm,
                                  mode: RenaissanceMode,
                                  measures: int) -> List[Tuple[MusicalPattern, int]]:
        """Generate a sequence of patterns for the composition.

        Args:
            form: The musical form
            mode: The Renaissance mode
            measures: Number of measures

        Returns:
            List of (pattern, measure_count) tuples
        """
        sequence = []
        remaining_measures = measures

        # Get suitable patterns for the form and mode
        form_patterns = self.pattern_library.query_patterns_by_form(form)
        mode_patterns = [p for p in form_patterns if p.mode == mode]

        # If no specific patterns, use general patterns
        if not mode_patterns:
            mode_patterns = self.pattern_library.query_patterns_by_mode(mode)

        # Start with an appropriate pattern
        if form in [MusicalForm.BASSE_DANSE, MusicalForm.PAVANE, MusicalForm.GALLIARD]:
            # Dance forms start with dance patterns
            dance_patterns = [p for p in mode_patterns if "dance" in p.pattern_type]
            if dance_patterns:
                current_pattern = random.choice(dance_patterns)
            else:
                current_pattern = random.choice(mode_patterns)
        else:
            # Other forms start with appropriate patterns
            current_pattern = random.choice(mode_patterns)

        # Generate sequence
        while remaining_measures > 0:
            # Determine how many measures this pattern should occupy
            if form in [MusicalForm.BASSE_DANSE, MusicalForm.PAVANE]:
                pattern_duration = random.choice([4, 8])  # 1-2 measures
            elif form == MusicalForm.GALLIARD:
                pattern_duration = random.choice([2, 4])  # 0.5-1 measure
            else:
                pattern_duration = random.choice([4, 8, 16])  # 1-4 measures

            pattern_duration = min(pattern_duration, remaining_measures)

            sequence.append((current_pattern, pattern_duration))
            remaining_measures -= pattern_duration

            # Select next pattern
            if remaining_measures > 0:
                current_pattern = self._select_next_pattern(
                    current_pattern, mode_patterns, form
                )

        return sequence

    def _select_next_pattern(self,
                           current_pattern: MusicalPattern,
                           available_patterns: List[MusicalPattern],
                           form: MusicalForm) -> MusicalPattern:
        """Select the next pattern based on transition rules.

        Args:
            current_pattern: The current pattern
            available_patterns: List of available patterns
            form: The musical form

        Returns:
            Next pattern
        """
        # Determine valid next pattern types
        current_type = current_pattern.pattern_type

        if current_type in self._transition_rules:
            valid_types = self._transition_rules[current_type]
        else:
            valid_types = ["dance_figure", "cadence", "ornament", "isorhythmic"]

        # Filter available patterns by valid types
        valid_patterns = [p for p in available_patterns if p.pattern_type in valid_types]

        if not valid_patterns:
            # Fallback to any pattern
            valid_patterns = available_patterns

        # For dance forms, ensure we have appropriate cadences at the end
        # This is handled at a higher level in sequence generation

        return random.choice(valid_patterns)

    def _create_voice_from_patterns(self,
                                   voice_idx: int,
                                   instrument: InstrumentType,
                                   pattern_sequence: List[Tuple[MusicalPattern, int]],
                                   mode: RenaissanceMode,
                                   tempo: float) -> Voice:
        """Create a voice from a pattern sequence.

        Args:
            voice_idx: Index of the voice
            instrument: Type of instrument
            pattern_sequence: Sequence of patterns and durations
            mode: The Renaissance mode
            tempo: Tempo in BPM

        Returns:
            Created voice
        """
        voice = Voice(
            name=f"Voice {voice_idx + 1} ({instrument.value})",
            instrument=instrument
        )

        # Get instrument characteristics
        instrument_chars = self._get_instrument_characteristics(instrument)
        voice.range_low = instrument_chars["range_low"]
        voice.range_high = instrument_chars["range_high"]

        # Process each pattern in the sequence
        current_time = 0.0
        seconds_per_measure = 60.0 / tempo * 4.0  # Assuming 4/4 time

        for pattern, measure_count in pattern_sequence:
            # Adapt pattern for instrument
            adapted_pattern = self._adapt_pattern_for_instrument(pattern, instrument)

            # Transform pattern to fit voice role
            voice_role = self._determine_voice_role(voice_idx)
            transformed_pattern = self._transform_pattern_for_voice_role(
                adapted_pattern, voice_role, mode
            )

            # Create notes from pattern
            pattern_duration = measure_count * seconds_per_measure
            pattern_notes = self._create_notes_from_pattern(
                transformed_pattern, current_time, pattern_duration, voice_idx
            )

            voice.notes.extend(pattern_notes)
            current_time += pattern_duration

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

    def _determine_voice_role(self, voice_idx: int) -> str:
        """Determine the role of a voice based on its index.

        Args:
            voice_idx: Index of the voice

        Returns:
            Voice role (soprano, alto, tenor, bass)
        """
        roles = ["soprano", "alto", "tenor", "bass"]
        return roles[voice_idx % len(roles)]

    def _adapt_pattern_for_instrument(self,
                                     pattern: MusicalPattern,
                                     instrument: InstrumentType) -> MusicalPattern:
        """Adapt a pattern for a specific instrument.

        Args:
            pattern: The pattern to adapt
            instrument: The instrument type

        Returns:
            Adapted pattern
        """
        instrument_chars = self._get_instrument_characteristics(instrument)

        # Create adapted notes
        adapted_notes = []
        for note in pattern.notes:
            if note.is_rest:
                adapted_notes.append(note)
                continue

            # Adjust pitch to fit instrument range
            adapted_pitch = self._adjust_pitch_to_range(
                note.pitch, instrument_chars["range_low"], instrument_chars["range_high"]
            )

            # Adjust duration if needed
            adapted_duration = note.duration
            if instrument_chars["complexity"] == "low" and adapted_duration < 0.5:
                adapted_duration = 0.5

            adapted_note = Note(
                pitch=adapted_pitch,
                duration=adapted_duration,
                velocity=note.velocity,
                start_time=note.start_time,
                voice=note.voice,
                is_rest=note.is_rest
            )
            adapted_notes.append(adapted_note)

        # Create adapted pattern
        adapted_pattern = MusicalPattern(
            name=f"{pattern.name}_adapted_for_{instrument.value}",
            pattern_type=pattern.pattern_type,
            mode=pattern.mode,
            notes=adapted_notes,
            voice_leading=[(adapted_notes[i].pitch, adapted_notes[i+1].pitch)
                          for i in range(len(adapted_notes)-1)],
            rhythm_profile=pattern.rhythm_profile,
            context_tags=pattern.context_tags + [f"adapted_for_{instrument.value}"],
            source_reference=f"Adapted from {pattern.source_reference}"
        )

        return adapted_pattern

    def _transform_pattern_for_voice_role(self,
                                        pattern: MusicalPattern,
                                        voice_role: str,
                                        mode: RenaissanceMode) -> MusicalPattern:
        """Transform a pattern to fit a specific voice role.

        Args:
            pattern: The pattern to transform
            voice_role: The voice role (soprano, alto, tenor, bass)
            mode: The Renaissance mode

        Returns:
            Transformed pattern
        """
        # Determine target octave based on voice role
        octave_adjustments = {
            "soprano": 2.0,  # One octave up
            "alto": 1.5,      # Perfect fifth up
            "tenor": 1.0,     # No adjustment
            "bass": 0.5,      # One octave down
        }

        octave_factor = octave_adjustments.get(voice_role, 1.0)

        # Create transformed notes
        transformed_notes = []
        for note in pattern.notes:
            if note.is_rest:
                transformed_notes.append(note)
                continue

            # Adjust pitch for voice role
            transformed_pitch = note.pitch * octave_factor

            transformed_note = Note(
                pitch=transformed_pitch,
                duration=note.duration,
                velocity=note.velocity,
                start_time=note.start_time,
                voice=note.voice,
                is_rest=note.is_rest
            )
            transformed_notes.append(transformed_note)

        # Create transformed pattern
        transformed_pattern = MusicalPattern(
            name=f"{pattern.name}_{voice_role}",
            pattern_type=pattern.pattern_type,
            mode=pattern.mode,
            notes=transformed_notes,
            voice_leading=[(transformed_notes[i].pitch, transformed_notes[i+1].pitch)
                          for i in range(len(transformed_notes)-1)],
            rhythm_profile=pattern.rhythm_profile,
            context_tags=pattern.context_tags + [voice_role],
            source_reference=f"Transformed from {pattern.source_reference}"
        )

        return transformed_pattern

    def _create_notes_from_pattern(self,
                                  pattern: MusicalPattern,
                                  start_time: float,
                                  duration: float,
                                  voice_idx: int) -> List[Note]:
        """Create notes from a pattern, scaled to fit the time duration.

        Args:
            pattern: The pattern to use
            start_time: Start time for the notes
            duration: Total duration for the pattern
            voice_idx: Index of the voice

        Returns:
            List of notes
        """
        if not pattern.notes:
            return []

        # Calculate time scaling
        pattern_end_time = max(note.start_time + note.duration for note in pattern.notes)
        time_scale = duration / pattern_end_time

        # Create scaled notes
        notes = []
        for note in pattern.notes:
            scaled_start = start_time + note.start_time * time_scale
            scaled_duration = note.duration * time_scale

            scaled_note = Note(
                pitch=note.pitch,
                duration=scaled_duration,
                velocity=note.velocity,
                start_time=scaled_start,
                voice=voice_idx,
                is_rest=note.is_rest
            )
            notes.append(scaled_note)

        return notes

    def _adjust_pitch_to_range(self, pitch: float, range_low: float, range_high: float) -> float:
        """Adjust a pitch to fit within a range.

        Args:
            pitch: The original pitch
            range_low: Lowest pitch
            range_high: Highest pitch

        Returns:
            Adjusted pitch
        """
        adjusted_pitch = pitch

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

        return adjusted_pitch

    def _apply_diminution(self, base_pattern: MusicalPattern) -> MusicalPattern:
        """Apply diminution (division of longer notes) to a pattern.

        Args:
            base_pattern: The base pattern to diminish

        Returns:
            Diminished pattern
        """
        diminished_notes = []

        for note in base_pattern.notes:
            if note.is_rest:
                diminished_notes.append(note)
                continue

            # Only diminish notes longer than the minimum
            if note.duration < self._diminution_rules["min_duration"] * 2:
                diminished_notes.append(note)
                continue

            # Determine number of divisions
            max_divisions = min(
                self._diminution_rules["max_divisions"],
                int(note.duration / self._diminution_rules["min_duration"])
            )

            if max_divisions < 2:
                diminished_notes.append(note)
                continue

            # Create divisions
            division_duration = note.duration / max_divisions
            current_time = note.start_time

            for i in range(max_divisions):
                # Create a stepwise motion
                if i == 0:
                    division_pitch = note.pitch
                else:
                    # Move by a preferred interval
                    interval = random.choice(self._diminution_rules["preferred_intervals"])
                    direction = random.choice([-1, 1])
                    semitone_change = interval * direction
                    division_pitch = note.pitch * (2 ** (semitone_change / 12))

                division_note = Note(
                    pitch=division_pitch,
                    duration=division_duration,
                    velocity=note.velocity,
                    start_time=current_time,
                    voice=note.voice,
                    is_rest=False
                )
                diminished_notes.append(division_note)
                current_time += division_duration

        # Create diminished pattern
        diminished_pattern = MusicalPattern(
            name=f"{base_pattern.name}_diminished",
            pattern_type=base_pattern.pattern_type,
            mode=base_pattern.mode,
            notes=diminished_notes,
            voice_leading=[(diminished_notes[i].pitch, diminished_notes[i+1].pitch)
                          for i in range(len(diminished_notes)-1)],
            rhythm_profile=[note.duration for note in diminished_notes],
            context_tags=base_pattern.context_tags + ["diminished"],
            source_reference=f"Diminution of {base_pattern.source_reference}"
        )

        return diminished_pattern

    def _apply_ornamentation(self, base_pattern: MusicalPattern) -> MusicalPattern:
        """Apply ornamentation to a pattern.

        Args:
            base_pattern: The base pattern to ornament

        Returns:
            Ornamented pattern
        """
        ornamented_notes = []

        for note in base_pattern.notes:
            if note.is_rest or note.duration < 0.2:
                ornamented_notes.append(note)
                continue

            # Decide whether to ornament this note
            if random.random() < 0.5:  # 50% chance of ornamentation
                ornamented_notes.append(note)
                continue

            # Choose ornament type
            ornament_type = random.choice(["trill", "turn", "mordent"])

            if ornament_type == "trill":
                ornamented_notes.extend(self._create_trill(note))
            elif ornament_type == "turn":
                ornamented_notes.extend(self._create_turn(note))
            else:  # mordent
                ornamented_notes.extend(self._create_mordent(note))

        # Create ornamented pattern
        ornamented_pattern = MusicalPattern(
            name=f"{base_pattern.name}_ornamented",
            pattern_type=base_pattern.pattern_type,
            mode=base_pattern.mode,
            notes=ornamented_notes,
            voice_leading=[(ornamented_notes[i].pitch, ornamented_notes[i+1].pitch)
                          for i in range(len(ornamented_notes)-1)],
            rhythm_profile=[note.duration for note in ornamented_notes],
            context_tags=base_pattern.context_tags + ["ornamented"],
            source_reference=f"Ornamented version of {base_pattern.source_reference}"
        )

        return ornamented_pattern

    def _apply_rhythmic_variation(self, base_pattern: MusicalPattern) -> MusicalPattern:
        """Apply rhythmic variation to a pattern.

        Args:
            base_pattern: The base pattern to vary rhythmically

        Returns:
            Rhythmically varied pattern
        """
        varied_notes = []

        for note in base_pattern.notes:
            if note.is_rest:
                varied_notes.append(note)
                continue

            # Apply rhythmic variation
            if random.random() < 0.3:  # 30% chance of variation
                # Divide note into shorter values
                if note.duration > 0.4:
                    division_count = random.choice([2, 3, 4])
                    division_duration = note.duration / division_count

                    for i in range(division_count):
                        division_note = Note(
                            pitch=note.pitch,
                            duration=division_duration,
                            velocity=note.velocity,
                            start_time=note.start_time + i * division_duration,
                            voice=note.voice,
                            is_rest=False
                        )
                        varied_notes.append(division_note)
                else:
                    # Double the note duration
                    varied_note = Note(
                        pitch=note.pitch,
                        duration=note.duration * 2,
                        velocity=note.velocity,
                        start_time=note.start_time,
                        voice=note.voice,
                        is_rest=False
                    )
                    varied_notes.append(varied_note)
            else:
                varied_notes.append(note)

        # Create varied pattern
        varied_pattern = MusicalPattern(
            name=f"{base_pattern.name}_rhythmic_variation",
            pattern_type=base_pattern.pattern_type,
            mode=base_pattern.mode,
            notes=varied_notes,
            voice_leading=[(varied_notes[i].pitch, varied_notes[i+1].pitch)
                          for i in range(len(varied_notes)-1)],
            rhythm_profile=[note.duration for note in varied_notes],
            context_tags=base_pattern.context_tags + ["rhythmic_variation"],
            source_reference=f"Rhythmic variation of {base_pattern.source_reference}"
        )

        return varied_pattern

    def _create_trill(self, note: Note) -> List[Note]:
        """Create a trill ornament.

        Args:
            note: The note to trill on

        Returns:
            List of notes forming the trill
        """
        # Trill alternates between the note and the note above
        upper_pitch = note.pitch * (2 ** (2 / 12))  # Major second above

        trill_duration = min(0.1, note.duration / 4)
        trill_count = int(note.duration / (trill_duration * 2))

        trill_notes = []
        current_time = note.start_time

        for _i in range(trill_count):
            # Lower note
            lower_note = Note(
                pitch=note.pitch,
                duration=trill_duration,
                velocity=note.velocity,
                start_time=current_time,
                voice=note.voice,
                is_rest=False
            )
            trill_notes.append(lower_note)
            current_time += trill_duration

            # Upper note
            upper_note = Note(
                pitch=upper_pitch,
                duration=trill_duration,
                velocity=note.velocity,
                start_time=current_time,
                voice=note.voice,
                is_rest=False
            )
            trill_notes.append(upper_note)
            current_time += trill_duration

        return trill_notes

    def _create_turn(self, note: Note) -> List[Note]:
        """Create a turn ornament.

        Args:
            note: The note to turn on

        Returns:
            List of notes forming the turn
        """
        # Turn: note - upper - note - lower - note
        upper_pitch = note.pitch * (2 ** (2 / 12))  # Major second above
        lower_pitch = note.pitch * (2 ** (-2 / 12))  # Major second below

        turn_duration = note.duration / 5

        turn_notes = [
            Note(pitch=note.pitch, duration=turn_duration, velocity=note.velocity,
                 start_time=note.start_time, voice=note.voice, is_rest=False),
            Note(pitch=upper_pitch, duration=turn_duration, velocity=note.velocity,
                 start_time=note.start_time + turn_duration, voice=note.voice, is_rest=False),
            Note(pitch=note.pitch, duration=turn_duration, velocity=note.velocity,
                 start_time=note.start_time + turn_duration * 2, voice=note.voice, is_rest=False),
            Note(pitch=lower_pitch, duration=turn_duration, velocity=note.velocity,
                 start_time=note.start_time + turn_duration * 3, voice=note.voice, is_rest=False),
            Note(pitch=note.pitch, duration=turn_duration, velocity=note.velocity,
                 start_time=note.start_time + turn_duration * 4, voice=note.voice, is_rest=False),
        ]

        return turn_notes

    def _create_mordent(self, note: Note) -> List[Note]:
        """Create a mordent ornament.

        Args:
            note: The note to mordent on

        Returns:
            List of notes forming the mordent
        """
        # Mordent: note - lower - note
        lower_pitch = note.pitch * (2 ** (-2 / 12))  # Major second below

        mordent_duration = note.duration / 3

        mordent_notes = [
            Note(pitch=note.pitch, duration=mordent_duration, velocity=note.velocity,
                 start_time=note.start_time, voice=note.voice, is_rest=False),
            Note(pitch=lower_pitch, duration=mordent_duration, velocity=note.velocity,
                 start_time=note.start_time + mordent_duration, voice=note.voice, is_rest=False),
            Note(pitch=note.pitch, duration=mordent_duration, velocity=note.velocity,
                 start_time=note.start_time + mordent_duration * 2, voice=note.voice, is_rest=False),
        ]

        return mordent_notes

    def _is_smooth_transition(self, pattern1: MusicalPattern, pattern2: MusicalPattern) -> bool:
        """Check if the transition between two patterns is smooth.

        Args:
            pattern1: First pattern
            pattern2: Second pattern

        Returns:
            True if transition is smooth
        """
        if not pattern1.notes or not pattern2.notes:
            return True

        # Get last note of first pattern and first note of second pattern
        last_note = pattern1.notes[-1]
        first_note = pattern2.notes[0]

        if last_note.is_rest or first_note.is_rest:
            return True

        # Check interval between last and first notes
        semitone_diff = abs(12 * math.log2(first_note.pitch / last_note.pitch))

        # Small intervals (less than a perfect fourth) are generally smooth
        return semitone_diff <= 5

    def _create_transition_pattern(self,
                                  pattern1: MusicalPattern,
                                  pattern2: MusicalPattern,
                                  mode: RenaissanceMode) -> MusicalPattern:
        """Create a transition pattern between two patterns.

        Args:
            pattern1: First pattern
            pattern2: Second pattern
            mode: The Renaissance mode

        Returns:
            Transition pattern
        """
        if not pattern1.notes or not pattern2.notes:
            return pattern1 if pattern1.notes else pattern2

        # Get last note of first pattern and first note of second pattern
        last_note = pattern1.notes[-1]
        first_note = pattern2.notes[0]

        if last_note.is_rest or first_note.is_rest:
            return pattern1

        # Create a simple transition
        transition_duration = 0.5
        transition_time = last_note.start_time + last_note.duration

        # Create a passing tone
        transition_pitch = (last_note.pitch + first_note.pitch) / 2

        transition_note = Note(
            pitch=transition_pitch,
            duration=transition_duration,
            velocity=last_note.velocity * 0.8,
            start_time=transition_time,
            voice=last_note.voice,
            is_rest=False
        )

        # Create transition pattern
        transition_pattern = MusicalPattern(
            name=f"transition_{pattern1.name}_to_{pattern2.name}",
            pattern_type="transition",
            mode=mode,
            notes=[transition_note],
            voice_leading=[],
            rhythm_profile=[transition_duration],
            context_tags=["transition"],
            source_reference=f"Transition between {pattern1.source_reference} and {pattern2.source_reference}"
        )

        return transition_pattern
