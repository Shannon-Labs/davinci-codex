"""
Leonardo's Mechanical Lion - Comprehensive Power System Analysis

This module provides a complete comparison between spring-wound and weight-driven
power systems for Leonardo's Mechanical Lion, analyzing performance, feasibility,
and Renaissance constructability to determine the optimal power source.

Analysis Framework:
1. Energy Requirements Analysis
2. Spring System Performance Evaluation
3. Weight System Performance Evaluation
4. Comparative Analysis Matrix
5. Renaissance Feasibility Assessment
6. Cost-Benefit Analysis
7. Final Recommendation

The analysis considers Leonardo's known expertise with spring mechanisms while
objectively evaluating the alternative weight-driven system based on Renaissance
technological capabilities and performance requirements.
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path

# Import system designs
from energy_budget import EnergyBudget
from spring_system_design import SpringPowerSystem
from weight_system_design import WeightPowerSystem

# Performance Metrics (from previous modules)
PERFORMANCE_DURATION = 30.0  # seconds
LION_WEIGHT_LIMIT = 200.0  # kg (maximum lion weight)
LION_VOLUME_LIMIT = 0.6  # m³ (maximum internal volume)

class PowerSystemComparison:
    """
    Comprehensive comparison of spring vs weight power systems.

    This class performs detailed analysis of both power systems across multiple
    criteria including performance, feasibility, cost, and Renaissance
    constructability.
    """

    def __init__(self):
        self.energy_budget = EnergyBudget()
        self.spring_system = SpringPowerSystem()
        self.weight_system = WeightPowerSystem()
        self.comparison_results = {}
        self._perform_comprehensive_analysis()

    def _perform_comprehensive_analysis(self) -> None:
        """Perform complete comparative analysis."""

        # Performance comparison
        performance_comparison = self._compare_performance()

        # Space and weight comparison
        space_comparison = self._compare_space_requirements()

        # Manufacturing feasibility comparison
        manufacturing_comparison = self._compare_manufacturing_feasibility()

        # Operational characteristics comparison
        operational_comparison = self._compare_operational_characteristics()

        # Renaissance feasibility comparison
        renaissance_comparison = self._compare_renaissance_feasibility()

        # Cost analysis comparison
        cost_comparison = self._compare_costs()

        # Compile comprehensive results
        self.comparison_results = {
            "performance": performance_comparison,
            "space_requirements": space_comparison,
            "manufacturing": manufacturing_comparison,
            "operational": operational_comparison,
            "renaissance_feasibility": renaissance_comparison,
            "cost_analysis": cost_comparison
        }

        # Calculate overall scoring after results are compiled
        self.comparison_results["overall_scoring"] = self._calculate_overall_scores()

    def _compare_performance(self) -> Dict:
        """Compare performance characteristics of both systems."""

        spring_perf = self.spring_system.calculate_performance()
        weight_perf = self.weight_system.calculate_performance()

        # Energy metrics
        spring_energy_ratio = spring_perf["usable_operating_time_s"] / PERFORMANCE_DURATION
        weight_energy_ratio = weight_perf["operating_time_s"] / PERFORMANCE_DURATION

        # Power metrics
        spring_power_adequacy = spring_perf["peak_power_delivery_w"] / self.energy_budget.peak_power_w
        weight_power_adequacy = weight_perf["regulated_power_w"] / self.energy_budget.peak_power_w

        # Consistency metrics
        spring_consistency_score = 0.7  # Spring force decreases during operation
        weight_consistency_score = 1.0  # Constant gravitational force

        return {
            "spring_system": {
                "operating_time_s": spring_perf["usable_operating_time_s"],
                "energy_adequacy_ratio": spring_energy_ratio,
                "peak_power_w": spring_perf["peak_power_delivery_w"],
                "power_adequacy_ratio": spring_power_adequacy,
                "force_consistency_score": spring_consistency_score,
                "meets_requirements": spring_perf["meets_performance_requirements"]
            },
            "weight_system": {
                "operating_time_s": weight_perf["operating_time_s"],
                "energy_adequacy_ratio": weight_energy_ratio,
                "regulated_power_w": weight_perf["regulated_power_w"],
                "power_adequacy_ratio": weight_power_adequacy,
                "force_consistency_score": weight_consistency_score,
                "meets_requirements": weight_perf["meets_performance_requirements"],
                "force_type": "Constant gravitational force"
            },
            "performance_winner": "spring" if spring_energy_ratio > weight_energy_ratio else "weight"
        }

    def _compare_space_requirements(self) -> Dict:
        """Compare space and weight requirements."""

        # Spring system space
        spring_volume = (
            self.spring_system.main_spring.free_length_m *
            math.pi * (self.spring_system.main_spring.mean_radius_m * 2) ** 2
        ) / 4  # Approximate spring cylinder volume

        spring_mass = self.spring_system.main_spring.mass_kg

        # Weight system space
        weight_space = self.weight_system.get_space_requirements()
        weight_volume = weight_space["total_volume_m3"]
        weight_mass = sum(w.mass_kg for w in self.weight_system.drive_weights)

        # Space efficiency
        spring_space_efficiency = 1.0 - (spring_volume / LION_VOLUME_LIMIT)
        weight_space_efficiency = 1.0 - (weight_volume / LION_VOLUME_LIMIT)

        # Weight efficiency
        spring_weight_efficiency = 1.0 - (spring_mass / LION_WEIGHT_LIMIT)
        weight_weight_efficiency = 1.0 - (weight_mass / LION_WEIGHT_LIMIT)

        return {
            "spring_system": {
                "volume_m3": spring_volume,
                "mass_kg": spring_mass,
                "space_efficiency_percent": spring_space_efficiency * 100,
                "weight_efficiency_percent": spring_weight_efficiency * 100,
                "fits_in_lion": spring_volume < LION_VOLUME_LIMIT and spring_mass < LION_WEIGHT_LIMIT
            },
            "weight_system": {
                "volume_m3": weight_volume,
                "mass_kg": weight_mass,
                "space_efficiency_percent": weight_space_efficiency * 100,
                "weight_efficiency_percent": weight_weight_efficiency * 100,
                "fits_in_lion": weight_space["fits_in_lion_body"] and weight_mass < LION_WEIGHT_LIMIT
            },
            "space_winner": "spring" if spring_space_efficiency > weight_space_efficiency else "weight"
        }

    def _compare_manufacturing_feasibility(self) -> Dict:
        """Compare manufacturing feasibility and complexity."""

        spring_manuf = self.spring_system.get_manufacturing_analysis()
        weight_manuf = self.weight_system.get_manufacturing_analysis()

        # Complexity scoring (lower is better)
        spring_complexity_score = 0.8  # High - requires spring expertise
        weight_complexity_score = 0.4  # Medium - standard clockmaker skills

        # Time to manufacture
        spring_time_weeks = 5.5  # Average of 4-6 weeks
        weight_time_weeks = 3.5  # Average of 3-4 weeks

        # Rarity of expertise
        spring_expertise_rarity = 0.9  # Very rare - spring masters
        weight_expertise_rarity = 0.3  # Common - clockmakers widely available

        return {
            "spring_system": {
                "construction_time_weeks": spring_time_weeks,
                "complexity_score": spring_complexity_score,
                "expertise_rarity_score": spring_expertise_rarity,
                "required_expertise": spring_manuf["required_expertise"],
                "renaissance_feasibility": spring_manuf["spring_manufacturing"]["renaissance_feasibility"]
            },
            "weight_system": {
                "construction_time_weeks": weight_time_weeks,
                "complexity_score": weight_complexity_score,
                "expertise_rarity_score": weight_expertise_rarity,
                "required_expertise": weight_manuf["required_expertise"],
                "renaissance_feasibility": weight_manuf["weight_casting"]["renaissance_feasibility"]
            },
            "manufacturing_winner": "weight" if weight_complexity_score < spring_complexity_score else "spring"
        }

    def _compare_operational_characteristics(self) -> Dict:
        """Compare operational characteristics."""

        # Reset time and effort
        spring_reset_time = self.spring_system.winding_mechanism["winding_time_s"]
        spring_reset_feasible = self.spring_system.winding_mechanism["is_human_feasible"]

        weight_reset_time = self.weight_system.reset_mechanism["reset_time_s"]
        weight_reset_feasible = self.weight_system.reset_mechanism["is_human_feasible"]

        # Maintenance requirements
        spring_maintenance_score = 0.4  # Spring fatigue and potential failure
        weight_maintenance_score = 0.8  # Simple and reliable

        # Safety considerations
        spring_safety_score = 0.6  # Spring tension hazards
        weight_safety_score = 0.9  # Controlled descent, safer

        # Performance consistency
        spring_consistency = 0.7  # Decreasing force as spring unwinds
        weight_consistency = 1.0  # Constant gravitational force

        return {
            "spring_system": {
                "reset_time_s": spring_reset_time,
                "reset_feasible": spring_reset_feasible,
                "maintenance_score": spring_maintenance_score,
                "safety_score": spring_safety_score,
                "consistency_score": spring_consistency,
                "reliability_score": 0.75
            },
            "weight_system": {
                "reset_time_s": weight_reset_time,
                "reset_feasible": weight_reset_feasible,
                "maintenance_score": weight_maintenance_score,
                "safety_score": weight_safety_score,
                "consistency_score": weight_consistency,
                "reliability_score": 0.95
            },
            "operational_winner": "weight" if (spring_maintenance_score + spring_safety_score) < (weight_maintenance_score + weight_safety_score) else "spring"
        }

    def _compare_renaissance_feasibility(self) -> Dict:
        """Compare Renaissance technological feasibility."""

        # Leonardo's expertise alignment
        spring_leonardo_alignment = 1.0  # Direct match with Leonardo's spring expertise
        weight_leonardo_alignment = 0.6  # Less aligned with Leonardo's known innovations

        # Material availability
        spring_material_rarity = 0.7  # High-quality steel springs were rare
        weight_material_rarity = 0.3  # Cast iron and rope were common

        # Workshop capability requirements
        spring_workshop_requirement = 0.8  # Requires specialized spring workshop
        weight_workshop_requirement = 0.4  # Standard clockmaker workshop sufficient

        # Historical precedent
        spring_historical_precedent = 0.6  # Some precedent but limited
        weight_historical_precedent = 0.9  # Well-established in tower clocks

        return {
            "spring_system": {
                "leonardo_expertise_alignment": spring_leonardo_alignment,
                "material_availability": 1.0 - spring_material_rarity,
                "workshop_requirements": 1.0 - spring_workshop_requirement,
                "historical_precedent": spring_historical_precedent,
                "overall_feasibility": (spring_leonardo_alignment + (1.0 - spring_material_rarity) + (1.0 - spring_workshop_requirement) + spring_historical_precedent) / 4
            },
            "weight_system": {
                "leonardo_expertise_alignment": weight_leonardo_alignment,
                "material_availability": 1.0 - weight_material_rarity,
                "workshop_requirements": 1.0 - weight_workshop_requirement,
                "historical_precedent": weight_historical_precedent,
                "overall_feasibility": (weight_leonardo_alignment + (1.0 - weight_material_rarity) + (1.0 - weight_workshop_requirement) + weight_historical_precedent) / 4
            },
            "renaissance_winner": "spring" if spring_leonardo_alignment > weight_leonardo_alignment else "weight"
        }

    def _compare_costs(self) -> Dict:
        """Compare relative costs in Renaissance context."""

        # Material costs (relative units)
        spring_material_cost = 40  # High-quality steel expensive
        weight_material_cost = 20  # Cast iron and rope moderate

        # Labor costs (expertise rarity)
        spring_labor_cost = 60  # Spring master expensive
        weight_labor_cost = 25  # Clockmaker moderate

        # Tool and equipment costs
        spring_equipment_cost = 30  # Specialized spring tools
        weight_equipment_cost = 15  # Standard workshop tools

        # Total costs
        spring_total_cost = spring_material_cost + spring_labor_cost + spring_equipment_cost
        weight_total_cost = weight_material_cost + weight_labor_cost + weight_equipment_cost

        return {
            "spring_system": {
                "material_cost_units": spring_material_cost,
                "labor_cost_units": spring_labor_cost,
                "equipment_cost_units": spring_equipment_cost,
                "total_cost_units": spring_total_cost,
                "cost_category": "High"
            },
            "weight_system": {
                "material_cost_units": weight_material_cost,
                "labor_cost_units": weight_labor_cost,
                "equipment_cost_units": weight_equipment_cost,
                "total_cost_units": weight_total_cost,
                "cost_category": "Medium"
            },
            "cost_winner": "weight" if weight_total_cost < spring_total_cost else "spring"
        }

    def _calculate_overall_scores(self) -> Dict:
        """Calculate weighted overall scores for both systems."""

        # Weight factors for different criteria
        weights = {
            "performance": 0.25,
            "space_efficiency": 0.15,
            "manufacturing_feasibility": 0.15,
            "operational_characteristics": 0.20,
            "renaissance_feasibility": 0.20,
            "cost": 0.05
        }

        # Spring system scores
        spring_scores = {
            "performance": self.comparison_results["performance"]["spring_system"]["energy_adequacy_ratio"],
            "space_efficiency": self.comparison_results["space_requirements"]["spring_system"]["space_efficiency_percent"] / 100,
            "manufacturing_feasibility": 1.0 - self.comparison_results["manufacturing"]["spring_system"]["complexity_score"],
            "operational_characteristics": (self.comparison_results["operational"]["spring_system"]["maintenance_score"] +
                                           self.comparison_results["operational"]["spring_system"]["safety_score"]) / 2,
            "renaissance_feasibility": self.comparison_results["renaissance_feasibility"]["spring_system"]["overall_feasibility"],
            "cost": 1.0 - (self.comparison_results["cost_analysis"]["spring_system"]["total_cost_units"] / 100)
        }

        # Weight system scores
        weight_scores = {
            "performance": self.comparison_results["performance"]["weight_system"]["energy_adequacy_ratio"],
            "space_efficiency": self.comparison_results["space_requirements"]["weight_system"]["space_efficiency_percent"] / 100,
            "manufacturing_feasibility": 1.0 - self.comparison_results["manufacturing"]["weight_system"]["complexity_score"],
            "operational_characteristics": (self.comparison_results["operational"]["weight_system"]["maintenance_score"] +
                                           self.comparison_results["operational"]["weight_system"]["safety_score"]) / 2,
            "renaissance_feasibility": self.comparison_results["renaissance_feasibility"]["weight_system"]["overall_feasibility"],
            "cost": 1.0 - (self.comparison_results["cost_analysis"]["weight_system"]["total_cost_units"] / 100)
        }

        # Calculate weighted totals
        spring_total = sum(spring_scores[category] * weights[category] for category in weights.keys())
        weight_total = sum(weight_scores[category] * weights[category] for category in weights.keys())

        return {
            "spring_system": {
                "individual_scores": spring_scores,
                "weighted_total": spring_total,
                "final_score_percent": spring_total * 100
            },
            "weight_system": {
                "individual_scores": weight_scores,
                "weighted_total": weight_total,
                "final_score_percent": weight_total * 100
            },
            "recommended_system": "spring" if spring_total > weight_total else "weight",
            "score_difference_percent": abs(spring_total - weight_total) * 100
        }

    def create_comparison_visualization(self, output_path: Path) -> None:
        """Create comprehensive comparison visualization."""

        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle("Leonardo's Mechanical Lion - Power System Comparison", fontsize=16, fontweight="bold")

        # 1. Performance Comparison
        ax1 = axes[0, 0]
        categories = ['Operating Time\nRatio', 'Power\nAdequacy', 'Force\nConsistency']
        spring_values = [
            self.comparison_results["performance"]["spring_system"]["energy_adequacy_ratio"],
            self.comparison_results["performance"]["spring_system"]["power_adequacy_ratio"],
            self.comparison_results["performance"]["spring_system"]["force_consistency_score"]
        ]
        weight_values = [
            self.comparison_results["performance"]["weight_system"]["energy_adequacy_ratio"],
            self.comparison_results["performance"]["weight_system"]["power_adequacy_ratio"],
            self.comparison_results["performance"]["weight_system"]["force_consistency_score"]
        ]

        x = np.arange(len(categories))
        width = 0.35
        ax1.bar(x - width/2, spring_values, width, label='Spring System', color='blue', alpha=0.7)
        ax1.bar(x + width/2, weight_values, width, label='Weight System', color='red', alpha=0.7)
        ax1.set_xlabel('Performance Metrics')
        ax1.set_ylabel('Performance Ratio')
        ax1.set_title('Performance Comparison')
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 1.2)

        # 2. Space and Weight Efficiency
        ax2 = axes[0, 1]
        space_categories = ['Space\nEfficiency', 'Weight\nEfficiency']
        spring_space = [
            self.comparison_results["space_requirements"]["spring_system"]["space_efficiency_percent"] / 100,
            self.comparison_results["space_requirements"]["spring_system"]["weight_efficiency_percent"] / 100
        ]
        weight_space = [
            self.comparison_results["space_requirements"]["weight_system"]["space_efficiency_percent"] / 100,
            self.comparison_results["space_requirements"]["weight_system"]["weight_efficiency_percent"] / 100
        ]

        x2 = np.arange(len(space_categories))
        ax2.bar(x2 - width/2, spring_space, width, label='Spring System', color='blue', alpha=0.7)
        ax2.bar(x2 + width/2, weight_space, width, label='Weight System', color='red', alpha=0.7)
        ax2.set_xlabel('Efficiency Metrics')
        ax2.set_ylabel('Efficiency Ratio')
        ax2.set_title('Space and Weight Efficiency')
        ax2.set_xticks(x2)
        ax2.set_xticklabels(space_categories)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1.2)

        # 3. Manufacturing Complexity
        ax3 = axes[0, 2]
        manuf_categories = ['Construction\nTime (weeks)', 'Complexity\nScore', 'Expertise\nRarity']
        spring_manuf = [
            self.comparison_results["manufacturing"]["spring_system"]["construction_time_weeks"] / 6,
            1.0 - self.comparison_results["manufacturing"]["spring_system"]["complexity_score"],
            1.0 - self.comparison_results["manufacturing"]["spring_system"]["expertise_rarity_score"]
        ]
        weight_manuf = [
            self.comparison_results["manufacturing"]["weight_system"]["construction_time_weeks"] / 6,
            1.0 - self.comparison_results["manufacturing"]["weight_system"]["complexity_score"],
            1.0 - self.comparison_results["manufacturing"]["weight_system"]["expertise_rarity_score"]
        ]

        x3 = np.arange(len(manuf_categories))
        ax3.bar(x3 - width/2, spring_manuf, width, label='Spring System', color='blue', alpha=0.7)
        ax3.bar(x3 + width/2, weight_manuf, width, label='Weight System', color='red', alpha=0.7)
        ax3.set_xlabel('Manufacturing Metrics')
        ax3.set_ylabel('Normalized Score')
        ax3.set_title('Manufacturing Analysis')
        ax3.set_xticks(x3)
        ax3.set_xticklabels(manuf_categories)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(0, 1.2)

        # 4. Operational Characteristics
        ax4 = axes[1, 0]
        op_categories = ['Reset\nFeasibility', 'Maintenance\nScore', 'Safety\nScore', 'Reliability\nScore']
        spring_op = [
            1.0 if self.comparison_results["operational"]["spring_system"]["reset_feasible"] else 0.0,
            self.comparison_results["operational"]["spring_system"]["maintenance_score"],
            self.comparison_results["operational"]["spring_system"]["safety_score"],
            self.comparison_results["operational"]["spring_system"]["reliability_score"]
        ]
        weight_op = [
            1.0 if self.comparison_results["operational"]["weight_system"]["reset_feasible"] else 0.0,
            self.comparison_results["operational"]["weight_system"]["maintenance_score"],
            self.comparison_results["operational"]["weight_system"]["safety_score"],
            self.comparison_results["operational"]["weight_system"]["reliability_score"]
        ]

        x4 = np.arange(len(op_categories))
        ax4.bar(x4 - width/2, spring_op, width, label='Spring System', color='blue', alpha=0.7)
        ax4.bar(x4 + width/2, weight_op, width, label='Weight System', color='red', alpha=0.7)
        ax4.set_xlabel('Operational Metrics')
        ax4.set_ylabel('Score (0-1)')
        ax4.set_title('Operational Characteristics')
        ax4.set_xticks(x4)
        ax4.set_xticklabels(op_categories)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim(0, 1.2)

        # 5. Renaissance Feasibility
        ax5 = axes[1, 1]
        renaissance_categories = ['Leonardo\nAlignment', 'Material\nAvailability', 'Workshop\nRequirements', 'Historical\nPrecedent']
        spring_ren = [
            self.comparison_results["renaissance_feasibility"]["spring_system"]["leonardo_expertise_alignment"],
            self.comparison_results["renaissance_feasibility"]["spring_system"]["material_availability"],
            self.comparison_results["renaissance_feasibility"]["spring_system"]["workshop_requirements"],
            self.comparison_results["renaissance_feasibility"]["spring_system"]["historical_precedent"]
        ]
        weight_ren = [
            self.comparison_results["renaissance_feasibility"]["weight_system"]["leonardo_expertise_alignment"],
            self.comparison_results["renaissance_feasibility"]["weight_system"]["material_availability"],
            self.comparison_results["renaissance_feasibility"]["weight_system"]["workshop_requirements"],
            self.comparison_results["renaissance_feasibility"]["weight_system"]["historical_precedent"]
        ]

        x5 = np.arange(len(renaissance_categories))
        ax5.bar(x5 - width/2, spring_ren, width, label='Spring System', color='blue', alpha=0.7)
        ax5.bar(x5 + width/2, weight_ren, width, label='Weight System', color='red', alpha=0.7)
        ax5.set_xlabel('Renaissance Feasibility')
        ax5.set_ylabel('Score (0-1)')
        ax5.set_title('Renaissance Feasibility Analysis')
        ax5.set_xticks(x5)
        ax5.set_xticklabels(renaissance_categories)
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        ax5.set_ylim(0, 1.2)

        # 6. Overall Scoring Radar Chart
        ax6 = axes[1, 2]
        categories_radar = ['Performance', 'Space', 'Manufacturing', 'Operational', 'Renaissance', 'Cost']
        spring_radar = list(self.comparison_results["overall_scoring"]["spring_system"]["individual_scores"].values())
        weight_radar = list(self.comparison_results["overall_scoring"]["weight_system"]["individual_scores"].values())

        # Convert to angles for radar chart
        angles = np.array([n * 2 * np.pi / len(categories_radar) for n in range(len(categories_radar))])
        angles = np.append(angles, angles[0])  # Complete the circle
        spring_radar.append(spring_radar[0])
        weight_radar.append(weight_radar[0])

        ax6.plot(angles, spring_radar, 'b-', linewidth=2, label='Spring System')
        ax6.fill(angles, spring_radar, 'b', alpha=0.1)
        ax6.plot(angles, weight_radar, 'r-', linewidth=2, label='Weight System')
        ax6.fill(angles, weight_radar, 'r', alpha=0.1)

        ax6.set_xticks(angles[:-1])
        ax6.set_xticklabels(categories_radar)
        ax6.set_ylim(0, 1)
        ax6.set_title('Overall Performance Radar')
        ax6.legend()
        ax6.grid(True)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

    def generate_recommendation_report(self) -> str:
        """Generate comprehensive recommendation report."""

        winner = self.comparison_results["overall_scoring"]["recommended_system"]
        spring_score = self.comparison_results["overall_scoring"]["spring_system"]["final_score_percent"]
        weight_score = self.comparison_results["overall_scoring"]["weight_system"]["final_score_percent"]
        score_diff = self.comparison_results["overall_scoring"]["score_difference_percent"]

        report = f"""
