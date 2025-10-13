
# Leonardo's Mechanical Lion - Leg Linkage System
# Complete mechanical linkage for four-legged walking

def create_leg_linkage_system():
    # Primary linkages (cam to leg)
    primary_linkages = {
        'type': 'Four-bar linkage mechanism',
        'material': 'Bronze with steel pins',
        'lengths': {
            'input_arm': 0.15,  # Connected to cam follower
            'coupling_arm': 0.25,  # Connects input to output
            'output_arm': 0.2,   # Connected to leg
            'ground_arm': 0.3    # Fixed frame connection
        },
        'function': 'Convert rotary cam motion to leg motion'
    }

    # Secondary linkages (leg articulation)
    secondary_linkages = {
        'knee_joint': {
            'type': 'Pin joint with bronze bearing',
            'range_of_motion': 120,  # degrees
            'spring_assist': 'Return spring for stance phase'
        },
        'ankle_joint': {
            'type': 'Flexible bronze strap',
            'function': 'Natural paw movement',
            'material': 'Tempered bronze strip'
        }
    }

    # Spring system
    springs = {
        'leg_return': {
            'type': 'Tension spring',
            'constant': 500.0,
            'function': 'Return leg to neutral position'
        },
        'weight_support': {
            'type': 'Compression spring',
            'constant': 1000,
            'function': 'Support body weight during swing phase'
        }
    }

    return {
        'primary_linkages': primary_linkages,
        'secondary_linkages': secondary_linkages,
        'springs': springs,
        'coordination': 'Phase-synchronized for natural gait'
    }
