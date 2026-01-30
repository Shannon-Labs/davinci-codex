/**
 * Leonardo's Mechanical Ensemble - Main Application
 * MP3 demo player with WebAudio visualization and timbre card synthesis
 */

// Ensure namespace exists
window.LeonardoEnsemble = window.LeonardoEnsemble || {};

/**
 * Main Application Class
 * Coordinates MP3 playback, visualizer, timbre card synthesis, and educational panels
 */
LeonardoEnsemble.App = class {
    constructor() {
        this.isInitialized = false;
        this.elements = {};
        this.eventHandlers = {};

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
            this.cacheElements();
            this.showLoading(true);
            this.setupEventListeners();

            // Initialize AudioEngine (Web Audio API)
            if (LeonardoEnsemble.AudioEngine) {
                this.audioEngine = new LeonardoEnsemble.AudioEngine();
            }

            this.showLoading(false);
            this.isInitialized = true;
            console.log("Leonardo's Mechanical Ensemble initialized successfully");
        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.showError("Failed to initialize Leonardo's Mechanical Ensemble");
            this.showLoading(false);
        }
    }

    /**
     * Cache frequently used DOM elements
     */
    cacheElements() {
        this.elements = {
            // Educational panels
            tabBtns: LeonardoEnsemble.Utils.dom.getAll('.tab-btn'),
            tabPanels: LeonardoEnsemble.Utils.dom.getAll('.tab-panel'),

            // Loading overlay
            loadingOverlay: LeonardoEnsemble.Utils.dom.get('#loading-overlay'),

            // Audio engine elements
            playBtn: LeonardoEnsemble.Utils.dom.get('#enter-court-btn'),
            audioVisualizer: LeonardoEnsemble.Utils.dom.get('#audio-visualizer'),
            trackSelect: LeonardoEnsemble.Utils.dom.get('#track-select'),
            audioPlayer: LeonardoEnsemble.Utils.dom.get('.audio-player'),
            timbreCards: LeonardoEnsemble.Utils.dom.getAll('.timbre-card[data-instrument]')
        };
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Tab controls
        this.eventHandlers.tabChange = (e) => this.handleTabChange(e);
        this.elements.tabBtns.forEach(btn => {
            LeonardoEnsemble.Utils.dom.on(btn, 'click', this.eventHandlers.tabChange);
        });

        // Keyboard shortcuts
        this.eventHandlers.keyboard = (e) => this.handleKeyboard(e);
        LeonardoEnsemble.Utils.dom.on(document, 'keydown', this.eventHandlers.keyboard);

        // Play / Pause button
        if (this.elements.playBtn) {
            LeonardoEnsemble.Utils.dom.on(this.elements.playBtn, 'click', () => this.handlePlayToggle());
        }

        // Track selector
        if (this.elements.trackSelect) {
            LeonardoEnsemble.Utils.dom.on(this.elements.trackSelect, 'change', (e) => this.handleTrackChange(e));
        }

        // Timbre card clicks + keyboard (Enter/Space)
        if (this.elements.timbreCards) {
            this.elements.timbreCards.forEach(card => {
                const id = card.dataset.instrument;
                LeonardoEnsemble.Utils.dom.on(card, 'click', () => this.handleTimbreCardClick(id, card));
                LeonardoEnsemble.Utils.dom.on(card, 'keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.handleTimbreCardClick(id, card);
                    }
                });
            });
        }
    }

    // ---- Audio playback ----

    /**
     * Toggle MP3 demo playback and visualizer.
     */
    handlePlayToggle() {
        if (!this.audioEngine) return;

        const audioEl = this.elements.audioPlayer;
        const canvas = this.elements.audioVisualizer;
        const btn = this.elements.playBtn;

        if (!audioEl) return;

        // If already playing, pause
        if (!audioEl.paused) {
            audioEl.pause();
            this.audioEngine.stopVisualizer();
            if (btn) btn.textContent = '\u25b6 Play';
            return;
        }

        this.audioEngine.playDemo(audioEl);
        if (canvas) this.audioEngine.startVisualizer(canvas);
        if (btn) btn.textContent = '\u23f8 Pause';

        // Reset button when track ends
        audioEl.addEventListener('ended', () => {
            this.audioEngine.stopVisualizer();
            if (btn) btn.textContent = '\u25b6 Play';
        }, { once: true });
    }

    /**
     * Handle track selector change — swap the <audio> source and update info.
     * @param {Event} e
     */
    handleTrackChange(e) {
        const sel = e.target;
        const value = sel.value;
        const opt = sel.options[sel.selectedIndex];

        const audioEl = this.elements.audioPlayer;
        if (!audioEl) return;

        // Pause current playback
        const wasPlaying = !audioEl.paused;
        if (wasPlaying && this.audioEngine) {
            this.audioEngine.stopDemo(audioEl);
            this.audioEngine.stopVisualizer();
        }

        // Swap source
        const sourceEl = audioEl.querySelector('source');
        if (sourceEl) {
            sourceEl.src = `assets/demo_${value}.mp3`;
        }
        audioEl.load();

        // Update track info
        const titleEl = document.querySelector('.track-title');
        const metaEl = document.querySelector('.track-meta');
        if (titleEl && opt) titleEl.textContent = `"${opt.dataset.title}"`;
        if (metaEl && opt) metaEl.textContent = opt.dataset.meta;

        // Update showcase header
        const showcaseTitle = document.querySelector('.audio-showcase-title');
        if (showcaseTitle && opt) {
            const formName = opt.textContent.trim();
            showcaseTitle.textContent = `Demo: ${formName}`;
        }

        // Reset play button
        const btn = this.elements.playBtn;
        if (btn) btn.textContent = '\u25b6 Play';

        // Resume if was playing
        if (wasPlaying && this.audioEngine) {
            audioEl.addEventListener('canplay', () => {
                this.handlePlayToggle();
            }, { once: true });
        }
    }

    /**
     * Handle timbre card click — synthesize the instrument's note.
     * @param {string} id    - instrument key
     * @param {HTMLElement} card
     */
    handleTimbreCardClick(id, card) {
        if (!this.audioEngine) return;
        this.audioEngine.playNote(id);

        // Brief visual flash
        card.style.borderColor = 'var(--leonardo-gold)';
        card.style.boxShadow = 'var(--glow-leonardo-strong)';
        setTimeout(() => {
            card.style.borderColor = '';
            card.style.boxShadow = '';
        }, 400);
    }

    // ---- Tab handling ----

    /**
     * Handle tab change for educational panels
     * @param {Event} event - Click event
     */
    handleTabChange(event) {
        const tabBtn = event.target;
        const tabId = tabBtn.dataset.tab;

        if (!tabId) return;

        this.elements.tabBtns.forEach(btn => {
            LeonardoEnsemble.Utils.dom.removeClass(btn, 'active');
            LeonardoEnsemble.Utils.dom.setAttr(btn, 'aria-selected', 'false');
        });

        LeonardoEnsemble.Utils.dom.addClass(tabBtn, 'active');
        LeonardoEnsemble.Utils.dom.setAttr(tabBtn, 'aria-selected', 'true');

        this.elements.tabPanels.forEach(panel => {
            LeonardoEnsemble.Utils.dom.removeClass(panel, 'active');
        });

        const targetPanel = LeonardoEnsemble.Utils.dom.get(`#${tabId}-panel`);
        if (targetPanel) {
            LeonardoEnsemble.Utils.dom.addClass(targetPanel, 'active');
        }
    }

    // ---- Keyboard shortcuts ----

    /**
     * Handle keyboard shortcuts (Space = play/pause)
     * @param {Event} event
     */
    handleKeyboard(event) {
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA' || event.target.tagName === 'SELECT') {
            return;
        }

        if (event.key === ' ') {
            event.preventDefault();
            this.handlePlayToggle();
        }
    }

    // ---- Loading theater ----

    /**
     * Show/hide loading overlay
     * @param {boolean} show
     */
    showLoading(show) {
        if (this.elements.loadingOverlay) {
            if (show) {
                this.elements.loadingOverlay.style.display = '';
                this.elements.loadingOverlay.style.opacity = '1';
                this.startLoadingTheater();
            } else {
                this.stopLoadingTheater();
                this.elements.loadingOverlay.style.opacity = '0';
                setTimeout(() => {
                    this.elements.loadingOverlay.style.display = 'none';
                }, 500);
            }
        }
    }

    /**
     * Start the loading theater with verified Leonardo quotes
     */
    startLoadingTheater() {
        const loadingQuotes = [
            {
                mirror: ".noitacitsihpos etamitlu eht si yticilpmiS",
                text: "Simplicity is the ultimate sophistication.",
                source: "commonly attributed"
            },
            {
                mirror: ".egdelwonk si nem doog fo erised larutan ehT",
                text: "The natural desire of good men is knowledge.",
                source: "Codex Atlanticus"
            },
            {
                mirror: ".gnitniap fo retsis eht dellac eb yam cisuM",
                text: "Music may be called the sister of painting.",
                source: "Trattato della Pittura"
            },
            {
                mirror: ".tra on si ereht ,dnah eht htiw krow ton seod tirips eht erehW",
                text: "Where the spirit does not work with the hand, there is no art.",
                source: "Codex Atlanticus"
            }
        ];

        const loadingStages = [
            "Tuning the instruments...",
            "Calibrating the mechanisms...",
            "Harmonizing the ensemble...",
            "Preparing the court...",
            "The court awaits..."
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
                marginalia.innerHTML = `"${quote.text}"<br><span style="text-align: right; display: block;">\u2014 Leonardo da Vinci, ${quote.source}</span>`;
                currentQuote++;
            }
        }, 2000);
    }

    /**
     * Stop the loading theater intervals
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
     * @param {string} message
     */
    showError(message) {
        const errorNotification = LeonardoEnsemble.Utils.dom.create('div', {
            className: 'error-notification',
            textContent: message
        });

        document.body.appendChild(errorNotification);

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
        if (this.audioEngine) {
            this.audioEngine.stopVisualizer();
            const audioEl = this.elements.audioPlayer;
            if (audioEl) this.audioEngine.stopDemo(audioEl);
        }

        LeonardoEnsemble.Utils.dom.off(document, 'keydown', this.eventHandlers.keyboard);

        this.elements = {};
        this.eventHandlers = {};

        console.log("Leonardo's Mechanical Ensemble disposed");
    }
};

// Initialize application when script loads
const app = new LeonardoEnsemble.App();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LeonardoEnsemble.App;
}
