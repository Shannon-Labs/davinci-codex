"""Tests for da Vinci's pyramid parachute module."""

import math

import pytest

from davinci_codex.inventions import parachute


def test_module_attributes():
    """Verify module exports required attributes."""
    assert parachute.SLUG == "parachute"
    assert parachute.TITLE == "Pyramid Parachute"
    assert parachute.STATUS == "in_progress"
    assert "pyramid" in parachute.SUMMARY.lower()


def test_plan_calculations():
    """Verify planning calculations are physically reasonable."""
    plan = parachute.plan()

    # Check structure
    assert "origin" in plan
    assert "modern_design" in plan
    assert "materials" in plan
    assert "performance" in plan

    # Check origin reference
    assert "Codex Atlanticus" in plan["origin"]["reference"]
    assert "381v" in plan["origin"]["reference"]

    # Check dimensions
    design = plan["modern_design"]
    assert design["canopy_size_m"] == pytest.approx(7.0, rel=0.1)
    assert design["base_area_m2"] == pytest.approx(49.0, rel=0.1)
    assert design["drag_coefficient"] == parachute.DRAG_COEFFICIENT_PYRAMID

    # Check materials are lighter than historical
    materials = plan["materials"]
    assert materials["canopy_density_kg_m2"] < 0.5  # Lighter than linen
    assert materials["frame_mass_kg"] < 50  # Lighter than wood equivalent

    # Check performance
    perf = plan["performance"]
    assert 5.0 <= perf["terminal_velocity_ms"] <= 10.0  # Reasonable descent speed
    assert perf["safe_landing"] is True  # Must be safe
    assert perf["descent_time_from_1000m"] > 100  # Takes time to descend


def test_simulate_descent():
    """Test descent simulation produces valid trajectory."""
    result = parachute.simulate(seed=42)

    # Check result structure
    assert "descent_time_s" in result
    assert "landing_velocity_ms" in result
    assert "safe_landing" in result
    assert "artifacts" in result

    # Check physics
    assert result["descent_time_s"] > 100  # Reasonable descent time
    assert 5.0 <= result["landing_velocity_ms"] <= 10.0
    assert result["landing_velocity_kmh"] == pytest.approx(
        result["landing_velocity_ms"] * 3.6, rel=0.01
    )
    assert result["safe_landing"] is True

    # Check artifacts were created
    assert "plot" in result["artifacts"]
    assert "trajectory_csv" in result["artifacts"]


def test_terminal_velocity_physics():
    """Verify terminal velocity calculation is correct."""
    # At terminal velocity: Weight = Drag
    # mg = 0.5 * rho * Cd * A * v^2
    # v = sqrt(2mg / (rho * Cd * A))

    plan_data = parachute.plan()
    total_mass = plan_data["performance"]["total_system_mass_kg"]
    base_area = plan_data["modern_design"]["base_area_m2"]

    expected_terminal = math.sqrt(
        (2 * total_mass * parachute.GRAVITY) /
        (parachute.RHO_AIR * parachute.DRAG_COEFFICIENT_PYRAMID * base_area)
    )

    assert plan_data["performance"]["terminal_velocity_ms"] == pytest.approx(
        expected_terminal, rel=0.01
    )


def test_evaluate_feasibility():
    """Test evaluation produces comprehensive assessment."""
    result = parachute.evaluate()

    # Check structure
    assert "feasibility" in result
    assert "safety" in result
    assert "historical_significance" in result
    assert "modern_improvements" in result
    assert "ethics" in result
    assert "recommendation" in result

    # Check feasibility assessment
    feasibility = result["feasibility"]
    assert feasibility["technical"] == "VALIDATED"
    assert feasibility["landing_safety"] is True

    # Check safety assessment
    safety = result["safety"]
    assert safety["landing_velocity_assessment"] in ["SAFE", "MARGINAL"]
    assert "structural_integrity" in safety

    # Check historical significance
    historical = result["historical_significance"]
    assert historical["ahead_of_time_years"] > 300  # Way ahead of its time
    assert "First documented parachute" in historical["innovation"]

    # Check recommendation
    assert result["recommendation"] == "BUILD_PROTOTYPE"


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
    result1 = parachute.simulate(seed=123)
    result2 = parachute.simulate(seed=123)

    assert result1["descent_time_s"] == result2["descent_time_s"]
    assert result1["landing_velocity_ms"] == result2["landing_velocity_ms"]
    assert result1["max_velocity_ms"] == result2["max_velocity_ms"]


def test_different_seeds_produce_variation():
    """Verify different seeds produce slightly different results (turbulence)."""
    result1 = parachute.simulate(seed=1)
    result2 = parachute.simulate(seed=999)

    # Should be similar but not identical due to turbulence
    assert abs(result1["descent_time_s"] - result2["descent_time_s"]) < 5.0
    assert abs(result1["landing_velocity_ms"] - result2["landing_velocity_ms"]) < 0.5

    # But not exactly the same
    assert result1["max_drag_force_N"] != result2["max_drag_force_N"]