#!/usr/bin/env python3
"""
Regenerate the docs/inventions index table from registry + YAML metadata.

This keeps the public inventions index aligned with the Python registry while
allowing per-invention metrics and primary documentation links to be edited in
one place (`inventions/module_metadata.yaml`).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from textwrap import shorten
from typing import Dict, List

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "inventions" / "index.md"
META_PATH = REPO_ROOT / "inventions" / "module_metadata.yaml"

BEGIN_MARKER = "<!-- BEGIN INVENTION_CARDS -->"
END_MARKER = "<!-- END INVENTION_CARDS -->"

SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from davinci_codex.registry import list_inventions  # noqa: E402


@dataclass
class InventionMeta:
    slug: str
    status: str
    primary_doc: str
    hero_asset: str
    metrics: List[Dict[str, str]]


def _load_metadata() -> Dict[str, InventionMeta]:
    raw = yaml.safe_load(META_PATH.read_text(encoding="utf-8")) or {}
    entries = raw.get("inventions", [])
    result: Dict[str, InventionMeta] = {}
    for entry in entries:
        meta = InventionMeta(
            slug=entry["slug"],
            status=entry["status"],
            primary_doc=entry["primary_doc"],
            hero_asset=entry["hero_asset"],
            metrics=entry.get("metrics", []),
        )
        result[meta.slug] = meta
    return result


def _format_metrics(metrics: List[Dict[str, str]]) -> str:
    if not metrics:
        return ""
    # Use at most two short metric snippets
    snippets = []
    for item in metrics[:2]:
        label = item.get("label", "").strip()
        value = item.get("value", "").strip()
        context = item.get("context", "").strip()
        parts = [p for p in (label, value) if p]
        text = " ".join(parts)
        if context:
            text = f"{text} ({context})"
        snippets.append(shorten(text, width=80, placeholder="…"))
    return "; ".join(snippets)


def _build_table() -> str:
    registry_specs = {spec.slug: spec for spec in list_inventions()}
    meta_by_slug = _load_metadata()

    lines = [
        BEGIN_MARKER,
        "| Slug | Title | Status | Metrics | Primary docs |",
        "| --- | --- | --- | --- | --- |",
    ]

    for slug in sorted(meta_by_slug):
        meta = meta_by_slug[slug]
        spec = registry_specs.get(slug)
        if spec is None:
            raise SystemExit(f"Metadata slug '{slug}' not found in registry.")
        if spec.status != meta.status:
            raise SystemExit(
                f"Status mismatch for '{slug}': registry={spec.status!r} metadata={meta.status!r}"
            )
        metrics_text = _format_metrics(meta.metrics)
        title = spec.title.replace("|", "\\|")
        metrics_text = metrics_text.replace("|", "\\|")
        primary_link = f"[report]({meta.primary_doc.replace('docs/', '../')})"
        lines.append(
            f"| `{slug}` | {title} | `{spec.status}` | {metrics_text} | {primary_link} |"
        )

    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"


def main() -> int:
    content = DOC_PATH.read_text(encoding="utf-8")
    if BEGIN_MARKER not in content or END_MARKER not in content:
        raise SystemExit(
            "Could not find invention cards markers in docs/inventions/index.md. "
            f"Ensure both {BEGIN_MARKER!r} and {END_MARKER!r} are present."
        )

    table_block = _build_table()
    prefix, _marker, rest = content.partition(BEGIN_MARKER)
    _table, _marker2, suffix = rest.partition(END_MARKER)
    updated = prefix + table_block + suffix.lstrip("\n")
    DOC_PATH.write_text(updated, encoding="utf-8")
    print("Updated docs/inventions/index.md from registry and module_metadata.yaml.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

