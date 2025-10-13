
# Leonardo's Mechanical Lion - Cam Followers
# Follower system for all cam tracks

def create_cam_followers():
    # Follower design
    followers = {
        'type': 'Roller followers with bronze wheels',
        'wheel_diameter': 0.04,  # 4cm diameter
        'axle_material': 'Steel with bronze bushings',
        'spring_load': 'Constant force spring'
    }

    # Follower arms
    arms = {
        'material': 'Bronze',
        'length': 0.25,  # 25cm from pivot to cam
        'pivot': 'Bronze bearing with minimal friction'
    }

    # Return springs
    springs = {
        'type': 'Constant force springs',
        'force': 50,  # N
        'function': 'Maintain contact with cam profile'
    }

    return {
        'followers': followers,
        'arms': arms,
        'springs': springs,
        'operation': 'Continuous contact with cam profiles'
    }
