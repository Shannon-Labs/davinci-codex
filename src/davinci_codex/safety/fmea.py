"""Failure Mode and Effects Analysis tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class FailureMode:
    """Structured record for a single failure mode."""

    mode: str
    cause: str
    effect: str
    severity: int
    occurrence: int
    detection: int
    mitigation: str

    @property
    def risk_priority_number(self) -> int:
        """Risk priority number (RPN) defined as severity * occurrence * detection."""
        return self.severity * self.occurrence * self.detection


class InventionFMEA:
    """Generate FMEA assessments for Renaissance mechanisms."""

    def analyze_ornithopter(self) -> List[FailureMode]:
        """Preliminary FMEA based on flapping-wing machine studies."""

        return [
            FailureMode(
                mode="Wing spar fracture",
                cause="Fatigue from cyclic loading",
                effect="Catastrophic loss of lift",
                severity=10,
                occurrence=6,
                detection=3,
                mitigation="Composite reinforcement at stress concentrations",
            ),
            FailureMode(
                mode="Pilot exhaustion",
                cause="Power requirement exceeds human capability",
                effect="Loss of control",
                severity=9,
                occurrence=8,
                detection=7,
                mitigation="Integrate stored-energy assist or counterweight system",
            ),
        ]

    def generate_fmea_report(self, failures: Iterable[FailureMode]) -> dict:
        """Summarise failure modes for reporting pipelines."""

        failure_list = list(failures)
        sorted_failures = sorted(
            failure_list,
            key=lambda item: item.risk_priority_number,
            reverse=True,
        )
        return {
            "failures": [
                {
                    "mode": fm.mode,
                    "cause": fm.cause,
                    "effect": fm.effect,
                    "severity": fm.severity,
                    "occurrence": fm.occurrence,
                    "detection": fm.detection,
                    "mitigation": fm.mitigation,
                    "rpn": fm.risk_priority_number,
                }
                for fm in sorted_failures
            ],
            "max_rpn": max((fm.risk_priority_number for fm in failure_list), default=0),
        }


__all__ = ["FailureMode", "InventionFMEA"]
