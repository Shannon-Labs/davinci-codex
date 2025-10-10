# File Structure Plan for Renaissance Music Adapter

## Overview

This document outlines the complete file structure for the Renaissance Music Adapter system, following the project's established conventions and ensuring proper organization of modules, tests, data, and documentation.

## Directory Structure

```
src/davinci_codex/
├── music_adapter/                    # Main package for Renaissance music adapter
│   ├── __init__.py                   # Package initialization and main interface
│   ├── cli.py                        # Command-line interface for music adapter
│   │
│   ├── core/                         # Core data structures and utilities
│   │   ├── __init__.py
│   │   ├── models.py                 # Core data models (MusicalScore, etc.)
│   │   ├── midi_parser.py            # MIDI file parsing
│   │   ├── abc_parser.py             # ABC notation parsing
│   │   └── score_normalizer.py       # Format normalization between input types
│   │
│   ├── analysis/                     # Music analysis modules
│   │   ├── __init__.py
│   │   ├── style_analyzer.py         # Renaissance style analysis
│   │   ├── structure_analyzer.py     # Musical form and structure analysis
│   │   ├── harmony_analyzer.py       # Harmonic content analysis
│   │   ├── rhythm_analyzer.py        # Rhythmic content analysis
│   │   ├── voice_analyzer.py         # Voice leading and texture analysis
│   │   └── analysis_pipeline.py      # Complete analysis pipeline
│   │
│   ├── constraints/                  # Constraint management and validation
│   │   ├── __init__.py
│   │   ├── instrument_db.py          # Instrument constraint database
│   │   ├── constraint_engine.py      # Main constraint enforcement engine
│   │   ├── pitch_validator.py        # Pitch constraint validation
│   │   ├── voice_validator.py        # Voice/polyphony constraint validation
│   │   ├── timing_validator.py       # Timing and duration constraint validation
│   │   ├── dynamic_validator.py      # Dynamic constraint validation
│   │   └── ensemble_validator.py     # Ensemble-level constraint validation
│   │
│   ├── patterns/                     # Renaissance musical patterns
│   │   ├── __init__.py
│   │   ├── pattern_library.py        # Main pattern library interface
│   │   ├── dance_patterns.py         # Dance rhythm patterns
│   │   ├── cadence_patterns.py       # Cadence patterns
│   │   ├── ornamentation_patterns.py # Ornamentation patterns
│   │   ├── modal_patterns.py         # Modal scale patterns
│   │   ├── pattern_matcher.py        # Pattern matching functionality
│   │   └── pattern_applier.py        # Pattern application functionality
│   │
│   ├── adaptation/                   # Music adaptation modules
│   │   ├── __init__.py
│   │   ├── adaptation_engine.py      # Main adaptation engine
│   │   ├── voice_adapter.py          # Voice count adaptation
│   │   ├── range_mapper.py           # Pitch range adaptation
│   │   ├── harmony_simplifier.py     # Harmony simplification
│   │   ├── rhythm_adapter.py         # Rhythm adaptation
│   │   ├── tempo_adjuster.py         # Tempo adjustment
│   │   ├── ornamentation_adapter.py  # Ornamentation adaptation
│   │   └── adaptation_optimizer.py   # Optimization of adaptation choices
│   │
│   ├── validation/                   # Validation and testing modules
│   │   ├── __init__.py
│   │   ├── validation_system.py      # Main validation system
│   │   ├── mechanical_validator.py   # Mechanical feasibility validation
│   │   ├── musical_validator.py      # Musical integrity validation
│   │   ├── simulation/               # Simulation modules
│   │   │   ├── __init__.py
│   │   │   ├── mechanical_simulator.py  # Mechanical performance simulation
│   │   │   ├── performance_simulator.py # Performance simulation
│   │   │   └── acoustic_simulator.py    # Acoustic simulation
│   │   └── analysis/                 # Validation analysis modules
│   │       ├── __init__.py
│   │       ├── playability_analyzer.py  # Playability analysis
│   │       ├── risk_analyzer.py         # Risk analysis
│   │       └── quality_analyzer.py      # Quality analysis
│   │
│   ├── integration/                  # Integration with existing systems
│   │   ├── __init__.py
│   │   ├── ensemble_interface.py     # Interface with Mechanical Ensemble
│   │   ├── audio_interface.py        # Interface with Audio System
│   │   ├── cad_interface.py          # Interface with CAD System
│   │   └── simulation_interface.py   # Interface with Simulation System
│   │
│   └── converters/                   # Data format converters
│       ├── __init__.py
│       ├── score_converter.py        # Score format conversion
│       ├── event_converter.py        # Event format conversion
│       └── parameter_converter.py    # Parameter format conversion
│
├── mechanical_ensemble.py            # Extended with Renaissance music support
├── core/
│   └── audio.py                      # Extended with adapted score rendering
│
├── tests/                            # Test suite
│   ├── test_music_adapter/           # Tests for music adapter
│   │   ├── __init__.py
│   │   ├── test_core/                # Core module tests
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_midi_parser.py
│   │   │   ├── test_abc_parser.py
│   │   │   └── test_score_normalizer.py
│   │   ├── test_analysis/            # Analysis module tests
│   │   │   ├── __init__.py
│   │   │   ├── test_style_analyzer.py
│   │   │   ├── test_structure_analyzer.py
│   │   │   ├── test_harmony_analyzer.py
│   │   │   ├── test_rhythm_analyzer.py
│   │   │   └── test_voice_analyzer.py
│   │   ├── test_constraints/         # Constraint module tests
│   │   │   ├── __init__.py
│   │   │   ├── test_constraint_engine.py
│   │   │   ├── test_pitch_validator.py
│   │   │   ├── test_voice_validator.py
│   │   │   └── test_timing_validator.py
│   │   ├── test_patterns/            # Pattern module tests
│   │   │   ├── __init__.py
│   │   │   ├── test_pattern_library.py
│   │   │   ├── test_dance_patterns.py
│   │   │   └── test_cadence_patterns.py
│   │   ├── test_adaptation/         # Adaptation module tests
│   │   │   ├── __init__.py
│   │   │   ├── test_adaptation_engine.py
│   │   │   ├── test_voice_adapter.py
│   │   │   └── test_range_mapper.py
│   │   ├── test_validation/          # Validation module tests
│   │   │   ├── __init__.py
│   │   │   ├── test_validation_system.py
│   │   │   ├── test_mechanical_validator.py
│   │   │   └── test_musical_validator.py
│   │   ├── test_integration/        # Integration tests
│   │   │   ├── __init__.py
│   │   │   ├── test_ensemble_integration.py
│   │   │   ├── test_audio_integration.py
│   │   │   └── test_cad_integration.py
│   │   └── test_converters/          # Converter tests
│   │       ├── __init__.py
│   │       └── test_score_converter.py
│   │
│   ├── conftest.py                   # Pytest configuration and fixtures
│   └── test_data/                    # Test data files
│       ├── renaissance_music/        # Sample Renaissance music files
│       │   ├── midi/
│       │   │   ├── pavana.mid
│       │   │   ├── galliard.mid
│       │   │   └── basse_danse.mid
│       │   └── abc/
│       │       ├── pavana.abc
│       │       ├── galliard.abc
│       │       └── basse_danse.abc
│       └── expected_outputs/         # Expected test outputs
│           ├── adapted_scores/
│           ├── validation_reports/
│           └── simulation_results/
│
├── data/                             # Data files
│   ├── renaissance_patterns/         # Pattern library data
│   │   ├── dance_patterns.yaml       # Dance rhythm patterns
│   │   ├── cadence_patterns.yaml     # Cadence patterns
│   │   ├── ornamentation_patterns.yaml # Ornamentation patterns
│   │   └── modal_patterns.yaml       # Modal scale patterns
│   ├── instrument_constraints/        # Instrument constraint data
│   │   ├── mechanical_drum.yaml      # Mechanical drum constraints
│   │   ├── mechanical_organ.yaml     # Mechanical organ constraints
│   │   ├── mechanical_trumpeter.yaml # Mechanical trumpeter constraints
│   │   ├── mechanical_carillon.yaml  # Mechanical carillon constraints
│   │   ├── viola_organista.yaml      # Viola organista constraints
│   │   └── programmable_flute.yaml   # Programmable flute constraints
│   └── sample_music/                 # Sample Renaissance pieces
│       ├── midi/                     # MIDI format samples
│       └── abc/                      # ABC notation samples
│
├── docs/                             # Documentation
│   ├── renaissance_music_adapter/    # Documentation for music adapter
│   │   ├── architecture.md           # System architecture overview
│   │   ├── user_guide.md             # User guide
│   │   ├── developer_guide.md        # Developer guide
│   │   ├── api_reference.md          # API reference
│   │   ├── examples/                 # Usage examples
│   │   │   ├── basic_adaptation.md
│   │   │   ├── custom_constraints.md
│   │   │   └── pattern_application.md
│   │   └── images/                   # Documentation images
│   │       ├── architecture_diagram.png
│   │       ├── workflow_diagram.png
│   │       └── example_outputs.png
│   └── provenance/                   # Provenance documentation
│       ├── renaissance_sources.md    # Historical music sources
│       └── mechanical_principles.md  # Mechanical instrument principles
│
├── sims/                             # Simulation configurations and results
│   ├── renaissance_music/            # Renaissance music simulations
│   │   ├── configs/                  # Simulation configurations
│   │   │   ├── mechanical_validation.yaml
│   │   │   ├── performance_simulation.yaml
│   │   │   └── acoustic_analysis.yaml
│   │   └── results/                  # Simulation results
│   │       ├── mechanical_performance/
│   │       ├── acoustic_analysis/
│   │       └── validation_reports/
│   └── templates/                    # Simulation templates
│       ├── mechanical_template.yaml
│       └── acoustic_template.yaml
│
├── cad/                              # CAD files and scripts
│   ├── renaissance_instruments/      # CAD models for Renaissance instruments
│   │   ├── mechanical_drum/
│   │   ├── mechanical_organ/
│   │   ├── mechanical_trumpeter/
│   │   ├── mechanical_carillon/
│   │   ├── viola_organista/
│   │   └── programmable_flute/
│   └── scripts/                      # CAD generation scripts
│       ├── generate_mechanical_visualization.py
│       └── export_performance_animation.py
│
└── notebooks/                        # Exploratory notebooks
    ├── renaissance_music_analysis/   # Music analysis notebooks
    │   ├── style_characteristics.ipynb
    │   ├── harmonic_analysis.ipynb
    │   └── rhythmic_patterns.ipynb
    ├── adaptation_experiments/       # Adaptation experiment notebooks
    │   ├── voice_reduction_strategies.ipynb
    │   ├── range_mapping_techniques.ipynb
    │   └── pattern_application_methods.ipynb
    └── validation_studies/           # Validation study notebooks
        ├── mechanical_feasibility.ipynb
        ├── musical_integrity.ipynb
        └── performance_simulation.ipynb
```

