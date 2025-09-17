# Computational Completion Methodology

The da Vinci Codex project advances from exploratory simulation toward a digital dissertation that reconstructs Leonardo da Vinci's complete mechanical corpus. "Computational completion" denotes the disciplined process of recovering intent from folio sketches, expressing that intent as executable models, and validating performance against historical constraints. This document records the methodology that every invention reconstruction must follow.

## 1. Research Framing
- **Historical scope**: Catalogue all ~500 known mechanical inventions across the Codex Atlanticus, Madrid Codices, Codex Leicester, Codex Arundel, Paris Manuscripts, and Windsor collections.
- **Research questions**: (a) Could Leonardo's mechanisms function with Renaissance-era materials and fabrication tolerances? (b) What previously overlooked inventions demonstrate transformative potential? (c) How does Leonardo's systematic reuse of mechanical primitives reveal integrated manufacturing systems?
- **Scholarly apparatus**: Maintain folio-level provenance with primary sources, peer-reviewed historiography, and modern engineering references documented in `references.bib`.

## 2. Evidence Acquisition
1. **Manuscript digitisation**: Each folio enters the `PROVENANCE/` registry with image metadata, transcription confidence, and archive identifiers.
2. **Mirror-script transcription**: Dual-pass OCR plus paleographic verification capture Leonardo's annotations. Ambiguities are flagged for expert review.
3. **Geometric extraction**: Computer vision recovers dimensions, proportions, and implied constraints. Measurements retain uncertainty bounds tied to scan resolution and draughting ambiguity.
4. **Materials linkage**: Every component references `materials/renaissance_db.yaml` to declare period-accurate mechanical properties (density, modulus, fatigue limits) with explicit uncertainty distributions sourced from archaeometallurgy and forestry studies.

## 3. Computational Completion Principles
- **Historical fidelity first**: Reconstructions prioritise period feasible geometry, actuation and materials. When the sketch omits a dimension or tolerance, we expose the assumption in the PROVENANCE file and carry its epistemic uncertainty through UQ.
- **Documenting modern interventions**: Any deviation from Renaissance context (e.g., composite spars, electric actuation, modern sensors) is catalogued in `synthesis/` with justification, allowing readers to separate historical capability from modern extrapolation.
- **Comparative analysis**: Each invention is analysed in two passes—**Historical Baseline** (Renaissance materials/constraints) and **Modern Counterfactual** (lightweight composites, low-friction bearings). Comparative reports quantify the performance delta.

## 4. Model Construction
1. **Primitive synthesis**: Assemble mechanisms from a validated library (`src/davinci_codex/primitives/`) covering gears, cams, linkages, springs, escapements, and hydraulic elements.
2. **Parametric definition**: Encode geometry and motion using typed dataclasses with SI units and Renaissance equivalents. Configuration files (YAML/JSON) document assumptions and tunable parameters.
3. **Simulation pipelines**: Employ energy-consistent integrators, rigid-body dynamics, finite-element surrogates, and CFD/FSI couplings appropriate to each invention class. Fluid-structure interaction is mandatory for aerodynamic studies (ornithopter, parachute, aerial screw) using unsteady vortex lattice + nonlinear beam coupling, or URANS/LES when warranted.
4. **Tribology and contact mechanics**: Self-propelled carts, odometers, and workshop tools undergo explicit friction, wear, and lubrication analyses. Classical tribology data and synthetic experiments calibrate loss models before viability scoring.
5. **Human-in-the-loop craftsmanship**: Iteratively reconcile simulated behaviour with craft notes derived from period workshops (joinery limits, hand-tool tolerances, natural material variability).

## 4. Verification & Validation (V&V)
- **Analytical baselines**: Compare simulations to closed-form solutions or canonical experimental correlations (e.g., Lewis bending stress for gears, beam theory for spars).
- **Mesh and timestep convergence**: Document mesh-independence and timestep sensitivity with Richardson extrapolation where applicable.
- **Cross-folio consistency**: Validate that shared primitives behave consistently across inventions; deviations trigger investigations into folio-specific annotations.
- **Physical prototyping**: When feasible, build scale or full-size prototypes using documented materials to verify mechanical viability.

