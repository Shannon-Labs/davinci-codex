"""
Energy Budget Analysis for Leonardo's Mechanical Lion

This module calculates the complete energy requirements for the Mechanical Lion
performance sequence, providing detailed power analysis for both spring-wound
and weight-driven power systems.

Performance Sequence:
1. Walking Phase: 3 steps forward with leg articulation
2. Tail Movement: Continuous swaying during walk
3. Post-Walk Pause: 2.5 seconds of dramatic stillness
4. Chest Opening: 3.5 seconds of panel deployment
5. Lily Elevation: 2.0 seconds of platform rise
6. Display Duration: 8.0 seconds of fleurs-de-lis presentation
7. Reset Sequence: 10.0 seconds for preparation

Total Performance Time: 30 seconds
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Physical Constants
GRAVITY = 9.80665  # m/s²

# Lion Parameters (from existing mechanical_lion.py)
LION_WEIGHT = 180.0  # kg (mechanical lion total weight)
LION_LENGTH = 2.4  # meters
LION_HEIGHT = 1.2  # meters
LION_WIDTH = 0.8  # meters

# Performance Timing (seconds)
WALKING_DURATION = 6.0  # 3 steps at 2 seconds each
TAIL_MOVEMENT_DURATION = 6.0  # During walking
POST_WALK_PAUSE = 2.5
CHEST_OPENING_DURATION = 3.5
LILY_ELEVATION_DURATION = 2.0
DISPLAY_DURATION = 8.0
RESET_DURATION = 10.0

TOTAL_PERFORMANCE_TIME = (
    WALKING_DURATION + POST_WALK_PAUSE +
    CHEST_OPENING_DURATION + LILY_ELEVATION_DURATION +
    DISPLAY_DURATION
)

# Mechanical Efficiency Factors
RENAISSANCE_GEAR_EFFICIENCY = 0.85  # Bronze gears with oil lubrication
WOOD_BEARING_EFFICIENCY = 0.90     # Oak bearings with wax
SPRING_EFFICIENCY = 0.95           # High-quality steel springs
LINKAGE_EFFICIENCY = 0.92          # Four-bar linkages
OVERALL_EFFICIENCY = (
    RENAISSANCE_GEAR_EFFICIENCY *
    WOOD_BEARING_EFFICIENCY *
    SPRING_EFFICIENCY *
    LINKAGE_EFFICIENCY
)

@dataclass
class EnergyComponent:
    """Individual energy-consuming component in the lion mechanism."""
    name: str
    duration_s: float
    force_n: float
    distance_m: float
    power_w: float
    energy_j: float
    description: str

class EnergyBudget:
    """
    Comprehensive energy budget calculation for the Mechanical Lion.

    This class analyzes all energy-consuming components throughout the
    performance sequence, providing detailed power requirements for
    optimal power system design.
    """

    def __init__(self):
        self.components: List[EnergyComponent] = []
        self.total_energy_j = 0.0
        self.peak_power_w = 0.0
        self.average_power_w = 0.0
        self._calculate_energy_requirements()

    def _calculate_energy_requirements(self) -> None:
        """Calculate energy requirements for all performance phases."""

        # 1. Walking Phase Energy
        self._calculate_walking_energy()

        # 2. Tail Movement Energy
        self._calculate_tail_energy()

        # 3. Chest Opening Energy
        self._calculate_chest_energy()

        # 4. Lily Platform Energy
        self._calculate_lily_energy()

        # 5. Control System Energy
        self._calculate_control_energy()

        # 6. Friction and Losses
        self._calculate_friction_losses()

        # Calculate totals
        self._calculate_totals()

    def _calculate_walking_energy(self) -> None:
        """Calculate energy requirements for walking mechanism."""

        # Leg articulation energy
        leg_mass = LION_WEIGHT * 0.15  # Each leg ~15% of total weight
        leg_lift_height = 0.1  # meters
        leg_forward_distance = LION_LENGTH / 6  # Step length

        # Energy per leg per step
        lift_energy_per_leg = leg_mass * GRAVITY * leg_lift_height
        forward_energy_per_leg = leg_mass * GRAVITY * leg_forward_distance * 0.1  # Rolling resistance

        # Total walking energy (4 legs × 3 steps)
        total_leg_energy = (lift_energy_per_leg + forward_energy_per_leg) * 4 * 3

        # Power during walking
        walking_power = total_leg_energy / WALKING_DURATION

        self.components.append(EnergyComponent(
            name="Walking Mechanism",
            duration_s=WALKING_DURATION,
            force_n=leg_mass * GRAVITY * 4,  # All legs combined
            distance_m=leg_forward_distance * 3,
            power_w=walking_power,
            energy_j=total_leg_energy,
            description="Four-leg articulation for 3 forward steps"
        ))

    def _calculate_tail_energy(self) -> None:
        """Calculate energy requirements for tail movement."""

        tail_mass = LION_WEIGHT * 0.03  # Tail ~3% of total weight
        tail_length = LION_LENGTH * 0.4  # 40% of body length
        tail_swing_angle = math.pi / 6  # 30 degrees swing
        tail_sway_frequency = 1.5  # Hz

        # Tail arc length
        tail_arc_length = tail_length * tail_swing_angle

        # Number of sways during walking
        num_sways = TAIL_MOVEMENT_DURATION * tail_sway_frequency

        # Total tail energy
        tail_energy = tail_mass * GRAVITY * tail_arc_length * num_sways * 0.5
        tail_power = tail_energy / TAIL_MOVEMENT_DURATION

        self.components.append(EnergyComponent(
            name="Tail Movement",
            duration_s=TAIL_MOVEMENT_DURATION,
            force_n=tail_mass * GRAVITY,
            distance_m=tail_arc_length * num_sways,
            power_w=tail_power,
            energy_j=tail_energy,
            description="Continuous tail swaying during walking phase"
        ))

    def _calculate_chest_energy(self) -> None:
        """Calculate energy requirements for chest cavity opening."""

        # Chest panel parameters
        panel_mass = 2.5  # kg per decorative panel
        num_panels = 4  # Left, right, top, bottom
        panel_com_distance = 0.3  # Center of mass distance from hinge
        opening_angle = math.pi / 3  # 60 degrees

        # Energy to open all panels
        panel_arc_length = panel_com_distance * opening_angle
        total_panel_energy = num_panels * panel_mass * GRAVITY * panel_arc_length

        # Power during chest opening
        chest_power = total_panel_energy / CHEST_OPENING_DURATION

        self.components.append(EnergyComponent(
            name="Chest Opening",
            duration_s=CHEST_OPENING_DURATION,
            force_n=num_panels * panel_mass * GRAVITY,
            distance_m=panel_arc_length,
            power_w=chest_power,
            energy_j=total_panel_energy,
            description="Opening 4 decorative chest panels to reveal interior"
        ))

    def _calculate_lily_energy(self) -> None:
        """Calculate energy requirements for lily platform elevation."""

        # Platform parameters
        platform_mass = 5.0  # kg
        lily_mass = 0.5  # kg per fleur-de-lis
        num_lilies = 3
        elevation_height = 0.15  # meters

        # Total mass being elevated
        total_elevated_mass = platform_mass + (lily_mass * num_lilies)

        # Gravitational potential energy
        lily_energy = total_elevated_mass * GRAVITY * elevation_height

        # Power during elevation
        lily_power = lily_energy / LILY_ELEVATION_DURATION

        self.components.append(EnergyComponent(
            name="Lily Platform",
            duration_s=LILY_ELEVATION_DURATION,
            force_n=total_elevated_mass * GRAVITY,
            distance_m=elevation_height,
            power_w=lily_power,
            energy_j=lily_energy,
            description="Elevating platform with 3 fleurs-de-lis"
        ))

    def _calculate_control_energy(self) -> None:
        """Calculate energy requirements for control system."""

        # Cam drum rotation energy
        cam_drum_mass = 8.0  # kg
        cam_drum_radius = 0.15  # meters
        cam_rotations = 5  # Total rotations during performance

        # Rotational kinetic energy
        cam_angular_velocity = (2 * math.pi * cam_rotations) / TOTAL_PERFORMANCE_TIME
        cam_rotational_energy = 0.5 * cam_drum_mass * (cam_drum_radius * cam_angular_velocity) ** 2

        # Escapement mechanism energy
        escapement_power = 2.0  # Continuous power for regulation
        escapement_energy = escapement_power * TOTAL_PERFORMANCE_TIME

        total_control_energy = cam_rotational_energy + escapement_energy
        control_power = total_control_energy / TOTAL_PERFORMANCE_TIME

        self.components.append(EnergyComponent(
            name="Control System",
            duration_s=TOTAL_PERFORMANCE_TIME,
            force_n=20.0,  # Approximate force for cam followers
            distance_m=2 * math.pi * cam_drum_radius * cam_rotations,
            power_w=control_power,
            energy_j=total_control_energy,
            description="Cam drum rotation and escapement regulation"
        ))

    def _calculate_friction_losses(self) -> None:
        """Calculate energy losses due to friction."""

        # Friction losses throughout performance
        base_friction_power = 5.0  # Continuous friction losses
        peak_friction_power = 15.0  # During high-load operations

        # Weighted average based on activity level
        avg_friction_power = (
            base_friction_power * 0.7 +  # 70% low activity
            peak_friction_power * 0.3    # 30% high activity
        )

        friction_energy = avg_friction_power * TOTAL_PERFORMANCE_TIME

        self.components.append(EnergyComponent(
            name="Friction Losses",
            duration_s=TOTAL_PERFORMANCE_TIME,
            force_n=10.0,  # Equivalent friction force
            distance_m=1.0,  # Normalized for power calculation
            power_w=avg_friction_power,
            energy_j=friction_energy,
            description="Friction in bearings, gears, and linkages"
        ))

    def _calculate_totals(self) -> None:
        """Calculate total energy and power requirements."""

        self.total_energy_j = sum(comp.energy_j for comp in self.components)
        self.peak_power_w = max(comp.power_w for comp in self.components)
        self.average_power_w = self.total_energy_j / TOTAL_PERFORMANCE_TIME

    def get_energy_breakdown(self) -> Dict[str, Dict[str, float]]:
        """Get detailed energy breakdown by component."""

        breakdown = {}
        for comp in self.components:
            breakdown[comp.name] = {
                "energy_j": comp.energy_j,
                "power_w": comp.power_w,
                "duration_s": comp.duration_s,
                "percentage": (comp.energy_j / self.total_energy_j) * 100
            }

        return breakdown

    def get_phase_power_profile(self) -> List[Tuple[float, float, str]]:
        """Get power requirements over time for each performance phase."""

        phases = [
            (0, WALKING_DURATION, "Walking"),
            (WALKING_DURATION, POST_WALK_PAUSE, "Pause"),
            (WALKING_DURATION + POST_WALK_PAUSE, CHEST_OPENING_DURATION, "Chest Opening"),
            (WALKING_DURATION + POST_WALK_PAUSE + CHEST_OPENING_DURATION,
             LILY_ELEVATION_DURATION, "Lily Elevation"),
            (WALKING_DURATION + POST_WALK_PAUSE + CHEST_OPENING_DURATION + LILY_ELEVATION_DURATION,
             DISPLAY_DURATION, "Display")
        ]

        profile = []
        current_time = 0.0

        for start_time, duration, phase_name in phases:
            # Calculate power for this phase
            phase_power = 0.0
            for comp in self.components:
                if (current_time >= comp.duration_s or
                    current_time + duration <= 0):
                    continue

                # Calculate overlapping time
                overlap_start = max(current_time, 0)
                overlap_end = min(current_time + duration, comp.duration_s)
                overlap_duration = overlap_end - overlap_start

                if overlap_duration > 0:
                    phase_power += comp.power_w * (overlap_duration / duration)

            profile.append((current_time, phase_power, phase_name))
            current_time += duration

        return profile

    def get_energy_summary(self) -> Dict[str, float]:
        """Get summary statistics for energy requirements."""

        return {
            "total_energy_j": self.total_energy_j,
            "peak_power_w": self.peak_power_w,
            "average_power_w": self.average_power_w,
            "performance_duration_s": TOTAL_PERFORMANCE_TIME,
            "energy_with_losses_j": self.total_energy_j / OVERALL_EFFICIENCY,
            "required_power_with_losses_w": self.average_power_w / OVERALL_EFFICIENCY,
            "peak_power_with_losses_w": self.peak_power_w / OVERALL_EFFICIENCY
        }

def main():
    """Main function to demonstrate energy budget analysis."""

    print("Leonardo's Mechanical Lion - Energy Budget Analysis")
    print("=" * 60)

    budget = EnergyBudget()

    # Display energy breakdown
    breakdown = budget.get_energy_breakdown()
    print("\nEnergy Breakdown by Component:")
    print("-" * 40)
    for name, data in breakdown.items():
        print(f"{name:20s}: {data['energy_j']:8.1f} J "
              f"({data['percentage']:5.1f}%)")

    # Display summary
    summary = budget.get_energy_summary()
    print(f"\nEnergy Summary:")
    print(f"Total Performance Time: {summary['performance_duration_s']:.1f} seconds")
    print(f"Total Energy Required: {summary['total_energy_j']:.1f} J")
    print(f"Average Power: {summary['average_power_w']:.1f} W")
    print(f"Peak Power: {summary['peak_power_w']:.1f} W")
    print(f"Energy with Losses: {summary['energy_with_losses_j']:.1f} J")
    print(f"Required Power with Losses: {summary['required_power_with_losses_w']:.1f} W")

    # Display phase power profile
    print(f"\nPower Profile by Performance Phase:")
    print("-" * 40)
    profile = budget.get_phase_power_profile()
    for time, power, phase in profile:
        print(f"{phase:20s}: {power:8.1f} W")

    return budget

if __name__ == "__main__":
    budget = main()