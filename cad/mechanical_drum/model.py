"""Parametric CAD generator for Leonardo's mechanical drum."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import trimesh

DEFAULT_PIN_HEIGHT = 0.05
DEFAULT_PIN_RADIUS = 0.009
SUPPORT_SIZE = (0.05, 0.2, 0.12)


def _drum(radius: float, length: float, segments: int = 64) -> trimesh.Trimesh:
    return trimesh.creation.cylinder(radius=radius, height=length, sections=segments)


def _pin(radius: float, height: float) -> trimesh.Trimesh:
    return trimesh.creation.cylinder(radius=radius, height=height, sections=32)


def _supports(spacing: float, width: float, height: float) -> Iterable[trimesh.Trimesh]:
    support = trimesh.creation.box(extents=SUPPORT_SIZE)
    offsets = (
        (spacing / 2, 0.0, -SUPPORT_SIZE[2] / 2),
        (-spacing / 2, 0.0, -SUPPORT_SIZE[2] / 2),
    )
    for ox, oy, oz in offsets:
        s = support.copy()
        s.apply_translation((ox, oy, oz))
        yield s


def generate_drum(params: Dict[str, object]) -> trimesh.Trimesh:
    drum_radius = float(params.get("drum_radius_m", 0.15))
    drum_length = float(params.get("drum_length_m", 0.3))
    beat_angles = params.get("beat_angles_deg", [0, 90, 180, 270])
    pin_radius = float(params.get("pin_radius_m", DEFAULT_PIN_RADIUS))
    pin_height = float(params.get("pin_height_m", DEFAULT_PIN_HEIGHT))

    drum = _drum(drum_radius, drum_length)
    drum.apply_translation((0.0, 0.0, -drum_length / 2))

    pins = []
    for idx, angle in enumerate(beat_angles):
        axial_offset = (-drum_length / 2) + (idx / max(len(beat_angles), 1)) * drum_length
        pin = _pin(pin_radius, pin_height)
        pin.apply_translation((0.0, 0.0, pin_height / 2))
        pin.apply_translation((drum_radius, 0.0, axial_offset + drum_length / 2))
        pin.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(angle), (0, 0, 1)))
        pins.append(pin)

    frame = trimesh.creation.box(extents=(0.4, 0.4, 0.1))
    frame.apply_translation((0, 0, -drum_length / 2 - 0.05))

    supports = list(_supports(spacing=drum_length * 0.6, width=SUPPORT_SIZE[0], height=SUPPORT_SIZE[2]))

    assembly = trimesh.util.concatenate([drum, frame] + pins + supports)
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path, params: Dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_drum(params)
    mesh.export(path)
    return path


if __name__ == "__main__":
    # Sample params for testing
    sample_params = {
        "drum_radius_m": 0.15,
        "drum_length_m": 0.35,
        "beat_angles_deg": [0, 90, 180, 270],
        "pin_radius_m": 0.009,
        "pin_height_m": 0.05,
    }
    export_mesh(Path("../../artifacts/mechanical_drum/cad/mechanical_drum.stl"), sample_params)
