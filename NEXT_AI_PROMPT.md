# PROMPT: Make the Renaissance Ensemble a Real Musical Experience

## Already Fixed (don't redo these)

- Misattributed quote ("Music is the arithmetic of sounds...") was Leibniz/Debussy,
  not Leonardo. Replaced with verified Leonardo quote from Trattato della Pittura
  ("Music may be called the sister of painting..."). All 3 occurrences + mirror text fixed.
- Copyright year updated to 2025.
- Broken WAV fallback removed (only MP3 exists).
- GitHub Pages workflow rewritten to deploy `web/` as static HTML (no Jekyll).

## The Problem

The Renaissance Ensemble page (`web/renaissance_ensemble/index.html`) is a beautiful
static page that *describes* a musical experience but doesn't *deliver* one. Right now:

- There is ONE audio file: `assets/demo_pavane.mp3` played via a bare `<audio>` tag
- The "interactive" section (play/pause/stop, tempo slider, instrument mixers) is
  **completely non-functional** -- the JS files are scaffolding with no audio synthesis
- The 6 instrument "timbre cards" are static text descriptions of harmonic parameters
- The visualization PNGs (waveform, spectrogram, score roll) are static images
- A visitor arrives, sees a wall of technical specs, and has no way to actually *hear* anything interesting

A person visiting this page should feel like they walked into a Renaissance court and
the mechanical orchestra is performing for them.

---

## What Exists (inventory of assets you have to work with)

### Audio

| Asset | Path | Notes |
|-------|------|-------|
| Pavane demo MP3 | `web/renaissance_ensemble/assets/demo_pavane.mp3` | 54 seconds, 6 instruments, Dorian mode |
| Full WAV source | `artifacts/mechanical_concert/demo/concert_audio.wav` | 4.8 MB, CD quality 44.1kHz |
| Score JSON | `artifacts/mechanical_concert/demo/concert_score.json` | Full note-by-note score data (1.5 MB) |

### Python concert generator

The Python backend can generate unlimited compositions:

```python
# src/davinci_codex/core/concert.py
perform_concert(
    form="pavane",      # pavane, galliard, basse_danse, saltarello, allemande
    mode="dorian",      # dorian, mixolydian, phrygian, lydian, ionian, aeolian
    seed=42,
    measures=16,
    tempo_bpm=80.0,
    reverb_wet=0.2,
    sample_rate=44100,
    output_dir=Path("artifacts/mechanical_concert/demo"),
    visualize=True,
)
```

CLI equivalent:
```bash
python -m davinci_codex.cli concert --form pavane --mode dorian --measures 16 --seed 42 --reverb 0.2
```

This produces: `concert_audio.wav`, `concert_score.json`, `waveform.png`,
`spectrogram.png`, `score_roll.png`.

### JavaScript (scaffolding, doesn't produce audio)

| File | What it does | What it's missing |
|------|-------------|-------------------|
| `js/app.js` | Main controller, wires up play/pause/stop buttons, tempo slider, composition selector | No actual audio playback or synthesis. `play()`, `pause()`, `stop()` methods exist but don't produce sound |
| `js/instrument-base.js` | Base class for instruments, canvas rendering, animation loop | Canvas animation only. No Web Audio API. No sound output |
| `js/carillon.js` | Carillon-specific canvas animation (bell ringing visuals) | Visual only |
| `js/drum.js` | Drum-specific canvas animation | Visual only |
| `js/utils.js` | Utility functions (animation, timing, DOM helpers, EventEmitter) | Solid utilities, usable as-is |

### CSS (complete, beautiful)

5 CSS files in `styles/` -- the visual design is done and polished. Don't touch these
unless needed for new UI elements.

### Physics parameters (already documented in the HTML)

Each instrument has its harmonic profile spelled out in the HTML:

