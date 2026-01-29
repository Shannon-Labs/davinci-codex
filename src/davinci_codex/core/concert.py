"""Master performance pipeline -- compose, adapt, render, and visualise."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from ..artifacts import ensure_artifact_dir
from .audio import render_score_to_wav


def _import_renaissance_submodule(name: str) -> Any:
    """Import a renaissance_music submodule, working around the circular
    import in ``renaissance_music.__init__`` -> ``.cli`` -> ``data/...`` ->
    ``renaissance_music.models``.  If the first import attempt fails we
    retry once, which succeeds because the partially-cached module satisfies
    the circular reference on the second pass.
    """
    full = f"davinci_codex.renaissance_music.{name}"
    if full in sys.modules:
        return sys.modules[full]
    try:
        return importlib.import_module(full)
    except ImportError:
        # The first attempt populates partial caches; retry usually works.
        return importlib.import_module(full)


def _build_default_assignments() -> Dict[int, Any]:
    """Build default voice-to-instrument mapping."""
    models = _import_renaissance_submodule("models")
    IT = models.InstrumentType
    return {
        0: IT.VIOLA_ORGANISTA,
        1: IT.MECHANICAL_ORGAN,
        2: IT.PROGRAMMABLE_FLUTE,
        3: IT.MECHANICAL_CARILLON,
        4: IT.MECHANICAL_TRUMPETER,
        5: IT.MECHANICAL_DRUM,
    }


def perform_concert(
    form: str = "pavane",
    mode: str = "dorian",
    seed: int = 0,
    measures: int = 16,
    tempo_bpm: float = 80.0,
    reverb_wet: float = 0.2,
    sample_rate: int = 44100,
    output_dir: Optional[Path] = None,
    instrument_assignments: Optional[Dict[int, Any]] = None,
    visualize: bool = True,
) -> Dict[str, Any]:
    """Run the full concert pipeline: compose, adapt, render, and visualise.

    Args:
        form: Musical form name (e.g. "pavane", "galliard", "basse_danse").
        mode: Church mode name (e.g. "dorian", "mixolydian").
        seed: Random seed for deterministic composition.
        measures: Number of measures to generate.
        tempo_bpm: Tempo in beats per minute.
        reverb_wet: Reverb wet/dry mix (0..1). 0 disables reverb.
        sample_rate: Audio sample rate.
        output_dir: Directory for artifacts. Defaults to artifacts/mechanical_concert/demo.
        instrument_assignments: Custom voice-to-instrument mapping.
        visualize: Whether to generate visualization PNGs.

    Returns:
        Dictionary with pipeline metadata, artifact paths, and score summary.
    """
    # Import renaissance_music submodules with circular-import resilience
    models_mod = _import_renaissance_submodule("models")
    composition_mod = _import_renaissance_submodule("composition")
    integration_mod = _import_renaissance_submodule("integration")

    MusicalForm = models_mod.MusicalForm
    RenaissanceMode = models_mod.RenaissanceMode
    RenaissanceCompositionGenerator = composition_mod.RenaissanceCompositionGenerator
    MechanicalEnsembleIntegrator = integration_mod.MechanicalEnsembleIntegrator

    # Resolve enums
    form_map: Dict[str, MusicalForm] = {f.value: f for f in MusicalForm}
    musical_form = form_map.get(form, MusicalForm.PAVANE)

    mode_map: Dict[str, RenaissanceMode] = {m.value: m for m in RenaissanceMode}
    musical_mode = mode_map.get(mode, RenaissanceMode.DORIAN)

    assignments = instrument_assignments or _build_default_assignments()

    # Ensure output directory
    if output_dir is None:
        output_dir = ensure_artifact_dir("mechanical_concert", subdir="demo")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    artifacts: List[str] = []

    # ------------------------------------------------------------------
    # Step 1: Compose a Renaissance score
    # ------------------------------------------------------------------
    composer = RenaissanceCompositionGenerator()
    score = composer.generate_composition(
        form=musical_form,
        mode=musical_mode,
        instrument_assignments=assignments,
        measures=measures,
        seed=seed,
    )
    score.tempo_bpm = tempo_bpm

    # ------------------------------------------------------------------
    # Step 2: Adapt for mechanical constraints
    # ------------------------------------------------------------------
    integrator = MechanicalEnsembleIntegrator()
    adaptation = integrator.adapt_score_for_ensemble(score, assignments)
    adapted_score = adaptation.adapted_score

    # ------------------------------------------------------------------
    # Step 3: Convert to ensemble event format (with slug + duration_s)
    # ------------------------------------------------------------------
    ensemble_events = integrator.convert_to_ensemble_format(
        adapted_score, assignments, tempo_bpm=tempo_bpm, measures=measures,
    )

    # Save ensemble score JSON
    score_json_path = output_dir / "concert_score.json"
    _save_score_json(
        score_json_path, ensemble_events, tempo_bpm, measures, form, mode, seed,
    )
    artifacts.append(str(score_json_path))

    # ------------------------------------------------------------------
    # Step 4: Render audio with physics-based timbres + reverb
    # ------------------------------------------------------------------
    wav_path = output_dir / "concert_audio.wav"
    render_score_to_wav(
        ensemble_events,
        tempo_bpm=tempo_bpm,
        beats_per_measure=4,
        output_path=wav_path,
        sample_rate=sample_rate,
        use_timbres=True,
        reverb_wet=reverb_wet,
    )
    artifacts.append(str(wav_path))

    # ------------------------------------------------------------------
    # Step 5: Generate visualisations
    # ------------------------------------------------------------------
    if visualize:
        try:
            from .concert_viz import plot_score_roll, plot_spectrogram, plot_waveform

            waveform_path = output_dir / "waveform.png"
            plot_waveform(wav_path, waveform_path)
            artifacts.append(str(waveform_path))

            spectrogram_path = output_dir / "spectrogram.png"
            plot_spectrogram(wav_path, spectrogram_path)
            artifacts.append(str(spectrogram_path))

            score_roll_path = output_dir / "score_roll.png"
            plot_score_roll(ensemble_events, score_roll_path)
            artifacts.append(str(score_roll_path))
        except Exception:
            pass  # Visualization is optional -- don't fail the pipeline

    # ------------------------------------------------------------------
    # Build result summary
    # ------------------------------------------------------------------
    instrument_names = sorted({
        str(event.get("slug", slug))
        for slug, events in ensemble_events.items()
        for event in events
        if "slug" in event
    } | set(ensemble_events.keys()))

    total_events = sum(len(evts) for evts in ensemble_events.values())

    return {
        "artifacts": artifacts,
        "form": form,
        "mode": mode,
        "seed": seed,
        "measures": measures,
        "tempo_bpm": tempo_bpm,
        "reverb_wet": reverb_wet,
        "sample_rate": sample_rate,
        "instruments": instrument_names,
        "total_events": total_events,
        "adaptation_success": adaptation.adaptation_success,
        "adaptation_log": adaptation.adaptation_log[:20],
    }


def _save_score_json(
    path: Path,
    ensemble_events: Dict[str, Any],
    tempo_bpm: float,
    measures: int,
    form: str,
    mode: str,
    seed: int,
) -> None:
    """Persist the ensemble score as JSON."""

    def _default(obj: Any) -> Any:
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    payload = {
        "tempo_bpm": tempo_bpm,
        "measures": measures,
        "beats_per_measure": 4,
        "form": form,
        "mode": mode,
        "seed": seed,
        "score": ensemble_events,
    }
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=_default)
