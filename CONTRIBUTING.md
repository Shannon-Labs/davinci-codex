# Contributing to the da Vinci Codex Project

## Welcome Contributors!

Thank you for your interest in contributing to the computational reconstruction of Leonardo da Vinci's mechanical inventions. This project thrives on collaboration between engineers, historians, educators, and enthusiasts worldwide.

## Ground Rules
- **License alignment:** All source code must be MIT-compatible. Generated docs, figures, meshes, and audio are released under CC0. Do not commit assets with unclear provenance.
- **Safety first:** Avoid weaponizable, harmful, or privacy-invasive concepts. If in doubt, open an issue before drafting a design.
- **Reproducibility:** Every addition should run headless via `make setup && make test && make demo`. Include deterministic seeds for stochastic simulations.
- **Documentation:** Provide provenance notes (folio IDs, catalog references), engineering assumptions, and ethical considerations in `docs/<slug>.md`.
- **Testing:** Add pytest coverage for new modules. Prefer unit-checked math and deterministic fixtures.

## Getting Started

### 1. Fork the Repository
Click the "Fork" button at the top of the [repository page](https://github.com/Shannon-Labs/davinci-codex) to create your own copy.

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/davinci-codex.git
cd davinci-codex
git remote add upstream https://github.com/Shannon-Labs/davinci-codex.git
```

### 3. Set Up Development Environment
```bash
make setup  # Creates virtual environment and installs dependencies
make test   # Verify everything works
```

### 4. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# Examples: feature/hydraulic-pump, fix/ornithopter-lift, docs/german-translation
```

### 5. Make Your Changes
- Write clean, documented code
- Add tests for new functionality
- Update relevant documentation
- Ensure historical accuracy

### 6. Test Your Changes
```bash
make lint   # Check code style
make test   # Run test suite
make demo   # Generate visualizations
```

### 7. Commit Your Changes
```bash
git add .
git commit -m "Add hydraulic pump invention from Codex Atlanticus f.386v"
```

### 8. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 9. Create Pull Request
- Go to your fork on GitHub
- Click "New Pull Request"
- Select your feature branch
- Fill out the PR template completely
- Submit for review

## Types of Contributions

### 🎨 New Inventions
Implement additional da Vinci designs:
- Research original manuscripts
- Create mathematical models
- Implement simulations
- Add safety analysis
- Document provenance

### 🔬 Enhanced Simulations
Improve existing models:
- Refine physics calculations
- Add CFD analysis
- Optimize performance
- Validate against experiments

### 📚 Documentation
Expand project knowledge:
- Translate documentation
- Add historical context
- Create tutorials
- Improve code comments

### 🧪 Testing
Strengthen quality assurance:
- Add unit tests
- Create integration tests
- Improve test coverage
- Add performance benchmarks

### 🎓 Educational Content
Develop learning materials:
- Jupyter notebooks
- Lesson plans
- Video tutorials
- Workshop materials

## Code Standards

### Python Style
- Python 3.9+ compatible
- Type hints required for public APIs
- Maximum line length: 100 characters
- Use `ruff` for linting
- Use `mypy` for type checking

### Documentation
- Docstrings for all public functions (Google style)
- Inline comments for complex algorithms
- Mathematical equations in LaTeX format
- References to original folios

### Testing
- Minimum 80% test coverage for new code
- Deterministic tests with fixed seeds
- Performance tests for simulations
- Safety validation tests

### Commit Messages
- Clear, descriptive messages
- Reference issue numbers
- Include manuscript references where applicable
- Example: `Add hydraulic pump from Codex Atlanticus f.386v (#42)`

## Review Process

### What We Look For
1. **Historical Accuracy**: Correct manuscript references
2. **Technical Correctness**: Valid physics and mathematics
3. **Safety Compliance**: Non-weaponized implementations
4. **Code Quality**: Clean, tested, documented
5. **Educational Value**: Clear explanations and learning opportunities

### Review Timeline
- Initial response: 2-3 days
- Full review: 1 week
- Merge decision: 2 weeks

## Community

### Communication Channels
- **GitHub Issues**: Bug reports, feature requests, and general questions
- **Pull Requests**: Code contributions
- **Email**: Direct communication with project maintainers

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Maintain academic integrity
- Respect historical accuracy
- Prioritize safety and ethics

## Recognition

Contributors will be:
- Listed in project credits
- Mentioned in release notes
- Acknowledged in publications
- Invited to collaborate on papers

## Contributors
- Hunter Bown (Shannon Labs) - Project lead and initial implementations
- Claude Opus 4.1 - Documentation architecture and development workflow automation
- Codex GPT-5 (High) - AI agent collaboration and engineering analysis
- Codex CLI Agent - Repository hygiene, contributor tooling, and guidelines authoring

## Questions?

If you have questions about contributing:
1. Check existing [issues](https://github.com/Shannon-Labs/davinci-codex/issues) and discussions
2. Review closed [pull requests](https://github.com/Shannon-Labs/davinci-codex/pulls?q=is%3Apr+is%3Aclosed)
3. Open a new issue for questions or suggestions
4. Email: hunter@shannonlabs.dev

---

**Thank you for helping preserve and share Leonardo da Vinci's engineering legacy!**