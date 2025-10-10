"""
Leonardo's Mechanical Lion Control System
Complete control sequence programming for theatrical performance

Historical Context:
- Created for 1517 royal court performance for King Francis I
- First programmable automation controller in history
- Cam-based mechanical programming system
- 26.5 seconds of mechanical theater

Engineering Innovation:
- Cam drum programming with machined profiles
- 8-channel control system
- Sequential logic coordination
- Theatrical timing optimization
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class PerformancePhase:
    """Individual phase of the theatrical performance"""
    name: str
    start_time: float
    duration: float
    control_settings: Dict[str, float]
    theatrical_notes: str

@dataclass
class CamProfile:
    """Mathematical cam profile for mechanical actuation"""
    name: str
    radius_function: callable
    angle_range: Tuple[float, float]
    follower_type: str
    max_lift: float
    material: str = "bronze"

class MechanicalLionController:
    """
    Complete control system for Leonardo's Mechanical Lion automaton
    Coordinates walking, tail movement, chest opening, and lily presentation
    """

    def __init__(self):
        # Performance timing specifications
        self.total_performance_time = 26.5  # seconds
        self.cam_drum_radius = 0.15  # meters
        self.cam_rotation_speed = 360 / self.total_performance_time  # degrees per second

        # Control channels (8 total actuators)
        self.control_channels = {
            'front_left_leg': 0,      # Primary walking control
            'front_right_leg': 0,     # Primary walking control
            'rear_left_leg': 0,       # Primary walking control
            'rear_right_leg': 0,      # Primary walking control
            'tail_actuator': 0,       # Tail movement during walking
            'chest_mechanism': 0,     # Chest cavity opening
            'lily_platform': 0,       # Lily presentation platform
            'master_timing': 0        # Overall performance timing
        }

        # Create complete theatrical performance sequence
        self.performance_phases = self._create_performance_sequence()

        # Generate mathematical cam profiles
        self.cam_profiles = self._create_cam_profiles()

        # State tracking
        self.current_time = 0.0
        self.is_performing = False
        self.performance_log = []

    def _create_performance_sequence(self) -> List[PerformancePhase]:
        """Create complete 26.5-second theatrical performance sequence"""
        phases = []

        # PHASE 1: Initial Position - Lion stands majestically at rest
        phases.append(PerformancePhase(
            name="initial_position",
            start_time=0.0,
            duration=2.0,
            control_settings={
                'front_left_leg': 0.0,      # Legs in neutral position
                'front_right_leg': 0.0,
                'rear_left_leg': 0.0,
                'rear_right_leg': 0.0,
                'tail_actuator': 0.1,       # Gentle tail movement
                'chest_mechanism': 0.0,     # Chest firmly closed
                'lily_platform': 0.0,       # Lily platform retracted
                'master_timing': 0.0        # Timing controller ready
            },
            theatrical_notes="Lion appears as magnificent statue, tail gently swaying"
        ))

        # PHASE 2: Prowling Phase - Lion turns in an arc (4 seconds)
        prowl_start_time = 2.0
        for step in range(2): # 2 prowling steps
            step_start = prowl_start_time + step * 2.0

            # Prowling turn - left legs move more
            phases.append(PerformancePhase(
                name=f"prowl_{step+1}_turn",
                start_time=step_start,
                duration=1.0,
                control_settings={
                    'front_left_leg': 1.2 * np.sin(np.pi * (step + 0.5)), # Larger step
                    'front_right_leg': 0.8 * np.sin(np.pi * step),      # Smaller step
                    'rear_left_leg': 1.2 * np.sin(np.pi * step),        # Larger step
                    'rear_right_leg': 0.8 * np.sin(np.pi * (step + 0.5)), # Smaller step
                    'tail_actuator': 0.5 + 0.2 * np.sin(4 * np.pi * (step + 0.25)),
                    'chest_mechanism': 0.0,
                    'lily_platform': 0.0,
                    'master_timing': 1.0
                },
                theatrical_notes=f"Prowl {step+1}: Lion turns with a powerful, deliberate step"
            ))
            # Prowling placement
            phases.append(PerformancePhase(
                name=f"prowl_{step+1}_place",
                start_time=step_start + 1.0,
                duration=1.0,
                control_settings={
                    'front_left_leg': 1.2 * np.sin(np.pi * (step + 1.5)),
                    'front_right_leg': 0.8 * np.sin(np.pi * (step + 1.0)),
                    'rear_left_leg': 1.2 * np.sin(np.pi * (step + 1.0)),
                    'rear_right_leg': 0.8 * np.sin(np.pi * (step + 1.5)),
                    'tail_actuator': 0.5 + 0.2 * np.sin(4 * np.pi * (step + 0.75)),
                    'chest_mechanism': 0.0,
                    'lily_platform': 0.0,
                    'master_timing': 1.0
                },
                theatrical_notes=f"Prowl {step+1}: Lion places paw with authority"
            ))

        # PHASE 3: Walking Phase - 2 graceful steps forward (6 seconds total)
        walk_start_time = 6.0
        for step in range(2):
            step_start = walk_start_time + step * 3.0

            # Step up and forward
            phases.append(PerformancePhase(
                name=f"step_{step+1}_lift",
                start_time=step_start,
                duration=1.0,
                control_settings={
                    'front_left_leg': np.sin(np.pi * (step + 0.5)),
                    'front_right_leg': np.sin(np.pi * step),
                    'rear_left_leg': np.sin(np.pi * step),
                    'rear_right_leg': np.sin(np.pi * (step + 0.5)),
                    'tail_actuator': 0.3 + 0.2 * np.sin(4 * np.pi * (step + 0.25)),
                    'chest_mechanism': 0.0,
                    'lily_platform': 0.0,
                    'master_timing': 1.0
                },
                theatrical_notes=f"Step {step+1}: Lion lifts and moves forward with natural grace"
            ))

            # Step down and placement
            phases.append(PerformancePhase(
                name=f"step_{step+1}_place",
                start_time=step_start + 1.0,
                duration=1.0,
                control_settings={
                    'front_left_leg': np.sin(np.pi * (step + 1.5)),
                    'front_right_leg': np.sin(np.pi * (step + 1.0)),
                    'rear_left_leg': np.sin(np.pi * (step + 1.0)),
                    'rear_right_leg': np.sin(np.pi * (step + 1.5)),
                    'tail_actuator': 0.3 + 0.2 * np.sin(4 * np.pi * (step + 0.75)),
                    'chest_mechanism': 0.0,
                    'lily_platform': 0.0,
                    'master_timing': 1.0
                },
                theatrical_notes=f"Step {step+1}: Lion places paw down majestically"
            ))

            # Brief pause between steps
            phases.append(PerformancePhase(
                name=f"step_{step+1}_pause",
                start_time=step_start + 2.0,
                duration=1.0,
                control_settings={
                    'front_left_leg': 0.0,
                    'front_right_leg': 0.0,
                    'rear_left_leg': 0.0,
                    'rear_right_leg': 0.0,
                    'tail_actuator': 0.4 + 0.1 * np.sin(2 * np.pi * (step + 0.5)),
                    'chest_mechanism': 0.0,
                    'lily_platform': 0.0,
                    'master_timing': 0.5
                },
                theatrical_notes=f"Paws {step+1}: Dramatic pause before next movement"
            ))

        # PHASE 4: Stopping Position - Lion pauses, prepares for reveal
        phases.append(PerformancePhase(
            name="stopping_position",
            start_time=12.0,
            duration=2.0,
            control_settings={
                'front_left_leg': 0.0,
                'front_right_leg': 0.0,
                'rear_left_leg': 0.0,
                'rear_right_leg': 0.0,
                'tail_actuator': 0.2,       # Gentle tail sway
                'chest_mechanism': 0.0,
                'lily_platform': 0.0,
                'master_timing': 0.0
            },
            theatrical_notes="Lion pauses majestically, court holds breath in anticipation"
        ))

        # PHASE 5: Chest Opening - Mechanical chest cavity opens (3.5 seconds)
        phases.append(PerformancePhase(
            name="chest_opening",
            start_time=14.0,
            duration=3.5,
            control_settings={
                'front_left_leg': 0.0,
                'front_right_leg': 0.0,
                'rear_left_leg': 0.0,
                'rear_right_leg': 0.0,
                'tail_actuator': 0.1,       # Tail slows for dramatic effect
                'chest_mechanism': 1.0,     # Chest fully opens
                'lily_platform': 0.0,       # Platform still hidden
                'master_timing': 1.0        # Precise timing control
            },
            theatrical_notes="Chest cavity slowly opens with mechanical precision, court gasps"
        ))

        # PHASE 6: Lily Presentation - Fleur-de-lis emerges from chest
        phases.append(PerformancePhase(
            name="lily_presentation",
            start_time=17.5,
            duration=2.0,
            control_settings={
                'front_left_leg': 0.0,
                'front_right_leg': 0.0,
                'rear_left_leg': 0.0,
                'rear_right_leg': 0.0,
                'tail_actuator': 0.15,
                'chest_mechanism': 1.0,     # Chest remains fully open
                'lily_platform': 1.0,      # Lily platform rises
                'master_timing': 1.0
            },
            theatrical_notes="Royal fleurs-de-lis emerges from chest, court cheers"
        ))

        # PHASE 7: Royal Display - Presentation of symbols (5 seconds)
        phases.append(PerformancePhase(
            name="royal_display",
            start_time=19.5,
            duration=5.0,
            control_settings={
                'front_left_leg': 0.0,
                'front_right_leg': 0.0,
                'rear_left_leg': 0.0,
                'rear_right_leg': 0.0,
                'tail_actuator': 0.2 + 0.1 * np.sin(2 * np.pi * 0.5),  # Gentle sway
                'chest_mechanism': 1.0,     # Chest remains open
                'lily_platform': 1.0,      # Lily platform held high
                'master_timing': 0.5        # Slower timing for display
            },
            theatrical_notes="Royal symbols displayed, King Francis I nods approval"
        ))

        # PHASE 8: Reset Sequence - Return to initial position
        phases.append(PerformancePhase(
            name="reset_sequence",
            start_time=24.5,
            duration=2.0,
            control_settings={
                'front_left_leg': 0.0,
                'front_right_leg': 0.0,
                'rear_left_leg': 0.0,
                'rear_right_leg': 0.0,
                'tail_actuator': 0.1,       # Tail returns to rest
                'chest_mechanism': 0.0,     # Chest closes smoothly
                'lily_platform': 0.0,      # Platform retracts
                'master_timing': 1.0        # Controlled reset timing
            },
            theatrical_notes="Lion smoothly resets to original position, performance complete"
        ))

        return phases

    def _create_cam_profiles(self) -> Dict[str, CamProfile]:
        """Create mathematical cam profiles for all mechanical movements"""
        profiles = {}

        # Walking Gait Cam - Sinusoidal profile for natural leg movement
        def walking_gait_profile(angle: float) -> float:
            """Sinusoidal profile for natural leg movement"""
            base_radius = 0.05  # meters
            lift_height = 0.03  # meters
            return base_radius + lift_height * np.sin(angle)

        profiles['walking_gait'] = CamProfile(
            name="walking_gait",
            radius_function=walking_gait_profile,
            angle_range=(0, 3 * 2 * np.pi),  # 3 complete cycles for 3 steps
            follower_type="roller",
            max_lift=0.03,
            material="bronze"
        )

        # Tail Motion Cam - Gentle wave pattern for realistic tail sway
        def tail_motion_profile(angle: float) -> float:
            """Gentle wave pattern for realistic tail sway"""
            base_radius = 0.04  # meters
            sway_amplitude = 0.02  # meters
            frequency = 2.0  # Double frequency for natural movement
            return base_radius + sway_amplitude * np.sin(frequency * angle)

        profiles['tail_motion'] = CamProfile(
            name="tail_motion",
            radius_function=tail_motion_profile,
            angle_range=(0, 2 * np.pi),
            follower_type="knife_edge",
            max_lift=0.02,
            material="bronze"
        )

        # Chest Opening Cam - Linear ramp with smooth acceleration/deceleration
        def chest_opening_profile(angle: float) -> float:
            """Linear ramp with smooth acceleration/deceleration"""
            base_radius = 0.03  # meters
            max_opening = 0.05  # meters

            # Smooth sigmoid-like transition
            if angle < np.pi:
                # Opening phase - smooth acceleration
                transition = 0.5 * (1 + np.tanh(4 * (angle/np.pi - 0.5)))
            else:
                # Closing phase - smooth deceleration
                transition = 0.5 * (1 + np.tanh(4 * (1.5 - angle/np.pi)))

            return base_radius + max_opening * transition

        profiles['chest_opening'] = CamProfile(
            name="chest_opening",
            radius_function=chest_opening_profile,
            angle_range=(0, 2 * np.pi),
            follower_type="flat_face",
            max_lift=0.05,
            material="hardened bronze"
        )

        # Lily Platform Cam - Controlled elevation with pause timing
        def lily_platform_profile(angle: float) -> float:
            """Controlled elevation with pause timing"""
            base_radius = 0.035  # meters
            presentation_height = 0.04  # meters

            # Step function with smooth transitions
            if angle < np.pi/2:
                # Rising phase
                position = angle / (np.pi/2)
            elif angle < 3*np.pi/2:
                # Hold at top - presentation phase
                position = 1.0
            else:
                # Lowering phase
                position = (2*np.pi - angle) / (np.pi/2)

            return base_radius + presentation_height * position

        profiles['lily_platform'] = CamProfile(
            name="lily_platform",
            radius_function=lily_platform_profile,
            angle_range=(0, 2 * np.pi),
            follower_type="roller",
            max_lift=0.04,
            material="bronze"
        )

        # Master Timing Cam - Sequence coordination and event timing
        def timing_control_profile(angle: float) -> float:
            """Master timing and event sequencing"""
            base_radius = 0.025  # meters
            timing_variations = 0.015  # meters

            # Complex profile for precise timing control
            timing_signal = (np.sin(angle) + 0.3 * np.sin(3*angle) +
                           0.2 * np.sin(5*angle)) / 1.5

            return base_radius + timing_variations * (0.5 + 0.5 * timing_signal)

        profiles['master_timing'] = CamProfile(
            name="master_timing",
            radius_function=timing_control_profile,
            angle_range=(0, 2 * np.pi),
            follower_type="knife_edge",
            max_lift=0.015,
            material="steel"
        )

        return profiles

    def get_active_phase(self, current_time: float) -> Optional[PerformancePhase]:
        """Get the currently active performance phase"""
        for phase in self.performance_phases:
            if phase.start_time <= current_time < phase.start_time + phase.duration:
                return phase
        return None

    def interpolate_control_values(self, current_time: float) -> Dict[str, float]:
        """Interpolate control values for smooth mechanical transitions"""
        active_phase = self.get_active_phase(current_time)

        if not active_phase:
            # Return default values for idle state
            return dict.fromkeys(self.control_channels.keys(), 0.0)

        # Calculate progress within current phase
        progress = (current_time - active_phase.start_time) / active_phase.duration

        # Smooth interpolation using cosine function for natural motion
        smooth_progress = 0.5 * (1 - np.cos(np.pi * progress))

        # Interpolate control values
        control_values = {}
        for channel, target_value in active_phase.control_settings.items():
            if channel in self.control_channels:
                current_value = self.control_channels[channel]
                # Smooth transition to target value
                control_values[channel] = current_value + (target_value - current_value) * smooth_progress

        return control_values

    def simulate_complete_performance(self, time_step: float = 0.01) -> Dict[str, List]:
        """Simulate complete 26.5-second theatrical performance"""
        simulation_time = np.arange(0, self.total_performance_time + time_step, time_step)

        control_history = {channel: [] for channel in self.control_channels}
        control_history['time'] = simulation_time
        control_history['phase'] = []

        for t in simulation_time:
            control_values = self.interpolate_control_values(t)
            active_phase = self.get_active_phase(t)

            for channel, value in control_values.items():
                control_history[channel].append(value)

            control_history['phase'].append(active_phase.name if active_phase else 'idle')

            # Update current control values
            self.control_channels.update(control_values)

        return control_history

    def generate_cam_coordinates(self, cam_name: str, num_points: int = 360) -> Tuple[np.ndarray, np.ndarray]:
        """Generate precise cam profile coordinates for Renaissance manufacturing"""
        if cam_name not in self.cam_profiles:
            raise ValueError(f"Cam profile '{cam_name}' not found")

        cam_profile = self.cam_profiles[cam_name]

        # Generate angle points
        angles = np.linspace(cam_profile.angle_range[0], cam_profile.angle_range[1], num_points)

        # Calculate radius for each angle
        radii = np.array([cam_profile.radius_function(angle) for angle in angles])

        # Convert to Cartesian coordinates for manufacturing
        x = radii * np.cos(angles)
        y = radii * np.sin(angles)

        return x, y

    def create_performance_timing_chart(self, save_path: Optional[str] = None) -> None:
        """Create comprehensive timing chart for theatrical performance"""
        # Simulate complete performance
        control_history = self.simulate_complete_performance()

        # Create subplot layout
        fig, axes = plt.subplots(len(self.control_channels) + 1, 1,
                                figsize=(14, 12), sharex=True)

        # Plot each control channel
        for i, (channel, values) in enumerate(control_history.items()):
            if channel == 'time' or channel == 'phase':
                continue

            ax = axes[i]
            ax.plot(control_history['time'], values, 'b-', linewidth=2)
            ax.set_ylabel(channel.replace('_', ' ').title(), fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.set_ylim(-0.1, 1.1)

        # Mark phase boundaries with theatrical annotations
        for phase in self.performance_phases:
            for ax in axes[:-1]:
                ax.axvline(x=phase.start_time, color='r', linestyle='--', alpha=0.5)
                ax.axvline(x=phase.start_time + phase.duration, color='r', linestyle='--', alpha=0.5)

        # Add phase annotations
        phase_axis = axes[-1]
        phase_axis.set_xlim(0, self.total_performance_time)
        phase_axis.set_ylim(0, 1)
        phase_axis.set_xlabel('Time (seconds)', fontsize=12)
        phase_axis.set_title('Mechanical Lion Performance - Complete Theatrical Sequence', fontsize=14, fontweight='bold')

        # Add phase labels
        for phase in self.performance_phases:
            phase_center = phase.start_time + phase.duration / 2
            phase_axis.text(phase_center, 0.5, phase.name.replace('_', ' ').title(),
                          ha='center', va='center', fontsize=9,
                          bbox={"boxstyle": 'round,pad=0.3', "facecolor": 'lightblue', "alpha": 0.7})

        phase_axis.set_yticks([])

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

    def export_cam_manufacturing_specs(self, output_dir: str) -> None:
        """Export detailed cam manufacturing specifications for Renaissance workshop"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        specs = {
            "project": "Leonardo's Mechanical Lion Control System",
            "date": "1517",
            "client": "King Francis I of France",
            "total_performance_time": self.total_performance_time,
            "cam_drum_specifications": {
                "diameter": 2 * self.cam_drum_radius,
                "rotation_speed": self.cam_rotation_speed,
                "material": "seasoned oak with bronze bushings",
                "surface_finish": "hand-polished",
                "tolerance": 0.1  # mm - achievable with Renaissance tools
            },
            "cam_profiles": {}
        }

        # Add detailed specifications for each cam
        for cam_name, _cam_profile in self.cam_profiles.items():
            x, y = self.generate_cam_coordinates(cam_name)

            specs["cam_profiles"][cam_name] = {
                "function": cam_name.replace('_', ' ').title(),
                "material": _cam_profile.material,
                "follower_type": _cam_profile.follower_type,
                "max_lift": _cam_profile.max_lift,
                "angle_range_degrees": tuple(np.degrees(_cam_profile.angle_range)),
                "manufacturing_notes": self._get_cam_manufacturing_notes(cam_name),
                "coordinates": {
                    "x_meters": x.tolist(),
                    "y_meters": y.tolist()
                }
            }

        # Save specifications
        specs_path = output_path / "cam_manufacturing_specifications.json"
        with open(specs_path, 'w') as f:
            json.dump(specs, f, indent=2)

        # Create individual cam profile drawings
        for cam_name, _cam_profile in self.cam_profiles.items():
            self._create_cam_profile_drawing(cam_name, output_path)

    def _get_cam_manufacturing_notes(self, cam_name: str) -> List[str]:
        """Get Renaissance-era manufacturing notes for each cam"""
        notes = {
            'walking_gait': [
                "Cut three complete cycles for three steps",
                "Smooth sinusoidal profile for natural movement",
                "Critical for realistic lion walking motion",
                "Use finest files for smooth transitions"
            ],
            'tail_motion': [
                "Gentle wave pattern for lifelike tail movement",
                "Double frequency creates natural sway",
                "Essential for theatrical effect",
                "Polish to mirror finish for smooth follower motion"
            ],
            'chest_opening': [
                "Smooth sigmoid transition for dramatic reveal",
                "Hardened bronze for durability",
                "Critical timing for theatrical impact",
                "Precise machining required for smooth opening"
            ],
            'lily_platform': [
                "Step profile with plateau for presentation",
                "Must hold position during royal display",
                "Critical for fleurs-de-lis presentation",
                "Roller follower recommended for smooth motion"
            ],
            'master_timing': [
                "Complex harmonic profile for coordination",
                "Steel construction for precision",
                "Controls all other cam timing",
                "Most critical cam - requires highest precision"
            ]
        }
        return notes.get(cam_name, ["Standard cam manufacturing procedures"])

    def _create_cam_profile_drawing(self, cam_name: str, output_dir: Path) -> None:
        """Create detailed cam profile drawing for manufacturing"""
        cam_profile = self.cam_profiles[cam_name]
        x, y = self.generate_cam_coordinates(cam_name)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

        # Plot cam profile geometry
        ax1.plot(x, y, 'b-', linewidth=2)
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_title(f'{cam_name.replace("_", " ").title()} Cam Profile\n'
                     f'Material: {cam_profile.material} | Follower: {cam_profile.follower_type}',
                     fontsize=12, fontweight='bold')
        ax1.set_xlabel('X (meters)')
        ax1.set_ylabel('Y (meters)')

        # Add reference circles for manufacturing
        for r in [0.02, 0.04, 0.06, 0.08]:
            circle = plt.Circle((0, 0), r, fill=False, linestyle='--', alpha=0.3)
            ax1.add_patch(circle)

        # Plot radius function
        angles = np.linspace(cam_profile.angle_range[0], cam_profile.angle_range[1], 360)
        radii = np.array([cam_profile.radius_function(angle) for angle in angles])

        ax2.plot(np.degrees(angles), radii * 1000, 'g-', linewidth=2)  # Convert to mm
        ax2.set_xlabel('Cam Angle (degrees)')
        ax2.set_ylabel('Radius (mm)')
        ax2.set_title(f'{cam_name.replace("_", " ").title()} Radius Function\n'
                     f'Maximum Lift: {cam_profile.max_lift*1000:.1f} mm',
                     fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Add manufacturing notes
        notes = self._get_cam_manufacturing_notes(cam_name)
        notes_text = '\n'.join([f"• {note}" for note in notes[:3]])
        ax2.text(0.02, 0.98, notes_text, transform=ax2.transAxes,
                fontsize=9, verticalalignment='top',
                bbox={"boxstyle": 'round,pad=0.5', "facecolor": 'lightyellow', "alpha": 0.8})

        plt.suptitle(f'Cam Manufacturing Specifications: {cam_name.replace("_", " ").title()}',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Save drawing
        drawing_path = output_dir / f'{cam_name}_cam_profile.png'
        plt.savefig(drawing_path, dpi=300, bbox_inches='tight')
        plt.close()

    def generate_performance_report(self) -> Dict:
        """Generate comprehensive performance report for royal court presentation"""
        return {
            "performance_summary": {
                "title": "Leonardo's Mechanical Lion - Royal Court Performance",
                "total_duration": self.total_performance_time,
                "number_of_phases": len(self.performance_phases),
                "control_channels": len(self.control_channels),
                "cam_profiles": len(self.cam_profiles),
                "target_audience": "King Francis I and Royal Court",
                "historical_significance": "First programmable automation controller"
            },
            "theatrical_breakdown": {
                "act_1_majestic_entrance": {
                    "duration": "2.0 seconds",
                    "description": "Lion stands majestically at rest",
                    "mechanical_elements": "Tail gently swaying",
                    "theatrical_impact": "Establishes mechanical marvel"
                },
                "act_2_prowling_survey": {
                    "duration": "4.0 seconds",
                    "description": "Lion turns in a slow arc, surveying the court",
                    "mechanical_elements": "Asymmetrical leg movement for turning gait",
                    "theatrical_impact": "Builds tension and displays intelligence"
                },
                "act_3_forward_advance": {
                    "duration": "6.0 seconds",
                    "description": "Two graceful steps forward",
                    "mechanical_elements": "Four-leg coordination with natural gait",
                    "theatrical_impact": "Demonstrates purposeful, lifelike movement"
                },
                "act_4_dramatic_pause": {
                    "duration": "2.0 seconds",
                    "description": "Lion pauses, prepares for reveal",
                    "mechanical_elements": "All mechanisms locked",
                    "theatrical_impact": "Builds anticipation"
                },
                "act_5_chest_reveal": {
                    "duration": "5.5 seconds",
                    "description": "Chest opens and lilies presented",
                    "mechanical_elements": "Chest mechanism and lily platform",
                    "theatrical_impact": "Celebration of Franco-Florentine alliance"
                },
                "act_6_royal_display": {
                    "duration": "5.0 seconds",
                    "description": "Presentation of royal symbols",
                    "mechanical_elements": "All mechanisms in display position",
                    "theatrical_impact": "Honors King Francis I"
                },
                "act_7_graceful_reset": {
                    "duration": "2.0 seconds",
                    "description": "Return to initial position",
                    "mechanical_elements": "Smooth mechanical reset",
                    "theatrical_impact": "Shows complete control mastery"
                }
            },
            "mechanical_innovations": {
                "cam_based_programming": "First use of cams for programmable automation",
                "multi_channel_control": "8 synchronized control channels",
                "theatrical_timing": "Precise coordination for dramatic effect",
                "biomechanical_design": "Natural lion gait replication",
                "reveal_mechanism": "Chest cavity with fleurs-de-lis presentation"
            },
            "renaissance_engineering_achievements": {
                "materials": "Bronze cams with oak framework",
                "precision": "±0.1mm manufacturing tolerance",
                "power_system": "Hand-wound springs with escapement",
                "reliability": "Repeatable performance for royal court",
                "craftsmanship": "Peak of 16th century mechanical art"
            },
            "historical_legacy": {
                "technological_impact": "Preceded modern robotics by 400 years",
                "cultural_significance": "Symbol of Franco-Italian alliance",
                "educational_value": "Foundation of automation theory",
                "artistic_achievement": "Fusion of art and engineering",
                "diplomatic_success": "Established Leonardo's reputation"
            }
        }

# Create global controller instance
lion_controller = MechanicalLionController()

def main():
    """Main function for demonstrating the control system"""
    print("=" * 70)
    print("LEONARDO'S MECHANICAL LION CONTROL SYSTEM")
    print("=" * 70)
    print("First Programmable Automation Controller in History")
    print("Created for King Francis I - Royal Court Performance, 1517")
    print()

    # Generate performance timing chart
    chart_path = "artifacts/lion_performance_timing.png"
    lion_controller.create_performance_timing_chart(chart_path)
    print(f"✓ Performance timing chart created: {chart_path}")

    # Export cam manufacturing specifications
    lion_controller.export_cam_manufacturing_specs("artifacts/cam_specifications")
    print("✓ Cam manufacturing specifications exported")

    # Generate performance report
    report = lion_controller.generate_performance_report()
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY:")
    print("=" * 70)
    print(f"Total Duration: {report['performance_summary']['total_duration']} seconds")
    print(f"Number of Phases: {report['performance_summary']['number_of_phases']}")
    print(f"Control Channels: {report['performance_summary']['control_channels']}")
    print(f"Cam Profiles: {report['performance_summary']['cam_profiles']}")

    print("\nTHEATRICAL BREAKDOWN:")
    for act, details in report['theatrical_breakdown'].items():
        print(f"  {act.replace('_', ' ').title()}:")
        print(f"    Duration: {details['duration']}")
        print(f"    Description: {details['description']}")
        print(f"    Impact: {details['theatrical_impact']}")

    print("\n" + "=" * 70)
    print("HISTORICAL SIGNIFICANCE:")
    print("=" * 70)
    print("This control system represents the birth of programmable automation,")
    print("preceding electronic computers by over 400 years. Leonardo's cam-based")
    print("programming created the first mechanical computer capable of complex,")
    print("coordinated theatrical performance.")

    print("\nPerformance complete! Ready for royal court presentation.")

if __name__ == "__main__":
    main()
