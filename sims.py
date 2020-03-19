

def get_sim_for(config):
    sim_type = config['DEFAULT']['sim_type']

    if sim_type == 'SandSim':
        from sandsim import SandSim
        sim = SandSim(config['SandSim'])
    else:
        raise ValueError('Unknown Simulation type: %s' % sim_type)
    return sim
