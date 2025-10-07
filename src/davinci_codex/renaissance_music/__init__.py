"""Renaissance Music Adaptation system for Leonardo's mechanical instruments."""

from .analysis import RenaissanceAnalyzer
from .cli import app
from .composition import RenaissanceCompositionGenerator
from .constraints import MechanicalConstraintValidator
from .integration import MechanicalEnsembleIntegrator
from .models import (
    AdaptationResult,
    InstrumentConstraints,
    MusicalPattern,
    MusicalScore,
)
from .pattern_composer import PatternBasedComposer
from .patterns import RenaissancePatternLibrary

__all__ = [
    "MusicalScore",
    "InstrumentConstraints",
    "MusicalPattern",
    "AdaptationResult",
    "RenaissanceAnalyzer",
    "MechanicalConstraintValidator",
    "RenaissancePatternLibrary",
    "MechanicalEnsembleIntegrator",
    "RenaissanceCompositionGenerator",
    "PatternBasedComposer",
    "app",
]
