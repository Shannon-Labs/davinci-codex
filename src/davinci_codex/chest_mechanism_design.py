"""
Chest Mechanism Design for Leonardo's Mechanical Lion
Complete compound hinge system with spring-powered deployment
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

import matplotlib.pyplot as plt

# Physical constants
GRAVITY_M_S2 = 9.81
BRONZE_DENSITY_KG_M3 = 8700
OAK_DENSITY_KG_M3 = 750

@dataclass
class ChestPanel:
    """Individual chest panel with precise mechanical properties."""
    panel_id: int
    width_m: float
    height_m: float
    thickness_m: float = 0.008
    material: str = "bronze"
    mass_kg: float = 0.0
    moment_of_inertia_kg_m2: float = 0.0

    def __post_init__(self):
        """Calculate mass and moment of inertia based on dimensions."""
        volume_m3 = self.width_m * self.height_m * self.thickness_m
        density = BRONZE_DENSITY_KG_M3 if self.material == "bronze" else OAK_DENSITY_KG_M3
        self.mass_kg = volume_m3 * density

        # Moment of inertia for rectangular panel about hinge edge
        self.moment_of_inertia_kg_m2 = (1/3) * self.mass_kg * (self.height_m**2 + self.thickness_m**2)

@dataclass
class HingeSystem:
    """Compound hinge mechanism for smooth panel deployment."""
    hinge_radius_m: float
    pin_diameter_m: float
    material: str = "bronze"
    friction_coefficient: float = 0.15
    max_load_capacity_n: float = 500.0

    def calculate_friction_torque(self, normal_force_n: float) -> float:
        """Calculate friction torque in hinge."""
        return self.friction_coefficient * normal_force_n * self.hinge_radius_m

class ChestCavityMechanism:
    """Complete chest cavity mechanism with compound hinges."""

    def __init__(self):
        # Initialize four chest panels
        self.panels = [
            ChestPanel(0, 0.4, 0.3, material="bronze"),  # Left panel
            ChestPanel(1, 0.4, 0.3, material="bronze"),  # Right panel
            ChestPanel(2, 0.8, 0.15, material="bronze"),  # Top panel
            ChestPanel(3, 0.8, 0.15, material="bronze"),  # Bottom panel
        ]

        # Initialize hinge systems
        self.hinges = [
            HingeSystem(0.015, 0.012),  # Left hinge
            HingeSystem(0.015, 0.012),  # Right hinge
            HingeSystem(0.015, 0.012),  # Top hinge
            HingeSystem(0.015, 0.012),  # Bottom hinge
        ]

        # Panel positions and angles
        self.panel_angles_rad = [0.0] * 4  # Current angles
        self.target_angles_rad = [0.0] * 4  # Target opening angles
        self.angular_velocities_rad_s = [0.0] * 4  # Angular velocities

        # Set target opening angles for dramatic effect
        self.target_angles_rad[0] = math.pi / 3   # Left panel opens 60°
        self.target_angles_rad[1] = math.pi / 3   # Right panel opens 60°
        self.target_angles_rad[2] = math.pi / 4   # Top panel opens 45°
        self.target_angles_rad[3] = math.pi / 4   # Bottom panel opens 45°

        # Spring system for panel deployment
        self.spring_constants_n_m = [150.0] * 4
        self.spring_compressions_m = [0.0] * 4

    def calculate_panel_torque(self, panel_idx: int, angle_rad: float) -> Tuple[float, float]:
        """
        Calculate gravitational torque and spring torque on a panel.

        Returns:
            Tuple of (gravitational_torque, spring_torque)
        """
        panel = self.panels[panel_idx]

        # Gravitational torque (acts to close the panel)
        # Center of mass distance from hinge
        com_distance_m = panel.height_m / 2
        gravitational_torque = panel.mass_kg * GRAVITY_M_S2 * com_distance_m * math.sin(angle_rad)

        # Spring torque (acts to open the panel)
        spring_torque = self.spring_constants_n_m[panel_idx] * self.spring_compressions_m[panel_idx] * com_distance_m

        return gravitational_torque, spring_torque

    def calculate_net_torque(self, panel_idx: int) -> float:
        """Calculate net torque on a panel including friction."""
        angle = self.panel_angles_rad[panel_idx]
        grav_torque, spring_torque = self.calculate_panel_torque(panel_idx, angle)

        # Friction torque opposes motion
        angular_vel = self.angular_velocities_rad_s[panel_idx]
        if abs(angular_vel) > 0.001:
            friction_direction = -math.copysign(1, angular_vel)
            normal_force = math.sqrt(grav_torque**2 + spring_torque**2) / self.hinges[panel_idx].hinge_radius_m
            friction_torque = friction_direction * self.hinges[panel_idx].calculate_friction_torque(normal_force)
        else:
            friction_torque = 0.0

        # Net torque
        net_torque = spring_torque - grav_torque + friction_torque
        return net_torque

    def update_panel_dynamics(self, dt_s: float) -> None:
        """Update panel positions using physics simulation."""
        for i in range(4):
            # Calculate net torque
            net_torque = self.calculate_net_torque(i)

            # Angular acceleration = torque / moment of inertia
            angular_acceleration = net_torque / self.panels[i].moment_of_inertia_kg_m2

            # Update angular velocity and position
            self.angular_velocities_rad_s[i] += angular_acceleration * dt_s
            self.panel_angles_rad[i] += self.angular_velocities_rad_s[i] * dt_s

            # Apply limits
            self.panel_angles_rad[i] = max(0.0, min(self.panel_angles_rad[i], self.target_angles_rad[i]))

            # Apply damping for smooth motion
            damping_coefficient = 0.1
            self.angular_velocities_rad_s[i] *= (1.0 - damping_coefficient * dt_s)

    def calculate_chest_aperture(self) -> float:
        """Calculate current chest aperture as percentage of maximum."""
        total_opening = sum(self.panel_angles_rad)
        max_opening = sum(self.target_angles_rad)
        return total_opening / max_opening if max_opening > 0 else 0.0

    def deploy_chest(self, deployment_progress: float) -> None:
        """Control chest deployment with specified progress (0.0 to 1.0)."""
        deployment_progress = max(0.0, min(1.0, deployment_progress))

        for i in range(4):
            # Set spring compression based on deployment progress
            max_compression = 0.1  # Maximum spring compression in meters
            self.spring_compressions_m[i] = max_compression * deployment_progress

    def reset_chest(self, reset_progress: float) -> None:
        """Reset chest to closed position with specified progress (0.0 to 1.0)."""
        reset_progress = max(0.0, min(1.0, reset_progress))

        for i in range(4):
            # Reduce spring compression
            max_compression = 0.1
            self.spring_compressions_m[i] = max_compression * (1.0 - reset_progress)

            # Apply gentle closing torque
            closing_torque = 5.0 * reset_progress  # N·m
            if self.panel_angles_rad[i] > 0:
                self.angular_velocities_rad_s[i] -= closing_torque / self.panels[i].moment_of_inertia_kg_m2 * 0.1

    def get_mechanical_stress(self) -> dict:
        """Calculate mechanical stress on components."""
        max_torque = 0.0
        max_spring_force = 0.0
        max_hinge_load = 0.0

        for i in range(4):
            torque = abs(self.calculate_net_torque(i))
            max_torque = max(max_torque, torque)

            spring_force = self.spring_constants_n_m[i] * self.spring_compressions_m[i]
            max_spring_force = max(max_spring_force, spring_force)

            hinge_load = math.sqrt(
                self.calculate_panel_torque(i, self.panel_angles_rad[i])[0]**2 +
                spring_force**2
            )
            max_hinge_load = max(max_hinge_load, hinge_load)

        return {
            "max_panel_torque_nm": max_torque,
            "max_spring_force_n": max_spring_force,
            "max_hinge_load_n": max_hinge_load,
            "total_system_mass_kg": sum(panel.mass_kg for panel in self.panels),
        }

def visualize_chest_mechanism():
    """Generate visualization of chest mechanism operation."""
    mechanism = ChestCavityMechanism()

    # Simulate deployment sequence
    time_steps = 200
    dt_s = 0.02
    time_array = []
    aperture_array = []
    torque_array = []
    spring_force_array = []

    for step in range(time_steps):
        time_s = step * dt_s
        time_array.append(time_s)

        if time_s < 3.5:  # Opening phase
            progress = time_s / 3.5
            mechanism.deploy_chest(progress)
        elif time_s < 11.5:  # Display phase
            progress = 1.0
            mechanism.deploy_chest(progress)
        else:  # Reset phase
            progress = (time_s - 11.5) / 10.0
            mechanism.reset_chest(progress)

        # Update physics
        mechanism.update_panel_dynamics(dt_s)

        # Record data
        aperture_array.append(mechanism.calculate_chest_aperture())
        stress = mechanism.get_mechanical_stress()
        torque_array.append(stress["max_panel_torque_nm"])
        spring_force_array.append(stress["max_spring_force_n"])

    # Create visualization
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    fig.suptitle("Chest Cavity Mechanism Performance Analysis", fontsize=16, fontweight='bold')

    # Plot 1: Chest aperture over time
    ax1.plot(time_array, aperture_array, 'b-', linewidth=2.5, label='Chest Aperture')
    ax1.set_ylabel('Aperture (normalized)', fontsize=12)
    ax1.set_title('Chest Opening Sequence', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1.1)
    ax1.legend(loc='upper right')

    # Add phase markers
    ax1.axvline(x=3.5, color='gray', linestyle='--', alpha=0.5, label='Opening Complete')
    ax1.axvline(x=11.5, color='gray', linestyle='--', alpha=0.5, label='Reset Start')

    # Plot 2: Torque requirements
    ax2.plot(time_array, torque_array, 'r-', linewidth=2.5, label='Panel Torque')
    ax2.set_ylabel('Torque (N·m)', fontsize=12)
    ax2.set_title('Mechanical Torque Requirements', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper right')

    # Plot 3: Spring force profile
    ax3.plot(time_array, spring_force_array, 'g-', linewidth=2.5, label='Spring Force')
    ax3.set_xlabel('Time (s)', fontsize=12)
    ax3.set_ylabel('Force (N)', fontsize=12)
    ax3.set_title('Spring Force Profile', fontsize=14)
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='upper right')

    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Generate visualization
    fig = visualize_chest_mechanism()
    plt.show()
