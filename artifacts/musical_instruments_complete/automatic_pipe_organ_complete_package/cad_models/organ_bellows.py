
# Automatic Pipe Organ - Organ Bellows
# Wind supply system

def create_organ_bellows():
    # Bellows specifications
    bellows = {
        'type': 'Single-fold wedge bellows',
        'material': 'Leather and wood',
        'frame': 'Oak',
        'capacity': '2 cubic feet',
        'pressure': '2-3 inches water column'
    }

    # Operating mechanism
    mechanism = {
        'drive': 'Weight-driven clock mechanism',
        'regulation': 'Centrifugal governor',
        'reservoir': 'Separate wind reservoir',
        'channels': 'Distribution to windchest'
    }

    return {
        'bellows': bellows,
        'mechanism': mechanism
    }
