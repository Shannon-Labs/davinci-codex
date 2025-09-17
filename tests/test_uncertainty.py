from pathlib import Path

import numpy as np
import pytest

from davinci_codex.uncertainty import MonteCarloSummary, RenaissanceUQ


class DummyInvention:
    def simulate(self, parameters):
        return float(np.sum(parameters))


def test_historical_bounds_pull_from_materials():
    materials_path = Path(__file__).resolve().parents[1] / "materials" / "renaissance_db.yaml"
    uq = RenaissanceUQ(materials_path=materials_path, sampler=lambda *_: np.zeros((1, 5)), analyzer=lambda *_: {"ST": np.zeros(5)})
    bounds = uq.get_historical_bounds()
    assert len(bounds) == 5
    # Guard against regression on density bounds
    oak_bounds = bounds[0]
    assert pytest.approx(oak_bounds[0]) == 650.0
    assert pytest.approx(oak_bounds[1]) == 750.0
    tolerance_bounds = bounds[-1]
    assert tolerance_bounds[0] == pytest.approx(0.001)
    assert tolerance_bounds[1] == pytest.approx(0.002)


def test_monte_carlo_analysis_with_injected_dependencies():
    materials_path = Path(__file__).resolve().parents[1] / "materials" / "renaissance_db.yaml"
    samples = np.array(
        [
            [0.1, 0.2, 0.3, 0.4, 0.5],
            [0.2, 0.3, 0.4, 0.5, 0.6],
            [0.3, 0.4, 0.5, 0.6, 0.7],
            [0.4, 0.5, 0.6, 0.7, 0.8],
        ]
    )
    sampler_calls = []

    def fake_sampler(problem, n_samples):
        sampler_calls.append((problem, n_samples))
        return samples

    def fake_analyzer(problem, outputs):
        assert outputs.shape == (4,)
        return {"ST": np.linspace(0.1, 0.5, num=5)}

    uq = RenaissanceUQ(materials_path=materials_path, sampler=fake_sampler, analyzer=fake_analyzer)
    summary = uq.monte_carlo_analysis(DummyInvention(), n_samples=4)

    assert isinstance(summary, MonteCarloSummary)
    assert sampler_calls and sampler_calls[0][1] == 4
    expected_outputs = np.sum(samples, axis=1)
    assert summary.mean == pytest.approx(np.mean(expected_outputs))
    assert summary.std == pytest.approx(np.std(expected_outputs, ddof=1))
    ci_lower, ci_upper = summary.confidence_95
    computed_lower, computed_upper = np.percentile(expected_outputs, [2.5, 97.5])
    assert ci_lower == pytest.approx(computed_lower)
    assert ci_upper == pytest.approx(computed_upper)
    assert summary.sensitivity == pytest.approx(dict(zip(uq.parameter_names, np.linspace(0.1, 0.5, num=5))))


def test_salib_missing_raises_runtime_error(monkeypatch):
    from davinci_codex import uncertainty as uq_module

    materials_path = Path(__file__).resolve().parents[1] / "materials" / "renaissance_db.yaml"
    monkeypatch.setattr(uq_module, "salib_sample", None)
    monkeypatch.setattr(uq_module, "salib_analyze", None)
    uq = RenaissanceUQ(materials_path=materials_path)

    with pytest.raises(RuntimeError, match="SALib is required"):
        uq.monte_carlo_analysis(DummyInvention(), n_samples=2)


def test_missing_materials_database_raises(tmp_path):
    missing_path = tmp_path / "does_not_exist.yaml"
    with pytest.raises(FileNotFoundError):
        RenaissanceUQ(materials_path=missing_path)
