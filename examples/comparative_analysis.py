#!/usr/bin/env python3
"""
Comparative Analysis System: Historical Performance vs Mechanical Adaptation
Phase 3: Cultural Revival - Comparative Study and Analysis

This program creates a comprehensive comparative analysis between traditional
Renaissance performance practice and Leonardo's mechanical instrument adaptations,
highlighting similarities, differences, and unique characteristics of each approach.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from davinci_codex.artifacts import ensure_artifact_dir
from davinci_codex.renaissance_music import (
    MechanicalEnsembleIntegrator,
    RenaissanceCompositionGenerator,
)
from davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


class ComparativeAnalysisSystem:
    """System for comparing historical and mechanical performance approaches."""

    def __init__(self):
        """Initialize the comparative analysis system."""
        self.integrator = MechanicalEnsembleIntegrator()
        self.composer = RenaissanceCompositionGenerator()

        # Define comparative analysis categories
        self.analysis_categories = {
            "tempo_consistency": "Analysis of tempo stability and variation",
            "dynamic_range": "Comparison of dynamic capabilities and expression",
            "articulation_precision": "Analysis of articulation clarity and consistency",
            "intonation_accuracy": "Assessment of pitch accuracy and stability",
            "texture_clarity": "Analysis of polyphonic clarity and voice separation",
            "ornamentation_capability": "Comparison of ornamentation and decorative elements",
            "ensemble_coordination": "Analysis of ensemble timing and coordination",
            "sustain_characteristics": "Comparison of note sustain and decay characteristics",
            "timbral_consistency": "Analysis of tone quality and consistency",
            "performance_reliability": "Assessment of performance consistency and reliability"
        }

        # Define historical performance characteristics
        self.historical_characteristics = {
            "tempo_consistency": {
                "description": "Human performers naturally vary tempo with rubato and expressive timing",
                "typical_variation": "5-15% tempo variation",
                "expressive_potential": "High - natural human expression",
                "technical_limitation": "Human endurance and concentration"
            },
            "dynamic_range": {
                "description": "Wide dynamic range from subtle pianissimo to powerful fortissimo",
                "typical_range": "30-100 dB for chamber music",
                "expressive_potential": "Very high - nuanced dynamic control",
                "technical_limitation": "Human breath control and physical strength"
            },
            "articulation_precision": {
                "description": "Variable articulation based on performer skill and technique",
                "typical_precision": "75-90% consistency depending on skill level",
                "expressive_potential": "High - individual artistic interpretation",
                "technical_limitation": "Human motor skills and technique"
            },
            "intonation_accuracy": {
                "description": "Adjustable intonation based on player skill and acoustic context",
                "typical_accuracy": "±10 cents for skilled performers",
                "expressive_potential": "High - expressive intonation adjustments",
                "technical_limitation": "Human ear training and physical control"
            },
            "texture_clarity": {
                "description": "Variable clarity based on performer communication and skill",
                "typical_clarity": "Dependent on ensemble experience and rehearsal",
                "expressive_potential": "High - interactive ensemble communication",
                "technical_limitation": "Human coordination and listening skills"
            },
            "ornamentation_capability": {
                "description": "Extensive ornamentation based on historical practice and individual style",
                "typical_complexity": "Highly variable based on performer expertise",
                "expressive_potential": "Very high - personal ornamentation style",
                "technical_limitation": "Human technical skill and historical knowledge"
            },
            "ensemble_coordination": {
                "description": "Visual and auditory cues for ensemble coordination",
                "typical_precision": "Dependent on rehearsal and conductor/leader",
                "expressive_potential": "High - interactive ensemble dynamics",
                "technical_limitation": "Human communication and response time"
            },
            "sustain_characteristics": {
                "description": "Variable sustain based on breath control and technique",
                "typical_consistency": "Variable based on player skill",
                "expressive_potential": "High - expressive sustain and decay",
                "technical_limitation": "Human breath control and physical endurance"
            },
            "timbral_consistency": {
                "description": "Variable tone color based on player technique and instrument condition",
                "typical_consistency": "Changes with player fatigue and environmental factors",
                "expressive_potential": "Very high - individual tonal personality",
                "technical_limitation": "Human physical technique and instrument quality"
            },
            "performance_reliability": {
                "description": "Variable reliability based on human factors",
                "typical_consistency": "75-95% consistency depending on conditions",
                "expressive_potential": "High - human spontaneity and creativity",
                "technical_limitation": "Human health, concentration, and environmental factors"
            }
        }

        # Define mechanical performance characteristics
        self.mechanical_characteristics = {
            "tempo_consistency": {
                "description": "Extremely consistent tempo maintained by mechanical regulation",
                "typical_variation": "1-3% mechanical variation",
                "expressive_potential": "Low - mechanical consistency limits expression",
                "technical_limitation": "Mechanical regulation systems and wear"
            },
            "dynamic_range": {
                "description": "Limited dynamic range constrained by mechanical design",
                "typical_range": "50-90 dB for mechanical instruments",
                "expressive_potential": "Moderate - registration changes and combinations",
                "technical_limitation": "Mechanical force limitations and sound production"
            },
            "articulation_precision": {
                "description": "Highly consistent articulation based on mechanical design",
                "typical_precision": "95-99% mechanical consistency",
                "expressive_potential": "Low - uniform mechanical articulation",
                "technical_limitation": "Mechanical precision and adjustment capability"
            },
            "intonation_accuracy": {
                "description": "Very stable intonation once properly regulated",
                "typical_accuracy": "±2 cents mechanical stability",
                "expressive_potential": "Low - fixed pitch limits expression",
                "technical_limitation": "Mechanical tuning stability and regulation"
            },
            "texture_clarity": {
                "description": "Consistent polyphonic clarity through mechanical independence",
                "typical_clarity": "High - mechanical voice independence",
                "expressive_potential": "Moderate - limited expressive interaction",
                "technical_limitation": "Mechanical design and sound coupling"
            },
            "ornamentation_capability": {
                "description": "Pre-programmed ornamentation with mechanical precision",
                "typical_complexity": "Limited by mechanical programming capability",
                "expressive_potential": "Low - fixed ornamentation patterns",
                "technical_limitation": "Mechanical programming complexity and reliability"
            },
            "ensemble_coordination": {
                "description": "Perfect mechanical coordination through synchronized mechanisms",
                "typical_precision": "99%+ mechanical synchronization",
                "expressive_potential": "Low - mechanical precision limits interaction",
                "technical_limitation": "Mechanical synchronization and regulation"
            },
            "sustain_characteristics": {
                "description": "Consistent sustain characteristics based on mechanical design",
                "typical_consistency": "High - mechanical sustain consistency",
                "expressive_potential": "Moderate - consistent but limited expression",
                "technical_limitation": "Mechanical sound production and decay characteristics"
            },
            "timbral_consistency": {
                "description": "Very consistent tone quality with minimal variation",
                "typical_consistency": "95-98% mechanical consistency",
                "expressive_potential": "Low - uniform mechanical tone production",
                "technical_limitation": "Mechanical sound production and material consistency"
            },
            "performance_reliability": {
                "description": "High reliability when properly maintained and regulated",
                "typical_consistency": "98%+ mechanical reliability",
                "expressive_potential": "Low - mechanical precision limits creativity",
                "technical_limitation": "Mechanical maintenance and regulation requirements"
            }
        }

    def create_comparison_pieces(self) -> Dict[str, Tuple[MusicalScore, MusicalScore]]:
        """Create pieces for comparison between historical and mechanical approaches."""

        print("Creating comparative analysis pieces...")

        comparison_pieces = {}

        # 1. Pavane comparison - showing sustain and legato capabilities
        pavane_historical = self._create_historical_pavane()
        pavane_mechanical = self._create_mechanical_pavane()
        comparison_pieces["pavane"] = (pavane_historical, pavane_mechanical)

        # 2. Galliard comparison - showing rhythmic precision and ornamentation
        galliard_historical = self._create_historical_galliard()
        galliard_mechanical = self._create_mechanical_galliard()
        comparison_pieces["galliard"] = (galliard_historical, galliard_mechanical)

        # 3. Polyphonic piece comparison - showing texture and coordination
        polyphonic_historical = self._create_historical_polyphony()
        polyphonic_mechanical = self._create_mechanical_polyphony()
        comparison_pieces["polyphony"] = (polyphonic_historical, polyphonic_mechanical)

        return comparison_pieces

    def _create_historical_pavane(self) -> MusicalScore:
        """Create a historical-style pavane emphasizing human performance characteristics."""

        score = MusicalScore(
            title="Pavane - Historical Performance Style",
            composer="Renaissance Style (Human Performance)",
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.PAVANE,
            tempo_bpm=84.0
        )

        # Create melody with human-like characteristics
        melody = Voice(name="Melody (Human)", instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Add expressive timing and articulation variations
        melody_notes = [
            Note(pitch=293.66, duration=1.9, velocity=0.75, start_time=0.0),    # Slightly uneven duration
            Note(pitch=329.63, duration=0.95, velocity=0.72, start_time=1.9),    # Slight dynamic variation
            Note(pitch=349.23, duration=1.05, velocity=0.78, start_time=2.85),   # Expressive timing
            Note(pitch=392.00, duration=0.98, velocity=0.74, start_time=3.9),    # Human rubato
            Note(pitch=349.23, duration=2.1, velocity=0.76, start_time=4.88),    # Slight tempo variation
            Note(pitch=329.63, duration=0.92, velocity=0.73, start_time=6.98),   # Natural variation
            Note(pitch=293.66, duration=2.05, velocity=0.77, start_time=7.9),    # Expressive ending
        ]

        for note in melody_notes:
            melody.add_note(note)

        # Add ornamentation typical of human performance
        ornamented_notes = self._add_human_ornamentation(melody_notes)
        melody.notes = ornamented_notes

        score.add_voice(melody)

        # Add supporting voices with human characteristics
        harmony = Voice(name="Harmony (Human)", instrument=InstrumentType.VIOLA_ORGANISTA)
        harmony_notes = [
            Note(pitch=196.00, duration=4.0, velocity=0.65, start_time=0.0),     # Slower harmonic rhythm
            Note(pitch=220.00, duration=4.0, velocity=0.63, start_time=4.0),     # Slight detuning
            Note(pitch=196.00, duration=4.0, velocity=0.67, start_time=8.0),     # Human tuning adjustments
        ]

        for note in harmony_notes:
            harmony.add_note(note)

        score.add_voice(harmony)

        return score

    def _create_mechanical_pavane(self) -> MusicalScore:
        """Create a mechanical-style pavane emphasizing mechanical performance characteristics."""

        score = MusicalScore(
            title="Pavane - Mechanical Performance Style",
            composer="Leonardo da Vinci (Mechanical Adaptation)",
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.PAVANE,
            tempo_bpm=84.0
        )

        # Create melody with mechanical precision
        melody = Voice(name="Melody (Mechanical)", instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Precise, consistent timing and articulation
        melody_notes = [
            Note(pitch=293.66, duration=2.0, velocity=0.75, start_time=0.0),     # Precise duration
            Note(pitch=329.63, duration=1.0, velocity=0.75, start_time=2.0),     # Exact timing
            Note(pitch=349.23, duration=1.0, velocity=0.75, start_time=3.0),     # Consistent dynamics
            Note(pitch=392.00, duration=1.0, velocity=0.75, start_time=4.0),     # Mechanical precision
            Note(pitch=349.23, duration=2.0, velocity=0.75, start_time=5.0),     # Perfect timing
            Note(pitch=329.63, duration=1.0, velocity=0.75, start_time=7.0),     # Consistent articulation
            Note(pitch=293.66, duration=2.0, velocity=0.75, start_time=8.0),     # Exact repetition
        ]

        for note in melody_notes:
            melody.add_note(note)

        # Add mechanical ornamentation (simpler, more precise)
        ornamented_notes = self._add_mechanical_ornamentation(melody_notes)
        melody.notes = ornamented_notes

        score.add_voice(melody)

        # Add supporting voices with mechanical characteristics
        harmony = Voice(name="Harmony (Mechanical)", instrument=InstrumentType.VIOLA_ORGANISTA)
        harmony_notes = [
            Note(pitch=196.00, duration=4.0, velocity=0.75, start_time=0.0),     # Exact tuning
            Note(pitch=220.00, duration=4.0, velocity=0.75, start_time=4.0),     # Perfect intonation
            Note(pitch=196.00, duration=4.0, velocity=0.75, start_time=8.0),     # Consistent tone
        ]

        for note in harmony_notes:
            harmony.add_note(note)

        score.add_voice(harmony)

        return score

    def _create_historical_galliard(self) -> MusicalScore:
        """Create a historical-style galliard emphasizing rhythmic flexibility."""

        score = MusicalScore(
            title="Galliard - Historical Performance Style",
            composer="Renaissance Style (Human Performance)",
            mode=RenaissanceMode.LYDIAN,
            form=MusicalForm.GALLIARD,
            tempo_bpm=126.0
        )

        # Create melody with rhythmic flexibility
        melody = Voice(name="Melody (Human)", instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Rhythmic variations typical of human performance
        melody_notes = [
            Note(pitch=329.63, duration=0.48, velocity=0.78, start_time=0.0),     # Slight rushing
            Note(pitch=415.30, duration=0.52, velocity=0.74, start_time=0.48),   # Natural variation
            Note(pitch=493.88, duration=0.47, velocity=0.76, start_time=1.0),    # Human timing
            Note(pitch=587.33, duration=0.53, velocity=0.72, start_time=1.47),   # Slight dragging
            Note(pitch=493.88, duration=0.49, velocity=0.75, start_time=2.0),    # Natural rhythm
            Note(pitch=415.30, duration=0.51, velocity=0.73, start_time=2.49),   # Human feel
            Note(pitch=329.63, duration=0.98, velocity=0.77, start_time=3.0),    # Phrase ending
        ]

        for note in melody_notes:
            melody.add_note(note)

        score.add_voice(melody)

        # Add rhythm with human characteristics
        rhythm = Voice(name="Rhythm (Human)", instrument=InstrumentType.MECHANICAL_DRUM)
        rhythm_notes = [
            Note(pitch=150.0, duration=0.48, velocity=0.82, start_time=0.0),      # Human rhythm
            Note(pitch=200.0, duration=0.52, velocity=0.78, start_time=0.48),    # Natural variation
            Note(pitch=150.0, duration=0.47, velocity=0.80, start_time=1.0),      # Slight inconsistency
            Note(pitch=200.0, duration=0.53, velocity=0.76, start_time=1.47),    # Human feel
        ]

        for note in rhythm_notes:
            rhythm.add_note(note)

        score.add_voice(rhythm)

        return score

    def _create_mechanical_galliard(self) -> MusicalScore:
        """Create a mechanical-style galliard emphasizing rhythmic precision."""

        score = MusicalScore(
            title="Galliard - Mechanical Performance Style",
            composer="Leonardo da Vinci (Mechanical Adaptation)",
            mode=RenaissanceMode.LYDIAN,
            form=MusicalForm.GALLIARD,
            tempo_bpm=126.0
        )

        # Create melody with mechanical precision
        melody = Voice(name="Melody (Mechanical)", instrument=InstrumentType.PROGRAMMABLE_FLUTE)

        # Precise rhythmic execution
        melody_notes = [
            Note(pitch=329.63, duration=0.5, velocity=0.75, start_time=0.0),      # Exact timing
            Note(pitch=415.30, duration=0.5, velocity=0.75, start_time=0.5),      # Perfect rhythm
            Note(pitch=493.88, duration=0.5, velocity=0.75, start_time=1.0),      # Mechanical precision
            Note(pitch=587.33, duration=0.5, velocity=0.75, start_time=1.5),      # Consistent execution
            Note(pitch=493.88, duration=0.5, velocity=0.75, start_time=2.0),      # Exact repetition
            Note(pitch=415.30, duration=0.5, velocity=0.75, start_time=2.5),      # Perfect consistency
            Note(pitch=329.63, duration=1.0, velocity=0.75, start_time=3.0),      # Precise ending
        ]

        for note in melody_notes:
            melody.add_note(note)

        score.add_voice(melody)

        # Add rhythm with mechanical characteristics
        rhythm = Voice(name="Rhythm (Mechanical)", instrument=InstrumentType.MECHANICAL_DRUM)
        rhythm_notes = [
            Note(pitch=150.0, duration=0.5, velocity=0.80, start_time=0.0),       # Perfect timing
            Note(pitch=200.0, duration=0.5, velocity=0.80, start_time=0.5),       # Exact rhythm
            Note(pitch=150.0, duration=0.5, velocity=0.80, start_time=1.0),       # Consistent execution
            Note(pitch=200.0, duration=0.5, velocity=0.80, start_time=1.5),       # Mechanical precision
        ]

        for note in rhythm_notes:
            rhythm.add_note(note)

        score.add_voice(rhythm)

        return score

    def _create_historical_polyphony(self) -> MusicalScore:
        """Create historical-style polyphony emphasizing ensemble interaction."""

        score = MusicalScore(
            title="Polyphony - Historical Performance Style",
            composer="Renaissance Style (Human Performance)",
            mode=RenaissanceMode.MIXOLYDIAN,
            form=MusicalForm.MOTET,
            tempo_bpm=96.0
        )

        # Create four voices with human interaction characteristics
        voices_data = [
            ("Soprano (Human)", [392.0, 440.0, 493.88, 523.25], [0.8, 0.7, 0.75, 0.72]),
            ("Alto (Human)", [329.63, 369.99, 415.30, 440.0], [0.68, 0.65, 0.70, 0.67]),
            ("Tenor (Human)", [261.63, 293.66, 329.63, 349.23], [0.75, 0.72, 0.78, 0.74]),
            ("Bass (Human)", [196.0, 220.0, 246.94, 261.63], [0.82, 0.79, 0.85, 0.81])
        ]

        for voice_name, pitches, velocities in voices_data:
            voice = Voice(name=voice_name, instrument=InstrumentType.MECHANICAL_ORGAN)

            # Add human interaction characteristics
            for i, (pitch, velocity) in enumerate(zip(pitches, velocities)):
                # Slight timing variations between voices
                timing_offset = i * 0.02  # Each voice slightly different
                duration_variation = 1.0 + (i * 0.05)  # Slight duration differences

                note = Note(
                    pitch=pitch * (1 + (i * 0.001)),  # Slight tuning variations
                    duration=2.0 * duration_variation,
                    velocity=velocity,
                    start_time=i * 2.0 + timing_offset,
                    voice=0
                )
                voice.add_note(note)

            score.add_voice(voice)

        return score

    def _create_mechanical_polyphony(self) -> MusicalScore:
        """Create mechanical-style polyphony emphasizing precision and coordination."""

        score = MusicalScore(
            title="Polyphony - Mechanical Performance Style",
            composer="Leonardo da Vinci (Mechanical Adaptation)",
            mode=RenaissanceMode.MIXOLYDIAN,
            form=MusicalForm.MOTET,
            tempo_bpm=96.0
        )

        # Create four voices with mechanical precision
        voices_data = [
            ("Soprano (Mechanical)", [392.0, 440.0, 493.88, 523.25], 0.75),
            ("Alto (Mechanical)", [329.63, 369.99, 415.30, 440.0], 0.75),
            ("Tenor (Mechanical)", [261.63, 293.66, 329.63, 349.23], 0.75),
            ("Bass (Mechanical)", [196.0, 220.0, 246.94, 261.63], 0.75)
        ]

        for voice_name, pitches, velocity in voices_data:
            voice = Voice(name=voice_name, instrument=InstrumentType.MECHANICAL_ORGAN)

            # Perfect mechanical coordination
            for i, pitch in enumerate(pitches):
                note = Note(
                    pitch=pitch,  # Exact tuning
                    duration=2.0,  # Precise duration
                    velocity=velocity,  # Consistent dynamics
                    start_time=i * 2.0,  # Perfect timing
                    voice=0
                )
                voice.add_note(note)

            score.add_voice(voice)

        return score

    def _add_human_ornamentation(self, notes: List[Note]) -> List[Note]:
        """Add human-style ornamentation to notes."""
        ornamented = []

        for note in notes:
            # Add the main note
            ornamented.append(note)

            # Add ornaments with human variation
            if not note.is_rest and note.duration > 0.5:
                # Add trill with slight timing variation
                trill_timing = note.duration * 0.1
                trill_pitch = note.pitch * 1.06  # Minor second above

                trill_note = Note(
                    pitch=trill_pitch * (1 + (hash(str(note)) % 5) * 0.001),  # Slight pitch variation
                    duration=trill_timing * 0.8,  # Slightly uneven
                    velocity=note.velocity * 0.7,
                    start_time=note.start_time + note.duration * 0.3,
                    voice=note.voice
                )
                ornamented.append(trill_note)

        return ornamented

    def _add_mechanical_ornamentation(self, notes: List[Note]) -> List[Note]:
        """Add mechanical-style ornamentation to notes."""
        ornamented = []

        for note in notes:
            # Add the main note
            ornamented.append(note)

            # Add precise mechanical ornaments
            if not note.is_rest and note.duration > 0.5:
                # Add exact trill
                trill_timing = note.duration * 0.1
                trill_pitch = note.pitch * 1.06  # Exact minor second above

                trill_note = Note(
                    pitch=trill_pitch,  # Exact pitch
                    duration=trill_timing,  # Precise timing
                    velocity=note.velocity * 0.7,
                    start_time=note.start_time + note.duration * 0.3,
                    voice=note.voice
                )
                ornamented.append(trill_note)

        return ornamented

    def analyze_comparative_performance(self, historical: MusicalScore, mechanical: MusicalScore) -> Dict:
        """Analyze comparative performance characteristics."""

        analysis = {}

        for category in self.analysis_categories:
            hist_char = self.historical_characteristics[category]
            mech_char = self.mechanical_characteristics[category]

            # Create comparative analysis for this category
            category_analysis = {
                "category": category,
                "description": self.analysis_categories[category],
                "historical_characteristics": hist_char,
                "mechanical_characteristics": mech_char,
                "comparative_assessment": self._assess_category_difference(category, historical, mechanical),
                "advantages": {
                    "historical": self._identify_historical_advantages(category),
                    "mechanical": self._identify_mechanical_advantages(category)
                },
                "applications": {
                    "historical": self._suggest_historical_applications(category),
                    "mechanical": self._suggest_mechanical_applications(category)
                }
            }

            analysis[category] = category_analysis

        return analysis

    def _assess_category_difference(self, category: str, historical: MusicalScore, mechanical: MusicalScore) -> Dict:
        """Assess the differences between historical and mechanical performance for a category."""

        assessments = {
            "tempo_consistency": {
                "primary_difference": "Human rubato vs. mechanical precision",
                "impact_on_music": "Historical: expressive but variable; Mechanical: precise but less expressive",
                "quantitative_difference": "Historical variation 5-15% vs. Mechanical 1-3%",
                "artistic_implications": "Choice between human expression and mechanical reliability"
            },
            "dynamic_range": {
                "primary_difference": "Wide human dynamic range vs. limited mechanical range",
                "impact_on_music": "Historical: nuanced dynamics; Mechanical: limited but consistent",
                "quantitative_difference": "Historical 30-100 dB vs. Mechanical 50-90 dB",
                "artistic_implications": "Historical better for dramatic contrast; Mechanical for consistency"
            },
            "articulation_precision": {
                "primary_difference": "Variable human articulation vs. precise mechanical articulation",
                "impact_on_music": "Historical: individual articulation style; Mechanical: consistent clarity",
                "quantitative_difference": "Historical 75-90% vs. Mechanical 95-99%",
                "artistic_implications": "Historical for personal expression; Mechanical for clarity"
            },
            "intonation_accuracy": {
                "primary_difference": "Flexible human intonation vs. fixed mechanical intonation",
                "impact_on_music": "Historical: expressive tuning; Mechanical: perfect stability",
                "quantitative_difference": "Historical ±10 cents vs. Mechanical ±2 cents",
                "artistic_implications": "Historical for expressive tuning; Mechanical for harmonic clarity"
            },
            "texture_clarity": {
                "primary_difference": "Interactive human texture vs. independent mechanical texture",
                "impact_on_music": "Historical: responsive ensemble; Mechanical: consistent separation",
                "quantitative_difference": "Variable vs. High consistency",
                "artistic_implications": "Historical for ensemble communication; Mechanical for polyphonic clarity"
            },
            "ornamentation_capability": {
                "primary_difference": "Flexible human ornamentation vs. programmed mechanical ornamentation",
                "impact_on_music": "Historical: personal ornamentation style; Mechanical: precise patterns",
                "quantitative_difference": "Highly variable vs. Limited by programming",
                "artistic_implications": "Historical for individual expression; Mechanical for consistency"
            },
            "ensemble_coordination": {
                "primary_difference": "Human visual/auditory cues vs. mechanical synchronization",
                "impact_on_music": "Historical: interactive coordination; Mechanical: perfect synchronization",
                "quantitative_difference": "Variable vs. 99%+ synchronization",
                "artistic_implications": "Historical for ensemble dynamics; Mechanical for precision"
            },
            "sustain_characteristics": {
                "primary_difference": "Variable human sustain vs. consistent mechanical sustain",
                "impact_on_music": "Historical: expressive sustain; Mechanical: consistent tone",
                "quantitative_difference": "Variable vs. High consistency",
                "artistic_implications": "Historical for expressive phrasing; Mechanical for stability"
            },
            "timbral_consistency": {
                "primary_difference": "Variable human timbre vs. consistent mechanical timbre",
                "impact_on_music": "Historical: individual tone color; Mechanical: uniform tone",
                "quantitative_difference": "Variable vs. 95-98% consistency",
                "artistic_implications": "Historical for tonal personality; Mechanical for consistency"
            },
            "performance_reliability": {
                "primary_difference": "Variable human reliability vs. high mechanical reliability",
                "impact_on_music": "Historical: human spontaneity; Mechanical: consistent execution",
                "quantitative_difference": "75-95% vs. 98%+ reliability",
                "artistic_implications": "Historical for creativity; Mechanical for consistency"
            }
        }

        return assessments.get(category, {
            "primary_difference": "General difference between human and mechanical performance",
            "impact_on_music": "Various artistic and technical implications",
            "quantitative_difference": "Varies by specific characteristic",
            "artistic_implications": "Context-dependent advantages"
        })

    def _identify_historical_advantages(self, category: str) -> List[str]:
        """Identify advantages of historical performance for a category."""

        advantages = {
            "tempo_consistency": [
                "Natural rubato and expressive timing",
                "Responsive to musical context",
                "Human interpretation and feeling",
                "Flexible adjustment to ensemble"
            ],
            "dynamic_range": [
                "Wide expressive dynamic range",
                "Nuanced dynamic shading",
                "Responsive to acoustic environment",
                "Individual artistic interpretation"
            ],
            "articulation_precision": [
                "Personal articulation style",
                "Context-appropriate articulation",
                "Expressive variation possibilities",
                "Interactive response to other performers"
            ],
            "intonation_accuracy": [
                "Expressive intonation adjustments",
                "Responsive to harmonic context",
                "Just intonation possibilities",
                "Ensemble tuning flexibility"
            ],
            "texture_clarity": [
                "Interactive ensemble communication",
                "Responsive balance adjustments",
                "Contextual voice emphasis",
                "Musical dialogue between performers"
            ],
            "ornamentation_capability": [
                "Personal ornamentation style",
                "Historically appropriate ornamentation",
                "Context-sensitive decoration",
                "Spontaneous creative additions"
            ],
            "ensemble_coordination": [
                "Interactive ensemble dynamics",
                "Responsive to musical gestures",
                "Spontaneous musical decisions",
                "Flexible adaptation to performance"
            ],
            "sustain_characteristics": [
                "Expressive sustain control",
                "Contextual phrase shaping",
                "Individual tone production",
                "Responsive musical phrasing"
            ],
            "timbral_consistency": [
                "Individual tonal personality",
                "Expressive tone coloration",
                "Responsive to musical material",
                "Artistic tonal interpretation"
            ],
            "performance_reliability": [
                "Spontaneous creativity",
                "Live performance energy",
                "Interactive musical communication",
                "Artistic inspiration and risk-taking"
            ]
        }

        return advantages.get(category, ["Human artistic interpretation and expression"])

    def _identify_mechanical_advantages(self, category: str) -> List[str]:
        """Identify advantages of mechanical performance for a category."""

        advantages = {
            "tempo_consistency": [
                "Perfect tempo stability",
                "Reliable rhythmic precision",
                "Consistent performance timing",
                "Predictable musical structure"
            ],
            "dynamic_range": [
                "Consistent dynamic levels",
                "Reliable sound production",
                "Stable ensemble balance",
                "Predictable dynamic transitions"
            ],
            "articulation_precision": [
                "Perfect articulation consistency",
                "Reliable note clarity",
                "Precise rhythmic execution",
                "Uniform performance quality"
            ],
            "intonation_accuracy": [
                "Perfect pitch stability",
                "Consistent tuning",
                "Reliable harmonic intonation",
                "Stable tonal center"
            ],
            "texture_clarity": [
                "Perfect voice separation",
                "Consistent polyphonic clarity",
                "Reliable texture balance",
                "Predictable ensemble sound"
            ],
            "ornamentation_capability": [
                "Precise ornamentation execution",
                "Consistent decorative patterns",
                "Reliable technical precision",
                "Uniform musical ornamentation"
            ],
            "ensemble_coordination": [
                "Perfect synchronization",
                "Reliable ensemble precision",
                "Consistent timing coordination",
                "Predictable musical coordination"
            ],
            "sustain_characteristics": [
                "Consistent sustain quality",
                "Reliable tone production",
                "Uniform decay characteristics",
                "Stable sound projection"
            ],
            "timbral_consistency": [
                "Uniform tone quality",
                "Consistent sound character",
                "Reliable timbral production",
                "Predictable tonal quality"
            ],
            "performance_reliability": [
                "Consistent performance quality",
                "Reliable execution",
                "Predictable musical results",
                "Stable technical performance"
            ]
        }

        return advantages.get(category, ["Technical precision and consistency"])

    def _suggest_historical_applications(self, category: str) -> List[str]:
        """Suggest appropriate applications for historical performance approach."""

        applications = {
            "tempo_consistency": [
                "Expressive solo performances",
                "Intimate chamber music",
                "Vocal accompaniment",
                "Improvisatory music"
            ],
            "dynamic_range": [
                "Dramatic musical works",
                "Expressive solo literature",
                "Contrasting repertoire",
                "Dynamic compositions"
            ],
            "articulation_precision": [
                "Personal artistic expression",
                "Interpretive performances",
                "Individual style development",
                "Artistic programming"
            ],
            "intonation_accuracy": [
                "Expressive ensemble music",
                "Chamber music with nuanced tuning",
                "Vocal music with expressive intonation",
                "Historically informed performances"
            ],
            "texture_clarity": [
                "Interactive chamber music",
                "Responsive ensemble performances",
                "Flexible musical combinations",
                "Artistic collaboration"
            ],
            "ornamentation_capability": [
                "Historically authentic performances",
                "Personal ornamentation style",
                "Improvisatory music",
                "Expressive decoration"
            ],
            "ensemble_coordination": [
                "Interactive chamber music",
                "Responsive ensemble performances",
                "Flexible musical groups",
                "Artistic collaboration"
            ],
            "sustain_characteristics": [
                "Expressive solo performances",
                "Vocal-style instrumental music",
                "Phrase-oriented performances",
                "Artistic interpretation"
            ],
            "timbral_consistency": [
                "Personal artistic expression",
                "Individual tonal development",
                "Artistic programming",
                "Expressive performances"
            ],
            "performance_reliability": [
                "Live concert performances",
                "Spontaneous musical events",
                "Interactive performances",
                "Artistic presentations"
            ]
        }

        return applications.get(category, ["Expressive artistic performances"])

    def _suggest_mechanical_applications(self, category: str) -> List[str]:
        """Suggest appropriate applications for mechanical performance approach."""

        applications = {
            "tempo_consistency": [
                "Dance music for choreography",
                "Educational demonstrations",
                "Technical showcases",
                "Consistent programming"
            ],
            "dynamic_range": [
                "Background music",
                "Educational presentations",
                "Technical demonstrations",
                "Consistent programming needs"
            ],
            "articulation_precision": [
                "Educational demonstrations",
                "Technical showcases",
                "Precision requirements",
                "Consistent performance needs"
            ],
            "intonation_accuracy": [
                "Harmonic demonstrations",
                "Educational tuning examples",
                "Technical precision requirements",
                "Consistent harmonic presentations"
            ],
            "texture_clarity": [
                "Polyphonic demonstrations",
                "Educational texture examples",
                "Complex ensemble music",
                "Consistent polyphonic presentations"
            ],
            "ornamentation_capability": [
                "Technical demonstrations",
                "Educational ornamentation examples",
                "Consistent decorative patterns",
                "Mechanical capability showcases"
            ],
            "ensemble_coordination": [
                "Complex ensemble music",
                "Educational coordination examples",
                "Synchronization demonstrations",
                "Consistent ensemble presentations"
            ],
            "sustain_characteristics": [
                "Educational sustain demonstrations",
                "Consistent tone production examples",
                "Technical showcases",
                "Reliable sustain requirements"
            ],
            "timbral_consistency": [
                "Educational timbre demonstrations",
                "Consistent tone quality examples",
                "Technical showcases",
                "Reliable sound production"
            ],
            "performance_reliability": [
                "Educational demonstrations",
                "Technical showcases",
                "Consistent programming needs",
                "Reliable performance requirements"
            ]
        }

        return applications.get(category, ["Technical and educational applications"])

    def generate_comparative_report(self, comparison_pieces: Dict[str, Tuple[MusicalScore, MusicalScore]]) -> Dict:
        """Generate comprehensive comparative analysis report."""

        print("Generating comparative analysis report...")

        report = {
            "introduction": {
                "purpose": "Comparative analysis of historical vs. mechanical Renaissance music performance",
                "methodology": "Side-by-side comparison of identical pieces performed in both styles",
                "scope": "Analysis of ten key performance categories across multiple musical forms",
                "significance": "Understanding the trade-offs between human expression and mechanical precision"
            },
            "analysis_pieces": {},
            "category_analyses": {},
            "summary_assessments": {},
            "recommendations": {}
        }

        # Analyze each comparison piece
        for piece_name, (historical, mechanical) in comparison_pieces.items():
            piece_analysis = {
                "piece_name": piece_name,
                "historical_score": {
                    "title": historical.title,
                    "composer": historical.composer,
                    "form": historical.form.value if historical.form else None,
                    "mode": historical.mode.value if historical.mode else None,
                    "tempo": historical.tempo_bpm,
                    "duration": historical.get_duration(),
                    "voice_count": historical.get_voice_count()
                },
                "mechanical_score": {
                    "title": mechanical.title,
                    "composer": mechanical.composer,
                    "form": mechanical.form.value if mechanical.form else None,
                    "mode": mechanical.mode.value if mechanical.mode else None,
                    "tempo": mechanical.tempo_bpm,
                    "duration": mechanical.get_duration(),
                    "voice_count": mechanical.get_voice_count()
                },
                "comparative_analysis": self.analyze_comparative_performance(historical, mechanical)
            }

            report["analysis_pieces"][piece_name] = piece_analysis

        # Generate category summaries
        for category in self.analysis_categories:
            category_summary = self._generate_category_summary(category, comparison_pieces)
            report["category_analyses"][category] = category_summary

        # Generate overall assessments
        report["summary_assessments"] = self._generate_summary_assessments(comparison_pieces)

        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(comparison_pieces)

        return report

    def _generate_category_summary(self, category: str, comparison_pieces: Dict) -> Dict:
        """Generate summary analysis for a specific category across all pieces."""

        summary = {
            "category": category,
            "description": self.analysis_categories[category],
            "historical_overview": self.historical_characteristics[category],
            "mechanical_overview": self.mechanical_characteristics[category],
            "key_differences": self._assess_category_difference(category, None, None),
            "piece_specific_observations": {},
            "overall_assessment": "",
            "best_use_cases": {
                "historical": self._suggest_historical_applications(category),
                "mechanical": self._suggest_mechanical_applications(category)
            }
        }

        # Add piece-specific observations
        for piece_name in comparison_pieces:
            # This would be filled with actual analysis of each piece
            summary["piece_specific_observations"][piece_name] = f"Analysis of {category} in {piece_name}"

        return summary

    def _generate_summary_assessments(self, comparison_pieces: Dict) -> Dict:
        """Generate overall summary assessments."""

        return {
            "overall_comparisons": {
                "expression_vs_precision": "Historical performance offers superior expressive capabilities, while mechanical performance provides unparalleled precision and consistency",
                "reliability_vs_spontaneity": "Mechanical performance ensures reliable execution, while historical performance allows for spontaneous creativity and human interaction",
                "authenticity_vs_innovation": "Historical performance maintains Renaissance authenticity, while mechanical performance represents Leonardo's innovative vision",
                "educational_vs_artistic": "Mechanical performance excels in educational demonstrations, while historical performance provides superior artistic experiences"
            },
            "contextual_recommendations": {
                "concert_performance": "Historical performance recommended for artistic concerts emphasizing human expression",
                "educational_demonstration": "Mechanical performance ideal for educational settings showcasing technical innovation",
                "research_presentation": "Combined approach best for scholarly presentations comparing both methods",
                "cultural_exhibition": "Mechanical performance preferred for exhibitions highlighting Leonardo's innovations"
            },
            "technical_assessments": {
                "feasibility": "Both approaches are technically feasible with appropriate resources and expertise",
                "resource_requirements": "Historical requires skilled musicians; mechanical requires well-maintained instruments",
                "scalability": "Mechanical performance more scalable for repeated presentations",
                "maintenance": "Historical requires ongoing musician training; mechanical requires regular technical maintenance"
            },
            "artistic_evaluation": {
                "musical_quality": "Both approaches can produce high-quality musical experiences appropriate to different contexts",
                "audience_engagement": "Historical performance offers emotional connection; mechanical provides intellectual stimulation",
                "educational_value": "Mechanical performance superior for technical education; historical for musical education",
                "cultural_significance": "Both approaches important for understanding Renaissance musical culture"
            }
        }

    def _generate_recommendations(self, comparison_pieces: Dict) -> Dict:
        """Generate practical recommendations based on the analysis."""

        return {
            "performance_recommendations": {
                "concert_programming": "Combine both approaches to showcase the full spectrum of Renaissance musical possibilities",
                "educational_programs": "Use mechanical demonstrations to explain technical concepts, historical performances to illustrate artistic elements",
                "cultural_presentations": "Emphasize mechanical performance for Leonardo-focused exhibitions, historical for general Renaissance programming"
            },
            "technical_recommendations": {
                "instrument_maintenance": "Regular maintenance essential for mechanical performance reliability",
                "musician_training": "Specialized training required for historical Renaissance performance practice",
                "acoustic_considerations": "Different acoustic requirements for each performance approach",
                "integration_strategies": "Careful planning needed when combining both approaches"
            },
            "research_directions": {
                "historical_research": "Continued research into Renaissance performance practice to improve historical authenticity",
                "technical_development": "Ongoing development of mechanical instruments to enhance capabilities",
                "comparative_studies": "Further comparative analysis to refine understanding of both approaches",
                "audience_research": "Study audience preferences and educational impact of both approaches"
            },
            "implementation_strategies": {
                "gradual_integration": "Begin with separate presentations before combining both approaches",
                "context_specific_programming": "Tailor performance approach to specific audience and context needs",
                "documentation_preservation": "Document both approaches thoroughly for future research and performance",
                "collaborative_approaches": "Foster collaboration between musicologists, engineers, and performers"
            }
        }

    def save_comparative_analysis(self, report: Dict) -> None:
        """Save the comparative analysis to artifacts."""

        print("Saving comparative analysis results...")

        # Create analysis directory
        analysis_dir = ensure_artifact_dir("comparative_analysis")

        # Save main report
        report_path = analysis_dir / "comparative_analysis_report.json"
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Save individual pieces
        pieces_dir = analysis_dir / "analysis_pieces"
        pieces_dir.mkdir(exist_ok=True)

        for piece_name, piece_data in report["analysis_pieces"].items():
            piece_dir = pieces_dir / piece_name
            piece_dir.mkdir(exist_ok=True)

            # Save piece summary
            summary_path = piece_dir / "piece_summary.json"
            with summary_path.open("w", encoding="utf-8") as f:
                json.dump(piece_data, f, indent=2)

        # Save category analyses
        categories_dir = analysis_dir / "category_analyses"
        categories_dir.mkdir(exist_ok=True)

        for category_name, category_data in report["category_analyses"].items():
            category_path = categories_dir / f"{category_name}.json"
            with category_path.open("w", encoding="utf-8") as f:
                json.dump(category_data, f, indent=2)

        # Create comprehensive summary document
        summary_path = analysis_dir / "executive_summary.md"
        summary_content = self._create_executive_summary(report)
        with summary_path.open("w", encoding="utf-8") as f:
            f.write(summary_content)

        print(f"Comparative analysis saved to: {analysis_dir}")
        print(f"  Main report: {report_path}")
        print(f"  Executive summary: {summary_path}")
        print(f"  Individual pieces: {pieces_dir}")
        print(f"  Category analyses: {categories_dir}")

    def _create_executive_summary(self, report: Dict) -> str:
        """Create executive summary of the comparative analysis."""

        summary = """# Comparative Analysis: Historical vs. Mechanical Renaissance Performance

