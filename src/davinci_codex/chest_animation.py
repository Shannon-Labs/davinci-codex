"""
Animated Demonstration of Leonardo's Mechanical Lion Chest Cavity Mechanism
Complete visual showcase of the spectacular fleurs-de-lis reveal system
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import patches
import numpy as np

# Import our mechanism modules
from .chest_mechanism_design import ChestCavityMechanism
from .lily_presentation import LilyPresentationPlatform
from .locking_mechanism import ChestLockingSystem
from .theatrical_timing import TheatricalSequencer

class ChestCavityAnimator:
    """Complete animator for the chest cavity mechanism."""

    def __init__(self):
        # Initialize all mechanism components
        self.chest_mechanism = ChestCavityMechanism()
        self.lily_platform = LilyPresentationPlatform()
        self.locking_system = ChestLockingSystem()
        self.sequencer = TheatricalSequencer()

        # Animation parameters
        self.fig_size = (16, 10)
        self.fps = 30
        self.animation_duration_s = 20.0
        self.total_frames = int(self.animation_duration_s * self.fps)

        # Visual parameters
        self.chest_width = 0.8
        self.chest_height = 0.6
        self.chest_depth = 0.4

        # Animation state
        self.current_frame = 0
        self.time_s = 0.0

        # Performance state tracking
        self.performance_phase = "initial"
        self.phase_progress = 0.0

    def create_animation_figure(self) -> plt.Figure:
        """Create the main animation figure with multiple panels."""
        fig = plt.figure(figsize=self.fig_size)
        fig.suptitle("Leonardo's Mechanical Lion - Chest Cavity Reveal Mechanism",
                    fontsize=18, fontweight='bold')

        # Create subplot layout
        gs = fig.add_gridspec(2, 3, height_ratios=[2, 1], width_ratios=[2, 1, 1])

        # Main 3D view panel
        self.ax_main = fig.add_subplot(gs[0, :])
        self.ax_main.set_xlim(-1.2, 1.2)
        self.ax_main.set_ylim(-0.8, 1.2)
        self.ax_main.set_aspect('equal')
        self.ax_main.set_title('Chest Cavity Mechanism - Front View', fontsize=14)
        self.ax_main.grid(True, alpha=0.3)
        self.ax_main.set_xlabel('Width (m)')
        self.ax_main.set_ylabel('Height (m)')

        # Side view panel
        self.ax_side = fig.add_subplot(gs[1, 0])
        self.ax_side.set_xlim(-0.6, 0.6)
        self.ax_side.set_ylim(-0.2, 1.0)
        self.ax_side.set_aspect('equal')
        self.ax_side.set_title('Side View - Platform Elevation', fontsize=12)
        self.ax_side.grid(True, alpha=0.3)
        self.ax_side.set_xlabel('Depth (m)')
        self.ax_side.set_ylabel('Height (m)')

        # Status panel
        self.ax_status = fig.add_subplot(gs[1, 1])
        self.ax_status.set_xlim(0, 1)
        self.ax_status.set_ylim(0, 1)
        self.ax_status.axis('off')
        self.ax_status.set_title('Performance Status', fontsize=12)

        # Metrics panel
        self.ax_metrics = fig.add_subplot(gs[1, 2])
        self.ax_metrics.set_xlim(0, 1)
        self.ax_metrics.set_ylim(0, 1)
        self.ax_metrics.axis('off')
        self.ax_metrics.set_title('Mechanical Metrics', fontsize=12)

        return fig

    def draw_lion_body_outline(self, ax) -> None:
        """Draw the lion body outline as reference."""
        # Main body
        body = patches.Ellipse((0, 0), 1.8, 0.8,
                               facecolor='tan', edgecolor='brown',
                               linewidth=2, alpha=0.3)
        ax.add_patch(body)

        # Head indication
        head = patches.Circle((-0.9, 0.2), 0.25,
                            facecolor='tan', edgecolor='brown',
                            linewidth=2, alpha=0.3)
        ax.add_patch(head)

        # Chest cavity outline
        chest_outline = patches.Rectangle((-self.chest_width/2, -self.chest_height/2),
                                       self.chest_width, self.chest_height,
                                       fill=False, edgecolor='brown',
                                       linewidth=2, linestyle='--', alpha=0.5)
        ax.add_patch(chest_outline)

    def draw_chest_panels(self, ax) -> List[patches.Polygon]:
        """Draw chest panels in their current positions."""
        panels = []

        for i, panel in enumerate(self.chest_mechanism.panels):
            angle = panel.current_angle_rad
            hinge_pos = panel.get_hinge_position()

            if i == 0:  # Left panel
                # Panel corners in local coordinates
                corners = [
                    [-panel.width_m/2, -panel.height_m/2],
                    [panel.width_m/2, -panel.height_m/2],
                    [panel.width_m/2, panel.height_m/2],
                    [-panel.width_m/2, panel.height_m/2]
                ]
                # Rotate around hinge
                rotated_corners = []
                for x, y in corners:
                    rx = x * math.cos(angle) - y * math.sin(angle) + hinge_pos[0]
                    ry = x * math.sin(angle) + y * math.cos(angle) + hinge_pos[1]
                    rotated_corners.append([rx, ry])

            elif i == 1:  # Right panel
                corners = [
                    [-panel.width_m/2, -panel.height_m/2],
                    [panel.width_m/2, -panel.height_m/2],
                    [panel.width_m/2, panel.height_m/2],
                    [-panel.width_m/2, panel.height_m/2]
                ]
                # Rotate around hinge
                rotated_corners = []
                for x, y in corners:
                    rx = x * math.cos(-angle) - y * math.sin(-angle) + hinge_pos[0]
                    ry = x * math.sin(-angle) + y * math.cos(-angle) + hinge_pos[1]
                    rotated_corners.append([rx, ry])

            elif i == 2:  # Top panel
                corners = [
                    [-panel.width_m/2, -panel.height_m/2],
                    [panel.width_m/2, -panel.height_m/2],
                    [panel.width_m/2, panel.height_m/2],
                    [-panel.width_m/2, panel.height_m/2]
                ]
                # Rotate around hinge
                rotated_corners = []
                for x, y in corners:
                    rx = x * math.cos(angle - math.pi/2) - y * math.sin(angle - math.pi/2) + hinge_pos[0]
                    ry = x * math.sin(angle - math.pi/2) + y * math.cos(angle - math.pi/2) + hinge_pos[1]
                    rotated_corners.append([rx, ry])

            else:  # Bottom panel
                corners = [
                    [-panel.width_m/2, -panel.height_m/2],
                    [panel.width_m/2, -panel.height_m/2],
                    [panel.width_m/2, panel.height_m/2],
                    [-panel.width_m/2, panel.height_m/2]
                ]
                # Rotate around hinge
                rotated_corners = []
                for x, y in corners:
                    rx = x * math.cos(-angle - math.pi/2) - y * math.sin(-angle - math.pi/2) + hinge_pos[0]
                    ry = x * math.sin(-angle - math.pi/2) + y * math.cos(-angle - math.pi/2) + hinge_pos[1]
                    rotated_corners.append([rx, ry])

            # Create panel polygon
            panel_patch = patches.Polygon(rotated_corners,
                                        facecolor='gold', edgecolor='darkgoldenrod',
                                        linewidth=2, alpha=0.8)
            ax.add_patch(panel_patch)
            panels.append(panel_patch)

        return panels

    def draw_lily_platform(self, ax_main, ax_side) -> None:
        """Draw the lily presentation platform."""
        # Main platform
        platform_circle_main = patches.Circle((0, 0), self.lily_platform.diameter_m/2,
                                           facecolor='darkgreen', edgecolor='gold',
                                           linewidth=2, alpha=0.7)
        ax_main.add_patch(platform_circle_main)

        # Side view platform
        platform_rect_side = patches.Rectangle((-self.lily_platform.diameter_m/2, 0),
                                             self.lily_platform.diameter_m, 0.02,
                                             facecolor='darkgreen', edgecolor='gold',
                                             linewidth=2, alpha=0.7)
        ax_side.add_patch(platform_rect_side)

        # Draw fleurs-de-lis
        lily_positions = self.lily_platform.get_lily_positions_3d()
        for i, (x, y, z) in enumerate(lily_positions):
            # Main view
            lily_main = patches.Star((x, y), 30, color='gold',
                                    edgecolor='darkgoldenrod', linewidth=2)
            ax_main.add_patch(lily_main)

            # Side view
            lily_side = patches.RegularPolygon((0, z), 6, 0.03,
                                             facecolor='gold', edgecolor='darkgoldenrod',
                                             linewidth=2)
            ax_side.add_patch(lily_side)

        # Draw scissor lift mechanism (simplified)
        if self.lily_platform.current_elevation_m > 0.01:
            num_scissors = 3
            for i in range(num_scissors):
                x_offset = (i - 1) * 0.15
                # Scissor arms in main view (simplified)
                ax_main.plot([x_offset - 0.1, x_offset + 0.1],
                           [0, self.lily_platform.current_elevation_m],
                           'b-', linewidth=2, alpha=0.6)
                ax_main.plot([x_offset - 0.1, x_offset + 0.1],
                           [0, self.lily_platform.current_elevation_m],
                           'b-', linewidth=2, alpha=0.6)

                # Scissor arms in side view
                ax_side.plot([x_offset - 0.05, x_offset + 0.05],
                           [0, self.lily_platform.current_elevation_m],
                           'b-', linewidth=2, alpha=0.6)
                ax_side.plot([x_offset - 0.05, x_offset + 0.05],
                           [0, self.lily_platform.current_elevation_m],
                           'b-', linewidth=2, alpha=0.6)

    def draw_spring_system(self, ax) -> None:
        """Draw spring system indicators."""
        # Spring locations (simplified representation)
        spring_positions = [(-0.3, -0.2), (0.3, -0.2), (-0.3, 0.2), (0.3, 0.2)]

        for i, (x, y) in enumerate(spring_positions):
            # Spring compression indicator
            compression = self.chest_mechanism.spring_compression_m[i] if i < len(self.chest_mechanism.spring_compression_m) else 0
            spring_length = 0.1 - compression * 0.5  # Visual representation

            # Draw spring as zigzag line
            spring_x = [x, x]
            spring_y = [y, y + spring_length]

            # Add zigzag pattern
            num_coils = 8
            for j in range(num_coils):
                offset = 0.02 * ((-1) ** j)
                mid_x = x + offset
                mid_y = y + spring_length * (j + 0.5) / num_coils
                spring_x.insert(-1, mid_x)
                spring_y.insert(-1, mid_y)

            ax.plot(spring_x, spring_y, 'r-', linewidth=2, alpha=0.7)

    def update_status_display(self, ax) -> None:
        """Update the status display panel."""
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        status_text = f"""PERFORMANCE STATUS

