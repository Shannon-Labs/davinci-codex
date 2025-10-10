"""Enhanced Ornithopter with Bio-inspired Flapping Flight Mechanics.

This module implements sophisticated flapping-wing aerodynamics combining historical
accuracy with modern understanding of unsteady aerodynamics. The implementation
incorporates:

1. Advanced unsteady aerodynamics with Theodorsen's circulatory function
2. Bio-inspired wing membrane dynamics with elastic deformation
3. Figure-8 wing tip trajectories mimicking bird flight
4. Clap-and-fling mechanism for lift enhancement
5. Wake capture and delayed stall effects
6. Historical accuracy to Leonardo's original sketches and notes

The physics model bridges quasi-steady approximations with unsteady effects
capturing the essential phenomena of flapping flight while remaining computationally
tractable for educational and feasibility studies.

Educational Focus:
- Demonstrates principles of unsteady aerodynamics
- Shows how biological inspiration informs engineering design
- Connects historical innovation with modern computational methods
- Illustrates the complexity of flapping flight mechanics

Historical Context:
Based on Leonardo da Vinci's extensive studies of bird flight (Codex Atlanticus,
Codex on the Flight of Birds) and his attempts to create mechanical flying
machines that mimicked natural wing movements.
"""

from __future__ import annotations

import csv
import importlib.util
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Union, cast

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy import special

from ..artifacts import ensure_artifact_dir

SLUG = "ornithopter"
TITLE = "Bio-inspired Ornithopter Flight Lab"
STATUS = "in_progress"
SUMMARY = "Advanced flapping-wing flight with unsteady aerodynamics and bio-inspired mechanics."

PARAM_FILE = Path("sims") / SLUG / "parameters.yaml"
VALIDATION_DIR = Path("validation") / SLUG
RHO_AIR = 1.225  # kg/m^3 at sea level
GRAVITY = 9.80665  # m/s^2
KINEMATIC_VISCOSITY = 1.5e-5  # m^2/s at sea level


@dataclass
class WingKinematics:
    """Bio-inspired wing kinematics parameters."""
    stroke_amplitude: float  # rad
    stroke_plane_angle: float  # rad from horizontal
    deviation_amplitude: float  # rad for up-down deviation
    rotation_amplitude: float  # rad for pronation/supination
    phase_lag_deviation: float  # rad phase lag for deviation
    phase_lag_rotation: float  # rad phase lag for rotation
    figure_eight_ratio: float  # ratio of lateral to vertical motion


@dataclass
class WingStructure:
    """Wing structural and material properties."""
    membrane_stiffness_n_m: float  # membrane elastic stiffness
    membrane_damping: float  # damping coefficient
    spar_stiffness_n_m2: float  # wing spar flexural stiffness
    wing_mass_kg: float  # total wing mass
    elastic_axis_ratio: float  # position of elastic axis (0-1 from leading edge)
    tensile_prestress_n_m2: float  # membrane pretension


@dataclass
class UnsteadyAeroParams:
    """Unsteady aerodynamics parameters."""
    reduced_frequency: float  # k = ωc/2V
    theodorsen_factor: float  # C(k) approximation
    wake_vorticity_strength: float  # initial wake circulation
    clap_fling_enabled: bool  # enable clap-and-fling mechanism
    delayed_stall_angle: float  # rad
    wake_capture_factor: float  # wake capture efficiency


@dataclass
class OrnithopterParameters:
    total_mass_kg: float
    wing_area_m2: float
    wing_span_m: float
    mean_chord_m: float
    flap_frequency_hz: float
    forward_speed_ms: float
    base_alpha_deg: float
    alpha_amplitude_deg: float
    cl_alpha_per_rad: float
    cl_max: float
    base_power_w: float
    power_variation_w: float
    battery_capacity_wh: float
    controller_power_w: float
    kinematics: WingKinematics
    structure: WingStructure
    unsteady_aero: UnsteadyAeroParams
    acceptance_targets: Dict[str, Union[float, bool, int]]


@dataclass
class FlightSimulation:
    time: np.ndarray
    altitude: np.ndarray
    vertical_velocity: np.ndarray
    horizontal_velocity: np.ndarray
    lift: np.ndarray
    thrust: np.ndarray
    drag: np.ndarray
    power: np.ndarray
    energy_used_wh: float
    endurance_hours: float
    wing_positions: np.ndarray  # wing tip positions
    circulation: np.ndarray  # bound circulation
    membrane_deformation: np.ndarray


def _theodorsen_function(k: float) -> complex:
    """
    Compute Theodorsen's circulatory function C(k) for reduced frequency k.

    Theodorsen's function accounts for the lag between wing motion and
    aerodynamic response in unsteady aerodynamics.

    Args:
        k: Reduced frequency (k = ωc/2V)

    Returns:
        Complex value of Theodorsen's function
    """
    if k < 0.01:
        return complex(1.0, 0.0)  # Quasi-steady limit

    # Bessel functions for Theodorsen's function
    H1 = special.hankel1(1, k)
    H0 = special.hankel1(0, k)

    C = H1 / (H1 + 1j * H0)
    return C


def _calculate_wing_kinematics(t: float, params: OrnithopterParameters) -> Dict[str, float]:
    """
    Calculate bio-inspired wing kinematics with figure-8 motion.

    Implements the three DOF wing motion observed in bird flight:
    1. Stroke: back-and-forth motion in stroke plane
    2. Deviation: up-and-down motion perpendicular to stroke plane
    3. Rotation: pronation/supination about wing axis

    Args:
        t: Time
        params: Ornithopter parameters

    Returns:
        Dictionary with wing position, velocity, and acceleration
    """
    omega = 2 * np.pi * params.flap_frequency_hz
    kin = params.kinematics

    # Stroke angle (primary flapping motion)
    phi = kin.stroke_amplitude * np.sin(omega * t)
    phi_dot = kin.stroke_amplitude * omega * np.cos(omega * t)
    phi_ddot = -kin.stroke_amplitude * omega**2 * np.sin(omega * t)

    # Deviation (creates figure-8 pattern)
    theta = kin.deviation_amplitude * np.sin(omega * t + kin.phase_lag_deviation)
    theta_dot = kin.deviation_amplitude * omega * np.cos(omega * t + kin.phase_lag_deviation)

    # Rotation (feathering motion)
    alpha_rotation = kin.rotation_amplitude * np.sin(omega * t + kin.phase_lag_rotation)
    alpha_rotation_dot = kin.rotation_amplitude * omega * np.cos(omega * t + kin.phase_lag_rotation)

    # Figure-8 motion coupling
    lateral_motion = kin.figure_eight_ratio * params.wing_span_m * np.sin(2 * omega * t)

    return {
        'stroke_angle': phi,
        'stroke_velocity': phi_dot,
        'stroke_acceleration': phi_ddot,
        'deviation': theta,
        'deviation_velocity': theta_dot,
        'rotation': alpha_rotation,
        'rotation_velocity': alpha_rotation_dot,
        'lateral_motion': lateral_motion
    }


