"""Pydantic models for validating the invention catalog."""

from __future__ import annotations

from collections import Counter
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class Category(str, Enum):
    textile = "textile"
    hydraulic = "hydraulic"
    workshop = "workshop"
    civil = "civil"
    measurement = "measurement"
    agriculture = "agriculture"
    domestic = "domestic"
    experimental = "experimental"
    music = "music"


class StatusFlag(str, Enum):
    not_started = "not_started"
    queued = "queued"
    in_progress = "in_progress"
    scheduled = "scheduled"
    pending = "pending"
    research = "research"
    not_applicable = "not_applicable"
    risk_review = "risk_review"


class CompletionLevel(str, Enum):
    detailed_with_dimensions = "detailed_with_dimensions"
    rough_sketch = "rough_sketch"
    concept_only = "concept_only"


class Overview(BaseModel):
    total_target: int = Field(..., gt=0)
    documented: int = Field(..., ge=0)
    focus_areas: Dict[Category, int]
    notes: Optional[str]

    @field_validator("focus_areas")
    @classmethod
    def focus_counts_non_negative(cls, value: Dict[Category, int]) -> Dict[Category, int]:
        for count in value.values():
            if count < 0:
                raise ValueError("Focus area targets must be non-negative")
        return value


class StatusBlock(BaseModel):
    simulation: StatusFlag
    uq: StatusFlag
    fmea: StatusFlag


class InventionRecord(BaseModel):
    slug: str
    folio_reference: str
    category: Category
    date_estimated: str
    completion_level: CompletionLevel
    related_sketches: List[str]
    historical_precedent: Optional[str]
    why_overlooked: Optional[str]
    status: StatusBlock
    provenance: Path

    @field_validator("slug")
    @classmethod
    def slug_must_be_lowercase(cls, value: str) -> str:
        if value.lower() != value:
            raise ValueError("Slug must be lowercase")
        if " " in value:
            raise ValueError("Slug must not contain spaces")
        return value

    @field_validator("related_sketches")
    @classmethod
    def related_sketches_distinct(cls, value: List[str]) -> List[str]:
        if len(value) != len(set(value)):
            raise ValueError("related_sketches entries must be unique")
        return value


class Catalog(BaseModel):
    overview: Overview
    inventions: List[InventionRecord]

    def category_counts(self) -> Dict[Category, int]:
        counts = Counter(record.category for record in self.inventions)
        return {category: counts.get(category, 0) for category in Category}


__all__ = [
    "Catalog",
    "InventionRecord",
    "StatusBlock",
    "StatusFlag",
    "CompletionLevel",
    "Category",
]
