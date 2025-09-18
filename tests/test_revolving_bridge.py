from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import numpy as np
import pytest

from davinci_codex.inventions import revolving_bridge


def _load_rotation_module():
    root = Path(__file__).resolve().parents[1]
    module_path = root / "sims" / revolving_bridge.SLUG / "rotation_profile.py"
    spec = importlib.util.spec_from_file_location("sims.revolving_bridge.rotation_profile", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError("Unable to load rotation profile module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


ROTATION_MODULE = _load_rotation_module()


def test_plan_references_counterweight_targets():
    payload = revolving_bridge.plan()
    assert payload["origin"]["folio"] == "Codex Atlanticus, folio 855r"
    assumptions = payload["modern_assumptions"]
    assert assumptions["span_length_m"] == pytest.approx(revolving_bridge.SPAN_LENGTH_M)
    assert assumptions["load_capacity_kg"] == pytest.approx(revolving_bridge.LOAD_CAPACITY_KG)
    assert payload["governing_equations"], "Governing equations should be listed"
    assert revolving_bridge.STATUS == "in_progress"


def test_rotation_profile_emits_csv_schema(tmp_path):
    result = ROTATION_MODULE.generate(tmp_path)
    csv_path = Path(result["csv"])
    assert csv_path.exists()
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    assert header == [
        "angle_deg",
        "moment_kNm",
        "stress_MPa",
        "deflection_mm",
        "torque_kNm",
        "stability_margin_kNm",
    ]
    plots = [Path(p) for p in result["plots"]]
    for plot in plots:
        assert plot.exists(), f"Missing plot {plot}"


def test_acceptance_metrics_meet_requirements():
    params = ROTATION_MODULE.load_parameters()
    rotation = ROTATION_MODULE.compute_rotation_profile(params)
    metrics = ROTATION_MODULE.acceptance_metrics(params, rotation)
    span = revolving_bridge.SPAN_LENGTH_M

    assert metrics["rotation_time_s"] <= revolving_bridge.ROTATION_TIME_LIMIT_S
    assert metrics["safety_factor"] >= revolving_bridge.TARGET_SAFETY_FACTOR
    assert metrics["max_deflection_m"] <= span / 800.0
    assert metrics["stability_margin_min_Nm"] > 0.0


def test_simulation_artifacts_reference_rotation_csv(tmp_path, monkeypatch):
    target_dir = tmp_path / "artifacts"

    def fake_ensure(slug: str, subdir: str | None = None):
        path = target_dir / slug
        if subdir:
            path = path / subdir
        path.mkdir(parents=True, exist_ok=True)
        return path

    monkeypatch.setattr("davinci_codex.inventions.revolving_bridge.ensure_artifact_dir", fake_ensure)
    results = revolving_bridge.simulate(seed=0)
    artifacts = [Path(path) for path in results["artifacts"]]
    csv_files = [path for path in artifacts if path.suffix == ".csv"]
    assert csv_files, "Expected at least one CSV artifact"
    for artifact in artifacts:
        assert artifact.exists(), f"Missing artifact {artifact}"
    rotation = ROTATION_MODULE.compute_rotation_profile(ROTATION_MODULE.load_parameters())
    assert np.isclose(results["torque_requirement_kNm"], float(rotation["rotation_torque_Nm"][0] / 1000.0))