```
Viola Organista:  harmonics [1,2,3,4,5,6,7,8], weights [1.0,0.3,0.7,0.15,0.5,0.1,0.35,0.08]
                  ADSR: A=80ms D=60ms S=75% R=150ms, vibrato 5Hz/12cents, 3% pink noise

Mechanical Organ: harmonics [1,2,3,4,5,6,7,8], weights 1/n series
                  ADSR: A=50ms D=30ms S=95% R=80ms, 2% breath noise

Programmable Flute: harmonics [1,2,3,4,5], weights [1.0,0.35,0.15,0.08,0.03]
                    ADSR: A=40ms D=50ms S=70% R=120ms, vibrato 4.5Hz/8cents, 8% breath noise

Mechanical Carillon: harmonics [1,2.4,3.9,5.4,6.7,8.2], weights [1.0,0.6,0.4,0.25,0.15,0.08]
                     ADSR: A=1ms D=300ms S=15% R=1500ms (inharmonic bell partials)

Mechanical Trumpeter: harmonics [1,2,3,4,5,6,7,8], weights [1.0,0.8,0.6,0.55,0.5,0.4,0.3,0.2]
                      ADSR: A=30ms D=40ms S=85% R=100ms, vibrato 5.5Hz/15cents, 4% breath noise

Mechanical Drum: harmonics (Bessel zeros) [1,1.59,2.14,2.30,2.65,2.92]
                 weights [1.0,0.7,0.5,0.35,0.2,0.1]
                 ADSR: A=2ms D=150ms S=0% R=200ms, 60% white noise burst
```

---

## What to Build (ordered by impact)

### Phase 1: Instant Gratification -- Make Things Sound Immediately

**Goal**: A visitor hears music within 5 seconds of landing on the page.

1. **Auto-play the demo with visual sync**: When the page loads, show a prominent
   "Enter the Court" button. On click, start the demo_pavane.mp3 with a
   real-time waveform/frequency visualizer drawn on a canvas using
   `AnalyserNode` from the Web Audio API. The existing static PNG visualizations
   should be replaced (or augmented) by live animated versions while audio plays.

2. **Clickable instrument timbre cards**: Each of the 6 instrument cards in the
   "Physics-Based Instrument Timbres" section should play a note when clicked.
   Use Web Audio API `OscillatorNode` + `GainNode` chains to synthesize sound
   from the harmonic parameters already in the HTML. A D4 note (293.66 Hz) for
   melodic instruments, a drum hit for percussion. This is the single most
   impactful feature -- visitors click a card and hear the physics come alive.

3. **Generate more demo MP3s**: Use the Python `perform_concert()` to generate
   at least 3 additional compositions and convert them to MP3:
   - Galliard in Mixolydian (energetic, dance-like)
   - Saltarello in Phrygian (dramatic, leaping)
   - Basse Danse in Lydian (stately, bright)

   Place them in `web/renaissance_ensemble/assets/` and add them to the audio
   showcase as a playlist/track selector so visitors can browse different pieces.

### Phase 2: Interactive Player -- Make the Controls Work

**Goal**: The play/pause/stop buttons, tempo slider, and instrument mixers do something.

4. **Wire up the audio player controls**: Connect the existing UI controls to
   the Web Audio API graph. The play button starts the current track, pause
   suspends the AudioContext, stop resets to beginning. The tempo slider could
   use `AudioBufferSourceNode.playbackRate` for pre-rendered audio, or control
   real-time synthesis speed.

5. **Working instrument mixer**: Each instrument's volume slider and mute button
   should control the mix. For pre-rendered audio this is harder (would need
   separate stems). For synthesized audio it's straightforward -- each instrument
   gets its own GainNode.

6. **Composition selector**: The dropdown (Renaissance Court Dance, Madrigal,
   Galliard, Pavane) should switch between the available MP3 demos.

### Phase 3: Real-Time Synthesis (stretch goal)

**Goal**: Generate music in the browser from the score JSON.

7. **Load `concert_score.json`**: Parse the score data and schedule note events
   using Web Audio API's precise timing (`AudioContext.currentTime`). Each note
   triggers the appropriate instrument's oscillator bank. This would make the
   instrument mixer fully functional (per-instrument volume/mute) and allow
   tempo changes in real-time.

