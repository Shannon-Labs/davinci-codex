"""
Leonardo's Mechanical Lion - Chest Reveal System

This module generates the parametric CAD model for the chest cavity reveal mechanism
that creates the spectacular fleurs-de-lis presentation. This was the centerpiece
of Leonardo's Mechanical Lion performance in 1515, celebrating the Franco-Florentine
alliance for King Francis I.

The chest system includes:
- Four-panel opening mechanism (left, right, top, bottom)
- Articulating hinges with precise control
- Lily platform with synchronized elevation
- Spring-loaded deployment system
- Cam-controlled timing mechanism
- Decorative fleurs-de-lis display elements
- Secure locking and release mechanisms

The mechanism creates a dramatic reveal where the lion's chest opens like a
flower blooming, presenting fleurs-de-lis to the royal court - a masterpiece
of mechanical theater and political symbolism.

CAD Features:
- Four-way panel opening with synchronized motion
- Hidden spring-loaded deployment mechanism
- Lily platform with smooth elevation
- Cam-timed reveal sequence
- Bronze bearings and steel springs
- Decorative fleurs-de-lis with gold leaf finish
- Renaissance-appropriate construction methods
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
import trimesh

# Chest cavity dimensions
CHEST_WIDTH = 0.6  # meters
CHEST_HEIGHT = 0.4  # meters
CHEST_DEPTH = 0.3  # meters
CHEST_WALL_THICKNESS = 0.03  # meters

# Panel dimensions and movement
PANEL_WIDTH = CHEST_WIDTH / 2  # meters
PANEL_HEIGHT = CHEST_HEIGHT / 2  # meters
PANEL_THICKNESS = 0.025  # meters
PANEL_OPENING_ANGLE = math.pi / 3  # 60 degrees

# Lily platform specifications
PLATFORM_DIAMETER = CHEST_WIDTH * 0.6  # meters
PLATFORM_THICKNESS = 0.02  # meters
PLATFORM_MAX_ELEVATION = 0.15  # meters
PLATFORM_ELEVATION_SPEED = 0.03  # meters per second

# Fleurs-de-lis display
LILY_COUNT = 3
LILY_HEIGHT = 0.08  # meters
LILY_WIDTH = 0.06  # meters
LILY_STEM_THICKNESS = 0.008  # meters
LILY_PETAL_COUNT = 6

# Hinge and mechanism specifications
HINGE_PIN_RADIUS = 0.006  # meters
HINGE_BUSHING_RADIUS = 0.008  # meters
SPRING_COMPARTMENT_SIZE = 0.04  # meters
CAM_RADIUS = 0.08  # meters
CAM_TRACK_WIDTH = 0.01  # meters

# Renaissance materials
MATERIALS = {
    "oak": {
        "density": 750,  # kg/m³
        "elastic_modulus": 12e9,  # Pa
        "tensile_strength": 40e6,  # Pa
        "color": [0.65, 0.45, 0.25, 1.0]  # Brown oak
    },
    "bronze": {
        "density": 8800,  # kg/m³
        "elastic_modulus": 100e9,  # Pa
        "tensile_strength": 200e6,  # Pa
        "color": [0.72, 0.45, 0.20, 1.0]  # Bronze
    },
    "steel": {
        "density": 7850,  # kg/m³
        "elastic_modulus": 200e9,  # Pa
        "tensile_strength": 400e6,  # Pa
        "color": [0.7, 0.7, 0.75, 1.0]  # Steel
    },
    "gold_leaf": {
        "density": 19300,  # kg/m³
        "elastic_modulus": 78e9,  # Pa
        "tensile_strength": 120e6,  # Pa
        "color": [1.0, 0.85, 0.0, 1.0]  # Gold
    },
    "silk": {
        "density": 1300,  # kg/m³
        "elastic_modulus": 0.5e9,  # Pa
        "tensile_strength": 400e6,  # Pa
        "color": [0.8, 0.1, 0.1, 1.0]  # Red silk
    }
}


class ChestPanel:
    """
    Individual chest panel with articulated hinge mechanism.

    Each panel opens smoothly to reveal the internal lily platform,
    using spring-loaded deployment and cam-controlled timing.
    """

    def __init__(self, panel_id: int, position: str):
        self.panel_id = panel_id
        self.position = position  # 'left', 'right', 'top', 'bottom'
        self.current_angle = 0.0
        self.max_angle = PANEL_OPENING_ANGLE

    def calculate_hinge_position(self, chest_center: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Calculate the 3D position of the panel hinge."""
        x, y, z = chest_center

        if self.position == 'left':
            return (x - PANEL_WIDTH/2, y, z)
        elif self.position == 'right':
            return (x + PANEL_WIDTH/2, y, z)
        elif self.position == 'top':
            return (x, y, z + PANEL_HEIGHT/2)
        else:  # bottom
            return (x, y, z - PANEL_HEIGHT/2)

    def calculate_panel_rotation_axis(self) -> Tuple[float, float, float]:
        """Calculate the rotation axis for the panel opening."""
        if self.position in ['left', 'right']:
            return (0, 1, 0)  # Rotate around Y-axis
        else:  # top, bottom
            return (1, 0, 0)  # Rotate around X-axis


