"""Integration module for connecting Renaissance music adaptation with the mechanical ensemble."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Dict, List, Union

import numpy as np

from ..artifacts import ensure_artifact_dir
from ..inventions.mechanical_ensemble import (
    _BEATS_PER_MEASURE,
    _repeat_events,
)
from .analysis import RenaissanceAnalyzer
from .constraints import MechanicalConstraintValidator
from .models import (
    AdaptationResult,
    InstrumentType,
    MusicalScore,
    Note,
    Voice,
)
from .patterns import RenaissancePatternLibrary


class MechanicalEnsembleIntegrator:
    """Integrates adapted Renaissance music with the mechanical ensemble system."""

    def __init__(self) -> None:
        """Initialize the integrator."""
        self.analyzer = RenaissanceAnalyzer()
        self.validator = MechanicalConstraintValidator()
        self.pattern_library = RenaissancePatternLibrary()

        # Import mechanical ensemble modules
        from ..inventions import (
            mechanical_carillon,
            mechanical_drum,
            mechanical_organ,
            mechanical_trumpeter,
            programmable_flute,
            viola_organista,
        )

        self.instrument_modules = {
            InstrumentType.MECHANICAL_DRUM: mechanical_drum,
            InstrumentType.MECHANICAL_ORGAN: mechanical_organ,
            InstrumentType.VIOLA_ORGANISTA: viola_organista,
            InstrumentType.PROGRAMMABLE_FLUTE: programmable_flute,
            InstrumentType.MECHANICAL_CARILLON: mechanical_carillon,
            InstrumentType.MECHANICAL_TRUMPETER: mechanical_trumpeter,
        }

    def adapt_score_for_ensemble(self, score: MusicalScore,
                                instrument_assignments: Dict[int, InstrumentType]) -> AdaptationResult:
        """Adapt a Renaissance score for the mechanical ensemble.

        Args:
            score: The original Renaissance score
            instrument_assignments: Mapping of voice indices to instrument types

        Returns:
            AdaptationResult with the adapted score and adaptation details
        """
        # Create a copy of the score for adaptation
        adapted_score = deepcopy(score)

        # Initialize adaptation result
        result = AdaptationResult(
            original_score=score,
            adapted_score=adapted_score,
            adaptation_success=False
        )

        # Analyze the original score
        detected_mode = self.analyzer.analyze_mode(score)
        detected_form = self.analyzer.classify_musical_form(score)
        rhythmic_patterns = self.analyzer.detect_rhythmic_patterns(score)

        result.add_log_entry(f"Detected mode: {detected_mode.value if detected_mode else 'unknown'}")
        result.add_log_entry(f"Detected form: {detected_form.value if detected_form else 'unknown'}")
        result.add_log_entry(f"Rhythmic patterns: {list(rhythmic_patterns.keys())}")

        # Validate against mechanical constraints
        validation_result = self.validator.validate_score(score, instrument_assignments)

        # If validation passes, we can use the original score
        if validation_result.adaptation_success:
            result.adaptation_success = True
            result.feasibility_scores = validation_result.feasibility_scores
            result.add_log_entry("Score is mechanically feasible without adaptation")
            return result

        # Otherwise, we need to adapt the score
        result.add_log_entry("Score requires adaptation for mechanical feasibility")

        # Apply adaptations based on constraint violations
        adapted_score = self._apply_adaptations(
            adapted_score, instrument_assignments, validation_result.constraint_violations, result
        )

        # Re-validate the adapted score
        revalidation_result = self.validator.validate_score(adapted_score, instrument_assignments)

        result.adapted_score = adapted_score
        result.feasibility_scores = revalidation_result.feasibility_scores
        result.constraint_violations = revalidation_result.constraint_violations
        result.adaptation_success = revalidation_result.adaptation_success

        if result.adaptation_success:
            result.add_log_entry("Successfully adapted score for mechanical performance")
        else:
            result.add_log_entry("Unable to fully adapt score for mechanical performance")
            result.add_log_entry(f"Remaining violations: {revalidation_result.constraint_violations}")

        return result

    def convert_to_ensemble_format(self, score: MusicalScore,
                                 instrument_assignments: Dict[int, InstrumentType],
                                 tempo_bpm: float = 120.0,
                                 measures: int = 4) -> Dict[str, List[Dict[str, Union[float, str]]]]:
        """Convert an adapted score to the format expected by the mechanical ensemble.

        Args:
            score: The adapted musical score
            instrument_assignments: Mapping of voice indices to instrument types
            tempo_bpm: Tempo in beats per minute
            measures: Number of measures to generate

        Returns:
            Dictionary in the format expected by mechanical_ensemble.demo()
        """
        # Calculate timing parameters
        seconds_per_beat = 60.0 / tempo_bpm
        seconds_per_measure = seconds_per_beat * _BEATS_PER_MEASURE

        # Convert each voice to events
        ensemble_score = {}

        for voice_idx, voice in enumerate(score.voices):
            instrument = instrument_assignments.get(voice_idx)
            if not instrument:
                continue

            # Get the instrument module
            instrument_module = self.instrument_modules.get(instrument)
            if not instrument_module:
                continue

            # Extract events from the voice
            events = self._extract_voice_events(voice, instrument)

            # Repeat events for the specified number of measures
            repeated_events = _repeat_events(events, measures, seconds_per_measure)

            # Add to ensemble score
            ensemble_score[instrument.value] = repeated_events

        return ensemble_score

    def validate_with_simulation(self, score: MusicalScore,
                               instrument_assignments: Dict[int, InstrumentType],
                               seed: int = 0) -> Dict[str, Union[bool, List[str]]]:
        """Validate the adapted score against the existing simulation system.

        Args:
            score: The adapted musical score
            instrument_assignments: Mapping of voice indices to instrument types
            seed: Random seed for simulation

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "valid": True,
            "warnings": [],
            "errors": []
        }

        # Check each instrument against its simulation
        for voice_idx, voice in enumerate(score.voices):
            instrument = instrument_assignments.get(voice_idx)
            if not instrument:
                validation_results["errors"].append(f"Voice {voice_idx} has no instrument assignment")
                validation_results["valid"] = False
                continue

            instrument_module = self.instrument_modules.get(instrument)
            if not instrument_module:
                validation_results["errors"].append(f"No simulation module for {instrument.value}")
                validation_results["valid"] = False
                continue

            try:
                # Load instrument parameters
                params = instrument_module._load_params()  # type: ignore[attr-defined]

                # Simulate the instrument
                simulation_data = instrument_module._simulate(params, seed=seed)  # type: ignore[attr-defined]

                # Check if the voice notes are compatible with the simulation
                voice_compatible = self._check_voice_simulation_compatibility(
                    voice, simulation_data, instrument
                )

                if not voice_compatible["compatible"]:
                    validation_results["valid"] = False
                    validation_results["errors"].extend(voice_compatible["errors"])
                else:
                    validation_results["warnings"].extend(voice_compatible["warnings"])

            except Exception as e:
                validation_results["errors"].append(
                    f"Simulation error for {instrument.value}: {str(e)}"
                )
                validation_results["valid"] = False

        return validation_results

    def generate_ensemble_demo(self, score: MusicalScore,
                             instrument_assignments: Dict[int, InstrumentType],
                             tempo_bpm: float = 120.0,
                             measures: int = 4,
                             render_audio: bool = False,
                             sample_rate: int = 44100,
                             seed: int = 0) -> Dict[str, Union[List[str], float]]:
        """Generate a complete ensemble demo from an adapted score.

        Args:
            score: The adapted musical score
            instrument_assignments: Mapping of voice indices to instrument types
            tempo_bpm: Tempo in beats per minute
            measures: Number of measures to generate
            render_audio: Whether to render audio output
            sample_rate: Audio sample rate
            seed: Random seed for simulation

        Returns:
            Dictionary with demo results
        """
        # Convert to ensemble format
        ensemble_score = self.convert_to_ensemble_format(
            score, instrument_assignments, tempo_bpm, measures
        )

        # Create demo configuration
        demo_config = {
            "tempo_bpm": tempo_bpm,
            "measures": measures,
            "beats_per_measure": _BEATS_PER_MEASURE,
            "score": ensemble_score,
        }

        # Validate with simulation
        validation_results = self.validate_with_simulation(
            score, instrument_assignments, seed
        )

        # Generate artifacts
        artifacts = []

        # Save the ensemble score
        demo_dir = ensure_artifact_dir("renaissance_music", subdir="demo")
        score_path = demo_dir / "adapted_ensemble_score.json"

        try:
            with score_path.open("w", encoding="utf-8") as f:
                json.dump(demo_config, f, indent=2)
        except (AttributeError, TypeError):
            pass

        artifacts.append(str(score_path))

        # Render audio if requested
        if render_audio:
            try:
                from ..core.audio import render_score_to_wav

                audio_path = demo_dir / "adapted_ensemble_audio.wav"
                render_score_to_wav(
                    ensemble_score, tempo_bpm, _BEATS_PER_MEASURE,
                    audio_path, sample_rate=sample_rate
                )
                artifacts.append(str(audio_path))
            except Exception as e:
                validation_results["warnings"].append(f"Audio rendering failed: {str(e)}")

        return {
            "artifacts": artifacts,
            "tempo_bpm": tempo_bpm,
            "measures": measures,
            "valid": validation_results["valid"],
            "warnings": validation_results["warnings"],
            "errors": validation_results["errors"],
        }

    def _apply_adaptations(self, score: MusicalScore,
                          instrument_assignments: Dict[int, InstrumentType],
                          violations: List[str],
                          result: AdaptationResult) -> MusicalScore:
        """Apply adaptations to fix constraint violations.

        Args:
            score: The score to adapt
            instrument_assignments: Mapping of voice indices to instrument types
            violations: List of constraint violations
            result: AdaptationResult to log changes

        Returns:
            The adapted score
        """
        adapted_score = deepcopy(score)

        # Group violations by type
        pitch_violations = [v for v in violations if "outside instrument range" in v]
        duration_violations = [v for v in violations if "duration" in v and "outside the valid range" in v]
        rapid_violations = [v for v in violations if "Rapid passage" in v]
        polyphony_violations = [v for v in violations if "simultaneous notes" in v]

        # Apply pitch adaptations
        if pitch_violations:
            adapted_score = self._adapt_pitch_ranges(
                adapted_score, instrument_assignments, result
            )

        # Apply duration adaptations
        if duration_violations:
            adapted_score = self._adapt_note_durations(
                adapted_score, instrument_assignments, result
            )

        # Apply rapid passage adaptations
        if rapid_violations:
            adapted_score = self._adapt_rapid_passages(
                adapted_score, instrument_assignments, result
            )

        # Apply polyphony adaptations
        if polyphony_violations:
            adapted_score = self._adapt_polyphony(
                adapted_score, instrument_assignments, result
            )

        return adapted_score

    def _adapt_pitch_ranges(self, score: MusicalScore,
                           instrument_assignments: Dict[int, InstrumentType],
                           result: AdaptationResult) -> MusicalScore:
        """Adapt notes to fit within instrument pitch ranges."""
        adapted_score = deepcopy(score)

        for voice_idx, voice in enumerate(score.voices):
            instrument = instrument_assignments.get(voice_idx)
            if not instrument:
                continue

            constraints = self.validator.get_constraints(instrument)
            min_pitch, max_pitch = constraints.pitch_range

            adapted_voice = deepcopy(voice)
            adapted_notes = []

            for note in voice.notes:
                if note.is_rest:
                    adapted_notes.append(note)
                    continue

                if note.pitch < min_pitch:
                    # Transpose up by octaves until in range
                    transposed_pitch = note.pitch
                    while transposed_pitch < min_pitch:
                        transposed_pitch *= 2.0

                    # If still out of range, transpose down
                    if transposed_pitch > max_pitch:
                        transposed_pitch = note.pitch
                        while transposed_pitch > max_pitch:
                            transposed_pitch *= 0.5

                    adapted_note = Note(
                        pitch=transposed_pitch,
                        duration=note.duration,
                        velocity=note.velocity,
                        start_time=note.start_time,
                        voice=note.voice,
                        is_rest=note.is_rest
                    )
                    adapted_notes.append(adapted_note)

                    result.add_log_entry(
                        f"Transposed note in voice {voice_idx} from {note.pitch:.1f}Hz "
                        f"to {transposed_pitch:.1f}Hz to fit instrument range"
                    )

                elif note.pitch > max_pitch:
                    # Transpose down by octaves until in range
                    transposed_pitch = note.pitch
                    while transposed_pitch > max_pitch:
                        transposed_pitch *= 0.5

                    # If still out of range, transpose up
                    if transposed_pitch < min_pitch:
                        transposed_pitch = note.pitch
                        while transposed_pitch < min_pitch:
                            transposed_pitch *= 2.0

                    adapted_note = Note(
                        pitch=transposed_pitch,
                        duration=note.duration,
                        velocity=note.velocity,
                        start_time=note.start_time,
                        voice=note.voice,
                        is_rest=note.is_rest
                    )
                    adapted_notes.append(adapted_note)

                    result.add_log_entry(
                        f"Transposed note in voice {voice_idx} from {note.pitch:.1f}Hz "
                        f"to {transposed_pitch:.1f}Hz to fit instrument range"
                    )

                else:
                    adapted_notes.append(note)

            adapted_voice.notes = adapted_notes
            adapted_score.voices[voice_idx] = adapted_voice

        return adapted_score

    def _adapt_note_durations(self, score: MusicalScore,
                             instrument_assignments: Dict[int, InstrumentType],
                             result: AdaptationResult) -> MusicalScore:
        """Adapt note durations to fit within instrument capabilities."""
        adapted_score = deepcopy(score)

        for voice_idx, voice in enumerate(score.voices):
            instrument = instrument_assignments.get(voice_idx)
            if not instrument:
                continue

            constraints = self.validator.get_constraints(instrument)

            adapted_voice = deepcopy(voice)
            adapted_notes = []

            for note in voice.notes:
                if note.is_rest:
                    adapted_notes.append(note)
                    continue

                adapted_duration = note.duration

                # Adjust duration if too short
                if adapted_duration < constraints.min_note_duration:
                    adapted_duration = constraints.min_note_duration
                    result.add_log_entry(
                        f"Lengthened note in voice {voice_idx} from {note.duration:.3f}s "
                        f"to {adapted_duration:.3f}s to meet minimum duration"
                    )

                # Adjust duration if too long
                elif adapted_duration > constraints.max_note_duration:
                    adapted_duration = constraints.max_note_duration
                    result.add_log_entry(
                        f"Shortened note in voice {voice_idx} from {note.duration:.3f}s "
                        f"to {adapted_duration:.3f}s to meet maximum duration"
                    )

                adapted_note = Note(
                    pitch=note.pitch,
                    duration=adapted_duration,
                    velocity=note.velocity,
                    start_time=note.start_time,
                    voice=note.voice,
                    is_rest=note.is_rest
                )
                adapted_notes.append(adapted_note)

            adapted_voice.notes = adapted_notes
            adapted_score.voices[voice_idx] = adapted_voice

        return adapted_score

    def _adapt_rapid_passages(self, score: MusicalScore,
                             instrument_assignments: Dict[int, InstrumentType],
                             result: AdaptationResult) -> MusicalScore:
        """Adapt rapid passages to be mechanically feasible."""
        adapted_score = deepcopy(score)

        for voice_idx, voice in enumerate(score.voices):
            instrument = instrument_assignments.get(voice_idx)
            if not instrument:
                continue

            constraints = self.validator.get_constraints(instrument)

            adapted_voice = deepcopy(voice)
            adapted_notes = []

            # Identify rapid passages
            rapid_indices = []
            for i in range(1, len(voice.notes)):
                prev_note = voice.notes[i-1]
                curr_note = voice.notes[i]

                if prev_note.is_rest or curr_note.is_rest:
                    continue

                time_diff = curr_note.start_time - prev_note.start_time

                if time_diff < constraints.rapid_passage_threshold:
                    if not rapid_indices or rapid_indices[-1] != i-1:
                        rapid_indices.append(i-1)
                    rapid_indices.append(i)

            # Simplify rapid passages
            for i, note in enumerate(voice.notes):
                if i in rapid_indices:
                    # Insert short rests between rapid notes
                    adapted_notes.append(note)

                    # Add a short rest after this note if the next note is also rapid
                    if i+1 in rapid_indices:
                        rest = Note(
                            pitch=0.0,
                            duration=constraints.rapid_passage_threshold * 0.5,
                            velocity=0.0,
                            start_time=note.start_time + note.duration,
                            voice=note.voice,
                            is_rest=True
                        )
                        adapted_notes.append(rest)
                else:
                    adapted_notes.append(note)

            # Adjust start times
            current_time = 0.0
            for note in adapted_notes:
                note.start_time = current_time
                current_time += note.duration

            adapted_voice.notes = adapted_notes
            adapted_score.voices[voice_idx] = adapted_voice

            if rapid_indices:
                result.add_log_entry(
                    f"Simplified rapid passage in voice {voice_idx} by adding rests"
                )

        return adapted_score

    def _adapt_polyphony(self, score: MusicalScore,
                        instrument_assignments: Dict[int, InstrumentType],
                        result: AdaptationResult) -> MusicalScore:
        """Adapt polyphony to stay within instrument limitations."""
        adapted_score = deepcopy(score)

        # This is a simplified implementation - a full implementation would
        # use more sophisticated voice redistribution techniques

        # For now, we'll just add a warning about polyphony limitations
        result.add_log_entry(
            "Polyphony adaptation not fully implemented - manual voice redistribution may be required"
        )

        return adapted_score

    def _extract_voice_events(self, voice: Voice,
                            instrument: InstrumentType) -> List[Dict[str, Union[float, str]]]:
        """Extract events from a voice in the format expected by the ensemble."""
        events = []

        for note in voice.notes:
            if note.is_rest:
                continue

            # Determine event kind based on instrument
            kind = "percussive" if instrument == InstrumentType.MECHANICAL_DRUM else "pitched"

            event = {
                "index": float(len(events)),
                "time_s": float(note.start_time),
                "frequency_hz": float(note.pitch),
                "intensity": float(note.velocity),
                "kind": kind,
            }
            events.append(event)

        return events

    def _check_voice_simulation_compatibility(self, voice: Voice,
                                            simulation_data: Dict[str, np.ndarray],
                                            instrument: InstrumentType) -> Dict[str, Union[bool, List[str]]]:
        """Check if a voice is compatible with the instrument simulation."""
        result = {
            "compatible": True,
            "errors": [],
            "warnings": []
        }

        # Check if the voice has notes
        if not voice.notes or all(note.is_rest for note in voice.notes):
            result["warnings"].append(f"Voice has no sounding notes for {instrument.value}")
            return result

        # Get voice pitch range
        voice_pitches = [note.pitch for note in voice.notes if not note.is_rest]
        voice_min_pitch = min(voice_pitches)
        voice_max_pitch = max(voice_pitches)

        # Check against simulation frequency range
        if "ideal_frequency_hz" in simulation_data:
            sim_freqs = np.asarray(simulation_data["ideal_frequency_hz"])
            sim_min_freq = float(np.min(sim_freqs))
            sim_max_freq = float(np.max(sim_freqs))

            if voice_min_pitch < sim_min_freq * 0.8 or voice_max_pitch > sim_max_freq * 1.2:
                result["errors"].append(
                    f"Voice pitch range ({voice_min_pitch:.1f}-{voice_max_pitch:.1f}Hz) "
                    f"is outside simulation range ({sim_min_freq:.1f}-{sim_max_freq:.1f}Hz) "
                    f"for {instrument.value}"
                )
                result["compatible"] = False

        # Check timing compatibility
        if "ideal_times_s" in simulation_data:
            sim_times = np.asarray(simulation_data["ideal_times_s"])
            sim_min_interval = float(np.min(np.diff(sim_times)))

            # Check if voice has very short notes
            voice_durations = [note.duration for note in voice.notes if not note.is_rest]
            min_duration = min(voice_durations)

            if min_duration < sim_min_interval * 0.5:
                result["warnings"].append(
                    f"Voice has very short notes ({min_duration:.3f}s) compared to "
                    f"simulation minimum interval ({sim_min_interval:.3f}s) for {instrument.value}"
                )

        return result
