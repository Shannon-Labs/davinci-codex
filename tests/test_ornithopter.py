"""Tests for the ornithopter modernization module."""

import os

from davinci_codex.inventions import ornithopter
from davinci_codex.artifacts import ensure_artifact_dir


def test_plan_contains_provenance():
    plan = ornithopter.plan()
    assert "origin" in plan
    folios = plan["origin"]["folios"]
    assert any("Codex Atlanticus" in entry["reference"] for entry in folios)
    metrics = plan["viability_metrics"]
    assert metrics["gross_weight_N"] > 0
    assert metrics["cruise_lift_N"] > 0


def test_simulation_produces_artifacts():
    result = ornithopter.simulate(seed=0)
    assert result["avg_lift_N"] > 0
    assert result["artifacts"]
    for path in result["artifacts"].values():
        assert os.path.exists(path)
    assert -0.5 < result["lift_margin"] < 1.0  # within reasonable range
    assert result["estimated_endurance_min"] > 0


def test_evaluate_aggregates_findings():
    evaluation = ornithopter.evaluate()
    assert "feasibility" in evaluation
    feasibility = evaluation["feasibility"]
    assert isinstance(feasibility["lift_margin"], float)
    assert feasibility["endurance_min"] > 0
    assert "risks" in evaluation
    assert "artifacts" in evaluation
    for artifact in evaluation["artifacts"].values():
        assert os.path.exists(artifact)


def test_build_generates_files():
    ornithopter.build()
    artifact_dir = ensure_artifact_dir(ornithopter.SLUG, subdir="cad")
    files = list(artifact_dir.glob("*"))
    assert files  # at least one artifact (SCAD or placeholder)