## Module Organization Details

### Core Module (music_adapter/core/)

The core module contains fundamental data structures and utilities:

- **models.py**: Defines all core data structures (MusicalScore, MusicalNote, etc.)
- **midi_parser.py**: Handles parsing of MIDI files into internal format
- **abc_parser.py**: Handles parsing of ABC notation files into internal format
- **score_normalizer.py**: Normalizes different input formats to unified representation

### Analysis Module (music_adapter/analysis/)

The analysis module contains components for understanding Renaissance music:

- **style_analyzer.py**: Analyzes Renaissance style characteristics
- **structure_analyzer.py**: Identifies musical forms and structures
- **harmony_analyzer.py**: Analyzes harmonic content and relationships
- **rhythm_analyzer.py**: Analyzes rhythmic patterns and characteristics
- **voice_analyzer.py**: Analyzes voice leading and texture
- **analysis_pipeline.py**: Orchestrates complete analysis process

### Constraints Module (music_adapter/constraints/)

The constraints module manages mechanical limitations:

- **instrument_db.py**: Database of instrument constraints
- **constraint_engine.py**: Main engine for enforcing constraints
- **pitch_validator.py**: Validates pitch constraints
- **voice_validator.py**: Validates voice/polyphony constraints
- **timing_validator.py**: Validates timing and duration constraints
- **dynamic_validator.py**: Validates dynamic constraints
- **ensemble_validator.py**: Validates ensemble-level constraints

