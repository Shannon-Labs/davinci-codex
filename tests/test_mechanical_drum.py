from pathlib import Path
from typing import Optional

from davinci_codex.inventions import mechanical_drum


def _write_params(path: Path, beat_angles: str) -> None:
    path.write_text(
        "\n".join(
            [
                "drum_radius_m: 0.15",
                "drum_length_m: 0.3",
                "pin_count: 16",
                "rotation_speed_rpm: 60",
                "gear_ratio: 1.0",
                f"beat_angles_deg: {beat_angles}",
                "noise_std: 0.05",
            ]
        )
        + "\n"
    )


def test_plan_returns_expected_fields(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file, "[0, 45, 90, 135, 180, 225, 270, 315]")
    monkeypatch.setattr(mechanical_drum, "PARAM_FILE", param_file)
    payload = mechanical_drum.plan()
    assert payload["assumptions"]["drum_radius_m"] == 0.15
    assert "governing_equations" in payload


def test_simulate_creates_artifacts(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file, "[0, 90, 180, 270]")
    monkeypatch.setattr(mechanical_drum, "PARAM_FILE", param_file)

    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target = target / subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_drum, "ensure_artifact_dir", fake_dir)
    result = mechanical_drum.simulate(seed=42)
    for artifact in result["artifacts"]:
        assert Path(artifact).exists()
    assert result["mean_interval_s"] > 0


def test_build_exports_mesh(monkeypatch, tmp_path):
    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target = target / subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_drum, "ensure_artifact_dir", fake_dir)

    class DummyCAD:
        def export_mesh(self, path: Path, params: dict):
            path.write_text("mesh")

    monkeypatch.setattr(mechanical_drum, "_cad_module", lambda: DummyCAD())
    mechanical_drum.build()
    exported = list((tmp_path / mechanical_drum.SLUG / "cad").glob("*.stl"))
    assert exported


def test_evaluate_flags_accuracy(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file, "[0, 45, 90, 135, 180, 225, 270, 315]")
    monkeypatch.setattr(mechanical_drum, "PARAM_FILE", param_file)
    payload = mechanical_drum.evaluate()
    assert payload["practicality"]["mean_interval_s"] > 0
    assert isinstance(payload["validated"]["low_error"], bool)
