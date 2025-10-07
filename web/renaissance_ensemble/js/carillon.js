/**
 * Leonardo's Mechanical Ensemble - Mechanical Carillon
 * Clock-driven bell system with rotating drum and strikers
 */

// Ensure namespace exists
window.LeonardoEnsemble = window.LeonardoEnsemble || {};

/**
 * Mechanical Carillon Instrument
 * Implements Leonardo's clock-driven carillon design
 */
LeonardoEnsemble.Carillon = class extends LeonardoEnsemble.InstrumentBase {
    /**
     * Create a new Carillon instrument
     * @param {HTMLCanvasElement} canvas - Canvas element for rendering
     * @param {Object} options - Configuration options
     */
    constructor(canvas, options = {}) {
        super('carillon', 'Mechanical Carillon', canvas, options);
        
        // Carillon-specific properties
        this.bellCount = options.bellCount || 8;
        this.drumRotation = 0;
        this.drumSpeed = 0.5; // Rotation speed in radians per second
        this.strikerPositions = [];
        this.activeStrikers = new Set();
        this.bellFrequencies = [];
        
        // Visual properties
        this.drumRadius = 60;
        this.drumCenterX = 150;
        this.drumCenterY = 200;
        this.bellRadius = 15;
        this.bellSpacing = 30;
        this.strikerLength = 40;
        
        // Animation properties
        this.strikerAnimations = new Map();
        this.bellAnimations = new Map();
        this.bellResonance = new Map();
        
        // Initialize carillon
        this.initializeCarillon();
    }
    
    /**
     * Initialize carillon components
     */
    initializeCarillon() {
        // Calculate bell frequencies (musical scale)
        const baseFrequency = 261.63; // C4
        const scale = [0, 2, 4, 5, 7, 9, 11, 12]; // Major scale
        
        for (let i = 0; i < this.bellCount; i++) {
            const semitone = scale[i % scale.length];
            const octave = Math.floor(i / scale.length);
            this.bellFrequencies[i] = baseFrequency * Math.pow(2, (semitone + octave * 12) / 12);
            
            // Initialize bell resonance
            this.bellResonance.set(i, {
                amplitude: 0,
                decay: 0.98,
                frequency: this.bellFrequencies[i]
            });
        }
        
        // Generate random striker positions on drum
        this.generateStrikerPositions();
        
        // Set up drum rotation based on tempo
        this.updateDrumSpeed();
    }
    
    /**
     * Generate random striker positions on the drum
     */
    generateStrikerPositions() {
        this.strikerPositions = [];
        
        // Create a pattern of pins around the drum
        const pinCount = 24;
        for (let i = 0; i < pinCount; i++) {
            const angle = (i / pinCount) * Math.PI * 2;
            const radius = this.drumRadius * 0.8;
            
            // Randomly assign pins to different bells
            const bellIndex = Math.floor(Math.random() * this.bellCount);
            
            this.strikerPositions.push({
                angle: angle,
                radius: radius,
                bellIndex: bellIndex,
                triggered: false
            });
        }
    }
    
    /**
     * Set up carillon-specific components
     */
    setupComponents() {
        // Drum component
        this.addComponent('drum', {
            x: this.drumCenterX,
            y: this.drumCenterY,
            radius: this.drumRadius,
            rotation: 0,
            update: (deltaTime) => {
                if (this.isPlaying) {
                    this.drumRotation += this.drumSpeed * deltaTime / 1000;
                    this.rotation = this.drumRotation;
                }
            },
            draw: (ctx) => {
                this.drawDrum(ctx);
            }
        });
        
        // Bell rack component
        this.addComponent('bellRack', {
            x: this.drumCenterX,
            y: this.drumCenterY - 120,
            width: this.bellSpacing * (this.bellCount - 1),
            height: 60,
            update: () => {},
            draw: (ctx) => {
                this.drawBellRack(ctx);
            }
        });
        
        // Strikers component
        this.addComponent('strikers', {
            update: (deltaTime) => {
                this.updateStrikers(deltaTime);
            },
            draw: (ctx) => {
                this.drawStrikers(ctx);
            }
        });
    }
    
    /**
     * Update drum speed based on tempo
     */
    updateDrumSpeed() {
        // Adjust drum rotation speed based on tempo
        // One complete rotation should take approximately 4 beats
        const beatsPerRotation = 4;
        const secondsPerBeat = 60 / this.tempo;
        const secondsPerRotation = beatsPerRotation * secondsPerBeat;
        this.drumSpeed = (Math.PI * 2) / secondsPerRotation;
    }
    
    /**
     * Handle tempo change
     * @param {number} tempo - New tempo in BPM
     */
    handleTempoChange(tempo) {
        super.handleTempoChange(tempo);
        this.updateDrumSpeed();
    }
    
    /**
     * Update striker animations and check for triggers
     * @param {number} deltaTime - Time since last frame
     */
    updateStrikers(deltaTime) {
        // Reset triggered flags
        this.strikerPositions.forEach(pin => {
            pin.triggered = false;
        });
        
        // Check for pin triggers
        this.strikerPositions.forEach(pin => {
            const pinAngle = pin.angle + this.drumRotation;
            const normalizedAngle = pinAngle % (Math.PI * 2);
            
            // Check if pin is at trigger position (bottom of drum)
            const triggerAngle = Math.PI * 1.5; // Bottom position
            const angleDiff = Math.abs(normalizedAngle - triggerAngle);
            
            if (angleDiff < 0.1 && !pin.triggered) {
                this.triggerStriker(pin.bellIndex);
                pin.triggered = true;
            }
        });
        
        // Update striker animations
        this.strikerAnimations.forEach((animation, bellIndex) => {
            animation.time += deltaTime;
            
            if (animation.state === 'striking') {
                // Move striker towards bell
                const progress = animation.time / animation.strikeDuration;
                if (progress >= 1) {
                    animation.state = 'retracting';
                    animation.time = 0;
                } else {
                    animation.position = this.easeInOutQuad(progress);
                }
            } else if (animation.state === 'retracting') {
                // Move striker back to rest position
                const progress = animation.time / animation.retractDuration;
                if (progress >= 1) {
                    this.strikerAnimations.delete(bellIndex);
                } else {
                    animation.position = 1 - this.easeInOutQuad(progress);
                }
            }
        });
        
        // Update bell resonance
        this.bellResonance.forEach((resonance, bellIndex) => {
            if (resonance.amplitude > 0.01) {
                resonance.amplitude *= resonance.decay;
            } else {
                resonance.amplitude = 0;
            }
        });
    }
    
    /**
     * Trigger a striker for a specific bell
     * @param {number} bellIndex - Bell index to strike
     */
    triggerStriker(bellIndex) {
        if (this.isMuted) return;
        
        // Create striker animation
        this.strikerAnimations.set(bellIndex, {
            state: 'striking',
            position: 0,
            time: 0,
            strikeDuration: 100,
            retractDuration: 200
        });
        
        // Start bell resonance
        this.bellResonance.get(bellIndex).amplitude = 1;
        
        // Create visual effect
        this.createBellEffect(bellIndex);
        
        // Play note
        this.playNote({
            pitch: this.bellFrequencies[bellIndex],
            duration: 500,
            bellIndex: bellIndex
        });
        
        // Add active striker
        this.activeStrikers.add(bellIndex);
        
        // Remove from active strikers after animation
        setTimeout(() => {
            this.activeStrikers.delete(bellIndex);
        }, 300);
    }
    
    /**
     * Create visual effect for bell strike
     * @param {number} bellIndex - Bell index
     */
    createBellEffect(bellIndex) {
        const bellX = this.drumCenterX - (this.bellSpacing * (this.bellCount - 1) / 2) + (bellIndex * this.bellSpacing);
        const bellY = this.drumCenterY - 120;
        
        // Create particle effect
        for (let i = 0; i < 5; i++) {
            this.addParticle({
                x: bellX,
                y: bellY,
                vx: LeonardoEnsemble.Utils.math.random(-2, 2),
                vy: LeonardoEnsemble.Utils.math.random(-3, -1),
                life: 1,
                decay: 0.02,
                size: LeonardoEnsemble.Utils.math.random(2, 4),
                color: `hsla(${45 + bellIndex * 10}, 70%, 60%, `,
                update: function(deltaTime) {
                    this.x += this.vx;
                    this.y += this.vy;
                    this.vy += 0.1; // Gravity
                    this.life -= this.decay;
                },
                draw: function(ctx) {
                    ctx.save();
                    ctx.globalAlpha = this.life;
                    ctx.fillStyle = this.color + this.life + ')';
                    LeonardoEnsemble.Utils.canvas.drawCircle(ctx, this.x, this.y, this.size);
                    ctx.restore();
                },
                isAlive: function() {
                    return this.life > 0;
                }
            });
        }
    }
    
    /**
     * Draw the drum
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     */
    drawDrum(ctx) {
        ctx.save();
        ctx.translate(this.drumCenterX, this.drumCenterY);
        ctx.rotate(this.drumRotation);
        
        // Draw drum cylinder
        const gradient = ctx.createLinearGradient(-this.drumRadius, 0, this.drumRadius, 0);
        gradient.addColorStop(0, '#8B4513');
        gradient.addColorStop(0.5, '#A0522D');
        gradient.addColorStop(1, '#8B4513');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(-this.drumRadius, -20, this.drumRadius * 2, 40);
        
        // Draw drum ends
        ctx.fillStyle = '#654321';
        ctx.beginPath();
        ctx.ellipse(0, -20, this.drumRadius, 15, 0, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.beginPath();
        ctx.ellipse(0, 20, this.drumRadius, 15, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw pins
        this.strikerPositions.forEach(pin => {
            const x = Math.cos(pin.angle) * pin.radius;
            const y = Math.sin(pin.angle) * 10; // Flatten for perspective
            
            ctx.fillStyle = '#FFD700';
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fill();
            
            // Draw pin connection to bell
            ctx.strokeStyle = '#FFD700';
            ctx.lineWidth = 1;
            ctx.setLineDash([2, 2]);
            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.lineTo(x, y + 30);
            ctx.stroke();
            ctx.setLineDash([]);
        });
        
        ctx.restore();
    }
    
    /**
     * Draw the bell rack
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     */
    drawBellRack(ctx) {
        const rackY = this.drumCenterY - 120;
        const rackStartX = this.drumCenterX - (this.bellSpacing * (this.bellCount - 1) / 2);
        
        // Draw rack frame
        ctx.fillStyle = '#654321';
        ctx.fillRect(rackStartX - 10, rackY - 20, this.bellSpacing * (this.bellCount - 1) + 20, 40);
        
        // Draw bells
        for (let i = 0; i < this.bellCount; i++) {
            const bellX = rackStartX + (i * this.bellSpacing);
            const resonance = this.bellResonance.get(i);
            
            // Bell glow effect when resonating
            if (resonance.amplitude > 0.01) {
                ctx.save();
                ctx.globalAlpha = resonance.amplitude * 0.3;
                ctx.fillStyle = '#FFD700';
                LeonardoEnsemble.Utils.canvas.drawCircle(ctx, bellX, rackY, this.bellRadius + 5);
                ctx.restore();
            }
            
            // Draw bell
            const bellGradient = ctx.createRadialGradient(bellX - 5, rackY - 5, 0, bellX, rackY, this.bellRadius);
            bellGradient.addColorStop(0, '#FFD700');
            bellGradient.addColorStop(0.7, '#FFA500');
            bellGradient.addColorStop(1, '#FF8C00');
            
            ctx.fillStyle = bellGradient;
            ctx.beginPath();
            ctx.arc(bellX, rackY, this.bellRadius, 0, Math.PI * 2);
            ctx.fill();
            
            // Bell outline
            ctx.strokeStyle = '#B8860B';
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Bell clapper
            ctx.fillStyle = '#654321';
            ctx.beginPath();
            ctx.arc(bellX, rackY + 5, 3, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    /**
     * Draw strikers
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     */
    drawStrikers(ctx) {
        const rackY = this.drumCenterY - 120;
        const rackStartX = this.drumCenterX - (this.bellSpacing * (this.bellCount - 1) / 2);
        
        for (let i = 0; i < this.bellCount; i++) {
            const bellX = rackStartX + (i * this.bellSpacing);
            const animation = this.strikerAnimations.get(i);
            
            // Calculate striker position
            let strikerY = rackY + 40; // Rest position
            if (animation) {
                const strikeDistance = 30;
                strikerY = rackY + 40 - (animation.position * strikeDistance);
            }
            
            // Draw striker arm
            ctx.strokeStyle = '#8B4513';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(bellX, strikerY + 20);
            ctx.lineTo(bellX, strikerY);
            ctx.stroke();
            
            // Draw striker hammer
            const hammerGradient = ctx.createRadialGradient(bellX, strikerY, 0, bellX, strikerY, 8);
            hammerGradient.addColorStop(0, '#D2691E');
            hammerGradient.addColorStop(1, '#8B4513');
            
            ctx.fillStyle = hammerGradient;
            ctx.beginPath();
            ctx.arc(bellX, strikerY, 8, 0, Math.PI * 2);
            ctx.fill();
            
            // Striker outline
            ctx.strokeStyle = '#654321';
            ctx.lineWidth = 1;
            ctx.stroke();
            
            // Highlight active striker
            if (this.activeStrikers.has(i)) {
                ctx.save();
                ctx.strokeStyle = '#FFD700';
                ctx.lineWidth = 2;
                ctx.setLineDash([2, 2]);
                ctx.beginPath();
                ctx.arc(bellX, strikerY, 12, 0, Math.PI * 2);
                ctx.stroke();
                ctx.restore();
            }
        }
    }
    
    /**
     * Handle note play
     * @param {Object} note - Note object
     */
    onNotePlay(note) {
        // Visual feedback for note play
        const bellIndex = note.bellIndex;
        if (bellIndex !== undefined) {
            this.createBellEffect(bellIndex);
        }
    }
    
    /**
     * Draw background with clock mechanism
     */
    drawBackground() {
        super.drawBackground();
        
        // Draw clock face background
        ctx.save();
        ctx.translate(this.drumCenterX, this.drumCenterY);
        
        // Clock face
        ctx.strokeStyle = 'rgba(139, 69, 19, 0.3)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(0, 0, this.drumRadius + 30, 0, Math.PI * 2);
        ctx.stroke();
        
        // Hour markers
        for (let i = 0; i < 12; i++) {
            const angle = (i / 12) * Math.PI * 2 - Math.PI / 2;
            const x1 = Math.cos(angle) * (this.drumRadius + 20);
            const y1 = Math.sin(angle) * (this.drumRadius + 20);
            const x2 = Math.cos(angle) * (this.drumRadius + 25);
            const y2 = Math.sin(angle) * (this.drumRadius + 25);
            
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }
        
        ctx.restore();
    }
    
    /**
     * Ease in out quadratic function
     * @param {number} t - Input value (0-1)
     * @returns {number} Eased value
     */
    easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }
    
    /**
     * Reset carillon to initial state
     */
    resetComponents() {
        super.resetComponents();
        
        this.drumRotation = 0;
        this.activeStrikers.clear();
        this.strikerAnimations.clear();
        
        // Reset bell resonance
        this.bellResonance.forEach(resonance => {
            resonance.amplitude = 0;
        });
        
        // Reset pin triggers
        this.strikerPositions.forEach(pin => {
            pin.triggered = false;
        });
    }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LeonardoEnsemble.Carillon;
}