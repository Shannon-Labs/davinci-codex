/**
 * Leonardo's Mechanical Ensemble - Mechanical Drum
 * Programmable percussion device using pinned barrels
 */

// Ensure namespace exists
window.LeonardoEnsemble = window.LeonardoEnsemble || {};

/**
 * Mechanical Drum Instrument
 * Implements Leonardo's pinned barrel percussion design
 */
LeonardoEnsemble.Drum = class extends LeonardoEnsemble.InstrumentBase {
    /**
     * Create a new Drum instrument
     * @param {HTMLCanvasElement} canvas - Canvas element for rendering
     * @param {Object} options - Configuration options
     */
    constructor(canvas, options = {}) {
        super('drum', 'Mechanical Drum', canvas, options);
        
        // Drum-specific properties
        this.barrelRotation = 0;
        this.barrelSpeed = 1.0; // Rotation speed in radians per second
        this.pinPositions = [];
        this.activeBeaters = new Set();
        
        // Visual properties
        this.barrelRadius = 50;
        this.barrelLength = 120;
        this.barrelCenterX = 125;
        this.barrelCenterY = 150;
        this.drumRadius = 60;
        this.drumCenterX = 125;
        this.drumCenterY = 220;
        this.beaterLength = 50;
        this.beaterCount = 4;
        
        // Animation properties
        this.beaterAnimations = new Map();
        this.drumVibration = 0;
        this.drumHeadResonance = 0;
        
        // Sound properties
        this.drumPitch = 100; // Base pitch for drum
        this.rhythmPatterns = [];
        this.currentPattern = 0;
        
        // Initialize drum
        this.initializeDrum();
    }
    
    /**
     * Initialize drum components
     */
    initializeDrum() {
        // Generate rhythm patterns
        this.generateRhythmPatterns();
        
        // Generate pin positions on barrel
        this.generatePinPositions();
        
        // Set up barrel rotation based on tempo
        this.updateBarrelSpeed();
    }
    
    /**
     * Generate rhythm patterns for the drum
     */
    generateRhythmPatterns() {
        this.rhythmPatterns = [
            // Pattern 1: Simple 4/4 beat
            [
                { position: 0, beater: 0, strength: 1.0 },
                { position: 0.5, beater: 1, strength: 0.8 },
                { position: 1.0, beater: 0, strength: 1.0 },
                { position: 1.5, beater: 1, strength: 0.8 }
            ],
            // Pattern 2: Syncopated rhythm
            [
                { position: 0, beater: 0, strength: 0.9 },
                { position: 0.25, beater: 2, strength: 0.7 },
                { position: 0.75, beater: 1, strength: 0.8 },
                { position: 1.0, beater: 0, strength: 0.9 },
                { position: 1.25, beater: 3, strength: 0.6 },
                { position: 1.75, beater: 1, strength: 0.8 }
            ],
            // Pattern 3: March rhythm
            [
                { position: 0, beater: 0, strength: 1.0 },
                { position: 0.5, beater: 1, strength: 0.5 },
                { position: 1.0, beater: 0, strength: 1.0 },
                { position: 1.5, beater: 1, strength: 0.5 }
            ]
        ];
    }
    
    /**
     * Generate pin positions on the barrel
     */
    generatePinPositions() {
        this.pinPositions = [];
        
        // Use current rhythm pattern
        const pattern = this.rhythmPatterns[this.currentPattern];
        
        pattern.forEach(beat => {
            // Convert position (in beats) to angle on barrel
            const angle = (beat.position / 2) * Math.PI * 2; // 2 beats per rotation
            
            // Determine pin height based on beater
            const beaterOffset = beat.beater * (this.barrelLength / (this.beaterCount + 1));
            const pinHeight = -this.barrelLength/2 + beaterOffset;
            
            this.pinPositions.push({
                angle: angle,
                height: pinHeight,
                beater: beat.beater,
                strength: beat.strength,
                triggered: false
            });
        });
    }
    
    /**
     * Set up drum-specific components
     */
    setupComponents() {
        // Barrel component
        this.addComponent('barrel', {
            x: this.barrelCenterX,
            y: this.barrelCenterY,
            radius: this.barrelRadius,
            length: this.barrelLength,
            rotation: 0,
            update: (deltaTime) => {
                if (this.isPlaying) {
                    this.barrelRotation += this.barrelSpeed * deltaTime / 1000;
                    this.rotation = this.barrelRotation;
                }
            },
            draw: (ctx) => {
                this.drawBarrel(ctx);
            }
        });
        
        // Drum component
        this.addComponent('drum', {
            x: this.drumCenterX,
            y: this.drumCenterY,
            radius: this.drumRadius,
            update: (deltaTime) => {
                this.updateDrumVibration(deltaTime);
            },
            draw: (ctx) => {
                this.drawDrum(ctx);
            }
        });
        
        // Beaters component
        this.addComponent('beaters', {
            update: (deltaTime) => {
                this.updateBeaters(deltaTime);
            },
            draw: (ctx) => {
                this.drawBeaters(ctx);
            }
        });
    }
    
    /**
     * Update barrel speed based on tempo
     */
    updateBarrelSpeed() {
        // One complete rotation should take exactly 2 beats
        const beatsPerRotation = 2;
        const secondsPerBeat = 60 / this.tempo;
        const secondsPerRotation = beatsPerRotation * secondsPerBeat;
        this.barrelSpeed = (Math.PI * 2) / secondsPerRotation;
    }
    
    /**
     * Handle tempo change
     * @param {number} tempo - New tempo in BPM
     */
    handleTempoChange(tempo) {
        super.handleTempoChange(tempo);
        this.updateBarrelSpeed();
    }
    
    /**
     * Update beater animations and check for pin triggers
     * @param {number} deltaTime - Time since last frame
     */
    updateBeaters(deltaTime) {
        // Reset triggered flags
        this.pinPositions.forEach(pin => {
            pin.triggered = false;
        });
        
        // Check for pin triggers
        this.pinPositions.forEach(pin => {
            const pinAngle = pin.angle + this.barrelRotation;
            const normalizedAngle = pinAngle % (Math.PI * 2);
            
            // Check if pin is at trigger position (bottom of barrel rotation)
            const triggerAngle = Math.PI * 1.5; // Bottom position
            const angleDiff = Math.abs(normalizedAngle - triggerAngle);
            
            if (angleDiff < 0.1 && !pin.triggered) {
                this.triggerBeater(pin.beater, pin.strength);
                pin.triggered = true;
            }
        });
        
        // Update beater animations
        this.beaterAnimations.forEach((animation, beaterIndex) => {
            animation.time += deltaTime;
            
            if (animation.state === 'striking') {
                // Move beater towards drum
                const progress = animation.time / animation.strikeDuration;
                if (progress >= 1) {
                    animation.state = 'retracting';
                    animation.time = 0;
                } else {
                    animation.position = this.easeOutQuad(progress);
                }
            } else if (animation.state === 'retracting') {
                // Move beater back to rest position
                const progress = animation.time / animation.retractDuration;
                if (progress >= 1) {
                    this.beaterAnimations.delete(beaterIndex);
                } else {
                    animation.position = 1 - this.easeInQuad(progress);
                }
            }
        });
    }
    
    /**
     * Update drum vibration and resonance
     * @param {number} deltaTime - Time since last frame
     */
    updateDrumVibration(deltaTime) {
        // Decay drum vibration
        this.drumVibration *= 0.95;
        this.drumHeadResonance *= 0.92;
        
        // Add small random vibration when playing
        if (this.isPlaying && this.drumVibration > 0.01) {
            this.drumVibration += Math.random() * 0.5;
        }
    }
    
    /**
     * Trigger a beater
     * @param {number} beaterIndex - Beater index to trigger
     * @param {number} strength - Strike strength (0-1)
     */
    triggerBeater(beaterIndex, strength) {
        if (this.isMuted) return;
        
        // Create beater animation
        this.beaterAnimations.set(beaterIndex, {
            state: 'striking',
            position: 0,
            time: 0,
            strikeDuration: 80,
            retractDuration: 150,
            strength: strength
        });
        
        // Set drum vibration based on strike strength
        this.drumVibration = 10 * strength;
        this.drumHeadResonance = 1 * strength;
        
        // Create visual effect
        this.createDrumEffect(beaterIndex, strength);
        
        // Play note with pitch variation based on beater
        const pitchVariation = 1 + (beaterIndex * 0.1);
        this.playNote({
            pitch: this.drumPitch * pitchVariation,
            duration: 200,
            beaterIndex: beaterIndex,
            strength: strength
        });
        
        // Add active beater
        this.activeBeaters.add(beaterIndex);
        
        // Remove from active beaters after animation
        setTimeout(() => {
            this.activeBeaters.delete(beaterIndex);
        }, 230);
    }
    
    /**
     * Create visual effect for drum strike
     * @param {number} beaterIndex - Beater index
     * @param {number} strength - Strike strength
     */
    createDrumEffect(beaterIndex, strength) {
        // Calculate beater position
        const beaterAngle = (beaterIndex / this.beaterCount) * Math.PI * 2 - Math.PI / 2;
        const beaterX = this.drumCenterX + Math.cos(beaterAngle) * (this.drumRadius + 20);
        const beaterY = this.drumCenterY + Math.sin(beaterAngle) * (this.drumRadius + 20);
        
        // Create impact particles
        const particleCount = Math.floor(3 * strength);
        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 3 + 1;
            
            this.addParticle({
                x: beaterX,
                y: beaterY,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed - 2,
                life: 1,
                decay: 0.03,
                size: Math.random() * 3 + 1,
                color: `hsla(${30 + Math.random() * 30}, 60%, 40%, `,
                update: function(deltaTime) {
                    this.x += this.vx;
                    this.y += this.vy;
                    this.vy += 0.2; // Gravity
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
        
        // Create sound wave effect
        this.addParticle({
            x: this.drumCenterX,
            y: this.drumCenterY,
            radius: this.drumRadius,
            maxRadius: this.drumRadius + 30,
            life: 1,
            decay: 0.05,
            update: function(deltaTime) {
                this.radius += 2;
                this.life -= this.decay;
            },
            draw: function(ctx) {
                ctx.save();
                ctx.globalAlpha = this.life * 0.3;
                ctx.strokeStyle = '#8B4513';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.stroke();
                ctx.restore();
            },
            isAlive: function() {
                return this.life > 0 && this.radius < this.maxRadius;
            }
        });
    }
    
    /**
     * Draw the barrel
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     */
    drawBarrel(ctx) {
        ctx.save();
        ctx.translate(this.barrelCenterX, this.barrelCenterY);
        
        // Draw barrel cylinder
        const gradient = ctx.createLinearGradient(0, -this.barrelLength/2, 0, this.barrelLength/2);
        gradient.addColorStop(0, '#654321');
        gradient.addColorStop(0.5, '#8B4513');
        gradient.addColorStop(1, '#654321');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(-this.barrelRadius, -this.barrelLength/2, this.barrelRadius * 2, this.barrelLength);
        
        // Draw barrel ends
        ctx.fillStyle = '#4A3018';
        ctx.beginPath();
        ctx.ellipse(0, -this.barrelLength/2, this.barrelRadius, 10, 0, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.beginPath();
        ctx.ellipse(0, this.barrelLength/2, this.barrelRadius, 10, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw pins
        ctx.save();
        ctx.rotate(this.barrelRotation);
        
        this.pinPositions.forEach(pin => {
            const x = Math.cos(pin.angle) * this.barrelRadius;
            const y = pin.height;
            
            // Pin
            ctx.fillStyle = '#FFD700';
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fill();
            
            // Pin connection line
            ctx.strokeStyle = '#FFD700';
            ctx.lineWidth = 1;
            ctx.setLineDash([2, 2]);
            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.lineTo(x + Math.cos(pin.angle) * 15, y);
            ctx.stroke();
            ctx.setLineDash([]);
        });
        
        ctx.restore();
        
        // Draw barrel supports
        ctx.fillStyle = '#4A3018';
        ctx.fillRect(-this.barrelRadius - 10, -5, 10, 10);
        ctx.fillRect(this.barrelRadius, -5, 10, 10);
        
        ctx.restore();
    }
    
    /**
     * Draw the drum
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     */
    drawDrum(ctx) {
        // Apply vibration effect
        const vibrationX = this.drumVibration * 0.2;
        const vibrationY = this.drumVibration * 0.1;
        
        ctx.save();
        ctx.translate(this.drumCenterX + vibrationX, this.drumCenterY + vibrationY);
        
        // Drum shell
        const shellGradient = ctx.createRadialGradient(0, 0, this.drumRadius * 0.7, 0, 0, this.drumRadius);
        shellGradient.addColorStop(0, '#A0522D');
        shellGradient.addColorStop(0.8, '#8B4513');
        shellGradient.addColorStop(1, '#654321');
        
        ctx.fillStyle = shellGradient;
        ctx.beginPath();
        ctx.arc(0, 0, this.drumRadius, 0, Math.PI * 2);
        ctx.fill();
        
        // Drum head with resonance effect
        const headRadius = this.drumRadius * (1 - this.drumHeadResonance * 0.05);
        const headGradient = ctx.createRadialGradient(0, 0, 0, 0, 0, headRadius);
        headGradient.addColorStop(0, '#F5DEB3');
        headGradient.addColorStop(0.7, '#DEB887');
        headGradient.addColorStop(1, '#D2691E');
        
        ctx.fillStyle = headGradient;
        ctx.beginPath();
        ctx.arc(0, 0, headRadius, 0, Math.PI * 2);
        ctx.fill();
        
        // Drum head rim
        ctx.strokeStyle = '#654321';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(0, 0, headRadius, 0, Math.PI * 2);
        ctx.stroke();
        
        // Drum tension ropes
        const ropeCount = 8;
        for (let i = 0; i < ropeCount; i++) {
            const angle = (i / ropeCount) * Math.PI * 2;
            const x1 = Math.cos(angle) * headRadius;
            const y1 = Math.sin(angle) * headRadius;
            const x2 = Math.cos(angle) * this.drumRadius;
            const y2 = Math.sin(angle) * this.drumRadius;
            
            ctx.strokeStyle = '#8B4513';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }
        
        ctx.restore();
    }
    
    /**
     * Draw beaters
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     */
    drawBeaters(ctx) {
        for (let i = 0; i < this.beaterCount; i++) {
            const beaterAngle = (i / this.beaterCount) * Math.PI * 2 - Math.PI / 2;
            const restX = this.drumCenterX + Math.cos(beaterAngle) * (this.drumRadius + 20);
            const restY = this.drumCenterY + Math.sin(beaterAngle) * (this.drumRadius + 20);
            
            // Calculate beater position
            let beaterX = restX;
            let beaterY = restY;
            
            const animation = this.beaterAnimations.get(i);
            if (animation) {
                const strikeDistance = this.beaterLength * animation.strength;
                beaterX = restX + Math.cos(beaterAngle) * (animation.position * strikeDistance);
                beaterY = restY + Math.sin(beaterAngle) * (animation.position * strikeDistance);
            }
            
            // Draw beater arm
            ctx.strokeStyle = '#8B4513';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(restX, restY);
            ctx.lineTo(beaterX, beaterY);
            ctx.stroke();
            
            // Draw beater head
            const beaterGradient = ctx.createRadialGradient(beaterX, beaterY, 0, beaterX, beaterY, 6);
            beaterGradient.addColorStop(0, '#D2691E');
            beaterGradient.addColorStop(1, '#8B4513');
            
            ctx.fillStyle = beaterGradient;
            ctx.beginPath();
            ctx.arc(beaterX, beaterY, 6, 0, Math.PI * 2);
            ctx.fill();
            
            // Beater head outline
            ctx.strokeStyle = '#654321';
            ctx.lineWidth = 1;
            ctx.stroke();
            
            // Highlight active beater
            if (this.activeBeaters.has(i)) {
                ctx.save();
                ctx.strokeStyle = '#FFD700';
                ctx.lineWidth = 2;
                ctx.setLineDash([2, 2]);
                ctx.beginPath();
                ctx.arc(beaterX, beaterY, 10, 0, Math.PI * 2);
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
        const beaterIndex = note.beaterIndex;
        if (beaterIndex !== undefined) {
            this.createDrumEffect(beaterIndex, note.strength || 1.0);
        }
    }
    
    /**
     * Draw background with mechanical elements
     */
    drawBackground() {
        super.drawBackground();
        
        // Draw mechanical base
        ctx.fillStyle = 'rgba(101, 67, 33, 0.3)';
        ctx.fillRect(this.barrelCenterX - 80, this.barrelCenterY + 60, 160, 20);
        
        // Draw gear decoration
        this.drawGear(ctx, this.barrelCenterX - 60, this.barrelCenterY + 40, 15, 8);
        this.drawGear(ctx, this.barrelCenterX + 60, this.barrelCenterY + 40, 15, 8);
    }
    
    /**
     * Draw a decorative gear
     * @param {CanvasRenderingContext2D} ctx - Canvas context
     * @param {number} x - Gear center X
     * @param {number} y - Gear center Y
     * @param {number} radius - Gear radius
     * @param {number} teeth - Number of teeth
     */
    drawGear(ctx, x, y, radius, teeth) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(this.animationTime * 0.001);
        
        ctx.fillStyle = 'rgba(139, 69, 19, 0.5)';
        ctx.beginPath();
        
        const toothHeight = radius * 0.3;
        const toothWidth = (Math.PI * 2) / (teeth * 2);
        
        for (let i = 0; i < teeth; i++) {
            const angle = (i / teeth) * Math.PI * 2;
            const nextAngle = ((i + 1) / teeth) * Math.PI * 2;
            
            // Tooth
            ctx.arc(0, 0, radius + toothHeight, angle - toothWidth/2, angle + toothWidth/2);
            ctx.arc(0, 0, radius, angle + toothWidth/2, nextAngle - toothWidth/2);
        }
        
        ctx.closePath();
        ctx.fill();
        
        // Center hole
        ctx.fillStyle = 'rgba(44, 24, 16, 0.5)';
        ctx.beginPath();
        ctx.arc(0, 0, radius * 0.3, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
    
    /**
     * Ease out quadratic function
     * @param {number} t - Input value (0-1)
     * @returns {number} Eased value
     */
    easeOutQuad(t) {
        return t * (2 - t);
    }
    
    /**
     * Ease in quadratic function
     * @param {number} t - Input value (0-1)
     * @returns {number} Eased value
     */
    easeInQuad(t) {
        return t * t;
    }
    
    /**
     * Reset drum to initial state
     */
    resetComponents() {
        super.resetComponents();
        
        this.barrelRotation = 0;
        this.activeBeaters.clear();
        this.beaterAnimations.clear();
        this.drumVibration = 0;
        this.drumHeadResonance = 0;
        
        // Reset pin triggers
        this.pinPositions.forEach(pin => {
            pin.triggered = false;
        });
    }
    
    /**
     * Switch to next rhythm pattern
     */
    switchPattern() {
        this.currentPattern = (this.currentPattern + 1) % this.rhythmPatterns.length;
        this.generatePinPositions();
    }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LeonardoEnsemble.Drum;
}