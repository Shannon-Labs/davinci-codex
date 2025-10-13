
# Leonardo's Mechanical Lion - Tail Mechanism
# Articulated tail with cam-driven movement

def create_tail_mechanism():
    # Tail segments
    segments = [
        {'length': 0.3, 'diameter': 0.08, 'material': 'Oak'},
        {'length': 0.25, 'diameter': 0.07, 'material': 'Oak'},
        {'length': 0.2, 'diameter': 0.06, 'material': 'Oak'}
    ]

    # Articulation mechanism
    articulation = {
        'type': 'Flexible bronze spine',
        'actuation': 'Cam-driven sine wave motion',
        'amplitude': 0.05,  # 5cm sweep
        'frequency': 'Synchronized with walking'
    }

    # Mounting
    mounting = {
        'location': 'Rear of body frame',
        'bearing': 'Bronze universal joint',
        'spring': 'Return spring for neutral position'
    }

    return {
        'segments': segments,
        'articulation': articulation,
        'mounting': mounting,
        'motion': 'Natural swaying during walking'
    }
