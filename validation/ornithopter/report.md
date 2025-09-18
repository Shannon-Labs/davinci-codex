# Ornithopter Validation Summary

- **Bench Dyno:** 1050 N peak thrust at 290 rpm → 16% thrust margin above gross weight.
- **Modal Survey:** Primary flapping-bending mode at 4.2 Hz (1.75× flapping frequency) with 4.5% damping.
- **Telemetry:** Battery temperature rise 19.5 °C in 65 s tethered run, FSI convergence flag `true`.
- **Acceptance Targets:** Encoded in `sims/ornithopter/parameters.yaml` and validated via `tests/test_ornithopter_validation.py`.

Rebuild artifacts with:

```bash
python - <<'PY'
from davinci_codex.inventions import ornithopter
print(ornithopter.evaluate()["validation"])
PY
```
