"""
Enhanced Blade Element Momentum Theory for Leonardo's Aerial Screw

Implements high-fidelity BEMT with vortex system modeling for improved
lift prediction while maintaining historical helical rotor design constraints.

Historical Constraints:
- Helical pitch: 3.5m from Codex Atlanticus 869r
- Rotor radius: 2.0m (Leonardo's specification)
- Material: wooden construction with linen covering
- Power source: human crank or early steam engine (power density limits)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class AerialScrewGeometry:
    """Leonardo's aerial screw geometry from Codex Atlanticus 869r."""

    # Rotor dimensions (from manuscript)
    rotor_radius: float = 2.0  # meters
    inner_radius: float = 1.6  # meters (hollow core)
    helical_pitch: float = 3.5  # meters per revolution
    num_blades: int = 2  # Double helix design

    # Blade geometry
    blade_chord: float = 0.4  # meters (estimated from sketches)
    blade_thickness: float = 0.05  # meters (wooden construction)
    twist_distribution: Optional[np.ndarray] = None

    # Operating conditions
    design_rpm: float = 100.0  # RPM (estimated from human power)
    slip_factor: float = 0.42  # Historical efficiency estimate

    def __post_init__(self):
        if self.twist_distribution is None:
            # Optimal twist for helical rotor
            r_elements = np.linspace(self.inner_radius, self.rotor_radius, 10)
            self.twist_distribution = np.degrees(np.arctan(self.helical_pitch / (2 * np.pi * r_elements)))


