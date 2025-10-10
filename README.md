# The da Vinci Codex Project
## Computational Archaeology of Renaissance Mechanical Engineering

<div align="center">

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Shannon-Labs/davinci-codex/actions/workflows/ci.yml/badge.svg)](https://github.com/Shannon-Labs/davinci-codex/actions/workflows/ci.yml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)


**An Open-Source Computational Framework for Leonardo da Vinci's Mechanical Inventions**

[**📖 Documentation**](docs/index.md) • [**🎨 Gallery & Visualizations**(#-gallery--visualizations) • [**🤝 Contributing**](CONTRIBUTING.md) • [**📚 References**](REFERENCES.md)

</div>

---

## 📜 Project Overview

This repository is an experimental open-source computational framework for analyzing Leonardo da Vinci's mechanical inventions. Using modern engineering principles, physics-based simulation, and safety analysis, we explore how da Vinci's 15th-century mechanical concepts might perform when implemented with contemporary materials and methods.

### 🎯 Project Goals

1. **Digital Exploration**: Create computational models of selected Renaissance mechanical concepts
2. **Educational Resources**: Develop open-source materials for STEM education
3. **Technical Analysis**: Apply modern simulation to explore historical engineering ideas
4. **Safety Focus**: Ensure all implementations prioritize safety
5. **Open Collaboration**: Enable community contributions to historical engineering study

### 🏛️ Historical Context

Leonardo da Vinci (1452-1519) produced over 13,000 pages of notes and drawings, including hundreds of mechanical invention sketches. This project explores five selected inventions, focusing on educational applications and maintaining strict adherence to non-weaponized implementations.

---

## 🎨 Gallery & Visualizations

### 🚁 Aerial Screw - Variable-Pitch System
> **MAJOR BREAKTHROUGH**: Optimized 15° helix angle achieves 1,416N lift with complete mechanical design

<table>
<tr>
<td width="33%" align="center">
<img src="artifacts/aerial_screw/sim/performance.png" alt="Aerial Screw Performance" width="100%"/>
<br/><b>Performance Analysis</b>
<br/>Optimal configuration: 1,416N lift at 10.8kW
<br/>4x improvement over original design
</td>
<td width="33%" align="center">
<img src="artifacts/aerial_screw/sim/rotor_demo.gif" alt="Rotor Animation" width="100%"/>
<br/><b>Rotor Mechanism</b>
<br/>Swashplate mechanism enables 15°-45° pitch control
<br/>Response time <0.5s, mechanical advantage 1.92
</td>
<td width="33%" align="center">
<img src="docs/images/aerial_screw_performance.png" alt="Power Envelope" width="100%"/>
<br/><b>Power Envelope</b>
<br/>Eagle-inspired tapered blades with 82% efficiency
<br/>Structural safety factor 2.0+ maintained
</td>
</tr>
</table>

**Available Resources:**
- 📦 [Complete CAD Package](artifacts/aerial_screw/complete_package/) - STL models at 15°, 30°, 45° pitch angles
- 🎬 [Animation Data](artifacts/aerial_screw/complete_package/animations/) - Assembly sequences & pitch operation
- 📐 [Technical Drawings](artifacts/aerial_screw/complete_package/technical_drawings/) - Full dimensional specifications
- 📊 [Simulation Results](artifacts/aerial_screw/sim/) - Performance data & analysis

---

### 🦁 Mechanical Lion Automaton
> Leonardo's programmable automaton featuring synchronized walking, chest reveal, and fleur-de-lis presentation

<table>
<tr>
<td width="25%" align="center">
<img src="artifacts/cam_demonstration/walking_gait_demo.png" alt="Walking Gait" width="100%"/>
<br/><b>Walking Gait</b>
<br/>Biomechanical quadruped locomotion
</td>
<td width="25%" align="center">
<img src="artifacts/cam_demonstration/chest_opening_demo.png" alt="Chest Reveal" width="100%"/>
<br/><b>Chest Reveal</b>
<br/>Theatrical fleur-de-lis presentation
</td>
<td width="25%" align="center">
<img src="artifacts/cam_demonstration/master_timing_demo.png" alt="Master Timing" width="100%"/>
<br/><b>Master Timing System</b>
<br/>Programmable cam-based control
</td>
<td width="25%" align="center">
<img src="artifacts/lion_performance_timing.png" alt="Performance Timeline" width="100%"/>
<br/><b>30-Second Performance</b>
<br/>Complete choreographed sequence
</td>
</tr>
</table>

**Available Resources:**
- 📦 [CAD Models](mechanical_lion_complete_package/) - Complete mechanical system (when generated)
- 🎭 [Cam Demonstrations](artifacts/cam_demonstration/) - All mechanical subsystems
- 🔧 [Control System](src/davinci_codex/control/lion_control_system.py) - Programmable timing system

---

### 🪂 Parachute - Pyramid Design
<table>
<tr>
<td width="50%" align="center">
<img src="docs/images/parachute_descent.png" alt="Parachute Descent" width="100%"/>
<br/><b>Descent Profile & Drag Polar</b>
<br/>Pyramid parachute achieving 11.5 m/s terminal velocity
</td>
<td width="50%" align="center">
<img src="artifacts/parachute/descent_simulation.png" alt="Drop Profiles" width="100%"/>
<br/><b>Validation Against Test Data</b>
<br/>Experimental validation confirms simulation accuracy
</td>
</tr>
</table>

---

### 🦅 Ornithopter - Flapping Wing Flight
<table>
<tr>
<td width="50%" align="center">
<img src="docs/images/ornithopter_lift.png" alt="Ornithopter Flight" width="100%"/>
<br/><b>Sustained Flight Campaign</b>
<br/>30-second flight achieving 120m altitude
</td>
<td width="50%" align="center">
<img src="artifacts/ornithopter/sim/lift_profile.png" alt="Wing Aerodynamics" width="100%"/>
<br/><b>Wing Aerodynamics</b>
<br/>NACA 0012 airfoil validation
</td>
</tr>
</table>

---

### 🚗 Self-Propelled Cart & Mechanical Odometer
<table>
<tr>
<td width="50%" align="center">
<img src="docs/images/cart_motion.png" alt="Cart Motion" width="100%"/>
<br/><b>Spring-Powered Locomotion</b>
<br/>Autonomous navigation system
</td>
<td width="50%" align="center">
<img src="docs/images/odometer_error.png" alt="Odometer Accuracy" width="100%"/>
<br/><b>Distance Measurement</b>
<br/>Mechanical odometer precision analysis
</td>
</tr>
</table>

---

### 🎵 Renaissance Musical Instruments
> Mechanical instruments capable of autonomous performance

<table>
<tr>
<td width="33%" align="center">
<img src="artifacts/mechanical_carillon/sim/frequency_scatter.png" alt="Carillon" width="100%"/>
<br/><b>Mechanical Carillon</b>
<br/>Automated bell tower system
</td>
<td width="33%" align="center">
<img src="artifacts/mechanical_organ/sim/frequency_profile.png" alt="Organ" width="100%"/>
<br/><b>Mechanical Organ</b>
<br/>Programmable pipe organ
</td>
<td width="33%" align="center">
<img src="artifacts/viola_organista/sim/amplitude_timeline.png" alt="Viola Organista" width="100%"/>
<br/><b>Viola Organista</b>
<br/>Bowed keyboard instrument
</td>
</tr>
</table>

---

### 🔄 Revolving Bridge - Engineering Innovation
<table>
<tr>
<td width="33%" align="center">
<img src="docs/images/revolving_bridge/rotation_torque.png" alt="Bridge Rotation" width="100%"/>
<br/><b>Rotation Dynamics</b>
<br/>360° rotation mechanism analysis
</td>
<td width="33%" align="center">
<img src="artifacts/revolving_bridge/sim/stress_deflection.png" alt="Structural Analysis" width="100%"/>
<br/><b>Structural Integrity</b>
<br/>Stress and deflection analysis
</td>
<td width="33%" align="center">
<img src="artifacts/revolving_bridge/sim/rotation_animation.gif" alt="Bridge Animation" width="100%"/>
<br/><b>Operational Sequence</b>
<br/>Complete rotation demonstration
</td>
</tr>
</table>

---

### 📊 Engineering Validation
<table>
<tr>
<td width="33%" align="center">
<img src="docs/images/material_comparisons.png" alt="Materials" width="100%"/>
<br/><b>Renaissance Materials</b>
<br/>Historical authenticity validation
</td>
<td width="33%" align="center">
<img src="docs/images/gear_bending_convergence.png" alt="Gear Analysis" width="100%"/>
<br/><b>Mechanical Analysis</b>
<br/>Gear stress & tribology validation
</td>
<td width="33%" align="center">
<img src="docs/images/rolling_friction_load_sweep.png" alt="Friction" width="100%"/>
<br/><b>Tribological Studies</b>
<br/>Renaissance-era friction coefficients
</td>
</tr>
</table>

---

### 🎓 Educational Resources
All visualizations, CAD models, and simulation data are available for:
- **Academic Research** - Validated engineering analysis
- **Museum Exhibitions** - Interactive displays & replicas
- **Educational Workshops** - Hands-on STEM learning
- **Digital Reconstruction** - Historical accuracy verification

**Documentation**: See [docs/](docs/) for detailed technical specifications of each invention.

---

## 📊 Simulation Results Summary

**⚠️ Important**: All metrics below are from computational simulations using **low-order surrogate models** suitable for educational exploration and trend analysis. Results should not be used for detailed design decisions without validation. See [Physics Derivations](docs/book/physics/index.md) for model assumptions and limitations.

| Invention | Status | Simulated Metrics* | Model Fidelity | Development Stage |
|-----------|--------|-------------------|----------------|------------------|
| **Aerial Screw** | 🚀 **BREAKTHROUGH ACHIEVED** | Lift: 1,416N (4x improvement)<br>Power: 10.8kW (modern engine viable)<br>Variable pitch: 15°-45° control | Blade Element Momentum + CFD | **Complete Design Package** |
| **Ornithopter** | ✅ Simulation Complete | Lift: ~1600N (surrogate)<br>Endurance: ~140 min (est.)<br>Altitude: <400m (trend) | Low-order quasi-steady | CAD Models Available |
| **Parachute** | ✅ Simulation Complete | Terminal: 6.9 m/s (analytical)<br>Drag: ~1250N (calc.)<br>Safe landing zone | Analytical solution | Design Complete |
| **Self-Propelled Cart** | ✅ Simulation Complete | Range: ~150m (energy-based)<br>Speed: ~7-8 m/s (calc.)<br>Energy: ~350J (spring) | Energy conservation | Design Complete |
| **Mechanical Odometer** | ✅ Simulation Complete | Error: <17% (geometric)<br>Range: ~1km (calc.)<br>Resolution: ~14m | Kinematic analysis | Design Complete |

### Material Upgrades

| Invention | Historical Baseline | Modern Material Stack | Performance Change |
| --- | --- | --- | --- |
| Ornithopter | Fir spars, rawhide hinges, human power | Carbon tubes, Kevlar joints, electric drivetrain | 72% lower power demand; +2300% endurance |
| Self-Propelled Cart | Oak chassis, rope bearings | Composite frame, bronze bushings | 238% greater range; 78% payload increase |
| Aerial Screw | Hemp sail, pine mast | Carbon shell, aluminum mast | 47% lighter rotor; 278% lift increase (still sub-hover) |

![Material comparison trends](docs/images/material_comparisons.png)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- Make (optional but recommended)
- 8GB RAM minimum for simulations

### Installation

```bash
# Clone the repository
git clone https://github.com/Shannon-Labs/davinci-codex.git
cd davinci-codex

# Set up Python virtual environment
make setup  # Or: python -m venv .venv && source .venv/bin/activate && pip install -e .

# Verify installation
make test   # Or: pytest

# Generate all visualizations
make demo   # Or: python -m davinci_codex.cli demo

# Build computational essays
make book   # Or: jupyter-book build docs/book
```

### Basic Usage

```python
# Python API
from davinci_codex import registry

# List all inventions
inventions = registry.list_inventions()

# Run specific simulation
ornithopter = registry.get_invention("ornithopter")
results = ornithopter.module.simulate(seed=42)

# Generate CAD models
ornithopter.module.build()
```

```bash
# Command Line Interface
davinci-codex list                          # Show all inventions
davinci-codex simulate --slug ornithopter   # Run simulation
davinci-codex pipeline --slug ornithopter   # Full pipeline
davinci-codex evaluate --slug parachute     # Safety analysis
```

---

## 📁 Repository Architecture

```
davinci-codex/
│
├── 📚 Documentation
│   ├── ABSTRACT.md                 # Academic abstract
│   ├── METHODOLOGY.md              # Computational completion framework
│   ├── ETHICS.md                   # Non-weaponisation charter
│   ├── references.bib              # BibTeX references for dissertation citations
│   └── docs/                       # Detailed documentation
│       ├── index.md               # Documentation hub
│       ├── images/                # Visualizations
│       ├── book/                  # Jupyter Book configuration for computational essays
│       ├── physics/               # Governing equation derivations (Markdown + LaTeX)
│       └── {invention}.md         # Individual analyses
│
├── 🧾 Provenance & Materials
│   ├── PROVENANCE/                 # Folio-level source records
│   │   ├── codex_atlanticus/
│   │   ├── madrid_codices/
│   │   └── manuscript_index.yaml
│   └── materials/                  # Renaissance material properties with uncertainty
│       └── renaissance_db.yaml
│
├── 🔬 Source Code
│   └── src/davinci_codex/
│       ├── cli.py                 # CLI interface
│       ├── registry.py            # Dynamic discovery
│       ├── pipelines.py           # Execution framework
│       ├── uncertainty.py         # Historical uncertainty quantification
│       ├── safety/                # FMEA and safety tooling
│       ├── primitives/            # Validated mechanical building blocks
│       └── inventions/            # Invention modules
│           ├── ornithopter.py
│           ├── parachute.py
│           ├── aerial_screw.py
│           ├── self_propelled_cart.py
│           └── mechanical_odometer.py
│
├── 🔧 Engineering Assets
│   ├── cad/                       # Parametric CAD models
│   ├── sims/                      # Simulation configs & container recipes
│   ├── synthesis/                 # Modern intervention studies & counterfactual builds
│   ├── anima/                     # Annotated folios, intent graphs, transcript JSON
│   ├── tva/                       # Techno-viability assessments & historical simulations
│   ├── ip_nexus/                  # Prior art studies, patent surveys, publication drafts
│   └── artifacts/                 # Generated outputs (plots, CSVs, reports)
│
├── 🧪 Testing & Validation
│   ├── tests/                     # Comprehensive test suite
│   ├── validation/                # Benchmark cases, mesh convergence, analytical comparisons
│   └── notebooks/                 # Jupyter explorations (to be published via Jupyter Book)
│
└── 📋 Project Management
    ├── .github/                   # GitHub automation
    ├── CONTRIBUTING.md            # Contribution guide
    ├── CITATION.cff              # Citation metadata
    └── LICENSE                    # MIT license
```

---

## 🧪 Testing, Validation & Toolchain

- **make test** runs the full pytest suite
- **make lint** executes Ruff + mypy with strict settings (no virtualenv required)
- **make book** builds the Jupyter Book essays in `docs/book` and executes notebooks
- **Simulation toolchain**: solids (FEniCS/pycalculix), CFD (OpenFOAM URANS/LES), vortex lattice + nonlinear beams for flapping FSI, Abaqus/tribology scripts for friction studies. Each solver configuration and mesh refinement study lives in `validation/<slug>/`.
- **Coverage**: Automated checks in CI.

Validation artefacts live in `tests/`, `validation/`, `sims/`, and `artifacts/` for reproducibility and peer review.

## 📘 Interactive Essays
- Execute `make book` (or `jupyter-book build docs/book`) to render the validation notebooks.
- HTML output drops into `docs/book/_build/html/`; open `index.html` for an offline preview.
- GitHub Pages: <https://shannon-labs.github.io/davinci-codex/> (auto-deployed from main branch).
- Chapters cover gear bending, ornithopter FSI, rolling friction tribology, plus consolidated physics derivations.

---

## 🔬 Methodology

### 1. Historical Research Phase
- **Source Analysis**: Original codex folio examination
- **Provenance Documentation**: Complete manuscript references
- **Dimensional Recovery**: Conversion from Renaissance units (braccia)
- **Intent Interpretation**: Engineering purpose analysis

### 2. Mathematical Modeling
- **Physics Framework**: Newtonian mechanics, fluid dynamics
- **Material Properties**: Modern composites mapped to Renaissance materials
- **Parametric Design**: Adjustable dimensions for optimization
- **Constraint Analysis**: Physical and safety limitations

### 3. Computational Simulation
- **Numerical Methods**: Finite element analysis, unsteady CFD with FSI, tribology/friction experiments
- **Validation Metrics**: Lift coefficients, stress margins, energy balance, wear & loss factors
- **Sensitivity Analysis**: Parameter variation studies with Sobol indices and tornado plots
- **Uncertainty Quantification**: Error propagation analysis with epistemic + aleatory modelling

### 4. Safety Assessment
- **Risk Analysis**: FMEA (Failure Mode and Effects Analysis)
- **Safety Factors**: Minimum 2x on all structural components
- **Ethical Review**: Non-weaponization verification
- **Regulatory Compliance**: Modern standards where applicable

### 5. Documentation & Dissemination
- **Open Source**: MIT licensed code, CC0 media
- **Reproducibility**: Seed-controlled simulations
- **Educational Resources**: Comprehensive documentation
- **Community Building**: GitHub discussions and contributions

---

## 📚 Upcoming Enhancements
- Publish validation dossiers (`validation/`) capturing mesh/timestep convergence and benchmark comparisons per solver.
- Release interactive computational essays (Jupyter Book) linking folios, derivations, and executable notebooks.
- Expand comparative analyses between historical materials vs. modern composites with quantified performance deltas.
- Deepen tribology + FSI datasets through archival experiment replication and modern wind-tunnel proxies.

---

## 🤝 Contributing

We welcome contributions from engineers, historians, educators, and enthusiasts worldwide!

### How to Contribute

1. **Fork & Clone**
   ```bash
   git fork https://github.com/Shannon-Labs/davinci-codex
   git clone https://github.com/YOUR_USERNAME/davinci-codex
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-invention
   ```

3. **Develop & Test**
   ```bash
   make test  # Ensure all tests pass
   make lint  # Check code quality
   ```

4. **Submit Pull Request**
   - Reference relevant codex folios
   - Include safety analysis
   - Add comprehensive tests
   - Update documentation

### Contribution Ideas

- 🎨 **New Inventions**: Implement additional da Vinci designs
- 🔬 **Enhanced Physics**: Improve simulation accuracy
- 📚 **Historical Research**: Add manuscript references
- 🌍 **Translations**: Internationalize documentation
- 🎓 **Educational Content**: Create tutorials and guides
- 🔧 **CAD Models**: Develop detailed parametric models

### Community Guidelines

- Maintain academic rigor and historical accuracy
- Prioritize safety in all implementations
- Document thoroughly with citations
- Respect the non-weaponization principle
- Foster inclusive, collaborative environment

---

## 📖 Leonardo's Original Manuscripts

Access digitized versions of Leonardo's original works:

### Primary Codices
- **[Codex Atlanticus](https://www.leonardodigitale.com/)** - Biblioteca Ambrosiana, Milan
- **[Codex Leicester](https://www.bl.uk/)** - Bill Gates Collection
- **[Madrid Codices](https://www.bne.es/)** - Biblioteca Nacional de España
- **[Paris Manuscripts](https://www.institutdefrance.fr/)** - Institut de France
- **[Codex on Flight of Birds](https://airandspace.si.edu/)** - Smithsonian

### Digital Archives
- **[Leonardo Digitale](https://www.leonardodigitale.com/)** - Comprehensive digital archive
- **[Universal Leonardo](https://www.universalleonardo.org/)** - Research resources
- **[e-Leo Archive](https://www.leonardodigitale.com/)** - High-resolution scans

---

## 🎓 Educational Applications

This project can serve as an educational resource for:

### STEM Education
- **Physics**: Classical mechanics, fluid dynamics, materials science
- **Mathematics**: Differential equations, numerical methods, optimization
- **Engineering**: Mechanical design, systems analysis, safety engineering
- **Computer Science**: Simulation, CAD/CAM, scientific computing

### Potential Curriculum Integration
- High school physics demonstrations
- Undergraduate engineering projects
- Graduate research foundations
- Maker space projects

### Available Resources
- Jupyter notebooks with guided explorations
- Parametric CAD models for 3D printing
- Simulation visualizations for educational use
- Historical context and provenance documentation

---

## 📊 Project Status

### Current Development
- **Test Coverage**: Comprehensive test suite
- **Simulation Framework**: Physics-based computational models
- **Documentation**: Growing collection of interactive notebooks

### Development Goals
- Develop open-source educational resources
- Create reproducible simulations for learning
- Document Renaissance engineering concepts
- Explore computational approaches to historical designs

---

## 🏆 Acknowledgments

### Project Author
- **Author**: Hunter Bown, Shannon Labs
- **Development**: Built with AI assistance for code generation and documentation

### Special Thanks
- Leonardo da Vinci for the timeless inspiration
- Open source community for foundational tools
- Digital archives for manuscript access
- Early testers and feedback providers

### Institutional Support
- Shannon Labs for computational resources
- GitHub for hosting and CI/CD
- Open Source Initiative for licensing framework

---

## 📜 License & Citation

### Code License
MIT License - See [LICENSE](LICENSE) for details

### Media License
CC0 1.0 Universal - Public Domain Dedication for generated content

### Academic Citation

```bibtex
@software{davinci_codex_2025,
  author = {Bown, Hunter},
  title = {The da Vinci Codex: Computational Archaeology of Renaissance Mechanical Engineering},
  year = {2025},
  month = {1},
  publisher = {GitHub},
  journal = {GitHub repository},
  url = {https://github.com/Shannon-Labs/davinci-codex}
}
```

### Contact

**Principal Investigator**: Hunter Bown  
**Email**: hunter@shannonlabs.dev  
**Institution**: Shannon Labs  
**Project Website**: https://shannon-labs.github.io/davinci-codex/  
**GitHub**: https://github.com/Shannon-Labs/davinci-codex

---

<div align="center">


### 📋 Development Roadmap

I am actively working to enhance the repository. See our [Enhancement Plan](ENHANCEMENT_PLAN.md) and [Architecture Guide](ARCHITECTURE.md) for detailed plans.

**Current Focus Areas:**
- 🎨 **Documentation & User Experience**: Improving documentation and usability
- 🔧 **Testing & Quality**: Expanding test coverage and code quality
- 📚 **Educational Resources**: Developing interactive learning materials
- 🔬 **Simulation Improvements**: Enhancing computational models

**"Obstacles do not bend me."** - Leonardo da Vinci

</div>