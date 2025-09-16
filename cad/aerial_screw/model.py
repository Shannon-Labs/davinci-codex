"""Parametric mesh generator for the aerial screw rotor."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import trimesh


def _blade_vertices(
    *,
    radius_outer: float,
    radius_inner: float,
    pitch: float,
    turns: float,
    thickness: float,
    steps: int,
) -> Tuple[np.ndarray, np.ndarray]:
    theta = np.linspace(0.0, 2.0 * np.pi * turns, steps)
    z = pitch * theta / (2.0 * np.pi)
    vertices = []
    for angle, height in zip(theta, z):
        cos_v = float(np.cos(angle))
        sin_v = float(np.sin(angle))
        for inner in (radius_inner, radius_outer):
            for offset in (-thickness / 2.0, thickness / 2.0):
                x = inner * cos_v
                y = inner * sin_v
                vertices.append((x, y, height + offset))
    vertices_np = np.array(vertices, dtype=float)
    faces = []
    for i in range(steps - 1):
        base = 4 * i
        nxt = base + 4
        # bottom surface
        faces.append((base + 0, base + 1, nxt + 1))
        faces.append((base + 0, nxt + 1, nxt + 0))
        # top surface
        faces.append((base + 2, nxt + 3, base + 3))
        faces.append((base + 2, nxt + 2, nxt + 3))
        # inner wall
        faces.append((base + 0, nxt + 0, nxt + 2))
        faces.append((base + 0, nxt + 2, base + 2))
        # outer wall
        faces.append((base + 1, base + 3, nxt + 3))
        faces.append((base + 1, nxt + 3, nxt + 1))
    return vertices_np, np.array(faces, dtype=np.int64)


def generate_mesh() -> trimesh.Trimesh:
    """Generate the aerial screw rotor mesh as a solid ribbon and mast."""
    blade_vertices, blade_faces = _blade_vertices(
        radius_outer=2.0,
        radius_inner=1.6,
        pitch=3.5,
        turns=2.5,
        thickness=0.06,
        steps=220,
    )
    blade_mesh = trimesh.Trimesh(vertices=blade_vertices, faces=blade_faces, process=True)
    mast_height = blade_vertices[:, 2].max() + 0.5
    mast = trimesh.creation.cylinder(radius=0.18, height=mast_height, sections=96)
    mast.apply_translation((0.0, 0.0, mast_height / 2.0))
    assembly = trimesh.util.concatenate([blade_mesh, mast])
    assembly.remove_duplicate_faces()
    assembly.remove_degenerate_faces()
    assembly.merge_vertices()
    return assembly


def export_mesh(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    mesh = generate_mesh()
    mesh.export(path)
    return path


if __name__ == "__main__":
    export_mesh(Path("../../artifacts/aerial_screw/cad/aerial_screw_mesh.stl"))
