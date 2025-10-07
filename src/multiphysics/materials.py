"""
Bio-Inspired Materials Research and Optimization Framework

Advanced materials modeling combining modern computational methods
with Leonardo's Renaissance engineering principles.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Tuple

import numpy as np
import scipy.optimize as opt

logger = logging.getLogger(__name__)


@dataclass
class MaterialModel:
    """Advanced material model with uncertainty quantification."""

    name: str
    base_properties: Dict[str, float]
    uncertainty_bounds: Dict[str, Tuple[float, float]]
    temperature_dependence: Dict[str, Callable[[float], float]] = field(default_factory=dict)
    moisture_dependence: Dict[str, Callable[[float], float]] = field(default_factory=dict)
    microstructure_parameters: Dict[str, float] = field(default_factory=dict)

    def get_property(self, property_name: str, temperature: float = 293.15,
                    moisture: float = 0.0, uncertainty_factor: float = 1.0) -> float:
        """Get material property with environmental and uncertainty effects."""

        base_value = self.base_properties.get(property_name, 0.0)

        # Temperature effects
        if property_name in self.temperature_dependence:
            temp_factor = self.temperature_dependence[property_name](temperature)
            base_value *= temp_factor

        # Moisture effects
        if property_name in self.moisture_dependence:
            moisture_factor = self.moisture_dependence[property_name](moisture)
            base_value *= moisture_factor

        # Uncertainty
        if property_name in self.uncertainty_bounds:
            lower, upper = self.uncertainty_bounds[property_name]
            uncertainty_range = upper - lower
            uncertainty_offset = (uncertainty_factor - 1.0) * uncertainty_range / 2
            base_value += uncertainty_offset

        return base_value


class BioinspiredOptimizer:
    """Nature-inspired optimization algorithms for material and structural design."""

    def __init__(self, algorithm: str = "genetic", population_size: int = 50):
        self.algorithm = algorithm
        self.population_size = population_size
        self.best_solution = None
        self.best_fitness = float('-inf')
        self.convergence_history = []

        # Genetic algorithm parameters
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8

        logger.info(f"Initialized {algorithm} optimizer")

    def optimize(self, objective_function: Callable, bounds: List[Tuple[float, float]],
                max_iterations: int = 100) -> Dict[str, Any]:
        """Run bio-inspired optimization."""

        self.bounds = bounds
        self.dimension = len(bounds)

        if self.algorithm == "genetic":
            return self._genetic_algorithm(objective_function, max_iterations)
        else:
            # Fallback to scipy optimization
            result = opt.differential_evolution(
                lambda x: -objective_function(x),  # Minimize negative
                bounds=bounds,
                maxiter=max_iterations,
                popsize=15
            )

            return {
                'best_solution': result.x,
                'best_fitness': -result.fun,
                'convergence_history': [],
                'iterations': result.nit
            }

    def _genetic_algorithm(self, objective_func: Callable, max_iter: int) -> Dict[str, Any]:
        """Genetic Algorithm implementation."""

        # Initialize population
        population = self._initialize_population()

        for generation in range(max_iter):
            # Evaluate fitness
            fitness_values = np.array([objective_func(individual) for individual in population])

            # Track best solution
            best_idx = np.argmax(fitness_values)
            if fitness_values[best_idx] > self.best_fitness:
                self.best_fitness = fitness_values[best_idx]
                self.best_solution = population[best_idx].copy()

            self.convergence_history.append(self.best_fitness)

            # Selection, crossover, mutation
            new_population = []

            # Keep best individual (elitism)
            new_population.append(population[best_idx])

            # Generate rest of population
            while len(new_population) < self.population_size:
                # Tournament selection
                parent1 = self._tournament_selection(population, fitness_values)
                parent2 = self._tournament_selection(population, fitness_values)

                # Crossover
                if np.random.random() < self.crossover_rate:
                    child1, child2 = self._crossover(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()

                # Mutation
                child1 = self._mutation(child1)
                child2 = self._mutation(child2)

                new_population.extend([child1, child2])

            population = np.array(new_population[:self.population_size])

            if generation % 20 == 0:
                logger.info(f"Generation {generation}: Best fitness = {self.best_fitness:.6f}")

        return {
            'best_solution': self.best_solution,
            'best_fitness': self.best_fitness,
            'convergence_history': self.convergence_history,
            'generations': generation + 1
        }

    def _initialize_population(self) -> np.ndarray:
        """Initialize random population within bounds."""

        population = np.zeros((self.population_size, self.dimension))

        for i in range(self.population_size):
            for j in range(self.dimension):
                min_val, max_val = self.bounds[j]
                population[i, j] = np.random.uniform(min_val, max_val)

        return population

    def _tournament_selection(self, population: np.ndarray, fitness: np.ndarray) -> np.ndarray:
        """Tournament selection."""

        tournament_size = 3
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitness = fitness[tournament_indices]
        winner_idx = tournament_indices[np.argmax(tournament_fitness)]

        return population[winner_idx].copy()

    def _crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Single-point crossover."""

        crossover_point = np.random.randint(1, len(parent1))

        child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
        child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])

        return child1, child2

    def _mutation(self, individual: np.ndarray) -> np.ndarray:
        """Gaussian mutation."""

        mutated = individual.copy()

        for i in range(len(individual)):
            if np.random.random() < self.mutation_rate:
                min_val, max_val = self.bounds[i]

                # Gaussian perturbation
                sigma = (max_val - min_val) * 0.1
                perturbation = np.random.normal(0, sigma)

                mutated[i] = np.clip(individual[i] + perturbation, min_val, max_val)

        return mutated


