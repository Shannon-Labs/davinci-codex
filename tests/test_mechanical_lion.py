"""
Comprehensive tests for Leonardo's Mechanical Lion walking mechanism.

This test suite validates the biomechanical analysis, stability calculations,
cam profile generation, and structural analysis of the mechanical lion
design. Tests ensure the design meets historical accuracy and modern
engineering standards.
"""

import math
from pathlib import Path

import numpy as np
import pytest

from davinci_codex.inventions.mechanical_lion import (
    CAM_DRUM_RADIUS,
    LATERAL_LEG_SPACING,
    LEG_LENGTH,
    LION_HEIGHT,
    # Constants to test
    LION_LENGTH,
    LION_WEIGHT,
    LION_WIDTH,
    PHASE_OFFSET_FRONT_REAR,
    PHASE_OFFSET_LEFT_RIGHT,
    STEP_DURATION,
    SWING_PHASE_RATIO,
    CamProfileDesigner,
    ChestMechanism,
    LegKinematics,
    StabilityAnalysis,
    evaluate,
    plan,
    simulate,
)


class TestLegKinematics:
    """Test leg kinematics and gait generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.lf_leg = LegKinematics('LF', True, True)   # Left Front
        self.rf_leg = LegKinematics('RF', True, False)  # Right Front
        self.lh_leg = LegKinematics('LH', False, True)  # Left Hind
        self.rh_leg = LegKinematics('RH', False, False) # Right Hind

    def test_leg_initialization(self):
        """Test leg initialization with correct parameters."""
        assert self.lf_leg.leg_id == 'LF'
        assert self.lf_leg.is_front
        assert self.lf_leg.is_left
        assert self.lf_leg.upper_leg_length == LEG_LENGTH * 0.5
        assert self.lf_leg.lower_leg_length == LEG_LENGTH * 0.5

    def test_phase_offset_calculation(self):
        """Test phase offset calculations for gait coordination."""
        # Left front leg is reference (phase offset = 0)
        assert self.lf_leg.phase_offset == 0.0

        # Right front leg offset by 0.25
        assert abs(self.rf_leg.phase_offset - PHASE_OFFSET_LEFT_RIGHT) < 1e-10

        # Left hind leg offset by 0.5
        assert abs(self.lh_leg.phase_offset - PHASE_OFFSET_FRONT_REAR) < 1e-10

        # Right hind leg offset by 0.5 + 0.25
        expected_rh_offset = PHASE_OFFSET_FRONT_REAR + PHASE_OFFSET_LEFT_RIGHT
        assert abs(self.rh_leg.phase_offset - expected_rh_offset) < 1e-10

    def test_joint_angles_bounds(self):
        """Test joint angles stay within realistic bounds."""
        # Test multiple time points
        for t in np.linspace(0, STEP_DURATION * 2, 20):
            hip_angle, knee_angle, ground_contact = self.lf_leg.calculate_joint_angles(t)

            # Hip angle should be within limits
            assert self.lf_leg.hip_min <= hip_angle <= self.lf_leg.hip_max

            # Knee angle should be within limits
            assert self.lf_leg.knee_min <= knee_angle <= self.lf_leg.knee_max

            # Ground contact should be boolean
            assert isinstance(ground_contact, bool)

    def test_swing_stance_phases(self):
        """Test proper swing and stance phase timing."""
        # Test left front leg (reference)
        for t in np.linspace(0, STEP_DURATION, 10):
            hip_angle, knee_angle, ground_contact = self.lf_leg.calculate_joint_angles(t)
            phase = (t / STEP_DURATION) % 1.0

            if phase < SWING_PHASE_RATIO:
                # Should be in swing phase (leg off ground)
                assert not ground_contact, f"Expected swing phase at t={t}, phase={phase}"
                # Knee should be flexed during swing
                assert knee_angle > self.lf_leg.knee_min + 0.1
            else:
                # Should be in stance phase (leg on ground)
                assert ground_contact, f"Expected stance phase at t={t}, phase={phase}"
                # Knee should be mostly extended during stance
                assert knee_angle < self.lf_leg.knee_max * 0.3

    def test_gait_coordination(self):
        """Test proper gait coordination between legs."""
        t = STEP_DURATION * 0.5  # Mid-step

        # Calculate ground contact for all legs
        contacts = {}
        for leg_name, leg in [('LF', self.lf_leg), ('RF', self.rf_leg),
                              ('LH', self.lh_leg), ('RH', self.rh_leg)]:
            _, _, ground_contact = leg.calculate_joint_angles(t)
            contacts[leg_name] = ground_contact

        # Should have at least 2 legs on ground for stability
        num_ground_contact = sum(contacts.values())
        assert num_ground_contact >= 2, f"Insufficient ground contact: {contacts}"

    def test_foot_position_calculation(self):
        """Test foot position kinematics."""
        hip_angle = 0.0  # Horizontal
        knee_angle = math.pi / 6  # 30 degrees flexed

        foot_x, foot_y, foot_z = self.lf_leg.calculate_foot_position(hip_angle, knee_angle)

        # Foot should be ahead of hip for positive hip angle
        assert foot_x > 0

        # Foot should be at ground level
        assert foot_y == 0.0

        # Foot height should be reasonable
        assert 0 <= foot_z <= LEG_LENGTH

    def test_cam_profile_generation(self):
        """Test cam profile generation for leg motion."""
        angles, radii = self.lf_leg.calculate_cam_profile(num_points=100)

        # Should have correct number of points
        assert len(angles) == 100
        assert len(radii) == 100

        # Angles should cover full rotation
        assert angles[0] == 0.0
        assert abs(angles[-1] - 2 * math.pi) < 1e-10

        # Radii should be positive and reasonable
        assert all(r > 0 for r in radii)
        assert all(r < 0.5 for r in radii)  # Reasonable cam radius


class TestStabilityAnalysis:
    """Test stability analysis and center of mass calculations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.stability_analyzer = StabilityAnalysis(LION_LENGTH, LATERAL_LEG_SPACING, LION_WEIGHT)

    def test_initialization(self):
        """Test stability analyzer initialization."""
        assert self.stability_analyzer.body_length == LION_LENGTH
        assert self.stability_analyzer.body_width == LATERAL_LEG_SPACING
        assert self.stability_analyzer.body_mass == LION_WEIGHT
        assert len(self.stability_analyzer.legs) == 4

    def test_support_polygon_calculation(self):
        """Test support polygon calculation."""
        # Test at multiple time points
        for t in np.linspace(0, STEP_DURATION * 2, 10):
            support_polygon = self.stability_analyzer.calculate_support_polygon(t)

            # Should have at least 2 contact points for stability
            assert len(support_polygon) >= 2

            # All points should be valid coordinates
            for point in support_polygon:
                assert len(point) == 2
                assert all(isinstance(coord, (int, float)) for coord in point)

    def test_center_of_mass_calculation(self):
        """Test center of mass calculation."""
        com_x, com_y = self.stability_analyzer.calculate_center_of_mass(0.0)

        # Center of mass should be near body center
        assert abs(com_x) < 0.5  # Within 0.5m of center
        assert abs(com_y) < 0.3  # Within 0.3m of center

    def test_stability_check(self):
        """Test stability checking functionality."""
        # Test at multiple time points
        for t in np.linspace(0, STEP_DURATION * 2, 20):
            stability_result = self.stability_analyzer.check_stability(t)

            # Should return all required fields
            required_fields = ['is_stable', 'stability_margin', 'support_area',
                             'com_distance', 'com_x', 'com_y', 'support_points']
            for field in required_fields:
                assert field in stability_result

            # Stability margin should be reasonable
            assert isinstance(stability_result['stability_margin'], (int, float))
            assert isinstance(stability_result['is_stable'], bool)
            assert stability_result['support_points'] >= 0

    def test_polygon_area_calculation(self):
        """Test polygon area calculation."""
        # Test square
        square = [(0, 0), (1, 0), (1, 1), (0, 1)]
        area = self.stability_analyzer._calculate_polygon_area(square)
        assert abs(area - 1.0) < 1e-10

        # Test triangle
        triangle = [(0, 0), (1, 0), (0, 1)]
        area = self.stability_analyzer._calculate_polygon_area(triangle)
        assert abs(area - 0.5) < 1e-10

    def test_point_in_polygon(self):
        """Test point-in-polygon detection."""
        # Test square
        square = [(0, 0), (2, 0), (2, 2), (0, 2)]

        # Point inside
        assert self.stability_analyzer._point_in_polygon(1, 1, square)

        # Point outside
        assert not self.stability_analyzer._point_in_polygon(3, 3, square)

        # Point on edge (implementation dependent)
        # assert self.stability_analyzer._point_in_polygon(1, 0, square)


