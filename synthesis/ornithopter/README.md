# Synthesis — Ornithopter Build Package

This folder tracks the modern engineering stack that will deliver a flyable ornithopter prototype.

Current contents:
- `cad/` — OpenSCAD generator (`cad/ornithopter/model.py`) producing frame, drivetrain placeholders, assembly manifest, and mass budget.
- `simulation/` — `flapping_model.py` aeroelastic solver exporting stroke/lift profiles and energy usage.
- `controllers/` — Control architecture notes with PX4 mixer layout and safety requirements.
- `bom/` — CSV bill of materials with supplier references and mass estimates.

Initial goals: confirm weight budget < 65 kg empty, simulate lift > 1.2× gross mass at 2.5 Hz flapping, and validate drivetrain torque margins with 2× 2 kW motors.
