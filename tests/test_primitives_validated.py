import pytest

from davinci_codex.primitives import ValidatedGear


def test_validated_gear_performs_validation():
    gear = ValidatedGear(teeth=24, module=3.0)
    assert gear.bending_stress is not None
    assert gear.converged_stress is not None
    assert gear.discretization_error is not None
    assert gear.discretization_error >= 0.0


def test_validated_gear_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        ValidatedGear(teeth=6, module=2.5)
