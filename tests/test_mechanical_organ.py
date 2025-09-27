from pathlib import Path
from typing import Optional

from davinci_codex.inventions import mechanical_organ


def _write_params(path: Path, schedule: str = "[0, 1, 2, 1]") -> None:
    path.write_text(
        "\n".join(
            [
                "pipe_lengths_m: [0.45, 0.4, 0.36, 0.32]",
                "pipe_diameters_m: [0.06, 0.055, 0.05, 0.045]",
                "bellows_pressure_kpa: 6.5",
                "wind_chest_volume_l: 12.0",
                "barrel_rotation_rpm: 18.0",
                f"note_schedule: {schedule}",
                "airflow_noise_std: 0.08",
            ]
        )
        + "\n"
    )


def test_plan_reports_pipe_count(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(mechanical_organ, "PARAM_FILE", param_file)
    payload = mechanical_organ.plan()
    assert payload["assumptions"]["pipe_count"] == 4
    assert payload["assumptions"]["bellows_pressure_kpa"] == 6.5


def test_simulate_creates_artifacts(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file, "[0, 1, 2, 3, 2, 1]")
    monkeypatch.setattr(mechanical_organ, "PARAM_FILE", param_file)

    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target /= subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_organ, "ensure_artifact_dir", fake_dir)
    result = mechanical_organ.simulate(seed=7)
    for artifact in result["artifacts"]:
        assert Path(artifact).exists()
    assert result["mean_frequency_hz"] > 0


def test_build_exports_mesh(monkeypatch, tmp_path):
    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target /= subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_organ, "ensure_artifact_dir", fake_dir)

    class DummyCAD:
        def export_mesh(self, path: Path, params: dict):
            path.write_text("mesh")

    monkeypatch.setattr(mechanical_organ, "_cad_module", lambda: DummyCAD())
    mechanical_organ.build()
    exported = list((tmp_path / mechanical_organ.SLUG / "cad").glob("*.stl"))
    assert exported


def test_evaluate_returns_metrics(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(mechanical_organ, "PARAM_FILE", param_file)
    payload = mechanical_organ.evaluate()
    assert payload["practicality"]["mean_frequency_hz"] > 0
    assert isinstance(payload["validated"]["stable_pitch"], bool)

