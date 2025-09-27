"""Parametric CAD model for Leonardo's viola organista."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import trimesh


def _base(width: float, depth: float, thickness: float) -> trimesh.Trimesh:
    plate = trimesh.creation.box(extents=(width, depth, thickness))
    plate.apply_translation((0.0, 0.0, thickness / 2.0))
    return plate


def _wheel(radius: float, width: float) -> trimesh.Trimesh:
    wheel = trimesh.creation.cylinder(radius=radius, height=width, sections=64)
    wheel.apply_translation((0.0, 0.0, radius))
    wheel.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [0, 1, 0]))
    return wheel


def _string(length: float, height: float, index: int, count: int) -> trimesh.Trimesh:
    spacing = 0.04
    offset = (index - (count - 1) / 2) * spacing
    bar = trimesh.creation.box(extents=(length, 0.005, 0.003))
    bar.apply_translation((length / 2.0, offset, height))
    return bar


def generate_viola(params: Dict[str, object]) -> trimesh.Trimesh:
    string_lengths = np.asarray(params.get("string_lengths_m", [0.6, 0.58, 0.55]), dtype=float)
    count = int(string_lengths.size)
    deck_width = max(0.5, string_lengths.max() + 0.2)
    deck_depth = 0.3
    deck_thickness = 0.04

    base = _base(deck_width, deck_depth, deck_thickness)

    wheel_radius = 0.1
    wheel_width = 0.2
    wheel = _wheel(wheel_radius, wheel_width)
    wheel.apply_translation((deck_width * 0.15, 0.0, wheel_radius + deck_thickness))

    strings = []
    for idx, length in enumerate(string_lengths):
        string = _string(length, deck_thickness + 0.08, idx, count)
        string.apply_translation((deck_width * 0.3, 0.0, 0.0))
        strings.append(string)

    keybed = trimesh.creation.box(extents=(0.35, deck_depth * 0.9, 0.05))
    keybed.apply_translation((deck_width * 0.65, 0.0, 0.05))

    assembly = trimesh.util.concatenate([base, wheel, keybed] + strings)
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path, params: Dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_viola(params)
    mesh.export(path)
    return path


if __name__ == "__main__":
    SAMPLE = {
        "string_lengths_m": [0.6, 0.58, 0.55, 0.52],
    }
    export_mesh(Path("../../artifacts/viola_organista/cad/viola_organista.stl"), SAMPLE)
