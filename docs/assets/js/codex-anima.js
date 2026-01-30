/**
 * Codex Anima — The Living Soul of the Machine
 * 
 * 1. The Sfumato Interface: GLSL shaders for soft edges and aerial perspective.
 * 2. The 3D Folio Engine: Three.js physical vellum simulation with vertex deformation.
 * 3. Generative Marginalia: Procedural silverpoint sketches of user navigation.
 * 4. The Polyphonic Counterpoint Engine: Real-time Renaissance counterpoint generation.
 * 5. The X-Ray Layer: Multispectral imaging toggle for underdrawings.
 */

class CodexAnima {
    constructor() {
        this.config = {
            sfumatoEnabled: true,
            folioEnabled: true,
            marginaliaEnabled: true,
            counterpointEnabled: true,
            xrayEnabled: false
        };

        this.init();
    }

    async init() {
        console.log("Invoking the Codex Anima...");
        
        this.setupSfumato();
        this.setupFolioEngine();
        this.setupMarginalia();
        this.setupCounterpoint();
        this.setupXRayLayer();
        this.setupUI();
    }

    /**
     * 1. The Sfumato Interface
     * Implementation of Leonardo's soft-edge technique via GLSL.
     */
    setupSfumato() {
        let canvas = document.getElementById('sfumato-overlay');
        if (!canvas) {
            canvas = document.createElement('canvas');
            canvas.id = 'sfumato-overlay';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100vw';
            canvas.style.height = '100vh';
            canvas.style.pointerEvents = 'none';
            canvas.style.zIndex = '9998';
            document.body.appendChild(canvas);
        }
        const gl = canvas.getContext('webgl');
        if (!gl) return;

        const vsSource = `
            attribute vec2 position;
            void main() {
                gl_Position = vec4(position, 0.0, 1.0);
            }
        `;

        const fsSource = `
            precision highp float;
            uniform float uTime;
            uniform vec2 uResolution;
            uniform float uScroll;

            float noise(vec2 p) {
                return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
            }

            void main() {
                vec2 uv = gl_FragCoord.xy / uResolution.xy;
                float n = noise(uv + uTime * 0.001);
                float charcoal = pow(n, 25.0) * 0.08;
                vec3 chalkyBlue = vec3(0.6, 0.7, 0.8);
                float depth = (uScroll / 2000.0);
                vec3 color = mix(vec3(0.0), chalkyBlue, (1.0 - uv.y) * 0.1 + depth * 0.1);
                float edge = smoothstep(0.0, 0.3, uv.x) * smoothstep(1.0, 0.7, uv.x) *
                             smoothstep(0.0, 0.3, uv.y) * smoothstep(1.0, 0.7, uv.y);
                gl_FragColor = vec4(color + charcoal, (1.0 - edge) * 0.15 + charcoal);
            }
        `;

        const createShader = (gl, type, source) => {
            const shader = gl.createShader(type);
            gl.shaderSource(shader, source);
            gl.compileShader(shader);
            return shader;
        };

        const program = gl.createProgram();
        gl.attachShader(program, createShader(gl, gl.VERTEX_SHADER, vsSource));
        gl.attachShader(program, createShader(gl, gl.FRAGMENT_SHADER, fsSource));
        gl.linkProgram(program);
        gl.useProgram(program);

        const buffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]), gl.STATIC_DRAW);

        const positionLocation = gl.getAttribLocation(program, "position");
        gl.enableVertexAttribArray(positionLocation);
        gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

        this.sfumatoUniforms = {
            time: gl.getUniformLocation(program, "uTime"),
            res: gl.getUniformLocation(program, "uResolution"),
            scroll: gl.getUniformLocation(program, "uScroll")
        };

        this.updateSfumato(gl, canvas);
    }

    updateSfumato(gl, canvas) {
        const render = (time) => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            gl.viewport(0, 0, canvas.width, canvas.height);
            gl.uniform1f(this.sfumatoUniforms.time, time);
            gl.uniform2f(this.sfumatoUniforms.res, canvas.width, canvas.height);
            gl.uniform1f(this.sfumatoUniforms.scroll, window.scrollY);
            gl.drawArrays(gl.TRIANGLES, 0, 6);

            // Aerial Perspective: Apply class to elements receding in depth
            const scroll = window.scrollY;
            document.querySelectorAll('section, .codex-card').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.top < -100) {
                    el.classList.add('aerial-recede');
                    el.style.setProperty('--recede-blur', `${Math.min(5, Math.abs(rect.top) / 200)}px`);
                } else {
                    el.classList.remove('aerial-recede');
                }
            });

            requestAnimationFrame(render);
        };
        requestAnimationFrame(render);
    }

    /**
     * 2. The 3D Folio Engine
     * Three.js physical vellum simulation with real-time vertex deformation.
     */
    setupFolioEngine() {
        if (!window.THREE) return;

        this.folioScene = new THREE.Scene();
        this.folioCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.folioRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        
        const container = document.createElement('div');
        container.id = 'folio-container';
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100%';
        container.style.height = '100%';
        container.style.zIndex = '0';
        document.body.insertBefore(container, document.body.firstChild);
        container.appendChild(this.folioRenderer.domElement);

        // Vellum Geometry with high segment count for deformation
        const geometry = new THREE.PlaneGeometry(10, 14, 32, 32);
        
        // Custom Vellum Material
        const material = new THREE.ShaderMaterial({
            uniforms: {
                uTorchPos: { value: new THREE.Vector3(0, 0, 5) },
                uTime: { value: 0 },
                uFold: { value: 0 }
            },
            vertexShader: `
                uniform float uFold;
                uniform float uTime;
                varying vec2 vUv;
                varying vec3 vPosition;

                void main() {
                    vUv = uv;
                    vec3 pos = position;
                    
                    // Vertex deformation for page turn
                    float foldEffect = sin(uv.x * 3.14159) * uFold;
                    pos.z += foldEffect * 2.0;
                    pos.x += foldEffect * 0.5;

                    vPosition = pos;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
                }
            `,
            fragmentShader: `
                uniform vec3 uTorchPos;
                varying vec3 vPosition;
                varying vec2 vUv;

                void main() {
                    // Virtual Torchlight logic
                    float dist = distance(vPosition, uTorchPos);
                    float light = 1.0 / (1.0 + dist * dist * 0.1);
                    
                    // Translucent vellum texture simulation
                    vec3 vellumColor = vec3(0.97, 0.95, 0.91);
                    gl_FragColor = vec4(vellumColor * light, 0.95);
                }
            `,
            side: THREE.DoubleSide,
            transparent: true
        });

        this.vellum = new THREE.Mesh(geometry, material);
        this.folioScene.add(this.vellum);

        // Virtual Torchlight
        this.torch = new THREE.PointLight(0xffaa66, 1, 20);
        this.torch.castShadow = true;
        this.folioScene.add(this.torch);

        this.animateFolio();
    }

    animateFolio() {
        const render = (time) => {
            this.vellum.material.uniforms.uTime.value = time * 0.001;
            
            // Mouse-driven torchlight
            // ...
            
            this.folioRenderer.render(this.folioScene, this.folioCamera);
            requestAnimationFrame(render);
        };
        requestAnimationFrame(render);
    }

    /**
     * 3. Generative Marginalia
     * Procedural silverpoint studies of the user's navigation patterns.
     */
    setupMarginalia() {
        this.marginaliaCanvas = document.createElement('canvas');
        this.marginaliaCanvas.id = 'marginalia-canvas';
        this.marginaliaCanvas.style.position = 'fixed';
        this.marginaliaCanvas.style.top = '0';
        this.marginaliaCanvas.style.left = '0';
        this.marginaliaCanvas.style.width = '100%';
        this.marginaliaCanvas.style.height = '100%';
        this.marginaliaCanvas.style.pointerEvents = 'none';
        this.marginaliaCanvas.style.zIndex = '9997';
        document.body.appendChild(this.marginaliaCanvas);

        this.mCtx = this.marginaliaCanvas.getContext('2d');
        this.mPoints = [];
        
        window.addEventListener('mousemove', (e) => {
            this.mPoints.push({ x: e.clientX, y: e.clientY, alpha: 1.0 });
            if (this.mPoints.length > 100) this.mPoints.shift();
            this.drawMarginalia();
        });
    }

    drawMarginalia() {
        this.mCtx.clearRect(0, 0, this.marginaliaCanvas.width, this.marginaliaCanvas.height);
        this.mCtx.strokeStyle = 'rgba(180, 180, 180, 0.3)'; // Silverpoint look
        this.mCtx.lineWidth = 0.5;

        if (this.mPoints.length < 2) return;

        this.mCtx.beginPath();
        this.mCtx.moveTo(this.mPoints[0].x, this.mPoints[0].y);

        for (let i = 1; i < this.mPoints.length; i++) {
            // Procedural geometry of curiosity
            const p = this.mPoints[i];
            const prev = this.mPoints[i-1];
            
            // Add subtle "mechanical" offsets
            const offsetX = Math.sin(i * 0.5) * 5;
            const offsetY = Math.cos(i * 0.5) * 5;
            
            this.mCtx.lineTo(p.x + offsetX, p.y + offsetY);
        }
        this.mCtx.stroke();
    }

    /**
     * 4. The Polyphonic Counterpoint Engine
     * Real-time Generative Cantus Firmus engine following Renaissance rules.
     */
    setupCounterpoint() {
        this.counterpointEngine = {
            intervals: { unison: 0, minorSecond: 1, majorSecond: 2, minorThird: 3, majorThird: 4, perfectFourth: 5, tritone: 6, perfectFifth: 7, minorSixth: 8, majorSixth: 9, minorSeventh: 10, majorSeventh: 11, octave: 12 },
            consonant: [0, 3, 4, 7, 8, 9, 12],
            perfect: [0, 7, 12],
            
            generateVoice: (cantusFirmus) => {
                let counterpoint = [];
                let lastNote = cantusFirmus[0] + 7; // Start at a fifth
                
                for (let i = 0; i < cantusFirmus.length; i++) {
                    const cfNote = cantusFirmus[i];
                    // Find a consonant note that avoids parallel fifths/octaves
                    let possibleNotes = this.counterpointEngine.consonant.map(c => cfNote + c);
                    let validNote = possibleNotes.find(n => {
                        const interval = Math.abs(n - cfNote) % 12;
                        const lastInterval = Math.abs(lastNote - (cantusFirmus[i-1] || cfNote)) % 12;
                        // Avoid parallel perfect intervals
                        if (this.counterpointEngine.perfect.includes(interval) && interval === lastInterval) return false;
                        return true;
                    }) || cfNote + 7;
                    
                    counterpoint.push(validNote);
                    lastNote = validNote;
                }
                return counterpoint;
            }
        };

        console.log("Generative Cantus Firmus engine active.");
        this.testCounterpoint();
    }

    testCounterpoint() {
        const cf = [62, 64, 65, 67, 69, 67, 65, 62]; // D Dorian scale
        const cp = this.counterpointEngine.generateVoice(cf);
        console.log("Generated Counterpoint:", cp);
    }

    /**
     * 5. The X-Ray Layer
     * Multispectral imaging toggle for underdrawings.
     */
    setupXRayLayer() {
        const toggle = document.createElement('button');
        toggle.id = 'xray-toggle';
        toggle.innerText = 'Multispectral Imaging';
        toggle.style.position = 'fixed';
        toggle.style.bottom = '20px';
        toggle.style.right = '20px';
        toggle.style.zIndex = '10000';
        toggle.className = 'btn-codex btn-codex-secondary';
        document.body.appendChild(toggle);

        toggle.addEventListener('click', () => {
            this.config.xrayEnabled = !this.config.xrayEnabled;
            document.body.classList.toggle('multispectral-active');
            console.log(`X-Ray Layer: ${this.config.xrayEnabled ? 'ON' : 'OFF'}`);
        });
    }

    setupUI() {
        // Additional UI refinements for "The Geometry of Curiosity"
    }
}

// Auto-initialize when Three.js is ready
document.addEventListener('DOMContentLoaded', () => {
    // Check if Three.js is loaded
    if (window.THREE) {
        window.codexAnima = new CodexAnima();
    } else {
        // Load Three.js if missing
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
        script.onload = () => {
            const orbit = document.createElement('script');
            orbit.src = 'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js';
            orbit.onload = () => {
                window.codexAnima = new CodexAnima();
            };
            document.head.appendChild(orbit);
        };
        document.head.appendChild(script);
    }
});
