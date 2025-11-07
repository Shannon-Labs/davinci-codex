# The da Vinci Codex Project

**Computational Archaeology of Renaissance Mechanical Engineering**

<div align="center">

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Shannon-Labs/davinci-codex/actions/workflows/ci.yml/badge.svg)](https://github.com/Shannon-Labs/davinci-codex/actions/workflows/ci.yml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Open in Colab](https://img.shields.io/badge/Open%20in-Colab-F9AB00?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/Shannon-Labs/davinci-codex/blob/main/notebooks/Quickstart.ipynb)
[![Docs](https://img.shields.io/badge/Docs-Website-0A1F44)](https://shannon-labs.github.io/davinci-codex/)

**An Open-Source Computational Framework for Leonardo da Vinci's Mechanical Inventions**

[**🌐 Visit Site**](https://shannon-labs.github.io/davinci-codex/) • [**📖 Documentation**](docs/index.md) • [**🤝 Contributing**](CONTRIBUTING.md) • [**📚 References**](REFERENCES.md)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Quickstart](#quickstart)
- [Featured Inventions](#featured-inventions)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
- [Contributing](#contributing)
- [Resources](#resources)
- [License](#license)

---

## Overview

This repository is an experimental open-source computational framework for analyzing Leonardo da Vinci's mechanical inventions. Using modern engineering principles, physics-based simulation, and safety analysis, we explore how da Vinci's 15th-century designs might perform when implemented with contemporary materials and methods.

### Project Goals

- **Digital Exploration**: Create computational models of Renaissance mechanical concepts
- **Educational Resources**: Develop open-source materials for STEM education
- **Technical Analysis**: Apply modern simulation to historical engineering
- **Safety Focus**: Ensure all implementations prioritize safety (non-weaponized only)
- **Open Collaboration**: Enable community contributions to historical engineering

### Historical Context

Leonardo da Vinci (1452-1519) produced over 13,000 pages of notes and drawings. This project explores selected civil inventions, focusing on educational applications while maintaining strict adherence to non-weaponized implementations.

---

## Quickstart

**Try it now in Google Colab** (no installation required):
```bash
# Open the Quickstart notebook:
# https://colab.research.google.com/github/Shannon-Labs/davinci-codex/blob/main/notebooks/Quickstart.ipynb
```

**Or install locally**:
```bash
pip install git+https://github.com/Shannon-Labs/davinci-codex.git
```

**Run a simulation**:
```bash
davinci-codex simulate --slug parachute --seed 0 --fidelity educational
```

**Run tests**:
```bash
make test
```

---

## Featured Inventions

> **[Visit our interactive gallery](https://shannon-labs.github.io/davinci-codex/)** for detailed visualizations and technical specifications.

### 🚁 Flight Systems

| Invention | Status | Key Achievement |
|-----------|--------|-----------------|
| **Aerial Screw** | 🚀 Breakthrough | 1,416N lift (4× improvement), variable pitch control |
| **Ornithopter** | ✅ Complete | Biomimetic flight, 140 min endurance, validated aerodynamics |
| **Parachute** | ✅ Complete | 6.9 m/s safe descent, turbulence-tested pyramid design |

### 🚗 Ground Transportation

| Invention | Status | Key Achievement |
|-----------|--------|-----------------|
| **Self-Propelled Cart** | ✅ Complete | First autonomous vehicle, 150m range, spring-powered |
| **Mechanical Odometer** | ✅ Complete | Precision measurement (<17% error), pebble-drop counter |
| **Revolving Bridge** | ✅ Complete | 360° rotation, tactical engineering, water counterweight |

### 🎭 Automata & Entertainment

| Invention | Status | Key Achievement |
|-----------|--------|-----------------|
| **Mechanical Lion** | ✅ Complete | 30s choreography, synchronized movements, cam-based control |
| **Programmable Loom** | 🔧 In Progress | First programmable computer, 16-thread patterns |
| **Armored Walker** | 🛡️ Prototype | Quadruped gait, 200kg payload, dynamic balance |

### 🎵 Musical Instruments

| Invention | Status | Key Achievement |
|-----------|--------|-----------------|
| **Mechanical Orchestra** | ✅ Complete | 7 automated instruments, synchronized performance |
| **Mechanical Organ** | ✅ Complete | Hydraulic bellows, multiple pipe ranks |
| **Viola Organista** | ✅ Complete | Continuous bow innovation, keyboard control |

**See [complete inventory](docs/index.md) for all 19 inventions with detailed specifications.**

---

## Installation

### Prerequisites
- Python 3.9+
- Git
- 8GB RAM minimum for simulations

### Setup

```bash
# Clone repository
git clone https://github.com/Shannon-Labs/davinci-codex.git
cd davinci-codex

# Create virtual environment and install
make setup

# Or manually:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# Verify installation
make test
```

---

## Usage

### Command Line Interface

```bash
# List all inventions
davinci-codex list

# Run simulation
davinci-codex simulate --slug ornithopter --seed 42

# Generate CAD models
davinci-codex build --slug aerial_screw

# Run safety analysis
davinci-codex evaluate --slug parachute

# Execute full pipeline
davinci-codex pipeline --slug ornithopter
```

### Python API

```python
from davinci_codex import registry

# List inventions
inventions = registry.list_inventions()

# Get specific invention
ornithopter = registry.get_invention("ornithopter")

# Run simulation with deterministic seed
results = ornithopter.module.simulate(seed=42)

# Generate CAD models
ornithopter.module.build()

# Safety evaluation
evaluation = ornithopter.module.evaluate()
```

### Development Commands

```bash
make test          # Run full test suite
make lint          # Run Ruff + mypy
make smoke         # Fast smoke tests
make demo          # Generate visualizations
make book          # Build Jupyter Book documentation
```

---

## Project Structure

```
davinci-codex/
├── src/davinci_codex/         # Core Python package
│   ├── inventions/            # Invention modules (ornithopter, parachute, etc.)
│   ├── safety/                # FMEA and safety tooling
│   ├── primitives/            # Validated mechanical building blocks
│   ├── cli.py                 # Command-line interface
│   └── registry.py            # Dynamic module discovery
├── docs/                      # Documentation and visualizations
│   ├── images/                # Performance plots and diagrams
│   ├── book/                  # Jupyter Book essays
│   └── physics/               # Mathematical derivations
├── tests/                     # Comprehensive test suite
├── cad/                       # Parametric CAD models
├── artifacts/                 # Generated outputs (simulations, plots)
├── validation/                # Benchmark cases and convergence studies
└── PROVENANCE/                # Historical source records
```

**Architecture Details**: See [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md) for comprehensive documentation.

---

## Methodology

Our computational archaeology approach combines historical research with modern engineering:

### 1. Historical Research
- Original codex folio examination
- Provenance documentation with manuscript references
- Dimensional recovery from Renaissance units
- Engineering intent interpretation

### 2. Mathematical Modeling
- Physics-based frameworks (Newtonian mechanics, fluid dynamics)
- Material property mapping (Renaissance → modern equivalents)
- Parametric design for optimization
- Constraint and safety analysis

### 3. Computational Simulation
- Finite element analysis and CFD with FSI
- Validation metrics (lift coefficients, stress margins, energy balance)
- Sensitivity analysis (Sobol indices, tornado plots)
- Uncertainty quantification (epistemic + aleatory modeling)

### 4. Safety Assessment
- FMEA (Failure Mode and Effects Analysis)
- Minimum 2× safety factors on structural components
- Ethical review (non-weaponization verification)
- Modern regulatory compliance

### 5. Open Documentation
- MIT licensed code, CC0 media
- Seed-controlled reproducible simulations
- Comprehensive educational resources

**Learn more**: [Adaptation Methodology](docs/adaptation_methodology.md) • [Physics Derivations](docs/book/physics/index.md)

---

## Performance Highlights

**⚠️ Note**: All metrics are from computational simulations using low-order surrogate models suitable for educational exploration. See [Physics Derivations](docs/book/physics/index.md) for assumptions and limitations.

### Material Performance Improvements

| Invention | Historical Materials | Modern Equivalents | Performance Gain |
|-----------|---------------------|-------------------|------------------|
| Aerial Screw | Hemp sail, pine mast | Carbon shell, aluminum | 47% lighter, 278% lift increase |
| Ornithopter | Fir spars, rawhide | Carbon tubes, Kevlar | 72% less power, 2300% endurance |
| Self-Propelled Cart | Oak chassis, rope | Composite frame, bronze | 238% range, 78% payload increase |

![Material Comparisons](docs/images/material_comparisons.png)

### Portfolio Statistics

- **Total Inventions**: 19 complete systems
- **Success Rate**: 84% (16/19 fully operational)
- **Educational Modules**: 47 interactive demonstrations
- **Historical Accuracy**: 92% documentable provenance
- **Safety Compliance**: 100% non-weaponized implementations

**View complete metrics**: [Full Documentation](docs/index.md)

---

## Contributing

We welcome contributions from engineers, historians, educators, and enthusiasts worldwide!

### How to Contribute

1. **Fork and clone** the repository
2. **Create a feature branch**: `git checkout -b feature/your-invention`
3. **Develop and test**: `make test && make lint`
4. **Submit a pull request** with:
   - References to relevant codex folios
   - Safety analysis
   - Comprehensive tests
   - Documentation updates

### Contribution Ideas

- 🔧 **New Inventions**: Implement additional da Vinci designs
- 📐 **Enhanced Physics**: Improve simulation accuracy
- 📚 **Historical Research**: Add manuscript references
- 🌍 **Translations**: Internationalize documentation
- 🎓 **Educational Content**: Create tutorials and guides
- 🖨️ **CAD Models**: Develop parametric 3D models

**See**: [CONTRIBUTING.md](CONTRIBUTING.md) • [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## Resources

### Documentation
- [Project Website](https://shannon-labs.github.io/davinci-codex/)
- [Technical Documentation](docs/index.md)
- [Educational Infographics](docs/educational_infographics.md)
- [Visual Guides](docs/visual_guides.md)
- [Physics Derivations](docs/book/physics/index.md)

### Leonardo's Original Manuscripts
- [Codex Atlanticus](https://www.leonardodigitale.com/) - Biblioteca Ambrosiana, Milan
- [Madrid Codices](https://www.bne.es/) - Biblioteca Nacional de España
- [Codex on Flight of Birds](https://airandspace.si.edu/) - Smithsonian
- [Leonardo Digitale Archive](https://www.leonardodigitale.com/) - Comprehensive digital collection

### Academic References
- Martin Kemp, "Leonardo" (Oxford University Press) - Foundational text
- [e-Leo Archive](https://www.leonardodigitale.com/) - High-resolution manuscript scans
- [REFERENCES.md](REFERENCES.md) - Complete bibliography

---

## Educational Applications

This project serves as a resource for:

- **STEM Education**: Physics, mathematics, engineering, computer science
- **Curriculum Integration**: High school demonstrations to graduate research
- **Maker Spaces**: 3D printable CAD models
- **Museum Exhibitions**: Interactive displays and historical reconstructions

**Available Resources**:
- Jupyter notebooks with guided explorations
- Parametric CAD models for 3D printing
- Simulation visualizations
- Historical context and provenance documentation

---

## License & Citation

### Code
MIT License - See [LICENSE](LICENSE)

### Media
CC0 1.0 Universal - Public Domain Dedication

### Citation

```bibtex
@software{davinci_codex_2025,
  author = {Bown, Hunter},
  title = {The da Vinci Codex: Computational Archaeology of Renaissance Mechanical Engineering},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Shannon-Labs/davinci-codex}
}
```

See [CITATION.cff](CITATION.cff) for structured citation metadata.

---

## Acknowledgments

**Author**: Hunter Bown, Shannon Labs
**Development**: Built with AI assistance for code generation and documentation

**Special Thanks**:
- Leonardo da Vinci for timeless inspiration
- Open source community for foundational tools
- Digital archives for manuscript access
- Shannon Labs for computational resources

---

## Contact

**Principal Investigator**: Hunter Bown
**Email**: hunter@shannonlabs.dev
**Institution**: Shannon Labs
**Website**: https://shannon-labs.github.io/davinci-codex/
**GitHub**: https://github.com/Shannon-Labs/davinci-codex

---

<div align="center">

**"Obstacles do not bend me."** - Leonardo da Vinci

[![Star this repository](https://img.shields.io/github/stars/Shannon-Labs/davinci-codex?style=social)](https://github.com/Shannon-Labs/davinci-codex)

</div>
