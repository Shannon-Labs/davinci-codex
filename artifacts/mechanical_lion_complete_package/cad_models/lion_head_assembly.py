
# Leonardo's Mechanical Lion - Head Assembly
# Articulated head with moving jaw

def create_head_assembly():
    # Main head structure
    head = {
        'length': 0.6,
        'width': 0.5,
        'height': 0.4,
        'material': 'Oak with bronze accents',
        'construction': 'Carved oak with decorative bronze trim'
    }

    # Jaw mechanism
    jaw = {
        'length': 0.4,
        'movement': 'Hinged at rear with spring return',
        'actuation': 'Cam-driven from main drum',
        'material': 'Bronze hinges and springs'
    }

    # Eyes (decorative)
    eyes = {
        'type': 'Glass or polished stone',
        'mounting': 'Bronze settings',
        'expression': 'Fierce and lifelike'
    }

    return {
        'head': head,
        'jaw': jaw,
        'eyes': eyes,
        'assembly': 'Modular attachment to body frame'
    }
