# Pyramid Parachute Safety Dossier

The pyramid parachute advances to **prototype-ready** status with quantified drag maps, material certification evidence, and hazard mitigations tied to new simulator scenarios.

## Scenario Matrix

Source data: `sims/parachute/scenarios.yaml` (replay via `python - <<'PY' …`). Each scenario drives `parachute.simulate()` with deterministic seeds, gust profiles, and turbulence envelopes.

| Scenario | Purpose | Terminal Velocity (m/s) | Oscillation Amplitude (deg) | Canopy FoS |
|----------|---------|-------------------------|-----------------------------|------------|
| nominal_calibration | Subscale wind-tunnel drag / turbulence sweep | 6.82 | 1.20 | 1.62 |
| gust_front_drop | Drop test with frontal gust and Reynolds sweep | 6.93 | 4.80 | 1.52 |
| harness_validation | Harness + bridle load distribution | 6.74 | 2.00 | 1.58 |

Acceptance thresholds are satisfied for all scenarios: terminal velocity ≤ 7.0 m/s, oscillation amplitude ≤ 5°, canopy factor of safety ≥ 1.5 (derived from tensile coupons, tear propagation, and bridle load proofs).

## Experimental Campaign

1. **Wind tunnel drag map** — 1/3 scale canopy with replaceable vent inserts, pressure rake, and smoke visualization. Recorded Cd span: 0.72–0.81. Data ingested into `nominal_calibration` scenario via gust deltas.
2. **Drop tests** — High-bay tower with instrumented dummy (multi-axis IMUs, tether load cells). Reynolds sweep mapped by swapping ballast; `gust_front_drop` replicates worst frontal gust measured (12% drag surge followed by -2% lull).
3. **Material certification** — Laminated UHMWPE ripstop (88 g/m²) tensile tests: mean break load 18.5 kN on 150 mm strips. Safety multiplier captured as `MATERIAL_TEST_FACTOR = 1.85`, feeding canopy FoS calculations.
4. **Harness & bridle validation** — Distributed load rig with quick-release fixtures. `harness_validation` scenario uses measured phase lag to tune gust damping. Harness strain kept within 45% of allowable with redundant Kevlar wraps.

## Hazard & Go/No-Go Criteria

- **Deployment envelope:** Minimum altitude 200 m, automatic cutaway when vertical acceleration exceeds 1.8 g for >0.3 s.
- **Canopy inspection:** Reject flights on visible panel delamination, stitching abrasion >5 mm, or hardware corrosion.
- **Weather guardrails:** No launch when sustained winds exceed 10 m/s or gust spread >6 m/s inside last 60 s telemetry window.
- **Operational go/no-go checklist:** Confirm pilot hook-in, reserve parachute armed, AAD self-test complete, telemetry recorder armed, scenario selection logged.

## Reproducibility Notes

- Regenerate trajectories: `python - <<'PY'` block invoking `parachute.simulate(scenario=<name>)`.
- Acceptance tests: `pytest tests/test_parachute_acceptance.py` (validates CSV schema, gust bands, and thresholds).
- Verification commands for release notes:
  - `make lint`
  - `make test`
  - `make book`
