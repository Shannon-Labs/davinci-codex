---
layout: landing
title: The da Vinci Codex
nav_order: 1
permalink: /
hero:
  title: Leonardo's mechanical inventions, rebuilt responsibly
  description: |
    Explore reproducible engineering research, interactive simulations, and open CAD derived from da Vinci's notebooks.
    
    - Parametric CAD models with full provenance tracking
    - Deterministic physics simulations validated against historical constraints
    - Safety-first approach with FMEA analysis and ethical review
  background: images/hero-texture.png
  cta:
    - label: Explore inventions
      href: "#inventions"
      style: primary
    - label: View interactive essays
      href: "book/index.html"
      style: secondary
meta:
  description: Open engineering reconstruction of Leonardo da Vinci’s civil inventions with simulations, CAD, and safety analysis.
  image: /docs/images/codex_logo.png
social:
  twitter: https://twitter.com/shannon_labs
  github: https://github.com/Shannon-Labs/davinci-codex
  email: safety@davinci-codex.org
sections:
  - id: overview
    title: Trustworthy computational archaeology
    intro: |
      The da Vinci Codex project translates Renaissance mechanical concepts into validated, reproducible implementations. Each module tracks provenance, quantitative planning, simulation, safety review, and modern fabrication pathways.
    cards:
      - title: Historical provenance
        body: Codex folio references, dimensional recovery, and intent interpretation mapped to modern units.
      - title: Engineering execution
        body: Deterministic simulations, parametric CAD models, and validated surrogate physics.
      - title: Ethical stewardship
        body: Exclusively civil inventions, FMEA-based safety margins, and transparent assumptions.
  - id: pipeline
    title: Invention Pipeline
    intro: Each invention follows a rigorous four-stage methodology ensuring historical accuracy, technical validity, and safety compliance.
    pipeline:
      - title: Plan
        icon: images/icons/plan.svg
        description: Research historical provenance, extract dimensions from Codex folios, and establish design parameters with modern unit conversions.
      - title: Simulate
        icon: images/icons/simulate.svg
        description: Run deterministic physics simulations with validated surrogate models, quantify performance envelopes, and verify against historical constraints.
      - title: Build
        icon: images/icons/build.svg
        description: Generate parametric CAD models, export fabrication-ready artifacts (STL/STEP), and document assembly procedures with tolerances.
      - title: Evaluate
        icon: images/icons/evaluate.svg
        description: Conduct FMEA safety analysis, assess feasibility metrics, identify ethical considerations, and recommend next steps.
  - id: highlights
    title: Current highlights
    layout: split
    primary:
      heading: Aerial Screw rotor breakthrough
      bullets:
        - text: 1,416 N lift with 4× efficiency improvement using variable-pitch control
        - text: Eagle-inspired taper geometry tuned via blade-element momentum methods
        - text: 99-piece CAD package with stress validation ≥ 2.0 safety factor
      cta:
        label: Read case study
        href: aerial_screw.md
      quote:
        text: "If a man have a tent made of linen of which the apertures have all been stopped up, and it be twelve braccia across and twelve in depth, he will be able to throw himself down from any great height without sustaining any injury."
        attribution: Leonardo da Vinci, Codex Atlanticus, f. 381v
    secondary:
      image: images/aerial_screw_performance.png
      caption: Variable pitch rotor performance envelope derived from integrated CFD + structural models.
  - id: inventions
    title: Active invention portfolio
    description: Status-tracked modules ready for exploration and replication.
    table:
      headers: [Module, Status, Summary]
      rows:
        - ["[Aerial Screw Rotor Lab](aerial_screw.md)", "validated", "Variable-pitch swashplate, 4× lift gain, CAD + simulation artifacts"]
        - ["[Self-Propelled Cart](self_propelled_cart.md)", "prototype_ready", "Programmable spring drive with kinematic validation"]
        - ["[Mechanical Odometer](mechanical_odometer.md)", "prototype_ready", "Pebble-drop surveying with calibrated tolerances"]
        - ["[Pyramid Parachute](parachute.md)", "prototype_ready", "Safety dossier with turbulence, tensile, and drop telemetry"]
        - ["[Self-Supporting Revolving Bridge](revolving_bridge.md)", "in_progress", "Counterweight trials, rotation envelope, structural proofs"]
        - ["[Ornithopter Flight Lab](ornithopter.md)", "in_progress", "Modal, telemetry, and aerodynamic acceptance campaign"]
  - id: resources
    title: Engineering resources
    columns:
      - heading: Interactive essays
        description: Reproducible Jupyter Book build with executed notebooks and derivations.
        links:
          - label: Launch the book
            href: book/index.html
          - label: Build locally
            href: ../README.md#-quick-start
      - heading: CAD & artifacts
        description: Parametric scripts and generated STL/STEP assets for physical prototyping.
        links:
          - label: Browse CAD library
            href: ../cad/
          - label: Artifact archive
            href: ../artifacts/
      - heading: Simulation + safety
        description: Deterministic runs, validation suites, and ethics/performance reviews.
        links:
          - label: Validation briefs
            href: #validation
          - label: Safety charter
            href: ../ETHICS.md
  - id: validation
    title: Validation briefs
    cards:
      - title: Parachute safety dossier
        body: Turbulence envelopes, tensile coupons, and hazard mitigation for prototype readiness.
        link:
          label: View report
          href: parachute_safety_dossier.md
      - title: Revolving bridge modernization
        body: Rotation profile CSVs, counterweight calibration, and field deployment instrumentation.
        link:
          label: View report
          href: revolving_bridge.md
      - title: Ornithopter validation log
        body: Dyno, modal, and telemetry analysis tracking acceptance metrics.
        link:
          label: View log
          href: ornithopter_validation.md
  - id: research
    title: Latest Research
    description: Recent technical analyses and specification developments from the engineering team.
    cards:
      - title: Aerial Screw Blade Element Analysis
        body: Variable-pitch swashplate optimization using blade element momentum theory, achieving 4× lift improvement with 82% rotor efficiency.
        link:
          label: Read specifications
          href: specifications/aerial_screw_specifications.md
      - title: Mechanical Lion Cam Programming
        body: Synchronized choreography system with polynomial interpolation, achieving ±2° angular precision across 12-second performance cycle.
        link:
          label: View cam design
          href: mechanical_lion.md
      - title: Parachute Turbulence Envelope
        body: Terminal velocity analysis with drag coefficient validation under varying atmospheric conditions and fabric permeability studies.
        link:
          label: See safety dossier
          href: parachute_safety_dossier.md
  - id: contribute
    title: Contribute & collaborate
    intro: Review contribution guidelines, safety scope, and provenance requirements before submitting changes.
    buttons:
      - label: Contribution guide
        href: ../CONTRIBUTING.md
      - label: Open issues
        href: https://github.com/Shannon-Labs/davinci-codex/issues
  - id: contact
    title: Contact
    list:
      - label: Maintainer
        value: Hunter Bown (Shannon Labs)
      - label: Email
        value: hunter@shannonlabs.dev
      - label: Project site
        value: https://shannon-labs.github.io/davinci-codex/
      - label: Repository
        value: https://github.com/Shannon-Labs/davinci-codex
---
