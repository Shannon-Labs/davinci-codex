#!/usr/bin/env python3
"""
Leonardo's Mechanical Ensemble - Renaissance Performance Suite
Phase 3: Cultural Revival - Authentic Renaissance Musical Experiences

This program creates complete Renaissance musical performances adapted for
Leonardo da Vinci's mechanical instruments, showcasing both technical
brilliance and cultural significance.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from davinci_codex.artifacts import ensure_artifact_dir
from davinci_codex.renaissance_music import (
    MechanicalEnsembleIntegrator,
    RenaissanceCompositionGenerator,
    RenaissancePatternLibrary,
)
from davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


class RenaissancePerformanceSuite:
    """Complete Renaissance performance suite for Leonardo's mechanical ensemble."""

    def __init__(self):
        """Initialize the performance suite."""
        self.integrator = MechanicalEnsembleIntegrator()
        self.composer = RenaissanceCompositionGenerator()
        self.pattern_library = RenaissancePatternLibrary()

        # Define instrument configurations for different ensemble types
        self.ensemble_configurations = {
            "chamber_ensemble": {
                0: InstrumentType.VIOLA_ORGANISTA,     # soprano/alto
                1: InstrumentType.PROGRAMMABLE_FLUTE,   # soprano
                2: InstrumentType.MECHANICAL_ORGAN,     # tenor/bass
                3: InstrumentType.MECHANICAL_CARILLON,  # harmonic support
            },
            "full_ensemble": {
                0: InstrumentType.VIOLA_ORGANISTA,     # soprano
                1: InstrumentType.PROGRAMMABLE_FLUTE,   # soprano/alto
                2: InstrumentType.MECHANICAL_TRUMPETER, # alto/tenor
                3: InstrumentType.MECHANICAL_ORGAN,     # tenor
                4: InstrumentType.MECHANICAL_DRUM,      # percussion
                5: InstrumentType.MECHANICAL_CARILLON,  # bass/harmony
            },
            "dance_ensemble": {
                0: InstrumentType.PROGRAMMABLE_FLUTE,   # melody
                1: InstrumentType.MECHANICAL_TRUMPETER, # harmony
                2: InstrumentType.MECHANICAL_DRUM,      # rhythm
                3: InstrumentType.MECHANICAL_CARILLON,  # bass
            }
        }

    def create_historical_pavane(self) -> MusicalScore:
        """Create a historical pavane based on authentic Renaissance dance forms."""

        # Create score in authentic Renaissance style
        score = MusicalScore(
            title="Pavane pour la Cour de Milan",
            composer="Leonardo da Vinci (mechanical adaptation)",
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.PAVANE,
            tempo_bpm=84.0
        )

        # Historical pavane characteristics:
        # - Duple meter, stately pace
        # - Four-part texture (soprano, alto, tenor, bass)
        # - Stepwise motion with occasional leaps
        # - Phrases in 4-measure units

        # Generate pavane melody using historical patterns
        melody_pitches = [
            293.66, 329.63, 349.23, 392.00,  # D4-G4 (Dorian scale)
            349.23, 329.63, 293.66, 261.63,  # F4-C4
            293.66, 329.63, 392.00, 440.00,  # D4-A4
            392.00, 349.23, 329.63, 293.66   # G4-D4
        ]

        # Create four voices with authentic Renaissance counterpoint
        voices_data = {
            "soprano": {
                "instrument": InstrumentType.PROGRAMMABLE_FLUTE,
                "pitches": melody_pitches,
                "octave_adjustment": 1.0
            },
            "alto": {
                "instrument": InstrumentType.VIOLA_ORGANISTA,
                "pitches": self._create_harmony_line(melody_pitches, -3),
                "octave_adjustment": 0.8
            },
            "tenor": {
                "instrument": InstrumentType.MECHANICAL_ORGAN,
                "pitches": self._create_harmony_line(melody_pitches, -7),
                "octave_adjustment": 0.6
            },
            "bass": {
                "instrument": InstrumentType.MECHANICAL_CARILLON,
                "pitches": self._create_bass_line(melody_pitches),
                "octave_adjustment": 0.4
            }
        }

        # Generate notes for each voice
        for voice_name, voice_data in voices_data.items():
            voice = Voice(name=voice_name, instrument=voice_data["instrument"])
            notes = self._create_pavane_rhythm(
                voice_data["pitches"],
                voice_data["octave_adjustment"],
                voice_name
            )
            for note in notes:
                voice.add_note(note)
            score.add_voice(voice)

        return score

    def create_basse_danse(self) -> MusicalScore:
        """Create a basse danse, one of the earliest Renaissance dance forms."""

        score = MusicalScore(
            title="La Basse Danse de Sforza",
            composer="Leonardo da Vinci (mechanical adaptation)",
            mode=RenaissanceMode.MIXOLYDIAN,
            form=MusicalForm.BASSE_DANSE,
            tempo_bpm=72.0
        )

        # Basse danse: slow, stately processional dance
        # Characterized by smooth bass line and elegant upper voices

        # Tenor cantus firmus (fixed melody)
        cantus_firmus = [
            392.00, 440.00, 493.88, 523.25,  # G4-C5 (Mixolydian)
            493.88, 440.00, 392.00, 349.23,  # B4-F4
            392.00, 440.00, 493.88, 392.00,  # G4-G4
            349.23, 329.63, 293.66, 261.63   # F4-C4
        ]

        # Create bass line (basse danse foundation)
        bass_line = self._create_basse_danse_bass(cantus_firmus)

        # Create three upper voices above the bass
        voices_config = [
            ("Cantus Firmus", InstrumentType.PROGRAMMABLE_FLUTE, cantus_firmus, 1.0),
            ("Contra", InstrumentType.VIOLA_ORGANISTA, self._create_harmony_line(cantus_firmus, -4), 0.8),
            ("Tenor", InstrumentType.MECHANICAL_TRUMPETER, self._create_harmony_line(cantus_firmus, -7), 0.6),
            ("Basse", InstrumentType.MECHANICAL_DRUM, bass_line, 0.4)
        ]

        for voice_name, instrument, pitches, octave_adj in voices_config:
            voice = Voice(name=voice_name, instrument=instrument)
            notes = self._create_basse_danse_rhythm(pitches, octave_adj, voice_name)
            for note in notes:
                voice.add_note(note)
            score.add_voice(voice)

        return score

    def create_galliard(self) -> MusicalScore:
        """Create a lively galliard, a triple-meter Renaissance dance."""

        score = MusicalScore(
            title="Gagliarda Milanese",
            composer="Leonardo da Vinci (mechanical adaptation)",
            mode=RenaissanceMode.LYDIAN,
            form=MusicalForm.GALLIARD,
            tempo_bpm=126.0
        )

        # Galliard: energetic triple-meter dance
        # Characterized by jumping steps and lively rhythms

        # Main galliard theme
        main_theme = [
            329.63, 392.00, 440.00, 493.88,  # E4-B4 (Lydian)
            440.00, 392.00, 329.63, 261.63,  # A4-C4
            329.63, 415.30, 493.88, 587.33,  # E4-D5
            493.88, 415.30, 329.63, 246.94   # B4-B3
        ]

        # Create ensemble for dance music
        voices_config = [
            ("Melody", InstrumentType.PROGRAMMABLE_FLUTE, main_theme, 1.0),
            ("Harmony", InstrumentType.MECHANICAL_TRUMPETER, self._create_galliard_harmony(main_theme), 0.8),
            ("Rhythm", InstrumentType.MECHANICAL_DRUM, self._create_galliard_rhythm(), 0.3),
            ("Bass", InstrumentType.MECHANICAL_CARILLON, self._create_galliard_bass(main_theme), 0.5)
        ]

        for voice_name, instrument, pitches_func, octave_adj in voices_config:
            voice = Voice(name=voice_name, instrument=instrument)
            if callable(pitches_func):
                notes = pitches_func()
            else:
                notes = self._create_galliard_rhythm_pattern(pitches_func, octave_adj, voice_name)
            for note in notes:
                voice.add_note(note)
            score.add_voice(voice)

        return score

    def _create_harmony_line(self, melody: List[float], interval: int) -> List[float]:
        """Create a harmony line at specified interval below melody."""
        harmony = []
        interval_ratio = 2 ** (interval / 12)  # Convert semitones to frequency ratio

        for pitch in melody:
            harmony_pitch = pitch / interval_ratio
            # Ensure harmony stays in reasonable range
            while harmony_pitch < 130.0:  # C3 minimum
                harmony_pitch *= 2.0
            while harmony_pitch > 800.0:   # G5 maximum
                harmony_pitch *= 0.5
            harmony.append(harmony_pitch)

        return harmony

    def _create_bass_line(self, melody: List[float]) -> List[float]:
        """Create a Renaissance-style bass line."""
        bass = []
        # Create bass using root and fifth of implied harmony
        root_positions = [0, 0, 2, 2, 4, 4, 5, 5, 0, 2, 4, 0]  # Simple chord progression

        for i, melody_pitch in enumerate(melody):
            if i < len(root_positions):
                bass_note = melody_pitch / (2 ** (root_positions[i] / 12))
                # Ensure bass is in proper range
                while bass_note < 100.0:
                    bass_note *= 2.0
                while bass_note > 300.0:
                    bass_note *= 0.5
                bass.append(bass_note)
            else:
                bass.append(bass[-1])  # Repeat last note

        return bass

    def _create_pavane_rhythm(self, pitches: List[float], octave_adj: float, voice_name: str) -> List[Note]:
        """Create pavane rhythm (slow, duple meter)."""
        notes = []
        current_time = 0.0
        beat_duration = 60.0 / 84.0  # Quarter note at 84 BPM

        for i, pitch in enumerate(pitches):
            # Pavane rhythm: predominantly half notes with some quarter notes
            duration = beat_duration * 2 if i % 4 in [0, 2] else beat_duration

            # Adjust for voice characteristics
            if voice_name == "bass":
                duration *= 1.5  # Bass moves slower
                main_note_start = current_time
                main_note_duration = duration
            elif voice_name == "soprano":
                # Add some ornamentation
                if i % 8 == 3:
                    # Add trill
                    trill_note = Note(
                        pitch=pitch * octave_adj * 1.06,  # Minor second above
                        duration=duration * 0.25,
                        velocity=0.6,
                        start_time=current_time,
                        voice=0
                    )
                    notes.append(trill_note)
                    main_note_start = current_time + duration * 0.25
                    main_note_duration = duration * 0.75
                else:
                    main_note_start = current_time
                    main_note_duration = duration
            else:
                main_note_start = current_time
                main_note_duration = duration

            note = Note(
                pitch=pitch * octave_adj,
                duration=main_note_duration,
                velocity=0.7 if voice_name != "bass" else 0.8,
                start_time=main_note_start,
                voice=0
            )
            notes.append(note)

            current_time += duration

        return notes

    def _create_basse_danse_bass(self, cantus_firmus: List[float]) -> List[float]:
        """Create bass line for basse danse."""
        bass = []
        # Basse danse bass: slow, deliberate motion supporting the cantus firmus

        for i, pitch in enumerate(cantus_firmus):
            if i % 2 == 0:  # Bass moves on every other note
                # Find the appropriate bass note (usually root or fifth)
                bass_note = pitch / 4.0  # Two octaves below
                while bass_note < 80.0:
                    bass_note *= 2.0
                while bass_note > 200.0:
                    bass_note *= 0.5
                bass.append(bass_note)

        return bass

    def _create_basse_danse_rhythm(self, pitches: List[float], octave_adj: float, voice_name: str) -> List[Note]:
        """Create basse danse rhythm (slow, stately)."""
        notes = []
        current_time = 0.0
        beat_duration = 60.0 / 72.0  # Quarter note at 72 BPM

        for i, pitch in enumerate(pitches):
            if voice_name == "Basse":
                # Bass moves slowly - whole and half notes
                if i % 2 == 0:
                    duration = beat_duration * 4  # Whole note
                else:
                    continue  # Skip every other note
            elif voice_name == "Cantus Firmus":
                # Cantus firmus moves moderately
                duration = beat_duration * 2  # Half notes
            else:
                # Other voices move more freely
                duration = beat_duration * (2 if i % 2 == 0 else 1)

            note = Note(
                pitch=pitch * octave_adj,
                duration=duration,
                velocity=0.7 if voice_name != "Basse" else 0.9,
                start_time=current_time,
                voice=0
            )
            notes.append(note)
            current_time += duration

        return notes

    def _create_galliard_harmony(self, melody: List[float]) -> List[float]:
        """Create harmony line for galliard."""
        harmony = []
        # Galliard harmony: lively, with more rhythmic interest

        for i, pitch in enumerate(melody):
            harmony_pitch = pitch / (2 ** (4 / 12)) if i % 2 == 0 else pitch / (2 ** (7 / 12))

            # Adjust range
            while harmony_pitch < 200.0:
                harmony_pitch *= 2.0
            while harmony_pitch > 600.0:
                harmony_pitch *= 0.5

            harmony.append(harmony_pitch)

        return harmony

    def _create_galliard_rhythm(self) -> callable:
        """Create galliard rhythm pattern (triple meter)."""
        def create_rhythm_notes():
            notes = []
            current_time = 0.0
            beat_duration = 60.0 / 126.0  # Quarter note at 126 BPM

            # Typical galliard rhythm: 1-2-3, 1-and-2-3 pattern
            pattern = [
                (0.0, beat_duration),      # Beat 1
                (beat_duration, beat_duration * 0.5),  # Beat 2
                (beat_duration * 1.5, beat_duration * 0.5),  # Beat 2 and
                (beat_duration * 2.0, beat_duration),  # Beat 3
            ]

            # Repeat pattern for several measures
            for _measure in range(8):
                for offset, duration in pattern:
                    note = Note(
                        pitch=150.0,  # Low percussion pitch
                        duration=duration,
                        velocity=0.8,
                        start_time=current_time + offset,
                        voice=0
                    )
                    notes.append(note)
                current_time += beat_duration * 3

            return notes

        return create_rhythm_notes

    def _create_galliard_bass(self, melody: List[float]) -> List[float]:
        """Create bass line for galliard."""
        bass = []
        # Galliard bass: supports the lively dance rhythm

        chord_progression = [0, 3, 0, 4, 0, 3, 0, 5]  # I-IV-I-V-I-IV-I-V pattern

        for i, scale_degree in enumerate(chord_progression):
            if i < len(melody):
                # Use melody as reference for key
                root = melody[0] / (2 ** (scale_degree / 12))
                while root < 100.0:
                    root *= 2.0
                while root > 250.0:
                    root *= 0.5
                bass.append(root)

        return bass

    def _create_galliard_rhythm_pattern(self, pitches: List[float], octave_adj: float, voice_name: str) -> List[Note]:
        """Create galliard rhythm pattern for melodic instruments."""
        notes = []
        current_time = 0.0
        beat_duration = 60.0 / 126.0  # Quarter note at 126 BPM

        for i, pitch in enumerate(pitches):
            if voice_name == "Melody":
                # Melody with characteristic galliard rhythm
                duration = beat_duration if i % 4 in [0, 2] else beat_duration * 0.5  # Eighth note
            elif voice_name == "Bass":
                # Bass emphasizes main beats
                duration = beat_duration * 1.5 if i % 2 == 0 else beat_duration * 0.5  # Eighth note
            else:
                duration = beat_duration  # Default quarter note

            note = Note(
                pitch=pitch * octave_adj,
                duration=duration,
                velocity=0.7 if voice_name != "Bass" else 0.8,
                start_time=current_time,
                voice=0
            )
            notes.append(note)
            current_time += duration

        return notes

    def generate_full_performance_suite(self) -> Dict[str, MusicalScore]:
        """Generate the complete Renaissance performance suite."""

        print("Generating Leonardo's Mechanical Ensemble Performance Suite...")
        print("=" * 60)

        # Create the three main pieces
        pieces = {
            "pavane": self.create_historical_pavane(),
            "basse_danse": self.create_basse_danse(),
            "galliard": self.create_galliard()
        }

        # Print information about each piece
        for piece_name, score in pieces.items():
            print(f"\n{piece_name.replace('_', ' ').title()}:")
            print(f"  Title: {score.title}")
            print(f"  Mode: {score.mode.value if score.mode else 'unknown'}")
            print(f"  Form: {score.form.value if score.form else 'unknown'}")
            print(f"  Tempo: {score.tempo_bpm} BPM")
            print(f"  Voices: {score.get_voice_count()}")
            print(f"  Duration: {score.get_duration():.1f} seconds")

        return pieces

    def adapt_and_validate_pieces(self, pieces: Dict[str, MusicalScore]) -> Dict[str, Dict]:
        """Adapt pieces for mechanical ensemble and validate."""

        print(f"\n{'='*60}")
        print("Adapting pieces for mechanical ensemble...")

        adapted_pieces = {}

        for piece_name, score in pieces.items():
            print(f"\nAdapting {piece_name.replace('_', ' ').title()}...")

            # Choose appropriate ensemble configuration
            if piece_name == "pavane" or piece_name == "basse_danse":
                config = self.ensemble_configurations["chamber_ensemble"]
            else:  # galliard
                config = self.ensemble_configurations["dance_ensemble"]

            # Adapt the score
            adaptation_result = self.integrator.adapt_score_for_ensemble(score, config)

            print(f"  Adaptation successful: {adaptation_result.adaptation_success}")

            if adaptation_result.feasibility_scores:
                print("  Feasibility scores:")
                for instrument, score_value in adaptation_result.feasibility_scores.items():
                    print(f"    {instrument.value}: {score_value:.2f}")

            if adaptation_result.constraint_violations:
                print("  Constraint violations:")
                for violation in adaptation_result.constraint_violations[:3]:  # Show first 3
                    print(f"    - {violation}")

            # Validate with simulation
            validation_result = self.integrator.validate_with_simulation(
                adaptation_result.adapted_score, config
            )

            print(f"  Simulation validation: {'PASSED' if validation_result['valid'] else 'FAILED'}")

            # Generate demo
            demo_result = self.integrator.generate_ensemble_demo(
                adaptation_result.adapted_score,
                config,
                tempo_bpm=score.tempo_bpm,
                measures=8,
                render_audio=False
            )

            adapted_pieces[piece_name] = {
                "original_score": score,
                "adapted_score": adaptation_result.adapted_score,
                "adaptation_result": adaptation_result,
                "validation_result": validation_result,
                "demo_result": demo_result,
                "instrument_config": config
            }

        return adapted_pieces

    def save_performance_suite(self, adapted_pieces: Dict[str, Dict]) -> None:
        """Save the complete performance suite to artifacts."""

        print(f"\n{'='*60}")
        print("Saving Renaissance Performance Suite...")

        # Create artifact directory
        suite_dir = ensure_artifact_dir("renaissance_performance_suite")

        # Save each piece
        for piece_name, piece_data in adapted_pieces.items():
            # Create piece directory
            piece_dir = suite_dir / piece_name
            piece_dir.mkdir(exist_ok=True)

            # Save original score
            original_path = piece_dir / "original_score.json"
            with original_path.open("w", encoding="utf-8") as f:
                json.dump(self._score_to_dict(piece_data["original_score"]), f, indent=2)

            # Save adapted score
            adapted_path = piece_dir / "adapted_score.json"
            with adapted_path.open("w", encoding="utf-8") as f:
                json.dump(self._score_to_dict(piece_data["adapted_score"]), f, indent=2)

            # Save adaptation details
            adaptation_path = piece_dir / "adaptation_details.json"
            adaptation_details = {
                "adaptation_success": piece_data["adaptation_result"].adaptation_success,
                "feasibility_scores": {
                    instrument.value: score
                    for instrument, score in piece_data["adaptation_result"].feasibility_scores.items()
                },
                "constraint_violations": piece_data["adaptation_result"].constraint_violations,
                "adaptation_log": piece_data["adaptation_result"].adaptation_log,
                "validation_result": piece_data["validation_result"]
            }
            with adaptation_path.open("w", encoding="utf-8") as f:
                json.dump(adaptation_details, f, indent=2)

            # Save instrument configuration
            config_path = piece_dir / "instrument_config.json"
            instrument_config = {
                voice_idx: instrument.value
                for voice_idx, instrument in piece_data["instrument_config"].items()
            }
            with config_path.open("w", encoding="utf-8") as f:
                json.dump(instrument_config, f, indent=2)

            print(f"  Saved {piece_name}:")
            print(f"    Original score: {original_path}")
            print(f"    Adapted score: {adapted_path}")
            print(f"    Adaptation details: {adaptation_path}")
            print(f"    Instrument config: {config_path}")

        # Create performance program
        program_path = suite_dir / "performance_program.md"
        program_content = self._create_performance_program(adapted_pieces)
        with program_path.open("w", encoding="utf-8") as f:
            f.write(program_content)

        print(f"\nPerformance program saved: {program_path}")
        print(f"\nComplete Renaissance Performance Suite saved to: {suite_dir}")

    def _score_to_dict(self, score: MusicalScore) -> Dict:
        """Convert a MusicalScore to a dictionary for JSON serialization."""
        return {
            "title": score.title,
            "composer": score.composer,
            "mode": score.mode.value if score.mode else None,
            "mensuration": score.mensuration.value if score.mensuration else None,
            "form": score.form.value if score.form else None,
            "tempo_bpm": score.tempo_bpm,
            "voices": [
                {
                    "name": voice.name,
                    "instrument": voice.instrument.value if voice.instrument else None,
                    "range_low": voice.range_low,
                    "range_high": voice.range_high,
                    "notes": [
                        {
                            "pitch": note.pitch,
                            "duration": note.duration,
                            "velocity": note.velocity,
                            "start_time": note.start_time,
                            "voice": note.voice,
                            "is_rest": note.is_rest
                        }
                        for note in voice.notes
                    ]
                }
                for voice in score.voices
            ],
            "metadata": score.metadata
        }

    def _create_performance_program(self, adapted_pieces: Dict[str, Dict]) -> str:
        """Create a performance program document."""

        program = """# Leonardo's Mechanical Ensemble - Renaissance Performance Suite

## Program Notes

Welcome to a unique musical experience that brings together Renaissance musical artistry and Leonardo da Vinci's mechanical genius. This performance suite features authentic Renaissance dance forms adapted for Leonardo's innovative mechanical instruments.

### Historical Context

The late 15th century in Milan was a period of extraordinary cultural flowering under Ludovico Sforza. Leonardo da Vinci, serving as court artist and engineer, designed numerous mechanical devices, including musical instruments that pushed the boundaries of Renaissance technology.

### The Instruments

- **Viola Organista**: Leonardo's bowed keyboard instrument combining violin and organ qualities
- **Mechanical Organ**: A sophisticated pipe organ with automated control
- **Programmable Flute**: An automated flute capable of complex melodic lines
- **Mechanical Trumpeter**: A brass instrument with mechanical articulation
- **Mechanical Drum**: Percussion with rhythmic precision
- **Mechanical Carillon**: Bell ensemble with harmonic resonance

---

## Performance Pieces

"""

        for piece_name, piece_data in adapted_pieces.items():
            score = piece_data["original_score"]
            adaptation = piece_data["adaptation_result"]

            program += f"""### {score.title}

**Composer**: {score.composer}
**Form**: {score.form.value.replace('_', ' ').title()}
**Mode**: {score.mode.value if score.mode else 'unknown'}
**Tempo**: {score.tempo_bpm} BPM
**Duration**: {score.get_duration():.1f} seconds

**Instrumentation**:
"""

            for voice_idx, instrument in piece_data["instrument_config"].items():
                voice_name = score.voices[voice_idx].name
                program += f"- {voice_name}: {instrument.value}\n"

            program += """
**Historical Notes**:
"""

            if piece_name == "pavane":
                program += """The pavane was a stately processional dance popular in European courts from the 16th century. Originating in Italy, it spread throughout Europe and became a standard part of court dance suites. The pavane's dignified pace (typically 80-90 BPM) and duple meter made it ideal for ceremonial entrances and formal social gatherings.

Leonardo would have encountered pavanes at the Sforza court, where they accompanied formal ceremonies and diplomatic processions. The mechanical adaptation preserves the dance's noble character while showcasing the technical capabilities of the viola organista and programmable flute.

"""
            elif piece_name == "basse_danse":
                program += """The basse danse represents one of the earliest Renaissance dance forms, emerging in the 15th century. Characterized by its smooth, gliding steps and solemn dignity, it was particularly popular in Burgundian and Italian courts. The dance features a tenor cantus firmus (fixed melody) with supporting voices in measured counterpoint.

This mechanical interpretation uses the drum for the foundational bass line, with the programmable flute carrying the cantus firmus - a configuration that would have fascinated Leonardo, who appreciated both mathematical precision and artistic beauty.

"""
            else:  # galliard
                program += """The galliard was a lively, athletic dance in triple meter that often followed the stately pavane. Known for its jumping steps and energetic character, it became popular throughout Renaissance Europe. The typical galliard rhythm (1-2-3, 1-and-2-3) creates a distinctive syncopated feel that showcases both technical skill and rhythmic vitality.

Leonardo's studies of human movement and mechanics would have made the galliard particularly appealing for mechanical adaptation. The combination of percussive rhythms and melodic freedom demonstrates the full capabilities of his mechanical ensemble.

"""

            program += "**Technical Adaptation**: " + ("Successful" if adaptation.adaptation_success else "Partial") + "\n\n"

            if adaptation.feasibility_scores:
                avg_feasibility = sum(adaptation.feasibility_scores.values()) / len(adaptation.feasibility_scores)
                program += f"**Mechanical Feasibility**: {avg_feasibility:.2f}/1.00\n\n"

        program += """---

## Performance Practice Notes

### Mechanical Considerations

1. **Temporal Precision**: The mechanical nature of these instruments provides exceptional rhythmic accuracy, though slight mechanical latency may be perceptible compared to human performance.

2. **Dynamic Range**: Mechanical instruments have different dynamic characteristics than their human-played counterparts. Adjustments have been made to optimize musical expressiveness within mechanical constraints.

3. **Articulation**: The mechanical adaptation emphasizes clarity of line and rhythmic precision, characteristics that align well with Renaissance performance ideals.

### Historical Authenticity

While the mechanical nature of these instruments represents an anachronistic element, every effort has been made to preserve:
- Authentic Renaissance modes and tunings
- Historically appropriate rhythmic patterns
- Correct voice-leading and counterpoint
- Suitable dance tempos and character

### Educational Value

This performance suite serves both as musical entertainment and as a demonstration of:
- Leonardo's mechanical ingenuity
- Renaissance musical forms and practices
- The intersection of art and technology in the Renaissance

---

## About This Adaptation

This mechanical adaptation was created using advanced computational analysis of Renaissance musical practice combined with detailed modeling of Leonardo's mechanical instrument designs. The adaptation process respects both historical authenticity and mechanical feasibility, creating a unique bridge between past and present.

*Generated as part of the da Vinci Codex Project - Phase 3: Cultural Revival*
"""

        return program


