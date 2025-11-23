/**
 * Leonardo's Mechanical Ensemble - Main Application
 * Entry point and main controller for the interactive visualization
 */

// Ensure namespace exists
window.LeonardoEnsemble = window.LeonardoEnsemble || {};

/**
 * Main Application Class
 * Coordinates all instruments and UI components
 */
LeonardoEnsemble.App = class {
    constructor() {
        // Application state
        this.isInitialized = false;
        this.isPlaying = false;
        this.currentTempo = 120;
        this.currentComposition = 'renaissance-dance';
        this.viewMode = 'both'; // 'notation', 'animation', 'both'
        
        // Instruments collection
        this.instruments = new Map();
        
        // UI elements
        this.elements = {};
        
        // Event handlers
        this.eventHandlers = {};
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initialize());
        } else {
            this.initialize();
        }
    }
    
    /**
     * Initialize the application
     */
    async initialize() {
        try {
            // Show loading overlay
            this.showLoading(true);
            
            // Cache DOM elements
            this.cacheElements();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Initialize instruments
            await this.initializeInstruments();
            
            // Initialize UI components
            this.initializeUI();
            
            // Load initial composition
            await this.loadComposition(this.currentComposition);
            
            // Hide loading overlay
            this.showLoading(false);
            
            // Mark as initialized
            this.isInitialized = true;
            
            console.log('Leonardo\'s Mechanical Ensemble initialized successfully');
            
        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.showError('Failed to initialize Leonardo\'s Mechanical Ensemble');
            this.showLoading(false);
        }
    }
    
    /**
     * Cache frequently used DOM elements
     */
    cacheElements() {
        this.elements = {
            // Controls
            playBtn: LeonardoEnsemble.Utils.dom.get('#play-btn'),
            pauseBtn: LeonardoEnsemble.Utils.dom.get('#pause-btn'),
            stopBtn: LeonardoEnsemble.Utils.dom.get('#stop-btn'),
            tempoSlider: LeonardoEnsemble.Utils.dom.get('#tempo-slider'),
            tempoDisplay: LeonardoEnsemble.Utils.dom.get('#tempo-display'),
            compositionSelect: LeonardoEnsemble.Utils.dom.get('#composition-select'),
            
            // View controls
            viewNotation: LeonardoEnsemble.Utils.dom.get('#view-notation'),
            viewAnimation: LeonardoEnsemble.Utils.dom.get('#view-animation'),
            viewBoth: LeonardoEnsemble.Utils.dom.get('#view-both'),
            
            // Timeline
            timelineProgress: LeonardoEnsemble.Utils.dom.get('#timeline-progress'),
            timelineMarker: LeonardoEnsemble.Utils.dom.get('#timeline-marker'),
            currentTime: LeonardoEnsemble.Utils.dom.get('#current-time'),
            totalTime: LeonardoEnsemble.Utils.dom.get('#total-time'),
            
            // Instrument controls
            instrumentMixers: LeonardoEnsemble.Utils.dom.getAll('.instrument-mixer'),
            
            // Educational panels
            tabBtns: LeonardoEnsemble.Utils.dom.getAll('.tab-btn'),
            tabPanels: LeonardoEnsemble.Utils.dom.getAll('.tab-panel'),
            
            // Loading overlay
            loadingOverlay: LeonardoEnsemble.Utils.dom.get('#loading-overlay'),
            
            // Canvas elements
            carillonCanvas: LeonardoEnsemble.Utils.dom.get('#carillon-canvas'),
            drumCanvas: LeonardoEnsemble.Utils.dom.get('#drum-canvas'),
            organCanvas: LeonardoEnsemble.Utils.dom.get('#organ-canvas'),
            trumpeterCanvas: LeonardoEnsemble.Utils.dom.get('#trumpeter-canvas'),
            fluteCanvas: LeonardoEnsemble.Utils.dom.get('#flute-canvas'),
            violaCanvas: LeonardoEnsemble.Utils.dom.get('#viola-canvas'),
            
            // Notation canvas
            notationCanvas: LeonardoEnsemble.Utils.dom.get('#notation-canvas')
        };
    }
    
    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Playback controls
        this.eventHandlers.play = () => this.play();
        this.eventHandlers.pause = () => this.pause();
        this.eventHandlers.stop = () => this.stop();
        
        LeonardoEnsemble.Utils.dom.on(this.elements.playBtn, 'click', this.eventHandlers.play);
        LeonardoEnsemble.Utils.dom.on(this.elements.pauseBtn, 'click', this.eventHandlers.pause);
        LeonardoEnsemble.Utils.dom.on(this.elements.stopBtn, 'click', this.eventHandlers.stop);
        
        // Tempo control
        this.eventHandlers.tempoChange = (e) => this.handleTempoChange(e);
        LeonardoEnsemble.Utils.dom.on(this.elements.tempoSlider, 'input', this.eventHandlers.tempoChange);
        
        // Composition selection
        this.eventHandlers.compositionChange = (e) => this.handleCompositionChange(e);
        LeonardoEnsemble.Utils.dom.on(this.elements.compositionSelect, 'change', this.eventHandlers.compositionChange);
        
        // View mode controls
        this.eventHandlers.viewModeChange = (e) => this.handleViewModeChange(e);
        LeonardoEnsemble.Utils.dom.on(this.elements.viewNotation, 'click', () => this.setViewMode('notation'));
        LeonardoEnsemble.Utils.dom.on(this.elements.viewAnimation, 'click', () => this.setViewMode('animation'));
        LeonardoEnsemble.Utils.dom.on(this.elements.viewBoth, 'click', () => this.setViewMode('both'));
        
        // Tab controls
        this.eventHandlers.tabChange = (e) => this.handleTabChange(e);
        this.elements.tabBtns.forEach(btn => {
            LeonardoEnsemble.Utils.dom.on(btn, 'click', this.eventHandlers.tabChange);
        });
        
        // Keyboard shortcuts
        this.eventHandlers.keyboard = (e) => this.handleKeyboard(e);
        LeonardoEnsemble.Utils.dom.on(document, 'keydown', this.eventHandlers.keyboard);
        
        // Window resize
        this.eventHandlers.resize = LeonardoEnsemble.Utils.debounce(() => this.handleResize(), 250);
        LeonardoEnsemble.Utils.dom.on(window, 'resize', this.eventHandlers.resize);
        
        // Instrument controls
        this.setupInstrumentControls();
    }
    
    /**
     * Set up instrument-specific controls
     */
    setupInstrumentControls() {
        this.elements.instrumentMixers.forEach(mixer => {
            const instrumentId = mixer.dataset.instrument;
            const muteBtn = mixer.querySelector('.mute-btn');
            const volumeSlider = mixer.querySelector('.volume-slider');
            const volumeDisplay = mixer.querySelector('.volume-display');
            
            // Mute button
            LeonardoEnsemble.Utils.dom.on(muteBtn, 'click', () => {
                this.toggleInstrumentMute(instrumentId);
            });
            
            // Volume slider
            LeonardoEnsemble.Utils.dom.on(volumeSlider, 'input', (e) => {
                const volume = parseInt(e.target.value);
                this.setInstrumentVolume(instrumentId, volume);
                volumeDisplay.textContent = `${volume}%`;
            });
        });
    }
    
    /**
     * Initialize all instruments
     */
    async initializeInstruments() {
        try {
            // Create instruments
            if (this.elements.carillonCanvas) {
                const carillon = new LeonardoEnsemble.Carillon(this.elements.carillonCanvas);
                this.instruments.set('carillon', carillon);
            }
            
            if (this.elements.drumCanvas) {
                const drum = new LeonardoEnsemble.Drum(this.elements.drumCanvas);
                this.instruments.set('drum', drum);
            }
            
            if (this.elements.organCanvas) {
                const organ = new LeonardoEnsemble.Organ(this.elements.organCanvas);
                this.instruments.set('organ', organ);
            }
            
            if (this.elements.trumpeterCanvas) {
                const trumpeter = new LeonardoEnsemble.Trumpeter(this.elements.trumpeterCanvas);
                this.instruments.set('trumpeter', trumpeter);
            }
            
            if (this.elements.fluteCanvas) {
                const flute = new LeonardoEnsemble.Flute(this.elements.fluteCanvas);
                this.instruments.set('flute', flute);
            }
            
            if (this.elements.violaCanvas) {
                const viola = new LeonardoEnsemble.ViolaOrganista(this.elements.violaCanvas);
                this.instruments.set('viola', viola);
            }
            
            // Set up instrument event listeners
            this.setupInstrumentEvents();
            
        } catch (error) {
            console.error('Failed to initialize instruments:', error);
            throw error;
        }
    }
    
    /**
     * Set up instrument event listeners
     */
    setupInstrumentEvents() {
        this.instruments.forEach((instrument, id) => {
            // Listen for instrument events
            instrument.events.on('notePlay', (data) => {
                this.onInstrumentNotePlay(id, data);
            });
            
            instrument.events.on('beat', (data) => {
                this.onInstrumentBeat(id, data);
            });
            
            instrument.events.on('start', (data) => {
                this.onInstrumentStart(id, data);
            });
            
            instrument.events.on('stop', (data) => {
                this.onInstrumentStop(id, data);
            });
        });
    }
    
    /**
     * Initialize UI components
     */
    initializeUI() {
        // Set initial tempo
        this.elements.tempoSlider.value = this.currentTempo;
        this.elements.tempoDisplay.textContent = `${this.currentTempo} BPM`;
        
        // Set initial composition
        this.elements.compositionSelect.value = this.currentComposition;
        
        // Set initial view mode
        this.setViewMode(this.viewMode);
        
        // Initialize notation renderer
        if (this.elements.notationCanvas) {
            this.notationRenderer = new LeonardoEnsemble.NotationRenderer(this.elements.notationCanvas);
        }
        
        // Initialize music engine
        this.musicEngine = new LeonardoEnsemble.MusicEngine();
        
        // Initialize ensemble controller
        this.ensembleController = new LeonardoEnsemble.EnsembleController(this.instruments);
    }
    
    /**
     * Load a composition
     * @param {string} compositionId - Composition identifier
     */
    async loadComposition(compositionId) {
        try {
            // Load composition data
            const composition = await this.fetchComposition(compositionId);
            
            // Update music engine
            this.musicEngine.loadComposition(composition);
            
            // Update notation renderer
            if (this.notationRenderer) {
                this.notationRenderer.loadComposition(composition);
            }
            
            // Update ensemble controller
            this.ensembleController.loadComposition(composition);
            
            // Update total time display
            this.elements.totalTime.textContent = LeonardoEnsemble.Utils.time.formatTime(composition.duration);
            
            console.log(`Loaded composition: ${composition.title}`);
            
        } catch (error) {
            console.error(`Failed to load composition ${compositionId}:`, error);
            this.showError(`Failed to load composition: ${compositionId}`);
        }
    }
    
    /**
     * Fetch composition data
     * @param {string} compositionId - Composition identifier
     * @returns {Object} Composition data
     */
    async fetchComposition(compositionId) {
        // In a real implementation, this would fetch from an API
        // For now, return mock composition data
        const compositions = {
            'renaissance-dance': {
                id: 'renaissance-dance',
                title: 'Renaissance Court Dance',
                tempo: 120,
                timeSignature: '4/4',
                duration: 225, // 3:45 in seconds
                parts: {
                    'carillon': [
                        { pitch: 261.63, duration: 500, time: 0 },
                        { pitch: 329.63, duration: 500, time: 1000 },
                        { pitch: 392.00, duration: 500, time: 2000 },
                        { pitch: 523.25, duration: 1000, time: 3000 }
                    ],
                    'drum': [
                        { pitch: 100, duration: 200, time: 0 },
                        { pitch: 100, duration: 200, time: 500 },
                        { pitch: 100, duration: 200, time: 1000 },
                        { pitch: 100, duration: 200, time: 1500 }
                    ]
                }
            },
            'madrigal': {
                id: 'madrigal',
                title: 'Madrigal in D Minor',
                tempo: 100,
                timeSignature: '4/4',
                duration: 180, // 3:00 in seconds
                parts: {
                    'organ': [
                        { pitch: 293.66, duration: 1000, time: 0 },
                        { pitch: 349.23, duration: 1000, time: 1000 },
                        { pitch: 440.00, duration: 1000, time: 2000 }
                    ],
                    'flute': [
                        { pitch: 587.33, duration: 500, time: 500 },
                        { pitch: 698.46, duration: 500, time: 1500 }
                    ]
                }
            },
            'galliard': {
                id: 'galliard',
                title: 'Galliard for Six Instruments',
                tempo: 140,
                timeSignature: '6/8',
                duration: 240, // 4:00 in seconds
                parts: {}
            },
            'pavane': {
                id: 'pavane',
                title: 'Pavane for Mechanical Ensemble',
                tempo: 80,
                timeSignature: '2/4',
                duration: 300, // 5:00 in seconds
                parts: {}
            }
        };
        
        return compositions[compositionId] || compositions['renaissance-dance'];
    }
    
    /**
     * Start playback
     */
    play() {
        if (!this.isInitialized || this.isPlaying) return;
        
        try {
            // Start all instruments
            this.instruments.forEach(instrument => {
                instrument.start();
            });
            
            // Start music engine
            this.musicEngine.start();
            
            // Start ensemble controller
            this.ensembleController.start();
            
            // Update UI state
            this.isPlaying = true;
            this.updatePlaybackControls();
            
            console.log('Started playback');
            
        } catch (error) {
            console.error('Failed to start playback:', error);
            this.showError('Failed to start playback');
        }
    }
    
    /**
     * Pause playback
     */
    pause() {
        if (!this.isPlaying) return;
        
        try {
            // Pause all instruments
            this.instruments.forEach(instrument => {
                instrument.pause();
            });
            
            // Pause music engine
            this.musicEngine.pause();
            
            // Pause ensemble controller
            this.ensembleController.pause();
            
            // Update UI state
            this.isPlaying = false;
            this.updatePlaybackControls();
            
            console.log('Paused playback');
            
        } catch (error) {
            console.error('Failed to pause playback:', error);
            this.showError('Failed to pause playback');
        }
    }
    
    /**
     * Stop playback
     */
    stop() {
        if (!this.isInitialized) return;
        
        try {
            // Stop all instruments
            this.instruments.forEach(instrument => {
                instrument.stop();
            });
            
            // Stop music engine
            this.musicEngine.stop();
            
            // Stop ensemble controller
            this.ensembleController.stop();
            
            // Reset timeline
            this.resetTimeline();
            
            // Update UI state
            this.isPlaying = false;
            this.updatePlaybackControls();
            
            console.log('Stopped playback');
            
        } catch (error) {
            console.error('Failed to stop playback:', error);
            this.showError('Failed to stop playback');
        }
    }
    
    /**
     * Handle tempo change
     * @param {Event} event - Input event
     */
    handleTempoChange(event) {
        const tempo = parseInt(event.target.value);
        this.currentTempo = tempo;
        
        // Update display
        this.elements.tempoDisplay.textContent = `${tempo} BPM`;
        
        // Update all instruments
        this.instruments.forEach(instrument => {
            instrument.handleTempoChange(tempo);
        });
        
        // Update music engine
        this.musicEngine.setTempo(tempo);
        
        console.log(`Tempo changed to ${tempo} BPM`);
    }
    
    /**
     * Handle composition change
     * @param {Event} event - Select event
     */
    async handleCompositionChange(event) {
        const compositionId = event.target.value;
        this.currentComposition = compositionId;
        
        // Stop current playback
        this.stop();
        
        // Load new composition
        await this.loadComposition(compositionId);
        
        console.log(`Changed to composition: ${compositionId}`);
    }
    
    /**
     * Handle view mode change
     * @param {string} mode - New view mode
     */
    setViewMode(mode) {
        this.viewMode = mode;
        
        // Update button states
        LeonardoEnsemble.Utils.dom.removeClass(this.elements.viewNotation, 'active');
        LeonardoEnsemble.Utils.dom.removeClass(this.elements.viewAnimation, 'active');
        LeonardoEnsemble.Utils.dom.removeClass(this.elements.viewBoth, 'active');
        
        switch (mode) {
            case 'notation':
                LeonardoEnsemble.Utils.dom.addClass(this.elements.viewNotation, 'active');
                this.showNotationView();
                break;
            case 'animation':
                LeonardoEnsemble.Utils.dom.addClass(this.elements.viewAnimation, 'active');
                this.showAnimationView();
                break;
            case 'both':
                LeonardoEnsemble.Utils.dom.addClass(this.elements.viewBoth, 'active');
                this.showBothView();
                break;
        }
        
        console.log(`View mode changed to: ${mode}`);
    }
    
    /**
     * Show notation view only
     */
    showNotationView() {
        // Show notation, hide animations
        const musicVisualization = LeonardoEnsemble.Utils.dom.get('.music-visualization');
        const instrumentsStage = LeonardoEnsemble.Utils.dom.get('.instruments-stage');
        
        if (musicVisualization) musicVisualization.style.display = 'block';
        if (instrumentsStage) instrumentsStage.style.display = 'none';
    }
    
    /**
     * Show animation view only
     */
    showAnimationView() {
        // Show animations, hide notation
        const musicVisualization = LeonardoEnsemble.Utils.dom.get('.music-visualization');
        const instrumentsStage = LeonardoEnsemble.Utils.dom.get('.instruments-stage');
        
        if (musicVisualization) musicVisualization.style.display = 'none';
        if (instrumentsStage) instrumentsStage.style.display = 'grid';
    }
    
    /**
     * Show both notation and animation
     */
    showBothView() {
        // Show both notation and animations
        const musicVisualization = LeonardoEnsemble.Utils.dom.get('.music-visualization');
        const instrumentsStage = LeonardoEnsemble.Utils.dom.get('.instruments-stage');
        
        if (musicVisualization) musicVisualization.style.display = 'block';
        if (instrumentsStage) instrumentsStage.style.display = 'grid';
    }
    
    /**
     * Handle tab change
     * @param {Event} event - Click event
     */
    handleTabChange(event) {
        const tabBtn = event.target;
        const tabId = tabBtn.dataset.tab;
        
        if (!tabId) return;
        
        // Update button states
        this.elements.tabBtns.forEach(btn => {
            LeonardoEnsemble.Utils.dom.removeClass(btn, 'active');
            LeonardoEnsemble.Utils.dom.setAttr(btn, 'aria-selected', 'false');
        });
        
        LeonardoEnsemble.Utils.dom.addClass(tabBtn, 'active');
        LeonardoEnsemble.Utils.dom.setAttr(tabBtn, 'aria-selected', 'true');
        
        // Update panel visibility
        this.elements.tabPanels.forEach(panel => {
            LeonardoEnsemble.Utils.dom.removeClass(panel, 'active');
        });
        
        const targetPanel = LeonardoEnsemble.Utils.dom.get(`#${tabId}-panel`);
        if (targetPanel) {
            LeonardoEnsemble.Utils.dom.addClass(targetPanel, 'active');
        }
    }
    
    /**
     * Handle keyboard shortcuts
     * @param {Event} event - Keyboard event
     */
    handleKeyboard(event) {
        // Ignore if user is typing in input field
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }
        
        switch (event.key) {
            case ' ':
                event.preventDefault();
                if (this.isPlaying) {
                    this.pause();
                } else {
                    this.play();
                }
                break;
            case 'Escape':
                this.stop();
                break;
            case 'ArrowUp':
                event.preventDefault();
                this.adjustTempo(5);
                break;
            case 'ArrowDown':
                event.preventDefault();
                this.adjustTempo(-5);
                break;
        }
    }
    
    /**
     * Handle window resize
     */
    handleResize() {
        // Resize canvases
        this.instruments.forEach(instrument => {
            instrument.initializeCanvas();
            instrument.draw();
        });
        
        // Resize notation canvas
        if (this.notationRenderer) {
            this.notationRenderer.resize();
        }
    }
    
    /**
     * Toggle instrument mute
     * @param {string} instrumentId - Instrument ID
     */
    toggleInstrumentMute(instrumentId) {
        const instrument = this.instruments.get(instrumentId);
        if (!instrument) return;
        
        const newMutedState = !instrument.isMuted;
        instrument.setMuted(newMutedState);
        
        // Update UI
        const mixer = LeonardoEnsemble.Utils.dom.get(`[data-instrument="${instrumentId}"]`);
        if (mixer) {
            const muteBtn = mixer.querySelector('.mute-btn');
            if (muteBtn) {
                LeonardoEnsemble.Utils.dom.toggleClass(muteBtn, 'muted', newMutedState);
            }
        }
    }
    
    /**
     * Set instrument volume
     * @param {string} instrumentId - Instrument ID
     * @param {number} volume - Volume level (0-100)
     */
    setInstrumentVolume(instrumentId, volume) {
        const instrument = this.instruments.get(instrumentId);
        if (!instrument) return;
        
        instrument.setVolume(volume);
    }
    
    /**
     * Adjust tempo
     * @param {number} delta - Tempo change amount
     */
    adjustTempo(delta) {
        const newTempo = LeonardoEnsemble.Utils.math.clamp(
            this.currentTempo + delta, 
            40, 
            200
        );
        
        this.elements.tempoSlider.value = newTempo;
        this.handleTempoChange({ target: { value: newTempo } });
    }
    
    /**
     * Update playback control states
     */
    updatePlaybackControls() {
        // Update button states
        this.elements.playBtn.disabled = this.isPlaying;
        this.elements.pauseBtn.disabled = !this.isPlaying;
        this.elements.stopBtn.disabled = !this.isPlaying && !this.musicEngine.hasPlayed;
    }
    
    /**
     * Reset timeline to beginning
     */
    resetTimeline() {
        this.elements.timelineProgress.style.width = '0%';
        this.elements.timelineMarker.style.left = '0%';
        this.elements.currentTime.textContent = '0:00';
    }
    
    /**
     * Update timeline position
     * @param {number} currentTime - Current playback time in seconds
     * @param {number} totalTime - Total duration in seconds
     */
    updateTimeline(currentTime, totalTime) {
        const progress = (currentTime / totalTime) * 100;
        
        this.elements.timelineProgress.style.width = `${progress}%`;
        this.elements.timelineMarker.style.left = `${progress}%`;
        this.elements.currentTime.textContent = LeonardoEnsemble.Utils.time.formatTime(currentTime);
    }
    
    /**
     * Handle instrument note play event
     * @param {string} instrumentId - Instrument ID
     * @param {Object} data - Event data
     */
    onInstrumentNotePlay(instrumentId, data) {
        // Update notation display
        if (this.notationRenderer) {
            this.notationRenderer.highlightNote(instrumentId, data.note);
        }
        
        // Update timeline
        if (data.note && data.note.time !== undefined) {
            this.updateTimeline(data.note.time / 1000, this.musicEngine.getDuration());
        }
    }
    
    /**
     * Handle instrument beat event
     * @param {string} instrumentId - Instrument ID
     * @param {Object} data - Event data
     */
    onInstrumentBeat(instrumentId, data) {
        // Visual feedback for beats
        const container = LeonardoEnsemble.Utils.dom.get(`[data-instrument="${instrumentId}"]`);
        if (container) {
            LeonardoEnsemble.Utils.dom.addClass(container, 'beat');
            setTimeout(() => {
                LeonardoEnsemble.Utils.dom.removeClass(container, 'beat');
            }, 100);
        }
    }
    
    /**
     * Handle instrument start event
     * @param {string} instrumentId - Instrument ID
     * @param {Object} data - Event data
     */
    onInstrumentStart(instrumentId, data) {
        console.log(`Instrument ${instrumentId} started`);
    }
    
    /**
     * Handle instrument stop event
     * @param {string} instrumentId - Instrument ID
     * @param {Object} data - Event data
     */
    onInstrumentStop(instrumentId, data) {
        console.log(`Instrument ${instrumentId} stopped`);
    }
    
    /**
     * Show/hide loading overlay with Leonardo's theatrical touch
     * @param {boolean} show - Whether to show loading overlay
     */
    showLoading(show) {
        if (this.elements.loadingOverlay) {
            if (show) {
                LeonardoEnsemble.Utils.dom.removeClass(this.elements.loadingOverlay, 'hidden');
                this.startLoadingTheater();
            } else {
                LeonardoEnsemble.Utils.dom.addClass(this.elements.loadingOverlay, 'hidden');
                this.stopLoadingTheater();
            }
        }
    }
    
    /**
     * Start the Renaissance loading theater experience
     */
    startLoadingTheater() {
        const loadingQuotes = [
            {
                mirror: ".ecnatropmi lacihtem fo ytiliba eht si cisum",
                text: "Music is the arithmetic of sounds as optics is the geometry of light.",
                source: "Codex Atlanticus"
            },
            {
                mirror: ".srucco lautcello na fo esilaer eb nac taht sgniht eht lla era erehT",
                text: "Here there are all the things that can be related to a musical corps.",
                source: "Codex Madrid I"
            },
            {
                mirror: ".emit eht fo scitsitats eht syawa stceffe stnemelpmoc lacihtem",
                text: "Mechanical compositions always effect the statistics of time.",
                source: "Manuscript B"
            },
            {
                mirror: ".ytiliba eht si cisum nehw esrevinu eht syawa stceffe sretniapS",
                text: "Sprains always effect the universe when music is the ability.",
                source: "Codex Leicester"
            }
        ];
        
        const loadingStages = [
            "Tuning the instruments...",
            "Calibrating the mechanisms...",
            "Harmonizing the ensemble...",
            "Preparing the court...",
            "Leonardo's spirit awakens..."
        ];
        
        let currentStage = 0;
        let currentQuote = 0;
        
        // Update loading stages
        this.loadingStageInterval = setInterval(() => {
            const progressText = LeonardoEnsemble.Utils.dom.get('#loading-progress-text');
            const progressFill = LeonardoEnsemble.Utils.dom.get('#loading-progress-fill');
            
            if (progressText && currentStage < loadingStages.length) {
                progressText.textContent = loadingStages[currentStage];
                currentStage++;
            }
            
            if (progressFill) {
                progressFill.style.width = `${(currentStage / loadingStages.length) * 100}%`;
            }
        }, 800);
        
        // Update Leonardo quotes
        this.loadingQuoteInterval = setInterval(() => {
            const mirrorText = LeonardoEnsemble.Utils.dom.get('.leonardo-loading-quote .mirror-text');
            const marginalia = LeonardoEnsemble.Utils.dom.get('.leonardo-loading-quote .leonardo-marginalia');
            
            if (mirrorText && marginalia && currentQuote < loadingQuotes.length) {
                const quote = loadingQuotes[currentQuote];
                mirrorText.textContent = quote.mirror;
                marginalia.innerHTML = `"${quote.text}"<br><span style="text-align: right; display: block;">— Leonardo da Vinci, ${quote.source}</span>`;
                currentQuote++;
            }
        }, 2000);
    }
    
    /**
     * Stop the Renaissance loading theater
     */
    stopLoadingTheater() {
        if (this.loadingStageInterval) {
            clearInterval(this.loadingStageInterval);
            this.loadingStageInterval = null;
        }
        
        if (this.loadingQuoteInterval) {
            clearInterval(this.loadingQuoteInterval);
            this.loadingQuoteInterval = null;
        }
    }
    
    /**
     * Show error message
     * @param {string} message - Error message
     */
    showError(message) {
        // Create error notification
        const errorNotification = LeonardoEnsemble.Utils.dom.create('div', {
            className: 'error-notification',
            textContent: message
        });
        
        // Add to page
        document.body.appendChild(errorNotification);
        
        // Remove after delay
        setTimeout(() => {
            if (errorNotification.parentNode) {
                errorNotification.parentNode.removeChild(errorNotification);
            }
        }, 5000);
    }
    
    /**
     * Dispose of application resources
     */
    dispose() {
        // Stop playback
        this.stop();
        
        // Dispose instruments
        this.instruments.forEach(instrument => {
            instrument.dispose();
        });
        
        // Clear instruments
        this.instruments.clear();
        
        // Remove event listeners
        LeonardoEnsemble.Utils.dom.off(this.elements.playBtn, 'click', this.eventHandlers.play);
        LeonardoEnsemble.Utils.dom.off(this.elements.pauseBtn, 'click', this.eventHandlers.pause);
        LeonardoEnsemble.Utils.dom.off(this.elements.stopBtn, 'click', this.eventHandlers.stop);
        LeonardoEnsemble.Utils.dom.off(this.elements.tempoSlider, 'input', this.eventHandlers.tempoChange);
        LeonardoEnsemble.Utils.dom.off(this.elements.compositionSelect, 'change', this.eventHandlers.compositionChange);
        LeonardoEnsemble.Utils.dom.off(document, 'keydown', this.eventHandlers.keyboard);
        LeonardoEnsemble.Utils.dom.off(window, 'resize', this.eventHandlers.resize);
        
        // Clear references
        this.elements = {};
        this.eventHandlers = {};
        
        console.log('Leonardo\'s Mechanical Ensemble disposed');
    }
};

// Initialize application when script loads
const app = new LeonardoEnsemble.App();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LeonardoEnsemble.App;
}