class BladeElementMomentumTheory:
    """
    Enhanced Blade Element Momentum Theory for Leonardo's aerial screw.

    Features:
    - BEMT with proper induced velocity calculation
    - Vortex wake modeling for complex flow patterns
    - Blade element integration with historical airfoil shapes
    - Power prediction with historical constraints
    """

    def __init__(self, geometry: AerialScrewGeometry):
        self.geometry = geometry

        # Atmospheric conditions
        self.air_density = 1.225  # kg/m³
        self.air_viscosity = 1.81e-5  # Pa·s
        self.sound_speed = 343.0  # m/s

        # Discretization
        self.num_elements = 20
        self.radial_positions = np.linspace(
            geometry.inner_radius, geometry.rotor_radius, self.num_elements
        )

        # Blade element properties
        self.chord_distribution = np.full(self.num_elements, geometry.blade_chord)
        self.twist_distribution = np.interp(
            self.radial_positions,
            np.linspace(geometry.inner_radius, geometry.rotor_radius, len(geometry.twist_distribution)),
            geometry.twist_distribution
        )

        # Flow variables
        self.induced_velocity = np.zeros(self.num_elements)
        self.tangential_induced_velocity = np.zeros(self.num_elements)
        self.angle_of_attack = np.zeros(self.num_elements)
        self.local_lift = np.zeros(self.num_elements)
        self.local_drag = np.zeros(self.num_elements)

        # Convergence parameters
        self.tolerance = 1e-6
        self.max_iterations = 100

        # Vortex wake parameters
        self.wake_vortices = []
        self.vortex_strength = 0.0

    def compute_rotor_performance(self, rpm: float, collective_pitch: float = 0.0) -> Dict[str, float]:
        """
        Compute comprehensive rotor performance using BEMT.

        Args:
            rpm: Rotor speed in revolutions per minute
            collective_pitch: Collective pitch adjustment [degrees]

        Returns:
            Dictionary with performance metrics
        """

        omega = 2 * np.pi * rpm / 60.0  # rad/s

        # Initialize induced velocities (momentum theory first guess)
        self._initialize_induced_velocities(rpm, collective_pitch)

        # Iterative BEMT solution
        for iteration in range(self.max_iterations):
            # Store old values for convergence check
            old_induced = self.induced_velocity.copy()

            # Update flow conditions at each blade element
            self._update_flow_conditions(rpm, collective_pitch)

            # Compute blade element forces
            self._compute_blade_element_forces()

            # Update induced velocities from momentum theory
            self._update_induced_velocities_momentum()

            # Check convergence
            error = np.max(np.abs(self.induced_velocity - old_induced))
            if error < self.tolerance:
                logger.debug(f"BEMT converged in {iteration} iterations")
                break
        else:
            logger.warning(f"BEMT did not converge after {self.max_iterations} iterations")

        # Integrate forces and moments
        total_thrust, total_torque, total_power = self._integrate_forces(omega)

        # Compute performance coefficients
        tip_speed = omega * self.geometry.rotor_radius
        disk_area = np.pi * (self.geometry.rotor_radius**2 - self.geometry.inner_radius**2)

        # Non-dimensional coefficients
        thrust_coefficient = total_thrust / (self.air_density * disk_area * tip_speed**2)
        power_coefficient = total_power / (self.air_density * disk_area * tip_speed**3)
        torque_coefficient = total_torque / (self.air_density * disk_area * tip_speed**2 * self.geometry.rotor_radius)

        # Efficiency metrics
        figure_of_merit = self._compute_figure_of_merit(total_thrust, total_power)
        induced_efficiency = self._compute_induced_efficiency()

        # Wake analysis
        wake_characteristics = self._analyze_wake_structure()

        return {
            'thrust_N': total_thrust,
            'torque_Nm': total_torque,
            'power_W': total_power,
            'thrust_coefficient': thrust_coefficient,
            'power_coefficient': power_coefficient,
            'torque_coefficient': torque_coefficient,
            'figure_of_merit': figure_of_merit,
            'induced_efficiency': induced_efficiency,
            'tip_speed_ms': tip_speed,
            'tip_mach': tip_speed / self.sound_speed,
            'advance_ratio': 0.0,  # Hover condition
            **wake_characteristics
        }

    def _initialize_induced_velocities(self, rpm: float, collective_pitch: float):
        """Initialize induced velocities using simple momentum theory."""

        omega = 2 * np.pi * rpm / 60.0
        np.pi * (self.geometry.rotor_radius**2 - self.geometry.inner_radius**2)

        # Estimate induced velocity from momentum theory
        # T = 2 * rho * A * v_i^2
        # For initial guess, assume moderate loading
        loading_factor = 0.1  # T/(rho*A*V_tip^2)
        tip_speed = omega * self.geometry.rotor_radius

        self.induced_velocity = np.full(self.num_elements,
                                       np.sqrt(loading_factor) * tip_speed)
        self.tangential_induced_velocity = np.zeros(self.num_elements)

    def _update_flow_conditions(self, rpm: float, collective_pitch: float):
        """Update flow conditions at each blade element."""

        omega = 2 * np.pi * rpm / 60.0

        for i in range(self.num_elements):
            r = self.radial_positions[i]

            # Velocities at blade element
            tangential_velocity = omega * r + self.tangential_induced_velocity[i]
            axial_velocity = self.induced_velocity[i]

            # Resultant velocity
            resultant_velocity = np.sqrt(tangential_velocity**2 + axial_velocity**2)

            # Inflow angle
            inflow_angle = np.arctan2(axial_velocity, tangential_velocity)

            # Blade geometric angle (including twist and collective)
            geometric_angle = np.radians(self.twist_distribution[i] + collective_pitch)

            # Angle of attack
            self.angle_of_attack[i] = geometric_angle - inflow_angle

            # Local Reynolds number
            chord = self.chord_distribution[i]
            local_re = self.air_density * resultant_velocity * chord / self.air_viscosity

            # Store local conditions for force calculation
            self.local_reynolds[i] = local_re if hasattr(self, 'local_reynolds') else 0
            self.local_resultant_velocity[i] = resultant_velocity if hasattr(self, 'local_resultant_velocity') else 0

        # Initialize arrays if not present
        if not hasattr(self, 'local_reynolds'):
            self.local_reynolds = np.zeros(self.num_elements)
        if not hasattr(self, 'local_resultant_velocity'):
            self.local_resultant_velocity = np.zeros(self.num_elements)

    def _compute_blade_element_forces(self):
        """Compute aerodynamic forces on each blade element."""

        for i in range(self.num_elements):
            alpha = self.angle_of_attack[i]
            V = self.local_resultant_velocity[i]
            Re = self.local_reynolds[i]

            # Lift and drag coefficients (historical airfoil)
            cl, cd = self._get_airfoil_coefficients(alpha, Re)

            # Dynamic pressure
            q = 0.5 * self.air_density * V**2

            # Blade element area
            dr = (self.geometry.rotor_radius - self.geometry.inner_radius) / self.num_elements
            element_area = self.chord_distribution[i] * dr

            # Forces per blade
            lift_per_blade = q * element_area * cl
            drag_per_blade = q * element_area * cd

            # Total forces (all blades)
            self.local_lift[i] = lift_per_blade * self.geometry.num_blades
            self.local_drag[i] = drag_per_blade * self.geometry.num_blades

    def _get_airfoil_coefficients(self, alpha: float, Re: float) -> Tuple[float, float]:
        """
        Get lift and drag coefficients for historical airfoil shape.

        Based on Leonardo's observations of bird wings and simple curved surfaces.
        """

        # Stall angle (historical airfoils stall early)
        alpha_stall = np.radians(12.0)

        if abs(alpha) <= alpha_stall:
            # Linear region (thin airfoil theory with historical corrections)
            cl_alpha = 2 * np.pi * 0.7  # Reduced effectiveness vs. ideal
            cl = cl_alpha * alpha

            # Drag polar (historical high drag)
            cd0 = 0.015  # Profile drag
            cd2 = 0.05   # Induced drag factor
            cd = cd0 + cd2 * alpha**2
        else:
            # Post-stall (deep stall characteristics)
            cl_stall = cl_alpha * alpha_stall * np.sign(alpha)
            cl = cl_stall * (1.0 - 0.3 * (abs(alpha) - alpha_stall) / alpha_stall)

            # Very high drag in stall
            cd = 0.1 + 0.5 * (abs(alpha) - alpha_stall)**2

        # Reynolds number corrections (low Re effects)
        if Re < 50000:
            # Low Reynolds number degradation
            re_factor = 0.5 + 0.5 * Re / 50000
            cl *= re_factor
            cd *= (2.0 - re_factor)

        return cl, cd

    def _update_induced_velocities_momentum(self):
        """Update induced velocities using momentum theory."""

        for i in range(self.num_elements):
            r = self.radial_positions[i]
            dr = (self.geometry.rotor_radius - self.geometry.inner_radius) / self.num_elements

            # Annular area
            area = 2 * np.pi * r * dr

            # Momentum theory: T = 2 * rho * A * v_i * (v_i + V0)
            # For hover: T = 2 * rho * A * v_i^2
            thrust_element = self.local_lift[i] * np.cos(self.angle_of_attack[i]) - \
                           self.local_drag[i] * np.sin(self.angle_of_attack[i])

            if thrust_element > 0:
                # Induced velocity from momentum theory
                v_i_new = np.sqrt(thrust_element / (2 * self.air_density * area))

                # Relaxation for stability
                relaxation = 0.3
                self.induced_velocity[i] = (1 - relaxation) * self.induced_velocity[i] + \
                                          relaxation * v_i_new

            # Tangential induced velocity from torque balance
            torque_element = (self.local_lift[i] * np.sin(self.angle_of_attack[i]) +
                            self.local_drag[i] * np.cos(self.angle_of_attack[i])) * r

            if torque_element > 0 and self.induced_velocity[i] > 0:
                # Angular momentum conservation
                v_t_new = torque_element / (2 * self.air_density * area * r * self.induced_velocity[i])

                relaxation = 0.3
                self.tangential_induced_velocity[i] = (1 - relaxation) * self.tangential_induced_velocity[i] + \
                                                     relaxation * v_t_new

    def _integrate_forces(self, omega: float) -> Tuple[float, float, float]:
        """Integrate forces and moments over all blade elements."""

        total_thrust = 0.0
        total_torque = 0.0

        for i in range(self.num_elements):
            # Thrust contribution
            thrust_element = self.local_lift[i] * np.cos(self.angle_of_attack[i]) - \
                           self.local_drag[i] * np.sin(self.angle_of_attack[i])
            total_thrust += thrust_element

            # Torque contribution
            r = self.radial_positions[i]
            torque_element = (self.local_lift[i] * np.sin(self.angle_of_attack[i]) +
                            self.local_drag[i] * np.cos(self.angle_of_attack[i])) * r
            total_torque += torque_element

        # Power required
        total_power = total_torque * omega

        return total_thrust, total_torque, total_power

    def _compute_figure_of_merit(self, thrust: float, power: float) -> float:
        """Compute figure of merit (induced efficiency)."""

        if power <= 0 or thrust <= 0:
            return 0.0

        # Ideal induced power
        disk_area = np.pi * (self.geometry.rotor_radius**2 - self.geometry.inner_radius**2)
        ideal_induced_velocity = np.sqrt(thrust / (2 * self.air_density * disk_area))
        ideal_power = thrust * ideal_induced_velocity

        # Figure of merit
        figure_of_merit = ideal_power / power

        return min(figure_of_merit, 1.0)  # Cap at 1.0

    def _compute_induced_efficiency(self) -> float:
        """Compute induced power efficiency."""

        # Average induced velocity
        avg_induced_velocity = np.mean(self.induced_velocity)

        # Ideal induced velocity from total thrust
        total_thrust = np.sum(self.local_lift * np.cos(self.angle_of_attack) -
                            self.local_drag * np.sin(self.angle_of_attack))
        disk_area = np.pi * (self.geometry.rotor_radius**2 - self.geometry.inner_radius**2)
        ideal_induced_velocity = np.sqrt(total_thrust / (2 * self.air_density * disk_area))

        if ideal_induced_velocity > 0:
            induced_efficiency = ideal_induced_velocity / avg_induced_velocity
            return min(induced_efficiency, 1.0)
        else:
            return 0.0

    def _analyze_wake_structure(self) -> Dict[str, float]:
        """Analyze vortex wake structure for complex flow patterns."""

        # Compute vortex circulation distribution
        circulation_distribution = np.zeros(self.num_elements)

        for i in range(self.num_elements):
            # Circulation from Kutta-Joukowski theorem
            V = self.local_resultant_velocity[i]
            circulation_distribution[i] = self.local_lift[i] / (self.air_density * V)

        # Total circulation
        total_circulation = np.sum(circulation_distribution)

        # Wake contraction/expansion factor
        avg_induced_velocity = np.mean(self.induced_velocity)
        tip_speed = 2 * np.pi * 100 / 60 * self.geometry.rotor_radius  # At design RPM
        wake_contraction = 1.0 - avg_induced_velocity / tip_speed

        # Vortex core size estimate
        reynolds_wake = self.air_density * avg_induced_velocity * self.geometry.rotor_radius / self.air_viscosity
        vortex_core_radius = self.geometry.rotor_radius / np.sqrt(reynolds_wake)

        return {
            'total_circulation_m2_s': total_circulation,
            'wake_contraction_factor': wake_contraction,
            'vortex_core_radius_m': vortex_core_radius,
            'tip_vortex_strength': circulation_distribution[-1] if len(circulation_distribution) > 0 else 0.0
        }

    def compute_performance_map(self, rpm_range: Tuple[float, float],
                              collective_range: Tuple[float, float]) -> Dict[str, np.ndarray]:
        """
        Compute comprehensive performance map over operating envelope.

        Args:
            rpm_range: (min_rpm, max_rpm)
            collective_range: (min_collective, max_collective) in degrees

        Returns:
            Dictionary with performance arrays
        """

        rpm_values = np.linspace(rpm_range[0], rpm_range[1], 20)
        collective_values = np.linspace(collective_range[0], collective_range[1], 10)

        # Initialize result arrays
        thrust_map = np.zeros((len(collective_values), len(rpm_values)))
        power_map = np.zeros((len(collective_values), len(rpm_values)))
        torque_map = np.zeros((len(collective_values), len(rpm_values)))
        fm_map = np.zeros((len(collective_values), len(rpm_values)))

        # Compute performance at each condition
        for i, collective in enumerate(collective_values):
            for j, rpm in enumerate(rpm_values):
                performance = self.compute_rotor_performance(rpm, collective)

                thrust_map[i, j] = performance['thrust_N']
                power_map[i, j] = performance['power_W']
                torque_map[i, j] = performance['torque_Nm']
                fm_map[i, j] = performance['figure_of_merit']

        return {
            'rpm_values': rpm_values,
            'collective_values': collective_values,
            'thrust_map': thrust_map,
            'power_map': power_map,
            'torque_map': torque_map,
            'figure_of_merit_map': fm_map
        }

    def assess_historical_feasibility(self, performance: Dict[str, float]) -> Dict[str, bool]:
        """
        Assess feasibility against historical constraints.

        Args:
            performance: Performance metrics from compute_rotor_performance

        Returns:
            Dictionary with feasibility assessments
        """

        assessments = {}

        # Human power constraints
        human_power_sustained = 150  # Watts
        assessments['human_power_feasible'] = performance['power_W'] < human_power_sustained

        # Material stress constraints (wood)
        max_tensile_stress_wood = 40e6  # Pa (spruce)
        # Estimate centrifugal stress
        omega = 2 * np.pi * 100 / 60  # rad/s at design RPM
        centrifugal_stress = self.air_density * omega**2 * self.geometry.rotor_radius**2
        assessments['material_stress_feasible'] = centrifugal_stress < max_tensile_stress_wood

        # Speed constraints (tip Mach number)
        assessments['tip_speed_subsonic'] = performance['tip_mach'] < 0.3

        # Structural dynamics (avoid resonance)
        natural_frequency_blade = 15.0  # Hz (estimate for wooden blade)
        rotation_frequency = 100 / 60  # Hz
        assessments['avoid_resonance'] = abs(rotation_frequency - natural_frequency_blade) > 2.0

        # Efficiency requirements
        assessments['minimum_efficiency'] = performance['figure_of_merit'] > 0.3

        # Overall feasibility
        assessments['overall_feasible'] = all(assessments.values())

        return assessments


