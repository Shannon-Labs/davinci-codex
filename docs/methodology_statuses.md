---
layout: default
title: Methodology & Status Assumptions
nav_order: 5
permalink: /methodology/statuses/
description: Definitions and assumptions behind the status labels used for da Vinci Codex inventions.
---

# Methodology & status assumptions

The da Vinci Codex project uses a small set of status labels to describe how far each reconstructed invention has progressed through the PLAN → SIMULATE → BUILD → EVALUATE workflow.

These statuses are intentionally conservative and focus on evidence, not marketing language.

## Status definitions

### `validated`

- End-to-end simulation pipeline exercised with fixed seeds and documented configuration.
- Quantitative validation metrics recorded (for example, lift forces, descent rates, gait stability) and compared to historical or engineering targets.
- Safety and ethics review completed with documented assumptions and mitigations.
- Smoke tests and core unit tests run in CI for the corresponding module.

### `prototype_ready`

- Core simulations run and checked for numerical stability and qualitative agreement with historical intent.
- A concrete build and test plan exists, including materials, key dimensions, and basic safety notes.
- Validation data may be partial or use scaled models, but is sufficient for careful workshop experimentation under supervision.

### `simulation_prototype`

- Main computational models are implemented and exercised, often exploring multiple configurations.
- Results are suitable for exploratory analysis and teaching but should not be treated as design-ready.
- Validation against physical experiments or detailed materials testing is still in progress.

### `in_progress`

- Active development status for modules that have partial implementations, early simulations, or open design questions.
- Interfaces and outputs may change; results are suitable for internal exploration rather than external commitments.

### `concept_reconstruction`

- Focused on kinematic reconstruction, motion studies, and qualitative behaviour based on folio analysis.
- Limited quantitative validation; parameters and materials are often approximate or illustrative.
- Intended for education, visualization, and historical reasoning rather than engineering sign-off.

## How statuses are used

- The Python registry (`davinci_codex.registry.list_inventions()`) carries `STATUS` and `SUMMARY` for each invention module.
- The CLI (`davinci-codex list` and `davinci-codex list --statuses`) and README registry table are generated from this registry to avoid divergence.
- CI enforces basic quality gates: required hooks (`plan`, `simulate`, `build`, `evaluate`), metadata completeness, and coverage floors for higher-maturity modules.

When in doubt, treat `validated` as suitable for citing specific metrics, and treat all other statuses as experimental or illustrative. New contributions should begin at `in_progress` or `concept_reconstruction` and only move upward when evidence and tests are in place.

