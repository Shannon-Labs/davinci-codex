"""Physics-inspired flapping wing simulation used by the test suite.

The repository originally referenced a synthesis module that did not make it
into the open-source drop. The CI exercises this simulator directly, so we
reconstruct a light-weight, numerically stable approximation here. The goal is
to provide deterministic outputs with the right units rather than a full CFD
model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np

_ARTIFACT_DIR = (
    Path(__file__).resolve().parents[3]
    / "artifacts"
    / "ornithopter"
    / "synthesis_sim"
)


@dataclass(slots=True, frozen=True)
class AeroelasticParameters:
    """Configuration bundle for the simplified aeroelastic model."""

    wing_span_m: float = 2.4
    wing_area_m2: float = 1.15
    flapping_frequency_hz: float = 2.4
    stroke_angle_deg: float = 75.0
    lift_coefficient: float = 1.1
    drag_coefficient: float = 0.12
    air_density: float = 1.225
    moment_arm_m: float = 0.58
    control_torque_limit_nm: float = 320.0
    motor_efficiency: float = 0.82
    battery_capacity_wh: float = 150.0
    damping_ratio: float = 0.07


@dataclass(slots=True)
class SimulationResult:
    """Container for simulation outputs with convenience helpers."""

    time: np.ndarray
    stroke_angle_rad: np.ndarray
    lift_N: np.ndarray
    torque_nm: np.ndarray
    control_torque_nm: np.ndarray
    energy_wh: float
    endurance_min: float

    def to_csv(self, destination: Path) -> None:
        """Persist the full state history to ``destination`` in CSV form."""

        header = "time_s,stroke_angle_rad,lift_N,torque_Nm,control_torque_Nm"
        data = np.column_stack(
            (
                self.time,
                self.stroke_angle_rad,
                self.lift_N,
                self.torque_nm,
                self.control_torque_nm,
            )
        )
        np.savetxt(destination, data, header=header, delimiter=",", comments="")


def _ensure_artifact_dir() -> None:
    _ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def _compute_stroke_angle(
    time: np.ndarray,
    params: AeroelasticParameters,
    rng: np.random.Generator,
) -> np.ndarray:
    stroke_amplitude = 0.5 * np.deg2rad(params.stroke_angle_deg)
    omega = 2.0 * np.pi * params.flapping_frequency_hz
    signal = stroke_amplitude * np.sin(omega * time)

    noise = rng.normal(scale=stroke_amplitude * 0.015, size=time.size)
    damped_signal = signal * np.exp(-params.damping_ratio * time) + noise
    return np.clip(damped_signal, -stroke_amplitude * 1.05, stroke_amplitude * 1.05)


def _compute_lift(
    stroke_angle: np.ndarray,
    stroke_rate: np.ndarray,
    params: AeroelasticParameters,
) -> tuple[np.ndarray, np.ndarray]:
    tip_speed = 0.5 * params.wing_span_m * stroke_rate
    dynamic_pressure = 0.5 * params.air_density * tip_speed**2
    lift = dynamic_pressure * params.wing_area_m2 * params.lift_coefficient
    lift = np.clip(lift, 0.0, None)

    torque = lift * params.moment_arm_m
    return lift, torque


def _compute_control_torque(
    time: np.ndarray,
    params: AeroelasticParameters,
    rng: np.random.Generator,
) -> np.ndarray:
    omega = 2.0 * np.pi * params.flapping_frequency_hz
    base = 0.45 * params.control_torque_limit_nm * np.sin(omega * time + np.pi / 8.0)
    modulation = 0.15 * params.control_torque_limit_nm * np.sin(omega * time * 0.5)
    noise = rng.normal(scale=params.control_torque_limit_nm * 0.04, size=time.size)

    control = base + modulation + noise
    return np.clip(control, -params.control_torque_limit_nm, params.control_torque_limit_nm)


def simulate(
    duration_s: float = 10.0,
    dt: float = 0.01,
    seed: Optional[int] = None,
    params: Optional[AeroelasticParameters] = None,
) -> SimulationResult:
    """Run a reproducible flapping simulation.

    The implementation aims for numerical stability and monotonic energy usage
    so automated checks remain deterministic across platforms.
    """

    if duration_s <= 0:
        raise ValueError("duration_s must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")

    params = params or AeroelasticParameters()
    rng = np.random.default_rng(seed)

    steps = int(np.floor(duration_s / dt)) + 1
    time = np.linspace(0.0, dt * (steps - 1), steps)

    stroke_angle = _compute_stroke_angle(time, params, rng)
    stroke_rate = np.gradient(stroke_angle, dt)
    lift, torque = _compute_lift(stroke_angle, stroke_rate, params)
    control_torque = _compute_control_torque(time, params, rng)

    mechanical_power = np.abs(control_torque * stroke_rate)
    energy_joules = np.trapz(mechanical_power, time) / max(params.motor_efficiency, 1e-6)
    energy_wh = energy_joules / 3600.0

    average_power_w = float(np.mean(mechanical_power))
    if average_power_w > 1e-6:
        endurance_hours = params.battery_capacity_wh / (average_power_w / 1000.0)
    else:
        endurance_hours = duration_s / 3600.0
    endurance_min = endurance_hours * 60.0

    result = SimulationResult(
        time=time,
        stroke_angle_rad=stroke_angle,
        lift_N=lift,
        torque_nm=torque,
        control_torque_nm=control_torque,
        energy_wh=float(energy_wh),
        endurance_min=float(endurance_min),
    )

    _ensure_artifact_dir()
    result.to_csv(_ARTIFACT_DIR / "flapping_state.csv")

    summary_path = _ARTIFACT_DIR / "summary.txt"
    summary_path.write_text(
        (
            "Ornithopter Synthesis Simulation\n"
            f"Duration [s]: {duration_s:.2f}\n"
            f"Samples: {len(time)}\n"
            f"Peak lift [N]: {float(np.max(lift)):.2f}\n"
            f"Peak control torque [Nm]: {float(np.max(np.abs(control_torque))):.2f}\n"
            f"Energy used [Wh]: {float(energy_wh):.2f}\n"
            f"Estimated endurance [min]: {float(endurance_min):.2f}\n"
        ),
        encoding="utf-8",
    )

    return result


__all__ = [
    "AeroelasticParameters",
    "SimulationResult",
    "simulate",
]

