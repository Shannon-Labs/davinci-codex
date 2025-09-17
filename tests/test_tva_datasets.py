import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORNITHOPTER_DATA = ROOT / "tva" / "ornithopter" / "data" / "fsi_modal_response.csv"
PARACHUTE_DATA = ROOT / "tva" / "parachute" / "data" / "drop_profiles.csv"


EXPECTED_ORNITHOPTER_COLUMNS = {
    "time_s",
    "historical_lift_N",
    "modern_lift_N",
    "historical_root_moment_Nm",
    "modern_root_moment_Nm",
}

EXPECTED_PARACHUTE_COLUMNS = {
    "time_s",
    "historical_velocity_ms",
    "modern_velocity_ms",
    "historical_accel_ms2",
    "modern_accel_ms2",
}


def _read_header(path: Path) -> set[str]:
    with path.open(encoding="utf-8") as stream:
        reader = csv.reader(stream)
        header = next(reader)
    return set(header)


def test_fsi_dataset_present() -> None:
    assert ORNITHOPTER_DATA.exists(), "Ornithopter FSI dataset missing"
    assert _read_header(ORNITHOPTER_DATA) == EXPECTED_ORNITHOPTER_COLUMNS


def test_parachute_dataset_present() -> None:
    assert PARACHUTE_DATA.exists(), "Parachute drop dataset missing"
    assert _read_header(PARACHUTE_DATA) == EXPECTED_PARACHUTE_COLUMNS
