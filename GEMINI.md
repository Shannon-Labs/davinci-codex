# GEMINI.md

## Project Overview

This project, "The da Vinci Codex," is a Python-based computational framework for analyzing and simulating Leonardo da Vinci's mechanical inventions. It applies modern engineering principles, physics-based simulation, and safety-critical analysis to da Vinci's 15th-century mechanical concepts.

**Main Technologies:**

*   **Programming Language:** Python 3.9+
*   **Linting:** Ruff
*   **Type Checking:** MyPy
*   **Testing:** Pytest
*   **Documentation:** Jupyter Book
*   **CLI:** Typer

**Architecture:**

The project is structured around a series of "invention modules," each representing one of da Vinci's inventions. These modules are discovered and managed by a central registry. Each module implements a common interface for planning, simulation, building (e.g., generating CAD files), and evaluation.

The core logic is located in the `src/davinci_codex` directory, with individual invention modules in `src/davinci_codex/inventions`. The project also includes extensive documentation, simulation configurations, and validation assets.

## Building and Running

The project uses a `Makefile` to simplify common tasks.

**Key `make` commands:**

*   `make setup`: Sets up a Python virtual environment and installs all dependencies.
*   `make lint`: Checks the code for style and type errors using Ruff and MyPy.
*   `make test`: Runs the test suite using Pytest.
*   `make demo`: Runs a lightweight simulation and evaluation for all inventions.
*   `make build`: Generates CAD or other build artifacts for all inventions.
*   `make book`: Builds the Jupyter Book documentation.

**Command-Line Interface (CLI):**

The project provides a command-line interface, `davinci-codex`, for interacting with the invention modules.

*   `davinci-codex list`: Lists all available inventions.
*   `davinci-codex plan [--slug <invention>]`: Prints the planning assumptions for an invention.
*   `davinci-codex simulate [--slug <invention>]`: Runs a simulation for an invention.
*   `davinci-codex build [--slug <invention>]`: Generates build artifacts (e.g., CAD files) for an invention.
*   `davinci-codex evaluate [--slug <invention>]`: Reviews the feasibility and ethics of an invention.
*   `davinci-codex demo [--slug <invention>]`: Runs a lightweight simulation and evaluation.
*   `davinci-codex pipeline [--slug <invention>]`: Runs a multi-stage pipeline (currently only for the ornithopter).
*   `davinci-codex validation-status`: Summarizes the validation evidence across all cases.

## Development Conventions

*   **Invention Module Protocol:** Each invention is implemented as a Python module that adheres to a specific protocol defined in `src/davinci_codex/registry.py`. This protocol requires each module to have `plan`, `simulate`, `build`, and `evaluate` functions, as well as metadata such as `SLUG`, `TITLE`, `STATUS`, and `SUMMARY`.
*   **Linting and Type Checking:** The project uses Ruff for code linting and MyPy for static type checking. The configuration for these tools can be found in the `pyproject.toml` file.
*   **Testing:** The project uses Pytest for testing. Tests are located in the `tests` directory.
*   **Commits:** The `COMMIT_PROMPT.md` file suggests a structured format for commit messages.
