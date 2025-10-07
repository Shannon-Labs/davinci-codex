"""
Comprehensive tests for Leonardo's Aerial Screw implementation.

This test suite validates the enhanced aerial screw functionality including:
- Advanced blade element momentum theory
- Historical accuracy and educational content
- Comprehensive performance analysis
- CAD model generation with multiple configurations
- Integration with multiphysics analysis
"""

from pathlib import Path
from typing import Optional
import numpy as np
import pytest

from davinci_codex.inventions import aerial_screw


class TestPlan:
    """Test comprehensive planning functionality."""

    def test_plan_contains_historical_context(self):
        """Verify plan includes detailed historical information."""
        payload = aerial_screw.plan()
        assert "origin" in payload
        assert "folio" in payload["origin"]
        assert "Codex Atlanticus" in payload["origin"]["folio"] and "869r" in payload["origin"]["folio"]
        assert "historical_context" in payload["origin"]
        assert "contemporary_works" in payload["origin"]["historical_context"]

    def test_plan_contains_engineering_principles(self):
        """Verify plan includes engineering education content."""
        payload = aerial_screw.plan()
        assert "engineering_principles" in payload
        assert "momentum_theory" in payload["engineering_principles"]
        assert "blade_element_theory" in payload["engineering_principles"]

    def test_plan_contains_comprehensive_assumptions(self):
        """Verify plan includes all necessary assumptions."""
        payload = aerial_screw.plan()
        assumptions = payload["assumptions"]
        assert assumptions["rotor_radius_m"] == aerial_screw.ROTOR_RADIUS
        assert "leonardo_radius_m" in assumptions
        assert "human_power_sustainable_W" in assumptions
        assert "gear_ratio" in assumptions

    def test_plan_contains_educational_outcomes(self):
        """Verify plan includes educational objectives."""
        payload = aerial_screw.plan()
        assert "educational_outcomes" in payload
        assert len(payload["educational_outcomes"]) > 3

    def test_plan_contains_safety_considerations(self):
        """Verify plan includes safety analysis."""
        payload = aerial_screw.plan()
        assert "safety_considerations" in payload
        assert len(payload["safety_considerations"]) > 3


class TestHelicalRotorAnalysis:
    """Test the advanced blade element momentum theory implementation."""

    def test_rotor_analysis_initialization(self):
        """Test HelicalRotorAnalysis class initialization."""
        rotor = aerial_screw.HelicalRotorAnalysis(
            radius=2.0,
            inner_radius=1.6,
            pitch=3.5,
            num_blades=1
        )
        assert rotor.radius == 2.0
        assert rotor.inner_radius == 1.6
        assert rotor.pitch == 3.5
        assert rotor.num_blades == 1

    def test_blade_geometry_computation(self):
        """Test blade geometry calculations."""
        rotor = aerial_screw.HelicalRotorAnalysis(2.0, 1.6, 3.5)
        chord, twist, thickness = rotor.compute_blade_geometry(1.8)
        assert chord > 0
        assert twist != 0
        assert thickness > 0

    def test_induced_velocity_calculation(self):
        """Test induced velocity calculations."""
        rotor = aerial_screw.HelicalRotorAnalysis(2.0, 1.6, 3.5)
        v_induced = rotor.compute_induced_velocity(100.0, 1.8)
        assert v_induced >= 0
        assert isinstance(v_induced, float)

    def test_element_force_calculation(self):
        """Test blade element force calculations."""
        rotor = aerial_screw.HelicalRotorAnalysis(2.0, 1.6, 3.5)
        dT, dQ, dP = rotor.compute_element_forces(100.0, 1.8)
        assert dT >= 0  # Thrust should be positive
        assert dQ >= 0  # Torque should be positive
        assert dP >= 0  # Power should be positive

    def test_performance_computation(self):
        """Test comprehensive performance calculation."""
        rotor = aerial_screw.HelicalRotorAnalysis(2.0, 1.6, 3.5)
        performance = rotor.compute_performance(100.0)
        required_keys = ['thrust', 'torque', 'power', 'tip_speed', 'tip_mach', 'figure_of_merit']
        for key in required_keys:
            assert key in performance
            assert performance[key] >= 0

    def test_performance_curve_generation(self):
        """Test performance curve data generation."""
        data = aerial_screw._performance_curve()
        required_arrays = ['rpm', 'thrust', 'torque', 'power', 'tip_speed', 'tip_mach', 'figure_of_merit']
        for array_name in required_arrays:
            assert array_name in data
            assert len(data[array_name]) > 0
            assert isinstance(data[array_name], np.ndarray)