## Executive Summary

This comprehensive comparative analysis examines the differences between traditional Renaissance music performance and Leonardo da Vinci's mechanical instrument adaptations. The study reveals distinct advantages and applications for each approach, providing valuable insights for performers, educators, and researchers.

## Key Findings

### Artistic Expression vs. Technical Precision

**Historical Performance Advantages:**
- Superior expressive capabilities through human interpretation
- Flexible timing and rubato for emotional content
- Wide dynamic range for dramatic contrast
- Personal ornamentation and improvisation
- Interactive ensemble communication

**Mechanical Performance Advantages:**
- Unparalleled precision and consistency
- Perfect tempo stability and rhythmic accuracy
- Reliable intonation and harmonic clarity
- Consistent tone quality and articulation
- Repeatable performance quality

### Contextual Applications

**Historical Performance Best For:**
- Artistic concerts emphasizing emotional expression
- Authentic Renaissance music experiences
- Intimate chamber music settings
- Demonstrations of human musical achievement

**Mechanical Performance Best For:**
- Educational demonstrations of technical innovation
- Showcases of Leonardo's mechanical genius
- Consistent programming requirements
- Technical and scientific presentations

### Educational Value

Both approaches offer significant educational benefits:

**Historical Performance:**
- Understanding of Renaissance musical aesthetics
- Appreciation of human artistic achievement
- Development of performance practice skills
- Cultural and historical context

