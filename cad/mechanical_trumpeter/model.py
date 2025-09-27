"""Parametric CAD for Leonardo's mechanical trumpeter."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import trimesh


def _tube(length: float, radius: float) -> trimesh.Trimesh:
    tube = trimesh.creation.cylinder(radius=radius, height=length, sections=64)
    tube.apply_translation((0.0, 0.0, length / 2.0))
    tube.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [0, 1, 0]))
    return tube


def _bell(length: float, radius: float) -> trimesh.Trimesh:
    bell = trimesh.creation.cone(radius=radius, height=length, sections=64)
    bell.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [0, 1, 0]))
    bell.apply_translation((length, 0.0, 0.0))
    return bell


def _valve_cluster(spacing: float, radius: float) -> trimesh.Trimesh:
    bodies = []
    for idx in range(3):
        valve = trimesh.creation.cylinder(radius=radius, height=0.07, sections=48)
        valve.apply_translation((spacing * idx, 0.02, radius))
        bodies.append(valve)
    return trimesh.util.concatenate(bodies)


def generate_trumpeter(params: Dict[str, object]) -> trimesh.Trimesh:
    bore_length = float(params.get("bore_length_m", 1.4))
    mouthpiece_length = float(params.get("mouthpiece_length_m", 0.12))
    bell_diameter = float(params.get("bell_diameter_m", 0.12))
    tube_radius = 0.008

    leadpipe = _tube(mouthpiece_length, tube_radius * 1.2)
    leadpipe.apply_translation((0.0, 0.0, 0.05))

    main_tube = _tube(bore_length, tube_radius)
    main_tube.apply_translation((mouthpiece_length, 0.0, 0.05))

    bell = _bell(0.18, bell_diameter / 2.0)
    bell.apply_translation((mouthpiece_length + bore_length, 0.0, 0.05))

    valves = _valve_cluster(0.05, 0.015)
    valves.apply_translation((mouthpiece_length + 0.25, -0.03, 0.08))

    brace = trimesh.creation.box(extents=(0.15, 0.015, 0.01))
    brace.apply_translation((mouthpiece_length + 0.2, -0.04, 0.05))

    assembly = trimesh.util.concatenate([leadpipe, main_tube, bell, valves, brace])
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path, params: Dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_trumpeter(params)
    mesh.export(path)
    return path


if __name__ == "__main__":
    SAMPLE = {
        "bore_length_m": 1.35,
        "bell_diameter_m": 0.13,
    }
    export_mesh(Path("../../artifacts/mechanical_trumpeter/cad/mechanical_trumpeter.stl"), SAMPLE)
