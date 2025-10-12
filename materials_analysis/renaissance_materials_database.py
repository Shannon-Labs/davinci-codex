"""
Renaissance Materials Database for Leonardo's Mechanical Lion
Comprehensive material properties and availability analysis for 16th-century Florence
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class RenaissanceMaterial:
    """Material with Renaissance-era properties and availability."""
    name: str
    material_type: str
    density_kg_m3: float
    tensile_strength_pa: float
    compressive_strength_pa: float
    young_modulus_pa: float
    cost_per_unit: float
    availability: str  # "Local", "Regional", "International", "Rare"
    processing_difficulty: int  # 1-5 scale
    durability_rating: int  # 1-5 scale
    aesthetic_quality: int  # 1-5 scale
    weather_resistance: int  # 1-5 scale
    workability: int  # 1-5 scale
    historical_notes: str
    florentine_suppliers: List[str]
    quality_variations: Dict[str, float]


class RenaissanceMaterialsDatabase:
    """Comprehensive database of materials available in Renaissance Florence."""

    def __init__(self):
        self.materials = {}
        self._initialize_materials()

    def _initialize_materials(self):
        """Initialize all materials available in Renaissance Florence."""

        # === STRUCTURAL WOODS ===

        self.materials['oak_tuscan'] = RenaissanceMaterial(
            name="Tuscan Oak",
            material_type="Hardwood",
            density_kg_m3=750,
            tensile_strength_pa=40e6,
            compressive_strength_pa=50e6,
            young_modulus_pa=12e9,
            cost_per_unit=12.0,  # florins per cubic meter
            availability="Local",
            processing_difficulty=3,
            durability_rating=5,
            aesthetic_quality=4,
            weather_resistance=4,
            workability=3,
            historical_notes="Prime structural timber from Casentine forests. Used by Brunelleschi for cathedral dome. Superior strength-to-weight ratio.",
            florentine_suppliers=["Arte dei Maestri di Pietra e Legname", "Casa di Legname Medicea"],
            quality_variations={"strength": 0.15, "density": 0.1, "workability": 0.2}
        )

        self.materials['oak_slavonian'] = RenaissanceMaterial(
            name="Slavonian Oak",
            material_type="Hardwood",
            density_kg_m3=780,
            tensile_strength_pa=45e6,
            compressive_strength_pa=55e6,
            young_modulus_pa=13e9,
            cost_per_unit=18.0,
            availability="Regional",
            processing_difficulty=3,
            durability_rating=5,
            aesthetic_quality=5,
            weather_resistance=5,
            workability=2,
            historical_notes="Premium oak from Dalmatian coast. Superior grain and strength. Used for shipbuilding and fine furniture.",
            florentine_suppliers=["Mercanti di Ragusa", "Compagnia dell'Adriatico"],
            quality_variations={"strength": 0.1, "density": 0.08, "workability": 0.15}
        )

        self.materials['pine_italian'] = RenaissanceMaterial(
            name="Italian Pine",
            material_type="Softwood",
            density_kg_m3=450,
            tensile_strength_pa=25e6,
            compressive_strength_pa=30e6,
            young_modulus_pa=8e9,
            cost_per_unit=8.0,
            availability="Local",
            processing_difficulty=2,
            durability_rating=3,
            aesthetic_quality=3,
            weather_resistance=3,
            workability=4,
            historical_notes="Abundant softwood from Apennine forests. Light and workable. Used for secondary structures.",
            florentine_suppliers=["Taglialegna Fiorentini", "Casa del Bosco"],
            quality_variations={"strength": 0.2, "density": 0.15, "workability": 0.1}
        )

        self.materials['ash_italian'] = RenaissanceMaterial(
            name="Italian Ash",
            material_type="Hardwood",
            density_kg_m3=680,
            tensile_strength_pa=50e6,
            compressive_strength_pa=45e6,
            young_modulus_pa=11e9,
            cost_per_unit=14.0,
            availability="Regional",
            processing_difficulty=3,
            durability_rating=4,
            aesthetic_quality=4,
            weather_resistance=3,
            workability=3,
            historical_notes="Excellent flexural strength. Used for tool handles and flexible components. Elastic properties ideal for springs.",
            florentine_suppliers=["Legnami di Bologna", "Mercanti dell'Emilia"],
            quality_variations={"strength": 0.12, "density": 0.1, "elasticity": 0.15}
        )

        # === METALS ===

        self.materials['bronze_florentine'] = RenaissanceMaterial(
            name="Florentine Bronze",
            material_type="Copper Alloy",
            density_kg_m3=8800,
            tensile_strength_pa=200e6,
            compressive_strength_pa=250e6,
            young_modulus_pa=100e9,
            cost_per_unit=45.0,
            availability="Local",
            processing_difficulty=4,
            durability_rating=5,
            aesthetic_quality=5,
            weather_resistance=5,
            workability=3,
            historical_notes="88% copper, 12% tin alloy. Florentine bronze casters renowned across Europe. Used by Ghiberti and Donatello.",
            florentine_suppliers=["Fonderia del Duomo", "Bottega dei Bronzei Medicei", "Arte dei Fabbri"],
            quality_variations={"strength": 0.08, "hardness": 0.1, "castability": 0.05}
        )

        self.materials['bronze_bell'] = RenaissanceMaterial(
            name="Bell Bronze",
            material_type="Copper Alloy",
            density_kg_m3=8700,
            tensile_strength_pa=220e6,
            compressive_strength_pa=280e6,
            young_modulus_pa=110e9,
            cost_per_unit=52.0,
            availability="Regional",
            processing_difficulty=4,
            durability_rating=5,
            aesthetic_quality=4,
            weather_resistance=5,
            workability=2,
            historical_notes="78% copper, 22% tin. Superior resonance and strength. Used for church bells and musical instruments.",
            floorentine_suppliers=["Fonderia di Campane", "Mercanti di Venezia"],
            quality_variations={"resonance": 0.1, "strength": 0.05, "hardness": 0.08}
        )

        self.materials['steel_florentine'] = RenaissanceMaterial(
            name="Florentine Steel",
            material_type="Iron Alloy",
            density_kg_m3=7850,
            tensile_strength_pa=400e6,
            compressive_strength_pa=450e6,
            young_modulus_pa=200e9,
            cost_per_unit=65.0,
            availability="Regional",
            processing_difficulty=5,
            durability_rating=4,
            aesthetic_quality=3,
            weather_resistance=3,
            workability=4,
            historical_notes="Hand-forged steel with 0.8% carbon. Used for cutting tools and springs. Variable quality due to manual processing.",
            floorentine_suppliers=["Fabbri di Brescia", "Arte dei Spadai", "Magister Ferariorum"],
            quality_variations={"strength": 0.25, "hardness": 0.3, "flexibility": 0.2}
        )

        self.materials['iron_wrought'] = RenaissanceMaterial(
            name="Wrought Iron",
            material_type="Iron",
            density_kg_m3=7750,
            tensile_strength_pa=250e6,
            compressive_strength_pa=300e6,
            young_modulus_pa=180e9,
            cost_per_unit=28.0,
            availability="Local",
            processing_difficulty=3,
            durability_rating=4,
            aesthetic_quality=2,
            weather_resistance=3,
            workability=4,
            historical_notes="Ductile iron with low carbon content. Excellent for forgings and fasteners. Used throughout construction.",
            floorentine_suppliers=["Fucine Fiorentine", "Magistri Ferariorum"],
            quality_variations={"strength": 0.15, "ductility": 0.2, "workability": 0.1}
        )

        # === PRECIOUS MATERIALS ===

        self.materials['gold_leaf'] = RenaissanceMaterial(
            name="Gold Leaf",
            material_type="Precious Metal",
            density_kg_m3=19300,
            tensile_strength_pa=120e6,
            compressive_strength_pa=150e6,
            young_modulus_pa=78e9,
            cost_per_unit=2500.0,
            availability="International",
            processing_difficulty=5,
            durability_rating=5,
            aesthetic_quality=5,
            weather_resistance=5,
            workability=5,
            historical_notes="23-karat gold beaten to 0.1μm thickness. Essential for royal commissions. Symbol of wealth and divine favor.",
            floorentine_suppliers=["Orefici del Battistero", "Banchieri Medicei", "Mercanti d'Oro"],
            quality_variations={"purity": 0.02, "thickness": 0.1, "uniformity": 0.05}
        )

        self.materials['silver'] = RenaissanceMaterial(
            name="Silver",
            material_type="Precious Metal",
            density_kg_m3=10500,
            tensile_strength_pa=170e6,
            compressive_strength_pa=200e6,
            young_modulus_pa=83e9,
            cost_per_unit=850.0,
            availability="International",
            processing_difficulty=4,
            durability_rating=4,
            aesthetic_quality=5,
            weather_resistance=4,
            workability=4,
            historical_notes="92.5% sterling silver. Tarnishes but polishes well. Used for decorative elements and ceremonial objects.",
            floorentine_suppliers=["Argentieri Fiorentini", "Mercanti di Genova"],
            quality_variations={"purity": 0.03, "tarnish_resistance": 0.15, "workability": 0.08}
        )

        # === ORGANIC MATERIALS ===

        self.materials['leather_calf'] = RenaissanceMaterial(
            name="Calf Leather",
            material_type="Organic",
            density_kg_m3=950,
            tensile_strength_pa=25e6,
            compressive_strength_pa=15e6,
            young_modulus_pa=50e6,
            cost_per_unit=15.0,
            availability="Local",
            processing_difficulty=2,
            durability_rating=3,
            aesthetic_quality=4,
            weather_resistance=2,
            workability=4,
            historical_notes="Fine-grained leather from local cattle. Used for gaskets, seals, and flexible connections.",
            floorentine_suppliers=["Conceria Fiorentina", "Cuoiài del Mercato"],
            quality_variations={"strength": 0.2, "flexibility": 0.15, "thickness": 0.1}
        )

        self.materials['silk_florentine'] = RenaissanceMaterial(
            name="Florentine Silk",
            material_type="Textile",
            density_kg_m3=1300,
            tensile_strength_pa=400e6,
            compressive_strength_pa=20e6,
            young_modulus_pa=10e9,
            cost_per_unit=120.0,
            availability="Local",
            processing_difficulty=1,
            durability_rating=3,
            aesthetic_quality=5,
            weather_resistance=2,
            workability=5,
            historical_notes="Luxury textile from Florentine workshops. Strong and beautiful. Used for internal linings and decorative elements.",
            floorentine_suppliers=["Arte della Seta", "Setaiuoli Fiorentini", "Tessitori di Oltrarno"],
            quality_variations={"strength": 0.1, "sheen": 0.15, "uniformity": 0.08}
        )

        self.materials['hemp_rope'] = RenaissanceMaterial(
            name="Hemp Rope",
            material_type="Natural Fiber",
            density_kg_m3=1450,
            tensile_strength_pa=150e6,
            compressive_strength_pa=10e6,
            young_modulus_pa=5e9,
            cost_per_unit=8.0,
            availability="Local",
            processing_difficulty=1,
            durability_rating=2,
            aesthetic_quality=2,
            weather_resistance=2,
            workability=5,
            historical_notes="Strong natural fiber rope. Used for pulleys and cable systems. Susceptible to rot in humid conditions.",
            floorentine_suppliers=["Canapai del Mugello", "Funai Fiorentini"],
            quality_variations={"strength": 0.25, "flexibility": 0.2, "durability": 0.3}
        )

        # === BINDING AND FINISHING MATERIALS ===

        self.materials['animal_glue'] = RenaissanceMaterial(
            name="Animal Glue",
            material_type="Organic Adhesive",
            density_kg_m3=1200,
            tensile_strength_pa=5e6,
            compressive_strength_pa=8e6,
            young_modulus_pa=2e9,
            cost_per_unit=6.0,
            availability="Local",
            processing_difficulty=2,
            durability_rating=2,
            aesthetic_quality=1,
            weather_resistance=1,
            workability=3,
            historical_notes="Made from animal hides and bones. Traditional woodworking adhesive. Weak when exposed to moisture.",
            floorentine_suppliers=["Collai di Santa Croce", "Speziali Fiorentini"],
            quality_variations={"strength": 0.3, "setting_time": 0.2, "water_resistance": 0.4}
        )

        self.materials['linseed_oil'] = RenaissanceMaterial(
            name="Linseed Oil",
            material_type="Organic Oil",
            density_kg_m3=930,
            tensile_strength_pa=1e6,
            compressive_strength_pa=2e6,
            young_modulus_pa=0.5e9,
            cost_per_unit=4.0,
            availability="Regional",
            processing_difficulty=1,
            durability_rating=3,
            aesthetic_quality=3,
            weather_resistance=4,
            workability=5,
            historical_notes="Wood finishing and preservation. Polymerizes to form protective coating. Enhances wood grain.",
            floorentine_suppliers=["Speziali di Via Tornabuoni", "Mercanti di Olio"],
            quality_variations={"clarity": 0.1, "drying_time": 0.2, "protection": 0.15}
        )

        self.materials['beeswax'] = RenaissanceMaterial(
            name="Beeswax",
            material_type="Natural Wax",
            density_kg_m3=960,
            tensile_strength_pa=2e6,
            compressive_strength_pa=3e6,
            young_modulus_pa=0.2e9,
            cost_per_unit=9.0,
            availability="Local",
            processing_difficulty=1,
            durability_rating=3,
            aesthetic_quality=4,
            workability=5,
            historical_notes="Natural lubricant and sealant. Used for moving parts and wood finishing. Pleasant honey scent.",
            floorentine_suppliers=["Apicoltori di Chianti", "Speziali Fiorentini"],
            quality_variations={"purity": 0.08, "hardness": 0.15, "fragrance": 0.1}
        )

        # === PIGMENTS AND DYES ===

        self.materials['vermilion'] = RenaissanceMaterial(
            name="Vermilion",
            material_type="Mineral Pigment",
            density_kg_m3=8100,
            tensile_strength_pa=10e6,
            compressive_strength_pa=20e6,
            young_modulus_pa=15e9,
            cost_per_unit=180.0,
            availability="International",
            processing_difficulty=3,
            durability_rating=4,
            aesthetic_quality=5,
            weather_resistance=4,
            workability=2,
            historical_notes="Mercury sulfide pigment. Brilliant red color prized for royal use. Toxic but essential for ceremonial objects.",
            floorentine_suppliers=["Speziali di Santa Maria Novella", "Mercanti di Pigmenti"],
            quality_variations={"color_intensity": 0.1, "stability": 0.15, "toxicity": 0.05}
        )

        self.materials['ultramarine'] = RenaissanceMaterial(
            name="Ultramarine",
            material_type="Mineral Pigment",
            density_kg_m3=2300,
            tensile_strength_pa=8e6,
            compressive_strength_pa=15e6,
            young_modulus_pa=10e9,
            cost_per_unit=450.0,
            availability="International",
            processing_difficulty=3,
            durability_rating=5,
            aesthetic_quality=5,
            weather_resistance=5,
            workability=2,
            historical_notes="Lapis lazuli pigment from Afghanistan. More valuable than gold. Reserved for Virgin Mary and royal commissions.",
            floorentine_suppliers=["Speziali Medicei", "Mercanti di Levante"],
            quality_variations={"color_purity": 0.08, "stability": 0.05, "rarity": 0.02}
        )

        # === NEW WORLD MATERIALS (Limited Availability) ===

        self.materials['rubber_natural'] = RenaissanceMaterial(
            name="Natural Rubber",
            material_type="Natural Polymer",
            density_kg_m3=920,
            tensile_strength_pa=20e6,
            compressive_strength_pa=15e6,
            young_modulus_pa=0.01e9,
            cost_per_unit=95.0,
            availability="Rare",
            processing_difficulty=4,
            durability_rating=2,
            aesthetic_quality=2,
            weather_resistance=2,
            workability=3,
            historical_notes="Recent import from New World via Spanish traders. Unique elastic properties. Unstable and degrades quickly.",
            floorentine_suppliers=["Mercanti Spagnuoli", "Agenti Portoghesi"],
            quality_variations={"elasticity": 0.4, "stability": 0.5, "purity": 0.3}
        )

    def get_material(self, name: str) -> Optional[RenaissanceMaterial]:
        """Get material by name."""
        return self.materials.get(name)

    def filter_materials(self, **criteria) -> List[RenaissanceMaterial]:
        """Filter materials by criteria."""
        filtered = []

        for material in self.materials.values():
            matches = True

            for key, value in criteria.items():
                if hasattr(material, key):
                    if getattr(material, key) != value:
                        matches = False
                        break
                else:
                    matches = False
                    break

            if matches:
                filtered.append(material)

        return filtered

    def get_materials_by_type(self, material_type: str) -> List[RenaissanceMaterial]:
        """Get all materials of a specific type."""
        return [m for m in self.materials.values() if m.material_type == material_type]

    def get_materials_by_availability(self, availability: str) -> List[RenaissanceMaterial]:
        """Get materials by availability level."""
        return [m for m in self.materials.values() if m.availability == availability]

    def calculate_material_cost(self, material_name: str, volume_m3: float) -> float:
        """Calculate total material cost."""
        material = self.get_material(material_name)
        if material is None:
            raise ValueError(f"Unknown material: {material_name}")

        return material.cost_per_unit * volume_m3

    def get_structural_materials_ranking(self) -> List[Tuple[str, float]]:
        """Rank structural materials by strength-to-weight ratio."""
        rankings = []

        for name, material in self.materials.items():
            if material.material_type in ["Hardwood", "Softwood", "Copper Alloy", "Iron Alloy"]:
                strength_to_weight = material.tensile_strength_pa / material.density_kg_m3
                rankings.append((name, strength_to_weight))

        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings

    def summarize_materials(self) -> Dict[str, int]:
        """Get summary of available materials by type."""
        summary = {}

        for material in self.materials.values():
            material_type = material.material_type
            summary[material_type] = summary.get(material_type, 0) + 1

        return summary
