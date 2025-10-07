"""Pattern library containing Renaissance musical patterns and motifs."""

from __future__ import annotations

from typing import Dict, List

from .models import (
    InstrumentType,
    MusicalForm,
    MusicalPattern,
    Note,
    RenaissanceMode,
)


class RenaissancePatternLibrary:
    """Library of Renaissance musical patterns and motifs."""

    def __init__(self) -> None:
        """Initialize the pattern library."""
        self._patterns: Dict[str, List[MusicalPattern]] = {}
        self._initialize_patterns()

    def _initialize_patterns(self) -> None:
        """Initialize the pattern library with pre-defined patterns."""
        self._initialize_dance_patterns()
        self._initialize_cadential_patterns()
        self._initialize_ornamental_patterns()
        self._initialize_isorhythmic_patterns()

    def _initialize_dance_patterns(self) -> None:
        """Initialize pre-defined dance patterns."""
        # Basse Danse patterns (slow, stately duple meter)
        basse_danse_patterns = self._create_basse_danse_patterns()
        self._patterns["basse_danse"] = basse_danse_patterns

        # Pavane patterns (slow processional duple meter)
        pavane_patterns = self._create_pavane_patterns()
        self._patterns["pavane"] = pavane_patterns

        # Galliard patterns (fast triple meter dance)
        galliard_patterns = self._create_galliard_patterns()
        self._patterns["galliard"] = galliard_patterns

    def _initialize_cadential_patterns(self) -> None:
        """Initialize common Renaissance cadential formulas."""
        cadential_patterns = self._create_cadential_patterns()
        self._patterns["cadence"] = cadential_patterns

    def _initialize_ornamental_patterns(self) -> None:
        """Initialize typical melodic ornaments and diminutions."""
        ornamental_patterns = self._create_ornamental_patterns()
        self._patterns["ornament"] = ornamental_patterns

    def _initialize_isorhythmic_patterns(self) -> None:
        """Initialize isorhythmic templates."""
        isorhythmic_patterns = self._create_isorhythmic_patterns()
        self._patterns["isorhythmic"] = isorhythmic_patterns

    def _create_basse_danse_patterns(self) -> List[MusicalPattern]:
        """Create Basse Danse patterns."""
        patterns = []

        # Standard Basse Danse bass line pattern
        bass_notes = [
            Note(pitch=196.00, duration=2.0, velocity=0.7, start_time=0.0),  # G3
            Note(pitch=220.00, duration=1.0, velocity=0.7, start_time=2.0),  # A3
            Note(pitch=246.94, duration=1.0, velocity=0.7, start_time=3.0),  # B3
            Note(pitch=261.63, duration=2.0, velocity=0.7, start_time=4.0),  # C4
            Note(pitch=293.66, duration=2.0, velocity=0.7, start_time=6.0),  # D4
            Note(pitch=329.63, duration=2.0, velocity=0.7, start_time=8.0),  # E4
            Note(pitch=392.00, duration=2.0, velocity=0.7, start_time=10.0), # G4
            Note(pitch=261.63, duration=2.0, velocity=0.7, start_time=12.0), # C4
        ]

        pattern = MusicalPattern(
            name="basse_danse_bass_standard",
            pattern_type="basse_danse",
            mode=RenaissanceMode.DORIAN,
            notes=bass_notes,
            voice_leading=[(196.00, 220.00), (220.00, 246.94), (246.94, 261.63),
                          (261.63, 293.66), (293.66, 329.63), (329.63, 392.00),
                          (392.00, 261.63)],
            rhythm_profile=[2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0],
            context_tags=["basse_danse", "bass_line", "standard"],
            source_reference="Arbeau's Orchésographie (1588)"
        )
        patterns.append(pattern)

        # Basse Danse tenor pattern
        tenor_notes = [
            Note(pitch=392.00, duration=1.0, velocity=0.6, start_time=0.0),  # G4
            Note(pitch=440.00, duration=1.0, velocity=0.6, start_time=1.0),  # A4
            Note(pitch=392.00, duration=1.0, velocity=0.6, start_time=2.0),  # G4
            Note(pitch=349.23, duration=1.0, velocity=0.6, start_time=3.0),  # F4
            Note(pitch=392.00, duration=2.0, velocity=0.6, start_time=4.0),  # G4
            Note(pitch=493.88, duration=2.0, velocity=0.6, start_time=6.0),  # B4
            Note(pitch=523.25, duration=2.0, velocity=0.6, start_time=8.0),  # C5
            Note(pitch=392.00, duration=2.0, velocity=0.6, start_time=10.0), # G4
        ]

        pattern = MusicalPattern(
            name="basse_danse_tenor_standard",
            pattern_type="basse_danse",
            mode=RenaissanceMode.DORIAN,
            notes=tenor_notes,
            voice_leading=[(392.00, 440.00), (440.00, 392.00), (392.00, 349.23),
                          (349.23, 392.00), (392.00, 493.88), (493.88, 523.25),
                          (523.25, 392.00)],
            rhythm_profile=[1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0],
            context_tags=["basse_danse", "tenor", "standard"],
            source_reference="Arbeau's Orchésographie (1588)"
        )
        patterns.append(pattern)

        return patterns

    def _create_pavane_patterns(self) -> List[MusicalPattern]:
        """Create Pavane patterns."""
        patterns = []

        # Standard Pavane rhythm pattern (duple meter, stately)
        pavane_rhythm = [1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 1.0]

        # Create a melodic pattern with this rhythm
        base_pitch = 329.63  # E4
        melody_notes = []
        current_time = 0.0

        for i, duration in enumerate(pavane_rhythm):
            # Simple stepwise motion with occasional leaps
            if i % 4 == 0:
                pitch = base_pitch
            elif i % 4 == 1:
                pitch = base_pitch * 1.125  # Major second up
            elif i % 4 == 2:
                pitch = base_pitch * 1.25   # Major third up
            else:
                pitch = base_pitch * 1.5    # Perfect fifth up

            melody_notes.append(
                Note(pitch=pitch, duration=duration, velocity=0.6,
                     start_time=current_time)
            )
            current_time += duration

        pattern = MusicalPattern(
            name="pavane_melody_standard",
            pattern_type="pavane",
            mode=RenaissanceMode.LYDIAN,
            notes=melody_notes,
            voice_leading=[(note.pitch, melody_notes[i+1].pitch)
                          for i, note in enumerate(melody_notes[:-1])],
            rhythm_profile=pavane_rhythm,
            context_tags=["pavane", "melody", "standard"],
            source_reference="Thoinot Arbeau, Orchésographie (1588)"
        )
        patterns.append(pattern)

        return patterns

    def _create_galliard_patterns(self) -> List[MusicalPattern]:
        """Create Galliard patterns."""
        patterns = []

        # Galliard rhythm (triple meter with characteristic hop)
        galliard_rhythm = [0.5, 0.5, 1.0, 0.5, 0.5, 1.0]

        # Create a melodic pattern with this rhythm
        base_pitch = 440.00  # A4
        melody_notes = []
        current_time = 0.0

        for i, duration in enumerate(galliard_rhythm):
            # More active melody for the faster dance
            if i % 3 == 0:
                pitch = base_pitch
            elif i % 3 == 1:
                pitch = base_pitch * 1.125  # Major second up
            else:
                pitch = base_pitch * 0.875  # Major second down

            melody_notes.append(
                Note(pitch=pitch, duration=duration, velocity=0.7,
                     start_time=current_time)
            )
            current_time += duration

        pattern = MusicalPattern(
            name="galliard_melody_standard",
            pattern_type="galliard",
            mode=RenaissanceMode.MIXOLYDIAN,
            notes=melody_notes,
            voice_leading=[(note.pitch, melody_notes[i+1].pitch)
                          for i, note in enumerate(melody_notes[:-1])],
            rhythm_profile=galliard_rhythm,
            context_tags=["galliard", "melody", "standard"],
            source_reference="Thoinot Arbeau, Orchésographie (1588)"
        )
        patterns.append(pattern)

        return patterns

    def _create_cadential_patterns(self) -> List[MusicalPattern]:
        """Create common Renaissance cadential formulas."""
        patterns = []

        # Authentic cadence (V-I)
        authentic_cadence = [
            Note(pitch=392.00, duration=0.5, velocity=0.6, start_time=0.0),  # G4
            Note(pitch=493.88, duration=0.5, velocity=0.6, start_time=0.5),  # B4
            Note(pitch=587.33, duration=0.5, velocity=0.6, start_time=1.0),  # D5
            Note(pitch=659.25, duration=0.5, velocity=0.6, start_time=1.5),  # E5 (leading tone)
            Note(pitch=392.00, duration=1.0, velocity=0.7, start_time=2.0),  # G4 (tonic)
        ]

        pattern = MusicalPattern(
            name="authentic_cadence",
            pattern_type="cadence",
            mode=RenaissanceMode.MIXOLYDIAN,
            notes=authentic_cadence,
            voice_leading=[(392.00, 493.88), (493.88, 587.33), (587.33, 659.25), (659.25, 392.00)],
            rhythm_profile=[0.5, 0.5, 0.5, 0.5, 1.0],
            context_tags=["cadence", "authentic", "strong"],
            source_reference="Standard Renaissance cadential formula"
        )
        patterns.append(pattern)

        # Plagal cadence (IV-I)
        plagal_cadence = [
            Note(pitch=349.23, duration=0.5, velocity=0.6, start_time=0.0),  # F4
            Note(pitch=440.00, duration=0.5, velocity=0.6, start_time=0.5),  # A4
            Note(pitch=523.25, duration=0.5, velocity=0.6, start_time=1.0),  # C5
            Note(pitch=392.00, duration=1.0, velocity=0.7, start_time=1.5),  # G4 (tonic)
        ]

        pattern = MusicalPattern(
            name="plagal_cadence",
            pattern_type="cadence",
            mode=RenaissanceMode.MIXOLYDIAN,
            notes=plagal_cadence,
            voice_leading=[(349.23, 440.00), (440.00, 523.25), (523.25, 392.00)],
            rhythm_profile=[0.5, 0.5, 0.5, 1.0],
            context_tags=["cadence", "plagal", "amen"],
            source_reference="Standard Renaissance cadential formula"
        )
        patterns.append(pattern)

        # Phrygian cadence (characteristic half-step)
        phrygian_cadence = [
            Note(pitch=293.66, duration=0.5, velocity=0.6, start_time=0.0),  # D4
            Note(pitch=369.99, duration=0.5, velocity=0.6, start_time=0.5),  # F#4
            Note(pitch=440.00, duration=0.5, velocity=0.6, start_time=1.0),  # A4
            Note(pitch=277.18, duration=0.5, velocity=0.6, start_time=1.5),  # C#4 (half-step below D)
            Note(pitch=293.66, duration=1.0, velocity=0.7, start_time=2.0),  # D4 (tonic)
        ]

        pattern = MusicalPattern(
            name="phrygian_cadence",
            pattern_type="cadence",
            mode=RenaissanceMode.PHRYGIAN,
            notes=phrygian_cadence,
            voice_leading=[(293.66, 369.99), (369.99, 440.00), (440.00, 277.18), (277.18, 293.66)],
            rhythm_profile=[0.5, 0.5, 0.5, 0.5, 1.0],
            context_tags=["cadence", "phrygian", "characteristic"],
            source_reference="Characteristic Phrygian cadence"
        )
        patterns.append(pattern)

        return patterns

    def _create_ornamental_patterns(self) -> List[MusicalPattern]:
        """Create typical melodic ornaments and diminutions."""
        patterns = []

        # Trill ornament
        trill_notes = [
            Note(pitch=440.00, duration=0.1, velocity=0.5, start_time=0.0),  # A4
            Note(pitch=466.16, duration=0.1, velocity=0.5, start_time=0.1),  # A#4
            Note(pitch=440.00, duration=0.1, velocity=0.5, start_time=0.2),  # A4
            Note(pitch=466.16, duration=0.1, velocity=0.5, start_time=0.3),  # A#4
            Note(pitch=440.00, duration=0.4, velocity=0.6, start_time=0.4),  # A4
        ]

        pattern = MusicalPattern(
            name="trill_standard",
            pattern_type="ornament",
            mode=RenaissanceMode.DORIAN,
            notes=trill_notes,
            voice_leading=[(440.00, 466.16), (466.16, 440.00), (440.00, 466.16), (466.16, 440.00)],
            rhythm_profile=[0.1, 0.1, 0.1, 0.1, 0.4],
            context_tags=["ornament", "trill", "standard"],
            source_reference="Standard Renaissance trill"
        )
        patterns.append(pattern)

        # Turn ornament
        turn_notes = [
            Note(pitch=440.00, duration=0.2, velocity=0.5, start_time=0.0),  # A4
            Note(pitch=493.88, duration=0.1, velocity=0.5, start_time=0.2),  # B4
            Note(pitch=440.00, duration=0.1, velocity=0.5, start_time=0.3),  # A4
            Note(pitch=392.00, duration=0.1, velocity=0.5, start_time=0.4),  # G4
            Note(pitch=440.00, duration=0.5, velocity=0.6, start_time=0.5),  # A4
        ]

        pattern = MusicalPattern(
            name="turn_standard",
            pattern_type="ornament",
            mode=RenaissanceMode.DORIAN,
            notes=turn_notes,
            voice_leading=[(440.00, 493.88), (493.88, 440.00), (440.00, 392.00), (392.00, 440.00)],
            rhythm_profile=[0.2, 0.1, 0.1, 0.1, 0.5],
            context_tags=["ornament", "turn", "standard"],
            source_reference="Standard Renaissance turn"
        )
        patterns.append(pattern)

        # Passaggi (diminution) pattern
        passaggi_notes = [
            Note(pitch=392.00, duration=0.3, velocity=0.5, start_time=0.0),  # G4
            Note(pitch=440.00, duration=0.1, velocity=0.5, start_time=0.3),  # A4
            Note(pitch=466.16, duration=0.1, velocity=0.5, start_time=0.4),  # A#4
            Note(pitch=493.88, duration=0.1, velocity=0.5, start_time=0.5),  # B4
            Note(pitch=523.25, duration=0.1, velocity=0.5, start_time=0.6),  # C5
            Note(pitch=587.33, duration=0.3, velocity=0.6, start_time=0.7),  # D5
        ]

        pattern = MusicalPattern(
            name="passaggi_rising",
            pattern_type="ornament",
            mode=RenaissanceMode.DORIAN,
            notes=passaggi_notes,
            voice_leading=[(392.00, 440.00), (440.00, 466.16), (466.16, 493.88),
                          (493.88, 523.25), (523.25, 587.33)],
            rhythm_profile=[0.3, 0.1, 0.1, 0.1, 0.1, 0.3],
            context_tags=["ornament", "passaggi", "rising"],
            source_reference="Renaissance diminution technique"
        )
        patterns.append(pattern)

        return patterns

    def _create_isorhythmic_patterns(self) -> List[MusicalPattern]:
        """Create isorhythmic templates."""
        patterns = []

        # Talea (rhythmic pattern)
        talea = [1.0, 0.5, 0.5, 1.0, 0.5, 0.5]

        # Color (melodic pattern)
        color_pitches = [392.00, 440.00, 493.88, 523.25, 493.88, 440.00]

        # Create isorhythmic pattern
        current_time = 0.0
        isorhythmic_notes = []

        for i, duration in enumerate(talea):
            pitch = color_pitches[i % len(color_pitches)]
            isorhythmic_notes.append(
                Note(pitch=pitch, duration=duration, velocity=0.6,
                     start_time=current_time)
            )
            current_time += duration

        pattern = MusicalPattern(
            name="isorhythmic_standard",
            pattern_type="isorhythmic",
            mode=RenaissanceMode.DORIAN,
            notes=isorhythmic_notes,
            voice_leading=[(isorhythmic_notes[i].pitch, isorhythmic_notes[i+1].pitch)
                          for i in range(len(isorhythmic_notes)-1)],
            rhythm_profile=talea,
            context_tags=["isorhythmic", "talea", "color"],
            source_reference="Medieval isorhythmic technique"
        )
        patterns.append(pattern)

        return patterns

    def query_patterns_by_mode(self, mode: RenaissanceMode) -> List[MusicalPattern]:
        """Query patterns by mode.

        Args:
            mode: The Renaissance mode to filter by

        Returns:
            List of patterns in the specified mode
        """
        matching_patterns = []

        for pattern_list in self._patterns.values():
            for pattern in pattern_list:
                if pattern.mode == mode:
                    matching_patterns.append(pattern)

        return matching_patterns

    def query_patterns_by_form(self, form: MusicalForm) -> List[MusicalPattern]:
        """Query patterns by musical form.

        Args:
            form: The musical form to filter by

        Returns:
            List of patterns suitable for the specified form
        """
        matching_patterns = []

        # Map form to pattern types
        form_pattern_types = {
            MusicalForm.BASSE_DANSE: ["basse_danse"],
            MusicalForm.PAVANE: ["pavane"],
            MusicalForm.GALLIARD: ["galliard"],
            MusicalForm.CHANSON: ["cadence", "ornament"],
            MusicalForm.MADRIGAL: ["cadence", "ornament"],
            MusicalForm.MOTET: ["cadence"],
            MusicalForm.ISORHYTHMIC: ["isorhythmic"],
            MusicalForm.FANTASIA: ["ornament", "cadence"],
        }

        pattern_types = form_pattern_types.get(form, [])

        for pattern_type in pattern_types:
            if pattern_type in self._patterns:
                matching_patterns.extend(self._patterns[pattern_type])

        return matching_patterns

    def query_patterns_by_instrument(self, instrument: InstrumentType) -> List[MusicalPattern]:
        """Query patterns suitable for a specific instrument.

        Args:
            instrument: The instrument type to filter by

        Returns:
            List of patterns suitable for the specified instrument
        """
        matching_patterns = []

        # Define instrument capabilities
        instrument_capabilities = {
            InstrumentType.MECHANICAL_DRUM: {
                "suitable_patterns": ["basse_danse", "pavane", "galliard"],
                "max_complexity": "low"
            },
            InstrumentType.MECHANICAL_ORGAN: {
                "suitable_patterns": ["basse_danse", "pavane", "galliard", "cadence", "isorhythmic"],
                "max_complexity": "high"
            },
            InstrumentType.VIOLA_ORGANISTA: {
                "suitable_patterns": ["pavane", "cadence", "ornament"],
                "max_complexity": "medium"
            },
            InstrumentType.PROGRAMMABLE_FLUTE: {
                "suitable_patterns": ["galliard", "ornament", "cadence"],
                "max_complexity": "high"
            },
            InstrumentType.MECHANICAL_CARILLON: {
                "suitable_patterns": ["basse_danse", "pavane", "isorhythmic"],
                "max_complexity": "low"
            },
            InstrumentType.MECHANICAL_TRUMPETER: {
                "suitable_patterns": ["galliard", "cadence"],
                "max_complexity": "medium"
            },
        }

        capabilities = instrument_capabilities.get(instrument, {})
        suitable_pattern_types = capabilities.get("suitable_patterns", [])

        for pattern_type in suitable_pattern_types:
            if pattern_type in self._patterns:
                matching_patterns.extend(self._patterns[pattern_type])

        # Filter by complexity if specified
        max_complexity = capabilities.get("max_complexity")
        if max_complexity == "low":
            # Keep only simple patterns
            matching_patterns = [p for p in matching_patterns
                               if p.pattern_type in ["basse_danse", "pavane", "galliard", "cadence"]]
        elif max_complexity == "medium":
            # Exclude complex ornaments
            matching_patterns = [p for p in matching_patterns
                               if p.pattern_type != "ornament" or
                               "trill" in p.name or "turn" in p.name]

        return matching_patterns

    def query_patterns_by_tags(self, tags: List[str]) -> List[MusicalPattern]:
        """Query patterns by context tags.

        Args:
            tags: List of tags to filter by

        Returns:
            List of patterns matching all specified tags
        """
        matching_patterns = []

        for pattern_list in self._patterns.values():
            for pattern in pattern_list:
                if all(tag in pattern.context_tags for tag in tags):
                    matching_patterns.append(pattern)

        return matching_patterns

    def add_pattern(self, pattern: MusicalPattern) -> None:
        """Add a custom pattern to the library.

        Args:
            pattern: The pattern to add
        """
        pattern_type = pattern.pattern_type

        if pattern_type not in self._patterns:
            self._patterns[pattern_type] = []

        self._patterns[pattern_type].append(pattern)

    def get_all_patterns(self) -> List[MusicalPattern]:
        """Get all patterns in the library.

        Returns:
            List of all patterns
        """
        all_patterns = []

        for pattern_list in self._patterns.values():
            all_patterns.extend(pattern_list)

        return all_patterns

    def adapt_pattern_to_mode(self, pattern: MusicalPattern,
                            target_mode: RenaissanceMode) -> MusicalPattern:
        """Adapt a pattern to a different mode.

        Args:
            pattern: The pattern to adapt
            target_mode: The target mode

        Returns:
            A new pattern adapted to the target mode
        """
        # This is a simplified adaptation - in a full implementation,
        # this would involve more sophisticated modal transformation

        # Get the final of the target mode
        mode_finals = {
            RenaissanceMode.DORIAN: 261.63,    # D4
            RenaissanceMode.PHRYGIAN: 293.66,  # D4
            RenaissanceMode.LYDIAN: 329.63,    # E4
            RenaissanceMode.MIXOLYDIAN: 392.00, # G4
            RenaissanceMode.HYPODORIAN: 261.63, # D4
            RenaissanceMode.HYPOPHRYGIAN: 293.66, # D4
            RenaissanceMode.HYPOLYDIAN: 329.63, # E4
            RenaissanceMode.HYPOMIXOLYDIAN: 392.00, # G4
        }

        target_final = mode_finals.get(target_mode, 261.63)

        # Calculate transposition factor
        original_final = pattern.notes[0].pitch if pattern.notes else 440.0
        transposition_factor = target_final / original_final

        # Create adapted notes
        adapted_notes = []
        for note in pattern.notes:
            adapted_pitch = note.pitch * transposition_factor
            adapted_note = Note(
                pitch=adapted_pitch,
                duration=note.duration,
                velocity=note.velocity,
                start_time=note.start_time,
                voice=note.voice,
                is_rest=note.is_rest
            )
            adapted_notes.append(adapted_note)

        # Create adapted pattern
        adapted_pattern = MusicalPattern(
            name=f"{pattern.name}_adapted_to_{target_mode.value}",
            pattern_type=pattern.pattern_type,
            mode=target_mode,
            notes=adapted_notes,
            voice_leading=[(adapted_notes[i].pitch, adapted_notes[i+1].pitch)
                          for i in range(len(adapted_notes)-1)],
            rhythm_profile=pattern.rhythm_profile,
            context_tags=pattern.context_tags + ["adapted"],
            source_reference=f"Adapted from {pattern.source_reference}"
        )

        return adapted_pattern
