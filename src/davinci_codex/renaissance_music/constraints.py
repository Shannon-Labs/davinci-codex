"""Constraint engine for validating mechanical instrument capabilities."""

from __future__ import annotations

from typing import Dict, List

from .models import (
    AdaptationResult,
    InstrumentConstraints,
    InstrumentType,
    MusicalScore,
    Voice,
)


class MechanicalConstraintValidator:
    """Validates musical scores against mechanical instrument constraints."""

    # Default constraints for each instrument type
    _DEFAULT_CONSTRAINTS = {
        InstrumentType.MECHANICAL_DRUM: InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_DRUM,
            pitch_range=(80.0, 400.0),  # Bass drum to snare range
            max_polyphony=1,
            min_note_duration=0.05,
            max_note_duration=2.0,
            max_rapid_passages=16,
            rapid_passage_threshold=0.15,
            mechanical_delay=0.02,
            can_play_legato=False,
            can_play_staccato=True,
        ),
        InstrumentType.MECHANICAL_ORGAN: InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_ORGAN,
            pitch_range=(65.41, 2093.0),  # C2 to C7
            max_polyphony=8,
            min_note_duration=0.2,
            max_note_duration=10.0,
            max_rapid_passages=12,
            rapid_passage_threshold=0.2,
            mechanical_delay=0.1,
            can_play_legato=True,
            can_play_staccato=True,
        ),
        InstrumentType.VIOLA_ORGANISTA: InstrumentConstraints(
            instrument_type=InstrumentType.VIOLA_ORGANISTA,
            pitch_range=(130.81, 1046.5),  # C3 to C6
            max_polyphony=4,
            min_note_duration=0.15,
            max_note_duration=8.0,
            max_rapid_passages=10,
            rapid_passage_threshold=0.25,
            mechanical_delay=0.08,
            can_play_legato=True,
            can_play_staccato=False,
        ),
        InstrumentType.PROGRAMMABLE_FLUTE: InstrumentConstraints(
            instrument_type=InstrumentType.PROGRAMMABLE_FLUTE,
            pitch_range=(261.63, 1568.0),  # C4 to G6
            max_polyphony=1,
            min_note_duration=0.1,
            max_note_duration=6.0,
            max_rapid_passages=20,
            rapid_passage_threshold=0.1,
            mechanical_delay=0.05,
            can_play_legato=True,
            can_play_staccato=True,
        ),
        InstrumentType.MECHANICAL_CARILLON: InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_CARILLON,
            pitch_range=(196.0, 3920.0),  # G3 to B7
            max_polyphony=4,
            min_note_duration=0.3,
            max_note_duration=5.0,
            max_rapid_passages=6,
            rapid_passage_threshold=0.4,
            mechanical_delay=0.15,
            can_play_legato=False,
            can_play_staccato=True,
        ),
        InstrumentType.MECHANICAL_TRUMPETER: InstrumentConstraints(
            instrument_type=InstrumentType.MECHANICAL_TRUMPETER,
            pitch_range=(164.81, 987.77),  # E3 to B5
            max_polyphony=1,
            min_note_duration=0.1,
            max_note_duration=4.0,
            max_rapid_passages=8,
            rapid_passage_threshold=0.2,
            mechanical_delay=0.03,
            can_play_legato=False,
            can_play_staccato=True,
        ),
    }

    def __init__(self) -> None:
        """Initialize the constraint validator."""
        self.constraints: Dict[InstrumentType, InstrumentConstraints] = {}
        self._load_default_constraints()

    def _load_default_constraints(self) -> None:
        """Load default constraints for all instrument types."""
        for instrument_type, constraints in self._DEFAULT_CONSTRAINTS.items():
            self.constraints[instrument_type] = constraints

    def set_constraints(self, instrument: InstrumentType,
                       constraints: InstrumentConstraints) -> None:
        """Set custom constraints for an instrument.

        Args:
            instrument: The instrument type
            constraints: The custom constraints
        """
        self.constraints[instrument] = constraints

    def get_constraints(self, instrument: InstrumentType) -> InstrumentConstraints:
        """Get constraints for an instrument.

        Args:
            instrument: The instrument type

        Returns:
            The constraints for the instrument
        """
        return self.constraints.get(
            instrument,
            self._DEFAULT_CONSTRAINTS.get(instrument, InstrumentConstraints(
                instrument_type=instrument,
                pitch_range=(0.0, 0.0),
                max_polyphony=1
            ))
        )

    def validate_score(self, score: MusicalScore,
                      instrument_assignments: Dict[int, InstrumentType]) -> AdaptationResult:
        """Validate a complete score against instrument constraints.

        Args:
            score: The musical score to validate
            instrument_assignments: Mapping of voice indices to instrument types

        Returns:
            AdaptationResult with validation details
        """
        from copy import deepcopy

        result = AdaptationResult(
            original_score=deepcopy(score),
            adapted_score=deepcopy(score),
            adaptation_success=False
        )

        # Validate each voice against its assigned instrument
        for voice_idx, voice in enumerate(score.voices):
            instrument = instrument_assignments.get(voice_idx)
            if not instrument:
                result.add_violation(f"Voice {voice_idx} has no instrument assignment")
                continue

            constraints = self.get_constraints(instrument)
            voice_result = self.validate_voice(voice, constraints)

            # Add violations to the result
            for violation in voice_result.constraint_violations:
                result.add_violation(f"Voice {voice_idx}: {violation}")

            # Set feasibility score
            result.set_feasibility_score(
                instrument,
                voice_result.get_overall_feasibility()
            )

        # Check overall polyphony constraints
        self._validate_ensemble_polyphony(score, instrument_assignments, result)

        # Check tempo relationships
        self._validate_tempo_relationships(score, instrument_assignments, result)

        # Determine overall success
        result.adaptation_success = (
            len(result.constraint_violations) == 0 and
            all(score >= 0.7 for score in result.feasibility_scores.values())
        )

        return result

    def validate_voice(self, voice: Voice,
                      constraints: InstrumentConstraints) -> AdaptationResult:
        """Validate a single voice against instrument constraints.

        Args:
            voice: The voice to validate
            constraints: The instrument constraints

        Returns:
            AdaptationResult with validation details
        """
        from copy import deepcopy

        # Create a temporary score for the voice
        temp_score = MusicalScore()
        temp_score.add_voice(voice)

        result = AdaptationResult(
            original_score=deepcopy(temp_score),
            adapted_score=deepcopy(temp_score),
            adaptation_success=False
        )

        # Validate pitch ranges
        self._validate_pitch_range(voice, constraints, result)

        # Validate rhythmic compatibility
        self._validate_rhythmic_compatibility(voice, constraints, result)

        # Validate rapid passages
        self._validate_rapid_passages(voice, constraints, result)

        # Validate note durations
        self._validate_note_durations(voice, constraints, result)

        # Calculate overall feasibility
        feasibility = constraints.calculate_mechanical_feasibility(voice.notes)
        result.set_feasibility_score(constraints.instrument_type, feasibility)

        result.adaptation_success = len(result.constraint_violations) == 0

        return result

    def _validate_pitch_range(self, voice: Voice,
                             constraints: InstrumentConstraints,
                             result: AdaptationResult) -> None:
        """Validate that all notes are within the instrument's pitch range."""
        for note in voice.notes:
            if note.is_rest:
                continue

            if not constraints.can_play_pitch(note.pitch):
                result.add_violation(
                    f"Note at {note.start_time:.2f}s (pitch: {note.pitch:.1f}Hz) "
                    f"is outside instrument range ({constraints.pitch_range[0]:.1f}-"
                    f"{constraints.pitch_range[1]:.1f}Hz)"
                )

    def _validate_rhythmic_compatibility(self, voice: Voice,
                                       constraints: InstrumentConstraints,
                                       result: AdaptationResult) -> None:
        """Validate rhythmic compatibility with mechanical timing."""
        # Check for very short notes that might be mechanically impossible
        for note in voice.notes:
            if note.is_rest:
                continue

            if note.duration < constraints.mechanical_delay:
                result.add_violation(
                    f"Note at {note.start_time:.2f}s is too short "
                    f"({note.duration:.3f}s) for mechanical response "
                    f"(delay: {constraints.mechanical_delay:.3f}s)"
                )

        # Check legato/staccato compatibility
        for i in range(1, len(voice.notes)):
            prev_note = voice.notes[i-1]
            curr_note = voice.notes[i]

            if prev_note.is_rest or curr_note.is_rest:
                continue

            # Check if this is a legato passage
            is_legato = (curr_note.start_time -
                        (prev_note.start_time + prev_note.duration)) < 0.01

            if is_legato and not constraints.can_play_legato:
                result.add_violation(
                    f"Legato passage at {prev_note.start_time:.2f}s "
                    f"is not supported by this instrument"
                )

    def _validate_rapid_passages(self, voice: Voice,
                               constraints: InstrumentConstraints,
                               result: AdaptationResult) -> None:
        """Validate that rapid passages don't exceed instrument limitations."""
        rapid_count = 0
        rapid_start_idx = -1

        for i in range(1, len(voice.notes)):
            prev_note = voice.notes[i-1]
            curr_note = voice.notes[i]

            if prev_note.is_rest or curr_note.is_rest:
                if rapid_count > constraints.max_rapid_passages:
                    result.add_violation(
                        f"Rapid passage starting at note {rapid_start_idx} "
                        f"has {rapid_count} notes (max: {constraints.max_rapid_passages})"
                    )
                rapid_count = 0
                rapid_start_idx = -1
                continue

            time_diff = curr_note.start_time - prev_note.start_time

            if time_diff < constraints.rapid_passage_threshold:
                if rapid_count == 0:
                    rapid_start_idx = i-1
                rapid_count += 1
            else:
                if rapid_count > constraints.max_rapid_passages:
                    result.add_violation(
                        f"Rapid passage starting at note {rapid_start_idx} "
                        f"has {rapid_count} notes (max: {constraints.max_rapid_passages})"
                    )
                rapid_count = 0
                rapid_start_idx = -1

        # Check the last rapid passage
        if rapid_count > constraints.max_rapid_passages:
            result.add_violation(
                f"Rapid passage starting at note {rapid_start_idx} "
                f"has {rapid_count} notes (max: {constraints.max_rapid_passages})"
            )

    def _validate_note_durations(self, voice: Voice,
                               constraints: InstrumentConstraints,
                               result: AdaptationResult) -> None:
        """Validate that note durations are within instrument capabilities."""
        for note in voice.notes:
            if note.is_rest:
                continue

            if not constraints.can_play_duration(note.duration):
                result.add_violation(
                    f"Note at {note.start_time:.2f}s has duration "
                    f"{note.duration:.3f}s which is outside the valid range "
                    f"({constraints.min_note_duration:.3f}s - "
                    f"{constraints.max_note_duration:.3f}s)"
                )

    def _validate_ensemble_polyphony(self, score: MusicalScore,
                                   instrument_assignments: Dict[int, InstrumentType],
                                   result: AdaptationResult) -> None:
        """Validate that ensemble polyphony doesn't exceed limitations."""
        # Get all time points where notes start or end
        time_points = set()
        for voice in score.voices:
            for note in voice.notes:
                time_points.add(note.start_time)
                time_points.add(note.start_time + note.duration)

        # Check polyphony at each time point
        for time_point in sorted(time_points):
            sounding_notes = score.get_notes_at_time(time_point)

            # Group by instrument type
            instrument_counts: Dict[InstrumentType, int] = {}
            for voice_idx, _note in sounding_notes:
                instrument = instrument_assignments.get(voice_idx)
                if instrument:
                    instrument_counts[instrument] = instrument_counts.get(instrument, 0) + 1

            # Check against constraints
            for instrument, count in instrument_counts.items():
                constraints = self.get_constraints(instrument)
                if count > constraints.max_polyphony:
                    result.add_violation(
                        f"At {time_point:.2f}s, {instrument.value} has "
                        f"{count} simultaneous notes (max: {constraints.max_polyphony})"
                    )

    def _validate_tempo_relationships(self, score: MusicalScore,
                                    instrument_assignments: Dict[int, InstrumentType],
                                    result: AdaptationResult) -> None:
        """Validate tempo relationships between instruments."""
        # Check if the tempo is suitable for all instruments
        tempo_bpm = score.tempo_bpm

        # Define tempo ranges for different instruments
        tempo_ranges = {
            InstrumentType.MECHANICAL_DRUM: (40, 200),
            InstrumentType.MECHANICAL_ORGAN: (40, 160),
            InstrumentType.VIOLA_ORGANISTA: (50, 140),
            InstrumentType.PROGRAMMABLE_FLUTE: (60, 180),
            InstrumentType.MECHANICAL_CARILLON: (40, 120),
            InstrumentType.MECHANICAL_TRUMPETER: (50, 160),
        }

        used_instruments = set(instrument_assignments.values())

        for instrument in used_instruments:
            min_tempo, max_tempo = tempo_ranges.get(instrument, (40, 200))

            if not (min_tempo <= tempo_bpm <= max_tempo):
                result.add_violation(
                    f"Tempo {tempo_bpm} BPM is outside the suitable range "
                    f"for {instrument.value} ({min_tempo}-{max_tempo} BPM)"
                )

    def suggest_adaptations(self, score: MusicalScore,
                          instrument_assignments: Dict[int, InstrumentType]) -> List[str]:
        """Suggest adaptations to make the score more mechanically feasible.

        Args:
            score: The musical score to analyze
            instrument_assignments: Mapping of voice indices to instrument types

        Returns:
            List of adaptation suggestions
        """
        suggestions = []

        # Validate the score first
        validation_result = self.validate_score(score, instrument_assignments)

        # Analyze violations and suggest fixes
        for violation in validation_result.constraint_violations:
            if "outside instrument range" in violation:
                suggestions.append(
                    "Consider transpose/transposing the voice to fit the instrument's range"
                )
            elif "too short" in violation and "mechanical response" in violation:
                suggestions.append("Lengthen very short notes or combine them with adjacent notes")
            elif "Legato passage" in violation and "not supported" in violation:
                suggestions.append("Add short breaks between notes or use a different instrument")
            elif "Rapid passage" in violation and "notes (max:" in violation:
                suggestions.append("Simplify rapid passages or assign to a more agile instrument")
            elif "simultaneous notes (max:" in violation:
                suggestions.append("Reduce polyphony or reassign some voices to different instruments")
            elif "Tempo" in violation and "outside the suitable range" in violation:
                suggestions.append("Adjust the tempo to suit all instruments")

        # Add general suggestions based on feasibility scores
        for instrument, score in validation_result.feasibility_scores.items():
            if score < 0.5:
                suggestions.append(
                    f"Consider using a different instrument than {instrument.value} "
                    f"or significantly simplifying the part"
                )
            elif score < 0.7:
                suggestions.append(
                    f"The {instrument.value} part may need some simplification "
                    f"for better mechanical performance"
                )

        return suggestions
