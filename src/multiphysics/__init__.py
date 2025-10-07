"""
DaVinci Codex Multi-Physics Simulation Framework

Advanced computational models for Leonardo's mechanical inventions incorporating:
- Fluid-Structure Interaction (FSI)
- Aeroelasticity and wing deformation
- Material stress and fatigue analysis
- Multi-body dynamics with constraints
- Thermal effects and material properties
- Optimization algorithms for design improvement

This framework enables high-fidelity simulation of Renaissance engineering
concepts using modern computational methods.
"""

from .aerodynamics import AerodynamicsModule
from .core import MultiPhysicsSimulator
from .materials import MaterialsModule
from .optimization import OptimizationEngine
from .structures import StructuralModule
from .validation import ValidationSuite

__version__ = "1.0.0"
__author__ = "DaVinci Codex Research Team"

__all__ = [
    "MultiPhysicsSimulator",
    "AerodynamicsModule",
    "StructuralModule",
    "MaterialsModule",
    "OptimizationEngine",
    "ValidationSuite"
]
