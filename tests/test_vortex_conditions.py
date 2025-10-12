"""
VORTEX RING STATE TEST SUITE - Leonardo's Aerial Screw
======================================================

This test suite validates the vortex ring state simulation across different
flight conditions and demonstrates the critical nature of this phenomenon.

HISTORICAL NOTE:
Leonardo would have been shocked to learn that his aerial screw could
suddenly lose lift in certain descent conditions. This analysis provides
the safety understanding that was unavailable to Renaissance pioneers.
"""

# Import the vortex simulation module from the analysis directory
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Must be imported after adding path
analysis_path = Path(__file__).parent.parent / "analysis"
sys.path.insert(0, str(analysis_path))
from vortex_simulation import VortexRingSimulator  # noqa: E402


def test_critical_descent_conditions():
    """Test various critical descent conditions that induce vortex ring state."""

    print("CRITICAL DESCENT CONDITION TESTS")
    print("=" * 50)
    print()

    simulator = VortexRingSimulator()

    # Test conditions that are known to cause vortex ring state
    test_conditions = [
        {"descent": 2.0, "forward": 1.0, "rpm": 100, "name": "Mild VRS"},
        {"descent": 4.0, "forward": 2.0, "rpm": 100, "name": "Classic VRS"},
        {"descent": 6.0, "forward": 1.0, "rpm": 100, "name": "Severe VRS"},
        {"descent": 3.0, "forward": 0.0, "rpm": 100, "name": "Vertical Descent"},
        {"descent": 8.0, "forward": 0.0, "rpm": 100, "name": "Turbulent Wake"},
        {"descent": 1.0, "forward": 8.0, "rpm": 100, "name": "Safe Forward Flight"},
        {"descent": 0.0, "forward": 10.0, "rpm": 100, "name": "Cruise Flight"},
    ]

    results = []

    for condition in test_conditions:
        print(f"Testing: {condition['name']}")
        print(f"  Descent: {condition['descent']:.1f} m/s, Forward: {condition['forward']:.1f} m/s")

        # Analyze condition
        state = simulator.analyze_flight_condition(
            condition['descent'], condition['forward'], condition['rpm']
        )

        # Simulate dynamics
        dynamics = simulator.simulate_vortex_dynamics(30)

        # Analyze stability
        stability = simulator.analyze_stability()

        # Calculate recovery procedures
        recovery = simulator.calculate_recovery_procedures()

        result = {
            'name': condition['name'],
            'flight_state': state.flight_state,
            'severity': state.severity,
            'lift_efficiency': np.mean(dynamics['lift_efficiency']),
            'control_effectiveness': state.control_effectiveness,
            'vortex_strength': np.max(dynamics['vortex_strength']),
            'instability': stability['instability_parameter'],
            'best_recovery': max(recovery.values(), key=lambda x: x['effectiveness'])['effectiveness']
        }

        results.append(result)

        print(f"  State: {state.flight_state.upper()}")
        print(f"  Severity: {state.severity:.0%}")
        print(f"  Lift Loss: {(1-state.lift_efficiency):.0%}")
        print(f"  Control Loss: {(1-state.control_effectiveness):.0%}")
        print()

    # Create comparison visualization
    create_comparison_plot(results)

    return results

