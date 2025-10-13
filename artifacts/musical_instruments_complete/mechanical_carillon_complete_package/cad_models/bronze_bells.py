
# Leonardo's Mechanical Carillon - Bronze Bells
# Tuned bells with harmonic overtone control

def create_bronze_bells():
    # Bell specifications
    bells = []
    min_dia, max_dia = 0.15, 0.45  # Bell diameter range in meters

    # Generate 8 bells spanning an octave
    for i in range(8):
        base_freq = 200  # Base frequency in Hz
        frequency = base_freq * (2 ** (i/12))
        diameter = max_dia * (frequency / base_freq) ** -0.5

        bell = {
            'diameter': diameter,
            'height': diameter * 0.8,
            'wall_thickness': diameter * 0.05,
            'material': 'Bronze (20% tin)',
            'fundamental_frequency': frequency,
            'overtones': ['2nd harmonic', '3rd harmonic', 'perfect fifth'],
            'casting_method': 'Lost-wax casting with tuning',
            'finish': 'Hand-polished interior'
        }
        bells.append(bell)

    return {
        'bells': bells,
        'tuning_system': 'Just intonation',
        'harmonic_profile': 'Rich harmonic series with strong fundamentals'
    }
