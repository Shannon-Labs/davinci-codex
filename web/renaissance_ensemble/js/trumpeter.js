/**
 * Leonardo's Mechanical Ensemble - Mechanical Trumpeter
 * Brass automaton with pneumatic control valves
 */

window.LeonardoEnsemble = window.LeonardoEnsemble || {};

LeonardoEnsemble.Trumpeter = class extends LeonardoEnsemble.InstrumentBase {
    constructor(canvas, options = {}) {
        super('trumpeter', 'Mechanical Trumpeter', canvas, options);
        
        this.valveStates = [false, false, false];
        this.bellVibration = 0;
        
        this.setupTrumpeter();
    }
    
    setupTrumpeter() {
        this.trumpetX = 100;
        this.trumpetY = 150;
    }
    
    setupComponents() {
        // Trumpet
        this.addComponent('trumpet', {
            update: (deltaTime) => {
                this.bellVibration *= 0.9;
            },
            draw: (ctx) => {
                this.drawTrumpet(ctx);
            }
        });
        
        // Valves
        this.addComponent('valves', {
            draw: (ctx) => {
                this.drawValves(ctx);
            }
        });
    }
    
    drawTrumpet(ctx) {
        ctx.save();
        ctx.translate(this.trumpetX, this.trumpetY);
        
        // Bell vibration
        const vib = Math.sin(this.animationTime * 0.1) * this.bellVibration;
        
        // Trumpet body
        ctx.strokeStyle = '#B8860B';
        ctx.lineWidth = 12;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(100, 0);
        ctx.stroke();
        
        // Bell
        const grad = ctx.createLinearGradient(100, -30, 150, 30);
        grad.addColorStop(0, '#FFD700');
        grad.addColorStop(0.5, '#FFA500');
        grad.addColorStop(1, '#B8860B');
        
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(100, 0);
        ctx.quadraticCurveTo(120, -40 + vib, 160, -50 + vib);
        ctx.lineTo(160, 50 - vib);
        ctx.quadraticCurveTo(120, 40 - vib, 100, 0);
        ctx.fill();
        ctx.stroke();
        
        ctx.restore();
    }
    
    drawValves(ctx) {
        for(let i=0; i<3; i++) {
            const x = this.trumpetX + 30 + i * 20;
            const y = this.trumpetY - 15;
            const h = this.valveStates[i] ? 10 : 25;
            
            ctx.fillStyle = '#8B4513';
            ctx.fillRect(x, y - h, 10, h);
            ctx.strokeRect(x, y - h, 10, h);
        }
    }
    
    onNotePlay(note) {
        this.bellVibration = 10;
        const v = Math.floor(LeonardoEnsemble.Utils.math.random(0, 3));
        this.valveStates[v] = true;
        setTimeout(() => this.valveStates[v] = false, 300);
    }
};
