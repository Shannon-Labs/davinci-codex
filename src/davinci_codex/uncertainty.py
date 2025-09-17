"""Uncertainty quantification utilities for Renaissance inventions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence

import numpy as np
import yaml

try:  # pragma: no cover - optional dependency
    from SALib import analyze as salib_analyze
    from SALib import sample as salib_sample
except ImportError:  # pragma: no cover - SALib not installed
    salib_analyze = None
    salib_sample = None

# Type aliases
Sampler = Callable[[Dict[str, Sequence[Sequence[float]]], int], np.ndarray]
Analyzer = Callable[[Dict[str, Sequence[Sequence[float]]], np.ndarray], Dict[str, np.ndarray]]


@dataclass(frozen=True)
class MonteCarloSummary:
    """Summary statistics from a Monte Carlo campaign."""

    mean: float
    std: float
    confidence_95: tuple[float, float]
    sensitivity: Dict[str, float]


class RenaissanceUQ:
    """Uncertainty quantification manager using historical parameter bounds."""

    def __init__(
        self,
        materials_path: Optional[Path] | None = None,
        sampler: Optional[Sampler] = None,
        analyzer: Optional[Analyzer] = None,
    ) -> None:
        self.materials = self._load_materials(materials_path)
        self.parameter_names = [
            "wood_density",
            "iron_yield",
            "rope_friction",
            "leather_elasticity",
            "dimensional_tolerance",
        ]
        self._sampler = sampler
        self._analyzer = analyzer

    def _load_materials(self, materials_path: Optional[Path]) -> Dict[str, dict]:
        candidate_paths: Iterable[Path]
        if materials_path:
            candidate_paths = [Path(materials_path)]
        else:
            root = Path(__file__).resolve().parents[2]
            candidate_paths = [
                root / "materials" / "renaissance_db.yaml",
                Path(__file__).resolve().with_name("materials.yaml"),
            ]
        for path in candidate_paths:
            if path.exists():
                with path.open("r", encoding="utf-8") as handle:
                    return yaml.safe_load(handle)
        raise FileNotFoundError(
            "Renaissance materials database not found. Provide `materials_path`."
        )

    def monte_carlo_analysis(self, invention: "Simulatable", n_samples: int = 10_000) -> MonteCarloSummary:
        """Run Sobol-based Monte Carlo analysis with historical uncertainties."""

        problem = {
            "num_vars": len(self.parameter_names),
            "names": self.parameter_names,
            "bounds": self.get_historical_bounds(),
        }

        sampler = self._resolve_sampler()
        analyzer = self._resolve_analyzer()

        samples = sampler(problem, n_samples)
        outputs = np.asarray([invention.simulate(sample) for sample in samples], dtype=float)

        sensitivity_indices = analyzer(problem, outputs)

        summary = MonteCarloSummary(
            mean=float(np.mean(outputs)),
            std=float(np.std(outputs, ddof=1)),
            confidence_95=self._confidence_interval(outputs),
            sensitivity=self._extract_total_sobol(sensitivity_indices),
        )
        return summary

    def get_historical_bounds(self) -> List[List[float]]:
        """Return parameter bounds derived from manuscript-era sources."""

        bounds: List[List[float]] = []
        bounds.append(self._material_bounds("seasoned_oak", "density"))
        bounds.append(self._material_bounds("wrought_iron_1500", "yield_strength"))
        bounds.append(self._heuristic_bounds(0.25, 0.05))  # rope friction coefficient
        bounds.append(self._material_bounds("kid_goat_leather", "tensile_strength", scale=1.0e6))
        bounds.append(self._heuristic_bounds(1.5, 0.5))  # dimensional tolerance in mm
        return bounds

    def _material_bounds(self, material_key: str, property_key: str, scale: float = 1.0) -> List[float]:
        material = self.materials.get(material_key, {})
        property_meta = material.get(property_key)
        if not property_meta:
            raise KeyError(f"Property '{property_key}' missing for material '{material_key}'")
        value = float(property_meta.get("value"))
        uncertainty = self._parse_uncertainty(property_meta.get("uncertainty", 0.0))
        lower = (value - uncertainty) * scale
        upper = (value + uncertainty) * scale
        return [lower, upper]

    def _heuristic_bounds(self, value: float, spread: float) -> List[float]:
        return [float(value - spread), float(value + spread)]

    def _parse_uncertainty(self, uncertainty: float | str | None) -> float:
        if uncertainty is None:
            return 0.0
        if isinstance(uncertainty, (int, float)):
            return float(uncertainty)
        cleaned = str(uncertainty).replace("+/-", "").strip()
        return float(cleaned)

    def _confidence_interval(self, data: np.ndarray) -> tuple[float, float]:
        lower, upper = np.percentile(data, [2.5, 97.5])
        return float(lower), float(upper)

    def _extract_total_sobol(self, sensitivity_indices: Dict[str, np.ndarray]) -> Dict[str, float]:
        total = sensitivity_indices.get("ST")
        if total is None:
            raise KeyError("SALib Sobol analyzer did not return total-order indices (ST)")
        return {
            name: float(value)
            for name, value in zip(self.parameter_names, total)
        }

    def _resolve_sampler(self) -> Sampler:
        if self._sampler:
            return self._sampler
        if salib_sample is None:
            raise RuntimeError(
                "SALib is required for Monte Carlo sampling. Install `SALib` or inject a custom sampler."
            )
        return lambda problem, n_samples: salib_sample.saltelli(
            problem,
            n_samples,
            calc_second_order=False,
        )

    def _resolve_analyzer(self) -> Analyzer:
        if self._analyzer:
            return self._analyzer
        if salib_analyze is None:
            raise RuntimeError(
                "SALib is required for Sobol analysis. Install `SALib` or inject a custom analyzer."
            )
        return lambda problem, outputs: salib_analyze.sobol(problem, outputs)


class Simulatable:
    """Protocol-style base class for inventions participating in UQ."""

    def simulate(self, parameters: Sequence[float]) -> float:  # pragma: no cover - interface definition
        raise NotImplementedError


__all__ = ["RenaissanceUQ", "MonteCarloSummary", "Simulatable"]