class TestCamProfileDesigner:
    """Test cam profile design and generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.designer = CamProfileDesigner()
        self.test_leg = LegKinematics('LF', True, True)

    def test_initialization(self):
        """Test cam designer initialization."""
        assert self.designer.cam_radius == CAM_DRUM_RADIUS
        assert 'lift' in self.designer.cam_types
        assert 'extend' in self.designer.cam_types
        assert 'swing' in self.designer.cam_types

    def test_leg_cam_profile_generation(self):
        """Test cam profile generation for specific leg."""
        for cam_type in self.designer.cam_types:
            profile = self.designer.generate_leg_cam_profile(self.test_leg, cam_type)

            # Should have correct number of points (360 degrees)
            assert len(profile) == 360

            # All values should be positive
            assert all(p > 0 for p in profile)

            # Values should be reasonable for cam radius
            assert all(p < CAM_DRUM_RADIUS * 3 for p in profile)

    def test_cam_profile_smoothing(self):
        """Test cam profile smoothing."""
        # Create noisy profile
        noisy_profile = np.ones(100) + np.random.normal(0, 0.1, 100)

        # Smooth the profile
        smoothed = self.designer._smooth_cam_profile(noisy_profile)

        # Should have same length
        assert len(smoothed) == len(noisy_profile)

        # Should be smoother (lower variance)
        assert np.var(smoothed) < np.var(noisy_profile)

    def test_cam_profile_export(self):
        """Test cam profile export functionality."""
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Export profiles
            profiles = self.designer.export_cam_profiles(temp_path)

            # Should generate profiles for all legs and cam types
            expected_profiles = 4 * len(self.designer.cam_types)  # 4 legs × cam types
            assert len(profiles) == expected_profiles

            # Check that files were created
            for profile_name in profiles:
                profile_file = temp_path / f"{profile_name}.csv"
                assert profile_file.exists()


class TestChestMechanism:
    """Test chest cavity reveal mechanism."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mechanism = ChestMechanism()

    def test_initialization(self):
        """Test chest mechanism initialization."""
        assert len(self.mechanism.panels) == 4  # 4 panels
        assert self.mechanism.lily_platform.lily_count == 3
        assert self.mechanism.current_phase == "closed"
        assert self.mechanism.is_locked

    def test_spring_force_calculation(self):
        """Test spring force calculation."""
        compression = 0.1  # 10cm compression
        force = self.mechanism.calculate_spring_force(compression)

        # Force should be positive and proportional to compression
        assert force > 0
        expected_force = 150.0 * compression  # SPRING_CONSTANT_N_PER_M * compression
        assert abs(force - expected_force) < 1e-10

    def test_cam_profile_calculation(self):
        """Test cam lift profile calculation."""
        # Test at different angles
        for angle in [0, math.pi/4, math.pi/2, math.pi]:
            lift = self.mechanism.calculate_cam_profile(angle)

            # Lift should be non-negative
            assert lift >= 0

            # Lift should be reasonable for cam size
            assert lift < CAM_DRUM_RADIUS * 2

    def test_panel_torque_calculation(self):
        """Test panel torque calculation."""
        panel = self.mechanism.panels[0]

        # Test at different angles
        for angle in [0, math.pi/6, math.pi/4, math.pi/3]:
            torque = self.mechanism.calculate_panel_torque(panel, angle)

            # Torque should be positive for opening motion
            if angle > 0:
                assert torque > 0

    def test_mechanism_update(self):
        """Test mechanism state updates."""
        # Test opening phase
        dt = 0.1
        self.mechanism.update_mechanism(dt, "opening")

        # Should have progressed through opening
        assert self.mechanism.performance_time_s > 0
        assert self.mechanism.cam_angle_rad > 0

        # Panels should have opened
        for panel in self.mechanism.panels:
            assert panel.current_angle_rad > 0

    def test_chest_aperture_calculation(self):
        """Test chest aperture calculation."""
        # Initially closed
        assert self.mechanism.get_chest_aperture() == 0.0

        # Open all panels
        for panel in self.mechanism.panels:
            panel.current_angle_rad = panel.opening_angle_rad

        # Should be fully open
        assert abs(self.mechanism.get_chest_aperture() - 1.0) < 1e-10

    def test_mechanical_stress_check(self):
        """Test mechanical stress checking."""
        stress = self.mechanism.check_mechanical_stress()

        # Should return all required fields
        required_fields = ['max_panel_torque_nm', 'max_spring_force_n', 'cam_load_n']
        for field in required_fields:
            assert field in stress
            assert isinstance(stress[field], (int, float))


