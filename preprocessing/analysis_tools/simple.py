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
    
#def trajectory_length(s, dt): 
#    '''calculates total length of trajectory from speed and dt '''
#    return(sum(s*dt))
    
def trajectory_length(x, y): 
    '''calculates the length of agents trajectory from x and y position vector'''    
    xx = np.diff(x)
    yy = np.diff(y)

    tra = np.sum(np.sqrt(xx**2 + yy**2))
    return tra    
    
def time_close(dist, max_dist, dt, percent = False):
    '''calculates the amount of time two agents were closer than a given threshold. 
    If percent = True instead of absolute time the percentage is calculated'''
    if len(dt) > 1: 
        dt = np.mean(dt)
    time_close = len(dist[dist < max_dist])*dt
    
    if percent: 
        time_total = len(dist)*dt
        time_close /= time_total
        
    return time_close    

    
def basic_vector_stats(vector): 
    stats_dict = {}
    stats_dict['keys'] = ['mean', 'var', 'min', '25%', 'median', '75%', 'max']
    stats_dict['mean'] = np.mean(vector)
    stats_dict['var'] = np.var(vector)
    stats_dict['min'] = np.min(vector)
    stats_dict['25%'] = np.percentile(vector, 25)
    stats_dict['median'] = np.median(vector)
    stats_dict['75%'] = np.percentile(vector, 75)
    stats_dict['max'] = np.max(vector)
    return stats_dict
