from pathlib import Path
from typing import Optional

from davinci_codex.inventions import mechanical_carillon


def _write_params(path: Path, sequence: str = "[0, 1, 2, 3]") -> None:
    path.write_text(
        "\n".join(
            [
                "bell_masses_kg: [12.0, 10.5, 9.0, 7.5]",
                "bell_frequencies_hz: [523.25, 466.16, 392.00, 329.63]",
                "striker_mass_kg: 2.5",
                "striker_arm_length_m: 0.45",
                "drum_radius_m: 0.25",
                "rotation_speed_rpm: 12.0",
                f"strike_sequence: {sequence}",
                "timing_noise_std: 0.05",
            ]
        )
        + "\n"
    )


def test_plan_reports_counts(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(mechanical_carillon, "PARAM_FILE", param_file)
    payload = mechanical_carillon.plan()
    assert payload["assumptions"]["bell_count"] == 4
    assert payload["assumptions"]["rotation_period_s"] > 0


def test_simulate_produces_artifacts(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file, "[0, 2, 1, 3, 0]")
    monkeypatch.setattr(mechanical_carillon, "PARAM_FILE", param_file)

    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target /= subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_carillon, "ensure_artifact_dir", fake_dir)
    result = mechanical_carillon.simulate(seed=5)
    for artifact in result["artifacts"]:
        assert Path(artifact).exists()
    assert result["mean_impact_energy_j"] > 0


def test_build_exports_mesh(monkeypatch, tmp_path):
    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target /= subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(mechanical_carillon, "ensure_artifact_dir", fake_dir)

    class DummyCAD:
        def export_mesh(self, path: Path, params: dict):
            path.write_text("mesh")

    monkeypatch.setattr(mechanical_carillon, "_cad_module", lambda: DummyCAD())
    mechanical_carillon.build()
    exported = list((tmp_path / mechanical_carillon.SLUG / "cad").glob("*.stl"))
    assert exported


def test_evaluate_returns_metrics(monkeypatch, tmp_path):
    param_file = tmp_path / "params.yaml"
    _write_params(param_file)
    monkeypatch.setattr(mechanical_carillon, "PARAM_FILE", param_file)
    payload = mechanical_carillon.evaluate()
    assert payload["practicality"]["mean_impact_energy_j"] >= 0
    assert isinstance(payload["validated"]["consistent_timing"], bool)

