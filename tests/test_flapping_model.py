"""Tests for the synthesis ornithopter flapping model."""

import sys
from importlib import util
from pathlib import Path

import numpy as np

module_path = Path(__file__).resolve().parents[1] / "synthesis" / "ornithopter" / "simulation" / "flapping_model.py"
spec = util.spec_from_file_location("ornithopter_flapping_model", module_path)
assert spec and spec.loader
flapping_model = util.module_from_spec(spec)
sys.modules[spec.name] = flapping_model
spec.loader.exec_module(flapping_model)  # type: ignore[attr-defined]


def test_simulation_outputs_have_expected_shapes():
    result = flapping_model.simulate(duration_s=2.0, dt=0.02, seed=42)
    assert result.time.shape == result.stroke_angle_rad.shape
    assert result.lift_N.shape == result.time.shape
    assert result.energy_wh > 0
    assert result.endurance_min > 0
    assert np.max(result.lift_N) > 0

    artifact_dir = Path("artifacts") / "ornithopter" / "synthesis_sim"
    assert artifact_dir.exists()
    assert (artifact_dir / "flapping_state.csv").exists()


def test_simulation_obeys_control_torque_limit():
    limit = 150.0
    params = flapping_model.AeroelasticParameters(control_torque_limit_nm=limit)
    result = flapping_model.simulate(duration_s=1.0, dt=0.01, seed=0, params=params)
    assert np.max(np.abs(result.control_torque_nm)) <= limit + 1e-3