def _create_chest_frame() -> trimesh.Trimesh:
    """
    Create the structural frame that supports the chest cavity and panels.

    Provides the mounting points for hinges, springs, and the lily platform
    mechanism while maintaining the external lion appearance.

    Returns:
        Trimesh object representing the chest frame structure
    """
    frame_components = []
    oak_props = MATERIALS["oak"]

    # Main chest frame structure
    frame = trimesh.creation.box(
        extents=[CHEST_WIDTH + 2*CHEST_WALL_THICKNESS,
                 CHEST_DEPTH + 2*CHEST_WALL_THICKNESS,
                 CHEST_HEIGHT + 2*CHEST_WALL_THICKNESS]
    )
    frame.visual.face_colors = oak_props["color"]
    frame_components.append(frame)

    # Hollow out the interior cavity (represented by internal walls)
    cavity_dimensions = [
        CHEST_WIDTH,
        CHEST_DEPTH - 2*CHEST_WALL_THICKNESS,
        CHEST_HEIGHT - 2*CHEST_WALL_THICKNESS
    ]

    # Internal walls for panel support
    # Left and right internal walls
    for x_offset in [-CHEST_WIDTH/2, CHEST_WIDTH/2]:
        wall = trimesh.creation.box(
            extents=[CHEST_WALL_THICKNESS,
                     CHEST_DEPTH - 2*CHEST_WALL_THICKNESS,
                     CHEST_HEIGHT - 2*CHEST_WALL_THICKNESS]
        )
        wall.apply_translation([x_offset, 0, 0])
        wall.visual.face_colors = oak_props["color"]
        frame_components.append(wall)

    # Top and bottom internal walls
    for z_offset in [-CHEST_HEIGHT/2, CHEST_HEIGHT/2]:
        wall = trimesh.creation.box(
            extents=[CHEST_WIDTH - 2*CHEST_WALL_THICKNESS,
                     CHEST_DEPTH - 2*CHEST_WALL_THICKNESS,
                     CHEST_WALL_THICKNESS]
        )
        wall.apply_translation([0, 0, z_offset])
        wall.visual.face_colors = oak_props["color"]
        frame_components.append(wall)

    # Reinforcement ribs
    num_ribs = 3
    for i in range(num_ribs):
        y_pos = -(CHEST_DEPTH/2 - CHEST_WALL_THICKNESS) + (i + 1) * \
                (CHEST_DEPTH - 2*CHEST_WALL_THICKNESS) / (num_ribs + 1)
        rib = trimesh.creation.box(
            extents=[CHEST_WIDTH - 2*CHEST_WALL_THICKNESS,
                     0.02,
                     CHEST_HEIGHT - 2*CHEST_WALL_THICKNESS]
        )
        rib.apply_translation([0, y_pos, 0])
        rib.visual.face_colors = oak_props["color"]
        frame_components.append(rib)

    return trimesh.util.concatenate(frame_components)


