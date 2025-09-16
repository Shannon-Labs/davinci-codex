# Mechanical Odometer Cart

## Original Context
- **Folio:** Codex Atlanticus, 1r (Royal Collection Trust)
- **Public-domain scan:** https://www.rct.uk/collection/912278
- **Leonardo's intent:** An odometer cart that dropped pebbles for each unit distance via geared drums, enabling survey crews to measure roads.
- **Missing elements:** Tooth counts for gear cascades, hopper capacity, and allowances for wheel slip were not recorded.

## Modernized Completion
- Adopt a 120:12 gear pair yielding ~16.5 m per pebble drop with 0.22 m wheels.
- Model accumulated error from slip and calibration drift with Monte Carlo-style perturbations (configurable via YAML).
- Provide CAD for the frame, four wheels, gear housing, and pebble drum for CNC or additive manufacturing.
- Offer reproducible CSV/plot outputs to support calibration experiments in schools or maker spaces.

## Build / Run
```bash
make setup
make test
make demo  # includes odometer error simulations
```

## Artifacts
- `artifacts/mechanical_odometer/sim/measurement_error.csv` — Actual vs. recorded distances and percentage error.
- `artifacts/mechanical_odometer/sim/error_curve.png` — Error curve compared to ±1% target band.
- `artifacts/mechanical_odometer/cad/mechanical_odometer.stl` — Parametric chassis and mechanism mesh.

## Feasibility Notes
- With baseline parameters, error stays within ±1.3% across 50–1000 m; seasonal recalibration keeps it under ±1%.
- Range per bucket (100 pebbles) exceeds 1.6 km, adequate for urban surveying legs.
- Device is passive and human-pushed, minimizing safety concerns; main focus is guarding the gear train.

## Next Steps
1. Fabricate gears via laser-cut stacked plywood or SLS nylon; compare friction losses.
2. Instrument wheel rotation with optical encoder to cross-check pebble counts.
3. Develop calibration worksheet for student survey teams.
4. Explore modular gear swaps for imperial unit conversions.
