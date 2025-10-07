"""Integration tests for complete simulation pipelines."""

import json
import tempfile
from pathlib import Path

import pytest

from davinci_codex.pipelines import run_ornithopter_pipeline
from davinci_codex.registry import get_invention, list_inventions


class TestFullPipelineIntegration:
    """Test complete simulation pipelines from start to finish."""

    def test_complete_ornithopter_pipeline(self):
        """Test the complete ornithopter pipeline including synthesis."""

        # Run the full pipeline
        result = run_ornithopter_pipeline(seed=42, duration_s=5.0)

        # Verify pipeline structure
        assert isinstance(result, dict)
        assert "analysis" in result
        assert "synthesis" in result
        assert "validation" in result

        # Verify analysis results
        analysis = result["analysis"]
        assert "performance" in analysis
        assert "safety_factor" in analysis

        # Verify synthesis results
        synthesis = result["synthesis"]
        assert "controllers" in synthesis
        assert "duration_s" in synthesis

        # Verify validation results
        validation = result["validation"]
        assert "fmea" in validation

    def test_invention_simulation_to_visualization_pipeline(self):
        """Test pipeline from simulation through visualization generation."""

        invention = get_invention("parachute")

        # Run simulation
        sim_results = invention.module.simulate(seed=42)
        assert isinstance(sim_results, dict)

        # Generate evaluation (includes visualization)
        eval_results = invention.module.evaluate()
        assert isinstance(eval_results, dict)

        # Verify evaluation contains expected components
        assert "feasibility" in eval_results
        assert "safety" in eval_results
        assert "fmea" in eval_results

    def test_batch_simulation_pipeline(self):
        """Test batch processing of multiple inventions."""

        inventions = list_inventions()
        results = {}

        # Process each invention
        for spec in inventions:
            try:
                # Simulate
                sim_result = spec.module.simulate(seed=42)

                # Evaluate
                eval_result = spec.module.evaluate()

                # Store combined results
                results[spec.slug] = {
                    "simulation": sim_result,
                    "evaluation": eval_result,
                    "status": "success"
                }

            except Exception as e:
                results[spec.slug] = {
                    "status": "failed",
                    "error": str(e)
                }

        # Verify all inventions processed
        assert len(results) == len(inventions)

        # Verify most inventions succeeded
        successful = sum(1 for r in results.values() if r["status"] == "success")
        success_rate = successful / len(results)
        assert success_rate >= 0.8, f"Success rate too low: {success_rate:.2%}"

    def test_simulation_with_uncertainty_quantification(self):
        """Test simulation pipeline with uncertainty quantification."""

        invention = get_invention("ornithopter")

        # Test with different uncertainty scenarios
        base_result = invention.module.simulate(seed=42)

        # Verify uncertainty handling in results
        if "uncertainty" in base_result:
            uncertainty = base_result["uncertainty"]
            assert isinstance(uncertainty, dict)

            # Should contain confidence intervals or uncertainty bounds
            assert any(key in uncertainty for key in [
                "confidence_intervals", "uncertainty_bounds", "sensitivity_analysis"
            ])

    def test_historical_provenance_integration(self):
        """Test integration with historical provenance system."""

        invention = get_invention("mechanical_odometer")

        # Get planning information (should include provenance)
        plan = invention.module.plan()
        assert isinstance(plan, dict)

        # Verify provenance information is included
        if "provenance" in plan:
            provenance = plan["provenance"]
            assert isinstance(provenance, dict)

            # Should contain manuscript references
            expected_fields = ["manuscript", "folio", "description"]
            assert any(field in provenance for field in expected_fields)

    def test_safety_analysis_integration(self):
        """Test integration of safety analysis throughout pipeline."""

        invention = get_invention("parachute")

        # Get evaluation with safety analysis
        evaluation = invention.module.evaluate()

        # Verify safety analysis is present
        assert "safety" in evaluation
        evaluation["safety"]

        # Verify FMEA analysis
        assert "fmea" in evaluation
        fmea = evaluation["fmea"]

        # FMEA should contain failure modes and risk assessments
        assert isinstance(fmea, dict)
        if "failure_modes" in fmea:
            assert isinstance(fmea["failure_modes"], list)

    def test_material_database_integration(self):
        """Test integration with Renaissance materials database."""

        # This test would verify that simulations properly use
        # historical material properties from the database

        invention = get_invention("self_propelled_cart")

        # Get planning information
        plan = invention.module.plan()

        # Verify material specifications
        if "materials" in plan:
            materials = plan["materials"]
            assert isinstance(materials, dict)

            # Should reference historical materials
            for material_spec in materials.values():
                if isinstance(material_spec, dict):
                    # Should have historical context
                    assert any(key in material_spec for key in [
                        "historical_name", "renaissance_source", "period_properties"
                    ])

    def test_cad_model_generation_integration(self):
        """Test integration with CAD model generation."""

        invention = get_invention("aerial_screw")

        # Test build functionality
        try:
            invention.module.build()
            # If build succeeds, it should generate appropriate files
            # This is a placeholder - actual implementation would check
            # for generated CAD files, STL exports, etc.

        except NotImplementedError:
            # Some inventions may not have build implemented yet
            pytest.skip(f"Build not implemented for {invention.slug}")
        except Exception as e:
            pytest.fail(f"Build failed with error: {e}")

    def test_validation_case_integration(self):
        """Test integration with validation case system."""

        # Test validation cases that exist in the validation/ directory
        validation_root = Path(__file__).parents[2] / "validation"

        if validation_root.exists():
            validation_dirs = [d for d in validation_root.iterdir() if d.is_dir()]

            # Test a few validation cases
            for val_dir in validation_dirs[:3]:  # Test first 3 cases
                case_file = val_dir / "case.yaml"
                val_dir / "report.md"

                if case_file.exists():
                    # Load and validate case configuration
                    import yaml
                    with case_file.open() as f:
                        case_config = yaml.safe_load(f)

                    assert isinstance(case_config, dict)

                    # Should have essential validation metadata
                    expected_fields = ["name", "description", "validation_type"]
                    present_fields = [field for field in expected_fields if field in case_config]
                    assert len(present_fields) > 0, f"No expected fields found in {case_file}"

    def test_end_to_end_data_flow(self):
        """Test complete data flow from input to output artifacts."""

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test complete flow for a simple invention
            invention = get_invention("mechanical_drum")

            # 1. Get planning data
            plan = invention.module.plan()

            # Save plan to temporary file
            plan_file = temp_path / "plan.json"
            with plan_file.open("w") as f:
                json.dump(plan, f, indent=2)

            # 2. Run simulation
            sim_results = invention.module.simulate(seed=42)

            # Save simulation results
            sim_file = temp_path / "simulation.json"
            with sim_file.open("w") as f:
                json.dump(sim_results, f, indent=2)

            # 3. Run evaluation
            eval_results = invention.module.evaluate()

            # Save evaluation results
            eval_file = temp_path / "evaluation.json"
            with eval_file.open("w") as f:
                json.dump(eval_results, f, indent=2)

            # Verify all files were created and contain valid data
            assert plan_file.exists()
            assert sim_file.exists()
            assert eval_file.exists()

            # Verify file sizes (should contain meaningful data)
            assert plan_file.stat().st_size > 50
            assert sim_file.stat().st_size > 50
            assert eval_file.stat().st_size > 50

    def test_error_handling_and_recovery(self):
        """Test error handling throughout the pipeline."""

        invention = get_invention("ornithopter")

        # Test simulation with invalid parameters
        try:
            # This should either handle gracefully or raise informative error
            result = invention.module.simulate(seed=-1)  # Potentially invalid seed

            # If it succeeds, result should still be valid
            assert isinstance(result, dict)

        except ValueError as e:
            # Should provide clear error message
            assert len(str(e)) > 10

        except Exception as e:
            # Should not raise unexpected exceptions
            pytest.fail(f"Unexpected exception type: {type(e).__name__}: {e}")
