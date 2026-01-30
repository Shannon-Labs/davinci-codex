# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the da Vinci Codex project - a collaborative effort to complete Leonardo da Vinci's unfinished inventions using modern engineering, materials, and computational methods. The project translates Renaissance designs into working implementations while maintaining da Vinci's original spirit of innovation.

## Build and Development Commands

```bash
# Setup development environment
make setup

# Run linting and type checking
make lint
# Equivalent to: ruff check . && mypy src

# Run tests
make test
# Equivalent to: pytest -q

# Run a single test file
pytest tests/test_<invention_name>.py

# Build all CAD/artifacts
make build
# Or using CLI: python -m davinci_codex.cli build --all

# Run demo (lightweight simulation + evaluation)
make demo
# Or using CLI: python -m davinci_codex.cli demo

# CLI commands for specific inventions
python -m davinci_codex.cli list                    # List all inventions
python -m davinci_codex.cli plan --slug <name>      # Show planning assumptions
python -m davinci_codex.cli simulate --slug <name>  # Run simulation
python -m davinci_codex.cli build --slug <name>     # Generate CAD/build artifacts
python -m davinci_codex.cli evaluate --slug <name>  # Review feasibility/ethics
```

## Architecture

### Module System
The project uses a plugin-based architecture for inventions. Each invention is a Python module in `src/davinci_codex/inventions/` that must implement:

1. **Module attributes:**
   - `SLUG`: Unique identifier
   - `TITLE`: Display name
   - `STATUS`: Development status (planning/in_progress/validated/prototype_ready)
   - `SUMMARY`: Brief description

2. **Required functions:**
   - `plan()`: Returns planning assumptions and design parameters
   - `simulate(seed=0)`: Runs simulation with deterministic seed
   - `build()`: Generates CAD models or build artifacts
   - `evaluate()`: Returns feasibility and safety analysis

### Registry Pattern
The `registry.py` module dynamically discovers invention modules using Python's `pkgutil`. Inventions are accessed through the `InventionSpec` dataclass which wraps modules with metadata.

### CAD Integration
CAD models live in `cad/<invention_name>/model.py` and are imported dynamically by invention modules using `importlib`. CAD scripts use parametric design (no binary files committed).

### Artifact Management
The `artifacts/` directory stores generated outputs (simulations, plots, CAD exports). Use `ensure_artifact_dir()` to create invention-specific subdirectories.

## Implementation Guidelines

### Historical Accuracy
- Reference original Codex folios (Atlanticus, Leicester, Madrid) with catalog IDs
- Document da Vinci's original intent and obstacles in `docs/<invention>.md`
- Explain modern solutions while respecting Renaissance engineering constraints

### Safety Requirements
- Focus on civil/educational inventions only
- Exclude weaponizable or harmful designs
- Include failure analysis in `evaluate()` function
- Document safety margins and ethical considerations

### Testing Approach
- Each invention has corresponding tests in `tests/test_<invention>.py`
- Tests verify mathematical calculations, simulation determinism, and artifact generation
- Use fixed seeds for reproducible stochastic simulations

## Current Inventions

- **aerial_screw**: Helical rotor lift feasibility (in_progress)
- **self_propelled_cart**: Spring-driven automaton cart (prototype_ready)
- **mechanical_odometer**: Survey cart with pebble-drop counter (prototype_ready)

## Adding New Inventions

1. Create module in `src/davinci_codex/inventions/<slug>.py`
2. Implement all required protocol functions
3. Add CAD model in `cad/<slug>/model.py` if applicable
4. Write tests in `tests/test_<slug>.py`
5. Document in `docs/<slug>.md` with provenance and safety notes
6. Update README.md invention index