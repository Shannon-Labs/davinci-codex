"""CAD generation for da Vinci's pyramid parachute."""

import math
from pathlib import Path

import numpy as np


def generate_pyramid_parachute(size: float, output_dir: Path) -> None:
    """Generate parametric CAD model of pyramid parachute.

    Args:
        size: Base width/depth in meters
        output_dir: Directory for output files
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate OpenSCAD script for parametric model
    scad_content = f"""
// da Vinci Pyramid Parachute - Parametric Model
// Based on Codex Atlanticus folio 381v

// Parameters
size = {size * 1000};  // Convert to mm
frame_diameter = 25;    // Frame pole diameter in mm
canopy_thickness = 0.5; // Canopy material thickness in mm

// Calculate pyramid height (equilateral triangles)
pyramid_height = size * 0.866;

module pyramid_frame() {{
    // Base square frame
    color("brown", 0.8)
    union() {{
        // Four base edges
        for (i = [0:3]) {{
            rotate([0, 0, i*90])
            translate([size/2, 0, 0])
            rotate([0, 90, 0])
            cylinder(h=size, d=frame_diameter, center=true);
        }}

        // Four apex edges
        for (i = [0:3]) {{
            rotate([0, 0, i*90])
            translate([size/2, size/2, 0])
            rotate([atan(pyramid_height/(size/sqrt(2))), 0, 45])
            cylinder(h=sqrt(pow(size/sqrt(2), 2) + pow(pyramid_height, 2)), d=frame_diameter);
        }}
    }}
}}

module canopy() {{
    // Pyramid canopy (simplified as solid for visualization)
    color("lightblue", 0.7)
    translate([0, 0, pyramid_height/2])
    scale([1, 1, pyramid_height/(size/2)])
    rotate([0, 0, 45])
    cylinder(h=size/2, d1=size*sqrt(2), d2=0, center=true, $fn=4);
}}

module suspension_lines() {{
    // Simplified suspension lines from apex to payload
    color("gray", 0.5)
    for (i = [0:3]) {{
        rotate([0, 0, i*90])
        translate([size/3, size/3, 0])
        cylinder(h=pyramid_height*1.2, d=2);
    }}
}}

module payload_harness() {{
    // Simplified payload attachment point
    color("darkgray")
    translate([0, 0, -200])
    cylinder(h=50, d=100, center=true);
}}

// Assembly
pyramid_frame();
canopy();
suspension_lines();
payload_harness();

