"""
Advanced Aerodynamics Module for Leonardo's Flying Machines

Implements computational fluid dynamics with emphasis on:
- Low Reynolds number flows (relevant to historical flying machines)
- Unsteady aerodynamics for flapping wing motion
- Vortex dynamics and wake modeling
- Ground effect and atmospheric boundary layer
- Bio-inspired aerodynamic mechanisms
"""

import logging
from typing import Any, Dict, Tuple

import numpy as np
import scipy.sparse as sp

from .core import PhysicsModule, SimulationParameters

logger = logging.getLogger(__name__)


class AerodynamicsModule(PhysicsModule):
    """
    Computational Fluid Dynamics module specialized for Renaissance aerodynamics.

    Features:
    - Panel method for inviscid flow
    - Boundary layer modeling for viscous effects
    - Unsteady wake modeling
    - Flapping wing kinematics
    - Historical atmosphere modeling
    """

    def __init__(self, parameters: SimulationParameters):
        super().__init__("aerodynamics", parameters)

        # Atmospheric conditions (Renaissance period approximation)
        self.air_density = 1.225  # kg/m³ at sea level
        self.air_viscosity = 1.81e-5  # Pa·s
        self.air_temperature = 288.15  # K (15°C)
        self.sound_speed = 343.0  # m/s

        # Numerical parameters
        self.num_panels = 0
        self.num_wake_panels = 0
        self.panel_coordinates = None
        self.panel_normals = None
        self.panel_areas = None
        self.control_points = None

        # Flow solution
        self.panel_strengths = None
        self.wake_strengths = None
        self.velocity_field = None
        self.pressure_field = None

        # Flapping wing parameters
        self.wing_kinematics = None
        self.flapping_amplitude = 0.0
        self.flapping_frequency = 0.0
        self.phase_lag = 0.0

        # Wake modeling
        self.wake_history = []
        self.max_wake_length = 100

        logger.info("Aerodynamics module initialized")

    def initialize(self, geometry, materials, boundary_conditions):
        """Initialize aerodynamic analysis with wing geometry."""

        self.geometry = geometry
        self.boundary_conditions = boundary_conditions

        # Generate panel mesh on wing surface
        self._generate_panel_mesh()

        # Initialize wake
        self._initialize_wake()

        # Set up flapping kinematics if specified
        if 'flapping' in boundary_conditions:
            self._setup_flapping_kinematics(boundary_conditions['flapping'])

        # Initialize flow field
        self._initialize_flow_field()

        self.is_initialized = True
        logger.info(f"Aerodynamics initialized with {self.num_panels} panels")

    def _generate_panel_mesh(self):
        """Generate panel mesh on wing surface using geometry data."""

        # Extract wing geometry (simplified for demonstration)
        if 'wing_geometry' in self.geometry:
            wing_data = self.geometry['wing_geometry']

            # Create panels along wing surface
            chord_panels = wing_data.get('chord_panels', 20)
            span_panels = wing_data.get('span_panels', 30)

            self.num_panels = chord_panels * span_panels

            # Generate panel coordinates (simplified wing)
            wingspan = wing_data.get('wingspan', 12.0)  # meters
            root_chord = wing_data.get('root_chord', 2.0)
            tip_chord = wing_data.get('tip_chord', 1.0)

            # Panel coordinates
            self.panel_coordinates = np.zeros((self.num_panels, 4, 3))  # 4 corners per panel
            self.control_points = np.zeros((self.num_panels, 3))
            self.panel_normals = np.zeros((self.num_panels, 3))
            self.panel_areas = np.zeros(self.num_panels)

            panel_idx = 0
            for i in range(span_panels):
                y_pos = (i / (span_panels - 1)) * wingspan / 2
                chord_length = root_chord + (tip_chord - root_chord) * (2 * y_pos / wingspan)

                for j in range(chord_panels):
                    x_pos = (j / (chord_panels - 1)) * chord_length

                    # Simple NACA-like airfoil shape
                    thickness = 0.12 * chord_length  # 12% thickness
                    camber = self._naca_camber(x_pos / chord_length) * chord_length
                    half_thickness = self._naca_thickness(x_pos / chord_length) * thickness

                    # Panel corners (quad)
                    dx = chord_length / chord_panels / 2
                    dy = wingspan / span_panels / 2

                    # Upper surface
                    z_upper = camber + half_thickness

                    self.panel_coordinates[panel_idx] = np.array([
                        [x_pos - dx, y_pos - dy, z_upper],
                        [x_pos + dx, y_pos - dy, z_upper],
                        [x_pos + dx, y_pos + dy, z_upper],
                        [x_pos - dx, y_pos + dy, z_upper]
                    ])

                    # Control point (panel center)
                    self.control_points[panel_idx] = np.mean(self.panel_coordinates[panel_idx], axis=0)

                    # Panel normal (pointing up for upper surface)
                    self.panel_normals[panel_idx] = np.array([0, 0, 1])

                    # Panel area
                    self.panel_areas[panel_idx] = (2 * dx) * (2 * dy)

                    panel_idx += 1

            logger.info(f"Generated {self.num_panels} panels for wing surface")

    def _naca_camber(self, x):
        """NACA 4-digit series camber line."""
        m = 0.02  # Maximum camber (2%)
        p = 0.4   # Position of maximum camber (40% chord)

        if x <= p:
            return m / (p * p) * (2 * p * x - x * x)
        else:
            return m / ((1 - p) * (1 - p)) * ((1 - 2 * p) + 2 * p * x - x * x)

    def _naca_thickness(self, x):
        """NACA 4-digit series thickness distribution."""
        t = 0.12  # Maximum thickness (12%)
        return t / 0.2 * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x * x +
                         0.2843 * x * x * x - 0.1036 * x * x * x * x)

    def _initialize_wake(self):
        """Initialize wake panel structure."""

        # Wake panels trail from trailing edge
        self.num_wake_panels = self.max_wake_length
        self.wake_coordinates = np.zeros((self.num_wake_panels, 4, 3))
        self.wake_strengths = np.zeros(self.num_wake_panels)

        # Initialize wake as extension of trailing edge
        if self.panel_coordinates is not None:
            trailing_edge_panels = self._find_trailing_edge_panels()

            for i, te_panel_idx in enumerate(trailing_edge_panels):
                if i < self.num_wake_panels:
                    # Extend wake downstream
                    te_panel = self.panel_coordinates[te_panel_idx]
                    wake_panel = te_panel.copy()

                    # Shift wake panels downstream
                    wake_panel[:, 0] += 0.1 * (i + 1)  # Move in x-direction
                    self.wake_coordinates[i] = wake_panel

        logger.info(f"Initialized wake with {self.num_wake_panels} panels")

    def _find_trailing_edge_panels(self):
        """Find panels on the trailing edge of the wing."""
        # Simplified: assume trailing edge is at maximum x-coordinate
        max_x = np.max(self.panel_coordinates[:, :, 0])
        tolerance = 0.01

        trailing_edge_indices = []
        for i in range(self.num_panels):
            panel_max_x = np.max(self.panel_coordinates[i, :, 0])
            if abs(panel_max_x - max_x) < tolerance:
                trailing_edge_indices.append(i)

        return trailing_edge_indices

    def _setup_flapping_kinematics(self, flapping_params):
        """Set up flapping wing kinematics parameters."""

        self.flapping_amplitude = flapping_params.get('amplitude', 30.0)  # degrees
        self.flapping_frequency = flapping_params.get('frequency', 2.0)  # Hz
        self.phase_lag = flapping_params.get('phase_lag', 90.0)  # degrees

        # Create kinematics function
        def wing_kinematics(time, span_position):
            """
            Compute wing angle as function of time and spanwise position.

            Args:
                time: Current time [s]
                span_position: Normalized spanwise position [0, 1]

            Returns:
                Wing twist angle [radians]
            """
            base_angle = self.flapping_amplitude * np.sin(2 * np.pi * self.flapping_frequency * time)
            phase_shift = np.radians(self.phase_lag) * span_position
            total_angle = base_angle + phase_shift
            return np.radians(total_angle)

        self.wing_kinematics = wing_kinematics

        logger.info(f"Flapping kinematics: {self.flapping_frequency} Hz, {self.flapping_amplitude}° amplitude")

    def _initialize_flow_field(self):
        """Initialize flow field variables."""

        # Freestream conditions
        freestream = self.boundary_conditions.get('freestream', {})
        self.freestream_velocity = np.array(freestream.get('velocity', [10.0, 0.0, 0.0]))
        self.angle_of_attack = np.radians(freestream.get('angle_of_attack', 5.0))

        # Initialize solution vectors
        self.panel_strengths = np.zeros(self.num_panels)
        self.velocity_field = np.zeros((self.num_panels, 3))
        self.pressure_field = np.zeros(self.num_panels)

        # State variables for coupling
        self.state_variables = {
            'panel_strengths': self.panel_strengths,
            'pressure_distribution': self.pressure_field,
            'velocity_field': self.velocity_field
        }

        logger.info("Flow field initialized")

    def compute_residual(self, state: np.ndarray, time: float) -> np.ndarray:
        """
        Compute aerodynamic residual for panel method solution.

        The residual represents the error in satisfying boundary conditions.
        """

        # Extract panel strengths from state vector
        if len(state) >= self.num_panels:
            self.panel_strengths = state[:self.num_panels]

        # Update wing geometry for flapping motion
        if self.wing_kinematics is not None:
            self._update_wing_position(time)

        # Compute influence coefficients
        influence_matrix = self._compute_influence_matrix()

        # Right-hand side (boundary conditions)
        rhs = self._compute_boundary_conditions(time)

        # Residual = A*x - b
        residual = influence_matrix @ self.panel_strengths - rhs

        # Add wake influence if present
        if len(self.wake_history) > 0:
            wake_influence = self._compute_wake_influence()
            residual -= wake_influence

        return residual

    def compute_jacobian(self, state: np.ndarray, time: float) -> sp.spmatrix:
        """Compute Jacobian matrix for aerodynamic system."""

        # For panel method, Jacobian is the influence coefficient matrix
        influence_matrix = self._compute_influence_matrix()

        # Convert to sparse matrix for efficiency
        return sp.csr_matrix(influence_matrix)

    def _compute_influence_matrix(self) -> np.ndarray:
        """
        Compute influence coefficient matrix for panel method.

        A[i,j] represents the velocity induced at control point i by panel j.
        """

        A = np.zeros((self.num_panels, self.num_panels))

        for i in range(self.num_panels):
            control_point = self.control_points[i]
            panel_normal = self.panel_normals[i]

            for j in range(self.num_panels):
                if i == j:
                    # Self-influence (analytical)
                    A[i, j] = 0.5
                else:
                    # Influence of panel j on control point i
                    induced_velocity = self._compute_panel_influence(
                        self.panel_coordinates[j], control_point
                    )

                    # Dot with normal to get normal velocity component
                    A[i, j] = np.dot(induced_velocity, panel_normal)

        return A

    def _compute_panel_influence(self, panel_coords: np.ndarray, target_point: np.ndarray) -> np.ndarray:
        """
        Compute velocity induced by a single panel at target point.

        Uses vortex panel method with constant strength distribution.
        """

        # Panel corners
        p1, p2, p3, p4 = panel_coords

        # Compute influence of each edge vortex
        velocity = np.zeros(3)

        edges = [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]

        for edge_start, edge_end in edges:
            # Biot-Savart law for straight vortex segment
            r1 = target_point - edge_start
            r2 = target_point - edge_end

            r1_mag = np.linalg.norm(r1)
            r2_mag = np.linalg.norm(r2)

            if r1_mag > 1e-10 and r2_mag > 1e-10:
                cross_product = np.cross(r1, r2)
                cross_mag = np.linalg.norm(cross_product)

                if cross_mag > 1e-10:
                    # Biot-Savart formula
                    coeff = 1.0 / (4.0 * np.pi * cross_mag * cross_mag)
                    dot_product = np.dot(r1 / r1_mag - r2 / r2_mag, edge_end - edge_start)
                    velocity += coeff * dot_product * cross_product

        return velocity

    def _compute_boundary_conditions(self, time: float) -> np.ndarray:
        """Compute right-hand side vector for boundary conditions."""

        rhs = np.zeros(self.num_panels)

        for i in range(self.num_panels):
            control_point = self.control_points[i]
            panel_normal = self.panel_normals[i]

            # Freestream velocity
            freestream_vel = self.freestream_velocity.copy()

            # Apply angle of attack rotation
            cos_alpha = np.cos(self.angle_of_attack)
            sin_alpha = np.sin(self.angle_of_attack)

            freestream_vel_rotated = np.array([
                freestream_vel[0] * cos_alpha - freestream_vel[2] * sin_alpha,
                freestream_vel[1],
                freestream_vel[0] * sin_alpha + freestream_vel[2] * cos_alpha
            ])

            # Add flapping motion velocity if applicable
            if self.wing_kinematics is not None:
                flapping_velocity = self._compute_flapping_velocity(control_point, time)
                freestream_vel_rotated += flapping_velocity

            # Normal component of total velocity (boundary condition)
            rhs[i] = -np.dot(freestream_vel_rotated, panel_normal)

        return rhs

    def _compute_flapping_velocity(self, point: np.ndarray, time: float) -> np.ndarray:
        """Compute velocity due to flapping motion at given point."""

        # Simplified flapping velocity calculation
        span_position = abs(point[1]) / (self.geometry['wing_geometry']['wingspan'] / 2)
        span_position = min(1.0, span_position)

        # Angular velocity from kinematics
        dt = 1e-6
        angle_now = self.wing_kinematics(time, span_position)
        angle_future = self.wing_kinematics(time + dt, span_position)
        angular_velocity = (angle_future - angle_now) / dt

        # Velocity = omega x r (cross product)
        omega = np.array([0, angular_velocity, 0])  # Rotation about y-axis
        r = np.array([point[0], 0, point[2]])  # Position relative to rotation axis

        return np.cross(omega, r)

    def _update_wing_position(self, time: float):
        """Update wing panel positions due to flapping motion."""

        if self.wing_kinematics is None:
            return

        # Update panel coordinates and control points
        for i in range(self.num_panels):
            # Get spanwise position
            y_pos = self.control_points[i, 1]
            wingspan = self.geometry['wing_geometry']['wingspan']
            span_position = abs(y_pos) / (wingspan / 2)
            span_position = min(1.0, span_position)

            # Get twist angle
            twist_angle = self.wing_kinematics(time, span_position)

            # Apply rotation to panel (simplified)
            cos_twist = np.cos(twist_angle)
            sin_twist = np.sin(twist_angle)

            rotation_matrix = np.array([
                [cos_twist, 0, sin_twist],
                [0, 1, 0],
                [-sin_twist, 0, cos_twist]
            ])

            # Rotate panel corners
            for j in range(4):
                self.panel_coordinates[i, j] = rotation_matrix @ self.panel_coordinates[i, j]

            # Update control point
            self.control_points[i] = rotation_matrix @ self.control_points[i]

            # Update normal
            self.panel_normals[i] = rotation_matrix @ self.panel_normals[i]

    def _compute_wake_influence(self) -> np.ndarray:
        """Compute influence of wake panels on wing boundary conditions."""

        wake_influence = np.zeros(self.num_panels)

        for wake_panel_idx, wake_strength in enumerate(self.wake_strengths):
            if wake_strength != 0:
                wake_coords = self.wake_coordinates[wake_panel_idx]

                for i in range(self.num_panels):
                    control_point = self.control_points[i]
                    panel_normal = self.panel_normals[i]

                    # Compute wake panel influence
                    induced_velocity = self._compute_panel_influence(wake_coords, control_point)
                    wake_influence[i] += wake_strength * np.dot(induced_velocity, panel_normal)

        return wake_influence

    def update_coupling_variables(self, coupled_data: Dict[str, Any]):
        """Update aerodynamics based on structural deformation."""

        if 'surface_displacement' in coupled_data:
            # Update panel positions based on structural displacement
            displacement = coupled_data['surface_displacement']

            if len(displacement) == self.num_panels:
                for i in range(self.num_panels):
                    # Apply displacement to panel corners
                    for j in range(4):
                        self.panel_coordinates[i, j] += displacement[i]

                    # Update control point
                    self.control_points[i] += displacement[i]

                logger.debug("Updated wing geometry from structural coupling")

    def get_coupling_variables(self) -> Dict[str, Any]:
        """Return aerodynamic variables for coupling to other modules."""

        # Compute pressure distribution
        self._compute_pressure_distribution()

        # Compute integrated forces
        total_force, total_moment = self._compute_integrated_forces()

        return {
            'pressure_distribution': self.pressure_field.copy(),
            'panel_forces': self.pressure_field * self.panel_areas,
            'total_force': total_force,
            'total_moment': total_moment,
            'control_points': self.control_points.copy(),
            'panel_areas': self.panel_areas.copy()
        }

    def _compute_pressure_distribution(self):
        """Compute pressure distribution from panel strengths using Bernoulli's equation."""

        # Compute velocity at each panel
        for i in range(self.num_panels):
            # Total velocity = freestream + induced
            total_velocity = self.freestream_velocity.copy()

            # Add induced velocities from all panels
            for j in range(self.num_panels):
                if i != j:
                    induced_vel = self._compute_panel_influence(
                        self.panel_coordinates[j], self.control_points[i]
                    )
                    total_velocity += self.panel_strengths[j] * induced_vel

            # Velocity magnitude
            vel_magnitude = np.linalg.norm(total_velocity)

            # Bernoulli's equation: p + 0.5*rho*V^2 = constant
            freestream_speed = np.linalg.norm(self.freestream_velocity)
            pressure_coefficient = 1.0 - (vel_magnitude / freestream_speed) ** 2

            # Dynamic pressure
            dynamic_pressure = 0.5 * self.air_density * freestream_speed * freestream_speed

            self.pressure_field[i] = pressure_coefficient * dynamic_pressure

    def _compute_integrated_forces(self) -> Tuple[np.ndarray, np.ndarray]:
        """Compute total force and moment on the wing."""

        total_force = np.zeros(3)
        total_moment = np.zeros(3)

        # Reference point for moments (wing root)
        reference_point = np.array([0, 0, 0])

        for i in range(self.num_panels):
            # Force on this panel
            panel_force = self.pressure_field[i] * self.panel_areas[i] * self.panel_normals[i]
            total_force += panel_force

            # Moment arm
            moment_arm = self.control_points[i] - reference_point

            # Moment contribution
            total_moment += np.cross(moment_arm, panel_force)

        return total_force, total_moment

    def advance_wake(self, time_step: float):
        """Advance wake panels downstream and update wake strength."""

        # Convect existing wake panels
        convection_velocity = self.freestream_velocity[0]  # Simplified

        for i in range(self.num_wake_panels):
            self.wake_coordinates[i, :, 0] += convection_velocity * time_step

        # Add new wake panel at trailing edge
        trailing_edge_panels = self._find_trailing_edge_panels()

        if trailing_edge_panels:
            # Set wake strength based on circulation
            new_wake_strength = np.mean([self.panel_strengths[idx] for idx in trailing_edge_panels])

            # Shift wake strengths
            self.wake_strengths[1:] = self.wake_strengths[:-1]
            self.wake_strengths[0] = new_wake_strength

        # Store wake history for analysis
        self.wake_history.append({
            'time': time_step,
            'coordinates': self.wake_coordinates.copy(),
            'strengths': self.wake_strengths.copy()
        })

        # Limit wake history length
        if len(self.wake_history) > self.max_wake_length:
            self.wake_history.pop(0)

    def compute_performance_metrics(self) -> Dict[str, float]:
        """Compute aerodynamic performance metrics."""

        # Integrated forces
        total_force, total_moment = self._compute_integrated_forces()

        # Reference values
        freestream_speed = np.linalg.norm(self.freestream_velocity)
        dynamic_pressure = 0.5 * self.air_density * freestream_speed * freestream_speed
        wing_area = np.sum(self.panel_areas)

        # Force coefficients
        lift = -total_force[2]  # Negative z is up
        drag = total_force[0]   # Positive x is drag

        lift_coefficient = lift / (dynamic_pressure * wing_area)
        drag_coefficient = drag / (dynamic_pressure * wing_area)

        # Efficiency
        lift_to_drag_ratio = lift_coefficient / drag_coefficient if drag_coefficient > 0 else float('inf')

        # Power requirements (for flapping wings)
        power_coefficient = 0.0
        if self.wing_kinematics is not None:
            # Simplified power calculation
            angular_velocity = 2 * np.pi * self.flapping_frequency
            power_coefficient = abs(total_moment[1]) * angular_velocity / (dynamic_pressure * wing_area * freestream_speed)

        return {
            'lift_coefficient': lift_coefficient,
            'drag_coefficient': drag_coefficient,
            'lift_to_drag_ratio': lift_to_drag_ratio,
            'power_coefficient': power_coefficient,
            'total_lift': lift,
            'total_drag': drag,
            'wing_area': wing_area,
            'reynolds_number': self.air_density * freestream_speed * np.sqrt(wing_area) / self.air_viscosity
        }
