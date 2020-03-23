

def get_sim_for(config):
    sim_type = config['DEFAULT']['sim_type']

    if sim_type == 'SandSim':
        from sandsim import SandSim
        sim = SandSim(config['SandSim'])
    elif sim_type == 'StarSim':
        from starsim import StarSim
        sim = StarSim(config['StarSim'])
    elif sim_type == 'DodoSim':
        from dodosim import DodoSim
        sim = DodoSim(config['DodoSim'])
    elif sim_type == 'ArrowSim':
        from arrowsim import ArrowSim
        sim = ArrowSim(config['ArrowSim'])
    elif sim_type == 'CubeSim':
        from cubesim import CubeSim
        sim = CubeSim(config['CubeSim'])
    else:
        raise ValueError('Unknown Simulation type: %s' % sim_type)
    return sim
