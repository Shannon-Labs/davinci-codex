---
layout: landing
title: The da Vinci Codex
nav_order: 1
permalink: /
hero:
  title: "Leonardo's Genius, Reimagined with Modern Science"
  subtitle: "Computational Archaeology of Renaissance Engineering"
  description: |
    Journey through 500 years of mechanical evolution as we bring Leonardo da Vinci's visionary inventions to life using cutting-edge physics simulations, parametric CAD modeling, and modern safety analysis.
    
    **Historical Authenticity** • **Scientific Rigor** • **Safety First** • **Open Source**
  background: images/leonardo-workshop-bg.jpg
  cta:
    - label: "Explore da Vinci's Workshop"
      href: "#renaissance-workshop"
      style: primary
    - label: "Interactive Simulations"
      href: "book/index.html"
      style: secondary
    - label: "Playground"
      href: "/playground/"
      style: link
meta:
  description: "Experience Leonardo da Vinci's mechanical genius through interactive simulations, 3D models, and modern engineering analysis. Open-source computational archaeology."
  image: /docs/images/davinci-codex-hero.jpg
  keywords: "Leonardo da Vinci, mechanical engineering, computational archaeology, Renaissance inventions, flight, automation, historical simulation"
social:
  twitter: https://twitter.com/shannon_labs
  github: https://github.com/Shannon-Labs/davinci-codex
  email: hunter@shannonlabs.dev

