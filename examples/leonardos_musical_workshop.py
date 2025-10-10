#!/usr/bin/env python3
"""
Leonardo's Musical Workshop - Individual Instrument Demonstrations
Phase 3: Cultural Revival - Technical Analysis and Demonstrations

This program creates detailed demonstrations of each of Leonardo's mechanical
instruments, showcasing their unique capabilities, technical innovations,
and musical characteristics with comprehensive technical explanations.
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
)
from davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


class LeonardosMusicalWorkshop:
    """Interactive demonstration of Leonardo's mechanical instruments."""

    def __init__(self):
        """Initialize the musical workshop."""
        self.integrator = MechanicalEnsembleIntegrator()
        self.composer = RenaissanceCompositionGenerator()

        # Define technical characteristics for each instrument
        self.instrument_profiles = {
            InstrumentType.VIOLA_ORGANISTA: {
                "name": "Viola Organista",
                "invention_date": "c. 1490",
                "codex_reference": "Codex Atlanticus, folio 899r",
                "description": "A bowed keyboard instrument combining the sustain of an organ with the expressive tone of a viola da gamba.",
                "mechanism": "Keyboard action pushes spinning wheels (rosined cylinders) against strings, creating continuous bowing action.",
                "range": "C3-G6 (130.81-1568.0 Hz)",
                "unique_features": [
                    "Continuous sustain without manual bowing",
                    "Dynamic control through keyboard pressure",
                    "Polyphonic capability unlike traditional viols",
                    "Organ-like sustain with string timbre"
                ],
                "historical_context": "Leonardo's solution to the challenge of creating sustained polyphonic string music. This instrument would have revolutionized ensemble music.",
                "technical_challenges": [
                    "Precise wheel rosin application for consistent tone",
                    "String tension and wheel pressure calibration",
                    "Keyboard action mechanism complexity",
                    "Maintaining intonation across the range"
                ]
            },
            InstrumentType.MECHANICAL_ORGAN: {
                "name": "Mechanical Organ",
                "invention_date": "c. 1485-1490",
                "codex_reference": "Codex Atlanticus, folios 20r, 21r",
                "description": "An automated pipe organ with programmable music using pinned barrels and complex windchest design.",
                "mechanism": "Pinned wooden cylinders control valve actions, directing air to specific pipes. Wind pressure regulated by water-weight bellows.",
                "range": "C2-C7 (65.41-2093.0 Hz)",
                "unique_features": [
                    "Automated performance without human intervention",
                    "Complex polyphonic capability",
                    "Dynamic registration control",
                    "Programmable music sequences"
                ],
                "historical_context": "Part of Leonardo's broader interest in automation and mechanical music. Would have provided entertainment for Sforza court gatherings.",
                "technical_challenges": [
                    "Precise pin placement on barrels",
                    "Windchest leak prevention",
                    "Pipe tuning stability",
                    "Bellows pressure regulation"
                ]
            },
            InstrumentType.PROGRAMMABLE_FLUTE: {
                "name": "Programmable Flute",
                "invention_date": "c. 1488",
                "codex_reference": "Codex Atlanticus, folio 742r",
                "description": "A mechanical flute system with automated finger holes and breath control, capable of complex melodic passages.",
                "mechanism": "Cam-driven mechanisms cover and uncover tone holes, while bellows provide controlled air pressure. Complex linkage system for rapid fingering.",
                "range": "C4-G6 (261.63-1568.0 Hz)",
                "unique_features": [
                    "Rapid fingering beyond human capability",
                    "Precise breath control",
                    "Complex ornamentation capability",
                    "Consistent tone production"
                ],
                "historical_context": "Leonardo's exploration of wind instrument automation, inspired by the popularity of flute music in Renaissance courts.",
                "technical_challenges": [
                    "Precise hole sealing for clean tone",
                    "Breath pressure modulation",
                    "Cam profile design for musical phrasing",
                    "Material selection for durability"
                ]
            },
            InstrumentType.MECHANICAL_TRUMPETER: {
                "name": "Mechanical Trumpeter",
                "invention_date": "c. 1495",
                "codex_reference": "Codex Atlanticus, folio 1085r",
                "description": "An automated brass instrument with mechanical lips and slide positioning, capable of fanfares and calls.",
                "mechanism": "Articulated mechanical lips create vibration, while adjustable slide mechanism changes pitch. Air supplied by regulated bellows.",
                "range": "E3-B5 (164.81-987.77 Hz)",
                "unique_features": [
                    "Mechanical lip vibration simulation",
                    "Dynamic control through pressure variation",
                    "Rapid articulation capability",
                    "Fanfare and military call patterns"
                ],
                "historical_context": "Designed for military and ceremonial use, reflecting Leonardo's work on military engineering for the Sforza court.",
                "technical_challenges": [
                    "Lip material and vibration characteristics",
                    "Slide mechanism precision",
                    "Air pressure and lip synchronization",
                    "Timbre quality optimization"
                ]
            },
            InstrumentType.MECHANICAL_DRUM: {
                "name": "Mechanical Drum",
                "invention_date": "c. 1490",
                "codex_reference": "Codex Atlanticus, folio 844r",
                "description": "A percussion system with multiple drumheads and automated striking mechanisms for rhythmic patterns.",
                "mechanism": "Cam-driven beaters strike tuned drumheads with precise timing. Multiple drum sizes provide pitch variation.",
                "range": "80-400 Hz (fundamental frequencies)",
                "unique_features": [
                    "Complex polyrhythmic capability",
                    "Multiple drum sizes for pitch variety",
                    "Programmable rhythmic patterns",
                    "Consistent strike force"
                ],
                "historical_context": "Essential for dance music and military applications, demonstrating Leonardo's understanding of rhythm and movement.",
                "technical_challenges": [
                    "Drumhead tension and tuning",
                    "Beater material and rebound characteristics",
                    "Cam design for rhythmic patterns",
                    "Multiple drum coordination"
                ]
            },
            InstrumentType.MECHANICAL_CARILLON: {
                "name": "Mechanical Carillon",
                "invention_date": "c. 1493",
                "codex_reference": "Codex Madrid I, folio 140r",
                "description": "A bell ensemble with automated striking mechanism, capable of harmonic progression and melody.",
                "mechanism": "Large bells struck by hammers controlled by pinned barrels. Multiple bell sizes provide full harmonic range.",
                "range": "G2-G7 (196.0-3920.0 Hz)",
                "unique_features": [
                    "Full harmonic and melodic capability",
                    "Sustained resonance for harmonic support",
                    "Powerful projection for outdoor use",
                    "Complex polyphonic music"
                ],
                "historical_context": "Designed for civic and religious buildings, representing Leonardo's interest in public art and urban design.",
                "technical_challenges": [
                    "Bell casting and tuning precision",
                    "Hammer striking force optimization",
                    "Resonance management",
                    "Structural support for large bells"
                ]
            }
        }

    def create_instrument_demonstration(self, instrument_type: InstrumentType) -> Dict:
        """Create a comprehensive demonstration for a specific instrument."""

        profile = self.instrument_profiles[instrument_type]

        # Create demonstration pieces for the instrument
        print(f"\nCreating demonstration for {profile['name']}...")

        # Generate multiple demonstration pieces
        demonstrations = []

        # 1. Technical capability demonstration
        technical_demo = self._create_technical_demonstration(instrument_type)
        demonstrations.append(("Technical Capabilities", technical_demo))

        # 2. Renaissance-style performance
        renaissance_demo = self._create_renaissance_demonstration(instrument_type)
        demonstrations.append(("Renaissance Performance", renaissance_demo))

        # 3. Extended technique demonstration
        extended_demo = self._create_extended_technique_demonstration(instrument_type)
        demonstrations.append(("Extended Techniques", extended_demo))

        # Analyze acoustic properties
        acoustic_analysis = self._analyze_acoustic_properties(instrument_type)

        return {
            "profile": profile,
            "demonstrations": demonstrations,
            "acoustic_analysis": acoustic_analysis
        }

    def _create_technical_demonstration(self, instrument_type: InstrumentType) -> MusicalScore:
        """Create a technical demonstration showcasing instrument capabilities."""

        profile = self.instrument_profiles[instrument_type]

        score = MusicalScore(
            title=f"{profile['name']} - Technical Capabilities",
            composer="Leonardo da Vinci (mechanical demonstration)",
            mode=RenaissanceMode.DORIAN,
            form=MusicalForm.FANTASIA,
            tempo_bpm=100.0
        )

        # Create technical demonstration voice
        voice = Voice(name="Technical Demonstration", instrument=instrument_type)

        # Get instrument range from profile
        if instrument_type == InstrumentType.VIOLA_ORGANISTA:
            notes = self._create_viola_organista_tech_demo()
        elif instrument_type == InstrumentType.MECHANICAL_ORGAN:
            notes = self._create_organ_tech_demo()
        elif instrument_type == InstrumentType.PROGRAMMABLE_FLUTE:
            notes = self._create_flute_tech_demo()
        elif instrument_type == InstrumentType.MECHANICAL_TRUMPETER:
            notes = self._create_trumpet_tech_demo()
        elif instrument_type == InstrumentType.MECHANICAL_DRUM:
            notes = self._create_drum_tech_demo()
        elif instrument_type == InstrumentType.MECHANICAL_CARILLON:
            notes = self._create_carillon_tech_demo()

        for note in notes:
            voice.add_note(note)

        score.add_voice(voice)
        return score

    def _create_renaissance_demonstration(self, instrument_type: InstrumentType) -> MusicalScore:
        """Create a Renaissance-style piece for the instrument."""

        profile = self.instrument_profiles[instrument_type]

        # Choose appropriate form based on instrument
        if instrument_type in [InstrumentType.VIOLA_ORGANISTA, InstrumentType.PROGRAMMABLE_FLUTE]:
            form = MusicalForm.PAVANE
            mode = RenaissanceMode.LYDIAN
        elif instrument_type == InstrumentType.MECHANICAL_TRUMPETER:
            form = MusicalForm.GALLIARD
            mode = RenaissanceMode.MIXOLYDIAN
        else:
            form = MusicalForm.BASSE_DANSE
            mode = RenaissanceMode.DORIAN

        score = MusicalScore(
            title=f"{profile['name']} - Renaissance Performance",
            composer="Leonardo da Vinci (Renaissance style)",
            mode=mode,
            form=form,
            tempo_bpm=90.0 if form != MusicalForm.GALLIARD else 120.0
        )

        # Generate Renaissance-style music for the instrument
        voice = Voice(name="Renaissance Performance", instrument=instrument_type)

        # Generate appropriate notes for the instrument and form
        notes = self._generate_renaissance_notes(instrument_type, form, mode)

        for note in notes:
            voice.add_note(note)

        score.add_voice(voice)
        return score

    def _create_extended_technique_demonstration(self, instrument_type: InstrumentType) -> MusicalScore:
        """Create demonstration of extended techniques and capabilities."""

        profile = self.instrument_profiles[instrument_type]

        score = MusicalScore(
            title=f"{profile['name']} - Extended Techniques",
            composer="Leonardo da Vinci (extended techniques)",
            mode=RenaissanceMode.PHRYGIAN,
            form=MusicalForm.FANTASIA,
            tempo_bpm=80.0
        )

        voice = Voice(name="Extended Techniques", instrument=instrument_type)

        # Create extended technique demonstration
        notes = self._generate_extended_technique_notes(instrument_type)

        for note in notes:
            voice.add_note(note)

        score.add_voice(voice)
        return score

    def _create_viola_organista_tech_demo(self) -> List[Note]:
        """Create technical demonstration for viola organista."""
        notes = []
        current_time = 0.0

        # Showcase sustain capability
        sustained_note = Note(
            pitch=440.0,  # A4
            duration=4.0,  # 4 second sustain
            velocity=0.8,
            start_time=current_time,
            voice=0
        )
        notes.append(sustained_note)
        current_time += 4.0

        # Showcase polyphonic capability
        chord_notes = [440.0, 554.37, 659.25]  # A major chord
        for pitch in chord_notes:
            chord_note = Note(
                pitch=pitch,
                duration=2.0,
                velocity=0.7,
                start_time=current_time,
                voice=0
            )
            notes.append(chord_note)
        current_time += 2.0

        # Showcase dynamic range
        for velocity in [0.3, 0.5, 0.7, 0.9]:
            dynamic_note = Note(
                pitch=523.25,  # C5
                duration=0.5,
                velocity=velocity,
                start_time=current_time,
                voice=0
            )
            notes.append(dynamic_note)
            current_time += 0.5

        return notes

    def _create_organ_tech_demo(self) -> List[Note]:
        """Create technical demonstration for mechanical organ."""
        notes = []
        current_time = 0.0

        # Showcase full range
        range_pitches = [130.81, 261.63, 523.25, 1046.5, 2093.0]  # C3 to C7
        for pitch in range_pitches:
            range_note = Note(
                pitch=pitch,
                duration=1.0,
                velocity=0.7,
                start_time=current_time,
                voice=0
            )
            notes.append(range_note)
            current_time += 1.0

        # Showcase polyphonic texture
        # Create a four-part chord progression
        progressions = [
            [261.63, 329.63, 392.00, 523.25],  # C major
            [293.66, 369.99, 440.00, 587.33],  # D minor
            [329.63, 415.30, 493.88, 659.25],  # E minor
            [261.63, 329.63, 392.00, 523.25],  # C major
        ]

        for chord in progressions:
            for pitch in chord:
                chord_note = Note(
                    pitch=pitch,
                    duration=2.0,
                    velocity=0.6,
                    start_time=current_time,
                    voice=0
                )
                notes.append(chord_note)
            current_time += 2.0

        return notes

    def _create_flute_tech_demo(self) -> List[Note]:
        """Create technical demonstration for programmable flute."""
        notes = []
        current_time = 0.0

        # Showcase rapid passage capability
        rapid_pitches = [523.25, 587.33, 659.25, 698.46, 783.99]  # C5-G5
        for pitch in rapid_pitches * 2:  # Play twice
            rapid_note = Note(
                pitch=pitch,
                duration=0.2,  # Very fast notes
                velocity=0.7,
                start_time=current_time,
                voice=0
            )
            notes.append(rapid_note)
            current_time += 0.2

        # Showcase ornamentation
        base_pitch = 440.0  # A4
        ornament_patterns = [
            (base_pitch, 0.8, 0.0),      # Main note
            (base_pitch * 1.06, 0.1, 0.8),  # Trill up
            (base_pitch, 0.1, 0.9),      # Back to main
            (base_pitch * 0.94, 0.1, 1.0),  # Trill down
            (base_pitch, 0.8, 1.1),      # Main note
        ]

        for pitch, duration, start_offset in ornament_patterns:
            ornament_note = Note(
                pitch=pitch,
                duration=duration,
                velocity=0.7,
                start_time=current_time + start_offset,
                voice=0
            )
            notes.append(ornament_note)

        return notes

    def _create_trumpet_tech_demo(self) -> List[Note]:
        """Create technical demonstration for mechanical trumpeter."""
        notes = []
        current_time = 0.0

        # Showcase fanfare patterns
        fanfare_pattern = [
            (440.0, 0.5),   # A4
            (554.37, 0.5),  # C#5
            (659.25, 1.0),  # E5
            (554.37, 0.5),  # C#5
            (440.0, 1.0),   # A4
        ]

        for pitch, duration in fanfare_pattern:
            fanfare_note = Note(
                pitch=pitch,
                duration=duration,
                velocity=0.8,
                start_time=current_time,
                voice=0
            )
            notes.append(fanfare_note)
            current_time += duration

        # Showcase dynamic fanfare
        for i in range(3):
            dynamic_pitch = 523.25 + i * 100  # Ascending pattern
            dynamic_note = Note(
                pitch=dynamic_pitch,
                duration=0.5,
                velocity=0.9 - i * 0.2,  # Decreasing dynamics
                start_time=current_time,
                voice=0
            )
            notes.append(dynamic_note)
            current_time += 0.5

        return notes

    def _create_drum_tech_demo(self) -> List[Note]:
        """Create technical demonstration for mechanical drum."""
        notes = []
        current_time = 0.0

        # Showcase rhythmic patterns
        rhythmic_patterns = [
            (150.0, 0.5),  # Low drum
            (200.0, 0.5),  # Medium drum
            (250.0, 0.5),  # High drum
            (200.0, 0.5),  # Medium drum
            (150.0, 1.0),  # Low drum
        ]

        for pitch, duration in rhythmic_patterns * 2:  # Repeat pattern
            rhythm_note = Note(
                pitch=pitch,
                duration=duration,
                velocity=0.8,
                start_time=current_time,
                voice=0
            )
            notes.append(rhythm_note)
            current_time += duration

        # Showcase polyrhythm
        polyrhythm_notes = [
            (150.0, 1.0),  # Low - whole note
            (200.0, 0.5),  # Medium - half note
            (250.0, 0.25), # High - quarter note
            (250.0, 0.25), # High - quarter note
            (200.0, 0.5),  # Medium - half note
        ]

        for pitch, duration in polyrhythm_notes:
            poly_note = Note(
                pitch=pitch,
                duration=duration,
                velocity=0.7,
                start_time=current_time,
                voice=0
            )
            notes.append(poly_note)
            current_time += duration

        return notes

    def _create_carillon_tech_demo(self) -> List[Note]:
        """Create technical demonstration for mechanical carillon."""
        notes = []
        current_time = 0.0

        # Showcase harmonic progression
        harmonic_progression = [
            [392.00, 493.88, 659.25],  # G major chord
            [349.23, 440.00, 554.37],  # F major chord
            [440.00, 554.37, 698.46],  # A minor chord
            [392.00, 493.88, 659.25],  # G major chord
        ]

        for chord in harmonic_progression:
            # Add resonance by staggering the chord notes slightly
            for i, pitch in enumerate(chord):
                chord_note = Note(
                    pitch=pitch,
                    duration=3.0,  # Long sustain for resonance
                    velocity=0.7 - i * 0.1,  # Slight dynamic variation
                    start_time=current_time + i * 0.1,  # Staggered attack
                    voice=0
                )
                notes.append(chord_note)
            current_time += 3.0

        # Showcase melody with harmony
        melody = [440.00, 493.88, 523.25, 587.33, 659.25, 587.33, 523.25, 493.88]
        harmony = [220.00, 246.94, 261.63, 293.66, 329.63, 293.66, 261.63, 246.94]

        for _i, (mel_pitch, harm_pitch) in enumerate(zip(melody, harmony)):
            # Melody note
            melody_note = Note(
                pitch=mel_pitch,
                duration=0.5,
                velocity=0.8,
                start_time=current_time,
                voice=0
            )
            notes.append(melody_note)

            # Harmony note
            harmony_note = Note(
                pitch=harm_pitch,
                duration=1.0,
                velocity=0.6,
                start_time=current_time,
                voice=0
            )
            notes.append(harmony_note)

            current_time += 0.5

        return notes

    def _generate_renaissance_notes(self, instrument_type: InstrumentType, form: MusicalForm, mode: RenaissanceMode) -> List[Note]:
        """Generate Renaissance-style notes for an instrument."""
        notes = []
        current_time = 0.0

        # Define scale for the mode
        mode_scales = {
            RenaissanceMode.DORIAN: [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25],
            RenaissanceMode.LYDIAN: [329.63, 369.99, 415.30, 440.00, 493.88, 554.37, 622.25, 659.25],
            RenaissanceMode.MIXOLYDIAN: [392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 739.99, 783.99],
            RenaissanceMode.PHRYGIAN: [293.66, 311.13, 349.23, 369.99, 415.30, 440.00, 493.88, 554.37],
        }

        scale = mode_scales.get(mode, mode_scales[RenaissanceMode.DORIAN])

        # Generate Renaissance melody based on form
        if form == MusicalForm.PAVANE:
            # Slow, stately melody
            for i in range(16):
                if i % 4 == 0:
                    pitch = scale[0]  # Tonic
                    duration = 1.0
                elif i % 4 == 1:
                    pitch = scale[2]  # Mediant
                    duration = 1.0
                elif i % 4 == 2:
                    pitch = scale[4]  # Dominant
                    duration = 1.0
                else:
                    pitch = scale[0]  # Tonic
                    duration = 1.0

                note = Note(
                    pitch=pitch,
                    duration=duration,
                    velocity=0.7,
                    start_time=current_time,
                    voice=0
                )
                notes.append(note)
                current_time += duration

        elif form == MusicalForm.GALLIARD:
            # Lively triple meter
            for i in range(12):
                if i % 3 == 0:
                    pitch = scale[0]  # Tonic
                    duration = 0.5
                elif i % 3 == 1:
                    pitch = scale[2]  # Mediant
                    duration = 0.25
                else:
                    pitch = scale[4]  # Dominant
                    duration = 0.25

                note = Note(
                    pitch=pitch,
                    duration=duration,
                    velocity=0.8,
                    start_time=current_time,
                    voice=0
                )
                notes.append(note)
                current_time += duration

        else:  # BASSE_DANSE
            # Processional style
            for i in range(12):
                pitch = scale[i % len(scale)]
                duration = 0.8

                note = Note(
                    pitch=pitch,
                    duration=duration,
                    velocity=0.7,
                    start_time=current_time,
                    voice=0
                )
                notes.append(note)
                current_time += duration

        return notes

    def _generate_extended_technique_notes(self, instrument_type: InstrumentType) -> List[Note]:
        """Generate extended technique demonstrations for an instrument."""
        notes = []
        current_time = 0.0

        # Different extended techniques based on instrument
        if instrument_type == InstrumentType.VIOLA_ORGANISTA:
            # Showcase continuous bowing with dynamic variation
            base_pitch = 440.0
            for i in range(8):
                dynamic = 0.4 + (i * 0.075)  # Gradual crescendo
                note = Note(
                    pitch=base_pitch,
                    duration=1.0,
                    velocity=dynamic,
                    start_time=current_time,
                    voice=0
                )
                notes.append(note)
                current_time += 1.0

        elif instrument_type == InstrumentType.PROGRAMMABLE_FLUTE:
            # Showcase extreme rapid passages
            base_pitch = 523.25
            for i in range(16):
                pitch = base_pitch * (1 + (i % 4) * 0.06)  # Small variations
                note = Note(
                    pitch=pitch,
                    duration=0.125,  # Very fast
                    velocity=0.7,
                    start_time=current_time,
                    voice=0
                )
                notes.append(note)
                current_time += 0.125

        else:
            # Generic extended technique - wide range and dynamics
            if instrument_type == InstrumentType.MECHANICAL_DRUM:
                pitches = [150, 200, 250, 300, 350, 400]
            elif instrument_type == InstrumentType.MECHANICAL_CARILLON:
                pitches = [392, 523, 659, 784, 988, 1175]
            else:
                pitches = [200, 300, 400, 500, 600, 700]

            for pitch in pitches:
                note = Note(
                    pitch=pitch,
                    duration=0.5,
                    velocity=0.8,
                    start_time=current_time,
                    voice=0
                )
                notes.append(note)
                current_time += 0.5

        return notes

    def _analyze_acoustic_properties(self, instrument_type: InstrumentType) -> Dict:
        """Analyze acoustic properties of the instrument."""
        self.instrument_profiles[instrument_type]

        # Simulate acoustic analysis based on instrument characteristics
        if instrument_type == InstrumentType.VIOLA_ORGANISTA:
            return {
                "fundamental_range": "130.81-1568.0 Hz",
                "harmonic_content": "Rich string harmonics with organ-like sustain",
                "attack_time": "0.1-0.2 seconds (wheel engagement)",
                "decay_characteristics": "Very slow decay - characteristic of bowed strings",
                "timbre_description": "Warm, mellow tone with string complexity and organ sustain",
                "dynamic_range": "50-90 dB",
                "resonance_peaks": "String resonances at harmonic intervals",
                "special_characteristics": "Continuous sustain without vibrato decay"
            }
        elif instrument_type == InstrumentType.MECHANICAL_ORGAN:
            return {
                "fundamental_range": "65.41-2093.0 Hz",
                "harmonic_content": "Complex pipe harmonics with wind chest resonance",
                "attack_time": "0.05-0.1 seconds (valve opening)",
                "decay_characteristics": "Moderate decay dependent on pipe size",
                "timbre_description": "Clear, bright tone with pipe organ character",
                "dynamic_range": "60-100 dB",
                "resonance_peaks": "Pipe resonances with room interaction",
                "special_characteristics": "Polyphonic capability with registration control"
            }
        elif instrument_type == InstrumentType.PROGRAMMABLE_FLUTE:
            return {
                "fundamental_range": "261.63-1568.0 Hz",
                "harmonic_content": "Air column harmonics with breath noise components",
                "attack_time": "0.02-0.05 seconds (quick articulation)",
                "decay_characteristics": "Fast decay without continuous breath support",
                "timbre_description": "Bright, focused tone with air noise component",
                "dynamic_range": "40-80 dB",
                "resonance_peaks": "Air column resonances with tone hole effects",
                "special_characteristics": "Rapid articulation beyond human capability"
            }
        elif instrument_type == InstrumentType.MECHANICAL_TRUMPETER:
            return {
                "fundamental_range": "164.81-987.77 Hz",
                "harmonic_content": "Brass harmonics with lip vibration characteristics",
                "attack_time": "0.03-0.08 seconds (lip engagement)",
                "decay_characteristics": "Moderate decay with bell radiation",
                "timbre_description": "Brassy, bright tone with mechanical lip character",
                "dynamic_range": "70-110 dB",
                "resonance_peaks": "Brass resonances with mouthpiece effects",
                "special_characteristics": "Mechanical lip simulation with fanfare capability"
            }
        elif instrument_type == InstrumentType.MECHANICAL_DRUM:
            return {
                "fundamental_range": "80-400 Hz",
                "harmonic_content": "Membrane harmonics with body resonance",
                "attack_time": "0.01-0.02 seconds (instantaneous impact)",
                "decay_characteristics": "Exponential decay dependent on drum size",
                "timbre_description": "Percussive attack with resonant body tone",
                "dynamic_range": "80-120 dB",
                "resonance_peaks": "Membrane modes with cavity resonance",
                "special_characteristics": "Programmable rhythmic patterns with multiple drum sizes"
            }
        else:  # MECHANICAL_CARILLON
            return {
                "fundamental_range": "196.0-3920.0 Hz",
                "harmonic_content": "Bell harmonics with complex overtone structure",
                "attack_time": "0.05-0.15 seconds (hammer impact and bell resonance)",
                "decay_characteristics": "Very long decay characteristic of bells",
                "timbre_description": "Rich, complex tone with bell harmonics and long sustain",
                "dynamic_range": "90-130 dB",
                "resonance_peaks": "Bell partials with clang tone components",
                "special_characteristics": "Long resonance suitable for harmonic support"
            }

    def generate_workshop_presentations(self) -> Dict[str, Dict]:
        """Generate complete workshop presentations for all instruments."""

        print("Leonardo's Musical Workshop - Individual Instrument Demonstrations")
        print("=" * 70)

        workshop_presentations = {}

        # Create demonstration for each instrument
        for instrument_type in InstrumentType:
            presentation = self.create_instrument_demonstration(instrument_type)
            workshop_presentations[instrument_type.value] = presentation

        return workshop_presentations

    def save_workshop_materials(self, presentations: Dict[str, Dict]) -> None:
        """Save all workshop materials to artifacts."""

        print(f"\n{'='*70}")
        print("Saving Leonardo's Musical Workshop materials...")

        # Create workshop directory
        workshop_dir = ensure_artifact_dir("leonardos_musical_workshop")

        # Save each instrument presentation
        for instrument_name, presentation in presentations.items():
            # Create instrument directory
            instrument_dir = workshop_dir / instrument_name
            instrument_dir.mkdir(exist_ok=True)

            # Save instrument profile
            profile_path = instrument_dir / "instrument_profile.json"
            with profile_path.open("w", encoding="utf-8") as f:
                json.dump(presentation["profile"], f, indent=2)

            # Save demonstrations
            demo_dir = instrument_dir / "demonstrations"
            demo_dir.mkdir(exist_ok=True)

            for demo_name, demo_score in presentation["demonstrations"]:
                # Save demonstration score
                demo_score_path = demo_dir / f"{demo_name.lower().replace(' ', '_')}.json"
                with demo_score_path.open("w", encoding="utf-8") as f:
                    json.dump(self._score_to_dict(demo_score), f, indent=2)

            # Save acoustic analysis
            acoustic_path = instrument_dir / "acoustic_analysis.json"
            with acoustic_path.open("w", encoding="utf-8") as f:
                json.dump(presentation["acoustic_analysis"], f, indent=2)

            # Create technical documentation
            tech_doc_path = instrument_dir / "technical_documentation.md"
            tech_doc_content = self._create_technical_documentation(presentation)
            with tech_doc_path.open("w", encoding="utf-8") as f:
                f.write(tech_doc_content)

            print(f"  Saved {presentation['profile']['name']}:")
            print(f"    Profile: {profile_path}")
            print(f"    Demonstrations: {demo_dir}")
            print(f"    Acoustic analysis: {acoustic_path}")
            print(f"    Technical documentation: {tech_doc_path}")

        # Create workshop overview
        overview_path = workshop_dir / "workshop_overview.md"
        overview_content = self._create_workshop_overview(presentations)
        with overview_path.open("w", encoding="utf-8") as f:
            f.write(overview_content)

        print(f"\nWorkshop overview saved: {overview_path}")
        print(f"\nComplete Leonardo's Musical Workshop saved to: {workshop_dir}")

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

    def _create_technical_documentation(self, presentation: Dict) -> str:
        """Create comprehensive technical documentation for an instrument."""

        profile = presentation["profile"]
        acoustic = presentation["acoustic_analysis"]

        doc = f"""# {profile['name']} - Technical Documentation

## Historical Background

**Invention Date:** {profile['invention_date']}
**Codex Reference:** {profile['codex_reference']}

{profile['description']}

## Mechanical Design

### Operating Mechanism
{profile['mechanism']}

### Unique Features
"""
        for feature in profile['unique_features']:
            doc += f"- {feature}\n"

        doc += f"""
## Technical Specifications

- **Range:** {profile['range']}
- **Pitch Range:** {acoustic['fundamental_range']}
- **Dynamic Range:** {acoustic['dynamic_range']}
- **Attack Time:** {acoustic['attack_time']}
- **Decay Characteristics:** {acoustic['decay_characteristics']}

## Acoustic Properties

### Timbre and Sound Characteristics
{acoustic['timbre_description']}

### Harmonic Content
{acoustic['harmonic_content']}

### Resonance Characteristics
{acoustic['resonance_peaks']}

### Special Acoustic Features
{acoustic['special_characteristics']}

## Historical Context

{profile['historical_context']}

## Technical Challenges

During Leonardo's design and potential construction, several technical challenges would have been encountered:

"""
        for challenge in profile['technical_challenges']:
            doc += f"- {challenge}\n"

        doc += f"""
## Musical Applications

### Renaissance Performance Context
The {profile['name']} would have been particularly suited for:
- Court ceremonies and official functions
- Ensemble performances requiring sustained or automated parts
- Educational demonstrations of musical mechanics
- Special effects and theatrical productions

### Musical Capabilities
Based on the technical demonstrations, the instrument excels at:
"""
        for demo_name, _ in presentation["demonstrations"]:
            doc += f"- {demo_name}\n"

        doc += f"""
## Modern Reconstruction Considerations

For modern recreation of Leonardo's {profile['name']}, several factors must be considered:

### Materials
- **Period-appropriate materials:** Wood, brass, iron, leather
- **Modern alternatives:** Composites, synthetic materials, precision bearings
- **Compromise:** Historical appearance with modern reliability

### Technical Adaptations
- **Historical accuracy vs. reliability:** Balance between period construction and dependable operation
- **Tuning systems:** Mean-tone temperament for Renaissance authenticity
- **Power source:** Traditional water/weight systems vs. modern electric motors

### Performance Considerations
- **Tempo flexibility:** Limited by mechanical constraints
- **Dynamic control:** Achievable through regulation of air pressure or force
- **Maintenance requirements:** Regular adjustment and tuning needed

## Educational Value

The {profile['name']} serves as an excellent educational tool for:
- Understanding Renaissance mechanical engineering
- Exploring the intersection of art and technology
- Demonstrating principles of acoustics and music mechanics
- Appreciating Leonardo's interdisciplinary genius

---

*This documentation is part of the da Vinci Codex Project - Phase 3: Cultural Revival*
"""

        return doc

    def _create_workshop_overview(self, presentations: Dict[str, Dict]) -> str:
        """Create workshop overview documentation."""

        overview = """# Leonardo's Musical Workshop - Complete Overview

## Introduction

Welcome to Leonardo's Musical Workshop, a comprehensive exploration of Leonardo da Vinci's mechanical musical instruments. This collection represents the intersection of Renaissance artistry, mechanical engineering, and musical innovation that characterized Leonardo's work in late 15th-century Milan.

## Historical Context

Leonardo da Vinci (1452-1519) served the Sforza court in Milan from 1482 to 1499, a period of extraordinary cultural and artistic achievement. During this time, he designed numerous mechanical devices, including a remarkable collection of musical instruments that pushed the boundaries of Renaissance technology.

These instruments reflect Leonardo's deep understanding of:
- Acoustics and sound production
- Mechanical engineering and automation
- Musical theory and performance practice
- The relationship between art and technology

## The Instrument Collection

### String Instruments

#### Viola Organista
Leonardo's most innovative string instrument, combining the sustained tone of an organ with the expressive quality of bowed strings. This invention would have revolutionized Renaissance ensemble music.

### Wind Instruments

#### Mechanical Organ
An automated pipe organ capable of performing complex polyphonic music without human intervention, representing Leonardo's fascination with automation.

#### Programmable Flute
A sophisticated wind instrument with automated finger holes and breath control, capable of rapid passages beyond human capability.

#### Mechanical Trumpeter
An automated brass instrument designed for fanfares and ceremonial music, reflecting Leonardo's work on military engineering.

### Percussion Instruments

#### Mechanical Drum
A complex percussion system providing rhythmic foundation for dance music and military applications.

#### Mechanical Carillon
A bell ensemble with automated striking mechanism, designed for civic and religious use.

## Technical Innovation Themes

### Automation and Mechanization
Leonardo's instruments demonstrate his interest in reducing human labor while increasing musical complexity. Each instrument uses mechanical systems to:
- Automate repetitive or technically demanding tasks
- Enable multiple simultaneous operations
- Provide consistent performance quality

### Acoustic Engineering
The instruments reveal sophisticated understanding of:
- Sound production mechanisms
- Resonance and amplification
- Material properties and their acoustic effects
- Tuning and temperament systems

### Integration of Art and Technology
Leonardo's musical instruments embody the Renaissance ideal of combining:
- Aesthetic beauty with functional design
- Mathematical precision with artistic expression
- Practical utility with innovative technology

## Educational Applications

This workshop collection serves multiple educational purposes:

### Historical Musicology
- Understanding Renaissance musical practice
- Exploring performance contexts and venues
- Studying instrument development and evolution

### Mechanical Engineering
- Analyzing mechanical design principles
- Understanding automation and control systems
- Studying material science and craftsmanship

### Interdisciplinary Studies
- Examining the intersection of art and technology
- Understanding Renaissance innovation patterns
- Appreciating Leonardo's multidisciplinary approach

## Demonstration Structure

Each instrument is presented through three types of demonstrations:

### 1. Technical Capabilities
Showcases the instrument's unique mechanical features and technical possibilities, demonstrating Leonardo's engineering solutions.

### 2. Renaissance Performance
Presents the instrument in historically appropriate musical contexts, using authentic Renaissance forms and styles.

### 3. Extended Techniques
Explores the full range of the instrument's capabilities, including features that would have been impossible for human performers.

## Modern Reconstruction Insights

The workshop materials provide insights for modern instrument makers:

### Historical Accuracy
- Period-appropriate materials and construction methods
- Renaissance tuning systems and temperaments
- Historical performance practice considerations

### Technical Adaptations
- Modern materials for improved reliability
- Contemporary control systems for precision
- Enhanced durability for frequent performance

### Performance Practice
- Appropriate repertoire and programming
- Historical tempo and dynamic considerations
- Ensemble integration techniques

## Legacy and Influence

Leonardo's mechanical instruments, though never fully realized in his lifetime, have influenced:

### Modern Instrument Making
- Extended technique instruments
- Mechanical music devices
- Experimental instrument design

### Musical Technology
- Automated performance systems
- Computer-controlled instruments
- Interactive music installations

### Interdisciplinary Art
- Kinetic sculpture with sound
- Multimedia performance art
- Technology-based artistic expression

## Conclusion

Leonardo's Musical Workshop represents a unique convergence of historical innovation and modern technology. By studying these instruments, we gain insight into:

- Leonardo's creative process and technical genius
- Renaissance approaches to problem-solving
- The historical development of musical instruments
- The enduring relationship between art and technology

This collection serves not only as a tribute to Leonardo's ingenuity but also as inspiration for future innovations at the intersection of art, music, and technology.

---

*Leonardo's Musical Workshop is part of the da Vinci Codex Project - Phase 3: Cultural Revival*
"""

        return overview


def main():
    """Main function to generate Leonardo's Musical Workshop materials."""

    print("Leonardo's Musical Workshop - Individual Instrument Demonstrations")
    print("Phase 3: Cultural Revival - Technical Analysis and Demonstrations")
    print("=" * 70)

    # Create workshop
    workshop = LeonardosMusicalWorkshop()

    # Generate all instrument presentations
    presentations = workshop.generate_workshop_presentations()

    # Save workshop materials
    workshop.save_workshop_materials(presentations)

    print(f"\n{'='*70}")
    print("Leonardo's Musical Workshop Complete!")
    print("\nThe workshop includes:")
    print("  1. Detailed technical documentation for each instrument")
    print("  2. Three demonstration pieces per instrument:")
    print("     - Technical Capabilities")
    print("     - Renaissance Performance")
    print("     - Extended Techniques")
    print("  3. Comprehensive acoustic analysis")
    print("  4. Historical context and reconstruction insights")
    print("  5. Complete workshop overview documentation")

    print(f"\nAll materials saved to: {ensure_artifact_dir('leonardos_musical_workshop')}")


if __name__ == "__main__":
    main()
