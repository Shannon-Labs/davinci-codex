
# Mechanical Carillon - Main Assembly
# Complete instrument assembly

def create_main_assembly():
    # Main structure
    structure = {
        'type': 'percussion',
        'materials': ['bells', 'frame', 'hammers', 'mechanism'],
        'dimensions': {'height': 3.0, 'width': 1.5, 'depth': 1.2, 'bell_diameter_range': (0.3, 0.8)}
    }

    # Assembly sequence
    sequence = [
        '1. Construct main frame/body',
        '2. Install sound production components',
        '3. Add mechanical control systems',
        '4. Install tuning mechanisms',
        '5. Add decorative elements',
        '6. Final assembly and testing'
    ]

    return {
        'structure': structure,
        'sequence': sequence,
        'complexity': 7
    }
