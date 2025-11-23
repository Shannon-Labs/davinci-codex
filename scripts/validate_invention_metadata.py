#!/usr/bin/env python3
"""
Validate invention module metadata for consistency and completeness.

This script ensures all invention modules follow the required protocol and
maintain consistent metadata structure for the da Vinci Codex framework.
"""

from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path
from typing import Any, Iterable, List

# Add src to path for imports
SRC_ROOT = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(SRC_ROOT))

from davinci_codex import inventions as inventions_package  # type: ignore[attr-defined]  # noqa: E402
from davinci_codex.registry import list_inventions  # noqa: E402

REQUIRED_ATTRIBUTES = [
    "SLUG",
    "TITLE",
    "STATUS",
    "SUMMARY"
]

REQUIRED_FUNCTIONS = [
    "plan",
    "simulate",
    "build",
    "evaluate"
]

VALID_STATUS_VALUES = [
    "planning",
    "in_progress",
    "simulation_prototype",
    "concept_reconstruction",
    "validated",
    "prototype_ready"
]


def _iter_invention_modules() -> Iterable[Any]:
    """Yield all invention modules, even if they are not fully wired into the registry."""
    package_path = getattr(inventions_package, "__path__", None)
    if not package_path:
        return []
    modules: List[Any] = []
    for module_info in __import__("pkgutil").walk_packages(package_path, inventions_package.__name__ + "."):
        if module_info.name.rsplit(".", 1)[-1].startswith("_"):
            continue
        module = import_module(module_info.name)
        modules.append(module)
    return modules


def validate_invention_module(invention_spec: Any) -> List[str]:
    """Validate a single invention module."""
    errors = []
    module = getattr(invention_spec, "module", invention_spec)
    slug = getattr(invention_spec, "slug", module.__name__.rsplit(".", 1)[-1])

    # Check required attributes
    for attr in REQUIRED_ATTRIBUTES:
        if not hasattr(module, attr):
            errors.append(f"{slug}: Missing required attribute '{attr}'")
        elif not getattr(module, attr):
            errors.append(f"{slug}: Attribute '{attr}' is empty")

    # Check required functions
    for func_name in REQUIRED_FUNCTIONS:
        if not hasattr(module, func_name):
            errors.append(f"{slug}: Missing required function '{func_name}'")
        elif not callable(getattr(module, func_name)):
            errors.append(f"{slug}: '{func_name}' is not callable")

    # Validate status
    if hasattr(module, 'STATUS'):
        status = module.STATUS
        if status not in VALID_STATUS_VALUES:
            errors.append(f"{slug}: Invalid status '{status}'. Must be one of: {VALID_STATUS_VALUES}")

    # Check SLUG consistency
    if hasattr(module, 'SLUG') and slug != module.SLUG:
        errors.append(f"{slug}: SLUG attribute '{module.SLUG}' doesn't match filename '{slug}'")

    return errors


def main() -> int:
    """Main validation function."""
    print("🔍 Validating invention module metadata...")

    try:
        inventions_from_registry = list_inventions()
    except Exception as e:
        print(f"❌ Failed to load inventions: {e}")
        return 1

    all_errors = []

    # First validate all modules discoverable via the registry
    for invention in inventions_from_registry:
        errors = validate_invention_module(invention)
        all_errors.extend(errors)

    # Then validate any remaining modules under davinci_codex.inventions that
    # are not currently surfaced via list_inventions() (e.g., missing hooks).
    registered_slugs = {inv.slug for inv in inventions_from_registry}
    for module in _iter_invention_modules():
        slug = getattr(module, "SLUG", module.__name__.rsplit(".", 1)[-1])
        if slug in registered_slugs:
            continue
        errors = validate_invention_module(module)
        all_errors.extend(errors)

    if all_errors:
        print(f"❌ Found {len(all_errors)} validation errors:")
        for error in all_errors:
            print(f"  • {error}")
        return 1
    else:
        total = len(list(inventions_from_registry)) + len(
            [m for m in _iter_invention_modules() if getattr(m, "SLUG", m.__name__.rsplit(".", 1)[-1]) not in registered_slugs]
        )
        print(f"✅ All {total} invention modules are valid!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
