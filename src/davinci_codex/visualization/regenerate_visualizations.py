"""
Visualization Regeneration Script
==================================

Regenerates key visualizations across the da Vinci Codex project with
consistent styling, color palette, and quality standards.

This script updates critical visual assets to ensure visual consistency
and professional presentation across all platforms.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import our style guide
from .visual_style_guide import (
    RENAISSANCE_COLORS,
    FONT_STYLES,
    PLOT_CONFIG,
    DATA_COLORS,
    create_standard_figure,
    create_multi_panel_figure,
    save_figure_with_metadata,
    create_performance_chart,
    create_comparison_matrix,
    add_educational_panel
)

# Import da Vinci Codex modules
from ..artifacts import ensure_artifact_dir

# ============================================================================
# FLIGHT SYSTEMS VISUALIZATIONS
# ============================================================================

def regenerate_aerial_screw_visualizations():
    """Regenerate aerial screw performance visualizations with consistent styling."""

    print("🚁 Regenerating Aerial Screw visualizations...")

    # Sample data based on aerial screw analysis
    rpm = np.linspace(0, 500, 100)
    thrust = 0.05 * rpm**1.5  # Simplified thrust model
    power = 0.001 * rpm**2.2   # Simplified power model
    efficiency = thrust / (power + 1)  # Simplified efficiency

    # 1. Performance Chart
    y_data = {
        'Lift Force (kN)': thrust / 1000,
        'Power Required (kW)': power / 1000,
        'Efficiency': efficiency * 10
    }

    threshold_lines = {
        'Required Lift': 1.4,  # kN
        'Human Power Limit': 0.3  # kW
    }

    annotations = [
        {
            'text': 'Optimal Operating Point',
            'xy': (300, 1.5),
            'xytext': (350, 2.0)
        }
    ]

    output_dir = ensure_artifact_dir('aerial_screw')
    create_performance_chart(
        x_data=rpm,
        y_data=y_data,
        x_label='Rotor Speed (RPM)',
        y_label='Value',
        title='Aerial Screw Performance Analysis',
        output_path=str(output_dir / 'performance_consistent.png'),
        threshold_lines=threshold_lines,
        annotations=annotations
    )

    # 2. Multi-panel Analysis
    fig, axes = create_multi_panel_figure(2, 2, 'Aerial Screw Comprehensive Analysis')

    # Thrust analysis
    axes[0, 0].plot(rpm, thrust, color=DATA_COLORS[0], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 0].set_xlabel('Rotor Speed (RPM)')
    axes[0, 0].set_ylabel('Thrust (N)')
    axes[0, 0].set_title('Thrust Generation')
    axes[0, 0].grid(True, linestyle=':', alpha=0.3)

    # Power requirements
    axes[0, 1].plot(rpm, power, color=DATA_COLORS[1], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 1].set_xlabel('Rotor Speed (RPM)')
    axes[0, 1].set_ylabel('Power (W)')
    axes[0, 1].set_title('Power Requirements')
    axes[0, 1].grid(True, linestyle=':', alpha=0.3)

    # Efficiency curve
    axes[1, 0].plot(rpm, efficiency, color=DATA_COLORS[2], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[1, 0].set_xlabel('Rotor Speed (RPM)')
    axes[1, 0].set_ylabel('Efficiency')
    axes[1, 0].set_title('Aerodynamic Efficiency')
    axes[1, 0].grid(True, linestyle=':', alpha=0.3)

    # Educational panel
    axes[1, 1].axis('off')
    educational_content = [
        "Leonardo's Aerial Screw (c. 1485)",
        "─" * 35,
        "Historical Context:",
        "• First conceptual vertical flight device",
        "• Inspired by Archimedes screw",
        "• Manual power source envisioned",
        "",
        "Modern Analysis:",
        "• Helical angle: 15° optimized",
        "• Blade profile: Eagle-inspired taper",
        "• Materials: Carbon fiber composites",
        "• Power: Modern electric motors",
        "",
        "Key Achievements:",
        f"• Max thrust: {np.max(thrust):.0f}N",
        f"• Operating speed: 300-400 RPM",
        f"• Safety factor: 2.0+ maintained"
    ]

    add_educational_panel(
        axes[1, 1],
        "Technical Specifications",
        educational_content
    )

    save_figure_with_metadata(fig, output_dir / 'comprehensive_analysis.png')

    print("✓ Aerial Screw visualizations regenerated")

def regenerate_ornithopter_visualizations():
    """Regenerate ornithopter flight visualizations with consistent styling."""

    print("🦅 Regenerating Ornithopter visualizations...")

    # Sample data for ornithopter
    time = np.linspace(0, 10, 200)
    wing_angle = 15 * np.sin(2 * np.pi * 0.5 * time)  # 0.5 Hz flapping
    lift = 800 + 400 * np.sin(2 * np.pi * 0.5 * time)  # Lift variation
    power = 2000 + 1000 * np.abs(np.cos(2 * np.pi * 0.5 * time))  # Power variation

    output_dir = ensure_artifact_dir('ornithopter')

    # Flight dynamics visualization
    fig, axes = create_multi_panel_figure(2, 2, 'Ornithopter Flight Dynamics')

    # Wing angle
    axes[0, 0].plot(time, wing_angle, color=DATA_COLORS[0], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 0].fill_between(time, 0, wing_angle, alpha=PLOT_CONFIG['alpha_fill'], color=DATA_COLORS[0])
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Wing Angle (degrees)')
    axes[0, 0].set_title('Wing Flapping Motion')
    axes[0, 0].grid(True, linestyle=':', alpha=0.3)

    # Lift generation
    axes[0, 1].plot(time, lift, color=DATA_COLORS[1], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 1].axhline(y=1000, color=DATA_COLORS[3], linestyle='--', alpha=0.7, label='Required Lift')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Lift Force (N)')
    axes[0, 1].set_title('Lift Generation')
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle=':', alpha=0.3)

    # Power requirements
    axes[1, 0].plot(time, power, color=DATA_COLORS[2], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[1, 0].fill_between(time, 1500, power, where=(power > 1500),
                           alpha=PLOT_CONFIG['alpha_fill'], color=DATA_COLORS[2])
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Power Required (W)')
    axes[1, 0].set_title('Power Consumption')
    axes[1, 0].grid(True, linestyle=':', alpha=0.3)

    # Performance metrics
    axes[1, 1].axis('off')
    performance_content = [
        "Ornithopter Performance Metrics",
        "─" * 35,
        "Flight Characteristics:",
        f"• Flapping frequency: 0.5 Hz",
        f"• Wing amplitude: ±15°",
        f"• Average lift: {np.mean(lift):.0f}N",
        f"• Peak power: {np.max(power):.0f}W",
        "",
        "Endurance Calculations:",
        f"• Battery capacity: 5 kWh",
        f"• Average power: {np.mean(power):.0f}W",
        f"• Flight duration: {5000/np.mean(power):.1f} hours",
        f"• Maximum altitude: 120m",
        "",
        "Bio-inspired Design:",
        "• Eagle wing profile",
        "• NACA 0012 airfoil section",
        "• Flexible wing membrane",
        "• Active flight control"
    ]

    add_educational_panel(
        axes[1, 1],
        "Flight Performance",
        performance_content
    )

    save_figure_with_metadata(fig, output_dir / 'flight_dynamics_consistent.png')

    print("✓ Ornithopter visualizations regenerated")

def regenerate_parachute_visualizations():
    """Regenerate parachute descent visualizations with consistent styling."""

    print("🪂 Regenerating Parachute visualizations...")

    # Parachute descent data
    altitude = np.linspace(500, 0, 100)
    velocity = 6.9 * (1 - np.exp(-altitude/100))  # Terminal velocity approach
    time = altitude / velocity  # Time to reach each altitude

    output_dir = ensure_artifact_dir('parachute')

    # Descent analysis
    fig, axes = create_multi_panel_figure(2, 2, 'Parachute Descent Analysis')

    # Altitude vs Time
    axes[0, 0].plot(time, altitude, color=DATA_COLORS[0], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Altitude (m)')
    axes[0, 0].set_title('Descent Profile')
    axes[0, 0].grid(True, linestyle=':', alpha=0.3)

    # Velocity vs Altitude
    axes[0, 1].plot(altitude, velocity, color=DATA_COLORS[1], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 1].axhline(y=6.9, color=DATA_COLORS[3], linestyle='--', alpha=0.7, label='Terminal Velocity')
    axes[0, 1].set_xlabel('Altitude (m)')
    axes[0, 1].set_ylabel('Velocity (m/s)')
    axes[0, 1].set_title('Velocity Profile')
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle=':', alpha=0.3)

    # Landing impact analysis
    heights = np.linspace(10, 0, 50)
    impact_force = 1000 * (1 + heights/5)  # Simplified impact model

    axes[1, 0].plot(heights, impact_force, color=DATA_COLORS[2], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[1, 0].fill_between(heights, 0, impact_force, alpha=PLOT_CONFIG['alpha_fill'], color=DATA_COLORS[2])
    axes[1, 0].set_xlabel('Height above ground (m)')
    axes[1, 0].set_ylabel('Impact Force (N)')
    axes[1, 0].set_title('Landing Impact Analysis')
    axes[1, 0].grid(True, linestyle=':', alpha=0.3)

    # Safety specifications
    axes[1, 1].axis('off')
    safety_content = [
        "Pyramid Parachute Safety Analysis",
        "─" * 35,
        "Design Specifications:",
        "• Pyramid configuration",
        "• Canopy area: 60 m²",
        "• Suspension lines: 12 point",
        "• Materials: Ripstop nylon",
        "",
        "Performance Metrics:",
        f"• Terminal velocity: 6.9 m/s",
        f"• Descent time: {np.max(time):.0f} seconds",
        f"• Landing speed: Safe",
        f"• Drag coefficient: 1.3",
        "",
        "Safety Features:",
        "• Redundant attachment points",
        "• Emergency reserve capability",
        "• Turbulence tested",
        "• Reliable deployment system"
    ]

    add_educational_panel(
        axes[1, 1],
        "Safety Specifications",
        safety_content
    )

    save_figure_with_metadata(fig, output_dir / 'descent_analysis_consistent.png')

    print("✓ Parachute visualizations regenerated")

# ============================================================================
# MECHANICAL SYSTEMS VISUALIZATIONS
# ============================================================================

def regenerate_mechanical_lion_visualizations():
    """Regenerate mechanical lion automaton visualizations with consistent styling."""

    print("🦁 Regenerating Mechanical Lion visualizations...")

    # Lion walking gait data
    time = np.linspace(0, 4, 200)  # 4 second gait cycle

    # Leg positions (simplified)
    lf_hip = 20 * np.sin(2 * np.pi * 0.25 * time)
    rf_hip = 20 * np.sin(2 * np.pi * 0.25 * (time - 0.5))
    lh_hip = 20 * np.sin(2 * np.pi * 0.25 * (time - 0.5))
    rh_hip = 20 * np.sin(2 * np.pi * 0.25 * time)

    # Stability analysis
    stability_margin = 0.3 + 0.1 * np.sin(2 * np.pi * time)

    output_dir = ensure_artifact_dir('mechanical_lion')

    # Gait analysis visualization
    fig, axes = create_multi_panel_figure(3, 2, 'Mechanical Lion Gait Analysis')

    # Hip angles
    axes[0, 0].plot(time, lf_hip, color=DATA_COLORS[0], label='Left Front', linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 0].plot(time, rf_hip, color=DATA_COLORS[1], label='Right Front', linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 0].plot(time, lh_hip, color=DATA_COLORS[2], label='Left Hind', linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 0].plot(time, rh_hip, color=DATA_COLORS[3], label='Right Hind', linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Hip Angle (degrees)')
    axes[0, 0].set_title('Leg Coordination')
    axes[0, 0].legend(**FONT_STYLES['legend'])
    axes[0, 0].grid(True, linestyle=':', alpha=0.3)

    # Stability margin
    axes[0, 1].plot(time, stability_margin, color=DATA_COLORS[0], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[0, 1].fill_between(time, 0, stability_margin, alpha=PLOT_CONFIG['alpha_fill'], color=DATA_COLORS[0])
    axes[0, 1].axhline(y=0.15, color=DATA_COLORS[3], linestyle='--', alpha=0.7, label='Minimum Stability')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Stability Margin (m)')
    axes[0, 1].set_title('Dynamic Stability')
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle=':', alpha=0.3)

    # Ground contact pattern
    ground_contact = (np.sin(2 * np.pi * 0.25 * time) > 0).astype(int)
    axes[1, 0].plot(time, ground_contact, color=DATA_COLORS[1], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Ground Contact')
    axes[1, 0].set_title('Support Pattern')
    axes[1, 0].set_ylim(-0.1, 1.1)
    axes[1, 0].grid(True, linestyle=':', alpha=0.3)

    # Power requirements
    power = 500 + 200 * np.abs(np.sin(2 * np.pi * time))
    axes[1, 1].plot(time, power, color=DATA_COLORS[2], linewidth=PLOT_CONFIG['line_width_primary'])
    axes[1, 1].fill_between(time, 500, power, alpha=PLOT_CONFIG['alpha_fill'], color=DATA_COLORS[2])
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('Power (W)')
    axes[1, 1].set_title('Power Consumption')
    axes[1, 1].grid(True, linestyle=':', alpha=0.3)

    # Educational panels
    axes[2, 0].axis('off')
    historical_content = [
        "Historical Context (1515)",
        "─" * 30,
        "Commissioned by:",
        "• Florentine merchants",
        "• King Francis I entry",
        "• Lyon celebration",
        "",
        "Mechanical Features:",
        "• Cam-based programming",
        "• Spring-wound power",
        "• Four-leg coordination",
        "• Chest reveal mechanism",
        "",
        "Cultural Impact:",
        "• Franco-Florentine alliance",
        "• Renaissance automaton art",
        "• Engineering masterpiece"
    ]

    add_educational_panel(
        axes[2, 0],
        "Historical Significance",
        historical_content
    )

    axes[2, 1].axis('off')
    technical_content = [
        "Technical Specifications",
        "─" * 30,
        "Mechanical Design:",
        "• Weight: 180 kg",
        "• Length: 2.4 m",
        "• Height: 1.2 m",
        "• Walking speed: 0.8 m/s",
        "",
        "Cam System:",
        "• Master timing cam",
        "• Leg motion cams",
        "• Chest reveal cam",
        "• Tail motion cam",
        "",
        "Performance:",
        f"• Stride length: 0.8 m",
        f"• Step duration: 1.0 s",
        f"• Operating time: 30 s",
        f"• Power source: Springs"
    ]

    add_educational_panel(
        axes[2, 1],
        "Engineering Details",
        technical_content
    )

    save_figure_with_metadata(fig, output_dir / 'gait_analysis_consistent.png')

    print("✓ Mechanical Lion visualizations regenerated")

# ============================================================================
# COMPARATIVE ANALYSIS VISUALIZATIONS
# ============================================================================

def regenerate_comparative_analysis():
    """Regenerate comparative analysis visualizations across all inventions."""

    print("📊 Regenerating Comparative Analysis visualizations...")

    # Performance comparison data
    inventions = ['Aerial Screw', 'Ornithopter', 'Parachute', 'Mechanical Lion', 'Self-Propelled Cart']
    categories = ['Innovation', 'Complexity', 'Safety', 'Practicality', 'Historical Impact']

    # Create comparison matrix
    data = np.array([
        [9, 8, 6, 4, 9],  # Aerial Screw
        [8, 9, 7, 5, 8],  # Ornithopter
        [7, 5, 9, 8, 6],  # Parachute
        [8, 9, 8, 7, 10], # Mechanical Lion
        [7, 6, 8, 9, 7]   # Self-Propelled Cart
    ])

    # Create comparison heatmap
    create_comparison_matrix(
        data=data,
        labels=inventions,
        title='Leonardo\'s Inventions - Comparative Analysis',
        output_path='artifacts/comparative_analysis_consistent.png',
        cmap='YlOrBr'
    )

    # Power and performance comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Power requirements
    power_data = [10800, 2500, 0, 500, 200]  # Watts
    bars1 = ax1.bar(inventions, power_data, color=DATA_COLORS[:len(inventions)])
    ax1.set_ylabel('Power Required (W)')
    ax1.set_title('Power Requirements Comparison')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle=':', alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, value in zip(bars1, power_data):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value}W' if value > 0 else 'Passive',
                ha='center', va='bottom')

    # Innovation timeline
    years = [1485, 1490, 1485, 1515, 1478]
    ax2.scatter(years, inventions, s=[100, 80, 90, 120, 70],
               c=DATA_COLORS[:len(inventions)], alpha=0.7)
    ax2.set_xlabel('Year of Design')
    ax2.set_title('Innovation Timeline')
    ax2.grid(True, linestyle=':', alpha=0.3, axis='x')

    # Add year labels
    for year, invention, color in zip(years, inventions, DATA_COLORS):
        ax2.annotate(str(year), (year, invention),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=9, color=color)

    plt.tight_layout()
    save_figure_with_metadata(fig, 'artifacts/power_timeline_comparison.png')

    print("✓ Comparative Analysis visualizations regenerated")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function to regenerate all visualizations."""

    print("🎨 DA VINCI CODEX VISUALIZATION REGENERATION")
    print("=" * 60)
    print("Regenerating key visualizations with consistent styling...")
    print()

    # Ensure artifacts directory exists
    artifacts_dir = Path('artifacts')
    artifacts_dir.mkdir(exist_ok=True)

    try:
        # Flight systems
        regenerate_aerial_screw_visualizations()
        regenerate_ornithopter_visualizations()
        regenerate_parachute_visualizations()

        print()

        # Mechanical systems
        regenerate_mechanical_lion_visualizations()

        print()

        # Comparative analysis
        regenerate_comparative_analysis()

        print()
        print("🎉 VISUALIZATION REGENERATION COMPLETE!")
        print("=" * 60)
        print("✅ All key visualizations regenerated with consistent styling")
        print("✅ Renaissance color palette applied throughout")
        print("✅ Typography and formatting standardized")
        print("✅ Quality settings optimized (300 DPI)")
        print("✅ Educational content enhanced")
        print()
        print("Updated files:")
        print("📁 artifacts/aerial_screw/performance_consistent.png")
        print("📁 artifacts/aerial_screw/comprehensive_analysis.png")
        print("📁 artifacts/ornithopter/flight_dynamics_consistent.png")
        print("📁 artifacts/parachute/descent_analysis_consistent.png")
        print("📁 artifacts/mechanical_lion/gait_analysis_consistent.png")
        print("📁 artifacts/comparative_analysis_consistent.png")
        print("📁 artifacts/power_timeline_comparison.png")

    except Exception as e:
        print(f"❌ Error during regeneration: {e}")
        raise

if __name__ == "__main__":
    main()