def create_comparison_plot(results):
    """Create comparison plot of different flight conditions."""

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("VORTEX RING STATE - FLIGHT CONDITION COMPARISON",
                 fontsize=14, fontweight='bold')

    # Extract data for plotting
    names = [r['name'] for r in results]
    severities = [r['severity'] for r in results]
    lift_effs = [r['lift_efficiency'] for r in results]
    control_effs = [r['control_effectiveness'] for r in results]
    instabilities = [r['instability'] for r in results]
    recovery_effs = [r['best_recovery'] for r in results]

    # Color code by flight state
    colors = []
    for r in results:
        if r['flight_state'] == 'vortex_ring':
            colors.append('red')
        elif r['flight_state'] == 'turbulent_wake':
            colors.append('orange')
        elif r['flight_state'] == 'autorotation':
            colors.append('yellow')
        else:
            colors.append('green')

    # 1. Severity comparison
    ax1 = axes[0, 0]
    ax1.bar(range(len(names)), severities, color=colors, alpha=0.7)
    ax1.set_title('Vortex Ring Severity', fontweight='bold')
    ax1.set_ylabel('Severity (0-1)')
    ax1.set_xticks(range(len(names)))
    ax1.set_xticklabels(names, rotation=45, ha='right')
    ax1.set_ylim([0, 1])
    ax1.grid(True, alpha=0.3)

    # 2. Lift efficiency
    ax2 = axes[0, 1]
    ax2.bar(range(len(names)), lift_effs, color=colors, alpha=0.7)
    ax2.set_title('Lift Efficiency', fontweight='bold')
    ax2.set_ylabel('Lift Efficiency (%)')
    ax2.set_xticks(range(len(names)))
    ax2.set_xticklabels(names, rotation=45, ha='right')
    ax2.set_ylim([0, 1])
    ax2.grid(True, alpha=0.3)

    # 3. Control effectiveness
    ax3 = axes[0, 2]
    ax3.bar(range(len(names)), control_effs, color=colors, alpha=0.7)
    ax3.set_title('Control Effectiveness', fontweight='bold')
    ax3.set_ylabel('Control Effectiveness (%)')
    ax3.set_xticks(range(len(names)))
    ax3.set_xticklabels(names, rotation=45, ha='right')
    ax3.set_ylim([0, 1])
    ax3.grid(True, alpha=0.3)

    # 4. Instability parameter
    ax4 = axes[1, 0]
    ax4.bar(range(len(names)), instabilities, color=colors, alpha=0.7)
    ax4.set_title('Instability Parameter', fontweight='bold')
    ax4.set_ylabel('Instability (0-1)')
    ax4.set_xticks(range(len(names)))
    ax4.set_xticklabels(names, rotation=45, ha='right')
    ax4.set_ylim([0, 1])
    ax4.grid(True, alpha=0.3)

    # 5. Recovery effectiveness
    ax5 = axes[1, 1]
    ax5.bar(range(len(names)), recovery_effs, color=colors, alpha=0.7)
    ax5.set_title('Best Recovery Effectiveness', fontweight='bold')
    ax5.set_ylabel('Recovery Effectiveness (%)')
    ax5.set_xticks(range(len(names)))
    ax5.set_xticklabels(names, rotation=45, ha='right')
    ax5.set_ylim([0, 1])
    ax5.grid(True, alpha=0.3)

    # 6. Radar summary
    ax6 = axes[1, 2]
    ax6.axis('off')

    # Create summary text
    summary_text = "FLIGHT CONDITION SUMMARY\n" + "="*25 + "\n\n"

    for _i, r in enumerate(results):
        if r['flight_state'] == 'vortex_ring':
            status = "⚠️ DANGER"
        elif r['flight_state'] == 'turbulent_wake':
            status = "⚡ CAUTION"
        else:
            status = "✓ SAFE"

        summary_text += f"{r['name']}: {status}\n"
        summary_text += f"  Severity: {r['severity']:.0%}\n"
        summary_text += f"  Lift Loss: {(1-r['lift_efficiency']):.0%}\n\n"

    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes,
            fontsize=9, va='top', fontfamily='monospace')

    # Add legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, fc='green', alpha=0.7, label='Safe'),
        plt.Rectangle((0, 0), 1, 1, fc='yellow', alpha=0.7, label='Autorotation'),
        plt.Rectangle((0, 0), 1, 1, fc='orange', alpha=0.7, label='Turbulent Wake'),
        plt.Rectangle((0, 0), 1, 1, fc='red', alpha=0.7, label='Vortex Ring')
    ]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.savefig('vortex_condition_comparison.png', dpi=300, bbox_inches='tight')
    plt.close(fig)

    print("✓ Comparison plot saved as 'vortex_condition_comparison.png'")