class MaterialsResearchFramework:
    """Advanced materials research framework."""

    def __init__(self):
        self.material_models = {}
        self._initialize_materials()
        logger.info("Materials research framework initialized")

    def _initialize_materials(self):
        """Initialize material models."""

        # Renaissance oak timber
        oak_temp_deps = {
            'young_modulus': lambda T: 1.0 - 0.002 * (T - 293.15),
            'yield_strength': lambda T: 1.0 - 0.001 * (T - 293.15)
        }

        self.material_models['renaissance_oak'] = MaterialModel(
            name="Renaissance Oak Timber",
            base_properties={
                'density': 700.0,
                'young_modulus': 12e9,
                'poisson_ratio': 0.35,
                'yield_strength': 40e6,
                'ultimate_strength': 50e6,
                'fracture_toughness': 1.2e6
            },
            uncertainty_bounds={
                'density': (600.0, 800.0),
                'young_modulus': (8e9, 16e9),
                'yield_strength': (25e6, 55e6)
            },
            temperature_dependence=oak_temp_deps,
            microstructure_parameters={
                'grain_density': 450,
                'fiber_angle': 15.0,
                'growth_ring_spacing': 2.5
            }
        )

        # Modern carbon fiber composite
        self.material_models['carbon_composite'] = MaterialModel(
            name="Bio-Inspired Carbon Fiber Composite",
            base_properties={
                'density': 1600.0,
                'young_modulus': 150e9,
                'poisson_ratio': 0.28,
                'yield_strength': 2000e6,
                'ultimate_strength': 2500e6,
                'fracture_toughness': 120e6
            },
            uncertainty_bounds={
                'young_modulus': (140e9, 160e9),
                'yield_strength': (1800e6, 2200e6)
            },
            microstructure_parameters={
                'fiber_volume_fraction': 0.6,
                'fiber_orientation': 0.0,
                'laminate_stacking': '[0/45/-45/90]s'
            }
        )

        # Biomimetic honeycomb
        self.material_models['bio_honeycomb'] = MaterialModel(
            name="Biomimetic Honeycomb Core",
            base_properties={
                'density': 100.0,
                'young_modulus': 2e6,
                'poisson_ratio': 0.0,
                'yield_strength': 3e6,
                'ultimate_strength': 5e6,
                'fracture_toughness': 0.8e6
            },
            uncertainty_bounds={
                'density': (80.0, 120.0),
                'young_modulus': (1.5e6, 2.5e6)
            },
            microstructure_parameters={
                'cell_size': 6.0,
                'wall_thickness': 0.1,
                'cell_angle': 120.0
            }
        )

    def optimize_material_selection(self, design_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize material selection for design requirements."""

        def material_objective(params):
            """Multi-objective fitness function."""

            target_strength = params[0]
            weight_factor = params[1]
            cost_factor = params[2]

            total_fitness = 0.0

            for material_name, material_model in self.material_models.items():
                density = material_model.get_property('density')
                strength = material_model.get_property('yield_strength')

                # Performance metrics
                strength_score = min(strength / target_strength, 2.0)
                weight_score = 1000.0 / density  # Lower density is better
                cost_score = self._get_cost_score(material_name)

                # Weighted fitness
                material_fitness = (
                    0.5 * strength_score +
                    0.3 * weight_score * weight_factor +
                    0.2 * cost_score * cost_factor
                )

                total_fitness += material_fitness

            return total_fitness

        # Optimization bounds
        bounds = [
            (1e6, 500e6),   # Target strength (Pa)
            (0.1, 2.0),     # Weight factor
            (0.1, 2.0)      # Cost factor
        ]

        # Run optimization
        optimizer = BioinspiredOptimizer(algorithm="genetic", population_size=20)
        result = optimizer.optimize(material_objective, bounds, max_iterations=30)

        # Rank materials
        best_params = result['best_solution']
        material_rankings = self._rank_materials(best_params)

        return {
            'optimization_result': result,
            'recommended_materials': material_rankings,
            'design_parameters': {
                'target_strength': best_params[0],
                'weight_factor': best_params[1],
                'cost_factor': best_params[2]
            }
        }

    def _get_cost_score(self, material_name: str) -> float:
        """Get relative cost score (higher is better)."""

        cost_factors = {
            'renaissance_oak': 0.8,
            'carbon_composite': 0.2,
            'bio_honeycomb': 0.4
        }

        return cost_factors.get(material_name, 0.5)

    def _rank_materials(self, optimization_params: np.ndarray) -> List[Dict[str, Any]]:
        """Rank materials based on optimization parameters."""

        target_strength = optimization_params[0]
        weight_factor = optimization_params[1]
        cost_factor = optimization_params[2]

        material_scores = []

        for material_name, material_model in self.material_models.items():
            density = material_model.get_property('density')
            strength = material_model.get_property('yield_strength')

            strength_score = min(strength / target_strength, 2.0)
            weight_score = 1000.0 / density
            cost_score = self._get_cost_score(material_name)

            total_score = (
                0.5 * strength_score +
                0.3 * weight_score * weight_factor +
                0.2 * cost_score * cost_factor
            )

            material_scores.append({
                'material_name': material_name,
                'total_score': total_score,
                'strength_score': strength_score,
                'weight_score': weight_score,
                'cost_score': cost_score,
                'properties': {
                    'density': density,
                    'strength': strength,
                    'young_modulus': material_model.get_property('young_modulus')
                }
            })

        # Sort by total score (descending)
        material_scores.sort(key=lambda x: x['total_score'], reverse=True)

        return material_scores

    def analyze_uncertainty_propagation(self, material_name: str,
                                      load_conditions: Dict[str, float]) -> Dict[str, Any]:
        """Analyze uncertainty propagation in material properties."""

        if material_name not in self.material_models:
            raise ValueError(f"Unknown material: {material_name}")

        material = self.material_models[material_name]

        # Monte Carlo simulation for uncertainty analysis
        num_samples = 1000
        results = []

        for _ in range(num_samples):
            # Sample uncertainty factors
            uncertainty_factors = {}
            for prop_name in material.uncertainty_bounds:
                lower, upper = material.uncertainty_bounds[prop_name]
                base_val = material.base_properties[prop_name]

                # Sample within uncertainty bounds
                uncertainty_factor = np.random.uniform(
                    lower / base_val, upper / base_val
                )
                uncertainty_factors[prop_name] = uncertainty_factor

            # Get properties with uncertainty
            temp = load_conditions.get('temperature', 293.15)
            moisture = load_conditions.get('moisture', 0.0)

            sampled_properties = {}
            for prop_name in material.base_properties:
                uncertainty_factor = uncertainty_factors.get(prop_name, 1.0)
                prop_value = material.get_property(
                    prop_name, temp, moisture, uncertainty_factor
                )
                sampled_properties[prop_name] = prop_value

            results.append(sampled_properties)

        # Statistical analysis
        statistics = {}
        for prop_name in material.base_properties:
            values = [result[prop_name] for result in results]

            statistics[prop_name] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'percentile_5': np.percentile(values, 5),
                'percentile_95': np.percentile(values, 95)
            }

        return {
            'material_name': material_name,
            'load_conditions': load_conditions,
            'statistics': statistics,
            'num_samples': num_samples,
            'sample_results': results[:10]  # Return first 10 samples
        }

    def design_bio_inspired_composite(self, performance_targets: Dict[str, float]) -> Dict[str, Any]:
        """Design bio-inspired composite material."""

        def composite_objective(design_vars):
            """Objective function for composite design."""

            fiber_volume_fraction = design_vars[0]
            fiber_angle = design_vars[1]
            design_vars[2]

            # Simplified composite mechanics
            fiber_modulus = 230e9  # Carbon fiber
            matrix_modulus = 3.5e9  # Epoxy

            # Rule of mixtures (simplified)
            composite_modulus = (fiber_volume_fraction * fiber_modulus +
                               (1 - fiber_volume_fraction) * matrix_modulus)

            # Angle effects (simplified)
            angle_factor = np.cos(np.radians(fiber_angle)) ** 2
            effective_modulus = composite_modulus * angle_factor

            # Density
            fiber_density = 1800.0
            matrix_density = 1200.0
            composite_density = (fiber_volume_fraction * fiber_density +
                               (1 - fiber_volume_fraction) * matrix_density)

            # Performance metrics
            modulus_score = effective_modulus / performance_targets.get('modulus', 100e9)
            density_score = performance_targets.get('max_density', 2000.0) / composite_density

            return modulus_score * density_score

        # Design variable bounds
        bounds = [
            (0.3, 0.7),   # Fiber volume fraction
            (0.0, 45.0),  # Fiber angle (degrees)
            (0.1, 1.0)    # Layer thickness (mm)
        ]

        # Optimize composite design
        optimizer = BioinspiredOptimizer(algorithm="genetic", population_size=15)
        result = optimizer.optimize(composite_objective, bounds, max_iterations=25)

        # Extract optimal design
        optimal_design = result['best_solution']

        return {
            'optimization_result': result,
            'optimal_design': {
                'fiber_volume_fraction': optimal_design[0],
                'fiber_angle': optimal_design[1],
                'layer_thickness': optimal_design[2]
            },
            'predicted_properties': self._predict_composite_properties(optimal_design),
            'bio_inspiration': "Inspired by layered structure of bird feathers and bamboo"
        }

    def _predict_composite_properties(self, design_vars: np.ndarray) -> Dict[str, float]:
        """Predict composite properties from design variables."""

        fiber_volume_fraction = design_vars[0]
        fiber_angle = design_vars[1]

        # Simplified predictions
        fiber_modulus = 230e9
        matrix_modulus = 3.5e9

        composite_modulus = (fiber_volume_fraction * fiber_modulus +
                           (1 - fiber_volume_fraction) * matrix_modulus)

        angle_factor = np.cos(np.radians(fiber_angle)) ** 2
        effective_modulus = composite_modulus * angle_factor

        fiber_density = 1800.0
        matrix_density = 1200.0
        composite_density = (fiber_volume_fraction * fiber_density +
                           (1 - fiber_volume_fraction) * matrix_density)

        return {
            'young_modulus': effective_modulus,
            'density': composite_density,
            'specific_modulus': effective_modulus / composite_density
        }
