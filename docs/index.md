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

## 📘 Interactive Essays
- Build locally with `make book` (Jupyter Book executes the curated notebooks).
- Generated HTML lives in `docs/book/_build/html/`; open `index.html` to preview before publishing.
- GitHub Pages will host the collection at <https://shannon-labs.github.io/davinci-codex/book/> once enabled.
- Available chapters: gear bending validation, ornithopter FSI convergence, rolling friction tribology, and supporting physics derivations.

## 🧪 Validation Briefs
- [Parachute Safety Dossier](parachute_safety_dossier.md) — turbulence scenarios, tensile coupons, and hazard analysis for prototype readiness.
- [Revolving Bridge Modernization](revolving_bridge.md) — rotation profile CSVs, counterweight calibration workflow, and acceptance metrics.
- [Ornithopter Validation Log](ornithopter_validation.md) — dyno, modal, and telemetry summaries satisfying acceptance targets.

## 📦 Active Modules

| Module | Status | Description |
|--------|--------|--------------|
| [**Aerial Screw Rotor Lab**](aerial_screw.md) | `validated` | Helical rotor lift feasibility with packaged simulation artifacts and torque-balancing frame design |
| [**Self-Propelled Cart**](self_propelled_cart.md) | `prototype_ready` | Spring-driven automaton with parametric CAD models and kinematic simulation |
| [**Mechanical Odometer**](mechanical_odometer.md) | `prototype_ready` | Survey cart with pebble-drop counter mechanism and precision calibration |
| [**Pyramid Parachute**](parachute.md) | `prototype_ready` | Safety dossier with turbulence scenarios, tensile coupons, and drop telemetry linked in [Parachute Safety Dossier](parachute_safety_dossier.md) |
| [**Self-Supporting Revolving Bridge**](revolving_bridge.md) | `in_progress` | Rotation profile CSVs, counterweight treatise, and stability proofs available for field deployment planning |
| [**Ornithopter Flight Lab**](ornithopter.md) | `in_progress` | Validation assets (dyno, modal survey, telemetry) summarized in [Ornithopter Validation Log](ornithopter_validation.md) |

## 🗺️ Development Roadmap

### Near-term Goals
1. **Pyramid Parachute** — Execute full-scale drop validation and integrate reserve deployment drills into the safety dossier
2. **Self-Supporting Revolving Bridge** — Fabricate counterweight prototypes and plan live rotation drills informed by the new rotation profile CSVs
3. **Ornithopter Flight Lab** — Transition from tethered ground-runs to free-flight envelope expansion using logged telemetry acceptance checks
4. **Self-Propelled Cart** — Package workshop testing scripts and path programming instrumentation for outreach deployments

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
