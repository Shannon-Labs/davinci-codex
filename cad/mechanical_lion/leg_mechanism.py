"""
Leonardo's Mechanical Lion - Leg Mechanism Assemblies

This module generates detailed parametric CAD models for the individual leg mechanisms
that drive Leonardo's Mechanical Lion. Each leg assembly includes:

- Hip joint with articulation range matching real lion biomechanics
- Four-bar linkage system converting cam rotation to natural leg motion
- Knee and ankle joints with proper articulation
- Paw design with ground contact and traction
- Bronze bearings and steel pivot points
- Adjustable linkage tuning for gait optimization

The leg mechanisms replicate the natural lateral sequence walking gait of lions,
providing stable, efficient locomotion through Leonardo's innovative cam-driven
four-bar linkage system.

CAD Features:
- Biomimetic joint ranges based on lion anatomy
- Four-bar linkage kinematics for natural motion
- Modular design for individual leg replacement
- Renaissance-appropriate materials and construction
- Adjustable linkages for gait tuning
- Bronze bushings for smooth articulation
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import trimesh

# Leg biomechanical parameters (based on Panthera leo)
LEG_LENGTH = 0.6  # meters (shoulder to paw)
UPPER_LEG_LENGTH = 0.3  # meters (femur/humerus)
LOWER_LEG_LENGTH = 0.25  # meters (tibia/radius)
PAW_LENGTH = 0.05  # meters

# Body positioning constants (meters)
FORELEG_TO_HINDLEG_DISTANCE = 0.8
LATERAL_LEG_SPACING = 0.4
BODY_HEIGHT = 0.6
WINDING_GEAR_RADIUS = 0.15

# Joint ranges (radians) - based on real lion anatomy
HIP_FLEXION_RANGE = (-math.pi/4, math.pi/3)  # -45° to +60°
HIP_ABDUCTION_RANGE = (-math.pi/6, math.pi/6)  # -30° to +30°
KNEE_FLEXION_RANGE = (0, math.pi*2/3)  # 0° to 120°
ANKLE_FLEXION_RANGE = (-math.pi/6, math.pi/6)  # -30° to +30°

# Four-bar linkage dimensions (Leonardo's design)
CRANK_RADIUS = 0.08  # meters (cam-driven crank)
COUPLER_LENGTH = 0.18  # meters (connecting rod)
ROCKER_LENGTH = 0.12  # meters (output lever)
GROUND_LINK_LENGTH = 0.25  # meters (fixed link)

# Component dimensions
HIP_JOINT_RADIUS = 0.025  # meters
KNEE_JOINT_RADIUS = 0.02  # meters
ANKLE_JOINT_RADIUS = 0.015  # meters
LINKAGE_WIDTH = 0.03  # meters
BEARING_THICKNESS = 0.01  # meters

# Paw design
PAW_WIDTH = 0.08  # meters
PAW_HEIGHT = 0.02  # meters
CLAW_LENGTH = 0.015  # meters
TOE_COUNT = 4

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
    "leather": {
        "density": 900,  # kg/m³
        "elastic_modulus": 0.1e9,  # Pa
        "tensile_strength": 20e6,  # Pa
        "color": [0.4, 0.3, 0.2, 1.0]  # Brown leather
    }
}


class LegKinematics:
    """
    Kinematic analysis and control for individual lion leg movement.

    Implements the four-bar linkage kinematics that Leonardo used to convert
    rotary cam motion into natural leg articulation patterns.
    """

    def __init__(self, is_front: bool, is_left: bool):
        self.is_front = is_front
        self.is_left = is_left

        # Four-bar linkage parameters
        self.crank_radius = CRANK_RADIUS
        self.coupler_length = COUPLER_LENGTH
        self.rocker_length = ROCKER_LENGTH
        self.ground_link_length = GROUND_LINK_LENGTH

        # Joint position tracking
        self.hip_angle = 0.0
        self.knee_angle = 0.0
        self.ankle_angle = 0.0

    def calculate_four_bar_position(self, crank_angle: float) -> Tuple[float, float]:
        """
        Calculate rocker and coupler angles from crank input.

        Uses the four-bar linkage equations to convert rotary motion to
        the coordinated hip and knee articulation patterns.

        Args:
            crank_angle: Input crank angle in radians

        Returns:
            Tuple of (rocker_angle, coupler_angle) in radians
        """
        # Four-bar linkage kinematics (complex loop equations)
        a = self.crank_radius
        b = self.coupler_length
        c = self.rocker_length
        d = self.ground_link_length
        theta2 = crank_angle

        # Calculate transmission angle using law of cosines
        cos_theta4 = (a**2 - b**2 + c**2 + d**2 - 2*a*d*math.cos(theta2)) / (2*c*d)
        cos_theta4 = max(-1, min(1, cos_theta4))  # Clamp to valid range
        theta4 = math.acos(cos_theta4)

        # Calculate coupler angle
        sin_theta3 = (a*math.sin(theta2)) / b
        sin_theta3 = max(-1, min(1, sin_theta3))  # Clamp to valid range
        theta3 = math.asin(sin_theta3)

        return theta4, theta3

    def calculate_joint_angles(self, crank_angle: float) -> Tuple[float, float, float]:
        """
        Convert four-bar linkage positions to biological joint angles.

        Maps the mechanical linkage positions to anatomically correct
        hip, knee, and ankle angles that mimic real lion movement.

        Args:
            crank_angle: Input crank angle in radians

        Returns:
            Tuple of (hip_angle, knee_angle, ankle_angle) in radians
        """
        rocker_angle, coupler_angle = self.calculate_four_bar_position(crank_angle)

        # Map mechanical angles to biological joint ranges
        hip_angle = HIP_FLEXION_RANGE[0] + (HIP_FLEXION_RANGE[1] - HIP_FLEXION_RANGE[0]) * \
                   ((rocker_angle + math.pi) / (2 * math.pi))

        # Knee motion coupled to hip through linkage geometry
        knee_ratio = 0.7  # Coupling ratio based on lion anatomy
        knee_angle = KNEE_FLEXION_RANGE[0] + (KNEE_FLEXION_RANGE[1] - KNEE_FLEXION_RANGE[0]) * \
                    knee_ratio * ((coupler_angle + math.pi) / (2 * math.pi))

        # Ankle motion for ground adaptation (simplified)
        ankle_angle = ANKLE_FLEXION_RANGE[0] + (ANKLE_FLEXION_RANGE[1] - ANKLE_FLEXION_RANGE[0]) * \
                     0.3 * math.sin(2 * crank_angle)

        # Store current angles
        self.hip_angle = hip_angle
        self.knee_angle = knee_angle
        self.ankle_angle = ankle_angle

        return hip_angle, knee_angle, ankle_angle


def _create_hip_joint(
    position: Tuple[float, float, float],
    is_left: bool = True
) -> List[trimesh.Trimesh]:
    """
    Create the hip joint assembly with bronze bushings and steel pivot.

    The hip joint provides primary articulation for leg movement with
    smooth rotation through bronze bearings.

    Args:
        position: 3D position of the hip joint center
        is_left: True for left leg, False for right leg

    Returns:
        List of trimesh components for the hip joint
    """
    components = []
    oak_props = MATERIALS["oak"]
    bronze_props = MATERIALS["bronze"]
    steel_props = MATERIALS["steel"]

    # Hip joint housing (oak)
    housing = trimesh.creation.cylinder(
        radius=HIP_JOINT_RADIUS + 0.01,
        height=0.08,
        sections=32
    )
    housing.apply_rotation([math.pi/2, 0, 0])
    housing.apply_translation(position)
    housing.visual.face_colors = oak_props["color"]
    components.append(housing)

    # Bronze bushing
    bushing = trimesh.creation.cylinder(
        radius=HIP_JOINT_RADIUS,
        height=0.06,
        sections=32
    )
    bushing.apply_rotation([math.pi/2, 0, 0])
    bushing.apply_translation(position)
    bushing.visual.face_colors = bronze_props["color"]
    components.append(bushing)

    # Steel pivot shaft
    pivot_shaft = trimesh.creation.cylinder(
        radius=0.01,
        height=0.12,
        sections=16
    )
    pivot_shaft.apply_rotation([math.pi/2, 0, 0])
    pivot_shaft.apply_translation(position)
    pivot_shaft.visual.face_colors = steel_props["color"]
    components.append(pivot_shaft)

    # Reinforcement rings
    for z_offset in [-0.03, 0.03]:
        ring = trimesh.creation.torus(
            major_radius=HIP_JOINT_RADIUS + 0.005,
            minor_radius=0.003,
            major_sections=32,
            minor_sections=16
        )
        ring.apply_rotation([0, math.pi/2, 0])
        ring_pos = list(position)
        ring_pos[2] += z_offset
        ring.apply_translation(ring_pos)
        ring.visual.face_colors = bronze_props["color"]
        components.append(ring)

    return components


def _create_upper_leg(
    hip_position: Tuple[float, float, float],
    hip_angle: float,
    is_left: bool = True
) -> List[trimesh.Trimesh]:
    """
    Create the upper leg (femur/humerus) with structural reinforcement.

    Provides the primary structural element of the leg with mounting points
    for the four-bar linkage system.

    Args:
        hip_position: 3D position of the hip joint
        hip_angle: Current hip joint angle in radians
        is_left: True for left leg, False for right leg

    Returns:
        List of trimesh components for the upper leg
    """
    components = []
    oak_props = MATERIALS["oak"]

    # Calculate knee position based on hip angle
    knee_x = hip_position[0] + UPPER_LEG_LENGTH * math.cos(hip_angle)
    knee_y = hip_position[1]
    knee_z = hip_position[2] - UPPER_LEG_LENGTH * math.sin(hip_angle)
    knee_position = (knee_x, knee_y, knee_z)

    # Main upper leg beam
    leg_vector = np.array(knee_position) - np.array(hip_position)
    leg_length = np.linalg.norm(leg_vector)
    leg_direction = leg_vector / leg_length

    upper_leg = trimesh.creation.cylinder(
        radius=0.02,
        height=leg_length,
        sections=32
    )

    # Align cylinder with leg direction
    default_direction = np.array([0, 0, 1])
    rotation_axis = np.cross(default_direction, leg_direction)
    rotation_angle = np.arccos(np.dot(default_direction, leg_direction))

    if np.linalg.norm(rotation_axis) > 1e-6:
        upper_leg.apply_transform(trimesh.transformations.rotation_matrix(
            rotation_angle, rotation_axis
        ))

    center_position = (np.array(hip_position) + np.array(knee_position)) / 2
    upper_leg.apply_translation(center_position)
    upper_leg.visual.face_colors = oak_props["color"]
    components.append(upper_leg)

    # Structural reinforcement ribs
    num_ribs = 3
    for i in range(num_ribs):
        rib_position = hip_position + (knee_position - hip_position) * (i + 1) / (num_ribs + 1)
        rib = trimesh.creation.box(extents=[0.04, 0.015, 0.015])
        rib.apply_translation(rib_position)
        rib.visual.face_colors = oak_props["color"]
        components.append(rib)

    # Four-bar linkage mounting points
    linkage_mount_1 = trimesh.creation.cylinder(
        radius=0.008, height=0.03, sections=16
    )
    mount_1_pos = hip_position + (knee_position - hip_position) * 0.3
    mount_1_pos = list(mount_1_pos)
    mount_1_pos[1] += 0.02 if is_left else -0.02
    linkage_mount_1.apply_translation(mount_1_pos)
    linkage_mount_1.visual.face_colors = MATERIALS["bronze"]["color"]
    components.append(linkage_mount_1)

    linkage_mount_2 = trimesh.creation.cylinder(
        radius=0.008, height=0.03, sections=16
    )
    mount_2_pos = hip_position + (knee_position - hip_position) * 0.7
    mount_2_pos = list(mount_2_pos)
    mount_2_pos[1] += 0.02 if is_left else -0.02
    linkage_mount_2.apply_translation(mount_2_pos)
    linkage_mount_2.visual.face_colors = MATERIALS["bronze"]["color"]
    components.append(linkage_mount_2)

    return components


def _create_knee_joint(
    knee_position: Tuple[float, float, float],
    knee_angle: float,
    is_left: bool = True
) -> List[trimesh.Trimesh]:
    """
    Create the knee joint with articulation and linkage attachment.

    The knee joint provides secondary articulation and serves as an attachment
    point for the four-bar linkage coupler.

    Args:
        knee_position: 3D position of the knee joint
        knee_angle: Current knee joint angle in radians
        is_left: True for left leg, False for right leg

    Returns:
        List of trimesh components for the knee joint
    """
    components = []
    oak_props = MATERIALS["oak"]
    bronze_props = MATERIALS["bronze"]

    # Knee joint housing
    housing = trimesh.creation.sphere(radius=KNEE_JOINT_RADIUS + 0.005, subdivisions=32)
    housing.apply_translation(knee_position)
    housing.visual.face_colors = oak_props["color"]
    components.append(housing)

    # Bronze pivot
    pivot = trimesh.creation.cylinder(
        radius=KNEE_JOINT_RADIUS,
        height=0.04,
        sections=32
    )
    pivot.apply_rotation([0, math.pi/2, 0])
    pivot.apply_translation(knee_position)
    pivot.visual.face_colors = bronze_props["color"]
    components.append(pivot)

    # Coupler attachment point
    coupler_mount = trimesh.creation.box(extents=[0.02, 0.02, 0.025])
    mount_pos = list(knee_position)
    mount_pos[1] += 0.03 if is_left else -0.03
    coupler_mount.apply_translation(mount_pos)
    coupler_mount.visual.face_colors = oak_props["color"]
    components.append(coupler_mount)

    # Reinforcement straps (leather appearance)
    for angle_offset in [0, math.pi/2, math.pi, 3*math.pi/2]:
        strap = trimesh.creation.box(extents=[0.001, 0.08, 0.001])
        strap_pos = list(knee_position)
        strap_pos[0] += (KNEE_JOINT_RADIUS + 0.002) * math.cos(angle_offset)
        strap_pos[1] += (KNEE_JOINT_RADIUS + 0.002) * math.sin(angle_offset)
        strap.apply_translation(strap_pos)
        strap.visual.face_colors = MATERIALS["leather"]["color"]
        components.append(strap)

    return components


def _create_lower_leg(
    knee_position: Tuple[float, float, float],
    knee_angle: float,
    ankle_angle: float,
    is_left: bool = True
) -> List[trimesh.Trimesh]:
    """
    Create the lower leg (tibia/radius) with ankle articulation.

    Provides the lower structural element connecting knee to paw with
    adjustable ankle for ground adaptation.

    Args:
        knee_position: 3D position of the knee joint
        knee_angle: Current knee joint angle in radians
        ankle_angle: Current ankle joint angle in radians
        is_left: True for left leg, False for right leg

    Returns:
        List of trimesh components for the lower leg
    """
    components = []
    oak_props = MATERIALS["oak"]

    # Calculate ankle position
    leg_extension_angle = knee_angle + ankle_angle
    ankle_x = knee_position[0] + LOWER_LEG_LENGTH * math.cos(leg_extension_angle)
    ankle_y = knee_position[1]
    ankle_z = knee_position[2] - LOWER_LEG_LENGTH * math.sin(leg_extension_angle)
    ankle_position = (ankle_x, ankle_y, ankle_z)

    # Main lower leg beam
    leg_vector = np.array(ankle_position) - np.array(knee_position)
    leg_length = np.linalg.norm(leg_vector)
    leg_direction = leg_vector / leg_length

    lower_leg = trimesh.creation.cylinder(
        radius=0.015,
        height=leg_length,
        sections=32
    )

    # Align cylinder with leg direction
    default_direction = np.array([0, 0, 1])
    rotation_axis = np.cross(default_direction, leg_direction)
    rotation_angle = np.arccos(np.dot(default_direction, leg_direction))

    if np.linalg.norm(rotation_axis) > 1e-6:
        lower_leg.apply_transform(trimesh.transformations.rotation_matrix(
            rotation_angle, rotation_axis
        ))

    center_position = (np.array(knee_position) + np.array(ankle_position)) / 2
    lower_leg.apply_translation(center_position)
    lower_leg.visual.face_colors = oak_props["color"]
    components.append(lower_leg)

    # Tendon simulation (decorative)
    tendon = trimesh.creation.cylinder(radius=0.002, height=leg_length, sections=8)
    tendon.apply_transform(trimesh.transformations.rotation_matrix(
        rotation_angle, rotation_axis
    ))
    tendon_pos = center_position.copy()
    tendon_pos[1] += 0.01 if is_left else -0.01
    tendon.apply_translation(tendon_pos)
    tendon.visual.face_colors = MATERIALS["leather"]["color"]
    components.append(tendon)

    # Ankle joint
    ankle_joint = trimesh.creation.sphere(radius=ANKLE_JOINT_RADIUS, subdivisions=16)
    ankle_joint.apply_translation(ankle_position)
    ankle_joint.visual.face_colors = MATERIALS["bronze"]["color"]
    components.append(ankle_joint)

    return components


def _create_paw(
    ankle_position: Tuple[float, float, float],
    is_left: bool = True
) -> List[trimesh.Trimesh]:
    """
    Create the paw with toes and claws for ground contact.

    Provides realistic paw design with traction surfaces and decorative
    claws that enhance the lifelike appearance.

    Args:
        ankle_position: 3D position of the ankle joint
        is_left: True for left leg, False for right leg

    Returns:
        List of trimesh components for the paw
    """
    components = []
    MATERIALS["oak"]
    steel_props = MATERIALS["steel"]

    # Paw pad
    paw_pad = trimesh.creation.box(extents=[PAW_LENGTH, PAW_WIDTH, PAW_HEIGHT])
    paw_pos = list(ankle_position)
    paw_pos[2] -= PAW_LENGTH
    paw_pad.apply_translation(paw_pos)
    paw_pad.visual.face_colors = MATERIALS["leather"]["color"]
    components.append(paw_pad)

    # Toe pads
    toe_radius = 0.015
    toe_spacing = PAW_WIDTH / (TOE_COUNT + 1)

    for i in range(TOE_COUNT):
        toe_x = paw_pos[0] + PAW_LENGTH/2
        toe_y = paw_pos[1] - PAW_WIDTH/2 + toe_spacing * (i + 1)
        toe_z = paw_pos[2] + PAW_HEIGHT/2

        toe_pad = trimesh.creation.cylinder(
            radius=toe_radius, height=0.01, sections=16
        )
        toe_pad.apply_translation([toe_x, toe_y, toe_z])
        toe_pad.visual.face_colors = MATERIALS["leather"]["color"]
        components.append(toe_pad)

        # Claw
        claw = trimesh.creation.cone(
            radius=0.003, height=CLAW_LENGTH, sections=8
        )
        claw.apply_rotation([math.pi/2, 0, 0])
        claw.apply_translation([toe_x + CLAW_LENGTH/2, toe_y, toe_z - 0.005])
        claw.visual.face_colors = steel_props["color"]
        components.append(claw)

    # Dew claw (smaller claw on inside of leg)
    dew_claw = trimesh.creation.cone(
        radius=0.002, height=CLAW_LENGTH * 0.6, sections=8
    )
    dew_claw_pos = paw_pos.copy()
    dew_claw_pos[0] += PAW_LENGTH * 0.3
    dew_claw_pos[1] += PAW_WIDTH/2 * (1 if is_left else -1)
    dew_claw_pos[2] += PAW_HEIGHT
    dew_claw.apply_rotation([math.pi/2, 0, 0])
    dew_claw.apply_translation(dew_claw_pos)
    dew_claw.visual.face_colors = steel_props["color"]
    components.append(dew_claw)

    return components


def _create_four_bar_linkage(
    hip_position: Tuple[float, float, float],
    knee_position: Tuple[float, float, float],
    crank_angle: float,
    is_left: bool = True
) -> List[trimesh.Trimesh]:
    """
    Create the four-bar linkage system for leg motion control.

    This is Leonardo's innovative mechanism that converts rotary cam motion
    into coordinated leg articulation patterns.

    Args:
        hip_position: 3D position of the hip joint
        knee_position: 3D position of the knee joint
        crank_angle: Current crank angle in radians
        is_left: True for left leg, False for right leg

    Returns:
        List of trimesh components for the four-bar linkage
    """
    components = []
    bronze_props = MATERIALS["bronze"]
    steel_props = MATERIALS["steel"]

    # Calculate linkage positions using kinematics
    kinematics = LegKinematics(True, is_left)  # Front leg kinematics
    rocker_angle, coupler_angle = kinematics.calculate_four_bar_position(crank_angle)

    # Ground link (fixed frame connection)
    ground_link = trimesh.creation.box(
        extents=[LINKAGE_WIDTH, GROUND_LINK_LENGTH, LINKAGE_WIDTH]
    )
    ground_link.apply_rotation([0, 0, math.pi/2])
    ground_link_pos = list(hip_position)
    ground_link_pos[1] -= GROUND_LINK_LENGTH/2 * (1 if is_left else -1)
    ground_link_pos[2] += 0.05
    ground_link.apply_translation(ground_link_pos)
    ground_link.visual.face_colors = bronze_props["color"]
    components.append(ground_link)

    # Crank (input from cam)
    crank_end_x = hip_position[0] + CRANK_RADIUS * math.cos(crank_angle)
    crank_end_y = hip_position[1] + CRANK_RADIUS * math.sin(crank_angle) * (1 if is_left else -1)
    crank_end_z = hip_position[2] + 0.05

    crank = trimesh.creation.cylinder(
        radius=0.005, height=CRANK_RADIUS, sections=16
    )
    crank.apply_rotation([0, math.pi/2, 0])
    crank_center = [(hip_position[0] + crank_end_x)/2,
                   (hip_position[1] + crank_end_y)/2,
                   crank_end_z]
    crank.apply_translation(crank_center)
    crank.visual.face_colors = steel_props["color"]
    components.append(crank)

    # Coupler (connecting rod)
    coupler_end_x = hip_position[0] + ROCKER_LENGTH * math.cos(rocker_angle)
    coupler_end_y = hip_position[1] + ROCKER_LENGTH * math.sin(rocker_angle) * (1 if is_left else -1)
    coupler_end_z = hip_position[2] + 0.05

    coupler_vector = np.array([coupler_end_x - crank_end_x,
                              coupler_end_y - crank_end_y,
                              coupler_end_z - crank_end_z])
    coupler_length = np.linalg.norm(coupler_vector)
    coupler_direction = coupler_vector / coupler_length

    coupler = trimesh.creation.cylinder(
        radius=0.004, height=coupler_length, sections=16
    )

    default_direction = np.array([0, 0, 1])
    rotation_axis = np.cross(default_direction, coupler_direction)
    rotation_angle = np.arccos(np.dot(default_direction, coupler_direction))

    if np.linalg.norm(rotation_axis) > 1e-6:
        coupler.apply_transform(trimesh.transformations.rotation_matrix(
            rotation_angle, rotation_axis
        ))

    coupler_center = [(crank_end_x + coupler_end_x)/2,
                     (crank_end_y + coupler_end_y)/2,
                     (crank_end_z + coupler_end_z)/2]
    coupler.apply_translation(coupler_center)
    coupler.visual.face_colors = steel_props["color"]
    components.append(coupler)

    # Rocker (output lever connected to knee)
    rocker = trimesh.creation.cylinder(
        radius=0.005, height=ROCKER_LENGTH, sections=16
    )
    rocker.apply_rotation([0, math.pi/2, 0])
    rocker_center = [(hip_position[0] + coupler_end_x)/2,
                    (hip_position[1] + coupler_end_y)/2,
                    coupler_end_z]
    rocker.apply_translation(rocker_center)
    rocker.visual.face_colors = bronze_props["color"]
    components.append(rocker)

    # Pivot joints at connections
    pivot_positions = [
        hip_position,
        (crank_end_x, crank_end_y, crank_end_z),
        (coupler_end_x, coupler_end_y, coupler_end_z),
        (hip_position[0] + ROCKER_LENGTH * math.cos(rocker_angle),
         hip_position[1] + ROCKER_LENGTH * math.sin(rocker_angle) * (1 if is_left else -1),
         hip_position[2] + 0.05)
    ]

    for pivot_pos in pivot_positions:
        pivot = trimesh.creation.sphere(radius=0.006, subdivisions=16)
        pivot.apply_translation(pivot_pos)
        pivot.visual.face_colors = bronze_props["color"]
        components.append(pivot)

    return components


def generate_complete_leg(
    is_front: bool = True,
    is_left: bool = True,
    crank_angle: float = 0.0,
    hip_position: Optional[Tuple[float, float, float]] = None,
    material: str = "oak"
) -> trimesh.Trimesh:
    """
    Generate a complete leg assembly with all components.

    Creates a full leg mechanism including hip joint, upper and lower leg,
    knee and ankle joints, paw, and four-bar linkage system.

    Args:
        is_front: True for front leg, False for rear leg
        is_left: True for left leg, False for right leg
        crank_angle: Current crank angle for linkage positioning
        hip_position: 3D position of hip joint (auto-calculated if None)
        material: Primary material for structural components

    Returns:
        Complete trimesh assembly of the leg
    """
    all_components = []

    # Calculate hip position if not provided
    if hip_position is None:
        hip_x = FORELEG_TO_HINDLEG_DISTANCE/2 if is_front else -FORELEG_TO_HINDLEG_DISTANCE/2
        hip_y = LATERAL_LEG_SPACING/2 if is_left else -LATERAL_LEG_SPACING/2
        hip_z = BODY_HEIGHT
        hip_position = (hip_x, hip_y, hip_z)

    # Calculate joint angles using kinematics
    kinematics = LegKinematics(is_front, is_left)
    hip_angle, knee_angle, ankle_angle = kinematics.calculate_joint_angles(crank_angle)

    # Create leg components in order
    hip_components = _create_hip_joint(hip_position, is_left)
    all_components.extend(hip_components)

    upper_leg_components = _create_upper_leg(hip_position, hip_angle, is_left)
    all_components.extend(upper_leg_components)

    # Calculate knee position
    knee_x = hip_position[0] + UPPER_LEG_LENGTH * math.cos(hip_angle)
    knee_y = hip_position[1]
    knee_z = hip_position[2] - UPPER_LEG_LENGTH * math.sin(hip_angle)
    knee_position = (knee_x, knee_y, knee_z)

    knee_components = _create_knee_joint(knee_position, knee_angle, is_left)
    all_components.extend(knee_components)

    lower_leg_components = _create_lower_leg(knee_position, knee_angle, ankle_angle, is_left)
    all_components.extend(lower_leg_components)

    # Calculate ankle position
    leg_extension_angle = knee_angle + ankle_angle
    ankle_x = knee_position[0] + LOWER_LEG_LENGTH * math.cos(leg_extension_angle)
    ankle_y = knee_position[1]
    ankle_z = knee_position[2] - LOWER_LEG_LENGTH * math.sin(leg_extension_angle)
    ankle_position = (ankle_x, ankle_y, ankle_z)

    paw_components = _create_paw(ankle_position, is_left)
    all_components.extend(paw_components)

    # Create four-bar linkage
    linkage_components = _create_four_bar_linkage(
        hip_position, knee_position, crank_angle, is_left
    )
    all_components.extend(linkage_components)

    # Combine all components
    if all_components:
        complete_leg = trimesh.util.concatenate(all_components)

        # Clean up the mesh
        complete_leg.remove_duplicate_faces()
        complete_leg.remove_degenerate_faces()
        complete_leg.merge_vertices()

        return complete_leg
    else:
        return trimesh.Trimesh()


def generate_all_legs(
    crank_angle: float = 0.0,
    material: str = "oak"
) -> List[trimesh.Trimesh]:
    """
    Generate all four leg assemblies for the mechanical lion.

    Creates the complete set of leg mechanisms with appropriate phase
    offsets for coordinated walking motion.

    Args:
        crank_angle: Base crank angle for leg positioning
        material: Primary material for structural components

    Returns:
        List of four trimesh leg assemblies
    """
    legs = []

    # Phase offsets for lateral sequence gait
    phase_offsets = {
        'LF': 0.0,      # Left Front - reference leg
        'RH': 0.25,     # Right Hind - 90° offset
        'RF': 0.5,      # Right Front - 180° offset
        'LH': 0.75      # Left Hind - 270° offset
    }

    leg_configs = [
        ('LF', True, True, phase_offsets['LF']),
        ('RF', True, False, phase_offsets['RF']),
        ('LH', False, True, phase_offsets['LH']),
        ('RH', False, False, phase_offsets['RH'])
    ]

    for _leg_name, is_front, is_left, phase_offset in leg_configs:
        leg_crank_angle = crank_angle + 2 * math.pi * phase_offset
        leg = generate_complete_leg(
            is_front=is_front,
            is_left=is_left,
            crank_angle=leg_crank_angle,
            material=material
        )
        legs.append(leg)

    return legs


def analyze_leg_properties(
    leg: trimesh.Trimesh,
    material: str = "oak"
) -> Dict[str, object]:
    """
    Analyze physical properties of a leg assembly.

    Calculates mass, center of mass, and structural properties for
    engineering analysis and validation.

    Args:
        leg: Trimesh leg assembly to analyze
        material: Primary material for property calculations

    Returns:
        Dictionary of calculated leg properties
    """
    mat_props = MATERIALS[material]

    # Volume and mass
    volume = leg.volume
    mass = volume * mat_props["density"]

    # Center of mass
    center_of_mass = leg.center_mass

    # Moments of inertia
    moment_of_inertia = leg.moment_inertia

    # Surface area
    surface_area = leg.area

    # Mesh statistics
    mesh_stats = {
        "vertices": len(leg.vertices),
        "faces": len(leg.faces),
        "components": leg.body_count if hasattr(leg, 'body_count') else 1
    }

    return {
        "volume_m3": volume,
        "mass_kg": mass,
        "center_of_mass_m": center_of_mass.tolist(),
        "moment_of_inertia_kgm2": moment_of_inertia.tolist(),
        "surface_area_m2": surface_area,
        "mesh_statistics": mesh_stats,
        "material": material,
        "material_properties": mat_props
    }


def export_leg_assembly(
    path: Path,
    leg_type: str = "LF",
    crank_angle: float = 0.0,
    material: str = "oak",
    format: str = "stl"
) -> Path:
    """
    Export a leg assembly to file with analysis.

    Generates and exports a complete leg assembly with comprehensive
    analysis data suitable for construction and documentation.

    Args:
        path: Output file path
        leg_type: Leg type ('LF', 'RF', 'LH', 'RH')
        crank_angle: Crank angle for leg positioning
        material: Primary material for components
        format: Export format ("stl", "obj", "ply")

    Returns:
        Path to exported file
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # Parse leg configuration
    is_front = 'F' in leg_type
    is_left = 'L' in leg_type

    # Generate leg assembly
    leg = generate_complete_leg(
        is_front=is_front,
        is_left=is_left,
        crank_angle=crank_angle,
        material=material
    )

    # Analyze properties
    properties = analyze_leg_properties(leg, material)

    # Export mesh
    if format.lower() == "stl":
        leg.export(path)
    elif format.lower() == "obj":
        leg.export(path.with_suffix(".obj"))
    elif format.lower() == "ply":
        leg.export(path.with_suffix(".ply"))
    else:
        raise ValueError(f"Unsupported export format: {format}")

    # Export analysis data
    analysis_path = path.with_name(path.stem + "_analysis.json")
    import json
    with open(analysis_path, 'w') as f:
        json.dump(properties, f, indent=2)

    return path


if __name__ == "__main__":
    # Export all leg configurations
    base_path = Path("../../artifacts/mechanical_lion/cad")

    leg_types = ['LF', 'RF', 'LH', 'RH']

    for leg_type in leg_types:
        # Export leg at neutral position
        leg_path = export_leg_assembly(
            base_path / f"leg_{leg_type.lower()}_assembly.stl",
            leg_type=leg_type,
            crank_angle=0.0,
            material="oak"
        )
        print(f"Exported {leg_type} leg assembly: {leg_path}")

        # Export leg at various positions for animation
        for angle_deg in [0, 90, 180, 270]:
            leg_anim_path = export_leg_assembly(
                base_path / f"leg_{leg_type.lower()}_pos_{angle_deg}deg.stl",
                leg_type=leg_type,
                crank_angle=math.radians(angle_deg),
                material="oak"
            )
            print(f"Exported {leg_type} leg at {angle_deg}°: {leg_anim_path}")

    print("Leonardo's Mechanical Lion leg mechanism CAD models complete!")