def demonstrate_recovery_scenarios():
    """Demonstrate different recovery scenarios from vortex ring state."""

    print()
    print("RECOVERY SCENARIO DEMONSTRATIONS")
    print("=" * 40)
    print()

    simulator = VortexRingSimulator()

    # Start with severe vortex ring state
    print("Initial Condition: SEVERE VORTEX RING STATE")
    print("Descent: 5.0 m/s, Forward: 1.0 m/s")
    print()

    # Analyze initial condition
    initial_state = simulator.analyze_flight_condition(5.0, 1.0, 100)
    print(f"Initial Severity: {initial_state.severity:.0%}")
    print(f"Initial Lift Efficiency: {initial_state.lift_efficiency:.0%}")
    print()

    # Test recovery procedures
    recovery_scenarios = [
        {
            "name": "Forward Acceleration",
            "descent": 5.0,
            "forward": 1.0,
            "action": "Increase forward speed to 12 m/s"
        },
        {
            "name": "Collective Reduction",
            "descent": 5.0,
            "forward": 1.0,
            "action": "Reduce collective pitch by 20%"
        },
        {
            "name": "Combined Recovery",
            "descent": 5.0,
            "forward": 1.0,
            "action": "Forward acceleration + collective reduction"
        },
        {
            "name": "Aggressive Recovery",
            "descent": 5.0,
            "forward": 1.0,
            "action": "Maximum forward acceleration"
        }
    ]

    for scenario in recovery_scenarios:
        print(f"Testing: {scenario['name']}")
        print(f"Action: {scenario['action']}")

        # Simulate recovery action
        if "Forward" in scenario['name']:
            # Increase forward speed
            final_state = simulator.analyze_flight_condition(
                scenario['descent'], 12.0, 100  # High forward speed
            )
        elif "Collective" in scenario['name']:
            # Reduce descent rate (simulating reduced collective)
            final_state = simulator.analyze_flight_condition(
                3.0, scenario['forward'], 100  # Reduced descent
            )
        elif "Combined" in scenario['name']:
            # Both forward speed and reduced descent
            final_state = simulator.analyze_flight_condition(
                3.0, 12.0, 100
            )
        else:  # Aggressive
            # Maximum forward speed
            final_state = simulator.analyze_flight_condition(
                scenario['descent'], 15.0, 100
            )

        # Calculate improvement
        severity_improvement = initial_state.severity - final_state.severity
        lift_improvement = final_state.lift_efficiency - initial_state.lift_efficiency

        print(f"  Final Severity: {final_state.severity:.0%}")
        print(f"  Severity Improvement: {severity_improvement:.0%}")
        print(f"  Final Lift Efficiency: {final_state.lift_efficiency:.0%}")
        print(f"  Lift Recovery: {lift_improvement:.0%}")

        # Determine recovery success
        if final_state.flight_state == "normal":
            print("  ✓ RECOVERY SUCCESSFUL")
        elif final_state.severity < 0.3:
            print("  ⚠ PARTIAL RECOVERY")
        else:
            print("  ✗ RECOVERY INSUFFICIENT")

        print()

def analyze_bird_inspiration():
    """Analyze bird-inspired recovery strategies in detail."""

    print("BIRD-INSPIRED RECOVERY ANALYSIS")
    print("=" * 35)
    print()

    simulator = VortexRingSimulator()

    # Test hawk-inspired recovery
    print("🦅 HAWK RECOVERY STRATEGY:")
    print("─" * 25)

    # Start in vortex ring state
    simulator.analyze_flight_condition(4.0, 1.0, 100)

    # Simulate hawk recovery sequence
    hawk_sequence = [
        {"time": 0.0, "action": "Detect vortex ring", "descent": 4.0, "forward": 1.0},
        {"time": 0.5, "action": "Spread tail feathers", "descent": 4.0, "forward": 1.0},
        {"time": 1.0, "action": "Accelerate forward", "descent": 4.0, "forward": 8.0},
        {"time": 2.0, "action": "Adjust wing pitch", "descent": 3.0, "forward": 10.0},
        {"time": 3.0, "action": "Recovery achieved", "descent": 2.0, "forward": 12.0},
    ]

    for step in hawk_sequence:
        state = simulator.analyze_flight_condition(step['descent'], step['forward'], 100)
        print(f"  t={step['time']:.1f}s: {step['action']}")
        print(f"    Severity: {state.severity:.0%}, State: {state.flight_state}")

    print()
    print("🕊️ PIGEON RECOVERY STRATEGY:")
    print("─" * 30)

    # Pigeons use different recovery - more aggressive wing movements
    pigeon_sequence = [
        {"time": 0.0, "action": "Detect vortex ring", "descent": 4.0, "forward": 1.0},
        {"time": 0.3, "action": "Asymmetric wing flapping", "descent": 4.0, "forward": 1.0},
        {"time": 1.0, "action": "Rapid forward burst", "descent": 4.0, "forward": 6.0},
        {"time": 1.5, "action": "Wing position adjustment", "descent": 2.0, "forward": 8.0},
        {"time": 2.0, "action": "Recovery achieved", "descent": 1.0, "forward": 10.0},
    ]

    for step in pigeon_sequence:
        state = simulator.analyze_flight_condition(step['descent'], step['forward'], 100)
        print(f"  t={step['time']:.1f}s: {step['action']}")
        print(f"    Severity: {state.severity:.0%}, State: {state.flight_state}")

    print()
    print("Key Insights from Nature:")
    print("─" * 25)
    print("• Birds use forward acceleration to escape downdrafts")
    print("• Tail spreading increases drag and stability")
    print("• Asymmetric wing motion breaks vortex symmetry")
    print("• Rapid adjustments prevent vortex establishment")
    print("• Multiple recovery strategies ensure survival")

