# Ornithopter Temporal Viability Report

**Run date:** 2025-09-16  
**Module:** `davinci_codex.tva.ornithopter.evaluate_viability`

## Summary
Leonardo's flapping-wing machine cannot achieve powered flight with Renaissance-era technology. Required drivetrain power is more than **14.6 kW**, while the best documented sustained human output from period crews is roughly **0.42 kW**, leaving a deficit of **≈14.25 kW**. Laminated torsion springs depicted in Manuscript B (folio 70r) fall short by **≈430 N·m** of torque during the downstroke. Fir spars would survive only **≈50 cycles** before fatigue failure, far below the **500 cycle** threshold set for reliable demonstrations.

## Key Metrics
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Required average power | 14.67 kW | ≥ human sustained 0.60 kW | ❌ exceeds capability |
| Sustained human power (galley rower benchmark) | 0.42 kW | – | Insufficient |
| Peak human power (short sprint) | 0.80 kW | – | Short-term only |
| Total drivetrain torque | 973 N·m | Spring capacity 540 N·m | ❌ springs overload |
| Torque margin | -433 N·m | ≥ 0 N·m | ❌ negative |
| Spar stress range | 22.1 MPa | Allowable 45 MPa | ✅ within static limit |
| Predicted fatigue life | 50 cycles | ≥ 500 cycles | ❌ fails |

## Interpretation
1. **Power Density Barrier:** Even assuming the strongest rowers of the Venetian fleet, the continuous power deficit exceeds 14 kW. No Renaissance gearing configuration or stored energy device closes this gap.
2. **Energy Storage Limits:** The dual laminated springs Leonardo sketched deliver roughly 540 N·m at maximum wind. Downstroke torque demand is ~973 N·m, resulting in stall or asymmetric wing motion.
3. **Material Fatigue:** Fir spars sized according to Leonardo's proportions endure fewer than 100 strokes before fatigue cracks form. Static stress is acceptable, but repeated bending quickly drives failure.
4. **Control Implications:** Because the springs saturate mid-stroke, reliable roll control would be impossible. This validates Leonardo's own note that "the weight of the head" must counter the springs—a cue that the system never met equilibrium.

## Recommendations
- Transition to composite spars and electric actuation (captured in `synthesis/ornithopter`).
- Replace mechanical springs with geared servo assistance providing ≥1.0 kN·m torque.
- Reduce stroke amplitude to 1.2 m during takeoff drills until composite fatigue data is validated.
- Document these findings in the open dossier (`docs/ornithopter.md`) to preserve the public-domain prior art.
