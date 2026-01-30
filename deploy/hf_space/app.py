from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import gradio as gr
import numpy as np

from davinci_codex.registry import get_invention

HERO_SLUGS = {
    "Parachute": "parachute",
    "Aerial Screw": "aerial_screw",
    "Mechanical Lion": "mechanical_lion",
}


def _coerce(value: Any) -> Any:
    """Convert numpy and path-like objects to JSON-serializable forms."""
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    return value


def run_simulation(slug: str, seed: int, fidelity: str) -> Dict[str, Any]:
    spec = get_invention(slug)
    simulate_kwargs: Dict[str, Any] = {"seed": seed}
    if fidelity:
        simulate_kwargs["fidelity"] = fidelity
    results = spec.module.simulate(**simulate_kwargs)  # type: ignore[arg-type]
    # Ensure results are JSON-serializable for Gradio JSON/code components
    return json.loads(json.dumps(results, default=_coerce))


def format_summary(results: Dict[str, Any]) -> str:
    summary = {
        "performance": results.get("performance_metrics")
        or results.get("performance")
        or results.get("results"),
        "highlights": results.get("educational_insights") or results.get("summary"),
    }
    return json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False)


def make_tab(slug: str) -> gr.Tab:
    with gr.Tab(slug.title()):
        seed = gr.Number(value=0, precision=0, label="Seed")
        fidelity = gr.Textbox(value="educational", label="Fidelity (optional)", placeholder="educational")
        json_output = gr.JSON(label="Simulation Summary")
        pretty_output = gr.Code(label="Highlights", language="json")

        def _run(seed_value: float, fidelity_value: str, hero_slug: str) -> tuple[Dict[str, Any], str]:
            results = run_simulation(hero_slug, int(seed_value), fidelity_value.strip())
            return results, format_summary(results)

        run_button = gr.Button("Run Simulation")
        run_button.click(
            fn=_run,
            inputs=[seed, fidelity, gr.State(HERO_SLUGS[slug.title()])],
            outputs=[json_output, pretty_output],
        )

    return gr.Tab


def main() -> gr.Blocks:
    with gr.Blocks(title="da Vinci Codex Demo") as demo:
        gr.Markdown(
            """
            # da Vinci Codex Hero Demos

            Explore Leonardo's inventions with deterministic, educational simulations.
            """
        )
        with gr.Tabs():
            for label, slug in HERO_SLUGS.items():
                with gr.Tab(label):
                    seed = gr.Number(value=0, precision=0, label="Seed")
                    fidelity = gr.Textbox(value="educational", label="Fidelity (optional)")
                    json_output = gr.JSON(label="Simulation Summary")
                    pretty_output = gr.Code(label="Highlights", language="json")
                    slug_state = gr.State(slug)

                    def _run(seed_value: float, fidelity_value: str, hero_slug: str) -> tuple[Dict[str, Any], str]:
                        results = run_simulation(hero_slug, int(seed_value), fidelity_value.strip())
                        return results, format_summary(results)

                    run_button = gr.Button("Run Simulation")
                    run_button.click(
                        fn=_run,
                        inputs=[seed, fidelity, slug_state],
                        outputs=[json_output, pretty_output],
                    )
        gr.Markdown(
            """Powered by [davinci-codex](https://github.com/Shannon-Labs/davinci-codex)."""
        )
    return demo


app = main()


if __name__ == "__main__":
    app.launch()
