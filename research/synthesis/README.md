# Synthesis Engine

Modernization stack translating da Vincis intent into working prototypes. Core elements:

- `materials/` — aerospace-grade composites, additive manufacturing alloys, actuator catalogs.
- `cad/` — parametric model generators (Python + OpenSCAD/OCC), finite-element prep, meshing.
- `simulation/` — aero/hydro/structural solvers (PyDy, MuJoCo, Bullet) with validation harnesses.
- `controllers/` — embedded firmware, sensing, and feedback control prototypes.

Synthesis consumes TVA constraints to propose feasible bill-of-materials, produce CAD/mesh artefacts, and run performance validations, emitting reproducible build manifests for IP Nexus.
