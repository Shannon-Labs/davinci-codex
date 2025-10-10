"""Artifact caching utilities for deterministic simulation outputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple

from .artifacts import ARTIFACTS_ROOT

_CACHE_DIR_NAME = "cache"
_DEFAULT_LABEL = "default"


class CacheEntry:
    """Represents a resolved cache location for a particular configuration."""

    def __init__(self, slug: str, label: str, cache_key: str) -> None:
        self.slug = slug
        self.label = label
        self.cache_key = cache_key
        self.path = ARTIFACTS_ROOT / slug / _CACHE_DIR_NAME / label / cache_key
        self.path.mkdir(parents=True, exist_ok=True)

    @property
    def metadata_path(self) -> Path:
        return self.path / "metadata.json"

    def write_metadata(self, metadata: Dict[str, Any]) -> None:
        with self.metadata_path.open("w", encoding="utf-8") as handle:
            json.dump(metadata, handle, indent=2, sort_keys=True)

    def read_metadata(self) -> Dict[str, Any] | None:
        if not self.metadata_path.exists():
            return None
        with self.metadata_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)


def _normalise_for_hash(data: Any) -> Any:
    """Normalise input data to a JSON-serialisable structure for hashing."""
    if isinstance(data, dict):
        return {str(key): _normalise_for_hash(value) for key, value in sorted(data.items())}
    if isinstance(data, (list, tuple, set)):
        return [_normalise_for_hash(value) for value in data]
    if isinstance(data, (str, int, float, bool)) or data is None:
        return data
    return str(data)


def compute_cache_key(payload: Dict[str, Any]) -> str:
    """Compute a stable hash for the given payload."""
    normalised = _normalise_for_hash(payload)
    serialised = json.dumps(normalised, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(serialised.encode("utf-8")).hexdigest()
    return digest[:16]


def resolve_cache_entry(
    slug: str,
    payload: Dict[str, Any],
    *,
    label: str | None = None,
) -> CacheEntry:
    """Resolve cache location for a slug/payload pair."""
    cache_key = compute_cache_key(payload)
    cache_label = label or _DEFAULT_LABEL
    return CacheEntry(slug=slug, label=cache_label, cache_key=cache_key)


def ensure_cached_result(
    slug: str,
    payload: Dict[str, Any],
    *,
    label: str | None = None,
) -> Tuple[CacheEntry, bool]:
    """Return cache entry and whether matching metadata already exists."""
    entry = resolve_cache_entry(slug, payload, label=label)
    return entry, entry.metadata_path.exists()
