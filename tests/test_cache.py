from __future__ import annotations

from pathlib import Path

import davinci_codex.artifacts as artifacts
import davinci_codex.cache as cache
from davinci_codex.cache import compute_cache_key, ensure_cached_result


def test_compute_cache_key_stable(tmp_path: Path) -> None:
    payload = {"alpha": 1, "beta": [1, 2, {"gamma": 3}]}
    first = compute_cache_key(payload)
    second = compute_cache_key({"beta": [1, 2, {"gamma": 3}], "alpha": 1})
    assert first == second
    assert len(first) == 16


def test_ensure_cached_result_creates_directory(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(artifacts, "ARTIFACTS_ROOT", tmp_path / "artifacts")
    monkeypatch.setattr(cache, "ARTIFACTS_ROOT", tmp_path / "artifacts")
    entry, hit = ensure_cached_result("demo", {"seed": 1}, label="unit")
    assert not hit
    assert entry.path.exists()
    entry.write_metadata({"seed": 1})
    _, hit_again = ensure_cached_result("demo", {"seed": 1}, label="unit")
    assert hit_again
    assert entry.metadata_path.read_text(encoding="utf-8") != ""
