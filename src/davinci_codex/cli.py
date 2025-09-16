"""Command-line interface for the da Vinci Codex project."""

from __future__ import annotations

import json
from typing import List, Optional

import typer

from . import __version__
from .pipelines import run_ornithopter_pipeline
from .registry import InventionSpec, get_invention, list_inventions

app = typer.Typer(help="Interact with da Vinci Codex invention modules.")


def _resolve_inventions(slug: Optional[str], all_flag: bool) -> List[InventionSpec]:
    if slug and all_flag:
        raise typer.BadParameter("Provide either --slug or --all, not both.")
    if slug:
        return [get_invention(slug)]
    if all_flag or not slug:
        return list_inventions()
    return []


@app.callback()
def main(version: bool = typer.Option(False, "--version", is_eager=True, help="Show version and exit.")) -> None:
    if version:
        typer.echo(__version__)
        raise typer.Exit()


@app.command("list")
def list_command() -> None:
    """List available inventions."""
    specs = list_inventions()
    if not specs:
        typer.echo("No inventions registered yet.")
        raise typer.Exit(code=1)
    for spec in specs:
        typer.echo(f"{spec.slug}: {spec.title} [{spec.status}] — {spec.summary}")


@app.command()
def plan(slug: Optional[str] = typer.Option(None, help="Slug of the invention to inspect.")) -> None:
    """Print planning assumptions for an invention."""
    specs = _resolve_inventions(slug, all_flag=slug is None)
    for spec in specs:
        typer.echo(f"# {spec.title} ({spec.slug})")
        payload = spec.module.plan()
        typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command()
def simulate(
    slug: Optional[str] = typer.Option(None, help="Slug of the invention to simulate."),
    seed: int = typer.Option(0, help="Random seed for deterministic simulations."),
) -> None:
    """Run simulations and persist artifacts for the selected inventions."""
    specs = _resolve_inventions(slug, all_flag=slug is None)
    for spec in specs:
        typer.echo(f"# Simulating {spec.title} ({spec.slug})")
        results = spec.module.simulate(seed)
        typer.echo(json.dumps(results, indent=2, sort_keys=True))


@app.command()
def build(
    slug: Optional[str] = typer.Option(None, help="Slug of the invention to build."),
    all: bool = typer.Option(False, "--all", help="Build CAD/scripts for all inventions."),
) -> None:
    """Generate CAD or other build artifacts."""
    specs = _resolve_inventions(slug, all_flag=all or slug is None)
    for spec in specs:
        typer.echo(f"# Building {spec.title} ({spec.slug})")
        spec.module.build()
        typer.echo("done")


@app.command()
def evaluate(slug: Optional[str] = typer.Option(None, help="Slug of the invention to evaluate.")) -> None:
    """Review feasibility and ethics outputs."""
    specs = _resolve_inventions(slug, all_flag=slug is None)
    for spec in specs:
        typer.echo(f"# Evaluating {spec.title} ({spec.slug})")
        payload = spec.module.evaluate()
        typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command()
def demo(slug: Optional[str] = typer.Option(None, help="Slug of the invention to demo.")) -> None:
    """Run a lightweight simulation + evaluation demo."""
    specs = _resolve_inventions(slug, all_flag=slug is None)
    for spec in specs:
        typer.echo(f"# Demo {spec.title} ({spec.slug})")
        sim = spec.module.simulate(0)
        eval_payload = spec.module.evaluate()
        typer.echo(json.dumps({"simulate": sim, "evaluate": eval_payload}, indent=2, sort_keys=True))


@app.command("pipeline")
def pipeline_command(
    slug: Optional[str] = typer.Option(None, help="Slug of the invention to run as a full pipeline."),
    seed: int = typer.Option(42, help="Random seed for stochastic steps."),
    duration: float = typer.Option(20.0, help="Simulation duration in seconds for synthesis stage."),
) -> None:
    """Run multi-stage pipelines (currently ornithopter-only)."""
    specs = _resolve_inventions(slug, all_flag=slug is None)
    for spec in specs:
        typer.echo(f"# Pipeline {spec.title} ({spec.slug})")
        if spec.slug != "ornithopter":
            typer.echo("Pipeline automation not yet implemented for this invention.")
            continue
        report = run_ornithopter_pipeline(seed=seed, duration_s=duration)
        typer.echo(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    app()
