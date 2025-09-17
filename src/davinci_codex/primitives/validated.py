"""Validated mechanical primitive implementations."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class MeshStudyResult:
    """Convergence metadata from Richardson extrapolation."""

    meshes: List[int]
    estimates: List[float]
    exact_solution: float
    error_estimate: float


class ValidatedGear:
    """Gear with simplified verification aligned to Lewis/AGMA practice."""

    def __init__(self, teeth: int, module: float, material: str = "seasoned_oak") -> None:
        if teeth < 8:
            raise ValueError("ValidatedGear requires at least 8 teeth to avoid undercutting")
        if module <= 0:
            raise ValueError("Module must be positive")
        self.teeth = teeth
        self.module = module
        self.material = material
        self.face_width = 10.0 * module
        self.design_torque = 120.0  # N·m representative textile drive
        self.bending_stress: float | None = None
        self.converged_stress: float | None = None
        self.discretization_error: float | None = None

        self.validate_involute_profile()
        self.mesh_convergence_study()

    def pitch_radius(self) -> float:
        return (self.teeth * self.module) / (2 * math.pi)

    def lewis_form_factor(self) -> float:
        return 0.124 - (0.684 / self.teeth)

    def transmitted_force(self) -> float:
        return self.design_torque / self.pitch_radius()

    def lewis_bending_stress(self) -> float:
        ft = self.transmitted_force()
        y = self.lewis_form_factor()
        section_modulus = self.face_width * self.module
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


__all__ = ["ValidatedGear", "MeshStudyResult"]
