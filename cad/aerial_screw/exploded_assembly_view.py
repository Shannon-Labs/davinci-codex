"""
Exploded Assembly View for Variable-Pitch Aerial Screw.

This module creates detailed exploded assembly views that clearly show all
mechanical interfaces, assembly relationships, and component interactions.
The exploded views are essential for understanding the complex mechanical
system and for workshop assembly instructions.

Features:
1. Exploded views at multiple detail levels
2. Assembly relationship indicators
3. Mechanical interface highlighting
4. Component numbering and identification
5. Assembly sequence visualization
6. Interface tolerance indications
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import trimesh
from individual_components import ManufacturingTolerances
from mechanical_linkage_system import (
    ControlLinkageSystem,
    LinkageGeometry,
    SwashplateAssembly,
)

# Import shared components
from variable_pitch_assembly import AerialScrewSpecs


@dataclass
class ExplosionConfiguration:
    """Configuration parameters for exploded assembly views."""
    # Explosion factors
    blade_explosion_factor: float = 2.0      # Radial explosion for blades
    hub_explosion_factor: float = 0.5        # Vertical explosion for hub
    swashplate_explosion_factor: float = 1.0 # Vertical explosion for swashplates
    linkage_explosion_factor: float = 1.5    # Radial explosion for linkages

    # Display options
    show_interface_curves: bool = True       # Show mating interfaces
    show_assembly_axes: bool = True          # Show assembly axes
    show_tolerance_indicators: bool = True   # Show tolerance zones
    show_component_numbers: bool = True      # Show component numbering

    # Level of detail
    detail_level: str = "high"              # "low", "medium", "high"
    include_fasteners: bool = True          # Include bolts and nuts
    include_annotations: bool = True        # Include text annotations

class ExplodedAssemblyGenerator:
    """Generates exploded assembly views with component relationships."""

    def __init__(self, specs: AerialScrewSpecs, config: ExplosionConfiguration):
        self.specs = specs
        self.config = config
        self.components = []
        self.interfaces = []
        self.annotations = []

    def create_blade_explosion(self, blade_index: int) -> Tuple[trimesh.Trimesh, Dict]:
        """Create exploded blade with attachment interfaces."""
        from individual_components import create_tapered_blade_manufacturing_model

        # Create blade component
        blade_mesh, blade_metadata = create_tapered_blade_manufacturing_model(
            blade_index, self.specs, ManufacturingTolerances(), include_attachment_points=True
        )

        # Calculate explosion position
        blade_angle = 2 * np.pi * blade_index / self.specs.num_blades
        explosion_distance = self.config.blade_explosion_factor * 0.8

        explosion_offset = [
            explosion_distance * np.cos(blade_angle),
            explosion_distance * np.sin(blade_angle),
            0
        ]

        # Apply explosion transformation
        blade_mesh.apply_translation(explosion_offset)

        # Create interface indicators
        blade_interfaces = self._create_blade_interfaces(blade_index, explosion_offset)

        return blade_mesh, {
            'component_type': 'blade',
            'index': blade_index,
            'explosion_offset': explosion_offset,
            'interfaces': blade_interfaces,
            'metadata': blade_metadata
        }

    def create_hub_explosion(self) -> Tuple[trimesh.Trimesh, Dict]:
        """Create exploded central hub with interfaces."""
        from individual_components import create_central_hub_manufacturing

        # Create hub component
        hub_mesh, hub_metadata = create_central_hub_manufacturing(
            self.specs, ManufacturingTolerances()
        )

        # Apply vertical explosion
        explosion_offset = [0, 0, -self.config.hub_explosion_factor]
        hub_mesh.apply_translation(explosion_offset)

        # Create hub interfaces
        hub_interfaces = self._create_hub_interfaces(explosion_offset)

        return hub_mesh, {
            'component_type': 'hub',
            'index': 0,
            'explosion_offset': explosion_offset,
            'interfaces': hub_interfaces,
            'metadata': hub_metadata
        }

    def create_swashplate_explosion(self) -> Tuple[List[trimesh.Trimesh], List[Dict]]:
        """Create exploded swashplate components."""
        geometry = LinkageGeometry()
        swashplate_assembly = SwashplateAssembly(self.specs, geometry)

        components = []
        component_data = []

        # Stationary swashplate
        stationary_swashplate = swashplate_assembly.create_stationary_swashplate()
        stationary_offset = [0, 0, self.config.swashplate_explosion_factor * 0.5]
        stationary_swashplate.apply_translation(stationary_offset)

        components.append(stationary_swashplate)
        component_data.append({
            'component_type': 'stationary_swashplate',
            'index': 0,
            'explosion_offset': stationary_offset,
            'interfaces': self._create_swashplate_interfaces('stationary', stationary_offset),
            'metadata': {'material': self.specs.bearing_material}
        })

        # Rotating swashplate
        rotating_swashplate = swashplate_assembly.create_rotating_swashplate()
        rotating_offset = [0, 0, self.config.swashplate_explosion_factor * 1.5]
        rotating_swashplate.apply_translation(rotating_offset)

        components.append(rotating_swashplate)
        component_data.append({
            'component_type': 'rotating_swashplate',
            'index': 0,
            'explosion_offset': rotating_offset,
            'interfaces': self._create_swashplate_interfaces('rotating', rotating_offset),
            'metadata': {'material': self.specs.bearing_material}
        })

        # Bearing assemblies
        bearings = swashplate_assembly.create_bearing_assembly()
        for i, bearing in enumerate(bearings):
            bearing_offset = [
                bearing.centroid[0] * 1.2,
                bearing.centroid[1] * 1.2,
                self.config.swashplate_explosion_factor
            ]
            bearing.apply_translation(bearing_offset)

            components.append(bearing)
            component_data.append({
                'component_type': 'bearing',
                'index': i,
                'explosion_offset': bearing_offset,
                'interfaces': self._create_bearing_interfaces(i, bearing_offset),
                'metadata': {'material': self.specs.bearing_material}
            })

        return components, component_data

    def create_linkage_explosion(self) -> Tuple[List[trimesh.Trimesh], List[Dict]]:
        """Create exploded control linkage system."""
        geometry = LinkageGeometry()
        linkage_system = ControlLinkageSystem(self.specs, geometry)

        components = []
        component_data = []

        # Control linkages and pitch horns
        for i in range(self.specs.num_blades):
            # Control linkage
            linkage = linkage_system.create_control_linkage(i)
            blade_angle = 2 * np.pi * i / self.specs.num_blades

            linkage_offset = [
                self.config.linkage_explosion_factor * 0.5 * np.cos(blade_angle),
                self.config.linkage_explosion_factor * 0.5 * np.sin(blade_angle),
                0.3
            ]
            linkage.apply_translation(linkage_offset)

            components.append(linkage)
            component_data.append({
                'component_type': 'control_linkage',
                'index': i,
                'explosion_offset': linkage_offset,
                'interfaces': self._create_linkage_interfaces(i, linkage_offset),
                'metadata': {'material': self.specs.structure_material}
            })

            # Pitch horn
            pitch_horn = linkage_system.create_pitch_control_horn(i)
            horn_offset = [
                self.config.linkage_explosion_factor * 0.7 * np.cos(blade_angle),
                self.config.linkage_explosion_factor * 0.7 * np.sin(blade_angle),
                0.1
            ]
            pitch_horn.apply_translation(horn_offset)

            components.append(pitch_horn)
            component_data.append({
                'component_type': 'pitch_horn',
                'index': i,
                'explosion_offset': horn_offset,
                'interfaces': self._create_horn_interfaces(i, horn_offset),
                'metadata': {'material': self.specs.structure_material}
            })

        return components, component_data

    def _create_blade_interfaces(self, blade_index: int, explosion_offset: List[float]) -> List[Dict]:
        """Create interface indicators for blade attachments."""
        interfaces = []
        blade_angle = 2 * np.pi * blade_index / self.specs.num_blades

        # Root attachment interface
        root_interface = {
            'type': 'cylindrical_bore',
            'position': [
                self.specs.root_radius * np.cos(blade_angle) + explosion_offset[0],
                self.specs.root_radius * np.sin(blade_angle) + explosion_offset[1],
                explosion_offset[2] + 0.05
            ],
            'normal': [np.cos(blade_angle), np.sin(blade_angle), 0],
            'diameter': 0.06,
            'tolerance': 'H7/g6',
            'mating_component': 'hub_mounting_boss'
        }
        interfaces.append(root_interface)

        # Control arm attachment interface
        arm_angle = blade_angle + np.pi / 8
        arm_interface = {
            'type': 'spherical_socket',
            'position': [
                (self.specs.root_radius - 0.1) * np.cos(arm_angle) + explosion_offset[0],
                (self.specs.root_radius - 0.1) * np.sin(arm_angle) + explosion_offset[1],
                explosion_offset[2] + 0.1
            ],
            'normal': [0, 0, 1],
            'diameter': 0.03,
            'tolerance': '±0.1mm',
            'mating_component': f'control_linkage_{blade_index}'
        }
        interfaces.append(arm_interface)

        return interfaces

    def _create_hub_interfaces(self, explosion_offset: List[float]) -> List[Dict]:
        """Create interface indicators for hub components."""
        interfaces = []

        # Blade mounting interfaces
        for i in range(self.specs.num_blades):
            blade_angle = 2 * np.pi * i / self.specs.num_blades

            mounting_interface = {
                'type': 'mounting_boss',
                'position': [
                    self.specs.root_radius * 0.9 * np.cos(blade_angle) + explosion_offset[0],
                    self.specs.root_radius * 0.9 * np.sin(blade_angle) + explosion_offset[1],
                    explosion_offset[2] + 0.1
                ],
                'normal': [0, 0, 1],
                'diameter': 0.04,
                'tolerance': 'H7/h6',
                'mating_component': f'blade_{i}_root'
            }
            interfaces.append(mounting_interface)

        # Swashplate mounting interface
        swashplate_interface = {
            'type': 'cylindrical_seat',
            'position': [0 + explosion_offset[0], 0 + explosion_offset[1], explosion_offset[2] + 0.2],
            'normal': [0, 0, 1],
            'diameter': self.specs.hub_radius * 2.3,
            'tolerance': 'H8/f7',
            'mating_component': 'stationary_swashplate'
        }
        interfaces.append(swashplate_interface)

        return interfaces

    def _create_swashplate_interfaces(self, swashplate_type: str, explosion_offset: List[float]) -> List[Dict]:
        """Create interface indicators for swashplate components."""
        interfaces = []

        if swashplate_type == 'rotating':
            # Control arm attachment interfaces
            for i in range(self.specs.num_blades):
                attachment_angle = 2 * np.pi * i / self.specs.num_blades

                attachment_interface = {
                    'type': 'spherical_bearing',
                    'position': [
                        0.35 * np.cos(attachment_angle) + explosion_offset[0],
                        0.35 * np.sin(attachment_angle) + explosion_offset[1],
                        explosion_offset[2] + 0.03
                    ],
                    'normal': [0, 0, 1],
                    'diameter': 0.012,
                    'tolerance': '±0.05mm',
                    'mating_component': f'control_linkage_{i}'
                }
                interfaces.append(attachment_interface)

        return interfaces

    def _create_bearing_interfaces(self, bearing_index: int, explosion_offset: List[float]) -> List[Dict]:
        """Create interface indicators for bearing assemblies."""
        interfaces = []

        bearing_angle = 2 * np.pi * bearing_index / 12

        # Inner race interface
        inner_interface = {
            'type': 'cylindrical_bore',
            'position': [
                0.4 * np.cos(bearing_angle) + explosion_offset[0],
                0.4 * np.sin(bearing_angle) + explosion_offset[1],
                explosion_offset[2]
            ],
            'normal': [0, 0, 1],
            'diameter': 0.025,
            'tolerance': 'H7/g6',
            'mating_component': 'shaft'
        }
        interfaces.append(inner_interface)

        # Outer race interface
        outer_interface = {
            'type': 'cylindrical_surface',
            'position': [
                0.4 * np.cos(bearing_angle) + explosion_offset[0],
                0.4 * np.sin(bearing_angle) + explosion_offset[1],
                explosion_offset[2]
            ],
            'normal': [np.cos(bearing_angle), np.sin(bearing_angle), 0],
            'diameter': 0.04,
            'tolerance': 'H7/p6',
            'mating_component': 'housing'
        }
        interfaces.append(outer_interface)

        return interfaces

    def _create_linkage_interfaces(self, linkage_index: int, explosion_offset: List[float]) -> List[Dict]:
        """Create interface indicators for control linkages."""
        interfaces = []
        linkage_angle = 2 * np.pi * linkage_index / self.specs.num_blades

        # Swashplate end interface
        swashplate_interface = {
            'type': 'spherical_joint',
            'position': [
                0.3 * np.cos(linkage_angle) + explosion_offset[0],
                0.3 * np.sin(linkage_angle) + explosion_offset[1],
                explosion_offset[2] - 0.15
            ],
            'normal': [0, 0, 1],
            'diameter': 0.012,
            'tolerance': '±0.1mm',
            'mating_component': 'rotating_swashplate'
        }
        interfaces.append(swashplate_interface)

        # Blade horn end interface
        horn_interface = {
            'type': 'spherical_joint',
            'position': [
                0.6 * np.cos(linkage_angle) + explosion_offset[0],
                0.6 * np.sin(linkage_angle) + explosion_offset[1],
                explosion_offset[2] + 0.15
            ],
            'normal': [0, 0, -1],
            'diameter': 0.012,
            'tolerance': '±0.1mm',
            'mating_component': f'pitch_horn_{linkage_index}'
        }
        interfaces.append(horn_interface)

        return interfaces

    def _create_horn_interfaces(self, horn_index: int, explosion_offset: List[float]) -> List[Dict]:
        """Create interface indicators for pitch horns."""
        interfaces = []
        horn_angle = 2 * np.pi * horn_index / self.specs.num_blades

        # Blade attachment interface
        blade_interface = {
            'type': 'cylindrical_bore',
            'position': [
                self.specs.root_radius * 0.95 * np.cos(horn_angle) + explosion_offset[0],
                self.specs.root_radius * 0.95 * np.sin(horn_angle) + explosion_offset[1],
                explosion_offset[2]
            ],
            'normal': [np.cos(horn_angle), np.sin(horn_angle), 0],
            'diameter': 0.016,
            'tolerance': 'H7/m6',
            'mating_component': f'blade_{horn_index}'
        }
        interfaces.append(blade_interface)

        # Control linkage interface
        linkage_interface = {
            'type': 'spherical_socket',
            'position': [
                (self.specs.root_radius * 0.95 - 0.08) * np.cos(horn_angle) + explosion_offset[0],
                (self.specs.root_radius * 0.95 - 0.08) * np.sin(horn_angle) + explosion_offset[1],
                explosion_offset[2] + 0.05
            ],
            'normal': [0, 0, 1],
            'diameter': 0.012,
            'tolerance': '±0.1mm',
            'mating_component': f'control_linkage_{horn_index}'
        }
        interfaces.append(linkage_interface)

        return interfaces

    def create_assembly_axes(self) -> List[trimesh.Trimesh]:
        """Create visualization axes for assembly reference."""
        axes = []

        if self.config.show_assembly_axes:
            # Main vertical axis
            axis_length = 1.5
            axis_radius = 0.005

            main_axis = trimesh.creation.cylinder(
                radius=axis_radius,
                height=axis_length,
                sections=16
            )
            main_axis.apply_translation([0, 0, axis_length / 2])
            main_axis.visual.face_colors = [0.2, 0.2, 0.8, 1.0]  # Blue
            axes.append(main_axis)

            # Radial axes for blade positions
            for i in range(self.specs.num_blades):
                blade_angle = 2 * np.pi * i / self.specs.num_blades

                radial_axis = trimesh.creation.cylinder(
                    radius=axis_radius * 0.7,
                    height=self.specs.tip_radius * 1.2,
                    sections=16
                )

                # Orient radial axis
                radial_axis.apply_transform(trimesh.transformations.rotation_matrix(
                    blade_angle, [0, 0, 1]
                ))
                radial_axis.apply_translation([
                    self.specs.tip_radius * 0.6 * np.cos(blade_angle),
                    self.specs.tip_radius * 0.6 * np.sin(blade_angle),
                    0
                ])
                radial_axis.visual.face_colors = [0.8, 0.2, 0.2, 1.0]  # Red
                axes.append(radial_axis)

        return axes

    def create_interface_indicators(self, interfaces: List[Dict]) -> List[trimesh.Trimesh]:
        """Create visual indicators for mating interfaces."""
        indicators = []

        if not self.config.show_interface_curves:
            return indicators

        for interface in interfaces:
            if interface['type'] == 'cylindrical_bore':
                # Create cylinder indicator
                indicator = trimesh.creation.cylinder(
                    radius=interface['diameter'] / 2,
                    height=0.02,
                    sections=16
                )
                indicator.apply_translation(interface['position'])
                indicator.visual.face_colors = [0.8, 0.8, 0.2, 0.7]  # Yellow, transparent

            elif interface['type'] == 'spherical_joint':
                # Create sphere indicator
                indicator = trimesh.creation.icosphere(
                    radius=interface['diameter'] / 2,
                    subdivisions=2
                )
                indicator.apply_translation(interface['position'])
                indicator.visual.face_colors = [0.2, 0.8, 0.2, 0.7]  # Green, transparent

            elif interface['type'] == 'mounting_boss':
                # Create mounting boss indicator
                indicator = trimesh.creation.cylinder(
                    radius=interface['diameter'] / 2,
                    height=0.03,
                    sections=16
                )
                indicator.apply_translation(interface['position'])
                indicator.visual.face_colors = [0.8, 0.4, 0.2, 0.7]  # Orange, transparent

            else:
                continue

            indicators.append(indicator)

        return indicators

    def generate_complete_exploded_view(self) -> Tuple[List[trimesh.Trimesh], Dict]:
        """Generate complete exploded assembly view with all components."""
        all_components = []
        all_interfaces = []
        component_info = {}

        # 1. Create hub explosion
        hub_mesh, hub_data = self.create_hub_explosion()
        all_components.append(hub_mesh)
        all_interfaces.extend(hub_data['interfaces'])
        component_info['hub'] = hub_data

        # 2. Create blade explosions
        for i in range(self.specs.num_blades):
            blade_mesh, blade_data = self.create_blade_explosion(i)
            all_components.append(blade_mesh)
            all_interfaces.extend(blade_data['interfaces'])
            component_info[f'blade_{i}'] = blade_data

        # 3. Create swashplate explosions
        swashplate_components, swashplate_data = self.create_swashplate_explosion()
        all_components.extend(swashplate_components)
        for data in swashplate_data:
            all_interfaces.extend(data['interfaces'])
            component_info[data['component_type']] = data

        # 4. Create linkage explosions
        linkage_components, linkage_data = self.create_linkage_explosion()
        all_components.extend(linkage_components)
        for data in linkage_data:
            all_interfaces.extend(data['interfaces'])
            component_info[f"{data['component_type']}_{data['index']}"] = data

        # 5. Create assembly axes
        axes = self.create_assembly_axes()
        all_components.extend(axes)

        # 6. Create interface indicators
        interface_indicators = self.create_interface_indicators(all_interfaces)
        all_components.extend(interface_indicators)

        # Create metadata
        metadata = {
            'total_components': len(all_components),
            'component_count_by_type': {
                'blades': self.specs.num_blades,
                'hub': 1,
                'swashplate_components': len(swashplate_components),
                'linkage_components': len(linkage_components),
                'interface_indicators': len(interface_indicators)
            },
            'explosion_configuration': {
                'blade_factor': self.config.blade_explosion_factor,
                'hub_factor': self.config.hub_explosion_factor,
                'swashplate_factor': self.config.swashplate_explosion_factor,
                'linkage_factor': self.config.linkage_explosion_factor
            },
            'interface_count': len(all_interfaces),
            'component_info': component_info,
            'assembly_notes': [
                'Components are exploded for clear visualization',
                'Yellow indicators show cylindrical interfaces',
                'Green indicators show spherical joints',
                'Orange indicators show mounting surfaces',
                'Blue axis shows main rotation axis',
                'Red axes show blade radial positions'
            ]
        }

        return all_components, metadata

def export_exploded_assembly_package(
    output_dir: Path,
    specs: Optional[AerialScrewSpecs] = None,
    config: Optional[ExplosionConfiguration] = None
) -> Dict[str, Path]:
    """
    Export complete exploded assembly package.

    Creates detailed exploded views with interface documentation and
    assembly instructions suitable for workshop manufacturing.

    Args:
        output_dir: Output directory for exploded view files
        specs: Technical specifications
        config: Explosion configuration

    Returns:
        Dictionary of exported file paths
    """
    if specs is None:
        specs = AerialScrewSpecs()
    if config is None:
        config = ExplosionConfiguration()

    output_dir.mkdir(parents=True, exist_ok=True)
    exported_files = {}

    print("Creating Exploded Assembly Views...")
    print("=" * 40)

    # Generate exploded assembly
    generator = ExplodedAssemblyGenerator(specs, config)
    components, metadata = generator.generate_complete_exploded_view()

    # Export complete exploded assembly
    complete_exploded_path = output_dir / "complete_exploded_assembly.stl"
    complete_assembly = trimesh.util.concatenate(components)
    complete_assembly.export(complete_exploded_path)
    exported_files['complete_exploded'] = complete_exploded_path

    # Export individual component groups
    component_groups = {
        'hub_only': [comp for comp in components if any(
            comp.bounds[0][2] < -0.2 and comp.bounds[1][2] < 0.2 for comp in [comp]
        )],
        'blades_only': [],
        'swashplate_only': [],
        'linkage_only': [],
        'interfaces_only': []
    }

    # Group components by type (simplified grouping)
    for comp in components:
        center = comp.centroid
        if center[2] < -0.2:
            component_groups['hub_only'].append(comp)
        elif center[2] > 0.4:
            component_groups['swashplate_only'].append(comp)
        elif np.sqrt(center[0]**2 + center[1]**2) > 1.5:
            component_groups['blades_only'].append(comp)
        elif 0.1 < center[2] < 0.4:
            component_groups['linkage_only'].append(comp)
        else:
            component_groups['interfaces_only'].append(comp)

    # Export grouped assemblies
    for group_name, group_components in component_groups.items():
        if group_components:
            group_path = output_dir / f"exploded_{group_name}.stl"
            if len(group_components) > 1:
                group_assembly = trimesh.util.concatenate(group_components)
            else:
                group_assembly = group_components[0]
            group_assembly.export(group_path)
            exported_files[f'exploded_{group_name}'] = group_path

    # Export assembly documentation
    import json

    assembly_doc = {
        'exploded_assembly_metadata': metadata,
        'component_interfaces': {
            f"component_{i}": {
                'interfaces': comp_data.get('interfaces', []) if isinstance(comp_data, dict) else [],
                'explosion_offset': comp_data.get('explosion_offset', [0, 0, 0]) if isinstance(comp_data, dict) else [0, 0, 0]
            }
            for i, comp_data in enumerate(metadata['component_info'].values())
        },
        'assembly_sequence': [
            '1. Position central hub (Component 1)',
            '2. Install blade mounting bosses (Components 2-5)',
            '3. Attach blades to hub (Components 6-9)',
            '4. Install stationary swashplate (Component 10)',
            '5. Install bearing assemblies (Components 11-22)',
            '6. Install rotating swashplate (Component 23)',
            '7. Attach control linkages (Components 24-27)',
            '8. Install pitch horns (Components 28-31)',
            '9. Verify all interface fits',
            '10. Test assembly movement'
        ],
        'interface_specifications': {
            'blade_to_hub': {
                'type': 'Cylindrical fit',
                'tolerance': 'H7/h6',
                'surface_finish': 'Ra 1.6 μm',
                'lubrication': 'Dry fit with wax coating'
            },
            'swashplate_bearings': {
                'type': 'Bronze sleeve bearings',
                'clearance': '0.1mm',
                'lubrication': 'Animal fat or olive oil',
                'material': 'Phosphor bronze'
            },
            'control_linkages': {
                'type': 'Spherical joints',
                'tolerance': '±0.1mm',
                'material': 'Wrought iron with bronze inserts',
                'maintenance': 'Monthly lubrication'
            }
        },
        'manufacturing_notes': [
            'All interfaces must be smooth and free of burrs',
            'Bearing surfaces require high precision machining',
            'Spherical joints should be hand-fitted for optimal motion',
            'Assembly sequence must be followed for proper fit',
            'Final assembly requires dynamic balancing'
        ]
    }

    doc_path = output_dir / "exploded_assembly_documentation.json"
    with open(doc_path, 'w') as f:
        json.dump(assembly_doc, f, indent=2)
    exported_files['documentation'] = doc_path

    # Create assembly instruction manual
    manual_path = output_dir / "exploded_assembly_manual.txt"
    with open(manual_path, 'w') as f:
        f.write("LEONARDO DA VINCI AERIAL SCREW - EXPLODED ASSEMBLY MANUAL\n")
        f.write("=" * 65 + "\n\n")
        f.write("EXPLANATION OF EXPLODED VIEW\n")
        f.write("-" * 35 + "\n")
        f.write("This exploded assembly view shows all components separated for\n")
        f.write("clear visualization of mechanical interfaces and assembly\n")
        f.write("relationships. Components are color-coded by type:\n\n")
        f.write("• Brown/Oak: Tapered blades with airfoil sections\n")
        f.write("• Gray/Iron: Structural components and linkages\n")
        f.write("• Bronze/Brown: Bearing surfaces and precision components\n")
        f.write("• Yellow: Cylindrical mating interfaces\n")
        f.write("• Green: Spherical joint interfaces\n")
        f.write("• Orange: Mounting and attachment surfaces\n\n")

        f.write("ASSEMBLY INSTRUCTIONS\n")
        f.write("-" * 35 + "\n")
        for step in assembly_doc['assembly_sequence']:
            f.write(f"{step}\n")
        f.write("\n")

        f.write("CRITICAL INTERFACE REQUIREMENTS\n")
        f.write("-" * 35 + "\n")
        for interface_name, spec in assembly_doc['interface_specifications'].items():
            f.write(f"\n{interface_name.upper()}:\n")
            for key, value in spec.items():
                f.write(f"  {key}: {value}\n")

    exported_files['assembly_manual'] = manual_path

    print(f"Exploded assembly package exported to: {output_dir}")
    print(f"Total components: {metadata['total_components']}")
    print(f"Total interfaces: {metadata['interface_count']}")
    print(f"Component groups: {len(component_groups)}")

    return exported_files

if __name__ == "__main__":
    # Create complete exploded assembly package
    base_dir = Path("../../artifacts/aerial_screw/exploded_views")

    specs = AerialScrewSpecs()
    config = ExplosionConfiguration(
        blade_explosion_factor=2.5,
        show_interface_curves=True,
        show_assembly_axes=True,
        detail_level="high"
    )

    exported_files = export_exploded_assembly_package(base_dir, specs, config)

    print("\nExploded assembly views created showing:")
    print("• All mechanical interfaces with tolerance specifications")
    print("• Component relationships and assembly sequence")
    print("• Color-coded interface indicators")
    print("• Assembly axes and reference geometry")
    print("• Workshop-ready assembly instructions")
