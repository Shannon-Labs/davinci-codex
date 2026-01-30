/**
 * Leonardo's Mechanical Ensemble - Audio Engine
 * Web Audio API synthesis and MP3 playback with real-time visualization
 */

window.LeonardoEnsemble = window.LeonardoEnsemble || {};

LeonardoEnsemble.AudioEngine = class {
    constructor() {
        /** @type {AudioContext|null} */
        this.ctx = null;
        /** @type {AnalyserNode|null} */
        this.analyser = null;
        /** @type {GainNode|null} */
        this.masterGain = null;
        /** @type {number|null} */
        this._vizRAF = null;
        /** @type {boolean} */
        this._vizRunning = false;
    }

    // ---- Timbre data for all 6 instruments ----
    static get timbres() {
        return {
            viola: {
                label: 'Viola Organista',
                harmonics:   [1, 2, 3, 4, 5, 6, 7, 8],
                weights:     [1.0, 0.3, 0.7, 0.15, 0.5, 0.1, 0.35, 0.08],
                attack: 0.08, decay: 0.06, sustain: 0.75, release: 0.15,
                vibrato: { rate: 5, cents: 12 },
                noise: { type: 'pink', amount: 0.03 },
                filterFreq: 3000,
                baseFreq: 293.66  // D4
            },
            organ: {
                label: 'Mechanical Organ',
                harmonics:   [1, 2, 3, 4, 5, 6, 7, 8],
                weights:     [1.0, 0.5, 0.333, 0.25, 0.2, 0.167, 0.143, 0.125],
                attack: 0.05, decay: 0.03, sustain: 0.95, release: 0.08,
                vibrato: null,
                noise: { type: 'pink', amount: 0.02 },
                filterFreq: 4000,
                baseFreq: 261.63  // C4
            },
            flute: {
                label: 'Programmable Flute',
                harmonics:   [1, 2, 3, 4, 5],
                weights:     [1.0, 0.35, 0.15, 0.08, 0.03],
                attack: 0.04, decay: 0.05, sustain: 0.70, release: 0.12,
                vibrato: { rate: 4.5, cents: 8 },
                noise: { type: 'pink', amount: 0.08 },
                filterFreq: 5000,
                baseFreq: 523.25  // C5
            },
            carillon: {
                label: 'Mechanical Carillon',
                harmonics:   [1, 2.4, 3.9, 5.4, 6.7, 8.2],
                weights:     [1.0, 0.6, 0.4, 0.25, 0.15, 0.08],
                attack: 0.001, decay: 0.3, sustain: 0.15, release: 1.5,
                vibrato: null,
                noise: null,
                filterFreq: 6000,
                baseFreq: 587.33  // D5
            },
            trumpeter: {
                label: 'Mechanical Trumpeter',
                harmonics:   [1, 2, 3, 4, 5, 6, 7, 8],
                weights:     [1.0, 0.8, 0.6, 0.55, 0.5, 0.4, 0.3, 0.2],
                attack: 0.03, decay: 0.04, sustain: 0.85, release: 0.10,
                vibrato: { rate: 5.5, cents: 15 },
                noise: { type: 'pink', amount: 0.04 },
                filterFreq: 3500,
                baseFreq: 349.23  // F4
            },
            drum: {
                label: 'Mechanical Drum',
                harmonics:   [1, 1.59, 2.14, 2.30, 2.65, 2.92],
                weights:     [1.0, 0.7, 0.5, 0.35, 0.2, 0.1],
                attack: 0.002, decay: 0.15, sustain: 0.0, release: 0.20,
                vibrato: null,
                noise: { type: 'white', amount: 0.60 },
                filterFreq: 2500,
                baseFreq: 110.0   // A2
            }
        };
    }

    // ---- Context management ----

    /**
     * Lazily create (or resume) AudioContext on first user gesture.
     * @returns {AudioContext}
     */
    ensureContext() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();

            // master gain
            this.masterGain = this.ctx.createGain();
            this.masterGain.gain.value = 0.55;

            // analyser for visualization
            this.analyser = this.ctx.createAnalyser();
            this.analyser.fftSize = 2048;
            this.analyser.smoothingTimeConstant = 0.8;

            // Route: masterGain -> analyser -> destination
            this.masterGain.connect(this.analyser);
            this.analyser.connect(this.ctx.destination);
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
        return this.ctx;
    }

    // ---- Demo MP3 playback ----

    /**
     * Route an <audio> element through the Web Audio graph for visualization.
     * @param {HTMLAudioElement} audioEl
     */
    playDemo(audioEl) {
        this.ensureContext();

        // Create MediaElementSource only once per element
        if (!audioEl._webAudioSource) {
            const src = this.ctx.createMediaElementSource(audioEl);
            src.connect(this.masterGain);
            audioEl._webAudioSource = src;
        }

        audioEl.play();
    }

    /**
     * Pause and reset the demo audio element.
     * @param {HTMLAudioElement} audioEl
     */
    stopDemo(audioEl) {
        audioEl.pause();
        audioEl.currentTime = 0;
    }

    // ---- Visualizer ----

    /**
     * Start a requestAnimationFrame loop drawing frequency bars + waveform.
     * @param {HTMLCanvasElement} canvas
     */
    startVisualizer(canvas) {
        if (!this.analyser) return;
        this._vizRunning = true;

        const ctx2d = canvas.getContext('2d');
        const analyser = this.analyser;
        const bufferLength = analyser.frequencyBinCount;
        const freqData = new Uint8Array(bufferLength);
        const waveData = new Uint8Array(bufferLength);

        const draw = () => {
            if (!this._vizRunning) return;
            this._vizRAF = requestAnimationFrame(draw);

            const W = canvas.width;
            const H = canvas.height;
            ctx2d.clearRect(0, 0, W, H);

            // --- Frequency bars (bottom portion) ---
            analyser.getByteFrequencyData(freqData);
            const barCount = Math.min(bufferLength, 128);
            const barW = W / barCount;
            for (let i = 0; i < barCount; i++) {
                const v = freqData[i] / 255;
                const barH = v * (H * 0.55);
                // Gold-to-crimson gradient
                const r = Math.floor(180 + 75 * v);
                const g = Math.floor(150 * (1 - v));
                const b = Math.floor(30 * (1 - v));
                ctx2d.fillStyle = `rgba(${r},${g},${b},0.85)`;
                ctx2d.fillRect(i * barW, H - barH, barW - 1, barH);
            }

            // --- Waveform (top portion) ---
            analyser.getByteTimeDomainData(waveData);
            ctx2d.beginPath();
            ctx2d.strokeStyle = 'rgba(255,215,0,0.7)';
            ctx2d.lineWidth = 2;
            const sliceW = W / bufferLength;
            let x = 0;
            for (let i = 0; i < bufferLength; i++) {
                const v = waveData[i] / 128.0;
                const y = (v * H * 0.25);
                if (i === 0) ctx2d.moveTo(x, y);
                else ctx2d.lineTo(x, y);
                x += sliceW;
            }
            ctx2d.stroke();
        };

        draw();
    }

    /**
     * Stop the visualizer loop.
     */
    stopVisualizer() {
        this._vizRunning = false;
        if (this._vizRAF) {
            cancelAnimationFrame(this._vizRAF);
            this._vizRAF = null;
        }
    }

    // ---- Additive synthesis for timbre cards ----

    /**
     * Play a note using additive synthesis matching the given instrument's timbre.
     * @param {string} instrumentId  - key in AudioEngine.timbres
     * @param {number} [freq]        - fundamental frequency (Hz); defaults to timbre's baseFreq
     * @param {number} [duration]    - total note length (s); defaults based on envelope
     */
    playNote(instrumentId, freq, duration) {
        const ctx = this.ensureContext();
        const timbre = LeonardoEnsemble.AudioEngine.timbres[instrumentId];
        if (!timbre) return;

        const f0 = freq || timbre.baseFreq;
        const dur = duration || (timbre.attack + timbre.decay + 0.6 + timbre.release);
        const now = ctx.currentTime;
        const EPS = 0.001; // floor for exponential ramps (can't ramp to 0)

        // Normalize weights so they sum to 1.0
        const weightSum = timbre.weights.reduce((s, w) => s + w, 0);

        // Peak amplitude for the note (after normalization, this is the
        // loudest the combined oscillators will be).
        const peakGain = 0.28;

        // --- Note-level gain (ADSR envelope using exponential ramps) ---
        const noteGain = ctx.createGain();
        noteGain.gain.setValueAtTime(EPS, now);
        // Attack
        noteGain.gain.exponentialRampToValueAtTime(peakGain, now + timbre.attack);
        // Decay -> sustain
        const sustainLevel = Math.max(peakGain * timbre.sustain, EPS);
        noteGain.gain.exponentialRampToValueAtTime(sustainLevel, now + timbre.attack + timbre.decay);
        // Sustain hold
        const sustainEnd = now + dur - timbre.release;
        noteGain.gain.setValueAtTime(sustainLevel, sustainEnd);
        // Release
        noteGain.gain.exponentialRampToValueAtTime(EPS, now + dur);

        // --- Lowpass filter to warm the tone ---
        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = timbre.filterFreq || 4000;
        filter.Q.value = 0.7;

        // Route: noteGain -> filter -> masterGain
        noteGain.connect(filter);
        filter.connect(this.masterGain);

        // --- Oscillators per harmonic (normalized weights) ---
        for (let i = 0; i < timbre.harmonics.length; i++) {
            const osc = ctx.createOscillator();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(f0 * timbre.harmonics[i], now);

            const harmGain = ctx.createGain();
            harmGain.gain.value = timbre.weights[i] / weightSum;
            osc.connect(harmGain);
            harmGain.connect(noteGain);

            // Vibrato LFO
            if (timbre.vibrato) {
                const lfo = ctx.createOscillator();
                lfo.type = 'sine';
                lfo.frequency.value = timbre.vibrato.rate;

                const lfoGain = ctx.createGain();
                // cents -> Hz deviation
                lfoGain.gain.value = f0 * timbre.harmonics[i] * (Math.pow(2, timbre.vibrato.cents / 1200) - 1);
                lfo.connect(lfoGain);
                lfoGain.connect(osc.frequency);

                lfo.start(now);
                lfo.stop(now + dur + 0.05);
            }

            osc.start(now);
            osc.stop(now + dur + 0.05);
        }

        // --- Optional noise layer (scaled relative to normalized signal) ---
        if (timbre.noise && timbre.noise.amount > 0) {
            const noiseNode = this._createNoiseNode(timbre.noise.type, dur);
            const noiseGain = ctx.createGain();
            noiseGain.gain.value = timbre.noise.amount;
            noiseNode.connect(noiseGain);
            noiseGain.connect(noteGain);
            noiseNode.start(now);
            noiseNode.stop(now + dur + 0.05);
        }
    }

    /**
     * Create a noise buffer source (white or Voss-McCartney pink).
     * @param {string} type      - 'white' or 'pink'
     * @param {number} duration  - length in seconds
     * @returns {AudioBufferSourceNode}
     */
    _createNoiseNode(type, duration) {
        const ctx = this.ctx;
        const sampleRate = ctx.sampleRate;
        const length = Math.ceil(sampleRate * duration);
        const buffer = ctx.createBuffer(1, length, sampleRate);
        const data = buffer.getChannelData(0);

        if (type === 'pink') {
            // Voss-McCartney pink noise approximation
            let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
            for (let i = 0; i < length; i++) {
                const white = Math.random() * 2 - 1;
                b0 = 0.99886 * b0 + white * 0.0555179;
                b1 = 0.99332 * b1 + white * 0.0750759;
                b2 = 0.96900 * b2 + white * 0.1538520;
                b3 = 0.86650 * b3 + white * 0.3104856;
                b4 = 0.55000 * b4 + white * 0.5329522;
                b5 = -0.7616 * b5 - white * 0.0168980;
                data[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11;
                b6 = white * 0.115926;
            }
        } else {
            // White noise
            for (let i = 0; i < length; i++) {
                data[i] = Math.random() * 2 - 1;
            }
        }

        const source = ctx.createBufferSource();
        source.buffer = buffer;
        return source;
    }

    // ---- Generative Cantus Firmus Engine ----

    /**
     * Generate and play a four-part counterpoint in real-time.
     */
    playGenerativeConcert() {
        const ctx = this.ensureContext();
        const now = ctx.currentTime;

        // Cantus Firmus (Dorian mode)
        const cf = [62, 64, 65, 67, 69, 67, 65, 62];
        const tempo = 72;
        const beatDur = 60 / tempo;

        const cp = this.generateCounterpoint(cf);

        cf.forEach((note, i) => {
            const time = now + i * beatDur;
            this.scheduleNote('organ', note, time, beatDur * 0.8);
            this.scheduleNote('viola', cp[i], time, beatDur * 0.8);
        });
    }

    generateCounterpoint(cf) {
        // Simple first-species counterpoint
        const consonant = [0, 3, 4, 7, 8, 9, 12];
        return cf.map(n => n + consonant[Math.floor(Math.random() * consonant.length)]);
    }

    scheduleNote(instrumentId, midiNote, startTime, duration) {
        const freq = 440 * Math.pow(2, (midiNote - 69) / 12);
        setTimeout(() => {
            this.playNote(instrumentId, freq, duration);
        }, (startTime - this.ctx.currentTime) * 1000);
    }
};
