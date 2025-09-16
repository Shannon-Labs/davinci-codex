#!/usr/bin/env python3
"""
da Vinci Codex Quick Start Example

This script demonstrates the basic usage of the da Vinci Codex library,
showing how to list inventions, run simulations, and generate artifacts.
"""

import matplotlib.pyplot as plt

from davinci_codex.pipelines import run_pipeline
from davinci_codex.registry import Registry


def main():
    # Initialize the registry
    registry = Registry()

    print("Welcome to the da Vinci Codex!")
    print("=" * 50)

    # List all available inventions
    print("\nAvailable Inventions:")
    print("-" * 30)
    inventions = registry.list_inventions()
    for inv in inventions:
        print(f"  • {inv.title} ({inv.slug})")
        print(f"    Status: {inv.status}")
        print(f"    {inv.summary}")
        print()

    # Example: Run the aerial screw simulation
    print("\nRunning Aerial Screw Simulation...")
    print("-" * 30)
    aerial_screw = registry.get_invention("aerial_screw")
    if aerial_screw:
        # Get planning assumptions
        plan = aerial_screw.module.plan()
        print(f"Design Parameters: {plan['design']}")

        # Run simulation
        sim_results = aerial_screw.module.simulate(seed=42)
        print(f"Simulation Results: {sim_results['summary']}")

        # Evaluate feasibility
        eval_results = aerial_screw.module.evaluate()
        print(f"Feasibility: {eval_results['feasible']}")
        print(f"Safety Rating: {eval_results['safety']}")

    # Example: Run full pipeline for ornithopter
    print("\nRunning Full Ornithopter Pipeline...")
    print("-" * 30)
    try:
        pipeline_results = run_pipeline("ornithopter", output_dir="artifacts/demo")
        print("Pipeline stages completed:")
        for stage, result in pipeline_results.items():
            print(f"  ✓ {stage}: {result.get('status', 'completed')}")
    except Exception as e:
        print(f"Pipeline demo skipped: {e}")

    # Example: Generate visualization
    print("\nGenerating Sample Visualization...")
    print("-" * 30)

    # Create a simple plot showing invention development status
    statuses = {}
    for inv in inventions:
        status = inv.status
        statuses[status] = statuses.get(status, 0) + 1

    if statuses:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(statuses.keys(), statuses.values())
        ax.set_xlabel("Development Status")
        ax.set_ylabel("Number of Inventions")
        ax.set_title("da Vinci Codex: Invention Development Progress")
        plt.tight_layout()
        plt.savefig("artifacts/status_overview.png")
        print("  ✓ Saved visualization to artifacts/status_overview.png")

    print("\n" + "=" * 50)
    print("Quick start complete! Explore more with:")
    print("  python -m davinci_codex.cli --help")
    print("  make demo")
    print("  jupyter notebook examples/exploration.ipynb")


if __name__ == "__main__":
    main()
