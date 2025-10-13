/**
 * da Vinci Codex 3D Viewer
 * Interactive 3D model viewer for Leonardo's inventions
 * Uses Three.js for rendering with Renaissance-themed interface
 */

class DaVinci3DViewer {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error(`Container with ID '${containerId}' not found`);
        }

        // Default configuration
        this.config = {
            backgroundColor: 0xF5F5DC, // Beige parchment color
            ambientLightColor: 0x404040,
            directionalLightColor: 0xFFFFFF,
            lightIntensity: 0.8,
            modelColor: 0x8B4513, // Renaissance brown
            wireframeColor: 0xDAA520, // Gold accent
            enableControls: true,
            enableMeasurement: true,
            enableAnnotations: true,
            autoRotate: false,
            autoRotateSpeed: 0.5,
            cameraDistance: 10,
            ...options
        };

        // Initialize Three.js components
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.model = null;
        this.annotationGroup = null;
        this.measurementGroup = null;

        // State management
        this.currentModel = null;
        this.annotations = [];
        this.measurements = [];
        this.viewMode = 'solid'; // solid, wireframe, points
        this.isLoading = false;

        // UI components
        this.loadingIndicator = null;
        this.controlPanel = null;
        this.infoPanel = null;

        this.init();
    }

    init() {
        this.createLoadingIndicator();
        this.setupRenderer();
        this.setupScene();
        this.setupCamera();
        this.setupControls();
        this.setupLighting();
        this.setupEventListeners();
        this.createControlPanel();
        this.createInfoPanel();

        // Start render loop
        this.animate();

        // Initial resize
        this.handleResize();
    }

    createLoadingIndicator() {
        this.loadingIndicator = document.createElement('div');
        this.loadingIndicator.className = 'davinci-3d-viewer-loading';
        this.loadingIndicator.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Loading da Vinci's masterpiece...</p>
            </div>
        `;
        this.container.appendChild(this.loadingIndicator);
    }

    setupRenderer() {
        // Create Three.js renderer
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance'
        });

        // Set pixel ratio for retina displays
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setClearColor(this.config.backgroundColor, 1);

        // Enable shadows for better depth perception
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.2;

        this.container.appendChild(this.renderer.domElement);
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(this.config.backgroundColor);

        // Add fog for depth and Renaissance atmosphere
        this.scene.fog = new THREE.Fog(this.config.backgroundColor, 20, 100);

        // Create groups for organization
        this.annotationGroup = new THREE.Group();
        this.measurementGroup = new THREE.Group();
        this.scene.add(this.annotationGroup);
        this.scene.add(this.measurementGroup);

        // Add grid helper for reference
        const gridHelper = new THREE.GridHelper(20, 20, 0xDAA520, 0xCD853F);
        gridHelper.material.opacity = 0.2;
        gridHelper.material.transparent = true;
        this.scene.add(gridHelper);
    }

    setupCamera() {
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);

        // Position camera for good viewing angle
        this.camera.position.set(
            this.config.cameraDistance,
            this.config.cameraDistance * 0.7,
            this.config.cameraDistance
        );
        this.camera.lookAt(0, 0, 0);
    }

    setupControls() {
        if (!this.config.enableControls) return;

        // Use OrbitControls for intuitive interaction
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);

        // Configure controls
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.enableZoom = true;
        this.controls.enablePan = true;
        this.controls.enableRotate = true;

        // Set limits for better user experience
        this.controls.minDistance = 2;
        this.controls.maxDistance = 50;
        this.controls.maxPolarAngle = Math.PI * 0.8;
        this.controls.autoRotate = this.config.autoRotate;
        this.controls.autoRotateSpeed = this.config.autoRotateSpeed;

        // Update controls target
        this.controls.target.set(0, 0, 0);
    }

    setupLighting() {
        // Ambient lighting for overall illumination
        const ambientLight = new THREE.AmbientLight(
            this.config.ambientLightColor,
            0.4
        );
        this.scene.add(ambientLight);

        // Main directional light (simulating sunlight)
        const directionalLight = new THREE.DirectionalLight(
            this.config.directionalLightColor,
            this.config.lightIntensity
        );
        directionalLight.position.set(10, 20, 10);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 50;
        directionalLight.shadow.camera.left = -20;
        directionalLight.shadow.camera.right = 20;
        directionalLight.shadow.camera.top = 20;
        directionalLight.shadow.camera.bottom = -20;
        this.scene.add(directionalLight);

        // Fill light to reduce harsh shadows
        const fillLight = new THREE.DirectionalLight(0xFFFFFF, 0.3);
        fillLight.position.set(-10, 5, -10);
        this.scene.add(fillLight);

        // Rim light for edge definition
        const rimLight = new THREE.DirectionalLight(0xDAA520, 0.2);
        rimLight.position.set(0, -10, -20);
        this.scene.add(rimLight);
    }

    setupEventListeners() {
        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());

        // Handle mouse events for measurements and annotations
        this.renderer.domElement.addEventListener('click', (event) => this.handleClick(event));
        this.renderer.domElement.addEventListener('mousemove', (event) => this.handleMouseMove(event));
    }

    createControlPanel() {
        this.controlPanel = document.createElement('div');
        this.controlPanel.className = 'davinci-3d-viewer-controls';
        this.controlPanel.innerHTML = `
            <div class="controls-header">
                <h4>Viewer Controls</h4>
                <button class="toggle-controls" title="Toggle panel">
                    <span>×</span>
                </button>
            </div>
            <div class="controls-content">
                <div class="control-group">
                    <label>View Mode:</label>
                    <select id="view-mode">
                        <option value="solid">Solid</option>
                        <option value="wireframe">Wireframe</option>
                        <option value="points">Points</option>
                    </select>
                </div>
                <div class="control-group">
                    <label>Model Color:</label>
                    <input type="color" id="model-color" value="#8B4513">
                </div>
                <div class="control-group">
                    <label>Rotation:</label>
                    <button id="toggle-rotation">Auto Rotate</button>
                </div>
                <div class="control-group">
                    <label>View:</label>
                    <div class="view-presets">
                        <button data-view="front">Front</button>
                        <button data-view="side">Side</button>
                        <button data-view="top">Top</button>
                        <button data-view="iso">Isometric</button>
                    </div>
                </div>
                ${this.config.enableMeasurement ? `
                <div class="control-group">
                    <label>Measurements:</label>
                    <button id="measure-mode">Measure Distance</button>
                    <button id="clear-measurements">Clear All</button>
                </div>
                ` : ''}
                <div class="control-group">
                    <label>Export:</label>
                    <button id="screenshot">Screenshot</button>
                    <button id="reset-view">Reset View</button>
                </div>
            </div>
        `;

        this.container.appendChild(this.controlPanel);
        this.setupControlEventListeners();
    }

    createInfoPanel() {
        this.infoPanel = document.createElement('div');
        this.infoPanel.className = 'davinci-3d-viewer-info';
        this.infoPanel.innerHTML = `
            <div class="info-header">
                <h4>Model Information</h4>
                <button class="toggle-info" title="Toggle panel">
                    <span>×</span>
                </button>
            </div>
            <div class="info-content">
                <div class="model-details">
                    <p class="model-name">No model loaded</p>
                    <p class="model-stats"></p>
                </div>
                <div class="annotations-list"></div>
                <div class="measurements-list"></div>
            </div>
        `;

        this.container.appendChild(this.infoPanel);
        this.setupInfoEventListeners();
    }

    setupControlEventListeners() {
        // View mode selector
        const viewModeSelect = this.controlPanel.querySelector('#view-mode');
        viewModeSelect.addEventListener('change', (e) => {
            this.setViewMode(e.target.value);
        });

        // Model color picker
        const colorPicker = this.controlPanel.querySelector('#model-color');
        colorPicker.addEventListener('change', (e) => {
            this.setModelColor(e.target.value);
        });

        // Auto rotate toggle
        const rotateToggle = this.controlPanel.querySelector('#toggle-rotation');
        rotateToggle.addEventListener('click', () => {
            this.toggleAutoRotation();
        });

        // View presets
        const viewButtons = this.controlPanel.querySelectorAll('[data-view]');
        viewButtons.forEach(button => {
            button.addEventListener('click', () => {
                this.setViewPreset(button.dataset.view);
            });
        });

        // Measurement mode
        if (this.config.enableMeasurement) {
            const measureButton = this.controlPanel.querySelector('#measure-mode');
            measureButton.addEventListener('click', () => {
                this.toggleMeasurementMode();
            });

            const clearMeasurements = this.controlPanel.querySelector('#clear-measurements');
            clearMeasurements.addEventListener('click', () => {
                this.clearMeasurements();
            });
        }

        // Export options
        const screenshotButton = this.controlPanel.querySelector('#screenshot');
        screenshotButton.addEventListener('click', () => {
            this.takeScreenshot();
        });

        const resetButton = this.controlPanel.querySelector('#reset-view');
        resetButton.addEventListener('click', () => {
            this.resetView();
        });

        // Panel toggle
        const toggleButton = this.controlPanel.querySelector('.toggle-controls');
        toggleButton.addEventListener('click', () => {
            this.controlPanel.classList.toggle('collapsed');
        });
    }

    setupInfoEventListeners() {
        const toggleButton = this.infoPanel.querySelector('.toggle-info');
        toggleButton.addEventListener('click', () => {
            this.infoPanel.classList.toggle('collapsed');
        });
    }

    async loadSTL(url, metadata = {}) {
        this.showLoading(true);

        try {
            const loader = new THREE.STLLoader();
            const geometry = await new Promise((resolve, reject) => {
                loader.load(url, resolve, undefined, reject);
            });

            // Remove existing model
            if (this.model) {
                this.scene.remove(this.model);
                this.model.geometry.dispose();
                this.model.material.dispose();
            }

            // Create material with Renaissance theming
            const material = new THREE.MeshPhongMaterial({
                color: this.config.modelColor,
                specular: 0x222222,
                shininess: 25,
                side: THREE.DoubleSide
            });

            // Create mesh
            this.model = new THREE.Mesh(geometry, material);
            this.model.castShadow = true;
            this.model.receiveShadow = true;

            // Center and scale the model
            this.centerAndScaleModel();

            // Add to scene
            this.scene.add(this.model);

            // Update view mode
            this.setViewMode(this.viewMode);

            // Update info panel
            this.updateModelInfo(metadata);

            // Add annotations if available
            if (metadata.annotations) {
                this.addAnnotations(metadata.annotations);
            }

            this.currentModel = { url, metadata };

        } catch (error) {
            console.error('Error loading STL:', error);
            this.showError('Failed to load 3D model. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    centerAndScaleModel() {
        if (!this.model) return;

        // Calculate bounding box
        const box = new THREE.Box3().setFromObject(this.model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        // Center the model
        this.model.position.sub(center);

        // Scale to fit in viewer
        const maxDim = Math.max(size.x, size.y, size.z);
        const scale = 8 / maxDim; // Target size of 8 units
        this.model.scale.multiplyScalar(scale);

        // Update controls target
        if (this.controls) {
            this.controls.target.set(0, 0, 0);
            this.controls.update();
        }
    }

    setViewMode(mode) {
        this.viewMode = mode;
        if (!this.model) return;

        const material = this.model.material;

        switch (mode) {
            case 'wireframe':
                material.wireframe = true;
                material.color.set(this.config.wireframeColor);
                break;
            case 'points':
                material.wireframe = false;
                // For points mode, we'd need to create a new geometry with points
                // This is a simplified implementation
                material.color.set(this.config.modelColor);
                break;
            default:
                material.wireframe = false;
                material.color.set(this.config.modelColor);
                break;
        }
    }

    setModelColor(color) {
        if (!this.model) return;
        this.model.material.color.set(color);
    }

    toggleAutoRotation() {
        if (!this.controls) return;
        this.controls.autoRotate = !this.controls.autoRotate;

        const button = this.controlPanel.querySelector('#toggle-rotation');
        button.textContent = this.controls.autoRotate ? 'Stop Rotation' : 'Auto Rotate';
        button.classList.toggle('active', this.controls.autoRotate);
    }

    setViewPreset(view) {
        if (!this.camera || !this.controls) return;

        const distance = this.config.cameraDistance;

        switch (view) {
            case 'front':
                this.camera.position.set(0, 0, distance);
                break;
            case 'side':
                this.camera.position.set(distance, 0, 0);
                break;
            case 'top':
                this.camera.position.set(0, distance, 0);
                break;
            case 'iso':
                this.camera.position.set(distance, distance * 0.7, distance);
                break;
        }

        this.camera.lookAt(0, 0, 0);
        this.controls.target.set(0, 0, 0);
        this.controls.update();
    }

    toggleMeasurementMode() {
        this.measurementMode = !this.measurementMode;

        const button = this.controlPanel.querySelector('#measure-mode');
        button.textContent = this.measurementMode ? 'Exit Measure Mode' : 'Measure Distance';
        button.classList.toggle('active', this.measurementMode);

        // Change cursor
        this.renderer.domElement.style.cursor = this.measurementMode ? 'crosshair' : 'default';
    }

    clearMeasurements() {
        // Clear measurement visualizations
        while (this.measurementGroup.children.length > 0) {
            const child = this.measurementGroup.children[0];
            this.measurementGroup.remove(child);
            if (child.geometry) child.geometry.dispose();
            if (child.material) child.material.dispose();
        }

        this.measurements = [];
        this.updateMeasurementsList();
    }

    addAnnotations(annotations) {
        // Clear existing annotations
        while (this.annotationGroup.children.length > 0) {
            const child = this.annotationGroup.children[0];
            this.annotationGroup.remove(child);
            if (child.geometry) child.geometry.dispose();
            if (child.material) child.material.dispose();
        }

        // Add new annotations
        annotations.forEach(annotation => {
            this.addAnnotation(annotation);
        });

        this.updateAnnotationsList();
    }

    addAnnotation(annotation) {
        // Create annotation marker
        const geometry = new THREE.SphereGeometry(0.1, 16, 16);
        const material = new THREE.MeshBasicMaterial({ color: 0xFFD700 });
        const marker = new THREE.Mesh(geometry, material);

        marker.position.set(...annotation.position);
        marker.userData = annotation;

        this.annotationGroup.add(marker);
        this.annotations.push(annotation);
    }

    handleClick(event) {
        if (this.measurementMode && this.model) {
            // Handle measurement point selection
            this.handleMeasurementClick(event);
        } else {
            // Handle annotation selection
            this.handleAnnotationClick(event);
        }
    }

    handleMeasurementClick(event) {
        const rect = this.renderer.domElement.getBoundingClientRect();
        const mouse = new THREE.Vector2(
            ((event.clientX - rect.left) / rect.width) * 2 - 1,
            -((event.clientY - rect.top) / rect.height) * 2 + 1
        );

        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, this.camera);

        const intersects = raycaster.intersectObject(this.model);

        if (intersects.length > 0) {
            const point = intersects[0].point;
            this.addMeasurementPoint(point);
        }
    }

    addMeasurementPoint(point) {
        // Create point visualization
        const geometry = new THREE.SphereGeometry(0.05, 8, 8);
        const material = new THREE.MeshBasicMaterial({ color: 0xFF0000 });
        const sphere = new THREE.Mesh(geometry, material);
        sphere.position.copy(point);

        this.measurementGroup.add(sphere);

        // Store measurement point
        this.measurementPoints = this.measurementPoints || [];
        this.measurementPoints.push(point);

        // If we have two points, create a measurement line
        if (this.measurementPoints.length === 2) {
            this.createMeasurementLine(this.measurementPoints[0], this.measurementPoints[1]);
            this.measurementPoints = [];
        }
    }

    createMeasurementLine(point1, point2) {
        const geometry = new THREE.BufferGeometry().setFromPoints([point1, point2]);
        const material = new THREE.LineBasicMaterial({ color: 0xFF0000, linewidth: 2 });
        const line = new THREE.Line(geometry, material);

        this.measurementGroup.add(line);

        // Calculate distance
        const distance = point1.distanceTo(point2);
        this.measurements.push({
            distance: distance.toFixed(2),
            points: [point1, point2]
        });

        this.updateMeasurementsList();
    }

    handleAnnotationClick(event) {
        const rect = this.renderer.domElement.getBoundingClientRect();
        const mouse = new THREE.Vector2(
            ((event.clientX - rect.left) / rect.width) * 2 - 1,
            -((event.clientY - rect.top) / rect.height) * 2 + 1
        );

        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, this.camera);

        const intersects = raycaster.intersectObjects(this.annotationGroup.children);

        if (intersects.length > 0) {
            const annotation = intersects[0].object.userData;
            this.showAnnotationDetails(annotation);
        }
    }

    showAnnotationDetails(annotation) {
        // Create or update annotation popup
        let popup = document.querySelector('.annotation-popup');
        if (!popup) {
            popup = document.createElement('div');
            popup.className = 'annotation-popup';
            document.body.appendChild(popup);
        }

        popup.innerHTML = `
            <div class="annotation-content">
                <h4>${annotation.title}</h4>
                <p>${annotation.description}</p>
                <button class="close-popup">×</button>
            </div>
        `;

        popup.style.display = 'block';

        const closeButton = popup.querySelector('.close-popup');
        closeButton.addEventListener('click', () => {
            popup.style.display = 'none';
        });
    }

    handleMouseMove(event) {
        // Update cursor based on what's being hovered
        const rect = this.renderer.domElement.getBoundingClientRect();
        const mouse = new THREE.Vector2(
            ((event.clientX - rect.left) / rect.width) * 2 - 1,
            -((event.clientY - rect.top) / rect.height) * 2 + 1
        );

        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, this.camera);

        // Check for annotations
        const annotationIntersects = raycaster.intersectObjects(this.annotationGroup.children);

        if (annotationIntersects.length > 0 || this.measurementMode) {
            this.renderer.domElement.style.cursor = 'pointer';
        } else {
            this.renderer.domElement.style.cursor = 'default';
        }
    }

    takeScreenshot() {
        const canvas = this.renderer.domElement;
        const link = document.createElement('a');
        link.download = 'davinci-model.png';
        link.href = canvas.toDataURL();
        link.click();
    }

    resetView() {
        this.setViewPreset('iso');
        this.setModelColor(this.config.modelColor);
        this.setViewMode('solid');

        if (this.controls) {
            this.controls.autoRotate = false;
            this.controls.reset();
        }

        // Reset UI controls
        const viewModeSelect = this.controlPanel.querySelector('#view-mode');
        viewModeSelect.value = 'solid';

        const colorPicker = this.controlPanel.querySelector('#model-color');
        colorPicker.value = '#8B4513';
    }

    updateModelInfo(metadata) {
        const nameElement = this.infoPanel.querySelector('.model-name');
        const statsElement = this.infoPanel.querySelector('.model-stats');

        nameElement.textContent = metadata.title || 'Unknown Model';

        if (this.model) {
            const geometry = this.model.geometry;
            const vertices = geometry.attributes.position ? geometry.attributes.position.count : 0;
            const faces = geometry.index ? geometry.index.count / 3 : vertices / 3;

            statsElement.innerHTML = `
                <strong>Vertices:</strong> ${vertices.toLocaleString()}<br>
                <strong>Faces:</strong> ${Math.floor(faces).toLocaleString()}<br>
                ${metadata.material ? `<strong>Material:</strong> ${metadata.material}<br>` : ''}
                ${metadata.dimensions ? `<strong>Dimensions:</strong> ${metadata.dimensions}<br>` : ''}
                ${metadata.year ? `<strong>Year:</strong> ${metadata.year}<br>` : ''}
                ${metadata.folio ? `<strong>Folio:</strong> ${metadata.folio}` : ''}
            `;
        }
    }

    updateAnnotationsList() {
        const listElement = this.infoPanel.querySelector('.annotations-list');

        if (this.annotations.length === 0) {
            listElement.innerHTML = '';
            return;
        }

        listElement.innerHTML = `
            <h5>Annotations:</h5>
            <ul>
                ${this.annotations.map(annotation => `
                    <li>
                        <strong>${annotation.title}:</strong> ${annotation.description}
                    </li>
                `).join('')}
            </ul>
        `;
    }

    updateMeasurementsList() {
        const listElement = this.infoPanel.querySelector('.measurements-list');

        if (this.measurements.length === 0) {
            listElement.innerHTML = '';
            return;
        }

        listElement.innerHTML = `
            <h5>Measurements:</h5>
            <ul>
                ${this.measurements.map((measurement, index) => `
                    <li>
                        Measurement ${index + 1}: ${measurement.distance} units
                    </li>
                `).join('')}
            </ul>
        `;
    }

    showLoading(show) {
        this.isLoading = show;
        this.loadingIndicator.style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'davinci-3d-viewer-error';
        errorDiv.innerHTML = `
            <div class="error-content">
                <span class="error-icon">⚠</span>
                <p>${message}</p>
                <button class="close-error">×</button>
            </div>
        `;

        this.container.appendChild(errorDiv);

        const closeButton = errorDiv.querySelector('.close-error');
        closeButton.addEventListener('click', () => {
            errorDiv.remove();
        });

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }

    handleResize() {
        if (!this.camera || !this.renderer) return;

        const width = this.container.clientWidth;
        const height = this.container.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        if (this.controls) {
            this.controls.update();
        }

        this.renderer.render(this.scene, this.camera);
    }

    dispose() {
        // Clean up Three.js resources
        if (this.model) {
            this.scene.remove(this.model);
            this.model.geometry.dispose();
            this.model.material.dispose();
        }

        // Clear annotations and measurements
        while (this.annotationGroup.children.length > 0) {
            const child = this.annotationGroup.children[0];
            this.annotationGroup.remove(child);
            if (child.geometry) child.geometry.dispose();
            if (child.material) child.material.dispose();
        }

        while (this.measurementGroup.children.length > 0) {
            const child = this.measurementGroup.children[0];
            this.measurementGroup.remove(child);
            if (child.geometry) child.geometry.dispose();
            if (child.material) child.material.dispose();
        }

        // Dispose renderer
        if (this.renderer) {
            this.renderer.dispose();
            this.container.removeChild(this.renderer.domElement);
        }

        // Remove event listeners
        window.removeEventListener('resize', this.handleResize);
    }
}

// Export for use in other modules
window.DaVinci3DViewer = DaVinci3DViewer;