"""
Visual Style Guide for da Vinci Codex Project
============================================

This module provides standardized visualization functions to ensure visual
consistency across all da Vinci Codex graphics, charts, and technical drawings.

Color Palette:
- Renaissance Brown: #8B4513
- Manuscript Beige: #F5F5DC
- Ink Black: #2F4F4F
- Gold Accent: #DAA520
- Peru Accent: #CD853F
- Parchment: #FDF6E3
- Sepia: #704214

Typography:
- Heading Font: Cinzel (serif)
- Body Font: EB Garamond (serif)
- Code Font: JetBrains Mono (monospace)
- Figure Font Size: 12px base, 14px labels, 16px titles

Plot Standards:
- Figure Size: (14, 10) for complex plots, (12, 8) for standard
- DPI: 300 for publication quality, 220 for web
- Line Width: 2.0 for main data, 1.5 for secondary
- Grid: True with alpha=0.3 and linestyle=':'
- Colors: Consistent color mapping across all plots
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Set matplotlib to use non-interactive backend
import matplotlib
matplotlib.use("Agg")

# ============================================================================
# RENAISSANCE COLOR PALETTE
# ============================================================================

RENAISSANCE_COLORS = {
    'primary': '#8B4513',        # Renaissance Brown
    'secondary': '#DAA520',      # Gold Accent
    'accent': '#CD853F',         # Peru Accent
    'background': '#F5F5DC',     # Manuscript Beige
    'surface': '#FDF6E3',        # Parchment
    'text_primary': '#2F4F4F',   # Ink Black
    'text_secondary': '#704214', # Sepia
    'success': '#228B22',        # Forest Green
    'warning': '#FF8C00',        # Dark Orange
    'danger': '#DC143C',         # Crimson
    'info': '#4682B4',           # Steel Blue
    'light': '#FAEBD7',          # Antique White
    'dark': '#8B4513',           # Dark Brown
}

# Standard data visualization colors
DATA_COLORS = [
    '#8B4513',  # Renaissance Brown
    '#DAA520',  # Gold
    '#CD853F',  # Peru
    '#2F4F4F',  # Ink Black
    '#4682B4',  # Steel Blue
    '#228B22',  # Forest Green
    '#DC143C',  # Crimson
    '#704214',  # Sepia
]

# ============================================================================
# TYPOGRAPHY AND TEXT STYLES
# ============================================================================

FONT_STYLES = {
    'title': {
        'fontsize': 16,
        'fontweight': 'bold',
        'color': RENAISSANCE_COLORS['text_primary'],
        'family': 'serif'
    },
    'subtitle': {
        'fontsize': 14,
        'fontweight': 'semibold',
        'color': RENAISSANCE_COLORS['text_primary'],
        'family': 'serif'
    },
    'label': {
        'fontsize': 12,
        'color': RENAISSANCE_COLORS['text_primary'],
        'family': 'serif'
    },
    'annotation': {
        'fontsize': 10,
        'color': RENAISSANCE_COLORS['text_secondary'],
        'family': 'serif'
    },
    'legend': {
        'fontsize': 11,
        'color': RENAISSANCE_COLORS['text_primary'],
        'family': 'serif'
    }
}

# ============================================================================
# PLOT CONFIGURATION STANDARDS
# ============================================================================

PLOT_CONFIG = {
    'figure_size_complex': (14, 10),  # Complex multi-panel plots
    'figure_size_standard': (12, 8),  # Standard single plots
    'figure_size_wide': (16, 8),      # Wide plots for time series
    'figure_size_tall': (8, 12),      # Tall plots for comparisons
    'dpi_publication': 300,           # Publication quality
    'dpi_web': 220,                   # Web optimized
    'line_width_primary': 2.0,        # Main data lines
    'line_width_secondary': 1.5,      # Secondary lines
    'line_width_grid': 0.5,           # Grid lines
    'alpha_primary': 0.8,             # Main elements
    'alpha_secondary': 0.6,           # Secondary elements
    'alpha_fill': 0.3,                # Filled areas
    'grid_alpha': 0.3,                # Grid transparency
    'marker_size': 6,                 # Data point markers
    'marker_size_large': 10,          # Important points
}

# ============================================================================
# STANDARDIZED PLOT FUNCTIONS
# ============================================================================

def apply_renaissance_style(fig: plt.Figure = None, ax: plt.Axes = None) -> None:
    """
    Apply consistent Renaissance styling to matplotlib figure.

    Args:
        fig: matplotlib figure to style (optional)
        ax: matplotlib axes to style (optional)
    """
    if fig is not None:
        fig.patch.set_facecolor(RENAISSANCE_COLORS['surface'])

    if ax is not None:
        ax.set_facecolor(RENAISSANCE_COLORS['background'])
        ax.grid(True, linestyle=':', alpha=PLOT_CONFIG['grid_alpha'], color=RENAISSANCE_COLORS['text_secondary'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(RENAISSANCE_COLORS['text_primary'])
        ax.spines['bottom'].set_color(RENAISSANCE_COLORS['text_primary'])
        ax.tick_params(colors=RENAISSANCE_COLORS['text_primary'])
        ax.xaxis.label.set_color(RENAISSANCE_COLORS['text_primary'])
        ax.yaxis.label.set_color(RENAISSANCE_COLORS['text_primary'])

def create_standard_figure(
    figure_type: str = 'standard',
    title: str = None,
    subtitle: str = None
) -> Tuple[plt.Figure, Union[plt.Axes, np.ndarray]]:
    """
    Create a standardized figure with consistent styling.

    Args:
        figure_type: Type of figure ('standard', 'complex', 'wide', 'tall')
        title: Figure title
        subtitle: Figure subtitle

    Returns:
        Tuple of (figure, axes)
    """
    size_map = {
        'standard': PLOT_CONFIG['figure_size_standard'],
        'complex': PLOT_CONFIG['figure_size_complex'],
        'wide': PLOT_CONFIG['figure_size_wide'],
        'tall': PLOT_CONFIG['figure_size_tall']
    }

    figsize = size_map.get(figure_type, PLOT_CONFIG['figure_size_standard'])
    fig, ax = plt.subplots(figsize=figsize)

    # Apply Renaissance styling
    apply_renaissance_style(fig, ax)

    # Set title if provided
    if title:
        ax.set_title(title, **FONT_STYLES['title'])
        if subtitle:
            ax.set_xlabel(subtitle, **FONT_STYLES['annotation'])

    plt.tight_layout()
    return fig, ax

def create_multi_panel_figure(
    rows: int,
    cols: int,
    title: str = None,
    figure_type: str = 'complex'
) -> Tuple[plt.Figure, np.ndarray]:
    """
    Create a standardized multi-panel figure.

    Args:
        rows: Number of rows
        cols: Number of columns
        title: Overall figure title
        figure_type: Figure size type

    Returns:
        Tuple of (figure, axes array)
    """
    size_map = {
        'standard': PLOT_CONFIG['figure_size_standard'],
        'complex': PLOT_CONFIG['figure_size_complex'],
        'wide': PLOT_CONFIG['figure_size_wide'],
        'tall': PLOT_CONFIG['figure_size_tall']
    }

    figsize = size_map.get(figure_type, PLOT_CONFIG['figure_size_complex'])
    fig, axes = plt.subplots(rows, cols, figsize=figsize)

    # Handle single axis case
    if rows == 1 and cols == 1:
        axes = np.array([axes])
    elif rows == 1 or cols == 1:
        axes = axes.reshape(-1)

    # Apply styling to all subplots
    apply_renaissance_style(fig)
    for ax in axes.flat:
        apply_renaissance_style(ax=ax)

    # Set main title
    if title:
        fig.suptitle(title, fontsize=18, fontweight='bold',
                    color=RENAISSANCE_COLORS['text_primary'], y=0.95)

    plt.tight_layout()
    return fig, axes

def save_figure_with_metadata(
    fig: plt.Figure,
    path: Union[str, Path],
    dpi: int = None,
    metadata: Dict = None
) -> None:
    """
    Save figure with standardized quality and metadata.

    Args:
        fig: matplotlib figure to save
        path: output path
        dpi: resolution (uses standard if None)
        metadata: additional metadata dictionary
    """
    if dpi is None:
        dpi = PLOT_CONFIG['dpi_publication']

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Save with tight bounding box
    fig.savefig(
        path,
        dpi=dpi,
        bbox_inches='tight',
        facecolor=RENAISSANCE_COLORS['surface'],
        edgecolor='none',
        transparent=False
    )

    plt.close(fig)

def create_performance_chart(
    x_data: np.ndarray,
    y_data: Dict[str, np.ndarray],
    x_label: str,
    y_label: str,
    title: str,
    output_path: str,
    threshold_lines: Dict[str, float] = None,
    annotations: List[Dict] = None
) -> None:
    """
    Create standardized performance chart with consistent styling.

    Args:
        x_data: X-axis data
        y_data: Dictionary of {label: y_data} for multiple series
        x_label: X-axis label
        y_label: Y-axis label
        title: Chart title
        output_path: Where to save the figure
        threshold_lines: Dictionary of {label: value} for horizontal lines
        annotations: List of annotation dictionaries
    """
    fig, ax = create_standard_figure('standard', title)

    # Plot data series with consistent colors
    for i, (label, data) in enumerate(y_data.items()):
        color = DATA_COLORS[i % len(DATA_COLORS)]
        ax.plot(x_data, data, label=label, color=color,
                linewidth=PLOT_CONFIG['line_width_primary'])

    # Add threshold lines
    if threshold_lines:
        for label, value in threshold_lines.items():
            ax.axhline(value, color=RENAISSANCE_COLORS['warning'],
                      linestyle='--', alpha=0.7, label=label)

    # Add annotations
    if annotations:
        for annotation in annotations:
            ax.annotate(annotation['text'],
                       xy=annotation['xy'],
                       xytext=annotation.get('xytext', annotation['xy']),
                       arrowprops=dict(arrowstyle='->',
                                     color=RENAISSANCE_COLORS['text_secondary'],
                                     alpha=0.7),
                       fontsize=FONT_STYLES['annotation']['fontsize'])

    # Styling
    ax.set_xlabel(x_label, **FONT_STYLES['label'])
    ax.set_ylabel(y_label, **FONT_STYLES['label'])
    ax.legend(**FONT_STYLES['legend'])

    save_figure_with_metadata(fig, output_path)

def create_comparison_matrix(
    data: np.ndarray,
    labels: List[str],
    title: str,
    output_path: str,
    cmap: str = 'YlOrBr'
) -> None:
    """
    Create standardized comparison heatmap/matrix.

    Args:
        data: 2D data array
        labels: Labels for axes
        title: Chart title
        output_path: Where to save the figure
        cmap: Colormap name (defaults to Renaissance-appropriate brown/gold)
    """
    fig, ax = create_standard_figure('standard', title)

    # Create heatmap with Renaissance colors
    im = ax.imshow(data, cmap=cmap, aspect='auto',
                   interpolation='nearest')

    # Set ticks and labels
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, **FONT_STYLES['label'])
    ax.set_yticklabels(labels, **FONT_STYLES['label'])

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Value', **FONT_STYLES['label'])

    # Rotate x labels if needed
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    save_figure_with_metadata(fig, output_path)

def add_educational_panel(
    ax: plt.Axes,
    title: str,
    content: List[str],
    box_style: str = 'round,pad=0.5'
) -> None:
    """
    Add educational information panel to plot.

    Args:
        ax: matplotlib axes
        title: Panel title
        content: List of content lines
        box_style: bbox style
    """
    text = '\n'.join([f"• {line}" for line in content])

    ax.text(0.05, 0.95, f"{title}\n{'─' * len(title)}\n\n{text}",
            transform=ax.transAxes,
            fontsize=FONT_STYLES['annotation']['fontsize'],
            verticalalignment='top',
            fontfamily='monospace',
            bbox={"boxstyle": box_style,
                  "facecolor": RENAISSANCE_COLORS['light'],
                  "alpha": 0.8,
                  "edgecolor": RENAISSANCE_COLORS['primary']})

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_visual_consistency() -> Dict[str, List[str]]:
    """
    Validate visual consistency across generated artifacts.

    Returns:
        Dictionary of validation results
    """
    issues = []
    warnings = []

    # Check if matplotlib backend is set correctly
    if matplotlib.get_backend() != 'Agg':
        warnings.append("matplotlib backend not set to 'Agg'")

    # Validate color palette consistency
    required_colors = ['primary', 'secondary', 'accent', 'background', 'text_primary']
    for color in required_colors:
        if color not in RENAISSANCE_COLORS:
            issues.append(f"Missing required color: {color}")

    # Validate font styles
    required_fonts = ['title', 'label', 'annotation', 'legend']
    for font in required_fonts:
        if font not in FONT_STYLES:
            issues.append(f"Missing required font style: {font}")

    return {
        'issues': issues,
        'warnings': warnings,
        'status': 'PASS' if not issues else 'FAIL'
    }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_color_palette(n_colors: int = None) -> List[str]:
    """
    Get consistent color palette for plotting.

    Args:
        n_colors: Number of colors needed (returns all if None)

    Returns:
        List of color hex codes
    """
    if n_colors is None:
        return DATA_COLORS
    return DATA_COLORS[:n_colors] + DATA_COLORS[:n_colors-len(DATA_COLORS)]

def apply_manuscript_background(ax: plt.Axes, alpha: float = 0.1) -> None:
    """
    Apply subtle manuscript-style background to axes.

    Args:
        ax: matplotlib axes
        alpha: transparency level
    """
    ax.imshow([[0, 1], [1, 0]],
              extent=[*ax.get_xlim(), *ax.get_ylim()],
              cmap='YlOrBr', alpha=alpha, aspect='auto', zorder=-1)

if __name__ == "__main__":
    # Run validation
    validation = validate_visual_consistency()
    print(f"Visual Style Guide Validation: {validation['status']}")

    if validation['issues']:
        print("Issues found:")
        for issue in validation['issues']:
            print(f"  - {issue}")

    if validation['warnings']:
        print("Warnings:")
        for warning in validation['warnings']:
            print(f"  - {warning}")

    print("Visual Style Guide loaded successfully!")