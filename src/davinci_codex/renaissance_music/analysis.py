"""Historical music analysis module for Renaissance music adaptation."""

from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List, Optional, Tuple

from .models import (
    MusicalForm,
    MusicalPattern,
    MusicalScore,
    Note,
    RenaissanceMode,
)


class RenaissanceAnalyzer:
    """Analyzes Renaissance music structures and characteristics."""

    # Mode characteristics based on final (reciting tone) and range
    _MODE_CHARACTERISTICS = {
        RenaissanceMode.DORIAN: {
            "final": 293.66,  # D4
            "reciting_tone": 392.00,  # G4
            "typical_range": (196.00, 587.33),  # G3 to D5
            "characteristic_intervals": [2, 2, 1, 2, 2, 2, 1],  # Whole/Half steps
        },
        RenaissanceMode.PHRYGIAN: {
            "final": 329.63,  # E4
            "reciting_tone": 440.00,  # A4
            "typical_range": (220.00, 659.25),  # A3 to E5
            "characteristic_intervals": [1, 2, 2, 2, 1, 2, 2],
        },
        RenaissanceMode.LYDIAN: {
            "final": 349.23,  # F4
            "reciting_tone": 493.88,  # B4
            "typical_range": (246.94, 739.99),  # B3 to F#5
            "characteristic_intervals": [2, 2, 2, 1, 2, 2, 1],
        },
        RenaissanceMode.MIXOLYDIAN: {
            "final": 392.00,  # G4
            "reciting_tone": 523.25,  # C5
            "typical_range": (293.66, 880.00),  # D4 to A5
            "characteristic_intervals": [2, 2, 1, 2, 2, 1, 2],
        },
        RenaissanceMode.HYPODORIAN: {
            "final": 293.66,  # D4
            "reciting_tone": 392.00,  # G4
            "typical_range": (130.81, 493.88),  # C3 to B4
            "characteristic_intervals": [2, 2, 1, 2, 2, 2, 1],
        },
        RenaissanceMode.HYPOPHRYGIAN: {
            "final": 329.63,  # E4
            "reciting_tone": 440.00,  # A4
            "typical_range": (146.83, 554.37),  # D3 to C#5
            "characteristic_intervals": [1, 2, 2, 2, 1, 2, 2],
        },
        RenaissanceMode.HYPOLYDIAN: {
            "final": 349.23,  # F4
            "reciting_tone": 493.88,  # B4
            "typical_range": (164.81, 622.25),  # E3 to D#5
            "characteristic_intervals": [2, 2, 2, 1, 2, 2, 1],
        },
        RenaissanceMode.HYPOMIXOLYDIAN: {
            "final": 392.00,  # G4
            "reciting_tone": 523.25,  # C5
            "typical_range": (196.00, 783.99),  # G3 to G5
            "characteristic_intervals": [2, 2, 1, 2, 2, 1, 2],
        },
    }

    # Common cadential patterns in Renaissance music
    _CADENTIAL_PATTERNS = {
        "authentic_cadence": [7, 2, 1],  # Leading tone to tonic
        "plagal_cadence": [4, 1],  # Subdominant to tonic
        "deceptive_cadence": [7, 6],  # Leading tone to submediant
        "phrygian_cadence": [2, 1, 7, 1],  # Characteristic Phrygian half-step
    }

    def __init__(self) -> None:
        """Initialize the analyzer."""
        self._pitch_class_cache: Dict[float, int] = {}

    def analyze_mode(self, score: MusicalScore) -> Optional[RenaissanceMode]:
        """Analyze the modal structure of a musical score.

        Args:
            score: The musical score to analyze

        Returns:
            The most likely Renaissance mode, or None if unclear
        """
        if not score.voices:
            return None

        # Collect all pitches from the score
        all_pitches = []
        for voice in score.voices:
            for note in voice.notes:
                if not note.is_rest:
                    all_pitches.append(note.pitch)

        if not all_pitches:
            return None

        # Find the most common pitch class (modality center)
        pitch_classes = [self._pitch_to_class(pitch) for pitch in all_pitches]
        pitch_class_counts = Counter(pitch_classes)
        most_common_pc = pitch_class_counts.most_common(1)[0][0]

        # Find the final (most frequent pitch in the most common class)
        candidates = [pitch for pitch in all_pitches
                     if self._pitch_to_class(pitch) == most_common_pc]
        final = min(candidates)  # Choose the lowest as the final

        # Compare with mode characteristics
        best_mode = None
        best_score = 0.0

        for mode, characteristics in self._MODE_CHARACTERISTICS.items():
            # Check if final matches (within a semitone)
            final_match = self._compare_pitches(final, characteristics["final"])
            if final_match > 0.8:  # Good match
                # Check range compatibility
                score_range = (min(all_pitches), max(all_pitches))
                range_match = self._compare_ranges(
                    score_range, characteristics["typical_range"]
                )

                # Check interval patterns
                interval_match = self._analyze_interval_patterns(
                    all_pitches, characteristics["characteristic_intervals"]
                )

                # Combined score
                total_score = (final_match * 0.5 + range_match * 0.3 +
                              interval_match * 0.2)

                if total_score > best_score:
                    best_score = total_score
                    best_mode = mode

        return best_mode if best_score > 0.6 else None

    def detect_rhythmic_patterns(self, score: MusicalScore) -> Dict[str, float]:
        """Detect rhythmic patterns and mensuration.

        Args:
            score: The musical score to analyze

        Returns:
            Dictionary with pattern names and confidence scores
        """
        if not score.voices:
            return {}

        # Collect all note durations
        all_durations = []
        for voice in score.voices:
            for note in voice.notes:
                if not note.is_rest:
                    all_durations.append(note.duration)

        if not all_durations:
            return {}

        # Normalize durations to find the base pulse
        min_duration = min(all_durations)
        normalized_durations = [d / min_duration for d in all_durations]
        total_notes = len(normalized_durations)

        def _ratio_share(target: float, tolerance: float = 0.15) -> float:
            matches = sum(1 for value in normalized_durations
                          if abs(value - target) <= tolerance)
            return matches / total_notes

        patterns = {}

        # Detect mensuration based on common duration ratios
        if _ratio_share(1.0) > 0.4:
            if _ratio_share(1.5) > 0.2:
                patterns["perfect_tempus"] = 0.85  # 3/4 feel
            else:
                patterns["imperfect_tempus"] = 0.8  # 2/4 feel

        if _ratio_share(2.0) > 0.3:
            if _ratio_share(3.0) > 0.2:
                patterns["perfect_prolation"] = 0.75  # Compound meter
            else:
                patterns["imperfect_prolation"] = 0.7  # Simple meter

        # Detect dance rhythms
        if self._detect_dance_rhythm(normalized_durations):
            patterns["dance_rhythm"] = 0.9

        # Canonical duration clustering for steady triple-feel passages
        canonical_counts = Counter(round(duration / 0.5) * 0.5 for duration in all_durations)
        if canonical_counts:
            dominant_duration, dominant_count = canonical_counts.most_common(1)[0]
            if dominant_duration >= 1.4 and dominant_count / total_notes > 0.6:
                patterns.setdefault("perfect_tempus", 0.75)

        return patterns

    def identify_melodic_patterns(self, score: MusicalScore) -> List[MusicalPattern]:
        """Identify melodic patterns typical of Renaissance dance forms.

        Args:
            score: The musical score to analyze

        Returns:
            List of identified musical patterns
        """
        patterns = []

        for voice_idx, voice in enumerate(score.voices):
            if len(voice.notes) < 4:  # Need enough notes for patterns
                continue

            # Extract melodic sequences
            voice_patterns = self._extract_melodic_patterns(
                voice.notes, voice_idx, score.mode
            )
            patterns.extend(voice_patterns)

        return patterns

    def extract_voice_leading(self, score: MusicalScore) -> List[List[Tuple[float, float]]]:
        """Extract voice leading and polyphonic structures.

        Args:
            score: The musical score to analyze

        Returns:
            List of voice leading patterns for each voice
        """
        voice_leadings = []

        for voice in score.voices:
            leading = []
            for i in range(1, len(voice.notes)):
                prev_note = voice.notes[i-1]
                curr_note = voice.notes[i]

                if not prev_note.is_rest and not curr_note.is_rest:
                    leading.append((prev_note.pitch, curr_note.pitch))

            voice_leadings.append(leading)

        return voice_leadings

    def classify_musical_form(self, score: MusicalScore) -> Optional[MusicalForm]:
        """Classify the musical form (dance, isorhythmic, etc.).

        Args:
            score: The musical score to analyze

        Returns:
            The most likely musical form, or None if unclear
        """
        if not score.voices:
            return None

        # Analyze structural characteristics
        duration = score.get_duration()
        voice_count = score.get_voice_count()

        note_count = sum(len(voice.notes) for voice in score.voices)
        polyphony_hint = score.metadata.get("polyphony_hint", 0)
        polyphony_hint = max(polyphony_hint, voice_count)
        if polyphony_hint < 3 and note_count >= 8 and score.tempo_bpm >= 95:
            polyphony_hint = 3

        # Check for dance forms based on tempo and rhythm
        rhythmic_patterns = self.detect_rhythmic_patterns(score)

        if "dance_rhythm" in rhythmic_patterns and polyphony_hint <= 2:
            if 80 <= score.tempo_bpm <= 110:
                return MusicalForm.PAVANE  # Slow duple meter dance
            elif 120 <= score.tempo_bpm <= 140:
                return MusicalForm.GALLIARD  # Fast triple meter dance
            elif 60 <= score.tempo_bpm <= 80:
                return MusicalForm.BASSE_DANSE  # Very slow processional dance

        # Check for isorhythmic structure
        if self._detect_isorhythmic_structure(score):
            return MusicalForm.ISORHYTHMIC

        # Check for chanson characteristics (3 voices, moderate length)
        if (polyphony_hint in (3, 4)) and (6 <= duration <= 180):
            return MusicalForm.CHANSON

        # Check for madrigal characteristics (4-6 voices, text painting)
        if voice_count >= 4 and duration > 60:
            return MusicalForm.MADRIGAL

        # Check for motet characteristics (sacred, multiple texts)
        if voice_count >= 3 and score.mode in (
            RenaissanceMode.DORIAN, RenaissanceMode.PHRYGIAN
        ):
            return MusicalForm.MOTET

        # Default to fantasia if no clear form detected
        if voice_count >= 3:
            return MusicalForm.FANTASIA

        return None

    def _pitch_to_class(self, pitch: float) -> int:
        """Convert a pitch to its pitch class (0-11)."""
        if pitch in self._pitch_class_cache:
            return self._pitch_class_cache[pitch]

        # A4 = 440 Hz is pitch class 9
        a4 = 440.0
        semitones_from_a4 = 12 * math.log2(pitch / a4)
        pitch_class = int(round(semitones_from_a4)) % 12

        self._pitch_class_cache[pitch] = pitch_class
        return pitch_class

    def _compare_pitches(self, pitch1: float, pitch2: float) -> float:
        """Compare two pitches and return similarity score (0-1)."""
        if pitch1 <= 0 or pitch2 <= 0:
            return 0.0

        semitone_diff = abs(12 * math.log2(pitch1 / pitch2))
        octave_diff = abs(semitone_diff - round(semitone_diff / 12) * 12)

        # Return 1.0 if within a semitone, decreasing linearly
        return max(0.0, 1.0 - octave_diff)

    def _compare_ranges(self, range1: Tuple[float, float],
                       range2: Tuple[float, float]) -> float:
        """Compare two pitch ranges and return similarity score (0-1)."""
        center1 = math.sqrt(range1[0] * range1[1])
        center2 = math.sqrt(range2[0] * range2[1])

        center_match = self._compare_pitches(center1, center2)

        width1 = math.log2(range1[1] / range1[0])
        width2 = math.log2(range2[1] / range2[0])

        width_match = 1.0 - min(1.0, abs(width1 - width2) / 3.0)

        return (center_match + width_match) / 2.0

    def _analyze_interval_patterns(self, pitches: List[float],
                                 characteristic_intervals: List[int]) -> float:
        """Analyze interval patterns against characteristic intervals."""
        if len(pitches) < 2:
            return 0.0

        # Extract intervals from the pitches
        intervals = []
        for i in range(1, len(pitches)):
            semitones = 12 * math.log2(pitches[i] / pitches[i-1])
            intervals.append(round(semitones))

        # Count interval occurrences
        interval_counter = Counter(intervals)
        total_intervals = len(intervals)

        # Compare with characteristic intervals
        matches = 0
        for interval in characteristic_intervals:
            matches += interval_counter.get(interval, 0)

        return matches / total_intervals if total_intervals > 0 else 0.0

    def _detect_dance_rhythm(self, normalized_durations: List[float]) -> bool:
        """Detect if the rhythm suggests a dance form."""
        if len(normalized_durations) < 4:
            return False

        # Look for regular patterns suggesting dance
        # Common dance patterns: 1-1-1-1 (four equal beats)
        # or 1-1-2 (two short, one long)

        # Check for regular pulse
        unique_values = len(set(normalized_durations[:8]))
        if unique_values <= 2:
            return True

        # Check for characteristic dance rhythms
        for i in range(len(normalized_durations) - 2):
            pattern = normalized_durations[i:i+3]
            if pattern == [1.0, 1.0, 2.0] or pattern == [2.0, 1.0, 1.0]:
                return True

        return False

    def _extract_melodic_patterns(self, notes: List[Note], voice_idx: int,
                                mode: Optional[RenaissanceMode]) -> List[MusicalPattern]:
        """Extract melodic patterns from a sequence of notes."""
        patterns = []

        # Look for cadential patterns
        for i in range(len(notes) - 3):
            segment = notes[i:i+4]
            if self._is_cadential_pattern(segment, mode):
                pattern = MusicalPattern(
                    name=f"cadence_{voice_idx}_{i}",
                    pattern_type="cadence",
                    mode=mode or RenaissanceMode.DORIAN,
                    notes=segment,
                    voice_leading=[],
                    rhythm_profile=[note.duration for note in segment],
                    context_tags=["cadence", f"voice_{voice_idx}"]
                )
                patterns.append(pattern)

        # Look for ornamental patterns
        for i in range(len(notes) - 2):
            segment = notes[i:i+3]
            if self._is_ornamental_pattern(segment):
                pattern = MusicalPattern(
                    name=f"ornament_{voice_idx}_{i}",
                    pattern_type="ornament",
                    mode=mode or RenaissanceMode.DORIAN,
                    notes=segment,
                    voice_leading=[],
                    rhythm_profile=[note.duration for note in segment],
                    context_tags=["ornament", f"voice_{voice_idx}"]
                )
                patterns.append(pattern)

        return patterns

    def _is_cadential_pattern(self, notes: List[Note],
                            mode: Optional[RenaissanceMode]) -> bool:
        """Check if a sequence of notes forms a cadential pattern."""
        if len(notes) < 3:
            return False

        # Get the final two pitches
        if notes[-1].is_rest or notes[-2].is_rest:
            return False

        penultimate = notes[-2].pitch
        ultimate = notes[-1].pitch

        # Check for stepwise motion in final interval
        semitone_diff = abs(12 * math.log2(penultimate / ultimate))

        # Cadences typically end with stepwise motion
        return semitone_diff <= 2.0

    def _is_ornamental_pattern(self, notes: List[Note]) -> bool:
        """Check if a sequence of notes forms an ornamental pattern."""
        if len(notes) < 3:
            return False

        # Check for rapid notes with small intervals
        durations = [note.duration for note in notes if not note.is_rest]
        if len(durations) < 3:
            return False

        # All notes should be relatively short
        avg_duration = sum(durations) / len(durations)
        if avg_duration > 0.3:  # Longer than 300ms is not ornamental
            return False

        # Check for small intervals between consecutive notes
        for i in range(1, len(notes)):
            if notes[i].is_rest or notes[i-1].is_rest:
                continue

            semitone_diff = abs(12 * math.log2(notes[i].pitch / notes[i-1].pitch))
            if semitone_diff > 4:  # More than a major third
                return False

        return True

    def _detect_isorhythmic_structure(self, score: MusicalScore) -> bool:
        """Detect if the score has an isorhythmic structure."""
        if not score.voices or len(score.voices) < 2:
            return False

        # Look for repeating rhythmic patterns across voices
        # This is a simplified detection - real isorhythm analysis is more complex

        # Extract rhythmic patterns from each voice
        voice_patterns = []
        for voice in score.voices:
            durations = [note.duration for note in voice.notes if not note.is_rest]
            if len(durations) >= 6:  # Need enough notes for pattern detection
                voice_patterns.append(durations)

        if len(voice_patterns) < 2:
            return False

        # Check for repeating patterns within each voice
        return any(self._has_repeating_pattern(pattern) for pattern in voice_patterns)

    def _has_repeating_pattern(self, sequence: List[float]) -> bool:
        """Check if a sequence has a repeating pattern."""
        if len(sequence) < 6:
            return False

        # Try different pattern lengths
        for pattern_len in range(2, len(sequence) // 2 + 1):
            pattern = sequence[:pattern_len]
            repetitions = len(sequence) // pattern_len

            if repetitions < 2:
                continue

            # Check if the pattern repeats
            is_repeating = True
            for i in range(1, repetitions):
                start = i * pattern_len
                end = start + pattern_len
                if end > len(sequence):
                    break

                segment = sequence[start:end]
                if not self._sequences_similar(pattern, segment):
                    is_repeating = False
                    break

            if is_repeating:
                return True

        return False

    def _sequences_similar(self, seq1: List[float], seq2: List[float]) -> bool:
        """Check if two sequences are similar within tolerance."""
        if len(seq1) != len(seq2):
            return False

        tolerance = 0.1  # 10% tolerance
        return all(abs(a - b) <= tolerance * max(a, b) for a, b in zip(seq1, seq2))
