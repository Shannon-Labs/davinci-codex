# Provenance Registry

This directory collates folio-level documentation for every manuscript referenced by the da Vinci Codex digital dissertation. Each subfolder corresponds to an archival source (e.g., `codex_atlanticus/`, `madrid_codices/`). Individual YAML files store structured metadata linking simulations, transcripts, and analyses to their primary evidence.

## File Schema
- `folio_id`: Canonical identifier using archive conventions.
- `canonical_name`: Short descriptive title for the invention.
- `category`: High-level classification aligning with `inventions/catalog.yaml`.
- `archive_source`: Repository metadata, image identifiers, and retrieval tracking.
- `transcription`: OCR/hand transcription method, language, and confidence.
- `mechanical_primitives`: List of building blocks referenced in the mechanism.
- `materials`: Period-accurate materials drawn from `materials/renaissance_db.yaml`.
- `validation_status`: Checklist covering UQ, V&V, and FMEA milestones.

All entries must cite supporting bibliography in `references.bib` and record review status.
