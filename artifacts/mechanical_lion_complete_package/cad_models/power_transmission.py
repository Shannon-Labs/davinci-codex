
# Leonardo's Mechanical Lion - Power Transmission
# Spring-powered drive system with gear reduction

def create_power_transmission():
    # Main power spring
    power_spring = {
        'type': 'Flat spiral spring',
        'material': 'High-carbon spring steel',
        'energy_storage': '5000 Joules',
        'torque_output': '50 Nm at full wind'
    }

    # Winding mechanism
    winding = {
        'type': 'Crank and ratchet system',
        'gear_ratio': 15.0,
        'winding_time': '5 minutes full wind',
        'safety': 'Overwind protection clutch'
    }

    # Gear train
    gears = {
        'material': 'Bronze with iron pinions',
        'ratios': [3.0, 5.0, 2.0],  # Total 30:1 reduction
        'construction': 'Spur gears with wooden hubs',
        'bearings': 'Bronze sleeve bearings'
    }

    # Clutch system
    clutch = {
        'type': 'Friction clutch with bronze plates',
        'control': 'Lever-operated engagement',
        'safety': 'Emergency disengagement possible'
    }

    return {
        'power_spring': power_spring,
        'winding': winding,
        'gears': gears,
        'clutch': clutch,
        'output': 'Continuous rotation to cam drum'
    }
