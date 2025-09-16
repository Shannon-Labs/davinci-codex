# Ornithopter TVA Analysis Notes

## Overview
These notes accompany the historical viability simulations executed via `davinci_codex.tva.ornithopter`. The objective is to quantify why Leonardo's flapping machine could not achieve powered flight using Renaissance materials and human actuation.

## Key Assumptions
- **Wing span:** 10.5 m total, 5.25 m per side (from Codex Atlanticus 846r).
- **Stroke amplitude:** 2.2 m peak-to-peak as interpreted from sketch geometry.
- **Flapping frequency:** 2.4 Hz required to sustain lift per Leonardo's proportional annotations.
- **Surface density (Renaissance):** 2.7 kg/m² combining fir spars, linen skin, and rawhide lashings.
- **Human power:** Long-duration benchmark taken from Venetian galley rower logs (≈420 W sustained).

## Metrics Produced by Simulation
The TVA module computes:
1. **Required drivetrain torque** to counter wing weight during each stroke.
2. **Power draw** at 2.4 Hz compared with sustained human output.
3. **Spring torque margin** relative to laminated steel torsion pairs.
4. **Fatigue life** for fir spars using Basquin's relation and assumed section modulus.
5. **Static stress ratio** against allowable bending stress for fir beams.

## Interim Findings (Baseline Run)
- Total required torque: ~0.97 kN·m (per pair of wings).
- Required average power: ~14.7 kW, exceeding historical human capacity by >14 kW.
- Laminated torsion springs fall short by ~430 N·m of torque.
- Predicted fatigue life of fir spars: ≈50 cycles vs. 500 cycles desired for demonstrations.

## Next Steps
- Parameter sweep varying wing surface density between 2.0–3.0 kg/m².
- Evaluate reduced stroke amplitude scenarios to quantify takeoff requirements.
- Integrate modern composite properties for comparison case in `synthesis/`.
- Export plots (torque vs. cycle, power deficit heatmap) for inclusion in the main dossier.
