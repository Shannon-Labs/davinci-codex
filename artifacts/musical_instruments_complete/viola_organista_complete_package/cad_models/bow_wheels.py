
# Viola Organista - Bow Wheels
# Rotating bow wheels for string excitation

def create_bow_wheels():
    # Wheel specifications
    wheels = []
    num_wheels = 4

    for _i in range(num_wheels):
        wheel = {
            'diameter': 0.15,
            'width': 0.02,
            'material': 'Horsehair on wooden wheel',
            'rotation_speed': 'Variable by key pressure',
            'rosin': 'Colophony rosin for grip'
        }
        wheels.append(wheel)

    # Operating mechanism
    mechanism = {
        'actuation': 'Key-driven mechanical linkage',
        'pressure': 'Variable contact pressure',
        'engagement': 'Wheel rises to contact string',
        'timing': 'Synchronized with key action'
    }

    return {
        'wheels': wheels,
        'mechanism': mechanism
    }
