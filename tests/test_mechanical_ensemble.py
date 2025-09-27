from types import SimpleNamespace

import numpy as np
import pytest

from davinci_codex.inventions import mechanical_ensemble


class DummyInstrument:
    def __init__(self, slug: str):
        self.SLUG = slug
        self._plan_called = False
        self._build_called = False

    def plan(self):
        self._plan_called = True
        return {
            "goals": ["Demo"],
            "assumptions": {"fundamental": 440.0},
        }

    def simulate(self, seed: int = 0):
        return {"artifacts": [f"{self.SLUG}/sim.csv"]}

    def build(self):
        self._build_called = True

    def evaluate(self):
        return {"practicality": {"value": 1.0}}

    def _load_params(self):  # noqa: D401 - mimic private access
        return SimpleNamespace()

    def _simulate(self, _params, seed: int = 0):  # noqa: D401
        base_time = np.linspace(0.0, 1.2, num=4)
        return {
            "time_s": base_time,
            "ideal_frequency_hz": np.array([440.0, 660.0, 880.0, 660.0]),
            "pressure_kpa": np.array([8.0, 7.5, 7.8, 8.1]),
        }


@pytest.fixture
def stubbed_ensemble(monkeypatch, tmp_path):
    dummy = DummyInstrument("dummy")
    monkeypatch.setattr(mechanical_ensemble, "_INSTRUMENTS", [("dummy", dummy)])

    def fake_ensure(slug: str, subdir: str | None = None):
        target = tmp_path / slug
        if subdir:
            target /= subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_ensemble, "ensure_artifact_dir", fake_ensure)
    yield dummy, tmp_path


def test_plan_collects_component_metadata(stubbed_ensemble):
    dummy, _ = stubbed_ensemble
    payload = mechanical_ensemble.plan()
    assert "components" in payload
    assert "dummy" in payload["components"]
    assert dummy._plan_called


def test_simulate_generates_spectral_summary(stubbed_ensemble):
    _, tmp_path = stubbed_ensemble
    result = mechanical_ensemble.simulate(seed=1)
    assert result["spectral_centroid_hz"] > 0
    assert "spectral_loudness_db" in result
    summary = tmp_path / mechanical_ensemble.SLUG / "sim" / "spectral_summary.csv"
    assert summary.exists()


def test_build_creates_manifest(stubbed_ensemble):
    dummy, tmp_path = stubbed_ensemble
    mechanical_ensemble.build()
    manifest = tmp_path / mechanical_ensemble.SLUG / "cad" / "ensemble_manifest.txt"
    assert manifest.exists()
    assert dummy._build_called


def test_evaluate_combines_metrics(stubbed_ensemble):
    result = mechanical_ensemble.evaluate()
    spectral = result["spectral"]
    assert spectral["centroid_hz"] > 0
    assert "loudness_db" in spectral
    assert result["validated"]["balanced_spectrum"] in {True, False}


def test_demo_writes_score(stubbed_ensemble):
    _, tmp_path = stubbed_ensemble
    result = mechanical_ensemble.demo(seed=2, tempo_bpm=120.0, measures=2)
    assert result["tempo_bpm"] == 120.0
    score = tmp_path / mechanical_ensemble.SLUG / "demo" / "ensemble_score.json"
    assert score.exists()
