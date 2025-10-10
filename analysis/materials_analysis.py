"""
Leonardo da Vinci's Definitive Materials Analysis for Aerial Screw Construction

This comprehensive analysis bridges Renaissance-era material capabilities with modern 
engineering requirements for the aerial screw. As Leonardo, I must carefully consider
what materials my workshop can actually procure and work with, while understanding 
the demanding requirements of flight.

Historical Context: Milan, circa 1485-1490
Workshop Capabilities: Basic hand tools, forge, woodworking, textile processing
Available Materials: Wood, linen, leather, bronze, iron, basic textiles
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import math
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# === RENAISSANCE MATERIAL DATABASE ===
# Based on historical records of Milanese workshop capabilities, circa 1490

@dataclass
class Material:
    """Material properties available in Renaissance Milan"""
    name: str
    density_kg_m3: float  # kg/m³
    elastic_modulus_pa: float  # Pa
    tensile_strength_pa: float  # Pa
    compressive_strength_pa: float  # Pa
    cost_relative: float  # Relative to oak = 1.0
    availability: str  # "abundant", "common", "scarce", "rare"
    workability: str  # "excellent", "good", "fair", "difficult"
    durability_years: float  # Expected service life
    renaissance_sources: List[str]  # Historical sources

RENAISSANCE_MATERIALS = {
    # === BLADE CORE MATERIALS ===
    "oak": Material(
        name="Oak (Quercus robur)",
        density_kg_m3=750,
        elastic_modulus_pa=12e9,
        tensile_strength_pa=90e6,
        compressive_strength_pa=50e6,
        cost_relative=1.0,
        availability="abundant",
        workability="fair",
        durability_years=50,
        renaissance_sources=["Northern Italian forests", "Alpine trade routes"]
    ),
    
    "ash": Material(
        name="Ash (Fraxinus excelsior)",
        density_kg_m3=680,
        elastic_modulus_pa=10e9,
        tensile_strength_pa=110e6,
        compressive_strength_pa=45e6,
        cost_relative=0.8,
        availability="common",
        workability="good",
        durability_years=30,
        renaissance_sources=["Lombardy plains", "Venetian territories"]
    ),
    
    "pine": Material(
        name="Pine (Pinus sylvestris)",
        density_kg_m3=500,
        elastic_modulus_pa=8e9,
        tensile_strength_pa=60e6,
        compressive_strength_pa=35e6,
        cost_relative=0.5,
        availability="abundant",
        workability="excellent",
        durability_years=15,
        renaissance_sources=["Alpine forests", "Local woodlands"]
    ),
    
    "willow": Material(
        name="Willow (Salix alba)",
        density_kg_m3=420,
        elastic_modulus_pa=7e9,
        tensile_strength_pa=55e6,
        compressive_strength_pa=30e6,
        cost_relative=0.6,
        availability="common",
        workability="excellent",
        durability_years=10,
        renaissance_sources=["Riverside areas", "Wetlands"]
    ),
    
    # === BLADE COVERING MATERIALS ===
    "linen": Material(
        name="Linen (Linum usitatissimum)",
        density_kg_m3=150,
        elastic_modulus_pa=0.5e9,
        tensile_strength_pa=50e6,
        compressive_strength_pa=5e6,
        cost_relative=2.0,
        availability="common",
        workability="excellent",
        durability_years=5,
        renaissance_sources=["Flax fields of Lombardy", "Flemish imports"]
    ),
    
    "hemp": Material(
        name="Hemp (Cannabis sativa)",
        density_kg_m3=180,
        elastic_modulus_pa=0.7e9,
        tensile_strength_pa=60e6,
        compressive_strength_pa=8e6,
        cost_relative=0.7,
        availability="common",
        workability="good",
        durability_years=7,
        renaissance_sources=["Local cultivation", "Rural estates"]
    ),
    
    "leather": Material(
        name="Leather (cowhide)",
        density_kg_m3=900,
        elastic_modulus_pa=0.1e9,
        tensile_strength_pa=25e6,
        compressive_strength_pa=2e6,
        cost_relative=1.5,
        availability="common",
        workability="good",
        durability_years=8,
        renaissance_sources=["Milanese tanneries", "Livestock farms"]
    ),
    
    "canvas": Material(
        name="Canvas (heavy cotton)",
        density_kg_m3=200,
        elastic_modulus_pa=0.3e9,
        tensile_strength_pa=30e6,
        compressive_strength_pa=3e6,
        cost_relative=1.2,
        availability="scarce",
        workability="excellent",
        durability_years=4,
        renaissance_sources=["Eastern imports", "Venetian merchants"]
    ),
    
    # === MECHANICAL COMPONENTS ===
    "bronze": Material(
        name="Bronze (copper-tin alloy)",
        density_kg_m3=8700,
        elastic_modulus_pa=100e9,
        tensile_strength_pa=200e6,
        compressive_strength_pa=150e6,
        cost_relative=15.0,
        availability="scarce",
        workability="difficult",
        durability_years=100,
        renaissance_sources=["Milanese foundries", "Venetian metalworkers"]
    ),
    
    "wrought_iron": Material(
        name="Wrought Iron",
        density_kg_m3=7750,
        elastic_modulus_pa=200e9,
        tensile_strength_pa=250e6,
        compressive_strength_pa=200e6,
        cost_relative=8.0,
        availability="common",
        workability="fair",
        durability_years=75,
        renaissance_sources=["Local forges", "Alpine iron mines"]
    ),
    
    "brass": Material(
        name="Brass (copper-zinc alloy)",
        density_kg_m3=8500,
        elastic_modulus_pa=95e9,
        tensile_strength_pa=180e6,
        compressive_strength_pa=140e6,
        cost_relative=12.0,
        availability="scarce",
        workability="fair",
        durability_years=80,
        renaissance_sources=["German merchants", "Specialized workshops"]
    )
}

# === AERIAL SCREW DESIGN REQUIREMENTS ===
# Based on Codex Atlanticus folio 869r analysis

DESIGN_REQUIREMENTS = {
    "rotor_radius_m": 2.0,  # Optimized for structural feasibility
    "blade_thickness_m": 0.06,  # Modern equivalent for analysis
    "operational_rpm": 120,  # Estimated hover RPM
    "safety_factor": 2.5,  # Renaissance conservative design
    "service_life_years": 10,  # Reasonable expectation
    "max_stress_pa": 100e6,  # Maximum allowable stress
    "weight_budget_kg": 150,  # Total allowable weight
}

def calculate_blade_loading(material: Material, rpm: float, radius: float) -> Dict:
    """
    Calculate structural loading on helical blade.
    
    This analysis considers both centrifugal forces and aerodynamic loading
    that Leonardo's screw would experience during operation.
    """
    omega = rpm * 2 * math.pi / 60  # rad/s
    
    # Centrifugal stress (worst case at blade root)
    # Assuming blade mass distribution along helical path
    blade_length = math.sqrt((2 * math.pi * radius)**2 + (radius * 0.5)**2)  # Approximate helical length
    blade_volume = blade_length * 0.06 * 0.12  # Length × thickness × chord
    blade_mass = blade_volume * material.density_kg_m3
    
    # Centrifugal force: F = m * ω² * r
    centrifugal_force = blade_mass * omega**2 * radius
    
    # Stress at root: σ = F / A
    root_area = 0.06 * 0.12  # thickness × chord
    centrifugal_stress = centrifugal_force / root_area
    
    # Aerodynamic loading (simplified)
    # Assume uniform pressure distribution on helical surface
    blade_area = blade_length * 0.12  # Length × chord
    air_density = 1.225  # kg/m³
    tip_speed = omega * radius
    dynamic_pressure = 0.5 * air_density * tip_speed**2
    
    # Approximate aerodynamic force on blade
    aero_force = dynamic_pressure * blade_area * 0.5  # Simplified lift coefficient
    aero_stress = aero_force / root_area
    
    # Combined stress with fatigue consideration
    combined_stress = centrifugal_stress + aero_stress
    
    # Fatigue factor for cyclic loading
    fatigue_factor = 1.5  # Renaissance conservative estimate
    
    return {
        "centrifugal_stress_pa": centrifugal_stress,
        "aerodynamic_stress_pa": aero_stress,
        "combined_stress_pa": combined_stress,
        "fatigue_adjusted_stress_pa": combined_stress * fatigue_factor,
        "safety_margin": material.tensile_strength_pa / (combined_stress * fatigue_factor),
        "tip_speed_m_s": tip_speed,
        "blade_mass_kg": blade_mass,
        "centrifugal_force_n": centrifugal_force
    }

def analyze_material_combinations() -> Dict:
    """
    Analyze all feasible material combinations for aerial screw construction.
    
    This represents Leonardo's systematic approach to material selection,
    considering both structural requirements and workshop capabilities.
    """
    combinations = []
    
    # Blade core materials
    blade_cores = ["oak", "ash", "pine", "willow"]
    
    # Blade covering materials
    blade_coverings = ["linen", "hemp", "leather", "canvas"]
    
    # Mechanical components
    mechanical_materials = ["bronze", "wrought_iron", "brass"]
    
    for core in blade_cores:
        core_mat = RENAISSANCE_MATERIALS[core]
        core_analysis = calculate_blade_loading(core_mat, DESIGN_REQUIREMENTS["operational_rpm"], 
                                              DESIGN_REQUIREMENTS["rotor_radius_m"])
        
        for covering in blade_coverings:
            cover_mat = RENAISSANCE_MATERIALS[covering]
            
            for mechanical in mechanical_materials:
                mech_mat = RENAISSANCE_MATERIALS[mechanical]
                
                # Calculate total weight
                blade_mass = core_analysis["blade_mass_kg"]
                covering_mass = 2.0  # Estimated covering mass per blade
                mechanical_mass = 25.0  # Hub, gears, bearings
                
                total_mass = blade_mass + covering_mass + mechanical_mass
                
                # Calculate cost
                total_cost = (core_mat.cost_relative + cover_mat.cost_relative * 0.5 + 
                            mech_mat.cost_relative * 0.3)
                
                # Feasibility assessment
                structural_feasible = core_analysis["safety_margin"] >= DESIGN_REQUIREMENTS["safety_factor"]
                weight_feasible = total_mass <= DESIGN_REQUIREMENTS["weight_budget_kg"]
                cost_feasible = total_cost <= 20  # Reasonable workshop budget
                
                overall_feasible = (structural_feasible and weight_feasible and 
                                     cost_feasible and cover_mat.durability_years >= 5)
                
                combinations.append({
                    "blade_core": core,
                    "blade_covering": covering,
                    "mechanical_components": mechanical,
                    "total_mass_kg": total_mass,
                    "total_cost_relative": total_cost,
                    "safety_margin": core_analysis["safety_margin"],
                    "structural_feasible": structural_feasible,
                    "weight_feasible": weight_feasible,
                    "cost_feasible": cost_feasible,
                    "overall_feasible": overall_feasible,
                    "durability_years": min(core_mat.durability_years, 
                                          cover_mat.durability_years, 
                                          mech_mat.durability_years),
                    "workshop_difficulty": (core_mat.workability, cover_mat.workability, 
                                          mech_mat.workability)
                })
    
    # Sort by feasibility and then by cost
    combinations.sort(key=lambda x: (-x["overall_feasible"], x["total_cost_relative"]))
    
    return {
        "all_combinations": combinations,
        "feasible_combinations": [c for c in combinations if c["overall_feasible"]],
        "best_combination": combinations[0] if combinations else None,
        "analysis_summary": {
            "total_combinations_analyzed": len(combinations),
            "feasible_combinations": len([c for c in combinations if c["overall_feasible"]]),
            "structural_failures": len([c for c in combinations if not c["structural_feasible"]]),
            "weight_failures": len([c for c in combinations if not c["weight_feasible"]]),
            "cost_failures": len([c for c in combinations if not c["cost_feasible"]])
        }
    }

def create_material_selection_matrix() -> None:
    """
    Create comprehensive material selection matrix for workshop reference.
    
    This visualization would help Leonardo and his apprentices make informed
    material selection decisions during construction.
    """
    combinations = analyze_material_combinations()
    
    # Create figure with multiple subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle("Leonardo's Aerial Screw - Material Selection Analysis", 
                 fontsize=16, fontweight="bold")
    
    # 1. Safety Margin Analysis
    ax1 = axes[0, 0]
    feasible = [c for c in combinations["all_combinations"] if c["overall_feasible"]]
    infeasible = [c for c in combinations["all_combinations"] if not c["overall_feasible"]]
    
    ax1.scatter([c["total_cost_relative"] for c in feasible], 
               [c["safety_margin"] for c in feasible],
               c="green", s=60, alpha=0.7, label="Feasible")
    ax1.scatter([c["total_cost_relative"] for c in infeasible], 
               [c["safety_margin"] for c in infeasible],
               c="red", s=60, alpha=0.7, label="Infeasible")
    ax1.set_xlabel("Relative Cost")
    ax1.set_ylabel("Safety Margin")
    ax1.set_title("Safety vs Cost Analysis")
    ax1.axhline(y=DESIGN_REQUIREMENTS["safety_factor"], color="orange", 
                linestyle="--", label="Required Safety Factor")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Weight Distribution
    ax2 = axes[0, 1]
    weights_feasible = [c["total_mass_kg"] for c in feasible]
    weights_infeasible = [c["total_mass_kg"] for c in infeasible]
    
    ax2.hist(weights_feasible, bins=10, alpha=0.7, color="green", label="Feasible")
    ax2.hist(weights_infeasible, bins=10, alpha=0.7, color="red", label="Infeasible")
    ax2.axvline(x=DESIGN_REQUIREMENTS["weight_budget_kg"], color="orange", 
                linestyle="--", label="Weight Budget")
    ax2.set_xlabel("Total Mass (kg)")
    ax2.set_ylabel("Number of Combinations")
    ax2.set_title("Weight Distribution Analysis")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Material Performance Comparison
    ax3 = axes[0, 2]
    core_materials = ["oak", "ash", "pine", "willow"]
    performance = []
    
    for material in core_materials:
        mat = RENAISSANCE_MATERIALS[material]
        analysis = calculate_blade_loading(mat, DESIGN_REQUIREMENTS["operational_rpm"],
                                         DESIGN_REQUIREMENTS["rotor_radius_m"])
        performance.append({
            "material": material,
            "strength_to_weight": mat.tensile_strength_pa / mat.density_kg_m3,
            "safety_margin": analysis["safety_margin"],
            "cost": mat.cost_relative,
            "workability_score": {"excellent": 4, "good": 3, "fair": 2, "difficult": 1}[mat.workability]
        })
    
    # Create radar chart for material comparison
    categories = ["Strength/Weight", "Safety Margin", "Cost (inverse)", "Workability"]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    for perf in performance:
        values = [
            perf["strength_to_weight"] / 1e5,  # Normalized
            perf["safety_margin"] / 10,  # Normalized
            5 - perf["cost"],  # Inverse cost (lower is better)
            perf["workability_score"]
        ]
        values += values[:1]  # Complete the circle
        
        ax3.plot(angles, values, 'o-', linewidth=2, label=perf["material"])
        ax3.fill(angles, values, alpha=0.1)
    
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(categories)
    ax3.set_title("Blade Core Material Performance")
    ax3.legend()
    ax3.grid(True)
    
    # 4. Durability Analysis
    ax4 = axes[1, 0]
    durability_groups = {}
    for combo in combinations["all_combinations"]:
        dur = combo["durability_years"]
        if dur not in durability_groups:
            durability_groups[dur] = {"feasible": 0, "infeasible": 0}
        
        if combo["overall_feasible"]:
            durability_groups[dur]["feasible"] += 1
        else:
            durability_groups[dur]["infeasible"] += 1
    
    dur_years = sorted(durability_groups.keys())
    feasible_counts = [durability_groups[d]["feasible"] for d in dur_years]
    infeasible_counts = [durability_groups[d]["infeasible"] for d in dur_years]
    
    width = 0.8
    ax4.bar(np.array(dur_years) - width/2, feasible_counts, width, 
            label="Feasible", color="green", alpha=0.7)
    ax4.bar(np.array(dur_years) + width/2, infeasible_counts, width,
            label="Infeasible", color="red", alpha=0.7)
    ax4.set_xlabel("Durability (years)")
    ax4.set_ylabel("Number of Combinations")
    ax4.set_title("Service Life Analysis")
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Workshop Difficulty Assessment
    ax5 = axes[1, 1]
    difficulty_scores = {"excellent": 4, "good": 3, "fair": 2, "difficult": 1}
    difficulty_matrix = {}
    
    for combo in combinations["all_combinations"]:
        core_diff = difficulty_scores[combo["workshop_difficulty"][0]]
        cover_diff = difficulty_scores[combo["workshop_difficulty"][1]]
        mech_diff = difficulty_scores[combo["workshop_difficulty"][2]]
        
        overall_diff = (core_diff + cover_diff + mech_diff) / 3
        
        difficulty_key = f"Difficulty {overall_diff:.1f}"
        if difficulty_key not in difficulty_matrix:
            difficulty_matrix[difficulty_key] = {"feasible": 0, "infeasible": 0}
        
        if combo["overall_feasible"]:
            difficulty_matrix[difficulty_key]["feasible"] += 1
        else:
            difficulty_matrix[difficulty_key]["infeasible"] += 1
    
    diff_levels = sorted(difficulty_matrix.keys())
    feasible_by_diff = [difficulty_matrix[d]["feasible"] for d in diff_levels]
    infeasible_by_diff = [difficulty_matrix[d]["infeasible"] for d in diff_levels]
    
    ax5.bar(range(len(diff_levels)), feasible_by_diff, 
            label="Feasible", color="green", alpha=0.7)
    ax5.bar(range(len(diff_levels)), infeasible_by_diff, bottom=feasible_by_diff,
            label="Infeasible", color="red", alpha=0.7)
    ax5.set_xlabel("Workshop Difficulty Level")
    ax5.set_ylabel("Number of Combinations")
    ax5.set_title("Construction Difficulty Analysis")
    ax5.set_xticks(range(len(diff_levels)))
    ax5.set_xticklabels(diff_levels, rotation=45)
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Summary Statistics
    ax6 = axes[1, 2]
    ax6.axis('off')
    
    summary_text = f"""
