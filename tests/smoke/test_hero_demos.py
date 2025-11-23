from __future__ import annotations

from typing import Any, Dict

from davinci_codex.registry import get_invention


def _has_expected_keys(results: Dict[str, Any]) -> bool:
    expected_key_groups = [
        {"performance", "performance_metrics"},
        {"biomechanical_analysis"},
        {"educational_insights"},
        {"artifacts"},
    ]
    keys = set(results.keys())
    return any(group & keys for group in expected_key_groups)


def test_parachute_simulate_smoke():
    spec = get_invention("parachute")
    # Parachute simulate(seed: int | None = None, scenario: str | None = None)
    results = spec.module.simulate(seed=0)  # type: ignore[attr-defined]
    assert isinstance(results, dict)
    assert results and _has_expected_keys(results)


def test_aerial_screw_simulate_smoke():
    spec = get_invention("aerial_screw")
    results = spec.module.simulate(seed=0)  # type: ignore[attr-defined]
    assert isinstance(results, dict)
    assert results and _has_expected_keys(results)


def test_mechanical_lion_simulate_smoke():
    spec = get_invention("mechanical_lion")
    results = spec.module.simulate(seed=0)  # type: ignore[attr-defined]
    assert isinstance(results, dict)
    assert results and _has_expected_keys(results)
