from pathlib import Path
from typing import Optional

from davinci_codex.inventions import self_propelled_cart


def test_plan_exposes_parameters(monkeypatch, tmp_path):
    param_file = tmp_path / "parameters.yaml"
    param_file.write_text(
        "mass_kg: 10\n"
        "wheel_radius_m: 0.1\n"
        "drag_coefficient: 0.5\n"
        "frontal_area_m2: 0.1\n"
        "spring_k_Nm: 5.0\n"
        "spring_max_theta_rad: 4.0\n"
        "rolling_coeff: 0.02\n"
        "gear_efficiency: 0.8\n"
        "timestep_s: 0.1\n"
        "duration_s: 2.0\n"
    )
    monkeypatch.setattr(self_propelled_cart, "PARAM_FILE", param_file)
    payload = self_propelled_cart.plan()
    assert payload["assumptions"]["mass_kg"] == 10
    assert "governing_equations" in payload


def test_simulation_generates_artifacts(monkeypatch, tmp_path):
    param_file = tmp_path / "parameters.yaml"
    param_file.write_text(
        "mass_kg: 20\n"
        "wheel_radius_m: 0.2\n"
        "drag_coefficient: 0.6\n"
        "frontal_area_m2: 0.15\n"
        "spring_k_Nm: 10.0\n"
        "spring_max_theta_rad: 6.0\n"
        "rolling_coeff: 0.01\n"
        "gear_efficiency: 0.85\n"
        "timestep_s: 0.05\n"
        "duration_s: 5.0\n"
    )
    monkeypatch.setattr(self_propelled_cart, "PARAM_FILE", param_file)

    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / "artifacts" / slug
        if subdir:
            target = target / subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(self_propelled_cart, "ensure_artifact_dir", fake_dir)
    results = self_propelled_cart.simulate(seed=123)
    for artifact in results["artifacts"]:
        assert Path(artifact).exists()
    assert results["distance_m"] > 0
    assert results["runtime_s"] > 0


def test_build_exports_mesh(monkeypatch, tmp_path):
    def fake_dir(slug: str, subdir: Optional[str] = None):
        target = tmp_path / slug
        if subdir:
            target = target / subdir
        target.mkdir(parents=True, exist_ok=True)
        return target

    monkeypatch.setattr(self_propelled_cart, "ensure_artifact_dir", fake_dir)

    class DummyCAD:
        def export_mesh(self, path: Path):
            path.write_text("mesh")

    monkeypatch.setattr(self_propelled_cart, "_cad_module", lambda: DummyCAD())
    self_propelled_cart.build()
    exported = list((tmp_path / self_propelled_cart.SLUG / "cad").glob("*.stl"))
    assert exported


def test_evaluate_reports_feasibility(monkeypatch, tmp_path):
    param_file = tmp_path / "parameters.yaml"
    param_file.write_text(
        "mass_kg: 18\n"
        "wheel_radius_m: 0.18\n"
        "drag_coefficient: 0.6\n"
        "frontal_area_m2: 0.12\n"
        "spring_k_Nm: 18.0\n"
        "spring_max_theta_rad: 5.0\n"
        "rolling_coeff: 0.02\n"
        "gear_efficiency: 0.8\n"
        "timestep_s: 0.05\n"
        "duration_s: 4.0\n"
    )
    monkeypatch.setattr(self_propelled_cart, "PARAM_FILE", param_file)
    payload = self_propelled_cart.evaluate()
    assert payload["practicality"]["distance_m"] >= 0
    assert payload["ethics"]["risk"].startswith("Low")
    assert isinstance(payload["validated"]["ready_for_workshop"], bool)
