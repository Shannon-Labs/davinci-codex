/**
 * Leonardo's Mechanical Ensemble - Viola Organista
 * Continuous bowed string instrument using friction wheels
 */

window.LeonardoEnsemble = window.LeonardoEnsemble || {};

LeonardoEnsemble.Viola = class extends LeonardoEnsemble.InstrumentBase {
    constructor(canvas, options = {}) {
        super('viola', 'Viola Organista', canvas, options);
        
        this.wheelRotation = 0;
        this.wheelSpeed = 1.2;
        this.keyCount = 12;
        this.activeKeys = new Map();
        
        this.setupViola();
    }
    
    setupViola() {
        this.wheelCenterX = 150;
        this.wheelCenterY = 180;
        this.wheelRadius = 80;
    }
    
    setupComponents() {
        // Friction wheel
        this.addComponent('wheel', {
            update: (deltaTime) => {
                if (this.isPlaying) {
                    this.wheelRotation += this.wheelSpeed * deltaTime / 1000;
                }
            },
            draw: (ctx) => {
                this.drawWheel(ctx);
            }
        });
        
        // Keys and strings
        this.addComponent('mechanism', {
            update: (deltaTime) => {
                this.activeKeys.forEach((key, id) => {
                    key.time += deltaTime;
                    if (key.time > key.duration) {
                        this.activeKeys.delete(id);
                    }
                });
            },
            draw: (ctx) => {
                this.drawMechanism(ctx);
            }
        });
    }
    
    drawWheel(ctx) {
        ctx.save();
        ctx.translate(this.wheelCenterX, this.wheelCenterY);
        ctx.rotate(this.wheelRotation);
        
        // Main wheel
        const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, this.wheelRadius);
        grad.addColorStop(0, '#4A3018');
        grad.addColorStop(0.8, '#654321');
        grad.addColorStop(1, '#2C1810');
        
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(0, 0, this.wheelRadius, 0, Math.PI * 2);
        ctx.fill();
        
        // Spokes
        ctx.strokeStyle = '#8B4513';
        ctx.lineWidth = 4;
        for(let i=0; i<8; i++) {
            ctx.rotate(Math.PI / 4);
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(this.wheelRadius - 5, 0);
            ctx.stroke();
        }
        
        ctx.restore();
    }
    
    drawMechanism(ctx) {
        // Draw strings
        ctx.strokeStyle = 'rgba(44, 24, 16, 0.4)';
        ctx.lineWidth = 1;
        for(let i=0; i<this.keyCount; i++) {
            const x = 50 + i * 18;
            ctx.beginPath();
            ctx.moveTo(x, 50);
            ctx.lineTo(x, 250);
            ctx.stroke();
            
            // Draw active string vibration
            if (this.activeKeys.has(i)) {
                const vib = Math.sin(this.animationTime * 0.05) * 2;
                ctx.strokeStyle = '#C9A227';
                ctx.beginPath();
                ctx.moveTo(x + vib, 50);
                ctx.lineTo(x - vib, 250);
                ctx.stroke();
            }
        }
    }
    
    onNotePlay(note) {
        const keyIndex = Math.floor(LeonardoEnsemble.Utils.math.random(0, this.keyCount));
        this.activeKeys.set(keyIndex, {
            time: 0,
            duration: 1000
        });
    }
};
