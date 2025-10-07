"""da Vinci Codex Innovations Module."""

from __future__ import annotations

from .innovation_discovery import SLUG as INNOVATION_DISCOVERY_SLUG
from .modern_inventions import get_modern_inventions, analyze_modern_inventions
from .bio_inspired_workflow import BioInspiredWorkflow
from .innovation_platform import InnovationPlatform
from .partnership_network import StrategicPartnershipNetwork
from .impact_analytics import ImpactAnalyticsSystem

__all__ = [
    "INNOVATION_DISCOVERY_SLUG",
    "get_modern_inventions",
    "analyze_modern_inventions",
    "BioInspiredWorkflow",
    "InnovationPlatform",
    "StrategicPartnershipNetwork",
    "ImpactAnalyticsSystem"
]