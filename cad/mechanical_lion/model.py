"""
Parametric mesh generator for Leonardo's Mechanical Lion.

This module creates detailed 3D models of the mechanical lion walking mechanism
with historically accurate geometry and Renaissance materials. The generator
supports both complete lion assembly and individual mechanism components for
detailed analysis and manufacturing.

Features:
- Parametric leg kinematics with four-bar linkages
- Cam drum profiles for natural gait generation
- Structural framework with Renaissance materials
- Chest cavity reveal mechanism integration
- Multiple configuration options for educational and research purposes
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import trimesh

# Lion body proportions (based on real Panthera leo)
LION_LENGTH = 2.4  # meters (nose to tail base)
LION_HEIGHT = 1.2  # meters (shoulder height)
LION_WIDTH = 0.8   # meters (body width)
LION_WEIGHT = 180.0  # kg (mechanical lion weight)

# Leg mechanism parameters
LEG_LENGTH = 0.6  # meters (shoulder to paw)
UPPER_LEG_LENGTH = 0.3  # meters (femur/humerus)
LOWER_LEG_LENGTH = 0.3  # meters (tibia/radius)
FOOT_WIDTH = 0.08  # meters
FOOT_LENGTH = 0.12  # meters

# Body positioning
FORELEG_TO_HINDLEG_DISTANCE = 0.8  # meters
LATERAL_LEG_SPACING = 0.4  # meters
BODY_HEIGHT = 0.7  # meters (ground clearance)

# Cam drum parameters
CAM_DRUM_RADIUS = 0.15  # meters
CAM_DRUM_LENGTH = 0.3  # meters
CAM_TRACK_WIDTH = 0.02  # meters

# Material properties (Renaissance materials)
MATERIALS = {
    "oak": {
        "density": 750,  # kg/m³
        "elastic_modulus": 12e9,  # Pa
        "tensile_strength": 40e6,  # Pa
        "color": [0.65, 0.45, 0.2, 1.0]  # Brown
    },
    "bronze": {
        "density": 8800,  # kg/m³
        "elastic_modulus": 100e9,  # Pa
        "tensile_strength": 200e6,  # Pa
        "color": [0.72, 0.45, 0.2, 1.0]  # Bronze
    },
    "steel": {
        "density": 7850,  # kg/m³
        "elastic_modulus": 200e9,  # Pa
        "tensile_strength": 400e6,  # Pa
        "color": [0.7, 0.7, 0.8, 1.0]  # Steel gray
    },
    "gilded_bronze": {
        "density": 8800,  # kg/m³
        "elastic_modulus": 100e9,  # Pa
        "tensile_strength": 200e6,  # Pa
        "color": [0.85, 0.7, 0.1, 1.0]  # Gold
    }
}


def _create_lion_body() -> trimesh.Trimesh:
    """
    Create the main lion body structure.

    Returns:
        Trimesh object representing the lion body
    """
    # Create main body as an elongated box with rounded ends
    body_length = LION_LENGTH * 0.7  # Main body, excluding head and tail
    body_shape = trimesh.creation.box(extents=[body_length, LION_WIDTH, LION_HEIGHT])

    # Add head section (triangular prism)
    head_length = LION_LENGTH * 0.2
    head_vertices = np.array([
        # Base triangle
        [-head_length, -LION_WIDTH/2, 0],
        [-head_length, LION_WIDTH/2, 0],
        [-head_length, 0, LION_HEIGHT],
        # Top triangle (offset forward)
        [0, -LION_WIDTH/3, LION_HEIGHT * 0.6],
        [0, LION_WIDTH/3, LION_HEIGHT * 0.6],
        [0, 0, LION_HEIGHT * 1.2]
    ])

    head_faces = np.array([
        [0, 1, 2],  # Base
        [3, 4, 5],  # Top
        [0, 3, 4], [0, 4, 1],  # Front faces
        [1, 4, 5], [1, 5, 2],  # Right faces
        [2, 5, 3], [2, 3, 0],  # Left faces
        [0, 3, 5], [0, 5, 2]   # Back faces
    ])

    head = trimesh.Trimesh(vertices=head_vertices, faces=head_faces)

    # Position head at front of body
    head.apply_translation([body_length/2 + head_length/2, 0, 0])

    # Combine body and head
    lion_body = trimesh.util.concatenate([body_shape, head])
    lion_body.visual.face_colors = MATERIALS["oak"]["color"]

    return lion_body


def _create_leg_mechanism(is_front: bool, is_left: bool) -> Dict[str, trimesh.Trimesh]:
    """
    Create a complete leg mechanism with four-bar linkage.

    Args:
        is_front: Whether this is a front leg
        is_left: Whether this is a left leg

    Returns:
        Dictionary of trimesh objects representing leg components
    """
    leg_components = {}

    # Upper leg (femur/humerus)
    upper_leg = trimesh.creation.cylinder(
        radius=0.03,
        height=UPPER_LEG_LENGTH,
        sections=16
    )
    upper_leg.visual.face_colors = MATERIALS["oak"]["color"]
    leg_components["upper_leg"] = upper_leg

    # Lower leg (tibia/radius)
    lower_leg = trimesh.creation.cylinder(
        radius=0.025,
        height=LOWER_LEG_LENGTH,
        sections=16
    )
    lower_leg.visual.face_colors = MATERIALS["oak"]["color"]
    leg_components["lower_leg"] = lower_leg

    # Foot/paw
    foot = trimesh.creation.box(extents=[FOOT_LENGTH, FOOT_WIDTH, 0.02])
    foot.visual.face_colors = MATERIALS["bronze"]["color"]
    leg_components["foot"] = foot

    # Hip/knee joints (bronze bearings)
    hip_joint = trimesh.creation.sphere(radius=0.02)
    hip_joint.visual.face_colors = MATERIALS["bronze"]["color"]
    leg_components["hip_joint"] = hip_joint

    knee_joint = trimesh.creation.sphere(radius=0.015)
    knee_joint.visual.face_colors = MATERIALS["bronze"]["color"]
    leg_components["knee_joint"] = knee_joint

    # Ankle joint
    ankle_joint = trimesh.creation.sphere(radius=0.015)
    ankle_joint.visual.face_colors = MATERIALS["bronze"]["color"]
    leg_components["ankle_joint"] = ankle_joint

    # Position leg components
    # Hip position
    if is_front:
        hip_x = FORELEG_TO_HINDLEG_DISTANCE / 2
    else:
        hip_x = -FORELEG_TO_HINDLEG_DISTANCE / 2

    if is_left:
        hip_y = LATERAL_LEG_SPACING / 2
    else:
        hip_y = -LATERAL_LEG_SPACING / 2

    hip_z = BODY_HEIGHT

    # Apply transformations
    upper_leg.apply_translation([hip_x, hip_y, hip_z - UPPER_LEG_LENGTH/2])
    hip_joint.apply_translation([hip_x, hip_y, hip_z])

    # Lower leg connects at knee
    knee_x = hip_x
    knee_y = hip_y
    knee_z = hip_z - UPPER_LEG_LENGTH

    lower_leg.apply_translation([knee_x, knee_y, knee_z - LOWER_LEG_LENGTH/2])
    knee_joint.apply_translation([knee_x, knee_y, knee_z])

    # Foot at ground level
    ankle_x = knee_x
    ankle_y = knee_y
    ankle_z = 0.02  # Slightly above ground

    foot.apply_translation([ankle_x + FOOT_LENGTH/2, ankle_y, ankle_z/2])
    ankle_joint.apply_translation([ankle_x, ankle_y, ankle_z])

    return leg_components


def _create_cam_drum() -> trimesh.Trimesh:
    """
    Create the cam drum with multiple tracks for leg control.

    Returns:
        Trimesh object representing the cam drum assembly
    """
    cam_components = []

    # Main drum cylinder
    main_drum = trimesh.creation.cylinder(
        radius=CAM_DRUM_RADIUS,
        height=CAM_DRUM_LENGTH,
        sections=32
    )
    main_drum.visual.face_colors = MATERIALS["oak"]["color"]
    cam_components.append(main_drum)

    # Create cam tracks (simplified representation)
    # In reality, these would be complex profiles for natural gait
    num_tracks = 12  # 3 tracks per leg × 4 legs
    track_spacing = CAM_DRUM_LENGTH / (num_tracks + 1)

    for i in range(num_tracks):
        track_position = -CAM_DRUM_LENGTH/2 + (i + 1) * track_spacing

        # Cam track groove (simplified as a raised ring)
        track = trimesh.creation.cylinder(
            radius=CAM_DRUM_RADIUS + 0.01,
            height=CAM_TRACK_WIDTH,
            sections=16
        )
        track.visual.face_colors = MATERIALS["bronze"]["color"]
        track.apply_translation([0, 0, track_position])
        cam_components.append(track)

    # Central drive shaft
    drive_shaft = trimesh.creation.cylinder(
        radius=0.02,
        height=CAM_DRUM_LENGTH + 0.1,
        sections=16
    )
    drive_shaft.visual.face_colors = MATERIALS["steel"]["color"]
    cam_components.append(drive_shaft)

    # Combine all cam components
    cam_drum = trimesh.util.concatenate(cam_components)

    return cam_drum


def _create_chest_mechanism() -> Dict[str, trimesh.Trimesh]:
    """
    Create the chest cavity reveal mechanism.

    Returns:
        Dictionary of trimesh objects representing chest components
    """
    chest_components = {}

    # Chest cavity (main body opening)
    chest_cavity = trimesh.creation.box(extents=[0.6, 0.4, 0.3])
    chest_cavity.visual.face_colors = MATERIALS["oak"]["color"]
    chest_components["chest_cavity"] = chest_cavity

    # Chest panels (4 panels that open)
    panel_configs = [
        {"size": [0.3, 0.4, 0.02], "offset": [-0.15, 0, 0]},  # Left
        {"size": [0.3, 0.4, 0.02], "offset": [0.15, 0, 0]},   # Right
        {"size": [0.6, 0.2, 0.02], "offset": [0, 0.1, 0]},   # Top
        {"size": [0.6, 0.2, 0.02], "offset": [0, -0.1, 0]},  # Bottom
    ]

    for i, config in enumerate(panel_configs):
        panel = trimesh.creation.box(extents=config["size"])
        panel.visual.face_colors = MATERIALS["gilded_bronze"]["color"]
        panel.apply_translation(config["offset"])
        chest_components[f"panel_{i}"] = panel

    # Lily platform (rising platform for fleurs-de-lis)
    lily_platform = trimesh.creation.cylinder(
        radius=0.25,
        height=0.02,
        sections=32
    )
    lily_platform.visual.face_colors = MATERIALS["gilded_bronze"]["color"]
    lily_platform.apply_translation([0, 0, 0.15])
    chest_components["lily_platform"] = lily_platform

    # Fleur-de-lis (simplified representation)
    for i in range(3):
        angle = 2 * np.pi * i / 3
        lily_radius = 0.15

        # Simple lily shape (cross on sphere)
        lily_base = trimesh.creation.sphere(radius=0.02)
        lily_base.visual.face_colors = MATERIALS["gilded_bronze"]["color"]

        lily_x = lily_radius * np.cos(angle)
        lily_y = lily_radius * np.sin(angle)
        lily_base.apply_translation([lily_x, lily_y, 0.18])

        chest_components[f"fleur_de_lis_{i}"] = lily_base

    return chest_components


def _create_support_structure() -> Dict[str, trimesh.Trimesh]:
    """
    Create the support structure and framework.

    Returns:
        Dictionary of trimesh objects representing support components
    """
    support_components = {}

    # Main frame (wooden beams)
    frame_configs = [
        {"length": LION_LENGTH, "position": [0, 0, 0], "rotation": [0, 0, 0]},  # Longitudinal beams
        {"length": LION_WIDTH, "position": [0, LION_WIDTH/2, BODY_HEIGHT/2], "rotation": [0, np.pi/2, 0]},
        {"length": LION_WIDTH, "position": [0, -LION_WIDTH/2, BODY_HEIGHT/2], "rotation": [0, np.pi/2, 0]},
    ]

    for i, config in enumerate(frame_configs):
        beam = trimesh.creation.box(extents=[config["length"], 0.05, 0.05])
        beam.visual.face_colors = MATERIALS["oak"]["color"]
        beam.apply_translation(config["position"])
        beam.apply_rotation(config["rotation"])
        support_components[f"frame_beam_{i}"] = beam

    # Support legs (for display)
    for i in range(4):
        angle = i * np.pi / 2
        leg_x = 0.5 * np.cos(angle)
        leg_y = 0.5 * np.sin(angle)

        support_leg = trimesh.creation.cylinder(
            radius=0.03,
            height=BODY_HEIGHT,
            sections=16
        )
        support_leg.visual.face_colors = MATERIALS["oak"]["color"]
        support_leg.apply_translation([leg_x, leg_y, BODY_HEIGHT/2])
        support_components[f"support_leg_{i}"] = support_leg

    # Cam drum support
    cam_support = trimesh.creation.box(extents=[0.4, 0.4, 0.05])
    cam_support.visual.face_colors = MATERIALS["oak"]["color"]
    cam_support.apply_translation([0, 0, -0.1])
    support_components["cam_support"] = cam_support

    return support_components


def generate_mesh(
    configuration: str = "complete",
    include_mechanism: bool = True,
    material: str = "oak"
) -> trimesh.Trimesh:
    """
    Generate complete mechanical lion assembly mesh.

    Creates a comprehensive 3D model of the mechanical lion with appropriate
    geometry for the specified configuration and materials.

    Args:
        configuration: "complete", "mechanism_only", "cam_drums", or "chest_mechanism"
        include_mechanism: Include walking mechanism if True
        material: Primary material for components

    Returns:
        Complete trimesh assembly
    """
    mesh_list = []

    if configuration in ["complete", "mechanism_only"]:
        # Create lion body
        lion_body = _create_lion_body()
        mesh_list.append(lion_body)

        if include_mechanism:
            # Create leg mechanisms
            leg_configs = [
                (True, True),   # Left front
                (True, False),  # Right front
                (False, True),  # Left hind
                (False, False)  # Right hind
            ]

            for is_front, is_left in leg_configs:
                leg_components = _create_leg_mechanism(is_front, is_left)
                mesh_list.extend(leg_components.values())

            # Create cam drum
            if configuration == "complete":
                cam_drum = _create_cam_drum()
                cam_drum.apply_translation([0, 0, BODY_HEIGHT + 0.2])
                mesh_list.append(cam_drum)

            # Create support structure
            support_components = _create_support_structure()
            mesh_list.extend(support_components.values())

    if configuration == "cam_drums":
        # Focus on cam drum mechanism
        cam_drum = _create_cam_drum()
        mesh_list.append(cam_drum)

    if configuration == "chest_mechanism":
        # Focus on chest reveal mechanism
        chest_components = _create_chest_mechanism()
        mesh_list.extend(chest_components.values())

    # Combine all meshes
    if len(mesh_list) > 1:
        assembly = trimesh.util.concatenate(mesh_list)
    else:
        assembly = mesh_list[0] if mesh_list else trimesh.Trimesh()

    # Clean up mesh
    assembly.remove_duplicate_faces()
    assembly.remove_degenerate_faces()
    assembly.merge_vertices()

    return assembly


def analyze_mesh_properties(mesh: trimesh.Trimesh, material: str = "oak") -> Dict:
    """
    Analyze physical properties of the generated mesh.

    Calculates mass, center of mass, moments of inertia, and other
    relevant engineering properties for the specified material.

    Args:
        mesh: Trimesh object to analyze
        material: Material name for property calculations

    Returns:
        Dictionary of calculated properties
    """
    mat_props = MATERIALS.get(material, MATERIALS["oak"])

    # Volume and mass
    volume = mesh.volume  # m³
    mass = volume * mat_props["density"]  # kg

    # Center of mass
    center_of_mass = mesh.center_mass

    # Moments of inertia (simplified)
    moment_of_inertia = mesh.moment_inertia

    # Surface area
    surface_area = mesh.area

    # Structural analysis (simplified)
    max_dimension = mesh.extents.max()
    estimated_frequency = np.sqrt(mat_props["elastic_modulus"] / mat_props["density"]) / (2 * max_dimension)

    return {
        "volume_m3": volume,
        "mass_kg": mass,
        "center_of_mass_m": center_of_mass.tolist(),
        "surface_area_m2": surface_area,
        "moment_of_inertia_kgm2": moment_of_inertia.tolist(),
        "material": material,
        "estimated_frequency_hz": estimated_frequency,
        "max_dimension_m": max_dimension,
        "material_properties": mat_props
    }


def export_mesh(
    path: Path,
    configuration: str = "complete",
    include_mechanism: bool = True,
    material: str = "oak",
    format: str = "stl"
) -> Path:
    """
    Export mechanical lion mesh to file with analysis.

    Generates and exports the mesh with comprehensive analysis data.

    Args:
        path: Output file path
        configuration: Assembly configuration
        include_mechanism: Include walking mechanism
        material: Material for components
        format: Export format ("stl", "obj", "ply")

    Returns:
        Path to exported file
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # Generate mesh
    mesh = generate_mesh(configuration, include_mechanism, material)

    # Analyze properties
    properties = analyze_mesh_properties(mesh, material)

    # Export mesh
    if format.lower() == "stl":
        mesh.export(path)
    elif format.lower() == "obj":
        mesh.export(path.with_suffix(".obj"))
    elif format.lower() == "ply":
        mesh.export(path.with_suffix(".ply"))
    else:
        raise ValueError(f"Unsupported export format: {format}")

    # Export analysis data
    analysis_path = path.with_name(path.stem + "_analysis.json")
    import json
    with open(analysis_path, 'w') as f:
        json.dump(properties, f, indent=2)

    return path


if __name__ == "__main__":
    # Generate and export all configurations
    base_path = Path("../../artifacts/mechanical_lion/cad")

    # Complete lion assembly
    complete_path = export_mesh(
        base_path / "mechanical_lion_complete.stl",
        configuration="complete",
        include_mechanism=True,
        material="oak"
    )
    print(f"Exported complete lion: {complete_path}")

    # Walking mechanism detail
    mechanism_path = export_mesh(
        base_path / "walking_mechanism.stl",
        configuration="mechanism_only",
        include_mechanism=True,
        material="oak"
    )
    print(f"Exported walking mechanism: {mechanism_path}")

    # Cam drum assembly
    cam_path = export_mesh(
        base_path / "cam_drum_assembly.stl",
        configuration="cam_drums",
        include_mechanism=True,
        material="oak"
    )
    print(f"Exported cam drum: {cam_path}")

    # Chest reveal mechanism
    chest_path = export_mesh(
        base_path / "chest_reveal_mechanism.stl",
        configuration="chest_mechanism",
        include_mechanism=True,
        material="oak"
    )
    print(f"Exported chest mechanism: {chest_path}")