### Patterns Module (music_adapter/patterns/)

The patterns module contains Renaissance musical patterns:

- **pattern_library.py**: Main interface for pattern library
- **dance_patterns.py**: Dance rhythm patterns (pavana, galliard, etc.)
- **cadence_patterns.py**: Cadence patterns (authentic, plagal, etc.)
- **ornamentation_patterns.py**: Ornamentation patterns (trills, mordents, etc.)
- **modal_patterns.py**: Modal scale patterns
- **pattern_matcher.py**: Matches patterns in musical scores
- **pattern_applier.py**: Applies patterns to adapted scores

### Adaptation Module (music_adapter/adaptation/)

The adaptation module modifies scores for mechanical compatibility:

- **adaptation_engine.py**: Main engine for score adaptation
- **voice_adapter.py**: Adapts voice count and distribution
- **range_mapper.py**: Maps pitch ranges to instrument capabilities
- **harmony_simplifier.py**: Simplifies harmonic content
- **rhythm_adapter.py**: Adapts rhythmic content
- **tempo_adjuster.py**: Adjusts tempo for mechanical instruments
- **ornamentation_adapter.py**: Adapts ornamentation
- **adaptation_optimizer.py**: Optimizes adaptation choices

### Validation Module (music_adapter/validation/)

The validation module ensures mechanical feasibility and musical integrity:

