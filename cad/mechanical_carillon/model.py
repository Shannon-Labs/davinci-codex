"""Parametric CAD model for Leonardo's mechanical carillon."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import trimesh


def _drum(radius: float, length: float) -> trimesh.Trimesh:
    cyl = trimesh.creation.cylinder(radius=radius, height=length, sections=64)
    cyl.apply_translation((0.0, 0.0, length / 2.0))
    return cyl


def _bell(diameter: float, height: float, offset: float) -> trimesh.Trimesh:
    bell = trimesh.creation.cone(radius=diameter / 2.0, height=height, sections=48)
    bell.apply_translation((offset, 0.0, height / 2.0))
    return bell


def _frame(width: float, depth: float, height: float) -> Iterable[trimesh.Trimesh]:
    leg = trimesh.creation.box(extents=(0.04, depth, height))
    offsets = (-width / 2.0, width / 2.0)
    for x in offsets:
        part = leg.copy()
        part.apply_translation((x, 0.0, height / 2.0))
        yield part


def _hammer(length: float, thickness: float, offset: float) -> trimesh.Trimesh:
    bar = trimesh.creation.box(extents=(length, thickness, thickness))
    bar.apply_translation((offset, 0.0, thickness / 2.0))
    return bar


def generate_carillon(params: Dict[str, object]) -> trimesh.Trimesh:
    bell_masses = np.asarray(params.get("bell_masses_kg", [12.0, 10.0, 8.0, 6.0]), dtype=float)
    bell_count = int(bell_masses.size)
    drum_radius = float(params.get("drum_radius_m", 0.25))
    drum_length = max(0.3, 0.12 * bell_count)
    frame_depth = 0.25
    frame_height = 0.5

    drum = _drum(drum_radius, drum_length)
    drum.apply_translation((0.0, -frame_depth / 2.0 - drum_radius, frame_height * 0.65))

    bells = []
    spacing = max(0.12, drum_length / max(bell_count, 1))
    x_start = -drum_length / 2.0 + spacing / 2.0
    for idx in range(bell_count):
        diameter = 0.16 + 0.01 * (bell_count - idx)
        height = 0.18 + 0.02 * (bell_count - idx)
        bell = _bell(diameter, height, x_start + idx * spacing)
        bell.apply_translation((0.0, 0.08, frame_height * 0.4))
        bells.append(bell)

    hammers = []
    for idx in range(bell_count):
        hammer = _hammer(length=0.18, thickness=0.02, offset=x_start + idx * spacing)
        hammer.apply_translation((0.0, -frame_depth / 2.0 - drum_radius + 0.02, frame_height * 0.6))
        hammers.append(hammer)

    frame = list(_frame(drum_length + 0.2, frame_depth, frame_height))
    base = trimesh.creation.box(extents=(drum_length + 0.25, frame_depth, 0.05))
    base.apply_translation((0.0, 0.0, 0.025))

    assembly = trimesh.util.concatenate(frame + [base, drum] + bells + hammers)
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path, params: Dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_carillon(params)
    mesh.export(path)
    return path


if __name__ == "__main__":
    SAMPLE = {
        "bell_masses_kg": [12.0, 9.5, 7.0, 5.0],
        "drum_radius_m": 0.22,
    }
    export_mesh(Path("../../artifacts/mechanical_carillon/cad/mechanical_carillon.stl"), SAMPLE)
