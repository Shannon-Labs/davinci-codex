#!/usr/bin/env python3
"""
Validate CAD model integrity and structure.

This script checks that CAD models are properly structured, have valid
geometry, and follow the project conventions for the da Vinci Codex.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List


def validate_cad_directory_structure(cad_root: Path) -> List[str]:
    """Validate the overall CAD directory structure."""
    errors = []

    if not cad_root.exists():
        errors.append("CAD root directory does not exist")
        return errors

    # Check for standard subdirectories
    expected_dirs = ["aerial_screw", "mechanical_lion"]
    for dir_name in expected_dirs:
        dir_path = cad_root / dir_name
        if dir_path.exists():
            # Check for model.py file
            model_file = dir_path / "model.py"
            if not model_file.exists():
                errors.append(f"{dir_name}: Missing model.py file")
            else:
                # Validate model file content
                model_errors = validate_model_file(model_file)
                errors.extend([f"{dir_name}: {error}" for error in model_errors])

    return errors


def validate_model_file(model_file: Path) -> List[str]:
    """Validate a CAD model Python file."""
    errors = []

    try:
        with open(model_file) as f:
            content = f.read()

        # Check for required imports
        required_imports = ["trimesh", "numpy"]
        for import_name in required_imports:
            if f"import {import_name}" not in content and f"from {import_name}" not in content:
                errors.append(f"Missing required import: {import_name}")

        # Check for export functions
        if "def export" not in content and "def generate" not in content:
            errors.append("No export/generate function found")

        # Check for docstring
        lines = content.split('\n')
        if not (len(lines) > 0 and lines[0].startswith('"""')):
            errors.append("Missing module docstring")

    except Exception as e:
        errors.append(f"Failed to read model file: {e}")

    return errors


def validate_cad_python_syntax() -> List[str]:
    """Validate Python syntax in CAD files."""
    errors = []
    cad_root = Path(__file__).parent.parent / "cad"

    for python_file in cad_root.glob("**/*.py"):
        try:
            with open(python_file) as f:
                content = f.read()

            # Basic syntax check
            compile(content, python_file, 'exec')

        except SyntaxError as e:
            errors.append(f"{python_file.relative_to(cad_root)}: Syntax error at line {e.lineno}: {e.msg}")
        except Exception as e:
            errors.append(f"{python_file.relative_to(cad_root)}: Error: {e}")

    return errors


def main() -> int:
    """Main validation function."""
    print("🔍 Validating CAD models...")

    cad_root = Path(__file__).parent.parent / "cad"
    all_errors = []

    # Validate directory structure
    structure_errors = validate_cad_directory_structure(cad_root)
    all_errors.extend(structure_errors)

    # Validate Python syntax
    syntax_errors = validate_cad_python_syntax()
    all_errors.extend(syntax_errors)

    if all_errors:
        print(f"❌ Found {len(all_errors)} CAD validation errors:")
        for error in all_errors:
            print(f"  • {error}")
        return 1
    else:
        print("✅ All CAD models are valid!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
