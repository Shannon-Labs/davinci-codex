"""
Advanced Unsteady Aerodynamics for Leonardo's Ornithopter

Implements Theodorsen-based unsteady aerodynamic theory with FSI coupling
for enhanced simulation fidelity while maintaining historical wing design constraints.

Historical Constraints:
- Wing planform from Codex Atlanticus 846r (bat-wing with articulated feathers)
- Flapping frequency limited by human power (~2 Hz maximum)
- Material: wooden spars with linen membrane (historical accuracy)
- No modern airfoil shapes - must use Leonardo's camber concepts
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import scipy.special as sp

from ..multiphysics.aerodynamics import AerodynamicsModule
from ..multiphysics.core import SimulationParameters


@dataclass
class OrnithopterGeometry:
    """Leonardo's ornithopter wing geometry from manuscript analysis."""

    # Wing planform (Codex Atlanticus 846r)
    wingspan: float = 12.0  # meters (total span)
    root_chord: float = 2.0  # meters
    tip_chord: float = 1.0  # meters
    sweep_angle: float = 15.0  # degrees (forward sweep from sketches)

    # Wing sections (bat-like anatomy)
    num_sections: int = 8  # articulated feather sections
    section_chord_ratio: np.ndarray = None  # chord taper along span

    # Flexibility properties (wood + linen construction)
    spanwise_stiffness: float = 1e6  # N⋅m² (estimated spruce wood)
    chordwise_stiffness: float = 5e5  # N⋅m²
    membrane_tension: float = 1e4  # N/m (linen under tension)

    def __post_init__(self):
        if self.section_chord_ratio is None:
            # Leonardo's tapered wing design
            self.section_chord_ratio = np.linspace(1.0, 0.5, self.num_sections)