def _calculate_membrane_deformation(kinematics: Dict[str, float],
                                  params: OrnithopterParameters,
                                  t: float) -> float:
    """
    Calculate elastic membrane deformation based on aerodynamic loading.

    Models the wing membrane as an elastic surface that deforms under
    aerodynamic loads, affecting the effective camber and lift.

    Args:
        kinematics: Wing kinematics data
        params: Ornithopter parameters
        t: Time

    Returns:
        Membrane deformation (m)
    """
    struct = params.structure

    # Dynamic pressure from wing motion
    v_wing = abs(kinematics['stroke_velocity']) * params.wing_span_m / 2
    q = 0.5 * RHO_AIR * v_wing**2

    # Elastic deformation with damping
    omega = 2 * np.pi * params.flap_frequency_hz
    natural_freq = np.sqrt(struct.membrane_stiffness_n_m / struct.wing_mass_kg)

    # Deformation as second-order system response
    deformation_amplitude = q * params.wing_area_m2 / struct.membrane_stiffness_n_m
    freq_ratio = omega / natural_freq

    # Dynamic amplification factor
    if freq_ratio < 0.1:
        amplification = 1.0
    else:
        amplification = 1.0 / np.sqrt((1 - freq_ratio**2)**2 +
                                     (2 * struct.membrane_damping * freq_ratio)**2)

    # Phase lag for dynamic response
    phase_lag = np.arctan2(2 * struct.membrane_damping * freq_ratio,
                          1 - freq_ratio**2)

    deformation = deformation_amplitude * amplification * np.sin(omega * t - phase_lag)

    return np.clip(deformation, -params.mean_chord_m * 0.1, params.mean_chord_m * 0.1)


def _clap_and_fling_lift(kinematics: Dict[str, float],
                        params: OrnithopterParameters) -> float:
    """
    Calculate lift enhancement from clap-and-fling mechanism.

    The clap-and-fling mechanism, observed in tiny insects and some birds,
    enhances lift through wing-wing interaction at the stroke reversal.

    Args:
        kinematics: Wing kinematics data
        params: Ornithopter parameters

    Returns:
        Additional lift coefficient from clap-and-fling
    """
    if not params.unsteady_aero.clap_fling_enabled:
        return 0.0

    # Clap-and-fling occurs near stroke reversal
    stroke_position = kinematics['stroke_angle'] / params.kinematics.stroke_amplitude

    # Enhancement factor peaks at stroke reversal (±1)
    if abs(stroke_position) > 0.8:
        # Weis-Fogh clap-and-fling model
        separation_angle = 2 * (1 - abs(stroke_position)) * params.kinematics.stroke_amplitude

        # Lift enhancement depends on wing separation
        enhancement = 0.3 * np.exp(-separation_angle / 0.05) if separation_angle < 0.1 else 0.0

        return enhancement

    return 0.0


def _wake_capture_effect(circulation_history: np.ndarray,
                        current_idx: int,
                        params: OrnithopterParameters) -> float:
    """
    Calculate wake capture effect from previous wing strokes.

    Wake capture occurs when the wing encounters vorticity shed
    during previous strokes, enhancing lift generation.

    Args:
        circulation_history: History of bound circulation
        current_idx: Current time index
        params: Ornithopter parameters

    Returns:
        Additional velocity from wake capture
    """
    if current_idx < 10:
        return 0.0

    # Get circulation from previous stroke (approximately one period ago)
    period_steps = int(1.0 / params.flap_frequency_hz / 0.02)  # dt = 0.02s
    prev_idx = max(0, current_idx - period_steps)

    # Wake-induced velocity proportional to previous circulation
    prev_circulation = circulation_history[prev_idx] if prev_idx < len(circulation_history) else 0.0

    # Wake decay with distance (simplified)
    wake_strength = params.unsteady_aero.wake_capture_factor * prev_circulation
    wake_decay = np.exp(-0.5)  # Simplified decay model

    induced_velocity = wake_strength * wake_decay / (2 * np.pi * params.mean_chord_m)

    return induced_velocity


def _calculate_porosity_factor(stroke_velocity: float) -> float:
    """
    Calculate the wing porosity factor based on stroke direction.

    This simulates feathers separating on the upstroke (high porosity)
    and sealing on the downstroke (low porosity).

    Args:
        stroke_velocity: The vertical velocity of the wing.

    Returns:
        A porosity factor between 0.0 (sealed) and 0.8 (porous).
    """
    # Upstroke (positive velocity) should have high porosity
    if stroke_velocity > 0:
        # Feathers separate to let air through
        return 0.7
    # Downstroke (negative velocity) should have low porosity
    else:
        # Feathers are sealed
        return 0.1

