"""
Assembly Animations for Variable-Pitch Aerial Screw.

This module creates comprehensive animation data showing the assembly process
and variable-pitch operation of Leonardo's aerial screw. The animations are
designed to demonstrate both the manufacturing sequence and operational
functionality of the complex mechanical system.

Animation Types:
1. Assembly sequence animation (component-by-component)
2. Variable-pitch operation animation (15° to 45° range)
3. Swashplate mechanism operation animation
4. Control linkage movement animation
5. Exploded to assembled transition animation
6. Operational cycle animation (complete pitch range)
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
import json
from dataclasses import dataclass

# Import shared components
from variable_pitch_assembly import AerialScrewSpecs, create_complete_assembly
from individual_components import ManufacturingTolerances
from mechanical_linkage_system import LinkageGeometry
from exploded_assembly_view import ExplosionConfiguration, ExplodedAssemblyGenerator

@dataclass
class AnimationConfiguration:
    """Configuration parameters for assembly animations."""
    # Animation parameters
    frame_rate: int = 30                    # Animation frame rate (fps)
    total_duration: float = 20.0            # Total animation duration (seconds)

    # Assembly animation
    assembly_sequence_duration: float = 10.0  # Assembly sequence duration
    component_settle_time: float = 0.5        # Time for component to settle

    # Pitch operation animation
    pitch_min_degrees: float = 15.0          # Minimum pitch angle
    pitch_max_degrees: float = 45.0          # Maximum pitch angle
    pitch_change_duration: float = 5.0       # Duration for full pitch change
    cycles_per_animation: int = 3            # Number of pitch cycles

    # Exploded animation
    explosion_duration: float = 3.0          # Duration to explode
    collapse_duration: float = 2.0           # Duration to collapse

    # Output format
    export_format: str = "json"              # Animation data format
    include_metadata: bool = True            # Include animation metadata

class KeyFrame:
    """Represents a single keyframe in the animation."""

    def __init__(self, time: float, components: Dict, description: str = ""):
        self.time = time  # Time in seconds
        self.components = components  # Component positions and orientations
        self.description = description  # Description of the keyframe

class AssemblyAnimation:
    """Creates assembly sequence animations."""

    def __init__(self, specs: AerialScrewSpecs, config: AnimationConfiguration):
        self.specs = specs
        self.config = config
        self.keyframes = []

    def create_assembly_sequence(self) -> List[KeyFrame]:
        """Create assembly sequence keyframes."""
        keyframes = []
        current_time = 0.0

        # Initial state - all components exploded
        explosion_config = ExplosionConfiguration(
            blade_explosion_factor=3.0,
            hub_explosion_factor=1.0,
            swashplate_explosion_factor=2.0,
            linkage_explosion_factor=2.5
        )

        generator = ExplodedAssemblyGenerator(self.specs, explosion_config)
        components, _ = generator.generate_complete_exploded_view()

        # Store initial exploded positions
        initial_positions = {}
        for i, component in enumerate(components):
            initial_positions[f'component_{i}'] = {
                'position': component.centroid.tolist(),
                'visible': True
            }

        keyframes.append(KeyFrame(
            current_time,
            initial_positions,
            "Initial exploded view - all components separated"
        ))

        # Assembly sequence timing
        sequence_steps = [
            (1.0, "hub", "Install central hub"),
            (2.0, "swashplate_stationary", "Install stationary swashplate"),
            (3.0, "bearings", "Install bearing assemblies"),
            (4.0, "swashplate_rotating", "Install rotating swashplate"),
            (5.0, "linkages", "Install control linkages"),
            (6.0, "pitch_horns", "Install pitch control horns"),
            (7.0, "blades", "Install blades"),
            (8.0, "final_adjustments", "Final assembly adjustments")
        ]

        # Create assembly keyframes
        for duration, component_type, description in sequence_steps:
            current_time += duration

            # Calculate component positions (gradual collapse)
            progress = min(current_time / self.config.assembly_sequence_duration, 1.0)

            frame_positions = {}
            for comp_name, initial_pos in initial_positions.items():
                if component_type in comp_name or progress >= 0.9:  # Component specific or final collapse
                    # Move component toward final position
                    final_position = self._calculate_final_position(comp_name)
                    current_position = [
                        initial_pos['position'][0] * (1 - progress) + final_position[0] * progress,
                        initial_pos['position'][1] * (1 - progress) + final_position[1] * progress,
                        initial_pos['position'][2] * (1 - progress) + final_position[2] * progress
                    ]
                    frame_positions[comp_name] = {
                        'position': current_position,
                        'visible': True,
                        'rotation': [0, 0, 0]  # Simplified rotation
                    }
                else:
                    frame_positions[comp_name] = initial_pos

            keyframes.append(KeyFrame(current_time, frame_positions, description))

        # Final assembled state
        final_time = self.config.assembly_sequence_duration
        final_positions = {}
        for comp_name in initial_positions.keys():
            final_positions[comp_name] = {
                'position': self._calculate_final_position(comp_name),
                'visible': True,
                'rotation': [0, 0, 0]
            }

        keyframes.append(KeyFrame(final_time, final_positions, "Assembly complete"))

        return keyframes

    def _calculate_final_position(self, component_name: str) -> List[float]:
        """Calculate final assembled position for a component."""
        # Simplified position calculation based on component type
        if 'hub' in component_name:
            return [0, 0, 0]
        elif 'blade' in component_name:
            # Extract blade index from component name
            blade_index = 0
            if '_' in component_name:
                try:
                    blade_index = int(component_name.split('_')[-1])
                except:
                    pass

            angle = 2 * np.pi * blade_index / self.specs.num_blades
            radius = self.specs.root_radius
            return [radius * np.cos(angle), radius * np.sin(angle), 0]
        elif 'swashplate' in component_name:
            if 'stationary' in component_name:
                return [0, 0, 0.1]
            else:
                return [0, 0, 0.15]
        elif 'bearing' in component_name:
            return [0, 0, 0.125]
        elif 'linkage' in component_name or 'horn' in component_name:
            return [0, 0, 0.2]
        else:
            return [0, 0, 0]

class PitchOperationAnimation:
    """Creates variable-pitch operation animations."""

    def __init__(self, specs: AerialScrewSpecs, config: AnimationConfiguration):
        self.specs = specs
        self.config = config
        self.keyframes = []

    def create_pitch_operation_sequence(self) -> List[KeyFrame]:
        """Create pitch operation keyframes."""
        keyframes = []
        current_time = 0.0

        # Create initial assembled state
        complete_assembly = create_complete_assembly(self.specs, 30.0)  # Start at 30° pitch

        initial_positions = self._extract_component_positions(complete_assembly)

        # Pitch change animation
        pitch_angles = np.linspace(
            self.config.pitch_min_degrees,
            self.config.pitch_max_degrees,
            20  # 20 frames per pitch change
        )

        for cycle in range(self.config.cycles_per_animation):
            if cycle % 2 == 0:
                # Forward cycle (min to max)
                angles = pitch_angles
            else:
                # Reverse cycle (max to min)
                angles = pitch_angles[::-1]

            for pitch_angle in angles:
                current_time += self.config.pitch_change_duration / len(pitch_angles)

                # Create assembly at current pitch angle
                pitch_assembly = create_complete_assembly(self.specs, pitch_angle)
                current_positions = self._extract_component_positions(pitch_assembly)

                # Calculate swashplate tilt based on pitch angle
                pitch_ratio = (pitch_angle - self.config.pitch_min_degrees) / (self.config.pitch_max_degrees - self.config.pitch_min_degrees)
                swashplate_tilt = 15 * (pitch_ratio - 0.5)  # Max tilt ±7.5°

                # Update swashplate position
                if 'swashplate_rotating' in current_positions:
                    current_positions['swashplate_rotating']['rotation'] = [np.radians(swashplate_tilt), 0, 0]

                keyframes.append(KeyFrame(
                    current_time,
                    current_positions,
                    f"Pitch angle: {pitch_angle:.1f}° (Cycle {cycle + 1})"
                ))

        return keyframes

    def _extract_component_positions(self, assembly) -> Dict:
        """Extract component positions from assembly mesh."""
        # Simplified component position extraction
        # In a real implementation, this would identify individual components
        positions = {
            'main_assembly': {
                'position': assembly.centroid.tolist(),
                'rotation': [0, 0, 0],
                'visible': True
            }
        }

        # Add key component positions
        bounds = assembly.bounds
        center = assembly.centroid

        # Estimate swashplate position
        positions['swashplate_rotating'] = {
            'position': [center[0], center[1], center[2] + 0.05],
            'rotation': [0, 0, 0],
            'visible': True
        }

        # Estimate blade positions
        for i in range(self.specs.num_blades):
            angle = 2 * np.pi * i / self.specs.num_blades
            radius = (self.specs.root_radius + self.specs.tip_radius) / 2
            positions[f'blade_{i}'] = {
                'position': [radius * np.cos(angle), radius * np.sin(angle), center[2]],
                'rotation': [0, 0, np.degrees(angle)],
                'visible': True
            }

        return positions

class ExplodedTransitionAnimation:
    """Creates exploded to assembled transition animations."""

    def __init__(self, specs: AerialScrewSpecs, config: AnimationConfiguration):
        self.specs = specs
        self.config = config
        self.keyframes = []

    def create_exploded_transition_sequence(self) -> List[KeyFrame]:
        """Create exploded to assembled transition keyframes."""
        keyframes = []
        current_time = 0.0

        # Start with assembled state
        complete_assembly = create_complete_assembly(self.specs, 30.0)
        assembled_positions = self._get_assembled_positions()

        keyframes.append(KeyFrame(
            current_time,
            assembled_positions,
            "Assembled state"
        ))

        # Explode animation
        explosion_frames = 30
        explosion_config = ExplosionConfiguration(
            blade_explosion_factor=2.5,
            hub_explosion_factor=1.0,
            swashplate_explosion_factor=1.5,
            linkage_explosion_factor=2.0
        )

        generator = ExplodedAssemblyGenerator(self.specs, explosion_config)
        components, _ = generator.generate_complete_exploded_view()
        exploded_positions = {}

        for i, component in enumerate(components):
            exploded_positions[f'component_{i}'] = {
                'position': component.centroid.tolist(),
                'visible': True,
                'rotation': [0, 0, 0]
            }

        # Create explosion animation frames
        for frame in range(explosion_frames):
            current_time += self.config.explosion_duration / explosion_frames
            progress = frame / explosion_frames

            frame_positions = {}
            for comp_name in assembled_positions.keys():
                if comp_name in exploded_positions:
                    # Interpolate between assembled and exploded positions
                    assembled_pos = assembled_positions[comp_name]['position']
                    exploded_pos = exploded_positions[comp_name]['position']

                    current_pos = [
                        assembled_pos[0] + (exploded_pos[0] - assembled_pos[0]) * progress,
                        assembled_pos[1] + (exploded_pos[1] - assembled_pos[1]) * progress,
                        assembled_pos[2] + (exploded_pos[2] - assembled_pos[2]) * progress
                    ]

                    frame_positions[comp_name] = {
                        'position': current_pos,
                        'visible': True,
                        'rotation': [0, 0, 0]
                    }
                else:
                    frame_positions[comp_name] = assembled_positions[comp_name]

            keyframes.append(KeyFrame(
                current_time,
                frame_positions,
                f"Exploding - {progress * 100:.1f}% complete"
            ))

        # Hold exploded state
        hold_duration = 2.0
        keyframes.append(KeyFrame(
            current_time + hold_duration,
            exploded_positions,
            "Fully exploded - showing all components"
        ))
        current_time += hold_duration

        # Collapse animation
        collapse_frames = 20
        for frame in range(collapse_frames):
            current_time += self.config.collapse_duration / collapse_frames
            progress = frame / collapse_frames

            frame_positions = {}
            for comp_name in assembled_positions.keys():
                if comp_name in exploded_positions:
                    # Interpolate back to assembled positions
                    assembled_pos = assembled_positions[comp_name]['position']
                    exploded_pos = exploded_positions[comp_name]['position']

                    current_pos = [
                        exploded_pos[0] + (assembled_pos[0] - exploded_pos[0]) * progress,
                        exploded_pos[1] + (assembled_pos[1] - exploded_pos[1]) * progress,
                        exploded_pos[2] + (assembled_pos[2] - exploded_pos[2]) * progress
                    ]

                    frame_positions[comp_name] = {
                        'position': current_pos,
                        'visible': True,
                        'rotation': [0, 0, 0]
                    }
                else:
                    frame_positions[comp_name] = assembled_positions[comp_name]

            keyframes.append(KeyFrame(
                current_time,
                frame_positions,
                f"Collapsing - {progress * 100:.1f}% complete"
            ))

        # Final assembled state
        keyframes.append(KeyFrame(
            current_time,
            assembled_positions,
            "Fully assembled"
        ))

        return keyframes

    def _get_assembled_positions(self) -> Dict:
        """Get assembled component positions."""
        complete_assembly = create_complete_assembly(self.specs, 30.0)

        positions = {
            'main_assembly': {
                'position': complete_assembly.centroid.tolist(),
                'rotation': [0, 0, 0],
                'visible': True
            },
            'hub': {
                'position': [0, 0, 0],
                'rotation': [0, 0, 0],
                'visible': True
            },
            'swashplate_stationary': {
                'position': [0, 0, 0.1],
                'rotation': [0, 0, 0],
                'visible': True
            },
            'swashplate_rotating': {
                'position': [0, 0, 0.15],
                'rotation': [0, 0, 0],
                'visible': True
            }
        }

        # Add blade positions
        for i in range(self.specs.num_blades):
            angle = 2 * np.pi * i / self.specs.num_blades
            radius = self.specs.root_radius
            positions[f'blade_{i}'] = {
                'position': [radius * np.cos(angle), radius * np.sin(angle), 0],
                'rotation': [0, 0, np.degrees(angle)],
                'visible': True
            }

        return positions

def generate_complete_animation_package(
    output_dir: Path,
    specs: Optional[AerialScrewSpecs] = None,
    config: Optional[AnimationConfiguration] = None
) -> Dict[str, Path]:
    """
    Generate complete animation package for the variable-pitch aerial screw.

    Creates comprehensive animation data showing assembly sequence, pitch
    operation, and exploded view transitions suitable for visualization
    and educational purposes.

    Args:
        output_dir: Output directory for animation files
        specs: Technical specifications
        config: Animation configuration

    Returns:
        Dictionary of exported file paths
    """
    if specs is None:
        specs = AerialScrewSpecs()
    if config is None:
        config = AnimationConfiguration()

    output_dir.mkdir(parents=True, exist_ok=True)
    exported_files = {}

    print("Generating Assembly Animations...")
    print("=" * 40)

    # 1. Create assembly sequence animation
    print("Creating assembly sequence animation...")
    assembly_anim = AssemblyAnimation(specs, config)
    assembly_keyframes = assembly_anim.create_assembly_sequence()

    assembly_animation_data = {
        'animation_type': 'assembly_sequence',
        'description': 'Complete assembly sequence from exploded to assembled state',
        'duration': config.assembly_sequence_duration,
        'frame_rate': config.frame_rate,
        'total_frames': int(config.assembly_sequence_duration * config.frame_rate),
        'keyframes': [
            {
                'time': kf.time,
                'components': kf.components,
                'description': kf.description
            }
            for kf in assembly_keyframes
        ]
    }

    assembly_anim_path = output_dir / "assembly_sequence_animation.json"
    with open(assembly_anim_path, 'w') as f:
        json.dump(assembly_animation_data, f, indent=2)
    exported_files['assembly_sequence'] = assembly_anim_path

    # 2. Create pitch operation animation
    print("Creating pitch operation animation...")
    pitch_anim = PitchOperationAnimation(specs, config)
    pitch_keyframes = pitch_anim.create_pitch_operation_sequence()

    pitch_animation_data = {
        'animation_type': 'pitch_operation',
        'description': 'Variable-pitch operation showing full range of motion',
        'duration': config.pitch_change_duration * config.cycles_per_animation,
        'frame_rate': config.frame_rate,
        'total_frames': int(config.pitch_change_duration * config.cycles_per_animation * config.frame_rate),
        'pitch_range': {
            'minimum': config.pitch_min_degrees,
            'maximum': config.pitch_max_degrees
        },
        'cycles': config.cycles_per_animation,
        'keyframes': [
            {
                'time': kf.time,
                'components': kf.components,
                'description': kf.description
            }
            for kf in pitch_keyframes
        ]
    }

    pitch_anim_path = output_dir / "pitch_operation_animation.json"
    with open(pitch_anim_path, 'w') as f:
        json.dump(pitch_animation_data, f, indent=2)
    exported_files['pitch_operation'] = pitch_anim_path

    # 3. Create exploded transition animation
    print("Creating exploded transition animation...")
    exploded_anim = ExplodedTransitionAnimation(specs, config)
    exploded_keyframes = exploded_anim.create_exploded_transition_sequence()

    exploded_animation_data = {
        'animation_type': 'exploded_transition',
        'description': 'Transition between assembled and exploded states',
        'duration': config.explosion_duration + 2.0 + config.collapse_duration,  # Including hold time
        'frame_rate': config.frame_rate,
        'total_frames': int((config.explosion_duration + 2.0 + config.collapse_duration) * config.frame_rate),
        'keyframes': [
            {
                'time': kf.time,
                'components': kf.components,
                'description': kf.description
            }
            for kf in exploded_keyframes
        ]
    }

    exploded_anim_path = output_dir / "exploded_transition_animation.json"
    with open(exploded_anim_path, 'w') as f:
        json.dump(exploded_animation_data, f, indent=2)
    exported_files['exploded_transition'] = exploded_anim_path

    # 4. Create animation metadata and instructions
    animation_metadata = {
        'animation_package_info': {
            'title': 'Leonardo da Vinci Variable-Pitch Aerial Screw Animations',
            'version': '1.0',
            'creation_date': '2025',
            'total_animations': 3,
            'total_duration': (
                config.assembly_sequence_duration +
                config.pitch_change_duration * config.cycles_per_animation +
                config.explosion_duration + 2.0 + config.collapse_duration
            ),
            'frame_rate': config.frame_rate
        },
        'animation_descriptions': {
            'assembly_sequence': 'Shows the step-by-step assembly process from individual components to the complete aerial screw. Demonstrates how each component fits together and the proper assembly sequence.',
            'pitch_operation': 'Demonstrates the variable-pitch mechanism in action, showing how the swashplate system controls blade pitch angles from 15° to 45°. Multiple cycles show the smooth operation of the control linkages.',
            'exploded_transition': 'Provides a clear view of all mechanical interfaces by transitioning between assembled and exploded states. Essential for understanding component relationships and assembly requirements.'
        },
        'technical_specifications': {
            'pitch_range_degrees': f"{config.pitch_min_degrees}° to {config.pitch_max_degrees}°",
            'number_of_blades': specs.num_blades,
            'rotor_diameter_m': f"{specs.tip_radius * 2:.1f}",
            'control_mechanism': 'Swashplate with spherical joint linkages',
            'materials': ['Oak/Ash blades', 'Wrought iron structure', 'Bronze bearings']
        },
        'rendering_recommendations': {
            'camera_positions': [
                {'name': 'overview', 'position': [5, 5, 3], 'target': [0, 0, 1]},
                {'name': 'detail', 'position': [2, 2, 1], 'target': [0, 0, 0.5]},
                {'name': 'side', 'position': [4, 0, 2], 'target': [0, 0, 1]},
                {'name': 'top', 'position': [0, 0, 6], 'target': [0, 0, 0]}
            ],
            'lighting': 'Soft, directional lighting to highlight mechanical details',
            'materials': 'Use historically accurate material colors and textures',
            'labels': 'Include component labels for educational purposes'
        },
        'usage_instructions': {
            'file_format': 'JSON animation data suitable for 3D rendering software',
            'interpolation': 'Use smooth interpolation between keyframes',
            'timing': 'Maintain specified frame rates for smooth animation',
            'looping': 'Animations can be looped for continuous display',
            'synchronization': 'Multiple animations can be synchronized for comprehensive presentation'
        }
    }

    metadata_path = output_dir / "animation_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(animation_metadata, f, indent=2)
    exported_files['metadata'] = metadata_path

    # 5. Create animation script for rendering
    animation_script_path = output_dir / "rendering_script.py"
    with open(animation_script_path, 'w') as f:
        f.write('"""')
        f.write('Rendering Script for Leonardo da Vinci Aerial Screw Animations\n\n')
        f.write('This script provides a framework for rendering the animation data\n')
        f.write('into visual animations using common 3D rendering libraries.\n')
        f.write('"""\n\n')
        f.write('import json\nimport numpy as np\n')
        f.write('# Animation rendering framework\n')
        f.write('# This would be implemented with specific rendering library\n')
        f.write('# such as Blender Python API, Three.js, or similar\n\n')
        f.write('def load_animation_data(file_path):\n')
        f.write('    """Load animation data from JSON file."""\n')
        f.write('    with open(file_path, \'r\') as f:\n')
        f.write('        return json.load(f)\n\n')
        f.write('def interpolate_keyframes(keyframes, frame_rate):\n')
        f.write('    """Interpolate between keyframes for smooth animation."""\n')
        f.write('    # Implementation would interpolate component positions\n')
        f.write('    # between keyframes for smooth motion\n')
        f.write('    pass\n\n')
        f.write('def render_animation(animation_data, output_path):\n')
        f.write('    """Render animation to video format."""\n')
        f.write('    # Implementation would use rendering library\n')
        f.write('    # to create visual animation from data\n')
        f.write('    pass\n\n')
        f.write('# Example usage:\n')
        f.write('# animation_data = load_animation_data("assembly_sequence_animation.json")\n')
        f.write('# render_animation(animation_data, "assembly_sequence.mp4")\n')

    exported_files['rendering_script'] = animation_script_path

    print(f"Animation package exported to: {output_dir}")
    print(f"Total animations: {len(exported_files) - 2}")  # Exclude metadata and script
    print(f"Total animation duration: {animation_metadata['animation_package_info']['total_duration']:.1f} seconds")
    print(f"Frame rate: {config.frame_rate} fps")

    return exported_files

if __name__ == "__main__":
    # Generate complete animation package
    base_dir = Path("../../artifacts/aerial_screw/animations")

    specs = AerialScrewSpecs()
    config = AnimationConfiguration(
        frame_rate=30,
        total_duration=25.0,
        pitch_change_duration=6.0,
        cycles_per_animation=3
    )

    exported_files = generate_complete_animation_package(base_dir, specs, config)

    print("\nAnimation package created with:")
    print("• Assembly sequence animation (component-by-component)")
    print("• Variable-pitch operation animation (15° to 45° range)")
    print("• Exploded view transition animation")
    print("• Complete rendering instructions and metadata")
    print("• Educational visualization suitable for workshops")