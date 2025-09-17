# da Vinci Codex Documentation Index

## Purpose
The da Vinci Codex project reconstructs Leonardo da Vinci's civil, non-weapon inventions using modern engineering methods. It is co-created by Hunter Bown (Shannon Labs) and the GPT-5 Codex agent to keep the reconstruction process transparent and reproducible. Each module follows a consistent workflow: historical provenance, quantitative completion plan, computational implementation, feasibility and ethics review, and reproducible artifact packaging.

## Safety Scope
- Only non-harmful, non-weaponizable devices are explored.
- Medical concepts must meet contemporary safety expectations; speculative or risky ideas are deferred.
- All datasets, imagery, and text are public-domain or newly generated under CC0.

## Repository Guide
- `docs/<slug>.md` — Module reports with provenance, engineering math, assumptions, and experimental proposals.
- `docs/book/` — Jupyter Book configuration + build output for computational essays.
- `notebooks/` — Curated notebooks executed through the Jupyter Book build to accompany validation results.
- `src/davinci_codex/` — Python package delivering CLI entry points and invention APIs.
- `cad/` — Parametric CAD scripts (OpenSCAD, FreeCAD Python, etc.).
- `sims/` — Simulation configurations, solver outputs, and logs.
- `tests/` — Pytest suites validating math, data integrity, and deterministic behavior.

## 📦 Active Modules

| Module | Status | Description |
|--------|--------|--------------|
| **Aerial Screw Rotor Lab** | `in_progress` | Helical rotor lift feasibility using modern composites and aerodynamic simulation |
| **Self-Propelled Cart** | `prototype_ready` | Spring-driven automaton with parametric CAD models and kinematic simulation |
| **Mechanical Odometer** | `prototype_ready` | Survey cart with pebble-drop counter mechanism and precision calibration |
| **Ornithopter Flight Lab** | `validated` | Bio-inspired flapping-wing aircraft with composite materials and electric actuation |
| **Pyramid Parachute** | `validated` | Analysis and optimization of da Vinci's pyramid-shaped parachute with modern safety validation |

## 🗺️ Development Roadmap

### Near-term Goals
1. **Aerial Screw Rotor Lab** — Complete lift vs. mass validation with composite rotor experiments
2. **Self-Propelled Cart** — Workshop testing and path programming instrumentation
3. **Pyramid Parachute** — Wind tunnel testing and scale model validation
4. **Ornithopter Flight Lab** — Composite drivetrain implementation and flight control integration

### Future Inventions
- Hydraulic pumps and water lifting devices
- Mechanical clock mechanisms
- Bridge designs and structural innovations
- Musical instruments and acoustic devices

## Provenance Logging
Each module documents original folio references (e.g., Codex Atlanticus, folio numbers) and high-resolution scan sources with catalog identifiers. When direct image reproduction is ambiguous, descriptions and derived vector sketches are provided instead of scans.

## How to Contribute
- Review `CONTRIBUTING.md` for development workflow.
- Discuss new modules via `.github/ISSUE_TEMPLATE/feature.md`.
- Prioritize transparency in assumptions, calculations, and testing.

## 📧 Contact & Support
- **Issues & Features**: [GitHub Issues](https://github.com/Shannon-Labs/davinci-codex/issues)
- **Documentation**: [Project Website](https://shannon-labs.github.io/davinci-codex/)
- **Safety Concerns**: `safety@davinci-codex.org`
- **Maintainer**: Hunter Bown (Shannon Labs)
