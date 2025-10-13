
# Viola Organista - Main Assembly
# Complete instrument assembly

def create_main_assembly():
    # Main structure
    structure = {
        'type': 'keyboard/string',
        'materials': ['soundboard', 'strings', 'keyboard', 'bow_wheels'],
        'dimensions': {'length': 2.2, 'width': 0.8, 'height': 1.0, 'string_count': 32}
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
        'complexity': 10
    }
