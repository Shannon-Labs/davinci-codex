"""
Weight-Driven Power System Design for Leonardo's Mechanical Lion

This module provides a comprehensive design analysis of a weight-driven power
system as an alternative to Leonardo's preferred spring-wound mechanism.
While Leonardo was known for his spring expertise, weight-driven systems were
well-established in Renaissance clockwork and offered certain advantages.

Weight System Components:
1. Drive Weights - Cast iron or lead weights for gravitational power
2. Weight Carriage - Framework to hold and guide weights
3. Cable/Drum System - Wound cables for weight suspension
4. Regulator - Clockwork escapement for speed control
5. Reset Mechanism - Winch system for weight lifting

Design Philosophy:
Weight-driven systems were common in 16th-century clockwork and would be
familiar to Renaissance craftsmen. They provide constant force output and
simpler energy storage, though require more vertical space. Leonardo may have
considered this approach for its reliability and ease of maintenance.

Historical Context:
- Tower clocks used weight systems for centuries
- Clockmakers understood weight-driven mechanisms
- Renaissance metallurgy could produce suitable weights
- Maintenance and repair were simpler than spring systems
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Physical Constants
GRAVITY = 9.80665  # m/s²
PI = math.pi

# Material Properties (Renaissance-era materials)
CAST_IRON_DENSITY = 7200  # kg/m³
LEAD_DENSITY = 11340  # kg/m³
OAK_DENSITY = 750  # kg/m³
ROPE_STRENGTH = 5000  # N (hemp rope strength)

# Energy Requirements (from energy_budget.py)
TOTAL_ENERGY_REQUIRED = 850.0  # Joules (from energy budget)
PEAK_POWER_REQUIRED = 45.0  # Watts (from energy budget)
PERFORMANCE_DURATION = 30.0  # seconds

# Mechanical Design Parameters
CABLE_DRUM_RADIUS = 0.08  # meters
WEIGHT_DROP_HEIGHT = 1.5  # meters (must fit in lion body)
EFFICIENCY_WEIGHT_SYSTEM = 0.90  # Weight system efficiency
GEAR_RATIO_DRIVE = 8.0  # Drive train mechanical advantage

@dataclass
class WeightSpecification:
    """Specification for drive weights."""
    material: str
    density_kg_per_m3: float
    dimensions_m: Tuple[float, float, float]  # length, width, height
    mass_kg: float
    force_n: float
    energy_potential_j: float
    drop_height_m: float

@dataclass
class CableSystemSpec:
    """Cable and drum system specification."""
    cable_material: str
    cable_diameter_mm: float
    drum_radius_m: float
    drum_length_m: float
    cable_length_m: float
    safety_factor: float
    breaking_strength_n: float

@dataclass
class RegulatorSpec:
    """Regulation mechanism specification."""
    type: str
    control_method: str
    regulation_accuracy_percent: float
    power_consumption_w: float
    complexity_level: str

class WeightPowerSystem:
    """
    Complete weight-driven power system design for the Mechanical Lion.

    This class designs a weight-driven system using gravitational potential
    energy storage, providing constant force output and reliable performance
    suitable for Renaissance manufacturing capabilities.
    """

    def __init__(self):
        self.drive_weights: List[WeightSpecification] = []
        self.cable_system: CableSystemSpec = None
        self.regulator: RegulatorSpec = None
        self.reset_mechanism: Dict = {}
        self._design_weight_system()

    def _design_weight_system(self) -> None:
        """Design the complete weight power system."""

        # Design drive weights
        self._design_drive_weights()

        # Design cable and drum system
        self._design_cable_system()

        # Design regulation mechanism
        self._design_regulator()

        # Design reset mechanism
        self._design_reset_mechanism()

    def _design_drive_weights(self) -> None:
        """Design optimal weight configuration."""

        # Calculate required weight for energy storage
        # E = m * g * h where E is energy, m is mass, g is gravity, h is height
        target_energy = TOTAL_ENERGY_REQUIRED * 1.3  # 30% safety margin
        effective_energy = target_energy / EFFICIENCY_WEIGHT_SYSTEM

        # Calculate required mass
        required_mass = effective_energy / (GRAVITY * WEIGHT_DROP_HEIGHT)

        # Design weight configuration
        # Use multiple smaller weights for better control and safety
        num_weights = 3  # Three weights for distributed load
        mass_per_weight = required_mass / num_weights

        # Material selection - Cast iron (common in Renaissance)
        material = "Cast iron"
        density = CAST_IRON_DENSITY

        # Calculate weight dimensions
        # Make weights compact but manageable
        weight_volume = mass_per_weight / density
        weight_side = weight_volume ** (1/3)  # Cube dimensions

        # Optimize dimensions for practical handling
        if weight_side > 0.3:  # Maximum 30cm per side
            weight_side = 0.3
            # Increase thickness instead
            base_area = weight_side ** 2
            thickness = weight_volume / base_area
            dimensions = (weight_side, weight_side, thickness)
        else:
            dimensions = (weight_side, weight_side, weight_side)

        # Create weight specifications
        for i in range(num_weights):
            weight = WeightSpecification(
                material=material,
                density_kg_per_m3=density,
                dimensions_m=dimensions,
                mass_kg=mass_per_weight,
                force_n=mass_per_weight * GRAVITY,
                energy_potential_j=mass_per_weight * GRAVITY * WEIGHT_DROP_HEIGHT,
                drop_height_m=WEIGHT_DROP_HEIGHT
            )
            self.drive_weights.append(weight)

    def _design_cable_system(self) -> None:
        """Design cable and drum system."""

        # Cable material - Hemp rope (Renaissance standard)
        cable_material = "Hemp rope"
        cable_diameter = 12.0  # mm (substantial for safety)

        # Calculate total load
        total_force = sum(weight.force_n for weight in self.drive_weights)

        # Calculate required breaking strength
        safety_factor = 8.0  # High safety factor for royal performance
        breaking_strength = total_force * safety_factor

        # Verify rope capacity
        if breaking_strength > ROPE_STRENGTH:
            # Increase rope diameter or number of ropes
            cable_diameter = 16.0  # mm
            breaking_strength = ROPE_STRENGTH * (cable_diameter / 12.0) ** 2

        # Drum design
        drum_radius = CABLE_DRUM_RADIUS
        drum_length = 0.2  # meters (to accommodate multiple cables)

        # Calculate cable length
        # Include extra for connections and wraps
        cable_length = WEIGHT_DROP_HEIGHT * 1.5

        self.cable_system = CableSystemSpec(
            cable_material=cable_material,
            cable_diameter_mm=cable_diameter,
            drum_radius_m=drum_radius,
            drum_length_m=drum_length,
            cable_length_m=cable_length,
            safety_factor=safety_factor,
            breaking_strength_n=breaking_strength
        )

    def _design_regulator(self) -> None:
        """Design regulation mechanism for constant speed."""

        # Use a crown wheel escapement (common in weight-driven clocks)
        # This provides reliable regulation for constant performance

        regulator_type = "Crown wheel escapement with verge"
        control_method = "Gravity-powered regulation"
        regulation_accuracy = 3.0  # ±3% (better than spring systems)
        power_consumption = 2.0  # Watts (lower than spring escapement)
        complexity = "Medium - standard clockmaker technology"

        self.regulator = RegulatorSpec(
            type=regulator_type,
            control_method=control_method,
            regulation_accuracy_percent=regulation_accuracy,
            power_consumption_w=power_consumption,
            complexity_level=complexity
        )

    def _design_reset_mechanism(self) -> None:
        """Design mechanism for resetting weights between performances."""

        # Total weight to lift
        total_mass = sum(weight.mass_kg for weight in self.drive_weights)
        total_force = total_mass * GRAVITY

        # Winch design for human operation
        winch_handle_radius = 0.2  # meters
        mechanical_advantage = 12.0  # Pulley system

        # Calculate human effort
        human_force_required = total_force / mechanical_advantage
        human_torque_required = human_force_required * winch_handle_radius

        # Number of handle turns
        cable_length_per_weight = WEIGHT_DROP_HEIGHT
        drum_circumference = 2 * PI * self.cable_system.drum_radius_m
        drum_rotations = cable_length_per_weight / drum_circumference
        handle_turns = drum_rotations * mechanical_advantage

        # Reset time
        reset_time = handle_turns / 2.0  # 2 turns per second

        self.reset_mechanism = {
            "total_mass_kg": total_mass,
            "total_force_n": total_force,
            "winch_handle_radius_m": winch_handle_radius,
            "mechanical_advantage": mechanical_advantage,
            "human_force_required_n": human_force_required,
            "human_torque_required_nm": human_torque_required,
            "handle_turns_required": handle_turns,
            "reset_time_s": reset_time,
            "is_human_feasible": human_torque_required < 60.0  # 60 N·m reasonable limit
        }

    def calculate_performance(self) -> Dict:
        """Calculate system performance metrics."""

        # Total energy available
        total_energy = sum(weight.energy_potential_j for weight in self.drive_weights)
        effective_energy = total_energy * EFFICIENCY_WEIGHT_SYSTEM

        # Constant force output
        total_force = sum(weight.force_n for weight in self.drive_weights)

        # Torque at drum
        drum_torque = total_force * self.cable_system.drum_radius_m

        # Power output (before regulation)
        mechanical_power = drum_torque * (WEIGHT_DROP_HEIGHT / PERFORMANCE_DURATION)

        # Regulated power output
        regulated_power = mechanical_power - self.regulator.power_consumption_w

        # Operating time
        operating_time = effective_energy / regulated_power

        # Performance summary
        performance = {
            "total_energy_stored_j": total_energy,
            "effective_energy_j": effective_energy,
            "constant_force_n": total_force,
            "drum_torque_nm": drum_torque,
            "regulated_power_w": regulated_power,
            "operating_time_s": operating_time,
            "meets_performance_requirements": operating_time >= PERFORMANCE_DURATION,
            "power_reserve_percentage": ((operating_time - PERFORMANCE_DURATION) / PERFORMANCE_DURATION) * 100,
            "force_consistency": "Excellent (constant gravitational force)"
        }

        return performance

    def get_space_requirements(self) -> Dict:
        """Calculate space requirements within lion body."""

        # Weight stack dimensions
        total_weight_volume = sum(
            weight.dimensions_m[0] * weight.dimensions_m[1] * weight.dimensions_m[2]
            for weight in self.drive_weights
        )

        # Weight carriage dimensions (with clearance)
        carriage_clearance = 0.05  # meters
        carriage_width = max(w.dimensions_m[0] for w in self.drive_weights) + 2 * carriage_clearance
        carriage_depth = max(w.dimensions_m[1] for w in self.drive_weights) + 2 * carriage_clearance
        carriage_height = WEIGHT_DROP_HEIGHT + 0.3  # Extra space for mechanisms

        # Drum and mechanism space
        drum_space_width = self.cable_system.drum_length_m + 0.1
        drum_space_depth = self.cable_system.drum_radius_m * 2 + 0.1
        drum_space_height = self.cable_system.drum_radius_m * 2 + 0.1

        # Total space requirements
        total_volume = carriage_width * carriage_depth * carriage_height + drum_space_width * drum_space_depth * drum_space_height

        return {
            "weight_carriage": {
                "width_m": carriage_width,
                "depth_m": carriage_depth,
                "height_m": carriage_height,
                "volume_m3": carriage_width * carriage_depth * carriage_height
            },
            "drum_mechanism": {
                "width_m": drum_space_width,
                "depth_m": drum_space_depth,
                "height_m": drum_space_height,
                "volume_m3": drum_space_width * drum_space_depth * drum_space_height
            },
            "total_volume_m3": total_volume,
            "fits_in_lion_body": total_volume < 0.5  # Less than 0.5 m³
        }

    def get_manufacturing_analysis(self) -> Dict:
        """Analyze manufacturing requirements and feasibility."""

        # Weight casting
        casting_difficulty = "Medium - standard foundry work"
        casting_tools = ["Foundry furnace", "Cast iron molds", "Finishing tools"]
        casting_time = "1 week for weight production"

        # Cable making
        cable_difficulty = "Low - rope making was common"
        cable_tools = ["Rope walk", "Hemp processing", "Finishing tools"]
        cable_time = "2-3 days for cable production"

        # Mechanism fabrication
        mechanism_difficulty = "Medium - clockmaker skills"
        mechanism_tools = ["Lathe", "Gear cutters", "Files", "Drill"]
        mechanism_time = "2 weeks for mechanism"

        return {
            "weight_casting": {
                "difficulty": casting_difficulty,
                "required_tools": casting_tools,
                "estimated_time": casting_time,
                "renaissance_feasibility": "Feasible - standard foundry technology"
            },
            "cable_production": {
                "difficulty": cable_difficulty,
                "required_tools": cable_tools,
                "estimated_time": cable_time,
                "renaissance_feasibility": "Feasible - common rope making"
            },
            "mechanism_fabrication": {
                "difficulty": mechanism_difficulty,
                "required_tools": mechanism_tools,
                "estimated_time": mechanism_time,
                "renaissance_feasibility": "Feasible - clockmaker technology"
            },
            "total_construction_time": "3-4 weeks",
            "required_expertise": ["Foundry worker", "Rope maker", "Clockmaker"]
        }

    def get_system_summary(self) -> Dict:
        """Get comprehensive system summary."""

        performance = self.calculate_performance()
        space = self.get_space_requirements()
        manufacturing = self.get_manufacturing_analysis()

        # Calculate total weight
        total_mass = sum(weight.mass_kg for weight in self.drive_weights)

        return {
            "drive_weights": {
                "num_weights": len(self.drive_weights),
                "individual_mass_kg": self.drive_weights[0].mass_kg,
                "total_mass_kg": total_mass,
                "material": self.drive_weights[0].material,
                "drop_height_m": WEIGHT_DROP_HEIGHT
            },
            "cable_system": {
                "material": self.cable_system.cable_material,
                "diameter_mm": self.cable_system.cable_diameter_mm,
                "drum_radius_m": self.cable_system.drum_radius_m,
                "safety_factor": self.cable_system.safety_factor
            },
            "regulator": {
                "type": self.regulator.type,
                "accuracy_percent": self.regulator.regulation_accuracy_percent,
                "power_consumption_w": self.regulator.power_consumption_w
            },
            "reset": {
                "human_feasible": self.reset_mechanism["is_human_feasible"],
                "reset_time_s": self.reset_mechanism["reset_time_s"],
                "effort_required": "Moderate - requires winch system"
            },
            "performance": performance,
            "space_requirements": space,
            "manufacturing": manufacturing,
            "advantages": [
                "Constant force output (excellent consistency)",
                "Simple and reliable technology",
                "Easy to understand and maintain",
                "No spring fatigue or failure concerns",
                "Better regulation accuracy than springs",
                "Standard Renaissance clockwork technology"
            ],
            "disadvantages": [
                "Requires significant vertical space",
                "Heavy weights increase overall lion mass",
                "Slower reset between performances",
                "Limited energy density compared to springs",
                "Weight carriage complexity",
                "Potential for cable wear over time"
            ]
        }

def main():
    """Main function to demonstrate weight system design."""

    print("Leonardo's Mechanical Lion - Weight-Driven Power System Design")
    print("=" * 70)

    weight_system = WeightPowerSystem()
    summary = weight_system.get_system_summary()

    # Display weight specifications
    print("\nDrive Weights Configuration:")
    print("-" * 40)
    weights = summary["drive_weights"]
    print(f"Number of Weights: {weights['num_weights']}")
    print(f"Individual Weight Mass: {weights['individual_mass_kg']:.1f} kg")
    print(f"Total Weight Mass: {weights['total_mass_kg']:.1f} kg")
    print(f"Material: {weights['material']}")
    print(f"Drop Height: {weights['drop_height_m']:.2f} m")

    # Display performance
    print(f"\nPerformance Characteristics:")
    print("-" * 40)
    perf = summary["performance"]
    print(f"Effective Energy: {perf['effective_energy_j']:.1f} J")
    print(f"Constant Force: {perf['constant_force_n']:.1f} N")
    print(f"Regulated Power: {perf['regulated_power_w']:.1f} W")
    print(f"Operating Time: {perf['operating_time_s']:.1f} s")
    print(f"Meets Requirements: {'✓' if perf['meets_performance_requirements'] else '✗'}")
    print(f"Force Consistency: {perf['force_consistency']}")

    # Display space requirements
    print(f"\nSpace Requirements:")
    print("-" * 40)
    space = summary["space_requirements"]
    print(f"Total Volume: {space['total_volume_m3']:.3f} m³")
    print(f"Fits in Lion Body: {'✓' if space['fits_in_lion_body'] else '✗'}")
    print(f"Weight Carriage Height: {space['weight_carriage']['height_m']:.2f} m")

    # Display reset analysis
    print(f"\nReset Mechanism:")
    print("-" * 40)
    reset = summary["reset"]
    print(f"Human Feasible: {'✓' if reset['human_feasible'] else '✗'}")
    print(f"Reset Time: {reset['reset_time_s']:.1f} seconds")
    print(f"Effort Required: {reset['effort_required']}")

    # Display manufacturing analysis
    print(f"\nManufacturing Analysis:")
    print("-" * 40)
    manuf = summary["manufacturing"]
    print(f"Total Construction Time: {manuf['total_construction_time']}")
    print(f"Required Expertise: {', '.join(manuf['required_expertise'])}")

    return weight_system

if __name__ == "__main__":
    weight_system = main()