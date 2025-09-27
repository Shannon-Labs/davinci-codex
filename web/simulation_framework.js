/**
 * Leonardo Challenge - Interactive Simulation Framework
 * Physics-accurate simulations of da Vinci's machines for the global competition platform
 */

class LeonardoSimulation {
    constructor(canvasId, inventionType) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.inventionType = inventionType;
        this.isRunning = false;
        this.animationId = null;
        
        // Physics constants
        this.gravity = 9.81; // m/s²
        this.airDensity = 1.225; // kg/m³
        this.timeStep = 0.016; // 60 FPS
        
        this.setupCanvas();
        this.initializeSimulation();
    }
    
    setupCanvas() {
        this.canvas.width = 800;
        this.canvas.height = 600;
        this.canvas.style.border = '2px solid #8B0000';
        this.canvas.style.borderRadius = '10px';
        this.canvas.style.background = 'linear-gradient(to bottom, #87CEEB, #E0F6FF)';
    }
    
    initializeSimulation() {
        switch(this.inventionType) {
            case 'ornithopter':
                this.initOrnithopter();
                break;
            case 'parachute':
                this.initParachute();
                break;
            case 'cart':
                this.initCart();
                break;
            case 'crossbow':
                this.initCrossbow();
                break;
            default:
                console.error('Unknown invention type:', this.inventionType);
        }
    }
    
    // ORNITHOPTER SIMULATION
    initOrnithopter() {
        this.ornithopter = {
            x: 100,
            y: 300,
            vx: 0,
            vy: 0,
            angle: 0,
            wingAngle: 0,
            wingSpan: 12, // meters (visual scale adjusted)
            mass: 80, // kg (pilot + machine)
            flapRate: 120, // beats per minute
            wingArea: 25, // m²
            lift: 0,
            drag: 0,
            isFlapping: false
        };
        
        this.ornithopterControls = {
            flapRate: 120,
            wingSpan: 12,
            pilotWeight: 75
        };
    }
    
    updateOrnithopter() {
        const o = this.ornithopter;
        
        if (o.isFlapping) {
            // Wing flapping physics
            const flapFreq = o.flapRate / 60; // Hz
            o.wingAngle = Math.sin(Date.now() * 0.001 * flapFreq * 2 * Math.PI) * 45;
            
            // Calculate lift from wing motion
            const wingSpeed = Math.abs(Math.cos(Date.now() * 0.001 * flapFreq * 2 * Math.PI)) * o.flapRate / 60;
            const reynoldsNumber = wingSpeed * o.wingSpan / 1.5e-5; // air kinematic viscosity
            const liftCoeff = Math.min(1.2, 0.8 + reynoldsNumber / 100000);
            
            o.lift = 0.5 * this.airDensity * o.wingArea * wingSpeed * wingSpeed * liftCoeff;
            o.drag = 0.5 * this.airDensity * o.wingArea * wingSpeed * wingSpeed * 0.15;
        } else {
            o.lift = 0;
            o.drag = 0.05 * this.airDensity * o.wingArea * (o.vx * o.vx + o.vy * o.vy);
        }
        
        // Forces
        const weight = o.mass * this.gravity;
        const netForceY = o.lift - weight;
        const netForceX = -o.drag * Math.sign(o.vx);
        
        // Update velocity and position
        o.vx += netForceX / o.mass * this.timeStep;
        o.vy += netForceY / o.mass * this.timeStep;
        
        o.x += o.vx * this.timeStep * 10; // Scale for display
        o.y -= o.vy * this.timeStep * 10; // Inverted Y for canvas
        
        // Boundary checks
        if (o.y > this.canvas.height - 50) {
            o.y = this.canvas.height - 50;
            o.vy = Math.max(0, o.vy); // Stop downward motion at ground
        }
        
        if (o.x > this.canvas.width) {
            o.x = -100; // Reset position for continuous demonstration
        }
    }
    
    drawOrnithopter() {
        const o = this.ornithopter;
        this.ctx.save();
        
        // Move to ornithopter position
        this.ctx.translate(o.x, o.y);
        this.ctx.rotate(o.angle * Math.PI / 180);
        
        // Draw body
        this.ctx.fillStyle = '#8B4513';
        this.ctx.fillRect(-15, -5, 30, 10);
        
        // Draw wings
        this.ctx.save();
        this.ctx.rotate(o.wingAngle * Math.PI / 180);
        this.ctx.strokeStyle = '#654321';
        this.ctx.lineWidth = 3;
        
        // Left wing
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.quadraticCurveTo(-40, -20, -60, -10);
        this.ctx.stroke();
        
        // Right wing
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.quadraticCurveTo(40, -20, 60, -10);
        this.ctx.stroke();
        
        this.ctx.restore();
        
        // Draw pilot
        this.ctx.fillStyle = '#FF6B35';
        this.ctx.beginPath();
        this.ctx.arc(0, 0, 8, 0, Math.PI * 2);
        this.ctx.fill();
        
        this.ctx.restore();
    }
    
    // PARACHUTE SIMULATION
    initParachute() {
        this.parachute = {
            x: 400,
            y: 50,
            vx: 0,
            vy: 0,
            deployed: false,
            canopyArea: 25, // m²
            mass: 80, // kg
            dragCoeff: 1.3,
            deployHeight: 200
        };
    }
    
    updateParachute() {
        const p = this.parachute;
        
        // Auto-deploy parachute at certain height
        if (!p.deployed && p.y > p.deployHeight) {
            p.deployed = true;
        }
        
        // Calculate drag force
        const dragArea = p.deployed ? p.canopyArea : 0.1; // tiny area when closed
        const dragCoeff = p.deployed ? p.dragCoeff : 0.3;
        const drag = 0.5 * this.airDensity * dragArea * p.vy * p.vy * dragCoeff;
        
        // Forces
        const weight = p.mass * this.gravity;
        const netForce = weight - drag;
        
        // Update physics
        p.vy += netForce / p.mass * this.timeStep;
        p.y += p.vy * this.timeStep * 10;
        
        // Ground collision
        if (p.y > this.canvas.height - 30) {
            p.y = this.canvas.height - 30;
            p.vy = 0;
        }
    }
    
    drawParachute() {
        const p = this.parachute;
        
        if (p.deployed) {
            // Draw parachute canopy
            this.ctx.fillStyle = 'rgba(255, 0, 0, 0.7)';
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y - 30, 40, 0, Math.PI, false);
            this.ctx.fill();
            
            // Draw cords
            this.ctx.strokeStyle = '#333';
            this.ctx.lineWidth = 1;
            for (let i = 0; i < 8; i++) {
                const angle = (i / 8) * Math.PI;
                const cordX = p.x + Math.cos(angle) * 40;
                const cordY = p.y - 30;
                this.ctx.beginPath();
                this.ctx.moveTo(cordX, cordY);
                this.ctx.lineTo(p.x, p.y);
                this.ctx.stroke();
            }
        }
        
        // Draw person
        this.ctx.fillStyle = '#FF6B35';
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, 8, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    // CART SIMULATION
    initCart() {
        this.cart = {
            x: 50,
            y: this.canvas.height - 80,
            vx: 0,
            angle: 0,
            springEnergy: 1000, // Joules
            mass: 150, // kg
            friction: 0.1,
            wheelRadius: 20,
            gearRatio: 4
        };
    }
    
    updateCart() {
        const c = this.cart;
        
        // Convert spring energy to kinetic energy
        if (c.springEnergy > 0) {
            const powerOutput = Math.min(100, c.springEnergy / 10); // Watts
            const force = powerOutput / Math.max(0.1, c.vx);
            const friction = c.friction * c.mass * this.gravity;
            
            const netForce = force - friction - 0.5 * this.airDensity * 2 * c.vx * c.vx * 0.3; // Air resistance
            
            c.vx += netForce / c.mass * this.timeStep;
            c.springEnergy -= powerOutput * this.timeStep;
        } else {
            // Only friction acts
            const friction = c.friction * c.mass * this.gravity * Math.sign(c.vx);
            c.vx -= friction / c.mass * this.timeStep;
        }
        
        // Update position
        c.x += c.vx * this.timeStep * 10;
        
        // Wheel rotation
        c.angle += c.vx / c.wheelRadius * this.timeStep * 10;
        
        // Reset if off screen
        if (c.x > this.canvas.width + 50) {
            c.x = -50;
            c.vx = 0;
            c.springEnergy = 1000; // Reset spring
        }
    }
    
    drawCart() {
        const c = this.cart;
        
        this.ctx.save();
        this.ctx.translate(c.x, c.y);
        
        // Draw cart body
        this.ctx.fillStyle = '#8B4513';
        this.ctx.fillRect(-25, -15, 50, 20);
        
        // Draw wheels
        this.ctx.strokeStyle = '#654321';
        this.ctx.lineWidth = 4;
        
        // Front wheel
        this.ctx.save();
        this.ctx.translate(15, 10);
        this.ctx.rotate(c.angle);
        this.ctx.beginPath();
        this.ctx.arc(0, 0, c.wheelRadius, 0, Math.PI * 2);
        this.ctx.stroke();
        // Spokes
        for (let i = 0; i < 6; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, 0);
            const spokeAngle = (i / 6) * Math.PI * 2;
            this.ctx.lineTo(Math.cos(spokeAngle) * 15, Math.sin(spokeAngle) * 15);
            this.ctx.stroke();
        }
        this.ctx.restore();
        
        // Back wheel
        this.ctx.save();
        this.ctx.translate(-15, 10);
        this.ctx.rotate(c.angle);
        this.ctx.beginPath();
        this.ctx.arc(0, 0, c.wheelRadius, 0, Math.PI * 2);
        this.ctx.stroke();
        this.ctx.restore();
        
        // Draw spring mechanism indicator
        const springPercent = c.springEnergy / 1000;
        this.ctx.fillStyle = `hsl(${springPercent * 120}, 80%, 50%)`;
        this.ctx.fillRect(-20, -25, 40 * springPercent, 5);
        
        this.ctx.restore();
    }
    
    // MAIN SIMULATION LOOP
    animate() {
        if (!this.isRunning) return;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw background elements
        this.drawBackground();
        
        // Update and draw based on simulation type
        switch(this.inventionType) {
            case 'ornithopter':
                this.updateOrnithopter();
                this.drawOrnithopter();
                this.drawOrnithopterUI();
                break;
            case 'parachute':
                this.updateParachute();
                this.drawParachute();
                this.drawParachuteUI();
                break;
            case 'cart':
                this.updateCart();
                this.drawCart();
                this.drawCartUI();
                break;
        }
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    drawBackground() {
        // Draw ground
        this.ctx.fillStyle = '#228B22';
        this.ctx.fillRect(0, this.canvas.height - 20, this.canvas.width, 20);
        
        // Draw clouds
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        for (let i = 0; i < 3; i++) {
            const x = (i * 250) + 100;
            const y = 80 + Math.sin(Date.now() * 0.001 + i) * 10;
            this.drawCloud(x, y);
        }
    }
    
    drawCloud(x, y) {
        this.ctx.beginPath();
        this.ctx.arc(x, y, 20, 0, Math.PI * 2);
        this.ctx.arc(x + 15, y, 25, 0, Math.PI * 2);
        this.ctx.arc(x + 30, y, 20, 0, Math.PI * 2);
        this.ctx.arc(x + 15, y - 15, 15, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    drawOrnithopterUI() {
        const o = this.ornithopter;
        
        // Flight data display
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(10, 10, 200, 120);
        
        this.ctx.fillStyle = 'white';
        this.ctx.font = '14px Arial';
        this.ctx.fillText(`Altitude: ${Math.max(0, (this.canvas.height - o.y) / 10).toFixed(1)}m`, 20, 30);
        this.ctx.fillText(`Speed: ${Math.sqrt(o.vx*o.vx + o.vy*o.vy).toFixed(1)}m/s`, 20, 50);
        this.ctx.fillText(`Lift: ${o.lift.toFixed(0)}N`, 20, 70);
        this.ctx.fillText(`Wing Rate: ${o.flapRate} bpm`, 20, 90);
        this.ctx.fillText(`Status: ${o.isFlapping ? 'Flying' : 'Gliding'}`, 20, 110);
    }
    
    drawParachuteUI() {
        const p = this.parachute;
        
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(10, 10, 200, 100);
        
        this.ctx.fillStyle = 'white';
        this.ctx.font = '14px Arial';
        this.ctx.fillText(`Altitude: ${Math.max(0, (this.canvas.height - p.y) / 10).toFixed(1)}m`, 20, 30);
        this.ctx.fillText(`Descent Rate: ${p.vy.toFixed(1)}m/s`, 20, 50);
        this.ctx.fillText(`Status: ${p.deployed ? 'Deployed' : 'Free Fall'}`, 20, 70);
        this.ctx.fillText(`Terminal V: ${Math.sqrt(2 * p.mass * this.gravity / (this.airDensity * p.canopyArea * p.dragCoeff)).toFixed(1)}m/s`, 20, 90);
    }
    
    drawCartUI() {
        const c = this.cart;
        
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(10, 10, 200, 100);
        
        this.ctx.fillStyle = 'white';
        this.ctx.font = '14px Arial';
        this.ctx.fillText(`Speed: ${c.vx.toFixed(1)}m/s`, 20, 30);
        this.ctx.fillText(`Spring Energy: ${c.springEnergy.toFixed(0)}J`, 20, 50);
        this.ctx.fillText(`Distance: ${(c.x / 10).toFixed(1)}m`, 20, 70);
        this.ctx.fillText(`Efficiency: ${((1000 - c.springEnergy) / 1000 * 100).toFixed(0)}%`, 20, 90);
    }
    
    // Control methods
    start() {
        this.isRunning = true;
        if (this.inventionType === 'ornithopter') {
            this.ornithopter.isFlapping = true;
        }
        this.animate();
    }
    
    stop() {
        this.isRunning = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.inventionType === 'ornithopter') {
            this.ornithopter.isFlapping = false;
        }
    }
    
    reset() {
        this.stop();
        this.initializeSimulation();
        this.animate();
    }
    
    updateParameter(param, value) {
        switch(this.inventionType) {
            case 'ornithopter':
                if (param === 'flapRate') this.ornithopter.flapRate = value;
                if (param === 'wingSpan') this.ornithopter.wingSpan = value;
                if (param === 'mass') this.ornithopter.mass = value;
                break;
            case 'parachute':
                if (param === 'canopyArea') this.parachute.canopyArea = value;
                if (param === 'mass') this.parachute.mass = value;
                break;
            case 'cart':
                if (param === 'springEnergy') this.cart.springEnergy = value;
                if (param === 'mass') this.cart.mass = value;
                break;
        }
    }
}

// Competition Analytics and Scoring System
class CompetitionScorer {
    constructor() {
        this.metrics = {
            historicalAccuracy: 0,
            engineeringInnovation: 0,
            performanceEfficiency: 0,
            safetyCompliance: 0,
            buildQuality: 0
        };
    }
    
    calculateScore(submissionData) {
        let totalScore = 0;
        
        // Historical Accuracy (25%)
        const accuracyScore = this.evaluateHistoricalAccuracy(submissionData);
        totalScore += accuracyScore * 0.25;
        
        // Engineering Innovation (25%)
        const innovationScore = this.evaluateInnovation(submissionData);
        totalScore += innovationScore * 0.25;
        
        // Performance (25%)
        const performanceScore = this.evaluatePerformance(submissionData);
        totalScore += performanceScore * 0.25;
        
        // Safety & Build Quality (25%)
        const qualityScore = this.evaluateQuality(submissionData);
        totalScore += qualityScore * 0.25;
        
        return {
            total: Math.round(totalScore),
            breakdown: {
                accuracy: accuracyScore,
                innovation: innovationScore,
                performance: performanceScore,
                quality: qualityScore
            }
        };
    }
    
    evaluateHistoricalAccuracy(data) {
        // Check adherence to Leonardo's original designs
        let score = 100;
        
        // Deduct points for modern materials not available in 1500s
        if (data.materials.includes('carbon_fiber')) score -= 20;
        if (data.materials.includes('aluminum')) score -= 10;
        
        // Award points for period-appropriate techniques
        if (data.construction.includes('mortise_and_tenon')) score += 10;
        if (data.construction.includes('rope_and_pulley')) score += 5;
        
        return Math.max(0, Math.min(100, score));
    }
    
    evaluateInnovation(data) {
        // Assess creative problem-solving and modern insights
        let score = 60; // Base score
        
        // Award points for novel solutions
        score += data.innovations.length * 10;
        
        // Check for biomimetic insights
        if (data.inspirations.includes('biomimetic')) score += 15;
        
        return Math.max(0, Math.min(100, score));
    }
    
    evaluatePerformance(data) {
        // Compare actual performance to theoretical maximums
        const efficiency = data.actualPerformance / data.theoreticalMax;
        return Math.round(efficiency * 100);
    }
    
    evaluateQuality(data) {
        let score = 0;
        
        // Safety compliance
        score += data.safetyTests.passed ? 50 : 0;
        
        // Build quality
        score += data.buildQuality * 0.5; // Assuming 0-100 scale
        
        return Math.max(0, Math.min(100, score));
    }
}

// Export for use in web platform
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { LeonardoSimulation, CompetitionScorer };
}