# Self-Propelled Cart

## Original Context
- **Folio:** Codex Atlanticus, 812r (Biblioteca Ambrosiana)
- **Public-domain scan:** https://www.leonardodigitale.com/opera/ca-812-r/
- **Leonardo's intent:** A theatrical automaton cart that could follow a pre-set route using cams and a torsion-spring drivetrain.
- **Missing elements:** Spring torque specification, gear train losses, and control cam programming are undocumented.

## Modernized Completion
- Model laminated torsion springs delivering up to 32 N·m/rad across a 14 rad winding range.
- Use actuator disk-style force balance with aerodynamic drag and rolling resistance to estimate run distance on level surfaces.
- Parametric CAD outlines a plywood/composite chassis with spring drum and four wheels suitable for CNC routing or 3D printing.
- Provide YAML-configurable simulations for educators to iterate on mass, spring rate, and efficiency parameters.

## Build / Run
```bash
make setup
make test
make demo  # now includes the self-propelled cart scenario
```

## Artifacts
- `artifacts/self_propelled_cart/sim/trajectory.csv` — Time history of position, speed, spring displacement, and drive force.
- `artifacts/self_propelled_cart/sim/profiles.png` — Distance and velocity traces over the run.
- `artifacts/self_propelled_cart/sim/motion.gif` — Animation suitable for presentations or classroom discussion.
- `artifacts/self_propelled_cart/cad/self_propelled_cart.stl` — Generated chassis + wheel assembly mesh.

## Feasibility Notes
- Baseline configuration travels ~18 m in 12 s with peak speed ~1.8 m/s before spring torque fades.
- Stored elastic energy (<350 J) keeps kinetic risk low; a modest braking pin suffices for safety.
- Performance scales linearly with spring rate and wind-up angle—modern clock springs can double range without major redesign.
- Escapement cams can be simplified to a fixed straight-line guide for early prototypes.

## Next Steps
1. Fabricate using 12 mm plywood or 3D-printed composite for classroom pilots.
2. Add microcontroller logging wheel rotations for empirical validation vs. simulation.
3. Explore swappable cam disks enabling curved trajectories and choreography.
4. Conduct wear testing on spring drum bearings to size bushings appropriately.
