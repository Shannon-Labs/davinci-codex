from pathlib import Path
from typing import Optional

from davinci_codex.inventions import aerial_screw


def test_plan_contains_key_metrics():
    payload = aerial_screw.plan()
    assert "origin" in payload
    assert payload["assumptions"]["rotor_radius_m"] == aerial_screw.ROTOR_RADIUS
    assert payload["governing_equations"], "Expected governing equations in plan output"


def test_simulation_outputs_artifacts(tmp_path, monkeypatch):
    target_dir = tmp_path / "artifacts"

    def fake_ensure(slug: str, subdir: Optional[str] = None):
        path = target_dir / slug
        if subdir:
            path = path / subdir
        path.mkdir(parents=True, exist_ok=True)
        return path

    monkeypatch.setattr("davinci_codex.inventions.aerial_screw.ensure_artifact_dir", fake_ensure)
    results = aerial_screw.simulate(seed=0)
    artifacts = [Path(p) for p in results["artifacts"]]
    for artifact in artifacts:
        assert artifact.exists(), f"Missing artifact {artifact}"
    assert results["max_lift_N"] > 0
    assert results["tip_mach_at_max_rpm"] < 1.0


def test_build_exports_mesh(tmp_path, monkeypatch):
    target_dir = tmp_path / "artifacts"

    def fake_ensure(slug: str, subdir: Optional[str] = None):
        path = target_dir / slug
        if subdir:
            path = path / subdir
        path.mkdir(parents=True, exist_ok=True)
        return path

    monkeypatch.setattr("davinci_codex.inventions.aerial_screw.ensure_artifact_dir", fake_ensure)

    class DummyCadModule:
        def export_mesh(self, path):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("mesh")

    monkeypatch.setattr("davinci_codex.inventions.aerial_screw._cad_module", lambda: DummyCadModule())
    aerial_screw.build()
    exported = list((target_dir / aerial_screw.SLUG / "cad").glob("*.stl"))
    assert exported, "Expected a mesh artifact"


def test_evaluate_reports_practicality():
    payload = aerial_screw.evaluate()
    assert "practicality" in payload
    assert payload["practicality"]["torque_at_100rpm_Nm"] > 0
    assert payload["ethics"]["risk"].startswith("Low")