LEONARDO'S MECHANICAL LION - POWER SYSTEM RECOMMENDATION REPORT
================================================================

EXECUTIVE SUMMARY:
Recommended Power System: {winner.upper()} SYSTEM
Spring System Score: {spring_score:.1f}%
Weight System Score: {weight_score:.1f}%
Score Difference: {score_diff:.1f}%

DETAILED ANALYSIS:

1. PERFORMANCE ANALYSIS:
   Spring System Operating Time: {self.comparison_results['performance']['spring_system']['operating_time_s']:.1f} seconds
   Weight System Operating Time: {self.comparison_results['performance']['weight_system']['operating_time_s']:.1f} seconds
   Performance Winner: {self.comparison_results['performance']['performance_winner'].upper()}

2. SPACE AND WEIGHT ANALYSIS:
   Spring System Volume: {self.comparison_results['space_requirements']['spring_system']['volume_m3']:.3f} m³
   Weight System Volume: {self.comparison_results['space_requirements']['weight_system']['volume_m3']:.3f} m³
   Space Efficiency Winner: {self.comparison_results['space_requirements']['space_winner'].upper()}

3. MANUFACTURING ANALYSIS:
   Spring System Construction: {self.comparison_results['manufacturing']['spring_system']['construction_time_weeks']:.1f} weeks
   Weight System Construction: {self.comparison_results['manufacturing']['weight_system']['construction_time_weeks']:.1f} weeks
   Manufacturing Winner: {self.comparison_results['manufacturing']['manufacturing_winner'].upper()}

