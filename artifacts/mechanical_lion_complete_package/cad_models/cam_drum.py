
# Leonardo's Mechanical Lion - Cam Drum Programming System
# Bronze cam drum with machined profiles

# Parameters
drum_radius = 0.15
drum_length = 0.8  # 80cm drum length
material = 'Bronze'

def create_cam_drum():
    # Main drum body
    drum_body = {
        'radius': drum_radius,
        'length': drum_length,
        'material': material,
        'construction': 'Cast bronze with machined cam tracks'
    }

    # Cam tracks (3 tracks for different functions)
    cam_tracks = {
        'track_1': {
            'function': 'Walking gait control',
            'profile': 'Sinusoidal lift pattern',
            'amplitude': 0.1,  # 10cm lift
            'period': 360  # One full rotation per step cycle
        },
        'track_2': {
            'function': 'Chest reveal trigger',
            'profile': 'Step function at 270 degrees',
            'trigger_point': 270,  # Degrees of rotation
            'action': 'Release chest latch'
        },
        'track_3': {
            'function': 'Tail movement',
            'profile': 'Gentle sinusoid',
            'amplitude': 0.05,  # 5cm tail sweep
            'phase_offset': 180
        }
    }

    # Mounting hardware
    mounting = {
        'bearing_type': 'Bronze sleeve bearings',
        'shaft_diameter': 0.05,  # 5cm shaft
        'keyway': 'Woodruff key for torque transmission'
    }

    return {
        'drum_body': drum_body,
        'cam_tracks': cam_tracks,
        'mounting': mounting,
        'machining': 'Precision cam profile machining required'
    }
