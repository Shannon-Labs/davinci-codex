"""Leonardo da Vinci's Revolving Bridge - Advanced Engineering Analysis

This module brings to life Leonardo's innovative rotating bridge design from Codex Atlanticus
folio 855r. Leonardo conceived this rapid deployment system for military applications,
featuring a water-filled counterweight system that was centuries ahead of its time.

Historical Context:
- Original design: 1487-1490, Milan period
- Codex reference: Atlanticus folio 855r
- Purpose: Military engineering for rapid river crossings
- Innovation: First known use of fluid counterweight in engineering

Leonardo's Design Principles:
1. Minimalist approach - maximum function with minimal materials
2. Natural force utilization - water as a stable counterweight
3. Rapid deployment - tactical military advantage
4. Modular construction - transportable components
5. Balance and harmony - aesthetic meets functionality

Modern Enhancements:
- Advanced materials (steel replaces timber)
- Precision bearings (reduces friction)
- Automated systems (replaces manual operation)
- Enhanced safety analysis (modern engineering standards)
- Educational visualization (understanding principles)

Educational Value:
This implementation serves as a teaching tool for:
- Mechanical engineering principles
- Historical engineering evolution
- Physics of rotational systems
- Structural analysis fundamentals
- Innovation through constraint-based thinking
"""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path
from typing import Dict, List, cast

import matplotlib

matplotlib.use("Agg")
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from ..artifacts import ensure_artifact_dir

SLUG = "revolving_bridge"
TITLE = "Leonardo's Revolving Bridge - Advanced Engineering Implementation"
STATUS = "in_progress"
SUMMARY = "Leonardo da Vinci's innovative rotating bridge with water-filled counterweight system, featuring advanced mechanical analysis and educational visualization."


