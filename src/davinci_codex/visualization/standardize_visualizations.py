"""
Visualization Standardization Script
====================================

This script standardizes all visualization functions across the da Vinci Codex project
to ensure consistent visual language, color palette, and styling.

Usage:
    python -m davinci_codex.visualization.standardize_visualizations --all
    python -m davinci_codex.visualization.standardize_visualizations --module aerial_screw
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Import our style guide
from .visual_style_guide import (
    RENAISSANCE_COLORS,
    FONT_STYLES,
    PLOT_CONFIG,
    DATA_COLORS
)

# ============================================================================
# STANDARDIZATION PATTERNS
# ============================================================================

# Common matplotlib import patterns to standardize
IMPORT_REPLACEMENTS = {
    r'import matplotlib\.pyplot as plt$': 'import matplotlib.pyplot as plt',
    r'import matplotlib\nmatplotlib\.use\("Agg"\)': 'import matplotlib\nmatplotlib.use("Agg")',
    r'from matplotlib import animation, patches': 'from matplotlib import animation, patches',
}

# Style patterns to replace
STYLE_REPLACEMENTS = {
    # Figure sizes
    r'figsize=\(\d+,\s*\d+\)': lambda match: f"figsize={PLOT_CONFIG['figure_size_standard']}",
    r'figsize=\(\s*14,\s*10\s*\)': lambda match: f"figsize={PLOT_CONFIG['figure_size_complex']}",

    # DPI settings
    r'dpi=\d+': lambda match: f"dpi={PLOT_CONFIG['dpi_publication']}",
    r'dpi=\d+,\s*bbox_inches=\'tight\'': lambda match: f"dpi={PLOT_CONFIG['dpi_publication']}, bbox_inches='tight'",

    # Line widths
    r'linewidth=\d': lambda match: f"linewidth={PLOT_CONFIG['line_width_primary']}",
    r'linewidth=\d\.\d': lambda match: f"linewidth={PLOT_CONFIG['line_width_primary']}",

    # Grid settings
    r'grid\(True.*?\)': "grid(True, linestyle=':', alpha=0.3)",

    # Colors (hardcoded values)
    r'\'blue\'': f"'{DATA_COLORS[0]}'",
    r'\'red\'': f"'{DATA_COLORS[1]}'",
    r'\'green\'': f"'{DATA_COLORS[2]}'",
    r'\'orange\'': f"'{DATA_COLORS[4]}'",
    r'\'black\'": f"'{RENAISSANCE_COLORS['text_primary']}'",

    # Font sizes
    r'fontsize=\d+': 'fontsize=12',
    r'fontsize=\d+\.\d+': 'fontsize=12',
}

# ============================================================================
# FILE PROCESSING FUNCTIONS
# ============================================================================

def find_visualization_files(project_root: Path) -> List[Path]:
    """
    Find all Python files containing visualization code.

    Args:
        project_root: Root directory of the project

    Returns:
        List of Python files with matplotlib/visualization code
    """
    viz_files = []

    # Common patterns that indicate visualization code
    viz_patterns = [
        r'import matplotlib',
        r'import plt',
        r'plt\.figure',
        r'plt\.subplot',
        r'\.savefig',
        r'fig\.savefig',
        r'matplotlib\.use'
    ]

    for py_file in project_root.rglob("*.py"):
        # Skip certain directories
        if any(part in str(py_file) for part in ['.venv', '__pycache__', 'build', 'dist']):
            continue

        try:
            content = py_file.read_text(encoding='utf-8')

            # Check if file contains visualization code
            for pattern in viz_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    viz_files.append(py_file)
                    break
        except (UnicodeDecodeError, PermissionError):
            continue

    return viz_files

def analyze_file_style(file_path: Path) -> Dict[str, List[str]]:
    """
    Analyze a Python file for styling issues and inconsistencies.

    Args:
        file_path: Path to the Python file

    Returns:
        Dictionary of issues found in the file
    """
    issues = {
        'inconsistent_dpi': [],
        'inconsistent_figure_size': [],
        'hardcoded_colors': [],
        'missing_grid': [],
        'inconsistent_font_sizes': [],
        'missing_bbox_inches': []
    }

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check DPI inconsistencies
            if re.search(r'dpi=(22[0-9]|19[0-9]|[0-9]{1,2})', line):
                if f"{PLOT_CONFIG['dpi_publication']}" not in line:
                    issues['inconsistent_dpi'].append(f"Line {i}: {line.strip()}")

            # Check figure size inconsistencies
            if re.search(r'figsize=\(\s*[0-9]+\.?[0-9]*\s*,\s*[0-9]+\.?[0-9]*\s*\)', line):
                if '14, 10' not in line and '12, 8' not in line and '16, 8' not in line and '8, 12' not in line:
                    issues['inconsistent_figure_size'].append(f"Line {i}: {line.strip()}")

            # Check for hardcoded colors
            hardcoded_colors = r"'(red|blue|green|orange|black|yellow|purple|cyan|magenta)'"
            if re.search(hardcoded_colors, line, re.IGNORECASE):
                issues['hardcoded_colors'].append(f"Line {i}: {line.strip()}")

            # Check for missing grid settings
            if 'grid(' in line and 'alpha=' not in line:
                issues['missing_grid'].append(f"Line {i}: {line.strip()}")

            # Check inconsistent font sizes
            if re.search(r'fontsize=([0-9]+\.?[0-9]*)', line):
                fontsize = re.search(r'fontsize=([0-9]+\.?[0-9]*)', line).group(1)
                if fontsize not in ['10', '11', '12', '14', '16']:
                    issues['inconsistent_font_sizes'].append(f"Line {i}: {line.strip()}")

            # Check for missing bbox_inches in savefig
            if 'savefig(' in line and 'bbox_inches=' not in line and 'plt.savefig(' in line:
                issues['missing_bbox_inches'].append(f"Line {i}: {line.strip()}")

    except (UnicodeDecodeError, PermissionError):
        pass

    return issues

def generate_style_imports() -> str:
    """Generate the standardized import block for visualization files."""
    return '''
# Standard visualization imports
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Import da Vinci Codex visual style guide
from ..visualization.visual_style_guide import (
    RENAISSANCE_COLORS,
    FONT_STYLES,
    PLOT_CONFIG,
    apply_renaissance_style,
    create_standard_figure,
    save_figure_with_metadata
)
'''

def update_file_style(file_path: Path, backup: bool = True) -> bool:
    """
    Update a Python file to use the standardized visual style.

    Args:
        file_path: Path to the file to update
        backup: Whether to create a backup of the original file

    Returns:
        True if file was updated, False otherwise
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # Create backup if requested
        if backup:
            backup_path = file_path.with_suffix(f'{file_path.suffix}.backup')
            backup_path.write_text(content, encoding='utf-8')

        # Apply standardizations
        updated_content = content

        # 1. Add standard imports if not present
        if 'from ..visualization.visual_style_guide import' not in content:
            # Find the import section
            lines = updated_content.split('\n')
            import_end = 0

            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    import_end = i + 1
                elif line.strip() == '' and import_end > 0:
                    break

            # Insert standard imports
            if import_end > 0:
                lines.insert(import_end, generate_style_imports())
                updated_content = '\n'.join(lines)

        # 2. Replace style patterns
        for pattern, replacement in STYLE_REPLACEMENTS.items():
            if callable(replacement):
                updated_content = re.sub(pattern, replacement, updated_content)
            else:
                updated_content = re.sub(pattern, replacement, updated_content)

        # 3. Apply more complex transformations

        # Replace figure creation with standard functions
        fig_patterns = [
            (r'fig = plt\.figure\((.*?)\)', lambda m: f"fig, ax = create_standard_figure('standard')"),
            (r'fig, axes = plt\.subplots\((.*?)\)', lambda m: "fig, axes = create_standard_figure('standard')"),
        ]

        for pattern, replacement in fig_patterns:
            updated_content = re.sub(pattern, replacement, updated_content)

        # Replace savefig calls
        savefig_pattern = r'plt\.savefig\((.*?)(?:,\s*dpi=\d+)?(?:,\s*bbox_inches=[\'\"]tight[\'\"])?\)'
        updated_content = re.sub(
            savefig_pattern,
            lambda m: f"save_figure_with_metadata(fig, {m.group(1)})",
            updated_content
        )

        # Write updated content
        if updated_content != original_content:
            file_path.write_text(updated_content, encoding='utf-8')
            return True

        return False

    except (UnicodeDecodeError, PermissionError) as e:
        print(f"Error updating {file_path}: {e}")
        return False

