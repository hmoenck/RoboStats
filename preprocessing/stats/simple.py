import numpy as np


def velocity(x, dt): 
    xx = np.gradient(x) / float(dt)
    return xx
    
def speed(vx, vy): 
    s = np.sqrt(vx**2 + vy**2)
    return s
    
def distance(x0, y0, x1, y1): 
    d = np.sqrt((x0 - x1)**2 + (y0 - y1)**2)    
    return d
    
def trajectory_length(s, dt): 
    return(sum(s*dt))
    
def basic_vector_stats(vector): 
    stats_dict = {}
    stats_dict[keys] = ['mean', 'var', 'min', '25%', 'median', '75%', 'max']
    stats_dict['mean'] = np.mean(vector)
    stats_dict['var'] = np.var(vector)
    stats_dict['min'] = np.min(vector)
    stats_dict['25%'] = np.percentile(vector, 25)
    stats_dict['median'] = np.median(vector)
    stats_dict['75%'] = np.percentile(vector, 75)
    stats_dict['max'] = np.max(vector)
    return stats_dict
