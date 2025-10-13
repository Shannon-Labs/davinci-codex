
# Leonardo's Mechanical Carillon - Hammer Mechanism
# Cam-driven hammer system with velocity control

def create_hammer_mechanism():
    # Cam drum system
    cam_drum = {
        'diameter': 0.4,
        'length': 1.2,
        'material': 'Bronze and iron',
        'cam_profiles': 'Programmable wooden cams with metal followers'
    }

    # Hammer assemblies
    hammers = []
    for _i in range(8):
        hammer = {
            'head_material': 'Hardwood ',
            'striking_surface': ' leather striking surfaces',
            'arm_length': 0.3,
            'pivot_type': 'Bronze bearing with minimal friction',
            'return_spring': 'Tempered steel spring',
            'velocity_control': 'Cam profile determines strike velocity'
        }
        hammers.append(hammer)

    # Timing system
    timing = {
        'drive_source': 'Weight-driven clock mechanism',
        'tempo_control': 'Adjustable pendulum regulator',
        'programming': 'Interchangeable cam cylinders'
    }

    return {
        'cam_drum': cam_drum,
        'hammers': hammers,
        'timing': timing,
        'articulation': 'Dynamic control for musical expression'
    }
