# Ornithopter Reconstruction Workspace

This workspace coordinates all cross-disciplinary assets for Leonardo's ornithopter modernization.

## Directory Guide
- `anima/` — Manuscript scans, transcription JSON, and part-graph annotations.
- `tva/` — Historical material models, cyclic fatigue studies, and viability reports.
- `synthesis/` — Modern CAD, MuJoCo simulations, bill-of-materials, and controller prototypes.
- `ip_nexus/` — Patent search results, claim comparisons, and defensive publication drafts.

## Immediate Actions
1. Finalize folio corpus (CA 846r, Ms. B 70r, Flight of Birds 12v) with annotated markup.
2. Run baseline TVA simulations comparing human power curves vs. required flapping energy.
3. Produce first-pass CAD skeleton (carbon composite frame, differential flapping gear train) — *complete*.
4. Ingest TVA baseline outputs (power deficit, fatigue life) into synthesis validation tasks via `synthesis/ornithopter/simulation/flapping_model.py`.

Progress across modules is mirrored back into `docs/ornithopter.md` and the Python pipeline implementation at `src/davinci_codex/inventions/ornithopter.py`.