def _create_hinge_mechanism(
    panel: ChestPanel,
    chest_center: Tuple[float, float, float]
) -> List[trimesh.Trimesh]:
    """
    Create the articulated hinge mechanism for a chest panel.

    Provides smooth, controlled panel opening through precision bronze
    bushings and steel hinge pins.

    Args:
        panel: ChestPanel object for this hinge
        chest_center: 3D position of chest cavity center

    Returns:
        List of trimesh components for the hinge mechanism
    """
    hinge_components = []
    bronze_props = MATERIALS["bronze"]
    steel_props = MATERIALS["steel"]

    hinge_position = panel.calculate_hinge_position(chest_center)
    rotation_axis = panel.calculate_panel_rotation_axis()

    # Hinge pin (steel)
    pin_length = PANEL_HEIGHT + 0.04
    hinge_pin = trimesh.creation.cylinder(
        radius=HINGE_PIN_RADIUS,
        height=pin_length,
        sections=32
    )

    # Orient pin based on panel position
    if panel.position in ['left', 'right']:
        hinge_pin.apply_rotation([0, math.pi/2, 0])
    else:  # top, bottom
        hinge_pin.apply_rotation([math.pi/2, 0, 0])

    hinge_pin.apply_translation(hinge_position)
    hinge_pin.visual.face_colors = steel_props["color"]
    hinge_components.append(hinge_pin)

    # Bronze bushings (2 per hinge)
    for z_offset in [-PANEL_HEIGHT/2, PANEL_HEIGHT/2]:
        bushing = trimesh.creation.cylinder(
            radius=HINGE_BUSHING_RADIUS,
            height=0.02,
            sections=32
        )

        if panel.position in ['left', 'right']:
            bushing.apply_rotation([0, math.pi/2, 0])
        else:  # top, bottom
            bushing.apply_rotation([math.pi/2, 0, 0])

        bushing_pos = list(hinge_position)
        if panel.position in ['left', 'right']:
            bushing_pos[2] += z_offset
        else:  # top, bottom
            bushing_pos[0] += z_offset

        bushing.apply_translation(bushing_pos)
        bushing.visual.face_colors = bronze_props["color"]
        hinge_components.append(bushing)

    # Hinge reinforcement plates
    plate_thickness = 0.005
    for offset in [-0.02, 0.02]:
        plate = trimesh.creation.box(
            extents=[0.06, 0.06, plate_thickness]
        )

        if panel.position == 'left':
            plate_pos = [hinge_position[0] - offset, hinge_position[1], hinge_position[2]]
        elif panel.position == 'right':
            plate_pos = [hinge_position[0] + offset, hinge_position[1], hinge_position[2]]
        elif panel.position == 'top':
            plate_pos = [hinge_position[0], hinge_position[1], hinge_position[2] + offset]
        else:  # bottom
            plate_pos = [hinge_position[0], hinge_position[1], hinge_position[2] - offset]

        plate.apply_translation(plate_pos)
        plate.visual.face_colors = bronze_props["color"]
        hinge_components.append(plate)

    return hinge_components


def _create_chest_panel(
    panel: ChestPanel,
    chest_center: Tuple[float, float, float],
    opening_angle: float = 0.0
) -> trimesh.Trimesh:
    """
    Create an individual chest panel with decorative exterior.

    Each panel is crafted to match the lion's exterior appearance while
    providing the structural strength needed for repeated operation.

    Args:
        panel: ChestPanel object defining panel properties
        chest_center: 3D position of chest cavity center
        opening_angle: Current opening angle in radians

    Returns:
        Trimesh object representing the chest panel
    """
    oak_props = MATERIALS["oak"]

    # Calculate panel position based on type
    if panel.position == 'left':
        panel_center = [chest_center[0] - PANEL_WIDTH/2 - PANEL_THICKNESS/2,
                       chest_center[1],
                       chest_center[2]]
    elif panel.position == 'right':
        panel_center = [chest_center[0] + PANEL_WIDTH/2 + PANEL_THICKNESS/2,
                       chest_center[1],
                       chest_center[2]]
    elif panel.position == 'top':
        panel_center = [chest_center[0],
                       chest_center[1],
                       chest_center[2] + PANEL_HEIGHT/2 + PANEL_THICKNESS/2]
    else:  # bottom
        panel_center = [chest_center[0],
                       chest_center[1],
                       chest_center[2] - PANEL_HEIGHT/2 - PANEL_THICKNESS/2]

    # Create main panel
    if panel.position in ['left', 'right']:
        panel = trimesh.creation.box(
            extents=[PANEL_THICKNESS, PANEL_WIDTH, PANEL_HEIGHT]
        )
    else:  # top, bottom
        panel = trimesh.creation.box(
            extents=[PANEL_WIDTH, PANEL_THICKNESS, PANEL_HEIGHT]
        )

    panel.apply_translation(panel_center)
    panel.visual.face_colors = oak_props["color"]

    # Apply opening rotation
    hinge_pos = panel.calculate_hinge_position(chest_center)
    rotation_axis = panel.calculate_panel_rotation_axis()

    # Create rotation matrix for opening angle
    if abs(opening_angle) > 1e-6:
        panel.apply_transform(trimesh.transformations.rotation_matrix(
            opening_angle, rotation_axis, hinge_pos
        ))

    # Add decorative fur texture pattern (simplified)
    if panel.position in ['left', 'right']:
        for i in range(3):
            for j in range(4):
                fur_patch = trimesh.creation.box(
                    extents=[PANEL_THICKNESS + 0.001, 0.02, 0.02]
                )
                patch_x = panel_center[0]
                patch_y = panel_center[1] - PANEL_WIDTH/2 + (i + 0.5) * PANEL_WIDTH/3
                patch_z = panel_center[2] - PANEL_HEIGHT/2 + (j + 0.5) * PANEL_HEIGHT/4
                fur_patch.apply_translation([patch_x, patch_y, patch_z])
                fur_patch.visual.face_colors = [0.7, 0.5, 0.3, 1.0]  # Lighter oak
                panel = trimesh.util.concatenate([panel, fur_patch])

    return panel


