from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = ROOT / "validation"

EXPECTED_CASES = {
    "validated_gear_lewis": {"convergence": "convergence.csv"},
    "ornithopter_fsi": {"convergence": "timestep_convergence.csv"},
    "cart_tribology": {"convergence": "load_sweep.csv"},
}


def test_validation_directory_exists() -> None:
    assert VALIDATION_DIR.exists(), "validation/ directory is missing"


def test_validation_assets_present() -> None:
    for slug, assets in EXPECTED_CASES.items():
        case_dir = VALIDATION_DIR / slug
        assert case_dir.exists(), f"validation/{slug} missing"

        case_file = case_dir / "case.yaml"
        report_file = case_dir / "report.md"
        assert case_file.exists(), f"case.yaml missing for {slug}"
        assert report_file.exists(), f"report.md missing for {slug}"

        with case_file.open(encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        assert isinstance(data, dict)

        conv = case_dir / assets["convergence"]
        assert conv.exists(), f"Convergence data missing for {slug}"
