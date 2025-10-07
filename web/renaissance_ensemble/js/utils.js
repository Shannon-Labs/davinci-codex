/**
 * Leonardo's Mechanical Ensemble - Utility Functions
 * Common utilities for the interactive visualization system
 */

// Global namespace for the ensemble application
window.LeonardoEnsemble = window.LeonardoEnsemble || {};

/**
 * Utility functions namespace
 */
LeonardoEnsemble.Utils = {
    /**
     * Animation frame management
     */
    animation: {
        frameId: null,
        callbacks: new Set(),
        
        /**
         * Add a callback to the animation loop
         * @param {Function} callback - Animation callback function
         */
        add(callback) {
            this.callbacks.add(callback);
            if (this.callbacks.size === 1) {
                this.start();
            }
        },
        
        /**
         * Remove a callback from the animation loop
         * @param {Function} callback - Animation callback function
         */
        remove(callback) {
            this.callbacks.delete(callback);
            if (this.callbacks.size === 0) {
                this.stop();
            }
        },
        
        /**
         * Start the animation loop
         */
        start() {
            const loop = (timestamp) => {
                this.callbacks.forEach(callback => callback(timestamp));
                this.frameId = requestAnimationFrame(loop);
            };
            this.frameId = requestAnimationFrame(loop);
        },
        
        /**
         * Stop the animation loop
         */
        stop() {
            if (this.frameId) {
                cancelAnimationFrame(this.frameId);
                this.frameId = null;
            }
        }
    },
    
    /**
     * Time and tempo utilities
     */
    time: {
        /**
         * Convert BPM to milliseconds per beat
         * @param {number} bpm - Beats per minute
         * @returns {number} Milliseconds per beat
         */
        bpmToMs(bpm) {
            return 60000 / bpm;
        },
        
        /**
         * Convert beats to seconds
         * @param {number} beats - Number of beats
         * @param {number} bpm - Beats per minute
         * @returns {number} Duration in seconds
         */
        beatsToSeconds(beats, bpm) {
            return (beats * 60) / bpm;
        },
        
        /**
         * Format time as MM:SS
         * @param {number} seconds - Time in seconds
         * @returns {string} Formatted time string
         */
        formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        },
        
        /**
         * Get current timestamp with high precision
         * @returns {number} High precision timestamp
         */
        getTimestamp() {
            return performance.now();
        }
    },
    
    /**
     * Mathematical utilities
     */
    math: {
        /**
         * Linear interpolation between two values
         * @param {number} a - Start value
         * @param {number} b - End value
         * @param {number} t - Interpolation factor (0-1)
         * @returns {number} Interpolated value
         */
        lerp(a, b, t) {
            return a + (b - a) * Math.max(0, Math.min(1, t));
        },
        
        /**
         * Clamp a value between min and max
         * @param {number} value - Value to clamp
         * @param {number} min - Minimum value
         * @param {number} max - Maximum value
         * @returns {number} Clamped value
         */
        clamp(value, min, max) {
            return Math.max(min, Math.min(max, value));
        },
        
        /**
         * Map a value from one range to another
         * @param {number} value - Value to map
         * @param {number} inMin - Input minimum
         * @param {number} inMax - Input maximum
         * @param {number} outMin - Output minimum
         * @param {number} outMax - Output maximum
         * @returns {number} Mapped value
         */
        map(value, inMin, inMax, outMin, outMax) {
            return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
        },
        
        /**
         * Convert degrees to radians
         * @param {number} degrees - Angle in degrees
         * @returns {number} Angle in radians
         */
        degToRad(degrees) {
            return degrees * (Math.PI / 180);
        },
        
        /**
         * Convert radians to degrees
         * @param {number} radians - Angle in radians
         * @returns {number} Angle in degrees
         */
        radToDeg(radians) {
            return radians * (180 / Math.PI);
        },
        
        /**
         * Generate a random number between min and max
         * @param {number} min - Minimum value
         * @param {number} max - Maximum value
         * @returns {number} Random number
         */
        random(min, max) {
            return Math.random() * (max - min) + min;
        },
        
        /**
         * Generate a random integer between min and max (inclusive)
         * @param {number} min - Minimum integer
         * @param {number} max - Maximum integer
         * @returns {number} Random integer
         */
        randomInt(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }
    },
    
    /**
     * Canvas drawing utilities
     */
    canvas: {
        /**
         * Clear a canvas
         * @param {HTMLCanvasElement} canvas - Canvas element
         */
        clear(canvas) {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        },
        
        /**
         * Set canvas size with proper scaling
         * @param {HTMLCanvasElement} canvas - Canvas element
         * @param {number} width - Canvas width
         * @param {number} height - Canvas height
         */
        setSize(canvas, width, height) {
            const dpr = window.devicePixelRatio || 1;
            canvas.width = width * dpr;
            canvas.height = height * dpr;
            canvas.style.width = width + 'px';
            canvas.style.height = height + 'px';
            
            const ctx = canvas.getContext('2d');
            ctx.scale(dpr, dpr);
        },
        
        /**
         * Draw a circle
         * @param {CanvasRenderingContext2D} ctx - Canvas context
         * @param {number} x - X position
         * @param {number} y - Y position
         * @param {number} radius - Circle radius
         * @param {Object} options - Drawing options
         */
        drawCircle(ctx, x, y, radius, options = {}) {
            ctx.save();
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            
            if (options.fill) {
                ctx.fillStyle = options.fill;
                ctx.fill();
            }
            
            if (options.stroke) {
                ctx.strokeStyle = options.stroke;
                ctx.lineWidth = options.lineWidth || 1;
                ctx.stroke();
            }
            
            ctx.restore();
        },
        
        /**
         * Draw a rectangle
         * @param {CanvasRenderingContext2D} ctx - Canvas context
         * @param {number} x - X position
         * @param {number} y - Y position
         * @param {number} width - Rectangle width
         * @param {number} height - Rectangle height
         * @param {Object} options - Drawing options
         */
        drawRect(ctx, x, y, width, height, options = {}) {
            ctx.save();
            
            if (options.fill) {
                ctx.fillStyle = options.fill;
                ctx.fillRect(x, y, width, height);
            }
            
            if (options.stroke) {
                ctx.strokeStyle = options.stroke;
                ctx.lineWidth = options.lineWidth || 1;
                ctx.strokeRect(x, y, width, height);
            }
            
            ctx.restore();
        },
        
        /**
         * Draw a line
         * @param {CanvasRenderingContext2D} ctx - Canvas context
         * @param {number} x1 - Start X position
         * @param {number} y1 - Start Y position
         * @param {number} x2 - End X position
         * @param {number} y2 - End Y position
         * @param {Object} options - Drawing options
         */
        drawLine(ctx, x1, y1, x2, y2, options = {}) {
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = options.stroke || '#000';
            ctx.lineWidth = options.lineWidth || 1;
            ctx.stroke();
            ctx.restore();
        },
        
        /**
         * Draw text with optional styling
         * @param {CanvasRenderingContext2D} ctx - Canvas context
         * @param {string} text - Text to draw
         * @param {number} x - X position
         * @param {number} y - Y position
         * @param {Object} options - Drawing options
         */
        drawText(ctx, text, x, y, options = {}) {
            ctx.save();
            ctx.font = options.font || '16px Arial';
            ctx.fillStyle = options.fill || '#000';
            ctx.textAlign = options.align || 'left';
            ctx.textBaseline = options.baseline || 'top';
            
            if (options.shadow) {
                ctx.shadowColor = options.shadow.color || 'rgba(0,0,0,0.5)';
                ctx.shadowBlur = options.shadow.blur || 4;
                ctx.shadowOffsetX = options.shadow.x || 2;
                ctx.shadowOffsetY = options.shadow.y || 2;
            }
            
            ctx.fillText(text, x, y);
            ctx.restore();
        }
    },
    
    /**
     * DOM manipulation utilities
     */
    dom: {
        /**
         * Get an element by selector
         * @param {string} selector - CSS selector
         * @param {Element} parent - Parent element to search within
         * @returns {Element|null} Found element or null
         */
        get(selector, parent = document) {
            return parent.querySelector(selector);
        },
        
        /**
         * Get all elements by selector
         * @param {string} selector - CSS selector
         * @param {Element} parent - Parent element to search within
         * @returns {NodeList} Found elements
         */
        getAll(selector, parent = document) {
            return parent.querySelectorAll(selector);
        },
        
        /**
         * Add event listener with automatic cleanup
         * @param {Element} element - Target element
         * @param {string} event - Event name
         * @param {Function} handler - Event handler
         * @param {Object} options - Event options
         */
        on(element, event, handler, options = {}) {
            element.addEventListener(event, handler, options);
        },
        
        /**
         * Remove event listener
         * @param {Element} element - Target element
         * @param {string} event - Event name
         * @param {Function} handler - Event handler
         */
        off(element, event, handler) {
            element.removeEventListener(event, handler);
        },
        
        /**
         * Add CSS class to element
         * @param {Element} element - Target element
         * @param {...string} classes - CSS classes to add
         */
        addClass(element, ...classes) {
            element.classList.add(...classes);
        },
        
        /**
         * Remove CSS class from element
         * @param {Element} element - Target element
         * @param {...string} classes - CSS classes to remove
         */
        removeClass(element, ...classes) {
            element.classList.remove(...classes);
        },
        
        /**
         * Toggle CSS class on element
         * @param {Element} element - Target element
         * @param {string} className - CSS class to toggle
         * @param {boolean} force - Force add or remove
         */
        toggleClass(element, className, force) {
            element.classList.toggle(className, force);
        },
        
        /**
         * Check if element has CSS class
         * @param {Element} element - Target element
         * @param {string} className - CSS class to check
         * @returns {boolean} Whether element has class
         */
        hasClass(element, className) {
            return element.classList.contains(className);
        },
        
        /**
         * Set element attribute
         * @param {Element} element - Target element
         * @param {string} attribute - Attribute name
         * @param {string} value - Attribute value
         */
        setAttr(element, attribute, value) {
            element.setAttribute(attribute, value);
        },
        
        /**
         * Get element attribute
         * @param {Element} element - Target element
         * @param {string} attribute - Attribute name
         * @returns {string|null} Attribute value or null
         */
        getAttr(element, attribute) {
            return element.getAttribute(attribute);
        },
        
        /**
         * Create element with optional properties
         * @param {string} tagName - Element tag name
         * @param {Object} properties - Element properties
         * @returns {Element} Created element
         */
        create(tagName, properties = {}) {
            const element = document.createElement(tagName);
            
            Object.entries(properties).forEach(([key, value]) => {
                if (key === 'className') {
                    element.className = value;
                } else if (key === 'innerHTML') {
                    element.innerHTML = value;
                } else if (key === 'textContent') {
                    element.textContent = value;
                } else if (key.startsWith('data-')) {
                    element.setAttribute(key, value);
                } else {
                    element[key] = value;
                }
            });
            
            return element;
        }
    },
    
    /**
     * Event management utilities
     */
    events: {
        /**
         * Create a custom event
         * @param {string} name - Event name
         * @param {Object} detail - Event detail data
         * @param {Object} options - Event options
         * @returns {CustomEvent} Custom event
         */
        create(name, detail = {}, options = {}) {
            return new CustomEvent(name, {
                detail,
                bubbles: true,
                cancelable: true,
                ...options
            });
        },
        
        /**
         * Dispatch a custom event
         * @param {Element} target - Event target
         * @param {string} name - Event name
         * @param {Object} detail - Event detail data
         * @param {Object} options - Event options
         */
        dispatch(target, name, detail = {}, options = {}) {
            const event = this.create(name, detail, options);
            target.dispatchEvent(event);
        },
        
        /**
         * Event emitter class for custom event management
         */
        EventEmitter: class {
            constructor() {
                this.events = new Map();
            }
            
            /**
             * Add event listener
             * @param {string} event - Event name
             * @param {Function} handler - Event handler
             */
            on(event, handler) {
                if (!this.events.has(event)) {
                    this.events.set(event, new Set());
                }
                this.events.get(event).add(handler);
            }
            
            /**
             * Remove event listener
             * @param {string} event - Event name
             * @param {Function} handler - Event handler
             */
            off(event, handler) {
                if (this.events.has(event)) {
                    this.events.get(event).delete(handler);
                }
            }
            
            /**
             * Emit event
             * @param {string} event - Event name
             * @param {*} data - Event data
             */
            emit(event, data) {
                if (this.events.has(event)) {
                    this.events.get(event).forEach(handler => {
                        try {
                            handler(data);
                        } catch (error) {
                            console.error(`Error in event handler for ${event}:`, error);
                        }
                    });
                }
            }
            
            /**
             * Remove all event listeners
             */
            clear() {
                this.events.clear();
            }
        }
    },
    
    /**
     * Storage utilities
     */
    storage: {
        /**
         * Set item in localStorage
         * @param {string} key - Storage key
         * @param {*} value - Value to store (will be JSON stringified)
         */
        set(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (error) {
                console.warn('Failed to save to localStorage:', error);
            }
        },
        
        /**
         * Get item from localStorage
         * @param {string} key - Storage key
         * @param {*} defaultValue - Default value if key not found
         * @returns {*} Stored value or default
         */
        get(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (error) {
                console.warn('Failed to read from localStorage:', error);
                return defaultValue;
            }
        },
        
        /**
         * Remove item from localStorage
         * @param {string} key - Storage key
         */
        remove(key) {
            try {
                localStorage.removeItem(key);
            } catch (error) {
                console.warn('Failed to remove from localStorage:', error);
            }
        },
        
        /**
         * Clear all localStorage items
         */
        clear() {
            try {
                localStorage.clear();
            } catch (error) {
                console.warn('Failed to clear localStorage:', error);
            }
        }
    },
    
    /**
     * Debounce function for performance optimization
     * @param {Function} func - Function to debounce
     * @param {number} wait - Wait time in milliseconds
     * @param {boolean} immediate - Whether to execute immediately
     * @returns {Function} Debounced function
     */
    debounce(func, wait, immediate = false) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    },
    
    /**
     * Throttle function for performance optimization
     * @param {Function} func - Function to throttle
     * @param {number} limit - Time limit in milliseconds
     * @returns {Function} Throttled function
     */
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func(...args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    /**
     * Check if device supports touch
     * @returns {boolean} Whether device supports touch
     */
    isTouchDevice() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    },
    
    /**
     * Get device pixel ratio
     * @returns {number} Device pixel ratio
     */
    getPixelRatio() {
        return window.devicePixelRatio || 1;
    },
    
    /**
     * Check if element is in viewport
     * @param {Element} element - Element to check
     * @param {number} threshold - Visibility threshold (0-1)
     * @returns {boolean} Whether element is in viewport
     */
    isInViewport(element, threshold = 0.5) {
        const rect = element.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const windowWidth = window.innerWidth || document.documentElement.clientWidth;
        
        const vertInView = (rect.top <= windowHeight * threshold) && ((rect.top + rect.height) >= windowHeight * (1 - threshold));
        const horInView = (rect.left <= windowWidth * threshold) && ((rect.left + rect.width) >= windowWidth * (1 - threshold));
        
        return vertInView && horInView;
    }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LeonardoEnsemble.Utils;
}