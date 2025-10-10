from __future__ import annotations

import json
from pathlib import Path

import davinci_codex.artifacts as artifacts
import davinci_codex.cache as cache
from davinci_codex.registry import get_invention
from davinci_codex.sweeps import run_parameter_sweep


def test_run_parameter_sweep_generates_summary(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(artifacts, "ARTIFACTS_ROOT", tmp_path / "artifacts")
    monkeypatch.setattr(cache, "ARTIFACTS_ROOT", tmp_path / "artifacts")
    spec = get_invention("mechanical_odometer")
    summary = run_parameter_sweep(spec, fidelity=None, seeds=[0, 1], label="pytest", reuse_cache=False)
    assert summary["slug"] == "mechanical_odometer"
    assert len(summary["runs"]) == 2
    aggregates = summary["aggregates"]
    assert isinstance(aggregates, dict)
    assert aggregates  # ensure metrics were captured

    sweep_root = Path("artifacts") / spec.slug / "cache" / "sweep"
    assert sweep_root.exists()

    summary_paths = list(sweep_root.glob("*/summary.json"))
    assert summary_paths
    loaded = json.loads(summary_paths[0].read_text(encoding="utf-8"))
    assert loaded["slug"] == summary["slug"]
