"""Tests for the ornithopter TVA module."""

from pathlib import Path

from davinci_codex.tva import evaluate_viability


def test_viability_metrics_fail_historical_limits():
    result = evaluate_viability()
    assert result.power_margin_w < 0
    assert result.torque_margin_nm < 0
    assert 30 < result.fatigue_cycles < 80
    assert result.passes_power is False
    assert result.passes_fatigue is False


def test_viability_report_exists_and_mentions_numbers():
    report = Path("tva/ornithopter/viability_report.md")
    text = report.read_text(encoding="utf-8")
    assert "14.67 kW" in text
    assert "50 cycles" in text
    assert "973 N·m" in text