4. OPERATIONAL ANALYSIS:
   Spring System Reset Time: {self.comparison_results['operational']['spring_system']['reset_time_s']:.1f} seconds
   Weight System Reset Time: {self.comparison_results['operational']['weight_system']['reset_time_s']:.1f} seconds
   Operational Winner: {self.comparison_results['operational']['operational_winner'].upper()}

5. RENAISSANCE FEASIBILITY:
   Spring System Feasibility: {self.comparison_results['renaissance_feasibility']['spring_system']['overall_feasibility']:.2f}
   Weight System Feasibility: {self.comparison_results['renaissance_feasibility']['weight_system']['overall_feasibility']:.2f}
   Renaissance Winner: {self.comparison_results['renaissance_feasibility']['renaissance_winner'].upper()}

6. COST ANALYSIS:
   Spring System Cost: {self.comparison_results['cost_analysis']['spring_system']['total_cost_units']} units (High)
   Weight System Cost: {self.comparison_results['cost_analysis']['weight_system']['total_cost_units']} units (Medium)
   Cost Winner: {self.comparison_results['cost_analysis']['cost_winner'].upper()}

RECOMMENDATION RATIONALE:

Based on the comprehensive analysis, the {winner} system is recommended for Leonardo's Mechanical Lion.

"""

        if winner == "spring":
            report += """
