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
