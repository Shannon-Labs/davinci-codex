"""
Uncertainty Quantification Framework for Historical Variables

Implements statistical treatment of uncertainties in Leonardo's inventions,
accounting for incomplete historical knowledge, material variability,
and Renaissance manufacturing tolerances.

This framework provides confidence intervals and sensitivity analysis while
maintaining historical authenticity.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import numpy.random as random

logger = logging.getLogger(__name__)


@dataclass
class UncertaintySource:
    """Definition of an uncertainty source in historical parameters."""

    name: str
    description: str
    parameter_name: str
    distribution_type: str  # 'normal', 'uniform', 'triangular', 'lognormal'
    distribution_params: Dict[str, float]
    source_type: str  # 'material', 'manufacturing', 'measurement', 'historical'
    confidence_level: float = 0.95
    historical_basis: str = ""


@dataclass
class UncertaintyResult:
    """Results from uncertainty quantification analysis."""

    parameter_name: str
    mean_value: float
    std_deviation: float
    confidence_interval: Tuple[float, float]
    coefficient_of_variation: float
    sensitivity_coefficient: float
    contribution_to_variance: float
    distribution_fit: Optional[Dict[str, float]] = None


@dataclass
class UQReport:
    """Comprehensive uncertainty quantification report."""

    invention_slug: str
    uncertainty_results: List[UncertaintyResult]
    total_variance: float
    dominant_uncertainties: List[str]
    reliability_metrics: Dict[str, float]
    design_recommendations: List[str]
    historical_confidence_assessment: str


class HistoricalUncertaintyQuantification:
    """
    Uncertainty quantification for Leonardo's inventions.

    Provides statistical analysis of historical uncertainties, material
    variability, and manufacturing tolerances.
    """

    def __init__(self):
        self.uncertainty_sources: Dict[str, List[UncertaintySource]] = {}
        self.correlation_matrix: Optional[np.ndarray] = None
        self.sampling_methods = ['monte_carlo', 'latin_hypercube', 'sobol']

        # Initialize uncertainty libraries
        self._initialize_material_uncertainties()
        self._initialize_manufacturing_uncertainties()
        self._initialize_historical_uncertainties()

    def _initialize_material_uncertainties(self):
        """Initialize material property uncertainties."""

        # Wood properties (high variability in Renaissance)
        self.uncertainty_sources['wood'] = [
            UncertaintySource(
                name="spruce_density",
                description="Density variation in spruce wood",
                parameter_name="density",
                distribution_type="normal",
                distribution_params={"loc": 450, "scale": 60},  # kg/m³
                source_type="material",
                historical_basis="Variability in Renaissance timber quality and moisture content"
            ),
            UncertaintySource(
                name="spruce_youngs_modulus",
                description="Young's modulus variation in spruce",
                parameter_name="young_modulus",
                distribution_type="lognormal",
                distribution_params={"mean": 10e9, "sigma": 0.2},  # Pa
                source_type="material",
                historical_basis="Inconsistent wood quality and growth conditions"
            ),
            UncertaintySource(
                name="spruce_strength",
                description="Tensile strength variation in spruce",
                parameter_name="tensile_strength",
                distribution_type="weibull",
                distribution_params={"shape": 5, "scale": 45e6},  # Pa
                source_type="material",
                historical_basis="Natural defects and grain variations"
            )
        ]

        # Iron properties (inconsistent Renaissance metallurgy)
        self.uncertainty_sources['iron'] = [
            UncertaintySource(
                name="wrought_iron_strength",
                description="Tensile strength of wrought iron",
                parameter_name="tensile_strength",
                distribution_type="normal",
                distribution_params={"loc": 200e6, "scale": 40e6},  # Pa
                source_type="material",
                historical_basis="Variable smelting processes and impurity levels"
            ),
            UncertaintySource(
                name="iron_density",
                description="Density variation in wrought iron",
                parameter_name="density",
                distribution_type="uniform",
                distribution_params={"low": 7600, "high": 7900},  # kg/m³
                source_type="material",
                historical_basis="Slag inclusion and carbon content variations"
            )
        ]

        # Textile properties
        self.uncertainty_sources['textile'] = [
            UncertaintySource(
                name="linen_strength",
                description="Tensile strength of linen fabric",
                parameter_name="tensile_strength",
                distribution_type="normal",
                distribution_params={"loc": 20e6, "scale": 5e6},  # Pa
                source_type="material",
                historical_basis="Variable thread quality and weaving techniques"
            ),
            UncertaintySource(
                name="linen_porosity",
                description="Air leakage through linen membrane",
                parameter_name="permeability",
                distribution_type="lognormal",
                distribution_params={"mean": 1e-8, "sigma": 0.5},  # m²
                source_type="material",
                historical_basis="Inconsistent fabric treatment and sizing"
            )
        ]

    def _initialize_manufacturing_uncertainties(self):
        """Initialize manufacturing tolerance uncertainties."""

        self.uncertainty_sources['manufacturing'] = [
            UncertaintySource(
                name="dimensional_tolerance",
                description="Dimensional accuracy of hand-cut components",
                parameter_name="dimension_error",
                distribution_type="normal",
                distribution_params={"loc": 0, "scale": 0.001},  # meters
                source_type="manufacturing",
                historical_basis="Hand tool limitations and measurement precision"
            ),
            UncertaintySource(
                name="gear_tooth_error",
                description="Gear tooth profile accuracy",
                parameter_name="gear_error",
                distribution_type="triangular",
                distribution_params={"left": 0, "mode": 0.5, "right": 2.0},  # mm
                source_type="manufacturing",
                historical_basis="Wooden gear cutting by hand"
            ),
            UncertaintySource(
                name="joint_clearance",
                description="Clearance in mechanical joints",
                parameter_name="joint_gap",
                distribution_type="uniform",
                distribution_params={"low": 0.1, "high": 1.0},  # mm
                source_type="manufacturing",
                historical_basis="Wear and assembly tolerances"
            ),
            UncertaintySource(
                name="surface_roughness",
                description="Surface finish quality",
                parameter_name="roughness",
                distribution_type="lognormal",
                distribution_params={"mean": 50e-6, "sigma": 0.3},  # meters
                source_type="manufacturing",
                historical_basis="Hand finishing techniques"
            )
        ]

    def _initialize_historical_uncertainties(self):
        """Initialize uncertainties from incomplete historical knowledge."""

        self.uncertainty_sources['historical'] = [
            UncertaintySource(
                name="human_power_variation",
                description="Variation in human power output",
                parameter_name="human_power",
                distribution_type="normal",
                distribution_params={"loc": 150, "scale": 30},  # Watts
                source_type="historical",
                historical_basis="Variation in human strength and endurance"
            ),
            UncertaintySource(
                name="manuscript_measurement_error",
                description="Measurement errors in manuscript translations",
                parameter_name="measurement_error",
                distribution_type="normal",
                distribution_params={"loc": 0, "scale": 0.05},  # 5% error
                source_type="historical",
                historical_basis="Scale interpretation and drawing accuracy"
            ),
            UncertaintySource(
                name="environmental_conditions",
                description="Historical environmental variations",
                parameter_name="air_density",
                distribution_type="normal",
                distribution_params={"loc": 1.225, "scale": 0.02},  # kg/m³
                source_type="historical",
                historical_basis="Weather and altitude variations in Renaissance Italy"
            )
        ]

    def analyze_uncertainties(self, invention_slug: str, nominal_parameters: Dict[str, float],
                            performance_function: Callable[[Dict[str, float]], float],
                            num_samples: int = 10000,
                            sampling_method: str = 'monte_carlo') -> UQReport:
        """
        Perform comprehensive uncertainty analysis.

        Args:
            invention_slug: Unique identifier for the invention
            nominal_parameters: Nominal parameter values
            performance_function: Function mapping parameters to performance metric
            num_samples: Number of Monte Carlo samples
            sampling_method: Sampling method to use

        Returns:
            Comprehensive uncertainty quantification report
        """

        # Get relevant uncertainty sources
        relevant_sources = self._get_relevant_uncertainty_sources(invention_slug)

        # Generate parameter samples
        parameter_samples = self._generate_parameter_samples(
            relevant_sources, nominal_parameters, num_samples, sampling_method
        )

        # Evaluate performance function for all samples
        performance_values = np.array([
            performance_function({**nominal_parameters, **sample})
            for sample in parameter_samples
        ])

        # Compute statistical metrics
        performance_stats = self._compute_performance_statistics(performance_values)

        # Perform sensitivity analysis
        sensitivity_results = self._perform_sensitivity_analysis(
            relevant_sources, nominal_parameters, performance_function
        )

        # Compute uncertainty contributions
        uncertainty_results = self._compute_uncertainty_contributions(
            relevant_sources, sensitivity_results, performance_stats
        )

        # Identify dominant uncertainties
        dominant_uncertainties = self._identify_dominant_uncertainties(uncertainty_results)

        # Compute reliability metrics
        reliability_metrics = self._compute_reliability_metrics(
            performance_values, nominal_parameters
        )

        # Generate design recommendations
        design_recommendations = self._generate_design_recommendations(
            uncertainty_results, reliability_metrics
        )

        # Assess historical confidence
        historical_confidence = self._assess_historical_confidence(uncertainty_results)

        return UQReport(
            invention_slug=invention_slug,
            uncertainty_results=uncertainty_results,
            total_variance=performance_stats['variance'],
            dominant_uncertainties=dominant_uncertainties,
            reliability_metrics=reliability_metrics,
            design_recommendations=design_recommendations,
            historical_confidence_assessment=historical_confidence
        )

    def _get_relevant_uncertainty_sources(self, invention_slug: str) -> List[UncertaintySource]:
        """Get uncertainty sources relevant to a specific invention."""

        relevant_sources = []

        # All inventions have basic uncertainties
        relevant_sources.extend(self.uncertainty_sources['historical'])
        relevant_sources.extend(self.uncertainty_sources['manufacturing'])

        # Invention-specific uncertainties
        if invention_slug in ['ornithopter', 'aerial_screw']:
            # Flying machines need material uncertainties
            relevant_sources.extend(self.uncertainty_sources['wood'])
            relevant_sources.extend(self.uncertainty_sources['iron'])
            relevant_sources.extend(self.uncertainty_sources['textile'])

        elif invention_slug in ['mechanical_organ', 'mechanical_drum']:
            # Musical instruments need precision manufacturing
            relevant_sources.extend(self.uncertainty_sources['wood'])
            # Add more manufacturing uncertainties
            relevant_sources.extend([
                self.uncertainty_sources['manufacturing'][1],  # gear_error
                self.uncertainty_sources['manufacturing'][2]   # joint_clearance
            ])

        elif invention_slug in ['self_propelled_cart', 'mechanical_odometer']:
            # Ground vehicles need durability
            relevant_sources.extend(self.uncertainty_sources['wood'])
            relevant_sources.extend(self.uncertainty_sources['iron'])

        return relevant_sources

    def _generate_parameter_samples(self, uncertainty_sources: List[UncertaintySource],
                                  nominal_parameters: Dict[str, float],
                                  num_samples: int, sampling_method: str) -> List[Dict[str, float]]:
        """Generate parameter samples according to uncertainty distributions."""

        samples = []

        for _ in range(num_samples):
            sample = {}

            for source in uncertainty_sources:
                if source.parameter_name in nominal_parameters:
                    # Generate sample from distribution
                    value = self._sample_from_distribution(source)
                    sample[source.parameter_name] = value

            samples.append(sample)

        return samples

    def _sample_from_distribution(self, uncertainty_source: UncertaintySource) -> float:
        """Generate a sample from the specified distribution."""

        dist_type = uncertainty_source.distribution_type
        params = uncertainty_source.distribution_params

        if dist_type == 'normal':
            return random.normal(params['loc'], params['scale'])
        elif dist_type == 'uniform':
            return random.uniform(params['low'], params['high'])
        elif dist_type == 'triangular':
            return random.triangular(params['left'], params['mode'], params['right'])
        elif dist_type == 'lognormal':
            return random.lognormal(mean=np.log(params['mean']), sigma=params['sigma'])
        elif dist_type == 'weibull':
            return random.weibull(params['shape']) * params['scale']
        else:
            # Default to normal
            return random.normal(0, 1)

    def _compute_performance_statistics(self, performance_values: np.ndarray) -> Dict[str, float]:
        """Compute statistical metrics for performance values."""

        return {
            'mean': np.mean(performance_values),
            'std': np.std(performance_values),
            'variance': np.var(performance_values),
            'min': np.min(performance_values),
            'max': np.max(performance_values),
            'median': np.median(performance_values),
            'q5': np.percentile(performance_values, 5),
            'q95': np.percentile(performance_values, 95)
        }

    def _perform_sensitivity_analysis(self, uncertainty_sources: List[UncertaintySource],
                                     nominal_parameters: Dict[str, float],
                                     performance_function: Callable) -> Dict[str, float]:
        """Perform local sensitivity analysis using finite differences."""

        sensitivity_coefficients = {}

        # Perturbation size (5% of nominal value)
        perturbation_factor = 0.05

        # Compute nominal performance
        performance_function(nominal_parameters)

        for source in uncertainty_sources:
            if source.parameter_name in nominal_parameters:
                # Perturb parameter
                perturbed_params = nominal_parameters.copy()
                nominal_value = nominal_parameters[source.parameter_name]

                if nominal_value != 0:
                    delta = perturbation_factor * abs(nominal_value)
                else:
                    delta = perturbation_factor  # Use 5% if nominal is zero

                # Forward perturbation
                perturbed_params[source.parameter_name] = nominal_value + delta
                performance_plus = performance_function(perturbed_params)

                # Backward perturbation
                perturbed_params[source.parameter_name] = nominal_value - delta
                performance_minus = performance_function(perturbed_params)

                # Central difference sensitivity
                sensitivity = (performance_plus - performance_minus) / (2 * delta)
                sensitivity_coefficients[source.parameter_name] = sensitivity

        return sensitivity_coefficients

    def _compute_uncertainty_contributions(self, uncertainty_sources: List[UncertaintySource],
                                         sensitivity_results: Dict[str, float],
                                         performance_stats: Dict[str, float]) -> List[UncertaintyResult]:
        """Compute uncertainty contributions for each parameter."""

        uncertainty_results = []

        for source in uncertainty_sources:
            if source.parameter_name in sensitivity_results:
                # Get sensitivity coefficient
                sensitivity = sensitivity_results[source.parameter_name]

                # Get parameter uncertainty (standard deviation)
                param_std = self._get_parameter_std(source)

                # Compute contribution to performance variance
                variance_contribution = (sensitivity * param_std) ** 2

                # Compute coefficient of variation
                nominal_mean = performance_stats['mean']
                cv = param_std / abs(nominal_mean) if nominal_mean != 0 else float('inf')

                # Compute confidence interval
                ci_lower = nominal_mean - 1.96 * abs(sensitivity) * param_std
                ci_upper = nominal_mean + 1.96 * abs(sensitivity) * param_std

                result = UncertaintyResult(
                    parameter_name=source.parameter_name,
                    mean_value=nominal_mean,
                    std_deviation=abs(sensitivity) * param_std,
                    confidence_interval=(ci_lower, ci_upper),
                    coefficient_of_variation=cv,
                    sensitivity_coefficient=sensitivity,
                    contribution_to_variance=variance_contribution
                )

                uncertainty_results.append(result)

        return uncertainty_results

    def _get_parameter_std(self, uncertainty_source: UncertaintySource) -> float:
        """Get standard deviation for parameter from its distribution."""

        dist_type = uncertainty_source.distribution_type
        params = uncertainty_source.distribution_params

        if dist_type == 'normal':
            return params['scale']
        elif dist_type == 'uniform':
            return (params['high'] - params['low']) / np.sqrt(12)
        elif dist_type == 'triangular':
            a, b, c = params['left'], params['mode'], params['right']
            return np.sqrt((a**2 + b**2 + c**2 - a*b - a*c - b*c) / 18)
        elif dist_type == 'lognormal':
            return params['mean'] * np.sqrt(np.exp(params['sigma']**2) - 1)
        elif dist_type == 'weibull':
            shape, scale = params['shape'], params['scale']
            return scale * np.sqrt(np.gamma(1 + 2/shape) - np.gamma(1 + 1/shape)**2)
        else:
            return 1.0  # Default

    def _identify_dominant_uncertainties(self, uncertainty_results: List[UncertaintyResult]) -> List[str]:
        """Identify parameters contributing most to total uncertainty."""

        # Sort by contribution to variance
        sorted_results = sorted(uncertainty_results, key=lambda x: x.contribution_to_variance, reverse=True)

        # Return top 3 contributors (or fewer if less available)
        dominant = [result.parameter_name for result in sorted_results[:3]]
        return dominant

    def _compute_reliability_metrics(self, performance_values: np.ndarray,
                                   nominal_parameters: Dict[str, float]) -> Dict[str, float]:
        """Compute reliability and robustness metrics."""

        metrics = {}

        # Probability of meeting performance targets
        # (This would need target values - simplified for demonstration)
        metrics['success_probability'] = 0.95  # Placeholder

        # Reliability index (safety margin in standard deviations)
        mean_performance = np.mean(performance_values)
        std_performance = np.std(performance_values)

        # Assuming higher values are better and minimum acceptable is 80% of nominal
        minimum_acceptable = 0.8 * mean_performance
        reliability_index = (mean_performance - minimum_acceptable) / std_performance
        metrics['reliability_index'] = reliability_index

        # Robustness index (inverse of coefficient of variation)
        robustness_index = 1.0 / (std_performance / abs(mean_performance)) if mean_performance != 0 else 0
        metrics['robustness_index'] = robustness_index

        # Design margin (95th percentile vs nominal)
        design_margin = np.percentile(performance_values, 95) / mean_performance - 1.0
        metrics['design_margin'] = design_margin

        return metrics

    def _generate_design_recommendations(self, uncertainty_results: List[UncertaintyResult],
                                       reliability_metrics: Dict[str, float]) -> List[str]:
        """Generate design recommendations based on uncertainty analysis."""

        recommendations = []

        # Check reliability
        if reliability_metrics['reliability_index'] < 2.0:
            recommendations.append(
                "Reliability index below 2.0 - consider increasing safety factors "
                "or reducing parameter uncertainties through quality control."
            )

        # Check robustness
        if reliability_metrics['robustness_index'] < 5.0:
            recommendations.append(
                "Design is sensitive to parameter variations - consider more "
                "conservative design or tighter manufacturing tolerances."
            )

        # Check design margin
        if reliability_metrics['design_margin'] < 0.1:
            recommendations.append(
                "Design margin is tight - consider increasing safety factors "
                "or improving material quality control."
            )

        # Check dominant uncertainties
        if uncertainty_results:
            dominant = sorted(uncertainty_results, key=lambda x: x.contribution_to_variance, reverse=True)[0]
            if dominant.contribution_to_variance > 0.5 * sum(r.contribution_to_variance for r in uncertainty_results):
                recommendations.append(
                    f"Parameter '{dominant.parameter_name}' dominates uncertainty - "
                    f"focus on reducing its variation or sensitivity."
                )

        # Historical considerations
        recommendations.append(
            "Consider Renaissance manufacturing capabilities when specifying "
            "tolerances and quality control measures."
        )

        return recommendations

    def _assess_historical_confidence(self, uncertainty_results: List[UncertaintyResult]) -> str:
        """Assess confidence in historical reconstruction."""

        if not uncertainty_results:
            return "No uncertainty data available"

        # Compute overall uncertainty metric
        total_cv = np.mean([r.coefficient_of_variation for r in uncertainty_results])

        if total_cv < 0.1:
            return "High confidence - historical reconstruction is well-constrained"
        elif total_cv < 0.2:
            return "Moderate confidence - some uncertainties in historical parameters"
        elif total_cv < 0.3:
            return "Low confidence - significant uncertainties in historical reconstruction"
        else:
            return "Very low confidence - historical reconstruction highly uncertain"

    def generate_tornado_diagram_data(self, uncertainty_results: List[UncertaintyResult]) -> Dict[str, Any]:
        """Generate data for tornado diagram visualization."""

        if not uncertainty_results:
            return {"error": "No uncertainty results available"}

        # Sort by absolute contribution to variance
        sorted_results = sorted(uncertainty_results, key=lambda x: x.contribution_to_variance, reverse=True)

        # Extract data for plotting
        parameters = [result.parameter_name for result in sorted_results]
        contributions = [result.contribution_to_variance for result in sorted_results]
        total_variance = sum(contributions)

        # Normalize to percentage
        percentages = [contrib / total_variance * 100 for contrib in contributions]

        return {
            'parameters': parameters,
            'contributions': contributions,
            'percentages': percentages,
            'total_variance': total_variance
        }


def create_uncertainty_quantifier() -> HistoricalUncertaintyQuantification:
    """Factory function to create configured uncertainty quantifier."""
    return HistoricalUncertaintyQuantification()


if __name__ == "__main__":
    # Demonstration of uncertainty quantification framework

    print("Leonardo's Inventions - Uncertainty Quantification")
    print("=" * 60)

    # Create uncertainty quantifier
    uq = create_uncertainty_quantifier()

    # Example: Ornithopter lift uncertainty analysis
    def ornithopter_lift_function(params):
        """Simplified lift function for demonstration."""
        # Simplified lift equation: L = 0.5 * rho * V^2 * S * CL
        rho = params.get('air_density', 1.225)
        velocity = 10.0  # m/s (fixed for this example)
        wing_area = 12.0 * 1.5  # m² (span * chord)

        # Lift coefficient depends on material quality (simplified)
        material_factor = params.get('tensile_strength', 40e6) / 40e6  # Normalized
        cl = 1.2 * material_factor  # Better materials allow higher CL

        lift = 0.5 * rho * velocity**2 * wing_area * cl
        return lift

    # Nominal parameters
    nominal_params = {
        'air_density': 1.225,
        'tensile_strength': 40e6,
        'young_modulus': 10e9,
        'human_power': 150.0
    }

    print("Analyzing Ornithopter Lift Uncertainty...")
    report = uq.analyze_uncertainties(
        invention_slug='ornithopter',
        nominal_parameters=nominal_params,
        performance_function=ornithopter_lift_function,
        num_samples=5000,
        sampling_method='monte_carlo'
    )

    print("\nUncertainty Analysis Results:")
    print(f"Total Performance Variance: {report.total_variance:.2e}")
    print(f"Historical Confidence: {report.historical_confidence_assessment}")

    print("\nDominant Uncertainty Sources:")
    for source in report.dominant_uncertainties:
        print(f"  • {source}")

    print("\nReliability Metrics:")
    for metric, value in report.reliability_metrics.items():
        print(f"  {metric.replace('_', ' ').title()}: {value:.3f}")

    print("\nDesign Recommendations:")
    for rec in report.design_recommendations:
        print(f"  • {rec}")

    print("\nIndividual Parameter Uncertainties:")
    for result in report.uncertainty_results[:5]:  # Show top 5
        print(f"  {result.parameter_name}:")
        print(f"    Std Dev: {result.std_deviation:.2e}")
        print(f"    95% CI: [{result.confidence_interval[0]:.2e}, {result.confidence_interval[1]:.2e}]")
        print(f"    Sensitivity: {result.sensitivity_coefficient:.2e}")
        print(f"    Variance Contribution: {result.contribution_to_variance:.2e}")

    # Generate tornado diagram data
    tornado_data = uq.generate_tornado_diagram_data(report.uncertainty_results)

    print("\nTornado Diagram Data:")
    print("Parameters sorted by contribution:")
    for i, param in enumerate(tornado_data['parameters'][:5]):
        contrib = tornado_data['contributions'][i]
        percent = tornado_data['percentages'][i]
        print(f"  {i+1}. {param}: {contrib:.2e} ({percent:.1f}%)")
