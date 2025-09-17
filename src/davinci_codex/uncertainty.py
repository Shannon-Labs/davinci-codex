"""Uncertainty quantification utilities for Renaissance inventions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Protocol, Sequence, cast

import numpy as np
import yaml

try:  # pragma: no cover - optional dependency
    from SALib import analyze as salib_analyze
    from SALib import sample as salib_sample
except ImportError:  # pragma: no cover - SALib not installed
    salib_analyze = None
    salib_sample = None

# Type aliases
ProblemSpec = Dict[str, Any]
Sampler = Callable[[ProblemSpec, int], np.ndarray]
Analyzer = Callable[[ProblemSpec, np.ndarray], Dict[str, np.ndarray]]


def load_materials(materials_path: Optional[Path] | None = None) -> Dict[str, Dict[str, Any]]:
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
                data = yaml.safe_load(handle)
            if not isinstance(data, Mapping):
                raise TypeError("Materials database must be a mapping")
            typed = cast(Dict[str, Dict[str, Any]], data)
            return typed
    raise FileNotFoundError(
        "Renaissance materials database not found. Provide `materials_path`."
    )


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
        self.materials = load_materials(materials_path)
        self.parameter_names = [
            "wood_density",
            "iron_yield",
            "rope_friction",
            "leather_elasticity",
            "dimensional_tolerance",
        ]
        self._sampler = sampler
        self._analyzer = analyzer

    def monte_carlo_analysis(self, invention: Simulatable, n_samples: int = 10_000) -> MonteCarloSummary:
        """Run Sobol-based Monte Carlo analysis with historical uncertainties."""

        problem: ProblemSpec = {
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
        bounds.append(self._heuristic_bounds(0.25, 0.05))  # rope friction coefficient (dimensionless)
        bounds.append(self._material_bounds("kid_goat_leather", "tensile_strength"))
        bounds.append(self._heuristic_bounds(self._convert_units(1.5, "mm"), self._convert_units(0.5, "mm")))
        return bounds

    def _material_bounds(self, material_key: str, property_key: str) -> List[float]:
        material = self.materials.get(material_key, {})
        if not isinstance(material, Mapping):
            raise TypeError(f"Material entry for '{material_key}' must be a mapping")
        property_meta = material.get(property_key)
        if not isinstance(property_meta, Mapping):
            raise KeyError(f"Property '{property_key}' missing for material '{material_key}'")
        value_raw = property_meta.get("value")
        if value_raw is None:
            raise KeyError(f"Property '{property_key}' missing 'value' field")
        units = property_meta.get("units")
        value = self._convert_units(float(value_raw), units)
        uncertainty = self._parse_uncertainty(property_meta.get("uncertainty", 0.0), units)
        lower = value - uncertainty
        upper = value + uncertainty
        return [float(lower), float(upper)]

    def _heuristic_bounds(self, value: float, spread: float) -> List[float]:
        return [float(value - spread), float(value + spread)]

    def _parse_uncertainty(self, uncertainty: float | str | None, units: Optional[str]) -> float:
        if uncertainty is None:
            return 0.0
        if isinstance(uncertainty, (int, float)):
            return self._convert_units(float(uncertainty), units)
        cleaned = str(uncertainty).replace("+/-", "").strip()
        if not cleaned:
            return 0.0
        numeric = float(cleaned)
        return self._convert_units(numeric, units)

    def _convert_units(self, value: float, units: Optional[str]) -> float:
        if units is None:
            return value
        normalized = units.strip().lower()
        unit_map = {
            "kg/m^3": 1.0,
            "kg/m3": 1.0,
            "gpa": 1.0e9,
            "mpa": 1.0e6,
            "pa": 1.0,
            "mm": 1.0e-3,
        }
        if normalized not in unit_map:
            raise ValueError(f"Unsupported unit '{units}' in materials database")
        return value * unit_map[normalized]

    def _confidence_interval(self, data: np.ndarray) -> tuple[float, float]:
        percentiles = cast(List[float], np.percentile(data, [2.5, 97.5]).tolist())
        lower, upper = percentiles
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


class Simulatable(Protocol):
    """Protocol for inventions participating in uncertainty analysis."""

    def simulate(self, parameters: Sequence[float]) -> float:
        ...


__all__ = ["RenaissanceUQ", "MonteCarloSummary", "Simulatable", "load_materials"]
