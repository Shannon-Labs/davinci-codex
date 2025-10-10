"""
Theatrical Timing Sequence Coordination for Leonardo's Mechanical Lion
Master controller for perfect royal court performance synchronization
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

class PerformancePhase(Enum):
    """Performance phases for the mechanical lion show."""
    INITIAL_POSITION = "initial_position"
    POST_WALK_PAUSE = "post_walk_pause"
    CHEST_OPENING = "chest_opening"
    LILY_ELEVATION = "lily_elevation"
    ROYAL_DISPLAY = "royal_display"
    CHEST_CLOSING = "chest_closing"
    RESET_POSITION = "reset_position"
    PERFORMANCE_COMPLETE = "performance_complete"

@dataclass
class PerformanceEvent:
    """Individual performance event with timing and actions."""
    event_id: str
    phase: PerformancePhase
    start_time_s: float
    duration_s: float
    actions: List[str]
    required_mechanisms: List[str]
    critical_timing: bool = True

@dataclass
class MusicalCue:
    """Musical cue for theatrical enhancement."""
    cue_id: str
    timing_s: float
    instrument: str
    musical_phrase: str
    volume_level: str
    duration_s: float

class TheatricalSequencer:
    """Master timing controller for the mechanical lion performance."""

    def __init__(self):
        # Performance timing parameters (optimized for royal court impact)
        self.post_walk_pause_s = 2.5
        self.chest_opening_duration_s = 3.5
        self.lily_elevation_duration_s = 2.0
        self.royal_display_duration_s = 8.0
        self.chest_closing_duration_s = 4.0
        self.reset_duration_s = 10.0

        # Calculate total performance time
        self.total_performance_time_s = (
            self.post_walk_pause_s +
            self.chest_opening_duration_s +
            self.lily_elevation_duration_s +
            self.royal_display_duration_s +
            self.chest_closing_duration_s +
            self.reset_duration_s
        )

        # Initialize performance events
        self.performance_events = self._create_performance_timeline()

        # Musical cues for dramatic effect
        self.musical_cues = self._create_musical_score()

        # Current state
        self.current_time_s = 0.0
        self.current_phase = PerformancePhase.INITIAL_POSITION
        self.phase_progress = 0.0
        self.performance_active = False

        # Synchronization parameters
        self.timing_tolerance_s = 0.1  # ±100ms tolerance
        self.synchronization_checks_enabled = True

    def _create_performance_timeline(self) -> List[PerformanceEvent]:
        """Create detailed performance timeline with all events."""
        events = []

        # Event 1: Post-walk dramatic pause
        events.append(PerformanceEvent(
            event_id="pause_after_walk",
            phase=PerformancePhase.POST_WALK_PAUSE,
            start_time_s=0.0,
            duration_s=self.post_walk_pause_s,
            actions=[
                "hold_position",
                "build_anticipation",
                "prepare_spring_release"
            ],
            required_mechanisms=["position_lock"],
            critical_timing=True
        ))

        # Event 2: Chest opening sequence
        events.append(PerformanceEvent(
            event_id="chest_opening",
            phase=PerformancePhase.CHEST_OPENING,
            start_time_s=self.post_walk_pause_s,
            duration_s=self.chest_opening_duration_s,
            actions=[
                "release_chest_lock",
                "activate_spring_system",
                "open_panels_gradually",
                "monitor_panel_synchronization"
            ],
            required_mechanisms=["chest_mechanism", "spring_system", "hinge_system"],
            critical_timing=True
        ))

        # Event 3: Lily platform elevation
        events.append(PerformanceEvent(
            event_id="lily_elevation",
            phase=PerformancePhase.LILY_ELEVATION,
            start_time_s=self.post_walk_pause_s + self.chest_opening_duration_s,
            duration_s=self.lily_elevation_duration_s,
            actions=[
                "activate_scissor_lift",
                "elevate_lily_platform",
                "ensure_smooth_motion",
                "position_fleurs_de_lis"
            ],
            required_mechanisms=["scissor_lift", "lily_platform", "elevation_springs"],
            critical_timing=True
        ))

        # Event 4: Royal display period
        events.append(PerformanceEvent(
            event_id="royal_display",
            phase=PerformancePhase.ROYAL_DISPLAY,
            start_time_s=self.post_walk_pause_s + self.chest_opening_duration_s + self.lily_elevation_duration_s,
            duration_s=self.royal_display_duration_s,
            actions=[
                "hold_platform_steady",
                "display_fleurs_de_lis",
                "maintain_royal_posture",
                "allow_court_admiration"
            ],
            required_mechanisms=["position_lock", "display_lighting"],
            critical_timing=False
        ))

        # Event 5: Chest closing sequence
        events.append(PerformanceEvent(
            event_id="chest_closing",
            phase=PerformancePhase.CHEST_CLOSING,
            start_time_s=self.post_walk_pause_s + self.chest_opening_duration_s + self.lily_elevation_duration_s + self.royal_display_duration_s,
            duration_s=self.chest_closing_duration_s,
            actions=[
                "lower_lily_platform",
                "close_chest_panels",
                "engage_locking_mechanism",
                "return_to_neutral_position"
            ],
            required_mechanisms=["scissor_lift", "chest_mechanism", "locking_system"],
            critical_timing=True
        ))

        # Event 6: Reset sequence
        events.append(PerformanceEvent(
            event_id="reset_sequence",
            phase=PerformancePhase.RESET_POSITION,
            start_time_s=self.total_performance_time_s - self.reset_duration_s,
            duration_s=self.reset_duration_s,
            actions=[
                "release_all_mechanisms",
                "reset_spring_tension",
                "verify_system_ready",
                "prepare_for_next_performance"
            ],
            required_mechanisms=["reset_system", "spring_tensioner"],
            critical_timing=False
        ))

        return events

    def _create_musical_score(self) -> List[MusicalCue]:
        """Create musical score to enhance theatrical impact."""
        cues = []

        # Opening fanfare (subtle)
        cues.append(MusicalCue(
            cue_id="anticipation_fanfare",
            timing_s=0.5,
            instrument="harp",
            musical_phrase="gentle_arpeggio",
            volume_level="piano",
            duration_s=2.0
        ))

        # Chest opening music
        cues.append(MusicalCue(
            cue_id="chest_opening_music",
            timing_s=self.post_walk_pause_s + 0.5,
            instrument="lute",
            musical_phrase="rising_melody",
            volume_level="mezzo_piano",
            duration_s=3.0
        ))

        # Lily reveal flourish
        cues.append(MusicalCue(
            cue_id="lily_reveal_flourish",
            timing_s=self.post_walk_pause_s + self.chest_opening_duration_s + 0.3,
            instrument="trumpet",
            musical_phrase="royal_fanfare",
            volume_level="forte",
            duration_s=1.5
        ))

        # Royal display music
        cues.append(MusicalCue(
            cue_id="royal_display_music",
            timing_s=self.post_walk_pause_s + self.chest_opening_duration_s + self.lily_elevation_duration_s,
            instrument="viola_organista",
            musical_phrase="majestic_theme",
            volume_level="mezzo_forte",
            duration_s=6.0
        ))

        # Closing music
        cues.append(MusicalCue(
            cue_id="closing_music",
            timing_s=self.post_walk_pause_s + self.chest_opening_duration_s + self.lily_elevation_duration_s + self.royal_display_duration_s,
            instrument="harp",
            musical_phrase="graceful_fade",
            volume_level="diminuendo",
            duration_s=4.0
        ))

        return cues

    def get_current_event(self) -> Optional[PerformanceEvent]:
        """Get the current performance event based on timing."""
        for event in self.performance_events:
            if event.start_time_s <= self.current_time_s < event.start_time_s + event.duration_s:
                return event
        return None

    def get_phase_progress(self) -> float:
        """Get progress within current phase (0.0 to 1.0)."""
        current_event = self.get_current_event()
        if current_event is None:
            return 1.0

        phase_elapsed = self.current_time_s - current_event.start_time_s
        return min(1.0, phase_elapsed / current_event.duration_s)

    def update_performance_state(self, dt_s: float) -> Dict[str, object]:
        """Update performance state and return current actions."""
        self.current_time_s += dt_s

        # Get current event and phase
        current_event = self.get_current_event()
        if current_event:
            self.current_phase = current_event.phase
            self.phase_progress = self.get_phase_progress()
        else:
            if self.current_time_s >= self.total_performance_time_s:
                self.current_phase = PerformancePhase.PERFORMANCE_COMPLETE
                self.phase_progress = 1.0
            else:
                self.current_phase = PerformancePhase.INITIAL_POSITION
                self.phase_progress = 0.0

        # Get active musical cues
        active_cues = [
            cue for cue in self.musical_cues
            if cue.timing_s <= self.current_time_s < cue.timing_s + cue.duration_s
        ]

        # Return performance state
        return {
            "current_time_s": self.current_time_s,
            "current_phase": self.current_phase.value,
            "phase_progress": self.phase_progress,
            "current_event": current_event.event_id if current_event else "none",
            "active_actions": current_event.actions if current_event else [],
            "active_musical_cues": [cue.cue_id for cue in active_cues],
            "performance_complete": self.current_phase == PerformancePhase.PERFORMANCE_COMPLETE,
        }

    def calculate_theatrical_timing(self) -> Dict[str, float]:
        """Calculate optimal timing parameters for maximum theatrical impact."""
        # Dramatic timing ratios (based on Renaissance performance principles)
        anticipation_ratio = 0.15  # 15% of total time for anticipation
        reveal_ratio = 0.35  # 35% of total time for reveal sequence
        display_ratio = 0.30  # 30% of total time for display
        conclusion_ratio = 0.20  # 20% of total time for conclusion

        # Calculate optimal timing
        optimal_anticipation = self.total_performance_time_s * anticipation_ratio
        optimal_reveal = self.total_performance_time_s * reveal_ratio
        optimal_display = self.total_performance_time_s * display_ratio
        optimal_conclusion = self.total_performance_time_s * conclusion_ratio

        return {
            "total_performance_time_s": self.total_performance_time_s,
            "optimal_anticipation_s": optimal_anticipation,
            "optimal_reveal_s": optimal_reveal,
            "optimal_display_s": optimal_display,
            "optimal_conclusion_s": optimal_conclusion,
            "theatrical_impact_score": self._calculate_impact_score(),
        }

    def _calculate_impact_score(self) -> float:
        """Calculate theatrical impact score based on timing optimization."""
        # Factors affecting impact
        anticipation_effectiveness = min(1.0, self.post_walk_pause_s / 3.0)
        reveal_smoothness = 1.0 - abs(self.chest_opening_duration_s - 3.5) / 2.0
        display_adequacy = min(1.0, self.royal_display_duration_s / 6.0)
        timing_precision = 1.0  # Assume perfect timing for calculation

        impact_score = (
            anticipation_effectiveness * 0.25 +
            reveal_smoothness * 0.30 +
            display_adequacy * 0.30 +
            timing_precision * 0.15
        )

        return impact_score

    def generate_performance_script(self) -> str:
        """Generate detailed performance script for royal court presentation."""
        script = []
        script.append("LEONARDO'S MECHANICAL LION - ROYAL PERFORMANCE SCRIPT")
        script.append("=" * 60)
        script.append(f"Total Performance Time: {self.total_performance_time_s:.1f} seconds")
        script.append(f"Commissioned for: King Francis I of France")
        script.append(f"Occasion: Celebration of Franco-Florentine Alliance")
        script.append("")

        for event in self.performance_events:
            script.append(f"PHASE {event.phase.value.upper()}")
            script.append(f"Timing: {event.start_time_s:.1f}s - {event.start_time_s + event.duration_s:.1f}s")
            script.append(f"Duration: {event.duration_s:.1f}s")
            script.append("Actions:")
            for action in event.actions:
                script.append(f"  - {action}")
            script.append(f"Critical Timing: {'YES' if event.critical_timing else 'No'}")
            script.append("")

        return "\n".join(script)

def simulate_theatrical_performance():
    """Simulate complete theatrical performance with all timing coordination."""
    sequencer = TheatricalSequencer()

    # Simulation parameters
    dt = 0.05  # 50ms time steps
    total_steps = int(sequencer.total_performance_time_s / dt)

    # Data storage for analysis
    time_array = []
    phase_array = []
    progress_array = []
    musical_cues_array = []
    timing_precision_array = []

    # Run simulation
    for step in range(total_steps + 1):
        t = step * dt
        state = sequencer.update_performance_state(dt)

        time_array.append(t)
        phase_array.append(state["current_phase"])
        progress_array.append(state["phase_progress"])
        musical_cues_array.append(len(state["active_musical_cues"]))

        # Calculate timing precision (inverse of phase transition jitter)
        if step > 0 and phase_array[-1] != phase_array[-2]:
            timing_precision = 1.0 - abs(t - round(t, 1)) / 0.1
        else:
            timing_precision = 1.0
        timing_precision_array.append(timing_precision)

    return {
        "time_s": time_array,
        "phases": phase_array,
        "progress": progress_array,
        "musical_cues": musical_cues_array,
        "timing_precision": timing_precision_array,
        "sequencer": sequencer,
    }

def create_theatrical_timing_visualization():
    """Create comprehensive visualization of theatrical timing coordination."""
    sim_data = simulate_theatrical_performance()
    sequencer = sim_data["sequencer"]

    # Create multi-panel figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Theatrical Timing Sequence - Royal Court Performance", fontsize=16, fontweight='bold')

    # Plot 1: Performance phases over time
    phase_colors = {
        "initial_position": "gray",
        "post_walk_pause": "blue",
        "chest_opening": "red",
        "lily_elevation": "green",
        "royal_display": "gold",
        "chest_closing": "purple",
        "reset_position": "brown",
        "performance_complete": "black"
    }

    for i in range(len(sim_data["time_s"]) - 1):
        phase = sim_data["phases"][i]
        if phase in phase_colors:
            axes[0, 0].axvspan(sim_data["time_s"][i], sim_data["time_s"][i+1],
                               facecolor=phase_colors[phase], alpha=0.6)

    axes[0, 0].set_ylabel('Performance Phase', fontsize=12)
    axes[0, 0].set_title('Performance Phase Timeline', fontsize=14)
    axes[0, 0].set_xlim(0, sequencer.total_performance_time_s)
    axes[0, 0].set_ylim(0, 1)

    # Add phase labels
    phase_labels = {
        "post_walk_pause": "Pause",
        "chest_opening": "Chest Opening",
        "lily_elevation": "Lily Rise",
        "royal_display": "Royal Display",
        "chest_closing": "Chest Closing",
        "reset_position": "Reset"
    }

    for event in sequencer.performance_events:
        if event.phase.value in phase_labels:
            mid_time = event.start_time_s + event.duration_s / 2
            axes[0, 0].text(mid_time, 0.5, phase_labels[event.phase.value],
                           ha='center', va='center', fontsize=10, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    # Plot 2: Phase progress over time
    axes[0, 1].plot(sim_data["time_s"], sim_data["progress"], 'b-', linewidth=2.5)
    axes[0, 1].set_ylabel('Phase Progress', fontsize=12)
    axes[0, 1].set_title('Phase Progress Tracking', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_ylim(0, 1.05)

    # Add phase transition markers
    for event in sequencer.performance_events:
        axes[0, 1].axvline(x=event.start_time_s, color='gray', linestyle='--', alpha=0.5)
        axes[0, 1].axvline(x=event.start_time_s + event.duration_s, color='gray', linestyle='--', alpha=0.5)

    # Plot 3: Musical cues activity
    axes[1, 0].plot(sim_data["time_s"], sim_data["musical_cues"], 'g-', linewidth=2.5, marker='o', markersize=3)
    axes[1, 0].set_xlabel('Time (s)', fontsize=12)
    axes[1, 0].set_ylabel('Active Musical Cues', fontsize=12)
    axes[1, 0].set_title('Musical Accompaniment', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_ylim(0, max(sim_data["musical_cues"]) + 0.5)

    # Add musical cue labels
    for cue in sequencer.musical_cues:
        axes[1, 0].axvline(x=cue.timing_s, color='orange', linestyle=':', alpha=0.7)
        axes[1, 0].text(cue.timing_s, max(sim_data["musical_cues"]), cue.instrument,
                       rotation=45, ha='right', va='bottom', fontsize=8)

    # Plot 4: Timing precision analysis
    axes[1, 1].plot(sim_data["time_s"], sim_data["timing_precision"], 'r-', linewidth=2.5)
    axes[1, 1].set_xlabel('Time (s)', fontsize=12)
    axes[1, 1].set_ylabel('Timing Precision', fontsize=12)
    axes[1, 1].set_title('Synchronization Precision', fontsize=14)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_ylim(0.5, 1.05)

    # Add timing precision threshold
    axes[1, 1].axhline(y=0.9, color='green', linestyle='--', alpha=0.5, label='Excellent Precision')
    axes[1, 1].axhline(y=0.7, color='orange', linestyle='--', alpha=0.5, label='Good Precision')
    axes[1, 1].legend(loc='lower right')

    plt.tight_layout()
    return fig

def generate_performance_timing_report():
    """Generate detailed timing analysis report."""
    sequencer = TheatricalSequencer()
    timing_analysis = sequencer.calculate_theatrical_timing()

    report = []
    report.append("THEATRICAL TIMING ANALYSIS REPORT")
    report.append("=" * 50)
    report.append("")
    report.append(f"Total Performance Duration: {timing_analysis['total_performance_time_s']:.1f} seconds")
    report.append("")
    report.append("OPTIMAL TIMING BREAKDOWN:")
    report.append(f"  Anticipation Period: {timing_analysis['optimal_anticipation_s']:.1f}s")
    report.append(f"  Reveal Sequence: {timing_analysis['optimal_reveal_s']:.1f}s")
    report.append(f"  Royal Display: {timing_analysis['optimal_display_s']:.1f}s")
    report.append(f"  Conclusion: {timing_analysis['optimal_conclusion_s']:.1f}s")
    report.append("")
    report.append(f"Theatrical Impact Score: {timing_analysis['theatrical_impact_score']:.2%}")
    report.append("")
    report.append("CRITICAL TIMING REQUIREMENTS:")
    report.append("  • Post-walk pause: Build anticipation (2.5s)")
    report.append("  • Chest opening: Smooth mechanical reveal (3.5s)")
    report.append("  • Lily elevation: Dramatic platform rise (2.0s)")
    report.append("  • Royal display: Adequate viewing time (8.0s)")
    report.append("  • Reset sequence: Efficient return (10.0s)")
    report.append("")
    report.append("MUSICAL COORDINATION:")
    report.append("  • Harp: Anticipation building")
    report.append("  • Lute: Chest opening accompaniment")
    report.append("  • Trumpet: Lily reveal flourish")
    report.append("  • Viola Organista: Royal display theme")
    report.append("  • Harp: Graceful conclusion")
    report.append("")
    report.append("ROYAL COURT PERFORMANCE NOTES:")
    report.append("  • Timing optimized for maximum dramatic impact")
    report.append("  • Synchronization tolerance: ±100ms")
    report.append("  • Musical cues enhance mechanical spectacle")
    report.append("  • Fleurs-de-lis display celebrates French royalty")
    report.append("  • Performance showcases Leonardo's mechanical genius")

    return "\n".join(report)

if __name__ == "__main__":
    # Generate visualizations and reports
    fig = create_theatrical_timing_visualization()
    report = generate_performance_timing_report()
    print(report)
    plt.show()