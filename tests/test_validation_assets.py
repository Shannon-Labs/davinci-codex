from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = ROOT / "validation"

EXPECTED_CASES = {
    "validated_gear_lewis": ["convergence.csv"],
    "ornithopter_fsi": ["timestep_convergence.csv"],
    "cart_tribology": ["load_sweep.csv"],
    "parachute_drop": ["descent_summary.csv", "benchmarks/drop_profiles.csv"],
    "mechanical_odometer_contact": [
        "contact_summary.csv",
        "benchmarks/slip_characterisation.csv",
    ],
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

        for asset in assets:
            asset_path = case_dir / asset
            assert asset_path.exists(), f"Validation asset {asset} missing for {slug}"