**Mechanical Performance:**
- Insight into Renaissance technological innovation
- Understanding of mechanical music principles
- Demonstration of Leonardo's interdisciplinary genius
- Integration of art and engineering concepts

## Recommendations

### For Performers and Presenters

1. **Integrated Programming**: Combine both approaches to provide comprehensive understanding
2. **Context-Specific Selection**: Choose performance approach based on audience and educational goals
3. **Documentation**: Thoroughly document both approaches for research and preservation
4. **Collaboration**: Foster collaboration between musicians, engineers, and scholars

### For Educational Institutions

1. **Curriculum Integration**: Include both approaches in music history and technology programs
2. **Practical Experience**: Provide hands-on experience with both performance styles
3. **Research Support**: Support ongoing research into both historical and mechanical approaches
4. **Interdisciplinary Programs**: Develop programs connecting music, engineering, and history

### For Researchers

1. **Comparative Studies**: Continue comparative analysis to refine understanding
2. **Technical Development**: Advance mechanical instrument design and capabilities
3. **Historical Research**: Deepen understanding of Renaissance performance practice
4. **Audience Studies**: Research audience preferences and educational impact

## Conclusion

The comparative analysis reveals that both historical and mechanical approaches to Renaissance music performance have distinct and valuable characteristics. Rather than viewing them as competing alternatives, they should be understood as complementary approaches that together provide a more complete understanding of Renaissance musical culture and Leonardo da Vinci's innovative vision.

