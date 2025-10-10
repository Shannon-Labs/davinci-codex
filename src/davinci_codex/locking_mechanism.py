"""
Locking Mechanism System for Leonardo's Mechanical Lion
Secure chest positioning system for reliable royal court performances
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np


class LockState(Enum):
    """Locking mechanism states."""
    LOCKED_CLOSED = "locked_closed"
    UNLOCKING = "unlocking"
    FREE_TO_MOVE = "free_to_move"
    LOCKING_OPEN = "locking_open"
    LOCKED_OPEN = "locked_open"
    RELEASING = "releasing"
    RESET = "reset"

@dataclass
class LockingBolt:
    """Individual locking bolt mechanism."""
    bolt_id: int
    diameter_m: float = 0.015  # 15mm bolt diameter
    length_m: float = 0.08    # 80mm bolt length
    material: str = "steel"
    spring_constant_n_m: float = 300.0
    max_extension_m: float = 0.025
    current_extension_m: float = 0.0
    engaged: bool = True

    def calculate_bolt_force(self) -> float:
        """Calculate force exerted by bolt when engaged."""
        if self.engaged:
            return self.spring_constant_n_m * self.current_extension_m
        return 0.0

    def calculate_shear_strength(self) -> float:
        """Calculate shear strength of bolt."""
        if self.material == "steel":
            shear_strength_mpa = 250  # Steel shear strength
        elif self.material == "bronze":
            shear_strength_mpa = 150  # Bronze shear strength
        else:
            shear_strength_mpa = 100  # Conservative estimate

        cross_section_area_m2 = math.pi * (self.diameter_m / 2) ** 2
        return shear_strength_mpa * 1e6 * cross_section_area_m2

@dataclass
class CamLock:
    """Cam-actuated locking mechanism."""
    cam_id: int
    cam_radius_m: float
    cam_profile: str  # "heart", "circular", "modified"
    lift_height_m: float
    material: str = "hardened_steel"
    current_angle_rad: float = 0.0
    engagement_force_n: float = 50.0

    def calculate_lift_height(self, angle_rad: float) -> float:
        """Calculate cam lift height at given angle."""
        if self.cam_profile == "heart":
            # Heart-shaped cam for smooth engagement/disengagement
            normalized_angle = (angle_rad % (2 * math.pi)) / (2 * math.pi)
            if normalized_angle < 0.5:
                lift = 2 * normalized_angle * self.lift_height_m
            else:
                lift = 2 * (1 - normalized_angle) * self.lift_height_m
        elif self.cam_profile == "circular":
            # Simple circular cam
            lift = self.lift_height_m * (1 + math.cos(angle_rad)) / 2
        else:  # modified profile
            # Modified sinusoidal for optimal performance
            lift = self.lift_height_m * (1 - math.cos(angle_rad * 2)) / 2

        return max(0, min(self.lift_height_m, lift))

    def calculate_cam_torque(self, angle_rad: float, load_n: float) -> float:
        """Calculate torque required to rotate cam under load."""
        self.calculate_lift_height(angle_rad)
        if self.cam_radius_m > 0:
            mechanical_advantage = self.cam_radius_m / (self.lift_height_m + 0.001)
            return load_n / mechanical_advantage
        return load_n

class ChestLockingSystem:
    """Complete chest locking mechanism system."""

    def __init__(self):
        # Initialize locking bolts (4 bolts for secure closure)
        self.locking_bolts = [
            LockingBolt(0, diameter_m=0.015, length_m=0.08),  # Top bolt
            LockingBolt(1, diameter_m=0.015, length_m=0.08),  # Bottom bolt
            LockingBolt(2, diameter_m=0.012, length_m=0.06),  # Left bolt
            LockingBolt(3, diameter_m=0.012, length_m=0.06),  # Right bolt
        ]

        # Initialize cam locks for controlled release
        self.cam_locks = [
            CamLock(0, cam_radius_m=0.025, cam_profile="heart", lift_height_m=0.020),
            CamLock(1, cam_radius_m=0.025, cam_profile="heart", lift_height_m=0.020),
        ]

        # System state
        self.current_state = LockState.LOCKED_CLOSED
        self.state_transition_progress = 0.0
        self.release_spring_compression_m = 0.0
        self.engagement_spring_compression_m = 0.0

        # Timing parameters
        self.unlock_duration_s = 0.5
        self.lock_open_duration_s = 0.3
        self.release_duration_s = 0.4
        self.reset_duration_s = 0.8

        # Safety parameters
        self.max_safe_load_n = 500.0  # Maximum load on locking system
        self.safety_factor = 3.0
        self.engagement_threshold_n = 25.0  # Minimum force for positive lock

    def calculate_total_locking_force(self) -> float:
        """Calculate total locking force from all bolts."""
        total_force = sum(bolt.calculate_bolt_force() for bolt in self.locking_bolts)
        return total_force

    def calculate_system_safety_margin(self) -> float:
        """Calculate safety margin for current locking configuration."""
        total_force = self.calculate_total_locking_force()
        min_shear_strength = min(bolt.calculate_shear_strength() for bolt in self.locking_bolts)

        if total_force > 0:
            safety_margin = min_shear_strength / (total_force * self.safety_factor)
            return safety_margin
        return float('inf')

    def update_locking_state(self, dt_s: float, target_state: LockState) -> Dict[str, object]:
        """Update locking system state based on target state."""
        state_changed = False

        # State machine logic
        if self.current_state == LockState.LOCKED_CLOSED and target_state == LockState.FREE_TO_MOVE:
            self.current_state = LockState.UNLOCKING
            self.state_transition_progress = 0.0
            state_changed = True

        elif self.current_state == LockState.UNLOCKING:
            self.state_transition_progress += dt_s / self.unlock_duration_s
            if self.state_transition_progress >= 1.0:
                self.current_state = LockState.FREE_TO_MOVE
                self.state_transition_progress = 0.0
                # Disengage all bolts
                for bolt in self.locking_bolts:
                    bolt.engaged = False
                    bolt.current_extension_m = 0.0
                state_changed = True

        elif self.current_state == LockState.FREE_TO_MOVE and target_state == LockState.LOCKED_OPEN:
            self.current_state = LockState.LOCKING_OPEN
            self.state_transition_progress = 0.0
            state_changed = True

        elif self.current_state == LockState.LOCKING_OPEN:
            self.state_transition_progress += dt_s / self.lock_open_duration_s
            if self.state_transition_progress >= 1.0:
                self.current_state = LockState.LOCKED_OPEN
                self.state_transition_progress = 0.0
                # Engage open position locks
                self.locking_bolts[0].engaged = True  # Top bolt
                self.locking_bolts[0].current_extension_m = self.locking_bolts[0].max_extension_m
                state_changed = True

        elif self.current_state == LockState.LOCKED_OPEN and target_state == LockState.RESET:
            self.current_state = LockState.RELEASING
            self.state_transition_progress = 0.0
            state_changed = True

        elif self.current_state == LockState.RELEASING:
            self.state_transition_progress += dt_s / self.release_duration_s
            if self.state_transition_progress >= 1.0:
                self.current_state = LockState.RESET
                self.state_transition_progress = 0.0
                # Disengage open position locks
                for bolt in self.locking_bolts:
                    bolt.engaged = False
                    bolt.current_extension_m = 0.0
                state_changed = True

        elif self.current_state == LockState.RESET:
            self.state_transition_progress += dt_s / self.reset_duration_s
            if self.state_transition_progress >= 1.0:
                self.current_state = LockState.LOCKED_CLOSED
                self.state_transition_progress = 0.0
                # Engage closed position locks
                for bolt in self.locking_bolts:
                    bolt.engaged = True
                    bolt.current_extension_m = bolt.max_extension_m
                state_changed = True

        # Update cam positions based on state
        self._update_cam_positions()

        # Calculate system status
        system_status = {
            "current_state": self.current_state.value,
            "transition_progress": self.state_transition_progress,
            "total_locking_force_n": self.calculate_total_locking_force(),
            "safety_margin": self.calculate_system_safety_margin(),
            "state_changed": state_changed,
            "engaged_bolts": sum(1 for bolt in self.locking_bolts if bolt.engaged),
            "cam_positions": [cam.current_angle_rad for cam in self.cam_locks],
        }

        return system_status

    def _update_cam_positions(self) -> None:
        """Update cam positions based on current state."""
        if self.current_state == LockState.UNLOCKING:
            # Rotate cams to release bolts
            target_angle = self.state_transition_progress * math.pi
            for cam in self.cam_locks:
                cam.current_angle_rad = target_angle

        elif self.current_state == LockState.LOCKING_OPEN:
            # Rotate cams to engage open position
            target_angle = self.state_transition_progress * math.pi
            for cam in self.cam_locks:
                cam.current_angle_rad = target_angle

        elif self.current_state == LockState.RELEASING:
            # Rotate cams to release open position
            target_angle = math.pi * (1 - self.state_transition_progress)
            for cam in self.cam_locks:
                cam.current_angle_rad = target_angle

        elif self.current_state == LockState.RESET:
            # Return cams to initial position
            target_angle = math.pi * (1 - self.state_transition_progress)
            for cam in self.cam_locks:
                cam.current_angle_rad = target_angle

        else:
            # Maintain current cam positions
            pass

    def calculate_engagement_reliability(self) -> float:
        """Calculate reliability of locking engagement."""
        # Factors affecting reliability
        force_reliability = min(1.0, self.calculate_total_locking_force() / self.engagement_threshold_n)
        safety_reliability = min(1.0, self.calculate_system_safety_margin() / 2.0)  # 2.0 is good margin
        mechanical_reliability = 0.95  # Base mechanical reliability

        # Check if bolts are properly engaged
        engagement_reliability = sum(1 for bolt in self.locking_bolts if bolt.engaged) / len(self.locking_bolts)

        overall_reliability = (
            force_reliability * 0.3 +
            safety_reliability * 0.2 +
            mechanical_reliability * 0.2 +
            engagement_reliability * 0.3
        )

        return overall_reliability

    def perform_safety_check(self) -> Dict[str, bool]:
        """Perform comprehensive safety check of locking system."""
        safety_checks = {}

        # Check bolt engagement
        safety_checks["bolts_engaged"] = all(
            bolt.engaged for bolt in self.locking_bolts
            if self.current_state in [LockState.LOCKED_CLOSED, LockState.LOCKED_OPEN]
        )

        # Check force limits
        total_force = self.calculate_total_locking_force()
        safety_checks["force_within_limits"] = total_force < self.max_safe_load_n

        # Check safety margins
        safety_margin = self.calculate_system_safety_margin()
        safety_checks["safety_margin_adequate"] = safety_margin > 1.0

        # Check cam positions
        safety_checks["cams_in_correct_position"] = all(
            0 <= cam.current_angle_rad <= 2 * math.pi for cam in self.cam_locks
        )

        # Check overall reliability
        reliability = self.calculate_engagement_reliability()
        safety_checks["reliability_acceptable"] = reliability > 0.9

        # Overall safety status
        safety_checks["overall_safe"] = all(safety_checks.values())

        return safety_checks

def simulate_locking_mechanism():
    """Simulate complete locking mechanism operation."""
    locking_system = ChestLockingSystem()

    # Simulation timing
    total_time = 20.0  # Total simulation time
    dt = 0.05  # Time step
    steps = int(total_time / dt)

    # Define state transitions
    state_schedule = [
        (0.0, LockState.LOCKED_CLOSED),
        (3.0, LockState.FREE_TO_MOVE),  # Start unlocking
        (8.0, LockState.LOCKED_OPEN),   # Start locking in open position
        (12.0, LockState.RESET),        # Start releasing
        (16.0, LockState.LOCKED_CLOSED) # Return to closed
    ]

    # Data storage
    time_array = []
    state_array = []
    force_array = []
    safety_margin_array = []
    reliability_array = []
    engaged_bolts_array = []

    current_schedule_idx = 0
    target_state = state_schedule[0][1]

    for step in range(steps + 1):
        t = step * dt
        time_array.append(t)

        # Check for state transitions
        while (current_schedule_idx < len(state_schedule) - 1 and
               t >= state_schedule[current_schedule_idx + 1][0]):
            current_schedule_idx += 1
            target_state = state_schedule[current_schedule_idx][1]

        # Update locking system
        status = locking_system.update_locking_state(dt, target_state)

        # Record data
        state_array.append(status["current_state"])
        force_array.append(status["total_locking_force_n"])
        safety_margin_array.append(status["safety_margin"])
        reliability_array.append(locking_system.calculate_engagement_reliability())
        engaged_bolts_array.append(status["engaged_bolts"])

    return {
        "time_s": time_array,
        "states": state_array,
        "locking_force_n": force_array,
        "safety_margin": safety_margin_array,
        "reliability": reliability_array,
        "engaged_bolts": engaged_bolts_array,
        "locking_system": locking_system,
    }

def create_locking_mechanism_visualization():
    """Create comprehensive visualization of locking mechanism performance."""
    sim_data = simulate_locking_mechanism()
    locking_system = sim_data["locking_system"]

    # Create multi-panel figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Chest Locking Mechanism - Royal Court Reliability System", fontsize=16, fontweight='bold')

    # State colors for visualization
    state_colors = {
        "locked_closed": "red",
        "unlocking": "orange",
        "free_to_move": "yellow",
        "locking_open": "lightgreen",
        "locked_open": "green",
        "releasing": "lightblue",
        "reset": "pink"
    }

    # Plot 1: State timeline
    for i in range(len(sim_data["time_s"]) - 1):
        state = sim_data["states"][i]
        if state in state_colors:
            axes[0, 0].axvspan(sim_data["time_s"][i], sim_data["time_s"][i+1],
                               facecolor=state_colors[state], alpha=0.7)

    axes[0, 0].set_ylabel('Locking State', fontsize=12)
    axes[0, 0].set_title('Locking Mechanism State Timeline', fontsize=14)
    axes[0, 0].set_xlim(0, 20)
    axes[0, 0].set_ylim(0, 1)

    # Add state labels

    # Plot 2: Locking force profile
    axes[0, 1].plot(sim_data["time_s"], sim_data["locking_force_n"], 'b-', linewidth=2.5)
    axes[0, 1].set_ylabel('Total Locking Force (N)', fontsize=12)
    axes[0, 1].set_title('Locking Force Profile', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)

    # Add force threshold line
    axes[0, 1].axhline(y=locking_system.engagement_threshold_n, color='red',
                       linestyle='--', alpha=0.5, label='Minimum Engagement Force')
    axes[0, 1].legend()

    # Plot 3: Safety margin analysis
    axes[1, 0].plot(sim_data["time_s"], sim_data["safety_margin"], 'g-', linewidth=2.5)
    axes[1, 0].set_xlabel('Time (s)', fontsize=12)
    axes[1, 0].set_ylabel('Safety Margin', fontsize=12)
    axes[1, 0].set_title('System Safety Margin', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)

    # Add safety threshold lines
    axes[1, 0].axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Minimum Safety')
    axes[1, 0].axhline(y=2.0, color='green', linestyle='--', alpha=0.5, label='Good Safety')
    axes[1, 0].legend()

    # Plot 4: Engagement reliability
    axes[1, 1].plot(sim_data["time_s"], sim_data["reliability"], 'm-', linewidth=2.5)
    axes[1, 1].plot(sim_data["time_s"], np.array(sim_data["engaged_bolts"]) / 4.0,
                    'c--', linewidth=2, label='Bolt Engagement Ratio')
    axes[1, 1].set_xlabel('Time (s)', fontsize=12)
    axes[1, 1].set_ylabel('Reliability / Engagement', fontsize=12)
    axes[1, 1].set_title('System Reliability Metrics', fontsize=14)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_ylim(0, 1.1)
    axes[1, 1].legend()

    plt.tight_layout()
    return fig

def generate_safety_analysis_report():
    """Generate comprehensive safety analysis report."""
    locking_system = ChestLockingSystem()
    safety_checks = locking_system.perform_safety_check()

    report = []
    report.append("CHEST LOCKING MECHANISM - SAFETY ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    report.append("SYSTEM CONFIGURATION:")
    report.append(f"  • Number of locking bolts: {len(locking_system.locking_bolts)}")
    report.append(f"  • Number of cam locks: {len(locking_system.cam_locks)}")
    report.append(f"  • Total locking force: {locking_system.calculate_total_locking_force():.1f} N")
    report.append(f"  • Safety factor: {locking_system.safety_factor}")
    report.append("")
    report.append("SAFETY CHECK RESULTS:")
    for check_name, result in safety_checks.items():
        status = "PASS" if result else "FAIL"
        report.append(f"  • {check_name.replace('_', ' ').title()}: {status}")
    report.append("")
    report.append("MECHANICAL SPECIFICATIONS:")
    for i, bolt in enumerate(locking_system.locking_bolts):
        report.append(f"  • Bolt {i}: {bolt.material}, Ø{bolt.diameter_m*1000:.0f}mm, "
                     f"Force: {bolt.calculate_bolt_force():.1f}N")
    report.append("")
    report.append("RELIABILITY ANALYSIS:")
    reliability = locking_system.calculate_engagement_reliability()
    report.append(f"  • Overall reliability: {reliability:.1%}")
    report.append(f"  • Safety margin: {locking_system.calculate_system_safety_margin():.2f}")
    report.append(f"  • Engagement threshold: {locking_system.engagement_threshold_n:.1f} N")
    report.append("")
    report.append("ROYAL COURT PERFORMANCE REQUIREMENTS:")
    report.append("  • Zero failure tolerance for royal performances")
    report.append("  • Positive lock engagement in all positions")
    report.append("  • Smooth transition between states")
    report.append("  • Manual override capability")
    report.append("  • Quick reset between performances")
    report.append("")
    report.append("MAINTENANCE RECOMMENDATIONS:")
    report.append("  • Inspect bolt engagement before each performance")
    report.append("  • Lubricate cam mechanisms weekly")
    report.append("  • Check spring tension monthly")
    report.append("  • Verify safety margins quarterly")
    report.append("  • Replace worn components annually")

    return "\n".join(report)

if __name__ == "__main__":
    # Generate visualizations and reports
    fig = create_locking_mechanism_visualization()
    report = generate_safety_analysis_report()
    print(report)
    plt.show()
