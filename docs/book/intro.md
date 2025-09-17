# Computational Essays

The da Vinci Codex uses simulation notebooks to accompany validation cases and translate folio sketches into quantitative models. These essays execute automatically during the Jupyter Book build:

- Reference derivations in [`docs/physics`](../physics/index.md).
- Reuse datasets in [`validation/`](../../validation).
- Embed figures from [`docs/images`](../images).

Launch locally with:

```bash
jupyter-book build docs/book
```

or preview interactively via `jupyter lab notebooks/`.
