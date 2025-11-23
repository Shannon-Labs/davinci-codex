#!/usr/bin/env python3
"""
Check per-invention module coverage for high-maturity inventions.

This script reads `coverage.xml` and enforces a minimum coverage threshold
for modules whose status is `validated` or `prototype_ready`.
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from davinci_codex.registry import list_inventions  # noqa: E402


def _load_coverage(path: Path) -> Dict[str, float]:
    """Return a mapping of module file path -> coverage fraction."""
    if not path.exists():
        raise FileNotFoundError(f"Coverage report not found at {path}")

    tree = ET.parse(path)
    root = tree.getroot()

    coverage_by_file: Dict[str, float] = {}
    # Coverage.py XML uses 'packages/package/classes/class' with 'filename' attributes.
    for clazz in root.findall(".//class"):
        filename = clazz.get("filename")
        if not filename:
            continue
        lines = clazz.find("lines")
        if lines is None:
            continue
        total = 0
        covered = 0
        for line in lines.findall("line"):
            hits = int(line.get("hits", "0"))
            total += 1
            if hits > 0:
                covered += 1
        if total:
            coverage_by_file[filename] = covered / total
    return coverage_by_file


def main(threshold: float = 0.80) -> int:
    coverage_path = REPO_ROOT / "coverage.xml"
    coverage_by_file = _load_coverage(coverage_path)

    specs = list_inventions()
    target_statuses = {"validated", "prototype_ready"}
    failures = []

    for spec in specs:
        if spec.status not in target_statuses:
            continue
        # Expect standard layout: src/davinci_codex/inventions/<slug>.py
        expected = f"src/davinci_codex/inventions/{spec.slug}.py"
        frac = coverage_by_file.get(expected)
        if frac is None:
            failures.append(f"{spec.slug}: no coverage data found for {expected}")
            continue
        if frac < threshold:
            pct = round(frac * 100, 1)
            failures.append(f"{spec.slug}: coverage {pct}% below threshold {int(threshold * 100)}%")

    if failures:
        print("❌ Coverage checks failed for high-maturity inventions:")
        for msg in failures:
            print(f"  • {msg}")
        return 1

    print("✅ Coverage thresholds met for validated/prototype_ready inventions.")
    return 0


if __name__ == "__main__":
    # Allow an optional numeric threshold argument, e.g., 0.8 or 0.85
    arg_threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 0.80
    raise SystemExit(main(arg_threshold))

