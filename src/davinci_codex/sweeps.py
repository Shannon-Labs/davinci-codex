"""Parameter sweep and uncertainty quantification utilities."""

from __future__ import annotations

import csv
import json
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .cache import alias_output_path, ensure_cached_result
from .registry import InventionSpec

_NUMERIC_TYPES = (int, float)


@dataclass
class SweepResult:
    """Holds flattened metrics for a single simulation run."""

    seed: int
    fidelity: str | None
    metrics: Dict[str, float]
    artifact_path: Path


def _invoke_simulation(
    spec: InventionSpec,
    *,
    seed: int,
    fidelity: str | None,
) -> Dict[str, Any]:
    """Invoke the invention's simulation with optional fidelity control."""
    simulate = spec.module.simulate
    kwargs: Dict[str, Any] = {"seed": seed}
    if fidelity is not None:
        kwargs["fidelity"] = fidelity
    try:
        return simulate(**kwargs)  # type: ignore[misc]
    except TypeError:
        # Retry without fidelity for backwards compatibility
        kwargs.pop("fidelity", None)
        return simulate(**kwargs)  # type: ignore[misc]


def _flatten_metrics(payload: Any, prefix: str = "") -> Dict[str, float]:
    """Extract numeric metrics from nested dictionaries."""
    metrics: Dict[str, float] = {}

    if isinstance(payload, dict):
        for key, value in payload.items():
            nested_key = f"{prefix}.{key}" if prefix else str(key)
            metrics.update(_flatten_metrics(value, nested_key))
        return metrics

    if isinstance(payload, list):
        for index, value in enumerate(payload):
            nested_key = f"{prefix}[{index}]" if prefix else f"[{index}]"
            metrics.update(_flatten_metrics(value, nested_key))
        return metrics

    if isinstance(payload, _NUMERIC_TYPES):
        metrics[prefix] = float(payload)
        return metrics

    if isinstance(payload, bool):
        metrics[prefix] = 1.0 if payload else 0.0
        return metrics

    return metrics


def _write_run_artifact(path: Path, result: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
    alias = alias_output_path(path)
    if alias is not None:
        alias.parent.mkdir(parents=True, exist_ok=True)
        with alias.open("w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2, sort_keys=True)


def _write_csv(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        return
    fieldnames = sorted({key for row in rows for key in row})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    alias = alias_output_path(path)
    if alias is not None:
        alias.parent.mkdir(parents=True, exist_ok=True)
        with alias.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


def _aggregate_metrics(results: List[SweepResult]) -> Dict[str, Dict[str, float]]:
    aggregates: Dict[str, Dict[str, float]] = {}
    if not results:
        return aggregates

    metric_names = {name for result in results for name in result.metrics}

    for name in sorted(metric_names):
        series = [r.metrics[name] for r in results if name in r.metrics]
        if not series:
            continue
        aggregates[name] = {
            "mean": statistics.fmean(series),
            "stdev": statistics.pstdev(series) if len(series) > 1 else 0.0,
            "minimum": min(series),
            "maximum": max(series),
            "samples": len(series),
        }

    return aggregates


def run_parameter_sweep(
    spec: InventionSpec,
    *,
    fidelity: str | None,
    seeds: Iterable[int],
    label: str | None = None,
    reuse_cache: bool = True,
) -> Dict[str, Any]:
    """Execute a sweep of simulations and collect summary statistics."""
    seeds = list(dict.fromkeys(seeds))  # Preserve order but remove duplicates
    sweep_payload = {
        "slug": spec.slug,
        "fidelity": fidelity,
        "seeds": seeds,
        "label": label,
    }

    cache_entry, cache_hit = ensure_cached_result(spec.slug, sweep_payload, label="sweep")
    summary_json = cache_entry.path / "summary.json"

    if reuse_cache and cache_hit and summary_json.exists():
        with summary_json.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    run_results: List[SweepResult] = []
    for seed in seeds:
        run_payload = {
            "seed": seed,
            "fidelity": fidelity,
        }
        run_cache_entry, run_hit = ensure_cached_result(spec.slug, run_payload, label="sweep-run")
        run_artifact = run_cache_entry.path / "result.json"

        if reuse_cache and run_hit and run_artifact.exists():
            with run_artifact.open("r", encoding="utf-8") as handle:
                result = json.load(handle)
        else:
            result = _invoke_simulation(spec, seed=seed, fidelity=fidelity)
            _write_run_artifact(run_artifact, result)
            run_cache_entry.write_metadata({"seed": seed, "fidelity": fidelity})

        metrics = _flatten_metrics(result)
        run_results.append(
            SweepResult(
                seed=seed,
                fidelity=fidelity,
                metrics=metrics,
                artifact_path=run_artifact,
            )
        )

    aggregates = _aggregate_metrics(run_results)

    summary = {
        "slug": spec.slug,
        "fidelity": fidelity,
        "seeds": seeds,
        "label": label,
        "runs": [
            {
                "seed": result.seed,
                "fidelity": result.fidelity,
                "artifact": str(result.artifact_path),
                "metrics": result.metrics,
            }
            for result in run_results
        ],
        "aggregates": aggregates,
    }

    cache_entry.write_metadata(sweep_payload)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    with summary_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
    alias_summary = alias_output_path(summary_json)
    if alias_summary is not None:
        alias_summary.parent.mkdir(parents=True, exist_ok=True)
        with alias_summary.open("w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2, sort_keys=True)

    csv_rows: List[Dict[str, Any]] = []
    for result in run_results:
        row: Dict[str, Any] = {"seed": result.seed}
        row.update(result.metrics)
        csv_rows.append(row)

    _write_csv(cache_entry.path / "runs.csv", csv_rows)

    agg_rows = [
        {
            "metric": name,
            "mean": values["mean"],
            "stdev": values["stdev"],
            "min": values["minimum"],
            "max": values["maximum"],
            "samples": values["samples"],
        }
        for name, values in aggregates.items()
    ]
    _write_csv(cache_entry.path / "summary.csv", agg_rows)

    return summary
