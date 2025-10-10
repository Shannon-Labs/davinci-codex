"""
Cost and Availability Analysis for Leonardo's Mechanical Lion
Comprehensive economic analysis for Renaissance royal commission
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from renaissance_materials_database import RenaissanceMaterialsDatabase
from lion_materials_analysis import LionMaterialsAnalyzer


@dataclass
class Supplier:
    """Renaissance supplier information."""
    name: str
    location: str
    specialty: str
    reliability_rating: float  # 0.0-1.0
    price_multiplier: float  # Relative to base price
    lead_time_days: int
    payment_terms: str
    quality_consistency: float  # 0.0-1.0


@dataclass
class TradeRoute:
    """Historical trade route information."""
    name: str
    origin: str
    destination: str
    distance_km: float
    travel_time_days: int
    cost_factor: float  # Multiplier for transportation cost
    reliability: float  # 0.0-1.0
    seasonal_availability: Dict[str, float]  # Season availability factors


@dataclass
class MaterialCost:
    """Detailed cost breakdown for material."""
    material_name: str
    base_cost: float  # Florins per unit
    quantity: float
    supplier_cost: float
    transportation_cost: float
    taxes_duties: float
    processing_cost: float
    total_cost: float
    cost_breakdown: Dict[str, float]


class RenaissanceCostAnalyzer:
    """Comprehensive cost and availability analysis for Renaissance materials."""
    
    def __init__(self):
        self.db = RenaissanceMaterialsDatabase()
        self.analyzer = LionMaterialsAnalyzer()
        self.suppliers = self._initialize_suppliers()
        self.trade_routes = self._initialize_trade_routes()
        self.renaissance_economics = self._initialize_economic_context()
    
    def _initialize_suppliers(self) -> Dict[str, List[Supplier]]:
        """Initialize Renaissance suppliers database."""
        
        suppliers = {}
        
        # === FLORENTINE SUPPLIERS ===
        
        suppliers["oak_tuscan"] = [
            Supplier(
                name="Arte dei Maestri di Pietra e Legname",
                location="Florence, Oltrarno District",
                specialty="Structural timber and fine woodworking",
                reliability_rating=0.9,
                price_multiplier=1.0,
                lead_time_days=14,
                payment_terms="30 days net",
                quality_consistency=0.85
            ),
            Supplier(
                name="Casa di Legname Medicea",
                location="Florence, Near Santa Croce",
                specialty="Premium structural timber",
                reliability_rating=0.95,
                price_multiplier=1.15,
                lead_time_days=21,
                payment_terms="60 days net",
                quality_consistency=0.92
            )
        ]
        
        suppliers["bronze_florentine"] = [
            Supplier(
                name="Fonderia del Duomo",
                location="Florence, Cathedral Workshop",
                specialty="Architectural bronze and statuary",
                reliability_rating=0.95,
                price_multiplier=1.0,
                lead_time_days=30,
                payment_terms="45 days net",
                quality_consistency=0.90
            ),
            Supplier(
                name="Bottega dei Bronzei Medicei",
                location="Florence, Medici Palace",
                specialty="Fine art bronze and decorative work",
                reliability_rating=0.98,
                price_multiplier=1.25,
                lead_time_days=45,
                payment_terms="60 days net",
                quality_consistency=0.95
            )
        ]
        
        suppliers["steel_florentine"] = [
            Supplier(
                name="Fabbri di Brescia",
                location="Brescia (with Florence office)",
                specialty="Hand-forged steel and tools",
                reliability_rating=0.80,
                price_multiplier=1.0,
                lead_time_days=35,
                payment_terms="30 days net",
                quality_consistency=0.75
            ),
            Supplier(
                name="Arte dei Spadai",
                location="Florence, Armorer's Guild",
                specialty="Weapon-grade steel and springs",
                reliability_rating=0.85,
                price_multiplier=1.20,
                lead_time_days=42,
                payment_terms="45 days net",
                quality_consistency=0.82
            )
        ]
        
        suppliers["gold_leaf"] = [
            Supplier(
                name="Orefici del Battistero",
                location="Florence, Baptistery Square",
                specialty="Ecclesiastical gold work",
                reliability_rating=0.92,
                price_multiplier=1.0,
                lead_time_days=60,
                payment_terms="90 days net",
                quality_consistency=0.88
            ),
            Supplier(
                name="Banchieri Medicei",
                location="Florence, Medici Bank",
                specialty="Precious metals trading",
                reliability_rating=0.98,
                price_multiplier=0.95,
                lead_time_days=45,
                payment_terms="Cash advance",
                quality_consistency=0.95
            )
        ]
        
        suppliers["silk_florentine"] = [
            Supplier(
                name="Arte della Seta",
                location="Florence, Silk Guild Hall",
                specialty="Luxury textiles and silk products",
                reliability_rating=0.90,
                price_multiplier=1.0,
                lead_time_days=21,
                payment_terms="30 days net",
                quality_consistency=0.87
            )
        ]
        
        # === REGIONAL SUPPLIERS ===
        
        suppliers["oak_slavonian"] = [
            Supplier(
                name="Mercanti di Ragusa",
                location="Ragusa (Dubrovnik), Dalmatian Coast",
                specialty="Premium Dalmatian oak",
                reliability_rating=0.75,
                price_multiplier=0.85,
                lead_time_days=90,
                payment_terms="Letter of credit",
                quality_consistency=0.80
            ),
            Supplier(
                name="Compagnia dell'Adriatico",
                location="Venice, Rialto",
                specialty="Adriatic timber imports",
                reliability_rating=0.82,
                price_multiplier=1.10,
                lead_time_days=75,
                payment_terms="45 days net",
                quality_consistency=0.85
            )
        ]
        
        suppliers["bronze_bell"] = [
            Supplier(
                name="Fonderia di Campane",
                location="Venice, Arsenal District",
                specialty="Church bells and resonant bronze",
                reliability_rating=0.88,
                price_multiplier=1.05,
                lead_time_days=60,
                payment_terms="60 days net",
                quality_consistency=0.90
            )
        ]
        
        # === INTERNATIONAL SUPPLIERS ===
        
        suppliers["ultramarine"] = [
            Supplier(
                name="Speziali Medicei",
                location="Florence, Medici Trading House",
                specialty="Rare pigments and spices",
                reliability_rating=0.70,
                price_multiplier=1.50,
                lead_time_days=180,
                payment_terms="Cash in advance",
                quality_consistency=0.60
            ),
            Supplier(
                name="Mercanti di Levante",
                location="Venice, Levantine Quarter",
                specialty="Eastern pigments and materials",
                reliability_rating=0.65,
                price_multiplier=1.75,
                lead_time_days=150,
                payment_terms="Letter of credit",
                quality_consistency=0.55
            )
        ]
        
        suppliers["rubber_natural"] = [
            Supplier(
                name="Mercanti Spagnuoli",
                location="Seville, Spanish Main",
                specialty="New World exotic materials",
                reliability_rating=0.40,
                price_multiplier=2.50,
                lead_time_days=270,
                payment_terms="Cash in advance",
                quality_consistency=0.30
            )
        ]
        
        return suppliers
    
    def _initialize_trade_routes(self) -> Dict[str, List[TradeRoute]]:
        """Initialize historical trade routes."""
        
        routes = {}
        
        # === MEDITERRANEAN ROUTES ===
        
        routes["adriatic"] = [
            TradeRoute(
                name="Venice to Ragusa",
                origin="Venice, Italy",
                destination="Ragusa, Dalmatia",
                distance_km=580,
                travel_time_days=14,
                cost_factor=1.2,
                reliability=0.85,
                seasonal_availability={
                    "Spring": 1.0, "Summer": 1.0, "Autumn": 0.8, "Winter": 0.4
                }
            )
        ]
        
        routes["levantine"] = [
            TradeRoute(
                name="Venice to Alexandria",
                origin="Venice, Italy",
                destination="Alexandria, Egypt",
                distance_km=2100,
                travel_time_days=45,
                cost_factor=1.8,
                reliability=0.70,
                seasonal_availability={
                    "Spring": 1.0, "Summer": 0.9, "Autumn": 0.7, "Winter": 0.3
                }
            ),
            TradeRoute(
                name="Genoa to Constantinople",
                origin="Genoa, Italy",
                destination="Constantinople, Byzantium",
                distance_km=1800,
                travel_time_days=40,
                cost_factor=1.6,
                reliability=0.75,
                seasonal_availability={
                    "Spring": 1.0, "Summer": 0.8, "Autumn": 0.6, "Winter": 0.2
                }
            )
        ]
        
        # === OVERLAND ROUTES ===
        
        routes["trans_alpine"] = [
            TradeRoute(
                name="Florence to Brescia",
                origin="Florence, Italy",
                destination="Brescia, Italy",
                distance_km=280,
                travel_time_days=8,
                cost_factor=1.1,
                reliability=0.90,
                seasonal_availability={
                    "Spring": 1.0, "Summer": 1.0, "Autumn": 0.9, "Winter": 0.5
                }
            )
        ]
        
        # === ATLANTIC ROUTES ===
        
        routes["atlantic"] = [
            TradeRoute(
                name="Seville to Florence",
                origin="Seville, Spain",
                destination="Florence, Italy",
                distance_km=1600,
                travel_time_days=35,
                cost_factor=2.0,
                reliability=0.50,
                seasonal_availability={
                    "Spring": 0.8, "Summer": 1.0, "Autumn": 0.7, "Winter": 0.2
                }
            )
        ]
        
        return routes
    
    def _initialize_economic_context(self) -> Dict:
        """Initialize Renaissance economic context."""
        
        return {
            "currency": "Florin d'oro (gold florin)",
            "exchange_rates": {
                "florin_to_lira": 7,  # 1 florin = 7 lire
                "florin_to_ducat": 0.8,  # 1 florin = 0.8 ducats
                "florin_to_scudo": 1.2
            },
            "inflation_rate": 0.02,  # 2% annual inflation
            "craftsman_daily_wage": 0.25,  # florins per day
            "master_craftsman_daily_wage": 0.5,  # florins per day
            "apprentice_daily_wage": 0.1,  # florins per day
            "tax_rates": {
                "import_duty": 0.10,  # 10% import tax
                "guild_tax": 0.05,  # 5% guild tax
                "sales_tax": 0.03  # 3% sales tax
            },
            "payment_terms": {
                "standard_net_30": 0.02,  # 2% discount for 30 days
                "standard_net_60": 0.0,  # No discount for 60 days
                "cash_advance": 0.05   # 5% discount for cash advance
            }
        }
    
    def calculate_material_cost(self, material_name: str, quantity: float, 
                              selected_supplier: Optional[Supplier] = None) -> MaterialCost:
        """Calculate comprehensive material cost."""
        
        material = self.db.get_material(material_name)
        if material is None:
            raise ValueError(f"Unknown material: {material_name}")
        
        # Get supplier information
        if selected_supplier is None:
            suppliers = self.suppliers.get(material_name, [])
            if suppliers:
                selected_supplier = suppliers[0]  # Use primary supplier
            else:
                # Create default supplier
                selected_supplier = Supplier(
                    name="Unknown Supplier",
                    location="Unknown",
                    specialty="General",
                    reliability_rating=0.5,
                    price_multiplier=1.0,
                    lead_time_days=30,
                    payment_terms="Standard",
                    quality_consistency=0.5
                )
        
        # Base material cost
        base_cost = material.cost_per_unit * quantity
        
        # Supplier cost adjustment
        supplier_cost = base_cost * selected_supplier.price_multiplier
        
        # Transportation cost
        transport_cost = self._calculate_transportation_cost(material_name, selected_supplier)
        
        # Taxes and duties
        taxes_duties = self._calculate_taxes_and_duties(material_name, supplier_cost)
        
        # Processing cost (for materials requiring additional processing)
        processing_cost = self._calculate_processing_cost(material_name, quantity)
        
        # Total cost
        total_cost = (base_cost + supplier_cost + transport_cost + 
                     taxes_duties + processing_cost)
        
        # Cost breakdown
        cost_breakdown = {
            "base_material_cost": base_cost,
            "supplier_premium": supplier_cost - base_cost,
            "transportation": transport_cost,
            "taxes_duties": taxes_duties,
            "processing": processing_cost
        }
        
        return MaterialCost(
            material_name=material_name,
            base_cost=base_cost,
            quantity=quantity,
            supplier_cost=supplier_cost,
            transportation_cost=transport_cost,
            taxes_duties=taxes_duties,
            processing_cost=processing_cost,
            total_cost=total_cost,
            cost_breakdown=cost_breakdown
        )
    
    def _calculate_transportation_cost(self, material_name: str, supplier: Supplier) -> float:
        """Calculate transportation cost based on supplier location."""
        
        # Base transportation cost factor
        if "Florence" in supplier.location:
            return 0.0  # Local pickup
        
        # Determine route and cost
        if "Venice" in supplier.location or "Ragusa" in supplier.location:
            route = self.trade_routes["adriatic"][0]
            base_transport_cost = 50.0  # Base cost per ton
        elif "Alexandria" in supplier.location or "Constantinople" in supplier.location:
            route = self.trade_routes["levantine"][0]
            base_transport_cost = 150.0  # Higher cost for longer routes
        elif "Seville" in supplier.location:
            route = self.trade_routes["atlantic"][0]
            base_transport_cost = 200.0  # Atlantic route premium
        else:
            route = self.trade_routes["trans_alpine"][0]
            base_transport_cost = 30.0  # Overland transport
        
        # Adjust for material weight and distance
        material = self.db.get_material(material_name)
        weight_factor = material.density_kg_m3 / 1000.0  # Convert to tons/m³
        
        transport_cost = base_transport_cost * weight_factor * route.cost_factor
        
        # Seasonal adjustment
        current_season = "Summer"  # Assume summer construction
        seasonal_factor = route.seasonal_availability.get(current_season, 1.0)
        
        return transport_cost * (2.0 - seasonal_factor)  # Higher cost in difficult seasons
    
    def _calculate_taxes_and_duties(self, material_name: str, supplier_cost: float) -> float:
        """Calculate taxes and import duties."""
        
        material = self.db.get_material(material_name)
        
        total_taxes = 0.0
        
        # Import duties for non-local materials
        if material.availability != "Local":
            import_duty = supplier_cost * self.renaissance_economics["tax_rates"]["import_duty"]
            total_taxes += import_duty
        
        # Guild taxes
        guild_tax = supplier_cost * self.renaissance_economics["tax_rates"]["guild_tax"]
        total_taxes += guild_tax
        
        # Sales tax
        sales_tax = supplier_cost * self.renaissance_economics["tax_rates"]["sales_tax"]
        total_taxes += sales_tax
        
        return total_taxes
    
    def _calculate_processing_cost(self, material_name: str, quantity: float) -> float:
        """Calculate additional processing costs."""
        
        material = self.db.get_material(material_name)
        
        # Base processing rate (florins per cubic meter)
        processing_rates = {
            "Hardwood": 40.0,  # Sawing, planing, seasoning
            "Softwood": 25.0,
            "Copper Alloy": 120.0,  # Casting, finishing
            "Iron Alloy": 80.0,  # Forging, heat treatment
            "Precious Metal": 300.0,  # Specialized processing
            "Organic": 15.0,  # Cutting, shaping
            "Textile": 35.0,  # Cutting, sewing
            "Mineral Pigment": 200.0  # Grinding, purification
        }
        
        base_rate = processing_rates.get(material.material_type, 50.0)
        
        # Adjust for processing difficulty
        difficulty_multiplier = 1.0 + (material.processing_difficulty - 3) * 0.2
        
        return base_rate * quantity * difficulty_multiplier
    
    def analyze_component_costs(self) -> Dict[str, Dict[str, MaterialCost]]:
        """Analyze costs for all lion components."""
        
        recommendations = self.analyzer.generate_component_recommendations()
        component_costs = {}
        
        for component_name, analysis in recommendations.items():
            primary_material = analysis["primary_selection"]["material"]
            
            # Estimate quantity needed
            quantity = self.analyzer._estimate_component_volume(component_name)
            
            if quantity > 0:
                # Get best supplier for this material
                suppliers = self.suppliers.get(primary_material.name, [])
                best_supplier = suppliers[0] if suppliers else None
                
                # Calculate cost
                material_cost = self.calculate_material_cost(
                    primary_material.name, quantity, best_supplier
                )
                
                component_costs[component_name] = {
                    "primary_material": material_cost,
                    "alternatives": {}
                }
                
                # Calculate costs for alternatives
                for alt_name in analysis["primary_selection"]["alternatives"]:
                    alt_material = self.db.get_material(alt_name[0])
                    alt_suppliers = self.suppliers.get(alt_name[0], [])
                    alt_supplier = alt_suppliers[0] if alt_suppliers else None
                    
                    alt_cost = self.calculate_material_cost(
                        alt_material.name, quantity, alt_supplier
                    )
                    
                    component_costs[component_name]["alternatives"][alt_name[0]] = alt_cost
        
        return component_costs
    
    def generate_total_cost_analysis(self) -> Dict:
        """Generate comprehensive total cost analysis."""
        
        component_costs = self.analyze_component_costs()
        
        total_material_cost = 0.0
        cost_breakdown = {
            "structural_materials": 0.0,
            "metal_components": 0.0,
            "decorative_elements": 0.0,
            "functional_components": 0.0,
            "transportation": 0.0,
            "taxes_duties": 0.0,
            "processing": 0.0
        }
        
        # Summarize costs by category
        for component_name, costs in component_costs.items():
            primary_cost = costs["primary_material"]
            total_material_cost += primary_cost.total_cost
            
            # Categorize costs
            material = self.db.get_material(primary_cost.material_name)
            
            if material.material_type in ["Hardwood", "Softwood"]:
                cost_breakdown["structural_materials"] += primary_cost.total_cost
            elif material.material_type in ["Copper Alloy", "Iron Alloy"]:
                cost_breakdown["metal_components"] += primary_cost.total_cost
            elif material.material_type == "Precious Metal":
                cost_breakdown["decorative_elements"] += primary_cost.total_cost
            else:
                cost_breakdown["functional_components"] += primary_cost.total_cost
            
            # Add transportation, taxes, and processing
            cost_breakdown["transportation"] += primary_cost.transportation_cost
            cost_breakdown["taxes_duties"] += primary_cost.taxes_duties
            cost_breakdown["processing"] += primary_cost.processing_cost
        
        # Labor cost estimation
        labor_analysis = self._estimate_labor_costs()
        
        # Timeline analysis
        timeline_analysis = self._analyze_project_timeline()
        
        # Risk analysis
        risk_analysis = self._analyze_cost_risks(component_costs)
        
        return {
            "total_material_cost": total_material_cost,
            "cost_breakdown": cost_breakdown,
            "labor_costs": labor_analysis,
            "total_project_cost": total_material_cost + labor_analysis["total_labor_cost"],
            "cost_per_component": {
                name: costs["primary_material"].total_cost
                for name, costs in component_costs.items()
            },
            "timeline": timeline_analysis,
            "cost_risks": risk_analysis,
            "payment_schedule": self._generate_payment_schedule(total_material_cost, labor_analysis)
        }
    
    def _estimate_labor_costs(self) -> Dict:
        """Estimate labor costs for the project."""
        
        # Labor requirements by component type
        labor_hours = {
            "carpentry": 800,  # Woodworking and frame construction
            "metalworking": 600,  # Bronze and steel work
            "spring_making": 200,  # Specialized spring fabrication
            "assembly": 400,  # Final assembly
            "finishing": 300,  # Surface preparation and finishing
            "testing": 150  # Testing and adjustment
        }
        
        # Skill level distribution
        skill_distribution = {
            "master_craftsmen": 0.3,  # 30% master craftsmen
            "journeymen": 0.5,  # 50% journeymen
            "apprentices": 0.2  # 20% apprentices
        }
        
        total_hours = sum(labor_hours.values())
        
        # Calculate labor costs
        master_hours = total_hours * skill_distribution["master_craftsmen"]
        journeyman_hours = total_hours * skill_distribution["journeymen"]
        apprentice_hours = total_hours * skill_distribution["apprentices"]
        
        master_cost = master_hours * self.renaissance_economics["master_craftsman_daily_wage"] / 8.0  # Convert to hourly
        journeyman_cost = journeyman_hours * 0.35 / 8.0  # Average journeyman rate
        apprentice_cost = apprentice_hours * self.renaissance_economics["apprentice_daily_wage"] / 8.0
        
        total_labor_cost = master_cost + journeyman_cost + apprentice_cost
        
        return {
            "total_hours": total_hours,
            "master_craftsmen_hours": master_hours,
            "journeymen_hours": journeyman_hours,
            "apprentice_hours": apprentice_hours,
            "master_craftsmen_cost": master_cost,
            "journeymen_cost": journeyman_cost,
            "apprentice_cost": apprentice_cost,
            "total_labor_cost": total_labor_cost,
            "breakdown_by_task": labor_hours
        }
    
    def _analyze_project_timeline(self) -> Dict:
        """Analyze project timeline and critical path."""
        
        # Material acquisition times
        material_lead_times = {}
        
        for material_name, suppliers in self.suppliers.items():
            if suppliers:
                # Use longest lead time for safety
                max_lead_time = max(supplier.lead_time_days for supplier in suppliers)
                material_lead_times[material_name] = max_lead_time
        
        # Construction phases
        phases = {
            "material_acquisition": {
                "duration_days": max(material_lead_times.values()) if material_lead_times else 30,
                "critical_materials": [name for name, time in material_lead_times.items() if time > 60]
            },
            "frame_construction": {
                "duration_days": 45,
                "depends_on": ["material_acquisition"]
            },
            "mechanism_fabrication": {
                "duration_days": 60,
                "depends_on": ["material_acquisition"]
            },
            "casting_and_metalwork": {
                "duration_days": 50,
                "depends_on": ["material_acquisition"]
            },
            "assembly": {
                "duration_days": 30,
                "depends_on": ["frame_construction", "mechanism_fabrication", "casting_and_metalwork"]
            },
            "finishing": {
                "duration_days": 25,
                "depends_on": ["assembly"]
            },
            "testing_and_adjustment": {
                "duration_days": 20,
                "depends_on": ["finishing"]
            }
        }
        
        # Calculate critical path
        total_duration = sum(phase["duration_days"] for phase in phases.values())
        
        return {
            "total_duration_days": total_duration,
            "total_duration_months": total_duration / 30.0,
            "phases": phases,
            "critical_path_materials": material_lead_times,
            "potential_delays": self._identify_potential_delays(material_lead_times)
        }
    
    def _identify_potential_delays(self, material_lead_times: Dict[str, int]) -> List[str]:
        """Identify potential delay sources."""
        
        delays = []
        
        for material_name, lead_time in material_lead_times.items():
            if lead_time > 90:
                delays.append(f"{material_name}: Long lead time ({lead_time} days)")
            elif lead_time > 60:
                delays.append(f"{material_name}: Moderate lead time ({lead_time} days)")
        
        # Seasonal considerations
        delays.append("Winter weather may affect overland transportation")
        delays.append("Mediterranean storm season (Sept-Nov) may affect shipping")
        
        # Supplier reliability issues
        for material_name, suppliers in self.suppliers.items():
            for supplier in suppliers:
                if supplier.reliability_rating < 0.7:
                    delays.append(f"{supplier.name}: Low reliability rating")
        
        return delays
    
    def _analyze_cost_risks(self, component_costs: Dict) -> Dict:
        """Analyze potential cost risks and mitigation strategies."""
        
        risk_factors = []
        mitigation_strategies = []
        
        # Material availability risks
        for component_name, costs in component_costs.items():
            primary_cost = costs["primary_material"]
            material = self.db.get_material(primary_cost.material_name)
            
            if material.availability in ["International", "Rare"]:
                risk_factors.append({
                    "risk": f"{material.name} supply disruption",
                    "impact": "High",
                    "probability": "Medium",
                    "component": component_name
                })
                mitigation_strategies.append(
                    f"Order {material.name} well in advance with safety stock"
                )
        
        # Price volatility risks
        for material_name in ["gold_leaf", "ultramarine", "bronze_florentine"]:
            if material_name in self.db.materials:
                risk_factors.append({
                    "risk": f"{material_name} price volatility",
                    "impact": "Medium",
                    "probability": "High",
                    "component": "Multiple"
                })
                mitigation_strategies.append(
                    f"Lock in {material_name} prices through forward contracts"
                )
        
        # Quality risks
        for material_name, suppliers in self.suppliers.items():
            for supplier in suppliers:
                if supplier.quality_consistency < 0.7:
                    risk_factors.append({
                        "risk": f"Quality variation from {supplier.name}",
                        "impact": "Medium",
                        "probability": "Medium",
                        "component": "Multiple"
                    })
                    mitigation_strategies.append(
                        f"Implement quality testing for {supplier.name} materials"
                    )
        
        return {
            "risk_factors": risk_factors,
            "mitigation_strategies": mitigation_strategies,
            "contingency_recommendation": "Include 20% contingency budget for material risks"
        }
    
    def _generate_payment_schedule(self, material_cost: float, labor_costs: Dict) -> Dict:
        """Generate payment schedule for the project."""
        
        total_cost = material_cost + labor_costs["total_labor_cost"]
        
        # Renaissance payment structure
        payments = [
            {
                "payment_number": 1,
                "description": "Initial deposit - Material procurement",
                "amount": total_cost * 0.30,
                "timing": "Project start",
                "purpose": "Secure materials and begin work"
            },
            {
                "payment_number": 2,
                "description": "Progress payment - Frame completion",
                "amount": total_cost * 0.25,
                "timing": "Month 2",
                "purpose": "Completion of main structural frame"
            },
            {
                "payment_number": 3,
                "description": "Progress payment - Mechanism installation",
                "amount": total_cost * 0.25,
                "timing": "Month 4",
                "purpose": "Installation of walking mechanism"
            },
            {
                "payment_number": 4,
                "description": "Final payment - Project completion",
                "amount": total_cost * 0.20,
                "timing": "Month 6",
                "purpose": "Final delivery and acceptance testing"
            }
        ]
        
        return {
            "total_contract_value": total_cost,
            "payment_schedule": payments,
            "payment_terms": "Net 30 days from invoice",
            "late_payment_penalties": "2% per month overdue"
        }
