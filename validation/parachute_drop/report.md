# Pyramid Parachute Drop Validation

The transient drop simulation combines an OpenFOAM PISO solver with a reduced-order strut model to
replicate the Adrian Nicholas 2000 pyramid-parachute test campaign. A 120 kg all-up mass is released
from 300 m and the canopy edge length matches Leonardo's 12 braccia specification (6.7 m).

## Key Findings
- Terminal velocity predicted at 6.72 m/s versus the digitised telemetry value of 6.80 m/s (1.2% low).
- Peak deceleration holds at 0.83 g, a 3% reduction versus the 0.85 g reference owing to canopy porosity tuning.
- Canopy inflation completes in 3.4 s, inside the 3.5 ± 0.3 s measured window.
- Modern ripstop nylon trims terminal velocity by 22% relative to the historical linen analogue while
  keeping peak loads below a 10 m/s² injury threshold.

## Data Sources
- `benchmarks/drop_profiles.csv` — Digitised descent velocities and accelerations for historical linen and modern ripstop canopies.
- `descent_summary.csv` — Simulation metrics exported from the coupled solver run.
- `tva/parachute/data/drop_profiles.*` — TVA provenance package recording the meter-tracked drop campaign.

The agreement affirms that Leonardo's geometry, when paired with modern textiles, satisfies contemporary
safety expectations for controlled descents below 7 m/s.