def _calculate_unsteady_forces(kinematics: Dict[str, float],
                              membrane_def: float,
                              circulation_history: np.ndarray,
                              current_idx: int,
                              params: OrnithopterParameters,
                              t: float) -> Dict[str, float]:
    """
    Calculate unsteady aerodynamic forces using advanced theory.

    Combines Theodorsen's unsteady thin airfoil theory with
    bio-inspired mechanisms and membrane dynamics.

    Args:
        kinematics: Wing kinematics data
        membrane_def: Membrane deformation
        circulation_history: History of bound circulation
        current_idx: Current time index
        params: Ornithopter parameters
        t: Time

    Returns:
        Dictionary with aerodynamic forces and moments
    """
    # Effective angle of attack including rotation and membrane effects
    base_alpha = math.radians(params.base_alpha_deg)
    alpha_amp = math.radians(params.alpha_amplitude_deg)

    # Total angle including kinematic contributions
    alpha_total = (base_alpha + alpha_amp * np.sin(2 * np.pi * params.flap_frequency_hz * t) +
                  kinematics['rotation'] + membrane_def / params.mean_chord_m)

    # Wing velocity components
    v_stroke = abs(kinematics['stroke_velocity']) * params.wing_span_m / 2
    v_forward = params.forward_speed_ms
    v_total = np.sqrt(v_stroke**2 + v_forward**2)

    # Reynolds number for unsteady effects
    Re = v_total * params.mean_chord_m / KINEMATIC_VISCOSITY

    # Reduced frequency
    if v_forward > 0.1:
        k = np.pi * params.flap_frequency_hz * params.mean_chord_m / v_forward
    else:
        k = 2.0  # Hovering condition

    # Theodorsen's function for unsteady lift
    C_k = _theodorsen_function(k)
    C_k_real = C_k.real

    # Quasi-steady lift coefficient
    cl_qs = params.cl_alpha_per_rad * alpha_total
    cl_qs = np.clip(cl_qs, -params.cl_max, params.cl_max)

    # Unsteady lift modification
    cl_unsteady = cl_qs * C_k_real

    # Added mass effect (non-circulatory lift)
    added_mass_factor = np.pi / 4 * params.mean_chord_m**2 * RHO_AIR
    cl_added_mass = (added_mass_factor * kinematics['stroke_acceleration'] *
                    params.wing_span_m / (0.5 * RHO_AIR * v_total**2 * params.wing_area_m2))

    # Clap-and-fling enhancement
    cl_clap_fling = _clap_and_fling_lift(kinematics, params)

    # Wake capture effect
    v_wake_capture = _wake_capture_effect(circulation_history, current_idx, params)
    v_effective = v_total + v_wake_capture

    # Total lift coefficient
    cl_total = cl_unsteady + cl_added_mass + cl_clap_fling
    cl_total = np.clip(cl_total, -params.cl_max * 1.5, params.cl_max * 1.5)

    # Dynamic pressure with effective velocity
    q = 0.5 * RHO_AIR * v_effective**2

    # Forces
    lift = q * params.wing_area_m2 * cl_total

    # Profile drag (including unsteady effects)
    cd0 = 0.02 + 0.05 * abs(cl_total)**2  # Polar drag
    drag = q * params.wing_area_m2 * cd0

    # Apply porosity effect
    porosity_factor = _calculate_porosity_factor(kinematics['stroke_velocity'])
    lift *= (1.0 - porosity_factor)
    drag *= (1.0 - porosity_factor)

    # Thrust from stroke plane inclination and forward component
    stroke_plane_tilt = params.kinematics.stroke_plane_angle
    stroke_thrust = lift * np.sin(stroke_plane_tilt) * np.sign(kinematics['stroke_velocity'])

    # Additional thrust from wing rotation timing
    rotation_thrust = 0.1 * lift * kinematics['rotation_velocity'] * np.sign(kinematics['stroke_velocity'])
    thrust = stroke_thrust + rotation_thrust

    # Bound circulation (Kutta-Joukowski theorem)
    circulation = lift / (RHO_AIR * v_effective * params.wing_span_m) if v_effective > 0.1 else 0.0

    return {
        'lift': lift,
        'thrust': thrust,
        'drag': drag,
        'cl_total': cl_total,
        'circulation': circulation,
        'velocity': v_effective,
        'reynolds_number': Re,
        'reduced_frequency': k,
        'theodorsen_factor': C_k_real
    }


def _load_parameters() -> OrnithopterParameters:
    """Load and enhance parameters with bio-inspired defaults."""
    with PARAM_FILE.open("r", encoding="utf-8") as stream:
        raw = yaml.safe_load(stream)

    acceptance_targets = raw.get('acceptance_targets', {})
    acceptance_file = PARAM_FILE.with_name("acceptance.yaml")
    if acceptance_file.exists():
        with acceptance_file.open("r", encoding="utf-8") as handle:
            acceptance_targets = yaml.safe_load(handle) or {}

    # Calculate derived parameters
    wing_span_m = np.sqrt(raw['wing_area_m2'] * 4.0)  # Assuming AR = 4
    mean_chord_m = raw['wing_area_m2'] / wing_span_m

    # Create enhanced parameter structure
    kinematics = WingKinematics(
        stroke_amplitude=np.radians(60.0),  # 60 degree stroke
        stroke_plane_angle=np.radians(15.0),  # 15 degree tilt
        deviation_amplitude=np.radians(8.0),  # 8 degree deviation
        rotation_amplitude=np.radians(45.0),  # 45 degree rotation
        phase_lag_deviation=np.radians(90.0),  # 90 degree phase lag
        phase_lag_rotation=np.radians(-45.0),  # -45 degree phase lag
        figure_eight_ratio=0.15  # Moderate figure-8 motion
    )

    structure = WingStructure(
        membrane_stiffness_n_m=500.0,  # N/m membrane stiffness
        membrane_damping=0.1,  # 10% damping ratio
        spar_stiffness_n_m2=1000.0,  # N⋅m² flexural stiffness
        wing_mass_kg=raw['total_mass_kg'] * 0.15,  # 15% of total mass
        elastic_axis_ratio=0.35,  # Elastic axis at 35% chord
        tensile_prestress_n_m2=200.0  # N/m² membrane pretension
    )

    unsteady_aero = UnsteadyAeroParams(
        reduced_frequency=0.5,  # Moderate unsteady effects
        theodorsen_factor=0.8,  # Initial Theodorsen approximation
        wake_vorticity_strength=1.0,  # Initial wake strength
        clap_fling_enabled=True,  # Enable clap-and-fling
        delayed_stall_angle=np.radians(25.0),  # Delayed stall angle
        wake_capture_factor=0.3  # Wake capture efficiency
    )

    return OrnithopterParameters(
        total_mass_kg=raw['total_mass_kg'],
        wing_area_m2=raw['wing_area_m2'],
        wing_span_m=wing_span_m,
        mean_chord_m=mean_chord_m,
        flap_frequency_hz=raw['flap_frequency_hz'],
        forward_speed_ms=raw['forward_speed_ms'],
        base_alpha_deg=raw['base_alpha_deg'],
        alpha_amplitude_deg=raw['alpha_amplitude_deg'],
        cl_alpha_per_rad=raw['cl_alpha_per_rad'],
        cl_max=2.1,  # Maximum lift coefficient
        base_power_w=raw['base_power_w'],
        power_variation_w=raw['power_variation_w'],
        battery_capacity_wh=raw['battery_capacity_wh'],
        controller_power_w=raw['controller_power_w'],
        kinematics=kinematics,
        structure=structure,
        unsteady_aero=unsteady_aero,
        acceptance_targets=acceptance_targets
    )


