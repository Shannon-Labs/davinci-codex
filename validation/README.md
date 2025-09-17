# Verification & Validation Playbook

This directory captures benchmark evidence demonstrating that each solver and modelling approach is trustworthy before it is applied to Leonardo's inventions. Populate one subfolder per invention or primitive (e.g., `ornithopter/`, `validated_gear/`).

## Required Artifacts
- `case.yaml`: metadata file enumerating solver, version, turbulence/contact models, mesh generator, numerical tolerances, and hardware used.
- `benchmarks/`: analytical solutions, experimental datasets, or literature references used for comparison.
- `convergence/`: plots and tables showing spatial/temporal refinement studies (e.g., Richardson extrapolation, CFL sweeps).
- `report.md`: concise narrative summarising validation results, discrepancies, and corrective actions.

## Workflow
1. Select a canonical benchmark (e.g., NACA oscillating airfoil for flapping validation, Hertzian contact for tribology, ASME gear tests for bending stresses).
2. Replicate the benchmark using the same solver configuration intended for Leonardo's design.
3. Record mesh/time-step refinement results until changes fall below acceptance criteria (<2% relative error unless historical uncertainty dictates otherwise).
4. Archive scripts and post-processing notebooks under `sims/` so reviewers can reproduce the evidence.

Maintaining a rigorous V&V trail ensures the computational archaeology work remains defensible in academic and engineering forums.

## Current Benchmarks
- `naca0012_oscillation/`: Coupled OpenFOAM–FEniCSx FSI validation of NASA TM 84245 forced oscillation data.
- `lewis_gear_bending/`: CalculiX structural verification of the Lewis 1892 gear tooth bending experiment.
- `rolling_friction_rig/`: Chrono tribology calibration against Bowden & Tabor rolling friction measurements.
- `parachute_drop/`: OpenFOAM PISO vs. Adrian Nicholas 2000 telemetry for the pyramid parachute release.
- `mechanical_odometer_contact/`: Chrono slip modelling for the odometer cart against packed earth, flagstone, and cobblestone measurements.

Each case directory contains `case.yaml`, a detailed `report.md`, digitised benchmark data under `benchmarks/`, and convergence plots within `convergence/`.
