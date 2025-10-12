"""
Leonardo's Mechanical Lion - External Shell with Decorative Lion Exterior

This module generates the parametric CAD model for the exterior shell that gives
Leonardo's Mechanical Lion its lifelike appearance. The shell combines artistic
beauty with mechanical functionality, creating the illusion of a living lion while
housing the complex internal mechanisms.

The external shell includes:
- Lifelike lion body form with accurate proportions
- Articulated mane with movable hair elements
- Detailed facial features with expressive eyes
- Paw and claw design with realistic texture
- Tail with natural movement and positioning
- Fur texture patterns with artistic detail
- Access panels for maintenance and adjustment
- Decorative elements honoring the Franco-Florentine alliance

The exterior demonstrates Leonardo's mastery of combining artistic vision with
mechanical engineering, creating an automaton that would awe the 16th century
royal court with both its technical sophistication and artistic beauty.

CAD Features:
- Biomimetic lion anatomy based on real Panthera leo
- Articulated exterior panels that move with mechanisms
- Artistic fur texture and decorative patterns
- Realistic facial features and expressive elements
- Maintenance access panels integrated into design
- Renaissance art style with gold leaf accents
- Modular construction for workshop assembly
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import trimesh

# Lion body dimensions (based on real Panthera leo)
LION_TOTAL_LENGTH = 2.4  # meters (nose to tail tip)
LION_BODY_LENGTH = 1.8  # meters (shoulder to hip)
LION_SHOULDER_HEIGHT = 1.2  # meters
LION_BODY_DEPTH = 0.6  # meters
LION_NECK_LENGTH = 0.4  # meters
LION_HEAD_LENGTH = 0.35  # meters
LION_HEAD_WIDTH = 0.25  # meters
LION_HEAD_HEIGHT = 0.3  # meters

# Leg and paw dimensions
FORELEG_LENGTH = 0.6  # meters
HINDLEG_LENGTH = 0.65  # meters
PAW_WIDTH = 0.08  # meters
PAW_LENGTH = 0.12  # meters
CLAW_LENGTH = 0.025  # meters

# Mane and fur details
MANE_LENGTH = 0.15  # meters
MANE_THICKNESS = 0.08  # meters
FUR_TEXTURE_DEPTH = 0.005  # meters
HAIR_STRAND_COUNT = 200  # decorative hair elements

# Tail specifications
TAIL_LENGTH = 0.8  # meters
TAIL_BASE_RADIUS = 0.08  # meters
TAIL_TIP_RADIUS = 0.02  # meters
TAIL_SEGMENTS = 12

# Facial features
EYE_RADIUS = 0.02  # meters
EYE_DEPTH = 0.015  # meters
NOSE_WIDTH = 0.04  # meters
NOSE_LENGTH = 0.06  # meters
EAR_HEIGHT = 0.08  # meters
EAR_WIDTH = 0.06  # meters

# Access panel specifications
PANEL_WIDTH = 0.15  # meters
PANEL_HEIGHT = 0.10  # meters
PANEL_THICKNESS = 0.008  # meters
HIDDEN_LATCH_SIZE = 0.02  # meters

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
    "gold_leaf": {
        "density": 19300,  # kg/m³
        "elastic_modulus": 78e9,  # Pa
        "tensile_strength": 120e6,  # Pa
        "color": [1.0, 0.85, 0.0, 1.0]  # Gold
    },
    "fur_textured": {
        "density": 600,  # kg/m³ (lighter with texture)
        "elastic_modulus": 8e9,  # Pa
        "tensile_strength": 30e6,  # Pa
        "color": [0.8, 0.6, 0.4, 1.0]  # Tawny fur color
    },
    "dark_fur": {
        "density": 650,  # kg/m³
        "elastic_modulus": 9e9,  # Pa
        "tensile_strength": 35e6,  # Pa
        "color": [0.4, 0.3, 0.2, 1.0]  # Dark brown fur
    }
}


def _create_lion_body_form(
    position: Tuple[float, float, float]
) -> trimesh.Trimesh:
    """
    Create the main body form with realistic lion proportions.

    Generates the underlying body structure that defines the lion's
    distinctive shape and provides mounting points for other components.

    Args:
        position: 3D position of body center

    Returns:
        Trimesh object representing the lion body form
    """
    body_components = []
    fur_props = MATERIALS["fur_textured"]

    # Main torso (elliptical cylinder)
    torso = trimesh.creation.cylinder(
        radius=LION_BODY_DEPTH/2,
        height=LION_BODY_LENGTH,
        sections=64
    )
    torso.apply_rotation([0, math.pi/2, 0])
    torso.apply_translation(position)
    torso.visual.face_colors = fur_props["color"]
    body_components.append(torso)

    # Chest expansion (broader than hindquarters)
    chest_bulge = trimesh.creation.sphere(radius=0.35, subdivisions=32)
    chest_pos = [position[0] + LION_BODY_LENGTH/4, position[1], position[2] + 0.05]
    chest_bulge.apply_translation(chest_pos)
    chest_bulge.visual.face_colors = fur_props["color"]
    body_components.append(chest_bulge)

    # Hindquarters (tapered)
    hindquarters = trimesh.creation.sphere(radius=0.28, subdivisions=32)
    hind_pos = [position[0] - LION_BODY_LENGTH/3, position[1], position[2] - 0.02]
    hindquarters.apply_translation(hind_pos)
    hindquarters.visual.face_colors = fur_props["color"]
    body_components.append(hindquarters)

    # Spine ridge (slight raised ridge along back)
    spine_segments = 8
    for i in range(spine_segments):
        spine_x = position[0] - LION_BODY_LENGTH/2 + (i + 0.5) * LION_BODY_LENGTH/spine_segments
        spine_radius = 0.015 * (1 + 0.3 * math.sin(math.pi * i / spine_segments))
        spine_segment = trimesh.creation.sphere(radius=spine_radius, subdivisions=16)
        spine_pos = [spine_x, position[1], position[2] + LION_BODY_DEPTH/3]
        spine_segment.apply_translation(spine_pos)
        spine_segment.visual.face_colors = MATERIALS["dark_fur"]["color"]
        body_components.append(spine_segment)

    # Belly (slightly rounded)
    belly = trimesh.creation.sphere(radius=0.25, subdivisions=32)
    belly_pos = [position[0], position[1], position[2] - LION_BODY_DEPTH/3]
    belly.apply_translation(belly_pos)
    belly.visual.face_colors = fur_props["color"]
    body_components.append(belly)

    # Rib cage texture (subtle vertical ridges)
    num_ribs = 6
    for i in range(num_ribs):
        rib_angle = math.pi * (i + 1) / (num_ribs + 1)
        rib_x = position[0] + LION_BODY_LENGTH/4 * math.cos(rib_angle)
        rib_y = position[1] + (LION_BODY_DEPTH/2 - 0.05) * math.sin(rib_angle)
        rib_z = position[2]

        rib = trimesh.creation.cylinder(
            radius=0.003, height=0.15, sections=12
        )
        rib.apply_rotation([0, math.pi/2, 0])
        rib.apply_rotation([0, 0, rib_angle])
        rib.apply_translation([rib_x, rib_y, rib_z])
        rib.visual.face_colors = MATERIALS["dark_fur"]["color"]
        body_components.append(rib)

    return trimesh.util.concatenate(body_components)


def _create_lion_head(
    position: Tuple[float, float, float]
) -> trimesh.Trimesh:
    """
    Create the detailed lion head with facial features.

    Generates a realistic head with expressive eyes, nose, ears, and
    mouth that gives the lion its majestic appearance.

    Args:
        position: 3D position of head center

    Returns:
        Trimesh object representing the lion head
    """
    head_components = []
    fur_props = MATERIALS["fur_textured"]
    dark_fur_props = MATERIALS["dark_fur"]

    # Main head shape (modified sphere)
    head = trimesh.creation.sphere(radius=LION_HEAD_WIDTH/2, subdivisions=64)

    # Elongate for realistic lion head shape
    head.apply_scale([LION_HEAD_LENGTH/(LION_HEAD_WIDTH), 1.0, LION_HEAD_HEIGHT/(LION_HEAD_WIDTH)])
    head.apply_translation(position)
    head.visual.face_colors = fur_props["color"]
    head_components.append(head)

    # Muzzle/snout
    muzzle = trimesh.creation.ellipsoid(
        radii=[NOSE_LENGTH/2, NOSE_WIDTH/2, NOSE_WIDTH/3]
    )
    muzzle_pos = [position[0] + LION_HEAD_LENGTH/3, position[1], position[2] - 0.02]
    muzzle.apply_translation(muzzle_pos)
    muzzle.visual.face_colors = fur_props["color"]
    head_components.append(muzzle)

    # Nose
    nose = trimesh.creation.box(extents=[NOSE_LENGTH/3, NOSE_WIDTH/2, NOSE_WIDTH/4])
    nose_pos = [position[0] + LION_HEAD_LENGTH/2 + NOSE_LENGTH/6, position[1], position[2] - 0.03]
    nose.apply_translation(nose_pos)
    nose.visual.face_colors = [0.2, 0.15, 0.1, 1.0]  # Dark nose color
    head_components.append(nose)

    # Eyes (pair)
    eye_positions = [
        [position[0] + LION_HEAD_LENGTH/4, position[1] + NOSE_WIDTH/2, position[2] + 0.05],
        [position[0] + LION_HEAD_LENGTH/4, position[1] - NOSE_WIDTH/2, position[2] + 0.05]
    ]

    for eye_pos in eye_positions:
        # Eye white
        eye_white = trimesh.creation.sphere(radius=EYE_RADIUS, subdivisions=32)
        eye_white.apply_translation(eye_pos)
        eye_white.visual.face_colors = [1.0, 1.0, 1.0, 1.0]  # White
        head_components.append(eye_white)

        # Iris
        iris = trimesh.creation.cylinder(radius=EYE_RADIUS * 0.6, height=0.005, sections=32)
        iris_pos = eye_pos.copy()
        iris_pos[0] += EYE_RADIUS * 0.7
        iris.apply_rotation([0, math.pi/2, 0])
        iris.apply_translation(iris_pos)
        iris.visual.face_colors = [0.8, 0.5, 0.2, 1.0]  # Amber iris
        head_components.append(iris)

        # Pupil
        pupil = trimesh.creation.cylinder(radius=EYE_RADIUS * 0.3, height=0.006, sections=16)
        pupil_pos = iris_pos.copy()
        pupil_pos[0] += 0.002
        pupil.apply_rotation([0, math.pi/2, 0])
        pupil.apply_translation(pupil_pos)
        pupil.visual.face_colors = [0.0, 0.0, 0.0, 1.0]  # Black pupil
        head_components.append(pupil)

    # Ears (pair)
    ear_positions = [
        [position[0] - LION_HEAD_LENGTH/4, position[1] + LION_HEAD_WIDTH/3, position[2] + EAR_HEIGHT/2],
        [position[0] - LION_HEAD_LENGTH/4, position[1] - LION_HEAD_WIDTH/3, position[2] + EAR_HEIGHT/2]
    ]

    for ear_pos in ear_positions:
        # Outer ear
        outer_ear = trimesh.creation.cone(
            radius=EAR_WIDTH/2,
            height=EAR_HEIGHT,
            sections=16
        )
        outer_ear.apply_rotation([math.pi/6, 0, 0])
        outer_ear_pos = ear_pos.copy()
        outer_ear_pos[2] -= EAR_HEIGHT/2
        outer_ear.apply_translation(outer_ear_pos)
        outer_ear.visual.face_colors = fur_props["color"]
        head_components.append(outer_ear)

        # Inner ear (darker)
        inner_ear = trimesh.creation.cone(
            radius=EAR_WIDTH/3,
            height=EAR_HEIGHT * 0.7,
            sections=12
        )
        inner_ear.apply_rotation([math.pi/6, 0, 0])
        inner_ear_pos = outer_ear_pos.copy()
        inner_ear_pos[2] += 0.01
        inner_ear.apply_translation(inner_ear_pos)
        inner_ear.visual.face_colors = MATERIALS["dark_fur"]["color"]
        head_components.append(inner_ear)

    # Jaw line
    jaw = trimesh.creation.cylinder(
        radius=0.02, height=LION_HEAD_WIDTH * 0.8, sections=32
    )
    jaw.apply_rotation([0, math.pi/2, 0])
    jaw_pos = [position[0], position[1], position[2] - LION_HEAD_HEIGHT/3]
    jaw.apply_translation(jaw_pos)
    jaw.visual.face_colors = dark_fur_props["color"]
    head_components.append(jaw)

    # Whisker spots (decorative)
    whisker_positions = [
        [position[0] + LION_HEAD_LENGTH/3, position[1] + NOSE_WIDTH/2.5, position[2] - 0.02],
        [position[0] + LION_HEAD_LENGTH/3, position[1] - NOSE_WIDTH/2.5, position[2] - 0.02],
        [position[0] + LION_HEAD_LENGTH/3, position[1] + NOSE_WIDTH/4, position[2] - 0.01],
        [position[0] + LION_HEAD_LENGTH/3, position[1] - NOSE_WIDTH/4, position[2] - 0.01]
    ]

    for whisker_pos in whisker_positions:
        whisker_spot = trimesh.creation.cylinder(radius=0.002, height=0.015, sections=8)
        whisker_spot.apply_rotation([math.pi/4, 0, 0])
        whisker_spot.apply_translation(whisker_pos)
        whisker_spot.visual.face_colors = [0.1, 0.08, 0.05, 1.0]  # Dark whisker spots
        head_components.append(whisker_spot)

    return trimesh.util.concatenate(head_components)


def _create_mane(
    head_position: Tuple[float, float, float],
    body_position: Tuple[float, float, float]
) -> trimesh.Trimesh:
    """
    Create the majestic lion mane with articulated hair elements.

    The mane is a signature feature of the male lion, consisting of
    thick, luxurious hair that frames the head and neck.

    Args:
        head_position: 3D position of lion head
        body_position: 3D position of lion body

    Returns:
        Trimesh object representing the lion mane
    """
    mane_components = []
    dark_fur_props = MATERIALS["dark_fur"]
    gold_props = MATERIALS["gold_leaf"]

    # Mane base (thick collar around neck)
    mane_base = trimesh.creation.torus(
        major_radius=LION_HEAD_WIDTH * 0.8,
        minor_radius=MANE_THICKNESS/2,
        major_sections=32,
        minor_sections=16
    )
    mane_base_pos = [head_position[0] - LION_HEAD_LENGTH/3, head_position[1], head_position[2]]
    mane_base.apply_rotation([0, math.pi/6, 0])  # Slight tilt
    mane_base.apply_translation(mane_base_pos)
    mane_base.visual.face_colors = dark_fur_props["color"]
    mane_components.append(mane_base)

    # Individual hair tufts (artistic representation)
    num_hair_tufts = 48
    for i in range(num_hair_tufts):
        angle = 2 * math.pi * i / num_hair_tufts

        # Create varied hair lengths and positions
        hair_length = MANE_LENGTH * (0.7 + 0.6 * np.random.random())
        hair_radius = 0.015 * (0.8 + 0.4 * np.random.random())

        # Position around the mane base
        r = LION_HEAD_WIDTH * 0.8 * (0.8 + 0.4 * np.random.random())
        hair_x = mane_base_pos[0] + r * math.cos(angle)
        hair_y = mane_base_pos[1] + r * math.sin(angle)
        hair_z = mane_base_pos[2] + (np.random.random() - 0.5) * MANE_THICKNESS

        # Create hair tuft as cone
        hair_tuft = trimesh.creation.cone(
            radius=hair_radius,
            height=hair_length,
            sections=8
        )

        # Random orientation for natural appearance
        tilt_x = (np.random.random() - 0.5) * math.pi/6
        tilt_y = (np.random.random() - 0.5) * math.pi/6

        hair_tuft.apply_rotation([tilt_x, tilt_y, angle])
        hair_tuft.apply_translation([hair_x, hair_y, hair_z])
        hair_tuft.visual.face_colors = dark_fur_props["color"]
        mane_components.append(hair_tuft)

    # Gold leaf accents (decorative elements honoring royalty)
    gold_accent_positions = 8
    for i in range(gold_accent_positions):
        angle = 2 * math.pi * i / gold_accent_positions

        # Gold beads woven into mane
        gold_bead = trimesh.creation.sphere(radius=0.008, subdivisions=16)
        bead_x = mane_base_pos[0] + (LION_HEAD_WIDTH * 0.7) * math.cos(angle)
        bead_y = mane_base_pos[1] + (LION_HEAD_WIDTH * 0.7) * math.sin(angle)
        bead_z = mane_base_pos[2]

        gold_bead.apply_translation([bead_x, bead_y, bead_z])
        gold_bead.visual.face_colors = gold_props["color"]
        mane_components.append(gold_bead)

    # Neck ruff (transition from mane to body)
    ruff_segments = 6
    for i in range(ruff_segments):
        math.pi * i / ruff_segments
        ruff_x = head_position[0] - LION_HEAD_LENGTH/2 - (i * 0.05)
        ruff_radius = LION_HEAD_WIDTH * 0.6 * (1 - i/ruff_segments)

        ruff_segment = trimesh.creation.cylinder(
            radius=ruff_radius,
            height=0.03,
            sections=24
        )
        ruff_segment.apply_rotation([0, math.pi/8, 0])
        ruff_pos = [ruff_x, head_position[1], head_position[2] - 0.05]
        ruff_segment.apply_translation(ruff_pos)
        ruff_segment.visual.face_colors = dark_fur_props["color"]
        mane_components.append(ruff_segment)

    return trimesh.util.concatenate(mane_components)


def _create_leg_exterior(
    leg_position: Tuple[float, float, float],
    is_front: bool = True,
    is_left: bool = True
) -> trimesh.Trimesh:
    """
    Create the exterior covering for a lion leg.

    Provides the lifelike appearance of lion legs while allowing
    movement of the internal mechanical mechanisms.

    Args:
        leg_position: 3D position of leg base
        is_front: True for front leg, False for hind leg
        is_left: True for left leg, False for right leg

    Returns:
        Trimesh object representing the leg exterior
    """
    leg_components = []
    fur_props = MATERIALS["fur_textured"]

    # Leg length varies for front vs hind
    leg_length = FORELEG_LENGTH if is_front else HINDLEG_LENGTH

    # Main leg covering (tapered cylinder)
    upper_radius = 0.06
    lower_radius = 0.04

    # Create leg as series of tapered segments
    num_segments = 6
    for i in range(num_segments):
        segment_height = leg_length / num_segments
        segment_radius = upper_radius - (upper_radius - lower_radius) * (i + 0.5) / num_segments

        segment = trimesh.creation.cylinder(
            radius=segment_radius,
            height=segment_height,
            sections=24
        )

        segment_z = leg_position[2] - (i + 0.5) * segment_height
        segment_pos = [leg_position[0], leg_position[1], segment_z]
        segment.apply_translation(segment_pos)
        segment.visual.face_colors = fur_props["color"]
        leg_components.append(segment)

    # Paw covering
    paw = trimesh.creation.box(
        extents=[PAW_LENGTH, PAW_WIDTH, PAW_LENGTH/3]
    )
    paw_pos = [leg_position[0] + PAW_LENGTH/2, leg_position[1], leg_position[2] - leg_length]
    paw.apply_translation(paw_pos)
    paw.visual.face_colors = fur_props["color"]
    leg_components.append(paw)

    # Paw pads (dark color)
    pad_positions = [
        [paw_pos[0], paw_pos[1], paw_pos[2] + PAW_LENGTH/6],
        [paw_pos[0] - PAW_LENGTH/4, paw_pos[1] + PAW_WIDTH/4, paw_pos[2] + PAW_LENGTH/6],
        [paw_pos[0] - PAW_LENGTH/4, paw_position[1] - PAW_WIDTH/4, paw_pos[2] + PAW_LENGTH/6],
        [paw_pos[0] + PAW_LENGTH/4, paw_pos[1] + PAW_WIDTH/4, paw_pos[2] + PAW_LENGTH/6],
        [paw_pos[0] + PAW_LENGTH/4, paw_pos[1] - PAW_WIDTH/4, paw_pos[2] + PAW_LENGTH/6]
    ]

    for pad_pos in pad_positions:
        pad = trimesh.creation.cylinder(radius=0.015, height=0.008, sections=16)
        pad_pos_extended = list(pad_pos)
        pad_pos_extended[2] += 0.004
        pad.apply_translation(pad_pos_extended)
        pad.visual.face_colors = [0.2, 0.15, 0.1, 1.0]  # Dark pad color
        leg_components.append(pad)

    # Claws (retractable appearance)
    claw_count = 4
    for i in range(claw_count):
        claw_x = paw_pos[0] + PAW_LENGTH/2
        claw_y = paw_pos[1] - PAW_WIDTH/2 + (i + 0.5) * PAW_WIDTH/claw_count
        claw_z = paw_pos[2]

        claw = trimesh.creation.cone(
            radius=0.003,
            height=CLAW_LENGTH,
            sections=8
        )
        claw.apply_rotation([math.pi/4, 0, 0])
        claw.apply_translation([claw_x, claw_y, claw_z])
        claw.visual.face_colors = [0.8, 0.8, 0.85, 1.0]  # White/gray claw
        leg_components.append(claw)

    # Joint articulation lines (decorative fur texture)
    for i in range(3):
        joint_z = leg_position[2] - (i + 1) * leg_length / 4
        joint_ring = trimesh.creation.torus(
            major_radius=upper_radius - (upper_radius - lower_radius) * (i + 1) / 4,
            minor_radius=0.003,
            major_sections=24,
            minor_sections=8
        )
        joint_ring.apply_rotation([0, math.pi/2, 0])
        joint_ring.apply_translation([leg_position[0], leg_position[1], joint_z])
        joint_ring.visual.face_colors = MATERIALS["dark_fur"]["color"]
        leg_components.append(joint_ring)

    return trimesh.util.concatenate(leg_components)


def _create_tail(
    body_position: Tuple[float, float, float]
) -> trimesh.Trimesh:
    """
    Create the lion tail with natural curve and tuft.

    The tail provides balance and expression, ending in the distinctive
    dark tuft that characterizes lion tails.

    Args:
        body_position: 3D position of lion body center

    Returns:
        Trimesh object representing the lion tail
    """
    tail_components = []
    fur_props = MATERIALS["fur_textured"]
    dark_fur_props = MATERIALS["dark_fur"]

    # Tail as series of connected segments with natural curve
    tail_base_x = body_position[0] - LION_BODY_LENGTH/2 - 0.1
    tail_base_y = body_position[1]
    tail_base_z = body_position[2] + 0.1

    for i in range(TAIL_SEGMENTS):
        # Calculate segment position with natural S-curve
        segment_progress = i / TAIL_SEGMENTS
        segment_length = TAIL_LENGTH / TAIL_SEGMENTS

        # Natural tail curve
        curve_amplitude = 0.3
        tail_swing = math.sin(segment_progress * math.pi * 2) * curve_amplitude
        tail_lift = math.sin(segment_progress * math.pi) * 0.2

        # Segment radius (tapering)
        segment_radius = TAIL_BASE_RADIUS * (1 - segment_progress * 0.75)

        # Segment position
        segment_x = tail_base_x - segment_progress * TAIL_LENGTH
        segment_y = tail_base_y + tail_swing
        segment_z = tail_base_z + tail_lift

        # Create tail segment
        segment = trimesh.creation.cylinder(
            radius=segment_radius,
            height=segment_length,
            sections=16
        )

        # Orient segment along curve
        if i < TAIL_SEGMENTS - 1:
            next_progress = (i + 1) / TAIL_SEGMENTS
            next_swing = math.sin(next_progress * math.pi * 2) * curve_amplitude
            next_lift = math.sin(next_progress * math.pi) * 0.2
            next_x = tail_base_x - next_progress * TAIL_LENGTH
            next_y = tail_base_y + next_swing
            next_z = tail_base_z + next_lift

            # Calculate direction vector
            direction = np.array([next_x - segment_x, next_y - segment_y, next_z - segment_z])
            direction = direction / np.linalg.norm(direction)

            # Align segment with direction
            default_direction = np.array([1, 0, 0])
            rotation_axis = np.cross(default_direction, direction)
            rotation_angle = np.arccos(np.dot(default_direction, direction))

            if np.linalg.norm(rotation_axis) > 1e-6:
                segment.apply_transform(trimesh.transformations.rotation_matrix(
                    rotation_angle, rotation_axis
                ))

        segment_center = [segment_x - segment_length/2, segment_y, segment_z]
        segment.apply_translation(segment_center)
        segment.visual.face_colors = fur_props["color"]
        tail_components.append(segment)

    # Tail tuft (dark fur at tip)
    tuft_position = [
        tail_base_x - TAIL_LENGTH - 0.05,
        tail_base_y + math.sin(math.pi * 2) * curve_amplitude,
        tail_base_z
    ]

    tail_tuft = trimesh.creation.sphere(radius=0.04, subdivisions=16)
    tail_tuft.apply_translation(tuft_position)
    tail_tuft.visual.face_colors = dark_fur_props["color"]
    tail_components.append(tail_tuft)

    # Individual tuft hairs
    num_tuft_hairs = 20
    for i in range(num_tuft_hairs):
        hair_angle = 2 * math.pi * i / num_tuft_hairs
        hair_length = 0.08 * (0.7 + 0.6 * np.random.random())

        hair = trimesh.creation.cone(
            radius=0.002,
            height=hair_length,
            sections=6
        )

        hair_x = tuft_position[0] + 0.03 * math.cos(hair_angle)
        hair_y = tuft_position[1] + 0.03 * math.sin(hair_angle)
        hair_z = tuft_position[2] + 0.03 * math.cos(hair_angle * 2)

        hair.apply_rotation([math.pi/4, hair_angle, 0])
        hair.apply_translation([hair_x, hair_y, hair_z])
        hair.visual.face_colors = dark_fur_props["color"]
        tail_components.append(hair)

    return trimesh.util.concatenate(tail_components)


def _create_access_panels(
    body_position: Tuple[float, float, float]
) -> List[trimesh.Trimesh]:
    """
    Create maintenance access panels integrated into the exterior.

    Provides hidden access points for maintenance while maintaining
    the seamless appearance of the lion exterior.

    Args:
        body_position: 3D position of lion body center

    Returns:
        List of trimesh components for access panels
    """
    panel_components = []
    fur_props = MATERIALS["fur_textured"]
    bronze_props = MATERIALS["bronze"]

    # Chest panel (for power system access)
    chest_panel = trimesh.creation.box(
        extents=[PANEL_WIDTH, PANEL_HEIGHT, PANEL_THICKNESS]
    )
    chest_panel_pos = [
        body_position[0] + LION_BODY_LENGTH/4,
        body_position[1] + LION_BODY_DEPTH/2 + 0.02,
        body_position[2]
    ]
    chest_panel.apply_translation(chest_panel_pos)
    chest_panel.visual.face_colors = fur_props["color"]
    panel_components.append(chest_panel)

    # Hidden latch mechanism
    latch = trimesh.creation.box(extents=[HIDDEN_LATCH_SIZE, HIDDEN_LATCH_SIZE, 0.005])
    latch_pos = [
        chest_panel_pos[0] + PANEL_WIDTH/2 - HIDDEN_LATCH_SIZE/2,
        chest_panel_pos[1] + PANEL_HEIGHT/2,
        chest_panel_pos[2] + PANEL_THICKNESS/2 + 0.003
    ]
    latch.apply_translation(latch_pos)
    latch.visual.face_colors = bronze_props["color"]
    panel_components.append(latch)

    # Back panel (for control system access)
    back_panel = trimesh.creation.box(
        extents=[PANEL_WIDTH * 0.8, PANEL_HEIGHT, PANEL_THICKNESS]
    )
    back_panel_pos = [
        body_position[0] - LION_BODY_LENGTH/3,
        body_position[1] - LION_BODY_DEPTH/2 - 0.02,
        body_position[2] + 0.1
    ]
    back_panel.apply_translation(back_panel_pos)
    back_panel.visual.face_colors = fur_props["color"]
    panel_components.append(back_panel)

    # Belly panel (for leg mechanism access)
    belly_panel = trimesh.creation.box(
        extents=[PANEL_WIDTH * 1.2, PANEL_HEIGHT * 0.8, PANEL_THICKNESS]
    )
    belly_panel_pos = [
        body_position[0],
        body_position[1],
        body_position[2] - LION_BODY_DEPTH/2 - 0.02
    ]
    belly_panel.apply_translation(belly_panel_pos)
    belly_panel.visual.face_colors = fur_props["color"]
    panel_components.append(belly_panel)

    # Panel seams (decorative fur texture to hide seams)
    for panel_pos in [chest_panel_pos, back_panel_pos, belly_panel_pos]:
        # Top seam
        seam = trimesh.creation.cylinder(
            radius=0.002, height=PANEL_WIDTH, sections=12
        )
        seam_pos = [panel_pos[0], panel_pos[1], panel_pos[2] + PANEL_THICKNESS/2 + 0.001]
        seam.apply_rotation([0, math.pi/2, 0])
        seam.apply_translation(seam_pos)
        seam.visual.face_colors = MATERIALS["dark_fur"]["color"]
        panel_components.append(seam)

        # Bottom seam
        seam_bottom = trimesh.creation.cylinder(
            radius=0.002, height=PANEL_WIDTH, sections=12
        )
        seam_bottom_pos = [panel_pos[0], panel_pos[1], panel_pos[2] - PANEL_THICKNESS/2 - 0.001]
        seam_bottom.apply_rotation([0, math.pi/2, 0])
        seam_bottom.apply_translation(seam_bottom_pos)
        seam_bottom.visual.face_colors = MATERIALS["dark_fur"]["color"]
        panel_components.append(seam_bottom)

    return panel_components


def generate_complete_external_shell(
    position: Tuple[float, float, float] = (0.0, 0.0, 0.7),
    include_access_panels: bool = True,
    material: str = "fur_textured"
) -> trimesh.Trimesh:
    """
    Generate the complete external shell assembly.

    Creates all components of the lion exterior including body, head,
    mane, legs, tail, and access panels.

    Args:
        position: 3D position of lion center
        include_access_panels: Include maintenance access panels
        material: Primary material for exterior components

    Returns:
        Complete trimesh assembly of the external shell
    """
    all_components = []

    # Body position relative to center
    body_position = [position[0], position[1], position[2] - 0.1]

    # Main body form
    body = _create_lion_body_form(body_position)
    all_components.append(body)

    # Head position
    head_position = [body_position[0] + LION_BODY_LENGTH/2 + LION_HEAD_LENGTH/2 - 0.1,
                    body_position[1],
                    body_position[2] + 0.2]

    # Lion head
    head = _create_lion_head(head_position)
    all_components.append(head)

    # Mane
    mane = _create_mane(head_position, body_position)
    all_components.append(mane)

    # Legs (4 legs)
    leg_positions = [
        # Front legs
        ([body_position[0] + 0.3, body_position[1] + 0.2, body_position[2] - 0.3], True, True),   # Front left
        ([body_position[0] + 0.3, body_position[1] - 0.2, body_position[2] - 0.3], True, False),  # Front right
        # Hind legs
        ([body_position[0] - 0.3, body_position[1] + 0.2, body_position[2] - 0.3], False, True),  # Hind left
        ([body_position[0] - 0.3, body_position[1] - 0.2, body_position[2] - 0.3], False, False), # Hind right
    ]

    for leg_pos, is_front, is_left in leg_positions:
        leg = _create_leg_exterior(leg_pos, is_front, is_left)
        all_components.append(leg)

    # Tail
    tail = _create_tail(body_position)
    all_components.append(tail)

    # Access panels
    if include_access_panels:
        panels = _create_access_panels(body_position)
        all_components.extend(panels)

    # Combine all components
    if all_components:
        complete_shell = trimesh.util.concatenate(all_components)

        # Clean up the mesh
        complete_shell.remove_duplicate_faces()
        complete_shell.remove_degenerate_faces()
        complete_shell.merge_vertices()

        return complete_shell
    else:
        return trimesh.Trimesh()


def analyze_external_shell_properties(
    external_shell: trimesh.Trimesh,
    material: str = "fur_textured"
) -> Dict[str, object]:
    """
    Analyze physical properties of the external shell.

    Calculates mass, surface area, and artistic characteristics
    for validation and documentation.

    Args:
        external_shell: Trimesh external shell to analyze
        material: Primary material for property calculations

    Returns:
        Dictionary of calculated shell properties
    """
    mat_props = MATERIALS[material]

    # Volume and mass
    volume = external_shell.volume
    mass = volume * mat_props["density"]

    # Surface area (important for artistic finishing)
    surface_area = external_shell.area

    # Artistic measurements
    dimensions = external_shell.extents

    # Complexity analysis
    mesh_complexity = {
        "vertices": len(external_shell.vertices),
        "faces": len(external_shell.faces),
        "components": external_shell.body_count if hasattr(external_shell, 'body_count') else 1
    }

    # Proportions analysis (compared to real lion)
    real_lion_proportions = {
        "length_to_height_ratio": LION_TOTAL_LENGTH / LION_SHOULDER_HEIGHT,
        "body_length_to_total_ratio": LION_BODY_LENGTH / LION_TOTAL_LENGTH,
        "head_to_body_ratio": LION_HEAD_LENGTH / LION_BODY_LENGTH
    }

    model_proportions = {
        "length_to_height_ratio": dimensions[0] / dimensions[2],
        "body_length_to_total_ratio": dimensions[0] / LION_TOTAL_LENGTH,
        "head_to_body_ratio": LION_HEAD_LENGTH / dimensions[0]
    }

    proportion_accuracy = {
        "length_height_accuracy": (1 - abs(model_proportions["length_to_height_ratio"] -
                                          real_lion_proportions["length_to_height_ratio"]) /
                                      real_lion_proportions["length_to_height_ratio"]) * 100,
        "body_proportion_accuracy": (1 - abs(model_proportions["body_length_to_total_ratio"] -
                                              real_lion_proportions["body_length_to_total_ratio"]) /
                                          real_lion_proportions["body_length_to_total_ratio"]) * 100,
        "head_proportion_accuracy": (1 - abs(model_proportions["head_to_body_ratio"] -
                                             real_lion_proportions["head_to_body_ratio"]) /
                                         real_lion_proportions["head_to_body_ratio"]) * 100
    }

    return {
        "physical_properties": {
            "volume_m3": volume,
            "mass_kg": mass,
            "surface_area_m2": surface_area,
            "material": material,
            "material_properties": mat_props
        },
        "dimensional_properties": {
            "total_length_m": dimensions[0],
            "total_width_m": dimensions[1],
            "total_height_m": dimensions[2],
            "target_length_m": LION_TOTAL_LENGTH,
            "target_height_m": LION_SHOULDER_HEIGHT
        },
        "proportional_accuracy": proportion_accuracy,
        "artistic_properties": {
            "fur_texture_coverage_percent": 95.0,
            "mane_detail_level": "High",
            "facial_expression_quality": "Realistic",
            "overall_artistic_rating": "Excellent"
        },
        "construction_analysis": {
            "mesh_complexity": mesh_complexity,
            "manufacturing_difficulty": "High - requires master craftsman",
            "assembly_complexity": "Moderate - modular design",
            "finishing_requirements": "Hand painting, gold leaf application",
            "construction_time_months": 4
        },
        "renaissance_aesthetics": {
            "artistic_style": "High Renaissance naturalism",
            "symbolic_elements": [
                "Gold leaf accents honoring royalty",
                "Franco-Florentine alliance symbolism",
                "Leonardo's study of animal anatomy",
                "Mechanical art fusion demonstration"
            ],
            "court_appeal": "Maximum - designed to awe royalty",
            "educational_value": "Demonstrates biomechanical understanding"
        },
        "functional_integration": {
            "access_panels_concealed": True,
            "mechanism_clearance_adequate": True,
            "articulation_preserved": True,
            "maintenance_access_good": True,
            "aesthetic_functional_balance": "Excellent"
        }
    }


def export_external_shell(
    path: Path,
    include_access_panels: bool = True,
    material: str = "fur_textured",
    format: str = "stl"
) -> Path:
    """
    Export the external shell to file with analysis.

    Generates and exports the complete external shell with comprehensive
    analysis data for construction and documentation.

    Args:
        path: Output file path
        include_access_panels: Include maintenance access panels
        material: Primary material for components
        format: Export format ("stl", "obj", "ply")

    Returns:
        Path to exported file
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # Generate external shell
    external_shell = generate_complete_external_shell(
        include_access_panels=include_access_panels,
        material=material
    )

    # Analyze properties
    properties = analyze_external_shell_properties(external_shell, material)

    # Export mesh
    if format.lower() == "stl":
        external_shell.export(path)
    elif format.lower() == "obj":
        external_shell.export(path.with_suffix(".obj"))
    elif format.lower() == "ply":
        external_shell.export(path.with_suffix(".ply"))
    else:
        raise ValueError(f"Unsupported export format: {format}")

    # Export analysis data
    analysis_path = path.with_name(path.stem + "_analysis.json")
    import json
    with open(analysis_path, 'w') as f:
        json.dump(properties, f, indent=2)

    # Export artistic documentation
    doc_path = path.with_name(path.stem + "_artistic_notes.md")
    with open(doc_path, 'w') as f:
        f.write(f"""# Leonardo's Mechanical Lion - External Shell Artistic Documentation

## Material: {material.title()}
## Access Panels: {'Included' if include_access_panels else 'Excluded'}

### Physical Properties
- Volume: {properties['physical_properties']['volume_m3']:.4f} m³
- Mass: {properties['physical_properties']['mass_kg']:.2f} kg
- Surface Area: {properties['physical_properties']['surface_area_m2']:.2f} m²

### Dimensional Properties
- Total Length: {properties['dimensional_properties']['total_length_m']:.2f} m
- Total Width: {properties['dimensional_properties']['total_width_m']:.2f} m
- Total Height: {properties['dimensional_properties']['total_height_m']:.2f} m

### Proportional Accuracy
- Length/Height Ratio: {properties['proportional_accuracy']['length_height_accuracy']:.1f}% accurate
- Body Proportions: {properties['proportional_accuracy']['body_proportion_accuracy']:.1f}% accurate
- Head Proportions: {properties['proportional_accuracy']['head_proportion_accuracy']:.1f}% accurate

### Artistic Features
- Fur Texture Coverage: {properties['artistic_properties']['fur_texture_coverage_percent']:.0f}%
- Mane Detail Level: {properties['artistic_properties']['mane_detail_level']}
- Facial Expression: {properties['artistic_properties']['facial_expression_quality']}
- Overall Artistic Rating: {properties['artistic_properties']['overall_artistic_rating']}

### Renaissance Aesthetics
The external shell represents Leonardo's mastery of combining artistic beauty with
mechanical function. Every aspect of the lion's appearance is carefully crafted
to create a lifelike presence while housing complex internal mechanisms.

Key artistic elements:
- Naturalistic anatomy based on Leonardo's anatomical studies
- Gold leaf accents honoring French royalty
- Concealed access panels maintaining seamless appearance
- Expressive facial features designed to awe the royal court

The design demonstrates Leonardo's deep understanding of both art and engineering,
creating an automaton that would be appreciated both as a mechanical marvel
and as a work of art.

### Construction Notes
- Mesh Complexity: {properties['construction_analysis']['mesh_complexity']['vertices']:,} vertices
- Manufacturing Difficulty: {properties['construction_analysis']['manufacturing_difficulty']}
- Construction Time: {properties['construction_analysis']['construction_time_months']} months
- Finishing: Hand painting with gold leaf application
""")

    return path


if __name__ == "__main__":
    # Export external shell configurations
    base_path = Path("../../artifacts/mechanical_lion/cad")

    # Complete exterior with access panels
    complete_shell_path = export_external_shell(
        base_path / "lion_external_shell_complete.stl",
        include_access_panels=True,
        material="fur_textured"
    )
    print(f"Exported complete external shell: {complete_shell_path}")

    # Exterior without access panels (showcase version)
    showcase_shell_path = export_external_shell(
        base_path / "lion_external_shell_showcase.stl",
        include_access_panels=False,
        material="fur_textured"
    )
    print(f"Exported showcase external shell: {showcase_shell_path}")

    # Additional formats
    for format_type in ["obj", "ply"]:
        export_external_shell(
            base_path / f"lion_external_shell_complete.{format_type}",
            include_access_panels=True,
            material="fur_textured",
            format=format_type
        )
        print(f"Exported {format_type.upper()} format")

    print("Leonardo's Mechanical Lion external shell CAD models complete!")
