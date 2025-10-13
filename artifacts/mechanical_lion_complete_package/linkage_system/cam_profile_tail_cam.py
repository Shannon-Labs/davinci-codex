
# Leonardo's Mechanical Lion - Tail Cam
# Controls tail movement

def create_tail_cam():
    # Cam specifications
    cam = {
        'base_radius': 0.15,
        'lift_height': 0.05,
        'material': 'Hardened bronze',
        'surface_finish': 'Polished for smooth follower movement'
    }

    # Profile definition
    profile = {
        'type': 'Gentle sinusoid',
        'duration': 360,
        'trigger_point': None,
        'function': 'Controls tail movement'
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
