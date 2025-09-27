# Mechanical Trumpeter

## Overview

Leonardo drafted automaton musicians for ducal festivals, including a trumpet player on Codex Atlanticus f.194r that uses clockwork cams to sequence valve motion and bellows breath.

## Historical Context

- **Folio**: CA f.194r
- **Date**: ~1494-1498
- **Category**: Music/Automation
- **Related Sketches**: CA f.195v, Madrid II f.12r

## Simulation

The module models programmable valve timing, breath pressure modulation, and resulting register shifts. It exports frequency/pressure timelines for quick comparison against period fanfares.

## CAD Model

Valve cluster, leadpipe, and bell geometry live in `cad/mechanical_trumpeter/model.py` for rapid STL iteration.

## Status

Concept reconstruction; valve spring tuning pending hardware prototyping.

For more details, see [source code](../src/davinci_codex/inventions/mechanical_trumpeter.py).

