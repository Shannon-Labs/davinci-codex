
# Leonardo's Mechanical Lion - Chest Reveal Doors
# Bi-fold doors with spring opening mechanism

def create_chest_doors():
    # Door construction
    doors = {
        'type': 'Bi-fold design',
        'material': 'Oak with gilded bronze exterior',
        'dimensions': {
            'width': 0.4,
            'height': 0.6,
            'thickness': 0.03
        },
        'construction': 'Frame and panel with decorative molding'
    }

    # Hinge system
    hinges = {
        'type': 'Concealed bronze hinges',
        'material': 'Bronze with steel pins',
        'location': 'Top and bottom of doors',
        'finish': 'Polished bronze'
    }

    # Opening mechanism
    mechanism = {
        'type': 'Spring-loaded with cam release',
        'springs': {
            'constant': 150.0,
            'type': 'Constant force springs',
            'quantity': 2
        },
        'release': 'Cam-activated latch release'
    }

    return {
        'doors': doors,
        'hinges': hinges,
        'mechanism': mechanism,
        'operation': 'Rapid opening when triggered by cam'
    }
