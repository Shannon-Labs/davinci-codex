"""Parametric CAD generator for Leonardo's automatic pipe organ."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import trimesh


def _base(width: float, depth: float, thickness: float) -> trimesh.Trimesh:
    plate = trimesh.creation.box(extents=(width, depth, thickness))
    plate.apply_translation((0.0, 0.0, thickness / 2.0))
    return plate


def _wind_chest(width: float, depth: float, height: float) -> trimesh.Trimesh:
    chest = trimesh.creation.box(extents=(width, depth, height))
    chest.apply_translation((0.0, 0.0, height / 2.0))
    return chest


def _pipe(length: float, diameter: float, x_offset: float, y_offset: float = 0.0) -> trimesh.Trimesh:
    pipe = trimesh.creation.cylinder(radius=diameter / 2.0, height=length, sections=48)
    pipe.apply_translation((x_offset, y_offset, length / 2.0))
    return pipe


def _barrel(radius: float, length: float) -> trimesh.Trimesh:
    barrel = trimesh.creation.cylinder(radius=radius, height=length, sections=64)
    barrel.apply_translation((0.0, -length / 2.0 - radius, radius))
    return barrel


def _supports(barrel_radius: float, depth: float) -> Iterable[trimesh.Trimesh]:
    upright = trimesh.creation.box(extents=(0.04, 0.04, barrel_radius * 2.0))
    offsets = (-0.18, 0.18)
    for x in offsets:
        support = upright.copy()
        support.apply_translation((x, -depth / 2.0 - 0.05, barrel_radius))
        yield support


def generate_organ(params: Dict[str, object]) -> trimesh.Trimesh:
    pipe_lengths = np.asarray(params.get("pipe_lengths_m", [0.45, 0.4, 0.35, 0.3]), dtype=float)
    pipe_diameters = np.asarray(params.get("pipe_diameters_m", [0.06, 0.055, 0.05, 0.045]), dtype=float)
    if pipe_diameters.size != pipe_lengths.size:
        pipe_diameters = np.full_like(pipe_lengths, pipe_diameters.mean() if pipe_diameters.size else 0.05)
    count = int(pipe_lengths.size)
    width = max(0.3, 0.08 * count)
    depth = 0.25
    base_thickness = 0.03
    chest_height = 0.14

    base = _base(width, depth, base_thickness)
    chest = _wind_chest(width * 0.95, depth * 0.8, chest_height)
    chest.apply_translation((0.0, 0.0, base_thickness))

    pipes = []
    spacing = width / max(count, 1)
    x_start = -width / 2.0 + spacing / 2.0
    for idx in range(count):
        length = float(pipe_lengths[idx])
        diameter = float(pipe_diameters[idx])
        x_offset = x_start + idx * spacing
        pipe = _pipe(length, diameter, x_offset)
        pipe.apply_translation((0.0, 0.0, chest_height + base_thickness))
        pipes.append(pipe)

    barrel = _barrel(radius=0.06, length=width * 0.8)
    barrel.apply_translation((0.0, 0.0, base_thickness + chest_height * 0.4))

    supports = list(_supports(barrel_radius=0.06, depth=depth))

    assembly = trimesh.util.concatenate([base, chest, barrel] + pipes + supports)
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path, params: Dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_organ(params)
    mesh.export(path)
    return path


if __name__ == "__main__":
    SAMPLE = {
        "pipe_lengths_m": [0.45, 0.4, 0.36, 0.32],
        "pipe_diameters_m": [0.06, 0.055, 0.05, 0.045],
    }
    export_mesh(Path("../../artifacts/mechanical_organ/cad/mechanical_organ.stl"), SAMPLE)
