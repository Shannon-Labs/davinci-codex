# TVA — Ornithopter Analysis

Historical engineering analyses quantifying why Leonardo's ornithopter stalled in the Renaissance.

Contents:
- `materials.yaml` — fir/rawhide spring properties, fatigue S–N parameters, and torque limits.
- `human_power_profiles.csv` — sustained and peak leg-crank power benchmarks from historical records.
- `analysis_notes.md` — engineering assumptions and next-step experiments.
- `viability_report.md` — narrative summary of TVA run (updated 2025-02-14).

Simulation code lives in `src/davinci_codex/tva/ornithopter.py` and is exercised via `tests/test_tva_ornithopter.py`.
