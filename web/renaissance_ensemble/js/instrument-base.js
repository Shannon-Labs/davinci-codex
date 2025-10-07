/**
 * Leonardo's Mechanical Ensemble - Base Instrument Class
 * Abstract base class for all mechanical instruments
 */

// Ensure namespace exists
window.LeonardoEnsemble = window.LeonardoEnsemble || {};

/**
 * Base Instrument Class
 * Provides common functionality for all mechanical instruments
 */
LeonardoEnsemble.InstrumentBase = class {
    /**
     * Create a new instrument
     * @param {string} id - Unique instrument identifier
     * @param {string} name - Instrument display name
     * @param {HTMLCanvasElement} canvas - Canvas element for rendering
     * @param {Object} options - Instrument configuration options
     */
    constructor(id, name, canvas, options = {}) {
        this.id = id;
        this.name = name;
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // Instrument state
        this.isPlaying = false;
        this.isMuted = false;
        this.volume = options.volume || 80;
        this.currentNote = null;
        this.animationTime = 0;
        
        // Timing and synchronization
        this.tempo = options.tempo || 120;
        this.beatDuration = LeonardoEnsemble.Utils.time.bpmToMs(this.tempo);
        this.lastBeatTime = 0;
        this.currentBeat = 0;
        
        // Animation properties
        this.animationFrame = null;
        this.components = new Map();
        this.particles = [];
        
        // Event emitter for instrument events
        this.events = new LeonardoEnsemble.Utils.events.EventEmitter();
        
        // Initialize canvas
        this.initializeCanvas();
        
        // Set up instrument-specific components
        this.setupComponents();
        
        // Bind methods
        this.animate = this.animate.bind(this);
        this.handleTempoChange = this.handleTempoChange.bind(this);
        
        // Store in global registry
        LeonardoEnsemble.InstrumentRegistry.register(this);
    }
    
    /**
     * Initialize canvas with proper sizing and context
     */
    initializeCanvas() {
        // Set canvas size with device pixel ratio support
        const rect = this.canvas.getBoundingClientRect();
        LeonardoEnsemble.Utils.canvas.setSize(this.canvas, rect.width, rect.height);
        
        // Set default context properties
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';
        
        // Enable transparency
        this.ctx.globalAlpha = 1;
    }
    
    /**
     * Set up instrument-specific components
     * Override in subclasses
     */
    setupComponents() {
        // Abstract method - implement in subclasses
        console.warn(`setupComponents() not implemented for ${this.name}`);
    }
    
    /**
     * Add a component to the instrument
     * @param {string} id - Component identifier
     * @param {Object} component - Component object
     */
    addComponent(id, component) {
        this.components.set(id, component);
    }
    
    /**
     * Get a component by ID
     * @param {string} id - Component identifier
     * @returns {Object|null} Component or null if not found
     */
    getComponent(id) {
        return this.components.get(id) || null;
    }
    
    /**
     * Start playing the instrument
     */
    start() {
        if (this.isPlaying) return;
        
        this.isPlaying = true;
        this.animationTime = 0;
        this.lastBeatTime = LeonardoEnsemble.Utils.time.getTimestamp();
        
        // Start animation loop
        LeonardoEnsemble.Utils.animation.add(this.animate);
        
        // Emit start event
        this.events.emit('start', { instrument: this });
        
        // Update UI
        this.updateUIState('playing');
    }
    
    /**
     * Stop playing the instrument
     */
    stop() {
        if (!this.isPlaying) return;
        
        this.isPlaying = false;
        this.currentBeat = 0;
        this.currentNote = null;
        
        // Stop animation loop
        LeonardoEnsemble.Utils.animation.remove(this.animate);
        
        // Clear animation frame
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }
        
        // Reset components
        this.resetComponents();
        
        // Clear particles
        this.particles = [];
        
        // Clear canvas
        LeonardoEnsemble.Utils.canvas.clear(this.canvas);
        
        // Draw static state
        this.draw();
        
        // Emit stop event
        this.events.emit('stop', { instrument: this });
        
        // Update UI
        this.updateUIState('stopped');
    }
    
    /**
     * Pause the instrument (maintains state)
     */
    pause() {
        if (!this.isPlaying) return;
        
        this.isPlaying = false;
        
        // Remove from animation loop but don't reset state
        LeonardoEnsemble.Utils.animation.remove(this.animate);
        
        // Emit pause event
        this.events.emit('pause', { instrument: this });
        
        // Update UI
        this.updateUIState('paused');
    }
    
    /**
     * Resume playing from paused state
     */
    resume() {
        if (this.isPlaying) return;
        
        this.isPlaying = true;
        this.lastBeatTime = LeonardoEnsemble.Utils.time.getTimestamp();
        
        // Resume animation loop
        LeonardoEnsemble.Utils.animation.add(this.animate);
        
        // Emit resume event
        this.events.emit('resume', { instrument: this });
        
        // Update UI
        this.updateUIState('playing');
    }
    
    /**
     * Set instrument volume
     * @param {number} volume - Volume level (0-100)
     */
    setVolume(volume) {
        this.volume = LeonardoEnsemble.Utils.math.clamp(volume, 0, 100);
        
        // Emit volume change event
        this.events.emit('volumeChange', { 
            instrument: this, 
            volume: this.volume 
        });
    }
    
    /**
     * Mute/unmute the instrument
     * @param {boolean} muted - Whether to mute the instrument
     */
    setMuted(muted) {
        this.isMuted = muted;
        
        // Emit mute change event
        this.events.emit('muteChange', { 
            instrument: this, 
            muted: this.isMuted 
        });
        
        // Update UI
        this.updateUIState(muted ? 'muted' : (this.isPlaying ? 'playing' : 'stopped'));
    }
    
    /**
     * Handle tempo change
     * @param {number} tempo - New tempo in BPM
     */
    handleTempoChange(tempo) {
        this.tempo = tempo;
        this.beatDuration = LeonardoEnsemble.Utils.time.bpmToMs(this.tempo);
        
        // Update components that depend on tempo
        this.updateTempoDependentComponents();
    }
    
    /**
     * Update components that depend on tempo
     * Override in subclasses
     */
    updateTempoDependentComponents() {
        // Abstract method - implement in subclasses if needed
    }
    
    /**
     * Reset all components to initial state
     */
    resetComponents() {
        this.components.forEach(component => {
            if (component.reset) {
                component.reset();
            }
        });
    }
    
    /**
     * Main animation loop
     * @param {number} timestamp - Current animation timestamp
     */
    animate(timestamp) {
        if (!this.isPlaying) return;
        
        // Update animation time
        const deltaTime = timestamp - this.animationTime;
        this.animationTime = timestamp;
        
        // Check for beat timing
        const currentTime = LeonardoEnsemble.Utils.time.getTimestamp();
        if (currentTime - this.lastBeatTime >= this.beatDuration) {
            this.onBeat();
            this.lastBeatTime = currentTime;
        }
        
        // Update components
        this.updateComponents(deltaTime);
        
        // Update particles
        this.updateParticles(deltaTime);
        
        // Draw instrument
        this.draw();
        
        // Process current note
        if (this.currentNote) {
            this.processNote(this.currentNote, deltaTime);
        }
    }
    
    /**
     * Handle beat timing
     * Override in subclasses
     */
    onBeat() {
        this.currentBeat++;
        
        // Emit beat event
        this.events.emit('beat', { 
            instrument: this, 
            beat: this.currentBeat,
            timestamp: LeonardoEnsemble.Utils.time.getTimestamp()
        });
    }
    
    /**
     * Update all components
     * @param {number} deltaTime - Time since last frame
     */
    updateComponents(deltaTime) {
        this.components.forEach(component => {
            if (component.update) {
                component.update(deltaTime, this.animationTime);
            }
        });
    }
    
    /**
     * Update particle effects
     * @param {number} deltaTime - Time since last frame
     */
    updateParticles(deltaTime) {
        // Update existing particles
        this.particles = this.particles.filter(particle => {
            particle.update(deltaTime);
            return particle.isAlive();
        });
        
        // Remove dead particles
        this.particles = this.particles.filter(particle => particle.life > 0);
    }
    
    /**
     * Add a particle effect
     * @param {Object} particle - Particle object
     */
    addParticle(particle) {
        this.particles.push(particle);
    }
    
    /**
     * Process current note
     * @param {Object} note - Note object
     * @param {number} deltaTime - Time since last frame
     */
    processNote(note, deltaTime) {
        // Override in subclasses
    }
    
    /**
     * Play a note
     * @param {Object} note - Note object with pitch, duration, etc.
     */
    playNote(note) {
        if (this.isMuted) return;
        
        this.currentNote = note;
        
        // Trigger note-specific animations
        this.onNotePlay(note);
        
        // Emit note play event
        this.events.emit('notePlay', { 
            instrument: this, 
            note: note 
        });
    }
    
    /**
     * Handle note play
     * Override in subclasses
     * @param {Object} note - Note object
     */
    onNotePlay(note) {
        // Abstract method - implement in subclasses
    }
    
    /**
     * Stop current note
     */
    stopNote() {
        if (this.currentNote) {
            this.onNoteStop(this.currentNote);
            
            // Emit note stop event
            this.events.emit('noteStop', { 
                instrument: this, 
                note: this.currentNote 
            });
            
            this.currentNote = null;
        }
    }
    
    /**
     * Handle note stop
     * Override in subclasses
     * @param {Object} note - Note object
     */
    onNoteStop(note) {
        // Abstract method - implement in subclasses
    }
    
    /**
     * Draw the instrument
     */
    draw() {
        // Clear canvas
        LeonardoEnsemble.Utils.canvas.clear(this.canvas);
        
        // Draw background
        this.drawBackground();
        
        // Draw components
        this.drawComponents();
        
        // Draw particles
        this.drawParticles();
        
        // Draw foreground
        this.drawForeground();
    }
    
    /**
     * Draw background
     * Override in subclasses
     */
    drawBackground() {
        // Default background
        const gradient = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.1)');
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0.05)');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    /**
     * Draw all components
     */
    drawComponents() {
        this.components.forEach(component => {
            if (component.draw) {
                component.draw(this.ctx);
            }
        });
    }
    
    /**
     * Draw particle effects
     */
    drawParticles() {
        this.particles.forEach(particle => {
            if (particle.draw) {
                particle.draw(this.ctx);
            }
        });
    }
    
    /**
     * Draw foreground elements
     * Override in subclasses
     */
    drawForeground() {
        // Default foreground - playing indicator
        if (this.isPlaying) {
            this.ctx.save();
            this.ctx.fillStyle = 'rgba(255, 215, 0, 0.3)';
            this.ctx.fillRect(0, 0, this.canvas.width, 4);
            this.ctx.restore();
        }
    }
    
    /**
     * Update UI state
     * @param {string} state - New state ('playing', 'stopped', 'paused', 'muted')
     */
    updateUIState(state) {
        // Find instrument container
        const container = document.querySelector(`[data-instrument="${this.id}"]`);
        if (!container) return;
        
        // Update container classes
        LeonardoEnsemble.Utils.dom.removeClass(container, 'playing', 'stopped', 'paused', 'muted');
        LeonardoEnsemble.Utils.dom.addClass(container, state);
        
        // Update status indicator
        const statusIndicator = container.querySelector('.instrument-status');
        if (statusIndicator) {
            const statusText = {
                'playing': 'Playing',
                'stopped': 'Ready',
                'paused': 'Paused',
                'muted': 'Muted'
            };
            statusIndicator.textContent = statusText[state] || 'Ready';
            LeonardoEnsemble.Utils.dom.removeClass(statusIndicator, 'playing');
            if (state === 'playing') {
                LeonardoEnsemble.Utils.dom.addClass(statusIndicator, 'playing');
            }
        }
        
        // Update canvas container
        const canvasContainer = this.canvas.parentElement;
        if (canvasContainer) {
            LeonardoEnsemble.Utils.dom.removeClass(canvasContainer, 'playing', 'stopped', 'paused', 'muted');
            LeonardoEnsemble.Utils.dom.addClass(canvasContainer, state);
        }
    }
    
    /**
     * Get instrument state for serialization
     * @returns {Object} Current instrument state
     */
    getState() {
        return {
            id: this.id,
            name: this.name,
            isPlaying: this.isPlaying,
            isMuted: this.isMuted,
            volume: this.volume,
            tempo: this.tempo,
            currentBeat: this.currentBeat,
            currentNote: this.currentNote
        };
    }
    
    /**
     * Restore instrument state
     * @param {Object} state - State to restore
     */
    restoreState(state) {
        this.volume = state.volume || 80;
        this.isMuted = state.isMuted || false;
        this.tempo = state.tempo || 120;
        this.beatDuration = LeonardoEnsemble.Utils.time.bpmToMs(this.tempo);
        
        if (state.isPlaying) {
            this.start();
        }
        
        this.updateUIState(state.isMuted ? 'muted' : (state.isPlaying ? 'playing' : 'stopped'));
    }
    
    /**
     * Clean up resources
     */
    dispose() {
        // Stop playing
        this.stop();
        
        // Clear event listeners
        this.events.clear();
        
        // Remove from registry
        LeonardoEnsemble.InstrumentRegistry.unregister(this);
        
        // Clear references
        this.components.clear();
        this.particles = [];
    }
};