class TestSimulation:
    """Test comprehensive simulation functionality."""

    def test_simulation_outputs_comprehensive_results(self, tmp_path, monkeypatch):
        """Test simulation produces comprehensive analysis results."""
        target_dir = tmp_path / "artifacts"

        def fake_ensure(slug: str, subdir: Optional[str] = None):
            path = target_dir / slug
            if subdir:
                path = path / subdir
            path.mkdir(parents=True, exist_ok=True)
            return path

        monkeypatch.setattr("davinci_codex.inventions.aerial_screw.ensure_artifact_dir", fake_ensure)
        results = aerial_screw.simulate(seed=0)

        # Check core performance metrics
        assert "performance" in results
        performance = results["performance"]
        assert performance["max_lift_N"] > 0
        assert performance["max_efficiency"] > 0
        assert performance["tip_mach_at_max_rpm"] < 1.0

        # Check human power feasibility
        assert "human_feasibility" in results
        feasibility = results["human_feasibility"]
        assert "single_operator" in feasibility
        assert "four_operators" in feasibility
        assert "geared_system" in feasibility

        # Check structural analysis
        assert "structural_analysis" in results
        structural = results["structural_analysis"]
        assert structural["max_tip_speed_m_s"] > 0

        # Check educational insights
        assert "educational_insights" in results
        insights = results["educational_insights"]
        assert "historical_significance" in insights
        assert "engineering_challenges" in insights

        # Check historical assessment
        assert "historical_assessment" in results
        assessment = results["historical_assessment"]
        assert "leonardos_concept_accuracy" in assessment
        assert "overall_feasibility_15th_century" in assessment

    def test_simulation_outputs_artifacts(self, tmp_path, monkeypatch):
        """Test simulation generates expected artifacts."""
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

        # Check that core artifacts exist
        for artifact in artifacts:
            assert artifact.exists(), f"Missing artifact {artifact}"

        # Check for expected file types
        artifact_names = [a.name for a in artifacts]
        assert any("performance.csv" in name for name in artifact_names)
        assert any("performance.png" in name for name in artifact_names)
        assert any("rotor_demo.gif" in name for name in artifact_names)
        assert any("educational_analysis.png" in name for name in artifact_names)

    def test_educational_plots_creation(self, tmp_path, monkeypatch):
        """Test educational plot generation."""
        target_dir = tmp_path / "artifacts"

        def fake_ensure(slug: str, subdir: Optional[str] = None):
            path = target_dir / slug
            if subdir:
                path = path / subdir
            path.mkdir(parents=True, exist_ok=True)
            return path

        monkeypatch.setattr("davinci_codex.inventions.aerial_screw.ensure_artifact_dir", fake_ensure)

        # Generate performance data
        data = aerial_screw._performance_curve()

        # Create educational plots
        plots = aerial_screw._create_educational_plots(target_dir / "educational.png", data)
        assert len(plots) > 0
        assert all(Path(p).exists() for p in plots)


class TestBuild:
    """Test comprehensive CAD build functionality."""

    def test_build_exports_multiple_configurations(self, tmp_path, monkeypatch):
        """Test build generates multiple CAD configurations."""
        target_dir = tmp_path / "artifacts"

        def fake_ensure(slug: str, subdir: Optional[str] = None):
            path = target_dir / slug
            if subdir:
                path = path / subdir
            path.mkdir(parents=True, exist_ok=True)
            return path

        monkeypatch.setattr("davinci_codex.inventions.aerial_screw.ensure_artifact_dir", fake_ensure)

        class DummyCadModule:
            def export_mesh(self, path, **kwargs):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("mesh")

        monkeypatch.setattr("davinci_codex.inventions.aerial_screw._cad_module", lambda: DummyCadModule())
        aerial_screw.build()

        # Check for multiple configurations
        cad_dir = target_dir / aerial_screw.SLUG / "cad"
        exported_files = list(cad_dir.glob("*.stl"))
        assert len(exported_files) >= 3  # Leonardo, modern, comparison

        # Check for multiple formats
        obj_files = list(cad_dir.glob("*.obj"))
        assert len(obj_files) >= 2  # At least Leonardo and modern in OBJ format

    def test_cad_module_integration(self):
        """Test CAD module can be imported and has expected functions."""
        cad_module = aerial_screw._cad_module()
        assert hasattr(cad_module, 'export_mesh')
        assert hasattr(cad_module, 'generate_mesh')
        assert callable(cad_module.export_mesh)
        assert callable(cad_module.generate_mesh)