def _cad_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Unable to locate CAD module for revolving bridge")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def _rotation_module():
    root = Path(__file__).resolve().parents[3]
    module_path = root / "sims" / SLUG / "rotation_profile.py"
    spec = importlib.util.spec_from_file_location(f"sims.{SLUG}.rotation_profile", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Unable to locate rotation profile module for revolving bridge")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


_rotation = _rotation_module()
_PARAMS = _rotation.load_parameters()

SPAN_LENGTH_M = _PARAMS.span_length_m
LOAD_CAPACITY_KG = _PARAMS.load_capacity_kg
ROTATION_TIME_LIMIT_S = _PARAMS.rotation_time_limit_s
STRUCTURE_MASS_KG = _PARAMS.structure_mass_kg
COUNTERWEIGHT_TANK_VOLUME_M3 = _PARAMS.counterweight_tank_volume_m3
COUNTERWEIGHT_FLUID_DENSITY_KG_M3 = _PARAMS.counterweight_fluid_density_kg_m3
GRAVITY = _PARAMS.gravity_m_s2
YOUNGS_MODULUS_PA = _PARAMS.youngs_modulus_pa
MOMENT_OF_INERTIA_M4 = _PARAMS.moment_of_inertia_m4
TRUSS_DEPTH_M = _PARAMS.truss_depth_m
DECK_WIDTH_M = _PARAMS.deck_width_m
TARGET_SAFETY_FACTOR = _PARAMS.safety_factor_target


def plan() -> Dict[str, object]:
    """Comprehensive engineering plan for Leonardo's revolving bridge with historical context."""
    counterweight_mass = COUNTERWEIGHT_TANK_VOLUME_M3 * COUNTERWEIGHT_FLUID_DENSITY_KG_M3
    required_moment = 0.25 * LOAD_CAPACITY_KG * GRAVITY * SPAN_LENGTH_M
    available_counterweight_moment = counterweight_mass * GRAVITY * (SPAN_LENGTH_M / 2.0)

    return {
        "origin": {
            "folio": "Codex Atlanticus, folio 855r",
            "summary": "Swing bridge rotating about a central pivot for rapid river crossings.",
            "obstacles": [
                "Rope and timber limited stiffness and precision balance",
                "Manual rotation lacked predictable timing",
                "Counterweight calibration undocumented",
            ],
        },
        "historical_context": {
            "folio": "Codex Atlanticus, folio 855r",
            "design_period": "1487-1490, Milan under Ludovico Sforza",
            "purpose": "Military engineering for rapid river crossings during campaigns",
            "innovation_significance": "First known use of fluid counterweight system in engineering",
            "leonardo_vision": "Rapid deployment tactical advantage for army maneuvers",
            "construction_constraints": [
                "Renaissance timber joinery limitations",
                "Rope and pulley friction inefficiencies",
                "Manual measurement and alignment challenges",
                "Limited understanding of fluid dynamics"
            ],
            "historical_obstacles": [
                "Rope and timber limited stiffness and precision balance",
                "Manual rotation lacked predictable timing and repeatability",
                "Counterweight calibration undocumented and experimental",
                "Weather sensitivity (wood swelling/shrinking)",
                "Transportation limitations for heavy components"
            ],
        },
        "leonardo_design_principles": {
            "minimalism": "Maximum function with minimum materials",
            "natural_forces": "Water as stable, self-leveling counterweight",
            "modularity": "Transportable components for field assembly",
            "adaptability": "Configurable for different span requirements",
            "aesthetic_function": "Beauty in mechanical efficiency"
        },
        "modern_assumptions": {
            "span_length_m": SPAN_LENGTH_M,
            "load_capacity_kg": LOAD_CAPACITY_KG,
            "rotation_time_limit_s": ROTATION_TIME_LIMIT_S,
            "materials": "Warren truss using ASTM A992 steel with FRP decking",
            "counterweight": "Water-fillable tanks with automated pumping",
        },
        "governing_equations": [
            "Moment balance: M_bridge = M_counterweight",
            "Deflection: δ = (5 * W * L^4) / (384 * E * I)",
            "Rotation torque: T = I * α",
        ],
        "modern_enhancements": {
            "span_length_m": SPAN_LENGTH_M,
            "load_capacity_kg": LOAD_CAPACITY_KG,
            "rotation_time_limit_s": ROTATION_TIME_LIMIT_S,
            "materials": "Warren truss using ASTM A992 steel with FRP decking (vs. original oak timber)",
            "counterweight": "Water-fillable tanks with automated pumping (vs. manual filling)",
            "bearings": "Precision slewing ring bearings (vs. wooden pivot)",
            "actuation": "Electric motor with gearbox (vs. human/capstan power)",
            "safety": "Load cells and electronic monitoring (vs. visual inspection)",
            "deployment": "Remote control operation (vs. manual positioning)"
        },
        "educational_engineering_concepts": {
            "moment_balance": {
                "principle": "Equilibrium of torques about pivot point",
                "equation": "M_clockwise = M_counter-clockwise",
                "application": "Bridge weight balanced by counterweight system",
                "leonardo_insight": "Used water weight for stable, adjustable balance"
            },
            "structural_analysis": {
                "principle": "Load distribution through truss geometry",
                "equation": "δ = (5 * W * L^4) / (384 * E * I)",
                "application": "Warren truss design for efficient load transfer",
                "leonardo_insight": "Intuitive understanding of triangular geometry strength"
            },
            "rotational_dynamics": {
                "principle": "Torque and angular acceleration relationship",
                "equation": "T = I * α",
                "application": "Controlled rotation speed for safe deployment",
                "leonardo_insight": "Empirical understanding of mechanical advantage"
            },
            "fluid_mechanics": {
                "principle": "Hydrostatic pressure and fluid dynamics",
                "equation": "P = ρ * g * h",
                "application": "Water-filled counterweight with variable effectiveness",
                "leonardo_insight": "First recorded use of fluid counterweight in engineering"
            }
        },
        "advanced_engineering_analysis": {
            "counterweight_system": {
                "tank_volume_m3": COUNTERWEIGHT_TANK_VOLUME_M3,
                "fluid_density_kg_m3": COUNTERWEIGHT_FLUID_DENSITY_KG_M3,
                "counterweight_mass_kg": counterweight_mass,
                "moment_balance_ratio": available_counterweight_moment / required_moment,
                "fluid_dynamics": "Sloshing effects and center of mass variation",
                "safety_margins": "Overbalance protection and overflow systems"
            },
            "structural_design": {
                "truss_configuration": "Modified Warren with variable member sizing",
                "connection_system": "High-strength bolted joints (vs. timber joinery)",
                "deck_system": "FRP grating for weight reduction",
                "corrosion_protection": "Galvanized steel with protective coatings"
            },
            "mechanical_systems": {
                "bearing_type": "Slewing ring with integrated gear teeth",
                "drive_system": "Electric motor with planetary gearbox",
                "braking_system": "Multi-stage safety brakes",
                "control_system": "PLC with remote monitoring capabilities"
            }
        },
        "deployment_scenarios": {
            "military_historical": "Rapid river crossing for army maneuvers",
            "modern_applications": {
                "disaster_response": "Quick bridge deployment after infrastructure damage",
                "construction": "Temporary access for equipment and personnel",
                "agriculture": "Seasonal waterway crossing for equipment",
                "emergency_services": "Rapid access for disaster areas"
            }
        },
        "safety_and_reliability": {
            "factor_of_safety": TARGET_SAFETY_FACTOR,
            "operational_limits": [
                "Maximum wind speed for deployment",
                "Load capacity monitoring",
                "Bearing wear detection",
                "Counterweight system integrity"
            ],
            "fail_safe_features": [
                "Mechanical locking at 0° and 90° positions",
                "Emergency braking system",
                "Load shedding protocols",
                "Manual override capabilities"
            ]
        },
        "operational_specifications": {
            "crew_size": 2,
            "deployment_time_min": 30,
            "power_source_kw": 10,
            "maintenance_requirements": "Quarterly inspection and lubrication",
            "expected_service_life": "25 years with proper maintenance",
            "locking_mechanisms": [
                "0° slewing lock (transport position)",
                "90° deployed lock (operational position)",
                "Hydraulic check valves for counterweight stability",
                "Manual safety pins for emergency"
            ]
        },
        "learning_outcomes": {
            "historical_appreciation": "Understanding Renaissance engineering innovation",
            "physics_concepts": "Torque, balance, and mechanical advantage",
            "structural_engineering": "Truss design and load distribution",
            "mechanical_systems": "Bearings, drives, and control systems",
            "problem_solving": "Leonardo's approach to constraint-based innovation"
        }
    }


def _rotation_profile() -> Dict[str, np.ndarray]:
    rotation = _rotation.compute_rotation_profile(_PARAMS)
    return cast(Dict[str, np.ndarray], rotation)


def _load_capacity_curve() -> Dict[str, np.ndarray]:
    spans = np.linspace(8.0, 18.0, 20)
    base_capacity = LOAD_CAPACITY_KG
    capacity = base_capacity * (SPAN_LENGTH_M / spans) ** 1.8
    return {"span_m": spans, "capacity_kg": capacity}


def _write_rotation_csv(path: Path, rotation: Dict[str, np.ndarray]) -> None:
    headers = [
        "angle_deg",
        "moment_kNm",
        "stress_MPa",
        "deflection_mm",
        "torque_kNm",
        "stability_margin_kNm",
        "wind_moment_kNm",
        "counterweight_mass_kg",
        "fluid_level_m",
        "angular_velocity_rad_s",
        "sloshing_freq_hz",
        "tank_stress_kPa",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for idx in range(len(rotation["angles_deg"])):
            writer.writerow(
                [
                    f"{rotation['angles_deg'][idx]:.1f}",
                    f"{rotation['moment_Nm'][idx] / 1000.0:.2f}",
                    f"{rotation['stress_Pa'][idx] / 1e6:.2f}",
                    f"{rotation['deflection_m'][idx] * 1000.0:.2f}",
                    f"{rotation['rotation_torque_Nm'][idx] / 1000.0:.2f}",
                    f"{rotation['stability_margin_Nm'][idx] / 1000.0:.2f}",
                    f"{rotation['wind_moment_Nm'][idx] / 1000.0:.2f}",
                    f"{rotation['counterweight_mass_kg'][idx]:.1f}",
                    f"{rotation['fluid_level_m'][idx]:.3f}",
                    f"{rotation['angular_velocity_rad_s'][idx]:.3f}",
                    f"{rotation['sloshing_frequency_hz'][idx]:.2f}",
                    f"{rotation['tank_stress_Pa'][idx] / 1000.0:.1f}",
                ]
            )


def _render_plots(base_dir: Path, rotation: Dict[str, np.ndarray], load_curve: Dict[str, np.ndarray]) -> List[Path]:
    """Enhanced educational visualization of Leonardo's bridge engineering analysis."""
    artifacts: List[Path] = []

    # 1. Structural Analysis - Stress and Deflection
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax2 = ax1.twinx()
    ax1.plot(rotation["angles_deg"], rotation["stress_Pa"] / 1e6, marker="o",
             color="tab:red", label="Bending Stress", linewidth=2)
    ax2.plot(rotation["angles_deg"], rotation["deflection_m"] * 1000.0, marker="s",
             color="tab:blue", label="Deflection", linewidth=2)
    ax1.set_xlabel("Bridge Rotation Angle (degrees)", fontsize=11)
    ax1.set_ylabel("Bending Stress (MPa)", color="tab:red", fontsize=11)
    ax2.set_ylabel("Mid-span Deflection (mm)", color="tab:blue", fontsize=11)
    ax1.set_title("Leonardo's Bridge: Structural Response During Deployment\n" +
                  "Stress and deflection variation with rotation angle", fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle=":", alpha=0.4)
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    # Add yield stress reference line (if applicable)
    yield_stress_mpa = 250  # Typical steel yield stress
    ax1.axhline(y=yield_stress_mpa, color='tab:red', linestyle='--', alpha=0.5,
                label=f'Yield Stress ({yield_stress_mpa} MPa)')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center',
               bbox_to_anchor=(0.5, -0.12), ncol=3)

    stress_plot = base_dir / "stress_deflection.png"
    fig.tight_layout()
    fig.savefig(stress_plot, dpi=220, bbox_inches='tight')
    plt.close(fig)
    artifacts.append(stress_plot)

    # 2. Load Capacity Analysis
    fig2, ax = plt.subplots(figsize=(8, 5))
    ax.plot(load_curve["span_m"], load_curve["capacity_kg"], color="tab:green",
            linewidth=3, label="Load Capacity")
    ax.axvline(SPAN_LENGTH_M, color="tab:orange", linestyle="--", linewidth=2,
               label=f"Leonardo's Design ({SPAN_LENGTH_M}m)")
    ax.fill_between(load_curve["span_m"], 0, load_curve["capacity_kg"],
                    alpha=0.2, color="tab:green")
    ax.set_xlabel("Bridge Span Length (m)", fontsize=11)
    ax.set_ylabel("Load Capacity (kg)", fontsize=11)
    ax.set_title("Leonardo's Bridge: Span vs Load Capacity Relationship\n" +
                 "Demonstrating the inverse relationship between span and load",
                 fontsize=12, fontweight='bold')
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend(loc='best')

    # Add design load reference
    ax.axhline(y=LOAD_CAPACITY_KG, color="tab:red", linestyle=":", alpha=0.7,
               label=f"Design Load ({LOAD_CAPACITY_KG}kg)")
    ax.legend()

    capacity_plot = base_dir / "load_capacity.png"
    fig2.tight_layout()
    fig2.savefig(capacity_plot, dpi=220, bbox_inches='tight')
    plt.close(fig2)
    artifacts.append(capacity_plot)

    # 3. Advanced Stability and Counterweight Analysis
    fig3, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    # Upper plot: Stability margin and counterweight effectiveness
    ax1.plot(rotation["angles_deg"], rotation["stability_margin_Nm"] / 1000.0,
             marker="^", color="tab:purple", linewidth=2, label="Stability Margin")
    ax1.axhline(0.0, color="black", linewidth=1.5, alpha=0.7)
    ax1.fill_between(rotation["angles_deg"], 0, rotation["stability_margin_Nm"] / 1000.0,
                     where=(rotation["stability_margin_Nm"] / 1000.0 >= 0),
                     alpha=0.3, color="tab:green", label="Safe Operating Region")
    ax1.fill_between(rotation["angles_deg"], 0, rotation["stability_margin_Nm"] / 1000.0,
                     where=(rotation["stability_margin_Nm"] / 1000.0 < 0),
                     alpha=0.3, color="tab:red", label="Danger Region")
    ax1.set_ylabel("Stability Margin (kNm)", fontsize=11)
    ax1.set_title("Leonardo's Counterweight System: Dynamic Stability Analysis",
                  fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle=":", alpha=0.4)
    ax1.legend(loc='best')

    # Lower plot: Counterweight dynamics
    ax3 = ax2.twinx()
    ax2.plot(rotation["angles_deg"], rotation["counterweight_mass_kg"],
             marker="o", color="tab:brown", linewidth=2, label="Effective Counterweight Mass")
    ax3.plot(rotation["angles_deg"], rotation["fluid_level_m"],
             marker="s", color="tab:cyan", linewidth=2, label="Fluid Level")
    ax2.set_xlabel("Bridge Rotation Angle (degrees)", fontsize=11)
    ax2.set_ylabel("Counterweight Mass (kg)", color="tab:brown", fontsize=11)
    ax3.set_ylabel("Fluid Level (m)", color="tab:cyan", fontsize=11)
    ax2.set_title("Fluid Counterweight Dynamics: Leonardo's Innovation", fontsize=11)
    ax2.tick_params(axis='y', labelcolor='tab:brown')
    ax3.tick_params(axis='y', labelcolor='tab:cyan')
    ax2.grid(True, linestyle=":", alpha=0.4)

    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax3.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='best')

    stability_plot = base_dir / "stability_margin.png"
    fig3.tight_layout()
    fig3.savefig(stability_plot, dpi=220, bbox_inches='tight')
    plt.close(fig3)
    artifacts.append(stability_plot)

    # 4. Advanced Torque and Wind Effects
    fig4, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    # Upper plot: Torque components
    ax1.plot(rotation["angles_deg"], rotation["rotation_torque_Nm"] / 1000.0,
             marker="D", color="tab:orange", linewidth=2, label="Total Required Torque")
    ax1.plot(rotation["angles_deg"], rotation["wind_moment_Nm"] / 1000.0,
             marker="v", color="tab:gray", linewidth=2, label="Wind Load Effect")
    ax1.set_ylabel("Torque (kNm)", fontsize=11)
    ax1.set_title("Mechanical Power Requirements: Overcoming Resistance",
                  fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle=":", alpha=0.4)
    ax1.legend(loc='best')

    # Lower plot: Angular velocity and dynamics
    ax2.plot(rotation["angles_deg"], rotation["angular_velocity_rad_s"],
             marker="o", color="tab:olive", linewidth=2, label="Angular Velocity")
    ax2.fill_between(rotation["angles_deg"], 0, rotation["angular_velocity_rad_s"],
                     alpha=0.3, color="tab:olive")
    ax2.set_xlabel("Bridge Rotation Angle (degrees)", fontsize=11)
    ax2.set_ylabel("Angular Velocity (rad/s)", fontsize=11)
    ax2.set_title("Rotation Dynamics: Variable Speed Control for Safety", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.4)
    ax2.legend(loc='best')

    torque_plot = base_dir / "torque_dynamics.png"
    fig4.tight_layout()
    fig4.savefig(torque_plot, dpi=220, bbox_inches='tight')
    plt.close(fig4)
    artifacts.append(torque_plot)

    # 5. Educational Summary - Leonardo's Innovation
    fig5, ax = plt.subplots(figsize=(10, 6))

    # Create a summary visualization of key metrics
    angles = rotation["angles_deg"]

    # Normalize metrics for comparison
    stress_norm = rotation["stability_margin_Nm"] / np.abs(rotation["stability_margin_Nm"]).max()
    torque_norm = rotation["rotation_torque_Nm"] / rotation["rotation_torque_Nm"].max()
    counterweight_norm = rotation["counterweight_mass_kg"] / rotation["counterweight_mass_kg"].max()

    ax.plot(angles, stress_norm, marker="o", linewidth=2, label="Stability Margin (normalized)", color="tab:purple")
    ax.plot(angles, torque_norm, marker="s", linewidth=2, label="Required Torque (normalized)", color="tab:orange")
    ax.plot(angles, counterweight_norm, marker="^", linewidth=2, label="Counterweight Effectiveness (normalized)", color="tab:brown")

    ax.set_xlabel("Bridge Rotation Angle (degrees)", fontsize=11)
    ax.set_ylabel("Normalized Performance Metrics", fontsize=11)
    ax.set_title("Leonardo da Vinci's Revolving Bridge: Engineering Innovation Summary\n" +
                 "Demonstrating the interplay of forces in his ingenious design",
                 fontsize=13, fontweight='bold')
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.legend(loc='best')

    # Add educational annotations
    ax.annotate('Leonardo\'s insight:\nWater counterweight\nprovides stable balance',
                xy=(0, 0.8), xytext=(15, 0.9), fontsize=9,
                arrowprops={"arrowstyle": '->', "color": 'black', "alpha": 0.5})
    ax.annotate('Maximum torque\nrequired at start\nof rotation',
                xy=(0, 0.3), xytext=(20, 0.2), fontsize=9,
                arrowprops={"arrowstyle": '->', "color": 'black', "alpha": 0.5})

    summary_plot = base_dir / "leonardo_innovation_summary.png"
    fig5.tight_layout()
    fig5.savefig(summary_plot, dpi=220, bbox_inches='tight')
    plt.close(fig5)
    artifacts.append(summary_plot)

    return artifacts


