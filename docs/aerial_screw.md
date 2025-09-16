# Aerial Screw Rotor Lab

## Original Context
- **Folio:** Codex Atlanticus, 869r (Biblioteca Ambrosiana)
- **Public-domain scan:** https://www.leonardodigitale.com/opera/ca-869-r/
- **Leonardo's intent:** A human-powered helical rotor meant to "screw" into the air and lift a passenger platform.
- **Missing elements:** No numerical lift estimates, unspecified materials for the rotor skin, absent counter-torque solution, and no stability or control surfaces.

## Modernized Completion
- Replace linen-hemp membrane with flax-carbon composite shell bonded to a lightweight aluminum mast.
- Size rotor radius at 2.0 m with 2.5 helical turns and 3.5 m pitch to maximize swept area while staying transportable.
- Model downwash via actuator-disk momentum theory adjusted by an empirical slip factor derived from screw propellers.
- Add torque-balancing frame assumptions (contra-rotating ring or reaction wheel) to prevent platform spin.
- Provide parametric CAD mesh for the rotor ribbon and mast generated through `trimesh` sweeping.

## Build / Run
```bash
make setup
make test
make demo  # runs aerial screw simulation + evaluation snapshot
```

## Artifacts
- `artifacts/aerial_screw/sim/performance.csv` — RPM sweep with lift, torque, power predictions.
- `artifacts/aerial_screw/sim/performance.png` — Lift vs. RPM with power overlay and hover requirement.
- `artifacts/aerial_screw/sim/rotor_demo.gif` — Animated rotor visualization for presentations.
- `artifacts/aerial_screw/cad/aerial_screw_mesh.stl` — Parametric rotor + mast mesh (generated, not tracked).

## Feasibility Notes
- Hover requires ~110 RPM with ~35 kW shaft power; human power alone cannot sustain flight.
- Peak tip Mach number stays <0.3, so compressibility effects remain minor.
- Torque exceeds 1.6 kN·m at 100 RPM, demanding rigid counter-rotation or reaction-wheel compensation.
- Composite blade must withstand centrifugal stress >40 MPa; suggested layup factors in 2× safety margin.

## Next Steps
1. Validate slip factor via wind-tunnel or large fan instrumentation at 1:3 scale.
2. Perform finite-element analysis on mast-blade junction to confirm torsional stiffness.
3. Explore multi-rotor cluster or coaxial design to halve required torque per rotor.
4. Test lightweight electric drivetrain options delivering >30 kW continuous with torque control.
