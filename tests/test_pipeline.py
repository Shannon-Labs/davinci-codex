"""Tests for the integrated ornithopter pipeline."""

from davinci_codex import pipelines


def test_run_ornithopter_pipeline():
    report = pipelines.run_ornithopter_pipeline(seed=0, duration_s=5.0)
    assert "plan" in report and "tva" in report and "synthesis" in report
    assert report["tva"]["passes_power"] is False
    assert report["synthesis"]["peak_lift_N"] > 0
    assert report["synthesis"]["peak_control_torque_Nm"] <= 350.0 + 1e-3
    assert report["synthesis"]["artifacts"]["csv"].endswith("flapping_state.csv")
