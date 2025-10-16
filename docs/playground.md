---
layout: default
title: Playground
permalink: /playground/
---

# Playground

Try the demos instantly:

- **Live Demo (HF Space)**: Coming soon — will be linked here when available.
- **Quickstart Notebook (Colab)**: https://colab.research.google.com/github/Shannon-Labs/davinci-codex/blob/main/notebooks/Quickstart.ipynb

## Local Quickstart

```bash
pip install -r requirements.lock
pip install -e .
# Explore
python -m davinci_codex.cli list | head -n 5
# Simulate
python -m davinci_codex.cli simulate --slug parachute --seed 0 --fidelity educational
```

## Hero Demos

- `parachute` — Educational descent physics and safety metrics
- `aerial_screw` — Blade element momentum analysis and vortex visuals
- `mechanical_lion` — Gait stability, cam profiles, and animated walk sequence
