# Repository Guidelines

## Project Structure & Module Organization
Core Python modules live in `src/davinci_codex/`, grouped by invention with shared utilities under `src/davinci_codex/core/`. Tests mirror this layout inside `tests/`, using `test_*.py` files per module. Simulation configs and captured results sit in `sims/`, parametric CAD scripts in `cad/`, and provenance docs plus engineering notes in `docs/`. Generated datasets and metadata stay under `data/`, while exploratory notebooks in `notebooks/` are synchronized to docs through automation.

## Build, Test, and Development Commands
Run `make setup` once to create `.venv/`, upgrade pip, and install editable dependencies. `make lint` chains `ruff check .` and `mypy src` to keep style and type guarantees aligned. Use `make test` (quiet pytest) before every push, `make demo` to exercise the CLI exemplar build, and `make build` for the full artifact pipeline.

## Coding Style & Naming Conventions
Write Python 3.10+ with 4-space indentation, descriptive snake_case functions, and PascalCase classes. Modules should expose typed dataclasses or Pydantic models for configuration; annotate public functions. Prefer pure functions for analysis routines and keep CLI wiring in Typer commands. Use `ruff` to enforce imports, docstrings, and formatting (enable autofix with `ruff check --fix` locally) and ensure `mypy` passes with `strict_optional = True` defaults retained.

## Testing Guidelines
New features require pytest coverage under `tests/` with fixtures reused via `conftest.py`. Name suites `test_<module>.py` and express scenarios as small, deterministic cases; parametrize physics sweeps instead of loops. When simulations emit files, write to `tmp_path` and capture hashes rather than binaries. CI expects `make test` to run cleanly.

## Commit & Pull Request Guidelines
Keep commits focused and written in sentence case (see history: “Document collaboration…”, “Initial public release…”). Reference the affected subsystem in the subject and elaborate in the body if APIs shift. Pull requests must describe the motivation, list verification commands (e.g., `make lint`, `make test`), link relevant docs, and attach screenshots or artifact paths when UX or geometry changes.

## Artifact & Safety Notes
Provenance evidence, scans, and generated media belong in `docs/` with CC0 markings; do not commit binaries to `cad/` or `sims/`. Flag any design with potential safety concerns in the PR summary and outline mitigations before requesting review.