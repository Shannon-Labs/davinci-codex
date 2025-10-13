
# Leonardo's Mechanical Lion - Chest Cavity Reveal Mechanism
# Spring-loaded doors with fleur-de-lis display

# Parameters
chest_width = 0.8
chest_height = 0.6
chest_depth = 0.4
spring_constant = 150.0

def create_chest_cavity():
    # Main chest cavity
    cavity = {
        'width': chest_width,
        'height': chest_height,
        'depth': chest_depth,
        'material': 'Oak with bronze trim',
        'construction': 'Frame and panel construction'
    }

    # Bi-fold doors
    doors = {
        'type': 'Bi-fold',
        'material': 'Oak with gilded bronze exterior',
        'hinges': 'Decorative bronze hinges',
        'opening_mechanism': 'Spring-loaded with cam release',
        'spring': f'{spring_constant} N/m constant force spring'
    }

    # Latching mechanism
    latch = {
        'type': 'Cam-activated release',
        'material': 'Bronze',
        'trigger': 'Cam follower from main drum',
        'safety': 'Secondary manual release'
    }

    # Fleur-de-lis display
    display = {
        'type': 'Mechanical pop-up',
        'material': 'Gilded bronze',
        'mechanism': 'Spring-loaded articulated display',
        'presentation': 'Rises from chest cavity when doors open'
    }

    return {
        'cavity': cavity,
        'doors': doors,
        'latch': latch,
        'display': display,
        'operation': 'Cam trigger at end of walking sequence'
    }
