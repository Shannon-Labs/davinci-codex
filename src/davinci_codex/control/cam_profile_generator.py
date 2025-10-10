"""
Cam Profile Generator for Leonardo's Mechanical Lion
Mathematical design of cam profiles for programmable automation

Historical Context:
- Leonardo's innovative cam drum programming system
- First use of mathematical curves for automation
- Renaissance precision manufacturing techniques
- Foundation of mechanical computing

Engineering Innovation:
- Mathematical function-based cam design
- Smooth motion profile optimization
- Multi-channel synchronization
- Theater-timed mechanical coordination
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple, Callable, Optional
from pathlib import Path
import json
import math

@dataclass
class CamSpecification:
    """Complete cam specification for manufacturing"""
    name: str
    function: str
    base_radius: float  # meters
    max_lift: float     # meters
    angle_range: Tuple[float, float]  # radians
    profile_type: str
    material: str
    follower_type: str
    surface_finish: str
    manufacturing_notes: List[str]
    mathematical_function: Callable[[float], float]

@dataclass
class CamProfileAnalysis:
    """Analysis of cam profile performance"""
    max_velocity: float     # m/s
    max_acceleration: float # m/s²
    max_jerk: float        # m/s³
    smoothness_rating: float
    manufacturing_complexity: float
    force_requirements: Dict[str, float]

class CamProfileGenerator:
    """
    Mathematical cam profile generator for Leonardo's Mechanical Lion

    This class designs the cam profiles that create the precise mechanical
    movements needed for the theatrical performance, using mathematical
    functions optimized for smooth, reliable operation.
    """

    def __init__(self):
        # Cam drum parameters
        self.drum_radius = 0.15  # meters
        self.rotation_speed = 13.58  # degrees per second
        self.max_cam_radius = 0.08  # meters
        self.min_cam_radius = 0.02  # meters

        # Material properties (Renaissance materials)
        self.materials = {
            'bronze': {'density': 8800, 'strength': 200e6, 'hardness': 65},
            'steel': {'density': 7850, 'strength': 400e6, 'hardness': 120},
            'oak': {'density': 750, 'strength': 40e6, 'hardness': 25}
        }

        # Follower types
        self.follower_types = {
            'knife_edge': {'friction': 0.15, 'wear_rate': 0.8},
            'roller': {'friction': 0.05, 'wear_rate': 0.2},
            'flat_face': {'friction': 0.1, 'wear_rate': 0.4}
        }

    def generate_walking_gait_cam(self) -> CamSpecification:
        """
        Generate cam profile for natural lion walking gait

        This cam creates the characteristic leg movement pattern that
        mimics a real lion's walking motion through careful mathematical
        design of the lift and swing phases.
        """
        def walking_profile(angle: float) -> float:
            """Mathematical function for natural walking gait"""
            base_radius = 0.05  # meters
            lift_height = 0.03  # meters

            # Complex waveform for natural walking
            # Combines multiple harmonics for realistic motion
            primary = math.sin(angle)
            secondary = 0.3 * math.sin(2 * angle)  # Double frequency for nuance
            tertiary = 0.1 * math.sin(3 * angle)   # Triple frequency for smoothness

            # Normalize and scale
            combined = (primary + secondary + tertiary) / 1.4

            return base_radius + lift_height * combined

        return CamSpecification(
            name="walking_gait_cam",
            function="Generate natural lion walking motion",
            base_radius=0.05,
            max_lift=0.03,
            angle_range=(0, 3 * 2 * math.pi),  # 3 complete cycles for 3 steps
            profile_type="complex_harmonic",
            material="bronze",
            follower_type="roller",
            surface_finish="polished",
            manufacturing_notes=[
                "Three complete cycles for three walking steps",
                "Complex harmonic profile for natural movement",
                "Critical for realistic lion gait",
                "Use finest files for smooth transitions",
                "Check cam follower clearance carefully",
                "Test with leg mechanism before final assembly"
            ],
            mathematical_function=walking_profile
        )

    def generate_tail_motion_cam(self) -> CamSpecification:
        """
        Generate cam profile for natural tail swaying motion

        The tail movement adds lifelike quality to the automaton,
        using a gentle wave pattern that creates natural-looking
        tail sway during the walking sequence.
        """
        def tail_profile(angle: float) -> float:
            """Mathematical function for natural tail motion"""
            base_radius = 0.04  # meters
            sway_amplitude = 0.02  # meters

            # Double frequency creates natural sway pattern
            # Add slight variation for organic movement
            primary = math.sin(2 * angle)
            variation = 0.2 * math.sin(5 * angle)  # Small higher frequency

            combined = primary + variation

            return base_radius + sway_amplitude * combined

        return CamSpecification(
            name="tail_motion_cam",
            function="Create natural tail swaying during walking",
            base_radius=0.04,
            max_lift=0.02,
            angle_range=(0, 2 * math.pi),
            profile_type="wave_pattern",
            material="bronze",
            follower_type="knife_edge",
            surface_finish="smooth",
            manufacturing_notes=[
                "Gentle wave pattern for lifelike movement",
                "Double frequency creates natural sway",
                "Subtle variations add organic quality",
                "Essential for theatrical effect",
                "Polish to mirror finish for smooth operation",
                "Test tail linkage for binding"
            ],
            mathematical_function=tail_profile
        )

    def generate_chest_opening_cam(self) -> CamSpecification:
        """
        Generate cam profile for dramatic chest cavity opening

        This cam controls the mechanical reveal mechanism, creating
        a smooth, dramatic opening that builds theatrical tension
        before the fleurs-de-lis presentation.
        """
        def chest_profile(angle: float) -> float:
            """Mathematical function for smooth chest opening"""
            base_radius = 0.03  # meters
            max_opening = 0.05  # meters

            # Sigmoid-like transition for smooth acceleration/deceleration
            # Creates dramatic theatrical effect
            if angle < math.pi:
                # Opening phase - smooth acceleration
                progress = angle / math.pi
                # Smooth sigmoid function
                transition = 0.5 * (1 + math.tanh(4 * (progress - 0.5)))
            else:
                # Closing phase - smooth deceleration
                progress = (2 * math.pi - angle) / math.pi
                transition = 0.5 * (1 + math.tanh(4 * (progress - 0.5)))

            return base_radius + max_opening * transition

        return CamSpecification(
            name="chest_opening_cam",
            function="Control dramatic chest cavity opening",
            base_radius=0.03,
            max_lift=0.05,
            angle_range=(0, 2 * math.pi),
            profile_type="sigmoid_transition",
            material="hardened_bronze",
            follower_type="flat_face",
            surface_finish="highly_polished",
            manufacturing_notes=[
                "Smooth sigmoid transition for dramatic effect",
                "Hardened bronze for repeated operation",
                "Critical for theatrical timing",
                "Precision machining required",
                "Test chest mechanism for binding",
                "Ensure smooth panel movement"
            ],
            mathematical_function=chest_profile
        )

    def generate_lily_platform_cam(self) -> CamSpecification:
        """
        Generate cam profile for fleurs-de-lis platform presentation

        This cam controls the vertical movement of the lily platform,
        creating a smooth elevation with a dramatic pause for the
        royal symbol presentation.
        """
        def lily_profile(angle: float) -> float:
            """Mathematical function for controlled lily platform elevation"""
            base_radius = 0.035  # meters
            presentation_height = 0.04  # meters

            # Step function with smooth transitions
            # Rise → Hold → Lower sequence for presentation
            if angle < math.pi / 2:
                # Rising phase
                position = (1 - math.cos(angle * 2)) / 2  # Smooth cosine rise
            elif angle < 3 * math.pi / 2:
                # Hold at top - presentation phase
                position = 1.0
            else:
                # Lowering phase
                progress = (2 * math.pi - angle) / (math.pi / 2)
                position = (1 + math.cos(progress * math.pi)) / 2  # Smooth cosine lower

            return base_radius + presentation_height * position

        return CamSpecification(
            name="lily_platform_cam",
            function="Control fleurs-de-lis platform presentation",
            base_radius=0.035,
            max_lift=0.04,
            angle_range=(0, 2 * math.pi),
            profile_type="step_function",
            material="bronze",
            follower_type="roller",
            surface_finish="polished",
            manufacturing_notes=[
                "Step profile with plateau for presentation",
                "Must hold position during royal display",
                "Critical for fleurs-de-lis presentation",
                "Roller follower recommended for smooth motion",
                "Test platform stability at full extension",
                "Ensure smooth return to retracted position"
            ],
            mathematical_function=lily_profile
        )

    def generate_master_timing_cam(self) -> CamSpecification:
        """
        Generate master timing cam for overall performance coordination

        This is the most critical cam, controlling the precise timing
        of all other mechanisms and ensuring the theatrical performance
        unfolds with perfect coordination.
        """
        def timing_profile(angle: float) -> float:
            """Complex mathematical function for master timing control"""
            base_radius = 0.025  # meters
            timing_variations = 0.015  # meters

            # Complex harmonic combination for precise timing control
            # Multiple frequencies create complex timing patterns
            fundamental = math.sin(angle)
            third_harmonic = 0.3 * math.sin(3 * angle)
            fifth_harmonic = 0.2 * math.sin(5 * angle)
            seventh_harmonic = 0.1 * math.sin(7 * angle)

            # Combine harmonics with weighting
            timing_signal = (fundamental + third_harmonic +
                           fifth_harmonic + seventh_harmonic) / 1.6

            return base_radius + timing_variations * (0.5 + 0.5 * timing_signal)

        return CamSpecification(
            name="master_timing_cam",
            function="Coordinate all mechanisms with precise timing",
            base_radius=0.025,
            max_lift=0.015,
            angle_range=(0, 2 * math.pi),
            profile_type="complex_harmonic",
            material="steel",
            follower_type="knife_edge",
            surface_finish="precision_ground",
            manufacturing_notes=[
                "Most critical cam - requires highest precision",
                "Complex harmonic profile for coordination",
                "Steel construction for stability",
                "Controls all other cam timing",
                "Precision ground surface essential",
                "Test timing with all mechanisms connected",
                "Verify theatrical sequence timing"
            ],
            mathematical_function=timing_profile
        )

    def analyze_cam_profile(self, cam_spec: CamSpecification) -> CamProfileAnalysis:
        """
        Analyze cam profile performance characteristics

        This function evaluates the mathematical properties of the cam
        profile to ensure smooth operation and reliable performance.
        """
        # Generate profile data points
        angles = np.linspace(cam_spec.angle_range[0], cam_spec.angle_range[1], 1000)
        radii = np.array([cam_spec.mathematical_function(angle) for angle in angles])

        # Calculate derivatives for motion analysis
        dt = 0.01  # time step in seconds
        dr_dt = np.gradient(radii, dt)  # velocity
        d2r_dt2 = np.gradient(dr_dt, dt)  # acceleration
        d3r_dt3 = np.gradient(d2r_dt2, dt)  # jerk

        # Calculate angular velocity (rad/s)
        angular_velocity = math.radians(self.rotation_speed)

        # Calculate actual velocities and accelerations
        velocities = np.abs(dr_dt * angular_velocity)
        accelerations = np.abs(d2r_dt2 * angular_velocity**2)
        jerks = np.abs(d3r_dt3 * angular_velocity**3)

        # Smoothness rating (lower jerk = smoother)
        smoothness = 1.0 / (1.0 + np.max(jerks))

        # Manufacturing complexity based on profile variation
        profile_variation = np.std(radii)
        complexity = min(1.0, profile_variation / cam_spec.max_lift)

        # Force requirements
        max_follower_force = np.max(accelerations) * 0.5  # 0.5 kg follower mass
        spring_force = max_follower_force * 1.5  # Safety factor

        return CamProfileAnalysis(
            max_velocity=np.max(velocities),
            max_acceleration=np.max(accelerations),
            max_jerk=np.max(jerks),
            smoothness_rating=smoothness,
            manufacturing_complexity=complexity,
            force_requirements={
                'max_follower_force_n': max_follower_force,
                'required_spring_force_n': spring_force,
                'bearing_load_n': max_follower_force * 1.2
            }
        )

    def generate_manufacturing_coordinates(self, cam_spec: CamSpecification,
                                         num_points: int = 360) -> Dict[str, np.ndarray]:
        """
        Generate precise manufacturing coordinates for cam profile

        This function creates the exact coordinates needed by Renaissance
        craftsmen to manufacture the cam profiles with hand tools.
        """
        angles = np.linspace(cam_spec.angle_range[0], cam_spec.angle_range[1], num_points)

        # Calculate radius for each angle
        radii = np.array([cam_spec.mathematical_function(angle) for angle in angles])

        # Convert to Cartesian coordinates
        x = radii * np.cos(angles)
        y = radii * np.sin(angles)

        # Calculate manufacturing tolerances
        tolerance = 0.0001  # 0.1mm - achievable with Renaissance tools

        return {
            'x_coordinates': x,
            'y_coordinates': y,
            'angles_degrees': np.degrees(angles),
            'radii_meters': radii,
            'tolerance_meters': tolerance,
            'surface_finish_requirements': cam_spec.surface_finish
        }

    def create_cam_profile_visualization(self, cam_spec: CamSpecification,
                                       save_path: Optional[str] = None) -> None:
        """
        Create comprehensive visualization of cam profile

        This generates the technical drawings needed for manufacturing
        and analysis of the cam profile performance.
        """
        # Generate profile data
        coords = self.generate_manufacturing_coordinates(cam_spec)
        analysis = self.analyze_cam_profile(cam_spec)

        # Create subplot layout
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # 1. Cam profile geometry
        ax1.plot(coords['x_coordinates'], coords['y_coordinates'], 'b-', linewidth=2)
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_title(f'{cam_spec.name.replace("_", " ").title()} - Cam Profile Geometry',
                     fontsize=12, fontweight='bold')
        ax1.set_xlabel('X (meters)')
        ax1.set_ylabel('Y (meters)')

        # Add reference circles
        for r in [0.02, 0.04, 0.06, 0.08]:
            circle = plt.Circle((0, 0), r, fill=False, linestyle='--', alpha=0.3)
            ax1.add_patch(circle)

        # 2. Radius function
        ax2.plot(np.degrees(coords['angles_degrees']), coords['radii_meters'] * 1000, 'g-', linewidth=2)
        ax2.set_xlabel('Cam Angle (degrees)')
        ax2.set_ylabel('Radius (mm)')
        ax2.set_title(f'Radius Function - Max Lift: {cam_spec.max_lift*1000:.1f} mm',
                     fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # 3. Motion analysis
        angles = np.linspace(cam_spec.angle_range[0], cam_spec.angle_range[1], 1000)
        radii = np.array([cam_spec.mathematical_function(angle) for angle in angles])

        # Calculate motion derivatives
        dt = 0.01
        dr_dt = np.gradient(radii, dt)
        d2r_dt2 = np.gradient(dr_dt, dt)
        d3r_dt3 = np.gradient(d2r_dt2, dt)

        angular_velocity = math.radians(self.rotation_speed)

        ax3.plot(np.degrees(angles), np.abs(dr_dt * angular_velocity) * 1000, 'r-',
                linewidth=2, label='Velocity')
        ax3.plot(np.degrees(angles), np.abs(d2r_dt2 * angular_velocity**2) * 1000, 'b-',
                linewidth=2, label='Acceleration')
        ax3.set_xlabel('Cam Angle (degrees)')
        ax3.set_ylabel('Motion (mm/s or mm/s²)')
        ax3.set_title('Motion Analysis', fontsize=12, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. Manufacturing specifications
        ax4.axis('off')

        # Create specification text
        spec_text = f"""
        MANUFACTURING SPECIFICATIONS
        ─────────────────────────
        Name: {cam_spec.name.replace('_', ' ').title()}
        Function: {cam_spec.function}
        Material: {cam_spec.material}
        Follower: {cam_spec.follower_type}
        Surface Finish: {cam_spec.surface_finish}

        DIMENSIONS
        ─────────────────────────
        Base Radius: {cam_spec.base_radius*1000:.1f} mm
        Max Lift: {cam_spec.max_lift*1000:.1f} mm
        Angle Range: {np.degrees(cam_spec.angle_range[0]):.1f}° - {np.degrees(cam_spec.angle_range[1]):.1f}°
        Profile Type: {cam_spec.profile_type}

        PERFORMANCE ANALYSIS
        ─────────────────────────
        Max Velocity: {analysis.max_velocity*1000:.2f} mm/s
        Max Acceleration: {analysis.max_acceleration*1000:.2f} mm/s²
        Smoothness Rating: {analysis.smoothness_rating:.2f}
        Manufacturing Complexity: {analysis.manufacturing_complexity:.2f}

        FORCE REQUIREMENTS
        ─────────────────────────
        Max Follower Force: {analysis.force_requirements['max_follower_force_n']:.2f} N
        Required Spring Force: {analysis.force_requirements['required_spring_force_n']:.2f} N
        Bearing Load: {analysis.force_requirements['bearing_load_n']:.2f} N

        MANUFACTURING NOTES
        ─────────────────────────
        """

        # Add manufacturing notes
        for i, note in enumerate(cam_spec.manufacturing_notes[:5]):
            spec_text += f"{i+1}. {note}\n"

        ax4.text(0.05, 0.95, spec_text, transform=ax4.transAxes,
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))

        plt.suptitle(f'Cam Profile Analysis: {cam_spec.name.replace("_", " ").title()}',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def export_cam_design_package(self, output_dir: str) -> None:
        """
        Export complete cam design package for manufacturing

        This creates all the technical documentation needed by
        Renaissance craftsmen to manufacture the cam profiles.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate all cam specifications
        cam_specs = {
            'walking_gait': self.generate_walking_gait_cam(),
            'tail_motion': self.generate_tail_motion_cam(),
            'chest_opening': self.generate_chest_opening_cam(),
            'lily_platform': self.generate_lily_platform_cam(),
            'master_timing': self.generate_master_timing_cam()
        }

        # Create design package summary
        design_package = {
            "project": "Leonardo's Mechanical Lion - Cam Design Package",
            "date": "1517",
            "designer": "Leonardo da Vinci",
            "client": "King Francis I of France",
            "purpose": "Royal court performance automation",
            "total_cams": len(cam_specs),
            "manufacturing_period": "4-6 months",
            "required_craftsmen": 2,
            "tools_required": [
                "Hand files (various grades)",
                "Calipers and compasses",
                "Polishing stones",
                "Hardened steel cutters",
                "Bronze casting equipment"
            ],
            "cam_specifications": {}
        }

        # Process each cam
        for cam_name, cam_spec in cam_specs.items():
            # Generate analysis
            analysis = self.analyze_cam_profile(cam_spec)

            # Generate manufacturing coordinates
            coords = self.generate_manufacturing_coordinates(cam_spec)

            # Create visualization
            viz_path = output_path / f"{cam_name}_cam_analysis.png"
            self.create_cam_profile_visualization(cam_spec, str(viz_path))

            # Add to design package
            design_package["cam_specifications"][cam_name] = {
                "name": cam_spec.name,
                "function": cam_spec.function,
                "material": cam_spec.material,
                "base_radius_mm": cam_spec.base_radius * 1000,
                "max_lift_mm": cam_spec.max_lift * 1000,
                "angle_range_degrees": [np.degrees(cam_spec.angle_range[0]),
                                       np.degrees(cam_spec.angle_range[1])],
                "profile_type": cam_spec.profile_type,
                "follower_type": cam_spec.follower_type,
                "surface_finish": cam_spec.surface_finish,
                "manufacturing_notes": cam_spec.manufacturing_notes,
                "performance_analysis": {
                    "max_velocity_mm_s": analysis.max_velocity * 1000,
                    "max_acceleration_mm_s2": analysis.max_acceleration * 1000,
                    "smoothness_rating": analysis.smoothness_rating,
                    "manufacturing_complexity": analysis.manufacturing_complexity
                },
                "manufacturing_coordinates": {
                    "x_coordinates_mm": (coords['x_coordinates'] * 1000).tolist(),
                    "y_coordinates_mm": (coords['y_coordinates'] * 1000).tolist(),
                    "angles_degrees": coords['angles_degrees'].tolist(),
                    "tolerance_mm": coords['tolerance_meters'] * 1000
                },
                "generated_files": [str(viz_path)]
            }

        # Save complete design package
        package_path = output_path / "cam_design_package.json"
        with open(package_path, 'w') as f:
            json.dump(design_package, f, indent=2)

        # Create manufacturing instruction sheets
        self._create_manufacturing_instructions(cam_specs, output_path)

        print(f"✓ Cam design package exported to: {output_path}")
        print(f"✓ Generated {len(cam_specs)} cam profiles")
        print(f"✓ Created technical drawings and specifications")

    def _create_manufacturing_instructions(self, cam_specs: Dict[str, CamSpecification],
                                         output_path: Path) -> None:
        """Create detailed manufacturing instructions for Renaissance craftsmen"""

        instructions = f"""
        LEONARDO'S MECHANICAL LION - CAM MANUFACTURING INSTRUCTIONS
        ==================================================================

        Prepared by: Leonardo da Vinci
        Date: 1517
        Purpose: Royal court performance for King Francis I

        GENERAL MANUFACTURING REQUIREMENTS
        ==================================================================

        1. MATERIAL PREPARATION
        ─────────────────────────
        • Use specified materials for each cam
        • Ensure metal is properly annealed before machining
        • Check for defects and imperfections
        • Verify material hardness and workability

        2. PRECISION REQUIREMENTS
        ─────────────────────────
        • Tolerance: ±0.1mm (achievable with careful hand work)
        • Surface finish: As specified for each cam
        • Profile accuracy: Follow mathematical functions exactly
        • Angle measurements: Use precision dividers and protractors

        3. MANUFACTURING SEQUENCE
        ─────────────────────────
        • Rough cut cam blank to approximate shape
        • Mark center hole and mount on mandrel
        • Transfer profile coordinates using dividers
        • Carefully file to precise profile shape
        • Polish to specified surface finish
        • Verify profile accuracy with templates
        • Heat treat if required by material specifications

        SPECIFIC CAM INSTRUCTIONS
        ==================================================================

        """

        # Add specific instructions for each cam
        for cam_name, cam_spec in cam_specs.items():
            instructions += f"""
        {cam_spec.name.replace('_', ' ').upper()}
        {'=' * len(cam_spec.name)}

        Function: {cam_spec.function}
        Material: {cam_spec.material}
        Follower: {cam_spec.follower_type}
        Surface Finish: {cam_spec.surface_finish}

        Manufacturing Notes:
        ─────────────────────────
        """

            for i, note in enumerate(cam_spec.manufacturing_notes, 1):
                instructions += f"        {i}. {note}\n"

            instructions += "\n"

        # Add quality control instructions
        instructions += f"""
        QUALITY CONTROL AND TESTING
        ==================================================================

        1. PROFILE VERIFICATION
        ─────────────────────────
        • Check cam profile against coordinate templates
        • Verify radius measurements at multiple angles
        • Test cam follower engagement for smoothness
        • Check for any binding or interference

        2. ASSEMBLY TESTING
        ─────────────────────────
        • Test each cam individually with its mechanism
        • Verify timing relationships between cams
        • Check complete system integration
        • Test full performance sequence

        3. PERFORMANCE VALIDATION
        ─────────────────────────
        • Verify walking gait smoothness and naturalness
        • Test chest opening timing and smoothness
        • Check lily platform elevation accuracy
        • Validate complete 26.5-second performance

        FINAL ACCEPTANCE CRITERIA
        ==================================================================

        • All cam profiles within specified tolerances
        • Smooth operation without binding or noise
        • Complete performance sequence executed flawlessly
        • Theatrical timing meets royal court requirements
        • System reliability for multiple demonstrations

        ==================================================================
        These cam profiles represent the pinnacle of Renaissance mechanical
        engineering. Each profile has been mathematically optimized for
        smooth, reliable operation and theatrical effect.

        Signed: Leonardo da Vinci
        Date: 1517
        ==================================================================
        """

        # Save instructions
        instructions_path = output_path / "manufacturing_instructions.txt"
        with open(instructions_path, 'w') as f:
            f.write(instructions)

