
# Leonardo's Mechanical Lion - Gait Cam
# Controls walking gait sequence

def create_gait_cam():
    # Cam specifications
    cam = {
        'base_radius': 0.15,
        'lift_height': 0.1,
        'material': 'Hardened bronze',
        'surface_finish': 'Polished for smooth follower movement'
    }

    # Profile definition
    profile = {
        'type': 'Sinusoidal with plateaus',
        'duration': 360,
        'trigger_point': None,
        'function': 'Controls walking gait sequence'
    }

    # Manufacturing notes
    manufacturing = {
        'method': 'Precision machining on wooden template',
        'tolerance': '±0.1mm on profile',
        'finish': 'Hand-polished to mirror finish',
        'hardening': 'Case hardened for wear resistance'
    }

    return {
        'cam': cam,
        'profile': profile,
        'manufacturing': manufacturing
    }
