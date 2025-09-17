# Mechanical Odometer Contact Validation

Chrono-based rolling contact simulations were benchmarked against workshop slip measurements on packed
earth, flagstone, and cobblestone courses. Each run used the 0.22 m wheel diameter and 120:12 gear train
specified for the mechanical odometer cart.

## Highlights
- Mean slip delta between simulation and measurements: 0.29 percentage points (target ≤ 0.50).
- Maximum slip deviation occurs on cobblestone at 600 N: 0.40 percentage points under the 0.50 limit.
- Wheel circumference error after 1 km: 0.56%, below the 0.60% acceptance band for survey tasks.
- Encoder drift after 100 drops remains below 0.18%, providing consistent pebble counts across terrains.

## Assets
- `benchmarks/slip_characterisation.csv` — Digitised workshop slip baselines.
- `contact_summary.csv` — Simulation metrics exported from the Chrono validation suite.
- `tva/mechanical_odometer/data/slip_characterisation.*` — TVA provenance for raw measurements and metadata.

These results validate that the odometer maintains sub-percent distance accuracy when compensated for
wheel slip across representative Renaissance street surfaces.
