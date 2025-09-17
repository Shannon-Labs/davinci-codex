"""Placeholder script documenting the Lewis gear bending validation case.

The actual finite-element model is executed in FEniCS or pycalculix and writes
results to `validation/validated_gear_lewis/convergence.csv`.

Steps to reproduce (high level):
1. Build quarter symmetry model of spur gear (module 3 mm, 20 teeth).
2. Apply rim constraint and incremental torque (120, 240 Nm).
3. Refine mesh with structured hexahedral elements reaching >19k elements.
4. Record maximum root stress per mesh and compute error versus Lewis formula.

See `validation/validated_gear_lewis/case.yaml` for metadata.
"""

if __name__ == "__main__":
    raise SystemExit("This script is documentation only; see comments for reproduction steps.")