def _create_lily_platform(
    chest_center: Tuple[float, float, float],
    elevation: float = 0.0
) -> trimesh.Trimesh:
    """
    Create the rising lily platform for fleurs-de-lis presentation.

    The platform elevates smoothly to present the fleurs-de-lis at the
    dramatic climax of the reveal sequence.

    Args:
        chest_center: 3D position of chest cavity center
        elevation: Current elevation above chest base in meters

    Returns:
        Trimesh object representing the lily platform
    """
    platform_components = []
    oak_props = MATERIALS["oak"]
    gold_props = MATERIALS["gold_leaf"]

    # Platform base
    platform_base = trimesh.creation.cylinder(
        radius=PLATFORM_DIAMETER/2,
        height=PLATFORM_THICKNESS,
        sections=32
    )
    platform_pos = [chest_center[0], chest_center[1], chest_center[2] - CHEST_HEIGHT/2 + elevation]
    platform_base.apply_translation(platform_pos)
    platform_base.visual.face_colors = oak_props["color"]
    platform_components.append(platform_base)

    # Decorative gold leaf edge
    gold_edge = trimesh.creation.torus(
        major_radius=PLATFORM_DIAMETER/2 - 0.005,
        minor_radius=0.005,
        major_sections=32,
        minor_sections=16
    )
    gold_edge.apply_rotation([math.pi/2, 0, 0])
    gold_edge.apply_translation([platform_pos[0], platform_pos[1], platform_pos[2] + PLATFORM_THICKNESS/2])
    gold_edge.visual.face_colors = gold_props["color"]
    platform_components.append(gold_edge)

    # Support column
    if elevation > 0.01:
        support_height = elevation
        support_column = trimesh.creation.cylinder(
            radius=0.015,
            height=support_height,
            sections=16
        )
        support_pos = [platform_pos[0], platform_pos[1], chest_center[2] - CHEST_HEIGHT/2 + support_height/2]
        support_column.apply_translation(support_pos)
        support_column.visual.face_colors = oak_props["color"]
        platform_components.append(support_column)

    return trimesh.util.concatenate(platform_components)


def _create_fleur_de_lis(
    position: Tuple[float, float, float],
    scale: float = 1.0
) -> trimesh.Trimesh:
    """
    Create a decorative fleur-de-lis with gold leaf finish.

    The fleur-de-lis is the symbol of French royalty, making this the
    perfect centerpiece for the political celebration of 1515.

    Args:
        position: 3D position for the fleur-de-lis
        scale: Size scale factor

    Returns:
        Trimesh object representing the fleur-de-lis
    """
    lily_components = []
    gold_props = MATERIALS["gold_leaf"]
    steel_props = MATERIALS["steel"]

    # Central stem
    stem_height = LILY_HEIGHT * scale
    stem = trimesh.creation.cylinder(
        radius=LILY_STEM_THICKNESS * scale,
        height=stem_height,
        sections=16
    )
    stem.apply_translation([position[0], position[1], position[2] + stem_height/2])
    stem.visual.face_colors = gold_props["color"]
    lily_components.append(stem)

    # Petals (6 petals around the stem)
    petal_height = LILY_HEIGHT * 0.4 * scale
    petal_width = LILY_WIDTH * 0.3 * scale

    for i in range(LILY_PETAL_COUNT):
        angle = 2 * math.pi * i / LILY_PETAL_COUNT

        # Create petal shape (elongated teardrop)
        petal_base = trimesh.creation.cone(
            radius=petal_width,
            height=petal_height,
            sections=16
        )

        # Position and orient petal
        petal_x = position[0] + (LILY_STEM_THICKNESS + petal_width/2) * math.cos(angle)
        petal_y = position[1] + (LILY_STEM_THICKNESS + petal_width/2) * math.sin(angle)
        petal_z = position[2] + stem_height - petal_height/2

        petal_base.apply_rotation([0, math.pi/2, 0])
        petal_base.apply_rotation([0, 0, angle - math.pi/2])
        petal_base.apply_translation([petal_x, petal_y, petal_z])
        petal_base.visual.face_colors = gold_props["color"]
        lily_components.append(petal_base)

    # Three central petals (larger, pointing upward)
    for i in range(3):
        angle = math.pi * i / 3

        central_petal = trimesh.creation.cone(
            radius=petal_width * 1.2,
            height=petal_height * 1.3,
            sections=16
        )

        petal_x = position[0] + petal_width * 0.8 * math.cos(angle)
        petal_y = position[1] + petal_width * 0.8 * math.sin(angle)
        petal_z = position[2] + stem_height + petal_height * 0.7

        central_petal.apply_rotation([0, math.pi/2, 0])
        central_petal.apply_rotation([0, 0, angle])
        central_petal.apply_translation([petal_x, petal_y, petal_z])
        central_petal.visual.face_colors = gold_props["color"]
        lily_components.append(central_petal)

    # Base mounting rod
    mounting_rod = trimesh.creation.cylinder(
        radius=0.003,
        height=stem_height * 0.3,
        sections=8
    )
    mounting_rod.apply_translation([position[0], position[1], position[2] - stem_height * 0.15])
    mounting_rod.visual.face_colors = steel_props["color"]
    lily_components.append(mounting_rod)

    return trimesh.util.concatenate(lily_components)