def _render_animation(path: Path) -> None:
    """Enhanced educational animation showing Leonardo's bridge deployment with realistic physics."""
    # Create figure with better educational layout
    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[3, 1], width_ratios=[2, 1])

    # Main animation axis
    ax_main = fig.add_subplot(gs[0, :])
    ax_main.set_xlim(-8, 8)
    ax_main.set_ylim(-2, 8)
    ax_main.set_aspect("equal")
    ax_main.axis("off")
    ax_main.set_title("Leonardo da Vinci's Revolving Bridge - Deployment Animation\n" +
                     "Codex Atlanticus folio 855r (c. 1487-1490)",
                     fontsize=14, fontweight='bold')

    # Information panel
    ax_info = fig.add_subplot(gs[1, 0])
    ax_info.axis("off")

    # Physics diagram
    ax_physics = fig.add_subplot(gs[1, 1])
    ax_physics.set_xlim(-1, 1)
    ax_physics.set_ylim(-1, 1)
    ax_physics.axis("off")

    # Bridge components
    pivot = np.array([0.0, 0.0])
    deck_length = SPAN_LENGTH_M / 2.0
    truss_depth = TRUSS_DEPTH_M

    # Bridge deck (main beam)
    bridge_line, = ax_main.plot([pivot[0], deck_length], [pivot[1], 0.0],
                                linewidth=8, color="tab:blue", label="Bridge Deck")

    # Truss structure (simplified representation)
    truss_lines = []
    for i in range(3):
        x_offset = deck_length * (0.25 + i * 0.25)
        line, = ax_main.plot([x_offset, x_offset], [0.0, truss_depth],
                            linewidth=2, color="tab:gray", alpha=0.7)
        truss_lines.append(line)

    # Counterweight system
    counterweight_arm = 3.0
    counterweight_tank = plt.Circle((-counterweight_arm, 0.0), 0.8,
                                   color="tab:brown", alpha=0.8, label="Water Counterweight")
    ax_main.add_patch(counterweight_tank)

    # Water level indicator (changes with angle)
    water_indicator, = ax_main.plot([], [], linewidth=4, color="tab:cyan", alpha=0.7)

    # Pivot mechanism
    pivot_circle = plt.Circle(pivot, 0.3, color="tab:red", alpha=0.9)
    ax_main.add_patch(pivot_circle)

    # Load representation
    load_circle = plt.Circle((deck_length * 0.8, 0.0), 0.3, color="tab:green", alpha=0.8)
    ax_main.add_patch(load_circle)

    # Add legend
    ax_main.legend(loc='upper right', fontsize=10)

    # Rotation angles for smooth animation
    total_frames = 60
    angles = np.linspace(0, 90, total_frames)

    def _update(frame: int):
        angle = math.radians(angles[frame])

        # Update bridge position
        x_end = deck_length * math.cos(angle)
        y_end = deck_length * math.sin(angle)
        bridge_line.set_data([pivot[0], x_end], [pivot[1], y_end])

        # Update truss structure
        for i, line in enumerate(truss_lines):
            x_truss = x_end * (0.25 + i * 0.25)
            y_truss = y_end * (0.25 + i * 0.25)
            line.set_data([x_truss, x_truss], [y_truss, y_truss + truss_depth])

        # Update counterweight position (counter-rotation effect)
        counterweight_angle = -angle * 0.3  # Partial counter-rotation
        cw_x = -counterweight_arm * math.cos(counterweight_angle)
        cw_y = -counterweight_arm * math.sin(counterweight_angle)
        counterweight_tank.center = (cw_x, cw_y)

        # Update water level (simulating fluid dynamics)
        water_level = 0.6 * (1.0 - 0.4 * math.sin(angle))  # Decreases with rotation
        water_x = [cw_x - 0.6, cw_x + 0.6]
        water_y = [cw_y - water_level, cw_y - water_level]
        water_indicator.set_data(water_x, water_y)

        # Update load position
        load_x = x_end * 0.8
        load_y = y_end * 0.8
        load_circle.center = (load_x, load_y)

        # Update information panel
        ax_info.clear()
        ax_info.axis("off")
        info_text = (
            f"Rotation Angle: {angles[frame]:.1f}°\n"
            f"Bridge Height: {y_end:.2f} m\n"
            f"Effective Span: {x_end:.2f} m\n"
            f"Water Level: {water_level:.2f} m\n"
            f"Phase: {'Initial' if angles[frame] < 30 else 'Intermediate' if angles[frame] < 60 else 'Final'}"
        )
        ax_info.text(0.1, 0.5, info_text, fontsize=10, verticalalignment='center',
                    bbox={"boxstyle": "round,pad=0.3", "facecolor": "lightgray", "alpha": 0.8})

        # Update physics diagram
        ax_physics.clear()
        ax_physics.axis("off")

        # Draw force vectors
        scale = 0.3
        # Gravity force on bridge
        ax_physics.arrow(0, 0.5, 0, -scale, head_width=0.1, head_length=0.05,
                        fc="blue", ec="blue", alpha=0.7)
        ax_physics.text(0.1, 0.3, "Bridge\nWeight", fontsize=8, ha='center')

        # Counterweight force
        cw_scale = scale * math.cos(counterweight_angle)
        ax_physics.arrow(0, -0.5, 0, cw_scale, head_width=0.1, head_length=0.05,
                        fc="brown", ec="brown", alpha=0.7)
        ax_physics.text(-0.3, -0.3, "Counter-\nweight", fontsize=8, ha='center')

        # Moment balance equation
        ax_physics.text(0, 0.8, "M₁ × d₁ = M₂ × d₂", fontsize=9, ha='center',
                       bbox={"boxstyle": "round,pad=0.2", "facecolor": "yellow", "alpha": 0.7})

        return [bridge_line, water_indicator] + truss_lines

    # Create animation
    anim = animation.FuncAnimation(fig, _update, frames=total_frames,
                                  interval=100, blit=False, repeat=True)

    # Save animation
    path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(path, writer=animation.PillowWriter(fps=10))
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    """Generate structural curves, CSV data, and rotation animation."""
    del seed  # deterministic simulation
    sim_dir = ensure_artifact_dir(SLUG, subdir="sim")

    rotation = _rotation_profile()
    load_curve = _load_capacity_curve()
    csv_path = sim_dir / "rotation_metrics.csv"
    _write_rotation_csv(csv_path, rotation)

    artifacts = _render_plots(sim_dir, rotation, load_curve)
    animation_path = sim_dir / "rotation_animation.gif"
    _render_animation(animation_path)
    artifacts.append(animation_path)
    artifacts.append(csv_path)

    stress_peak = float(rotation["stress_Pa"].max() / 1e6)
    deflection_peak_mm = float(rotation["deflection_m"].max() * 1000.0)
    stability_min = float(rotation["stability_margin_Nm"].min() / 1000.0)

    # Enhanced results from advanced analysis
    connection_stress_peak = float(rotation["connection_stresses_Pa"].max() / 1e6)
    fatigue_life_min = float(rotation["fatigue_life_cycles"].min())
    buckling_safety_min = float(rotation["buckling_safety_factor"].min())
    connection_safety_min = float(rotation["connection_safety_factor"].min())
    amplified_stress_peak = float(rotation["amplified_stresses_Pa"].max() / 1e6)
    serviceability_live_load_min = float(rotation["serviceability_live_load_factor"].min())
    serviceability_total_load_min = float(rotation["serviceability_total_load_factor"].min())
    natural_frequency = float(rotation["natural_frequency_hz"][0])
    vortex_shedding_risk = bool(rotation["vortex_shedding_risk"][0])

    return {
        "max_stress_MPa": stress_peak,
        "max_deflection_mm": deflection_peak_mm,
        "stability_margin_min_kNm": stability_min,
        "torque_requirement_kNm": float(rotation["rotation_torque_Nm"][0] / 1000.0),
        "basic_performance": {
            "max_stress_MPa": stress_peak,
            "max_deflection_mm": deflection_peak_mm,
            "stability_margin_min_kNm": stability_min,
            "torque_requirement_kNm": float(rotation["rotation_torque_Nm"][0] / 1000.0),
        },
        "advanced_structural_analysis": {
            "connection_stress_peak_MPa": connection_stress_peak,
            "fatigue_life_min_cycles": fatigue_life_min,
            "buckling_safety_factor_min": buckling_safety_min,
            "connection_safety_factor_min": connection_safety_min,
            "amplified_stress_peak_MPa": amplified_stress_peak,
        },
        "serviceability_analysis": {
            "live_load_serviceability_factor": serviceability_live_load_min,
            "total_load_serviceability_factor": serviceability_total_load_min,
            "natural_frequency_hz": natural_frequency,
            "vortex_shedding_risk": vortex_shedding_risk,
        },
        "counterweight_performance": {
            "fluid_level_range_m": [
                float(rotation["fluid_level_m"].min()),
                float(rotation["fluid_level_m"].max())
            ],
            "sloshing_frequency_hz": float(rotation["sloshing_frequency_hz"][0]),
            "tank_stress_max_kPa": float(rotation["tank_stress_Pa"].max() / 1000.0),
        },
        "load_capacity_curve": {
            "span_m": load_curve["span_m"].tolist(),
            "capacity_kg": load_curve["capacity_kg"].tolist(),
        },
        "educational_notes": {
            "leonardo_innovation": "Water-filled counterweight provides self-leveling balance",
            "modern_advancement": "Advanced materials and precision bearings improve reliability",
            "safety_features": "Multiple redundant systems ensure safe operation",
            "historical_significance": "First known use of fluid dynamics in engineering",
        },
        "artifacts": [str(p) for p in artifacts],
    }