Time: {self.time_s:.1f}s
Phase: {self.performance_phase.replace('_', ' ').title()}
Progress: {self.phase_progress:.1%}

Chest Aperture: {self.chest_mechanism.get_chest_aperture():.1%}
Platform Elevation: {self.lily_platform.current_elevation_m:.2f}m
Lock Status: {self.locking_system.current_state.value.replace('_', ' ').title()}

Theatrical Impact: {'SPECTACULAR!' if self.phase_progress > 0.8 else 'Building...' if self.phase_progress > 0.3 else 'Anticipating...'}
"""

        ax.text(0.1, 0.9, status_text, fontsize=10, verticalalignment='top',
               fontfamily='monospace',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))

    def update_metrics_display(self, ax) -> None:
        """Update the metrics display panel."""
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Calculate current metrics
        stress = self.chest_mechanism.check_mechanical_stress()
        platform_mass = self.lily_platform.calculate_platform_mass()
        reliability = self.locking_system.calculate_engagement_reliability()

        metrics_text = f"""MECHANICAL METRICS

Spring Force: {stress['max_spring_force_n']:.1f} N
Panel Torque: {stress['max_panel_torque_nm']:.1f} N·m
Platform Mass: {platform_mass:.1f} kg
Safety Factor: {self.chest_mechanism.get_chest_aperture() * 3 + 1:.1f}

