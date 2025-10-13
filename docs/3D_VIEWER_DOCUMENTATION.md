# 3D Viewer System Documentation

## Overview

The da Vinci Codex 3D Viewer System is an interactive web-based platform for exploring Leonardo da Vinci's mechanical inventions in three dimensions. Built with Three.js and styled with Renaissance-inspired aesthetics, the system provides an immersive educational experience that brings historical engineering to life.

## System Architecture

### Core Components

1. **3D Viewer Engine** (`/assets/js/3d-viewer.js`)
   - Three.js-based rendering engine
   - STL file loading and processing
   - Interactive controls (rotation, zoom, pan)
   - Measurement and annotation systems
   - Renaissance-themed visual design

2. **Styling System** (`/assets/css/3d-viewer.css`)
   - Responsive design for all devices
   - Renaissance color palette and typography
   - Accessibility-compliant interface
   - Print-friendly styles

3. **Jekyll Integration** (`/_layouts/viewer.html`)
   - Template system for viewer pages
   - Dynamic model loading from front matter
   - SEO optimization
   - Mobile-responsive layout

4. **Content Management**
   - Individual model pages with metadata
   - Gallery overview page
   - Navigation integration
   - Educational context integration

## Features

### Interactive Controls
- **Rotation**: Click and drag to rotate models in 3D space
- **Zoom**: Mouse wheel or pinch gesture for zooming
- **Pan**: Right-click and drag to move the view
- **Auto-rotation**: Toggle automatic model rotation
- **View presets**: Predefined camera angles (front, side, top, isometric)

### Model Analysis Tools
- **Measurement system**: Click-to-measure distance tool
- **Component annotations**: Interactive hotspots with detailed information
- **View modes**: Solid, wireframe, and point cloud rendering
- **Color customization**: Adjustable model colors for educational emphasis

### Educational Features
- **Historical context**: Detailed background information
- **Technical specifications**: Engineering parameters and materials
- **Multiple configurations**: Different operating states and assembly views
- **Related content**: Links to similar inventions and concepts

## File Structure

```
docs/
├── assets/
│   ├── js/
│   │   └── 3d-viewer.js          # Main viewer JavaScript
│   └── css/
│       └── 3d-viewer.css         # Viewer styles
├── _layouts/
│   └── viewer.html               # Jekyll viewer layout
├── aerial_screw_viewer.md        # Aerial Screw viewer page
├── mechanical_lion_viewer.md     # Mechanical Lion viewer page
├── musical_instruments_viewer.md # Musical Instruments collection
├── self_propelled_cart_viewer.md # Self-Propelled Cart viewer page
└── 3d-gallery.md                 # Main gallery overview
```

## Model Requirements

### File Formats
- **Primary**: STL (Stereolithography) files
- **Supported**: OBJ files (future enhancement)
- **Optimization**: Progressive loading for large models

### Model Specifications
- **Recommended vertices**: < 200,000 per model
- **Recommended file size**: < 15 MB
- **Coordinate system**: Right-handed, Y-up
- **Units**: Meters (1:1 scale preferred)

### Metadata Structure
Each model should include:
- Title and description
- Historical context and dating
- Technical specifications
- Component annotations
- Multiple configurations (if applicable)

## Page Front Matter Template

```yaml
---
layout: viewer
title: "Invention Name - Interactive 3D Model"
subtitle: "Brief description"
category: "Category Name"
date: YYYY-MM-DD
folio: "Codex reference"

model_url: "/path/to/model.stl"

model_variants:
  - name: "Configuration Name"
    url: "/path/to/variant.stl"
    metadata:
      description: "Description of this configuration"
      vertices: 100000
      faces: 67000

model_metadata:
  vertices: 100000
  faces: 67000
  file_size: "8.2 MB"
  materials: ["Material 1", "Material 2"]
  scale: "1:1"
  dimensions: "1.6m × 0.8m × 1.2m"

annotations:
  - title: "Component Name"
    description: "Detailed description"
    position: [x, y, z]
    material: "Material type"

technical_specifications: |
  ## Detailed technical specifications
  Engineering details in Markdown format

historical_context: |
  ## Historical background
  Historical information in Markdown format

---
```

## Browser Compatibility

### Supported Browsers
- **Chrome**: 80+ (recommended)
- **Firefox**: 75+
- **Safari**: 13+
- **Edge**: 80+
- **Mobile**: iOS Safari 13+, Android Chrome 80+

### Required Features
- WebGL 2.0 support
- ES6 JavaScript support
- CSS Grid and Flexbox
- File API for model loading

### Performance Optimization
- Progressive model loading
- Level-of-detail rendering
- Memory management for large models
- Touch gesture optimization

## Usage Guide

### For Users

1. **Loading Models**: Models load automatically when pages open
2. **Basic Navigation**: Use mouse/touch to rotate, zoom, and pan
3. **Information Access**: Click annotations to learn about components
4. **Measurement**: Activate measurement tool to analyze dimensions
5. **Configuration**: Use variant selector to view different model states

### For Content Creators

1. **Prepare Models**: Export STL files with appropriate detail levels
2. **Create Annotations**: Define component information and positions
3. **Write Content**: Provide historical and technical context
4. **Configure Metadata**: Include specifications and materials
5. **Test Integration**: Verify models load and display correctly

### For Developers

1. **Customization**: Modify viewer settings in the constructor options
2. **Extension**: Add new features through the modular architecture
3. **Integration**: Embed viewers in other applications
4. **Styling**: Customize appearance through CSS variables