class TestIntegration:
    """Integration tests for complete system."""

    def test_plan_function(self):
        """Test plan function returns comprehensive planning document."""
        plan_result = plan()

        # Check major sections
        required_sections = [
            'origin', 'historical_significance', 'design_requirements',
            'biomechanical_analysis', 'mechanical_design_specifications',
            'renaissance_constraints', 'engineering_principles',
            'success_criteria', 'validation_plan', 'educational_outcomes'
        ]

        for section in required_sections:
            assert section in plan_result, f"Missing section: {section}"

        # Check specific historical details
        assert '1515' in str(plan_result['origin']['historical_event'])
        assert 'Francis I' in str(plan_result['origin'])

    def test_simulate_function(self):
        """Test simulate function runs without errors."""
        sim_result = simulate()

        # Check major result sections
        required_sections = [
            'biomechanical_analysis', 'mechanical_design', 'historical_analysis',
            'educational_insights', 'artifacts', 'validation', 'success_criteria'
        ]

        for section in required_sections:
            assert section in sim_result, f"Missing section: {section}"

        # Check biomechanical analysis results
        biomech = sim_result['biomechanical_analysis']
        assert 'gait_stability' in biomech
        assert 'walking_performance' in biomech
        assert 'leg_articulation' in biomech

        # Check that artifacts were generated
        assert len(sim_result['artifacts']) > 0

    def test_evaluate_function(self):
        """Test evaluate function provides comprehensive assessment."""
        eval_result = evaluate()

        # Check major evaluation sections
        required_sections = [
            'practicality', 'ethics', 'historical_analysis',
            'educational_value', 'speculative', 'legacy_impact',
            'validation', 'next_actions'
        ]

        for section in required_sections:
            assert section in eval_result, f"Missing section: {section}"

        # Check validation results
        validation = eval_result['validation']
        assert validation['mechanical_soundness']
        assert validation['renaissance_authenticity']

    def test_gait_stability_throughout_cycle(self):
        """Test stability throughout complete gait cycle."""
        stability_analyzer = StabilityAnalysis(LION_LENGTH, LATERAL_LEG_SPACING, LION_WEIGHT)

        # Test throughout multiple gait cycles
        for t in np.linspace(0, STEP_DURATION * 4, 100):
            stability_result = stability_analyzer.check_stability(t)

            # Should be stable most of the time
            # Allow some instability during transitions
            if stability_result['stability_margin'] < 0:
                # If unstable, should be momentary (check neighboring times)
                for dt in [-0.05, 0.05]:
                    neighbor_t = t + dt
                    if 0 <= neighbor_t <= STEP_DURATION * 4:
                        neighbor_result = stability_analyzer.check_stability(neighbor_t)
                        if neighbor_result['stability_margin'] > 0:
                            break  # Found stable neighbor, acceptable
                else:
                    # If no stable neighbors found, this might be a problem
                    pytest.fail(f"Prolonged instability at t={t}")

    def test_power_requirements_reasonableness(self):
        """Test that power requirements are reasonable for human operation."""
        from davinci_codex.inventions.mechanical_lion import _analyze_power_requirements

        power_results = _analyze_power_requirements()

        # Check that results are reasonable
        assert power_results['work_per_step_J'] > 0
        assert power_results['power_required_W'] > 0
        assert power_results['spring_energy_stored_J'] > 0
        assert power_results['operating_time_per_winding_s'] > 0
        assert power_results['winding_force_required_N'] > 0

        # Human winding should be feasible
        assert power_results['human_winding_feasibility']

    def test_structural_analysis_safety_factors(self):
        """Test structural analysis provides adequate safety factors."""
        from davinci_codex.inventions.mechanical_lion import _perform_structural_analysis

        structural_results = _perform_structural_analysis()

        # Check that all safety factors are adequate
        required_safety_factors = [
            'oak_safety_factor',
            'bronze_safety_factor',
            'spring_safety_factor'
        ]

        min_safety_factor = 2.0  # Minimum acceptable

        for factor_name in required_safety_factors:
            assert factor_name in structural_results
            safety_factor = structural_results[factor_name]
            assert safety_factor > min_safety_factor, f"Safety factor too low: {factor_name} = {safety_factor}"

        # Overall integrity should be good
        overall_integrity = structural_results['overall_structural_integrity']
        assert overall_integrity > min_safety_factor


