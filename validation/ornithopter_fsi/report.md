# Ornithopter Flapping FSI Benchmark

Coupled vortex lattice + nonlinear beam simulations were validated against Theodorsen-based flapping-wing data. Time-step refinement from 10 ms to 1.25 ms decreases lift error from 1.1% to <0.05% relative to the analytical benchmark (1580 N). Peak wing twist converges to 12.5° within 0.1°. These results justify the time step and coupling frequency used in production runs (`sims/ornithopter/fsi_coupling.py`).

Notebook: `notebooks/ornithopter_fsi_validation.ipynb`
