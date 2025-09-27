from pathlib import Path
from typing import Optional

from davinci_codex.inventions import programmable_flute


def _write_params(path: Path, sequence: str = "[0, 1, 2, 3]") -> None:
    path.write_text(
        "\n".join(
            [
                "pipe_lengths_m: [0.42, 0.38, 0.34, 0.31]",
                "hole_positions_m: [0.08, 0.12, 0.16, 0.2]",
                "barrel_rotation_rpm: 24.0",
                "cam_lobe_count: 8",
                "airflow_rate_lps: 7.5",
                "valve_latency_s: 0.08",
                f"note_sequence: {sequence}",
                "air_noise_std: 0.06",
            ]
        )
        + "\n"
    )


def test_plan_reports_pipe_count(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(programmable_flute, "PARAM_FILE", param_file)
    payload = programmable_flute.plan()
    assert payload["assumptions"]["pipe_count"] == 4
    assert payload["assumptions"]["airflow_rate_lps"] == 7.5


def test_simulate_produces_artifacts(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file, "[0, 3, 1, 2, 0]")
    monkeypatch.setattr(programmable_flute, "PARAM_FILE", param_file)

    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target /= subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(programmable_flute, "ensure_artifact_dir", fake_dir)
    result = programmable_flute.simulate(seed=19)
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

    monkeypatch.setattr(programmable_flute, "ensure_artifact_dir", fake_dir)

    class DummyCAD:
        def export_mesh(self, path: Path, params: dict):
            path.write_text("mesh")

    monkeypatch.setattr(programmable_flute, "_cad_module", lambda: DummyCAD())
    programmable_flute.build()
    exported = list((tmp_path / programmable_flute.SLUG / "cad").glob("*.stl"))
    assert exported


def test_evaluate_returns_metrics(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(programmable_flute, "PARAM_FILE", param_file)
    payload = programmable_flute.evaluate()
    assert payload["practicality"]["mean_frequency_hz"] > 0
    assert isinstance(payload["validated"]["stable_pitch"], bool)

