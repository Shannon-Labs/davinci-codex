#!/usr/bin/env python3
"""
Validate invention module metadata for consistency and completeness.

This script ensures all invention modules follow the required protocol and
maintain consistent metadata structure for the da Vinci Codex framework.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from davinci_codex.registry import list_inventions

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


def validate_invention_module(invention_spec: Any) -> List[str]:
    """Validate a single invention module."""
    errors = []
    module = invention_spec.module
    slug = invention_spec.slug

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

    # Validate docstrings
    for func_name in REQUIRED_FUNCTIONS:
        if hasattr(module, func_name):
            func = getattr(module, func_name)
            if not func.__doc__:
                errors.append(f"{slug}: Function '{func_name}' is missing docstring")

    return errors


def main() -> int:
    """Main validation function."""
    print("🔍 Validating invention module metadata...")

    try:
        inventions = list_inventions()
    except Exception as e:
        print(f"❌ Failed to load inventions: {e}")
        return 1

    all_errors = []

    for invention in inventions:
        errors = validate_invention_module(invention)
        all_errors.extend(errors)

    if all_errors:
        print(f"❌ Found {len(all_errors)} validation errors:")
        for error in all_errors:
            print(f"  • {error}")
        return 1
    else:
        print(f"✅ All {len(inventions)} invention modules are valid!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
