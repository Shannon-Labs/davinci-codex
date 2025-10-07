"""
Parametric mesh generator for Leonardo's Aerial Screw rotor.

This module creates detailed 3D models of the helical rotor with historically
accurate geometry and modern materials analysis. The generator supports both
Leonardo's original design parameters and modern optimized configurations.

Features:
- Parametric helical blade geometry with variable thickness
- Support for both historical (linen) and modern (composite) materials
- Aerodynamic surface modeling with realistic airfoil cross-sections
- Structural analysis integration with material properties
- Multiple configuration options for educational and research purposes
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import trimesh

# Leonardo's original design parameters (from Codex Atlanticus analysis)
LEONARDO_RADIUS = 4.0  # meters
LEONARDO_INNER_RADIUS = 3.2  # meters
LEONARDO_PITCH = 8.0  # meters per revolution
LEONARDO_TURNS = 3.0
LEONARDO_WIDTH = 0.3  # meters (linen ribbon width)

# Modern optimized parameters
MODERN_RADIUS = 2.0  # meters
MODERN_INNER_RADIUS = 1.6  # meters
MODERN_PITCH = 3.5  # meters per revolution
MODERN_TURNS = 2.5
MODERN_THICKNESS = 0.06  # meters (carbon fiber thickness)

# Material properties
MATERIALS = {
    "linen": {
        "density": 150,  # kg/m³
        "elastic_modulus": 0.5e9,  # Pa
        "tensile_strength": 50e6,  # Pa
        "color": [0.9, 0.85, 0.7, 1.0]  # Beige
    },
    "reed": {
        "density": 400,  # kg/m³
        "elastic_modulus": 10e9,  # Pa
        "tensile_strength": 100e6,  # Pa
        "color": [0.7, 0.6, 0.4, 1.0]  # Brown
    },
    "carbon_fiber": {
        "density": 1600,  # kg/m³
        "elastic_modulus": 150e9,  # Pa
        "tensile_strength": 3.5e9,  # Pa
        "color": [0.2, 0.2, 0.2, 1.0]  # Black
    },
    "aluminum": {
        "density": 2700,  # kg/m³
        "elastic_modulus": 70e9,  # Pa
        "tensile_strength": 310e6,  # Pa
        "color": [0.7, 0.7, 0.8, 1.0]  # Light gray
    }
}


def _airfoil_section(
    chord: float,
    thickness_ratio: float = 0.12,
    camber_ratio: float = 0.02,
    num_points: int = 20
) -> np.ndarray:
    """
    Generate NACA-like airfoil cross-section coordinates.

    Creates a realistic airfoil shape for the blade cross-section rather than
    a simple rectangular profile. This improves both aesthetic and aerodynamic
    accuracy of the model.

    Args:
        chord: Chord length [m]
        thickness_ratio: Maximum thickness as fraction of chord
        camber_ratio: Maximum camber as fraction of chord
        num_points: Number of points defining the airfoil

    Returns:
        Array of (x, y) coordinates defining the airfoil shape
    """
    # NACA 4-digit thickness distribution
    x = np.linspace(0, 1, num_points)

    # Thickness distribution (NACA 0012-like)
    yt = 5 * thickness_ratio * (
        0.2969 * np.sqrt(x) -
        0.1260 * x -
        0.3516 * x**2 +
        0.2843 * x**3 -
        0.1036 * x**4
    )

    # Camber line (NACA 2412-like)
    p = 0.4  # Position of maximum camber
    m = camber_ratio
    yc = np.where(x < p,
                  m / p**2 * (2 * p * x - x**2),
                  m / (1 - p)**2 * ((1 - 2 * p) + 2 * p * x - x**2))

    # Upper and lower surfaces
    xu = x * chord
    yu = yc + yt * chord
    xl = x * chord
    yl = yc - yt * chord

    # Combine upper and lower surfaces
    airfoil = np.zeros((2 * num_points, 2))
    airfoil[:num_points] = np.column_stack([xu, yu])
    airfoil[num_points:] = np.column_stack([xl[::-1], yl[::-1]])

    return airfoil


def _helical_blade_vertices(
    *,
    radius_outer: float,
    radius_inner: float,
    pitch: float,
    turns: float,
    thickness: float,
    steps: int = 100,
    cross_sections: int = 20,
    airfoil_sections: bool = True
) -> Tuple[np.ndarray, np.ndarray, List[Dict]]:
    """
    Generate vertices and faces for a helical blade with improved geometry.

    This function creates a sophisticated helical blade model with either
    rectangular or airfoil cross-sections, providing more realistic
    geometry for both visualization and analysis.

    Args:
        radius_outer: Outer radius of helix [m]
        radius_inner: Inner radius of helix [m]
        pitch: Helical pitch [m per revolution]
        turns: Number of complete revolutions
        thickness: Blade thickness [m]
        steps: Number of steps along the helix
        cross_sections: Number of cross-sections along radius
        airfoil_sections: Use airfoil cross-sections if True

    Returns:
        Tuple of (vertices, faces, metadata)
    """
    theta = np.linspace(0.0, 2.0 * np.pi * turns, steps)
    z = pitch * theta / (2.0 * np.pi)
    r = np.linspace(radius_inner, radius_outer, cross_sections)

    vertices = []
    vertex_metadata = []

    for t_idx, (angle, height) in enumerate(zip(theta, z)):
        cos_a = float(np.cos(angle))
        sin_a = float(np.sin(angle))

        for r_idx, radius in enumerate(r):
            # Local chord varies with radius (tapered blade)
            local_chord = thickness * (1.0 - 0.3 * (radius - radius_inner) / (radius_outer - radius_inner))

            if airfoil_sections:
                # Generate airfoil cross-section
                airfoil = _airfoil_section(local_chord, 0.12, 0.02, 12)

                # Transform airfoil to 3D position
                for x_air, y_air in airfoil:
                    # Rotate airfoil to align with radial direction
                    x_rot = x_air * cos_a - y_air * sin_a
                    y_rot = x_air * sin_a + y_air * cos_a
                    z_pos = height

                    vertices.append([x_rot, y_rot, z_pos])
                    vertex_metadata.append({
                        'section': r_idx,
                        'step': t_idx,
                        'radius': radius,
                        'angle': angle,
                        'chord': local_chord
                    })
            else:
                # Simple rectangular cross-section
                for x_offset in (-local_chord/2, local_chord/2):
                    for y_offset in (-thickness/2, thickness/2):
                        x = radius * cos_a + x_offset * cos_a - y_offset * sin_a
                        y = radius * sin_a + x_offset * sin_a + y_offset * cos_a
                        vertices.append([x, y, height])
                        vertex_metadata.append({
                            'section': r_idx,
                            'step': t_idx,
                            'radius': radius,
                            'angle': angle,
                            'chord': local_chord
                        })

    vertices_np = np.array(vertices, dtype=float)
    faces = []

    # Generate faces (quads or triangles)
    vertices_per_section = len(r) * (12 if airfoil_sections else 4)

    for step in range(steps - 1):
        for section in range(cross_sections - 1):
            # Index calculation depends on cross-section type
            if airfoil_sections:
                # Airfoil cross-sections have more complex connectivity
                base1 = step * vertices_per_section + section * 12
                base2 = (step + 1) * vertices_per_section + section * 12

                # Simplified face generation for airfoil
                for i in range(11):
                    faces.append((base1 + i, base1 + i + 1, base2 + i + 1, base2 + i))
            else:
                # Rectangular cross-sections
                base = step * vertices_per_section + section * 4
                nxt = base + vertices_per_section

                # Four vertices per section form a quad
                faces.extend([
                    (base + 0, base + 1, nxt + 1, nxt + 0),  # bottom
                    (base + 2, nxt + 2, nxt + 3, base + 3),  # top
                    (base + 0, nxt + 0, nxt + 2, base + 2),  # inner
                    (base + 1, base + 3, nxt + 3, nxt + 1),  # outer
                ])

    return vertices_np, np.array(faces, dtype=np.int64), vertex_metadata


def _support_structure(
    blade_height: float,
    radius: float,
    material: str = "aluminum"
) -> Tuple[trimesh.Trimesh, List[trimesh.Trimesh]]:
    """
    Generate support structure for the helical rotor.

    Creates central mast, support struts, and reinforcing rings that would
    have been necessary for Leonardo's design. Modern materials allow for
    more efficient structures.

    Args:
        blade_height: Height of the helical blade [m]
        radius: Rotor radius [m]
        material: Material for structural components

    Returns:
        Tuple of (mast_mesh, support_meshes)
    """
    support_meshes = []
    mat_props = MATERIALS[material]

    # Central mast
    mast_radius = 0.15  # meters
    mast = trimesh.creation.cylinder(
        radius=mast_radius,
        height=blade_height + 1.0,
        sections=64
    )
    mast.apply_translation([0, 0, (blade_height + 1.0) / 2.0])
    mast.visual.face_colors = mat_props["color"]

    # Support rings at regular intervals
    num_rings = 4
    for i in range(num_rings):
        ring_height = blade_height * (i + 1) / (num_rings + 1)
        ring = trimesh.creation.torus(
            major_radius=radius * 0.8,
            minor_radius=0.02,
            major_sections=32,
            minor_sections=16
        )
        ring.apply_rotation([np.pi/2, 0, 0])  # Orient horizontally
        ring.apply_translation([0, 0, ring_height])
        ring.visual.face_colors = mat_props["color"]
        support_meshes.append(ring)

    # Support struts
    num_struts = 8
    for i in range(num_struts):
        angle = 2 * np.pi * i / num_struts
        strut_start = [mast_radius * np.cos(angle), mast_radius * np.sin(angle), 0]
        strut_end = [radius * 0.9 * np.cos(angle), radius * 0.9 * np.sin(angle), blade_height * 0.8]

        # Create cylinder for strut
        strut_vector = np.array(strut_end) - np.array(strut_start)
        strut_length = np.linalg.norm(strut_vector)
        strut = trimesh.creation.cylinder(
            radius=0.03,
            height=strut_length,
            sections=16
        )

        # Position and orient strut
        strut_center = (np.array(strut_start) + np.array(strut_end)) / 2
        strut.apply_translation(strut_center)

        # Align strut with direction vector
        strut_axis = strut_vector / strut_length
        default_axis = [0, 0, 1]
        rotation_axis = np.cross(default_axis, strut_axis)
        rotation_angle = np.arccos(np.dot(default_axis, strut_axis))
        if np.linalg.norm(rotation_axis) > 1e-6:
            strut.apply_transform(trimesh.transformations.rotation_matrix(
                rotation_angle, rotation_axis
            ))

        strut.visual.face_colors = mat_props["color"]
        support_meshes.append(strut)

    return mast, support_meshes


def generate_mesh(
    configuration: str = "modern",
    include_supports: bool = True,
    material: str = "carbon_fiber"
) -> trimesh.Trimesh:
    """
    Generate complete aerial screw assembly mesh.

    Creates a comprehensive 3D model of the aerial screw with appropriate
    geometry for the specified configuration and materials.

    Args:
        configuration: "leonardo" or "modern"
        include_supports: Include support structure if True
        material: Primary material for components

    Returns:
        Complete trimesh assembly
    """
    if configuration == "leonardo":
        blade_vertices, blade_faces, metadata = _helical_blade_vertices(
            radius_outer=LEONARDO_RADIUS,
            radius_inner=LEONARDO_INNER_RADIUS,
            pitch=LEONARDO_PITCH,
            turns=LEONARDO_TURNS,
            thickness=LEONARDO_WIDTH,
            steps=150,
            cross_sections=8,
            airfoil_sections=False
        )
        blade_material = "linen"
    else:  # modern
        blade_vertices, blade_faces, metadata = _helical_blade_vertices(
            radius_outer=MODERN_RADIUS,
            radius_inner=MODERN_INNER_RADIUS,
            pitch=MODERN_PITCH,
            turns=MODERN_TURNS,
            thickness=MODERN_THICKNESS,
            steps=120,
            cross_sections=12,
            airfoil_sections=True
        )
        blade_material = material

    # Create blade mesh
    blade_mesh = trimesh.Trimesh(vertices=blade_vertices, faces=blade_faces, process=True)
    mat_props = MATERIALS[blade_material]
    blade_mesh.visual.face_colors = mat_props["color"]

    # Add support structure if requested
    mesh_list = [blade_mesh]

    if include_supports:
        blade_height = blade_vertices[:, 2].max()
        radius = blade_vertices[:, :2].max(axis=0)[0]

        mast, supports = _support_structure(blade_height, radius, material)
        mesh_list.append(mast)
        mesh_list.extend(supports)

    # Combine all meshes
    if len(mesh_list) > 1:
        assembly = trimesh.util.concatenate(mesh_list)
    else:
        assembly = blade_mesh

    # Clean up mesh
    assembly.remove_duplicate_faces()
    assembly.remove_degenerate_faces()
    assembly.merge_vertices()

    return assembly


def analyze_mesh_properties(mesh: trimesh.Trimesh, material: str = "carbon_fiber") -> Dict:
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
    mat_props = MATERIALS[material]

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
    configuration: str = "modern",
    include_supports: bool = True,
    material: str = "carbon_fiber",
    format: str = "stl"
) -> Path:
    """
    Export aerial screw mesh to file with analysis.

    Generates and exports the mesh with comprehensive analysis data.

    Args:
        path: Output file path
        configuration: "leonardo" or "modern"
        include_supports: Include support structure
        material: Material for components
        format: Export format ("stl", "obj", "ply")

    Returns:
        Path to exported file
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # Generate mesh
    mesh = generate_mesh(configuration, include_supports, material)

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
    # Generate and export both configurations
    base_path = Path("../../artifacts/aerial_screw/cad")

    # Leonardo's original design
    leonardo_path = export_mesh(
        base_path / "aerial_screw_leonardo.stl",
        configuration="leonardo",
        include_supports=True,
        material="linen"
    )
    print(f"Exported Leonardo design: {leonardo_path}")

    # Modern optimized design
    modern_path = export_mesh(
        base_path / "aerial_screw_modern.stl",
        configuration="modern",
        include_supports=True,
        material="carbon_fiber"
    )
    print(f"Exported modern design: {modern_path}")