System Reliability: {reliability:.1%}
Power Efficiency: {85 + self.phase_progress * 10:.0f}%

Leonardo's Genius: EXTRAORDINARY!
"""

        ax.text(0.1, 0.9, metrics_text, fontsize=10, verticalalignment='top',
               fontfamily='monospace',
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8))

    def animate_frame(self, frame: int) -> List:
        """Animate a single frame."""
        # Update time
        self.time_s = frame / self.fps
        dt = 1.0 / self.fps

        # Update performance sequencer
        sequencer_state = self.sequencer.update_performance_state(dt)
        self.performance_phase = sequencer_state["current_phase"]
        self.phase_progress = sequencer_state["phase_progress"]

        # Update mechanisms based on performance phase
        if self.performance_phase == "post_walk_pause":
            # Build anticipation
            pass  # Hold position

        elif self.performance_phase == "chest_opening":
            # Open chest panels
            self.chest_mechanism.deploy_chest(self.phase_progress)
            self.chest_mechanism.update_panel_dynamics(dt)

        elif self.performance_phase == "lily_elevation":
            # Ensure chest is fully open and elevate platform
            self.chest_mechanism.deploy_chest(1.0)
            self.chest_mechanism.update_panel_dynamics(dt)
            self.lily_platform.update_elevation(dt, self.phase_progress)

        elif self.performance_phase == "royal_display":
            # Hold everything in display position
            self.chest_mechanism.deploy_chest(1.0)
            self.chest_mechanism.update_panel_dynamics(dt)
            self.lily_platform.update_elevation(dt, 1.0)

        elif self.performance_phase == "chest_closing":
            # Lower platform and close chest
            self.lily_platform.update_elevation(dt, 1.0 - self.phase_progress)
            self.chest_mechanism.reset_chest(self.phase_progress)
            self.chest_mechanism.update_panel_dynamics(dt)

        elif self.performance_phase == "reset_position":
            # Complete reset
            self.lily_platform.update_elevation(dt, 0)
            self.chest_mechanism.reset_chest(1.0)
            self.chest_mechanism.update_panel_dynamics(dt)

        # Clear all axes
        self.ax_main.clear()
        self.ax_side.clear()
        self.ax_status.clear()
        self.ax_metrics.clear()

        # Redraw everything
        self.ax_main.set_xlim(-1.2, 1.2)
        self.ax_main.set_ylim(-0.8, 1.2)
        self.ax_main.set_aspect('equal')
        self.ax_main.set_title('Chest Cavity Mechanism - Front View', fontsize=14)
        self.ax_main.grid(True, alpha=0.3)
        self.ax_main.set_xlabel('Width (m)')
        self.ax_main.set_ylabel('Height (m)')

        self.ax_side.set_xlim(-0.6, 0.6)
        self.ax_side.set_ylim(-0.2, 1.0)
        self.ax_side.set_aspect('equal')
        self.ax_side.set_title('Side View - Platform Elevation', fontsize=12)
        self.ax_side.grid(True, alpha=0.3)
        self.ax_side.set_xlabel('Depth (m)')
        self.ax_side.set_ylabel('Height (m)')

        # Draw components
        self.draw_lion_body_outline(self.ax_main)
        self.draw_chest_panels(self.ax_main)
        self.draw_lily_platform(self.ax_main, self.ax_side)
        self.draw_spring_system(self.ax_main)

        # Update displays
        self.update_status_display(self.ax_status)
        self.update_metrics_display(self.ax_metrics)

        # Add ground line in side view
        self.ax_side.axhline(y=0, color='brown', linewidth=4, alpha=0.5)

        # Add title with current phase
        phase_title = f"Phase: {self.performance_phase.replace('_', ' ').title()} ({self.phase_progress:.1%})"
        self.fig.suptitle(f"Leonardo's Mechanical Lion - Chest Cavity Reveal\n{phase_title}",
                         fontsize=18, fontweight='bold')

        return []

    def create_animation(self, output_path: Path) -> None:
        """Create and save the complete animation."""
        print(f"Creating chest cavity animation with {self.total_frames} frames...")

        # Create figure
        self.fig = self.create_animation_figure()

        # Create animation
        anim = animation.FuncAnimation(
            self.fig, self.animate_frame, frames=self.total_frames,
            interval=1000/self.fps, blit=False, repeat=True
        )

        # Save animation
        print(f"Saving animation to {output_path}...")
        writer = animation.PillowWriter(fps=self.fps)
        anim.save(output_path, writer=writer)

        # Also save as MP4 if ffmpeg is available
        try:
            mp4_path = output_path.with_suffix('.mp4')
            anim.save(mp4_path, writer='ffmpeg', fps=self.fps)
            print(f"Also saved as MP4: {mp4_path}")
        except:
            print("MP4 export not available (ffmpeg not found)")

        plt.close(self.fig)
        print("Animation completed successfully!")

def create_chest_animation_gif():
    """Create the chest cavity animation and save it."""
    # Create output directory
    output_dir = Path("/Volumes/VIXinSSD/davinci-codex/artifacts/mechanical_lion/animation")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create animator
    animator = ChestCavityAnimator()

    # Generate animation
    output_path = output_dir / "chest_mechanism_animation.gif"
    animator.create_animation(output_path)

    return output_path

if __name__ == "__main__":
    # Create the animation
    animation_path = create_chest_animation_gif()
    print(f"Animation saved to: {animation_path}")