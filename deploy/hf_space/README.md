# da Vinci Codex – Hugging Face Space

A minimal Gradio app exposing hero demos from `davinci-codex`:

- Parachute
- Aerial Screw
- Mechanical Lion

## Local Development

```bash
# From repo root
pip install -r hf_space/requirements.txt
pip install -e .
python hf_space/app.py
```

Then open the URL printed by Gradio (default http://127.0.0.1:7860).

## App Behavior

- Tabs for each hero demo
- Inputs: `Seed` (int), `Fidelity` (string, optional; defaults to `educational`)
- Outputs: JSON summary + pretty highlights (performance + educational insight excerpts)

## Deploying to Hugging Face Spaces

1. Create a new Space (Gradio SDK, Python runtime)
2. Add `hf_space/requirements.txt` and `hf_space/app.py` to the Space repository
3. Ensure the Space points to `app` exported by `app.py`
4. (Optional) Add a README to the Space

Once deployed, copy the Space URL and update the Live Demo badge in the root `README.md`.