class TheodorsenUnsteadyAero(AerodynamicsModule):
    """
    Theodorsen unsteady aerodynamics for flapping wing flight.

    Implements classical unsteady thin airfoil theory with:
    - Theodorsen's circulation function C(k)
    - Wagner function for indicial lift response
    - Added mass effects for accelerating wings
    - FSI coupling with flexible wing structure
    """

    def __init__(self, parameters: SimulationParameters):
        super().__init__("theodorsen_unsteady_aero", parameters)

        # Theodorsen function cache
        self._theodorsen_cache = {}
        self._wagner_cache = {}

        # FSI coupling variables
        self.structural_deformation = np.zeros(8)  # wing section deflections
        self.structural_velocities = np.zeros(8)

        # Unsteady flow variables
        self.bound_circulation = 0.0
        self.wake_circulation = []
        self.added_mass_coeff = 0.0

        # Historical operating conditions
        self.reynolds_number = 0.0
        self.reduced_frequency = 0.0

    def initialize(self, geometry: OrnithopterGeometry, materials, boundary_conditions):
        """Initialize unsteady aerodynamics with Leonardo's wing design."""

        self.geometry = geometry
        self.materials = materials
        self.boundary_conditions = boundary_conditions

        # Generate wing panels based on historical planform
        self._generate_leonardo_wing_panels()

        # Initialize FSI coupling
        self._initialize_fsi_coupling()

        # Set up flapping kinematics (human-powered constraints)
        self._setup_human_flapping_kinematics()

        # Compute Theodorsen function parameters
        self._compute_theodorsen_parameters()

        self.is_initialized = True

    def _generate_leonardo_wing_panels(self):
        """Generate wing panels matching Leonardo's bat-wing design."""

        # Wing sections based on Codex Atlanticus 846r
        self.num_panels = self.geometry.num_sections * 10  # 10 panels per section
        self.panel_coordinates = np.zeros((self.num_panels, 4, 3))
        self.control_points = np.zeros((self.num_panels, 3))
        self.panel_normals = np.zeros((self.num_panels, 3))
        self.panel_areas = np.zeros(self.num_panels)

        panel_idx = 0
        for section in range(self.geometry.num_sections):
            # Spanwise position of this section
            y_section = (section / self.geometry.num_sections) * self.geometry.wingspan / 2
            chord_length = (self.geometry.root_chord +
                          (self.geometry.tip_chord - self.geometry.root_chord) *
                          (2 * y_section / self.geometry.wingspan))

            # Generate panels for this wing section
            for chord_panel in range(10):
                x_pos = (chord_panel / 9.0) * chord_length

                # Leonardo's airfoil shape (high camber, simple curvature)
                thickness_ratio = 0.15  # Thick airfoils from Leonardo's observations
                camber_ratio = 0.08    # Significant camber for lift

                # Panel geometry
                dx = chord_length / 10.0 / 2.0
                dy = self.geometry.wingspan / self.geometry.num_sections / 2.0

                # Airfoil shape (simplified Leonardo camber line)
                camber = camber_ratio * chord_length * np.sin(np.pi * x_pos / chord_length)
                thickness = thickness_ratio * chord_length

                # Panel corners (upper surface)
                self.panel_coordinates[panel_idx] = np.array([
                    [x_pos - dx, y_section - dy, camber + thickness/2],
                    [x_pos + dx, y_section - dy, camber + thickness/2],
                    [x_pos + dx, y_section + dy, camber + thickness/2],
                    [x_pos - dx, y_section + dy, camber + thickness/2]
                ])

                # Control point and normal
                self.control_points[panel_idx] = np.array([x_pos, y_section, camber])
                self.panel_normals[panel_idx] = np.array([0, 0, 1])
                self.panel_areas[panel_idx] = (2 * dx) * (2 * dy)

                panel_idx += 1

    def _initialize_fsi_coupling(self):
        """Initialize fluid-structure interaction for flexible wings."""

        # Wing structural parameters (wood + linen)
        self.structural_mass = np.zeros(self.geometry.num_sections)
        self.structural_stiffness = np.zeros(self.geometry.num_sections)

        for section in range(self.geometry.num_sections):
            # Mass distribution (wood spars + linen membrane)
            chord_length = (self.geometry.root_chord +
                          (self.geometry.tip_chord - self.geometry.root_chord) *
                          (section / self.geometry.num_sections))
            section_area = chord_length * (self.geometry.wingspan / self.geometry.num_sections)

            # Historical materials (spruce wood + linen)
            wood_density = 450  # kg/m³ (spruce)
            linen_density = 300  # kg/m³ (treated linen)

            self.structural_mass[section] = section_area * (
                0.7 * wood_density * 0.02 +  # spar thickness 2cm
                0.3 * linen_density * 0.001   # membrane thickness 1mm
            )

            # Bending stiffness
            self.structural_stiffness[section] = (
                self.geometry.spanwise_stiffness *
                (1.0 - 0.3 * section / self.geometry.num_sections)  # taper toward tip
            )

    def _setup_human_flapping_kinematics(self):
        """Set up flapping kinematics within human power constraints."""

        # Human power limits (historical constraint)
        max_power_output = 150  # Watts (sustained human power)
        mech_efficiency = 0.3  # Leonardo's mechanism efficiency

        # Flapping parameters derived from power constraints
        available_power = max_power_output * mech_efficiency

        # Wing mass and inertia
        total_wing_mass = np.sum(self.structural_mass)
        wing_moment = total_wing_mass * (self.geometry.wingspan / 4) ** 2

        # Natural flapping frequency from power balance
        # P = 0.5 * I * omega² * omega  (approximate)
        self.flapping_frequency = min(2.0, (available_power / (0.5 * wing_moment)) ** (1/3))
        self.flapping_amplitude = 30.0  # degrees (Leonardo's design)

        # Phase lag for wing twist (Leonardo's articulated feathers)
        self.twist_phase_lag = 90.0  # degrees

        def leonardo_kinematics(time: float, span_position: float) -> Tuple[float, float]:
            """
            Leonardo's flapping kinematics with articulated wing twist.

            Returns:
                flapping_angle: Wing flapping angle [radians]
                twist_angle: Wing twist angle [radians]
            """
            # Flapping motion (sinusoidal)
            omega = 2 * np.pi * self.flapping_frequency
            flapping_angle = np.radians(self.flapping_amplitude) * np.sin(omega * time)

            # Wing twist (articulated feathers, phase-lagged)
            twist_amplitude = np.radians(15.0)  # 15 degrees twist
            phase_shift = np.radians(self.twist_phase_lag) * span_position
            twist_angle = twist_amplitude * np.sin(omega * time + phase_shift)

            return flapping_angle, twist_angle

        self.kinematics = leonardo_kinematics

    def _compute_theodorsen_parameters(self):
        """Compute parameters for Theodorsen unsteady aerodynamics."""

        # Reference chord (mean aerodynamic chord)
        self.mean_chord = (self.geometry.root_chord + self.geometry.tip_chord) / 2

        # Flight conditions
        self.freestream_velocity = 10.0  # m/s (cruise speed)
        self.air_density = 1.225  # kg/m³

        # Reduced frequency (key parameter for unsteady effects)
        self.reduced_frequency = (
            self.flapping_frequency * self.mean_chord / self.freestream_velocity
        )

        # Reynolds number
        kinematic_viscosity = 1.5e-5  # m²/s
        self.reynolds_number = (
            self.freestream_velocity * self.mean_chord / kinematic_viscosity
        )

        # Theodorsen function C(k) for reduced frequency k
        self._compute_theodorsen_function()

    def _compute_theodorsen_function(self):
        """Compute Theodorsen's circulation function C(k)."""

        k = self.reduced_frequency

        # Bessel functions for Theodorsen function
        if k > 0:
            # Hankel functions H1^(2) and H2^(2)
            H1_2 = sp.hankel2(1, k)
            H2_2 = sp.hankel2(2, k)

            # Theodorsen function: C(k) = H1^(2)(k) / (H1^(2)(k) + i*H2^(2)(k))
            numerator = H1_2
            denominator = H1_2 + 1j * H2_2

            self.theodorsen_C = numerator / denominator
        else:
            # Quasi-steady limit (k → 0)
            self.theodorsen_C = 1.0 - np.pi * k / 2

        # Wagner function (indicial response)
        self._compute_wagner_function()

    def _compute_wagner_function(self):
        """Compute Wagner function for indicial lift response."""

        # Simplified Wagner function approximation
        # φ(s) = 1 - 0.165*exp(-0.0455*s) - 0.335*exp(-0.3*s)

        self.wagner_coeffs = [1.0, -0.165, -0.335]
        self.wagner_time_constants = [0.0, 0.0455, 0.3]

    def compute_unsteady_lift(self, time: float) -> Dict[str, float]:
        """
        Compute unsteady lift using Theodorsen theory with FSI effects.

        Returns:
            Dictionary with lift components and total lift
        """

        # Wing kinematics
        span_positions = np.linspace(0, 1, self.geometry.num_sections)
        total_lift = 0.0
        circulatory_lift = 0.0
        noncirculatory_lift = 0.0
        added_mass_lift = 0.0

        for section_idx, y_pos in enumerate(span_positions):
            # Section chord
            chord = (self.geometry.root_chord +
                    (self.geometry.tip_chord - self.geometry.root_chord) * y_pos)

            # Kinematics at this section
            flapping_angle, twist_angle = self.kinematics(time, y_pos)

            # Effective angle of attack
            alpha = flapping_angle + twist_angle

            # Angular velocity and acceleration
            omega = 2 * np.pi * self.flapping_frequency
            angular_velocity = np.radians(self.flapping_amplitude) * omega * np.cos(omega * time)
            angular_acceleration = -np.radians(self.flapping_amplitude) * omega**2 * np.sin(omega * time)

            # Section area
            section_area = chord * (self.geometry.wingspan / self.geometry.num_sections)

            # Circulatory lift (Theodorsen function)
            dynamic_pressure = 0.5 * self.air_density * self.freestream_velocity**2
            cl_quasi_steady = 2 * np.pi * alpha  # Thin airfoil theory

            # Apply Theodorsen function for unsteady effects
            C_real = np.real(self.theodorsen_C)
            np.imag(self.theodorsen_C)

            circulatory_section = dynamic_pressure * section_area * cl_quasi_steady * C_real
            circulatory_lift += circulatory_section

            # Non-circulatory lift (added mass effects)
            added_mass_coeff = np.pi * self.air_density * chord**2 / 4

            # Angular velocity contribution
            noncirculatory_section = added_mass_coeff * chord * angular_velocity * self.freestream_velocity
            noncirculatory_lift += noncirculatory_section

            # Angular acceleration contribution (pure added mass)
            added_mass_section = added_mass_coeff * chord**2 * angular_acceleration / 2
            added_mass_lift += added_mass_section

            # FSI coupling effects (flexible wing deformation)
            if self.structural_deformation[section_idx] != 0:
                deformation_angle = self.structural_deformation[section_idx] / chord
                fsi_correction = dynamic_pressure * section_area * 2 * np.pi * deformation_angle * C_real
                total_lift += fsi_correction

            total_lift += circulatory_section + noncirculatory_section + added_mass_section

        return {
            'total_lift': total_lift,
            'circulatory_lift': circulatory_lift,
            'noncirculatory_lift': noncirculatory_lift,
            'added_mass_lift': added_mass_lift,
            'reduced_frequency': self.reduced_frequency,
            'reynolds_number': self.reynolds_number
        }

    def compute_structural_response(self, time: float, aerodynamic_loads: np.ndarray) -> np.ndarray:
        """
        Compute structural response to aerodynamic loads (FSI coupling).

        Args:
            time: Current time
            aerodynamic_loads: Aerodynamic force distribution on wing sections

        Returns:
            Structural deformation at each wing section
        """

        # Simple spring-mass-damper model for wing flexibility
        damping_ratio = 0.05  # Light damping for wood structure

        deformations = np.zeros(self.geometry.num_sections)

        for section_idx in range(self.geometry.num_sections):
            # Mass, stiffness, damping
            mass = self.structural_mass[section_idx]
            stiffness = self.structural_stiffness[section_idx]
            2 * damping_ratio * np.sqrt(mass * stiffness)

            # Natural frequency of this section
            omega_n = np.sqrt(stiffness / mass)

            # Aerodynamic forcing
            aero_force = aerodynamic_loads[section_idx]

            # Static deformation (simplified)
            if stiffness > 0:
                static_deform = aero_force / stiffness

                # Dynamic amplification (resonance effects)
                freq_ratio = self.flapping_frequency / omega_n

                if freq_ratio < 0.5:
                    # Below resonance - quasi-static response
                    dynamic_factor = 1.0
                elif freq_ratio < 2.0:
                    # Near resonance - dynamic amplification
                    dynamic_factor = 1.0 / (2 * damping_ratio)
                else:
                    # Above resonance - reduced response
                    dynamic_factor = 1.0 / freq_ratio**2

                deformations[section_idx] = static_deform * dynamic_factor

        # Update structural state
        self.structural_deformation = deformations

        return deformations

    def advance_wake(self, time_step: float):
        """Advance wake vortex system with proper convection."""

        # Wake convection velocity
        convection_velocity = self.freestream_velocity * 0.8  # Downwash effect

        # Add new wake vortex from trailing edge
        trailing_edge_strength = self.bound_circulation * 0.1  # Shed circulation

        new_wake_vortex = {
            'strength': trailing_edge_strength,
            'position': np.array([self.geometry.root_chord, 0, 0]),
            'age': 0.0
        }

        self.wake_circulation.append(new_wake_vortex)

        # Age and convect existing wake vortices
        for vortex in self.wake_circulation:
            vortex['position'][0] += convection_velocity * time_step
            vortex['age'] += time_step

        # Remove old wake vortices
        max_age = 5.0 / self.flapping_frequency  # 5 flapping periods
        self.wake_circulation = [
            v for v in self.wake_circulation if v['age'] < max_age
        ]

    def compute_performance_metrics(self) -> Dict[str, float]:
        """Compute enhanced performance metrics with uncertainty bounds."""

        # Get basic metrics from parent class
        basic_metrics = super().compute_performance_metrics()

        # Add unsteady aerodynamics metrics
        lift_components = self.compute_unsteady_lift(0.0)

        # Efficiency metrics
        propulsive_efficiency = self._compute_propulsive_efficiency()

        # Power requirements (human constraints)
        power_required = self._compute_power_requirements()

        # Structural loads
        max_stress = self._compute_max_structural_stress()

        return {
            **basic_metrics,
            **lift_components,
            'propulsive_efficiency': propulsive_efficiency,
            'power_required_watts': power_required,
            'max_structural_stress_pa': max_stress,
            'flapping_frequency_hz': self.flapping_frequency,
            'human_power_factor': power_required / 150.0,  # Ratio to human power
        }

    def _compute_propulsive_efficiency(self) -> float:
        """Compute propulsive efficiency considering unsteady effects."""

        # Modified propulsive efficiency with Theodorsen effects
        C_real = np.real(self.theodorsen_C)

        # Basic efficiency from reduced frequency
        basic_efficiency = 1.0 / (1.0 + self.reduced_frequency)

        # Theodorsen correction
        theodorsen_correction = C_real

        return basic_efficiency * theodorsen_correction

    def _compute_power_requirements(self) -> float:
        """Compute power required for flapping within human constraints."""

        # Inertial power (accelerating wing mass)
        total_wing_mass = np.sum(self.structural_mass)
        wing_radius = self.geometry.wingspan / 4
        wing_inertia = total_wing_mass * wing_radius**2

        omega = 2 * np.pi * self.flapping_frequency
        amplitude_rad = np.radians(self.flapping_amplitude)

        inertial_power = 0.5 * wing_inertia * omega**3 * amplitude_rad**2

        # Aerodynamic power
        dynamic_pressure = 0.5 * self.air_density * self.freestream_velocity**2
        wing_area = (self.geometry.root_chord + self.geometry.tip_chord) / 2 * self.geometry.wingspan

        # Induced power from lift generation
        lift_required = total_wing_mass * 9.81
        induced_velocity = np.sqrt(lift_required / (2 * self.air_density * wing_area))
        induced_power = lift_required * induced_velocity

        # Profile power (overcoming drag)
        cd_profile = 0.02  # Estimate for flexible membrane wing
        profile_power = dynamic_pressure * wing_area * cd_profile * self.freestream_velocity

        total_power = inertial_power + induced_power + profile_power

        return total_power

    def _compute_max_structural_stress(self) -> float:
        """Compute maximum structural stress in wing spars."""

        # Maximum bending moment at wing root
        total_wing_mass = np.sum(self.structural_mass)
        wing_half_span = self.geometry.wingspan / 2

        # Bending moment from wing weight
        weight_moment = total_wing_mass * 9.81 * wing_half_span / 2

        # Bending moment from aerodynamic loads
        lift_force = total_wing_mass * 9.81 * 1.2  # 20% margin
        aero_moment = lift_force * wing_half_span / 2

        total_moment = weight_moment + aero_moment

        # Maximum stress in wooden spar
        spar_diameter = 0.1  # 10cm diameter spar (Leonardo's design)
        section_modulus = np.pi * spar_diameter**3 / 32

        max_stress = total_moment / section_modulus

        return max_stress


