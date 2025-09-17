import pytest

from davinci_codex.safety import FailureMode, InventionFMEA


def test_failure_mode_rpn_property():
    failure = FailureMode(
        mode="Test",
        cause="Hypothetical",
        effect="Minor",
        severity=4,
        occurrence=3,
        detection=2,
        mitigation="Monitor",
    )
    assert failure.risk_priority_number == 24


def test_generate_fmea_report_sorts_failures():
    fmea = InventionFMEA()
    failures = fmea.analyze_ornithopter()
    report = fmea.generate_fmea_report(failures)

    assert report["max_rpn"] == max(item.risk_priority_number for item in failures)
    rpn_values = [entry["rpn"] for entry in report["failures"]]
    assert rpn_values == sorted(rpn_values, reverse=True)


def test_failure_mode_rejects_out_of_range_values():
    with pytest.raises(ValueError):
        FailureMode(
            mode="Invalid",
            cause="Test",
            effect="Test",
            severity=0,
            occurrence=5,
            detection=5,
            mitigation="None",
        )


def test_failure_mode_requires_integer_ratings():
    with pytest.raises(TypeError):
        FailureMode(
            mode="Invalid",
            cause="Test",
            effect="Test",
            severity=5,
            occurrence=5,
            detection=5.5,  # type: ignore[arg-type]
            mitigation="None",
        )


def test_failure_mode_requires_description():
    with pytest.raises(ValueError):
        FailureMode(
            mode="",
            cause="Test",
            effect="Test",
            severity=5,
            occurrence=5,
            detection=5,
            mitigation="None",
        )
