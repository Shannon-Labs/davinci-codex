#!/usr/bin/env python3
"""
Regenerate the README invention registry table from the Python registry.

This keeps the README in sync with the authoritative `registry.list_inventions()`
API and avoids manual status or summary drift.
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import shorten

# Ensure local src is importable when running as a script
REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from davinci_codex.registry import list_inventions  # noqa: E402


BEGIN_MARKER = "<!-- BEGIN INVENTION_REGISTRY -->"
END_MARKER = "<!-- END INVENTION_REGISTRY -->"


def _format_table() -> str:
    """Build the Markdown table body from the registry."""
    specs = list_inventions()
    lines = [
        f"{BEGIN_MARKER}",
        "| Slug | Title | Status | Summary |",
        "| --- | --- | --- | --- |",
    ]
    for spec in specs:
        summary = shorten(spec.summary, width=160, placeholder="…")
        # Escape pipe characters to avoid breaking the table
        safe_title = spec.title.replace("|", "\\|")
        safe_summary = summary.replace("|", "\\|")
        lines.append(f"| {spec.slug} | {safe_title} | {spec.status} | {safe_summary} |")
    lines.append(f"{END_MARKER}")
    return "\n".join(lines) + "\n"


def main() -> int:
    readme_path = REPO_ROOT / "README.md"
    original = readme_path.read_text(encoding="utf-8")

    if BEGIN_MARKER not in original or END_MARKER not in original:
        raise SystemExit(
            "Could not find invention registry markers in README.md. "
            f"Ensure both {BEGIN_MARKER!r} and {END_MARKER!r} are present."
        )

    table_block = _format_table()
    prefix, _marker, rest = original.partition(BEGIN_MARKER)
    _table, _marker2, suffix = rest.partition(END_MARKER)

    updated = prefix + table_block + suffix.lstrip("\n")
    readme_path.write_text(updated, encoding="utf-8")
    print("Updated README invention registry table from registry.list_inventions().")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

