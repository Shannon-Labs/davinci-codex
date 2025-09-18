from __future__ import annotations

import csv
from pathlib import Path

import yaml

from davinci_codex.inventions import ornithopter

VALIDATION_DIR = Path(__file__).resolve().parents[1] / "validation" / ornithopter.SLUG


def test_acceptance_targets_present():
    params = ornithopter._load_parameters()  # type: ignore[attr-defined]
    targets = params.acceptance_targets
    assert "thrust_to_weight_margin" in targets
    assert "modal_frequency_factor" in targets
    assert "battery_temperature_rise_C" in targets
    assert "fsi_divergence_allowed" in targets


def test_bench_dyno_exceeds_thrust_margin():
    params = ornithopter._load_parameters()  # type: ignore[attr-defined]
    targets = params.acceptance_targets
    margin = float(targets["thrust_to_weight_margin"])
    gross_weight = params.total_mass_kg * ornithopter.GRAVITY

    bench_path = VALIDATION_DIR / "bench_dyno.yaml"
    with bench_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    thrust_values = [point["thrust_N"] for point in data["rpm_points"]]
    assert max(thrust_values) >= gross_weight * (1.0 + margin)


def test_modal_frequency_margin():
    params = ornithopter._load_parameters()  # type: ignore[attr-defined]
    targets = params.acceptance_targets
    modal_factor = float(targets["modal_frequency_factor"])

    modal_path = VALIDATION_DIR / "modal_survey.yaml"
    with modal_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    first_mode = data["modal_results"][0]["frequency_hz"]
    required = params.flap_frequency_hz * modal_factor
    assert first_mode >= required


def test_telemetry_summary_meets_limits():
    params = ornithopter._load_parameters()  # type: ignore[attr-defined]
    targets = params.acceptance_targets
    telemetry_path = VALIDATION_DIR / "telemetry_summary.csv"
    metrics = {}
    with telemetry_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            value = row["value"]
            if value.lower() in {"true", "false"}:
                metrics[row["metric"]] = value.lower() == "true"
            else:
                metrics[row["metric"]] = float(value)

    assert metrics["battery_temperature_rise_C"] <= float(targets["battery_temperature_rise_C"])
    assert metrics["thrust_to_weight_margin"] >= float(targets["thrust_to_weight_margin"])
    assert metrics["telemetry_duration_s"] >= float(targets["telemetry_duration_s"])
    assert metrics["fsi_converged"] == (not bool(targets["fsi_divergence_allowed"]))
