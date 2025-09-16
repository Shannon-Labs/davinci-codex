"""Parametric CAD scaffolding for the ornithopter."""

from __future__ import annotations

import csv
from pathlib import Path


def generate_ornithopter_frame(span_m: float, chord_m: float, output_dir: Path) -> None:
    """Emit OpenSCAD source plus a lightweight BOM for the ornithopter frame."""
    output_dir.mkdir(parents=True, exist_ok=True)
    span_mm = span_m * 1000.0
    chord_mm = chord_m * 1000.0
    fuselage_length_mm = 3600.0
    wing_spar_diameter_mm = 45.0
    rib_count = 18
    motor_mount_length_mm = 240.0
    gearbox_offset_mm = 320.0

    scad = f"""
// Ornithopter frame (generated {span_m:.2f}m span)
span = {span_mm:.1f};
chord = {chord_mm:.1f};
fuselage_length = {fuselage_length_mm:.1f};
wing_spar_diameter = {wing_spar_diameter_mm:.1f};
rib_count = {rib_count};
motor_mount_length = {motor_mount_length_mm:.1f};
gearbox_offset = {gearbox_offset_mm:.1f};

module wing_rib(rib_index) {{
    offset_factor = sin($pi * rib_index / rib_count) * 0.08;
    translate([0, 0, (rib_index/rib_count) * span/2])
        color([0.8, 0.8, 0.8], 0.4)
        linear_extrude(height = 6)
        offset(r = offset_factor * chord)
            circle(d = chord * (0.92 - 0.05 * (rib_index/rib_count)));
}}

module wing_half() {{
    color([0.1, 0.1, 0.1], 0.9)
    cylinder(h = span/2, d = wing_spar_diameter);
    for (i = [0:rib_count]) {{
        wing_rib(i);
    }}
    // leading edge spar
    translate([chord*0.45, 0, 0])
        color([0.1, 0.1, 0.1], 0.7)
        cylinder(h = span/2, d = 28);
    // trailing edge carbon strip
    translate([-chord*0.35, 0, 0])
        color([0.12, 0.12, 0.12], 0.6)
        cube([chord*0.05, 12, span/2], center = true);
}}

module fuselage() {{
    color([0.45, 0.45, 0.45], 0.85)
    hull() {{
        translate([-chord/3, -chord/4, 0])
            cube([chord*0.65, chord*0.5, wing_spar_diameter*1.2], center = false);
        translate([-chord/4, -chord/8, -fuselage_length/2])
            cube([chord*0.55, chord*0.42, fuselage_length], center = false);
    }}
}}

module drivetrain() {{
    color([0.75, 0.75, 0.75], 0.9)
    translate([0, 0, gearbox_offset])
        cube([chord*0.22, chord*0.22, motor_mount_length], center = true);
    // placeholder gears
    for (side = [-1, 1]) {{
        translate([side * chord*0.12, 0, gearbox_offset + motor_mount_length/2])
            color([0.6, 0.6, 0.6], 0.8)
            cylinder(h = 40, d = chord*0.18, center = true, $fn=48);
    }}
}}

module tailplane() {{
    color([0.2, 0.2, 0.6], 0.6)
    translate([-chord/2, -chord/3, -fuselage_length])
        cube([chord*1.1, chord*0.65, chord*0.06]);
    translate([-chord/2, 0, -fuselage_length - chord*0.3])
        color([0.2, 0.2, 0.6], 0.6)
        cube([chord*0.3, chord*0.65, chord*0.02]);
}}

module motor_mounts() {{
    for (side = [-1, 1]) {{
        translate([side * chord*0.18, 0, gearbox_offset + motor_mount_length/2])
            color([0.8, 0.5, 0.2], 0.9)
            cube([chord*0.11, chord*0.08, motor_mount_length], center = true);
    }}
}}

module ornithopter() {{
    translate([0, 0, -wing_spar_diameter/2])
        fuselage();
    drivetrain();
    motor_mounts();
    rotate([90, 0, 0]) {{
        wing_half();
        mirror([0, 0, 1]) wing_half();
    }}
    tailplane();
}}

ornithopter();
"""

    scad_path = output_dir / "ornithopter_frame.scad"
    scad_path.write_text(scad, encoding="utf-8")

    bom_path = output_dir / "bill_of_materials.csv"
    with bom_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["component", "material", "quantity", "notes"])
        writer.writerow(["Wing spar", "Carbon fiber tube", 2, f"{span_m/2:.2f} m each, {wing_spar_diameter_mm} mm OD"])
        writer.writerow(["Leading edge spar", "Carbon rod", 2, f"{span_m/2:.2f} m each, 28 mm OD"])
        writer.writerow(["Wing ribs", "CFRP laminate", rib_count * 2, f"Chord {chord_m:.2f} m varying camber"])
        writer.writerow(["Fuselage boom", "Carbon fiber box", 1, f"Length {fuselage_length_mm/1000:.2f} m"])
        writer.writerow(["Tailplane", "Kevlar sandwich", 1, "Bolt-on with differential elevator"])
        writer.writerow(["Motor mount", "7075-T6 aluminum", 2, "Supports 2 kW outrunner motors"])
        writer.writerow(["Gear pair", "Harmonic reducer", 2, "Placeholder for drivetrain"])

    assembly_manifest = output_dir / "assembly.json"
    assembly_manifest.write_text(
        (
            '{"root":"ornithopter",'
            '"subassemblies":[{"name":"left_wing","components":["wing_spar_left","leading_edge_left","ribs_left"]},'
            '{"name":"right_wing","components":["wing_spar_right","leading_edge_right","ribs_right"]},'
            '{"name":"powertrain","components":["gearbox","motor_mount_left","motor_mount_right"]},'
            '{"name":"tail","components":["tailplane","elevator"]}]}'
        ),
        encoding="utf-8",
    )

    mass_report = output_dir / "mass_budget.txt"
    estimated_structure_mass = 0.26 * span_m * chord_m * 100.0  # updated scaling estimate
    motor_mass = 2 * 4.2  # kg per motor
    gearbox_mass = 6.5
    tail_mass = 3.1
    total_mass = estimated_structure_mass + motor_mass + gearbox_mass + tail_mass
    mass_report.write_text(
        (
            "Ornithopter structural mass estimate\n"
            f"Span: {span_m:.2f} m\n"
            f"Chord: {chord_m:.2f} m\n"
            f"Estimated structure mass: {estimated_structure_mass:.2f} kg\n"
            f"Motor mass (2x): {motor_mass:.2f} kg\n"
            f"Gearbox mass: {gearbox_mass:.2f} kg\n"
            f"Tail assembly mass: {tail_mass:.2f} kg\n"
            f"Total estimated mass: {total_mass:.2f} kg\n"
            "Assumes carbon sandwich skins with foam core ribs."
        ),
        encoding="utf-8",
    )
