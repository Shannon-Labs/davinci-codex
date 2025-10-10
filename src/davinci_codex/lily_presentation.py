"""
Lily Presentation Platform for Leonardo's Mechanical Lion
Spectacular rising platform revealing fleurs-de-lis for King Francis I
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

# French royal symbolism
FLEUR_DE_LIS_SYMBOLISM = {
    "meaning": "French royal symbol of sovereignty and honor",
    "historical_significance": "Gift to celebrate Franco-Florentine alliance",
    "leonardo_interpretation": "Mechanical poetry representing unity of Florence and France",
}

@dataclass
class FleurDeLis:
    """Individual fleur-de-lis decorative element."""
    id: int
    height_mm: float = 120.0
    width_mm: float = 80.0
    material: str = "gilded bronze"
    weight_kg: float = 0.15
    mounting_type: str = "screw_socket"
    gem_decorations: int = 3  # Small gems for royal sparkle

@dataclass
class ScissorLiftArm:
    """Individual scissor lift arm for platform elevation."""
    length_m: float
    width_m: float = 0.03
    thickness_m: float = 0.008
    material: str = "bronze"
    joint_radius_m: float = 0.008

    def calculate_arm_mass(self) -> float:
        """Calculate mass of scissor lift arm."""
        volume_m3 = self.length_m * self.width_m * self.thickness_m
        density = 8700 if self.material == "bronze" else 750
        return volume_m3 * density

class LilyPresentationPlatform:
    """Rising platform system for dramatic lily presentation."""

    def __init__(self):
        # Platform dimensions
        self.diameter_m = 0.56  # Platform diameter (70% of chest width)
        self.thickness_m = 0.02  # Platform thickness
        self.max_elevation_m = 0.32  # Maximum elevation (80% of chest depth)

        # Current state
        self.current_elevation_m = 0.0
        self.target_elevation_m = 0.0
        self.elevation_velocity_m_s = 0.0

        # Scissor lift mechanism
        self.num_scissor_pairs = 3
        self.scissor_arms = []
        for i in range(self.num_scissor_pairs):
            arm_length = self.max_elevation_m / (2 * math.sin(math.pi/6))  # 30° angle
            self.scissor_arms.append(ScissorLiftArm(arm_length))

        # Fleurs-de-lis arrangement
        self.fleurs_de_lis = []
        self.arrange_lilies()

        # Drive mechanism
        self.drive_gear_ratio = 4.0
        self.cam_lift_profile = "modified_sinusoidal"
        self.spring_assistance_force_n = 80.0

        # Performance timing
        self.elevation_duration_s = 2.0
        self.display_duration_s = 8.0
        self.lowering_duration_s = 3.0

    def arrange_lilies(self) -> None:
        """Arrange fleurs-de-lis in symbolic pattern on platform."""
        # Central fleur-de-lis (largest, most important)
        self.fleurs_de_lis.append(FleurDeLis(0, height_mm=150.0, width_mm=100.0))

        # Surrounding fleurs-de-lis in trinity pattern
        radius = self.diameter_m * 0.3
        for i in range(3):
            angle = 2 * math.pi * i / 3 - math.pi/2  # Start from top
            lily = FleurDeLis(i + 1)
            lily.angle_rad = angle
            lily.radius_m = radius
            self.fleurs_de_lis.append(lily)

    def calculate_platform_mass(self) -> float:
        """Calculate total mass of platform and decorations."""
        # Platform mass
        platform_volume = math.pi * (self.diameter_m/2)**2 * self.thickness_m
        platform_mass = platform_volume * 750  # Oak density

        # Scissor lift mass
        scissor_mass = sum(arm.calculate_arm_mass() for arm in self.scissor_arms)

        # Fleurs-de-lis mass
        lilies_mass = sum(lily.weight_kg for lily in self.fleurs_de_lis)

        return platform_mass + scissor_mass + lilies_mass

    def calculate_required_force(self, elevation_m: float) -> float:
        """Calculate force required to maintain platform at given elevation."""
        total_mass = self.calculate_platform_mass()
        gravitational_force = total_mass * 9.81

        # Scissor lift mechanical advantage decreases with elevation
        angle = math.asin(elevation_m / (2 * self.scissor_arms[0].length_m))
        mechanical_advantage = 1 / (2 * math.tan(angle)) if angle > 0.01 else 100.0

        required_force = gravitational_force / mechanical_advantage
        return required_force - self.spring_assistance_force_n  # Subtract spring assistance

    def calculate_cam_profile(self, angle_rad: float) -> float:
        """
        Calculate cam lift profile for smooth platform elevation.

        Uses modified sinusoidal profile for gentle acceleration/deceleration.
        """
        # Base sinusoidal lift
        base_lift = (1 - math.cos(angle_rad)) / 2

        # Add smoothing curves for theatrical effect
        smoothing = math.sin(angle_rad * 3) * 0.05 * math.sin(angle_rad)

        lift_factor = base_lift + smoothing
        return max(0.0, min(1.0, lift_factor))

    def update_elevation(self, dt_s: float, target_progress: float) -> None:
        """Update platform elevation with smooth motion control."""
        # Calculate target elevation based on progress
        self.target_elevation_m = self.max_elevation_m * target_progress

        # Calculate required force
        required_force = self.calculate_required_force(self.current_elevation_m)

        # Spring-assisted elevation dynamics
        spring_force = self.spring_assistance_force_n * target_progress
        net_force = spring_force - required_force

        # Update velocity and position
        total_mass = self.calculate_platform_mass()
        acceleration = net_force / total_mass

        self.elevation_velocity_m_s += acceleration * dt_s

        # Apply damping for smooth motion
        damping_coefficient = 0.2
        self.elevation_velocity_m_s *= (1.0 - damping_coefficient * dt_s)

        # Update elevation
        self.current_elevation_m += self.elevation_velocity_m_s * dt_s

        # Apply limits
        self.current_elevation_m = max(0.0, min(self.current_elevation_m, self.max_elevation_m))

    def get_lily_positions_3d(self) -> List[Tuple[float, float, float]]:
        """Get 3D positions of all fleurs-de-lis at current elevation."""
        positions = []

        for lily in self.fleurs_de_lis:
            if lily.id == 0:  # Central lily
                x, y = 0.0, 0.0
            else:  # Surrounding lilies
                x = lily.radius_m * math.cos(lily.angle_rad)
                y = lily.radius_m * math.sin(lily.angle_rad)

            z = self.current_elevation_m + (lily.height_mm / 1000)  # Height above platform
            positions.append((x, y, z))

        return positions

    def calculate_theatrical_impact(self) -> dict:
        """Calculate theatrical impact metrics for royal performance."""
        elevation_ratio = self.current_elevation_m / self.max_elevation_m if self.max_elevation_m > 0 else 0.0

        # Visibility impact (based on elevation and number of lilies)
        visibility_score = elevation_ratio * len(self.fleurs_de_lis) / 4.0

        # Royal symbolism impact
        symbolism_score = 1.0  # Maximum for fleurs-de-lis

        # Mechanical elegance score
        smoothness_score = 1.0 - abs(self.elevation_velocity_m_s) / 0.5  # Penalty for fast motion
        smoothness_score = max(0.0, smoothness_score)

        overall_impact = (visibility_score * 0.4 + symbolism_score * 0.4 + smoothness_score * 0.2)

        return {
            "visibility_score": visibility_score,
            "symbolism_score": symbolism_score,
            "smoothness_score": smoothness_score,
            "overall_theatrical_impact": overall_impact,
            "royal_appeal": "High - fleurs-de-lis symbolize Franco-Florentine alliance",
        }

def simulate_lily_presentation():
    """Simulate complete lily presentation sequence."""
    platform = LilyPresentationPlatform()

    # Timing parameters
    total_time = 16.0  # Total performance time
    dt = 0.05  # Time step
    steps = int(total_time / dt)

    # Data storage
    time_array = []
    elevation_array = []
    velocity_array = []
    force_array = []
    impact_array = []

    # Simulation phases
    pause_duration = 2.5
    elevation_duration = platform.elevation_duration_s
    display_duration = platform.display_duration_s
    lowering_duration = platform.lowering_duration_s

    for step in range(steps):
        t = step * dt
        time_array.append(t)

        # Determine phase and target progress
        if t < pause_duration:
            target_progress = 0.0
            phase = "pause"
        elif t < pause_duration + elevation_duration:
            progress = (t - pause_duration) / elevation_duration
            target_progress = platform.calculate_cam_profile(progress * math.pi)
            phase = "rising"
        elif t < pause_duration + elevation_duration + display_duration:
            target_progress = 1.0
            phase = "display"
        elif t < pause_duration + elevation_duration + display_duration + lowering_duration:
            progress = (t - pause_duration - elevation_duration - display_duration) / lowering_duration
            target_progress = 1.0 - progress
            phase = "lowering"
        else:
            target_progress = 0.0
            phase = "reset"

        # Update platform
        platform.update_elevation(dt, target_progress)

        # Record data
        elevation_array.append(platform.current_elevation_m)
        velocity_array.append(platform.elevation_velocity_m_s)
        force_array.append(platform.calculate_required_force(platform.current_elevation_m))
        impact_data = platform.calculate_theatrical_impact()
        impact_array.append(impact_data["overall_theatrical_impact"])

    return {
        "time_s": time_array,
        "elevation_m": elevation_array,
        "velocity_m_s": velocity_array,
        "required_force_n": force_array,
        "theatrical_impact": impact_array,
        "platform": platform,
    }

def visualize_lily_presentation():
    """Create comprehensive visualization of lily presentation."""
    sim_data = simulate_lily_presentation()
    platform = sim_data["platform"]

    # Create multi-panel figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Lily Presentation Platform - Spectacular Royal Reveal", fontsize=16, fontweight='bold')

    # Plot 1: Platform elevation over time
    axes[0, 0].plot(sim_data["time_s"], sim_data["elevation_m"], 'g-', linewidth=3, label='Platform Elevation')
    axes[0, 0].set_ylabel('Elevation (m)', fontsize=12)
    axes[0, 0].set_title('Lily Platform Elevation Sequence', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_ylim(0, platform.max_elevation_m * 1.1)
    axes[0, 0].legend(loc='upper right')

    # Add phase markers
    phase_markers = [2.5, 4.5, 12.5, 15.5]
    phase_labels = ['Rise', 'Display', 'Lower', 'Reset']
    for i, (marker, label) in enumerate(zip(phase_markers, phase_labels)):
        axes[0, 0].axvline(x=marker, color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].text(marker, platform.max_elevation_m * 0.9, label,
                       ha='center', fontsize=10, alpha=0.7)

    # Plot 2: Elevation velocity profile
    axes[0, 1].plot(sim_data["time_s"], sim_data["velocity_m_s"], 'b-', linewidth=2.5, label='Elevation Velocity')
    axes[0, 1].set_ylabel('Velocity (m/s)', fontsize=12)
    axes[0, 1].set_title('Smooth Motion Profile', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend(loc='upper right')

    # Plot 3: Force requirements
    axes[1, 0].plot(sim_data["time_s"], sim_data["required_force_n"], 'r-', linewidth=2.5, label='Required Force')
    axes[1, 0].set_xlabel('Time (s)', fontsize=12)
    axes[1, 0].set_ylabel('Force (N)', fontsize=12)
    axes[1, 0].set_title('Mechanical Force Requirements', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend(loc='upper right')

    # Plot 4: Theatrical impact
    axes[1, 1].plot(sim_data["time_s"], sim_data["theatrical_impact"], 'm-', linewidth=3, label='Theatrical Impact')
    axes[1, 1].set_xlabel('Time (s)', fontsize=12)
    axes[1, 1].set_ylabel('Impact Score', fontsize=12)
    axes[1, 1].set_title('Royal Court Performance Impact', fontsize=14)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_ylim(0, 1.1)
    axes[1, 1].legend(loc='upper right')

    plt.tight_layout()
    return fig

def create_lily_arrangement_diagram():
    """Create detailed diagram of lily arrangement on platform."""
    platform = LilyPresentationPlatform()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Fleur-de-Lis Arrangement - Royal Symbolism", fontsize=16, fontweight='bold')

    # Top view of platform
    circle = plt.Circle((0, 0), platform.diameter_m/2, fill=False, edgecolor='brown', linewidth=2)
    ax1.add_patch(circle)

    # Draw lilies
    for lily in platform.fleurs_de_lis:
        if lily.id == 0:
            x, y = 0, 0
            marker_size = 200
            color = 'gold'
        else:
            x = lily.radius_m * math.cos(lily.angle_rad)
            y = lily.radius_m * math.sin(lily.angle_rad)
            marker_size = 150
            color = 'orange'

        ax1.scatter(x, y, s=marker_size, c=color, marker='*',
                   edgecolors='black', linewidth=2, label=f'Fleur-de-lis {lily.id}' if lily.id <= 1 else '')

    ax1.set_xlim(-platform.diameter_m/2 * 1.3, platform.diameter_m/2 * 1.3)
    ax1.set_ylim(-platform.diameter_m/2 * 1.3, platform.diameter_m/2 * 1.3)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X Position (m)')
    ax1.set_ylabel('Y Position (m)')
    ax1.set_title('Platform Top View')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Side view showing elevation
    ax2.add_patch(plt.Rectangle((-platform.diameter_m/2, 0), platform.diameter_m, 0.02,
                                facecolor='brown', edgecolor='black'))

    # Draw scissor lift arms
    for i in range(platform.num_scissor_pairs):
        x_offset = (i - 1) * 0.15
        ax2.plot([x_offset - 0.1, x_offset + 0.1], [0, platform.max_elevation_m],
                'b-', linewidth=2, alpha=0.6)
        ax2.plot([x_offset - 0.1, x_offset + 0.1], [0, platform.max_elevation_m],
                'b-', linewidth=2, alpha=0.6)

    # Draw elevated platform
    ax2.add_patch(plt.Rectangle((-platform.diameter_m/2, platform.max_elevation_m),
                                platform.diameter_m, 0.02,
                                facecolor='brown', edgecolor='black', alpha=0.7))

    # Draw lilies at elevated positions
    for lily in platform.fleurs_de_lis:
        if lily.id == 0:
            x_pos = 0
        else:
            x_pos = lily.radius_m * math.cos(lily.angle_rad)

        y_pos = platform.max_elevation_m + lily.height_mm / 1000
        ax2.scatter(x_pos, y_pos, s=100, c='gold', marker='*',
                   edgecolors='black', linewidth=2)

    ax2.set_xlim(-platform.diameter_m/2 * 1.3, platform.diameter_m/2 * 1.3)
    ax2.set_ylim(-0.05, platform.max_elevation_m + 0.2)
    ax2.set_xlabel('X Position (m)')
    ax2.set_ylabel('Height (m)')
    ax2.set_title('Platform Side View - Maximum Elevation')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Generate visualizations
    fig1 = visualize_lily_presentation()
    fig2 = create_lily_arrangement_diagram()
    plt.show()