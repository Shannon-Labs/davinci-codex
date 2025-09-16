# da Vinci Codex — Public-Domain Engineering Lab

A reproducible exploration of Leonardo da Vinci's civil inventions, rebuilt with modern analysis and open tooling. The project is a collaborative effort between Hunter M. Bown (Shannon Labs) and the GPT-5 Codex agent, documenting every step openly. Every artifact is released under permissive licenses (MIT for code, CC0 for generated media) so the community can study, remix, and extend the work safely.

## Safety and Scope
- Focus on non-weapon, non-harmful devices with educational or civic value.
- Source material originates from public-domain folios of Leonardo's notebooks; provenance is documented in `docs/`.
- Any design with ambiguous or risky applications is excluded or reframed toward benign outcomes.
- Simulations and prototypes prioritize safety margins, failure analyses, and ethical review before suggesting physical builds.

## Reproducing the Project
All steps run headless and are scripted.
```bash
make setup
make test
make demo
```
Additional commands (see `Makefile`) support linting, builds, and artifact generation for CI.

## Invention Index
| Invention | Status | Notes |
|-----------|--------|-------|
| ![status](https://img.shields.io/badge/status-in_progress-blue) [Aerial Screw Rotor Lab](docs/aerial_screw.md) | Modeling phase | Helical rotor lift feasibility using modern composites |
| ![status](https://img.shields.io/badge/status-prototype_ready-brightgreen) [Self-Propelled Cart](docs/self_propelled_cart.md) | Prototype-ready | Spring-driven automaton cart with reproducible CAD and sims |
| ![status](https://img.shields.io/badge/status-prototype_ready-brightgreen) [Mechanical Odometer Cart](docs/mechanical_odometer.md) | Prototype-ready | Survey cart with pebble-drop counter and calibration scripts |

_Status badges summarize the maturity of each module: planning → in_progress → validated._

## Repository Structure
```
.
├─ LICENSE / LICENSE-CC0
├─ README.md
├─ docs/            # provenance notes, feasibility reports
├─ notebooks/       # exploratory analysis (mirrored to docs via CI)
├─ src/             # python package with CLI + invention modules
├─ cad/             # parametric CAD scripts (no binary exports)
├─ sims/            # simulation configs and captured outputs
├─ tests/           # pytest suites per invention
├─ data/            # generated or metadata-only datasets
└─ .github/         # automation, issue/PR templates, CI
```

## Provenance & Licensing
- Original folio references are noted per module with catalog IDs and public-domain image links.
- Generated figures, meshes, and text are dedicated to the public domain via CC0 (`LICENSE-CC0`).
- External datasets or libraries retain their respective licenses and are cited in module READMEs.

## Contributing
We welcome pull requests that expand the catalog of safe, open, da Vinci-inspired inventions. See `CONTRIBUTING.md` for guidelines and `docs/index.md` for the roadmap. Please avoid introducing proprietary assets or unsafe concepts.

## Citation
If you build upon this project, cite the repository using the metadata in `CITATION.cff` and attribute Leonardo's original work per module's provenance notes.