class TestEvaluate:
    """Test comprehensive evaluation functionality."""

    def test_evaluate_reports_comprehensive_analysis(self):
        """Test evaluation provides comprehensive multi-perspective analysis."""
        payload = aerial_screw.evaluate()

        # Check practicality assessment
        assert "practicality" in payload
        practicality = payload["practicality"]
        assert "performance_metrics" in practicality
        assert "human_power_feasibility" in practicality
        assert "structural_feasibility" in practicality
        assert "control_challenges" in practicality
        assert "overall_assessment" in practicality

        # Check ethical assessment
        assert "ethics" in payload
        ethics = payload["ethics"]
        assert "risk_assessment" in ethics
        assert "safety_mitigations" in ethics
        assert "responsible_innovation" in ethics

        # Check speculative analysis
        assert "speculative" in payload
        speculative = payload["speculative"]
        assert "research_opportunities" in speculative
        assert "technological_challenges" in speculative
        assert "future_applications" in speculative
        assert "open_questions" in speculative

        # Check historical analysis
        assert "historical_analysis" in payload
        historical = payload["historical_analysis"]
        assert "leonardos_genius" in historical
        assert "historical_limitations" in historical
        assert "what_leonardo_got_right" in historical
        assert "what_leonardo_missed" in historical

        # Check educational value
        assert "educational_value" in payload
        educational = payload["educational_value"]
        assert "learning_objectives" in educational
        assert "interdisciplinary_connections" in educational
        assert "teaching_applications" in educational

    def test_evaluate_performance_metrics(self):
        """Test evaluation includes realistic performance metrics."""
        payload = aerial_screw.evaluate()
        practicality = payload["practicality"]["performance_metrics"]

        assert practicality["torque_at_100rpm_Nm"] > 0
        assert practicality["power_requirement_kW"] > 0
        assert practicality["efficiency_at_100rpm"] >= 0
        assert practicality["lift_at_100rpm_N"] >= 0

    def test_evaluate_feasibility_scores(self):
        """Test evaluation provides quantitative feasibility assessments."""
        payload = aerial_screw.evaluate()
        assessment = payload["practicality"]["overall_assessment"]

        assert "15th_century_feasibility_score" in assessment
        assert "modern_feasibility_score" in assessment
        assert "educational_value_score" in assessment
        assert "historical_significance_score" in assessment

        # Scores should be reasonable values
        for score_key, score_value in assessment.items():
            assert 0 <= score_value <= 1, f"Score {score_key} should be between 0 and 1"


class TestConstants:
    """Test that constants are properly defined and reasonable."""

    def test_physical_constants(self):
        """Test physical constants are reasonable."""
        assert aerial_screw.RHO_AIR > 1.0  # Air density should be around 1.2 kg/m³
        assert aerial_screw.GRAVITY > 9.0  # Gravity should be around 9.8 m/s²
        assert aerial_screw.SPEED_OF_SOUND > 300  # Speed of sound should be around 343 m/s

    def test_design_parameters(self):
        """Test design parameters are reasonable."""
        assert aerial_screw.LEONARDO_RADIUS > aerial_screw.ROTOR_RADIUS
        assert aerial_screw.LEONARDO_PITCH > aerial_screw.HELICAL_PITCH
        assert aerial_screw.ROTOR_RADIUS > aerial_screw.ROTOR_INNER_RADIUS
        assert aerial_screw.HELICAL_PITCH > 0

    def test_human_power_parameters(self):
        """Test human power parameters are realistic."""
        assert aerial_screw.HUMAN_POWER_SUSTAINABLE > 50  # Should be around 75W
        assert aerial_screw.HUMAN_POWER_PEAK > aerial_screw.HUMAN_POWER_SUSTAINABLE
        assert aerial_screw.MULTI_OPERATOR_POWER > aerial_screw.HUMAN_POWER_SUSTAINABLE
        assert aerial_screw.GEAR_RATIO > 1.0
        assert 0 < aerial_screw.GEAR_EFFICIENCY <= 1.0