KEY ADVANTAGES OF SPRING SYSTEM:
• Superior energy density in compact form factor
• Excellent alignment with Leonardo's proven expertise
• Better space efficiency within lion body
• Faster reset between performances
• Consistent with Leonardo's innovative approach

CONSIDERATIONS:
• Requires specialized spring manufacturing expertise
• Higher initial cost and construction time
• Complex maintenance requirements
• Potential for spring fatigue over time

IMPLEMENTATION RECOMMENDATIONS:
• Utilize Leonardo's spring expertise from previous automata projects
• Partner with master spring maker from Florence or Milan
• Implement rigorous testing and quality control
• Develop maintenance protocols for royal court use
"""

        else:
            report += """
KEY ADVANTAGES OF WEIGHT SYSTEM:
• Simpler manufacturing with standard Renaissance technology
• Superior operational reliability and safety
• Constant force output for consistent performance
• Lower cost and faster construction
• Easier maintenance and repair

CONSIDERATIONS:
• Requires more vertical space within lion body
• Heavier system increases overall lion weight
• Slower reset between performances
• Less aligned with Leonardo's innovative reputation

IMPLEMENTATION RECOMMENDATIONS:
• Optimize weight carriage design for space efficiency
• Use high-quality materials for reliability
• Develop efficient winch system for reset operations
• Implement safety features for royal court demonstrations
"""

        report += f"""
