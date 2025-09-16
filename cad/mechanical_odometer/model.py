"""Parametric CAD generator for Leonardo's odometer cart."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import trimesh


def _wheel(radius: float, width: float, segments: int = 64) -> trimesh.Trimesh:
    rim = trimesh.creation.cylinder(radius=radius, height=width, sections=segments)
    hub = trimesh.creation.cylinder(radius=radius * 0.3, height=width * 1.3, sections=segments)
    rim = rim.difference(hub)
    spokes = []
    for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        box = trimesh.creation.box(extents=(radius * 0.15, width * 0.9, width * 0.35))
        box.apply_translation((radius * 0.5, 0.0, 0.0))
        box.apply_transform(trimesh.transformations.rotation_matrix(angle, (0, 0, 1)))
        spokes.append(box)
    wheel = trimesh.util.concatenate([rim, hub] + spokes)
    wheel.merge_vertices()
    return wheel


def generate_odometer() -> trimesh.Trimesh:
    wheel_radius = 0.22
    wheel_width = 0.05
    track = 0.65
    wheelbase = 0.8

    frame = trimesh.creation.box(extents=(wheelbase, track, 0.08))
    frame.apply_translation((0.0, 0.0, wheel_radius + 0.04))

    wheels = []
    offsets: Tuple[Tuple[float, float], ...] = (
        (wheelbase / 2, track / 2),
        (-wheelbase / 2, track / 2),
        (wheelbase / 2, -track / 2),
        (-wheelbase / 2, -track / 2),
    )
    for ox, oy in offsets:
        wheel = _wheel(wheel_radius, wheel_width)
        wheel.apply_translation((ox, oy, wheel_radius))
        wheels.append(wheel)

    gear_housing = trimesh.creation.box(extents=(0.3, 0.3, 0.25))
    gear_housing.apply_translation((wheelbase * 0.3, 0.0, wheel_radius + 0.18))

    pebble_drum = trimesh.creation.cylinder(radius=0.12, height=0.16, sections=96)
    pebble_drum.apply_translation((wheelbase * 0.3, 0.0, wheel_radius + 0.35))

    assembly = trimesh.util.concatenate([frame, gear_housing, pebble_drum] + wheels)
    assembly.remove_duplicate_faces()
    assembly.remove_degenerate_faces()
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_odometer()
    mesh.export(path)
    return path


if __name__ == "__main__":
    export_mesh(Path("../../artifacts/mechanical_odometer/cad/mechanical_odometer.stl"))
