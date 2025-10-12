# ANIMA — Ornithopter Package

Artifacts in this folder document Leonardo's original intent for the flapping-wing machine.

- `folio_refs.csv` — catalog IDs, repositories, licensing info for source scans.
- `transcriptions/` — Italian mirror-text OCR with English translations aligned by line.
- `annotations/` — vector overlays (SVG/JSON) mapping mechanical linkages and leverage arms.
- `intent.json` — normalized output consumed by TVA describing components, joints, degrees of freedom, and ambiguous areas needing expert review.

Next steps: ingest hi-res scans from Biblioteca Ambrosiana, finalize transcription pipeline (tesseract + custom mirror-handwriting model), and publish draft `intent.json` seeded from manual annotations.
