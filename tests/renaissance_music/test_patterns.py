"""Tests for Renaissance music pattern library."""


from src.davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalPattern,
    Note,
    RenaissanceMode,
)
from src.davinci_codex.renaissance_music.patterns import RenaissancePatternLibrary


class TestRenaissancePatternLibrary:
    """Test the RenaissancePatternLibrary class."""

    def test_library_creation(self) -> None:
        """Test creating a pattern library."""
        library = RenaissancePatternLibrary()
        assert library is not None
        assert len(library._patterns) > 0
        assert "basse_danse" in library._patterns
        assert "pavane" in library._patterns
        assert "galliard" in library._patterns
        assert "cadence" in library._patterns
        assert "ornament" in library._patterns
        assert "isorhythmic" in library._patterns

    def test_query_patterns_by_mode(self) -> None:
        """Test querying patterns by mode."""
        library = RenaissancePatternLibrary()

        # Query for Dorian mode patterns
        dorian_patterns = library.query_patterns_by_mode(RenaissanceMode.DORIAN)
        assert len(dorian_patterns) > 0
        assert all(pattern.mode == RenaissanceMode.DORIAN for pattern in dorian_patterns)

        # Query for Phrygian mode patterns
        phrygian_patterns = library.query_patterns_by_mode(RenaissanceMode.PHRYGIAN)
        assert len(phrygian_patterns) > 0
        assert all(pattern.mode == RenaissanceMode.PHRYGIAN for pattern in phrygian_patterns)

    def test_query_patterns_by_form(self) -> None:
        """Test querying patterns by musical form."""
        library = RenaissancePatternLibrary()

        # Query for Basse Danse patterns
        basse_danse_patterns = library.query_patterns_by_form(MusicalForm.BASSE_DANSE)
        assert len(basse_danse_patterns) > 0
        assert all(pattern.pattern_type == "basse_danse" for pattern in basse_danse_patterns)

        # Query for Pavane patterns
        pavane_patterns = library.query_patterns_by_form(MusicalForm.PAVANE)
        assert len(pavane_patterns) > 0
        assert all(pattern.pattern_type == "pavane" for pattern in pavane_patterns)

        # Query for Galliard patterns
        galliard_patterns = library.query_patterns_by_form(MusicalForm.GALLIARD)
        assert len(galliard_patterns) > 0
        assert all(pattern.pattern_type == "galliard" for pattern in galliard_patterns)

        # Query for Chanson patterns
        chanson_patterns = library.query_patterns_by_form(MusicalForm.CHANSON)
        assert len(chanson_patterns) > 0
        assert all(pattern.pattern_type in ["cadence", "ornament"] for pattern in chanson_patterns)

    def test_query_patterns_by_instrument(self) -> None:
        """Test querying patterns by instrument type."""
        library = RenaissancePatternLibrary()

        # Query for Mechanical Drum patterns
        drum_patterns = library.query_patterns_by_instrument(InstrumentType.MECHANICAL_DRUM)
        assert len(drum_patterns) > 0
        # Drum should get simple patterns
        assert all(pattern.pattern_type in ["basse_danse", "pavane", "galliard", "dance_figure"]
                  for pattern in drum_patterns)

        # Query for Mechanical Organ patterns
        organ_patterns = library.query_patterns_by_instrument(InstrumentType.MECHANICAL_ORGAN)
        assert len(organ_patterns) > 0
        # Organ should get more complex patterns
        assert any(pattern.pattern_type == "isorhythmic" for pattern in organ_patterns)

        # Query for Programmable Flute patterns
        flute_patterns = library.query_patterns_by_instrument(InstrumentType.PROGRAMMABLE_FLUTE)
        assert len(flute_patterns) > 0
        # Flute should get ornamental patterns
        assert any(pattern.pattern_type == "ornament" for pattern in flute_patterns)

    def test_query_patterns_by_tags(self) -> None:
        """Test querying patterns by context tags."""
        library = RenaissancePatternLibrary()

        # Query for patterns with "standard" tag
        standard_patterns = library.query_patterns_by_tags(["standard"])
        assert len(standard_patterns) > 0
        assert all("standard" in pattern.context_tags for pattern in standard_patterns)

        # Query for patterns with multiple tags
        multi_tag_patterns = library.query_patterns_by_tags(["cadence", "strong"])
        assert len(multi_tag_patterns) > 0
        assert all("cadence" in pattern.context_tags and "strong" in pattern.context_tags
                  for pattern in multi_tag_patterns)

    def test_add_pattern(self) -> None:
        """Test adding a custom pattern."""
        library = RenaissancePatternLibrary()

        # Create a custom pattern
        notes = [
            Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=0.0),
            Note(pitch=493.88, duration=1.0, velocity=0.7, start_time=1.0),
        ]

        custom_pattern = MusicalPattern(
            name="custom_test_pattern",
            pattern_type="custom",
            mode=RenaissanceMode.DORIAN,
            notes=notes,
            voice_leading=[(440.0, 493.88)],
            rhythm_profile=[1.0, 1.0],
            context_tags=["test", "custom"]
        )

        # Add the pattern
        library.add_pattern(custom_pattern)

        # Verify it was added
        custom_patterns = library.query_patterns_by_tags(["test"])
        assert len(custom_patterns) == 1
        assert custom_patterns[0].name == "custom_test_pattern"

    def test_get_all_patterns(self) -> None:
        """Test getting all patterns."""
        library = RenaissancePatternLibrary()

        all_patterns = library.get_all_patterns()
        assert len(all_patterns) > 0

        # Check that we have patterns from different types
        pattern_types = {pattern.pattern_type for pattern in all_patterns}
        assert "basse_danse" in pattern_types
        assert "pavane" in pattern_types
        assert "galliard" in pattern_types
        assert "cadence" in pattern_types
        assert "ornament" in pattern_types
        assert "isorhythmic" in pattern_types

    def test_adapt_pattern_to_mode(self) -> None:
        """Test adapting a pattern to a different mode."""
        library = RenaissancePatternLibrary()

        # Get a Dorian pattern
        dorian_patterns = library.query_patterns_by_mode(RenaissanceMode.DORIAN)
        original_pattern = dorian_patterns[0]

        # Adapt to Lydian mode
        adapted_pattern = library.adapt_pattern_to_mode(original_pattern, RenaissanceMode.LYDIAN)

        # Verify the adaptation
        assert adapted_pattern.mode == RenaissanceMode.LYDIAN
        assert adapted_pattern.name.endswith("_adapted_to_lydian")
        assert adapted_pattern.pattern_type == original_pattern.pattern_type
        assert adapted_pattern.rhythm_profile == original_pattern.rhythm_profile
        assert "adapted" in adapted_pattern.context_tags

        # Check that pitches were transposed
        original_pitches = [note.pitch for note in original_pattern.notes]
        adapted_pitches = [note.pitch for note in adapted_pattern.notes]

        # All pitches should be different (transposed)
        for orig, adapted in zip(original_pitches, adapted_pitches):
            assert orig != adapted

    def test_basse_danse_patterns(self) -> None:
        """Test Basse Danse patterns."""
        library = RenaissancePatternLibrary()

        basse_danse_patterns = library._patterns["basse_danse"]
        assert len(basse_danse_patterns) >= 2  # At least bass and tenor

        # Check bass pattern
        bass_pattern = next(p for p in basse_danse_patterns if "bass" in p.name)
        assert bass_pattern.pattern_type == "basse_danse"
        assert bass_pattern.mode == RenaissanceMode.DORIAN
        assert len(bass_pattern.notes) == 8
        assert "basse_danse" in bass_pattern.context_tags
        assert "Arbeau's Orchésographie" in bass_pattern.source_reference

        # Check tenor pattern
        tenor_pattern = next(p for p in basse_danse_patterns if "tenor" in p.name)
        assert tenor_pattern.pattern_type == "basse_danse"
        assert tenor_pattern.mode == RenaissanceMode.DORIAN
        assert len(tenor_pattern.notes) == 8
        assert "basse_danse" in tenor_pattern.context_tags

    def test_pavane_patterns(self) -> None:
        """Test Pavane patterns."""
        library = RenaissancePatternLibrary()

        pavane_patterns = library._patterns["pavane"]
        assert len(pavane_patterns) >= 1

        pavane_pattern = pavane_patterns[0]
        assert pavane_pattern.pattern_type == "pavane"
        assert pavane_pattern.mode == RenaissanceMode.LYDIAN
        assert "pavane" in pavane_pattern.context_tags
        assert "Arbeau" in pavane_pattern.source_reference and "Orchésographie" in pavane_pattern.source_reference

    def test_galliard_patterns(self) -> None:
        """Test Galliard patterns."""
        library = RenaissancePatternLibrary()

        galliard_patterns = library._patterns["galliard"]
        assert len(galliard_patterns) >= 1

        galliard_pattern = galliard_patterns[0]
        assert galliard_pattern.pattern_type == "galliard"
        assert galliard_pattern.mode == RenaissanceMode.MIXOLYDIAN
        assert "galliard" in galliard_pattern.context_tags
        assert "Arbeau" in galliard_pattern.source_reference and "Orchésographie" in galliard_pattern.source_reference

    def test_cadential_patterns(self) -> None:
        """Test cadential patterns."""
        library = RenaissancePatternLibrary()

        cadential_patterns = library._patterns["cadence"]
        assert len(cadential_patterns) >= 3  # At least authentic, plagal, and Phrygian

        # Check authentic cadence
        authentic_cadence = next(p for p in cadential_patterns if p.name == "authentic_cadence")
        assert authentic_cadence.pattern_type == "cadence"
        assert authentic_cadence.mode == RenaissanceMode.MIXOLYDIAN
        assert "cadence" in authentic_cadence.context_tags
        assert "authentic" in authentic_cadence.context_tags

        # Check plagal cadence
        plagal_cadence = next(p for p in cadential_patterns if p.name == "plagal_cadence")
        assert plagal_cadence.pattern_type == "cadence"
        assert "amen" in plagal_cadence.context_tags

        # Check Phrygian cadence
        phrygian_cadence = next(p for p in cadential_patterns if p.name == "phrygian_cadence")
        assert phrygian_cadence.mode == RenaissanceMode.PHRYGIAN
        assert "characteristic" in phrygian_cadence.context_tags

    def test_ornamental_patterns(self) -> None:
        """Test ornamental patterns."""
        library = RenaissancePatternLibrary()

        ornamental_patterns = library._patterns["ornament"]
        assert len(ornamental_patterns) >= 3  # At least trill, turn, and passaggi

        # Check trill
        trill_pattern = next(p for p in ornamental_patterns if "trill" in p.name)
        assert trill_pattern.pattern_type == "ornament"
        assert "trill" in trill_pattern.context_tags

        # Check turn
        turn_pattern = next(p for p in ornamental_patterns if "turn" in p.name)
        assert turn_pattern.pattern_type == "ornament"
        assert "turn" in turn_pattern.context_tags

        # Check passaggi
        passaggi_pattern = next(p for p in ornamental_patterns if "passaggi" in p.name)
        assert passaggi_pattern.pattern_type == "ornament"
        assert "passaggi" in passaggi_pattern.context_tags
        assert "rising" in passaggi_pattern.context_tags

    def test_isorhythmic_patterns(self) -> None:
        """Test isorhythmic patterns."""
        library = RenaissancePatternLibrary()

        isorhythmic_patterns = library._patterns["isorhythmic"]
        assert len(isorhythmic_patterns) >= 1

        isorhythmic_pattern = isorhythmic_patterns[0]
        assert isorhythmic_pattern.pattern_type == "isorhythmic"
        assert isorhythmic_pattern.mode == RenaissanceMode.DORIAN
        assert "isorhythmic" in isorhythmic_pattern.context_tags
        assert "talea" in isorhythmic_pattern.context_tags
        assert "color" in isorhythmic_pattern.context_tags
        assert "Medieval isorhythmic technique" in isorhythmic_pattern.source_reference
