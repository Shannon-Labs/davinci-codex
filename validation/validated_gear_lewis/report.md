# Validated Gear Lewis Benchmark

We benchmarked the spur-gear bending model against AGMA 908-B89 Lewis stress factors. A quarter-symmetry finite-element model was built in FEniCS with quadratic hexahedral elements. Mesh refinement shows first-order convergence toward the analytical Lewis stress (185 MPa) with <0.7% error at 9.6k elements. Safety factor against the allowable 280 MPa is 1.51. The FE-derived Lewis factor matches the closed-form coefficient (0.337) within 1.4% when back-calculated from the peak stress.

CSV: `convergence.csv`
Solver script: `sims/gear/validated_lewis_fea.py`
