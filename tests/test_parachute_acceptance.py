from __future__ import annotations

import csv
from pathlib import Path
from typing import List

import pytest
import yaml

from davinci_codex.inventions import parachute

SCENARIO_PATH = Path(__file__).resolve().parents[1] / "sims" / parachute.SLUG / "scenarios.yaml"


def _scenario_names() -> List[str]:
    with SCENARIO_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return sorted(data.get("scenarios", {}).keys())


@pytest.mark.parametrize("scenario_name", _scenario_names())
def test_parachute_acceptance_thresholds(tmp_path, monkeypatch, scenario_name):
    def fake_artifact_dir(slug: str):
        path = tmp_path / slug
        path.mkdir(parents=True, exist_ok=True)
        return path

    monkeypatch.setattr("davinci_codex.inventions.parachute.ensure_artifact_dir", fake_artifact_dir)

    result = parachute.simulate(scenario=scenario_name)

    assert result["landing_velocity_ms"] <= parachute.MAX_SAFE_VELOCITY
    assert result["oscillation_amplitude_deg"] <= 5.0
    assert result["canopy_factor_of_safety"] >= parachute.SAFETY_FACTOR

    csv_path = Path(result["artifacts"]["trajectory_csv"])
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            gust = float(row["gust_factor"])
            assert 0.8 <= gust <= 1.2
