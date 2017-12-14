import numpy as np
import pandas as pd




def basic_stats(data, info): 
    #TODO Still this expects pretty specific data format
    
    # expects data to come as a pandas df. with columns: 
    # [time, x0, y0, x1, y1, v_x0, v_y0, v_x1, v_y1, d]
    # info is supposed to be a dict, with entries: 
    # {'start_time': t0, 'stop_time':t1, 'agent1' : True }
    
    t0 = info['start_time']
    t1 = info['stop_time']
    
    agent_idx = []
    for key in info: # find out which agents were activted and retrieve their indices
        if key.find('agent') >= 0 and info[key] == True:
            idx = key[key.find('_')+1:]
            agent_idx.append(idx)
            
    for idx in agent_idx: 
        speed = np.sqrt((data['v_x'+ idx])**2 + (data['v_y'+ idx])**2)
        info['mean_speed_' + idx] = np.mean(speed[t0:t1])
        info['std_speed_' + idx] = np.sqrt(np.var(speed[t0:t1]))
        
    info['mean_dist'] = np.mean(data['d'].values[t0:t1])
    info['std_dist'] = np.sqrt(np.var(data['d'][t0:t1]))

    return info
