import json
from pathlib import Path

import yaml

VALIDATION_DIR = Path(__file__).resolve().parents[1] / "validation"


def iter_validation_cases():
    for path in VALIDATION_DIR.iterdir():
        if path.is_dir():
            case = path / "case.yaml"
            report = path / "report.md"
            yield path.name, case, report


def test_all_validation_cases_have_metadata():
    missing = []
    for name, case_path, report_path in iter_validation_cases():
        if not case_path.exists() or not report_path.exists():
            missing.append(name)
    assert not missing, f"Validation cases missing metadata: {missing}"


def test_case_files_are_well_formed_yaml():
    for name, case_path, _ in iter_validation_cases():
        with case_path.open(encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        assert isinstance(data, dict), f"Case file {name} is not a mapping"
        assert "validation_assets" in data, f"Case file {name} lacks validation_assets"
        # ensure referenced assets exist when paths are relative
        assets = data.get("validation_assets", {})
        case_dir = case_path.parent
        for value in assets.values():
            if isinstance(value, str):
                asset_path = (case_dir / value).resolve()
                assert asset_path.exists(), f"Asset {value} missing for {name}"
            elif isinstance(value, list):
                for entry in value:
                    if isinstance(entry, str):
                        asset_path = (case_dir / entry).resolve()
                        assert asset_path.exists(), f"Asset {entry} missing for {name}"


def test_validation_notebook_exists():
    notebook = Path(__file__).resolve().parents[1] / "notebooks" / "ornithopter_fsi_validation.ipynb"
    assert notebook.exists()
    content = json.loads(notebook.read_text())
    assert "cells" in content and content["cells"], "Notebook should contain at least one cell"


def test_cli_validation_status_collection():
    from davinci_codex.cli import _collect_validation_status

    status = _collect_validation_status()
    names = {entry["name"] for entry in status}
    expected = {
        "validated_gear_lewis",
        "ornithopter_fsi",
        "cart_tribology",
        "parachute_drop",
        "mechanical_odometer_contact",
    }
    assert expected.issubset(names)
