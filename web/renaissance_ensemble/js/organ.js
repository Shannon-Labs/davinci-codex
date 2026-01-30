/**
 * Leonardo's Mechanical Ensemble - Mechanical Organ
 * Water-driven organ with automated bellows
 */

window.LeonardoEnsemble = window.LeonardoEnsemble || {};

LeonardoEnsemble.Organ = class extends LeonardoEnsemble.InstrumentBase {
    constructor(canvas, options = {}) {
        super('organ', 'Mechanical Organ', canvas, options);
        
        this.bellowsPressure = 0;
        this.pipeCount = 10;
        this.activePipes = new Set();
        
        this.setupOrgan();
    }
    
    setupOrgan() {
        this.pipeWidth = 20;
        this.pipeMaxHeight = 150;
    }
    
    setupComponents() {
        // Pipes
        this.addComponent('pipes', {
            update: (deltaTime) => {
                this.bellowsPressure = 0.5 + Math.sin(this.animationTime * 0.002) * 0.5;
            },
            draw: (ctx) => {
                this.drawPipes(ctx);
            }
        });
        
        // Bellows
        this.addComponent('bellows', {
            draw: (ctx) => {
                this.drawBellows(ctx);
            }
        });
    }
    
    drawPipes(ctx) {
        for(let i=0; i<this.pipeCount; i++) {
            const h = this.pipeMaxHeight * (0.5 + i/this.pipeCount * 0.5);
            const x = 40 + i * 25;
            const y = 200 - h;
            
            // Pipe body
            const grad = ctx.createLinearGradient(x, y, x + this.pipeWidth, y);
            grad.addColorStop(0, '#B8860B');
            grad.addColorStop(0.5, '#FFD700');
            grad.addColorStop(1, '#B8860B');
            
            ctx.fillStyle = grad;
            ctx.fillRect(x, y, this.pipeWidth, h);
            
            // Active pipe effect
            if (this.activePipes.has(i)) {
                ctx.save();
                ctx.globalAlpha = 0.4;
                ctx.fillStyle = '#FFFFFF';
                ctx.beginPath();
                ctx.arc(x + this.pipeWidth/2, y - 10, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }
    }
    
    drawBellows(ctx) {
        ctx.save();
        ctx.translate(150, 240);
        const scale = 1 - this.bellowsPressure * 0.3;
        ctx.scale(1, scale);
        
        ctx.fillStyle = '#8B4513';
        ctx.beginPath();
        ctx.moveTo(-60, 0);
        ctx.lineTo(0, -40);
        ctx.lineTo(60, 0);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        ctx.restore();
    }
    
    onNotePlay(note) {
        const pipeIndex = Math.floor(LeonardoEnsemble.Utils.math.random(0, this.pipeCount));
        this.activePipes.add(pipeIndex);
        setTimeout(() => this.activePipes.delete(pipeIndex), 500);
    }
};
