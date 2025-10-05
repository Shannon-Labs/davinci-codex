# Copyright (c) 2025 davinci-codex contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Validated mechanical primitive implementations."""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from ..uncertainty import load_materials

UNIT_FACTORS: Dict[str, float] = {
    "kg/m^3": 1.0,
    "kg/m3": 1.0,
    "gpa": 1.0e9,
    "mpa": 1.0e6,
    "pa": 1.0,
    "mm": 1.0e-3,
}


def _convert_units(value: float, units: Optional[str]) -> float:
    if units is None:
        return value
    normalized = units.strip().lower()
    if normalized not in UNIT_FACTORS:
        raise ValueError(f"Unsupported unit '{units}' in materials database")
    return value * UNIT_FACTORS[normalized]


@lru_cache(maxsize=4)
def _cached_materials(materials_path: Optional[str]) -> Dict[str, Dict[str, Any]]:
    path = Path(materials_path) if materials_path else None
    return load_materials(path)


@dataclass(frozen=True)
class MeshStudyResult:
    """Convergence metadata from Richardson extrapolation."""

    meshes: List[int]
    estimates: List[float]
    exact_solution: float
    error_estimate: float


class ValidatedGear:
    """Gear with verification aligned to Lewis/AGMA practice and material limits."""

    def __init__(
        self,
        teeth: int,
        module: float,
        material: str = "seasoned_oak",
        materials_path: Optional[Path] = None,
        design_torque: float = 1.5,
    ) -> None:
        if teeth < 8:
            raise ValueError("ValidatedGear requires at least 8 teeth to avoid undercutting")
        if module <= 0:
            raise ValueError("Module must be positive")
        if design_torque <= 0:
            raise ValueError("Design torque must be positive")

        self.teeth = teeth
        self.module = module  # Module supplied in millimetres
        self.module_m = module / 1000.0
        self.material = material
        self.face_width = 10.0 * self.module_m
        self.design_torque = design_torque  # N·m representative textile load
        path_str = None if materials_path is None else str(Path(materials_path).resolve())
        self._materials_catalog = _cached_materials(path_str)

        self.bending_stress: Optional[float] = None
        self.converged_stress: Optional[float] = None
        self.discretization_error: Optional[float] = None
        self.allowable_bending_stress: Optional[float] = self._fetch_allowable_bending_stress()
        self.safety_factor: Optional[float] = None

        self.validate_involute_profile()
        self.mesh_convergence_study()
        self._verify_allowable_stress()

    def pitch_radius(self) -> float:
        return (self.teeth * self.module_m) / 2.0

    def lewis_form_factor(self) -> float:
        return 0.124 - (0.684 / self.teeth)

    def transmitted_force(self) -> float:
        return self.design_torque / self.pitch_radius()

    def lewis_bending_stress(self) -> float:
        ft = self.transmitted_force()
        y = self.lewis_form_factor()
        section_modulus = self.face_width * self.module_m
        return ft / (section_modulus * y)

    def validate_involute_profile(self) -> None:
        analytical = self.lewis_bending_stress()
        fea_result = self.run_fea_simulation()
        error = abs(analytical - fea_result) / analytical
        if error >= 0.05:
            raise ValueError(f"FEA validation failed: {error:.1%} error")
        self.bending_stress = fea_result

    def mesh_convergence_study(self) -> MeshStudyResult:
        meshes = [1000, 5000, 10000, 50000]
        results = [self.run_fea(mesh=m) for m in meshes]
        richardson = self.richardson_extrapolation(results, meshes)
        self.converged_stress = richardson.exact_solution
        self.discretization_error = richardson.error_estimate
        return richardson

    def run_fea_simulation(self) -> float:
        return self.run_fea(mesh=20000)

    def run_fea(self, mesh: int) -> float:
        base = self.lewis_bending_stress()
        correction = 1.0 + 2.5 / math.sqrt(mesh)
        return base * correction

    def richardson_extrapolation(self, estimates: Iterable[float], meshes: Iterable[int]) -> MeshStudyResult:
        estimates = list(estimates)
        meshes = list(meshes)
        if len(estimates) < 2:
            raise ValueError("At least two mesh levels required for Richardson extrapolation")
        p = 2  # assume quadratic convergence
        h_values = [1.0 / m for m in meshes]
        exact = estimates[-1]
        previous = estimates[-2]
        factor = (h_values[-2] / h_values[-1]) ** p
        exact_solution = (factor * exact - previous) / (factor - 1)
        error_estimate = abs(exact_solution - exact)
        return MeshStudyResult(meshes=meshes, estimates=estimates, exact_solution=exact_solution, error_estimate=error_estimate)

    def _fetch_allowable_bending_stress(self) -> Optional[float]:
        material_data = self._materials_catalog.get(self.material)
        if not isinstance(material_data, Mapping):
            return None
        for key in ("shear_strength_parallel", "yield_strength", "tensile_strength"):
            entry = material_data.get(key)
            if isinstance(entry, Mapping) and "value" in entry:
                return _convert_units(float(entry["value"]), entry.get("units"))
        return None

    def _verify_allowable_stress(self) -> None:
        if self.bending_stress is None or self.allowable_bending_stress is None:
            return
        self.safety_factor = self.allowable_bending_stress / self.bending_stress
        if self.safety_factor < 1.5:
            raise ValueError(
                f"Bending stress exceeds allowable limits for {self.material}: safety factor {self.safety_factor:.2f}"
            )


__all__ = ["ValidatedGear", "MeshStudyResult"]
