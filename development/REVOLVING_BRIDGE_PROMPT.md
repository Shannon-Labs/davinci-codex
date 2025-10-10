# Revolving Bridge Implementation Prompt

## Task
Implement Leonardo da Vinci's revolving bridge design as a new invention module in the da Vinci Codex project. This portable bridge was designed to allow armies to cross rivers quickly, but we'll adapt it for modern civil engineering and emergency response applications.

## Historical Context
- **Original Source**: Codex Atlanticus, folio 855r (circa 1480-1490)
- **Purpose**: A swing bridge that could be quickly deployed by rotating on a central pivot
- **Key Innovation**: No permanent foundation required - self-supporting through counterweights
- **da Vinci's Design**: Used rope and pulley system with a balanced beam that could rotate 90 degrees

## Implementation Requirements

### 1. Create the module file
Create `src/davinci_codex/inventions/revolving_bridge.py` with:
- SLUG = "revolving_bridge"
- TITLE = "Self-Supporting Revolving Bridge"
- STATUS = "planning" (initially)
- SUMMARY = "Portable rotating bridge with counterweight balance for rapid deployment"

### 2. Implement required functions

#### plan()
Should include:
- Folio reference to Codex Atlanticus 855r
- Original obstacles (materials, precise balance calculations)
- Modern assumptions:
  - Span length: 12 meters
  - Load capacity: 5000 kg (emergency vehicles)
  - Rotation time: < 2 minutes
  - Materials: Steel truss with composite decking
  - Counterweight system using water-fillable tanks
- Governing equations:
  - Moment balance: M_bridge = M_counterweight
  - Structural deflection: δ = (5WL^4)/(384EI)
  - Rotation torque: T = I * α (angular acceleration)

#### simulate(seed=0)
Should calculate and visualize:
- Stress distribution during rotation at different angles (0°, 45°, 90°)
- Dynamic stability analysis during rotation
- Load capacity vs. span length curves
- Animation of bridge rotation sequence
- CSV output with structural parameters at each rotation angle

#### build()
Generate parametric CAD model (`cad/revolving_bridge/model.py`):
- Truss structure with parametric span and height
- Central pivot mechanism with bearing specifications
- Counterweight tanks with adjustable volume
- Deck surfacing compatible with emergency vehicles
- Export as STL mesh for 3D printing scaled model

#### evaluate()
Safety and feasibility analysis:
- Maximum safe wind speed during operation
- Factor of safety for structural members (target > 3.0)
- Deployment time vs. traditional temporary bridges
- Cost comparison with Bailey bridges
- Emergency response scenarios (flood, earthquake, military)

### 3. Create tests
Write `tests/test_revolving_bridge.py`:
- Test moment balance calculations
- Verify rotation completes within time limit
- Check structural safety factors
- Validate artifact generation

### 4. Add documentation
Create `docs/revolving_bridge.md`:
- Link to digitized Codex Atlanticus folio
- Modern engineering adaptations
- Deployment procedures
- Safety protocols for operators
- Case studies: Venice acqua alta, disaster relief

### 5. Key Engineering Considerations

#### Structural
- Use Warren truss design for optimal strength-to-weight
- High-strength steel (ASTM A992) for main members
- Composite FRP decking to reduce dead load
- Redundant load paths for critical connections

#### Mechanical
- Slewing bearing rated for 150% of maximum moment
- Hydraulic rotation system with manual backup
- Automatic locking pins at 0° and 90° positions
- Anti-slip surface treatment on deck

#### Counterweight System
- Water-fillable tanks for adjustable balance
- Automatic pumping system to maintain equilibrium
- Drainage capability for transport mode
- Freeze protection for cold climates

### 6. Validation Metrics
- Rotation achievable with < 10 kW power source
- Deployment by 2-person crew in under 30 minutes
- Support 40-ton emergency vehicle at midspan
- Withstand 100 km/h wind loads when locked

## Expected Deliverables
1. Fully functional Python module following project conventions
2. Parametric CAD model exportable to STL
3. Performance curves and structural analysis plots
4. Animation of bridge rotation sequence
5. Comprehensive safety evaluation
6. All tests passing with `make test`

## Notes for Implementation
- Focus on civil emergency applications, not military
- Emphasize rapid deployment for disaster relief
- Include modern safety features (railings, lighting mounts)
- Consider modular design for different span requirements
- Document how modern materials solve da Vinci's original challenges

This invention beautifully demonstrates da Vinci's understanding of mechanical advantage and structural balance, updated with modern engineering to create a practical emergency infrastructure solution.