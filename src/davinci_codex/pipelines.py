"""Pipeline orchestrations tying ANIMA, TVA, and Synthesis outputs together."""

from __future__ import annotations

from importlib import util
from pathlib import Path
from typing import Any, Dict

import numpy as np
import sys

from davinci_codex.inventions import ornithopter as ornithopter_module
from davinci_codex.tva.ornithopter import evaluate_viability


def _load_flapping_model():
    module_path = Path(__file__).resolve().parents[2] / "synthesis" / "ornithopter" / "simulation" / "flapping_model.py"
    spec = util.spec_from_file_location("davinci_codex._ornithopter_flap", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load ornithopter flapping model")
    module = util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def run_ornithopter_pipeline(seed: int = 42, duration_s: float = 20.0) -> Dict[str, Any]:
    """Execute plan → TVA → synthesis simulations for the ornithopter."""
    plan_payload = ornithopter_module.plan()
    tva_result = evaluate_viability()

    flapping_model = _load_flapping_model()
    flapping_state = flapping_model.simulate(duration_s=duration_s, seed=seed)

    lift_peak = float(np.max(flapping_state.lift_N))
    torque_peak = float(np.max(np.abs(flapping_state.torque_nm)))
    control_peak = float(np.max(np.abs(flapping_state.control_torque_nm)))

    summary = {
        "plan": {
            "goals": plan_payload.get("goals", []),
            "assumptions": plan_payload.get("assumptions", {}),
        },
        "tva": {
            "required_power_w": tva_result.required_power_w,
            "power_margin_w": tva_result.power_margin_w,
            "torque_margin_nm": tva_result.torque_margin_nm,
            "fatigue_cycles": tva_result.fatigue_cycles,
            "passes_power": tva_result.passes_power,
            "passes_fatigue": tva_result.passes_fatigue,
        },
        "synthesis": {
            "duration_s": duration_s,
            "peak_lift_N": lift_peak,
            "peak_torque_Nm": torque_peak,
            "peak_control_torque_Nm": control_peak,
            "energy_used_wh": flapping_state.energy_wh,
            "estimated_endurance_min": flapping_state.endurance_min,
            "artifacts": {
                "csv": str(Path("artifacts") / "ornithopter" / "synthesis_sim" / "flapping_state.csv"),
                "summary": str(Path("artifacts") / "ornithopter" / "synthesis_sim" / "summary.txt"),
            },
        },
    }

    return summary
