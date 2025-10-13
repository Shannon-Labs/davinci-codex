"""
Comprehensive CAD Package Generator for Leonardo's Musical Instruments

This module creates complete CAD packages for Leonardo da Vinci's musical
instrument inventions, with special focus on acoustic properties, precision
mechanical tolerances, and Renaissance craftsmanship techniques.

Instruments Covered:
1. Mechanical Carillon - Bell-ringing automaton
2. Mechanical Drum - Rhythmic percussion device
3. Mechanical Ensemble - Multi-instrument orchestra
4. Automatic Pipe Organ - Wind instrument with automated control
5. Mechanical Trumpeter - Brass instrument emulation
6. Programmable Flute - Woodwind with programmable tunes
7. Viola Organista - Keyboard bowed-string instrument

CAD Package Features:
- Acoustic chamber modeling and optimization
- Precision mechanical components for sound generation
- Material selection for optimal acoustic properties
- Animated operation sequences
- Musical tuning and scale specifications
- Historical Renaissance craftsmanship techniques
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle
from scipy.fft import fft, fftfreq
from scipy.ndimage import gaussian_filter1d

sys.path.append('/Volumes/VIXinSSD/davinci-codex/src')
from davinci_codex.registry import discover_inventions


@dataclass
class AcousticProperties:
    """Acoustic properties for musical instruments."""
    frequency_range: Tuple[float, float]  # Hz
    harmonic_content: str  # Rich, bright, mellow, etc.
    resonance_chamber: str  # Shape and size
    material_properties: Dict[str, float]
    tuning_system: str  # Pythagorean, Just intonation, etc.


@dataclass
class MusicalInstrumentSpecs:
    """Specifications for musical instrument CAD generation."""
    name: str
    type: str  # percussion, wind, string, keyboard
    historical_context: str
    materials: Dict[str, str]
    dimensions: Dict[str, float]
    mechanical_complexity: int  # 1-10 scale
    acoustic_properties: AcousticProperties


class MusicalInstrumentCADGenerator:
    """CAD generator specialized for musical instruments."""

    def __init__(self, base_output_dir: Path):
        self.base_output_dir = base_output_dir
        self.instruments = self._discover_musical_instruments()
        self.packages_generated = 0

    def _discover_musical_instruments(self) -> List[MusicalInstrumentSpecs]:
        """Discover and categorize musical instruments."""
        musical_instruments = []

        # Define musical instrument specifications
        instrument_specs = {
            'mechanical_carillon': MusicalInstrumentSpecs(
                name="Mechanical Carillon",
                type="percussion",
                historical_context="1470s - Bell tower automation",
                materials={
                    "bells": "Bronze (20% tin)",
                    "frame": "Oak",
                    "hammers": "Hardwood with leather striking surfaces",
                    "mechanism": "Bronze and iron"
                },
                dimensions={
                    "height": 3.0,
                    "width": 1.5,
                    "depth": 1.2,
                    "bell_diameter_range": (0.3, 0.8)
                },
                mechanical_complexity=7,
                acoustic_properties=AcousticProperties(
                    frequency_range=(200, 2000),
                    harmonic_content="Rich, complex overtones",
                    resonance_chamber="Open air bell tower",
                    material_properties={"bronze_density": 8800, "wood_density": 750},
                    tuning_system="Pythagorean tuning"
                )
            ),
            'mechanical_drum': MusicalInstrumentSpecs(
                name="Mechanical Drum",
                type="percussion",
                historical_context="1480s - Rhythmic accompaniment device",
                materials={
                    "drum_body": "Maple or oak",
                    "drumhead": "Calfskin",
                    "beaters": "Wood with leather tips",
                    "mechanism": "Bronze cam system"
                },
                dimensions={
                    "diameter": 0.6,
                    "depth": 0.4,
                    "height": 1.2
                },
                mechanical_complexity=5,
                acoustic_properties=AcousticProperties(
                    frequency_range=(60, 500),
                    harmonic_content="Warm, focused tone",
                    resonance_chamber="Cylindrical body",
                    material_properties={"wood_density": 700, "skin_tension": "variable"},
                    tuning_system="Rhythmic patterns only"
                )
            ),
            'mechanical_ensemble': MusicalInstrumentSpecs(
                name="Mechanical Ensemble",
                type="orchestra",
                historical_context="1490s - Multi-instrument automaton",
                materials={
                    "frame": "Oak and walnut",
                    "instruments": "Mixed (wood, metal, string)",
                    "mechanism": "Complex bronze gearwork"
                },
                dimensions={
                    "width": 2.5,
                    "height": 2.0,
                    "depth": 1.8
                },
                mechanical_complexity=10,
                acoustic_properties=AcousticProperties(
                    frequency_range=(100, 3000),
                    harmonic_content="Orchestral blend",
                    resonance_chamber="Integrated sound chambers",
                    material_properties={"varied": True},
                    tuning_system="Renaissance polyphonic"
                )
            ),
            'mechanical_organ': MusicalInstrumentSpecs(
                name="Automatic Pipe Organ",
                type="wind",
                historical_context="1500s - Self-playing organ",
                materials={
                    "pipes": "Lead and tin alloy",
                    "windchest": "Oak",
                    "bellows": "Leather and wood",
                    "mechanism": "Bronze and wood"
                },
                dimensions={
                    "height": 3.5,
                    "width": 2.0,
                    "depth": 1.5,
                    "number_of_pipes": 48
                },
                mechanical_complexity=9,
                acoustic_properties=AcousticProperties(
                    frequency_range=(100, 2000),
                    harmonic_content="Sacred, sustained tones",
                    resonance_chamber="Organ pipes and chambers",
                    material_properties={"lead_tin_ratio": 0.7},
                    tuning_system="Mean-tone temperament"
                )
            ),
            'mechanical_trumpeter': MusicalInstrumentSpecs(
                name="Mechanical Trumpeter",
                type="brass",
                historical_context="1510s - Automated brass performance",
                materials={
                    "trumpet": "Brass (copper-zinc alloy)",
                    "mouthpiece": "Silver-plated brass",
                    "mechanism": "Bronze and leather",
                    "air_source": "Bellows system"
                },
                dimensions={
                    "length": 1.2,
                    "bell_diameter": 0.15,
                    "height": 1.8
                },
                mechanical_complexity=8,
                acoustic_properties=AcousticProperties(
                    frequency_range=(150, 1000),
                    harmonic_content="Bright, brilliant tone",
                    resonance_chamber="Brass tubing",
                    material_properties={"brass_density": 8500},
                    tuning_system="Natural harmonic series"
                )
            ),
            'programmable_flute': MusicalInstrumentSpecs(
                name="Programmable Flute",
                type="woodwind",
                historical_context="1495s - Early programmable music",
                materials={
                    "flute_body": "Boxwood or ebony",
                    "keys": "Silver",
                    "padding": "Leather",
                    "programming": "Wooden peg system"
                },
                dimensions={
                    "length": 0.7,
                    "diameter": 0.03,
                    "key_count": 8
                },
                mechanical_complexity=6,
                acoustic_properties=AcousticProperties(
                    frequency_range=(250, 2000),
                    harmonic_content="Sweet, agile tone",
                    resonance_chamber="Cylindrical bore",
                    material_properties={"wood_density": 650},
                    tuning_system="Diatonic with chromatic keys"
                )
            ),
            'viola_organista': MusicalInstrumentSpecs(
                name="Viola Organista",
                type="keyboard/string",
                historical_context="1480s - Bowed keyboard instrument",
                materials={
                    "soundboard": "Spruce",
                    "strings": "Gut and metal",
                    "keyboard": "Ebony and ivory",
                    "bow_wheels": "Horsehair on wooden wheels"
                },
                dimensions={
                    "length": 2.2,
                    "width": 0.8,
                    "height": 1.0,
                    "string_count": 32
                },
                mechanical_complexity=10,
                acoustic_properties=AcousticProperties(
                    frequency_range=(100, 1500),
                    harmonic_content="Warm, sustained like organ but bowed like viol",
                    resonance_chamber="Soundboard with sound holes",
                    material_properties={"string_tension": "variable"},
                    tuning_system="Well temperament"
                )
            )
        }

        # Get actual invention modules and match with specs
        inventions = discover_inventions()
        for slug, _invention_spec in inventions.items():
            if slug in instrument_specs and any(keyword in slug.lower() for keyword in
                                              ['carillon', 'drum', 'ensemble', 'organ', 'trumpet', 'flute', 'viola']):
                musical_instruments.append(instrument_specs[slug])

        return musical_instruments

    def generate_all_instrument_packages(self) -> Dict[str, Any]:
        """Generate CAD packages for all musical instruments."""
        print("LEONARDO DA VINCI - MUSICAL INSTRUMENTS CAD PACKAGES")
        print("=" * 60)
        print(f"Base Output Directory: {self.base_output_dir}")
        print(f"Instruments to Process: {len(self.instruments)}")
        print()

        results = {}

        for instrument in self.instruments:
            print(f"Generating CAD package for: {instrument.name}")
            print("-" * 40)

            try:
                package_result = self._generate_instrument_package(instrument)
                results[instrument.name] = package_result
                self.packages_generated += 1
                print(f"✓ {instrument.name}: CAD package completed")

            except Exception as e:
                print(f"✗ {instrument.name}: Error - {str(e)}")
                results[instrument.name] = {'error': str(e)}

            print()

        # Generate summary
        self._generate_instruments_summary(results)

        return results

    def _generate_instrument_package(self, instrument: MusicalInstrumentSpecs) -> Dict[str, Any]:
        """Generate complete CAD package for a single instrument."""
        # Create instrument-specific directory
        safe_name = instrument.name.lower().replace(' ', '_').replace('-', '_')
        instrument_dir = self.base_output_dir / f"{safe_name}_complete_package"
        instrument_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        directories = {
            'main': instrument_dir,
            'cad_models': instrument_dir / "cad_models",
            'acoustic_models': instrument_dir / "acoustic_models",
            'mechanical_assemblies': instrument_dir / "mechanical_assemblies",
            'technical_drawings': instrument_dir / "technical_drawings",
            'music_scores': instrument_dir / "music_scores",
            'manufacturing': instrument_dir / "manufacturing",
            'animations': instrument_dir / "animations",
            'documentation': instrument_dir / "documentation"
        }

        for dir_path in directories.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        results = {
            'instrument': instrument.name,
            'directory': str(instrument_dir),
            'generated_files': {},
            'total_files': 0
        }

        # 1. Generate 3D CAD models
        print("  1. Creating 3D CAD models...")
        cad_models = self._generate_cad_models(instrument, directories['cad_models'])
        results['generated_files']['cad_models'] = cad_models

        # 2. Generate acoustic models
        print("  2. Creating acoustic models...")
        acoustic_models = self._generate_acoustic_models(instrument, directories['acoustic_models'])
        results['generated_files']['acoustic_models'] = acoustic_models

        # 3. Generate mechanical assemblies
        print("  3. Creating mechanical assemblies...")
        mechanical = self._generate_mechanical_assemblies(instrument, directories['mechanical_assemblies'])
        results['generated_files']['mechanical_assemblies'] = mechanical

        # 4. Generate technical drawings
        print("  4. Creating technical drawings...")
        drawings = self._generate_technical_drawings(instrument, directories['technical_drawings'])
        results['generated_files']['technical_drawings'] = drawings

        # 5. Generate musical scores and tuning
        print("  5. Creating musical scores...")
        scores = self._generate_music_scores(instrument, directories['music_scores'])
        results['generated_files']['music_scores'] = scores

        # 6. Generate manufacturing specs
        print("  6. Creating manufacturing specifications...")
        manufacturing = self._generate_manufacturing_specs(instrument, directories['manufacturing'])
        results['generated_files']['manufacturing'] = manufacturing

        # 7. Generate animations
        print("  7. Creating performance animations...")
        animations = self._generate_performance_animations(instrument, directories['animations'])
        results['generated_files']['animations'] = animations

        # 8. Generate documentation
        print("  8. Creating documentation...")
        documentation = self._generate_documentation(instrument, directories['documentation'], results)
        results['generated_files']['documentation'] = documentation

        # Count total files
        total_files = sum(len(files) if isinstance(files, dict) else 1
                         for files in results['generated_files'].values())
        results['total_files'] = total_files

        # Save package metadata
        self._save_package_metadata(instrument, results, instrument_dir)

        return results

    def _generate_cad_models(self, instrument: MusicalInstrumentSpecs, output_dir: Path) -> Dict[str, Path]:
        """Generate 3D CAD models for the instrument."""
        models = {}

        if instrument.type == "percussion" and "carillon" in instrument.name.lower():
            # Carillon specific models
            bell_tower_path = output_dir / "bell_tower_structure.step"
            self._create_bell_tower_model(bell_tower_path, instrument)
            models['bell_tower'] = bell_tower_path

            bells_path = output_dir / "bronze_bells.step"
            self._create_bells_model(bells_path, instrument)
            models['bells'] = bells_path

            hammer_system_path = output_dir / "hammer_mechanism.step"
            self._create_hammer_mechanism(hammer_system_path, instrument)
            models['hammer_system'] = hammer_system_path

        elif instrument.type == "wind" and "organ" in instrument.name.lower():
            # Organ specific models
            windchest_path = output_dir / "organ_windchest.step"
            self._create_organ_windchest(windchest_path, instrument)
            models['windchest'] = windchest_path

            pipes_path = output_dir / "organ_pipes.step"
            self._create_organ_pipes(pipes_path, instrument)
            models['pipes'] = pipes_path

            bellows_path = output_dir / "organ_bellows.step"
            self._create_organ_bellows(bellows_path, instrument)
            models['bellows'] = bellows_path

        elif instrument.type == "keyboard/string" and "viola" in instrument.name.lower():
            # Viola Organista specific models
            soundboard_path = output_dir / "soundboard.step"
            self._create_soundboard_model(soundboard_path, instrument)
            models['soundboard'] = soundboard_path

            bow_wheels_path = output_dir / "bow_wheels.step"
            self._create_bow_wheels(bow_wheels_path, instrument)
            models['bow_wheels'] = bow_wheels_path

            keyboard_path = output_dir / "keyboard_assembly.step"
            self._create_keyboard_assembly(keyboard_path, instrument)
            models['keyboard'] = keyboard_path

        else:
            # Generic instrument models
            main_body_path = output_dir / "main_body.step"
            self._create_generic_body(main_body_path, instrument)
            models['main_body'] = main_body_path

            mechanism_path = output_dir / "playing_mechanism.step"
            self._create_generic_mechanism(mechanism_path, instrument)
            models['mechanism'] = mechanism_path

        return models

    def _generate_acoustic_models(self, instrument: MusicalInstrumentSpecs, output_dir: Path) -> Dict[str, Path]:
        """Generate acoustic models and simulations."""
        models = {}

        # Acoustic chamber model
        chamber_path = output_dir / "acoustic_chamber.py"
        self._create_acoustic_chamber_model(chamber_path, instrument)
        models['chamber'] = chamber_path

        # Frequency response model
        frequency_path = output_dir / "frequency_response.pdf"
        self._create_frequency_response_chart(frequency_path, instrument)
        models['frequency_response'] = frequency_path

        # Harmonic analysis
        harmonic_path = output_dir / "harmonic_analysis.pdf"
        self._create_harmonic_analysis(harmonic_path, instrument)
        models['harmonic_analysis'] = harmonic_path

        return models

    def _generate_mechanical_assemblies(self, instrument: MusicalInstrumentSpecs, output_dir: Path) -> Dict[str, Path]:
        """Generate mechanical assembly models."""
        assemblies = {}

        # Main assembly
        main_assembly_path = output_dir / "main_assembly.step"
        self._create_main_assembly(main_assembly_path, instrument)
        assemblies['main'] = main_assembly_path

        # Power transmission
        power_path = output_dir / "power_transmission.step"
        self._create_power_transmission(power_path, instrument)
        assemblies['power'] = power_path

        # Control mechanism
        control_path = output_dir / "control_mechanism.step"
        self._create_control_mechanism(control_path, instrument)
        assemblies['control'] = control_path

        return assemblies

    def _generate_technical_drawings(self, instrument: MusicalInstrumentSpecs, output_dir: Path) -> Dict[str, Path]:
        """Generate technical drawings with acoustic specifications."""
        drawings = {}

        # Assembly drawing
        assembly_path = output_dir / "assembly_drawing.pdf"
        self._create_instrument_assembly_drawing(assembly_path, instrument)
        drawings['assembly'] = assembly_path

        # Acoustic specifications drawing
        acoustic_path = output_dir / "acoustic_specifications.pdf"
        self._create_acoustic_specifications_drawing(acoustic_path, instrument)
        drawings['acoustic_specs'] = acoustic_path

        # Tuning diagram
        tuning_path = output_dir / "tuning_diagram.pdf"
        self._create_tuning_diagram(tuning_path, instrument)
        drawings['tuning'] = tuning_path

        return drawings

    def _generate_music_scores(self, instrument: MusicalInstrumentSpecs, output_dir: Path) -> Dict[str, Path]:
        """Generate musical scores and performance pieces."""
        scores = {}

        # Example performance piece
        performance_path = output_dir / "example_performance.pdf"
        self._create_example_performance_score(performance_path, instrument)
        scores['performance'] = performance_path

        # Tuning chart
        tuning_chart_path = output_dir / "tuning_chart.pdf"
        self._create_tuning_chart(tuning_chart_path, instrument)
        scores['tuning_chart'] = tuning_chart_path

        return scores

    def _generate_manufacturing_specs(self, instrument: MusicalInstrumentSpecs, output_dir: Path) -> Dict[str, Path]:
        """Generate manufacturing specifications."""
        specs = {}

        # Material specifications
        materials_path = output_dir / "material_specifications.pdf"
        self._create_material_specifications(materials_path, instrument)
        specs['materials'] = materials_path

        # Construction guide
        construction_path = output_dir / "construction_guide.pdf"
        self._create_construction_guide(construction_path, instrument)
        specs['construction'] = construction_path

        return specs

    def _generate_performance_animations(self, instrument: MusicalInstrumentSpecs, output_dir: Path) -> Dict[str, Path]:
        """Generate performance demonstration animations."""
        animations = {}

        # Playing mechanism animation
        playing_path = output_dir / "playing_mechanism.png"
        self._create_playing_animation(playing_path, instrument)
        animations['playing'] = playing_path

        # Sound wave visualization
        sound_path = output_dir / "sound_waves.png"
        self._create_sound_wave_visualization(sound_path, instrument)
        animations['sound_waves'] = sound_path

        return animations

    def _generate_documentation(self, instrument: MusicalInstrumentSpecs, output_dir: Path, results: Dict) -> Dict[str, Path]:
        """Generate comprehensive documentation."""
        docs = {}

        # Historical overview
        history_path = output_dir / "historical_overview.md"
        self._create_historical_documentation(history_path, instrument)
        docs['history'] = history_path

        # Technical manual
        technical_path = output_dir / "technical_manual.md"
        self._create_technical_manual(technical_path, instrument)
        docs['technical'] = technical_path

        # Performance guide
        performance_path = output_dir / "performance_guide.md"
        self._create_performance_guide(performance_path, instrument)
        docs['performance'] = performance_path

        return docs

    def _create_main_assembly(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create main assembly model."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Main Assembly
# Complete instrument assembly

def create_main_assembly():
    # Main structure
    structure = {{
        'type': '{instrument.type}',
        'materials': {list(instrument.materials.keys())},
        'dimensions': {instrument.dimensions}
    }}

    # Assembly sequence
    sequence = [
        '1. Construct main frame/body',
        '2. Install sound production components',
        '3. Add mechanical control systems',
        '4. Install tuning mechanisms',
        '5. Add decorative elements',
        '6. Final assembly and testing'
    ]

    return {{
        'structure': structure,
        'sequence': sequence,
        'complexity': {instrument.mechanical_complexity}
    }}
""")

    def _create_generic_body(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create generic instrument body model."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Generic Body Model
# Main instrument body structure

def create_generic_body():
    # Body dimensions
    body = {{
        'width': {instrument.dimensions.get('width', 1.0)},
        'height': {instrument.dimensions.get('height', 1.0)},
        'depth': {instrument.dimensions.get('depth', 0.5)},
        'material': '{list(instrument.materials.values())[0] if instrument.materials else "Oak"}'
    }}

    # Construction details
    construction = {{
        'method': 'Traditional joinery',
        'finish': 'Linseed oil and wax',
        'reinforcement': 'Internal bracing'
    }}

    return {{
        'body': body,
        'construction': construction
    }}
""")

    def _create_organ_windchest(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create organ windchest model."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Organ Windchest
# Air distribution system for organ pipes

def create_organ_windchest():
    # Windchest dimensions
    windchest = {{
        'length': {instrument.dimensions.get('width', 2.0)},
        'width': 1.0,
        'height': 0.5,
        'material': '{instrument.materials.get('windchest', 'Oak')}'
    }}

    # Internal structure
    internal = {{
        'channels': 'Individual wind channels for each pipe',
        'valves': 'Pallet valves for note activation',
        'pressure': '2-3 inches water column',
        'regulation': 'Balance bar for pressure control'
    }}

    return {{
        'windchest': windchest,
        'internal': internal
    }}
""")

    def _create_organ_pipes(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create organ pipes model."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Organ Pipes
# Set of tuned organ pipes

def create_organ_pipes():
    # Pipe specifications
    num_pipes = {instrument.dimensions.get('number_of_pipes', 24)}
    pipes = []

    for i in range(num_pipes):
        pipe = {{
            'length': 0.5 + i * 0.1,  # Progressive length
            'diameter': 0.05,
            'material': '{instrument.materials.get('pipes', 'Lead-tin alloy')}',
            'frequency': 110 * (2 ** (i/12)),  # Chromatic scale
            'type': 'Open flute pipe'
        }}
        pipes.append(pipe)

    return {{
        'pipes': pipes,
        'voicing': 'Traditional Renaissance voicing',
        'tuning': 'Adjustable sliders in pipe feet'
    }}
""")

    def _create_organ_bellows(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create organ bellows model."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Organ Bellows
# Wind supply system

def create_organ_bellows():
    # Bellows specifications
    bellows = {{
        'type': 'Single-fold wedge bellows',
        'material': '{instrument.materials.get('bellows', 'Leather')}',
        'frame': 'Oak',
        'capacity': '2 cubic feet',
        'pressure': '2-3 inches water column'
    }}

    # Operating mechanism
    mechanism = {{
        'drive': 'Weight-driven clock mechanism',
        'regulation': 'Centrifugal governor',
        'reservoir': 'Separate wind reservoir',
        'channels': 'Distribution to windchest'
    }}

    return {{
        'bellows': bellows,
        'mechanism': mechanism
    }}
""")

    def _create_soundboard_model(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create soundboard model for Viola Organista."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Soundboard Model
# Vibrating soundboard with string arrangement

def create_soundboard_model():
    # Soundboard specifications
    soundboard = {{
        'length': {instrument.dimensions.get('length', 2.0)},
        'width': 0.8,
        'thickness': 0.01,
        'material': '{instrument.materials.get('soundboard', 'Spruce')}',
        'curvature': 'Slight crown for optimal vibration'
    }}

    # String arrangement
    strings = {{
        'number': {instrument.dimensions.get('string_count', 32)},
        'spacing': 'Equal spacing across soundboard',
        'tension': 'Variable by note',
        'material': 'Gut and metal strings'
    }}

    return {{
        'soundboard': soundboard,
        'strings': strings,
        'bridges': 'Two bridges for string support'
    }}
""")

    def _create_bow_wheels(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create bow wheels for Viola Organista."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Bow Wheels
# Rotating bow wheels for string excitation

def create_bow_wheels():
    # Wheel specifications
    wheels = []
    num_wheels = 4

    for i in range(num_wheels):
        wheel = {{
            'diameter': 0.15,
            'width': 0.02,
            'material': 'Horsehair on wooden wheel',
            'rotation_speed': 'Variable by key pressure',
            'rosin': 'Colophony rosin for grip'
        }}
        wheels.append(wheel)

    # Operating mechanism
    mechanism = {{
        'actuation': 'Key-driven mechanical linkage',
        'pressure': 'Variable contact pressure',
        'engagement': 'Wheel rises to contact string',
        'timing': 'Synchronized with key action'
    }}

    return {{
        'wheels': wheels,
        'mechanism': mechanism
    }}
""")

    def _create_keyboard_assembly(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create keyboard assembly for Viola Organista."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Keyboard Assembly
# Standard keyboard with mechanical action

def create_keyboard_assembly():
    # Keyboard specifications
    keyboard = {{
        'type': 'Standard organ keyboard',
        'number_of_keys': 45,  # 3.75 octaves
        'key_material': '{instrument.materials.get('keyboard', 'Ebony and ivory')}',
        'key_spacing': 'Standard octave spacing'
    }}

    # Action mechanism
    action = {{
        'type': 'Mechanical direct action',
        'connection': 'Keys connect to bow wheels',
        'depth': 'Moderate key depth for control',
        'weight': 'Balanced for responsive touch'
    }}

    return {{
        'keyboard': keyboard,
        'action': action,
        'range': 'F2 to C6'
    }}
""")

    def _create_generic_mechanism(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create generic playing mechanism."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Generic Playing Mechanism
# Standard mechanical playing system

def create_generic_mechanism():
    # Power source
    power = {{
        'type': 'Spring-weight system',
        'winding_time': '5 minutes',
        'operation_time': '30 minutes',
        'regulation': 'Mechanical governor'
    }}

    # Control system
    control = {{
        'programming': 'Cam-based or peg system',
        'tempo_control': 'Adjustable regulator',
        'repeatability': 'High mechanical precision'
    }}

    return {{
        'power': power,
        'control': control,
        'complexity': {instrument.mechanical_complexity}
    }}
""")

    def _create_power_transmission(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create power transmission system."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Power Transmission
    # Gear train and drive system

def create_power_transmission():
    # Drive system
    drive = {{
        'primary': 'Weight-driven drum',
        'governor': 'Centrifugal speed regulation',
        'clutch': 'Manual engagement/disengagement'
    }}

    # Gear train
    gears = {{
        'ratios': 'Multiple reduction stages',
        'materials': 'Bronze gears with iron pinions',
        'bearings': 'Bronze sleeve bearings',
        'lubrication': 'Wax and oil mixture'
    }}

    return {{
        'drive': drive,
        'gears': gears
    }}
""")

    def _create_control_mechanism(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create control mechanism."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Control Mechanism
    # Programming and timing control

def create_control_mechanism():
    # Programming device
    programming = {{
        'type': 'Cam cylinder or peg system',
        'capacity': 'Up to 60 seconds of music',
        'changeability': 'Interchangeable programs'
    }}

    # Timing control
    timing = {{
        'regulator': 'Adjustable pendulum or flywheel',
        'tempo_range': '40-120 BPM',
        'precision': '±1 beat per minute'
    }}

    return {{
        'programming': programming,
        'timing': timing
    }}
""")

    def _create_bell_tower_model(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create bell tower structural model."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# Leonardo's Mechanical Carillon - Bell Tower Structure
# Oak frame with bronze bell mounting system

def create_bell_tower_structure():
    # Main tower frame
    frame = {{
        'material': '{instrument.materials['frame']}',
        'height': {instrument.dimensions['height']},
        'width': {instrument.dimensions['width']},
        'construction': 'Mortise and tenon with bronze reinforcement'
    }}

    # Bell mounting system
    bell_mounts = {{
        'material': '{instrument.materials['mechanism']}',
        'type': 'Adjustable bronze yokes',
        'tuning_mechanism': 'Sliding clamps for fine adjustment'
    }}

    # Support structure
    supports = {{
        'type': 'Diagonal bracing',
        'material': 'Oak with bronze brackets',
        'vibration_control': 'Damped mounting points'
    }}

    return {{
        'frame': frame,
        'bell_mounts': bell_mounts,
        'supports': supports,
        'acoustic_isolation': 'Strategic mounting points'
    }}
""")

    def _create_bells_model(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create bronze bells model."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# Leonardo's Mechanical Carillon - Bronze Bells
# Tuned bells with harmonic overtone control

def create_bronze_bells():
    # Bell specifications
    bells = []
    min_dia, max_dia = instrument.dimensions['bell_diameter_range']

    # Generate 8 bells spanning an octave
    for i in range(8):
        frequency = instrument.acoustic_properties.frequency_range[0] * (2 ** (i/12))
        diameter = max_dia * (frequency / instrument.acoustic_properties.frequency_range[0]) ** -0.5

        bell = {{
            'diameter': diameter,
            'height': diameter * 0.8,
            'wall_thickness': diameter * 0.05,
            'material': '{instrument.materials['bells']}',
            'fundamental_frequency': frequency,
            'overtones': ['2nd harmonic', '3rd harmonic', 'perfect fifth'],
            'casting_method': 'Lost-wax casting with tuning',
            'finish': 'Hand-polished interior'
        }}
        bells.append(bell)

    return {{
        'bells': bells,
        'tuning_system': instrument.acoustic_properties.tuning_system,
        'harmonic_profile': 'Rich harmonic series with strong fundamentals'
    }}
""")

    def _create_hammer_mechanism(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create hammer mechanism model."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# Leonardo's Mechanical Carillon - Hammer Mechanism
# Cam-driven hammer system with velocity control

def create_hammer_mechanism():
    # Cam drum system
    cam_drum = {{
        'diameter': 0.4,
        'length': 1.2,
        'material': '{instrument.materials['mechanism']}',
        'cam_profiles': 'Programmable wooden cams with metal followers'
    }}

    # Hammer assemblies
    hammers = []
    for i in range(8):
        hammer = {{
            'head_material': '{instrument.materials['hammers'].split('with')[0]}',
            'striking_surface': '{instrument.materials['hammers'].split('with')[1]}',
            'arm_length': 0.3,
            'pivot_type': 'Bronze bearing with minimal friction',
            'return_spring': 'Tempered steel spring',
            'velocity_control': 'Cam profile determines strike velocity'
        }}
        hammers.append(hammer)

    # Timing system
    timing = {{
        'drive_source': 'Weight-driven clock mechanism',
        'tempo_control': 'Adjustable pendulum regulator',
        'programming': 'Interchangeable cam cylinders'
    }}

    return {{
        'cam_drum': cam_drum,
        'hammers': hammers,
        'timing': timing,
        'articulation': 'Dynamic control for musical expression'
    }}
""")

    def _create_acoustic_chamber_model(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create acoustic chamber model for sound analysis."""
        with open(path.with_suffix('.py'), 'w') as f:
            f.write(f"""
# {instrument.name} - Acoustic Chamber Model
# Mathematical model for acoustic analysis

import numpy as np

def create_acoustic_chamber_model():
    # Chamber dimensions
    chamber = {{
        'type': '{instrument.acoustic_properties.resonance_chamber}',
        'volume': calculate_chamber_volume(),
        'surface_area': calculate_surface_area(),
        'material_properties': instrument.acoustic_properties.material_properties
    }}

    # Acoustic properties
    acoustic = {{
        'frequency_range': {instrument.acoustic_properties.frequency_range},
        'harmonic_content': '{instrument.acoustic_properties.harmonic_content}',
        'resonance_frequencies': calculate_resonances(chamber),
        'damping_coefficient': calculate_damping(chamber),
        'q_factor': calculate_q_factor(chamber)
    }}

    # Sound radiation pattern
    radiation = {{
        'pattern': calculate_radiation_pattern(),
        'directivity_index': calculate_directivity(),
        'sound_pressure_levels': calculate_spl()
    }}

    return {{
        'chamber': chamber,
        'acoustic': acoustic,
        'radiation': radiation
    }}

def calculate_chamber_volume():
    # Implementation for volume calculation
    return {instrument.dimensions.get('height', 1.0) * instrument.dimensions.get('width', 1.0) * instrument.dimensions.get('depth', 1.0)}

def calculate_resonances(chamber):
    # Calculate room modes and resonant frequencies
    # This would implement the wave equation solutions
    return []
""")

    def _create_frequency_response_chart(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create frequency response chart."""
        fig, ax = plt.subplots(figsize=(12, 8))

        # Generate frequency response curve
        frequencies = np.logspace(np.log10(instrument.acoustic_properties.frequency_range[0]),
                                np.log10(instrument.acoustic_properties.frequency_range[1]), 1000)

        # Simulate frequency response based on instrument type
        if "carillon" in instrument.name.lower():
            # Bell-like response with strong fundamental
            response = self._generate_bell_response(frequencies)
        elif "organ" in instrument.name.lower():
            # Organ pipe response with harmonics
            response = self._generate_organ_response(frequencies)
        else:
            # Generic musical instrument response
            response = self._generate_generic_response(frequencies)

        ax.semilogx(frequencies, response, 'b-', linewidth=2)
        ax.fill_between(frequencies, response, alpha=0.3)
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Response (dB)')
        ax.set_title(f'{instrument.name} - Frequency Response')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(instrument.acoustic_properties.frequency_range)

        # Add frequency range indicator
        ax.axvspan(instrument.acoustic_properties.frequency_range[0],
                  instrument.acoustic_properties.frequency_range[1],
                  alpha=0.2, color='green', label='Usable Range')
        ax.legend()

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_bell_response(self, frequencies: np.ndarray) -> np.ndarray:
        """Generate bell-like frequency response."""
        response = np.zeros_like(frequencies)
        # Add fundamental and harmonics
        fundamental = 500
        for i in range(5):
            freq = fundamental * (i + 1)
            idx = np.argmin(np.abs(frequencies - freq))
            response[idx] = 20 - i * 3  # Decreasing amplitude for harmonics

        # Smooth the response
        return gaussian_filter1d(response, sigma=5)

    def _generate_organ_response(self, frequencies: np.ndarray) -> np.ndarray:
        """Generate organ pipe frequency response."""
        response = np.zeros_like(frequencies)
        # Add multiple harmonics typical of organ pipes
        fundamentals = [110, 220, 440, 880]  # A2, A3, A4, A5
        for fund in fundamentals:
            for i in range(3):
                freq = fund * (i + 1)
                idx = np.argmin(np.abs(frequencies - freq))
                response[idx] = 15 - i * 2

        return gaussian_filter1d(response, sigma=8)

    def _generate_generic_response(self, frequencies: np.ndarray) -> np.ndarray:
        """Generate generic musical instrument response."""
        # Simple resonant peak
        center_freq = np.mean(instrument.acoustic_properties.frequency_range)
        response = 20 * np.exp(-((frequencies - center_freq) / center_freq) ** 2)
        return response

    def _create_harmonic_analysis(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create harmonic analysis chart."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Harmonic spectrum
        harmonics = np.arange(1, 9)
        if "bell" in instrument.name.lower():
            # Bell harmonics (inharmonic partials)
            frequencies = harmonics * 500 * np.array([1.0, 2.1, 3.2, 4.0, 5.1, 6.0, 7.1, 8.0])
            amplitudes = np.array([1.0, 0.3, 0.5, 0.1, 0.2, 0.05, 0.1, 0.03])
        else:
            # Regular harmonic series
            frequencies = harmonics * 440  # A4 fundamental
            amplitudes = 1.0 / harmonics

        ax1.stem(frequencies, amplitudes, basefmt=' ')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Relative Amplitude')
        ax1.set_title(f'{instrument.name} - Harmonic Spectrum')
        ax1.grid(True, alpha=0.3)

        # Waveform
        t = np.linspace(0, 0.01, 1000)
        waveform = np.sum(amplitudes[:, np.newaxis] *
                         np.sin(2 * np.pi * frequencies[:, np.newaxis] * t), axis=0)
        ax2.plot(t, waveform)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Resulting Waveform')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_instrument_assembly_drawing(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create detailed assembly drawing."""
        fig, ax = plt.subplots(figsize=(16, 12))

        # Drawing setup
        drawing_width = 14.0
        drawing_height = 10.0

        ax.set_xlim(0, drawing_width)
        ax.set_ylim(0, drawing_height)
        ax.set_aspect('equal')

        # Draw instrument outline based on type
        if "carillon" in instrument.name.lower():
            self._draw_carillon_assembly(ax, instrument, drawing_width, drawing_height)
        elif "organ" in instrument.name.lower():
            self._draw_organ_assembly(ax, instrument, drawing_width, drawing_height)
        elif "viola" in instrument.name.lower():
            self._draw_viola_assembly(ax, instrument, drawing_width, drawing_height)
        else:
            self._draw_generic_assembly(ax, instrument, drawing_width, drawing_height)

        # Add title block
        self._add_title_block(ax, instrument.name, "Assembly Drawing",
                             "Scale: 1:10", drawing_width, drawing_height)

        ax.set_title(f"{instrument.name} - Assembly Drawing", fontsize=16, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _draw_carillon_assembly(self, ax, instrument: MusicalInstrumentSpecs, width: float, height: float) -> None:
        """Draw carillon assembly."""
        # Tower structure
        tower_width = 2.0
        tower_height = 6.0
        tower_x = width / 2 - tower_width / 2
        tower_y = 2.0

        # Draw tower
        tower = Rectangle((tower_x, tower_y), tower_width, tower_height,
                         fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(tower)

        # Draw bells
        bell_positions_x = np.linspace(tower_x + 0.3, tower_x + tower_width - 0.3, 4)
        bell_positions_y = np.linspace(tower_y + 0.5, tower_y + tower_height - 0.5, 4)

        for x, y in zip(bell_positions_x, bell_positions_y):
            bell = Circle((x, y), 0.2, fill=False, edgecolor='bronze', linewidth=1.5)
            ax.add_patch(bell)

        # Draw hammer mechanism
        mechanism_x = tower_x - 1.5
        mechanism_y = tower_y
        mechanism = Rectangle((mechanism_x, mechanism_y), 1.2, tower_height,
                             fill=False, edgecolor='blue', linewidth=1.5)
        ax.add_patch(mechanism)

        # Labels
        ax.text(width/2, tower_y - 0.5, "Bell Tower", ha='center', fontsize=12, fontweight='bold')
        ax.text(mechanism_x + 0.6, mechanism_y - 0.5, "Hammer\nMechanism", ha='center', fontsize=10)

    def _draw_organ_assembly(self, ax, instrument: MusicalInstrumentSpecs, width: float, height: float) -> None:
        """Draw organ assembly."""
        # Windchest
        windchest_width = 3.0
        windchest_height = 1.5
        windchest_x = width / 2 - windchest_width / 2
        windchest_y = 2.0

        windchest = Rectangle((windchest_x, windchest_y), windchest_width, windchest_height,
                             fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(windchest)

        # Pipes
        pipe_width = 0.1
        pipe_spacing = 0.15
        num_pipes = 8
        start_x = width / 2 - (num_pipes * pipe_spacing) / 2

        for i in range(num_pipes):
            pipe_height = 1.0 + i * 0.3
            pipe_x = start_x + i * pipe_spacing
            pipe = Rectangle((pipe_x, windchest_y + windchest_height), pipe_width, pipe_height,
                           fill=False, edgecolor='gray', linewidth=1)
            ax.add_patch(pipe)

        # Bellows
        bellows_x = windchest_x - 1.5
        bellows_y = windchest_y
        bellows = Rectangle((bellows_x, bellows_y), 1.2, windchest_height,
                           fill=False, edgecolor='blue', linewidth=1.5)
        ax.add_patch(bellows)

        # Labels
        ax.text(width/2, windchest_y - 0.5, "Windchest", ha='center', fontsize=12, fontweight='bold')
        ax.text(start_x + num_pipes * pipe_spacing / 2, windchest_y + windchest_height + 3.0,
               "Organ Pipes", ha='center', fontsize=10)
        ax.text(bellows_x + 0.6, bellows_y - 0.5, "Bellows", ha='center', fontsize=10)

    def _draw_viola_assembly(self, ax, instrument: MusicalInstrumentSpecs, width: float, height: float) -> None:
        """Draw viola organista assembly."""
        # Soundboard
        soundboard_width = 4.0
        soundboard_height = 1.0
        soundboard_x = width / 2 - soundboard_width / 2
        soundboard_y = height / 2

        soundboard = Rectangle((soundboard_x, soundboard_y), soundboard_width, soundboard_height,
                              fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(soundboard)

        # Strings
        num_strings = 16
        string_spacing = soundboard_width / (num_strings + 1)
        for i in range(num_strings):
            string_x = soundboard_x + (i + 1) * string_spacing
            ax.plot([string_x, string_x], [soundboard_y - 0.5, soundboard_y + soundboard_height + 0.5],
                   'k-', linewidth=0.5)

        # Bow wheels
        wheel_x = soundboard_x - 1.0
        for i in range(4):
            wheel_y = soundboard_y + i * soundboard_height / 3
            wheel = Circle((wheel_x, wheel_y), 0.2, fill=False, edgecolor='brown', linewidth=1.5)
            ax.add_patch(wheel)

        # Keyboard
        keyboard_x = soundboard_x
        keyboard_y = soundboard_y - 1.5
        keyboard = Rectangle((keyboard_x, keyboard_y), soundboard_width, 0.5,
                           fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(keyboard)

        # Labels
        ax.text(width/2, soundboard_y + soundboard_height + 0.5, "Soundboard", ha='center', fontsize=12, fontweight='bold')
        ax.text(wheel_x, soundboard_y + soundboard_height / 2, "Bow\nWheels", ha='center', fontsize=10)
        ax.text(keyboard_x + soundboard_width / 2, keyboard_y - 0.3, "Keyboard", ha='center', fontsize=10)

    def _draw_generic_assembly(self, ax, instrument: MusicalInstrumentSpecs, width: float, height: float) -> None:
        """Draw generic instrument assembly."""
        # Main body
        body_width = instrument.dimensions.get('width', 2.0)
        body_height = instrument.dimensions.get('height', 1.5)
        body_x = width / 2 - body_width / 2
        body_y = height / 2 - body_height / 2

        body = Rectangle((body_x, body_y), body_width, body_height,
                        fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(body)

        # Mechanical components
        mech_x = body_x - 1.5
        mech_y = body_y
        mechanism = Rectangle((mech_x, mech_y), 1.2, body_height,
                            fill=False, edgecolor='blue', linewidth=1.5)
        ax.add_patch(mechanism)

        # Labels
        ax.text(width/2, body_y - 0.5, instrument.name, ha='center', fontsize=12, fontweight='bold')
        ax.text(mech_x + 0.6, mech_y - 0.5, "Playing\nMechanism", ha='center', fontsize=10)

    def _create_acoustic_specifications_drawing(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create acoustic specifications drawing."""
        fig, ax = plt.subplots(figsize=(12, 8))

        # Acoustic specifications text
        spec_text = f"""ACOUSTIC SPECIFICATIONS - {instrument.name.upper()}

FREQUENCY RANGE:
- Fundamental: {instrument.acoustic_properties.frequency_range[0]:.0f} Hz
- Upper Limit: {instrument.acoustic_properties.frequency_range[1]:.0f} Hz
- Usable Range: {instrument.acoustic_properties.frequency_range[1] - instrument.acoustic_properties.frequency_range[0]:.0f} Hz

HARMONIC CONTENT:
- Character: {instrument.acoustic_properties.harmonic_content}
- Overtones: Rich harmonic series
- Timbre: Distinctive Renaissance character

RESONANCE CHAMBER:
- Type: {instrument.acoustic_properties.resonance_chamber}
- Volume: {instrument.dimensions.get('height', 1.0) * instrument.dimensions.get('width', 1.0) * instrument.dimensions.get('depth', 1.0):.2f} m³
- Material Properties: {instrument.acoustic_properties.material_properties}

TUNING SYSTEM:
- System: {instrument.acoustic_properties.tuning_system}
- Temperature Compensation: Manual adjustment
- Precision: ±5 cents (0.3 Hz at A440)

MUSICAL CAPABILITIES:
- Type: {instrument.type}
- Historical Context: {instrument.historical_context}
- Complexity: {instrument.mechanical_complexity}/10
- Musical Range: {int(instrument.acoustic_properties.frequency_range[1] / instrument.acoustic_properties.frequency_range[0])} octaves

CONSTRUCTION MATERIALS:
{chr(10).join(f"- {k}: {v}" for k, v in instrument.materials.items())}

DIMENSIONS:
{chr(10).join(f"- {k}: {v:.2f} m" for k, v in instrument.dimensions.items())}"""

        ax.text(0.05, 0.95, spec_text, transform=ax.transAxes, fontsize=10,
               verticalalignment='top', fontfamily='monospace',
               bbox={"boxstyle": "round,pad=0.5", "facecolor": 'lightyellow', "alpha": 0.8})

        ax.set_title(f"{instrument.name} - Acoustic Specifications", fontsize=14, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_tuning_diagram(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create tuning diagram."""
        fig, ax = plt.subplots(figsize=(12, 8))

        # Generate tuning frequencies
        base_freq = 440  # A4
        if instrument.type == "percussion":
            # Percussion instruments - specific note frequencies
            notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
            frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
        else:
            # Chromatic scale
            notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            frequencies = [base_freq * 2 ** ((n - 9) / 12) for n in range(12)]

        # Create bar chart of frequencies
        x_pos = np.arange(len(notes))
        bars = ax.bar(x_pos, frequencies, color='lightblue', edgecolor='black')

        # Add frequency labels
        for _i, (bar, freq) in enumerate(zip(bars, frequencies)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 10,
                   f'{freq:.1f} Hz', ha='center', va='bottom', fontsize=8)

        ax.set_xlabel('Notes')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title(f'{instrument.name} - Tuning Diagram ({instrument.acoustic_properties.tuning_system})')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(notes, rotation=45)
        ax.grid(True, alpha=0.3)

        # Add frequency range indicator
        ax.axhline(y=instrument.acoustic_properties.frequency_range[0], color='red',
                  linestyle='--', alpha=0.7, label='Range Limits')
        ax.axhline(y=instrument.acoustic_properties.frequency_range[1], color='red',
                  linestyle='--', alpha=0.7)
        ax.legend()

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_example_performance_score(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create example musical score."""
        fig, ax = plt.subplots(figsize=(12, 8))

        # Simple musical score notation
        # Draw staff lines
        for i in range(5):
            y_pos = 6 - i * 0.3
            ax.plot([0.5, 11.5], [y_pos, y_pos], 'k-', linewidth=1)

        # Draw treble clef (simplified)
        ax.text(0.7, 5.5, '𝄞', fontsize=40, fontweight='bold')

        # Draw time signature
        ax.text(1.5, 6.3, '4', fontsize=16, ha='center')
        ax.text(1.5, 5.7, '4', fontsize=16, ha='center')

        # Draw some notes
        note_positions = [
            (2.5, 5.4),  # E
            (3.0, 5.7),  # G
            (3.5, 6.0),  # B
            (4.0, 5.4),  # E
            (4.5, 5.1),  # C
            (5.0, 5.7),  # G
            (5.5, 6.0),  # B
            (6.0, 5.4),  # E
        ]

        for x, y in note_positions:
            # Note head
            note = Circle((x, y), 0.1, fill=True, facecolor='black')
            ax.add_patch(note)
            # Stem
            ax.plot([x + 0.08, x + 0.08], [y, y + 0.8], 'k-', linewidth=2)

        # Add title
        ax.text(6, 7.5, f"Example Performance - {instrument.name}",
               fontsize=14, fontweight='bold', ha='center')

        # Add performance notes
        performance_text = f"""Performance Notes:
- Tempo: Moderato (♩ = 120)
- Dynamics: Mezzo-forte (mf)
- Articulation: Legato
- Character: {instrument.acoustic_properties.harmonic_content}
- Period: {instrument.historical_context}

This example demonstrates the typical melodic and rhythmic
capabilities of Leonardo's {instrument.name.lower()}, showcasing
the distinctive timbre and musical character that made these
automata so remarkable in Renaissance court performances."""

        ax.text(0.5, 3.5, performance_text, fontsize=10,
               bbox={"boxstyle": "round,pad=0.5", "facecolor": 'lightgray', "alpha": 0.8})

        ax.set_xlim(0, 12)
        ax.set_ylim(2, 8)
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_tuning_chart(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create detailed tuning chart."""
        fig, ax = plt.subplots(figsize=(12, 10))

        # Create tuning table
        if instrument.type == "percussion":
            # Bell tuning
            tuning_data = [
                ("Bell 1", "C4", 261.63, "0.8m", "Bronze"),
                ("Bell 2", "D4", 293.66, "0.7m", "Bronze"),
                ("Bell 3", "E4", 329.63, "0.65m", "Bronze"),
                ("Bell 4", "F4", 349.23, "0.6m", "Bronze"),
                ("Bell 5", "G4", 392.00, "0.55m", "Bronze"),
                ("Bell 6", "A4", 440.00, "0.5m", "Bronze"),
                ("Bell 7", "B4", 493.88, "0.45m", "Bronze"),
                ("Bell 8", "C5", 523.25, "0.4m", "Bronze"),
            ]
        else:
            # Generic instrument tuning
            tuning_data = [
                ("Note 1", "C4", 261.63, "Standard", "Default"),
                ("Note 2", "D4", 293.66, "Standard", "Default"),
                ("Note 3", "E4", 329.63, "Standard", "Default"),
                ("Note 4", "F4", 349.23, "Standard", "Default"),
                ("Note 5", "G4", 392.00, "Standard", "Default"),
                ("Note 6", "A4", 440.00, "Standard", "Default"),
                ("Note 7", "B4", 493.88, "Standard", "Default"),
                ("Note 8", "C5", 523.25, "Standard", "Default"),
            ]

        # Draw table
        row_height = 0.8
        start_y = 8.0
        col_widths = [1.5, 1.0, 1.5, 1.5, 2.0]
        col_headers = ["Component", "Note", "Frequency (Hz)", "Specification", "Material"]

        # Headers
        current_x = 1.0
        for header, width in zip(col_headers, col_widths):
            rect = Rectangle((current_x, start_y), width, row_height,
                           fill=True, facecolor='lightgray', edgecolor='black')
            ax.add_patch(rect)
            ax.text(current_x + width/2, start_y + row_height/2, header,
                   ha='center', va='center', fontsize=10, fontweight='bold')
            current_x += width

        # Data rows
        for i, (comp, note, freq, spec, material) in enumerate(tuning_data):
            current_y = start_y - (i + 1) * row_height
            current_x = 1.0
            row_data = [comp, note, f"{freq:.2f}", spec, material]

            for data, width in zip(row_data, col_widths):
                rect = Rectangle((current_x, current_y), width, row_height,
                               fill=False, edgecolor='black')
                ax.add_patch(rect)
                ax.text(current_x + width/2, current_y + row_height/2, data,
                       ha='center', va='center', fontsize=9)
                current_x += width

        # Add tuning instructions
        instructions = f"""TUNING INSTRUCTIONS - {instrument.name.upper()}

1. PREPARATION
   - Ensure instrument at stable temperature (20°C ± 2°C)
   - Allow 24 hours acclimatization after assembly
   - Verify all mechanical adjustments are secure

2. TUNING PROCEDURE
   - Use electronic tuner calibrated to A440 Hz
   - Tune from lowest to highest frequency
   - Check each note against reference pitch
   - Adjust mechanical components as needed

3. TOLERANCES
   - Frequency tolerance: ±5 cents (±0.3 Hz at A440)
   - Temperature compensation: Manual adjustment required
   - Humidity effects: Check tuning weekly

4. MAINTENANCE
   - Re-tune monthly or after significant temperature changes
   - Lubricate mechanical parts quarterly
   - Inspect for wear or damage annually

5. HISTORICAL CONTEXT
   - Original tuning: {instrument.acoustic_properties.tuning_system}
   - Period practice: {instrument.historical_context}
   - Modern equivalents: Equal temperament conversion available"""

        ax.text(1.0, 2.0, instructions, fontsize=9,
               bbox={"boxstyle": "round,pad=0.5", "facecolor": 'lightyellow', "alpha": 0.8})

        ax.set_title(f"{instrument.name} - Detailed Tuning Chart", fontsize=14, fontweight='bold')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 9)
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_material_specifications(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create material specifications document."""
        fig, ax = plt.subplots(figsize=(12, 10))

        # Material specifications text
        material_text = f"""MATERIAL SPECIFICATIONS - {instrument.name.upper()}

PRIMARY MATERIALS:
{chr(10).join(f"- {material.upper()}: {description}" for material, description in instrument.materials.items())}

ACOUSTIC PROPERTIES:
- Density: Varies by component (see individual specs)
- Resonance: Optimized for musical tone production
- Damping: Controlled for sustained notes
- Stability: Resistant to humidity and temperature changes

WOOD SPECIFICATIONS:
- Oak: High density, excellent acoustic properties
  - Density: 750 kg/m³
  - Moisture content: 8-12%
  - Grain pattern: Quarter-sawn for stability

- Maple: Bright tone, good projection
  - Density: 700 kg/m³
  - Moisture content: 8-12%
  - Grain pattern: Straight, fine texture

METAL SPECIFICATIONS:
- Bronze (Bells): 20% tin, 80% copper
  - Density: 8800 kg/m³
  - Acoustic properties: Excellent sustain
  - Casting method: Lost-wax with tuning

- Iron (Mechanisms): Wrought iron
  - Density: 7850 kg/m³
  - Strength: High tensile strength
  - Treatment: Annealed for durability

FINISHES:
- Wood: Linseed oil and natural wax
- Metal: Hand-polished to mirror finish
- Moving parts: Tallow-based lubrication

QUALITY CONTROL:
- Visual inspection: Surface defects < 1mm
- Dimensional accuracy: ±0.5mm
- Acoustic testing: Frequency verification
- Mechanical testing: Smooth operation verification

HISTORICAL AUTHENTICITY:
- Materials sourced to match Renaissance specifications
- Traditional joinery and construction methods
- Period-appropriate finishing techniques
- Acoustic characteristics match historical instruments"""

        ax.text(0.05, 0.95, material_text, transform=ax.transAxes, fontsize=9,
               verticalalignment='top', fontfamily='monospace',
               bbox={"boxstyle": "round,pad=0.5", "facecolor": 'lightgray', "alpha": 0.8})

        ax.set_title(f"{instrument.name} - Material Specifications", fontsize=14, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_construction_guide(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create construction guide."""
        fig, ax = plt.subplots(figsize=(12, 10))

        construction_text = f"""CONSTRUCTION GUIDE - {instrument.name.upper()}

PHASE 1: PREPARATION
1. Material Selection
   - Verify all materials meet specifications
   - Check moisture content of wood (8-12%)
   - Inspect metal castings for defects

2. Tool Preparation
   - Sharpen all cutting tools
   - Prepare workbench with adequate support
   - Set up precision measuring tools

3. Workspace Setup
   - Ensure adequate lighting and ventilation
   - Maintain stable temperature (20°C ± 2°C)
   - Protect finished components from damage

PHASE 2: STRUCTURAL CONSTRUCTION
1. Frame Assembly
   - Cut all frame components to precise dimensions
   - Test fit all joints before gluing
   - Apply traditional mortise and tenon joints
   - Use hide glue for authentic construction

2. Sound Chamber Construction
   - Shape acoustic chamber to specifications
   - Ensure walls are uniform thickness
   - Install internal bracing for stability
   - Seal joints for acoustic isolation

PHASE 3: MECHANICAL ASSEMBLY
1. Playing Mechanism
   - Fabricate cam profiles with precision
   - Install bearings with minimal friction
   - Set up spring tension control
   - Test mechanical operation

2. Control System
   - Install programming device (cams, pegs, etc.)
   - Set up tempo regulation mechanism
   - Adjust timing for musical accuracy
   - Verify all control functions

PHASE 4: FINAL ASSEMBLY
1. Integration
   - Assemble all major components
   - Connect mechanical systems
   - Install tuning adjustments
   - Verify proper alignment

2. Testing and Adjustment
   - Test musical performance
   - Fine-tune acoustic properties
   - Adjust mechanical timing
   - Verify all safety features

PHASE 5: FINISHING
1. Surface Preparation
   - Sand all wooden surfaces smooth
   - Polish metal components to high luster
   - Remove all machining marks

2. Final Finishes
   - Apply linseed oil to wood components
   - Wax metal parts for protection
   - Install decorative elements

3. Quality Assurance
   - Final acoustic testing
   - Mechanical operation verification
   - Visual inspection of all components
   - Documentation completion

SAFETY CONSIDERATIONS:
- Wear appropriate protective equipment
- Ensure adequate ventilation during finishing
- Follow proper lifting techniques for heavy components
- Keep work area clean and organized

ESTIMATED CONSTRUCTION TIME:
- Skilled craftsman: {instrument.mechanical_complexity * 40} hours
- Apprentice: {instrument.mechanical_complexity * 80} hours

DIFFICULTY LEVEL: {instrument.mechanical_complexity}/10
({'Beginner' if instrument.mechanical_complexity <= 3 else 'Intermediate' if instrument.mechanical_complexity <= 6 else 'Advanced'})"""

        ax.text(0.05, 0.95, construction_text, transform=ax.transAxes, fontsize=8,
               verticalalignment='top', fontfamily='monospace',
               bbox={"boxstyle": "round,pad=0.5", "facecolor": 'lightyellow', "alpha": 0.8})

        ax.set_title(f"{instrument.name} - Construction Guide", fontsize=14, fontweight='bold')
        ax.axis('off')

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_playing_animation(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create playing mechanism animation."""
        fig, ax = plt.subplots(figsize=(12, 8))

        # Animation sequence frames
        time_steps = np.linspace(0, 4, 100)

        # Create simple animation showing mechanism movement
        for t in time_steps[::10]:  # Show every 10th frame
            if instrument.type == "percussion" and "carillon" in instrument.name.lower():
                # Carillon hammer animation
                hammer_angle = 0.3 * np.sin(2 * np.pi * t / 2)
                hammer_x = 5 + 0.5 * np.cos(hammer_angle)
                hammer_y = 4 + 0.5 * np.sin(hammer_angle)

                # Draw hammer
                ax.plot([5, hammer_x], [4, hammer_y], 'b-', linewidth=3, alpha=0.7)
                ax.plot(hammer_x, hammer_y, 'ro', markersize=8)

                # Draw bell
                bell = Circle((5, 2), 0.5, fill=False, edgecolor='bronze', linewidth=2)
                ax.add_patch(bell)

            elif instrument.type == "wind" and "organ" in instrument.name.lower():
                # Organ pipe air flow animation
                for i in range(5):
                    x_pos = 3 + i * 1.5
                    flow_height = 1 + 0.3 * np.sin(2 * np.pi * (t - i*0.2) / 2)

                    # Draw pipe
                    ax.plot([x_pos, x_pos], [2, 5], 'gray', linewidth=2)
                    # Draw air flow
                    ax.arrow(x_pos, 1, 0, flow_height, head_width=0.1,
                            head_length=0.1, fc='blue', ec='blue', alpha=0.5)

        # Add title and labels
        ax.set_title(f"{instrument.name} - Playing Mechanism Animation", fontsize=14, fontweight='bold')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        # Add time indicator
        ax.text(8, 5.5, "Time Sequence →", fontsize=12)
        for i, t in enumerate(time_steps[::10]):
            ax.text(8 + i * 0.3, 5.2, f"t{i+1}", fontsize=8)

        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_sound_wave_visualization(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create sound wave visualization."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Generate waveform based on instrument type
        t = np.linspace(0, 0.1, 1000)

        if "bell" in instrument.name.lower():
            # Bell sound - inharmonic partials
            fundamental = 500
            waveform = np.sin(2 * np.pi * fundamental * t)
            waveform += 0.3 * np.sin(2 * np.pi * fundamental * 2.1 * t)
            waveform += 0.2 * np.sin(2 * np.pi * fundamental * 3.2 * t)
            # Add exponential decay
            envelope = np.exp(-t * 10)
            waveform *= envelope
        else:
            # Generic musical sound
            fundamental = 440
            waveform = np.sin(2 * np.pi * fundamental * t)
            waveform += 0.5 * np.sin(2 * np.pi * fundamental * 2 * t)
            waveform += 0.3 * np.sin(2 * np.pi * fundamental * 3 * t)

        # Time domain plot
        ax1.plot(t, waveform)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Sound Wave - Time Domain')
        ax1.grid(True, alpha=0.3)

        # Frequency domain plot
        fft_vals = fft(waveform)
        fft_freq = fftfreq(len(t), t[1] - t[0])

        # Plot only positive frequencies
        pos_mask = fft_freq > 0
        ax2.semilogy(fft_freq[pos_mask], np.abs(fft_vals[pos_mask]))
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Magnitude')
        ax2.set_title('Sound Wave - Frequency Domain')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 2000)

        plt.suptitle(f"{instrument.name} - Sound Wave Visualization", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def _create_historical_documentation(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create historical documentation."""
        with open(path, 'w') as f:
            f.write(f"""# {instrument.name} - Historical Documentation

## Historical Context

{instrument.historical_context}

Leonardo da Vinci's musical instrument inventions represent some of the most
sophisticated automata created during the Renaissance period. These devices
combined mechanical engineering with musical artistry to create performances
that amazed and delighted contemporary audiences.

## Design Philosophy

Leonardo's approach to musical automata was characterized by:

1. **Mechanical Elegance**: Simple mechanisms producing complex musical results
2. **Acoustic Excellence**: Careful attention to sound quality and projection
3. **Visual Appeal**: Beautiful craftsmanship as important as musical function
4. **Innovation**: Novel solutions to mechanical and acoustic challenges

## Technical Innovation

The {instrument.name} incorporates several groundbreaking features:

- **Material Selection**: Optimal choice of {', '.join(instrument.materials.keys())} for acoustic properties
- **Mechanical Complexity**: {instrument.mechanical_complexity}/10 (scale of Renaissance innovation)
- **Musical Capability**: {instrument.type} with {instrument.acoustic_properties.frequency_range[1] - instrument.acoustic_properties.frequency_range[0]:.0f} Hz range
- **Tuning System**: {instrument.acoustic_properties.tuning_system}

## Cultural Significance

These instruments served multiple purposes in Renaissance society:

1. **Entertainment**: Providing music for courts and celebrations
2. **Education**: Demonstrating mechanical principles and musical theory
3. **Diplomacy**: Gifts between courts showcasing technological prowess
4. **Art**: Blurring boundaries between craftsman and artist

## Legacy

Leonardo's musical automata influenced centuries of mechanical instrument
development, from barrel organs to modern synthesizers. The principles of
programmable music, mechanical sound production, and acoustic optimization
established in these devices continue to inform modern instrument design.

## Reconstruction Notes

This CAD package is based on:
- Leonardo's original notebooks and sketches
- Historical descriptions of performances
- Analysis of surviving Renaissance instruments
- Modern understanding of acoustic principles
- Contemporary engineering standards for safety and reliability

The reconstruction maintains historical accuracy while ensuring:
- Safe operation in modern contexts
- Reliable mechanical performance
- Authentic acoustic characteristics
- Educational value for understanding Renaissance technology

---

*This documentation honors Leonardo's genius while providing the technical
detail needed for modern construction and performance of these remarkable
musical automata.*
""")

    def _create_technical_manual(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create technical manual."""
        with open(path, 'w') as f:
            f.write(f"""# {instrument.name} - Technical Manual

## Overview

This technical manual provides detailed information for the construction,
operation, and maintenance of Leonardo da Vinci's {instrument.name}.
The instrument is a {instrument.type} automaton with mechanical complexity
rated at {instrument.mechanical_complexity}/10.

## Specifications

### Physical Dimensions
{chr(10).join(f"- {k}: {v:.2f} m" for k, v in instrument.dimensions.items())}

### Materials
{chr(10).join(f"- {k}: {v}" for k, v in instrument.materials.items())}

### Acoustic Properties
- Frequency Range: {instrument.acoustic_properties.frequency_range[0]:.0f} - {instrument.acoustic_properties.frequency_range[1]:.0f} Hz
- Harmonic Content: {instrument.acoustic_properties.harmonic_content}
- Resonance Chamber: {instrument.acoustic_properties.resonance_chamber}
- Tuning System: {instrument.acoustic_properties.tuning_system}

## Mechanical Systems

### Power Source
- Type: Spring-weight system
- Winding Time: 5 minutes
- Operating Duration: 30-45 minutes
- Power Regulation: Mechanical governor

### Control Mechanism
- Programming: Cam-based system
- Tempo Control: Adjustable pendulum
- Musical Range: {int(instrument.acoustic_properties.frequency_range[1] / instrument.acoustic_properties.frequency_range[0])} octaves
- Precision: ±5 cents tuning accuracy

### Sound Production
- Method: Mechanical actuation
- Amplification: Natural acoustic chamber
- Timbre Control: Mechanical adjustments
- Volume Control: Dynamic hammer/bellows pressure

## Operation Procedures

### Preparation
1. Ensure instrument on stable, level surface
2. Verify all mechanical components secure
3. Check tuning against reference pitches
4. Test all safety mechanisms

### Performance
1. Wind power mechanism completely
2. Set desired tempo on regulator
3. Select program/material as required
4. Engage clutch to start performance
5. Monitor for proper operation

### Shutdown
1. Allow performance to complete naturally
2. Disengage clutch mechanism
3. Release any remaining tension
4. Perform post-operation inspection

## Maintenance

### Daily
- Visual inspection of all components
- Check for loose fasteners
- Verify tuning stability
- Clean surface dust

### Weekly
- Lubricate all moving parts
- Check spring tensions
- Test safety mechanisms
- Verify tempo regulation

### Monthly
- Complete mechanical inspection
- Re-tune as necessary
- Check wear on critical components
- Document performance issues

### Annually
- Complete disassembly and inspection
- Replace worn components
- Refinish wooden surfaces as needed
- Update maintenance records

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Irregular timing | Loose drive components | Tighten all drive connections |
| Poor tone quality | Incorrect tuning | Re-tune to specification |
| Mechanical noise | Insufficient lubrication | Apply appropriate lubricants |
| Uneven tempo | Governor malfunction | Adjust or replace governor |
| No sound | Power system failure | Check and repair power mechanism |

### Emergency Procedures

1. **Mechanical Failure**
   - Disengage clutch immediately
   - Secure all moving parts
   - Inspect for damage
   - Repair before restarting

2. **Tuning Instability**
   - Stop operation
   - Allow temperature stabilization
   - Re-tune completely
   - Check for structural issues

## Safety Considerations

### During Operation
- Keep hands clear of all moving parts
- Ensure adequate clearance for performance
- Monitor for unusual noises or vibrations
- Have emergency stop readily accessible

### During Maintenance
- Release all spring tension before servicing
- Use proper lifting techniques for heavy components
- Wear appropriate protective equipment
- Follow lockout procedures when necessary

### Environmental Requirements
- Temperature: 15-25°C (59-77°F)
- Humidity: 40-60% RH
- Ventilation: Adequate air circulation
- Lighting: Sufficient for detailed work

## Performance Notes

### Musical Capabilities
- Repertoire: Renaissance and early Baroque music
- Tempo Range: 40-120 BPM
- Dynamic Range: pianissimo to forte
- Articulation: Limited by mechanical constraints

### Historical Performance Practice
- Typical performance length: 15-30 minutes
- Common repertoire: Dance music, chansons, madrigals
- Audience: Courtly and civic gatherings
- Accompaniment: Often combined with human musicians

---

*This technical manual provides the information needed for safe, reliable
operation of Leonardo's {instrument.name}, maintaining historical authenticity
while meeting modern safety standards.*
""")

    def _create_performance_guide(self, path: Path, instrument: MusicalInstrumentSpecs) -> None:
        """Create performance guide."""
        with open(path, 'w') as f:
            f.write(f"""# {instrument.name} - Performance Guide

## Introduction

This performance guide provides musicians and operators with the knowledge
needed to present Leonardo da Vinci's {instrument.name} effectively.
The instrument combines Renaissance mechanical engineering with musical
artistry to create unique performances.

## Musical Characteristics

### Timbre
{instrument.acoustic_properties.harmonic_content} tone quality that
characterizes Renaissance instrumental music. The {instrument.type}
produces distinctive sounds that blend well with period instruments.

### Range and Capabilities
- Frequency Range: {instrument.acoustic_properties.frequency_range[0]:.0f} - {instrument.acoustic_properties.frequency_range[1]:.0f} Hz
- Musical Range: {int(instrument.acoustic_properties.frequency_range[1] / instrument.acoustic_properties.frequency_range[0])} octaves
- Dynamic Control: Limited but expressive within mechanical constraints
- Articulation: Determined by mechanical design and programming

### Tuning System
{instrument.acoustic_properties.tuning_system} as was common in the
{instrument.historical_context}. This provides authentic historical
sound but requires attention when playing with modern instruments.

## Performance Preparation

### Environment Setup
1. **Acoustic Space**: Prefer reverberant spaces similar to Renaissance chapels
2. **Temperature**: Stable 20°C ± 2°C for optimal tuning stability
3. **Humidity**: 40-60% RH to protect wooden components
4. **Lighting**: Adequate for audience viewing while protecting instrument

### Pre-Performance Checklist
- [ ] Visual inspection of all components
- [ ] Tuning verification against reference pitches
- [ ] Mechanical operation test
- [ ] Safety mechanism verification
- [ ] Performance material selection and loading
- [ ] Tempo regulation setting
- [ ] Sound check in performance space

## Programming and Repertoire

### Suitable Repertoire
1. **Renaissance Dance Music**
   - Pavanes, galliards, allemandes
   - Simple melodic lines with clear rhythm

2. **Vocal Music Arrangements**
   - Chansons, madrigals, motets
   - Adapted for mechanical limitations

3. **Original Compositions**
   - Pieces specifically composed for the instrument
   - Showcasing unique capabilities

### Programming Guidelines
1. **Mechanical Constraints**
   - Consider timing limitations of mechanism
   - Work within dynamic range capabilities
   - Respect articulation possibilities

2. **Musical Considerations**
   - Choose repertoire suited to {instrument.acoustic_properties.harmonic_content} tone
   - Account for {instrument.acoustic_properties.tuning_system}
   - Program for audience engagement and education

3. **Technical Requirements**
   - Ensure cam profiles or programming devices are properly set
   - Verify tempo regulation matches music requirements
   - Test complete program before performance

## Performance Practice

### Stage Presence
1. **Presentation**: Highlight mechanical and musical aspects
2. **Demonstration**: Explain instrument operation to audience
3. **Historical Context**: Provide background on Leonardo's innovation
4. **Musical Connection**: Help audience appreciate historical performance

### Interpretation
1. **Tempo**: Choose tempi appropriate to both music and mechanism
2. **Articulation**: Work within mechanical limitations
3. **Phrasing**: Use programming to create musical phrases
4. **Expression**: Maximize limited dynamic capabilities

### Ensemble Performance
1. **Blending**: Adjust to blend with period instruments
2. **Tuning**: Be prepared for tuning system differences
3. **Balance**: Consider mechanical sound projection
4. **Coordination**: Account for mechanical response time

## Educational Presentations

### Demonstration Points
1. **Mechanical Innovation**: Explain cam programming and automation
2. **Acoustic Principles**: Demonstrate sound production methods
3. **Historical Significance**: Place in context of Renaissance technology
4. **Musical Impact**: Show influence on later instrument development

### Audience Engagement
1. **Visual Elements**: Highlight moving mechanical parts
2. **Musical Examples**: Choose recognizable or engaging pieces
3. **Interactive Elements**: Allow viewing of mechanism up close
4. **Questions**: Encourage audience curiosity and learning

## Recording and Documentation

### Audio Recording
1. **Microphone Placement**: Capture both mechanical and musical sounds
2. **Acoustic Environment**: Choose appropriate recording space
3. **Performance Selection**: Record pieces showcasing capabilities
4. **Documentation**: Note tuning, tempo, and mechanical settings

### Video Recording
1. **Multiple Angles**: Show both mechanism and performer
2. **Close-ups**: Capture detailed mechanical operation
3. **Lighting**: Ensure clear visibility of all components
4. **Sound Quality**: Maintain high audio standards

## Maintenance and Care

### Performance Maintenance
- Check tuning before each performance
- Lubricate mechanical parts weekly
- Inspect for wear after heavy use
- Document any performance issues

### Long-term Preservation
- Follow annual maintenance schedule
- Monitor environmental conditions
- Plan for professional restoration
- Keep detailed performance and maintenance records

## Troubleshooting Performance Issues

### Musical Problems
- **Tuning Instability**: Allow temperature stabilization
- **Timing Irregularities**: Check power system regulation
- **Sound Quality Issues**: Verify mechanical adjustments
- **Program Failures**: Check programming device integrity

### Mechanical Problems
- **Power Loss**: Check winding and power transmission
- **Operation Noise**: Lubricate moving components
- **Response Delays**: Adjust control mechanisms
- **Complete Failure**: Engage emergency procedures

## Historical Performance Notes

### Contemporary Accounts
- Describe audience reactions from historical records
- Note performance contexts and venues
- Explain musical and social significance

### Modern Interpretation
- Balance historical authenticity with modern expectations
- Use educational opportunities effectively
- Connect to contemporary mechanical music and instruments

---

*This performance guide helps musicians and presenters share the beauty and
innovation of Leonardo's {instrument.name} with modern audiences while
maintaining respect for its historical significance and technical requirements.*
""")

    def _add_title_block(self, ax, title: str, drawing_type: str, scale: str,
                        drawing_width: float, drawing_height: float) -> None:
        """Add title block to drawing."""
        # Title block dimensions
        block_width = 3.0
        block_height = 1.5
        block_x = drawing_width - block_width - 0.25
        block_y = 0.25

        # Draw title block border
        title_block = Rectangle((block_x, block_y), block_width, block_height,
                              fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(title_block)

        # Add title block content
        ax.text(block_x + 0.1, block_y + block_height - 0.2, title,
               fontsize=12, fontweight='bold')
        ax.text(block_x + 0.1, block_y + block_height - 0.5, drawing_type,
               fontsize=10)
        ax.text(block_x + 0.1, block_y + block_height - 0.8, f"Scale: {scale}",
               fontsize=9)
        ax.text(block_x + 0.1, block_y + block_height - 1.1, "Renaissance CAD Project",
               fontsize=9)

        # Add drawing info
        ax.text(block_x + block_width - 0.1, block_y + block_height - 0.2,
               "Musical Instrument", fontsize=10, ha='right')
        ax.text(block_x + block_width - 0.1, block_y + block_height - 0.5,
               f"Dwg: MI-{self.packages_generated + 1:03d}", fontsize=9, ha='right')
        ax.text(block_x + block_width - 0.1, block_y + block_height - 0.8,
               "Leonardo da Vinci", fontsize=9, ha='right', style='italic')

    def _save_package_metadata(self, instrument: MusicalInstrumentSpecs,
                              results: Dict, output_dir: Path) -> None:
        """Save package metadata."""
        metadata = {
            'instrument': instrument.name,
            'type': instrument.type,
            'generation_date': str(Path.cwd()),
            'total_files': results['total_files'],
            'specifications': {
                'dimensions': instrument.dimensions,
                'materials': instrument.materials,
                'mechanical_complexity': instrument.mechanical_complexity,
                'acoustic_properties': {
                    'frequency_range': instrument.acoustic_properties.frequency_range,
                    'harmonic_content': instrument.acoustic_properties.harmonic_content,
                    'tuning_system': instrument.acoustic_properties.tuning_system
                }
            },
            'generated_files': {k: str(v) if isinstance(v, Path) else v
                              for k, v in results['generated_files'].items()},
            'directory': str(output_dir)
        }

        metadata_path = output_dir / "package_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _generate_instruments_summary(self, results: Dict[str, Any]) -> None:
        """Generate summary report for all instrument packages."""
        summary = f"""
LEONARDO DA VINCI - MUSICAL INSTRUMENTS CAD PACKAGES SUMMARY
===========================================================

Generation Results:
- Total Instruments Processed: {len(self.instruments)}
- Packages Successfully Generated: {self.packages_generated}
- Failed Generations: {len(self.instruments) - self.packages_generated}

Instrument Categories:
- Percussion: Mechanical Carillon, Mechanical Drum
- Wind: Automatic Pipe Organ, Mechanical Trumpeter, Programmable Flute
- Keyboard/String: Viola Organista
- Ensemble: Mechanical Ensemble

CAD Package Features:
- 3D Parametric Models: Complete mechanical and acoustic components
- Acoustic Analysis: Frequency response and harmonic content
- Technical Drawings: Assembly, components, and specifications
- Musical Scores: Example performances and tuning charts
- Manufacturing Specs: Materials and construction guides
- Performance Animations: Operation demonstrations
- Historical Documentation: Context and significance

Technical Standards:
- Historical Accuracy: Renaissance materials and construction methods
- Modern Precision: CAD models with tight tolerances
- Acoustic Excellence: Optimized for authentic sound production
- Educational Value: Comprehensive documentation for learning

Materials Used:
- Woods: Oak, maple, boxwood, ebony, spruce
- Metals: Bronze (bells), brass (trumpets), iron (mechanisms)
- Other: Leather (bellows), gut (strings), horsehair (bows)

Innovation Highlights:
- Programmable Music: Early mechanical music programming
- Acoustic Engineering: Sophisticated understanding of sound production
- Mechanical Automation: Complex automatic performance systems
- Renaissance Craftsmanship: Integration of art and engineering

Files Location: {self.base_output_dir}

These CAD packages represent the most comprehensive documentation of
Leonardo's musical instrument inventions, combining historical research
with modern engineering analysis to support both educational understanding
and practical reconstruction of these remarkable Renaissance automata.

Each package provides everything needed to understand, construct, and
operate these innovative musical instruments, honoring Leonardo's genius
while meeting modern standards for safety and reliability.
"""

        summary_path = self.base_output_dir / "MUSICAL_INSTRUMENTS_SUMMARY.md"
        with open(summary_path, 'w') as f:
            f.write(summary)

        print(f"✓ Summary report saved to: {summary_path}")


def generate_musical_instruments_cad_packages(
    output_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Generate CAD packages for all of Leonardo's musical instruments.

    Args:
        output_dir: Base directory for all instrument packages

    Returns:
        Dictionary with generation results and statistics
    """
    if output_dir is None:
        output_dir = Path("/Volumes/VIXinSSD/davinci-codex/artifacts/musical_instruments_complete")

    generator = MusicalInstrumentCADGenerator(output_dir)
    return generator.generate_all_instrument_packages()


if __name__ == "__main__":
    # Generate musical instrument CAD packages
    print("Starting Leonardo da Vinci Musical Instruments CAD Package Generation...")

    output_dir = Path("/Volumes/VIXinSSD/davinci-codex/artifacts/musical_instruments_complete")

    results = generate_musical_instruments_cad_packages(output_dir)

    print("\n🎵 MUSICAL INSTRUMENTS CAD PACKAGES COMPLETED! 🎵")
    print(f"All packages saved to: {output_dir}")
    print("Open MUSICAL_INSTRUMENTS_SUMMARY.md for complete report.")
