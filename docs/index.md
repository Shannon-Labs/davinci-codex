# da Vinci Codex Documentation Index

## Purpose
The da Vinci Codex project reconstructs Leonardo da Vinci's civil, non-weapon inventions using modern engineering methods. Each module follows a consistent workflow: historical provenance, quantitative completion plan, computational implementation, feasibility and ethics review, and reproducible artifact packaging.

## Safety Scope
- Only non-harmful, non-weaponizable devices are explored.
- Medical concepts must meet contemporary safety expectations; speculative or risky ideas are deferred.
- All datasets, imagery, and text are public-domain or newly generated under CC0.

## Repository Guide
- `docs/<slug>.md` — Module reports with provenance, engineering math, assumptions, and experimental proposals.
- `notebooks/` — Optional exploratory analysis in Jupyter; exported to Markdown/HTML via CI for archival.
- `src/davinci_codex/` — Python package delivering CLI entry points and invention APIs.
- `cad/` — Parametric CAD scripts (OpenSCAD, FreeCAD Python, etc.).
- `sims/` — Simulation configurations, solver outputs, and logs.
- `tests/` — Pytest suites validating math, data integrity, and deterministic behavior.

## Active Modules
- Aerial Screw Rotor Lab — Lift feasibility simulations and CAD.
- Self-Propelled Cart — Spring-driven automaton with CAD + YAML-configured dynamics.
- Mechanical Odometer Cart — Error modeling scripts with calibration guides.

## Roadmap
1. **Aerial Screw Rotor Lab** — Continue validating lift vs. mass with composite rotor experiments.
2. **Self-Propelled Cart** — Prototype-ready for workshop testing; next focus on path programming instrumentation.
3. Ornithopter Glider Study — Compare flapping and fixed-wing energy budgets for safe gliding demonstrations.

## Provenance Logging
Each module documents original folio references (e.g., Codex Atlanticus, folio numbers) and high-resolution scan sources with catalog identifiers. When direct image reproduction is ambiguous, descriptions and derived vector sketches are provided instead of scans.

## How to Contribute
- Review `CONTRIBUTING.md` for development workflow.
- Discuss new modules via `.github/ISSUE_TEMPLATE/feature.md`.
- Prioritize transparency in assumptions, calculations, and testing.

## Contact
For questions or safety escalations, reach maintainers at `safety@davinci-codex.org`.
