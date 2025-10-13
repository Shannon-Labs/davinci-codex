
# Viola Organista - Soundboard Model
# Vibrating soundboard with string arrangement

def create_soundboard_model():
    # Soundboard specifications
    soundboard = {
        'length': 2.2,
        'width': 0.8,
        'thickness': 0.01,
        'material': 'Spruce',
        'curvature': 'Slight crown for optimal vibration'
    }

    # String arrangement
    strings = {
        'number': 32,
        'spacing': 'Equal spacing across soundboard',
        'tension': 'Variable by note',
        'material': 'Gut and metal strings'
    }

    return {
        'soundboard': soundboard,
        'strings': strings,
        'bridges': 'Two bridges for string support'
    }
