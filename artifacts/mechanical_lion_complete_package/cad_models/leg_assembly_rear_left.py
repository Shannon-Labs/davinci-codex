
# Leonardo's Mechanical Lion - Rear Left Leg Assembly
# Cam-driven walking mechanism

# Parameters
leg_length = 0.6
phase_offset = 0.5
cam_drum_radius = 0.15
spring_constant = 500.0

def create_leg_assembly():
    # Upper leg (thigh)
    upper_leg = {
        'length': leg_length * 0.5,
        'material': 'Bronze',
        'construction': 'Cast and machined',
        'mounting': 'Hip joint with bronze bearing'
    }

    # Lower leg (calf)
    lower_leg = {
        'length': leg_length * 0.5,
        'material': 'Bronze',
        'construction': 'Cast and machined',
        'joint': 'Knee joint with pin'
    }

    # Cam follower
    cam_follower = {
        'radius': 0.02,
        'material': 'Hardened steel',
        'spring': f'{spring_constant} N/m return spring'
    }

    # Paw mechanism
    paw = {
        'material': 'Bronze with leather pad',
        'articulation': 'Passive flexion',
        'ground_contact': 'Leather pad for grip'
    }

    return {
        'upper_leg': upper_leg,
        'lower_leg': lower_leg,
        'cam_follower': cam_follower,
        'paw': paw,
        'phase_offset': phase_offset,
        'assembly': 'Modular bolted construction'
    }