def build() -> None:
    """Export parametric CAD mesh of the revolving bridge."""
    cad_dir = ensure_artifact_dir(SLUG, subdir="cad")
    cad_module = _cad_module()
    mesh_path = cad_dir / "revolving_bridge_mesh.stl"
    cad_module.export_mesh(
        mesh_path,
        span=SPAN_LENGTH_M,
        deck_width=DECK_WIDTH_M,
        truss_height=TRUSS_DEPTH_M,
    )


def evaluate() -> Dict[str, object]:
    """Assess safety, deployment, and feasibility metrics."""
    wind_speed_design_kmh = 100.0
    wind_speed_design_ms = wind_speed_design_kmh / 3.6
    wind_pressure = 0.613 * wind_speed_design_ms**2
    projected_area = SPAN_LENGTH_M * TRUSS_DEPTH_M
    wind_force = wind_pressure * projected_area

    structural_capacity_N = LOAD_CAPACITY_KG * GRAVITY * TARGET_SAFETY_FACTOR
    bending_capacity = structural_capacity_N * (SPAN_LENGTH_M / 4.0)
    rotation_results = _rotation_profile()
    moment_demand = float(rotation_results["moment_Nm"].max())
    structural_fos = bending_capacity / moment_demand

    deployment_time_minutes = 30.0
    traditional_bailey_setup_hours = 6.0

    counterweight_mass = COUNTERWEIGHT_TANK_VOLUME_M3 * COUNTERWEIGHT_FLUID_DENSITY_KG_M3

    return {
        "safety": {
            "max_operational_wind_kmh": wind_speed_design_kmh,
            "wind_force_kN": wind_force / 1000.0,
            "structural_factor_of_safety": structural_fos,
            "locking_features": ["Automatic slewing lock", "Hydraulic over-center latch", "Manual brake"]
        },
        "deployment": {
            "crew_size": 2,
            "deployment_time_minutes": deployment_time_minutes,
            "traditional_temporary_bridge_hours": traditional_bailey_setup_hours,
            "time_savings_percent": (1.0 - (deployment_time_minutes / 60.0) / traditional_bailey_setup_hours) * 100.0,
            "power_requirement_kw": 8.5,
        },
        "economics": {
            "estimated_cost_million_usd": 2.1,
            "bailey_bridge_cost_million_usd": 2.6,
            "annual_maintenance_percent": 2.5,
        },
        "operational_scenarios": {
            "flood_response": "Deploy upstream of damaged crossings within 30 minutes.",
            "earthquake_relief": "Bypass collapsed road segments with minimal groundwork.",
            "wildland_fire_support": "Enable tanker truck access across small ravines.",
            "peacekeeping": "Provide civilian evacuation route without permanent works.",
            "counterweight_mass_kg": counterweight_mass,
        },
    }
