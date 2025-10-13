
# Mechanical Drum - Generic Body Model
# Main instrument body structure

def create_generic_body():
    # Body dimensions
    body = {
        'width': 1.0,
        'height': 1.2,
        'depth': 0.4,
        'material': 'Maple or oak'
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
