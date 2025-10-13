
# Leonardo's Mechanical Lion - Reveal Cam
# Triggers chest reveal mechanism

def create_reveal_cam():
    # Cam specifications
    cam = {
        'base_radius': 0.15,
        'lift_height': 0.15,
        'material': 'Hardened bronze',
        'surface_finish': 'Polished for smooth follower movement'
    }

    # Profile definition
    profile = {
        'type': 'Step function',
        'duration': 360,
        'trigger_point': 270,
        'function': 'Triggers chest reveal mechanism'
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
