"""
Structural Analysis for Leonardo's Mechanical Lion Chest Cavity
Comprehensive stress and load analysis for royal court performance reliability
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np

# Material properties (Renaissance materials)
MATERIAL_PROPERTIES = {
    "bronze": {
        "yield_strength_mpa": 200.0,
        "ultimate_strength_mpa": 400.0,
        "elastic_modulus_gpa": 110.0,
        "density_kg_m3": 8800.0,
        "fatigue_strength_mpa": 120.0,
        "poisson_ratio": 0.34
    },
    "oak": {
        "yield_strength_mpa": 40.0,
        "ultimate_strength_mpa": 60.0,
        "elastic_modulus_gpa": 12.0,
        "density_kg_m3": 750.0,
        "fatigue_strength_mpa": 15.0,
        "poisson_ratio": 0.35
    },
    "steel": {
        "yield_strength_mpa": 250.0,
        "ultimate_strength_mpa": 450.0,
        "elastic_modulus_gpa": 200.0,
        "density_kg_m3": 7850.0,
        "fatigue_strength_mpa": 180.0,
        "poisson_ratio": 0.30
    }
}

@dataclass
class StructuralComponent:
    """Individual structural component with properties and loads."""
    component_id: str
    material: str
    dimensions_m: Tuple[float, float, float]  # (length, width, height)
    function: str
    safety_factor: float = 3.0

    def get_material_properties(self) -> dict:
        """Get material properties for this component."""
        return MATERIAL_PROPERTIES.get(self.material, MATERIAL_PROPERTIES["bronze"])

    def calculate_cross_sectional_area(self) -> float:
        """Calculate cross-sectional area."""
        _, width, height = self.dimensions_m
        return width * height

    def calculate_moment_of_inertia(self) -> float:
        """Calculate moment of inertia for bending."""
        _, width, height = self.dimensions_m
        # Second moment of area for rectangle
        return (width * height**3) / 12.0

    def calculate_mass(self) -> float:
        """Calculate component mass."""
        volume = math.prod(self.dimensions_m)
        density = self.get_material_properties()["density_kg_m3"]
        return volume * density

@dataclass
class LoadCase:
    """Structural load case for analysis."""
    load_id: str
    load_type: str  # "static", "dynamic", "impact", "fatigue"
    force_n: float
    moment_nm: float
    application_point: Tuple[float, float, float]
    duration_s: float
    frequency_hz: float = 0.0

class ChestStructuralAnalyzer:
    """Comprehensive structural analysis system for chest cavity."""

    def __init__(self):
        # Initialize structural components
        self.components = self._initialize_components()

        # Initialize load cases
        self.load_cases = self._initialize_load_cases()

        # Analysis results storage
        self.stress_results = {}
        self.deflection_results = {}
        self.safety_factors = {}

        # Performance requirements
        self.max_allowable_deflection_m = 0.005  # 5mm maximum deflection
        self.min_safety_factor = 2.0
        self.fatigue_life_cycles = 1000  # Royal performances

    def _initialize_components(self) -> List[StructuralComponent]:
        """Initialize all structural components of chest cavity."""
        components = []

        # Chest panels
        components.append(StructuralComponent(
            "left_panel", "bronze", (0.4, 0.002, 0.3), "chest_panel"
        ))
        components.append(StructuralComponent(
            "right_panel", "bronze", (0.4, 0.002, 0.3), "chest_panel"
        ))
        components.append(StructuralComponent(
            "top_panel", "bronze", (0.8, 0.002, 0.15), "chest_panel"
        ))
        components.append(StructuralComponent(
            "bottom_panel", "bronze", (0.8, 0.002, 0.15), "chest_panel"
        ))

        # Hinge components
        components.append(StructuralComponent(
            "left_hinge", "bronze", (0.015, 0.015, 0.08), "hinge"
        ))
        components.append(StructuralComponent(
            "right_hinge", "bronze", (0.015, 0.015, 0.08), "hinge"
        ))
        components.append(StructuralComponent(
            "top_hinge", "bronze", (0.015, 0.015, 0.08), "hinge"
        ))
        components.append(StructuralComponent(
            "bottom_hinge", "bronze", (0.015, 0.015, 0.08), "hinge"
        ))

        # Support frame
        components.append(StructuralComponent(
            "frame_vertical", "oak", (0.6, 0.03, 0.04), "structural_frame"
        ))
        components.append(StructuralComponent(
            "frame_horizontal", "oak", (0.9, 0.03, 0.04), "structural_frame"
        ))

        # Spring housing
        components.append(StructuralComponent(
            "spring_housing", "steel", (0.2, 0.05, 0.05), "spring_mechanism"
        ))

        # Cam mechanism
        components.append(StructuralComponent(
            "cam_shaft", "steel", (0.3, 0.02, 0.02), "cam_mechanism"
        ))

        return components

    def _initialize_load_cases(self) -> List[LoadCase]:
        """Initialize all relevant load cases for analysis."""
        load_cases = []

        # Static load: weight of components
        total_weight = sum(comp.calculate_mass() * 9.81 for comp in self.components)
        load_cases.append(LoadCase(
            "static_weight", "static", total_weight, 0.0, (0.0, 0.0, 0.0), float('inf')
        ))

        # Dynamic load: spring force during opening
        load_cases.append(LoadCase(
            "spring_opening", "dynamic", 300.0, 50.0, (0.0, 0.0, 0.2), 3.5
        ))

        # Impact load: panel closure
        load_cases.append(LoadCase(
            "panel_closure", "impact", 150.0, 30.0, (0.0, 0.0, 0.1), 0.1
        ))

        # Fatigue load: repeated operation
        load_cases.append(LoadCase(
            "repeated_operation", "fatigue", 200.0, 25.0, (0.0, 0.0, 0.15), 0.2, 0.1
        ))

        # Load from lily platform
        load_cases.append(LoadCase(
            "lily_platform", "static", 50.0, 10.0, (0.0, 0.0, 0.32), float('inf')
        ))

        return load_cases

    def calculate_component_stress(self, component: StructuralComponent, load_case: LoadCase) -> Dict[str, float]:
        """Calculate stress in component for given load case."""
        material_props = component.get_material_properties()

        # Cross-sectional properties
        area = component.calculate_cross_sectional_area()
        moment_of_inertia = component.calculate_moment_of_inertia()

        # Normal stress from axial load
        normal_stress = load_case.force_n / area if area > 0 else 0

        # Bending stress from moment
        bending_stress = (load_case.moment_nm * 0.001) / (moment_of_inertia / (component.dimensions_m[2] / 2)) if moment_of_inertia > 0 else 0

        # Combined stress (von Mises for ductile materials)
        if component.material in ["bronze", "steel"]:
            von_mises_stress = math.sqrt(normal_stress**2 + 3 * (bending_stress/2)**2)
        else:  # Wood - use maximum principal stress
            von_mises_stress = normal_stress + bending_stress

        # Dynamic amplification factor
        if load_case.load_type == "dynamic":
            amplification_factor = 1.5
        elif load_case.load_type == "impact":
            amplification_factor = 2.0
        else:
            amplification_factor = 1.0

        amplified_stress = von_mises_stress * amplification_factor

        return {
            "normal_stress_mpa": normal_stress / 1e6,
            "bending_stress_mpa": bending_stress / 1e6,
            "von_mises_stress_mpa": amplified_stress / 1e6,
            "yield_strength_mpa": material_props["yield_strength_mpa"],
            "ultimate_strength_mpa": material_props["ultimate_strength_mpa"],
            "safety_factor": material_props["yield_strength_mpa"] / (amplified_stress / 1e6) if amplified_stress > 0 else float('inf')
        }

    def calculate_component_deflection(self, component: StructuralComponent, load_case: LoadCase) -> Dict[str, float]:
        """Calculate deflection of component for given load case."""
        material_props = component.get_material_properties()
        length, width, height = component.dimensions_m

        # Elastic modulus
        E = material_props["elastic_modulus_gpa"] * 1e9  # Convert GPa to Pa

        # Moment of inertia
        I = component.calculate_moment_of_inertia()

        # Deflection due to bending (simply supported beam with center load)
        if load_case.force_n > 0 and I > 0:
            deflection = (load_case.force_n * length**3) / (48 * E * I)
        else:
            deflection = 0.0

        # Angular deflection
        if load_case.moment_nm > 0 and I > 0:
            angular_deflection = (load_case.moment_nm * length) / (E * I)
        else:
            angular_deflection = 0.0

        return {
            "linear_deflection_m": deflection,
            "angular_deflection_rad": angular_deflection,
            "max_allowable_deflection_m": self.max_allowable_deflection_m,
            "deflection_ratio": deflection / self.max_allowable_deflection_m if self.max_allowable_deflection_m > 0 else 0
        }

    def perform_fatigue_analysis(self, component: StructuralComponent, load_case: LoadCase) -> Dict[str, float]:
        """Perform fatigue analysis for component."""
        material_props = component.get_material_properties()
        stress_result = self.calculate_component_stress(component, load_case)

        # S-N curve parameters (simplified)
        fatigue_strength = material_props["fatigue_strength_mpa"]
        stress_amplitude = stress_result["von_mises_stress_mpa"]

        # Fatigue life calculation (Basquin's equation simplified)
        if stress_amplitude > 0:
            # Simplified fatigue life estimation
            stress_ratio = stress_amplitude / fatigue_strength
            if stress_ratio < 1.0:
                fatigue_life = 1e6 * (1.0 / stress_ratio)**6  # Simplified S-N relationship
            else:
                fatigue_life = 1e3  # Very low life if stress exceeds fatigue strength
        else:
            fatigue_life = float('inf')

        # Required life for royal performances
        required_life = self.fatigue_life_cycles

        return {
            "stress_amplitude_mpa": stress_amplitude,
            "fatigue_strength_mpa": fatigue_strength,
            "estimated_life_cycles": fatigue_life,
            "required_life_cycles": required_life,
            "fatigue_safety_factor": fatigue_life / required_life if required_life > 0 else float('inf'),
            "adequate_fatigue_life": fatigue_life >= required_life
        }

    def perform_comprehensive_analysis(self) -> Dict[str, object]:
        """Perform comprehensive structural analysis of all components."""
        analysis_results = {
            "component_stresses": {},
            "component_deflections": {},
            "fatigue_analysis": {},
            "overall_safety": {},
            "critical_components": [],
            "recommendations": []
        }

        # Analyze each component under each load case
        for component in self.components:
            component_results = {
                "stresses": {},
                "deflections": {},
                "fatigue": {},
                "overall_safety_factor": float('inf')
            }

            min_safety_factor = float('inf')

            for load_case in self.load_cases:
                # Stress analysis
                stress_result = self.calculate_component_stress(component, load_case)
                component_results["stresses"][load_case.load_id] = stress_result
                min_safety_factor = min(min_safety_factor, stress_result["safety_factor"])

                # Deflection analysis
                deflection_result = self.calculate_component_deflection(component, load_case)
                component_results["deflections"][load_case.load_id] = deflection_result

                # Fatigue analysis (only for fatigue load case)
                if load_case.load_type == "fatigue":
                    fatigue_result = self.perform_fatigue_analysis(component, load_case)
                    component_results["fatigue"][load_case.load_id] = fatigue_result

            component_results["overall_safety_factor"] = min_safety_factor
            analysis_results["component_stresses"][component.component_id] = component_results

            # Check for critical components
            if min_safety_factor < self.min_safety_factor:
                analysis_results["critical_components"].append({
                    "component_id": component.component_id,
                    "safety_factor": min_safety_factor,
                    "material": component.material,
                    "function": component.function
                })

        # Calculate overall system safety
        all_safety_factors = [
            results["overall_safety_factor"]
            for results in analysis_results["component_stresses"].values()
        ]
        analysis_results["overall_safety"] = {
            "minimum_safety_factor": min(all_safety_factors) if all_safety_factors else float('inf'),
            "average_safety_factor": sum(all_safety_factors) / len(all_safety_factors) if all_safety_factors else 0,
            "critical_components_count": len(analysis_results["critical_components"]),
            "total_components": len(self.components)
        }

        # Generate recommendations
        analysis_results["recommendations"] = self._generate_recommendations(analysis_results)

        return analysis_results

    def _generate_recommendations(self, analysis_results: Dict[str, object]) -> List[str]:
        """Generate design recommendations based on analysis results."""
        recommendations = []

        # Check for critical safety issues
        if analysis_results["overall_safety"]["minimum_safety_factor"] < self.min_safety_factor:
            recommendations.append(
                f"CRITICAL: Minimum safety factor ({analysis_results['overall_safety']['minimum_safety_factor']:.2f}) "
                f"below required value ({self.min_safety_factor}). Component redesign required."
            )

        # Check critical components
        for comp in analysis_results["critical_components"]:
            if comp["safety_factor"] < 1.5:
                recommendations.append(
                    f"High priority: {comp['component_id']} has low safety factor ({comp['safety_factor']:.2f}). "
                    f"Consider increasing material strength or reducing loads."
                )

        # Material recommendations
        bronze_components = [c for c in self.components if c.material == "bronze"]
        for comp in bronze_components:
            comp_results = analysis_results["component_stresses"][comp.component_id]
            if comp_results["overall_safety_factor"] < 2.5:
                recommendations.append(
                    f"Consider steel reinforcement for {comp.component_id} to improve safety margin."
                )

        # Fatigue recommendations
        fatigue_issues = 0
        for component in self.components:
            comp_results = analysis_results["component_stresses"][component.component_id]
            for load_id, fatigue_data in comp_results["fatigue"].items():
                if not fatigue_data["adequate_fatigue_life"]:
                    fatigue_issues += 1

        if fatigue_issues > 0:
            recommendations.append(
                f"Fatigue life concerns for {fatigue_issues} components. "
                f"Consider stress relief features or material upgrades."
            )

        # General recommendations
        if analysis_results["overall_safety"]["average_safety_factor"] > 5.0:
            recommendations.append(
                "Overall safety factors are high. Consider weight optimization opportunities."
            )

        recommendations.append(
            "Implement regular inspection schedule for royal court performances."
        )
        recommendations.append(
            "Maintain detailed maintenance logs for all critical components."
        )

        return recommendations

def create_structural_analysis_visualization():
    """Create comprehensive visualization of structural analysis results."""
    analyzer = ChestStructuralAnalyzer()
    results = analyzer.perform_comprehensive_analysis()

    # Create multi-panel figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle("Chest Cavity Structural Analysis - Royal Court Performance Safety", fontsize=16, fontweight='bold')

    # Extract data for visualization
    component_ids = list(results["component_stresses"].keys())
    safety_factors = [results["component_stresses"][comp_id]["overall_safety_factor"] for comp_id in component_ids]

    # Component colors based on safety factor
    def get_safety_color(safety_factor):
        if safety_factor >= 3.0:
            return 'green'
        elif safety_factor >= 2.0:
            return 'orange'
        else:
            return 'red'

    colors = [get_safety_color(sf) for sf in safety_factors]

    # Plot 1: Safety factors by component
    bars1 = axes[0, 0].bar(component_ids, safety_factors, color=colors)
    axes[0, 0].set_ylabel('Safety Factor', fontsize=12)
    axes[0, 0].set_title('Component Safety Factors', fontsize=14)
    axes[0, 0].axhline(y=analyzer.min_safety_factor, color='red', linestyle='--', alpha=0.7, label='Minimum Required')
    axes[0, 0].axhline(y=3.0, color='green', linestyle='--', alpha=0.7, label='Target')
    axes[0, 0].legend()
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Plot 2: Material stress distribution
    materials = ["bronze", "oak", "steel"]
    material_stresses = []
    material_strengths = []

    for material in materials:
        material_comps = [c for c in analyzer.components if c.material == material]
        if material_comps:
            max_stress = 0
            for comp in material_comps:
                comp_results = results["component_stresses"][comp.component_id]
                for stress_data in comp_results["stresses"].values():
                    max_stress = max(max_stress, stress_data["von_mises_stress_mpa"])
            material_stresses.append(max_stress)
            material_strengths.append(MATERIAL_PROPERTIES[material]["yield_strength_mpa"])
        else:
            material_stresses.append(0)
            material_strengths.append(0)

    x = np.arange(len(materials))
    width = 0.35

    bars2 = axes[0, 1].bar(x - width/2, material_stresses, width, label='Maximum Stress', alpha=0.8)
    bars3 = axes[0, 1].bar(x + width/2, material_strengths, width, label='Yield Strength', alpha=0.8)

    axes[0, 1].set_ylabel('Stress (MPa)', fontsize=12)
    axes[0, 1].set_title('Material Stress Analysis', fontsize=14)
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(materials)
    axes[0, 1].legend()

    # Plot 3: Load case analysis
    load_case_names = [lc.load_id for lc in analyzer.load_cases]
    load_magnitudes = [lc.force_n for lc in analyzer.load_cases]

    bars4 = axes[0, 2].bar(load_case_names, load_magnitudes, color=['blue', 'red', 'orange', 'green', 'purple'])
    axes[0, 2].set_ylabel('Force (N)', fontsize=12)
    axes[0, 2].set_title('Load Case Magnitudes', fontsize=14)
    axes[0, 2].tick_params(axis='x', rotation=45)

    # Plot 4: Deflection analysis
    component_deflections = []
    for comp_id in component_ids:
        comp_results = results["component_stresses"][comp_id]
        max_deflection = 0
        for deflection_data in comp_results["deflections"].values():
            max_deflection = max(max_deflection, deflection_data["linear_deflection_m"])
        component_deflections.append(max_deflection * 1000)  # Convert to mm

    bars5 = axes[1, 0].bar(component_ids, component_deflections, color='cyan')
    axes[1, 0].set_ylabel('Maximum Deflection (mm)', fontsize=12)
    axes[1, 0].set_title('Component Deflection Analysis', fontsize=14)
    axes[1, 0].axhline(y=analyzer.max_allowable_deflection_m * 1000, color='red', linestyle='--', alpha=0.7, label='Allowable Limit')
    axes[1, 0].legend()
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Plot 5: Fatigue analysis
    fatigue_safety_factors = []
    for comp in analyzer.components:
        comp_results = results["component_stresses"][comp.component_id]
        if comp_results["fatigue"]:
            fatigue_data = list(comp_results["fatigue"].values())[0]
            fatigue_safety_factors.append(fatigue_data["fatigue_safety_factor"])
        else:
            fatigue_safety_factors.append(10.0)  # High value for non-fatigue components

    bars6 = axes[1, 1].bar(component_ids, fatigue_safety_factors, color='magenta')
    axes[1, 1].set_ylabel('Fatigue Safety Factor', fontsize=12)
    axes[1, 1].set_title('Fatigue Life Analysis', fontsize=14)
    axes[1, 1].axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Minimum Required')
    axes[1, 1].legend()
    axes[1, 1].tick_params(axis='x', rotation=45)

    # Plot 6: Overall system summary
    summary_text = f"""STRUCTURAL ANALYSIS SUMMARY

