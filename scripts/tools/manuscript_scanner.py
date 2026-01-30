"""Digitisation utilities for cataloguing Leonardo's manuscripts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class FolioRecord:
    """Minimal folio descriptor used by ManuscriptDigitizer."""

    number: str
    image: str
    annotations: dict


class ManuscriptDigitizer:
    """Extract and catalog all mechanical sketches from digitised folios."""

    def scan_codex(self, manuscript: str = "Codex Atlanticus") -> List[dict]:
        inventions: List[dict] = []
        for folio in self.get_folios(manuscript):
            text = self.mirror_ocr(folio.image)
            components = self.detect_mechanical_primitives(folio.image)
            dimensions = self.extract_measurements(folio.annotations)
            inventions.append(
                {
                    "folio_id": f"{manuscript} f.{folio.number}",
                    "date_estimate": self.date_by_style(folio),
                    "category": self.classify_mechanism(components),
                    "completeness": self.assess_detail_level(dimensions),
                    "transcription": text,
                    "components": components,
                    "related_folios": self.find_similar(folio),
                }
            )
        return inventions

    def get_folios(self, manuscript: str) -> Iterable[FolioRecord]:  # pragma: no cover - to be implemented
        return []

    def mirror_ocr(self, image_path: str) -> str:  # pragma: no cover - to be implemented
        raise NotImplementedError

    def detect_mechanical_primitives(self, image_path: str) -> List[str]:  # pragma: no cover - to be implemented
        raise NotImplementedError

    def extract_measurements(self, annotations: dict) -> dict:  # pragma: no cover - to be implemented
        raise NotImplementedError

    def date_by_style(self, folio: FolioRecord) -> str:  # pragma: no cover - to be implemented
        raise NotImplementedError

    def classify_mechanism(self, components: List[str]) -> str:  # pragma: no cover - to be implemented
        raise NotImplementedError

    def assess_detail_level(self, dimensions: dict) -> float:  # pragma: no cover - to be implemented
        raise NotImplementedError

    def find_similar(self, folio: FolioRecord) -> List[str]:  # pragma: no cover - to be implemented
        raise NotImplementedError


__all__ = ["ManuscriptDigitizer", "FolioRecord"]
