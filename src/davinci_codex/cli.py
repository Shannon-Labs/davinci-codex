"""Command-line interface for the da Vinci Codex project."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import typer

from . import __version__
from .artifacts import ensure_artifact_dir
from .inventions import mechanical_ensemble as mechanical_ensemble_module
from .pipelines import run_ornithopter_pipeline
from .registry import InventionSpec, get_invention, list_inventions
from .sweeps import run_parameter_sweep

app = typer.Typer(help="Interact with da Vinci Codex invention modules.")


def _validation_root() -> Path:
    return Path(__file__).resolve().parents[2] / "validation"


def _collect_validation_status() -> List[dict[str, str]]:
    status: List[dict[str, str]] = []
    root = _validation_root()
    if not root.exists():
        return status
    for case_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        case_file = case_dir / "case.yaml"
        report = case_dir / "report.md"
        assets_ok = case_file.exists() and report.exists()
        missing_assets = []
        if assets_ok:
            try:
                import yaml  # local import to avoid heavy dependency during CLI help

                with case_file.open(encoding="utf-8") as handle:
                    data = yaml.safe_load(handle) or {}
                assets = data.get("validation_assets", {})
                for value in assets.values():
                    if isinstance(value, str):
                        if not (case_dir / value).exists():
                            missing_assets.append(value)
                    elif isinstance(value, list):
                        for entry in value:
                            if isinstance(entry, str) and not (case_dir / entry).exists():
                                missing_assets.append(entry)
            except Exception as exc:  # pragma: no cover - defensive
                missing_assets.append(f"yaml-error: {exc}")
        status.append(
            {
                "name": case_dir.name,
                "case": "✓" if case_file.exists() else "✗",
                "report": "✓" if report.exists() else "✗",
                "assets": "✓" if not missing_assets else f"missing: {', '.join(missing_assets)}",
            }
        )
    return status


def _load_validation_metrics(case: str, filename: str) -> Optional[Dict[str, str]]:
    """Load a simple metric table from a validation case CSV."""
    case_dir = _validation_root() / case
    path = case_dir / filename
    if not path.exists():
        return None
    metrics: Dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            metric = row.get("metric")
            value = row.get("value")
            units = row.get("units", "")
            if not metric or value is None:
                continue
            label = value if not units else f"{value} {units}"
            metrics[metric] = label.strip()
    return metrics or None


def _resolve_inventions(slug: Optional[str], all_flag: bool) -> List[InventionSpec]:
    if slug and all_flag:
        raise typer.BadParameter("Provide either --slug or --all, not both.")
    if slug:
        return [get_invention(slug)]
    if all_flag or not slug:
        return list_inventions()
    return []


def _load_acceptance_targets(slug: str) -> Dict[str, object]:
    path = Path("sims") / slug / "acceptance.yaml"
    if not path.exists():
        return {}
    import yaml  # local, heavy dependency optional

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        return {}
    return {str(key): value for key, value in data.items()}


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
    fidelity: Optional[str] = typer.Option(None, help="Optional fidelity level (e.g. educational, advanced)."),
) -> None:
    """Run simulations and persist artifacts for the selected inventions."""
    specs = _resolve_inventions(slug, all_flag=slug is None)
    for spec in specs:
        typer.echo(f"# Simulating {spec.title} ({spec.slug})")
        kwargs: Dict[str, object] = {"seed": seed}
        if fidelity:
            kwargs["fidelity"] = fidelity
        try:
            results = spec.module.simulate(**kwargs)  # type: ignore[misc]
        except TypeError:
            kwargs.pop("fidelity", None)
            results = spec.module.simulate(**kwargs)  # type: ignore[misc]
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
        payload: Dict[str, object] = {"simulate": sim, "evaluate": eval_payload}
        if spec.slug == "mechanical_odometer":
            validation = _load_validation_metrics(
                "mechanical_odometer_contact", "contact_summary.csv"
            )
            if validation:
                payload["validation"] = validation
        if spec.slug == "parachute":
            validation = _load_validation_metrics("parachute_drop", "descent_summary.csv")
            if validation:
                payload["validation"] = validation
        typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command()
def sweep(
    slug: Optional[str] = typer.Option(None, help="Slug of the invention to sweep."),
    runs: int = typer.Option(5, help="Number of seeds to sample when explicit seeds are not provided."),
    seed: Optional[List[int]] = typer.Option(None, "--seed", help="Explicit seed values to run."),
    fidelity: Optional[str] = typer.Option(None, help="Optional fidelity level."),
    label: Optional[str] = typer.Option(None, help="Optional label used for cache grouping."),
    reuse_cache: bool = typer.Option(True, help="Skip reruns when cached results are available."),
) -> None:
    """Run repeated simulations and summarise aggregated statistics."""
    if not slug:
        raise typer.BadParameter("Provide --slug to select an invention for sweeping.")
    spec = get_invention(slug)

    if seed:
        seeds: Sequence[int] = [int(value) for value in seed]
    else:
        seeds = list(range(runs))

    typer.echo(f"# Sweep {spec.title} ({spec.slug})")
    summary = run_parameter_sweep(
        spec,
        fidelity=fidelity,
        seeds=seeds,
        label=label,
        reuse_cache=reuse_cache,
    )
    typer.echo(json.dumps(summary, indent=2, sort_keys=True))


@app.command()
def validate(
    slug: Optional[str] = typer.Option(None, help="Slug of the invention to validate."),
    fidelity: Optional[str] = typer.Option(None, help="Optional fidelity level for evaluation."),
) -> None:
    """Evaluate acceptance targets and record validation summaries."""
    specs = _resolve_inventions(slug, all_flag=slug is None)
    for spec in specs:
        typer.echo(f"# Validating {spec.title} ({spec.slug})")
        evaluation_kwargs: Dict[str, object] = {}
        if fidelity:
            evaluation_kwargs["fidelity"] = fidelity
        try:
            evaluation = spec.module.evaluate(**evaluation_kwargs)  # type: ignore[misc]
        except TypeError:
            evaluation = spec.module.evaluate()  # type: ignore[misc]

        meets_targets: Dict[str, bool] = {}
        metrics: Dict[str, float] = {}

        if isinstance(evaluation, dict):
            validation_block = evaluation.get("validation")
            if isinstance(validation_block, dict):
                meets = validation_block.get("meets_targets")
                if isinstance(meets, dict):
                    meets_targets = {key: bool(value) for key, value in meets.items()}
                candidate_metrics = validation_block.get("metrics")
                if isinstance(candidate_metrics, dict):
                    for key, value in candidate_metrics.items():
                        if isinstance(value, (int, float)):
                            metrics[key] = float(value)
        overall_pass = all(meets_targets.values()) if meets_targets else False

        summary = {
            "slug": spec.slug,
            "overall_pass": overall_pass,
            "meets_targets": meets_targets,
            "metrics": metrics,
            "targets": _load_acceptance_targets(spec.slug),
        }
        typer.echo(json.dumps(summary, indent=2, sort_keys=True))

        artifact_dir = ensure_artifact_dir(spec.slug, subdir="validation")
        with (artifact_dir / "validation_summary.json").open("w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2, sort_keys=True)


@app.command("gallery")
def gallery_command() -> None:
    """Regenerate static simulation gallery assets."""
    from scripts.generate_simulation_gallery import (
        main as gallery_main,  # pylint: disable=import-outside-toplevel
    )

    typer.echo("# Regenerating gallery")
    gallery_main()
    typer.echo("done")


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


@app.command("ensemble-demo")
def ensemble_demo_command(
    seed: int = typer.Option(0, help="Random seed for deterministic playback."),
    tempo: float = typer.Option(96.0, "--tempo", help="Target tempo in beats per minute."),
    measures: int = typer.Option(4, "--measures", help="Number of measures to generate."),
) -> None:
    """Generate a pseudo-score for the full mechanical ensemble."""

    result = mechanical_ensemble_module.demo(seed=seed, tempo_bpm=tempo, measures=measures)
    typer.echo(json.dumps(result, indent=2, sort_keys=True))


@app.command("validation-status")
def validation_status() -> None:
    """Summarise validation evidence across cases."""

    status = _collect_validation_status()
    if not status:
        typer.echo("No validation cases recorded yet. Populate the `validation/` directory.")
        raise typer.Exit(code=1)
    header = f"{'Case':<28}{'case.yaml':<12}{'report.md':<12}assets"
    typer.echo(header)
    typer.echo("-" * len(header))
    for entry in status:
        typer.echo(f"{entry['name']:<28}{entry['case']:<12}{entry['report']:<12}{entry['assets']}")


if __name__ == "__main__":
    app()