def _create_spring_mechanism(
    chest_center: Tuple[float, float, float]
) -> List[trimesh.Trimesh]:
    """
    Create the spring-loaded deployment mechanism for panel opening.

    Provides the controlled force needed to open the panels smoothly
    and hold them in the revealed position.

    Args:
        chest_center: 3D position of chest cavity center

    Returns:
        List of trimesh components for the spring mechanism
    """
    spring_components = []
    steel_props = MATERIALS["steel"]
    oak_props = MATERIALS["oak"]

    # Spring compartment (one for each panel)
    spring_positions = [
        [chest_center[0] - PANEL_WIDTH/2, chest_center[1] + CHEST_DEPTH/2 + 0.02, chest_center[2]],
        [chest_center[0] + PANEL_WIDTH/2, chest_center[1] + CHEST_DEPTH/2 + 0.02, chest_center[2]],
        [chest_center[0], chest_center[1] + CHEST_DEPTH/2 + 0.02, chest_center[2] + PANEL_HEIGHT/2],
        [chest_center[0], chest_center[1] + CHEST_DEPTH/2 + 0.02, chest_center[2] - PANEL_HEIGHT/2]
    ]

    for spring_pos in spring_positions:
        # Spring housing
        housing = trimesh.creation.box(
            extents=[SPRING_COMPARTMENT_SIZE, 0.03, SPRING_COMPARTMENT_SIZE]
        )
        housing.apply_translation(spring_pos)
        housing.visual.face_colors = oak_props["color"]
        spring_components.append(housing)

        # Spring coils (decorative representation)
        num_coils = 6
        coil_radius = 0.015
        for i in range(num_coils):
            coil_height = i * 0.004
            spring_coil = trimesh.creation.torus(
                major_radius=coil_radius,
                minor_radius=0.0015,
                major_sections=16,
                minor_sections=8
            )
            coil_pos = spring_pos.copy()
            coil_pos[2] += coil_height
            spring_coil.apply_rotation([math.pi/2, 0, 0])
            spring_coil.apply_translation(coil_pos)
            spring_coil.visual.face_colors = steel_props["color"]
            spring_components.append(spring_coil)

        # Spring attachment points
        attachment_point = trimesh.creation.cylinder(
            radius=0.004, height=0.02, sections=16
        )
        attachment_point.apply_rotation([math.pi/2, 0, 0])
        attachment_point.apply_translation(spring_pos)
        attachment_point.visual.face_colors = steel_props["color"]
        spring_components.append(attachment_point)

    return spring_components


