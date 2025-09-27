# Mechanical Ensemble

## Overview

This orchestrator coordinates Leonardo''s automated musical inventions—drum, organ, viola organista, programmable flute, carillon, and trumpeter—into a single simulation and CAD pipeline with spectral balancing.

## Historical Context

- **Folios**: CA f.30r, f.80r, f.93v, f.194r, and related festival sketches
- **Date**: Composite of 1490s court entertainment studies
- **Category**: Music/Automation
- **Related Sketches**: CA f.837r, CA f.572r, Madrid I f.96r

## Simulation

`simulate()` runs each instrument module, extracts spectral summaries, and writes a combined CSV detailing fundamentals, spectral centroid, bandwidth, loudness (dB), and decay slope to guide the ensemble mix.

## CAD Manifest

`build()` invokes every instrument''s CAD export and packages a manifest of STL paths for stage layout.

## Evaluation

`evaluate()` aggregates practicality metrics from each invention, computes a composite spectral balance ratio, reports ensemble loudness and harmonic decay slope, and suggests next acoustic tuning actions.

## Demo Workflow

`demo()` (surfaced via `davinci-codex ensemble-demo`) generates a pseudo-score JSON file with tempo-synchronised events for every instrument alongside the latest spectral summary. Use it to storyboard court performances or feed downstream synthesis tools.

For API details, see [source code](../src/davinci_codex/inventions/mechanical_ensemble.py).