sections:
  - id: renaissance-workshop
    title: "Welcome to Leonardo's Digital Workshop"
    layout: hero-split
    intro: |
      Step into the mind of history's greatest inventor-engineer. Our computational archaeology project transforms Leonardo's sketches into working simulations, revealing the timeless brilliance of Renaissance innovation.
    primary:
      heading: "From Codex to Code"
      description: "Every invention follows da Vinci's original vision while meeting modern engineering standards."
      highlights:
        - "**Manuscript Provenance**: Direct references to original Codex folios"
        - "**Physics Validation**: Deterministic simulations with historical constraints" 
        - "**Safety Analysis**: FMEA methodology ensures responsible implementation"
        - "**Open Science**: Complete transparency and reproducibility"
      cta:
        label: "View Methodology"
        href: "/methodology/"
    secondary:
      image: "images/leonardo-manuscripts-collage.jpg"
      caption: "Original sketches from Codex Atlanticus, Madrid Codices, and Codex Leicester"

  - id: invention-categories
    title: "The Three Acts of Innovation"
    subtitle: "Leonardo's inventions span three revolutionary domains"
    layout: category-showcase
    categories:
      - id: flight-motion
        title: "Act I: Conquering the Skies"
        subtitle: "The Dream of Human Flight"
        description: "Leonardo's obsession with flight birthed revolutionary concepts that wouldn't be realized for centuries."
        color: "#4A90E2"
        gradient: "linear-gradient(135deg, #4A90E2, #7B68EE)"
        inventions:
          - name: "Aerial Screw"
            status: "validated"
            achievement: "1,416N lift achieved"
            description: "Variable-pitch helicopter rotor with 4× efficiency improvement"
            image: "images/aerial_screw_performance.png"
            href: "aerial_screw.html"
            stats:
              - "Power: 10.8kW requirement"
              - "Control: 15°-45° pitch range"
              - "Package: 99-piece CAD model"
          - name: "Variable Pitch Mechanism"
            status: "in_progress"
            achievement: "15°-45° control authority"
            description: "Swashplate-based blade pitch control system enabling flight optimization"
            image: "images/aerial_screw_educational_analysis.png"
            href: "variable_pitch_mechanism.html"
            stats:
              - "Response: <0.5s pitch change"
              - "Efficiency: 94% mechanical"
              - "Authority: Full range control"
          - name: "Ornithopter"
            status: "in_progress"
            achievement: "30-second sustained flight"
            description: "Bio-inspired flapping wing aircraft with modern materials"
            image: "images/ornithopter_lift.png"
            href: "ornithopter.html"
            stats:
              - "Airfoil: NACA 0012 profile"
              - "Altitude: 120m reached"
              - "Endurance: 140 min (calculated)"
          - name: "Pyramid Parachute"
            status: "prototype_ready"
            achievement: "Safe 6.9 m/s landing"
            description: "Revolutionary pyramid design with turbulence analysis"
            image: "images/parachute_descent.png"
            href: "parachute.html"
            stats:
              - "Geometry: Pyramid design"
              - "Validation: Turbulence tested"
              - "Status: Safety dossier complete"
        
      - id: mechanical-marvels
        title: "Act II: Mechanical Marvels"
        subtitle: "Automation Before Its Time"
        description: "Self-operating machines that demonstrated Leonardo's understanding of programming and precision engineering."
        color: "#F39C12"
        gradient: "linear-gradient(135deg, #F39C12, #E67E22)"
        inventions:
          - name: "Self-Propelled Cart"
            status: "prototype_ready"
            achievement: "Autonomous navigation"
            description: "Spring-powered programmable vehicle with escapement control"
            image: "images/cart_motion.png"
            href: "self_propelled_cart.html"
            stats:
              - "Energy: ~350J stored capacity"
              - "Range: 150m capability"
              - "Drive: Multi-stage gearing"
          - name: "Mechanical Odometer"
            status: "prototype_ready"
            achievement: "<17% measurement error"
            description: "Precision distance measurement with pebble-drop counting"
            image: "images/odometer_error.png"
            href: "mechanical_odometer.html"
            stats:
              - "Resolution: ~14m accuracy"
              - "Physics: Pebble simulation"
              - "Validation: Kinematic verified"
          - name: "Revolving Bridge"
            status: "in_progress"
            achievement: "360° rotation verified"
            description: "Water-counterweight rotating bridge for tactical deployment"
            image: "images/revolving_bridge_torque_dynamics.png"
            href: "revolving_bridge.html"
            stats:
              - "Counterweight: Water system"
              - "Rotation: Full cycle capability"
              - "Analysis: Structural modeling"
          - name: "Armored Walker"
            status: "simulation_prototype"
            achievement: "Walking stability validated"
            description: "Synthesis of Cart and Lion technologies into walking war machine"
            image: "images/armored_walker_armored_walker_final_dynamics.png"
            href: "armored_walker.html"
            stats:
              - "Speed: 0.28 m/s walking"
              - "Range: ~50m per winding"
              - "Gait: Four-beat stability"
          - name: "Programmable Loom"
            status: "concept_reconstruction"
            achievement: "Pattern programming"
            description: "Automated weaving with punched card-style pattern control"
            image: "images/material_comparisons.png"
            href: "programmable_loom.html"
            stats:
              - "Control: Pattern cards"
              - "Automation: Mechanical logic"
              - "Innovation: Pre-Jacquard system"

      - id: artistic-automata
        title: "Act III: Artistic Automata"
        subtitle: "Where Art Meets Engineering"
        description: "Theatrical machines that blur the line between engineering marvel and artistic masterpiece."
        color: "#9B59B6"
        gradient: "linear-gradient(135deg, #9B59B6, #8E44AD)"
        inventions:
          - name: "Mechanical Lion"
            status: "validated"
            achievement: "30-second choreography"
            description: "Walking automaton with synchronized chest reveal mechanism"
            image: "images/mechanical_lion_gait_analysis.png"
            href: "mechanical_lion.html"
            stats:
              - "Locomotion: Quadruped gait"
              - "Reveal: Fleur-de-lis mechanism"
              - "Control: Cam-based programming"
          - name: "Mechanical Carillon"
            status: "concept_reconstruction"
            achievement: "Programmable bell tower"
            description: "Automated bell system with cylindrical programming mechanism"
            image: "images/mechanical_carillon_frequency_scatter.png"
            href: "mechanical_carillon.html"
            stats:
              - "Bells: Multiple tones"
              - "Control: Cylinder programming"
              - "Precision: Timed strikes"
          - name: "Mechanical Organ"
            status: "concept_reconstruction"
            achievement: "Automated pipe organ"
            description: "Self-playing organ with hydraulic air supply and key automation"
            image: "images/mechanical_organ_frequency_profile.png"
            href: "mechanical_organ.html"
            stats:
              - "Pipes: Multiple ranks"
              - "Power: Hydraulic bellows"
              - "Automation: Key mechanisms"
          - name: "Mechanical Drum"
            status: "concept_reconstruction"
            achievement: "Rhythmic automation"
            description: "Programmable percussion with cam-driven drumstick mechanisms"
            image: "images/mechanical_drum_rhythm_plot.png"
            href: "mechanical_drum.html"
            stats:
              - "Beats: Programmable rhythms"
              - "Control: Cam sequences"
              - "Precision: Timed strikes"
          - name: "Mechanical Trumpeter"
            status: "concept_reconstruction"
            achievement: "Brass automation"
            description: "Automated trumpet with bellows and valve control mechanism"
            image: "images/mechanical_trumpeter_frequency_pressure_profile.png"
            href: "mechanical_trumpeter.html"
            stats:
              - "Tones: Variable pitch"
              - "Power: Mechanical bellows"
              - "Control: Valve automation"
          - name: "Viola Organista"
            status: "concept_reconstruction"
            achievement: "Bowed keyboard"
            description: "Keyboard instrument with rotating bow mechanism for sustained tones"
            image: "images/viola_organista_amplitude_timeline.png"
            href: "viola_organista.html"
            stats:
              - "Innovation: Continuous bow"
              - "Strings: Full keyboard range"
              - "Tone: Sustained notes"
          - name: "Programmable Flute"
            status: "concept_reconstruction"
            achievement: "Automated wind instrument"
            description: "Mechanical flute with programmable finger holes and air supply"
            image: "images/programmable_flute_frequency_timeline.png"
            href: "programmable_flute.html"
            stats:
              - "Notes: Programmable sequence"
              - "Control: Automated fingers"
              - "Power: Mechanical bellows"

  - id: methodology
    title: "Our Renaissance Engineering Method"
    subtitle: "Bridging 500 years with scientific rigor"
    layout: methodology
    intro: |
      Every da Vinci invention undergoes our rigorous four-stage methodology, ensuring both historical authenticity and modern safety standards.
    stages:
      - title: "PLAN"
        icon: "images/icons/plan.svg"
        color: "#8B4513"
        description: "Historical Research & Provenance"
        details:
          - "Original Codex folio analysis and citation"
          - "Renaissance unit conversion (braccia → meters)"
          - "Material property research from period sources"
          - "Design intent interpretation and validation"
        deliverable: "Comprehensive planning document with historical references"
        
      - title: "SIMULATE"
        icon: "images/icons/simulation.svg"
        color: "#4A90E2"
        description: "Physics-Based Computational Analysis"
        details:
          - "Deterministic simulations with fixed seeds"
          - "Multi-physics modeling (CFD, FEA, dynamics)"
          - "Performance envelope characterization"
          - "Historical constraint validation"
        deliverable: "Validated simulation results with uncertainty analysis"
        
      - title: "BUILD"
        icon: "images/icons/build.svg"
        color: "#F39C12"
        description: "Parametric CAD & Manufacturing"
        details:
          - "Parametric 3D models with full history"
          - "Manufacturing drawings with tolerances"
          - "STL/STEP export for 3D printing/machining"
          - "Assembly instructions and bill of materials"
        deliverable: "Complete fabrication-ready CAD package"
        
      - title: "EVALUATE"
        icon: "images/icons/evaluate.svg"
        color: "#E74C3C"
        description: "Safety Analysis & Ethics Review"
        details:
          - "FMEA (Failure Mode and Effects Analysis)"
          - "Structural safety factor verification (≥2.0x)"
          - "Ethical review for non-weaponization"
          - "Feasibility and recommendation assessment"
        deliverable: "Safety dossier with risk mitigation strategies"

  - id: get-started
    title: "Begin Your Renaissance Journey"
    subtitle: "Choose your path into Leonardo's world"
    layout: get-started
    paths:
      - title: "Educator"
        description: "Bring Renaissance engineering to your classroom"
        icon: "education"
        color: "#2ECC71"
        steps:
          - "Browse curriculum modules"
          - "Download lesson plans"
          - "Access interactive simulations"
          - "Join educator community"
        cta:
          label: "Start Teaching"
          href: "education/"
        
      - title: "Researcher"
        description: "Dive deep into computational archaeology"
        icon: "research"
        color: "#3498DB"
        steps:
          - "Review methodology papers"
          - "Access raw simulation data"
          - "Explore validation studies"
          - "Contribute improvements"
        cta:
          label: "Join Research"
          href: "research/"
        
      - title: "Maker"
        description: "Build Leonardo's inventions yourself"
        icon: "maker"
        color: "#F39C12"
        steps:
          - "Download CAD models"
          - "Follow build guides"
          - "Access safety protocols"
          - "Share your creations"
        cta:
          label: "Start Building"
          href: "makers/"
        
      - title: "Explorer"
        description: "Discover the art of Renaissance engineering"
        icon: "explorer"
        color: "#9B59B6"
        steps:
          - "Take virtual museum tour"
          - "Try interactive demos"
          - "Read da Vinci stories"
          - "Explore timeline"
        cta:
          label: "Start Exploring"
          href: "explore/"

  - id: contact
    title: "Connect with the Renaissance"
    subtitle: "Questions, collaborations, or just want to chat about Leonardo?"
    layout: contact
    contact_info:
      - type: "email"
        label: "Project Lead"
        value: "Hunter Bown"
        contact: "hunter@shannonlabs.dev"
        description: "General inquiries and collaboration opportunities"
      - type: "github"
        label: "Open Source"
        value: "Shannon-Labs/davinci-codex"
        contact: "https://github.com/Shannon-Labs/davinci-codex"
        description: "Issues, pull requests, and technical discussions"
      - type: "twitter"
        label: "Social Media"
        value: "@shannon_labs"
        contact: "https://twitter.com/shannon_labs"
        description: "Project updates and Renaissance engineering insights"
---