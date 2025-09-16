"""Utilities for discovering and interacting with invention modules."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from types import ModuleType
from typing import Callable, Dict, Iterable, List, Protocol
import pkgutil


class InventionModule(Protocol):
    """Protocol describing an invention module contract."""

    SLUG: str
    TITLE: str
    STATUS: str
    SUMMARY: str

    def plan() -> Dict[str, object]:
        ...

    def simulate(seed: int = 0) -> Dict[str, object]:
        ...

    def build() -> None:
        ...

    def evaluate() -> Dict[str, object]:
        ...


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


def discover_inventions() -> Dict[str, InventionSpec]:
    """Discover all invention modules available in the package."""
    specs: Dict[str, InventionSpec] = {}
    for module in _iter_invention_modules():
        required_attrs = ["plan", "simulate", "build", "evaluate"]
        if not all(hasattr(module, attr) for attr in required_attrs):
            continue
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
