/**
 * Leonardo's Mechanical Ensemble - Programmable Flute
 * Cam-controlled flute with mechanical fingering
 */

window.LeonardoEnsemble = window.LeonardoEnsemble || {};

LeonardoEnsemble.Flute = class extends LeonardoEnsemble.InstrumentBase {
    constructor(canvas, options = {}) {
        super('flute', 'Programmable Flute', canvas, options);
        
        this.camRotation = 0;
        this.fingerCount = 6;
        this.activeFingers = new Set();
        
        this.setupFlute();
    }
    
    setupFlute() {
        this.fluteX = 50;
        this.fluteY = 150;
        this.fluteWidth = 200;
        this.fluteHeight = 30;
    }
    
    setupComponents() {
        // Flute body
        this.addComponent('flute', {
            update: (deltaTime) => {
                if (this.isPlaying) {
                    this.camRotation += 0.8 * deltaTime / 1000;
                }
            },
            draw: (ctx) => {
                this.drawFlute(ctx);
            }
        });
        
        // Cams
        this.addComponent('cams', {
            draw: (ctx) => {
                this.drawCams(ctx);
            }
        });
    }
    
    drawFlute(ctx) {
        // Main flute
        const grad = ctx.createLinearGradient(this.fluteX, this.fluteY, this.fluteX, this.fluteY + this.fluteHeight);
        grad.addColorStop(0, '#5F7A6A');
        grad.addColorStop(0.5, '#87A96B');
        grad.addColorStop(1, '#5F7A6A');
        
        ctx.fillStyle = grad;
        ctx.fillRect(this.fluteX, this.fluteY, this.fluteWidth, this.fluteHeight);
        
        // Holes
        for(let i=0; i<this.fingerCount; i++) {
            const x = this.fluteX + 40 + i * 25;
            const y = this.fluteY + this.fluteHeight/2;
            
            ctx.fillStyle = this.activeFingers.has(i) ? '#2C1810' : '#4A3018';
            ctx.beginPath();
            ctx.arc(x, y, 6, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    drawCams(ctx) {
        ctx.save();
        ctx.translate(150, 220);
        ctx.rotate(this.camRotation);
        
        ctx.fillStyle = '#8B7355';
        ctx.beginPath();
        for(let i=0; i<8; i++) {
            const r = 20 + Math.sin(i + this.animationTime * 0.01) * 10;
            const angle = (i/8) * Math.PI * 2;
            ctx.lineTo(Math.cos(angle) * r, Math.sin(angle) * r);
        }
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        ctx.restore();
    }
    
    onNotePlay(note) {
        const fingerIndex = Math.floor(LeonardoEnsemble.Utils.math.random(0, this.fingerCount));
        this.activeFingers.add(fingerIndex);
        setTimeout(() => this.activeFingers.delete(fingerIndex), 400);
    }
};
