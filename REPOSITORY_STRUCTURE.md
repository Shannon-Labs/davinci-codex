# da Vinci Codex - Repository Structure Guide

## 🏛️ Professional Organization

This document outlines the systematic organization of the da Vinci Codex repository, following Renaissance principles of order and beauty while maintaining modern software engineering best practices.

## 📁 Core Directory Structure

```
davinci-codex/
├── 📚 PROJECT ROOT
│   ├── README.md                     # Project overview and getting started
│   ├── LICENSE                       # MIT License
│   ├── CITATION.cff                  # Academic citation metadata
│   ├── pyproject.toml               # Python project configuration
│   ├── requirements.txt             # Python dependencies
│   └── Makefile                     # Professional development automation
│
├── 🏛️ GOVERNANCE & PROCESS
│   ├── CODE_OF_CONDUCT.md          # Community standards
│   ├── CONTRIBUTING.md             # Contribution guidelines
│   ├── SECURITY.md                 # Security policies
│   ├── ETHICS.md                   # Non-weaponization charter
│   ├── METHODOLOGY.md              # Research methodology
│   └── ARCHITECTURE.md             # Technical architecture
│
├── 🔧 DEVELOPMENT INFRASTRUCTURE
│   ├── .github/                    # GitHub automation
│   │   ├── workflows/              # CI/CD pipelines
│   │   ├── ISSUE_TEMPLATE/         # Issue templates
│   │   └── PULL_REQUEST_TEMPLATE.md
│   ├── .pre-commit-config.yaml     # Code quality hooks
│   ├── docker-compose.yml          # Container orchestration
│   ├── Dockerfile                  # Container definitions
│   └── scripts/                    # Utility and automation scripts
│
├── 💻 SOURCE CODE
│   └── src/davinci_codex/          # Main Python package
│       ├── __init__.py
│       ├── cli.py                  # Command-line interface
│       ├── registry.py             # Invention discovery system
│       ├── pipelines.py            # Execution framework
│       ├── inventions/             # Leonardo's inventions
│       │   ├── aerial_screw.py
│       │   ├── ornithopter.py
│       │   ├── parachute.py
│       │   ├── mechanical_lion.py
│       │   └── ...
│       ├── core/                   # Shared utilities
│       │   ├── physics.py
│       │   ├── materials.py
│       │   └── validation.py
│       └── safety/                 # FMEA and safety analysis
│
├── 🧪 TESTING & VALIDATION
│   ├── tests/                      # Comprehensive test suite
│   │   ├── test_aerial_screw.py
│   │   ├── test_ornithopter.py
│   │   ├── integration/            # Integration tests
│   │   ├── benchmarks/             # Performance benchmarks
│   │   └── validation/             # Scientific validation
│   └── validation/                 # Validation studies and reports
│
├── 🏗️ ENGINEERING ASSETS
│   ├── cad/                        # Parametric CAD models
│   │   ├── aerial_screw/
│   │   ├── mechanical_lion/
│   │   └── shared_components/
│   ├── artifacts/                  # Generated outputs
│   │   ├── simulations/
│   │   ├── cad_exports/
│   │   └── documentation/
│   └── materials/                  # Renaissance material properties
│
├── 📚 DOCUMENTATION & WEBSITE
│   ├── docs/                       # GitHub Pages Jekyll site
│   │   ├── _config.yml             # Site configuration
│   │   ├── _layouts/               # Page layouts
│   │   ├── _includes/              # Reusable components
│   │   ├── assets/                 # CSS, JS, images
│   │   ├── index.md               # Landing page
│   │   ├── book/                   # Jupyter Book
│   │   └── inventions/             # Individual invention pages
│   └── notebooks/                  # Jupyter explorations
│
└── 🎓 EDUCATIONAL & RESEARCH
    ├── education/                  # Curriculum materials
    ├── examples/                   # Usage examples
    ├── research/                   # Academic papers and studies
    └── data/                       # Research datasets
```

## 🗂️ Consolidated Directories

### Primary Consolidation Areas

1. **Historical Research** → `PROVENANCE/`
   - Manuscript analysis
   - Folio references
   - Historical context

2. **Engineering Analysis** → `analysis/`
   - Performance studies
   - Comparative analysis
   - Technical reports

3. **Interactive Experiences** → `web/`
   - Web applications
   - Interactive demos
   - Virtual exhibitions

4. **Development Tools** → `tools/`
   - Build scripts
   - Generators
   - Utilities

## 🧹 Cleanup Actions Performed

### Removed/Consolidated
- ✅ Cleaned up Python cache files (`__pycache__/`, `.pytest_cache/`, `.ruff_cache/`)
- ✅ Organized build artifacts into `artifacts/`
- ✅ Consolidated scattered documentation
- ✅ Moved development tools to `tools/`
- ✅ Standardized naming conventions

### Enhanced Organization
- ✅ Professional `.gitignore` with comprehensive exclusions
- ✅ Standardized directory naming (snake_case)
- ✅ Clear separation of concerns
- ✅ Logical grouping of related files

## 📋 Directory Purpose Guide

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `src/` | Core source code | Python modules, CLI, algorithms |
| `tests/` | Quality assurance | Unit tests, integration tests, benchmarks |
| `docs/` | Documentation | Jekyll site, Jupyter Book, guides |
| `cad/` | 3D models | Parametric CAD, STL exports, drawings |
| `artifacts/` | Generated outputs | Simulation results, plots, reports |
| `materials/` | Historical data | Renaissance material properties |
| `education/` | Learning resources | Curricula, worksheets, tutorials |
| `examples/` | Usage demonstrations | Sample code, tutorials, guides |
| `tools/` | Development utilities | Scripts, generators, validators |
| `research/` | Academic work | Papers, studies, methodologies |

## 🎯 File Naming Conventions

### Python Modules
- **Snake case**: `aerial_screw.py`, `mechanical_lion.py`
- **Descriptive names**: Clear purpose indication
- **Consistent patterns**: Similar files follow same structure

### Documentation
- **UPPERCASE**: Major project documents (`README.md`, `LICENSE`)
- **Title Case**: User-facing guides (`Contributing.md`)
- **lowercase**: Technical docs and pages

### CAD and Assets
- **Descriptive paths**: `cad/aerial_screw/rotor_assembly.py`
- **Version control**: Avoid binary files in git
- **Organized hierarchy**: Logical nesting by invention

## 🔄 Maintenance Guidelines

1. **Regular Cleanup**: Remove temporary files and outdated assets
2. **Consistent Organization**: Follow established patterns for new files
3. **Documentation Updates**: Keep structure docs current with changes
4. **Access Control**: Maintain appropriate permissions and visibility
5. **Backup Strategy**: Ensure critical assets are preserved

## 🌟 Renaissance Principles Applied

Following Leonardo's approach to organization and documentation:

- **Systematic Categorization**: Like da Vinci's notebooks, organized by theme
- **Visual Clarity**: Clear hierarchy and logical flow
- **Comprehensive Documentation**: Nothing left unexplained
- **Cross-referencing**: Connections between related concepts
- **Aesthetic Beauty**: Pleasing and professional presentation

---

*"Simplicity is the ultimate sophistication."* - Leonardo da Vinci

This organizational structure reflects both Renaissance attention to detail and modern software engineering excellence.