# ============================================================================
# REPORTING FUNCTIONS
# ============================================================================

def generate_consistency_report(project_root: Path) -> Dict:
    """
    Generate a comprehensive report on visualization consistency.

    Args:
        project_root: Root directory of the project

    Returns:
        Dictionary containing the consistency report
    """
    report = {
        'summary': {
            'total_files': 0,
            'files_with_issues': 0,
            'total_issues': 0
        },
        'files': {},
        'issues_by_type': {
            'inconsistent_dpi': 0,
            'inconsistent_figure_size': 0,
            'hardcoded_colors': 0,
            'missing_grid': 0,
            'inconsistent_font_sizes': 0,
            'missing_bbox_inches': 0
        }
    }

    viz_files = find_visualization_files(project_root)
    report['summary']['total_files'] = len(viz_files)

    for file_path in viz_files:
        issues = analyze_file_style(file_path)

        if any(issues.values()):
            report['summary']['files_with_issues'] += 1
            report['files'][str(file_path.relative_to(project_root))] = issues

            # Count issues by type
            for issue_type, issue_list in issues.items():
                report['issues_by_type'][issue_type] += len(issue_list)
                report['summary']['total_issues'] += len(issue_list)

    return report

def print_consistency_report(report: Dict) -> None:
    """Print a formatted consistency report."""
    print("=" * 60)
    print("DA VINCI CODEX VISUAL CONSISTENCY REPORT")
    print("=" * 60)

    summary = report['summary']
    print(f"\n📊 SUMMARY:")
    print(f"   Total files analyzed: {summary['total_files']}")
    print(f"   Files with issues: {summary['files_with_issues']}")
    print(f"   Total issues found: {summary['total_issues']}")

    print(f"\n🔍 ISSUES BY TYPE:")
    for issue_type, count in report['issues_by_type'].items():
        if count > 0:
            print(f"   {issue_type.replace('_', ' ').title()}: {count}")

    if report['files']:
        print(f"\n📁 FILES WITH ISSUES:")
        for file_path, issues in report['files'].items():
            print(f"\n   {file_path}:")
            for issue_type, issue_list in issues.items():
                if issue_list:
                    print(f"     {issue_type.replace('_', ' ').title()}:")
                    for issue in issue_list[:3]:  # Show first 3 issues
                        print(f"       {issue}")
                    if len(issue_list) > 3:
                        print(f"       ... and {len(issue_list) - 3} more")

    print("\n" + "=" * 60)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Standardize visualizations across the da Vinci Codex project"
    )
    parser.add_argument(
        '--project-root',
        type=Path,
        default=Path(__file__).parent.parent.parent.parent,
        help='Root directory of the project'
    )
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Only generate report, do not modify files'
    )
    parser.add_argument(
        '--module',
        type=str,
        help='Standardize specific module only'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files'
    )

    args = parser.parse_args()

    project_root = args.project_root

    if args.module:
        # Process specific module
        module_files = list(project_root.rglob(f"{args.module}.py"))
        if not module_files:
            print(f"Module {args.module} not found!")
            return

        viz_files = module_files
    else:
        # Process all visualization files
        viz_files = find_visualization_files(project_root)

    print(f"Found {len(viz_files)} files with visualization code")

    # Generate and print report
    report = generate_consistency_report(project_root)
    print_consistency_report(report)

    if args.report_only:
        return

    # Ask for confirmation before proceeding
    if report['summary']['total_issues'] > 0:
        response = input(f"\nProceed with standardizing {len(viz_files)} files? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    # Update files
    updated_count = 0
    for file_path in viz_files:
        if update_file_style(file_path, backup=not args.no_backup):
            updated_count += 1
            print(f"✓ Updated: {file_path.relative_to(project_root)}")

    print(f"\n✅ Standardization complete!")
    print(f"   Files updated: {updated_count}")
    print(f"   Files skipped: {len(viz_files) - updated_count}")

    if not args.no_backup:
        print(f"   Backup files created with .backup extension")

if __name__ == "__main__":
    main()