## API Reference

### DaVinci3DViewer Class

```javascript
// Initialize viewer
const viewer = new DaVinci3DViewer(containerId, options);

// Load model
await viewer.loadSTL(url, metadata);

// Control methods
viewer.setViewMode(mode); // 'solid', 'wireframe', 'points'
viewer.setModelColor(color);
viewer.toggleAutoRotation();
viewer.setViewPreset(view); // 'front', 'side', 'top', 'iso'
viewer.resetView();

// Measurement tools
viewer.toggleMeasurementMode();
viewer.clearMeasurements();

// Annotations
viewer.addAnnotations(annotations);
viewer.clearAnnotations();

// Export
viewer.takeScreenshot();

// Cleanup
viewer.dispose();
```

### Configuration Options

```javascript
const options = {
    backgroundColor: 0xF5F5DC,    // Parchment color
    ambientLightColor: 0x404040,  // Ambient lighting
    directionalLightColor: 0xFFFFFF, // Main light
    lightIntensity: 0.8,          // Light intensity
    modelColor: 0x8B4513,         // Renaissance brown
    wireframeColor: 0xDAA520,     // Gold accent
    enableControls: true,         // Enable orbit controls
    enableMeasurement: true,      // Enable measurement tools
    enableAnnotations: true,      // Enable annotations
    autoRotate: false,            // Auto-rotate on load
    autoRotateSpeed: 0.5,         // Rotation speed
    cameraDistance: 10            // Initial camera distance
};
```

## Performance Guidelines

### Model Optimization
- **Polygon Count**: Keep under 200,000 triangles for smooth performance
- **Texture Usage**: Minimize textures; use solid colors where possible
- **File Size**: Compress STL files without losing essential detail
- **Level of Detail**: Provide multiple detail levels if possible

### Loading Optimization
- **Progressive Loading**: Load basic geometry first, then details
- **Caching**: Leverage browser caching for repeated visits
- **Compression**: Use gzip compression for model files
- **Lazy Loading**: Load additional models on demand

### Memory Management
- **Dispose Resources**: Clean up Three.js objects when switching models
- **Geometry Merging**: Combine static elements where possible
- **Texture Recycling**: Reuse materials and textures across models
- **Garbage Collection**: Monitor memory usage during extended sessions

## Accessibility Features

### Keyboard Navigation
- **Tab**: Navigate between interactive elements
- **Enter/Space**: Activate buttons and controls
- **Arrow Keys**: Adjust view angles when applicable
- **Escape**: Exit measurement mode

### Screen Reader Support
- **ARIA Labels**: Comprehensive labeling for all controls
- **Alternative Text**: Descriptive text for visual content
- **Semantic HTML**: Proper heading structure and landmarks
- **Focus Management**: Logical tab order and focus indicators

### Visual Accessibility
- **High Contrast**: Support for high contrast mode
- **Text Scaling**: Adjustable font sizes
- **Color Independence**: Information not conveyed by color alone
- **Reduced Motion**: Respect user's motion preferences

## Troubleshooting

### Common Issues

1. **Model Won't Load**
   - Check file path and permissions
   - Verify STL file format
   - Ensure CORS headers are set
   - Check browser console for errors

2. **Performance Issues**
   - Reduce model complexity
   - Close other browser tabs
   - Update graphics drivers
   - Try a different browser

3. **Controls Not Working**
   - Check for JavaScript errors
   - Verify Three.js library loaded
   - Ensure WebGL is enabled
   - Check for conflicting scripts

4. **Mobile Issues**
   - Check touch event support
   - Verify responsive design
   - Test on different devices
   - Check orientation changes

### Debug Information

Enable debug mode by adding `?debug=true` to the URL to see:
- Model loading status
- Performance metrics
- Error messages
- Viewer configuration

## Future Enhancements

### Planned Features
- **Animation Support**: Skeletal animation for moving parts
- **VR/AR Integration**: Immersive viewing experiences
- **Collaboration Tools**: Multi-user viewing and annotation
- **Advanced Materials**: Realistic material rendering
- **Audio Integration**: Period-appropriate sound effects

### Technical Improvements
- **WebGL2 Optimization**: Advanced rendering techniques
- **WebAssembly**: Performance-critical calculations
- **Service Workers**: Offline viewing capability
- **CDN Integration**: Global content delivery
- **Analytics**: Usage tracking and optimization

## Contributing

### Development Setup
1. Install Node.js and npm
2. Clone the repository
3. Install dependencies with `npm install`
4. Run development server with `npm run dev`
5. Build for production with `npm run build`

### Code Standards
- Use ESLint for JavaScript linting
- Follow Prettier formatting rules
- Write comprehensive tests
- Document all public APIs
- Ensure accessibility compliance

### Testing
- Unit tests for core functionality
- Integration tests for viewer workflows
- Performance testing on various devices
- Accessibility testing with screen readers
- Cross-browser compatibility testing

## License

This 3D Viewer System is part of the da Vinci Codex project and is licensed under the same terms as the main project. Please refer to the main repository for license information.

## Support

For technical support, feature requests, or bug reports:
- **Issues**: Create an issue on the GitHub repository
- **Documentation**: Check this guide and inline comments
- **Community**: Join discussions in the repository forums
- **Email**: Contact the development team directly

---

*This documentation is part of the da Vinci Codex project, bringing Leonardo's engineering genius to life through modern technology.*