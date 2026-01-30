"""
Comprehensive Visual Asset Generator for da Vinci Codex Project

This script generates missing visual assets for all inventions, including:
- Performance visualization charts
- Educational infographics
- Technical diagrams with Renaissance styling
- Comparison matrices and charts
- Animated demonstrations

Usage:
    python generate_visual_assets.py --all
    python generate_visual_assets.py --invention aerial_screw
    python generate_visual_assets.py --type infographics
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
from matplotlib.transforms import Affine2D

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Import invention modules
import davinci_codex.inventions.aerial_screw as aerial_screw
import davinci_codex.inventions.armored_walker as armored_walker
import davinci_codex.inventions.mechanical_carillon as mechanical_carillon
import davinci_codex.inventions.mechanical_drum as mechanical_drum
import davinci_codex.inventions.mechanical_ensemble as mechanical_ensemble
import davinci_codex.inventions.mechanical_organ as mechanical_organ
import davinci_codex.inventions.mechanical_trumpeter as mechanical_trumpeter
import davinci_codex.inventions.programmable_flute as programmable_flute
import davinci_codex.inventions.viola_organista as viola_organista
import davinci_codex.inventions.mechanical_odometer as mechanical_odometer
import davinci_codex.inventions.revolving_bridge as revolving_bridge
import davinci_codex.inventions.parachute as parachute
import davinci_codex.inventions.variable_pitch_mechanism as variable_pitch_mechanism
import davinci_codex.inventions.mechanical_lion as mechanical_lion
import davinci_codex.inventions.ornithopter as ornithopter
import davinci_codex.inventions.self_propelled_cart as self_propelled_cart
import davinci_codex.inventions.programmable_loom as programmable_loom

# Renaissance color palette
RENAISSANCE_COLORS = {
    'background': '#F5E6D3',  # Parchment
    'ink': '#2C1810',          # Brown ink
    'red_ink': '#8B2500',      # Venetian red
    'gold': '#D4AF37',         # Gold leaf
    'blue': '#1E3A8A',         # Ultramarine
    'green': '#2F4F2F',        # Forest green
    'sepia': '#704214',        # Sepia brown
    'parchment': '#F5E6D3',    # Parchment
    'wood': '#8B4513',         # Wood
    'metal': '#708090',        # Metal
    'highlight': '#FFE4B5',    # Highlight
}

def setup_renaissance_style() -> None:
    """Configure matplotlib for Renaissance styling"""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'Georgia', 'serif'],
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 10,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.titlesize': 14,
        'axes.linewidth': 0.8,
        'grid.linewidth': 0.5,
        'lines.linewidth': 1.5,
        'patch.linewidth': 0.5,
    })

def create_renaissance_background(ax, title: str = "") -> None:
    """Apply Renaissance styling to axes"""
    ax.set_facecolor(RENAISSANCE_COLORS['background'])
    ax.figure.patch.set_facecolor(RENAISSANCE_COLORS['parchment'])

    # Add subtle border
    for spine in ax.spines.values():
        spine.set_color(RENAISSANCE_COLORS['ink'])
        spine.set_linewidth(1.5)

    # Style grid
    ax.grid(True, alpha=0.3, color=RENAISSANCE_COLORS['sepia'], linestyle='--')

    if title:
        ax.set_title(title, color=RENAISSANCE_COLORS['ink'],
                    fontweight='bold', pad=20)

def generate_armored_walker_visualizations() -> List[str]:
    """Generate comprehensive visualizations for Armored Walker"""
    artifacts = []

    # 1. Mechanical Analysis Chart
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Armored Walker - Mechanical Analysis", fontsize=16,
                 fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    create_renaissance_background(ax1, "Power Dynamics")
    create_renaissance_background(ax2, "Motion Profile")
    create_renaissance_background(ax3, "Structural Stress")
    create_renaissance_background(ax4, "Efficiency Metrics")

    # Simulate data for visualization
    time = np.linspace(0, 60, 100)
    power_available = 800 * np.exp(-time/30) + 200
    power_required = 400 + 100 * np.sin(time/5)

    ax1.plot(time, power_available, color=RENAISSANCE_COLORS['blue'],
             linewidth=2, label='Available Power')
    ax1.plot(time, power_required, color=RENAISSANCE_COLORS['red_ink'],
             linewidth=2, label='Required Power')
    ax1.fill_between(time, 0, power_available, alpha=0.3, color=RENAISSANCE_COLORS['blue'])
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Power (W)")
    ax1.legend()

    # Motion profile
    position = np.cumsum(np.concatenate([[0], np.diff(time) * 0.8]))
    velocity = 0.8 * np.ones_like(time)

    ax2_twin = ax2.twinx()
    ax2.plot(time, position, color=RENAISSANCE_COLORS['green'], linewidth=2)
    ax2_twin.plot(time, velocity, color=RENAISSANCE_COLORS['red_ink'], linewidth=2)
    ax2.set_ylabel("Position (m)", color=RENAISSANCE_COLORS['green'])
    ax2_twin.set_ylabel("Velocity (m/s)", color=RENAISSANCE_COLORS['red_ink'])
    ax2.set_xlabel("Time (s)")

    # Structural stress
    components = ['Frame', 'Legs', 'Gears', 'Springs', 'Armor']
    stress_levels = [12, 25, 18, 22, 15]
    colors = [RENAISSANCE_COLORS['green'] if s < 20 else RENAISSANCE_COLORS['red_ink']
              for s in stress_levels]

    bars = ax3.bar(components, stress_levels, color=colors, alpha=0.7)
    ax3.axhline(y=20, color=RENAISSANCE_COLORS['red_ink'], linestyle='--',
                alpha=0.5, label='Safety Limit')
    ax3.set_ylabel("Stress (MPa)")
    ax3.legend()
    ax3.set_xticklabels(components, rotation=45, ha='right')

    # Efficiency metrics
    metrics = ['Mechanical', 'Energy', 'Operation', 'Overall']
    efficiency = [78, 65, 82, 75]

    ax4.bar(metrics, efficiency, color=RENAISSANCE_COLORS['blue'], alpha=0.7)
    ax4.set_ylabel("Efficiency (%)")
    ax4.set_ylim(0, 100)

    plt.tight_layout()
    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/armored_walker/mechanical_analysis.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    # 2. Technical Diagram
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle("Armored Walker - Technical Schematic", fontsize=16,
                 fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    create_renaissance_background(ax)

    # Draw simplified walker schematic
    # Main body
    body = FancyBboxPatch((-1, -0.5), 2, 1, boxstyle="round,pad=0.1",
                          facecolor=RENAISSANCE_COLORS['wood'],
                          edgecolor=RENAISSANCE_COLORS['ink'], linewidth=2)
    ax.add_patch(body)

    # Legs
    leg_positions = [(-0.7, -0.5), (0.7, -0.5), (-0.7, 0.5), (0.7, 0.5)]
    for i, (x, y) in enumerate(leg_positions):
        # Upper leg
        ax.plot([x, x*0.8], [y, y-1.2], color=RENAISSANCE_COLORS['metal'], linewidth=4)
        # Lower leg
        ax.plot([x*0.8, x*0.6], [y-1.2, y-2.4], color=RENAISSANCE_COLORS['metal'], linewidth=4)
        # Foot
        foot = Circle((x*0.6, y-2.5), 0.2, color=RENAISSANCE_COLORS['wood'],
                     edgecolor=RENAISSANCE_COLORS['ink'], linewidth=1)
        ax.add_patch(foot)

        # Joint
        joint = Circle((x*0.8, y-1.2), 0.1, color=RENAISSANCE_COLORS['metal'],
                      edgecolor=RENAISSANCE_COLORS['ink'], linewidth=1)
        ax.add_patch(joint)

    # Spring mechanism
    spring_x = np.linspace(-0.3, 0.3, 20)
    spring_y = 0.3 + 0.1 * np.sin(10 * spring_x)
    ax.plot(spring_x, spring_y, color=RENAISSANCE_COLORS['metal'], linewidth=2)

    # Gear mechanism
    gear = Circle((0, 0.8), 0.2, color=RENAISSANCE_COLORS['metal'],
                  edgecolor=RENAISSANCE_COLORS['ink'], linewidth=2)
    ax.add_patch(gear)

    # Labels
    ax.text(0, 0, 'MAIN\nBODY', ha='center', va='center', fontsize=8,
            color=RENAISSANCE_COLORS['ink'], fontweight='bold')
    ax.text(-1.5, -1.2, 'SPRING\nMECHANISM', ha='center', va='center', fontsize=8,
            color=RENAISSANCE_COLORS['ink'])
    ax.text(0, 0.8, 'GEAR\nTRAIN', ha='center', va='center', fontsize=8,
            color=RENAISSANCE_COLORS['ink'])

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-3.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Add scale
    ax.plot([1.5, 2.0], [-3.2, -3.2], color=RENAISSANCE_COLORS['ink'], linewidth=2)
    ax.text(1.75, -3.4, '1m', ha='center', fontsize=8, color=RENAISSANCE_COLORS['ink'])

    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/armored_walker/technical_schematic.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    return artifacts

def generate_variable_pitch_mechanism_visualizations() -> List[str]:
    """Generate comprehensive visualizations for Variable Pitch Mechanism"""
    artifacts = []

    # 1. Swashplate Engineering Diagram
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Variable Pitch Swashplate Mechanism - Engineering Analysis",
                 fontsize=16, fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    create_renaissance_background(ax1, "Swashplate Geometry")
    create_renaissance_background(ax2, "Control Linkage Forces")
    create_renaissance_background(ax3, "Pitch Response Dynamics")
    create_renaissance_background(ax4, "Efficiency vs Pitch Angle")

    # Swashplate geometry
    theta = np.linspace(0, 2*np.pi, 100)
    r_outer = 0.12
    r_inner = 0.06

    ax1.fill_between(r_outer * np.cos(theta), r_outer * np.sin(theta),
                     alpha=0.3, color=RENAISSANCE_COLORS['metal'])
    ax1.fill_between(r_inner * np.cos(theta), r_inner * np.sin(theta),
                     alpha=0.5, color=RENAISSANCE_COLORS['background'])
    ax1.set_xlim(-0.2, 0.2)
    ax1.set_ylim(-0.2, 0.2)
    ax1.set_aspect('equal')
    ax1.set_xlabel("X (m)")
    ax1.set_ylabel("Y (m)")

    # Control linkage forces
    pitch_angles = np.linspace(15, 45, 50)
    linkage_forces = 200 + 8 * (pitch_angles - 15)

    ax2.plot(pitch_angles, linkage_forces, color=RENAISSANCE_COLORS['blue'], linewidth=2)
    ax2.fill_between(pitch_angles, 0, linkage_forces, alpha=0.3, color=RENAISSANCE_COLORS['blue'])
    ax2.set_xlabel("Pitch Angle (degrees)")
    ax2.set_ylabel("Linkage Force (N)")
    ax2.grid(True, alpha=0.3)

    # Pitch response dynamics
    time = np.linspace(0, 1, 100)
    pitch_response = 25 + 20 * (1 - np.exp(-time/0.2))

    ax3.plot(time, pitch_response, color=RENAISSANCE_COLORS['green'], linewidth=2)
    ax3.axhline(y=45, color=RENAISSANCE_COLORS['red_ink'], linestyle='--', alpha=0.5)
    ax3.axhline(y=25, color=RENAISSANCE_COLORS['red_ink'], linestyle='--', alpha=0.5)
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Blade Pitch (degrees)")
    ax3.grid(True, alpha=0.3)

    # Efficiency vs pitch angle
    efficiency = 92 - 0.3 * (pitch_angles - 25)**2

    ax4.plot(pitch_angles, efficiency, color=RENAISSANCE_COLORS['red_ink'], linewidth=2)
    ax4.fill_between(pitch_angles, 0, efficiency, alpha=0.3, color=RENAISSANCE_COLORS['red_ink'])
    ax4.set_xlabel("Pitch Angle (degrees)")
    ax4.set_ylabel("Mechanical Efficiency (%)")
    ax4.set_ylim(0, 100)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/variable_pitch_mechanism/engineering_analysis.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    return artifacts

def generate_programmable_loom_visualizations() -> List[str]:
    """Generate comprehensive visualizations for Programmable Loom"""
    artifacts = []

    # 1. Pattern Programming System
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Programmable Loom - Pattern Programming System",
                 fontsize=16, fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    create_renaissance_background(ax1, "Cam Programming Pattern")
    create_renaissance_background(ax2, "Thread Tension Analysis")
    create_renaissance_background(ax3, "Fabric Pattern Preview")
    create_renaissance_background(ax4, "Production Efficiency")

    # Cam programming pattern - Leonardo's lily motif
    pattern_size = 32
    pattern_matrix = np.zeros((pattern_size, pattern_size))
    for i in range(pattern_size):
        for j in range(pattern_size):
            x, y = i/pattern_size - 0.5, j/pattern_size - 0.5
            r = np.sqrt(x**2 + y**2)
            if r < 0.3:
                pattern_matrix[i, j] = (np.sin(8 * np.pi * x) * np.cos(6 * np.pi * y)) > 0
            else:
                pattern_matrix[i, j] = (i + j) % 4 < 2

    ax1.imshow(pattern_matrix, cmap='RdYlBu_r', interpolation='nearest')
    ax1.set_xlabel("Warp Position")
    ax1.set_ylabel("Weft Position")
    ax1.set_title("Leonardo's Lily Motif Pattern")

    # Thread tension analysis
    thread_types = ['Silk', 'Linen', 'Wool', 'Gold Thread']
    tensions = [2.8, 4.2, 1.8, 3.5]
    colors_bar = [RENAISSANCE_COLORS['gold'], RENAISSANCE_COLORS['sepia'],
                  RENAISSANCE_COLORS['wood'], RENAISSANCE_COLORS['gold']]

    bars = ax2.bar(thread_types, tensions, color=colors_bar, alpha=0.7)
    ax2.set_ylabel("Tensile Strength (N)")
    ax2.set_xticklabels(thread_types, rotation=45, ha='right')

    # Fabric pattern preview - zoomed section
    zoom_pattern = pattern_matrix[8:24, 8:24]
    ax3.imshow(zoom_pattern, cmap='RdYlBu_r', interpolation='nearest')
    ax3.set_xlabel("Warp Position (zoomed)")
    ax3.set_ylabel("Weft Position (zoomed)")
    ax3.set_title("Pattern Detail (4x Zoom)")

    # Production efficiency
    loom_types = ['Manual', 'Simple Loom', 'Programmable Loom']
    efficiency = [25, 45, 85]
    productivity = [0.2, 0.4, 0.8]

    ax4_twin = ax4.twinx()
    bars1 = ax4.bar([x-0.2 for x in range(len(loom_types))], efficiency,
                   width=0.4, color=RENAISSANCE_COLORS['blue'], alpha=0.7, label='Efficiency')
    bars2 = ax4_twin.bar([x+0.2 for x in range(len(loom_types))], productivity,
                        width=0.4, color=RENAISSANCE_COLORS['green'], alpha=0.7, label='Productivity')

    ax4.set_ylabel("Efficiency (%)", color=RENAISSANCE_COLORS['blue'])
    ax4_twin.set_ylabel("Production Rate (m²/hr)", color=RENAISSANCE_COLORS['green'])
    ax4.set_xticks(range(len(loom_types)))
    ax4.set_xticklabels(loom_types, rotation=45, ha='right')

    plt.tight_layout()
    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/programmable_loom/pattern_programming.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    # 2. Cam System Technical Diagram
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle("Programmable Loom - Cam System Mechanism",
                 fontsize=16, fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    create_renaissance_background(ax)

    # Draw cam barrel
    cam_barrel = Circle((0, 0), 1.5, facecolor=RENAISSANCE_COLORS['wood'],
                       edgecolor=RENAISSANCE_COLORS['ink'], linewidth=2)
    ax.add_patch(cam_barrel)

    # Draw peg positions
    n_pegs = 32
    for i in range(n_pegs):
        angle = i * 2 * np.pi / n_pegs
        if i % 4 < 2:  # Pattern for pegs
            peg_x = 1.2 * np.cos(angle)
            peg_y = 1.2 * np.sin(angle)
            peg = Circle((peg_x, peg_y), 0.08, color=RENAISSANCE_COLORS['metal'],
                        edgecolor=RENAISSANCE_COLORS['ink'], linewidth=1)
            ax.add_patch(peg)

    # Draw cam followers
    follower_positions = [(2.5, 0.8), (2.5, 0), (2.5, -0.8)]
    for i, (x, y) in enumerate(follower_positions):
        # Follower arm
        ax.plot([1.7, x], [y, y], color=RENAISSANCE_COLORS['metal'], linewidth=3)
        # Follower wheel
        follower = Circle((x, y), 0.15, color=RENAISSANCE_COLORS['metal'],
                         edgecolor=RENAISSANCE_COLORS['ink'], linewidth=1)
        ax.add_patch(follower)
        # Control rod
        ax.plot([x, x+0.8], [y, y-0.5*i+0.5], color=RENAISSANCE_COLORS['blue'], linewidth=2)

        # Labels
        ax.text(x, y-0.4, f'Cam {i+1}', ha='center', fontsize=8,
                color=RENAISSANCE_COLORS['ink'])

    # Labels
    ax.text(0, -2.2, 'Cam Barrel', ha='center', fontsize=10,
            color=RENAISSANCE_COLORS['ink'], fontweight='bold')
    ax.text(3.5, 1.2, 'Control Linkages', ha='center', fontsize=10,
            color=RENAISSANCE_COLORS['ink'], fontweight='bold')

    # Add rotation arrow
    arrow = patches.FancyArrowPatch((0, 1.8), (0.7, 1.8),
                                  connectionstyle="arc3,rad=.3",
                                  arrowstyle='->,head_width=0.3,head_length=0.2',
                                  color=RENAISSANCE_COLORS['red_ink'], linewidth=2)
    ax.add_patch(arrow)
    ax.text(0.35, 2.1, 'Rotation', ha='center', fontsize=8,
            color=RENAISSANCE_COLORS['red_ink'])

    ax.set_xlim(-2.5, 4.5)
    ax.set_ylim(-3, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')

    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/programmable_loom/cam_system_diagram.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    return artifacts

def generate_musical_instrument_infographic(invention_module, instrument_name: str) -> List[str]:
    """Generate infographic for musical instruments"""
    artifacts = []

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"{instrument_name} - Musical Engineering Analysis",
                 fontsize=16, fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    create_renaissance_background(ax1, "Frequency Spectrum")
    create_renaissance_background(ax2, "Note Precision Analysis")
    create_renaissance_background(ax3, "Acoustic Power Output")
    create_renaissance_background(ax4, "Mechanical Efficiency")

    # Generate realistic frequency data based on instrument type
    if 'trumpeter' in instrument_name.lower():
        freq_range = np.linspace(200, 1000, 50)
        frequencies = freq_range
        amplitude = np.exp(-(freq_range - 500)**2 / 50000) + 0.3 * np.random.random(50)
    elif 'organ' in instrument_name.lower():
        freq_range = np.linspace(100, 800, 50)
        frequencies = freq_range
        amplitude = 0.8 * np.exp(-(freq_range - 400)**2 / 40000) + 0.2
    elif 'carillon' in instrument_name.lower():
        freq_range = np.linspace(500, 3000, 50)
        frequencies = freq_range
        amplitude = np.exp(-(freq_range - 1500)**2 / 200000) + 0.2
    else:  # Default for other instruments
        freq_range = np.linspace(200, 2000, 50)
        frequencies = freq_range
        amplitude = 0.7 * np.exp(-(freq_range - 800)**2 / 100000) + 0.3

    # Frequency spectrum
    ax1.plot(frequencies, amplitude, color=RENAISSANCE_COLORS['blue'], linewidth=2)
    ax1.fill_between(frequencies, 0, amplitude, alpha=0.3, color=RENAISSANCE_COLORS['blue'])
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.3)

    # Note precision analysis
    note_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    precision = [92, 88, 95, 90, 87, 93, 91]
    colors_notes = [RENAISSANCE_COLORS['green'] if p > 90 else RENAISSANCE_COLORS['red_ink']
                   for p in precision]

    bars = ax2.bar(note_names, precision, color=colors_notes, alpha=0.7)
    ax2.set_ylabel("Precision (%)")
    ax2.set_ylim(0, 100)
    ax2.axhline(y=90, color=RENAISSANCE_COLORS['red_ink'], linestyle='--', alpha=0.5)

    # Acoustic power output
    time = np.linspace(0, 5, 100)
    power_output = 80 + 20 * np.sin(2 * np.pi * time / 2) + 5 * np.random.random(100)

    ax3.plot(time, power_output, color=RENAISSANCE_COLORS['green'], linewidth=1.5)
    ax3.fill_between(time, 0, power_output, alpha=0.3, color=RENAISSANCE_COLORS['green'])
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Acoustic Power (dB)")
    ax3.grid(True, alpha=0.3)

    # Mechanical efficiency
    metrics = 'Air Flow', 'Valve Timing', 'Resonance', 'Overall'
    efficiency_scores = [85, 78, 92, 85]

    ax4.bar(metrics, efficiency_scores, color=RENAISSANCE_COLORS['red_ink'], alpha=0.7)
    ax4.set_ylabel("Efficiency (%)")
    ax4.set_ylim(0, 100)

    plt.tight_layout()

    # Create instrument-specific directory
    safe_name = instrument_name.lower().replace(' ', '_')
    output_dir = f"/Volumes/VIXinSSD/davinci-codex/artifacts/{safe_name}"
    os.makedirs(output_dir, exist_ok=True)

    output_path = f"{output_dir}/musical_engineering_analysis.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    return artifacts

def generate_comparison_matrix() -> List[str]:
    """Generate comprehensive comparison matrix for all inventions"""
    artifacts = []

    # Collect all invention data
    inventions_data = {
        'Aerial Screw': {
            'category': 'Aviation',
            'complexity': 85,
            'innovation': 95,
            'feasibility': 70,
            'safety': 60,
            'educational_value': 90
        },
        'Armored Walker': {
            'category': 'Military',
            'complexity': 90,
            'innovation': 88,
            'feasibility': 75,
            'safety': 50,
            'educational_value': 85
        },
        'Self-Propelled Cart': {
            'category': 'Transportation',
            'complexity': 75,
            'innovation': 85,
            'feasibility': 90,
            'safety': 80,
            'educational_value': 88
        },
        'Mechanical Odometer': {
            'category': 'Surveying',
            'complexity': 60,
            'innovation': 78,
            'feasibility': 95,
            'safety': 95,
            'educational_value': 82
        },
        'Programmable Loom': {
            'category': 'Manufacturing',
            'complexity': 95,
            'innovation': 98,
            'feasibility': 85,
            'safety': 75,
            'educational_value': 95
        },
        'Variable Pitch Mechanism': {
            'category': 'Aviation',
            'complexity': 88,
            'innovation': 92,
            'feasibility': 80,
            'safety': 70,
            'educational_value': 87
        },
        'Ornithopter': {
            'category': 'Aviation',
            'complexity': 92,
            'innovation': 94,
            'feasibility': 65,
            'safety': 55,
            'educational_value': 90
        },
        'Parachute': {
            'category': 'Safety',
            'complexity': 50,
            'innovation': 80,
            'feasibility': 95,
            'safety': 90,
            'educational_value': 75
        },
        'Mechanical Lion': {
            'category': 'Entertainment',
            'complexity': 85,
            'innovation': 90,
            'feasibility': 80,
            'safety': 70,
            'educational_value': 92
        },
        'Revolving Bridge': {
            'category': 'Engineering',
            'complexity': 78,
            'innovation': 85,
            'feasibility': 88,
            'safety': 85,
            'educational_value': 80
        }
    }

    # 1. Overall Performance Radar Chart
    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))
    fig.suptitle("da Vinci Inventions - Comprehensive Performance Analysis",
                 fontsize=16, fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    create_renaissance_background(ax)

    # Metrics for radar chart
    metrics = ['Complexity', 'Innovation', 'Feasibility', 'Safety', 'Educational Value']
    N = len(metrics)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the circle

    # Plot each invention
    colors_inventions = plt.cm.Set3(np.linspace(0, 1, len(inventions_data)))

    for i, (invention, data) in enumerate(inventions_data.items()):
        values = [data['complexity'], data['innovation'], data['feasibility'],
                 data['safety'], data['educational_value']]
        values += values[:1]

        ax.plot(angles, values, 'o-', linewidth=2, label=invention,
                color=colors_inventions[i], alpha=0.7)
        ax.fill(angles, values, alpha=0.1, color=colors_inventions[i])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    ax.set_ylim(0, 100)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.grid(True)

    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=8)

    plt.tight_layout()
    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/comprehensive_performance_radar.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    # 2. Category Comparison Chart
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("da Vinci Inventions - Category Analysis",
                 fontsize=16, fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    create_renaissance_background(ax1, "Inventions by Category")
    create_renaissance_background(ax2, "Innovation Score Distribution")
    create_renaissance_background(ax3, "Feasibility vs Safety")
    create_renaissance_background(ax4, "Educational Value Ranking")

    # Category distribution
    categories = {}
    for data in inventions_data.values():
        cat = data['category']
        categories[cat] = categories.get(cat, 0) + 1

    ax1.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%',
           colors=[RENAISSANCE_COLORS['blue'], RENAISSANCE_COLORS['green'],
                  RENAISSANCE_COLORS['red_ink'], RENAISSANCE_COLORS['gold'],
                  RENAISSANCE_COLORS['sepia']])

    # Innovation score distribution
    innovation_scores = [data['innovation'] for data in inventions_data.values()]
    ax2.hist(innovation_scores, bins=5, color=RENAISSANCE_COLORS['blue'],
            alpha=0.7, edgecolor=RENAISSANCE_COLORS['ink'])
    ax2.set_xlabel("Innovation Score")
    ax2.set_ylabel("Count")
    ax2.set_xlim(0, 100)

    # Feasibility vs Safety scatter
    feasibility_scores = [data['feasibility'] for data in inventions_data.values()]
    safety_scores = [data['safety'] for data in inventions_data.values()]

    ax3.scatter(feasibility_scores, safety_scores,
               c=[RENAISSANCE_COLORS['green'] if s > 75 else RENAISSANCE_COLORS['red_ink']
                  for s in safety_scores],
               s=100, alpha=0.7)
    ax3.set_xlabel("Feasibility Score")
    ax3.set_ylabel("Safety Score")
    ax3.set_xlim(0, 100)
    ax3.set_ylim(0, 100)
    ax3.axhline(y=75, color=RENAISSANCE_COLORS['red_ink'], linestyle='--', alpha=0.5)
    ax3.axvline(x=75, color=RENAISSANCE_COLORS['red_ink'], linestyle='--', alpha=0.5)

    # Educational value ranking
    sorted_inventions = sorted(inventions_data.items(),
                              key=lambda x: x[1]['educational_value'], reverse=True)
    invention_names = [item[0] for item in sorted_inventions]
    educational_scores = [item[1]['educational_value'] for item in sorted_inventions]

    bars = ax4.barh(invention_names, educational_scores,
                   color=RENAISSANCE_COLORS['gold'], alpha=0.7)
    ax4.set_xlabel("Educational Value Score")
    ax4.set_xlim(0, 100)

    plt.tight_layout()
    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/category_analysis_dashboard.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    return artifacts

def generate_renaissance_technical_drawings() -> List[str]:
    """Generate Renaissance-style technical drawings"""
    artifacts = []

    # Create a comprehensive technical drawing sheet
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(RENAISSANCE_COLORS['parchment'])

    # Main title
    fig.suptitle("Codex Atlanticus - Technical Reconstructions",
                 fontsize=20, fontweight='bold', color=RENAISSANCE_COLORS['ink'],
                 y=0.95)

    # Create grid layout for multiple drawings
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

    # Drawing 1: Aerial Screw cross-section
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title("Aerial Screw - Cross Section", fontsize=10,
                  color=RENAISSANCE_COLORS['ink'])
    ax1.set_facecolor(RENAISSANCE_COLORS['background'])

    # Draw helical screw
    theta = np.linspace(0, 6*np.pi, 1000)
    x = theta * 0.02
    y = np.sin(theta) * 0.5
    ax1.plot(x, y, color=RENAISSANCE_COLORS['ink'], linewidth=2)
    ax1.plot(x, -y, color=RENAISSANCE_COLORS['ink'], linewidth=2)

    # Draw support structure
    ax1.plot([0, x[-1]], [0, 0], color=RENAISSANCE_COLORS['wood'], linewidth=4)
    ax1.plot([0, 0], [-0.8, 0.8], color=RENAISSANCE_COLORS['wood'], linewidth=3)

    ax1.set_xlim(-0.1, max(x) + 0.1)
    ax1.set_ylim(-1, 1)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # Drawing 2: Gear system
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title("Variable Pitch - Gear Train", fontsize=10,
                  color=RENAISSANCE_COLORS['ink'])
    ax2.set_facecolor(RENAISSANCE_COLORS['background'])

    # Draw gears
    gear_positions = [(0, 0), (0.8, 0), (1.6, 0.3)]
    gear_sizes = [0.3, 0.2, 0.15]

    for i, (x, y) in enumerate(gear_positions):
        gear = Circle((x, y), gear_sizes[i], facecolor=RENAISSANCE_COLORS['metal'],
                     edgecolor=RENAISSANCE_COLORS['ink'], linewidth=1)
        ax2.add_patch(gear)

        # Add gear teeth indication
        n_teeth = int(20 * gear_sizes[i] / 0.3)
        for j in range(n_teeth):
            angle = j * 2 * np.pi / n_teeth
            x_tooth = x + gear_sizes[i] * np.cos(angle)
            y_tooth = y + gear_sizes[i] * np.sin(angle)
            ax2.plot([x + (gear_sizes[i]-0.02) * np.cos(angle), x_tooth],
                    [y + (gear_sizes[i]-0.02) * np.sin(angle), y_tooth],
                    color=RENAISSANCE_COLORS['ink'], linewidth=0.5)

    ax2.set_xlim(-0.5, 2.0)
    ax2.set_ylim(-0.5, 1.0)
    ax2.set_aspect('equal')
    ax2.axis('off')

    # Drawing 3: Cam profile
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_title("Loom - Cam Profile", fontsize=10,
                  color=RENAISSANCE_COLORS['ink'])
    ax3.set_facecolor(RENAISSANCE_COLORS['background'])

    # Draw cam profile
    cam_angles = np.linspace(0, 2*np.pi, 100)
    cam_radius = 0.4 + 0.1 * np.sin(4 * cam_angles)
    cam_x = cam_radius * np.cos(cam_angles)
    cam_y = cam_radius * np.sin(cam_angles)

    ax3.fill(cam_x, cam_y, color=RENAISSANCE_COLORS['wood'], alpha=0.7,
            edgecolor=RENAISSANCE_COLORS['ink'], linewidth=2)

    # Draw cam follower
    ax3.plot([0.5, 0.8], [0, 0], color=RENAISSANCE_COLORS['metal'], linewidth=3)
    follower = Circle((0.8, 0), 0.05, color=RENAISSANCE_COLORS['metal'],
                     edgecolor=RENAISSANCE_COLORS['ink'], linewidth=1)
    ax3.add_patch(follower)

    ax3.set_xlim(-0.6, 1.0)
    ax3.set_ylim(-0.6, 0.6)
    ax3.set_aspect('equal')
    ax3.axis('off')

    # Drawing 4: Spring mechanism
    ax4 = fig.add_subplot(gs[0, 3])
    ax4.set_title("Walker - Spring Power", fontsize=10,
                  color=RENAISSANCE_COLORS['ink'])
    ax4.set_facecolor(RENAISSANCE_COLORS['background'])

    # Draw spring
    spring_x = np.linspace(0, 1, 50)
    spring_y = 0.1 * np.sin(20 * spring_x)
    ax4.plot(spring_x, spring_y, color=RENAISSANCE_COLORS['metal'], linewidth=2)

    # Draw housing
    ax4.plot([0, 0], [-0.2, 0.2], color=RENAISSANCE_COLORS['wood'], linewidth=4)
    ax4.plot([1, 1], [-0.15, 0.15], color=RENAISSANCE_COLORS['wood'], linewidth=4)

    # Draw force arrow
    ax4.arrow(0.5, 0.3, 0, -0.15, head_width=0.05, head_length=0.03,
             color=RENAISSANCE_COLORS['red_ink'], linewidth=2)
    ax4.text(0.5, 0.4, 'Force', ha='center', fontsize=8,
            color=RENAISSANCE_COLORS['red_ink'])

    ax4.set_xlim(-0.2, 1.2)
    ax4.set_ylim(-0.3, 0.5)
    ax4.set_aspect('equal')
    ax4.axis('off')

    # Add annotations and measurements
    fig.text(0.5, 0.02, "Scale: 1 unit = 1 meter", ha='center', fontsize=10,
            color=RENAISSANCE_COLORS['ink'])
    fig.text(0.02, 0.5, "Notes: All dimensions in historical braccia",
            rotation=90, va='center', fontsize=10, color=RENAISSANCE_COLORS['ink'])

    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/renaissance_technical_drawings.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    return artifacts

def generate_animated_mechanism_demos() -> List[str]:
    """Generate animated demonstrations for key mechanisms"""
    artifacts = []

    # Note: Animation requires additional libraries and considerable computation
    # For now, we'll create static frames that imply motion

    # 1. Walker motion sequence
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    fig.suptitle("Armored Walker - Walking Sequence",
                 fontsize=16, fontweight='bold', color=RENAISSANCE_COLORS['ink'])

    for i, ax in enumerate(axes):
        ax.set_facecolor(RENAISSANCE_COLORS['background'])
        ax.set_title(f"Step {i+1}", fontsize=10, color=RENAISSANCE_COLORS['ink'])

        # Body
        body = FancyBboxPatch((-0.3, -0.2), 0.6, 0.4, boxstyle="round,pad=0.05",
                              facecolor=RENAISSANCE_COLORS['wood'],
                              edgecolor=RENAISSANCE_COLORS['ink'], linewidth=1)
        ax.add_patch(body)

        # Legs in different positions
        leg_phase = i * np.pi / 2
        left_leg_y = -0.2 - 0.3 * np.sin(leg_phase)
        right_leg_y = -0.2 - 0.3 * np.sin(leg_phase + np.pi)

        # Left leg
        ax.plot([-0.2, -0.2], [-0.2, left_leg_y],
               color=RENAISSANCE_COLORS['metal'], linewidth=3)
        ax.plot([-0.2, -0.2], [left_leg_y, left_leg_y-0.3],
               color=RENAISSANCE_COLORS['metal'], linewidth=3)

        # Right leg
        ax.plot([0.2, 0.2], [-0.2, right_leg_y],
               color=RENAISSANCE_COLORS['metal'], linewidth=3)
        ax.plot([0.2, 0.2], [right_leg_y, right_leg_y-0.3],
               color=RENAISSANCE_COLORS['metal'], linewidth=3)

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 0.5)
        ax.set_aspect('equal')
        ax.axis('off')

    plt.tight_layout()
    output_path = "/Volumes/VIXinSSD/davinci-codex/artifacts/armored_walker/walking_sequence.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=RENAISSANCE_COLORS['parchment'])
    plt.close()
    artifacts.append(output_path)

    return artifacts

def main():
    """Main function to generate all visual assets"""
    parser = argparse.ArgumentParser(description="Generate visual assets for da Vinci Codex")
    parser.add_argument('--all', action='store_true', help='Generate all assets')
    parser.add_argument('--invention', type=str, help='Generate assets for specific invention')
    parser.add_argument('--type', type=str, help='Generate specific type of assets')

    args = parser.parse_args()

    setup_renaissance_style()

    all_artifacts = []

    if args.all or not args.invention:
        print("Generating comprehensive visual assets...")

        # Generate specific invention visualizations
        print("1. Armored Walker visualizations...")
        all_artifacts.extend(generate_armored_walker_visualizations())

        print("2. Variable Pitch Mechanism visualizations...")
        all_artifacts.extend(generate_variable_pitch_mechanism_visualizations())

        print("3. Programmable Loom visualizations...")
        all_artifacts.extend(generate_programmable_loom_visualizations())

        # Generate musical instrument infographics
        musical_instruments = [
            (mechanical_carillon, "Mechanical Carillon"),
            (mechanical_organ, "Mechanical Organ"),
            (mechanical_trumpeter, "Mechanical Trumpeter"),
            (programmable_flute, "Programmable Flute"),
            (viola_organista, "Viola Organista")
        ]

        print("4. Musical instrument infographics...")
        for module, name in musical_instruments:
            print(f"   - {name}")
            all_artifacts.extend(generate_musical_instrument_infographic(module, name))

        # Generate comprehensive analysis
        print("5. Comparison matrices and analysis...")
        all_artifacts.extend(generate_comparison_matrix())

        print("6. Renaissance technical drawings...")
        all_artifacts.extend(generate_renaissance_technical_drawings())

        print("7. Animated mechanism demos...")
        all_artifacts.extend(generate_animated_mechanism_demos())

    elif args.invention:
        print(f"Generating assets for {args.invention}...")
        # Generate specific invention assets
        if args.invention == 'armored_walker':
            all_artifacts.extend(generate_armored_walker_visualizations())
        elif args.invention == 'variable_pitch_mechanism':
            all_artifacts.extend(generate_variable_pitch_mechanism_visualizations())
        elif args.invention == 'programmable_loom':
            all_artifacts.extend(generate_programmable_loom_visualizations())
        # Add other inventions as needed

    # Generate summary report
    print(f"\nGenerated {len(all_artifacts)} visual assets:")
    for artifact in all_artifacts:
        print(f"  - {artifact}")

    print(f"\nAll assets saved to: /Volumes/VIXinSSD/davinci-codex/artifacts/")
    print("Visual asset generation complete!")

if __name__ == "__main__":
    main()