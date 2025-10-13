
# Automatic Pipe Organ - Organ Pipes
# Set of tuned organ pipes

def create_organ_pipes():
    # Pipe specifications
    num_pipes = 48
    pipes = []

    for i in range(num_pipes):
        pipe = {
            'length': 0.5 + i * 0.1,  # Progressive length
            'diameter': 0.05,
            'material': 'Lead and tin alloy',
            'frequency': 110 * (2 ** (i/12)),  # Chromatic scale
            'type': 'Open flute pipe'
        }
        pipes.append(pipe)

    return {
        'pipes': pipes,
        'voicing': 'Traditional Renaissance voicing',
        'tuning': 'Adjustable sliders in pipe feet'
    }
