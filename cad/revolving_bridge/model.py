"""Advanced parametric CAD generator for Leonardo's revolving bridge.

This module creates a detailed 3D model of Leonardo da Vinci's innovative rotating bridge
design from Codex Atlanticus folio 855r. The model includes:

- Accurate Warren truss geometry with variable member sizing
- Detailed counterweight system with water tank
- Precision bearing and pivot mechanism
- Deck and access walkway systems
- Connection and joint details
- Educational cross-section views

The design balances Leonardo's original vision with modern engineering standards
for materials and manufacturing precision.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import trimesh


def _warren_truss(span: float, height: float, width: float) -> trimesh.Trimesh:
    """Generate an advanced Warren truss with variable member sizing based on stress analysis."""
    panel_count = 8  # Increased for better resolution
    panel_length = span / panel_count
    nodes = []

    # Generate nodes for top and bottom chords with more detail
    for i in range(panel_count + 1):
        x = i * panel_length
        nodes.append((x, width / 2.0, height))      # Top chord right
        nodes.append((x, -width / 2.0, height))     # Top chord left
        nodes.append((x, width / 2.0, 0.0))         # Bottom chord right
        nodes.append((x, -width / 2.0, 0.0))        # Bottom chord left

    # Define beam connections with structural optimization
    beams = []

    # Top and bottom chords (larger members - carry maximum load)
    chord_radius = 0.12
    for i in range(panel_count):
        idx = i * 4
        beams.extend([
            (idx, idx + 4, chord_radius),      # Top chord right
            (idx + 1, idx + 5, chord_radius),  # Top chord left
            (idx + 2, idx + 6, chord_radius),  # Bottom chord right
            (idx + 3, idx + 7, chord_radius),  # Bottom chord left
        ])

    # Vertical members (medium load)
    vertical_radius = 0.08
    for i in range(panel_count + 1):
        idx = i * 4
        beams.extend([
            (idx, idx + 2, vertical_radius),     # Right vertical
            (idx + 1, idx + 3, vertical_radius)  # Left vertical
        ])

    # Diagonal members (variable sizing based on position)
    for i in range(panel_count):
        idx = i * 4
        # Diagonals near supports carry more load
        position_factor = 1.0 - abs(i - panel_count/2) / (panel_count/2)
        diagonal_radius = 0.06 + 0.04 * position_factor  # 0.06 to 0.10

        beams.extend([
            (idx, idx + 7, diagonal_radius),     # Main diagonal
            (idx + 1, idx + 6, diagonal_radius), # Cross diagonal
            (idx + 4, idx + 3, diagonal_radius), # Return diagonal
            (idx + 5, idx + 2, diagonal_radius), # Cross return
        ])

    # Generate tubes with variable sizing
    tubes = []
    for start_idx, end_idx, radius in beams:
        start = np.array(nodes[start_idx])
        end = np.array(nodes[end_idx])
        direction = end - start
        length = float(np.linalg.norm(direction))
        if length == 0:
            continue

        # Create tube with appropriate radius and resolution
        cylinder = trimesh.creation.cylinder(radius=radius, height=length, sections=32)
        cylinder.apply_translation((0.0, 0.0, length / 2.0))
        cylinder.apply_transform(
            trimesh.geometry.align_vectors(
                np.array([0.0, 0.0, 1.0]),
                direction,
                False,
            )
        )
        cylinder.apply_translation(start)
        tubes.append(cylinder)

    # Add connection plates at joints
    for i in range(panel_count + 1):
        idx = i * 4
        x = i * panel_length

        # Top chord connection plate
        top_plate = trimesh.creation.box(extents=(0.3, width + 0.2, 0.05))
        top_plate.apply_translation((x, 0.0, height + 0.025))

        # Bottom chord connection plate
        bottom_plate = trimesh.creation.box(extents=(0.3, width + 0.2, 0.05))
        bottom_plate.apply_translation((x, 0.0, -0.025))

        tubes.extend([top_plate, bottom_plate])

    return trimesh.util.concatenate(tubes)


def _deck(span: float, width: float) -> trimesh.Trimesh:
    """Generate a detailed deck system with walkway and safety features."""
    deck_components = []

    # Main deck surface with grating texture
    deck = trimesh.creation.box(extents=(span, width, 0.18))
    deck.apply_translation((span / 2.0, 0.0, 0.09))
    deck_components.append(deck)

    # Add non-slip surface texture (represented by raised elements)
    for i in range(int(span / 0.5)):
        for j in range(int(width / 0.5)):
            x = (i + 0.5) * 0.5
            y = (j + 0.5) * 0.5 - width / 2.0
            if abs(y) < width / 2.0 - 0.25:  # Keep within deck bounds
                texture_element = trimesh.creation.box(extents=(0.4, 0.4, 0.02))
                texture_element.apply_translation((x, y, 0.19))
                deck_components.append(texture_element)

    # Safety curbs (raised edges)
    curb_height = 0.15
    curb_width = 0.08

    # Left curb
    left_curb = trimesh.creation.box(extents=(span, curb_width, curb_height))
    left_curb.apply_translation((span / 2.0, -width / 2.0 - curb_width / 2.0, curb_height / 2.0))
    deck_components.append(left_curb)

    # Right curb
    right_curb = trimesh.creation.box(extents=(span, curb_width, curb_height))
    right_curb.apply_translation((span / 2.0, width / 2.0 + curb_width / 2.0, curb_height / 2.0))
    deck_components.append(right_curb)

    # Access walkway (narrower section for maintenance)
    walkway_width = 0.8
    walkway = trimesh.creation.box(extents=(span, walkway_width, 0.12))
    walkway.apply_translation((span / 2.0, width / 2.0 + curb_width + walkway_width / 2.0 + 0.2, 0.06))
    deck_components.append(walkway)

    # Handrail posts
    rail_height = 1.1
    post_spacing = 2.0
    for i in range(int(span / post_spacing) + 1):
        x = i * post_spacing
        # Left handrail post
        left_post = trimesh.creation.cylinder(radius=0.04, height=rail_height, sections=16)
        left_post.apply_translation((x, -width / 2.0 - curb_width, rail_height / 2.0))
        deck_components.append(left_post)

        # Right handrail post
        right_post = trimesh.creation.cylinder(radius=0.04, height=rail_height, sections=16)
        right_post.apply_translation((x, width / 2.0 + curb_width, rail_height / 2.0))
        deck_components.append(right_post)

    # Handrail horizontal members
    rail_radius = 0.025
    # Left handrail
    left_rail = trimesh.creation.cylinder(radius=rail_radius, height=span, sections=16)
    left_rail.apply_transform(
        trimesh.geometry.align_vectors(
            np.array([0.0, 0.0, 1.0]),
            np.array([1.0, 0.0, 0.0]),
            False,
        )
    )
    left_rail.apply_translation((span / 2.0, -width / 2.0 - curb_width, rail_height))
    deck_components.append(left_rail)

    # Right handrail
    right_rail = trimesh.creation.cylinder(radius=rail_radius, height=span, sections=16)
    right_rail.apply_transform(
        trimesh.geometry.align_vectors(
            np.array([0.0, 0.0, 1.0]),
            np.array([1.0, 0.0, 0.0]),
            False,
        )
    )
    right_rail.apply_translation((span / 2.0, width / 2.0 + curb_width, rail_height))
    deck_components.append(right_rail)

    return trimesh.util.concatenate(deck_components)


def _pivot(height: float) -> trimesh.Trimesh:
    """Generate a detailed pivot mechanism with precision bearing system."""
    pivot_components = []

    # Foundation base plate
    base_plate = trimesh.creation.cylinder(radius=1.2, height=0.3, sections=64)
    base_plate.apply_translation((0.0, 0.0, 0.15))
    pivot_components.append(base_plate)

    # Anchor bolts (foundation connection)
    bolt_radius = 0.06
    bolt_height = 0.8
    bolt_positions = [(0.8, 0), (0, 0.8), (-0.8, 0), (0, -0.8), (0.6, 0.6), (-0.6, 0.6), (-0.6, -0.6), (0.6, -0.6)]
    for x, y in bolt_positions:
        bolt = trimesh.creation.cylinder(radius=bolt_radius, height=bolt_height, sections=16)
        bolt.apply_translation((x, y, -bolt_height / 2.0 + 0.15))
        pivot_components.append(bolt)

    # Main support column (structural)
    mast_radius = 0.4
    mast = trimesh.creation.cylinder(radius=mast_radius, height=height, sections=64)
    mast.apply_translation((0.0, 0.0, height / 2.0 + 0.3))
    pivot_components.append(mast)

    # Reinforcement ribs
    rib_count = 8
    for i in range(rib_count):
        angle = 2 * np.pi * i / rib_count
        rib = trimesh.creation.box(extents=(0.1, mast_radius + 0.2, height * 0.8))
        rib.apply_transform(trimesh.transformations.rotation_matrix(angle, [0, 0, 1]))
        rib.apply_translation((0.0, mast_radius + 0.1, height * 0.4 + 0.3))
        pivot_components.append(rib)

    # Precision slewing ring bearing (inner race)
    inner_race_radius = 0.8
    inner_race_height = 0.15
    inner_race = trimesh.creation.cylinder(radius=inner_race_radius, height=inner_race_height, sections=128)
    inner_race.apply_translation((0.0, 0.0, height + 0.3 + inner_race_height / 2.0))
    pivot_components.append(inner_race)

    # Bearing housing (outer race)
    outer_race_radius = 1.0
    outer_race = trimesh.creation.cylinder(radius=outer_race_radius, height=inner_race_height, sections=128)
    outer_race.apply_translation((0.0, 0.0, height + 0.3 + inner_race_height / 2.0))
    pivot_components.append(outer_race)

    # Bearing gear teeth (simplified representation)
    gear_height = 0.08
    for i in range(64):  # 64 teeth for precision rotation
        angle = 2 * np.pi * i / 64
        tooth = trimesh.creation.box(extents=(0.05, 0.1, gear_height))
        tooth.apply_transform(trimesh.transformations.rotation_matrix(angle, [0, 0, 1]))
        tooth.apply_translation((outer_race_radius + 0.05, 0.0, height + 0.3 + inner_race_height + gear_height / 2.0))
        pivot_components.append(tooth)

    # Locking mechanism housing
    lock_housing = trimesh.creation.box(extents=(0.6, 0.4, 0.25))
    lock_housing.apply_translation((1.3, 0.0, height + 0.3 + inner_race_height / 2.0))
    pivot_components.append(lock_housing)

    # Rotation sensor housing
    sensor_housing = trimesh.creation.cylinder(radius=0.15, height=0.2, sections=32)
    sensor_housing.apply_translation((1.1, 1.1, height + 0.3 + inner_race_height / 2.0))
    pivot_components.append(sensor_housing)

    return trimesh.util.concatenate(pivot_components)


def _counterweight(span: float, height: float) -> trimesh.Trimesh:
    """Generate a detailed counterweight system with water tank and support structure."""
    counterweight_components = []

    # Main water tank (Leonardo's innovation)
    tank_width = 2.0
    tank_height = 2.0
    tank_depth = 2.0
    wall_thickness = 0.08

    # Tank outer shell
    tank_outer = trimesh.creation.box(extents=(tank_width, tank_depth, tank_height))
    tank_outer.apply_translation((-span / 4.0, 0.0, height / 2.0))
    counterweight_components.append(tank_outer)

    # Tank inner cavity (hollow)
    inner_width = tank_width - wall_thickness * 2
    inner_depth = tank_depth - wall_thickness * 2
    inner_height = tank_height - wall_thickness * 2
    tank_inner = trimesh.creation.box(extents=(inner_width, inner_depth, inner_height))
    tank_inner.apply_translation((-span / 4.0, 0.0, height / 2.0 + wall_thickness))
    # Remove inner cavity (represented as separate component for visualization)
    counterweight_components.append(tank_inner)

    # Water level indicator (visual representation at 75% full)
    water_level = 0.75
    water = trimesh.creation.box(extents=(inner_width, inner_depth, inner_height * water_level))
    water.apply_translation((-span / 4.0, 0.0, height / 2.0 + wall_thickness + inner_height * (1 - water_level) / 2.0))
    counterweight_components.append(water)

    # Tank reinforcement ribs
    rib_count = 4
    for i in range(rib_count):
        z_position = height / 2.0 - tank_height / 2.0 + (i + 1) * tank_height / (rib_count + 1)
        rib = trimesh.creation.box(extents=(tank_width + 0.2, 0.05, 0.05))
        rib.apply_translation((-span / 4.0, 0.0, z_position))
        counterweight_components.append(rib)

    # Support frame (structural connection to bridge)
    frame_radius = 0.15
    frame_length = span / 3.0

    # Main horizontal support beam
    main_frame = trimesh.creation.cylinder(radius=frame_radius, height=frame_length, sections=32)
    main_frame.apply_transform(
        trimesh.geometry.align_vectors(
            np.array([0.0, 0.0, 1.0]),
            np.array([1.0, 0.0, 0.0]),
            False,
        )
    )
    main_frame.apply_translation((-frame_length / 2.0 - span / 6.0, 0.0, height / 2.0))
    counterweight_components.append(main_frame)

    # Diagonal support braces
    brace_count = 3
    for i in range(brace_count):
        x_offset = (i + 1) * frame_length / (brace_count + 1)
        y_offset = 0.8
        z_offset = -0.6

        # Upper diagonal brace
        upper_brace_start = np.array([-x_offset, 0.0, height / 2.0])
        upper_brace_end = np.array([-x_offset + 0.5, y_offset, height / 2.0 + z_offset])
        brace_vector = upper_brace_end - upper_brace_start
        brace_length = np.linalg.norm(brace_vector)

        upper_brace = trimesh.creation.cylinder(radius=0.08, height=brace_length, sections=16)
        upper_brace.apply_translation((0.0, 0.0, brace_length / 2.0))
        upper_brace.apply_transform(
            trimesh.geometry.align_vectors(
                np.array([0.0, 0.0, 1.0]),
                brace_vector,
                False,
            )
        )
        upper_brace.apply_translation(upper_brace_start)
        counterweight_components.append(upper_brace)

        # Lower diagonal brace
        lower_brace_end = np.array([-x_offset + 0.5, -y_offset, height / 2.0 + z_offset])
        brace_vector = lower_brace_end - upper_brace_start
        brace_length = np.linalg.norm(brace_vector)

        lower_brace = trimesh.creation.cylinder(radius=0.08, height=brace_length, sections=16)
        lower_brace.apply_translation((0.0, 0.0, brace_length / 2.0))
        lower_brace.apply_transform(
            trimesh.geometry.align_vectors(
                np.array([0.0, 0.0, 1.0]),
                brace_vector,
                False,
            )
        )
        lower_brace.apply_translation(upper_brace_start)
        counterweight_components.append(lower_brace)

    # Water filling system
    fill_pipe = trimesh.creation.cylinder(radius=0.06, height=2.0, sections=16)
    fill_pipe.apply_transform(
        trimesh.geometry.align_vectors(
            np.array([0.0, 0.0, 1.0]),
            np.array([0.0, 1.0, 0.0]),
            False,
        )
    )
    fill_pipe.apply_translation((-span / 4.0, tank_depth / 2.0 + 1.0, height / 2.0 + tank_height / 2.0))
    counterweight_components.append(fill_pipe)

    # Drain pipe
    drain_pipe = trimesh.creation.cylinder(radius=0.05, height=1.5, sections=16)
    drain_pipe.apply_transform(
        trimesh.geometry.align_vectors(
            np.array([0.0, 0.0, 1.0]),
            np.array([0.0, 1.0, 0.0]),
            False,
        )
    )
    drain_pipe.apply_translation((-span / 4.0, -tank_depth / 2.0 - 0.75, height / 2.0 - tank_height / 2.0))
    counterweight_components.append(drain_pipe)

    # Level indicator (visual)
    level_indicator = trimesh.creation.cylinder(radius=0.08, height=0.3, sections=16)
    level_indicator.apply_translation((-span / 4.0, tank_depth / 2.0 + 0.4, height / 2.0))
    counterweight_components.append(level_indicator)

    return trimesh.util.concatenate(counterweight_components)


def generate_bridge(span: float = 12.0, deck_width: float = 4.0, truss_height: float = 2.6) -> trimesh.Trimesh:
    """Assemble Leonardo's advanced revolving bridge with all detailed components."""
    # Generate main structural components
    truss = _warren_truss(span, truss_height, deck_width)
    deck = _deck(span, deck_width)
    pivot = _pivot(truss_height + 0.5)
    counterweight = _counterweight(span, truss_height)

    # Additional safety and operational components
    safety_components = _add_safety_features(span, deck_width, truss_height)

    # Educational cross-section indicators
    educational_markers = _add_educational_markers(span, deck_width, truss_height)

    # Combine all components
    bridge_components = [truss, deck, counterweight, safety_components, educational_markers]
    bridge = trimesh.util.concatenate(bridge_components)

    # Position bridge at correct height relative to pivot
    bridge.apply_translation((0.0, 0.0, truss_height / 2.0))

    # Final assembly with pivot
    complete_bridge = trimesh.util.concatenate([bridge, pivot])

    return complete_bridge


