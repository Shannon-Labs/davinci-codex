#!/usr/bin/env python3
"""
Leonardo da Vinci's Self-Supporting Revolving Bridge - CAD Model

This module provides a computational model of Leonardo's revolving bridge design,
as documented in Codex Atlanticus, f.855r. The bridge was designed for military
applications, allowing rapid deployment across rivers or moats without support
from the opposite bank.

Copyright (c) 2025 davinci-codex contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This content is dedicated to the public domain under CC0 1.0 Universal.
Original designs and concepts by Leonardo da Vinci (1452-1519) are in the public domain.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, List, Optional
import math


@dataclass
class BridgeParameters:
    """Physical parameters for Leonardo's revolving bridge design."""
    # Bridge dimensions (meters)
    length: float = 16.0  # Span length
    width: float = 3.0    # Bridge width
    height: float = 1.5   # Structural height
    
    # Material properties (modern equivalents)
    wood_density: float = 700.0  # kg/m³ (oak equivalent)
    wood_strength: float = 40.0  # MPa
    youngs_modulus: float = 12.0e9  # Pa
    
    # Operational parameters
    rotation_time: float = 120.0  # seconds to deploy
    counterweight_mass: float = 5000.0  # kg
    safety_factor: float = 6.0
    
    # Environmental factors
    wind_load: float = 500.0  # N/m²
    live_load: float = 5000.0  # N/m²