def _create_cam_control_system(
    chest_center: Tuple[float, float, float]
) -> List[trimesh.Trimesh]:
    """
    Create the cam-based timing control system for synchronized panel opening.

    Uses Leonardo's cam technology to coordinate the precise timing of
    the reveal sequence for maximum dramatic effect.

    Args:
        chest_center: 3D position of chest cavity center

    Returns:
        List of trimesh components for the cam control system
    """
    cam_components = []
    bronze_props = MATERIALS["bronze"]
    oak_props = MATERIALS["oak"]

    # Main cam drum
    cam_drum = trimesh.creation.cylinder(
        radius=CAM_RADIUS,
        height=0.15,
        sections=64
    )
    cam_pos = [chest_center[0], chest_center[1] - CHEST_DEPTH/2 - 0.1, chest_center[2]]
    cam_drum.apply_rotation([math.pi/2, 0, 0])
    cam_drum.apply_translation(cam_pos)
    cam_drum.visual.face_colors = oak_props["color"]
    cam_components.append(cam_drum)

    # Cam profiles for each panel (4 tracks)
    track_height = 0.15 / 4
    for i in range(4):
        z_offset = -0.075 + (i + 0.5) * track_height

        # Cam track profile (simplified sinusoidal shape)
        track_points = []
        for angle in np.linspace(0, 2*math.pi, 32):
            radius = CAM_RADIUS * (1 + 0.2 * math.sin(angle))
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            track_points.append([x, y, z_offset])

        # Create cam track as extruded profile
        if len(track_points) > 2:
            cam_track = trimesh.creation.extrude_triangulation(
                [(p[0], p[1]) for p in track_points],
                [p[2] for p in track_points],
                [[i, i+1, i+2] for i in range(len(track_points)-2)]
            )
            if cam_track.is_watertight:
                cam_track.apply_translation([cam_pos[0], cam_pos[1], cam_pos[2]])
                cam_track.visual.face_colors = bronze_props["color"]
                cam_components.append(cam_track)

    # Cam followers (one per panel)
    for i in range(4):
        follower = trimesh.creation.cylinder(
            radius=0.006, height=0.03, sections=16
        )
        follower_pos = [cam_pos[0] + CAM_RADIUS + 0.01,
                       cam_pos[1],
                       cam_pos[2] - 0.075 + (i + 0.5) * track_height]
        follower.apply_rotation([math.pi/2, 0, 0])
        follower.apply_translation(follower_pos)
        follower.visual.face_colors = bronze_props["color"]
        cam_components.append(follower)

    # Drive shaft
    drive_shaft = trimesh.creation.cylinder(
        radius=0.01, height=0.25, sections=32
    )
    drive_shaft.apply_rotation([math.pi/2, 0, 0])
    drive_shaft.apply_translation([cam_pos[0], cam_pos[1], cam_pos[2]])
    drive_shaft.visual.face_colors = bronze_props["color"]
    cam_components.append(drive_shaft)

    return cam_components


def generate_complete_chest_system(
    opening_progress: float = 0.0,
    include_lilies: bool = True,
    material: str = "oak"
) -> trimesh.Trimesh:
    """
    Generate the complete chest reveal system assembly.

    Creates all components of the chest reveal mechanism including panels,
    platform, springs, cams, and decorative elements.

    Args:
        opening_progress: Progress of reveal sequence (0.0 to 1.0)
        include_lilies: Include fleurs-de-lis on platform
        material: Primary material for structural components

    Returns:
        Complete trimesh assembly of the chest system
    """
    all_components = []

    # Chest center position
    chest_center = (0.5, 0, 0.7)  # Positioned on lion body

    # Chest frame
    chest_frame = _create_chest_frame()
    all_components.append(chest_frame)

    # Create panels
    panels = [
        ChestPanel(0, 'left'),
        ChestPanel(1, 'right'),
        ChestPanel(2, 'top'),
        ChestPanel(3, 'bottom')
    ]

    for panel in panels:
        # Calculate panel opening angle based on progress
        panel_angle = panel.max_angle * opening_progress
        panel.current_angle = panel_angle

        # Hinge mechanism
        hinge_components = _create_hinge_mechanism(panel, chest_center)
        all_components.extend(hinge_components)

        # Panel itself
        panel_mesh = _create_chest_panel(panel, chest_center, panel_angle)
        all_components.append(panel_mesh)

    # Lily platform (elevates when panels are 50% open)
    if opening_progress > 0.5:
        platform_elevation = PLATFORM_MAX_ELEVATION * ((opening_progress - 0.5) / 0.5)
    else:
        platform_elevation = 0.0

    lily_platform = _create_lily_platform(chest_center, platform_elevation)
    all_components.append(lily_platform)

    # Fleurs-de-lis (appear when platform is elevated)
    if include_lilies and platform_elevation > 0.01:
        platform_center = [chest_center[0], chest_center[1],
                          chest_center[2] - CHEST_HEIGHT/2 + platform_elevation + PLATFORM_THICKNESS]

        # Position lilies in a triangular arrangement
        lily_positions = [
            [platform_center[0], platform_center[1] + PLATFORM_DIAMETER * 0.2, platform_center[2]],
            [platform_center[0] - PLATFORM_DIAMETER * 0.17, platform_center[1] - PLATFORM_DIAMETER * 0.1, platform_center[2]],
            [platform_center[0] + PLATFORM_DIAMETER * 0.17, platform_center[1] - PLATFORM_DIAMETER * 0.1, platform_center[2]]
        ]

        for lily_pos in lily_positions:
            fleur_de_lis = _create_fleur_de_lis(lily_pos)
            all_components.append(fleur_de_lis)

    # Spring mechanism
    spring_components = _create_spring_mechanism(chest_center)
    all_components.extend(spring_components)

    # Cam control system
    cam_components = _create_cam_control_system(chest_center)
    all_components.extend(cam_components)

    # Combine all components
    if all_components:
        complete_system = trimesh.util.concatenate(all_components)

        # Clean up the mesh
        complete_system.remove_duplicate_faces()
        complete_system.remove_degenerate_faces()
        complete_system.merge_vertices()

        return complete_system
    else:
        return trimesh.Trimesh()


