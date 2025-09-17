"""Document rolling-loss validation calculations for the self-propelled cart."""

import csv
import pathlib
from statistics import mean

DATA = pathlib.Path("data/tribology/cart_friction_curve.csv")


def load_data(path: pathlib.Path):
    with path.open() as handle:
        reader = csv.DictReader(row for row in handle if not row.startswith("#"))
        rows = [{
            "time_s": float(row["time_s"]),
            "torque_Nm": float(row["torque_Nm"]),
            "load_N": float(row["load_N"]),
        } for row in reader]
    return rows


def rolling_coefficient(rows):
    radius = 0.18  # m
    mean_torque = mean(row["torque_Nm"] for row in rows)
    mean_load = mean(row["load_N"] for row in rows)
    return mean_torque / (radius * mean_load)


def main() -> None:
    if not DATA.exists():
        raise SystemExit(f"Missing data file: {DATA}")
    rows = load_data(DATA)
    coeff = rolling_coefficient(rows)
    print(f"Rolling resistance coefficient: {coeff:.3f}")


if __name__ == "__main__":
    main()
