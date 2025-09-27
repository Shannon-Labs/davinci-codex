from pathlib import Path
from typing import Optional

from davinci_codex.inventions import mechanical_trumpeter


def _write_params(path: Path, sequence: str = "[0, 2, 4, 5]") -> None:
    path.write_text(
        "\n".join(
            [
                "bore_length_m: 1.35",
                "bell_diameter_m: 0.12",
                "mouthpiece_length_m: 0.14",
                "plenum_pressure_kpa: 8.0",
                "valve_latencies_s: [0.12, 0.1, 0.14, 0.11]",
                f"note_sequence: {sequence}",
                "breath_profile: [1.0, 0.9, 1.1, 1.0]",
                "timbre_noise_std: 0.04",
            ]
        )
        + "\n"
    )


def test_plan_reports_fundamental(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(mechanical_trumpeter, "PARAM_FILE", param_file)
    payload = mechanical_trumpeter.plan()
    assert payload["assumptions"]["fundamental_frequency_hz"] > 0
    assert payload["assumptions"]["sequence_length"] == 4


def test_simulate_creates_artifacts(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file, "[0, 3, 5, 7, 5]")
    monkeypatch.setattr(mechanical_trumpeter, "PARAM_FILE", param_file)

    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target /= subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_trumpeter, "ensure_artifact_dir", fake_dir)
    result = mechanical_trumpeter.simulate(seed=17)
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

    monkeypatch.setattr(mechanical_trumpeter, "ensure_artifact_dir", fake_dir)

    class DummyCAD:
        def export_mesh(self, path: Path, params: dict):
            path.write_text("mesh")

    monkeypatch.setattr(mechanical_trumpeter, "_cad_module", lambda: DummyCAD())
    mechanical_trumpeter.build()
    exported = list((tmp_path / mechanical_trumpeter.SLUG / "cad").glob("*.stl"))
    assert exported


def test_evaluate_returns_metrics(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(mechanical_trumpeter, "PARAM_FILE", param_file)
    payload = mechanical_trumpeter.evaluate()
    assert payload["practicality"]["frequency_error_hz"] >= 0
    assert isinstance(payload["validated"]["stable_pitch"], bool)

