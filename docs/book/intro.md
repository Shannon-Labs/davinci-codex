# Computational Essays

The da Vinci Codex uses simulation notebooks to accompany validation cases and translate folio sketches into quantitative models. These essays execute automatically during the Jupyter Book build:

- Reference derivations in {doc}`physics/index`.
- Reuse datasets provisioned under `validation/`.
- Embed figures stored in `docs/images/`.

Launch locally with:

```bash
jupyter-book build docs/book
```

or preview interactively via `jupyter lab notebooks/`.
