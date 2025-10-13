
# Leonardo's Mechanical Lion - Body Frame
# Parametric model for oak construction


# Parameters
body_length = 2.4
body_height = 1.2
body_width = 0.8
frame_thickness = 0.05  # 5cm oak beams

# Main frame structure
def create_body_frame():
    # Longitudinal beams (oak)
    longitudinal_beams = [
        {'length': body_length, 'position': (0, body_width/2, 0)},
        {'length': body_length, 'position': (0, -body_width/2, 0)}
    ]

    # Transverse ribs
    transverse_ribs = []
    num_ribs = int(body_length / 0.3)  # Rib every 30cm
    for i in range(num_ribs):
        x_pos = i * (body_length / (num_ribs - 1))
        transverse_ribs.append({
            'length': body_width,
            'position': (x_pos, 0, 0)
        })

    # Vertical supports
    vertical_supports = [
        {'height': body_height, 'position': (0.2, body_width/2 - 0.1, 0)},
        {'height': body_height, 'position': (0.2, -body_width/2 + 0.1, 0)},
        {'height': body_height, 'position': (body_length - 0.2, body_width/2 - 0.1, 0)},
        {'height': body_height, 'position': (body_length - 0.2, -body_width/2 + 0.1, 0)}
    ]

    return {
        'longitudinal_beams': longitudinal_beams,
        'transverse_ribs': transverse_ribs,
        'vertical_supports': vertical_supports,
        'material': 'Oak',
        'construction': 'Mortise and tenon joints'
    }

# Assembly instructions
frame_parts = create_body_frame()