## 5. Simulation Toolchain & Environment
- **Core solvers**: Finite-element solids via FEniCS/pycalculix; CFD via OpenFOAM with URANS/LES for bluff body flows; vortex lattice + beam coupling for flapping studies; tribology experiments scripted in Python + Abaqus where necessary.
- **Version control**: Each study records solver version, turbulence model, mesh generator, and numerical tolerances inside `validation/<slug>/case.yaml`.
- **Reproducible runs**: `sims/` contains CLI recipes and container manifests so reviewers can re-execute pipelines on HPC clusters or local workstations.

## 6. Units & Parameter Distributions
- **SI baseline**: Store all quantitative parameters in SI units (N, m, Pa, kg/m³). Document any conversions from Renaissance units (e.g., braccia, oncie) inside the associated `PROVENANCE/<codex>/<folio>.yaml` entry and configuration files.
- **Default distributions**: Apply normal distributions for measured material properties (with historical standard deviations), triangular distributions for craft tolerances (hand-cut gears, cams), and bounded uniform distributions for friction coefficients or uncalibrated loads. Deviations must be justified in the simulation notes.
- **Catalog alignment**: Each invention record in `inventions/catalog.yaml` must reference a `PROVENANCE` slug and cite the distribution assumptions used by `RenaissanceUQ`.

## 7. Uncertainty Quantification (UQ)
- **Input uncertainty**: Derive probability distributions for materials, fabrication tolerances, and operating conditions from historical sources. Epistemic uncertainty from ambiguous sketches is parameterised as interval or triangular distributions with provenance references.
- **Sampling strategy**: Use Sobol/Saltelli sampling (via `RenaissanceUQ`) for global sensitivity and Monte Carlo analysis to estimate output distributions.
- **Reporting**: All reported metrics (altitude, lift, efficiency, safety factors) include 95% confidence intervals and tornado charts describing dominant uncertainty contributors.

## 8. Safety, Ethics, and FMEA
- **Failure Mode & Effects Analysis**: Execute systematic FMEA for each invention with severity, occurrence, detection ratings, and mitigations.
- **Non-weaponisation**: Enforce the principles described in `ETHICS.md`; mechanisms with offensive potential receive heightened scrutiny and explicit risk communication.

## 9. Workflow Governance
1. **Version control**: Each reconstruction proceeds through design review, simulation review, and historical validation checklists before merging.
2. **Reproducibility**: Provide deterministic scripts under `sims/` and notebooks in `notebooks/` that rebuild figures, tables, and summary statistics.
3. **Peer review**: Engage domain experts (historians, mechanical engineers, materials scientists) for formal review cycles documented in `docs/review_logs/` (forthcoming).
4. **Provenance compliance**: Every merge request must reference the relevant `PROVENANCE` slug(s) and pass automated catalog/provenance schema validation in CI.

## 10. Human & AI Collaboration Disclosure
- **Human-led interpretation**: Domain experts define research questions, interpret folios, select boundary conditions, and approve engineering decisions.
- **AI assistance**: Large language models (GPT-5 Codex, Claude Opus) assist with code scaffolding, documentation drafting, and exploratory analysis under human supervision. Outputs are reviewed, edited, and validated before inclusion.
- **Transparency**: `AGENTS.md` logs AI-assisted sessions. Every manuscript or commit with substantive AI contribution references the supervising researcher and verification steps.

## 11. Dissertation Deliverables
- **Complete catalog** with provenance, models, simulations, and analyses for 500 inventions.
- **Textile revolution dossier** covering the first tranche of reconstructions (CA f.1090r onwards) with economic impact analysis.
- **FSI case studies** (ornithopter, aerial screw, fluid-driven pumps) demonstrating multiphysics fidelity.
- **Open dataset** releasing CAD, simulation inputs, uncertainty samples, and analytical summaries under CC0 terms.

This methodology evolves with each review cycle. Updates must cite rationale, affected inventions, and validation evidence so that the digital dissertation remains auditable and defensible.
