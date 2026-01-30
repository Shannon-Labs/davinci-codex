"""
Leonardo's Mechanical Lion - Comprehensive Materials Analysis
Definitive material selection analysis for royal commission components
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

from renaissance_materials_database import RenaissanceMaterial, RenaissanceMaterialsDatabase


@dataclass
class ComponentRequirement:
    """Specific requirements for lion components."""
    name: str
    function: str
    loading_type: str  # "Compression", "Tension", "Shear", "Fatigue", "Wear"
    min_strength_pa: float
    max_weight_kg: float
    aesthetic_importance: int  # 1-5 scale
    visibility: str  # "External", "Internal", "Hidden"
    environmental_exposure: str  # "Protected", "Semi-exposed", "Exposed"
    motion_type: str  # "Static", "Rotating", "Sliding", "Flexible"


class LionMaterialsAnalyzer:
    """Comprehensive materials analysis for Mechanical Lion components."""

    def __init__(self):
        self.db = RenaissanceMaterialsDatabase()
        self.component_requirements = self._define_component_requirements()
        self.material_selections = {}

    def _define_component_requirements(self) -> Dict[str, ComponentRequirement]:
        """Define requirements for all lion components."""

        requirements = {}

        # === MAIN FRAME AND BODY ===

        requirements['main_frame'] = ComponentRequirement(
            name="Main Structural Frame",
            function="Primary load-bearing structure supporting entire lion",
            loading_type="Compression",
            min_strength_pa=35e6,
            max_weight_kg=80.0,
            aesthetic_importance=3,
            visibility="Internal",
            environmental_exposure="Protected",
            motion_type="Static"
        )

        requirements['body_shell'] = ComponentRequirement(
            name="Outer Body Shell",
            function="Lion-shaped exterior shell providing form and protection",
            loading_type="Compression",
            min_strength_pa=25e6,
            max_weight_kg=40.0,
            aesthetic_importance=5,
            visibility="External",
            environmental_exposure="Exposed",
            motion_type="Static"
        )

        # === LEG MECHANISM COMPONENTS ===

        requirements['leg_upper_beams'] = ComponentRequirement(
            name="Upper Leg Beams (Femur/Humerus)",
            function="Primary structural elements for leg support and movement",
            loading_type="Compression",
            min_strength_pa=45e6,
            max_weight_kg=8.0,
            aesthetic_importance=2,
            visibility="Internal",
            environmental_exposure="Protected",
            motion_type="Static"
        )

        requirements['leg_lower_beams'] = ComponentRequirement(
            name="Lower Leg Beams (Tibia/Radius)",
            function="Secondary leg elements transmitting forces to feet",
            loading_type="Compression",
            min_strength_pa=40e6,
            max_weight_kg=6.0,
            aesthetic_importance=2,
            visibility="Internal",
            environmental_exposure="Protected",
            motion_type="Static"
        )

        requirements['joint_bearings'] = ComponentRequirement(
            name="Joint Bearings and Bushings",
            function="Low-friction pivot points for leg articulation",
            loading_type="Wear",
            min_strength_pa=180e6,
            max_weight_kg=0.5,
            aesthetic_importance=1,
            visibility="Hidden",
            environmental_exposure="Protected",
            motion_type="Rotating"
        )

        requirements['cam_drums'] = ComponentRequirement(
            name="Cam Drums",
            function="Programmable motion control through precisely shaped profiles",
            loading_type="Wear",
            min_strength_pa=30e6,
            max_weight_kg=15.0,
            aesthetic_importance=2,
            visibility="Internal",
            environmental_exposure="Protected",
            motion_type="Rotating"
        )

        requirements['cam_followers'] = ComponentRequirement(
            name="Cam Followers",
            function="Track cam profiles and convert rotary to linear motion",
            loading_type="Wear",
            min_strength_pa=200e6,
            max_weight_kg=2.0,
            aesthetic_importance=1,
            visibility="Hidden",
            environmental_exposure="Protected",
            motion_type="Sliding"
        )

        # === POWER SYSTEM COMPONENTS ===

        requirements['power_springs'] = ComponentRequirement(
            name="Main Power Springs",
            function="Energy storage and release for walking motion",
            loading_type="Fatigue",
            min_strength_pa=350e6,
            max_weight_kg=8.0,
            aesthetic_importance=1,
            visibility="Hidden",
            environmental_exposure="Protected",
            motion_type="Flexible"
        )

        requirements['spring_housings'] = ComponentRequirement(
            name="Spring Housings",
            function="Protective containment for high-tension springs",
            loading_type="Compression",
            min_strength_pa=50e6,
            max_weight_kg=5.0,
            aesthetic_importance=1,
            visibility="Hidden",
            environmental_exposure="Protected",
            motion_type="Static"
        )

        requirements['winding_mechanism'] = ComponentRequirement(
            name="Winding Mechanism and Gears",
            function="Energy input system with mechanical advantage",
            loading_type="Wear",
            min_strength_pa=220e6,
            max_weight_kg=6.0,
            aesthetic_importance=2,
            visibility="Internal",
            environmental_exposure="Protected",
            motion_type="Rotating"
        )

        # === CHEST REVEAL MECHANISM ===

        requirements['chest_panels'] = ComponentRequirement(
            name="Chest Cavity Panels",
            function="Hinged panels opening to reveal fleurs-de-lis",
            loading_type="Compression",
            min_strength_pa=20e6,
            max_weight_kg=12.0,
            aesthetic_importance=5,
            visibility="External",
            environmental_exposure="Exposed",
            motion_type="Static"
        )

        requirements['panel_hinges'] = ComponentRequirement(
            name="Panel Hinges",
            function="Pivot points for chest panel movement",
            loading_type="Wear",
            min_strength_pa=150e6,
            max_weight_kg=3.0,
            aesthetic_importance=3,
            visibility="Semi-exposed",
            environmental_exposure="Semi-exposed",
            motion_type="Rotating"
        )

        requirements['lily_platform'] = ComponentRequirement(
            name="Fleur-de-lis Display Platform",
            function="Elevating platform for royal symbol presentation",
            loading_type="Compression",
            min_strength_pa=15e6,
            max_weight_kg=4.0,
            aesthetic_importance=5,
            visibility="External",
            environmental_exposure="Exposed",
            motion_type="Static"
        )

        # === FASTENERS AND CONNECTORS ===

        requirements['structural_bolts'] = ComponentRequirement(
            name="Structural Bolts and Fasteners",
            function="Primary structural connections and load transfer",
            loading_type="Shear",
            min_strength_pa=200e6,
            max_weight_kg=4.0,
            aesthetic_importance=1,
            visibility="Hidden",
            environmental_exposure="Protected",
            motion_type="Static"
        )

        requirements['decorative_fasteners'] = ComponentRequirement(
            name="Decorative Fasteners and Trim",
            function="Visible connections with aesthetic function",
            loading_type="Tension",
            min_strength_pa=100e6,
            max_weight_kg=2.0,
            aesthetic_importance=4,
            visibility="External",
            environmental_exposure="Exposed",
            motion_type="Static"
        )

        # === DECORATIVE AND SYMBOLIC ELEMENTS ===

        requirements['gold_leaf_elements'] = ComponentRequirement(
            name="Gold Leaf Decorative Elements",
            function="Royal embellishments and status symbols",
            loading_type="Tension",
            min_strength_pa=50e6,
            max_weight_kg=0.5,
            aesthetic_importance=5,
            visibility="External",
            environmental_exposure="Exposed",
            motion_type="Static"
        )

        requirements['fleurs_de_lis'] = ComponentRequirement(
            name="Fleurs-de-lis Symbols",
            function="Royal French symbols revealed in chest cavity",
            loading_type="Compression",
            min_strength_pa=80e6,
            max_weight_kg=1.5,
            aesthetic_importance=5,
            visibility="External",
            environmental_exposure="Exposed",
            motion_type="Static"
        )

        requirements['mane_elements'] = ComponentRequirement(
            name="Mane and Fur Elements",
            function="Realistic lion appearance and texture",
            loading_type="Tension",
            min_strength_pa=10e6,
            max_weight_kg=3.0,
            aesthetic_importance=4,
            visibility="External",
            environmental_exposure="Exposed",
            motion_type="Static"
        )

        # === FUNCTIONAL COMPONENTS ===

        requirements['cable_systems'] = ComponentRequirement(
            name="Control Cable Systems",
            function="Mechanical control and synchronization",
            loading_type="Tension",
            min_strength_pa=100e6,
            max_weight_kg=2.0,
            aesthetic_importance=1,
            visibility="Hidden",
            environmental_exposure="Protected",
            motion_type="Flexible"
        )

        requirements['seals_gaskets'] = ComponentRequirement(
            name="Seals and Gaskets",
            function="Weather protection and friction reduction",
            loading_type="Compression",
            min_strength_pa=5e6,
            max_weight_kg=0.5,
            aesthetic_importance=1,
            visibility="Hidden",
            environmental_exposure="Protected",
            motion_type="Static"
        )

        requirements['lubrication_system'] = ComponentRequirement(
            name="Lubrication System Components",
            function="Friction reduction and wear prevention",
            loading_type="Compression",
            min_strength_pa=2e6,
            max_weight_kg=1.0,
            aesthetic_importance=1,
            visibility="Hidden",
            environmental_exposure="Protected",
            motion_type="Static"
        )

        return requirements

    def calculate_material_suitability_score(self, material: RenaissanceMaterial,
                                          requirement: ComponentRequirement) -> float:
        """Calculate suitability score for material-component pairing."""

        max_score = 100.0

        # === STRENGTH REQUIREMENT (40 points) ===
        if material.tensile_strength_pa >= requirement.min_strength_pa:
            strength_score = 40.0
        else:
            strength_ratio = material.tensile_strength_pa / requirement.min_strength_pa
            strength_score = 40.0 * strength_ratio

        # === WEIGHT REQUIREMENT (20 points) ===
        # Calculate if material can meet weight constraint for typical component size
        typical_volume = requirement.max_weight_kg / material.density_kg_m3
        if typical_volume > 0:  # Valid volume calculation
            weight_score = min(20.0, 10.0 * (requirement.max_weight_kg /
                                           (typical_volume * material.density_kg_m3)))
        else:
            weight_score = 10.0

        # === ENVIRONMENTAL SUITABILITY (15 points) ===
        env_scores = {
            "Protected": {"Protected": 15, "Semi-exposed": 12, "Exposed": 8},
            "Semi-exposed": {"Protected": 12, "Semi-exposed": 15, "Exposed": 10},
            "Exposed": {"Protected": 8, "Semi-exposed": 10, "Exposed": 15}
        }

        env_score = env_scores.get(material.weather_resistance, {}).get(
            requirement.environmental_exposure, 5)

        # === FUNCTIONAL SUITABILITY (15 points) ===
        function_scores = {
            "Static": {"Hardwood": 15, "Softwood": 12, "Copper Alloy": 13, "Iron Alloy": 14},
            "Rotating": {"Hardwood": 8, "Softwood": 6, "Copper Alloy": 15, "Iron Alloy": 14},
            "Sliding": {"Hardwood": 10, "Softwood": 8, "Copper Alloy": 12, "Iron Alloy": 15},
            "Flexible": {"Hardwood": 12, "Softwood": 14, "Copper Alloy": 5, "Iron Alloy": 8}
        }

        function_score = function_scores.get(requirement.motion_type, {}).get(
            material.material_type, 7)

        # === AESTHETIC SUITABILITY (10 points) ===
        aesthetic_multiplier = requirement.aesthetic_importance / 5.0
        aesthetic_score = material.aesthetic_quality * 2.0 * aesthetic_multiplier

        # === AVAILABILITY AND COST (BONUS/DEMERIT) ===
        availability_bonus = {
            "Local": 5,
            "Regional": 3,
            "International": 1,
            "Rare": -2
        }

        cost_factor = max(0.5, 100.0 / (material.cost_per_unit + 50.0))

        bonus_score = availability_bonus.get(material.availability, 0) + cost_factor

        # Total score
        total_score = (strength_score + weight_score + env_score +
                      function_score + aesthetic_score + bonus_score)

        return min(max_score, total_score)

    def analyze_component_materials(self, component_name: str) -> List[Tuple[str, float]]:
        """Analyze suitable materials for a specific component."""

        requirement = self.component_requirements.get(component_name)
        if requirement is None:
            raise ValueError(f"Unknown component: {component_name}")

        material_scores = []

        for material_name, material in self.db.materials.items():
            score = self.calculate_material_suitability_score(material, requirement)
            material_scores.append((material_name, score))

        # Sort by score (descending)
        material_scores.sort(key=lambda x: x[1], reverse=True)

        return material_scores

    def generate_component_recommendations(self) -> Dict[str, Dict]:
        """Generate material recommendations for all components."""

        recommendations = {}

        for component_name, requirement in self.component_requirements.items():
            material_scores = self.analyze_component_materials(component_name)

            # Get top 3 recommendations
            top_materials = material_scores[:3]

            # Primary recommendation
            primary_material_name = top_materials[0][0]
            primary_material = self.db.get_material(primary_material_name)

            # Analysis and justification
            analysis = {
                "component": component_name,
                "requirement": requirement,
                "recommended_materials": [
                    {
                        "material_name": name,
                        "score": score,
                        "material": self.db.get_material(name),
                        "justification": self._generate_justification(
                            self.db.get_material(name), requirement, score)
                    }
                    for name, score in top_materials
                ],
                "primary_selection": {
                    "material": primary_material,
                    "confidence": top_materials[0][1] / 100.0,
                    "alternatives": top_materials[1:3]
                }
            }

            recommendations[component_name] = analysis

        return recommendations

    def _generate_justification(self, material: RenaissanceMaterial,
                              requirement: ComponentRequirement, score: float) -> str:
        """Generate justification for material selection."""

        justifications = []

        # Strength justification
        if material.tensile_strength_pa >= requirement.min_strength_pa:
            justifications.append(
                f"Exceeds strength requirement by {material.tensile_strength_pa/requirement.min_strength_pa:.1f}x")

        # Weight justification
        weight_efficiency = material.tensile_strength_pa / material.density_kg_m3
        justifications.append(f"Excellent strength-to-weight ratio ({weight_efficiency/1e6:.1f} MN⋅m/kg)")

        # Environmental justification
        env_mapping = {"Protected": "protected", "Semi-exposed": "semi-exposed", "Exposed": "exposed"}
        justifications.append(f"Suitable for {env_mapping.get(requirement.environmental_exposure, 'general')} environments")

        # Functional justification
        if requirement.motion_type == "Rotating" and material.material_type in ["Copper Alloy"]:
            justifications.append("Excellent bearing properties for rotating applications")
        elif requirement.motion_type == "Wear" and material.durability_rating >= 4:
            justifications.append("Superior wear resistance for moving parts")
        elif requirement.loading_type == "Fatigue" and material.material_type == "Iron Alloy":
            justifications.append("Good fatigue resistance for spring applications")

        # Aesthetic justification
        if requirement.aesthetic_importance >= 4 and material.aesthetic_quality >= 4:
            justifications.append("Premium appearance suitable for royal presentation")

        # Availability justification
        if material.availability == "Local":
            justifications.append("Readily available from Florentine suppliers")
        elif material.availability == "Regional":
            justifications.append("Available through regional trade networks")

        # Cost justification
        if material.cost_per_unit < 20:
            justifications.append("Cost-effective for royal commission")
        elif material.cost_per_unit > 100:
            justifications.append("Premium material appropriate for royal commission")

        return "; ".join(justifications)

    def calculate_total_material_costs(self, recommendations: Dict) -> Dict[str, float]:
        """Calculate estimated total material costs."""

        total_costs = {}

        for component_name, analysis in recommendations.items():
            primary_material = analysis["primary_selection"]["material"]

            # Estimate component volume based on typical dimensions
            estimated_volume = self._estimate_component_volume(component_name)

            if estimated_volume > 0:
                cost = self.db.calculate_material_cost(
                    primary_material.name, estimated_volume)
                total_costs[component_name] = cost

        return total_costs

    def _estimate_component_volume(self, component_name: str) -> float:
        """Estimate component volume in cubic meters."""

        volume_estimates = {
            'main_frame': 0.12,  # ~120 liters of wood
            'body_shell': 0.08,
            'leg_upper_beams': 0.015,  # Per leg
            'leg_lower_beams': 0.012,  # Per leg
            'joint_bearings': 0.0005,  # Per bearing
            'cam_drums': 0.025,
            'cam_followers': 0.002,  # Per follower
            'power_springs': 0.008,  # Per spring
            'spring_housings': 0.006,
            'winding_mechanism': 0.010,
            'chest_panels': 0.018,  # Per panel
            'panel_hinges': 0.001,  # Per hinge
            'lily_platform': 0.008,
            'structural_bolts': 0.0002,  # Per bolt
            'decorative_fasteners': 0.0001,  # Per fastener
            'gold_leaf_elements': 0.0001,  # Very thin
            'fleurs_de_lis': 0.002,  # Per lily
            'mane_elements': 0.004,
            'cable_systems': 0.001,
            'seals_gaskets': 0.0005,
            'lubrication_system': 0.0008
        }

        # Multiply by quantity if multiple components
        multipliers = {
            'leg_upper_beams': 4,  # 4 legs
            'leg_lower_beams': 4,
            'joint_bearings': 12,  # 3 joints per leg
            'cam_followers': 12,
            'power_springs': 3,  # Multiple springs
            'chest_panels': 4,
            'panel_hinges': 8,
            'fleurs_de_lis': 3,
            'structural_bolts': 50,  # Many bolts
            'decorative_fasteners': 20
        }

        base_volume = volume_estimates.get(component_name, 0.001)
        multiplier = multipliers.get(component_name, 1)

        return base_volume * multiplier

    def generate_supply_chain_analysis(self) -> Dict[str, List[str]]:
        """Analyze supply chain for selected materials."""

        recommendations = self.generate_component_recommendations()
        supply_requirements = {}

        for component_name, analysis in recommendations.items():
            primary_material = analysis["primary_selection"]["material"]
            material_name = primary_material.name

            if material_name not in supply_requirements:
                supply_requirements[material_name] = []

            supply_requirements[material_name].append(component_name)

        # Generate supplier analysis
        supplier_analysis = {}

        for material_name, components in supply_requirements.items():
            material = self.db.get_material(material_name)

            supplier_analysis[material_name] = {
                "components": components,
                "suppliers": material.florentine_suppliers,
                "availability": material.availability,
                "lead_time": self._estimate_lead_time(material.availability),
                "quality_considerations": self._get_quality_considerations(material_name)
            }

        return supplier_analysis

    def _estimate_lead_time(self, availability: str) -> str:
        """Estimate lead time for material acquisition."""

        lead_times = {
            "Local": "1-2 weeks",
            "Regional": "3-6 weeks",
            "International": "2-4 months",
            "Rare": "4-8 months (if available)"
        }

        return lead_times.get(availability, "Unknown")

    def _get_quality_considerations(self, material_name: str) -> List[str]:
        """Get quality considerations for material."""

        considerations = {
            "oak_tuscan": [
                "Select mature trees with straight grain",
                "Proper seasoning essential (2-3 years)",
                "Check for knots and defects",
                "Grain orientation critical for strength"
            ],
            "bronze_florentine": [
                "Verify tin content (10-12%)",
                "Test casting quality for soundness",
                "Check for porosity and inclusions",
                "Ensure proper alloy mixing"
            ],
            "steel_florentine": [
                "Test carbon content (0.6-1.0%)",
                "Verify heat treatment quality",
                "Check for crack formation",
                "Test spring temper consistency"
            ],
            "gold_leaf": [
                "Verify purity (23 karat minimum)",
                "Check thickness uniformity",
                "Test adhesion to substrate",
                "Handle with extreme care"
            ]
        }

        return considerations.get(material_name, ["Standard quality inspection required"])