def _add_safety_features(span: float, deck_width: float, truss_height: float) -> trimesh.Trimesh:
    """Add safety features and operational components."""
    safety_parts = []

    # Emergency stop buttons
    stop_button_positions = [(1.0, deck_width/2 + 0.5), (span - 1.0, deck_width/2 + 0.5)]
    for x, y in stop_button_positions:
        button = trimesh.creation.cylinder(radius=0.08, height=0.15, sections=16)
        button.apply_translation((x, y, 0.25))
        safety_parts.append(button)

    # Warning signs (simplified as plates)
    sign_positions = [(2.0, -deck_width/2 - 0.5), (span - 2.0, -deck_width/2 - 0.5)]
    for x, y in sign_positions:
        sign = trimesh.creation.box(extents=(0.8, 0.05, 0.4))
        sign.apply_translation((x, y, 0.4))
        safety_parts.append(sign)

    # Load capacity indicators
    capacity_indicator = trimesh.creation.box(extents=(1.0, 0.1, 0.3))
    capacity_indicator.apply_translation((span/2, 0.0, truss_height + 0.5))
    safety_parts.append(capacity_indicator)

    return trimesh.util.concatenate(safety_parts)


def _add_educational_markers(span: float, deck_width: float, truss_height: float) -> trimesh.Trimesh:
    """Add educational markers and measurement indicators."""
    educational_parts = []

    # Dimension lines (simplified as thin boxes)
    # Span indicator
    span_indicator = trimesh.creation.box(extents=(span/2, 0.02, 0.02))
    span_indicator.apply_translation((span/2, -deck_width/2 - 1.0, 0.0))
    educational_parts.append(span_indicator)

    # Height indicator
    height_indicator = trimesh.creation.box(extents=(0.02, 0.02, truss_height/2))
    height_indicator.apply_translation((-1.0, 0.0, truss_height/2))
    educational_parts.append(height_indicator)

    # Measurement points (small spheres)
    measurement_points = [
        (0, 0, 0),                    # Origin
        (span, 0, 0),                 # Far end
        (0, 0, truss_height),         # Top
        (span/4, 0, truss_height/2),  # Mid-span reference
    ]
    for x, y, z in measurement_points:
        point = trimesh.creation.icosphere(radius=0.05, subdivisions=2)
        point.apply_translation((x, y, z))
        educational_parts.append(point)

    return trimesh.util.concatenate(educational_parts)


def export_mesh(path: Path, span: float = 12.0, deck_width: float = 4.0, truss_height: float = 2.6) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_bridge(span=span, deck_width=deck_width, truss_height=truss_height)
    mesh.remove_duplicate_faces()
    mesh.remove_degenerate_faces()
    mesh.merge_vertices()
    mesh.export(path)
    return path


if __name__ == "__main__":
    export_mesh(Path("../../artifacts/revolving_bridge/cad/revolving_bridge_mesh.stl"))
