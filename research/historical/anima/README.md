# ANIMA Core

Tools for decoding Leonardo's manuscripts. This package will handle manuscript ingestion, handwriting analysis, sketch vectorization, and production of structured JSON describing intent, components, and constraints. Subpackages will be organized as:

- `ingest/` — scan normalization, catalog metadata, OCR/mirror-text pipelines.
- `interpret/` — mechanical principle extraction, kinematics reconstruction.
- `outputs/` — schemas and serializers for downstream modules.

Each invention receives an `anima/<slug>/` notebook and config capturing folio references, transcription notes, and annotated markup for reuse by TVA, Synthesis, and IP Nexus.
