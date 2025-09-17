"""Pipeline orchestrations for invention workflows."""

from __future__ import annotations

from typing import Any, Dict

from davinci_codex.inventions import ornithopter as ornithopter_module


def run_ornithopter_pipeline(seed: int = 42, duration_s: float = 20.0) -> Dict[str, Any]:
    """Execute simplified ornithopter pipeline."""
    plan_payload = ornithopter_module.plan()
    sim_result = ornithopter_module.simulate(seed=seed)
    eval_result = ornithopter_module.evaluate()

    summary = {
        "plan": plan_payload,
        "simulation": sim_result,
        "evaluation": eval_result
    }

    return summary