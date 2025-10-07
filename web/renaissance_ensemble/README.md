# Leonardo's Mechanical Ensemble - Interactive Visualization

An immersive web experience that brings Leonardo da Vinci's mechanical musical inventions to life through interactive animations and synchronized music playback.

## Overview

This project recreates six of Leonardo's innovative mechanical instruments in a Renaissance court setting, complete with authentic animations, synchronized music notation, and educational content about the historical context and engineering principles behind each invention.

## Instruments Featured

1. **Mechanical Carillon** - Clock-driven bell system with rotating drum and programmable strikers
2. **Mechanical Drum** - Pinned barrel percussion device with multiple beaters
3. **Mechanical Organ** - Automatic pipe organ with bellows and pinned program barrel
4. **Mechanical Trumpeter** - Automated trumpet with valve system and bellows
5. **Programmable Flute** - Cam-driven recorder with automated fingering mechanisms
6. **Viola Organista** - Keyboard instrument with rosined wheel that continuously bows strings

## Features

### Interactive Visualizations
- Real-time animated instrument mechanisms
- Accurate mechanical movement based on Leonardo's designs
- Visual feedback for note playing and rhythm patterns
- Particle effects and resonance animations

### Music System
- Synchronized playback across all instruments
- Multiple Renaissance compositions
- Adjustable tempo control
- Individual instrument volume and mute controls

### Educational Content
- Historical context for each instrument
- Engineering principle explanations
- Leonardo's design innovations
- Modern adaptation information

### User Interface
- Responsive design for all devices
- Accessibility features (keyboard navigation, screen reader support)
- Multiple view modes (notation, animation, or both)
- Intuitive controls with visual feedback

## Technical Architecture

### Frontend Technologies
- **HTML5** - Semantic structure and canvas elements
- **CSS3** - Renaissance aesthetic with responsive design
- **JavaScript (ES6+)** - Interactive animations and music synchronization
- **Canvas API** - Real-time instrument animations
- **Web Audio API** - Sound synthesis and playback

### Code Organization
```
web/renaissance_ensemble/
├── index.html                 # Main application page
├── styles/                    # CSS stylesheets
│   ├── renaissance-ensemble.css    # Main styling
│   ├── instruments.css             # Instrument-specific styles
│   ├── notation.css                # Music notation styles
│   ├── controls.css                # UI control styles
│   └── responsive.css              # Responsive design
├── js/                        # JavaScript modules
│   ├── utils.js                    # Utility functions
│   ├── instrument-base.js          # Base instrument class
│   ├── carillon.js                 # Carillion implementation
│   ├── drum.js                     # Drum implementation
│   ├── organ.js                    # Organ implementation
│   ├── trumpeter.js                # Trumpeter implementation
│   ├── flute.js                    # Flute implementation
│   ├── viola-organista.js          # Viola implementation
│   ├── notation-renderer.js        # Music notation display
│   ├── music-engine.js             # Music playback system
│   ├── ensemble-controller.js      # Ensemble coordination
│   ├── ui-controller.js            # UI management
│   └── app.js                      # Main application controller
└── README.md                   # This documentation
```

### Design Patterns
- **Module Pattern** - Encapsulated JavaScript modules
- **Observer Pattern** - Event-driven architecture
- **Factory Pattern** - Instrument creation
- **Strategy Pattern** - Different animation and rendering strategies
- **Singleton Pattern** - Application state management

## Getting Started

### Prerequisites
- Modern web browser with HTML5, CSS3, and JavaScript ES6+ support
- Local web server (recommended for development)

### Installation
1. Clone or download the project files
2. Serve the files from a local web server:
   ```bash
   # Using Python 3
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8000
   ```
3. Open `http://localhost:8000` in your web browser

### Development
- Edit CSS files in the `styles/` directory
- Modify JavaScript modules in the `js/` directory
- Update HTML structure in `index.html`
- Refresh browser to see changes

## Usage Guide

### Basic Controls
- **Play/Pause** - Start or stop the ensemble performance
- **Stop** - Reset all instruments to initial state
- **Tempo Slider** - Adjust playback speed (40-200 BPM)
- **Composition Selector** - Choose different musical pieces

### Instrument Controls
- **Volume Sliders** - Adjust individual instrument volumes
- **Mute Buttons** - Silence specific instruments
- **Visual Indicators** - See which instruments are currently playing

### View Modes
- **Notation** - Display musical notation only
- **Animation** - Show instrument animations only
- **Both** - Display both notation and animations

### Educational Panels
- **Historical Context** - Learn about Renaissance court entertainment
- **Mechanical Design** - Understand the engineering principles
- **Modern Adaptation** - See how the designs work today
- **About Leonardo** - Discover the inventor's background

### Keyboard Shortcuts
- **Space** - Play/Pause
- **Escape** - Stop playback
- **Arrow Up** - Increase tempo
- **Arrow Down** - Decrease tempo

## Historical Context

Leonardo da Vinci designed these mechanical instruments between 1490-1496 for the sophisticated courts of Renaissance Italy. They represented the perfect fusion of art and engineering, capable of performing complex musical compositions without human musicians - a marvel that would have astonished contemporary audiences.

The designs draw on several key innovations:
- **Pinned Cylinders** - Rotating barrels with strategically placed pins to trigger mechanical actions
- **Cam Mechanisms** - Precisely shaped profiles to convert rotary motion into complex movements
- **Bellows Systems** - Automated air pressure regulation for wind instruments
- **Gear Trains** - Complex gearing for timing and synchronization

## Browser Compatibility

This application supports all modern browsers:
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Performance Considerations

- Canvas animations are optimized for 60fps playback
- Audio processing uses efficient Web Audio API scheduling
- Memory management prevents leaks during long playback sessions
- Responsive design adapts to device capabilities

## Accessibility

- Full keyboard navigation support
- Screen reader compatible with ARIA labels
- High contrast mode support
- Reduced motion preferences respected
- Focus indicators for all interactive elements

## Future Enhancements

### Planned Features
- [ ] Complete remaining instrument visualizations (Organ, Trumpeter, Flute, Viola)
- [ ] Advanced music notation rendering
- [ ] Recording and playback functionality
- [ ] Virtual reality (VR) support
- [ ] Multi-language support
- [ ] Additional Renaissance compositions

### Technical Improvements
- [ ] WebAssembly integration for performance
- [ ] Progressive Web App (PWA) features
- [ ] Real-time collaboration features
- [ ] Cloud-based composition sharing

## Contributing

This project is part of the Leonardo da Vinci Mechanical Ensemble simulation system. Contributions are welcome in the following areas:

- Instrument animation improvements
- Historical accuracy research
- Musical composition additions
- Accessibility enhancements
- Performance optimizations
- Bug fixes and testing

## License

This project is open source and available under the terms specified in the repository license. Educational use is strongly encouraged.

## Acknowledgments

- Historical research based on Leonardo's Codex Atlanticus manuscripts
- Musical compositions inspired by Renaissance court music
- Engineering principles derived from Leonardo's mechanical studies
- Educational content developed with historical accuracy in mind

---

*Experience the genius of Leonardo da Vinci through the intersection of art, music, and engineering in this interactive Renaissance court setting.*