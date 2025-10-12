#!/usr/bin/env python3
"""
Check simulation reproducibility by validating seed usage.

This script ensures that all simulations use deterministic seeds for
reproducible results, which is critical for scientific validity.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import List


class SeedChecker(ast.NodeVisitor):
    """AST visitor to check for proper seed usage in simulation functions."""

    def __init__(self):
        self.has_seed_param = False
        self.sets_seed = False
        self.function_name = None
        self.errors = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name == "simulate":
            self.function_name = node.name

            # Check if function has seed parameter
            for arg in node.args.args:
                if arg.arg == "seed":
                    self.has_seed_param = True
                    break

            # Check function body for seed usage
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call):
                    if (hasattr(stmt.func, 'attr') and
                        stmt.func.attr in ['seed', 'random_state'] or
                        hasattr(stmt.func, 'id') and
                        stmt.func.id in ['seed']):
                        self.sets_seed = True
                        break

        self.generic_visit(node)

    def get_errors(self) -> List[str]:
        errors = []
        if self.function_name == "simulate":
            if not self.has_seed_param:
                errors.append("simulate() function missing 'seed' parameter")
            if not self.sets_seed:
                errors.append("simulate() function doesn't set random seed")
        return errors


def check_invention_file(file_path: Path) -> List[str]:
    """Check a single invention file for proper seed usage."""
    errors = []

    try:
        with open(file_path) as f:
            content = f.read()

        tree = ast.parse(content)
        checker = SeedChecker()
        checker.visit(tree)

        file_errors = checker.get_errors()
        errors.extend([f"{file_path.name}: {error}" for error in file_errors])

    except SyntaxError as e:
        errors.append(f"{file_path.name}: Syntax error: {e}")
    except Exception as e:
        errors.append(f"{file_path.name}: Error parsing file: {e}")

    return errors


def check_reproducibility_patterns(file_path: Path) -> List[str]:
    """Check for common reproducibility anti-patterns."""
    errors = []

    try:
        with open(file_path) as f:
            content = f.read()

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for time-based seeds (anti-pattern)
            if 'time()' in line and 'seed' in line:
                errors.append(f"{file_path.name}:{i}: Using time-based seed (non-reproducible)")

            # Check for random.random() without seed setting
            if 'random.random()' in line or 'np.random.random()' in line:
                # Look backwards for seed setting in same function
                found_seed = False
                for j in range(max(0, i-20), i):
                    if 'seed(' in lines[j] or 'random_state' in lines[j]:
                        found_seed = True
                        break

                if not found_seed:
                    errors.append(f"{file_path.name}:{i}: Random usage without visible seed setting")

    except Exception as e:
        errors.append(f"{file_path.name}: Error checking patterns: {e}")

    return errors


def main() -> int:
    """Main validation function."""
    print("🔍 Checking simulation reproducibility...")

    inventions_dir = Path(__file__).parent.parent / "src" / "davinci_codex" / "inventions"

    if not inventions_dir.exists():
        print(f"❌ Inventions directory not found: {inventions_dir}")
        return 1

    all_errors = []
    checked_files = 0

    for py_file in inventions_dir.glob("*.py"):
        if py_file.name.startswith("__"):
            continue

        checked_files += 1

        # Check for proper seed usage
        seed_errors = check_invention_file(py_file)
        all_errors.extend(seed_errors)

        # Check for reproducibility anti-patterns
        pattern_errors = check_reproducibility_patterns(py_file)
        all_errors.extend(pattern_errors)

    if all_errors:
        print(f"❌ Found {len(all_errors)} reproducibility issues in {checked_files} files:")
        for error in all_errors:
            print(f"  • {error}")
        return 1
    else:
        print(f"✅ All {checked_files} simulation files follow reproducibility best practices!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