class RevolvingBridgeModel:
    """
    Computational model of Leonardo's self-supporting revolving bridge.
    
    This model simulates the mechanical behavior, structural analysis,
    and deployment dynamics of the bridge design.
    """
    
    def __init__(self, params: Optional[BridgeParameters] = None):
        """Initialize the bridge model with default or custom parameters."""
        self.params = params or BridgeParameters()
        self.rotation_angle = 0.0  # Current rotation angle (radians)
        self.is_deployed = False
        
        # Calculate derived properties
        self._calculate_properties()
    
    def _calculate_properties(self):
        """Calculate derived structural properties."""
        # Bridge mass
        volume = self.params.length * self.params.width * self.params.height
        self.bridge_mass = volume * self.params.wood_density
        
        # Moment of inertia about rotation axis
        self.moment_of_inertia = (1/3) * self.bridge_mass * self.params.length**2
        
        # Center of gravity from pivot point
        self.center_of_gravity = self.params.length / 2
        
        # Maximum bending moment
        self.max_moment = (self.bridge_mass * 9.81 * self.params.length**2) / 8
    
    def calculate_rotation_profile(self, time_steps: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate the rotation profile for bridge deployment.
        
        Args:
            time_steps: Number of time points in the profile
            
        Returns:
            Tuple of (time_array, angle_array) for the deployment sequence
        """
        time = np.linspace(0, self.params.rotation_time, time_steps)
        
        # S-curve profile for smooth acceleration/deceleration
        # Using a sigmoid-like function for controlled motion
        normalized_time = time / self.params.rotation_time
        
        # Smooth S-curve: 3t² - 2t³ for 0 ≤ t ≤ 1
        smooth_factor = 3 * normalized_time**2 - 2 * normalized_time**3
        angles = smooth_factor * (np.pi / 2)  # 90-degree rotation
        
        return time, angles
    
    def calculate_moment_balance(self, angle: float) -> Tuple[float, float, float]:
        """
        Calculate moment balance at a given rotation angle.
        
        Args:
            angle: Current rotation angle in radians
            
        Returns:
            Tuple of (bridge_moment, counterweight_moment, moment_ratio)
        """
        # Bridge moment about pivot
        bridge_moment = self.bridge_mass * 9.81 * self.center_of_gravity * np.cos(angle)
        
        # Counterweight moment (assumed constant)
        counterweight_moment = self.params.counterweight_mass * 9.81 * 2.0  # 2m lever arm
        
        # Moment ratio (safety factor)
        moment_ratio = counterweight_moment / bridge_moment if bridge_moment > 0 else float('inf')
        
        return bridge_moment, counterweight_moment, moment_ratio
    
    def calculate_deflection(self, load: float) -> float:
        """
        Calculate maximum deflection under load.
        
        Args:
            load: Applied load in N/m²
            
        Returns:
            Maximum deflection in meters
        """
        # Simple beam deflection formula
        # δ = (5 * w * L⁴) / (384 * E * I)
        
        # Second moment of area for rectangular cross-section
        I = (self.params.width * self.params.height**3) / 12
        
        # Distributed load
        w = load * self.params.width
        
        # Maximum deflection
        deflection = (5 * w * self.params.length**4) / (384 * self.params.youngs_modulus * I)
        
        return deflection
    
    def calculate_stress(self, load: float) -> float:
        """
        Calculate maximum bending stress.
        
        Args:
            load: Applied load in N/m²
            
        Returns:
            Maximum stress in Pa
        """
        # Bending stress formula: σ = M * c / I
        moment = (load * self.params.width * self.params.length**2) / 8
        I = (self.params.width * self.params.height**3) / 12
        c = self.params.height / 2
        
        stress = (moment * c) / I
        
        return stress
    
    def structural_analysis(self, angle: float = 0.0) -> dict:
        """
        Perform comprehensive structural analysis at a given angle.
        
        Args:
            angle: Rotation angle in radians
            
        Returns:
            Dictionary containing analysis results
        """
        # Moment balance
        bridge_moment, counterweight_moment, moment_ratio = self.calculate_moment_balance(angle)
        
        # Stress analysis
        total_load = self.params.wind_load + self.params.live_load
        stress = self.calculate_stress(total_load)
        allowable_stress = self.params.wood_strength / self.params.safety_factor
        
        # Deflection analysis
        deflection = self.calculate_deflection(total_load)
        
        # Safety checks
        stress_safety = allowable_stress / stress if stress > 0 else float('inf')
        deflection_limit = self.params.length / 250  # Standard deflection limit
        deflection_safety = deflection_limit / deflection if deflection > 0 else float('inf')
        
        return {
            'rotation_angle_deg': np.degrees(angle),
            'bridge_moment_kNm': bridge_moment / 1000,
            'counterweight_moment_kNm': counterweight_moment / 1000,
            'moment_ratio': moment_ratio,
            'max_stress_MPa': stress / 1e6,
            'allowable_stress_MPa': allowable_stress / 1e6,
            'stress_safety_factor': stress_safety,
            'max_deflection_mm': deflection * 1000,
            'deflection_limit_mm': deflection_limit * 1000,
            'deflection_safety_factor': deflection_safety,
            'structurally_safe': stress_safety >= 1.0 and deflection_safety >= 1.0
        }
    
    def plot_rotation_profile(self, save_path: Optional[str] = None):
        """Generate and optionally save the rotation profile plot."""
        time, angles = self.calculate_rotation_profile()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Rotation angle over time
        ax1.plot(time, np.degrees(angles), 'b-', linewidth=2)
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Rotation Angle (degrees)')
        ax1.set_title('Bridge Deployment Rotation Profile')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=90, color='r', linestyle='--', alpha=0.7, label='Target (90°)')
        ax1.legend()
        
        # Angular velocity over time
        angular_velocity = np.gradient(angles, time)
        ax2.plot(time, np.degrees(angular_velocity), 'g-', linewidth=2)
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Angular Velocity (degrees/second)')
        ax2.set_title('Angular Velocity During Deployment')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_moment_analysis(self, save_path: Optional[str] = None):
        """Generate and optionally save the moment balance analysis plot."""
        angles = np.linspace(0, np.pi/2, 50)
        bridge_moments = []
        counterweight_moments = []
        moment_ratios = []
        
        for angle in angles:
            b_m, c_m, ratio = self.calculate_moment_balance(angle)
            bridge_moments.append(b_m / 1000)  # Convert to kNm
            counterweight_moments.append(c_m / 1000)
            moment_ratios.append(ratio)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Moment comparison
        ax1.plot(np.degrees(angles), bridge_moments, 'b-', linewidth=2, label='Bridge Moment')
        ax1.plot(np.degrees(angles), counterweight_moments, 'r-', linewidth=2, label='Counterweight Moment')
        ax1.set_xlabel('Rotation Angle (degrees)')
        ax1.set_ylabel('Moment (kNm)')
        ax1.set_title('Moment Balance Analysis')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Moment ratio (safety factor)
        ax2.plot(np.degrees(angles), moment_ratios, 'g-', linewidth=2)
        ax2.axhline(y=1.0, color='r', linestyle='--', alpha=0.7, label='Minimum Safety Factor')
        ax2.set_xlabel('Rotation Angle (degrees)')
        ax2.set_ylabel('Moment Ratio (Safety Factor)')
        ax2.set_title('Safety Factor Throughout Deployment')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()


def main():
    """Demonstrate the revolving bridge model with analysis and visualization."""
    # Create bridge model with default parameters
    bridge = RevolvingBridgeModel()
    
    print("Leonardo da Vinci's Self-Supporting Revolving Bridge")
    print("=" * 60)
    print(f"Bridge Length: {bridge.params.length} m")
    print(f"Bridge Mass: {bridge.bridge_mass:.0f} kg")
    print(f"Rotation Time: {bridge.params.rotation_time} seconds")
    print(f"Safety Factor: {bridge.params.safety_factor}")
    print()
    
    # Analysis at different deployment positions
    positions = [0, 30, 45, 60, 90]  # degrees
    
    print("Structural Analysis at Different Positions:")
    print("-" * 60)
    
    for pos in positions:
        analysis = bridge.structural_analysis(np.radians(pos))
        print(f"Position: {pos}°")
        print(f"  Bridge Moment: {analysis['bridge_moment_kNm']:.1f} kNm")
        print(f"  Counterweight Moment: {analysis['counterweight_moment_kNm']:.1f} kNm")
        print(f"  Moment Ratio: {analysis['moment_ratio']:.2f}")
        print(f"  Max Stress: {analysis['max_stress_MPa']:.2f} MPa")
        print(f"  Max Deflection: {analysis['max_deflection_mm']:.2f} mm")
        print(f"  Structurally Safe: {'✓' if analysis['structurally_safe'] else '✗'}")
        print()
    
    # Create visualizations
    bridge.plot_rotation_profile()
    bridge.plot_moment_analysis()


if __name__ == "__main__":
    main()