- **validation_system.py**: Main validation system interface
- **mechanical_validator.py**: Validates mechanical feasibility
- **musical_validator.py**: Validates musical integrity
- **simulation/**: Simulation submodules
  - **mechanical_simulator.py**: Simulates mechanical performance
  - **performance_simulator.py**: Simulates performance characteristics
  - **acoustic_simulator.py**: Simulates acoustic output
- **analysis/**: Validation analysis submodules
  - **playability_analyzer.py**: Analyzes playability
  - **risk_analyzer.py**: Analyzes performance risks
  - **quality_analyzer.py**: Analyzes musical quality

### Integration Module (music_adapter/integration/)

The integration module connects with existing systems:

- **ensemble_interface.py**: Interface with Mechanical Ensemble
- **audio_interface.py**: Interface with Audio System
- **cad_interface.py**: Interface with CAD System
- **simulation_interface.py**: Interface with Simulation System

### Converters Module (music_adapter/converters/)

The converters module handles data format conversion:

- **score_converter.py**: Converts between score formats
- **event_converter.py**: Converts between event formats
- **parameter_converter.py**: Converts between parameter formats

## Data Organization

### Pattern Data (data/renaissance_patterns/)

Pattern data is stored in YAML format for easy editing and version control:

- **dance_patterns.yaml**: Dance rhythm patterns with timing and accent information
- **cadence_patterns.yaml**: Cadence patterns with voice leading
- **ornamentation_patterns.yaml**: Ornamentation patterns with execution details
- **modal_patterns.yaml**: Modal scale patterns with characteristic intervals

### Instrument Constraints (data/instrument_constraints/)

Instrument constraints are stored in YAML format:

- **mechanical_drum.yaml**: Constraints for mechanical drum
- **mechanical_organ.yaml**: Constraints for mechanical organ
- **mechanical_trumpeter.yaml**: Constraints for mechanical trumpeter
- **mechanical_carillon.yaml**: Constraints for mechanical carillon
- **viola_organista.yaml**: Constraints for viola organista
- **programmable_flute.yaml**: Constraints for programmable flute

### Sample Music (data/sample_music/)

Sample Renaissance music in both MIDI and ABC formats for testing and examples.

## Test Organization

### Test Structure (tests/test_music_adapter/)

Tests mirror the structure of the main package:

- **test_core/**: Tests for core modules
- **test_analysis/**: Tests for analysis modules
- **test_constraints/**: Tests for constraint modules
- **test_patterns/**: Tests for pattern modules
- **test_adaptation/**: Tests for adaptation modules
- **test_validation/**: Tests for validation modules
- **test_integration/**: Integration tests
- **test_converters/**: Tests for converter modules

### Test Data (tests/test_data/)

Test data includes:

- **renaissance_music/**: Sample Renaissance music files
- **expected_outputs/**: Expected outputs for verification

## Documentation Organization

### Documentation Structure (docs/renaissance_music_adapter/)

Documentation includes:

- **architecture.md**: System architecture overview
- **user_guide.md**: User guide for using the adapter
- **developer_guide.md**: Developer guide for extending the system
- **api_reference.md**: Complete API reference
- **examples/**: Usage examples with detailed explanations

## Simulation Organization

### Simulation Structure (sims/renaissance_music/)

Simulation files include:

- **configs/**: Configuration files for different simulation types
- **results/**: Results from simulation runs
- **templates/**: Template configurations for new simulations

## CAD Organization

### CAD Structure (cad/renaissance_instruments/)

CAD files include:

- Individual instrument directories with CAD models
- **scripts/**: Scripts for generating visualizations and animations

## Notebook Organization

### Notebook Structure (notebooks/)

Exploratory notebooks include:

- **renaissance_music_analysis/**: Music analysis notebooks
- **adaptation_experiments/**: Adaptation experiment notebooks
- **validation_studies/**: Validation study notebooks

This file structure provides a comprehensive organization for the Renaissance Music Adapter system, following established conventions and ensuring maintainability and extensibility.