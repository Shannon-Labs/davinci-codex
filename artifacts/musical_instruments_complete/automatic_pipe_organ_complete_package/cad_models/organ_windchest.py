
# Automatic Pipe Organ - Organ Windchest
# Air distribution system for organ pipes

def create_organ_windchest():
    # Windchest dimensions
    windchest = {
        'length': 2.0,
        'width': 1.0,
        'height': 0.5,
        'material': 'Oak'
    }

    # Internal structure
    internal = {
        'channels': 'Individual wind channels for each pipe',
        'valves': 'Pallet valves for note activation',
        'pressure': '2-3 inches water column',
        'regulation': 'Balance bar for pressure control'
    }

    return {
        'windchest': windchest,
        'internal': internal
    }
