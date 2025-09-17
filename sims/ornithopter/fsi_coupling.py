"""Document the loose FSI coupling procedure for ornithopter validation.

Steps:
1. Run AVL 3.37 in unsteady mode with wing kinematics from PROVENANCE/CA_f1090r.yaml.
2. Feed aerodynamic loads into nonlinear beam solver (see notebooks/ornithopter_fsi_validation.ipynb).
3. Iterate until lift/twist residuals <1e-3 and record timestep convergence in
   `validation/ornithopter_fsi/timestep_convergence.csv`.
"""

if __name__ == "__main__":
    raise SystemExit("Documentation-only script. Refer to README for reproduction steps.")
