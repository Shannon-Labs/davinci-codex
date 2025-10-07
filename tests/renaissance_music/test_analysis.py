"""Tests for Renaissance music analysis module."""


from src.davinci_codex.renaissance_music.analysis import RenaissanceAnalyzer
from src.davinci_codex.renaissance_music.models import (
    MusicalForm,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


class TestRenaissanceAnalyzer:
    """Test the RenaissanceAnalyzer class."""

    def test_analyzer_creation(self) -> None:
        """Test creating a Renaissance analyzer."""
        analyzer = RenaissanceAnalyzer()
        assert analyzer is not None
        assert hasattr(analyzer, '_MODE_CHARACTERISTICS')
        assert hasattr(analyzer, '_CADENTIAL_PATTERNS')

    def test_analyze_mode_empty_score(self) -> None:
        """Test analyzing mode of empty score."""
        analyzer = RenaissanceAnalyzer()
        score = MusicalScore()

        mode = analyzer.analyze_mode(score)
        assert mode is None

    def test_analyze_mode_dorian(self) -> None:
        """Test analyzing Dorian mode."""
        analyzer = RenaissanceAnalyzer()

        # Create a score in Dorian mode (D is the final)
        voice = Voice()

        # Dorian scale: D-E-F-G-A-B-C-D
        dorian_pitches = [293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25, 587.33]

        for i, pitch in enumerate(dorian_pitches):
            note = Note(pitch=pitch, duration=1.0, velocity=0.7, start_time=float(i))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        mode = analyzer.analyze_mode(score)
        assert mode == RenaissanceMode.DORIAN

    def test_analyze_mode_phrygian(self) -> None:
        """Test analyzing Phrygian mode."""
        analyzer = RenaissanceAnalyzer()

        # Create a score in Phrygian mode (E is the final)
        voice = Voice()

        # Phrygian scale: E-F-G-A-B-C-D-E
        phrygian_pitches = [329.63, 349.23, 392.00, 440.00, 493.88, 523.25, 587.33, 659.25]

        for i, pitch in enumerate(phrygian_pitches):
            note = Note(pitch=pitch, duration=1.0, velocity=0.7, start_time=float(i))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        mode = analyzer.analyze_mode(score)
        assert mode == RenaissanceMode.PHRYGIAN

    def test_detect_rhythmic_patterns_empty(self) -> None:
        """Test detecting rhythmic patterns in empty score."""
        analyzer = RenaissanceAnalyzer()
        score = MusicalScore()

        patterns = analyzer.detect_rhythmic_patterns(score)
        assert patterns == {}

    def test_detect_rhythmic_patterns_perfect_tempus(self) -> None:
        """Test detecting perfect tempus (triple meter)."""
        analyzer = RenaissanceAnalyzer()

        voice = Voice()

        # Create a pattern with 1.5 duration notes (compound triple feel)
        for i in range(4):
            note = Note(pitch=440.0, duration=1.5, velocity=0.7, start_time=float(i * 1.5))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        patterns = analyzer.detect_rhythmic_patterns(score)
        assert "perfect_tempus" in patterns
        assert patterns["perfect_tempus"] > 0.5

    def test_detect_rhythmic_patterns_imperfect_tempus(self) -> None:
        """Test detecting imperfect tempus (duple meter)."""
        analyzer = RenaissanceAnalyzer()

        voice = Voice()

        # Create a pattern with 1.0 duration notes (simple duple feel)
        for i in range(4):
            note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=float(i))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        patterns = analyzer.detect_rhythmic_patterns(score)
        assert "imperfect_tempus" in patterns
        assert patterns["imperfect_tempus"] > 0.5

    def test_identify_melodic_patterns_empty(self) -> None:
        """Test identifying melodic patterns in empty score."""
        analyzer = RenaissanceAnalyzer()
        score = MusicalScore()

        patterns = analyzer.identify_melodic_patterns(score)
        assert patterns == []

    def test_identify_melodic_patterns_cadence(self) -> None:
        """Test identifying cadential patterns."""
        analyzer = RenaissanceAnalyzer()

        voice = Voice()

        # Create a simple cadential pattern
        notes = [
            Note(pitch=392.00, duration=0.5, velocity=0.7, start_time=0.0),  # G4
            Note(pitch=493.88, duration=0.5, velocity=0.7, start_time=0.5),  # B4
            Note(pitch=587.33, duration=0.5, velocity=0.7, start_time=1.0),  # D5
            Note(pitch=659.25, duration=0.5, velocity=0.7, start_time=1.5),  # E5
            Note(pitch=392.00, duration=1.0, velocity=0.7, start_time=2.0),  # G4
        ]

        for note in notes:
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        patterns = analyzer.identify_melodic_patterns(score)
        assert len(patterns) > 0
        assert any(pattern.pattern_type == "cadence" for pattern in patterns)

    def test_identify_melodic_patterns_ornament(self) -> None:
        """Test identifying ornamental patterns."""
        analyzer = RenaissanceAnalyzer()

        voice = Voice()

        # Create a simple ornamental pattern (rapid notes with small intervals)
        notes = [
            Note(pitch=440.00, duration=0.1, velocity=0.7, start_time=0.0),  # A4
            Note(pitch=466.16, duration=0.1, velocity=0.7, start_time=0.1),  # A#4
            Note(pitch=440.00, duration=0.1, velocity=0.7, start_time=0.2),  # A4
            Note(pitch=466.16, duration=0.1, velocity=0.7, start_time=0.3),  # A#4
            Note(pitch=440.00, duration=0.4, velocity=0.7, start_time=0.4),  # A4
        ]

        for note in notes:
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        patterns = analyzer.identify_melodic_patterns(score)
        assert len(patterns) > 0
        assert any(pattern.pattern_type == "ornament" for pattern in patterns)

    def test_extract_voice_leading_empty(self) -> None:
        """Test extracting voice leading from empty score."""
        analyzer = RenaissanceAnalyzer()
        score = MusicalScore()

        voice_leading = analyzer.extract_voice_leading(score)
        assert voice_leading == []

    def test_extract_voice_leading(self) -> None:
        """Test extracting voice leading."""
        analyzer = RenaissanceAnalyzer()

        voice = Voice()

        # Create a simple melodic line
        notes = [
            Note(pitch=440.00, duration=1.0, velocity=0.7, start_time=0.0),  # A4
            Note(pitch=493.88, duration=1.0, velocity=0.7, start_time=1.0),  # B4
            Note(pitch=523.25, duration=1.0, velocity=0.7, start_time=2.0),  # C5
            Note(pitch=587.33, duration=1.0, velocity=0.7, start_time=3.0),  # D5
        ]

        for note in notes:
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)

        voice_leading = analyzer.extract_voice_leading(score)
        assert len(voice_leading) == 1
        assert len(voice_leading[0]) == 3
        assert voice_leading[0][0] == (440.00, 493.88)
        assert voice_leading[0][1] == (493.88, 523.25)
        assert voice_leading[0][2] == (523.25, 587.33)

    def test_classify_musical_form_empty(self) -> None:
        """Test classifying musical form of empty score."""
        analyzer = RenaissanceAnalyzer()
        score = MusicalScore()

        form = analyzer.classify_musical_form(score)
        assert form is None

    def test_classify_musical_form_pavane(self) -> None:
        """Test classifying Pavane form."""
        analyzer = RenaissanceAnalyzer()

        voice = Voice()

        # Create a slow duple meter pattern suitable for Pavane
        for i in range(8):
            note = Note(pitch=440.0, duration=1.0, velocity=0.7, start_time=float(i))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)
        score.tempo_bpm = 90.0  # Slow tempo suitable for Pavane

        form = analyzer.classify_musical_form(score)
        assert form == MusicalForm.PAVANE

    def test_classify_musical_form_galliard(self) -> None:
        """Test classifying Galliard form."""
        analyzer = RenaissanceAnalyzer()

        voice = Voice()

        # Create a fast triple meter pattern suitable for Galliard
        for i in range(6):
            note = Note(pitch=440.0, duration=0.5, velocity=0.7, start_time=float(i * 0.5))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)
        score.tempo_bpm = 130.0  # Fast tempo suitable for Galliard

        form = analyzer.classify_musical_form(score)
        assert form == MusicalForm.GALLIARD

    def test_classify_musical_form_basse_danse(self) -> None:
        """Test classifying Basse Danse form."""
        analyzer = RenaissanceAnalyzer()

        voice = Voice()

        # Create a very slow pattern suitable for Basse Danse
        for i in range(4):
            note = Note(pitch=440.0, duration=2.0, velocity=0.7, start_time=float(i * 2.0))
            voice.add_note(note)

        score = MusicalScore()
        score.add_voice(voice)
        score.tempo_bpm = 70.0  # Very slow tempo suitable for Basse Danse

        form = analyzer.classify_musical_form(score)
        assert form == MusicalForm.BASSE_DANSE

    def test_classify_musical_form_chanson(self) -> None:
        """Test classifying Chanson form."""
        analyzer = RenaissanceAnalyzer()

        # Create a 3-voice texture
        for voice_idx in range(3):
            voice = Voice()

            for i in range(8):
                pitch = 440.0 * (1 + voice_idx * 0.1)  # Different pitch for each voice
                note = Note(pitch=pitch, duration=1.0, velocity=0.7, start_time=float(i))
                voice.add_note(note)

            score = MusicalScore()
            score.add_voice(voice)

        score.tempo_bpm = 100.0

        form = analyzer.classify_musical_form(score)
        assert form == MusicalForm.CHANSON

    def test_detect_isorhythmic_structure(self) -> None:
        """Test detecting isorhythmic structure."""
        analyzer = RenaissanceAnalyzer()

        # Create a score with repeating rhythmic pattern
        voice1 = Voice()

        # Create a repeating pattern: 1.0, 0.5, 0.5, 1.0
        pattern = [1.0, 0.5, 0.5, 1.0]

        for repeat in range(2):
            for i, duration in enumerate(pattern):
                pitch = 440.0 + i * 50.0
                start_time = repeat * sum(pattern) + sum(pattern[:i])
                note = Note(pitch=pitch, duration=duration, velocity=0.7, start_time=start_time)
                voice1.add_note(note)

        voice2 = Voice()

        # Second voice with different melody but same rhythm
        for repeat in range(2):
            for i, duration in enumerate(pattern):
                pitch = 330.0 + i * 40.0
                start_time = repeat * sum(pattern) + sum(pattern[:i])
                note = Note(pitch=pitch, duration=duration, velocity=0.7, start_time=start_time)
                voice2.add_note(note)

        score = MusicalScore()
        score.add_voice(voice1)
        score.add_voice(voice2)

        # Test the internal isorhythmic detection method
        has_isorhythm = analyzer._detect_isorhythmic_structure(score)
        assert has_isorhythm is True
