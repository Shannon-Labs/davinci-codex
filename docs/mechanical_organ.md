# Mechanical Organ

## Overview

Leonardo sketched an automatic pipe organ on Codex Atlanticus f.80r, combining a pinned program barrel with twin bellows to sustain polyphonic court music without a dedicated organist.

## Historical Context

- **Folio**: CA f.80r
- **Date**: ~1490-1495
- **Category**: Music/Automation
- **Related Sketches**: CA f.80v, Madrid I f.85r

## Simulation

Models the pinned program rotation, bellows pressure variation, and resulting pitch stability across the registered pipes. Outputs CSV/plots for frequency drift review.

## CAD Model

Parametric solids for wind chest, pipe ranks, and the program barrel live in `cad/mechanical_organ/model.py`.

## Status

Concept reconstruction; further validation planned with physical bellows tests.

For more details, see [source code](../src/davinci_codex/inventions/mechanical_organ.py).

