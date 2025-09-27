"""Parametric CAD for Leonardo's programmable flute."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import trimesh


def _flute_body(length: float, diameter: float) -> trimesh.Trimesh:
    body = trimesh.creation.cylinder(radius=diameter / 2.0, height=length, sections=64)
    body.apply_translation((0.0, 0.0, length / 2.0))
    body.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [0, 1, 0]))
    return body


def _cam_barrel(radius: float, length: float) -> trimesh.Trimesh:
    barrel = trimesh.creation.cylinder(radius=radius, height=length, sections=64)
    barrel.apply_translation((0.0, -length / 2.0 - radius, radius))
    return barrel


def _stand(width: float, depth: float, height: float) -> trimesh.Trimesh:
    stand = trimesh.creation.box(extents=(width, depth, height))
    stand.apply_translation((0.0, 0.0, height / 2.0))
    return stand


def _finger_hole(position: float, radius: float) -> trimesh.Trimesh:
    hole = trimesh.creation.cylinder(radius=radius, height=0.02, sections=32)
    hole.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [1, 0, 0]))
    hole.apply_translation((position, 0.0, radius))
    return hole


def generate_flute(params: Dict[str, object]) -> trimesh.Trimesh:
    pipe_lengths = np.asarray(params.get("pipe_lengths_m", [0.4, 0.36, 0.32]), dtype=float)
    body_length = float(pipe_lengths.max() if pipe_lengths.size else 0.4)
    body_diameter = 0.035
    barrel_radius = 0.05
    barrel_length = body_length * 0.6

    body = _flute_body(body_length, body_diameter)
    cam_barrel = _cam_barrel(barrel_radius, barrel_length)
    cam_barrel.apply_translation((0.0, 0.0, 0.1))

    stand = _stand(body_length + 0.2, 0.1, 0.04)
    stand.apply_translation((0.0, 0.0, 0.02))

    holes = []
    hole_positions = np.asarray(params.get("hole_positions_m", [0.08, 0.12, 0.16, 0.2, 0.24]), dtype=float)
    for position in hole_positions:
        hole = _finger_hole(position - body_length / 2.0, body_diameter / 4.0)
        holes.append(hole)

    assembly = trimesh.util.concatenate([body, cam_barrel, stand] + holes)
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path, params: Dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_flute(params)
    mesh.export(path)
    return path


if __name__ == "__main__":
    SAMPLE = {
        "pipe_lengths_m": [0.4, 0.35, 0.3],
        "hole_positions_m": [0.08, 0.12, 0.16, 0.2, 0.24],
    }
    export_mesh(Path("../../artifacts/programmable_flute/cad/programmable_flute.stl"), SAMPLE)