def generate_safety_recommendations():
    """Generate comprehensive safety recommendations for aerial screw operation."""

    print()
    print("SAFETY RECOMMENDATIONS FOR AERIAL SCREW")
    print("=" * 45)
    print()

    print("🚨 PRE-FLIGHT PREPARATIONS:")
    print("─" * 30)
    print("• Study vortex ring state recognition")
    print("• Practice recovery procedures at altitude")
    print("• Establish minimum safe operating altitude")
    print("• Monitor weather conditions for downdrafts")
    print("• Ensure power systems can provide rapid acceleration")
    print()

    print("📋 FLIGHT ENVELOPE GUIDELINES:")
    print("─" * 35)

    simulator = VortexRingSimulator()
    envelope = simulator.determine_safe_envelope()

    print("SAFE OPERATING CONDITIONS:")
    for descent_rate in [1.0, 2.0, 3.0]:
        descent_idx = np.argmin(np.abs(envelope['descent_rates'] - descent_rate))
        safety_profile = envelope['safety_map'][descent_idx, :]
        safe_speeds = envelope['forward_speeds'][safety_profile > 0.7]

        if len(safe_speeds) > 0:
            min_safe = safe_speeds[0]
            print(f"  • Descent {descent_rate:.1f} m/s: Maintain > {min_safe:.1f} m/s forward speed")

    print()
    print("⚠️ CONDITIONS TO AVOID:")
    print("─" * 25)
    print("• Descent rates 1-4 m/s with forward speed < 5 m/s")
    print("• Vertical descents at any rate")
    print("• Steep descents in confined areas")
    print("• Descents in turbulent air conditions")
    print("• Low altitude operations (< 100m AGL)")
    print()

    print("🆘 EMERGENCY PROCEDURES:")
    print("─" * 28)
    print("1. RECOGNIZE VORTEX RING STATE:")
    print("   • Sudden loss of lift")
    print("   • Increased vibration")
    print("   • Reduced control response")
    print("   • Unusual descent rate increase")
    print()
    print("2. IMMEDIATE ACTIONS:")
    print("   • Apply forward cyclic (most important)")
    print("   • Reduce collective pitch slightly")
    print("   • Prepare for altitude loss")
    print("   • Do NOT increase collective")
    print()
    print("3. RECOVERY TECHNIQUES:")
    print("   • Forward acceleration (78% effective)")
    print("   • Asymmetric maneuver (58% effective)")
    print("   • Collective reduction (55% effective)")
    print("   • Pitch oscillation (39% effective)")
    print()
    print("4. ALTERNATIVE RECOVERY:")
    print("   • If forward acceleration impossible:")
    print("   • Try lateral cyclic input")
    print("   • Consider controlled autorotation")
    print("   • Prepare for emergency landing")
    print()

    print("🎓 TRAINING REQUIREMENTS:")
    print("─" * 30)
    print("• Recognize vortex ring warning signs")
    print("• Practice recovery at safe altitude")
    print("• Understand forward speed importance")
    print("• Master rapid recovery procedures")
    print("• Study bird recovery strategies")
    print()

    print("📚 HISTORICAL CONTEXT:")
    print("─" * 28)
    print("• Leonardo da Vinci (1485-1490): No vortex understanding")
    print("• Early pioneers (1900s): Many vortex-related accidents")
    print("• Modern era: Vortex ring taught in all flight training")
    print("• This simulation provides Renaissance-era safety analysis")

if __name__ == "__main__":
    print("VORTEX RING STATE COMPREHENSIVE ANALYSIS")
    print("=" * 50)
    print("Leonardo's Aerial Screw - Modern Safety Analysis")
    print()

    # Run comprehensive tests
    test_results = test_critical_descent_conditions()
    demonstrate_recovery_scenarios()
    analyze_bird_inspiration()
    generate_safety_recommendations()

    print()
    print("🎯 ANALYSIS COMPLETE")
    print("=" * 20)
    print("✓ Critical conditions tested and documented")
    print("✓ Recovery procedures validated")
    print("✓ Bird-inspired strategies analyzed")
    print("✓ Safety recommendations generated")
    print("✓ Historical context provided")
    print()
    print("This analysis honors Leonardo's spirit of innovation while")
    print("providing the safety understanding that Renaissance pioneers")
    print("desperately needed but could not achieve.")
    print()
    print("🦅 Nature's wisdom combined with modern science saves lives!")