MATERIAL SELECTION SUMMARY
═══════════════════════════

Total Combinations Analyzed: {combinations["analysis_summary"]["total_combinations_analyzed"]}
Feasible Combinations: {combinations["analysis_summary"]["feasible_combinations"]}
Success Rate: {combinations["analysis_summary"]["feasible_combinations"]/combinations["analysis_summary"]["total_combinations_analyzed"]*100:.1f}%

Failure Analysis:
• Structural Failures: {combinations["analysis_summary"]["structural_failures"]}
• Weight Failures: {combinations["analysis_summary"]["weight_failures"]}
• Cost Failures: {combinations["analysis_summary"]["cost_failures"]}

Best Combination:
• Blade Core: {combinations["best_combination"]["blade_core"] if combinations["best_combination"] else "N/A"}
• Blade Covering: {combinations["best_combination"]["blade_covering"] if combinations["best_combination"] else "N/A"}
• Mechanical: {combinations["best_combination"]["mechanical_components"] if combinations["best_combination"] else "N/A"}
• Total Mass: {combinations["best_combination"]["total_mass_kg"]:.1f} kg
• Safety Margin: {combinations["best_combination"]["safety_margin"]:.2f}
• Durability: {combinations["best_combination"]["durability_years"]} years
• Relative Cost: {combinations["best_combination"]["total_cost_relative"]:.1f}
    """
    
    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    plt.tight_layout()
    
    # Save the analysis
    output_path = Path("/Volumes/VIXinSSD/davinci-codex/material_selection_matrix.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

def main():
    """
    Main function to run Leonardo's comprehensive materials analysis.
    
    This function generates all the analysis files that Leonardo would need
    to make informed decisions about aerial screw construction.
    """
    print("Leonardo da Vinci's Aerial Screw - Materials Analysis")
    print("=" * 60)
    print("Milan Workshop, circa 1485-1490")
    print()
    
    # Run comprehensive analysis
    print("Analyzing material combinations...")
    combinations = analyze_material_combinations()
    
    print(f"Total combinations analyzed: {combinations['analysis_summary']['total_combinations_analyzed']}")
    print(f"Feasible combinations: {combinations['analysis_summary']['feasible_combinations']}")
    print(f"Success rate: {combinations['analysis_summary']['feasible_combinations']/combinations['analysis_summary']['total_combinations_analyzed']*100:.1f}%")
    print()
    
    if combinations["best_combination"]:
        best = combinations["best_combination"]
        print("OPTIMAL MATERIAL SELECTION:")
        print(f"  Blade Core: {best['blade_core']}")
        print(f"  Blade Covering: {best['blade_covering']}")
        print(f"  Mechanical Components: {best['mechanical_components']}")
        print(f"  Total Mass: {best['total_mass_kg']:.1f} kg")
        print(f"  Safety Margin: {best['safety_margin']:.2f}")
        print(f"  Durability: {best['durability_years']} years")
        print(f"  Relative Cost: {best['total_cost_relative']:.1f}")
        print()
    
    # Generate material selection matrix
    print("Generating material selection matrix...")
    matrix_path = create_material_selection_matrix()
    print(f"Material selection matrix saved to: {matrix_path}")
    print()
    
    return {
        "material_selection_matrix": str(matrix_path),
        "best_combination": combinations["best_combination"],
        "feasibility_score": combinations["analysis_summary"]["feasible_combinations"]/combinations["analysis_summary"]["total_combinations_analyzed"]
    }

if __name__ == "__main__":
    results = main()