CONCLUSION:
The {winner} system provides the optimal balance of performance, feasibility, and Renaissance
authenticity for Leonardo's Mechanical Lion. This recommendation ensures successful
performance for King Francis I's court while maintaining historical accuracy and
technical excellence worthy of Leonardo's reputation.

Final Score: {spring_score if winner == 'spring' else weight_score:.1f}%
"""

        return report

def main():
    """Main function to perform comprehensive power system analysis."""

    print("Leonardo's Mechanical Lion - Comprehensive Power System Analysis")
    print("=" * 70)

    # Perform analysis
    comparison = PowerSystemComparison()

    # Display key results
    print("\nOVERALL SCORING:")
    print("-" * 40)
    overall = comparison.comparison_results["overall_scoring"]
    print(f"Spring System: {overall['spring_system']['final_score_percent']:.1f}%")
    print(f"Weight System: {overall['weight_system']['final_score_percent']:.1f}%")
    print(f"Recommended: {overall['recommended_system'].upper()} SYSTEM")
    print(f"Score Difference: {overall['score_difference_percent']:.1f}%")

    # Display individual category winners
    print(f"\nCATEGORY WINNERS:")
    print("-" * 40)
    print(f"Performance: {comparison.comparison_results['performance']['performance_winner'].upper()}")
    print(f"Space Efficiency: {comparison.comparison_results['space_requirements']['space_winner'].upper()}")
    print(f"Manufacturing: {comparison.comparison_results['manufacturing']['manufacturing_winner'].upper()}")
    print(f"Operational: {comparison.comparison_results['operational']['operational_winner'].upper()}")
    print(f"Renaissance Feasibility: {comparison.comparison_results['renaissance_feasibility']['renaissance_winner'].upper()}")
    print(f"Cost: {comparison.comparison_results['cost_analysis']['cost_winner'].upper()}")

    # Create visualization
    artifacts_dir = Path("/Volumes/VIXinSSD/davinci-codex/artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    comparison.create_comparison_visualization(artifacts_dir / "power_comparison_chart.png")
    print(f"\nComparison chart saved to: {artifacts_dir / 'power_comparison_chart.png'}")

    # Generate recommendation report
    report = comparison.generate_recommendation_report()
    with open(artifacts_dir / "power_system_recommendation.txt", "w") as f:
        f.write(report)
    print(f"Recommendation report saved to: {artifacts_dir / 'power_system_recommendation.txt'}")

    # Display summary recommendation
    print(f"\nRECOMMENDATION SUMMARY:")
    print("-" * 40)
    print(f"Recommended System: {overall['recommended_system'].upper()}")
    print(f"Confidence Level: {'High' if overall['score_difference_percent'] > 10 else 'Medium' if overall['score_difference_percent'] > 5 else 'Low'}")
    print(f"Key Advantage: {'Energy density and Leonardo\'s expertise' if overall['recommended_system'] == 'spring' else 'Reliability and simpler construction'}")

    return comparison

if __name__ == "__main__":
    comparison = main()