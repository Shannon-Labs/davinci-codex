
# Programmable Flute - Generic Body Model
# Main instrument body structure

def create_generic_body():
    # Body dimensions
    body = {
        'width': 1.0,
        'height': 1.0,
        'depth': 0.5,
        'material': 'Boxwood or ebony'
    }

    # Construction details
    construction = {
        'method': 'Traditional joinery',
        'finish': 'Linseed oil and wax',
        'reinforcement': 'Internal bracing'
    }

    return {
        'body': body,
        'construction': construction
    }