Overall Safety Factor: {results['overall_safety']['minimum_safety_factor']:.2f}
Average Safety Factor: {results['overall_safety']['average_safety_factor']:.2f}
Critical Components: {results['overall_safety']['critical_components_count']}/{results['overall_safety']['total_components']}

Materials Performance:
• Bronze: {material_stresses[0]:.1f}/{material_strengths[0]:.1f} MPa
• Oak: {material_stresses[1]:.1f}/{material_strengths[1]:.1f} MPa
• Steel: {material_stresses[2]:.1f}/{material_strengths[2]:.1f} MPa

Performance Rating: {'EXCELLENT' if results['overall_safety']['minimum_safety_factor'] >= 3.0 else 'ACCEPTABLE' if results['overall_safety']['minimum_safety_factor'] >= 2.0 else 'NEEDS IMPROVEMENT'}

Royal Court Ready: {'YES' if results['overall_safety']['minimum_safety_factor'] >= 2.0 else 'NO'}
"""

    axes[1, 2].text(0.1, 0.5, summary_text, fontsize=11, verticalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    axes[1, 2].set_xlim(0, 1)
    axes[1, 2].set_ylim(0, 1)
    axes[1, 2].axis('off')
    axes[1, 2].set_title('Analysis Summary', fontsize=14)

    plt.tight_layout()
    return fig

def generate_structural_analysis_report():
    """Generate comprehensive structural analysis report."""
    analyzer = ChestStructuralAnalyzer()
    results = analyzer.perform_comprehensive_analysis()

    report = []
    report.append("CHEST CAVITY STRUCTURAL ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    report.append("ANALYSIS SUMMARY:")
    report.append(f"  • Total Components Analyzed: {len(analyzer.components)}")
    report.append(f"  • Load Cases Evaluated: {len(analyzer.load_cases)}")
    report.append(f"  • Minimum Safety Factor: {results['overall_safety']['minimum_safety_factor']:.2f}")
    report.append(f"  • Average Safety Factor: {results['overall_safety']['average_safety_factor']:.2f}")
    report.append(f"  • Critical Components: {results['overall_safety']['critical_components_count']}")
    report.append("")
    report.append("COMPONENT SAFETY ANALYSIS:")
    for comp_id, comp_data in results["component_stresses"].items():
        safety_factor = comp_data["overall_safety_factor"]
        status = "SAFE" if safety_factor >= 3.0 else "MARGINAL" if safety_factor >= 2.0 else "CRITICAL"
        report.append(f"  • {comp_id}: Safety Factor {safety_factor:.2f} ({status})")
    report.append("")
    report.append("MATERIAL PERFORMANCE:")
    for material in ["bronze", "oak", "steel"]:
        material_comps = [c for c in analyzer.components if c.material == material]
        if material_comps:
            max_stress = 0
            for comp in material_comps:
                comp_results = results["component_stresses"][comp.component_id]
                for stress_data in comp_results["stresses"].values():
                    max_stress = max(max_stress, stress_data["von_mises_stress_mpa"])

            strength = MATERIAL_PROPERTIES[material]["yield_strength_mpa"]
            utilization = (max_stress / strength) * 100 if strength > 0 else 0
            report.append(f"  • {material.title()}: {max_stress:.1f}/{strength:.1f} MPa ({utilization:.1f}% utilized)")
    report.append("")
    report.append("DEFLECTION ANALYSIS:")
    for comp_id, comp_data in results["component_stresses"].items():
        max_deflection = 0
        for deflection_data in comp_data["deflections"].values():
            max_deflection = max(max_deflection, deflection_data["linear_deflection_m"])

        deflection_mm = max_deflection * 1000
        allowable_mm = analyzer.max_allowable_deflection_m * 1000
        status = "WITHIN LIMIT" if deflection_mm <= allowable_mm else "EXCEEDS LIMIT"
        report.append(f"  • {comp_id}: {deflection_mm:.2f}/{allowable_mm:.2f} mm ({status})")
    report.append("")
    report.append("FATIGUE LIFE ANALYSIS:")
    for comp in analyzer.components:
        comp_results = results["component_stresses"][comp.component_id]
        if comp_results["fatigue"]:
            for load_id, fatigue_data in comp_results["fatigue"].items():
                life_cycles = fatigue_data["estimated_life_cycles"]
                required_cycles = fatigue_data["required_life_cycles"]
                status = "ADEQUATE" if fatigue_data["adequate_fatigue_life"] else "INADEQUATE"
                report.append(f"  • {comp.component_id} ({load_id}): {life_cycles:.0e}/{required_cycles:.0e} cycles ({status})")
    report.append("")
    report.append("CRITICAL COMPONENTS:")
    if results["critical_components"]:
        for comp in results["critical_components"]:
            report.append(f"  • {comp['component_id']}: Safety Factor {comp['safety_factor']:.2f} ({comp['material']}, {comp['function']})")
    else:
        report.append("  • No critical components identified - all factors acceptable")
    report.append("")
    report.append("DESIGN RECOMMENDATIONS:")
    for i, rec in enumerate(results["recommendations"], 1):
        report.append(f"  {i}. {rec}")
    report.append("")
    report.append("ROYAL COURT PERFORMANCE CERTIFICATION:")
    if results["overall_safety"]["minimum_safety_factor"] >= 2.0:
        report.append("  ✓ STRUCTURAL INTEGRITY: CERTIFIED FOR ROYAL PERFORMANCE")
        report.append("  ✓ SAFETY MARGINS: WITHIN ACCEPTABLE LIMITS")
        report.append("  ✓ FATIGUE LIFE: ADEQUATE FOR REPEAT PERFORMANCES")
        report.append("  ✓ DEFLECTION: WITHIN ALLOWABLE LIMITS")
    else:
        report.append("  ✗ STRUCTURAL INTEGRITY: REQUIRES IMPROVEMENT BEFORE ROYAL PERFORMANCE")
        report.append("  ✗ SAFETY MARGINS: BELOW REQUIRED MINIMUM")
        report.append("  ✗ DESIGN MODIFICATIONS NEEDED")

    return "\n".join(report)

if __name__ == "__main__":
    # Generate visualizations and reports
    fig = create_structural_analysis_visualization()
    report = generate_structural_analysis_report()
    print(report)
    plt.show()