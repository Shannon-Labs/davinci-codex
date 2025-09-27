# Mechanical Carillon

## Overview

Leonardo sketched a clock-driven carillon on Codex Atlanticus f.30r where a rotating drum cues bell strikers, delivering programmable civic chimes without a resident ringer.

## Historical Context

- **Folio**: CA f.30r
- **Date**: ~1490-1494
- **Category**: Music/Automation
- **Related Sketches**: CA f.31v, Madrid I f.96r

## Simulation

The model evaluates strike timing jitter, bell frequency coverage, and hammer impact energy for a configurable rotation program. It outputs CSV schedules and frequency scatter plots for analysis.

## CAD Model

Drum, bell rack, frame, and striker arms are scripted in `cad/mechanical_carillon/model.py` for rapid STL export and iteration.

## Status

Concept reconstruction; tower-scale integration pending mechanical brake testing.

For more details, see [source code](../src/davinci_codex/inventions/mechanical_carillon.py).

