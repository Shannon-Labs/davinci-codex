"""Parametric CAD generator for the self-propelled cart prototype."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import trimesh


def _wheel(radius: float, width: float, segments: int = 64) -> trimesh.Trimesh:
    # annulus avoids boolean backends while providing visual accuracy
    wheel = trimesh.creation.annulus(r_min=radius * 0.35, r_max=radius, height=width, sections=segments)
    spoke_count = 6
    spokes = []
    for idx in range(spoke_count):
        angle = 2.0 * np.pi * idx / spoke_count
        box = trimesh.creation.box(extents=(width * 0.9, radius * 0.15, width * 0.4))
        box.apply_translation((0.0, radius * 0.5, 0.0))
        box.apply_transform(trimesh.transformations.rotation_matrix(angle, (0, 0, 1)))
        spokes.append(box)
    wheel = trimesh.util.concatenate([wheel] + spokes)
    wheel.merge_vertices()
    return wheel


def generate_cart() -> trimesh.Trimesh:
    """Generate chassis, wheels, and spring drum as a watertight mesh."""
    wheel_radius = 0.18
    wheel_width = 0.04
    track = 0.65
    wheelbase = 0.85
    chassis = trimesh.creation.box(extents=(wheelbase, track, 0.06))
    chassis.apply_translation((0.0, 0.0, wheel_radius + 0.04))

    wheels = []
    offsets: Tuple[Tuple[float, float], ...] = (
        (wheelbase / 2.0, track / 2.0),
        (-wheelbase / 2.0, track / 2.0),
        (wheelbase / 2.0, -track / 2.0),
        (-wheelbase / 2.0, -track / 2.0),
    )
    for ox, oy in offsets:
        wheel = _wheel(wheel_radius, wheel_width)
        wheel.apply_translation((ox, oy, wheel_radius))
        wheels.append(wheel)

    drum = trimesh.creation.cylinder(radius=0.12, height=0.18, sections=96)
    drum.apply_translation((0.0, 0.0, wheel_radius + 0.09))
    drum_spindle = trimesh.creation.cylinder(radius=0.05, height=0.24, sections=48)
    drum_spindle.apply_translation((0.0, 0.0, wheel_radius + 0.09))

    assembly = trimesh.util.concatenate([chassis, drum, drum_spindle] + wheels)
    assembly.remove_duplicate_faces()
    assembly.remove_degenerate_faces()
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_cart()
    mesh.export(path)
    return path


if __name__ == "__main__":
    export_mesh(Path("../../artifacts/self_propelled_cart/cad/self_propelled_cart.stl"))
