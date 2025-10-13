
# Mechanical Ensemble - Generic Body Model
# Main instrument body structure

def create_generic_body():
    # Body dimensions
    body = {
        'width': 2.5,
        'height': 2.0,
        'depth': 1.8,
        'material': 'Oak and walnut'
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