// Instrument Registry for managing all instruments
LeonardoEnsemble.InstrumentRegistry = {
    instruments: new Map(),
    
    /**
     * Register an instrument
     * @param {LeonardoEnsemble.InstrumentBase} instrument - Instrument to register
     */
    register(instrument) {
        this.instruments.set(instrument.id, instrument);
    },
    
    /**
     * Unregister an instrument
     * @param {string|LeonardoEnsemble.InstrumentBase} instrument - Instrument or ID to unregister
     */
    unregister(instrument) {
        const id = typeof instrument === 'string' ? instrument : instrument.id;
        this.instruments.delete(id);
    },
    
    /**
     * Get an instrument by ID
     * @param {string} id - Instrument ID
     * @returns {LeonardoEnsemble.InstrumentBase|null} Instrument or null
     */
    get(id) {
        return this.instruments.get(id) || null;
    },
    
    /**
     * Get all instruments
     * @returns {Array<LeonardoEnsemble.InstrumentBase>} All registered instruments
     */
    getAll() {
        return Array.from(this.instruments.values());
    },
    
    /**
     * Start all instruments
     */
    startAll() {
        this.instruments.forEach(instrument => instrument.start());
    },
    
    /**
     * Stop all instruments
     */
    stopAll() {
        this.instruments.forEach(instrument => instrument.stop());
    },
    
    /**
     * Set tempo for all instruments
     * @param {number} tempo - New tempo in BPM
     */
    setTempoAll(tempo) {
        this.instruments.forEach(instrument => instrument.handleTempoChange(tempo));
    },
    
    /**
     * Clear all instruments
     */
    clear() {
        this.instruments.forEach(instrument => instrument.dispose());
        this.instruments.clear();
    }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        InstrumentBase: LeonardoEnsemble.InstrumentBase,
        InstrumentRegistry: LeonardoEnsemble.InstrumentRegistry
    };
}