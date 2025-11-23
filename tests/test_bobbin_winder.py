"""Tests for the automatic bobbin winder module."""

import os

import pytest

from davinci_codex.artifacts import ensure_artifact_dir
from davinci_codex.inventions import bobbin_winder


@pytest.fixture(scope="module")
def compound_result():
    return bobbin_winder.simulate(cam_type="compound")


@pytest.fixture(scope="module")
def heart_result():
    return bobbin_winder.simulate(cam_type="heart")


def test_plan_cites_codex_atlanticus():
    plan = bobbin_winder.plan()
    origin = plan["origin"]
    assert "1090r" in origin["folio"]
    assert "Walnut" in origin["materials"]["frame"]


def test_compound_cam_meets_uniformity_target(compound_result):
    assert compound_result["uniformity"] >= 0.95
    assert compound_result["production_rate_m_per_hr"] >= 200.0
    for artifact_path in compound_result["artifacts"].values():
        assert os.path.exists(artifact_path)


def test_compound_outperforms_heart(compound_result, heart_result):
    assert compound_result["uniformity"] > heart_result["uniformity"]
    assert compound_result["tension_std_N"] < heart_result["tension_std_N"]


def test_build_creates_placeholder():
    bobbin_winder.build()
    artifact_dir = ensure_artifact_dir(bobbin_winder.SLUG, subdir="cad")
    assert any(artifact_dir.iterdir())


def test_evaluate_reports_wear_margin():
    report = bobbin_winder.evaluate()
    assert report["performance"]["meets_uniformity_target"] is True
    wear = report["wear_analysis"]
    assert wear["estimated_cycles"] >= wear["target_cycles"]
    for path in report["artifacts"].values():
        assert os.path.exists(path)