8. **Live score visualization**: As notes play, highlight them on a scrolling
   piano-roll canvas visualization (replacing the static score_roll.png).

### Phase 4: Ambient Experience (creative extras)

9. **MiniMax music generation**: The project has MiniMax MCP tools available.
   You could use `mcp__MiniMax__music_generation` to generate a Renaissance-style
   ambient background track with actual lyrics, or use `mcp__MiniMax__text_to_audio`
   to create a narrated introduction ("Welcome to Leonardo's court...") in a
   period-appropriate voice.

10. **Reverb and spatialization**: Add a convolution reverb (or the Schroeder
    reverb described on the page) to give the audio a cathedral/court hall feel.
    The Web Audio API `ConvolverNode` can do this with an impulse response.

---

## Technical Implementation Notes

### Web Audio API Synthesis (for the timbre cards)

Here's pseudocode for synthesizing one instrument note:

```javascript
function playInstrumentNote(audioCtx, harmonics, weights, adsr, freq, duration) {
    const now = audioCtx.currentTime;
    const masterGain = audioCtx.createGain();
    masterGain.connect(audioCtx.destination);

    // ADSR envelope
    masterGain.gain.setValueAtTime(0, now);
    masterGain.gain.linearRampToValueAtTime(1.0, now + adsr.attack);
    masterGain.gain.linearRampToValueAtTime(adsr.sustain, now + adsr.attack + adsr.decay);
    masterGain.gain.setValueAtTime(adsr.sustain, now + duration - adsr.release);
    masterGain.gain.linearRampToValueAtTime(0, now + duration);

    // Additive synthesis: one oscillator per harmonic
    harmonics.forEach((h, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.frequency.value = freq * h;
        gain.gain.value = weights[i] * 0.15; // scale down to avoid clipping
        osc.connect(gain);
        gain.connect(masterGain);
        osc.start(now);
        osc.stop(now + duration);
    });
}
```

### File structure for new assets

```
web/renaissance_ensemble/
  assets/
    demo_pavane.mp3          (existing)
    demo_galliard.mp3        (generate)
    demo_saltarello.mp3      (generate)
    demo_basse_danse.mp3     (generate)
    concert_score.json       (copy from artifacts/)
    waveform.png             (existing)
    spectrogram.png          (existing)
    score_roll.png           (existing)
  js/
    audio-engine.js          (NEW - Web Audio API synthesis engine)
    app.js                   (existing - wire up to audio engine)
    instrument-base.js       (existing)
    carillon.js              (existing)
    drum.js                  (existing)
    utils.js                 (existing)
```

### Key constraint

The site deploys as static HTML to GitHub Pages via the workflow in
`.github/workflows/pages.yml`. Everything must work client-side. No server.
The Python generator is for pre-rendering assets only.

### Converting WAV to MP3 for web

After generating WAV files with the Python CLI:
```bash
# Using ffmpeg
ffmpeg -i concert_audio.wav -codec:a libmp3lame -qscale:a 2 demo_galliard.mp3
```

---

## Success Criteria

A visitor to https://shannon-labs.github.io/davinci-codex/renaissance_ensemble/ should:

1. See an inviting "Enter the Court" button and hear music within one click
2. Be able to click any instrument card and hear what it sounds like
3. Browse 3-4 different Renaissance compositions
4. See live audio visualizations while music plays
5. Feel like they experienced something -- not just read about it

The page should go from "technical documentation about audio synthesis" to
"I just attended a concert in Leonardo's court."

---

## DO NOT

- Break the existing visual design (the CSS is great)
- Remove the educational content (harmonic specs, historical quotes)
- Use external CDNs or heavy libraries (Web Audio API is built into browsers)
- Create server-side dependencies (everything must work as static files)
- Forget to add new files to git and verify the Pages workflow deploys them