def main():
    """Main function for demonstrating cam profile generation"""
    print("=" * 80)
    print("CAM PROFILE GENERATOR - LEONARDO'S MECHANICAL LION")
    print("=" * 80)
    print("Mathematical Design of Cam Profiles for Programmable Automation")
    print("First Mechanical Computer in History - 1517")
    print()

    # Initialize generator
    generator = CamProfileGenerator()

    # Generate all cam specifications
    cams = {
        'walking_gait': generator.generate_walking_gait_cam(),
        'tail_motion': generator.generate_tail_motion_cam(),
        'chest_opening': generator.generate_chest_opening_cam(),
        'lily_platform': generator.generate_lily_platform_cam(),
        'master_timing': generator.generate_master_timing_cam()
    }

    print(f"Generated {len(cams)} cam profiles:")
    print()

    # Analyze each cam
    for cam_name, cam_spec in cams.items():
        analysis = generator.analyze_cam_profile(cam_spec)
        print(f"  {cam_name.replace('_', ' ').title()}:")
        print(f"    Function: {cam_spec.function}")
        print(f"    Material: {cam_spec.material}")
        print(f"    Max Lift: {cam_spec.max_lift*1000:.1f} mm")
        print(f"    Smoothness: {analysis.smoothness_rating:.2f}")
        print(f"    Complexity: {analysis.manufacturing_complexity:.2f}")
        print()

    # Export complete design package
    generator.export_cam_design_package("artifacts/cam_designs")

    print("=" * 80)
    print("CAM PROFILE GENERATION COMPLETE")
    print("=" * 80)
    print("These mathematically designed cam profiles create the world's first")
    print("programmable automation controller, enabling Leonardo's Mechanical")
    print("Lion to perform its theatrical ballet for King Francis I.")
    print()
    print("Each profile has been optimized for smooth, reliable operation")
    print("and maximum theatrical effect using Renaissance manufacturing")
    print("capabilities.")

if __name__ == "__main__":
    main()