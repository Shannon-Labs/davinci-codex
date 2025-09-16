"""Validate the ornithopter intent.json structure."""

import json
from pathlib import Path

import pytest

INTENT_PATH = Path("anima/ornithopter/intent.json")


@pytest.fixture(scope="module")
def intent_payload() -> dict:
    with INTENT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_intent_contains_required_sections(intent_payload: dict) -> None:
    for key in ["components", "joints", "control_paths", "uncertainties"]:
        assert key in intent_payload
        assert isinstance(intent_payload[key], list)
        assert intent_payload[key], f"Expected non-empty list for {key}"


def test_components_have_materials(intent_payload: dict) -> None:
    for component in intent_payload["components"]:
        assert "id" in component
        assert "modern_material" in component
        assert "renaissance_material" in component


def test_control_paths_map_inputs_outputs(intent_payload: dict) -> None:
    for path in intent_payload["control_paths"]:
        assert set(path.keys()) >= {"id", "inputs", "outputs"}
        assert path["inputs"]
        assert path["outputs"]