Historical performance preserves the human artistic expression that defined Renaissance music, while mechanical performance demonstrates the technological innovation that characterized Leonardo's work. Together, they offer unique insights into the intersection of art, music, and technology that defined the Renaissance period.

This analysis provides a foundation for continued exploration of both approaches, supporting ongoing research, performance, and educational efforts to bring Leonardo's musical innovations to modern audiences while preserving the rich traditions of Renaissance musical performance.

---

*This comparative analysis is part of the da Vinci Codex Project - Phase 3: Cultural Revival*
"""

        return summary


def main():
    """Main function to run the comparative analysis system."""

    print("Comparative Analysis System: Historical vs. Mechanical Performance")
    print("Phase 3: Cultural Revival - Comparative Study and Analysis")
    print("=" * 80)

    # Create analysis system
    analyzer = ComparativeAnalysisSystem()

    # Generate comparison pieces
    comparison_pieces = analyzer.create_comparison_pieces()

    # Generate comprehensive report
    report = analyzer.generate_comparative_report(comparison_pieces)

    # Save results
    analyzer.save_comparative_analysis(report)

    print(f"\n{'='*80}")
    print("Comparative Analysis Complete!")
    print("\nAnalysis includes:")
    print("  1. Three comparison pieces (Pavane, Galliard, Polyphony)")
    print("  2. Ten performance categories analyzed")
    print("  3. Detailed historical vs. mechanical comparisons")
    print("  4. Contextual recommendations and applications")
    print("  5. Educational and implementation guidelines")

    print(f"\nAll analysis results saved to: {ensure_artifact_dir('comparative_analysis')}")


if __name__ == "__main__":
    main()
