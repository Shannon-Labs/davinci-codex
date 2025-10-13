
# Automatic Pipe Organ - Main Assembly
# Complete instrument assembly

def create_main_assembly():
    # Main structure
    structure = {
        'type': 'wind',
        'materials': ['pipes', 'windchest', 'bellows', 'mechanism'],
        'dimensions': {'height': 3.5, 'width': 2.0, 'depth': 1.5, 'number_of_pipes': 48}
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
        'complexity': 9
    }