def create_enhanced_ornithopter_sim() -> TheodorsenUnsteadyAero:
    """
    Factory function to create enhanced ornithopter simulation.

    Returns:
        Configured TheodorsenUnsteadyAero instance
    """

    # Simulation parameters for high-fidelity analysis
    params = SimulationParameters(
        time_start=0.0,
        time_end=10.0,
        time_step=0.001,  # 1ms time steps for unsteady effects
        mesh_density="fine",
        enable_fsi=True,
        enable_fatigue=True,
        coupling_tolerance=1e-8,
        max_coupling_iterations=100
    )

    # Leonardo's wing geometry
    OrnithopterGeometry(
        wingspan=12.0,
        root_chord=2.0,
        tip_chord=1.0,
        sweep_angle=15.0,
        num_sections=8
    )

    # Create aerodynamics module
    aero_module = TheodorsenUnsteadyAero(params)

    return aero_module


if __name__ == "__main__":
    # Demonstration of enhanced ornithopter simulation

    print("Leonardo's Ornithopter - Enhanced Unsteady Aerodynamics")
    print("=" * 60)

    # Create enhanced simulation
    sim = create_enhanced_ornithopter_sim()

    # Initialize with Leonardo's wing design
    geometry = OrnithopterGeometry()
    materials = {}  # Would contain historical material properties
    boundary_conditions = {
        'freestream': {'velocity': [10.0, 0.0, 0.0], 'angle_of_attack': 5.0},
        'flapping': {
            'amplitude': 30.0,
            'frequency': 2.0,
            'phase_lag': 90.0
        }
    }

    sim.initialize(geometry, materials, boundary_conditions)

    print(f"Wing span: {geometry.wingspan} m")
    print(f"Root chord: {geometry.root_chord} m")
    print(f"Tip chord: {geometry.tip_chord} m")
    print(f"Flapping frequency: {sim.flapping_frequency:.2f} Hz")
    print(f"Reduced frequency: {sim.reduced_frequency:.3f}")
    print(f"Reynolds number: {sim.reynolds_number:.0f}")

    # Compute lift at different time points
    times = np.linspace(0, 2.0, 5)
    print("\nUnsteady Lift Analysis:")
    print("Time (s) | Total Lift (N) | Circulatory | Non-circulatory | Added Mass")
    print("-" * 70)

    for t in times:
        lift_data = sim.compute_unsteady_lift(t)
        print(f"{t:8.2f} | {lift_data['total_lift']:13.1f} | "
              f"{lift_data['circulatory_lift']:11.1f} | "
              f"{lift_data['noncirculatory_lift']:14.1f} | "
              f"{lift_data['added_mass_lift']:10.1f}")

    # Performance metrics
    metrics = sim.compute_performance_metrics()
    print("\nPerformance Metrics:")
    print(f"Propulsive efficiency: {metrics['propulsive_efficiency']:.3f}")
    print(f"Power required: {metrics['power_required_watts']:.1f} W")
    print(f"Human power factor: {metrics['human_power_factor']:.2f}")
    print(f"Max structural stress: {metrics['max_structural_stress_pa']/1e6:.1f} MPa")

    print("\nHistorical Compliance:")
    print(f"Human power feasible: {'✓' if metrics['human_power_factor'] < 1.0 else '✗'}")
    print(f"Wood stress safe: {'✓' if metrics['max_structural_stress_pa'] < 40e6 else '✗'}")