// Export note
echo(str("Parachute size: ", size/1000, " meters"));
echo(str("Pyramid height: ", pyramid_height/1000, " meters"));
echo(str("Estimated canopy area: ", 2*size*sqrt(pow(size/2,2)+pow(pyramid_height,2))/1000000, " m²"));
"""

    scad_path = output_dir / "pyramid_parachute.scad"
    with open(scad_path, "w") as f:
        f.write(scad_content)

    # Generate STL mesh data (simplified pyramid)
    generate_stl_mesh(size, output_dir / "pyramid_parachute.stl")

    # Generate technical drawing data
    generate_technical_drawing(size, output_dir / "technical_drawing.svg")


def generate_stl_mesh(size: float, output_path: Path) -> None:
    """Generate STL mesh file for 3D printing/visualization.

    Args:
        size: Base width in meters
        output_path: Path for STL file
    """
    # Simplified pyramid vertices (in meters, scaled for printing)
    scale = 0.01  # 1:100 scale model
    s = size * scale
    h = size * 0.866 * scale  # Pyramid height

    # Define vertices
    vertices = [
        # Base square
        [-s/2, -s/2, 0],
        [s/2, -s/2, 0],
        [s/2, s/2, 0],
        [-s/2, s/2, 0],
        # Apex
        [0, 0, h]
    ]

    # Define faces (triangles)
    faces = [
        # Base (2 triangles)
        [0, 1, 2],
        [0, 2, 3],
        # Sides (4 triangles)
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4]
    ]

    # Write STL file (ASCII format)
    with open(output_path, "w") as f:
        f.write("solid pyramid_parachute\n")

        for face in faces:
            # Calculate normal vector
            v1 = np.array(vertices[face[1]]) - np.array(vertices[face[0]])
            v2 = np.array(vertices[face[2]]) - np.array(vertices[face[0]])
            normal = np.cross(v1, v2)
            normal = normal / np.linalg.norm(normal)

            f.write(f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")
            f.write("    outer loop\n")
            for vertex_idx in face:
                v = vertices[vertex_idx]
                f.write(f"      vertex {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")

        f.write("endsolid pyramid_parachute\n")


def generate_technical_drawing(size: float, output_path: Path) -> None:
    """Generate SVG technical drawing with dimensions.

    Args:
        size: Base width in meters
        output_path: Path for SVG file
    """
    # Drawing scale (pixels per meter)
    scale = 50
    margin = 100
    width = int(size * scale + 2 * margin)
    height = int(size * scale + 2 * margin)

    pyramid_height = size * 0.866

    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="{width/2}" y="30" font-family="Arial" font-size="18" font-weight="bold" text-anchor="middle">
    da Vinci Pyramid Parachute - Technical Drawing
  </text>
  <text x="{width/2}" y="50" font-family="Arial" font-size="12" text-anchor="middle">
    Codex Atlanticus folio 381v (circa 1485)
  </text>

  <!-- Front view -->
  <g transform="translate({margin}, {margin})">
    <!-- Pyramid outline -->
    <path d="M 0 {size*scale} L {size*scale/2} 0 L {size*scale} {size*scale} Z"
          fill="none" stroke="black" stroke-width="2"/>

    <!-- Base line -->
    <line x1="0" y1="{size*scale}" x2="{size*scale}" y2="{size*scale}"
          stroke="black" stroke-width="2"/>

    <!-- Dimensions -->
    <!-- Base width -->
    <line x1="0" y1="{size*scale + 20}" x2="{size*scale}" y2="{size*scale + 20}"
          stroke="red" stroke-width="1"/>
    <line x1="0" y1="{size*scale + 15}" x2="0" y2="{size*scale + 25}"
          stroke="red" stroke-width="1"/>
    <line x1="{size*scale}" y1="{size*scale + 15}" x2="{size*scale}" y2="{size*scale + 25}"
          stroke="red" stroke-width="1"/>
    <text x="{size*scale/2}" y="{size*scale + 35}" font-family="Arial" font-size="12"
          fill="red" text-anchor="middle">{size:.1f} m</text>

    <!-- Height -->
    <line x1="{size*scale + 20}" y1="0" x2="{size*scale + 20}" y2="{size*scale}"
          stroke="blue" stroke-width="1"/>
    <line x1="{size*scale + 15}" y1="0" x2="{size*scale + 25}" y2="0"
          stroke="blue" stroke-width="1"/>
    <line x1="{size*scale + 15}" y1="{size*scale}" x2="{size*scale + 25}" y2="{size*scale}"
          stroke="blue" stroke-width="1"/>
    <text x="{size*scale + 40}" y="{size*scale/2}" font-family="Arial" font-size="12"
          fill="blue" text-anchor="middle" transform="rotate(-90, {size*scale + 40}, {size*scale/2})">{pyramid_height:.1f} m</text>

    <!-- Suspension lines -->
    <line x1="{size*scale/2}" y1="0" x2="{size*scale/2}" y2="{size*scale + 60}"
          stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>

    <!-- Payload -->
    <circle cx="{size*scale/2}" cy="{size*scale + 60}" r="10"
            fill="gray" stroke="black" stroke-width="1"/>
    <text x="{size*scale/2}" y="{size*scale + 80}" font-family="Arial" font-size="10"
          text-anchor="middle">Payload</text>
  </g>

  <!-- Specifications box -->
  <rect x="{width - 250}" y="{height - 150}" width="230" height="130"
        fill="white" stroke="black" stroke-width="1"/>
  <text x="{width - 240}" y="{height - 130}" font-family="Arial" font-size="12" font-weight="bold">
    Specifications:
  </text>
  <text x="{width - 240}" y="{height - 110}" font-family="Arial" font-size="10">
    Base: {size:.1f} m × {size:.1f} m
  </text>
  <text x="{width - 240}" y="{height - 95}" font-family="Arial" font-size="10">
    Height: {pyramid_height:.1f} m
  </text>
  <text x="{width - 240}" y="{height - 80}" font-family="Arial" font-size="10">
    Canopy Area: {2*size*math.sqrt((size/2)**2 + pyramid_height**2):.1f} m²
  </text>
  <text x="{width - 240}" y="{height - 65}" font-family="Arial" font-size="10">
    Material: Ripstop Nylon
  </text>
  <text x="{width - 240}" y="{height - 50}" font-family="Arial" font-size="10">
    Frame: Carbon Fiber
  </text>
  <text x="{width - 240}" y="{height - 35}" font-family="Arial" font-size="10">
    Scale: 1:{int(1000/scale)} (drawing)
  </text>
</svg>"""

    with open(output_path, "w") as f:
        f.write(svg_content)


def export_mesh(output_path: Path) -> None:
    """Export mesh for compatibility with existing code.

    Args:
        output_path: Path for mesh file
    """
    # Default size from main module
    size = 7.0  # meters
    generate_stl_mesh(size, output_path)
