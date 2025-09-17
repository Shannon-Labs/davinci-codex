import pytest

from davinci_codex.primitives import ValidatedGear


def test_validated_gear_performs_validation():
    gear = ValidatedGear(teeth=24, module=3.0)
    assert gear.bending_stress is not None
    assert gear.converged_stress is not None
    assert gear.discretization_error is not None
    assert gear.discretization_error >= 0.0
    assert gear.safety_factor is not None and gear.safety_factor > 1.5


def test_pitch_radius_matches_standard_definition():
    gear = ValidatedGear(teeth=20, module=2.5, design_torque=0.5)
    expected_radius = (gear.teeth * gear.module) / 2000.0
    assert gear.pitch_radius() == pytest.approx(expected_radius)


def test_richardson_extrapolation_restores_exact_solution():
    gear = ValidatedGear(teeth=24, module=3.0)
    meshes = [1000, 4000, 16000]
    exact = 100.0
    coefficient = 5.0
    estimates = [exact + coefficient / (m**2) for m in meshes]
    result = gear.richardson_extrapolation(estimates, meshes)
    assert result.exact_solution == pytest.approx(exact, rel=1e-6)
    assert result.error_estimate == pytest.approx(abs(exact - estimates[-1]))


def test_validated_gear_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        ValidatedGear(teeth=6, module=2.5)


def test_validated_gear_flags_excessive_torque():
    with pytest.raises(ValueError):
        ValidatedGear(teeth=24, module=3.0, design_torque=40.0)