class TestPhysicalConstraints:
    """Test physical constraints and realism."""

    def test_lion_proportions_realistic(self):
        """Test lion proportions are realistic."""
        # Lions typically have certain proportions
        length_to_height_ratio = LION_LENGTH / LION_HEIGHT
        assert 1.5 <= length_to_height_ratio <= 2.5, "Lion proportions unrealistic"

        # Weight should be reasonable for size
        volume_estimate = LION_LENGTH * LION_WIDTH * LION_HEIGHT
        density_estimate = LION_WEIGHT / volume_estimate
        assert 200 <= density_estimate <= 2000, "Lion density unrealistic"

    def test_walking_speed_reasonable(self):
        """Test walking speed is reasonable for a lion."""
        # Lions typically walk at 0.5-1.5 m/s
        from davinci_codex.inventions.mechanical_lion import LION_WALKING_SPEED
        assert 0.3 <= LION_WALKING_SPEED <= 2.0, "Walking speed unrealistic"

    def test_leg_length_proportions(self):
        """Test leg length proportions are realistic."""
        # Leg length should be appropriate for body height
        leg_to_body_ratio = LEG_LENGTH / LION_HEIGHT
        assert 0.4 <= leg_to_body_ratio <= 0.8, "Leg proportions unrealistic"

    def test_cam_size_reasonable(self):
        """Test cam drum size is reasonable for mechanism."""
        # Cam should be large enough for precision but not excessively large
        cam_to_body_ratio = CAM_DRUM_RADIUS / LION_LENGTH
        assert 0.02 <= cam_to_body_ratio <= 0.2, "Cam size unreasonable"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
