"""
Material Selection Matrix for Leonardo's Mechanical Lion
Decision-making framework for optimal material selection
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from lion_materials_analysis import LionMaterialsAnalyzer
from renaissance_materials_database import RenaissanceMaterialsDatabase


@dataclass
class SelectionCriteria:
    """Criteria for material selection decisions."""
    name: str
    weight: float  # 0.0-1.0 importance weighting
    min_acceptable: float
    optimal_value: float
    description: str


@dataclass
class MaterialAlternative:
    """Alternative material option with analysis."""
    material_name: str
    score: float
    confidence: float
    advantages: List[str]
    disadvantages: List[str]
    risk_factors: List[str]
    mitigation_strategies: List[str]


class MaterialSelectionMatrix:
    """Comprehensive material selection decision framework."""
    
    def __init__(self):
        self.analyzer = LionMaterialsAnalyzer()
        self.db = RenaissanceMaterialsDatabase()
        self.selection_criteria = self._define_selection_criteria()
        self.component_matrix = {}
        self.final_recommendations = {}
    
    def _define_selection_criteria(self) -> Dict[str, SelectionCriteria]:
        """Define comprehensive selection criteria."""
        
        criteria = {}
        
        # === TECHNICAL PERFORMANCE CRITERIA ===
        
        criteria['strength_adequacy'] = SelectionCriteria(
            name="Strength Adequacy",
            weight=0.20,
            min_acceptable=0.8,  # 80% of required strength minimum
            optimal_value=1.5,   # 150% of required strength
            description="Material must meet or exceed strength requirements with safety margin"
        )
        
        criteria['weight_efficiency'] = SelectionCriteria(
            name="Weight Efficiency",
            weight=0.15,
            min_acceptable=0.6,
            optimal_value=1.0,
            description="High strength-to-weight ratio for mobile applications"
        )
        
        criteria['fatigue_resistance'] = SelectionCriteria(
            name="Fatigue Resistance",
            weight=0.12,
            min_acceptable=0.7,
            optimal_value=1.0,
            description="Ability to withstand cyclic loading for repeated performances"
        )
        
        criteria['wear_resistance'] = SelectionCriteria(
            name="Wear Resistance",
            weight=0.10,
            min_acceptable=0.8,
            optimal_value=1.0,
            description="Resistance to surface degradation in moving applications"
        )
        
        # === ENVIRONMENTAL CRITERIA ===
        
        criteria['environmental_stability'] = SelectionCriteria(
            name="Environmental Stability",
            weight=0.08,
            min_acceptable=0.7,
            optimal_value=1.0,
            description="Performance consistency in palace environments"
        )
        
        criteria['corrosion_resistance'] = SelectionCriteria(
            name="Corrosion Resistance",
            weight=0.06,
            min_acceptable=0.6,
            optimal_value=1.0,
            description="Resistance to environmental degradation"
        )
        
        # === MANUFACTURING CRITERIA ===
        
        criteria['workability'] = SelectionCriteria(
            name="Workability",
            weight=0.08,
            min_acceptable=0.5,
            optimal_value=1.0,
            description="Ease of fabrication with Renaissance workshop tools"
        )
        
        criteria['joinability'] = SelectionCriteria(
            name="Joinability",
            weight=0.06,
            min_acceptable=0.6,
            optimal_value=1.0,
            description="Compatibility with traditional joining methods"
        )
        
        # === ECONOMIC CRITERIA ===
        
        criteria['cost_effectiveness'] = SelectionCriteria(
            name="Cost Effectiveness",
            weight=0.08,
            min_acceptable=0.4,
            optimal_value=1.0,
            description="Material cost relative to royal commission budget"
        )
        
        criteria['availability'] = SelectionCriteria(
            name="Material Availability",
            weight=0.07,
            min_acceptable=0.6,
            optimal_value=1.0,
            description="Reliability of supply chain in Renaissance Florence"
        )
        
        return criteria
    
    def create_component_matrix(self, component_name: str) -> Dict[str, Dict]:
        """Create detailed selection matrix for a component."""
        
        # Get component requirements and material candidates
        requirement = self.analyzer.component_requirements.get(component_name)
        material_scores = self.analyzer.analyze_component_materials(component_name)
        
        # Select top 5 materials for detailed analysis
        candidate_materials = material_scores[:5]
        
        matrix = {
            "component": component_name,
            "requirement": requirement,
            "candidates": {},
            "criteria_weights": {name: crit.weight for name, crit in self.selection_criteria.items()},
            "decision_analysis": {}
        }
        
        # Analyze each candidate material against criteria
        for material_name, base_score in candidate_materials:
            material = self.db.get_material(material_name)
            
            criteria_scores = self._evaluate_material_against_criteria(material, requirement)
            weighted_score = self._calculate_weighted_score(criteria_scores)
            
            matrix["candidates"][material_name] = {
                "material": material,
                "base_score": base_score,
                "criteria_scores": criteria_scores,
                "weighted_score": weighted_score,
                "meets_minimum_requirements": self._check_minimum_requirements(criteria_scores)
            }
        
        # Decision analysis
        matrix["decision_analysis"] = self._perform_decision_analysis(matrix["candidates"])
        
        self.component_matrix[component_name] = matrix
        return matrix
    
    def _evaluate_material_against_criteria(self, material, requirement) -> Dict[str, float]:
        """Evaluate material against all selection criteria."""
        
        scores = {}
        
        for criterion_name, criterion in self.selection_criteria.items():
            
            if criterion_name == 'strength_adequacy':
                # Calculate strength ratio
                strength_ratio = material.tensile_strength_pa / requirement.min_strength_pa
                score = min(1.0, strength_ratio / criterion.optimal_value)
            
            elif criterion_name == 'weight_efficiency':
                # Strength-to-weight ratio
                strength_to_weight = material.tensile_strength_pa / material.density_kg_m3
                # Normalize against reference (oak = 53.3 kN⋅m/kg)
                reference_ratio = 53.3e3
                score = min(1.0, strength_to_weight / reference_ratio)
            
            elif criterion_name == 'fatigue_resistance':
                # Based on material type and loading conditions
                fatigue_ratings = {
                    "Iron Alloy": 0.9,
                    "Copper Alloy": 0.7,
                    "Hardwood": 0.6,
                    "Softwood": 0.4
                }
                base_rating = fatigue_ratings.get(material.material_type, 0.5)
                
                # Adjust for loading type
                if requirement.loading_type == "Fatigue":
                    score = base_rating
                elif requirement.loading_type == "Wear":
                    score = base_rating * 0.8
                else:
                    score = base_rating * 1.2
                
                score = min(1.0, score)
            
            elif criterion_name == 'wear_resistance':
                # Based on durability rating
                score = material.durability_rating / 5.0
                
                # Adjust for motion type
                if requirement.motion_type in ["Rotating", "Sliding"]:
                    score = min(1.0, score * 1.2)
            
            elif criterion_name == 'environmental_stability':
                # Based on weather resistance
                score = material.weather_resistance / 5.0
                
                # Adjust for exposure
                exposure_factors = {
                    "Protected": 1.2,
                    "Semi-exposed": 1.0,
                    "Exposed": 0.8
                }
                score *= exposure_factors.get(requirement.environmental_exposure, 1.0)
                score = min(1.0, score)
            
            elif criterion_name == 'corrosion_resistance':
                # Material-specific corrosion resistance
                corrosion_ratings = {
                    "Copper Alloy": 0.9,
                    "Precious Metal": 1.0,
                    "Iron Alloy": 0.4,
                    "Hardwood": 0.7,
                    "Softwood": 0.6
                }
                score = corrosion_ratings.get(material.material_type, 0.5)
            
            elif criterion_name == 'workability':
                # Direct from material rating
                score = material.workability / 5.0
            
            elif criterion_name == 'joinability':
                # Based on material type and traditional methods
                joinability_ratings = {
                    "Hardwood": 0.9,  # Excellent traditional joinery
                    "Softwood": 0.8,
                    "Iron Alloy": 0.7,  # Forging and riveting
                    "Copper Alloy": 0.6,  # Casting and mechanical fastening
                    "Precious Metal": 0.4   # Specialized techniques
                }
                score = joinability_ratings.get(material.material_type, 0.5)
            
            elif criterion_name == 'cost_effectiveness':
                # Inverse cost relationship (lower cost = higher score)
                # Normalize against reference cost (50 florins)
                reference_cost = 50.0
                cost_ratio = reference_cost / material.cost_per_unit
                score = min(1.0, cost_ratio)
            
            elif criterion_name == 'availability':
                # Based on availability category
                availability_scores = {
                    "Local": 1.0,
                    "Regional": 0.8,
                    "International": 0.5,
                    "Rare": 0.2
                }
                score = availability_scores.get(material.availability, 0.3)
            
            else:
                score = 0.5  # Default score
            
            scores[criterion_name] = score
        
        return scores
    
    def _calculate_weighted_score(self, criteria_scores: Dict[str, float]) -> float:
        """Calculate weighted score from criteria scores."""
        
        total_score = 0.0
        total_weight = 0.0
        
        for criterion_name, score in criteria_scores.items():
            criterion = self.selection_criteria[criterion_name]
            total_score += score * criterion.weight
            total_weight += criterion.weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _check_minimum_requirements(self, criteria_scores: Dict[str, float]) -> bool:
        """Check if material meets minimum requirements."""
        
        for criterion_name, score in criteria_scores.items():
            criterion = self.selection_criteria[criterion_name]
            if score < criterion.min_acceptable:
                return False
        
        return True
    
    def _perform_decision_analysis(self, candidates: Dict) -> Dict:
        """Perform comprehensive decision analysis."""
        
        # Filter candidates meeting minimum requirements
        viable_candidates = {
            name: data for name, data in candidates.items()
            if data["meets_minimum_requirements"]
        }
        
        if not viable_candidates:
            # No candidates meet minimum requirements - select closest
            best_candidate = max(candidates.items(), key=lambda x: x[1]["weighted_score"])
            return {
                "recommended": best_candidate[0],
                "confidence": 0.3,
                "risk_level": "High",
                "alternatives": [],
                "recommendation_notes": [
                    "No material meets all minimum requirements",
                    "Significant design modifications required",
                    "Consider alternative engineering solutions"
                ]
            }
        
        # Select best candidate
        best_candidate = max(viable_candidates.items(), key=lambda x: x[1]["weighted_score"])
        best_name = best_candidate[0]
        best_data = best_candidate[1]
        
        # Calculate confidence
        confidence = min(1.0, best_data["weighted_score"] / 0.8)
        
        # Determine risk level
        if confidence >= 0.8:
            risk_level = "Low"
        elif confidence >= 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Select alternatives
        alternatives = [
            (name, data) for name, data in viable_candidates.items()
            if name != best_name
        ][:2]  # Top 2 alternatives
        
        # Generate recommendation notes
        notes = self._generate_recommendation_notes(best_data, alternatives)
        
        return {
            "recommended": best_name,
            "confidence": confidence,
            "risk_level": risk_level,
            "alternatives": [alt[0] for alt in alternatives],
            "recommendation_notes": notes
        }
    
    def _generate_recommendation_notes(self, best_data: Dict, alternatives: List) -> List[str]:
        """Generate recommendation analysis notes."""
        
        notes = []
        material = best_data["material"]
        
        # Strength analysis
        if best_data["criteria_scores"]["strength_adequacy"] >= 1.0:
            notes.append("Exceeds strength requirements with good safety margin")
        elif best_data["criteria_scores"]["strength_adequacy"] >= 0.8:
            notes.append("Meets strength requirements adequately")
        else:
            notes.append("Marginal strength - careful design required")
        
        # Cost analysis
        if best_data["criteria_scores"]["cost_effectiveness"] >= 0.8:
            notes.append("Cost-effective solution for royal commission")
        elif best_data["criteria_scores"]["cost_effectiveness"] >= 0.5:
            notes.append("Moderate cost - appropriate for importance")
        else:
            notes.append("Premium material - justified for royal commission")
        
        # Availability analysis
        if material.availability == "Local":
            notes.append("Readily available from Florentine suppliers")
        elif material.availability == "Regional":
            notes.append("Available through regional trade networks")
        else:
            notes.append("Extended lead time - plan acquisition carefully")
        
        # Manufacturing considerations
        if best_data["criteria_scores"]["workability"] >= 0.8:
            notes.append("Excellent workability with Renaissance tools")
        elif best_data["criteria_scores"]["workability"] >= 0.6:
            notes.append("Good workability with skilled craftsmen")
        else:
            notes.append("Challenging to work - requires specialist expertise")
        
        # Alternative analysis
        if alternatives:
            alt_name = alternatives[0][1]["material"].name
            notes.append(f"Consider {alt_name} as backup if primary supply issues")
        
        return notes
    
    def generate_comprehensive_matrix(self) -> Dict[str, Dict]:
        """Generate selection matrix for all components."""
        
        all_components = list(self.analyzer.component_requirements.keys())
        
        for component_name in all_components:
            print(f"Creating selection matrix for {component_name}...")
            self.create_component_matrix(component_name)
        
        return self.component_matrix
    
    def generate_final_recommendations(self) -> Dict[str, MaterialAlternative]:
        """Generate final material recommendations with alternatives analysis."""
        
        recommendations = {}
        
        for component_name, matrix in self.component_matrix.items():
            decision = matrix["decision_analysis"]
            primary_name = decision["recommended"]
            primary_data = matrix["candidates"][primary_name]
            
            # Create material alternative
            alternative = MaterialAlternative(
                material_name=primary_name,
                score=primary_data["weighted_score"],
                confidence=decision["confidence"],
                advantages=self._extract_advantages(primary_data),
                disadvantages=self._extract_disadvantages(primary_data),
                risk_factors=self._identify_risk_factors(primary_data),
                mitigation_strategies=self._develop_mitigation_strategies(primary_data)
            )
            
            recommendations[component_name] = alternative
        
        self.final_recommendations = recommendations
        return recommendations
    
    def _extract_advantages(self, material_data: Dict) -> List[str]:
        """Extract material advantages."""
        
        advantages = []
        material = material_data["material"]
        scores = material_data["criteria_scores"]
        
        if scores["strength_adequacy"] >= 0.9:
            advantages.append("Superior strength performance")
        
        if scores["weight_efficiency"] >= 0.8:
            advantages.append("Excellent strength-to-weight ratio")
        
        if scores["fatigue_resistance"] >= 0.8:
            advantages.append("Good fatigue resistance for repeated use")
        
        if scores["wear_resistance"] >= 0.8:
            advantages.append("Excellent wear resistance for moving parts")
        
        if scores["workability"] >= 0.8:
            advantages.append("Easy to work with Renaissance tools")
        
        if material.availability == "Local":
            advantages.append("Readily available in Florence")
        
        if scores["cost_effectiveness"] >= 0.7:
            advantages.append("Cost-effective for royal budget")
        
        if material.aesthetic_quality >= 4:
            advantages.append("Premium appearance suitable for royalty")
        
        return advantages
    
    def _extract_disadvantages(self, material_data: Dict) -> List[str]:
        """Extract material disadvantages."""
        
        disadvantages = []
        material = material_data["material"]
        scores = material_data["criteria_scores"]
        
        if scores["strength_adequacy"] < 0.7:
            disadvantages.append("Marginal strength - requires careful design")
        
        if scores["weight_efficiency"] < 0.5:
            disadvantages.append("Heavy material affecting mobility")
        
        if scores["fatigue_resistance"] < 0.5:
            disadvantages.append("Limited fatigue life - frequent inspection needed")
        
        if scores["wear_resistance"] < 0.5:
            disadvantages.append("Poor wear resistance - high maintenance")
        
        if scores["workability"] < 0.5:
            disadvantages.append("Difficult to work with - requires specialist skills")
        
        if material.availability in ["International", "Rare"]:
            disadvantages.append("Limited availability - supply chain risks")
        
        if scores["cost_effectiveness"] < 0.4:
            disadvantages.append("High cost - budget impact")
        
        if material.processing_difficulty >= 4:
            disadvantages.append("Challenging manufacturing process")
        
        return disadvantages
    
    def _identify_risk_factors(self, material_data: Dict) -> List[str]:
        """Identify risk factors for material selection."""
        
        risk_factors = []
        material = material_data["material"]
        
        # Supply chain risks
        if material.availability == "Rare":
            risk_factors.append("Material may not be available when needed")
        elif material.availability == "International":
            risk_factors.append("Extended delivery times from international suppliers")
        
        # Quality risks
        if "strength" in material.quality_variations:
            variation = material.quality_variations["strength"]
            if variation > 0.2:
                risk_factors.append("Significant strength variation between batches")
        
        # Manufacturing risks
        if material.processing_difficulty >= 4:
            risk_factors.append("High risk of manufacturing defects")
        
        # Environmental risks
        if material.weather_resistance <= 2:
            risk_factors.append("Vulnerable to environmental conditions")
        
        # Cost risks
        if material.cost_per_unit > 200:
            risk_factors.append("Budget overruns due to material cost")
        
        return risk_factors
    
    def _develop_mitigation_strategies(self, material_data: Dict) -> List[str]:
        """Develop risk mitigation strategies."""
        
        strategies = []
        material = material_data["material"]
        
        # Supply chain strategies
        if material.availability != "Local":
            strategies.append("Secure multiple suppliers")
            strategies.append("Order materials well in advance")
        
        # Quality control strategies
        if any(var > 0.15 for var in material.quality_variations.values()):
            strategies.append("Implement strict quality testing")
            strategies.append("Test multiple samples before bulk purchase")
        
        # Manufacturing strategies
        if material.processing_difficulty >= 4:
            strategies.append("Use master craftsmen for critical components")
            strategies.append("Create prototypes to refine manufacturing process")
        
        # Design strategies
        if material_data["criteria_scores"]["strength_adequacy"] < 0.8:
            strategies.append("Increase safety factors in design")
            strategies.append("Consider reinforcement strategies")
        
        # Maintenance strategies
        if material.durability_rating <= 3:
            strategies.append("Develop regular maintenance schedule")
            strategies.append("Create replacement parts inventory")
        
        return strategies
    
    def export_matrix_summary(self) -> Dict:
        """Export summary of all selections for final report."""
        
        summary = {
            "total_components": len(self.final_recommendations),
            "high_confidence_selections": 0,
            "medium_confidence_selections": 0,
            "low_confidence_selections": 0,
            "primary_materials": {},
            "material_usage_frequency": {},
            "total_estimated_cost": 0.0,
            "critical_path_materials": [],
            "risk_summary": {}
        }
        
        # Analyze confidence levels
        for component, alternative in self.final_recommendations.items():
            if alternative.confidence >= 0.8:
                summary["high_confidence_selections"] += 1
            elif alternative.confidence >= 0.6:
                summary["medium_confidence_selections"] += 1
            else:
                summary["low_confidence_selections"] += 1
            
            # Track material usage
            material_name = alternative.material_name
            summary["primary_materials"][component] = material_name
            summary["material_usage_frequency"][material_name] = \
                summary["material_usage_frequency"].get(material_name, 0) + 1
        
        # Identify critical path materials
        for material_name, frequency in summary["material_usage_frequency"].items():
            if frequency >= 3:  # Used in 3+ components
                material = self.db.get_material(material_name)
                if material.availability != "Local":
                    summary["critical_path_materials"].append(material_name)
        
        return summary
