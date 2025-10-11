"""The Armored Walker - A walking war machine combining the chassis of the Self-Propelled Cart with the leg mechanism of the Mechanical Lion."""

from __future__ import annotations

from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np
import math
import matplotlib.pyplot as plt
from ..artifacts import ensure_artifact_dir

# --- Constants and Parameters ---

SLUG = "armored_walker"
TITLE = "The Armored Walker"
STATUS = "simulation_prototype"
SUMMARY = "A walking war machine combining the chassis of the Self-Propelled Cart with the leg mechanism of the Mechanical Lion."

GRAVITY = 9.80665

# --- Dataclasses ---

@dataclass
class SpringProperties:
    k_linear: float
    max_theta: float
    material: str

@dataclass
class GearStage:
    ratio: float
    efficiency: float

@dataclass
class EscapementProperties:
    period_target: float # Time per step cycle

@dataclass
class WalkerParameters:
    mass_kg: float
    drag_coefficient: float
    frontal_area_m2: float
    rolling_resistance: float # A combined friction term for the walking mechanism
    stride_length_m: float
    timestep_s: float
    duration_s: float
    spring: SpringProperties
    gear_train: List[GearStage]
    escapement: EscapementProperties

# --- Simulation Core ---

def plan() -> Dict[str, object]:
    """Planning document for the Armored Walker."""
    # ... (plan function remains the same)

def _simulate_dynamics(params: WalkerParameters) -> Dict:
    """Final, corrected simulation based on stride kinematics and power constraints."""
    steps = int(params.duration_s / params.timestep_s) + 1
    time = np.linspace(0.0, params.duration_s, steps)

    # State arrays
    position = np.zeros_like(time)
    velocity = np.zeros_like(time)
    spring_theta = np.zeros_like(time)
    power_available = np.zeros_like(time)
    power_required = np.zeros_like(time)

    spring_theta[0] = params.spring.max_theta

    # Determine target velocity from gait
    stride_frequency = 1.0 / params.escapement.period_target
    target_velocity = params.stride_length_m * stride_frequency

    total_gear_ratio = np.prod([stage.ratio for stage in params.gear_train])
    total_efficiency = np.prod([stage.efficiency for stage in params.gear_train])

    # Camshaft speed is determined by the escapement
    cam_shaft_omega = 2 * math.pi / params.escapement.period_target

    for i in range(1, steps):
        # Calculate available power from the spring
        torque = params.spring.k_linear * spring_theta[i-1]
        spring_power = torque * (cam_shaft_omega / total_gear_ratio)
        power_available[i] = spring_power * total_efficiency

        # Calculate power required to move at target velocity
        drag_force = 0.5 * 1.225 * params.drag_coefficient * params.frontal_area_m2 * target_velocity**2
        friction_force = params.rolling_resistance * params.mass_kg * GRAVITY
        power_required[i] = (drag_force + friction_force) * target_velocity

        # Check if there is enough power to walk
        if power_available[i] >= power_required[i]:
            velocity[i] = target_velocity
        else:
            # Not enough power, the machine stops
            velocity[i] = 0
            break # End simulation

        # Update position
        position[i] = position[i-1] + velocity[i] * params.timestep_s

        # Update spring based on power consumed
        power_drawn_from_spring = power_required[i] / total_efficiency
        torque_drawn = power_drawn_from_spring / (cam_shaft_omega / total_gear_ratio)
        theta_unwound = torque_drawn / params.spring.k_linear
        spring_theta[i] = spring_theta[i-1] - theta_unwound

        if spring_theta[i] < 0:
            break

    return {
        "time": time[:i],
        "position": position[:i],
        "velocity": velocity[:i],
        "power_available": power_available[:i],
        "power_required": power_required[:i],
    }

def _plot_profiles(path: Path, result: Dict, params: WalkerParameters) -> None:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.suptitle("Armored Walker Performance Analysis", fontsize=16, fontweight='bold')

    # Plot Position and Velocity
    ax1.plot(result["time"], result["position"], label="Position (m)", color='b')
    ax1.set_ylabel("Position (m)", color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True, linestyle='--')

    ax1_twin = ax1.twinx()
    ax1_twin.plot(result["time"], result["velocity"], label="Velocity (m/s)", color='r')
    ax1_twin.set_ylabel("Velocity (m/s)", color='r')
    ax1_twin.tick_params(axis='y', labelcolor='r')
    ax1.set_title("Motion Profile")

    # Plot Power
    ax2.plot(result["time"], result["power_available"], label="Power Available (W)", color='g')
    ax2.plot(result["time"], result["power_required"], label="Power Required (W)", color='orange')
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Power (W)")
    ax2.legend()
    ax2.grid(True)
    ax2.set_title("Power Dynamics")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path)
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    """Simulation for the Armored Walker."""
    spring_props = SpringProperties(
        k_linear=500.0, max_theta=150.0, material="advanced_renaissance_alloy"
    )
    gear_train = [GearStage(ratio=20.0, efficiency=0.8), GearStage(ratio=20.0, efficiency=0.8)]
    escapement_props = EscapementProperties(period_target=3.0)
    params = WalkerParameters(
        mass_kg=1200.0,
        drag_coefficient=2.0,
        frontal_area_m2=3.0,
        rolling_resistance=0.08,
        stride_length_m=0.8,
        timestep_s=0.1,
        duration_s=600.0,
        spring=spring_props,
        gear_train=gear_train,
        escapement=escapement_props,
    )

    sim_results = _simulate_dynamics(params)

    artifacts_dir = ensure_artifact_dir(SLUG, subdir="sim")
    plot_path = artifacts_dir / "armored_walker_final_dynamics.png"
    _plot_profiles(plot_path, sim_results, params)

    return {
        "status": "final_simulation_complete",
        "artifacts": [str(plot_path)],
        "results": {
            "travel_distance_m": sim_results["position"][-1],
            "constant_speed_ms": sim_results["velocity"][-1],
            "runtime_s": sim_results["time"][-1],
        },
    }

def build() -> None:
    """Build instructions for the Armored Walker."""
    print("Build function for the Armored Walker is not yet implemented.")

def evaluate() -> Dict[str, object]:
    """Evaluation of the Armored Walker."""
    return {
        "status": "not_implemented",
        "notes": "The evaluation for the Armored Walker is not yet implemented.",
    }
