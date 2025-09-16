# Contributing to da Vinci Codex

Thanks for your interest in expanding Leonardo's open, civil inventions! This repository is intentionally reproducible and licensing-friendly. To keep it that way, please follow these principles:

## Ground Rules
- **License alignment:** All source code must be MIT-compatible. Generated docs, figures, meshes, and audio are released under CC0. Do not commit assets with unclear provenance.
- **Safety first:** Avoid weaponizable, harmful, or privacy-invasive concepts. If in doubt, open an issue before drafting a design.
- **Reproducibility:** Every addition should run headless via `make setup && make test && make demo`. Include deterministic seeds for stochastic simulations.
- **Documentation:** Provide provenance notes (folio IDs, catalog references), engineering assumptions, and ethical considerations in `docs/<slug>.md`.
- **Testing:** Add pytest coverage for new modules. Prefer unit-checked math and deterministic fixtures.

## Development Workflow
1. Fork the repository and create a feature branch.
2. Run `make setup` to create the virtual environment.
3. Develop your module under `src/davinci_codex/inventions/<slug>/` with matching tests in `tests/`.
4. Update the invention index in `README.md` and the roadmap in `docs/index.md`.
5. Ensure `make lint test demo` succeeds locally.
6. Submit a pull request using the provided template; include provenance sources and safety notes.

## Reporting Issues
Use `.github/ISSUE_TEMPLATE/feature.md` when proposing a new invention module. For bugs or regressions, open a free-form issue with reproduction steps, expected behavior, and environment details.

## Code Style
- Python 3.11+, typed where practical.
- Lint with `ruff`, type-check with `mypy`.
- Keep functions small and document math-heavy sections inline or via module docstrings.

Thanks for helping grow the open da Vinci knowledge base!
