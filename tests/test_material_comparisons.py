import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "materials" / "material_comparisons.csv"


def _percentage_change(old: float, new: float) -> float:
    return (new - old) / old * 100.0


def test_material_comparisons_exist() -> None:
    assert DATA_FILE.exists(), "material_comparisons.csv missing"


def test_improvement_percentages_match_values() -> None:
    with DATA_FILE.open(encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)

    inventions = {row["invention"] for row in rows}
    assert {"ornithopter", "self_propelled_cart", "aerial_screw"}.issubset(inventions)

    for row in rows:
        historic = float(row["historical_value"])
        modern = float(row["modern_value"])
        expected = round(_percentage_change(historic, modern), 2)
        stored = round(float(row["improvement_pct"]), 2)
        assert abs(expected - stored) < 0.01, (
            f"Improvement mismatch for {row['invention']} {row['metric']}"
        )
