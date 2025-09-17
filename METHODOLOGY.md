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
4. **Materials linkage**: Every component references `materials/renaissance_db.yaml` to declare period-accurate mechanical properties (density, modulus, fatigue limits) with explicit uncertainty.

## 3. Model Construction
1. **Primitive synthesis**: Assemble mechanisms from a validated library (`src/davinci_codex/primitives/`) covering gears, cams, linkages, springs, escapements, and hydraulic elements.
2. **Parametric definition**: Encode geometry and motion using typed dataclasses with SI units and Renaissance equivalents. Configuration files (YAML/JSON) document assumptions and tunable parameters.
3. **Simulation pipelines**: Employ energy-consistent integrators, rigid-body dynamics, and finite-element surrogates appropriate to each invention class.
4. **Human-in-the-loop craftsmanship**: Iteratively reconcile simulated behaviour with craft notes derived from period workshops (joinery limits, hand-tool tolerances, natural material variability).

## 4. Verification & Validation (V&V)
- **Analytical baselines**: Compare simulations to closed-form solutions or canonical experimental correlations (e.g., Lewis bending stress for gears, beam theory for spars).
- **Mesh and timestep convergence**: Document mesh-independence and timestep sensitivity with Richardson extrapolation where applicable.
- **Cross-folio consistency**: Validate that shared primitives behave consistently across inventions; deviations trigger investigations into folio-specific annotations.
- **Physical prototyping**: When feasible, build scale or full-size prototypes using documented materials to verify mechanical viability.

## 5. Uncertainty Quantification (UQ)
- **Input uncertainty**: Derive probability distributions for materials, fabrication tolerances, and operating conditions from historical sources.
- **Sampling strategy**: Use Sobol/Saltelli sampling (via `RenaissanceUQ`) for global sensitivity and Monte Carlo analysis to estimate output distributions.
- **Reporting**: All results include 95% confidence intervals, sensitivity indices, and narrative interpretation relating uncertainty to historical risk.

## 6. Safety, Ethics, and FMEA
- **Failure Mode & Effects Analysis**: Execute systematic FMEA for each invention with severity, occurrence, detection ratings, and mitigations.
- **Non-weaponisation**: Enforce the principles described in `ETHICS.md`; mechanisms with offensive potential receive heightened scrutiny and explicit risk communication.

## 7. Workflow Governance
1. **Version control**: Each reconstruction proceeds through design review, simulation review, and historical validation checklists before merging.
2. **Reproducibility**: Provide deterministic scripts under `sims/` and notebooks in `notebooks/` that rebuild figures, tables, and summary statistics.
3. **Peer review**: Engage domain experts (historians, mechanical engineers, materials scientists) for formal review cycles documented in `docs/review_logs/` (forthcoming).

## 8. Dissertation Deliverables
- **Complete catalog** with provenance, models, simulations, and analyses for 500 inventions.
- **Textile revolution dossier** covering the first tranche of reconstructions (CA f.1090r onwards) with economic impact analysis.
- **FSI case studies** (ornithopter, aerial screw, fluid-driven pumps) demonstrating multiphysics fidelity.
- **Open dataset** releasing CAD, simulation inputs, uncertainty samples, and analytical summaries under CC0 terms.

This methodology evolves with each review cycle. Updates must cite rationale, affected inventions, and validation evidence so that the digital dissertation remains auditable and defensible.
