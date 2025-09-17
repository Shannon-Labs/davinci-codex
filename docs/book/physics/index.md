# Physics Derivations

<div class="chapter-start">
The pages that follow collect the governing relations used throughout the Codex. Each derivation is concise, referenced, and paired with validation where possible—just as Leonardo alternated between folio, measurement, and refinement.
</div>

## Overview and Historical Thread

- Unsteady Airfoil Dynamics: From da Vinci’s sketches of vortices to modern added-mass and Theodorsen-like models, we quantify phase and amplitude response under oscillation. See {doc}`unsteady_aero`.
- Gear Tooth Bending: From hand-laid involutes to Lewis bending theory and stress concentration, we derive design formulas and compare against mesh-based convergence. See {doc}`gear_bending`.
- Rolling Tribology: Contact mechanics, hysteresis, and slip define energy losses in motion—ideas that echo in Leonardo’s odometers and carts. See {doc}`tribology`.

Each page emphasizes assumptions, limits of applicability, and typical parameter ranges. Equations favor legibility; proofs that are standard are summarized with references.

## Notation and Conventions

- Scalars are italic (e.g., V, Re); vectors bold (u); time derivatives use overdots; complex harmonics use Re{·} convention.
- SI units throughout; conversions appear inline where historical units are cited.
- Figures use a muted Renaissance palette for consistency with the book’s theme.

## Provenance and Reuse

Source code snippets referenced here come from typed utilities under `src/davinci_codex/core/` and are exercised in the notebooks. Where data are used for calibration or comparison, they are stored and hashed under `validation/` with citations in `REFERENCES.md`.

Proceed to any topic:

- [Unsteady Airfoil Dynamics](unsteady_aero.md)
- [Gear Tooth Bending Theory](gear_bending.md)
- [Rolling Tribology Models](tribology.md)
