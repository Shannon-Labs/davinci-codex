"""Tests for da Vinci's pyramid parachute module."""

import csv
import math
from pathlib import Path

import pytest

from davinci_codex.inventions import parachute


def test_module_attributes():
    """Verify module exports required attributes."""
    assert parachute.SLUG == "parachute"
    assert parachute.TITLE == "Pyramid Parachute"
    assert parachute.STATUS == "prototype_ready"
    assert "pyramid" in parachute.SUMMARY.lower()


def test_plan_calculations():
    """Verify planning calculations are physically reasonable."""
    plan = parachute.plan()

    # Check structure
    assert "educational_physics" in plan
    assert "historical_analysis" in plan
    assert "modern_engineering" in plan
    assert "system_performance" in plan

    # Check historical analysis
    historical = plan["historical_analysis"]
    assert "Codex Atlanticus" in historical["reference"]
    assert "381v" in historical["reference"]

    # Check dimensions
    design = plan["modern_engineering"]["canopy_dimensions"]
    assert design["base_width_m"] == pytest.approx(7.0, rel=0.1)
    assert design["base_area_m2"] == pytest.approx(49.0, rel=0.1)

    # Check materials are lighter than historical
    materials = plan["modern_engineering"]["materials_analysis"]
    assert materials["canopy_density_kg_m2"] < 0.5  # Lighter than linen
    assert materials["frame_mass_kg"] < 50  # Lighter than wood equivalent

    # Check performance
    perf = plan["system_performance"]
    assert 5.0 <= perf["descent_rate_ms"] <= 10.0  # Reasonable descent speed


def test_simulate_descent():
    """Test descent simulation produces valid trajectory."""
    result = parachute.simulate(seed=42, scenario="nominal_calibration")

    # Check result structure
    assert "performance_metrics" in result
    assert "aerodynamic_analysis" in result
    assert "stability_assessment" in result
    assert "safety_analysis" in result
    assert "artifacts" in result

    # Extract performance metrics
    perf = result["performance_metrics"]
    assert 100 < perf["descent_time_s"] < 400  # Reasonable descent time range
    assert perf["landing_velocity_ms"] <= parachute.MAX_SAFE_VELOCITY  # Should be safe
    assert perf["landing_velocity_kmh"] == pytest.approx(
        perf["landing_velocity_ms"] * 3.6, rel=0.01
    )

    # Check safety analysis
    safety = result["safety_analysis"]
    assert safety["safe_landing"] is True

    # Check stability assessment
    stability = result["stability_assessment"]
    assert stability["max_sway_angle_deg"] <= 15.0  # Should be within reasonable limits

    # Check artifacts were created and CSV schema is comprehensive
    assert "comprehensive_plot" in result["artifacts"]
    assert "trajectory_csv" in result["artifacts"]
    csv_path = Path(result["artifacts"]["trajectory_csv"])
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    # Check that new comprehensive CSV includes more columns
    assert len(header) > 5
    assert "time_s" in header
    assert "altitude_m" in header
    assert "vertical_velocity_ms" in header
    assert "reynolds_number" in header


def test_terminal_velocity_physics():
    """Verify terminal velocity calculation is correct."""
    # At terminal velocity: Weight = Drag
    # mg = 0.5 * rho * Cd * A * v^2
    # v = sqrt(2mg / (rho * Cd * A))

    plan_data = parachute.plan()
    total_mass = plan_data["system_performance"]["total_system_mass_kg"]
    base_area = plan_data["modern_engineering"]["canopy_dimensions"]["base_area_m2"]
    drag_coeff = float(plan_data["modern_engineering"]["aerodynamic_performance"]["drag_coefficient"])

    expected_terminal = math.sqrt(
        (2 * total_mass * parachute.GRAVITY) /
        (parachute.RHO_AIR_SEA_LEVEL * drag_coeff * base_area)
    )

    assert plan_data["system_performance"]["descent_rate_ms"] == pytest.approx(
        expected_terminal, rel=0.05
    )


def test_evaluate_feasibility():
    """Test evaluation produces comprehensive assessment."""
    result = parachute.evaluate()

    # Check structure
    assert "executive_summary" in result
    assert "technical_feasibility" in result
    assert "comprehensive_safety_analysis" in result
    assert "historical_significance" in result
    assert "educational_impact" in result
    assert "implementation_roadmap" in result

    # Check executive summary
    exec_summary = result["executive_summary"]
    assert exec_summary["feasibility_rating"] == "VALIDATED"
    assert exec_summary["safety_rating"] == "ACCEPTABLE"
    assert exec_summary["recommendation"] == "PROCEED_TO_PROTOTYPE"

    # Check technical feasibility
    tech_feas = result["technical_feasibility"]
    assert "aerodynamic_performance" in tech_feas
    assert "structural_integrity" in tech_feas
    assert "simulation_results" in tech_feas

    # Check historical significance
    historical = result["historical_significance"]
    assert historical["historical_impact"]["ahead_of_time"] > 300  # Way ahead of its time

    # Check safety analysis
    safety = result["comprehensive_safety_analysis"]
    assert "failure_mode_assessment" in safety
    assert "safety_compliance" in safety


def test_build_creates_artifacts():
    """Test that build function creates CAD artifacts."""
    # This should not raise an exception
    parachute.build()

    # Check that artifact directory exists
    from davinci_codex.artifacts import ensure_artifact_dir
    artifact_dir = ensure_artifact_dir(parachute.SLUG)
    assert artifact_dir.exists()

    # Should create either CAD files or placeholder
    files = list(artifact_dir.glob("*"))
    assert len(files) > 0  # At least one file created


def test_deterministic_simulation():
    """Verify simulation is deterministic with same seed."""
    result1 = parachute.simulate(seed=123, scenario="nominal_calibration")
    result2 = parachute.simulate(seed=123, scenario="nominal_calibration")

    perf1 = result1["performance_metrics"]
    perf2 = result2["performance_metrics"]

    assert perf1["descent_time_s"] == perf2["descent_time_s"]
    assert perf1["landing_velocity_ms"] == perf2["landing_velocity_ms"]
    assert perf1["max_velocity_ms"] == perf2["max_velocity_ms"]


def test_different_seeds_produce_variation():
    """Verify different seeds produce slightly different results (turbulence)."""
    result1 = parachute.simulate(seed=1, scenario="nominal_calibration")
    result2 = parachute.simulate(seed=999, scenario="nominal_calibration")

    perf1 = result1["performance_metrics"]
    perf2 = result2["performance_metrics"]

    # Should be similar but not identical due to turbulence
    assert abs(perf1["descent_time_s"] - perf2["descent_time_s"]) < 50.0  # Allow more variation
    assert abs(perf1["landing_velocity_ms"] - perf2["landing_velocity_ms"]) < 2.0  # Allow more variation

    # But not exactly the same
    assert result1["aerodynamic_analysis"]["max_drag_force_N"] != result2["aerodynamic_analysis"]["max_drag_force_N"]
