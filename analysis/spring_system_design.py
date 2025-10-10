"""
Spring-Wound Power System Design for Leonardo's Mechanical Lion

This module provides a comprehensive design analysis of the spring-wound power
system, leveraging Leonardo's expertise in spring mechanisms and clockwork
engineering. The design uses Renaissance-era materials and manufacturing
techniques while maximizing energy density and reliability.

Spring System Components:
1. Main Power Spring - High-carbon steel spiral spring
2. Winding Mechanism - Hand crank with mechanical advantage
3. Escapement Regulation - Clockwork speed control
4. Power Distribution - Geared drive train
5. Safety Features - Controlled energy release

Design Philosophy:
Leonardo would have used his extensive knowledge of spring mechanics,
developed through his work on clocks, automata, and mechanical devices.
The spring system provides high energy density in a compact form factor,
essential for fitting within the lion's body while maintaining aesthetic
appearance.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Physical Constants
GRAVITY = 9.80665  # m/s²
PI = math.pi

# Spring Material Properties (Renaissance-era high-carbon steel)
STEEL_DENSITY = 7850  # kg/m³
STEEL_YIELD_STRENGTH = 400e6  # Pa (400 MPa for high-carbon steel)
STEEL_ELASTIC_MODULUS = 200e9  # Pa (200 GPa)
SPRING_EFFICIENCY = 0.95  # Energy retention in well-made springs

# Energy Requirements (from energy_budget.py)
TOTAL_ENERGY_REQUIRED = 850.0  # Joules (from energy budget)
PEAK_POWER_REQUIRED = 45.0  # Watts (from energy budget)
PERFORMANCE_DURATION = 30.0  # seconds

# Mechanical Design Parameters
GEAR_RATIO_WINDING = 20.0  # Mechanical advantage for winding
WINDING_HANDLE_RADIUS = 0.15  # meters
WINDING_TORQUE_LIMIT = 50.0  # Newton-meters (reasonable human effort)
ESCAPEMENT_FREQUENCY = 2.0  # Hz (2 ticks per second)

@dataclass
class SpringSpecification:
    """Detailed specification for a spiral spring."""
    wire_diameter_mm: float
    mean_radius_m: float
    active_coils: int
    free_length_m: float
    solid_length_m: float
    spring_constant_n_per_m: float
    max_torque_nm: float
    energy_capacity_j: float
    mass_kg: float
    material: str

@dataclass
class EscapementSpec:
    """Escapement mechanism specification."""
    type: str
    tooth_count: int
    escape_wheel_radius_m: float
    pendulum_length_m: float
    regulation_accuracy_percent: float
    power_consumption_w: float

class SpringPowerSystem:
    """
    Complete spring-wound power system design for the Mechanical Lion.

    This class designs the optimal spring configuration based on Leonardo's
    knowledge of spring mechanics, incorporating Renaissance manufacturing
    constraints and performance requirements.
    """

    def __init__(self):
        self.main_spring: SpringSpecification = None
        self.escapement: EscapementSpec = None
        self.winding_mechanism: Dict = {}
        self.power_distribution: Dict = {}
        self._design_spring_system()

    def _design_spring_system(self) -> None:
        """Design the complete spring power system."""

        # Design main power spring
        self.main_spring = self._design_main_spring()

        # Design escapement mechanism
        self.escapement = self._design_escapement()

        # Design winding mechanism
        self.winding_mechanism = self._design_winding_mechanism()

        # Design power distribution
        self.power_distribution = self._design_power_distribution()

    def _design_main_spring(self) -> SpringSpecification:
        """Design the main power spring based on energy requirements."""

        # Target energy storage (with safety margin)
        target_energy = TOTAL_ENERGY_REQUIRED * 1.5  # 50% safety margin
        effective_energy = target_energy / SPRING_EFFICIENCY

        # Spiral spring design (Leonardo's preferred approach)
        # Based on his spring designs in Codex Atlanticus

        # Wire diameter calculation
        # τ = T*r / J where τ is shear stress, T is torque, r is radius, J is polar moment
        # J = π*d^4/32 for circular wire

        # Assume max torque occurs at full wind
        max_torque_target = 25.0  # Newton-meters (reasonable for lion mechanism)

        # Calculate wire diameter for this torque
        # Rearranging shear stress formula
        allowable_shear_stress = STEEL_YIELD_STRENGTH * 0.6  # 60% of yield strength
        wire_diameter = (32 * max_torque_target / (PI * allowable_shear_stress)) ** 0.25
        wire_diameter_mm = wire_diameter * 1000

        # Optimize wire diameter for manufacturing
        if wire_diameter_mm < 2.0:
            wire_diameter_mm = 2.0
        elif wire_diameter_mm > 6.0:
            wire_diameter_mm = 6.0

        wire_diameter = wire_diameter_mm / 1000  # Convert back to meters

        # Calculate spring geometry
        outer_radius = 0.12  # meters (must fit in lion body)
        inner_radius = 0.03  # meters (central arbor)
        mean_radius = (outer_radius + inner_radius) / 2

        # Calculate spring constant
        # k = G*d^4 / (10.8*D^3*n) where G is shear modulus, d is wire diameter,
        # D is mean coil diameter, n is number of active coils
        shear_modulus = STEEL_ELASTIC_MODULUS / (2 * (1 + 0.3))  # Poisson's ratio ≈ 0.3
        mean_coil_diameter = 2 * mean_radius

        # Calculate number of active coils for desired energy capacity
        # Energy = 0.5 * k * θ^2 where θ is angular deflection
        # Maximum angular deflection ≈ 2π * active_coils

        target_spring_constant = 2 * effective_energy / (PI ** 2)  # Simplified calculation
        active_coils = (shear_modulus * wire_diameter ** 4) / (10.8 * mean_coil_diameter ** 3 * target_spring_constant)

        # Optimize coil count
        if active_coils < 10:
            active_coils = 10
        elif active_coils > 30:
            active_coils = 30

        # Recalculate actual spring constant
        spring_constant = (shear_modulus * wire_diameter ** 4) / (10.8 * mean_coil_diameter ** 3 * active_coils)

        # Calculate energy capacity
        max_wind_angle = 2 * PI * active_coils * 0.8  # 80% of maximum to avoid overstress
        energy_capacity = 0.5 * spring_constant * max_wind_angle ** 2

        # Calculate spring mass
        wire_length = 2 * PI * mean_radius * active_coils
        wire_area = PI * (wire_diameter / 2) ** 2
        spring_mass = wire_length * wire_area * STEEL_DENSITY

        # Calculate dimensions
        free_length = outer_radius - inner_radius + wire_diameter * active_coils
        solid_length = wire_diameter * active_coils

        return SpringSpecification(
            wire_diameter_mm=wire_diameter_mm,
            mean_radius_m=mean_radius,
            active_coils=int(active_coils),
            free_length_m=free_length,
            solid_length_m=solid_length,
            spring_constant_n_per_m=spring_constant,
            max_torque_nm=spring_constant * max_wind_angle,
            energy_capacity_j=energy_capacity,
            mass_kg=spring_mass,
            material="High-carbon steel (Renaissance forge)"
        )

    def _design_escapement(self) -> EscapementSpec:
        """Design the escapement mechanism for power regulation."""

        # Leonardo would have used a verge escapement (common in 16th century)
        # This provides reliable speed regulation for constant performance

        # Escapement wheel design
        tooth_count = 30  # Standard for clockwork mechanisms
        escape_wheel_radius = 0.05  # meters

        # Verge design
        verge_length = 0.08  # meters
        pendulum_length = 0.25  # meters (for 2 Hz frequency)

        # Regulation accuracy (Renaissance craftsmanship)
        regulation_accuracy = 5.0  # ±5% timing accuracy

        # Power consumption
        power_consumption = 3.0  # Watts (continuous)

        return EscapementSpec(
            type="Verge escapement with foliot balance",
            tooth_count=tooth_count,
            escape_wheel_radius_m=escape_wheel_radius,
            pendulum_length_m=pendulum_length,
            regulation_accuracy_percent=regulation_accuracy,
            power_consumption_w=power_consumption
        )

    def _design_winding_mechanism(self) -> Dict:
        """Design the winding mechanism for human operation."""

        # Hand crank design
        handle_radius = WINDING_HANDLE_RADIUS
        gear_ratio = GEAR_RATIO_WINDING

        # Calculate required human effort
        spring_wind_torque = self.main_spring.max_torque_nm
        human_torque_required = spring_wind_torque / gear_ratio

        # Winding force at handle
        winding_force = human_torque_required / handle_radius

        # Number of winding turns required
        wind_angle_rad = 2 * PI * self.main_spring.active_coils * 0.8
        handle_turns = wind_angle_rad / (2 * PI)

        # Winding time (reasonable for court preparation)
        winding_time_s = handle_turns / 2.0  # 2 turns per second

        # Effort analysis
        is_feasible = human_torque_required < WINDING_TORQUE_LIMIT

        return {
            "handle_radius_m": handle_radius,
            "gear_ratio": gear_ratio,
            "human_torque_required_nm": human_torque_required,
            "winding_force_n": winding_force,
            "handle_turns_required": handle_turns,
            "winding_time_s": winding_time_s,
            "is_human_feasible": is_feasible,
            "mechanism_type": "Spur gear train with bronze gears"
        }

    def _design_power_distribution(self) -> Dict:
        """Design the power distribution system."""

        # Primary drive gear
        drive_gear_radius = 0.08  # meters
        drive_gear_teeth = 60

        # Secondary gears for leg mechanisms
        leg_gear_ratio = 3.0  # Reduce speed, increase torque

        # Chest mechanism gear train
        chest_gear_ratio = 5.0  # High torque for panel opening

        # Lily platform gear train
        lily_gear_ratio = 4.0  # Moderate torque for elevation

        return {
            "primary_drive_gear": {
                "radius_m": drive_gear_radius,
                "teeth": drive_gear_teeth,
                "material": "Bronze with oil lubrication"
            },
            "leg_mechanism_gears": {
                "ratio": leg_gear_ratio,
                "material": "Bronze",
                "arrangement": "Bevel gears for rotary to linear conversion"
            },
            "chest_mechanism_gears": {
                "ratio": chest_gear_ratio,
                "material": "Bronze",
                "arrangement": "Worm gear for smooth operation"
            },
            "lily_platform_gears": {
                "ratio": lily_gear_ratio,
                "material": "Bronze",
                "arrangement": "Spur gears with rack and pinion"
            },
            "overall_efficiency": 0.85  # Renaissance gear efficiency
        }

    def calculate_performance(self) -> Dict:
        """Calculate system performance metrics."""

        # Energy delivery profile
        total_energy = self.main_spring.energy_capacity_j * SPRING_EFFICIENCY
        operating_time = total_energy / (PEAK_POWER_REQUIRED + self.escapement.power_consumption_w)

        # Power delivery at different stages
        walking_power = PEAK_POWER_REQUIRED * 0.7  # 70% of peak for walking
        chest_power = PEAK_POWER_REQUIRED * 0.9   # 90% of peak for chest opening
        lily_power = PEAK_POWER_REQUIRED * 0.5    # 50% of peak for lily elevation

        # Performance summary
        performance = {
            "total_energy_stored_j": total_energy,
            "usable_operating_time_s": operating_time,
            "peak_power_delivery_w": self.main_spring.max_torque_nm * ESCAPEMENT_FREQUENCY,
            "walking_power_w": walking_power,
            "chest_power_w": chest_power,
            "lily_power_w": lily_power,
            "meets_performance_requirements": operating_time >= PERFORMANCE_DURATION,
            "power_reserve_percentage": ((operating_time - PERFORMANCE_DURATION) / PERFORMANCE_DURATION) * 100
        }

        return performance

    def get_manufacturing_analysis(self) -> Dict:
        """Analyze manufacturing requirements and feasibility."""

        # Spring manufacturing (Leonardo's expertise)
        spring_difficulty = "High - requires skilled spring maker"
        spring_tools = ["Forge", "Draw bench", "Coiling mandrel", "Tempering furnace"]
        spring_time = "2-3 weeks for spring master"

        # Gear manufacturing
        gear_difficulty = "Medium - standard clockmaker skills"
        gear_tools = ["Gear cutters", "Lathe", "Files", "Dividing head"]
        gear_time = "1-2 weeks for gear train"

        # Assembly and tuning
        assembly_difficulty = "High - precise alignment required"
        assembly_time = "1 week for final assembly and tuning"

        return {
            "spring_manufacturing": {
                "difficulty": spring_difficulty,
                "required_tools": spring_tools,
                "estimated_time": spring_time,
                "renaissance_feasibility": "Feasible - Leonardo had spring expertise"
            },
            "gear_manufacturing": {
                "difficulty": gear_difficulty,
                "required_tools": gear_tools,
                "estimated_time": gear_time,
                "renaissance_feasibility": "Feasible - standard clockmaker technology"
            },
            "assembly": {
                "difficulty": assembly_difficulty,
                "estimated_time": assembly_time,
                "renaissance_feasibility": "Feasible with Leonardo's workshop"
            },
            "total_construction_time": "4-6 weeks",
            "required_expertise": ["Spring maker", "Clockmaker", "Mechanical assembler"]
        }

    def get_system_summary(self) -> Dict:
        """Get comprehensive system summary."""

        performance = self.calculate_performance()
        manufacturing = self.get_manufacturing_analysis()

        return {
            "main_spring": {
                "wire_diameter_mm": self.main_spring.wire_diameter_mm,
                "outer_radius_m": self.main_spring.mean_radius_m,
                "active_coils": self.main_spring.active_coils,
                "energy_capacity_j": self.main_spring.energy_capacity_j,
                "mass_kg": self.main_spring.mass_kg,
                "max_torque_nm": self.main_spring.max_torque_nm
            },
            "escapement": {
                "type": self.escapement.type,
                "regulation_accuracy_percent": self.escapement.regulation_accuracy_percent,
                "power_consumption_w": self.escapement.power_consumption_w
            },
            "winding": {
                "human_effort_feasible": self.winding_mechanism["is_human_feasible"],
                "winding_time_s": self.winding_mechanism["winding_time_s"],
                "handle_turns": self.winding_mechanism["handle_turns_required"]
            },
            "performance": performance,
            "manufacturing": manufacturing,
            "advantages": [
                "High energy density in compact form",
                "Consistent power delivery through escapement",
                "Proven Renaissance technology",
                "Relatively quick reset between performances",
                "Leonardo's demonstrated expertise"
            ],
            "disadvantages": [
                "Complex spring manufacturing",
                "Requires careful tuning",
                "Spring fatigue over time",
                "Potential for sudden energy release if failed"
            ]
        }

def main():
    """Main function to demonstrate spring system design."""

    print("Leonardo's Mechanical Lion - Spring-Wound Power System Design")
    print("=" * 70)

    spring_system = SpringPowerSystem()
    summary = spring_system.get_system_summary()

    # Display spring specifications
    print("\nMain Power Spring Specifications:")
    print("-" * 40)
    spring = summary["main_spring"]
    print(f"Wire Diameter: {spring['wire_diameter_mm']:.1f} mm")
    print(f"Outer Radius: {spring['outer_radius_m']:.3f} m")
    print(f"Active Coils: {spring['active_coils']}")
    print(f"Energy Capacity: {spring['energy_capacity_j']:.1f} J")
    print(f"Spring Mass: {spring['mass_kg']:.2f} kg")
    print(f"Maximum Torque: {spring['max_torque_nm']:.1f} N·m")

    # Display performance
    print(f"\nPerformance Characteristics:")
    print("-" * 40)
    perf = summary["performance"]
    print(f"Usable Operating Time: {perf['usable_operating_time_s']:.1f} s")
    print(f"Peak Power Delivery: {perf['peak_power_delivery_w']:.1f} W")
    print(f"Meets Requirements: {'✓' if perf['meets_performance_requirements'] else '✗'}")
    print(f"Power Reserve: {perf['power_reserve_percentage']:.1f}%")

    # Display winding analysis
    print(f"\nWinding Mechanism:")
    print("-" * 40)
    winding = summary["winding"]
    print(f"Human Effort Feasible: {'✓' if winding['human_effort_feasible'] else '✗'}")
    print(f"Winding Time: {winding['winding_time_s']:.1f} seconds")
    print(f"Handle Turns Required: {winding['handle_turns']:.0f}")

    # Display manufacturing analysis
    print(f"\nManufacturing Analysis:")
    print("-" * 40)
    manuf = summary["manufacturing"]
    print(f"Total Construction Time: {manuf['total_construction_time']}")
    print(f"Required Expertise: {', '.join(manuf['required_expertise'])}")

    return spring_system

if __name__ == "__main__":
    spring_system = main()