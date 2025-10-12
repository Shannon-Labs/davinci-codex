#!/usr/bin/env python3
"""
Demonstration of Leonardo's Mechanical Lion Walking Mechanism

This script showcases the complete functionality of Leonardo's Mechanical Lion
design, including biomechanical analysis, gait simulation, and performance
evaluation. It demonstrates how Leonardo's innovative cam-based system created
natural walking motion and the spectacular chest reveal mechanism.

Historical Context:
- Built 1515 for King Francis I's entry into Lyon
- First complex walking automaton in history
- Celebrated Franco-Florentine alliance
- Demonstrated Leonardo's mastery of biomechanics and automation
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from davinci_codex.inventions.mechanical_lion import (
    LION_HEIGHT,
    LION_LENGTH,
    LION_WALKING_SPEED,
    LION_WEIGHT,
    STEP_DURATION,
    CamProfileDesigner,
    ChestMechanism,
    LegKinematics,
    StabilityAnalysis,
    evaluate,
    simulate,
)


def demonstrate_leg_kinematics():
    """Demonstrate individual leg movement and kinematics."""
    print("=" * 60)
    print("LEONARDO'S MECHANICAL LION - LEG KINEMATICS DEMONSTRATION")
    print("=" * 60)
    print()

    # Create all four legs
    legs = {
        'LF': LegKinematics('LF', True, True),   # Left Front
        'RF': LegKinematics('RF', True, False),  # Right Front
        'LH': LegKinematics('LH', False, True),  # Left Hind
        'RH': LegKinematics('RH', False, False)  # Right Hind
    }

    print("Lion Configuration:")
    print(f"  Body Length: {LION_LENGTH:.1f} m")
    print(f"  Body Height: {LION_HEIGHT:.1f} m")
    print(f"  Total Weight: {LION_WEIGHT:.0f} kg")
    print(f"  Walking Speed: {LION_WALKING_SPEED:.1f} m/s")
    print(f"  Step Duration: {STEP_DURATION:.1f} s")
    print()

    print("Leg Phase Offsets (Gait Coordination):")
    for leg_name, leg in legs.items():
        print(f"  {leg_name}: Phase offset = {leg.phase_offset:.2f}π radians")
    print()

    # Analyze one complete gait cycle
    print("Gait Analysis - One Complete Step:")
    print("-" * 40)

    time_points = np.linspace(0, STEP_DURATION, 9)

    for t in time_points:
        print(f"\nTime: {t:.2f}s")
        print("-" * 20)

        ground_contacts = []
        for leg_name, leg in legs.items():
            hip_angle, knee_angle, ground_contact = leg.calculate_joint_angles(t)
            foot_x, foot_y, foot_z = leg.calculate_foot_position(hip_angle, knee_angle)

            status = "GROUND" if ground_contact else "SWING"
            print(f"  {leg_name}: Hip={np.degrees(hip_angle):5.1f}°, "
                  f"Knee={np.degrees(knee_angle):5.1f}°, "
                  f"Status={status}, "
                  f"Foot_z={foot_z:.3f}m")

            if ground_contact:
                ground_contacts.append(leg_name)

        print(f"  Stability: {len(ground_contacts)} legs on ground ({', '.join(ground_contacts)})")

    return legs


def demonstrate_stability_analysis(legs):
    """Demonstrate stability analysis throughout the gait cycle."""
    print("\n" + "=" * 60)
    print("DYNAMIC STABILITY ANALYSIS")
    print("=" * 60)
    print()

    # Create stability analyzer
    stability_analyzer = StabilityAnalysis(LION_LENGTH, 0.4, LION_WEIGHT)

    print("Stability Assessment Throughout Gait Cycle:")
    print("-" * 50)

    # Test stability at multiple points
    test_times = np.linspace(0, STEP_DURATION * 2, 13)
    stability_summary = []

    for t in test_times:
        stability_result = stability_analyzer.check_stability(t)
        com_x, com_y = stability_analyzer.calculate_center_of_mass(t)
        support_polygon = stability_analyzer.calculate_support_polygon(t)

        support_points = stability_result.get('support_points', len(support_polygon))
        stability_summary.append({
            'time': t,
            'is_stable': stability_result['is_stable'],
            'stability_margin': stability_result['stability_margin'],
            'support_points': support_points,
            'com_x': com_x,
            'com_y': com_y
        })

        status = "STABLE" if stability_result['is_stable'] else "UNSTABLE"
        print(f"t={t:4.2f}s: {status:8s} | "
              f"Margin={stability_result['stability_margin']:6.3f}m | "
              f"Support={stability_result['support_points']:1d} points | "
              f"COM=({com_x:5.2f}, {com_y:5.2f})")

    # Calculate stability statistics
    stable_times = sum(1 for s in stability_summary if s['is_stable'])
    total_times = len(stability_summary)
    stability_percentage = 100.0 * stable_times / total_times

    print("\nStability Summary:")
    print(f"  Stable periods: {stable_times}/{total_times} ({stability_percentage:.1f}%)")
    print(f"  Average stability margin: {np.mean([s['stability_margin'] for s in stability_summary]):.3f} m")
    print(f"  Minimum stability margin: {min([s['stability_margin'] for s in stability_summary]):.3f} m")

    return stability_analyzer


def demonstrate_cam_profiles(legs):
    """Demonstrate cam profile generation for natural gait."""
    print("\n" + "=" * 60)
    print("CAM PROFILE DESIGN - NATURAL GAIT GENERATION")
    print("=" * 60)
    print()

    cam_designer = CamProfileDesigner()

    print("Leonardo's Cam Drum System:")
    print(f"  Cam drum radius: {cam_designer.cam_radius:.3f} m")
    print(f"  Number of cam types: {len(cam_designer.cam_types)}")
    print("  Profile resolution: 360 points (1° increments)")
    print()

    # Generate cam profiles for one leg
    test_leg = legs['LF']
    print(f"Cam Profiles for {test_leg.leg_id} Leg:")
    print("-" * 40)

    for cam_type in cam_designer.cam_types:
        profile = cam_designer.generate_leg_cam_profile(test_leg, cam_type)
        print(f"  {cam_type.capitalize()} cam:")
        print(f"    Range: {profile.min():.4f} - {profile.max():.4f} m")
        print(f"    Mean: {profile.mean():.4f} m")
        print(f"    Variation: {profile.std():.4f} m")

    print("\nCam Profile Characteristics:")
    print("  - Lift cam: Controls vertical leg movement")
    print("  - Extend cam: Controls leg extension/flexion")
    print("  - Swing cam: Controls forward/backward motion")
    print("  - Smooth profiles ensure natural, lifelike movement")


def demonstrate_chest_mechanism():
    """Demonstrate the chest cavity reveal mechanism."""
    print("\n" + "=" * 60)
    print("CHEST CAVITY REVEAL MECHANISM")
    print("=" * 60)
    print()

    chest = ChestMechanism()

    print("Chest Configuration:")
    print(f"  Number of panels: {len(chest.panels)}")
    print(f"  Lily count: {chest.lily_platform.lily_count}")
    print(f"  Current state: {chest.current_phase}")
    print(f"  Is locked: {chest.is_locked}")
    print()

    print("Panel Specifications:")
    for i, panel in enumerate(chest.panels):
        print(f"  Panel {i}: {panel.width_m:.2f}m × {panel.height_m:.2f}m × "
              f"{panel.mass_kg:.1f}kg")
        print(f"    Opening angle: {np.degrees(panel.opening_angle_rad):.1f}°")
        print(f"    Current angle: {np.degrees(panel.current_angle_rad):.1f}°")

    print("\nReveal Sequence Timing:")
    print("  Post-walk pause: 2.5 seconds")
    print("  Chest opening: 3.5 seconds")
    print("  Lily elevation: 2.0 seconds")
    print("  Display duration: 8.0 seconds")
    print("  Reset sequence: 10.0 seconds")
    print("  Total performance: 26.0 seconds")

    # Simulate opening sequence
    print("\nSimulating Chest Opening Sequence:")
    print("-" * 40)

    dt = 0.5
    for step in range(8):
        chest.update_mechanism(dt, "opening")
        aperture = chest.get_chest_aperture()
        elevation = chest.lily_platform.current_elevation_m

        print(f"  Step {step + 1}: Aperture = {aperture:.1%}, "
              f"Lily elevation = {elevation:.3f}m")

        if chest.current_phase == "display":
            break


def demonstrate_complete_simulation():
    """Run the complete simulation and analysis."""
    print("\n" + "=" * 60)
    print("COMPLETE SIMULATION AND PERFORMANCE ANALYSIS")
    print("=" * 60)
    print()

    print("Running comprehensive simulation...")
    sim_result = simulate()

    print("✓ Simulation completed successfully!")
    print(f"  Generated {len(sim_result['artifacts'])} analysis artifacts")
    print()

    # Display key results
    biomech = sim_result['biomechanical_analysis']
    mechanical = sim_result['mechanical_design']
    historical = sim_result['historical_analysis']

    print("Biomechanical Performance:")
    print(f"  Walking speed: {biomech['walking_performance']['walking_speed_m_s']:.1f} m/s")
    print(f"  Stride length: {biomech['walking_performance']['stride_length_m']:.1f} m")
    print(f"  Ground clearance: {biomech['walking_performance']['ground_clearance_m']:.2f} m")
    print(f"  Stability percentage: {biomech['gait_stability']['stability_percentage']:.1f}%")
    print(f"  Minimum stability margin: {biomech['gait_stability']['minimum_stability_margin_m']:.3f} m")
    print()

    print("Mechanical Design:")
    print(f"  Cam drum radius: {mechanical['cam_system']['cam_drum_radius_m']:.3f} m")
    print(f"  Number of cam tracks: {mechanical['cam_system']['number_of_cam_tracks']}")
    print(f"  Four-bar linkages: {mechanical['linkage_system']['four_bar_linkages']}")
    print(f"  Mechanical advantage: {mechanical['linkage_system']['mechanical_advantage']:.1f}×")
    print(f"  Overall structural integrity: {mechanical['structural_analysis']['overall_structural_integrity']:.1f}× safety factor")
    print()

    print("Historical Analysis:")
    print(f"  Construction time: {historical['leonardos_workshop']['construction_time_months']} months")
    print(f"  Team size: {historical['leonardos_workshop']['team_size']} people")
    print(f"  Walking distance: {historical['ceremonial_performance']['walking_distance_m']:.1f} m")
    print(f"  Performance duration: {historical['ceremonial_performance']['performance_duration_s']:.0f} seconds")
    print(f"  Audience: {historical['ceremonial_performance']['audience']}")

    return sim_result


def demonstrate_evaluation(sim_result):
    """Demonstrate comprehensive evaluation and assessment."""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE EVALUATION AND ASSESSMENT")
    print("=" * 60)
    print()

    print("Running evaluation...")
    eval_result = evaluate()

    print("✓ Evaluation completed successfully!")
    print()

    # Display key evaluation results
    practical = eval_result['practicality']
    educational = eval_result['educational_value']

    print("Practical Assessment:")
    print(f"  Mechanical feasibility: {practical['mechanical_feasibility']['walking_mechanism']}")
    print(f"  Walking speed: {practical['performance_assessment']['walking_speed_m_s']:.1f} m/s")
    print(f"  Reliability rating: {practical['performance_assessment']['reliability_rating']:.0f}%")
    print(f"  Court impression: {practical['ceremonial_effectiveness']['royal_court_impression']}")
    print()

    print("Educational Value:")
    print("  STEM Learning Areas:")
    for area in educational['stem_learning']:
        print(f"    • {area}")
    print()
    print("  Historical Connections:")
    for connection in educational['historical_connections']:
        print(f"    • {connection}")
    print()

    print("Validation Results:")
    validation = eval_result['validation']
    for key, value in validation.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")


def create_visualization():
    """Create visualizations of the walking mechanism."""
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATIONS")
    print("=" * 60)
    print()

    # Create a simple gait diagram
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Create legs and analyze gait
    legs = {
        'LF': LegKinematics('LF', True, True),
        'RF': LegKinematics('RF', True, False),
        'LH': LegKinematics('LH', False, True),
        'RH': LegKinematics('RH', False, False)
    }

    # Time array for two complete steps
    time = np.linspace(0, STEP_DURATION * 2, 100)
    colors = {'LF': 'blue', 'RF': 'red', 'LH': 'green', 'RH': 'orange'}

    # Plot 1: Ground contact pattern
    ax1.set_title('Ground Contact Pattern - Leonardo\'s Lateral Sequence Gait', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Ground Contact')
    ax1.set_ylim([-0.1, 1.1])
    ax1.grid(True, alpha=0.3)

    for leg_name, leg in legs.items():
        ground_contact = []
        for t in time:
            _, _, contact = leg.calculate_joint_angles(t)
            ground_contact.append(1 if contact else 0)

        ax1.fill_between(time, ground_contact, alpha=0.3, color=colors[leg_name], label=leg_name)
        ax1.plot(time, ground_contact, color=colors[leg_name], linewidth=2)

    ax1.legend(loc='upper right')
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['Swing', 'Stance'])

    # Plot 2: Hip joint angles
    ax2.set_title('Hip Joint Angles Throughout Gait Cycle', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Hip Angle (degrees)')
    ax2.grid(True, alpha=0.3)

    for leg_name, leg in legs.items():
        hip_angles = []
        for t in time:
            hip_angle, _, _ = leg.calculate_joint_angles(t)
            hip_angles.append(np.degrees(hip_angle))

        ax2.plot(time, hip_angles, color=colors[leg_name], linewidth=2, label=leg_name)

    ax2.legend(loc='upper right')
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax2.axhline(y=45, color='gray', linestyle='--', alpha=0.5)
    ax2.axhline(y=-45, color='gray', linestyle='--', alpha=0.5)

    plt.tight_layout()

    # Save the plot
    output_dir = Path("artifacts/mechanical_lion")
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_path = output_dir / "gait_visualization.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Gait visualization saved to: {plot_path}")
    print()
    print("Visualization Features:")
    print("  • Ground contact pattern showing lateral sequence gait")
    print("  • Hip joint angles demonstrating natural leg movement")
    print("  • Proper phase relationships between legs")
    print("  • Clear swing and stance phase identification")


def main():
    """Main demonstration function."""
    print("LEONARDO DA VINCI'S MECHANICAL LION - COMPREHENSIVE DEMONSTRATION")
    print("=" * 80)
    print()
    print("This demonstration showcases Leonardo's groundbreaking 1515 Mechanical Lion,")
    print("the first complex walking automaton in history. The lion walked gracefully before")
    print("King Francis I's court, then opened its chest to reveal fleurs-de-lis, celebrating")
    print("the Franco-Florentine alliance through mechanical artistry and engineering genius.")
    print()

    try:
        # Run all demonstrations
        legs = demonstrate_leg_kinematics()
        demonstrate_stability_analysis(legs)
        demonstrate_cam_profiles(legs)
        demonstrate_chest_mechanism()
        sim_result = demonstrate_complete_simulation()
        demonstrate_evaluation(sim_result)
        create_visualization()

        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("Key Achievements Demonstrated:")
        print("✓ Biomechanical gait analysis with lateral sequence walking")
        print("✓ Dynamic stability assessment throughout gait cycle")
        print("✓ Cam profile design for natural movement generation")
        print("✓ Chest cavity reveal mechanism with fleurs-de-lis display")
        print("✓ Comprehensive simulation and performance analysis")
        print("✓ Historical accuracy and Renaissance constructibility")
        print("✓ Educational value for STEM and historical learning")
        print()
        print("Leonardo's Mechanical Lion represents:")
        print("• The first programmable walking automaton (400+ years before modern robotics)")
        print("• Pioneering application of biomechanics to mechanical design")
        print("• Masterpiece of Renaissance engineering and political symbolism")
        print("• Foundation for modern robotics and automation technology")
        print("• Inspiring example of art-science integration and innovation")

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Please check the implementation and try again.")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