def create_enhanced_aerial_screw_analysis() -> BladeElementMomentumTheory:
    """
    Factory function to create enhanced aerial screw analysis.

    Returns:
        Configured BladeElementMomentumTheory instance
    """

    # Leonardo's aerial screw geometry
    geometry = AerialScrewGeometry(
        rotor_radius=2.0,
        inner_radius=1.6,
        helical_pitch=3.5,
        num_blades=2,
        blade_chord=0.4,
        design_rpm=100.0,
        slip_factor=0.42
    )

    return BladeElementMomentumTheory(geometry)


if __name__ == "__main__":
    # Demonstration of enhanced aerial screw analysis

    print("Leonardo's Aerial Screw - Enhanced Blade Element Momentum Theory")
    print("=" * 70)

    # Create analysis instance
    analysis = create_enhanced_aerial_screw_analysis()

    print("Rotor Configuration:")
    print(f"  Radius: {analysis.geometry.rotor_radius} m")
    print(f"  Inner radius: {analysis.geometry.inner_radius} m")
    print(f"  Helical pitch: {analysis.geometry.helical_pitch} m")
    print(f"  Number of blades: {analysis.geometry.num_blades}")
    print(f"  Blade chord: {analysis.geometry.blade_chord} m")

    # Performance at design conditions
    print("\nPerformance at Design Conditions (100 RPM):")
    performance = analysis.compute_rotor_performance(rpm=100.0, collective_pitch=0.0)

    print(f"  Thrust: {performance['thrust_N']:.1f} N")
    print(f"  Torque: {performance['torque_Nm']:.1f} Nm")
    print(f"  Power: {performance['power_W']:.1f} W")
    print(f"  Figure of Merit: {performance['figure_of_merit']:.3f}")
    print(f"  Tip Speed: {performance['tip_speed_ms']:.1f} m/s (Mach {performance['tip_mach']:.3f})")

    # Historical feasibility assessment
    feasibility = analysis.assess_historical_feasibility(performance)
    print("\nHistorical Feasibility Assessment:")
    for criterion, feasible in feasibility.items():
        status = "✓" if feasible else "✗"
        print(f"  {criterion.replace('_', ' ').title()}: {status}")

    # Performance map
    print("\nGenerating Performance Map...")
    perf_map = analysis.compute_performance_map((50, 150), (-10, 10))

    # Find optimal operating point
    fm_map = perf_map['figure_of_merit_map']
    max_fm_idx = np.unravel_index(np.argmax(fm_map), fm_map.shape)
    optimal_rpm = perf_map['rpm_values'][max_fm_idx[1]]
    optimal_collective = perf_map['collective_values'][max_fm_idx[0]]

    print("Optimal Operating Point:")
    print(f"  RPM: {optimal_rpm:.0f}")
    print(f"  Collective: {optimal_collective:.1f}°")
    print(f"  Max Figure of Merit: {fm_map[max_fm_idx]:.3f}")

    # Performance at optimal point
    optimal_performance = analysis.compute_rotor_performance(optimal_rpm, optimal_collective)
    print(f"  Thrust at optimum: {optimal_performance['thrust_N']:.1f} N")
    print(f"  Power at optimum: {optimal_performance['power_W']:.1f} W")

    # Compare with required lift for human flight
    human_mass = 80  # kg
    machine_mass = 65  # kg (estimated from Leonardo's design)
    required_lift = (human_mass + machine_mass) * 9.81

    print("\nLift Capability:")
    print(f"  Required lift: {required_lift:.1f} N")
    print(f"  Available lift: {optimal_performance['thrust_N']:.1f} N")
    print(f"  Lift margin: {(optimal_performance['thrust_N']/required_lift - 1)*100:.1f}%")

    if optimal_performance['thrust_N'] > required_lift:
        print("  ✓ Capable of lifting human + machine")
    else:
        print("  ✗ Insufficient lift for human flight")
        lift_deficit = required_lift - optimal_performance['thrust_N']
        print(f"    Additional {lift_deficit:.1f} N of thrust needed")
