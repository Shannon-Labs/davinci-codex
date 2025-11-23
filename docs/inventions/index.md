---
layout: default
title: Inventions & Status
nav_order: 2
permalink: /inventions/
description: Status overview for all da Vinci Codex inventions, with links to primary documentation.
---

# Inventions & status

This page summarises the current reconstruction status of each invention exposed via the `davinci-codex` CLI and registry.

- `validated`: simulations plus a supporting validation dossier with documented metrics and safety review.
- `prototype_ready`: simulations and build plan suitable for careful workshop prototypes.
- `simulation_prototype` / `in_progress`: active reconstruction work with core models running but validation still in progress.
- `concept_reconstruction`: historically grounded reconstruction focused on geometry and motion, with limited quantitative validation.

For methodology details and assumptions behind each label, see the [Methodology & status assumptions](../methodology_statuses.md) page.

## Invention cards

<!-- BEGIN INVENTION_CARDS -->
| Slug | Title | Status | Metrics | Primary docs |
| --- | --- | --- | --- | --- |
| `aerial_screw` | Leonardo's Aerial Screw - Advanced Aerodynamic Analysis | `validated` | Maximum lift 1,416 N (optimized rotor at 10.8 kW); CAD package 99 files (parametric models, drawings, animations) | [report](../aerial_screw.md) |
| `armored_walker` | The Armored Walker | `simulation_prototype` | Walking speed ≈0.28 m/s (forward gait in simulation); Range ≈50 m (per winding) | [report](../armored_walker.md) |
| `mechanical_carillon` | Mechanical Carillon | `concept_reconstruction` | Bell count 8–24 (modeled bell array); Programs 12–24 (pin patterns per cylinder) | [report](../mechanical_carillon.md) |
| `mechanical_drum` | Mechanical Drum | `prototype_ready` | Pattern length up to 16 beats (per cam program in model); Channels 2–4 (independent drum lines) | [report](../mechanical_drum.md) |
| `mechanical_ensemble` | Leonardo Mechanical Ensemble | `concept_reconstruction` | Instruments 7 (ensemble members); Program duration ≈45 min (per synchronized sequence) | [report](../mechanical_ensemble.md) |
| `mechanical_lion` | Leonardo's Mechanical Lion - Complete Walking and Reveal Mechanism | `validated` | Choreography duration 30 s (simulated walking and reveal sequence); Gait speed ≈0.28 m/s (steady walking in simulation) | [report](../mechanical_lion.md) |
| `mechanical_odometer` | Leonardo's Mechanical Odometer Cart | `prototype_ready` | Measurement error <17% (across test course); Distance resolution ≈14 m (per pebble drop) | [report](../mechanical_odometer.md) |
| `mechanical_organ` | Automatic Pipe Organ | `concept_reconstruction` | Pipe range 4–5 octaves (modeled ranks); Programming length 8–12 min (continuous performance per barrel) | [report](../mechanical_organ.md) |
| `mechanical_trumpeter` | Mechanical Trumpeter | `concept_reconstruction` | Pitch range 2–2.5 octaves (fanfares and calls); Phrase duration 8–12 s (per breath cycle) | [report](../mechanical_trumpeter.md) |
| `ornithopter` | Bio-inspired Ornithopter Flight Lab | `in_progress` | Simulated climb 120 m (30 s sustained flight case); Lift ≈1,600 N (representative flapping cycle) | [report](../ornithopter.md) |
| `parachute` | Pyramid Parachute | `prototype_ready` | Descent rate 6.9 m/s (pyramid parachute terminal velocity (sim)); Drop height case 400 m (baseline descent profile) | [report](../parachute.md) |
| `programmable_flute` | Programmable Flute | `concept_reconstruction` | Tone holes 8–10 (modeled recorder geometry); Program length up to 64 notes (per cam sequence) | [report](../programmable_flute.md) |
| `programmable_loom` | Leonardo's Programmable Loom - Textile Pattern Automation | `in_progress` | Warp threads ≈200 (baseline configuration); Pattern length ≤64 steps (cam barrel circumference limit) | [report](../programmable_loom.md) |
| `revolving_bridge` | Leonardo's Revolving Bridge - Advanced Engineering Implementation | `in_progress` | Rotation 360° (full bridge swing); Load case vehicular traffic (simulated structural margin) | [report](../revolving_bridge.md) |
| `self_propelled_cart` | Self-Propelled Cart | `prototype_ready` | Stored spring energy ≈350 J (per winding in simulation); Range ≈150 m (on level terrain) | [report](../self_propelled_cart.md) |
| `variable_pitch_mechanism` | Variable Pitch Swashplate Mechanism | `in_progress` | Pitch range 15°–45° (swashplate control authority); Response time <0.5 s (modeled pitch step change) | [report](../variable_pitch_mechanism.md) |
| `viola_organista` | Viola Organista | `concept_reconstruction` | Pitch range 3–4 octaves (modeled keyboard span); Sustain continuous (wheel-bowed strings) | [report](../viola_organista.md) |
<!-- END INVENTION_CARDS -->
