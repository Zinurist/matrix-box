

def get_sim_for(config):
    sim_type = config['DEFAULT']['sim_type']

    if sim_type == 'SandSim':
        from sandsim import SandSim
        sim = SandSim(config['SandSim'])
    elif sim_type == 'ArrowSim':
        from arrowsim import ArrowSim
        sim = ArrowSim(config['ArrowSim'])
    else:
        raise ValueError('Unknown Simulation type: %s' % sim_type)
    return sim
