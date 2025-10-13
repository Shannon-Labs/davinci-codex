
# Viola Organista - Keyboard Assembly
# Standard keyboard with mechanical action

def create_keyboard_assembly():
    # Keyboard specifications
    keyboard = {
        'type': 'Standard organ keyboard',
        'number_of_keys': 45,  # 3.75 octaves
        'key_material': 'Ebony and ivory',
        'key_spacing': 'Standard octave spacing'
    }

    # Action mechanism
    action = {
        'type': 'Mechanical direct action',
        'connection': 'Keys connect to bow wheels',
        'depth': 'Moderate key depth for control',
        'weight': 'Balanced for responsive touch'
    }

    return {
        'keyboard': keyboard,
        'action': action,
        'range': 'F2 to C6'
    }
