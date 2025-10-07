from pathlib import Path
from typing import Optional

from davinci_codex.inventions import mechanical_odometer


def test_plan_returns_expected_fields(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    param_file.write_text(
        "wheel_radius_m: 0.2\n"
        "wheel_width_m: 0.05\n"
        "drive_gear_teeth: 60\n"
        "counter_gear_teeth: 10\n"
        "bucket_capacity: 50\n"
        "pebbles_per_drop: 1\n"
        "slip_std_percent: 0.5\n"
        "calibration_error_percent: 0.25\n"
        "distance_grid_m: [50, 100]\n"
    )
    monkeypatch.setattr(mechanical_odometer, "PARAM_FILE", param_file)
    payload = mechanical_odometer.plan()
    assert payload["assumptions"]["wheel_radius_m"] == 0.2
    assert "governing_equations" in payload


def test_simulate_creates_artifacts(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    param_file.write_text(
        "wheel_radius_m: 0.25\n"
        "wheel_width_m: 0.05\n"
        "drive_gear_teeth: 80\n"
        "counter_gear_teeth: 8\n"
        "bucket_capacity: 20\n"
        "pebbles_per_drop: 1\n"
        "slip_std_percent: 0.3\n"
        "calibration_error_percent: 0.1\n"
        "distance_grid_m: [100, 200]\n"
        "wheel_wood_type: oak\n"
        "gear_material: bronze\n"
        "terrain_type: packed_earth\n"
        "pebble_shape: rounded\n"
        "weather_conditions: dry\n"
    )
    monkeypatch.setattr(mechanical_odometer, "PARAM_FILE", param_file)

    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target = target / subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_odometer, "ensure_artifact_dir", fake_dir)
    result = mechanical_odometer.simulate(seed=42)
    for artifact in result["artifacts"]:
        assert Path(artifact).exists()
    # Updated to use new nested structure
    assert result["performance_metrics"]["max_error_percent"] >= 0
    assert "performance_grade" in result["performance_metrics"]
    assert "educational_notes" in result


def test_build_exports_mesh(monkeypatch, tmp_path):
    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target = target / subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_odometer, "ensure_artifact_dir", fake_dir)

    class DummyCAD:
        def export_mesh(self, path: Path):
            path.write_text("mesh")

    monkeypatch.setattr(mechanical_odometer, "_cad_module", lambda: DummyCAD())
    mechanical_odometer.build()
    exported = list((tmp_path / mechanical_odometer.SLUG / "cad").glob("*.stl"))
    assert exported


def test_evaluate_flags_accuracy(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    param_file.write_text(
        "wheel_radius_m: 0.24\n"
        "wheel_width_m: 0.05\n"
        "drive_gear_teeth: 90\n"
        "counter_gear_teeth: 9\n"
        "bucket_capacity: 60\n"
        "pebbles_per_drop: 1\n"
        "slip_std_percent: 0.4\n"
        "calibration_error_percent: 0.2\n"
        "distance_grid_m: [50, 100, 150]\n"
        "wheel_wood_type: oak\n"
        "gear_material: bronze\n"
        "terrain_type: packed_earth\n"
        "pebble_shape: rounded\n"
        "weather_conditions: dry\n"
    )
    monkeypatch.setattr(mechanical_odometer, "PARAM_FILE", param_file)
    payload = mechanical_odometer.evaluate()
    # Updated to use new nested structure
    assert payload["practicality"]["measurement_accuracy"]["max_error_percent"] >= 0
    assert isinstance(payload["validation_status"]["performance_targets"]["within_two_percent"], bool)
    assert "educational_value" in payload
    assert "safety_and_ethics" in payload