class TestModuleMetadata:
    """Test module metadata and structure."""

    def test_module_constants(self):
        """Test required module constants are defined."""
        assert hasattr(aerial_screw, 'SLUG')
        assert hasattr(aerial_screw, 'TITLE')
        assert hasattr(aerial_screw, 'STATUS')
        assert hasattr(aerial_screw, 'SUMMARY')
        assert aerial_screw.SLUG == "aerial_screw"
        assert aerial_screw.STATUS in ["planning", "in_progress", "validated", "prototype_ready"]

    def test_required_functions(self):
        """Test required functions are implemented."""
        required_functions = ['plan', 'simulate', 'build', 'evaluate']
        for func_name in required_functions:
            assert hasattr(aerial_screw, func_name)
            assert callable(getattr(aerial_screw, func_name))


# Integration tests
class TestIntegration:
    """Integration tests for complete workflow."""

    def test_complete_workflow(self, tmp_path, monkeypatch):
        """Test complete workflow from plan to evaluation."""
        target_dir = tmp_path / "artifacts"

        def fake_ensure(slug: str, subdir: Optional[str] = None):
            path = target_dir / slug
            if subdir:
                path = path / subdir
            path.mkdir(parents=True, exist_ok=True)
            return path

        monkeypatch.setattr("davinci_codex.inventions.aerial_screw.ensure_artifact_dir", fake_ensure)

        # Test plan
        plan_result = aerial_screw.plan()
        assert "origin" in plan_result

        # Test simulate
        sim_result = aerial_screw.simulate(seed=0)
        assert "performance" in sim_result
        assert len(sim_result["artifacts"]) > 0

        # Test build
        class DummyCadModule:
            def export_mesh(self, path, **kwargs):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("mesh")

        monkeypatch.setattr("davinci_codex.inventions.aerial_screw._cad_module", lambda: DummyCadModule())
        aerial_screw.build()
        cad_files = list((target_dir / aerial_screw.SLUG / "cad").glob("*.stl"))
        assert len(cad_files) > 0

        # Test evaluate
        eval_result = aerial_screw.evaluate()
        assert "practicality" in eval_result
        assert "educational_value" in eval_result

    def test_performance_data_consistency(self):
        """Test that performance data is internally consistent."""
        data = aerial_screw._performance_curve()

        # Check that arrays have consistent lengths
        base_length = len(data["rpm"])
        for key, array in data.items():
            if isinstance(array, np.ndarray) and key != "leonardo_rpm" and key != "leonardo_power":
                assert len(array) == base_length, f"Array {key} has inconsistent length"

        # Check that performance relationships make sense
        assert np.all(data["thrust"] >= 0)
        assert np.all(data["power"] >= 0)
        assert np.all(data["torque"] >= 0)
        assert np.all(data["tip_speed"] >= 0)
        assert np.all(data["tip_mach"] >= 0)
        assert np.all(data["figure_of_merit"] >= 0)


# Legacy tests for backward compatibility
def test_plan_contains_key_metrics():
    """Legacy test - ensure backward compatibility."""
    payload = aerial_screw.plan()
    assert "origin" in payload
    assert payload["assumptions"]["rotor_radius_m"] == aerial_screw.ROTOR_RADIUS
    assert payload["governing_equations"], "Expected governing equations in plan output"


def test_simulation_outputs_artifacts(tmp_path, monkeypatch):
    """Legacy test - ensure backward compatibility."""
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
    assert results["performance"]["max_lift_N"] > 0
    assert results["performance"]["tip_mach_at_max_rpm"] < 1.0


def test_build_exports_mesh(tmp_path, monkeypatch):
    """Legacy test - ensure backward compatibility."""
    target_dir = tmp_path / "artifacts"

    def fake_ensure(slug: str, subdir: Optional[str] = None):
        path = target_dir / slug
        if subdir:
            path = path / subdir
        path.mkdir(parents=True, exist_ok=True)
        return path

    monkeypatch.setattr("davinci_codex.inventions.aerial_screw.ensure_artifact_dir", fake_ensure)

    class DummyCadModule:
        def export_mesh(self, path, **kwargs):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("mesh")

    monkeypatch.setattr("davinci_codex.inventions.aerial_screw._cad_module", lambda: DummyCadModule())
    aerial_screw.build()
    exported = list((target_dir / aerial_screw.SLUG / "cad").glob("*.stl"))
    assert exported, "Expected a mesh artifact"


def test_evaluate_reports_practicality():
    """Legacy test - ensure backward compatibility."""
    payload = aerial_screw.evaluate()
    assert "practicality" in payload
    assert payload["practicality"]["performance_metrics"]["torque_at_100rpm_Nm"] > 0
    assert isinstance(payload["ethics"]["risk_assessment"], dict)