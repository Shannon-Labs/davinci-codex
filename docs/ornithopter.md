# Ornithopter Modernization Dossier

## Source Manuscripts
- **Codex Atlanticus, folio 846r** — Annotated planform showing pilot-in-frame, twin flapping wings, and crank-driven gearing.
- **Manuscript B (Institut de France), folio 70r** — Side elevation with torsion springs and shoulder harness notes.
- **Codex on the Flight of Birds, folio 12v** — Aerodynamic observations on wing camber and feather articulation leveraged for control assumptions.

Digitized scans are catalogued in `anima/ornithopter/` with mirrored, high-resolution TIFF references and transcription JSON linking Italian mirror-text to English glosses.

## Renaissance Limitations
1. **Insufficient Power Density:** Human leg and arm cranks could not deliver the ~750 W continuous power needed for sustained flapping lift at the prescribed span.
2. **Material Fatigue:** Primary spars specified in fir and rawhide hinges would fail under cyclic bending within tens of cycles, lacking spring-tempered alloys.
3. **Control Authority:** Sketches omit roll damping surfaces; without real-time feedback, pilot workload exceeded plausible reaction times.
4. **Manufacturing Precision:** Gear ratios and chain links require tolerances (<0.25 mm) unattainable with 16th-century workshops, leading to binding and asymmetric strokes.

TVA simulations reproduce these constraints using fir/linen properties, rawhide joints, and human power curves to highlight exact failure timings.

### TVA Baseline (2025-09-16)
- Required drivetrain power at 2.4 Hz: **14.67 kW**
- Sustained human output (galley rower benchmark): **0.42 kW** → **−14.25 kW** deficit
- Laminated torsion spring margin: **−433 N·m** (springs saturate mid-stroke)
- Fir spar fatigue life: **≈50 cycles** vs. ≥500 cycles desired
- Static stress ratio: **0.49** (within limit, fatigue is governing)

These results are archived in `tva/ornithopter/viability_report.md` with reproducible calculations under `davinci_codex.tva.ornithopter`.

## Modern Synthesis Strategy
- **Structure:** Carbon-fiber tube wing spars with 7075-T6 aluminum root fittings; FlexLam skin with Kevlar hinge strips for aeroelastic twist.
- **Actuation:** Brushless outrunner motors (2× 2 kW) driving a crank-rocker mechanism with harmonic reduction gears; Li-ion battery pack sized for 10-minute endurance.
- **Control:** Embedded flight computer (PX4 + IMU + pressure sensors) commanding differential flapping amplitude and tailplane servos.
- **Safety:** Ballistic parachute integration and energy-absorbing landing skid.

Synthesis deliverables include parametric CAD in `cad/ornithopter/model.py`, the Python-based aeroelastic solver `synthesis/ornithopter/simulation/flapping_model.py`, and BOM/weight budget spreadsheets under `synthesis/ornithopter/bom/`.

## Material Comparison

| Metric | Historical (fir/rawhide) | Modern (carbon/Kevlar) | Improvement |
| --- | --- | --- | --- |
| Structural mass (kg) | 42.0 | 28.5 | 32% lighter |
| Required power (kW) | 14.7 | 4.1 | 72% reduction |
| Endurance (min) | 0.5 | 12.0 | +2300% mission duration |

Source data: `data/materials/material_comparisons.csv` and TVA trace `tva/ornithopter/data/fsi_modal_response.csv`.


## Pipeline Integration Roadmap
1. **ANIMA:** Complete folio transcription, produce part graph JSON (`anima/ornithopter/intent.json`), and highlight ambiguous annotations for historian review.
2. **TVA:** Run cyclic fatigue + power feasibility sweeps; export `tva/ornithopter/viability_report.md` summarizing failure loads and earliest feasible metallurgy.
3. **Synthesis:** Generate CAD, run aeroelastic solver (`python -m davinci_codex.cli pipeline --slug ornithopter` executes the full chain), and validate lift-to-weight > 1.2 at 2.5 Hz flapping. Publish simulation artifacts in `artifacts/ornithopter/synthesis_sim/`.
4. **IP Nexus:** Search USPTO CPC B64C related patents, map overlapping claims, and draft defensive publication sections referencing TVA/Synthesis results.

Cross-module coordination notes live in `inventions/ornithopter/README.md`, aligning the artifact directory hierarchy with the Python implementation living under `src/davinci_codex/inventions/ornithopter.py`.
