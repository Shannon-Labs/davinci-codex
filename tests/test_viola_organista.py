from pathlib import Path
from typing import Optional

from davinci_codex.inventions import viola_organista


def _write_params(path: Path, sequence: str = "[0, 1, 2, 1]") -> None:
    path.write_text(
        "\n".join(
            [
                "string_lengths_m: [0.62, 0.59, 0.56]",
                "string_tensions_n: [240.0, 225.0, 210.0]",
                "string_linear_density_kg_per_m: [0.005, 0.0048, 0.0046]",
                "wheel_surface_speed_m_per_s: 0.65",
                "bow_contact_time_s: 0.35",
                "key_velocity_profile: [0.8, 0.6, 0.7, 0.9]",
                f"note_sequence: {sequence}",
                "bow_noise_std: 0.05",
            ]
        )
        + "\n"
    )


def test_plan_reports_string_count(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(viola_organista, "PARAM_FILE", param_file)
    payload = viola_organista.plan()
    assert payload["assumptions"]["string_count"] == 3
    assert payload["assumptions"]["wheel_surface_speed_m_per_s"] == 0.65


def test_simulate_writes_artifacts(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file, "[0, 2, 1, 2, 0]")
    monkeypatch.setattr(viola_organista, "PARAM_FILE", param_file)

    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target /= subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(viola_organista, "ensure_artifact_dir", fake_dir)
    result = viola_organista.simulate(seed=11)
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

    monkeypatch.setattr(viola_organista, "ensure_artifact_dir", fake_dir)

    class DummyCAD:
        def export_mesh(self, path: Path, params: dict):
            path.write_text("mesh")

    monkeypatch.setattr(viola_organista, "_cad_module", lambda: DummyCAD())
    viola_organista.build()
    exported = list((tmp_path / viola_organista.SLUG / "cad").glob("*.stl"))
    assert exported


def test_evaluate_returns_metrics(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(viola_organista, "PARAM_FILE", param_file)
    payload = viola_organista.evaluate()
    assert payload["practicality"]["mean_frequency_hz"] > 0
    assert isinstance(payload["validated"]["expressive_control"], bool)

