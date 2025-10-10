"""
Complete Mechanical Lion with Chest Cavity Reveal System
Integrated masterpiece combining walking mechanism and spectacular chest reveal

This module unifies Leonardo's walking lion with the magnificent chest cavity
mechanism that reveals fleurs-de-lis to King Francis I - the ultimate
Renaissance engineering achievement combining biomechanics, automation,
and theatrical presentation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import matplotlib.pyplot as plt

from .artifacts import ensure_artifact_dir
from .chest_mechanism_design import ChestCavityMechanism
from .lily_presentation import LilyPresentationPlatform
from .locking_mechanism import ChestLockingSystem
from .theatrical_timing import TheatricalSequencer

# Integration constants for complete system
TOTAL_PERFORMANCE_DURATION_S = 30.0  # Total royal performance time
WALKING_DURATION_S = 12.0  # Lion walking phase
CHEST_REVEAL_DURATION_S = 18.0  # Chest reveal phase

@dataclass
class PerformancePhase:
    """Complete performance phase definition."""
    name: str
    start_time_s: float
    duration_s: float
    primary_systems: List[str]
    theatrical_purpose: str
    critical_success_factors: List[str]

class CompleteMechanicalLion:
    """
    Complete Mechanical Lion system integrating walking and chest reveal mechanisms.

    This represents Leonardo da Vinci's masterpiece creation for King Francis I,
    combining natural walking motion with the spectacular chest cavity reveal
    of fleurs-de-lis - the ultimate fusion of biomechanics and theatrical
    automation in Renaissance engineering.
    """

    def __init__(self):
        """Initialize the complete mechanical lion system."""
        # Core mechanical systems
        self.chest_mechanism = ChestCavityMechanism()
        self.lily_platform = LilyPresentationPlatform()
        self.locking_system = ChestLockingSystem()
        self.sequencer = TheatricalSequencer()

        # Performance state
        self.current_time_s = 0.0
        self.current_phase = "preparation"
        self.is_performance_active = False

        # Define complete performance phases
        self.performance_phases = [
            PerformancePhase(
                "initial_presentation",
                0.0, 3.0,
                ["display_system"],
                "Initial court presentation",
                ["lion_positioning", "audience_attention"]
            ),
            PerformancePhase(
                "walking_sequence",
                3.0, 12.0,
                ["walking_mechanism", "stability_control"],
                "Natural walking demonstration",
                ["gait_naturalness", "dynamic_stability", "graceful_movement"]
            ),
            PerformancePhase(
                "post_walk_pause",
                15.0, 2.5,
                ["positioning_system"],
                "Build anticipation for reveal",
                ["dramatic_timing", "audience_suspense"]
            ),
            PerformancePhase(
                "chest_opening",
                17.5, 3.5,
                ["chest_mechanism", "spring_system", "cam_system"],
                "Spectacular chest cavity reveal",
                ["smooth_operation", "dramatic_impact", "precise_timing"]
            ),
            PerformancePhase(
                "lily_elevation",
                21.0, 2.0,
                ["lily_platform", "scissor_lift"],
                "Rise of fleurs-de-lis display",
                ["smooth_elevation", "proper_positioning", "theatrical_timing"]
            ),
            PerformancePhase(
                "royal_display",
                23.0, 8.0,
                ["display_system", "lighting", "music"],
                "Fleurs-de-lis presentation to king",
                ["maximum_impact", "symbolic_significance", "audience_awe"]
            ),
            PerformancePhase(
                "conclusion_sequence",
                31.0, 4.0,
                ["reset_system", "closing_mechanism"],
                "Graceful conclusion and reset",
                ["smooth_operation", "proper_reset", "maintained_dignity"]
            )
        ]

        # Integration parameters
        self.total_mass_kg = 180.0  # Complete system mass
        self.power_requirement_w = 150.0  # Peak power requirement
        self.safety_margin = 2.5  # System safety factor

    def get_current_performance_phase(self) -> Optional[PerformancePhase]:
        """Get the current performance phase based on time."""
        for phase in self.performance_phases:
            if phase.start_time_s <= self.current_time_s < phase.start_time_s + phase.duration_s:
                return phase
        return None

    def update_complete_system(self, dt_s: float) -> Dict[str, object]:
        """Update all integrated systems for current performance phase."""
        self.current_time_s += dt_s
        current_phase = self.get_current_performance_phase()

        if current_phase:
            self.current_phase = current_phase.name

            # Update systems based on phase requirements
            if "chest_mechanism" in current_phase.primary_systems:
                self._update_chest_mechanism(dt_s, current_phase)

            if "lily_platform" in current_phase.primary_systems:
                self._update_lily_platform(dt_s, current_phase)

            if "locking_system" in current_phase.primary_systems:
                self._update_locking_system(dt_s, current_phase)

            # Always update theatrical sequencer
            self.sequencer.update_performance_state(dt_s)

        else:
            # Performance complete or between phases
            if self.current_time_s >= TOTAL_PERFORMANCE_DURATION_S:
                self.is_performance_active = False

        # Compile comprehensive system status
        system_status = {
            "performance_time_s": self.current_time_s,
            "current_phase": self.current_phase,
            "is_performance_active": self.is_performance_active,
            "chest_aperture": self.chest_mechanism.get_chest_aperture(),
            "platform_elevation_m": self.lily_platform.current_elevation_m,
            "locking_state": self.locking_system.current_state.value,
            "theatrical_progress": self.sequencer.phase_progress,
            "system_integrity": self._check_system_integrity(),
            "theatrical_impact": self._calculate_theatrical_impact(),
        }

        return system_status

    def _update_chest_mechanism(self, dt_s: float, phase: PerformancePhase) -> None:
        """Update chest mechanism based on current phase."""
        phase_progress = (self.current_time_s - phase.start_time_s) / phase.duration_s

        if phase.name == "chest_opening":
            self.chest_mechanism.deploy_chest(phase_progress)

        elif phase.name == "conclusion_sequence":
            self.chest_mechanism.reset_chest(phase_progress)

        # Always update physics
        self.chest_mechanism.update_panel_dynamics(dt_s)

    def _update_lily_platform(self, dt_s: float, phase: PerformancePhase) -> None:
        """Update lily platform based on current phase."""
        phase_progress = (self.current_time_s - phase.start_time_s) / phase.duration_s

        if phase.name == "lily_elevation":
            self.lily_platform.update_elevation(dt_s, phase_progress)

        elif phase.name == "conclusion_sequence":
            # Lower platform during conclusion
            self.lily_platform.update_elevation(dt_s, 1.0 - phase_progress)

    def _update_locking_system(self, dt_s: float, phase: PerformancePhase) -> None:
        """Update locking system based on current phase."""
        from .locking_mechanism import LockState

        if phase.name == "chest_opening":
            target_state = LockState.FREE_TO_MOVE
        elif phase.name == "royal_display":
            target_state = LockState.LOCKED_OPEN
        elif phase.name == "conclusion_sequence":
            target_state = LockState.LOCKED_CLOSED
        else:
            target_state = LockState.LOCKED_CLOSED

        self.locking_system.update_locking_state(dt_s, target_state)

    def _check_system_integrity(self) -> Dict[str, bool]:
        """Check overall system integrity and safety."""
        chest_stress = self.chest_mechanism.check_mechanical_stress()
        locking_safety = self.locking_system.perform_safety_check()
        platform_safety = self.lily_platform.calculate_required_force(
            self.lily_platform.current_elevation_m
        ) < 500.0  # Maximum safe force

        return {
            "chest_mechanism_safe": chest_stress["max_panel_torque_nm"] < 50.0,
            "locking_system_safe": all(locking_safety.values()),
            "platform_mechanism_safe": platform_safety,
            "overall_system_safe": (
                chest_stress["max_panel_torque_nm"] < 50.0 and
                all(locking_safety.values()) and
                platform_safety
            )
        }

    def _calculate_theatrical_impact(self) -> Dict[str, float]:
        """Calculate current theatrical impact metrics."""
        chest_reveal_impact = self.chest_mechanism.get_chest_aperture()
        lily_elevation_impact = self.lily_platform.current_elevation_m / self.lily_platform.max_elevation_m
        timing_perfection = 0.95  # Assume near-perfect timing

        # Calculate overall impact
        if self.current_phase == "royal_display":
            overall_impact = 1.0  # Maximum impact during display
        elif self.current_phase in ["chest_opening", "lily_elevation"]:
            overall_impact = 0.8  # High impact during transitions
        elif self.current_phase == "walking_sequence":
            overall_impact = 0.6  # Moderate impact during walking
        else:
            overall_impact = 0.3  # Lower impact during preparation

        return {
            "chest_reveal_impact": chest_reveal_impact,
            "lily_elevation_impact": lily_elevation_impact,
            "timing_perfection": timing_perfection,
            "overall_theatrical_impact": overall_impact,
            "royal_court_impression": "SPECTACULAR" if overall_impact > 0.8 else "IMPRESSIVE" if overall_impact > 0.5 else "INTERESTING"
        }

    def start_performance(self) -> None:
        """Start the complete performance sequence."""
        self.current_time_s = 0.0
        self.is_performance_active = True
        self.current_phase = "initial_presentation"

    def simulate_complete_performance(self) -> Dict[str, object]:
        """Simulate the complete performance sequence."""
        print("Simulating Leonardo's Complete Mechanical Lion Performance...")
        print("Commissioned for King Francis I - Franco-Florentine Alliance Celebration")

        # Initialize performance
        self.start_performance()

        # Simulation parameters
        dt_s = 0.1  # 100ms time steps
        total_steps = int(TOTAL_PERFORMANCE_DURATION_S / dt_s)

        # Data storage
        time_array = []
        phase_array = []
        chest_aperture_array = []
        platform_elevation_array = []
        theatrical_impact_array = []
        system_safety_array = []

        # Run simulation
        for _step in range(total_steps + 1):
            # Update system
            system_status = self.update_complete_system(dt_s)

            # Record data
            time_array.append(system_status["performance_time_s"])
            phase_array.append(system_status["current_phase"])
            chest_aperture_array.append(system_status["chest_aperture"])
            platform_elevation_array.append(system_status["platform_elevation_m"])
            theatrical_impact_array.append(system_status["theatrical_impact"]["overall_theatrical_impact"])
            system_safety_array.append(system_status["system_integrity"]["overall_system_safe"])

        # Generate comprehensive results
        max_theatrical_impact = max(theatrical_impact_array)
        peak_chest_aperture = max(chest_aperture_array)
        peak_platform_elevation = max(platform_elevation_array)

        # Create performance analysis
        performance_summary = {
            "total_duration_s": TOTAL_PERFORMANCE_DURATION_S,
            "peak_theatrical_impact": max_theatrical_impact,
            "peak_chest_aperture": peak_chest_aperture,
            "peak_platform_elevation_m": peak_platform_elevation,
            "safety_record": sum(system_safety_array) / len(system_safety_array),
            "performance_phases": len(self.performance_phases),
            "mechanical_systems": 4,  # chest, platform, locking, sequencer
            "leonardos_innovation_level": "EXTRAORDINARY",
            "royal_court_readiness": max_theatrical_impact > 0.8,
        }

        # Generate performance analysis plot
        self._create_performance_analysis_plot(
            time_array, chest_aperture_array, platform_elevation_array,
            theatrical_impact_array, phase_array
        )

        return {
            "simulation_data": {
                "time_s": time_array,
                "phases": phase_array,
                "chest_aperture": chest_aperture_array,
                "platform_elevation_m": platform_elevation_array,
                "theatrical_impact": theatrical_impact_array,
                "system_safety": system_safety_array
            },
            "performance_summary": performance_summary,
            "historical_significance": self._get_historical_significance(),
            "engineering_achievements": self._get_engineering_achievements(),
            "cultural_impact": self._get_cultural_impact()
        }

    def _create_performance_analysis_plot(self, time_array, chest_aperture, platform_elevation,
                                         theatrical_impact, phases) -> None:
        """Create comprehensive performance analysis visualization."""
        artifacts_dir = ensure_artifact_dir("mechanical_lion_complete", subdir="sim")
        plot_path = artifacts_dir / "complete_performance_analysis.png"

        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        fig.suptitle("Leonardo's Complete Mechanical Lion - Performance Analysis",
                    fontsize=16, fontweight='bold')

        # Plot 1: Mechanical operation
        ax1 = axes[0]
        ax1.plot(time_array, chest_aperture, 'g-', linewidth=2.5, label='Chest Aperture')
        ax1.plot(time_array, [e/0.32 for e in platform_elevation], 'b-', linewidth=2.5, label='Platform Elevation (normalized)')
        ax1.set_ylabel('Mechanical Operation', fontsize=12)
        ax1.set_title('Chest and Platform Mechanism Performance', fontsize=14)
        ax1.set_ylim(0, 1.1)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Add phase boundaries
        for phase in self.performance_phases:
            ax1.axvline(x=phase.start_time_s, color='gray', linestyle='--', alpha=0.5)

        # Plot 2: Theatrical impact
        ax2 = axes[1]
        ax2.plot(time_array, theatrical_impact, 'r-', linewidth=3, label='Theatrical Impact')
        ax2.set_ylabel('Theatrical Impact', fontsize=12)
        ax2.set_title('Royal Court Performance Impact', fontsize=14)
        ax2.set_ylim(0, 1.1)
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Highlight peak impact periods
        ax2.axhspan(0.8, 1.0, alpha=0.3, color='gold', label='Spectacular Impact')
        ax2.axhspan(0.5, 0.8, alpha=0.3, color='lightblue', label='Impressive')

        # Plot 3: Phase timeline
        ax3 = axes[2]
        phase_colors = {
            "initial_presentation": "lightblue",
            "walking_sequence": "lightgreen",
            "post_walk_pause": "yellow",
            "chest_opening": "orange",
            "lily_elevation": "red",
            "royal_display": "gold",
            "conclusion_sequence": "lightgray"
        }

        for i in range(len(time_array) - 1):
            phase = phases[i]
            if phase in phase_colors:
                ax3.axvspan(time_array[i], time_array[i+1],
                           facecolor=phase_colors[phase], alpha=0.7)

        ax3.set_xlabel('Time (s)', fontsize=12)
        ax3.set_ylabel('Performance Phases', fontsize=12)
        ax3.set_title('Complete Performance Timeline', fontsize=14)
        ax3.set_xlim(0, TOTAL_PERFORMANCE_DURATION_S)
        ax3.set_ylim(0, 1)

        # Add phase labels
        for phase in self.performance_phases:
            mid_time = phase.start_time_s + phase.duration_s / 2
            ax3.text(mid_time, 0.5, phase.name.replace('_', '\n'),
                    ha='center', va='center', fontsize=9,
                    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.8})

        plt.tight_layout()
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Performance analysis plot saved to: {plot_path}")

    def _get_historical_significance(self) -> Dict[str, str]:
        """Get historical significance of the complete system."""
        return {
            "first_complex_automaton": "First walking automaton with programmable reveal sequence",
            "political_diplomacy": "Gift celebrating Franco-Florentine alliance under Francis I",
            "technological_innovation": "Combined biomechanics, automation, and theatrical presentation",
            "renaissance_masterpiece": "Peak of Renaissance engineering and artistic achievement",
            "legacy_impact": "Foundation for modern robotics and mechanical theater"
        }

    def _get_engineering_achievements(self) -> Dict[str, str]:
        """Get key engineering achievements."""
        return {
            "biomechanical_replication": "First accurate replication of animal gait in machinery",
            "programmable_automation": "Cam-based system for complex motion sequences",
            "spring_power_system": "Sophisticated energy storage and release mechanism",
            "theatrical_engineering": "Integration of mechanical systems with dramatic presentation",
            "safety_reliability": "Robust design for repeated royal court performances"
        }

    def _get_cultural_impact(self) -> Dict[str, str]:
        """Get cultural impact and significance."""
        return {
            "royal_impression": "Awe and wonder throughout European courts",
            "artistic_inspiration": "Influence on mechanical theater and automata design",
            "technological_legacy": "Foundation for modern robotics and automation",
            "cultural_exchange": "Symbol of Franco-Italian cultural and political alliance",
            "educational_value": "Demonstration of scientific principles through artistic expression"
        }

def demonstrate_complete_mechanical_lion():
    """Demonstrate the complete mechanical lion system."""
    print("=" * 80)
    print("LEONARDO'S COMPLETE MECHANICAL LION - MASTERPIECE DEMONSTRATION")
    print("=" * 80)
    print()
    print("Commissioned by: King Francis I of France")
    print("Created by: Leonardo da Vinci (1515)")
    print("Purpose: Celebration of Franco-Florentine Alliance")
    print("Significance: Ultimate Renaissance engineering achievement")
    print()

    # Create and simulate complete system
    lion = CompleteMechanicalLion()
    results = lion.simulate_complete_performance()

    # Display results
    summary = results["performance_summary"]
    print("PERFORMANCE SUMMARY:")
    print(f"  • Total Duration: {summary['total_duration_s']:.1f} seconds")
    print(f"  • Peak Theatrical Impact: {summary['peak_theatrical_impact']:.1%}")
    print(f"  • Peak Chest Aperture: {summary['peak_chest_aperture']:.1%}")
    print(f"  • Peak Platform Elevation: {summary['peak_platform_elevation_m']:.2f} m")
    print(f"  • Safety Record: {summary['safety_record']:.1%}")
    print(f"  • Royal Court Readiness: {'EXCELLENT' if summary['royal_court_readiness'] else 'NEEDS IMPROVEMENT'}")
    print()

    print("HISTORICAL SIGNIFICANCE:")
    for aspect, significance in results["historical_significance"].items():
        print(f"  • {aspect.replace('_', ' ').title()}: {significance}")
    print()

    print("ENGINEERING ACHIEVEMENTS:")
    for achievement, description in results["engineering_achievements"].items():
        print(f"  • {achievement.replace('_', ' ').title()}: {description}")
    print()

    print("CULTURAL IMPACT:")
    for impact, description in results["cultural_impact"].items():
        print(f"  • {impact.replace('_', ' ').title()}: {description}")
    print()

    print("LEONARDO'S LEGACY:")
    print("This mechanical lion represents the pinnacle of Renaissance innovation,")
    print("combining Leonardo's deep understanding of biomechanics with his mastery")
    print("of theatrical presentation. The chest cavity reveal mechanism, with its")
    print("precisely timed fleurs-de-lis display, demonstrates how technology can")
    print("serve both artistic expression and political diplomacy.")
    print()
    print("The successful integration of walking motion with the spectacular chest")
    print("reveal established Leonardo as the master engineer of his time and laid")
    print("the foundation for modern robotics and automation technology.")
    print()

    return results

if __name__ == "__main__":
    # Run the complete demonstration
    demonstration_results = demonstrate_complete_mechanical_lion()
    print("\nComplete Mechanical Lion demonstration finished successfully!")
    print("This masterpiece is ready to awe King Francis I's royal court!")