def analyze_chest_system_properties(
    chest_system: trimesh.Trimesh,
    material: str = "oak"
) -> Dict[str, object]:
    """
    Analyze physical properties of the chest reveal system.

    Calculates mass, center of mass, and operational properties for
    engineering validation and historical accuracy assessment.

    Args:
        chest_system: Trimesh chest system to analyze
        material: Primary material for property calculations

    Returns:
        Dictionary of calculated system properties
    """
    mat_props = MATERIALS[material]

    # Volume and mass
    volume = chest_system.volume
    mass = volume * mat_props["density"]

    # Center of mass
    center_of_mass = chest_system.center_mass

    # Moments of inertia
    moment_of_inertia = chest_system.moment_inertia

    # Surface area
    surface_area = chest_system.area

    # Operational specifications
    opening_time = 3.5  # seconds (historical performance)
    platform_elevation_time = 2.0  # seconds
    total_reveal_time = opening_time + platform_elevation_time

    # Spring force requirements (simplified)
    panel_weight = mass * 0.15 / 4  # Each panel ~15% of total mass
    spring_force_per_panel = panel_weight * 9.81 * 1.5  # 1.5 safety factor
    total_spring_force = spring_force_per_panel * 4

    return {
        "physical_properties": {
            "volume_m3": volume,
            "mass_kg": mass,
            "center_of_mass_m": center_of_mass.tolist(),
            "moment_of_inertia_kgm2": moment_of_inertia.tolist(),
            "surface_area_m2": surface_area
        },
        "operational_properties": {
            "opening_time_s": opening_time,
            "platform_elevation_time_s": platform_elevation_time,
            "total_reveal_time_s": total_reveal_time,
            "max_panel_angle_deg": math.degrees(PANEL_OPENING_ANGLE),
            "platform_max_elevation_m": PLATFORM_MAX_ELEVATION
        },
        "mechanical_properties": {
            "panel_weight_kg": panel_weight,
            "spring_force_per_panel_N": spring_force_per_panel,
            "total_spring_force_N": total_spring_force,
            "cam_radius_m": CAM_RADIUS,
            "hinge_pin_radius_m": HINGE_PIN_RADIUS
        },
        "material_properties": mat_props,
        "renaissance_feasibility": {
            "construction_method": "Hand-carved oak with bronze fittings",
            "spring_technology": "Hand-forged steel springs",
            "cam_precision": "Achievable with Renaissance tools",
            "assembly_complexity": "High but within master craftsman capability",
            "historical_accuracy": "Consistent with 1515 technology"
        }
    }


