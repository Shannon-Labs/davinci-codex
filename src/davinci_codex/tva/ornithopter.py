"""Historical viability analysis for Leonardo's ornithopter."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from ..inventions.ornithopter import PARAM_FILE as SYNTHESIS_PARAM_FILE
from ..inventions.ornithopter import GRAVITY


def _as_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    raise TypeError(f"Expected dict, received {type(value)!r}")


def _to_float(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        return float(value)
    raise TypeError(f"Cannot convert {value!r} to float")

ROOT = Path(__file__).resolve().parents[3]
TVA_ROOT = ROOT / "tva" / "ornithopter"
PARAM_FILE = TVA_ROOT / "materials.yaml"
POWER_FILE = TVA_ROOT / "human_power_profiles.csv"
SPAN_M = 10.5  # derived from intent.json assumptions
REQUIRED_CYCLES = 500


@dataclass
class Material:
    density_kg_m3: float
    fatigue_strength_MPa: float
    fatigue_exponent: float
    allowable_stress_MPa: float
    section_modulus_m3: float


@dataclass
class PowerProfile:
    profile: str
    avg_power_w: float
    duration_s: float
    notes: str


@dataclass
class TVAResult:
    required_power_w: float
    sustained_power_available_w: float
    peak_power_available_w: float
    power_margin_w: float
    torque_required_nm: float
    spring_capacity_nm: float
    torque_margin_nm: float
    stress_range_MPa: float
    stress_ratio: float
    fatigue_cycles: float
    passes_power: bool
    passes_fatigue: bool


def _load_materials() -> Tuple[Material, Dict[str, Any]]:
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        raw = yaml.safe_load(stream)
    materials = _as_dict(raw.get("materials", {}))
    surfaces = _as_dict(raw.get("surfaces", {}))
    springs = _as_dict(raw.get("springs", {}))
    limits = _as_dict(raw.get("limits", {}))
    fir = _as_dict(materials["fir_spar"])
    material = Material(
        density_kg_m3=fir["density_kg_m3"],
        fatigue_strength_MPa=fir["fatigue_strength_MPa"],
        fatigue_exponent=fir["fatigue_exponent"],
        allowable_stress_MPa=fir["allowable_stress_MPa"],
        section_modulus_m3=fir["section_modulus_m3"],
    )
    torsion = _as_dict(springs["torsion_pair"])

    surface_density: float = _to_float(surfaces["renaissance_surface_density_kg_m2"])
    modern_surface_density: float = _to_float(surfaces["modern_surface_density_kg_m2"])
    spring_capacity: float = _to_float(torsion["max_torque_nm"])
    spring_stiffness: float = _to_float(torsion["stiffness_nm_per_rad"])
    minimum_cycles: float = _to_float(limits.get("minimum_cycles_required", REQUIRED_CYCLES))
    sustained_power_target: float = _to_float(limits.get("sustained_power_target_w", 600.0))

    context: Dict[str, Any] = {
        "surface_density_kg_m2": surface_density,
        "modern_surface_density_kg_m2": modern_surface_density,
        "spring_capacity_nm": spring_capacity,
        "spring_stiffness_nm_per_rad": spring_stiffness,
        "minimum_cycles_required": minimum_cycles,
        "sustained_power_target_w": sustained_power_target,
    }
    return material, context


def _load_power_profiles() -> List[PowerProfile]:
    profiles: List[PowerProfile] = []
    with POWER_FILE.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            profiles.append(
                PowerProfile(
                    profile=row["profile"],
                    avg_power_w=float(row["avg_power_w"]),
                    duration_s=float(row["duration_s"]),
                    notes=row["notes"],
                )
            )
    return profiles


def evaluate_viability() -> TVAResult:
    """Compute historical viability metrics for the ornithopter."""
    params = _load_synthesis_parameters()
    material, context = _load_materials()
    power_profiles = _load_power_profiles()

    surface_density = _to_float(context["surface_density_kg_m2"])
    wing_mass_total = params["wing_area_m2"] * surface_density
    wing_mass_per_side = wing_mass_total / 2.0
    lever_arm_m = SPAN_M / 4.0

    torque_per_side = wing_mass_per_side * GRAVITY * lever_arm_m
    total_torque = 2.0 * torque_per_side
    angular_velocity = 2.0 * math.pi * params["flap_frequency_hz"]
    required_power = total_torque * angular_velocity

    sustained_profile = max(
        (p for p in power_profiles if p.duration_s >= 60.0),
        key=lambda item: item.avg_power_w,
        default=None,
    )
    sustained_power = sustained_profile.avg_power_w if sustained_profile else 0.0
    peak_power = max((p.avg_power_w for p in power_profiles), default=0.0)

    spring_capacity = _to_float(context["spring_capacity_nm"])
    torque_margin = spring_capacity - total_torque

    stress_range = (torque_per_side / material.section_modulus_m3) / 1e6  # convert to MPa
    stress_ratio = stress_range / material.allowable_stress_MPa
    fatigue_strength_pa = material.fatigue_strength_MPa * 1e6
    stress_range_pa = stress_range * 1e6
    if stress_range_pa <= 0:
        fatigue_cycles = math.inf
    else:
        ratio = fatigue_strength_pa / stress_range_pa
        fatigue_cycles = ratio ** material.fatigue_exponent if ratio > 0 else 0.0

    passes_power = sustained_power >= required_power
    passes_fatigue = fatigue_cycles >= _to_float(context["minimum_cycles_required"])

    return TVAResult(
        required_power_w=required_power,
        sustained_power_available_w=sustained_power,
        peak_power_available_w=peak_power,
        power_margin_w=sustained_power - required_power,
        torque_required_nm=total_torque,
        spring_capacity_nm=spring_capacity,
        torque_margin_nm=torque_margin,
        stress_range_MPa=stress_range,
        stress_ratio=stress_ratio,
        fatigue_cycles=fatigue_cycles,
        passes_power=passes_power,
        passes_fatigue=passes_fatigue,
    )


def _load_synthesis_parameters() -> Dict[str, float]:
    with SYNTHESIS_PARAM_FILE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    return {
        "wing_area_m2": float(data["wing_area_m2"]),
        "stroke_amplitude_m": float(data["stroke_amplitude_m"]),
        "flap_frequency_hz": float(data["flap_frequency_hz"]),
        "forward_speed_ms": float(data["forward_speed_ms"]),
    }