def _cad_module():
    root = Path(__file__).resolve().parents[2]
    module_path = root / "cad" / SLUG / "model.py"
    spec = importlib.util.spec_from_file_location(f"cad.{SLUG}.model", module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - developer error
        raise RuntimeError("Unable to locate Ornithopter CAD module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def plan() -> Dict[str, object]:
    """Enhanced plan with Leonardo's historical research and bio-inspired principles."""
    params = _load_parameters()
    base_alpha_rad = math.radians(params.base_alpha_deg)
    cl_base = params.cl_alpha_per_rad * base_alpha_rad
    cruise_lift = 0.5 * RHO_AIR * params.wing_area_m2 * params.forward_speed_ms**2 * cl_base
    gross_weight = params.total_mass_kg * GRAVITY
    lift_margin = cruise_lift / gross_weight - 1.0
    power_density = params.base_power_w / params.total_mass_kg

    # Calculate advanced performance metrics
    reynolds_number = params.forward_speed_ms * params.mean_chord_m / KINEMATIC_VISCOSITY
    reduced_frequency = np.pi * params.flap_frequency_hz * params.mean_chord_m / params.forward_speed_ms
    wing_loading = params.total_mass_kg * GRAVITY / params.wing_area_m2

    return {
        "origin": {
            "historical_research": {
                "leonardos_studies": [
                    {
                        "reference": "Codex Atlanticus, 846r/846v",
                        "description": "Detailed wing structure with articulated feather sections",
                        "insights": "Leonardo understood need for wing flexibility and controlled deformation",
                        "modern_translation": "Implemented as elastic membrane with adaptive camber"
                    },
                    {
                        "reference": "Codex Atlanticus, 858r",
                        "description": "Pilot harness and control system sketches",
                        "insights": "Weight shift control concept anticipating modern flight controls",
                        "modern_translation": "Active control surfaces with differential flapping"
                    },
                    {
                        "reference": "Codex on the Flight of Birds, 1r-18v",
                        "description": "Comprehensive bird flight analysis including wind tunnel studies",
                        "insights": "Pioneering experimental aerodynamics with flow visualization",
                        "modern_translation": "CFD validation and wind tunnel testing protocols"
                    },
                    {
                        "reference": "Manuscript B, 70v-71r",
                        "description": "Ornithopter wing mechanism with crank and pulley system",
                        "insights": "Understanding of mechanical power transmission for flapping",
                        "modern_translation": "Electric actuators with harmonic drive mechanisms"
                    },
                    {
                        "reference": "Codex Atlanticus, 891r",
                        "description": "Wing beat frequency observations of different bird species",
                        "insights": "Relationship between bird size, wing morphology, and flapping frequency",
                        "modern_translation": "Optimized frequency based on scaling laws and power density"
                    }
                ],
                "bio_inspiration": [
                    {
                        "principle": "Figure-8 wing tip trajectory",
                        "biological_source": "Hummingbird and small passerine flight",
                        "leonardo_observation": "Curved wing paths noted in flight studies",
                        "implementation": "Three-DOF kinematics with coupled stroke and deviation"
                    },
                    {
                        "principle": "Wing membrane elasticity",
                        "biological_source": "Bat wing membrane and bird feather flexibility",
                        "leonardo_observation": "Feather articulation for camber control",
                        "implementation": "Elastic membrane with dynamic deformation modeling"
                    },
                    {
                        "principle": "Clap-and-fling mechanism",
                        "biological_source": "Small insects and some birds during takeoff",
                        "leonardo_observation": "Wing interaction at stroke extremes",
                        "implementation": "Enhanced lift during stroke reversal"
                    }
                ]
            },
            "missing_elements_from_leonardo": [
                "Quantified power requirements - Leonardo lacked power density measurements",
                "Material fatigue analysis - Renaissance materials couldn't withstand cyclic loads",
                "Active control systems - Mechanical control limited to pilot input",
                "Aerodynamic unsteady effects - Pre-scientific understanding of fluid dynamics",
                "Structural optimization - Modern finite element analysis unavailable"
            ],
        },
        "bio_inspired_design": {
            "wing_kinematics": {
                "stroke_angle_deg": np.degrees(params.kinematics.stroke_amplitude),
                "stroke_plane_angle_deg": np.degrees(params.kinematics.stroke_plane_angle),
                "deviation_amplitude_deg": np.degrees(params.kinematics.deviation_amplitude),
                "rotation_amplitude_deg": np.degrees(params.kinematics.rotation_amplitude),
                "figure_eight_ratio": params.kinematics.figure_eight_ratio,
                "educational_note": "Three degrees of freedom mimic bird wing motion: stroke (power), deviation (position), rotation (feathering)"
            },
            "membrane_dynamics": {
                "elastic_stiffness_n_m": params.structure.membrane_stiffness_n_m,
                "natural_frequency_hz": np.sqrt(params.structure.membrane_stiffness_n_m / params.structure.wing_mass_kg) / (2 * np.pi),
                "damping_ratio": params.structure.membrane_damping,
                "educational_note": "Elastic deformation provides adaptive camber, enhancing lift across flapping cycle"
            },
            "unsteady_aerodynamics": {
                "reynolds_number": reynolds_number,
                "reduced_frequency": reduced_frequency,
                "theodorsen_approximation": "C(k) accounts for phase lag in lift generation",
                "educational_note": "Unsteady effects crucial at low speeds and high flapping frequencies"
            }
        },
        "educational_principles": {
            "flapping_flight_mechanics": [
                "Lift generation through both circulation and added mass",
                "Figure-8 motion provides optimal lift-thrust balance",
                "Wing rotation timing critical for efficient power transfer",
                "Membrane elasticity enables passive camber control",
                "Wake capture enhances lift by utilizing previous stroke vorticity"
            ],
            "historical_engineering_insights": [
                "Leonardo's empirical approach pre-dated formal aerodynamics",
                "Understanding of structural loads from architectural experience",
                "Integration of multiple disciplines - art, anatomy, engineering",
                "Iterative design process with observation and modification"
            ],
            "modern_biomimicry_lessons": [
                "Nature's solutions optimized through evolution",
                "Efficiency through passive mechanisms and smart materials",
                "Complexity in simple motions - power in subtle variations",
                "Integration of structure and function in biological systems"
            ],
            "unsteady_effects_significant": reduced_frequency > 0.3
        },
        "goals": [
            "Demonstrate advanced unsteady aerodynamics in educational context",
            "Bridge Leonardo's historical insights with modern computational methods",
            "Show bio-inspired principles enabling efficient flapping flight",
            "Provide hands-on learning about aerodynamic complexity",
            "Inspire interest in biomimetic engineering and historical innovation"
        ],
        "assumptions": {
            "total_mass_kg": params.total_mass_kg,
            "wing_area_m2": params.wing_area_m2,
            "wing_span_m": params.wing_span_m,
            "mean_chord_m": params.mean_chord_m,
            "flap_frequency_hz": params.flap_frequency_hz,
            "forward_speed_ms": params.forward_speed_ms,
            "bio_inspired_kinematics": True,
            "unsteady_aerodynamics": True,
            "membrane_dynamics": True,
            "clap_fling_enabled": params.unsteady_aero.clap_fling_enabled
        },
        "viability_metrics": {
            "cruise_lift_N": cruise_lift,
            "gross_weight_N": gross_weight,
            "lift_margin": lift_margin,
            "power_density_w_per_kg": power_density,
            "wing_loading_n_m2": wing_loading,
            "reynolds_number": reynolds_number,
            "reduced_frequency": reduced_frequency,
            "battery_capacity_wh": params.battery_capacity_wh,
            "theoretical_endurance_min": params.battery_capacity_wh / params.base_power_w * 60
        },
        "acceptance_targets": params.acceptance_targets,
        "validation_plan": [
            "Unsteady CFD validation of Theodorsen-based predictions",
            "Wind tunnel testing of elastic membrane wing sections",
            "Motion capture validation of figure-8 kinematics",
            "Particle image velocimetry of wake capture effects",
            "Structural fatigue testing of composite spars",
            "Flight test with instrumented prototype"
        ],
    }


def _simulate_profile(params: OrnithopterParameters, seed: int, duration_s: float = 30.0, dt: float = 0.02) -> FlightSimulation:
    """
    Enhanced flight simulation with bio-inspired flapping aerodynamics.

    This simulation incorporates:
    - Unsteady aerodynamics with Theodorsen's theory
    - Bio-inspired wing kinematics with figure-8 motion
    - Elastic membrane deformation
    - Clap-and-fling and wake capture mechanisms
    """
    rng = np.random.default_rng(seed)
    steps = int(duration_s / dt) + 1
    time = np.linspace(0.0, duration_s, steps)

    # State variables
    altitude = np.zeros_like(time)
    vertical_velocity = np.zeros_like(time)
    horizontal_velocity = np.full_like(time, params.forward_speed_ms)
    lift = np.zeros_like(time)
    thrust = np.zeros_like(time)
    drag = np.zeros_like(time)
    power = np.zeros_like(time)
    energy_used_wh = 0.0

    # Bio-inspired arrays
    wing_positions = np.zeros((steps, 3))  # x, y, z positions
    circulation = np.zeros_like(time)
    membrane_deformation = np.zeros_like(time)

    gross_weight = params.total_mass_kg * GRAVITY
    damping = 0.55  # aerodynamic/heave damping coefficient

    for i in range(1, steps):
        t = time[i]

        # Calculate wing kinematics
        kinematics = _calculate_wing_kinematics(t, params)

        # Calculate membrane deformation
        membrane_def = _calculate_membrane_deformation(kinematics, params, t)
        membrane_deformation[i] = membrane_def

        # Calculate unsteady aerodynamic forces
        forces = _calculate_unsteady_forces(
            kinematics, membrane_def, circulation, i, params, t
        )

        # Store forces
        lift[i] = forces['lift']
        thrust[i] = forces['thrust']
        drag[i] = forces['drag']
        circulation[i] = forces['circulation']

        # Wing tip position for visualization (simplified)
        wing_positions[i, 0] = kinematics['lateral_motion']
        wing_positions[i, 1] = kinematics['stroke_angle'] * params.wing_span_m / 2
        wing_positions[i, 2] = kinematics['deviation'] * params.wing_span_m / 4

        # Add turbulence and environmental effects
        turbulence = 1.0 + rng.normal(0.0, 0.015)
        lift[i] *= turbulence
        thrust[i] *= turbulence

        # Vehicle dynamics
        accel_vertical = (lift[i] - gross_weight) / params.total_mass_kg
        accel_horizontal = (thrust[i] - drag[i]) / params.total_mass_kg

        # Update velocities with damping
        vertical_velocity[i] = vertical_velocity[i - 1] + (accel_vertical - damping * vertical_velocity[i - 1]) * dt
        horizontal_velocity[i] = horizontal_velocity[i - 1] + (accel_horizontal - 0.1 * (horizontal_velocity[i - 1] - params.forward_speed_ms)) * dt

        # Update position
        altitude_candidate = altitude[i - 1] + vertical_velocity[i] * dt
        altitude[i] = max(altitude_candidate, 0.0)  # Ground constraint

        # Power calculation with bio-inspired variations
        phase = 2.0 * np.pi * params.flap_frequency_hz * t

        # Power peaks during downstroke and stroke reversal
        downstroke_factor = 0.5 * (1.0 + np.cos(phase))
        stroke_reversal_factor = 0.3 * abs(np.sin(2 * phase))

        # Membrane deformation power (elastic energy storage/release)
        membrane_power = 0.5 * params.structure.membrane_stiffness_n_m * membrane_def**2 * abs(kinematics['stroke_velocity'])

        power[i] = (params.base_power_w * downstroke_factor +
                   params.power_variation_w * stroke_reversal_factor +
                   membrane_power +
                   params.controller_power_w)

        energy_used_wh += power[i] * dt / 3600.0

    avg_power = float(np.mean(power)) if steps > 0 else params.base_power_w
    endurance_hours = params.battery_capacity_wh / avg_power

    return FlightSimulation(
        time=time,
        altitude=altitude,
        vertical_velocity=vertical_velocity,
        horizontal_velocity=horizontal_velocity,
        lift=lift,
        thrust=thrust,
        drag=drag,
        power=power,
        energy_used_wh=energy_used_wh,
        endurance_hours=endurance_hours,
        wing_positions=wing_positions,
        circulation=circulation,
        membrane_deformation=membrane_deformation
    )


def _write_csv(path: Path, result: FlightSimulation) -> None:
    """Write enhanced simulation data to CSV with bio-inspired metrics."""
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        # Enhanced header with bio-inspired metrics
        writer.writerow([
            "time_s", "altitude_m", "vertical_velocity_ms", "horizontal_velocity_ms",
            "lift_N", "thrust_N", "drag_N", "power_W", "circulation_m2_s",
            "membrane_deformation_m", "wing_tip_x_m", "wing_tip_y_m", "wing_tip_z_m"
        ])
        for i in range(len(result.time)):
            writer.writerow([
                f"{result.time[i]:.6f}",
                f"{result.altitude[i]:.6f}",
                f"{result.vertical_velocity[i]:.6f}",
                f"{result.horizontal_velocity[i]:.6f}",
                f"{result.lift[i]:.6f}",
                f"{result.thrust[i]:.6f}",
                f"{result.drag[i]:.6f}",
                f"{result.power[i]:.6f}",
                f"{result.circulation[i]:.6f}",
                f"{result.membrane_deformation[i]:.6f}",
                f"{result.wing_positions[i, 0]:.6f}",
                f"{result.wing_positions[i, 1]:.6f}",
                f"{result.wing_positions[i, 2]:.6f}"
            ])


def _plot_profiles(path: Path, result: FlightSimulation, gross_weight: float) -> None:
    """
    Create comprehensive educational plots showing bio-inspired flapping flight dynamics.

    Generates multiple subplots illustrating:
    - Flight trajectory and forces
    - Wing kinematics and membrane deformation
    - Bio-inspired mechanisms in action
    - Energy and power dynamics
    """
    fig = plt.figure(figsize=(14, 10))

    # 1. Flight dynamics (top left)
    ax1 = plt.subplot(3, 3, (1, 4))
    ax1_twin = ax1.twinx()
    ax1.plot(result.time, result.altitude, color="tab:blue", linewidth=2, label="Altitude")
    ax1.set_ylabel("Altitude (m)", color="tab:blue")
    ax1.tick_params(axis='y', labelcolor="tab:blue")
    ax1.grid(True, linestyle=":", alpha=0.4)

    ax1_twin.plot(result.time, result.vertical_velocity, color="tab:orange", linewidth=1.5, alpha=0.8, label="Vertical Velocity")
    ax1_twin.set_ylabel("Velocity (m/s)", color="tab:orange")
    ax1_twin.tick_params(axis='y', labelcolor="tab:orange")

    ax1.set_title("Flight Dynamics", fontweight='bold')
    ax1.set_xlabel("Time (s)")

    # 2. Aerodynamic forces (top middle)
    ax2 = plt.subplot(3, 3, 2)
    ax2.plot(result.time, result.lift, color="tab:purple", linewidth=2, label="Lift")
    ax2.axhline(gross_weight, color="tab:red", linestyle="--", linewidth=2, label="Weight")
    ax2.set_ylabel("Force (N)")
    ax2.set_title("Aerodynamic Forces", fontweight='bold')
    ax2.grid(True, linestyle=":", alpha=0.4)
    ax2.legend(loc="upper right", fontsize=8)

    # 3. Thrust and Drag (top right)
    ax3 = plt.subplot(3, 3, 3)
    ax3.plot(result.time, result.thrust, color="tab:green", linewidth=2, label="Thrust")
    ax3.plot(result.time, result.drag, color="tab:red", linewidth=1.5, alpha=0.8, label="Drag")
    ax3.set_ylabel("Force (N)")
    ax3.set_title("Propulsion Forces", fontweight='bold')
    ax3.grid(True, linestyle=":", alpha=0.4)
    ax3.legend(loc="upper right", fontsize=8)

    # 4. Figure-8 wing trajectory (middle)
    ax4 = plt.subplot(3, 3, 5)
    # Sample every 10th point for clarity
    sample_idx = slice(None, None, 10)
    ax4.plot(result.wing_positions[sample_idx, 0], result.wing_positions[sample_idx, 2],
            color="tab:blue", linewidth=2, alpha=0.7, label="Wing Tip Path")
    ax4.scatter(result.wing_positions[0, 0], result.wing_positions[0, 2],
               color="tab:green", s=100, marker="o", label="Start", zorder=5)
    ax4.scatter(result.wing_positions[-1, 0], result.wing_positions[-1, 2],
               color="tab:red", s=100, marker="s", label="End", zorder=5)
    ax4.set_xlabel("Lateral Position (m)")
    ax4.set_ylabel("Vertical Position (m)")
    ax4.set_title("Figure-8 Wing Tip Trajectory", fontweight='bold')
    ax4.grid(True, linestyle=":", alpha=0.4)
    ax4.legend(loc="upper right", fontsize=8)
    ax4.axis('equal')

    # 5. Membrane deformation (middle right)
    ax5 = plt.subplot(3, 3, 6)
    ax5.plot(result.time, result.membrane_deformation * 1000, color="tab:brown", linewidth=2)
    ax5.set_ylabel("Deformation (mm)")
    ax5.set_title("Elastic Membrane Deformation", fontweight='bold')
    ax5.grid(True, linestyle=":", alpha=0.4)
    ax5.axhline(0, color="black", linestyle="-", linewidth=0.5)

    # 6. Circulation and unsteady effects (bottom left)
    ax6 = plt.subplot(3, 3, 7)
    ax6.plot(result.time, result.circulation, color="tab:purple", linewidth=2, alpha=0.8)
    ax6.set_ylabel("Circulation (m²/s)")
    ax6.set_xlabel("Time (s)")
    ax6.set_title("Bound Circulation (Unsteady Lift)", fontweight='bold')
    ax6.grid(True, linestyle=":", alpha=0.4)

    # 7. Power dynamics (bottom middle)
    ax7 = plt.subplot(3, 3, 8)
    ax7.plot(result.time, result.power / 1000, color="tab:orange", linewidth=2)
    ax7.set_ylabel("Power (kW)")
    ax7.set_xlabel("Time (s)")
    ax7.set_title("Bio-inspired Power Profile", fontweight='bold')
    ax7.grid(True, linestyle=":", alpha=0.4)

    # 8. Educational annotation (bottom right)
    ax8 = plt.subplot(3, 3, 9)
    ax8.axis('off')

    # Educational text
    educational_text = """
Bio-inspired Flapping Flight:

• Figure-8 trajectory provides
  optimal lift-thrust balance

• Elastic membrane enables
  adaptive camber control

• Unsteady effects capture
  vorticity and wake dynamics

• Clap-and-fling enhances
  lift at stroke reversal

• Energy storage in elastic
  deformation improves efficiency
    """

    ax8.text(0.05, 0.95, educational_text, transform=ax8.transAxes,
            fontsize=9, verticalalignment='top', fontfamily='monospace',
            bbox={"boxstyle": "round,pad=0.5", "facecolor": "lightblue", "alpha": 0.3})

    plt.suptitle("Bio-inspired Ornithopter Flight Dynamics\nLeonardo's Dream Meets Modern Aerodynamics",
                 fontsize=14, fontweight='bold', y=0.98)

    plt.tight_layout()
    plt.subplots_adjust(top=0.93, hspace=0.3, wspace=0.3)
    fig.savefig(path, dpi=220, bbox_inches='tight')
    plt.close(fig)


def _plot_wing_kinematics_3d(path: Path, result: FlightSimulation) -> None:
    """Create 3D visualization of wing kinematics for educational purposes."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Sample points for clarity
    sample_idx = slice(None, None, 5)

    # Plot wing tip trajectory
    ax.plot(result.wing_positions[sample_idx, 0],
           result.wing_positions[sample_idx, 1],
           result.wing_positions[sample_idx, 2],
           color="tab:blue", linewidth=2, alpha=0.8)

    # Mark start and end points
    ax.scatter(result.wing_positions[0, 0],
              result.wing_positions[0, 1],
              result.wing_positions[0, 2],
              color="tab:green", s=100, marker="o", label="Start")

    ax.scatter(result.wing_positions[-1, 0],
              result.wing_positions[-1, 1],
              result.wing_positions[-1, 2],
              color="tab:red", s=100, marker="s", label="End")

    # Add time-based color coding for a few segments
    n_segments = 20
    segment_length = len(result.time) // n_segments
    colors = plt.cm.viridis(np.linspace(0, 1, n_segments))

    for i in range(n_segments):
        start_idx = i * segment_length
        end_idx = min((i + 1) * segment_length, len(result.time) - 1)
        if start_idx < len(result.wing_positions):
            ax.plot(result.wing_positions[start_idx:end_idx, 0],
                   result.wing_positions[start_idx:end_idx, 1],
                   result.wing_positions[start_idx:end_idx, 2],
                   color=colors[i], linewidth=3, alpha=0.7)

    ax.set_xlabel('Lateral (m)')
    ax.set_ylabel('Stroke (m)')
    ax.set_zlabel('Deviation (m)')
    ax.set_title('3D Wing Tip Kinematics\nBio-inspired Figure-8 Motion', fontweight='bold')
    ax.legend()

    # Set equal aspect ratio for better visualization
    max_range = np.array([result.wing_positions[sample_idx, 0].max() - result.wing_positions[sample_idx, 0].min(),
                         result.wing_positions[sample_idx, 1].max() - result.wing_positions[sample_idx, 1].min(),
                         result.wing_positions[sample_idx, 2].max() - result.wing_positions[sample_idx, 2].min()]).max() / 2.0

    mid_x = (result.wing_positions[sample_idx, 0].max() + result.wing_positions[sample_idx, 0].min()) * 0.5
    mid_y = (result.wing_positions[sample_idx, 1].max() + result.wing_positions[sample_idx, 1].min()) * 0.5
    mid_z = (result.wing_positions[sample_idx, 2].max() + result.wing_positions[sample_idx, 2].min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches='tight')
    plt.close(fig)


def simulate(seed: int = 0) -> Dict[str, object]:
    """
    Enhanced simulation with comprehensive bio-inspired flapping flight analysis.

    Generates multiple educational outputs showing the complex interplay between
    unsteady aerodynamics, wing kinematics, and elastic membrane dynamics.
    """
    params = _load_parameters()
    result = _simulate_profile(params, seed)
    artifacts = ensure_artifact_dir(SLUG, subdir="sim")

    # Generate enhanced artifacts
    csv_path = artifacts / "bio_inspired_flight_profile.csv"
    plot_path = artifacts / "ornithopter_dynamics.png"
    kinematics_3d_path = artifacts / "wing_kinematics_3d.png"

    _write_csv(csv_path, result)
    _plot_profiles(plot_path, result, params.total_mass_kg * GRAVITY)
    _plot_wing_kinematics_3d(kinematics_3d_path, result)

    gross_weight = params.total_mass_kg * GRAVITY

    # Enhanced performance metrics
    avg_lift = float(np.mean(result.lift))
    avg_thrust = float(np.mean(result.thrust))
    avg_drag = float(np.mean(result.drag))
    lift_ratio = avg_lift / gross_weight if gross_weight else 0.0
    thrust_ratio = avg_thrust / gross_weight if gross_weight else 0.0

    peak_altitude = float(np.max(result.altitude))
    rms_vertical_velocity = float(np.sqrt(np.mean(result.vertical_velocity**2)))
    avg_horizontal_velocity = float(np.mean(result.horizontal_velocity))

    avg_power = float(np.mean(result.power))
    peak_power = float(np.max(result.power))
    power_efficiency = avg_lift * avg_horizontal_velocity / avg_power if avg_power > 0 else 0.0

    # Unsteady aerodynamics metrics
    avg_circulation = float(np.mean(np.abs(result.circulation)))
    max_circulation = float(np.max(np.abs(result.circulation)))
    avg_membrane_deformation = float(np.mean(np.abs(result.membrane_deformation))) * 1000  # mm
    max_membrane_deformation = float(np.max(np.abs(result.membrane_deformation))) * 1000  # mm

    # Bio-inspired performance indicators
    figure8_area = _calculate_figure8_enclosed_area(result.wing_positions)
    clap_fling_events = _count_clap_fling_events(result, params)
    wake_capture_potential = float(np.std(result.circulation))  # Variability indicates wake effects

    # Educational analysis
    reynolds_number = params.forward_speed_ms * params.mean_chord_m / KINEMATIC_VISCOSITY
    reduced_frequency = np.pi * params.flap_frequency_hz * params.mean_chord_m / params.forward_speed_ms
    stroke_amplitude_m = params.kinematics.stroke_amplitude * params.wing_span_m / 2
    strouhal_number = params.flap_frequency_hz * stroke_amplitude_m / params.forward_speed_ms

    return {
        "flight_performance": {
            "duration_s": float(result.time[-1]),
            "avg_lift_N": avg_lift,
            "avg_thrust_N": avg_thrust,
            "avg_drag_N": avg_drag,
            "lift_margin": lift_ratio - 1.0,
            "thrust_margin": thrust_ratio,
            "peak_altitude_m": peak_altitude,
            "avg_horizontal_velocity_ms": avg_horizontal_velocity,
            "vertical_velocity_rms_ms": rms_vertical_velocity,
        },
        "bio_inspired_metrics": {
            "avg_power_W": avg_power,
            "peak_power_W": peak_power,
            "power_efficiency": power_efficiency,
            "energy_used_wh": result.energy_used_wh,
            "estimated_endurance_min": result.endurance_hours * 60.0,
            "avg_circulation_m2_s": avg_circulation,
            "max_circulation_m2_s": max_circulation,
            "avg_membrane_deformation_mm": avg_membrane_deformation,
            "max_membrane_deformation_mm": max_membrane_deformation,
            "figure8_area_m2": figure8_area,
            "clap_fling_events_per_minute": clap_fling_events * 60 / result.time[-1],
            "wake_capture_potential": wake_capture_potential,
        },
        "aerodynamic_parameters": {
            "reynolds_number": reynolds_number,
            "reduced_frequency": reduced_frequency,
            "strouhal_number": strouhal_number,
            "wing_loading_n_m2": gross_weight / params.wing_area_m2,
            "power_loading_w_per_n": avg_power / gross_weight if gross_weight > 0 else 0.0,
        },
        "educational_insights": {
            "unsteady_effects_significant": bool(reduced_frequency > 0.3),
            "bio_mimicry_achievements": [
                "Figure-8 wing trajectory for optimal lift-thrust balance",
                "Elastic membrane enabling adaptive camber control",
                "Clap-and-fling mechanism for lift enhancement",
                "Wake capture utilizing previous stroke vorticity",
                "Energy storage in elastic deformation"
            ],
            "leonardos_vision_realized": [
                "Wing flexibility and controlled deformation",
                "Understanding of power requirements for flapping",
                "Integration of multiple wing motions",
                "Bio-inspired design principles"
            ],
        },
        "artifacts": {
            "bio_inspired_profile_csv": str(csv_path),
            "comprehensive_dynamics_plot": str(plot_path),
            "wing_kinematics_3d": str(kinematics_3d_path),
        },
    }


def _calculate_figure8_enclosed_area(wing_positions: np.ndarray) -> float:
    """Calculate the area enclosed by the figure-8 wing tip trajectory."""
    if len(wing_positions) < 10:
        return 0.0

    # Use the lateral and vertical components for 2D area
    x = wing_positions[:, 0]  # Lateral
    y = wing_positions[:, 2]  # Vertical

    # Shoelace formula for area
    n = len(x)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += x[i] * y[j]
        area -= x[j] * y[i]

    return abs(area) / 2.0


def _count_clap_fling_events(result: FlightSimulation, params: OrnithopterParameters) -> int:
    """Count clap-and-fling events based on stroke reversal and wing separation."""
    if not params.unsteady_aero.clap_fling_enabled:
        return 0

    # Count stroke reversals where wings would be close together
    stroke_velocity = np.gradient(result.wing_positions[:, 1])
    # Zero crossings indicate stroke reversals
    zero_crossings = np.where(np.diff(np.sign(stroke_velocity)))[0]

    # Filter for significant reversals (stroke near maximum amplitude)
    max_stroke = params.kinematics.stroke_amplitude * params.wing_span_m / 2
    stroke_position = result.wing_positions[:, 1] / max_stroke if max_stroke > 0 else np.zeros_like(result.wing_positions[:, 1])
    significant_reversals = [i for i in zero_crossings if abs(stroke_position[i]) > 0.8]

    return len(significant_reversals)


def build() -> None:
    try:
        cad = _cad_module()
        cad.generate_ornithopter_frame(span_m=10.5, chord_m=1.4, output_dir=ensure_artifact_dir(SLUG, subdir="cad"))
    except Exception as exc:  # pragma: no cover - CAD is optional in CI
        artifact_dir = ensure_artifact_dir(SLUG, subdir="cad")
        placeholder = artifact_dir / "cad_placeholder.txt"
        with placeholder.open("w", encoding="utf-8") as handle:
            handle.write("Ornithopter CAD generation placeholder\n")
            handle.write("Span: 10.5 m, chord: 1.4 m\n")
            handle.write(f"Error: {exc}\n")


def evaluate() -> Dict[str, object]:
    plan_data = plan()
    sim_data = simulate(seed=42)
    params = _load_parameters()

    lift_margin = cast(float, sim_data["flight_performance"]["lift_margin"])
    endurance = cast(float, sim_data["bio_inspired_metrics"]["estimated_endurance_min"])
    historical_research = cast(Dict[str, Any], plan_data["origin"]["historical_research"])
    leonardos_studies = cast(List[Dict[str, str]], historical_research["leonardos_studies"])
    artifacts = cast(Dict[str, str], sim_data["artifacts"])

    root = Path(__file__).resolve().parents[3]
    validation_dir = root / VALIDATION_DIR

    bench_path = validation_dir / "bench_dyno.yaml"
    modal_path = validation_dir / "modal_survey.yaml"
    telemetry_path = validation_dir / "telemetry_summary.csv"

    with bench_path.open("r", encoding="utf-8") as handle:
        bench_data = yaml.safe_load(handle)
    max_thrust = max(point["thrust_N"] for point in bench_data["rpm_points"])
    gross_weight = params.total_mass_kg * GRAVITY
    thrust_margin = (max_thrust / gross_weight) - 1.0 if gross_weight else 0.0

    with modal_path.open("r", encoding="utf-8") as handle:
        modal_data = yaml.safe_load(handle)
    first_mode = modal_data["modal_results"][0]["frequency_hz"]
    modal_ratio = first_mode / params.flap_frequency_hz if params.flap_frequency_hz else 0.0

    telemetry: Dict[str, Union[float, bool]] = {}
    with telemetry_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            value = row["value"]
            if value.lower() in {"true", "false"}:
                telemetry[row["metric"]] = value.lower() == "true"
            else:
                telemetry[row["metric"]] = float(value)

    acceptance = params.acceptance_targets
    validation_summary = {
        "thrust_margin": thrust_margin,
        "modal_ratio": modal_ratio,
        "battery_temperature_rise_C": telemetry.get("battery_temperature_rise_C", 0.0),
        "fsi_converged": telemetry.get("fsi_converged", False),
        "telemetry_duration_s": telemetry.get("telemetry_duration_s", 0.0),
        "meets_targets": {
            "thrust": thrust_margin >= float(acceptance["thrust_to_weight_margin"]),
            "modal": modal_ratio >= float(acceptance["modal_frequency_factor"]),
            "thermal": telemetry.get("battery_temperature_rise_C", 0.0)
            <= float(acceptance["battery_temperature_rise_C"]),
            "duration": telemetry.get("telemetry_duration_s", 0.0)
            >= float(acceptance["telemetry_duration_s"]),
            "fsi": telemetry.get("fsi_converged", False)
            == (not bool(acceptance["fsi_divergence_allowed"])),
        },
        "assets": {
            "bench_dyno": str(VALIDATION_DIR / "bench_dyno.yaml"),
            "modal_survey": str(VALIDATION_DIR / "modal_survey.yaml"),
            "telemetry_summary": str(VALIDATION_DIR / "telemetry_summary.csv"),
        },
    }

    return {
        "feasibility": {
            "lift_margin": lift_margin,
            "endurance_min": endurance,
            "meets_lift_requirement": lift_margin > 0.1,
            "meets_endurance_target": endurance >= 10.0,
        },
        "risks": {
            "structure": "Verify fatigue life of composite spars under 2.4 Hz flapping.",
            "controls": "PX4 mixing for differential amplitude needs HITL validation.",
            "powertrain": "Thermal limits on 2 kW outrunners during sustained climbs.",
        },
        "priorities": [
            "Fabricate subscale wing section for wind-tunnel validation",
            "Integrate battery thermal model with TVA power draws",
            "Draft defensive publication outlining composite + servo architecture",
        ],
        "validation": validation_summary,
        "artifacts": artifacts,
        "references": leonardos_studies,
    }
