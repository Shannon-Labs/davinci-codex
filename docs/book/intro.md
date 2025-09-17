# Codex Digitalis: Leonardo's Mechanical Visions Reborn

<div class="chapter-start">
"Obstacles do not bend me. Every obstacle yields to stern resolve."
— Leonardo da Vinci

In the flickering candlelight of his workshop, Leonardo sketched machines that would not fly for another 400 years. His notebooks—written in mirrored script and alive with gears, wings, and vortices—contained the DNA of modern engineering, waiting for the computational power to bring them to life. This digital codex bridges five centuries, using verifiable physics and open simulations to test and illuminate the mechanical intuitions of history’s greatest polymath.

Our goal is both scientific and artistic: to treat each validation as a miniature illuminated manuscript. Every chapter blends narrative with derivation, rendering models with the aesthetic warmth of parchment while holding fast to modern standards of reproducibility. Where Leonardo reasoned by sketch, we reason by notebook; where he layered chalk and ink, we layer equations, code, and measured data.
</div>

## How to Read This Book

- Begin with the Physics Derivations to understand the governing models: added-mass and unsteady lift, gear tooth bending, and rolling tribology. See {doc}`physics/index`.
- Explore the Validation Notebooks to see the models exercised against canonical experiments and historical designs. Data and figures are embedded for clarity and provenance.
- Follow the narrative marginalia: short notes in the style of Leonardo’s workshop that connect modern results to original folio sketches, historical experiments, and material practice.

## Renaissance Meets Silicon

Leonardo’s process was iterative, comparative, and relentlessly empirical. He did not simply draw; he measured, annotated, and revised. This project mirrors that ethic:

- Historical context anchors each essay—why a wing beats, why a tooth bends, why a parachute “fills.”
- Clean derivations and unit-tested helpers maintain scientific rigor.
- Visualizations are tuned for interpretability first, beauty always.

Throughout, we adopt a Renaissance palette—sepia grounds, golden accents, deep blues—and subtle typographic cues (decorated drop caps, script flourishes) to evoke the feel of an illuminated folio without sacrificing accessibility.

## The Gallery of Machines

- Ornithopter: Unsteady aerodynamics meet living kinematics. We compare added-mass predictions and phase-lag behavior to modern FSI references.
- Pyramid Parachute: From Fausto Veranzio to da Vinci’s sketch, canopy inflation and descent are quantified with fill time, Cd, and terminal velocity envelopes.
- Gears: Lewis bending theory and stress convergence tie hand-drafted involutes to today’s design limits.
- Rolling Friction: Contact, slip, and hysteresis captured in tribological sweeps.
- NACA 0012 Oscillation: A modern surrogate for airfoil dynamics that calibrates our aero toolkit.

Each chapter begins with a short epigraph—Latin and English—and a historical vignette. Where possible, we link to the corresponding folio or faithful reproduction, and we flag any interpretive gaps or safety caveats.

## Using the Codex

Build the book locally, or explore notebooks interactively:

```bash
make book
open docs/book/_build/html/index.html

# Or explore interactively
jupyter lab notebooks/
```

Provenance is preserved across the repository. Datasets live under `validation/`; figures under `docs/images/`; and derivations under `docs/book/physics/`. All notebooks in this Jupyter Book execute during build to ensure results and text remain synchronized.

## Navigation

- Physics Foundations → {doc}`physics/index`
- Validation Essays → see the left navigation for Ornithopter, Parachute, Gears, Rolling Friction, and NACA 0012.
- Project overview and artifact gallery → `docs/index.md`.

"Learning never exhausts the mind." May the same spirit guide this digital workshop as we bring Leonardo’s machines to life—faithfully, beautifully, and openly.