def main():
    """Main function to generate the complete Renaissance performance suite."""

    print("Leonardo da Vinci's Mechanical Ensemble")
    print("Renaissance Performance Suite Generator")
    print("Phase 3: Cultural Revival")
    print("=" * 60)

    # Create performance suite
    suite = RenaissancePerformanceSuite()

    # Generate pieces
    pieces = suite.generate_full_performance_suite()

    # Adapt for mechanical ensemble
    adapted_pieces = suite.adapt_and_validate_pieces(pieces)

    # Save the complete suite
    suite.save_performance_suite(adapted_pieces)

    print(f"\n{'='*60}")
    print("Renaissance Performance Suite Complete!")
    print("\nThe suite includes:")
    print("  1. Pavane pour la Cour de Milan (stately court dance)")
    print("  2. La Basse Danse de Sforza (solemn processional)")
    print("  3. Gagliarda Milanese (lively triple-meter dance)")
    print("\nEach piece has been:")
    print("  - Adapted for Leonardo's mechanical instruments")
    print("  - Validated for mechanical feasibility")
    print("  - Documented with historical context")
    print("  - Saved with performance notes")

    print(f"\nArtifacts saved to: {ensure_artifact_dir('renaissance_performance_suite')}")


if __name__ == "__main__":
    main()
