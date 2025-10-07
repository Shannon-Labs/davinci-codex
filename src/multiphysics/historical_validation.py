"""
Historical Constraint Validation Framework

Validates simulation results against Leonardo's historical constraints and
Renaissance engineering limitations to ensure authenticity and feasibility.

This framework ensures that enhanced simulations maintain historical integrity
while providing scientific rigor.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional, Union
import numpy as np
import logging

logger = logging.getLogger(__name__)


@dataclass
class HistoricalConstraint:
    """Definition of a historical constraint for validation."""

    name: str
    description: str
    source_manuscript: str  # Codex reference
    constraint_type: str  # 'material', 'power', 'geometry', 'manufacturing'
    constraint_function: callable
    tolerance_factor: float = 1.0  # Allowable factor above/below constraint
    mandatory: bool = True  # Whether this constraint must be satisfied
    historical_notes: str = ""


@dataclass
class ValidationResult:
    """Result of historical constraint validation."""

    constraint_name: str
    is_satisfied: bool
    actual_value: float
    constraint_value: float
    tolerance_applied: float
    violation_magnitude: float
    historical_compliance: float  # 0-1 scale
    notes: str = ""


@dataclass
class ValidationReport:
    """Comprehensive validation report for an invention."""

    invention_slug: str
    overall_compliance_score: float
    validation_results: List[ValidationResult]
    mandatory_constraints_satisfied: bool
    recommendations: List[str]
    historical_fidelity_rating: str  # 'Poor', 'Fair', 'Good', 'Excellent'
    enhancement_opportunities: List[str]


class HistoricalValidator:
    """
    Validates simulation results against Leonardo's historical constraints.

    Ensures that enhanced physics models respect Renaissance engineering
    limitations while providing scientific insights.
    """

    def __init__(self):
        self.constraints: Dict[str, List[HistoricalConstraint]] = {}
        self.validation_history: List[ValidationReport] = []

        # Initialize constraint libraries
        self._initialize_material_constraints()
        self._initialize_power_constraints()
        self._initialize_manufacturing_constraints()

    def _initialize_material_constraints(self):
        """Initialize material property constraints from Renaissance era."""

        # Wood properties (spruce, oak - common in Leonardo's time)
        self.constraints['wood'] = [
            HistoricalConstraint(
                name="max_tensile_stress_spruce",
                description="Maximum tensile stress for spruce wood",
                source_manuscript="Codex Atlanticus, various structural analyses",
                constraint_type="material",
                constraint_function=lambda x: x <= 40e6,  # 40 MPa
                tolerance_factor=1.1,
                historical_notes="Based on typical spruce wood properties available in Renaissance Italy"
            ),
            HistoricalConstraint(
                name="max_compressive_stress_spruce",
                description="Maximum compressive stress for spruce wood",
                source_manuscript="Codex Atlanticus, beam loading studies",
                constraint_type="material",
                constraint_function=lambda x: x <= 30e6,  # 30 MPa
                tolerance_factor=1.1,
                historical_notes="Compression strength lower than tension due to grain structure"
            ),
            HistoricalConstraint(
                name="max_shear_stress_wood",
                description="Maximum shear stress for wooden joints",
                source_manuscript="Codex Atlanticus, joint design studies",
                constraint_type="material",
                constraint_function=lambda x: x <= 5e6,  # 5 MPa
                tolerance_factor=1.0,  # No tolerance for shear - critical failure mode
                historical_notes="Wood is weak in shear - critical for joint design"
            )
        ]

        # Iron properties (wrought iron - best available in Renaissance)
        self.constraints['iron'] = [
            HistoricalConstraint(
                name="max_tensile_stress_iron",
                description="Maximum tensile stress for wrought iron",
                source_manuscript="Codex Atlanticus, chain and cable studies",
                constraint_type="material",
                constraint_function=lambda x: x <= 200e6,  # 200 MPa
                tolerance_factor=1.2,
                historical_notes="Wrought iron with inconsistent quality, variable strength"
            ),
            HistoricalConstraint(
                name="max_fatigue_stress_iron",
                description="Maximum fatigue stress for cyclic loading",
                source_manuscript="Codex Atlanticus, spring and clock mechanism studies",
                constraint_type="material",
                constraint_function=lambda x: x <= 80e6,  # 80 MPa
                tolerance_factor=1.0,
                historical_notes="Fatigue poorly understood - high failure rates"
            )
        ]

        # Linen and canvas (membrane materials)
        self.constraints['textile'] = [
            HistoricalConstraint(
                name="max_tensile_stress_linen",
                description="Maximum tensile stress for linen fabric",
                source_manuscript="Codex Atlanticus, parachute and wing membrane studies",
                constraint_type="material",
                constraint_function=lambda x: x <= 20e6,  # 20 MPa
                tolerance_factor=1.1,
                historical_notes="Linen treated with sizing for air retention"
            ),
            HistoricalConstraint(
                name="max_membrane_pressure",
                description="Maximum pressure differential for textile membranes",
                source_manuscript="Codex Atlanticus, balloon and aerostat studies",
                constraint_type="material",
                constraint_function=lambda x: x <= 5000,  # Pa
                tolerance_factor=1.0,
                historical_notes="Membranes would rupture under high pressure"
            )
        ]

    def _initialize_power_constraints(self):
        """Initialize power and energy constraints from Renaissance era."""

        self.constraints['power'] = [
            HistoricalConstraint(
                name="human_power_sustained",
                description="Maximum sustained human power output",
                source_manuscript="Codex Atlanticus, human-powered machine studies",
                constraint_type="power",
                constraint_function=lambda x: x <= 150,  # Watts
                tolerance_factor=1.0,
                historical_notes="Based on sustained human labor studies"
            ),
            HistoricalConstraint(
                name="human_power_peak",
                description="Maximum peak human power output",
                source_manuscript="Codex Atlanticus, sudden force applications",
                constraint_type="power",
                constraint_function=lambda x: x <= 300,  # Watts
                tolerance_factor=1.0,
                historical_notes="Short duration bursts only"
            ),
            HistoricalConstraint(
                name="early_steam_power",
                description="Early steam engine power availability",
                source_manuscript="Post-Leonardo era - for comparative analysis",
                constraint_type="power",
                constraint_function=lambda x: x <= 2000,  # Watts
                tolerance_factor=1.5,
                historical_notes="Early Newcomen engines, not available to Leonardo"
            ),
            HistoricalConstraint(
                name="animal_power_horse",
                description="Maximum sustained horse power",
                source_manuscript="Codex Atlanticus, animal-powered mechanisms",
                constraint_type="power",
                constraint_function=lambda x: x <= 750,  # Watts
                tolerance_factor=1.0,
                historical_notes="Draft horse in good condition"
            )
        ]

    def _initialize_manufacturing_constraints(self):
        """Initialize manufacturing and fabrication constraints."""

        self.constraints['manufacturing'] = [
            HistoricalConstraint(
                name="max_wood_span",
                description="Maximum single-piece wood span available",
                source_manuscript="Codex Atlanticus, timber availability studies",
                constraint_type="manufacturing",
                constraint_function=lambda x: x <= 15.0,  # meters
                tolerance_factor=1.0,
                historical_notes="Longest clear timber available in Renaissance Italy"
            ),
            HistoricalConstraint(
                name="min_machining_tolerance",
                description="Minimum achievable machining tolerance",
                source_manuscript="Codex Atlanticus, tool and precision studies",
                constraint_type="manufacturing",
                constraint_function=lambda x: x >= 0.5,  # mm
                tolerance_factor=1.0,
                historical_notes="Hand tools with limited precision"
            ),
            HistoricalConstraint(
                name="max_gear_ratio_single_stage",
                description="Maximum practical single-stage gear ratio",
                source_manuscript="Codex Atlanticus, gear mechanism studies",
                constraint_type="manufacturing",
                constraint_function=lambda x: x <= 10.0,
                tolerance_factor=1.2,
                historical_notes="Wooden gears with tooth strength limitations"
            ),
            HistoricalConstraint(
                name="max_joint_complexity",
                description="Maximum number of joints in practical assembly",
                source_manuscript="Codex Atlanticus, assembly and maintenance studies",
                constraint_type="manufacturing",
                constraint_function=lambda x: x <= 50,
                tolerance_factor=1.5,
                historical_notes="Assembly complexity and maintenance considerations"
            )
        ]

    def validate_invention(self, invention_slug: str, simulation_results: Dict[str, Any],
                          additional_constraints: Optional[List[HistoricalConstraint]] = None) -> ValidationReport:
        """
        Validate an invention against historical constraints.

        Args:
            invention_slug: Unique identifier for the invention
            simulation_results: Results from physics simulation
            additional_constraints: Optional additional constraints

        Returns:
            Comprehensive validation report
        """

        # Determine relevant constraints for this invention
        relevant_constraints = self._get_relevant_constraints(invention_slug)

        # Add any additional constraints
        if additional_constraints:
            relevant_constraints.extend(additional_constraints)

        # Validate each constraint
        validation_results = []
        for constraint in relevant_constraints:
            result = self._validate_constraint(constraint, simulation_results)
            validation_results.append(result)

        # Compute overall metrics
        mandatory_satisfied = all(
            r.is_satisfied for r in validation_results
            if self._get_constraint_by_name(constraint.name).mandatory
        )

        overall_compliance = self._compute_overall_compliance(validation_results)
        fidelity_rating = self._compute_fidelity_rating(overall_compliance)

        # Generate recommendations
        recommendations = self._generate_recommendations(validation_results)
        enhancement_opportunities = self._identify_enhancement_opportunities(
            invention_slug, validation_results, simulation_results
        )

        # Create report
        report = ValidationReport(
            invention_slug=invention_slug,
            overall_compliance_score=overall_compliance,
            validation_results=validation_results,
            mandatory_constraints_satisfied=mandatory_satisfied,
            recommendations=recommendations,
            historical_fidelity_rating=fidelity_rating,
            enhancement_opportunities=enhancement_opportunities
        )

        # Store in history
        self.validation_history.append(report)

        return report

    def _get_relevant_constraints(self, invention_slug: str) -> List[HistoricalConstraint]:
        """Get constraints relevant to a specific invention."""

        relevant_constraints = []

        # All inventions share basic constraints
        relevant_constraints.extend(self.constraints['power'])
        relevant_constraints.extend(self.constraints['manufacturing'])

        # Invention-specific constraints
        if invention_slug in ['ornithopter', 'aerial_screw']:
            # Flying machines need strong materials
            relevant_constraints.extend(self.constraints['wood'])
            relevant_constraints.extend(self.constraints['iron'])
            relevant_constraints.extend(self.constraints['textile'])

        elif invention_slug in ['mechanical_organ', 'mechanical_drum']:
            # Musical instruments need precision
            relevant_constraints.extend(self.constraints['wood'])
            relevant_constraints.append(self.constraints['manufacturing'][2])  # gear ratio

        elif invention_slug in ['self_propelled_cart', 'mechanical_odometer']:
            # Ground vehicles need durability
            relevant_constraints.extend(self.constraints['wood'])
            relevant_constraints.extend(self.constraints['iron'])

        return relevant_constraints

    def _validate_constraint(self, constraint: HistoricalConstraint,
                           simulation_results: Dict[str, Any]) -> ValidationResult:
        """Validate a single constraint against simulation results."""

        # Extract the relevant value from simulation results
        actual_value = self._extract_constraint_value(constraint, simulation_results)

        # Get constraint limit
        constraint_value = self._get_constraint_limit(constraint)

        # Apply tolerance
        tolerance_applied = constraint_value * constraint.tolerance_factor

        # Check constraint
        is_satisfied = constraint.constraint_function(actual_value * constraint.tolerance_factor)

        # Compute violation magnitude
        if is_satisfied:
            violation_magnitude = 0.0
        else:
            if constraint_value > 0:
                violation_magnitude = abs((actual_value - constraint_value) / constraint_value)
            else:
                violation_magnitude = abs(actual_value - constraint_value)

        # Compute historical compliance (0-1 scale)
        if is_satisfied:
            if constraint.tolerance_factor == 1.0:
                historical_compliance = 1.0
            else:
                # Reduced compliance for tolerance usage
                historical_compliance = 1.0 - (constraint.tolerance_factor - 1.0) * 0.5
        else:
            historical_compliance = max(0.0, 1.0 - violation_magnitude)

        # Generate notes
        notes = self._generate_constraint_notes(constraint, actual_value, constraint_value, is_satisfied)

        return ValidationResult(
            constraint_name=constraint.name,
            is_satisfied=is_satisfied,
            actual_value=actual_value,
            constraint_value=constraint_value,
            tolerance_applied=tolerance_applied,
            violation_magnitude=violation_magnitude,
            historical_compliance=historical_compliance,
            notes=notes
        )

    def _extract_constraint_value(self, constraint: HistoricalConstraint,
                                simulation_results: Dict[str, Any]) -> float:
        """Extract the relevant value from simulation results."""

        # Map constraint names to simulation result keys
        value_mapping = {
            'human_power_sustained': ['power_required_watts', 'avg_power_W', 'power_W'],
            'human_power_peak': ['peak_power_W', 'max_power_W'],
            'max_tensile_stress_spruce': ['max_structural_stress_pa', 'max_stress_pa'],
            'max_tensile_stress_iron': ['max_iron_stress_pa'],
            'max_wood_span': ['wingspan', 'span', 'length'],
            'tip_speed_subsonic': ['tip_mach', 'tip_speed_ms'],
        }

        # Try to find the value in simulation results
        possible_keys = value_mapping.get(constraint.name, [constraint.name])

        for key in possible_keys:
            if key in simulation_results:
                value = simulation_results[key]

                # Handle unit conversions if needed
                if 'mach' in key and 'speed' in constraint.name:
                    # Convert Mach number to speed constraint
                    value = value * 343.0  # m/s at sea level

                return float(value)

        # If not found, try to compute it
        if constraint.name == 'tip_speed_subsonic':
            if 'tip_speed_ms' in simulation_results:
                return simulation_results['tip_speed_ms']
            elif 'rpm' in simulation_results and 'rotor_radius_m' in simulation_results:
                omega = 2 * np.pi * simulation_results['rpm'] / 60.0
                return omega * simulation_results['rotor_radius_m']

        # Default to 0 if not found
        logger.warning(f"Could not extract value for constraint {constraint.name}")
        return 0.0

    def _get_constraint_limit(self, constraint: HistoricalConstraint) -> float:
        """Get the numerical limit for a constraint."""

        # Extract limit from constraint function
        # This is a simplified approach - in practice, would need function analysis

        if 'tensile_stress' in constraint.name:
            if 'spruce' in constraint.name:
                return 40e6
            elif 'iron' in constraint.name:
                return 200e6
            elif 'linen' in constraint.name:
                return 20e6
        elif 'compressive_stress' in constraint.name:
            return 30e6
        elif 'shear_stress' in constraint.name:
            return 5e6
        elif 'fatigue_stress' in constraint.name:
            return 80e6
        elif 'human_power' in constraint.name:
            if 'sustained' in constraint.name:
                return 150.0
            elif 'peak' in constraint.name:
                return 300.0
        elif 'steam_power' in constraint.name:
            return 2000.0
        elif 'horse' in constraint.name:
            return 750.0
        elif 'wood_span' in constraint.name:
            return 15.0
        elif 'machining_tolerance' in constraint.name:
            return 0.5e-3  # Convert mm to m
        elif 'gear_ratio' in constraint.name:
            return 10.0
        elif 'joint_complexity' in constraint.name:
            return 50.0
        elif 'membrane_pressure' in constraint.name:
            return 5000.0

        # Default
        return 1.0

    def _generate_constraint_notes(self, constraint: HistoricalConstraint,
                                 actual_value: float, constraint_value: float,
                                 is_satisfied: bool) -> str:
        """Generate explanatory notes for constraint validation."""

        if is_satisfied:
            if constraint.tolerance_factor > 1.0:
                return (f"Within tolerance ({constraint.tolerance_factor:.1f}x). "
                       f"Actual: {actual_value:.2e}, Limit: {constraint_value:.2e}")
            else:
                return (f"Constraint satisfied. "
                       f"Actual: {actual_value:.2e}, Limit: {constraint_value:.2e}")
        else:
            if actual_value > constraint_value:
                return (f"Exceeds historical capability by "
                       f"{(actual_value/constraint_value - 1)*100:.1f}%. "
                       f"This would not be achievable with Renaissance technology.")
            else:
                return (f"Below minimum requirement. "
                       f"Actual: {actual_value:.2e}, Required: {constraint_value:.2e}")

    def _compute_overall_compliance(self, validation_results: List[ValidationResult]) -> float:
        """Compute overall compliance score (0-1)."""

        if not validation_results:
            return 0.0

        # Weight mandatory constraints more heavily
        total_weight = 0.0
        weighted_compliance = 0.0

        for result in validation_results:
            constraint = self._get_constraint_by_name(result.constraint_name)
            weight = 2.0 if constraint.mandatory else 1.0

            total_weight += weight
            weighted_compliance += result.historical_compliance * weight

        return weighted_compliance / total_weight if total_weight > 0 else 0.0

    def _compute_fidelity_rating(self, compliance_score: float) -> str:
        """Convert compliance score to rating."""

        if compliance_score >= 0.9:
            return "Excellent"
        elif compliance_score >= 0.75:
            return "Good"
        elif compliance_score >= 0.6:
            return "Fair"
        else:
            return "Poor"

    def _generate_recommendations(self, validation_results: List[ValidationResult]) -> List[str]:
        """Generate recommendations based on validation results."""

        recommendations = []

        for result in validation_results:
            if not result.is_satisfied:
                constraint = self._get_constraint_by_name(result.constraint_name)

                if 'power' in constraint.constraint_type:
                    if result.actual_value > constraint.constraint_value:
                        recommendations.append(
                            f"Reduce power requirements through mechanical advantage "
                            f"or accept reduced performance. Current: {result.actual_value:.1f}W, "
                            f"Historical limit: {constraint.constraint_value:.1f}W"
                        )

                elif 'material' in constraint.constraint_type:
                    if result.actual_value > constraint.constraint_value:
                        recommendations.append(
                            f"Use multiple smaller structural elements or change geometry "
                            f"to reduce stress. Current: {result.actual_value/1e6:.1f}MPa, "
                            f"Historical limit: {constraint.constraint_value/1e6:.1f}MPa"
                        )

                elif 'manufacturing' in constraint.constraint_type:
                    recommendations.append(
                        f"Simplify design to meet Renaissance manufacturing capabilities. "
                        f"Current complexity exceeds historical standards."
                    )

        # Add general recommendations if no specific ones
        if not recommendations:
            recommendations.append("Design appears historically feasible with Renaissance technology")

        return recommendations

    def _identify_enhancement_opportunities(self, invention_slug: str,
                                         validation_results: List[ValidationResult],
                                         simulation_results: Dict[str, Any]) -> List[str]:
        """Identify opportunities for enhancement while maintaining historical integrity."""

        opportunities = []

        # Look for underutilized capabilities
        if invention_slug in ['ornithopter', 'aerial_screw']:
            # Check if power is well within limits
            power_constraint = next((r for r in validation_results
                                   if 'human_power' in r.constraint_name), None)

            if power_constraint and power_constraint.is_satisfied:
                utilization = power_constraint.actual_value / power_constraint.constraint_value
                if utilization < 0.7:
                    opportunities.append(
                        f"Power utilization only {utilization*100:.0f}% of historical capacity. "
                        f"Could increase performance through larger wings or higher speeds."
                    )

            # Check if structural stress is conservative
            stress_constraint = next((r for r in validation_results
                                    if 'tensile_stress' in r.constraint_name), None)

            if stress_constraint and stress_constraint.is_satisfied:
                utilization = stress_constraint.actual_value / stress_constraint.constraint_value
                if utilization < 0.6:
                    opportunities.append(
                        f"Structural utilization only {utilization*100:.0f}% of material capacity. "
                        f"Could optimize structure for weight reduction or increased size."
                    )

        elif invention_slug in ['mechanical_organ', 'mechanical_drum']:
            # Musical instrument enhancements
            opportunities.append(
                "Consider implementing Renaissance tuning systems (meantone temperament) "
                "for historical authenticity in musical performance."
            )

        # General enhancement opportunities
        if all(r.is_satisfied for r in validation_results if r.mandatory):
            opportunities.append(
                "All mandatory constraints satisfied - consider pushing performance "
                "envelope while maintaining historical feasibility."
            )

        return opportunities

    def _get_constraint_by_name(self, name: str) -> HistoricalConstraint:
        """Get constraint by name from all constraint libraries."""

        for category_constraints in self.constraints.values():
            for constraint in category_constraints:
                if constraint.name == name:
                    return constraint

        # Return a dummy constraint if not found
        return HistoricalConstraint(
            name=name,
            description="Unknown constraint",
            source_manuscript="Unknown",
            constraint_type="unknown",
            constraint_function=lambda x: True
        )

    def generate_comparative_analysis(self, invention_slugs: List[str]) -> Dict[str, Any]:
        """
        Generate comparative analysis across multiple inventions.

        Args:
            invention_slugs: List of invention slugs to compare

        Returns:
            Comparative analysis results
        """

        # Filter validation history for requested inventions
        relevant_reports = [
            report for report in self.validation_history
            if report.invention_slug in invention_slugs
        ]

        if not relevant_reports:
            return {"error": "No validation data found for specified inventions"}

        # Compute comparative metrics
        comparison = {
            'inventions': {},
            'summary': {}
        }

        for slug in invention_slugs:
            slug_reports = [r for r in relevant_reports if r.invention_slug == slug]
            if slug_reports:
                latest_report = slug_reports[-1]
                comparison['inventions'][slug] = {
                    'compliance_score': latest_report.overall_compliance_score,
                    'fidelity_rating': latest_report.historical_fidelity_rating,
                    'mandatory_constraints_satisfied': latest_report.mandatory_constraints_satisfied,
                    'total_constraints': len(latest_report.validation_results),
                    'violated_constraints': len([r for r in latest_report.validation_results if not r.is_satisfied])
                }

        # Summary statistics
        all_scores = [data['compliance_score'] for data in comparison['inventions'].values()]
        comparison['summary'] = {
            'average_compliance': np.mean(all_scores),
            'best_performer': max(comparison['inventions'].items(), key=lambda x: x[1]['compliance_score'])[0],
            'worst_performer': min(comparison['inventions'].items(), key=lambda x: x[1]['compliance_score'])[0],
            'all_mandatory_satisfied': all(data['mandatory_constraints_satisfied'] for data in comparison['inventions'].values())
        }

        return comparison


def create_historical_validator() -> HistoricalValidator:
    """Factory function to create configured historical validator."""
    return HistoricalValidator()


if __name__ == "__main__":
    # Demonstration of historical validation framework

    print("Leonardo's Inventions - Historical Constraint Validation")
    print("=" * 60)

    # Create validator
    validator = create_historical_validator()

    # Example validation for ornithopter
    ornithopter_results = {
        'power_required_watts': 280.0,
        'max_structural_stress_pa': 25e6,
        'wingspan': 12.0,
        'tip_speed_ms': 45.0,
        'max_iron_stress_pa': 150e6
    }

    print("Validating Ornithopter Design...")
    report = validator.validate_invention('ornithopter', ornithopter_results)

    print(f"\nValidation Results:")
    print(f"Overall Compliance Score: {report.overall_compliance_score:.2f}")
    print(f"Historical Fidelity Rating: {report.historical_fidelity_rating}")
    print(f"Mandatory Constraints Satisfied: {report.mandatory_constraints_satisfied}")

    print(f"\nIndividual Constraint Results:")
    for result in report.validation_results:
        status = "✓" if result.is_satisfied else "✗"
        print(f"  {status} {result.constraint_name}: {result.notes}")

    print(f"\nRecommendations:")
    for rec in report.recommendations:
        print(f"  • {rec}")

    print(f"\nEnhancement Opportunities:")
    for opp in report.enhancement_opportunities:
        print(f"  • {opp}")

    # Comparative analysis example
    print(f"\n" + "="*60)
    print("Comparative Analysis Example")
    print("="*60)

    # Validate multiple inventions
    aerial_screw_results = {
        'power_required_watts': 1800.0,
        'max_structural_stress_pa': 15e6,
        'wingspan': 4.0,
        'tip_speed_ms': 25.0
    }

    cart_results = {
        'power_required_watts': 120.0,
        'max_structural_stress_pa': 8e6,
        'wingspan': 2.0,
        'max_iron_stress_pa': 50e6
    }

    validator.validate_invention('aerial_screw', aerial_screw_results)
    validator.validate_invention('self_propelled_cart', cart_results)

    comparison = validator.generate_comparative_analysis(['ornithopter', 'aerial_screw', 'self_propelled_cart'])

    print(f"Comparative Summary:")
    print(f"  Average Compliance: {comparison['summary']['average_compliance']:.2f}")
    print(f"  Best Performer: {comparison['summary']['best_performer']}")
    print(f"  Worst Performer: {comparison['summary']['worst_performer']}")

    print(f"\nIndividual Invention Scores:")
    for slug, data in comparison['inventions'].items():
        print(f"  {slug}: {data['compliance_score']:.2f} ({data['fidelity_rating']})")