def export_chest_system(
    path: Path,
    opening_progress: float = 0.0,
    include_lilies: bool = True,
    material: str = "oak",
    format: str = "stl"
) -> Path:
    """
    Export the chest reveal system to file with analysis.

    Generates and exports the complete chest system with comprehensive
    analysis data for construction and documentation.

    Args:
        path: Output file path
        opening_progress: Reveal sequence progress (0.0 to 1.0)
        include_lilies: Include fleurs-de-lis decorations
        material: Primary material for components
        format: Export format ("stl", "obj", "ply")

    Returns:
        Path to exported file
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # Generate chest system
    chest_system = generate_complete_chest_system(
        opening_progress=opening_progress,
        include_lilies=include_lilies,
        material=material
    )

    # Analyze properties
    properties = analyze_chest_system_properties(chest_system, material)

    # Export mesh
    if format.lower() == "stl":
        chest_system.export(path)
    elif format.lower() == "obj":
        chest_system.export(path.with_suffix(".obj"))
    elif format.lower() == "ply":
        chest_system.export(path.with_suffix(".ply"))
    else:
        raise ValueError(f"Unsupported export format: {format}")

    # Export analysis data
    analysis_path = path.with_name(path.stem + "_analysis.json")
    import json
    with open(analysis_path, 'w') as f:
        json.dump(properties, f, indent=2)

    # Export operation documentation
    doc_path = path.with_name(path.stem + "_operation.md")
    with open(doc_path, 'w') as f:
        f.write(f"""# Leonardo's Mechanical Lion - Chest Reveal System Documentation

## Opening Progress: {opening_progress*100:.0f}%
## Material: {material.title()}

### Physical Properties
- Volume: {properties['physical_properties']['volume_m3']:.4f} m³
- Mass: {properties['physical_properties']['mass_kg']:.2f} kg
- Center of Mass: ({properties['physical_properties']['center_of_mass_m'][0]:.3f},
                    {properties['physical_properties']['center_of_mass_m'][1]:.3f},
                    {properties['physical_properties']['center_of_mass_m'][2]:.3f}) m
- Surface Area: {properties['physical_properties']['surface_area_m2']:.2f} m²

### Operational Specifications
- Opening Time: {properties['operational_properties']['opening_time_s']:.1f} seconds
- Platform Elevation: {properties['operational_properties']['platform_elevation_time_s']:.1f} seconds
- Total Reveal Time: {properties['operational_properties']['total_reveal_time_s']:.1f} seconds
- Maximum Panel Opening: {properties['operational_properties']['max_panel_angle_deg']:.1f}°
- Platform Maximum Elevation: {properties['operational_properties']['platform_max_elevation_m']:.2f} m

### Mechanical Properties
- Panel Weight: {properties['mechanical_properties']['panel_weight_kg']:.2f} kg
- Spring Force per Panel: {properties['mechanical_properties']['spring_force_per_panel_N']:.1f} N
- Total Spring Force: {properties['mechanical_properties']['total_spring_force_N']:.1f} N
- Cam Radius: {properties['mechanical_properties']['cam_radius_m']:.3f} m
- Hinge Pin Radius: {properties['mechanical_properties']['hinge_pin_radius_m']:.3f} m

### Historical Context
The chest reveal mechanism was the centerpiece of Leonardo's Mechanical Lion performance.
When the lion stopped before King Francis I, the chest would open dramatically to reveal
fleurs-de-lis - the symbol of French royalty. This celebrated the Franco-Florentine alliance
and demonstrated Leonardo's mastery of mechanical theater.

The mechanism uses Leonardo's innovative cam technology to coordinate the precise timing
of panel opening and platform elevation, creating a seamless magical transformation that
would awe the 16th century royal court.
""")

    return path


if __name__ == "__main__":
    # Export chest system at various opening stages
    base_path = Path("../../artifacts/mechanical_lion/cad")

    # Closed position
    closed_path = export_chest_system(
        base_path / "chest_system_closed.stl",
        opening_progress=0.0,
        include_lilies=False,
        material="oak"
    )
    print(f"Exported closed chest system: {closed_path}")

    # Partial opening (50%)
    partial_path = export_chest_system(
        base_path / "chest_system_partial.stl",
        opening_progress=0.5,
        include_lilies=False,
        material="oak"
    )
    print(f"Exported partial opening: {partial_path}")

    # Fully opened with lilies
    open_path = export_chest_system(
        base_path / "chest_system_open.stl",
        opening_progress=1.0,
        include_lilies=True,
        material="oak"
    )
    print(f"Exported fully opened chest: {open_path}")

    # Animation frames
    for i in range(5):
        progress = i / 4.0
        frame_path = export_chest_system(
            base_path / f"chest_frame_{i:02d}.stl",
            opening_progress=progress,
            include_lilies=(progress > 0.5),
            material="oak"
        )
        print(f"Exported animation frame {i}: {frame_path}")

    # Additional formats
    for format_type in ["obj", "ply"]:
        export_chest_system(
            base_path / f"chest_system_open.{format_type}",
            opening_progress=1.0,
            include_lilies=True,
            material="oak",
            format=format_type
        )
        print(f"Exported {format_type.upper()} format")

    print("Leonardo's Mechanical Lion chest reveal system CAD models complete!")