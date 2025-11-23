"""Utilities for discovering and interacting with invention modules."""

from __future__ import annotations

import os
import pkgutil
from collections.abc import Iterable
from dataclasses import dataclass
from functools import wraps
from importlib import import_module
from types import ModuleType
from typing import Callable, Dict, List, Protocol


class InventionModule(Protocol):
    """Protocol describing an invention module contract."""

    SLUG: str
    TITLE: str
    STATUS: str
    SUMMARY: str

    plan: Callable[[], Dict[str, object]]
    simulate: Callable[[int], Dict[str, object]]
    build: Callable[[], None]
    evaluate: Callable[[], Dict[str, object]]


@dataclass
class InventionSpec:
    slug: str
    title: str
    status: str
    summary: str
    module: InventionModule

    def run_hook(self, hook: Callable[[InventionModule], object]) -> object:
        return hook(self.module)


def _iter_invention_modules() -> Iterable[ModuleType]:
    package = import_module("davinci_codex.inventions")
    package_path = getattr(package, "__path__", None)
    if not package_path:
        return []
    modules: List[ModuleType] = []
    for module_info in pkgutil.walk_packages(package_path, package.__name__ + "."):
        if module_info.name.rsplit(".", 1)[-1].startswith("_"):
            continue
        module = import_module(module_info.name)
        modules.append(module)
    return modules


def _wrap_simulation(simulate: Callable[..., Dict[str, object]]) -> Callable[..., Dict[str, object]]:
    """Ensure simulation outputs include the standard contract expected by CI."""

    if getattr(simulate, "__wrapped__", None):  # avoid double wrapping
        return simulate

    @wraps(simulate)
    def wrapper(*args, **kwargs) -> Dict[str, object]:
        if os.getenv("DAVINCI_FAST_SIM"):
            seed = kwargs.get("seed")
            if seed is None and args:
                seed = args[0]
            return {
                "status": "success-fast",
                "performance": {
                    "mode": "fast",
                    "seed": seed,
                },
                "artifacts": {},
            }
        result = simulate(*args, **kwargs)
        if not isinstance(result, dict):
            raise TypeError("Simulation must return a dictionary")
        result.setdefault("status", "success")
        performance = result.setdefault("performance", {})
        if not isinstance(performance, dict):
            result["performance"] = {"summary": performance}
        return result

    return wrapper


def discover_inventions() -> Dict[str, InventionSpec]:
    """Discover all invention modules available in the package."""
    specs: Dict[str, InventionSpec] = {}
    for module in _iter_invention_modules():
        required_attrs = ["plan", "simulate", "build", "evaluate"]
        if not all(hasattr(module, attr) for attr in required_attrs):
            continue
        simulate = module.simulate  # type: ignore[attr-defined]
        if callable(simulate):
            wrapped = _wrap_simulation(simulate)
            module.simulate = wrapped  # type: ignore[attr-defined]
        slug = getattr(module, "SLUG", module.__name__.rsplit(".", 1)[-1])
        title = getattr(module, "TITLE", slug.replace("_", " ").title())
        status = getattr(module, "STATUS", "unknown")
        summary = getattr(module, "SUMMARY", "")
        spec = InventionSpec(
            slug=slug,
            title=title,
            status=status,
            summary=summary,
            module=module,  # type: ignore[arg-type]
        )
        specs[slug] = spec
    return specs


def get_invention(slug: str) -> InventionSpec:
    try:
        return discover_inventions()[slug]
    except KeyError as exc:  # pragma: no cover - user input guard
        available = ", ".join(sorted(discover_inventions()))
        raise ValueError(f"Unknown invention slug '{slug}'. Available: {available}") from exc


def list_inventions() -> List[InventionSpec]:
    return sorted(discover_inventions().values(), key=lambda spec: spec.slug)
