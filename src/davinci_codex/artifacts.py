"""Helpers for storing deterministic, reproducible artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

ARTIFACTS_ROOT = Path("artifacts")


def ensure_artifact_dir(slug: str, *, subdir: Optional[str] = None) -> Path:
    """Return (and create) an artifact directory for the given invention slug."""
    target = ARTIFACTS_ROOT / slug
    if subdir:
        target /= subdir
    target.mkdir(parents=True, exist_ok=True)
    return target
