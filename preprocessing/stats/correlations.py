import numpy as np
from scipy.stats import spearmanr
from scipy.stats import pearsonr


#def relVel(x0 ,y0, vx0, vy0, x1, y1, vx1, vy1):
#    '''calculates scalar product between an agents velocity and their normalized distance. 
#    It can be positive (distance grows) or negative (distance decreases)'''
#    rel_x = x0 - x1
#    rel_y = y0 - y1
#    dist = np.sqrt(rel_x**2 + rel_y**2)
#    u_rel_x = rel_x / dist
#    u_rel_y = rel_y /dist
#    
#    relvel0 = vx0*u_rel_x + vy0*u_rel_y
#    relvel1 = vx1*u_rel_x + vy1*u_rel_y
#    
#    return relvel0, relvel1

#def correlation_relative_velocity(relvel0, relvel1, s0, s1, corr = 'Pearson'):
#    ''' point of refrence = agent 0 '''
#    
#    relvel = relvel0-relvel1

#    if corr == 'Pearson': 
#        rho0, p0 = pearsonr(relvel, s0)
#        rho1, p1 = pearsonr(relvel, s1)
#        
#    elif corr == 'Spearman': 
#        rho0, p0 = spearmanr(relvel, s0)
#        rho1, p1 = spearmanr(relvel, s1)
#        
#    return rho0, p0, rho1, p1


#def calc_xcorr(x,y,normed=True,maxlags=None):
#    """ Calculate time lagged cross-correlation
#        the input of y[i] is shifted according to y[i+shift] 
#        with shift from -mlags to +mlags
#        ---- taken from : AnalyzeFish.py
#    """
#    c=np.correlate(x,y,mode=2)
#    if(normed==True):
#        c/=np.sqrt(np.dot(x,x)*np.dot(y,y));

#    datl=np.min([len(x),len(y)])
#    lags=np.arange(1,2*datl)-datl

#    if(maxlags is not None):
#        tlags=int(len(lags)/2)
#        if(maxlags<tlags):
#            lags=lags[tlags-maxlags:tlags+maxlags+1]
#            c=c[tlags-maxlags:tlags+maxlags+1]

#    return lags,c

def distance(agent0_x, agent0_y, agent1_x, agent1_y, plot= False): 
    rel_x = agent0_x - agent1_x
    rel_y = agent0_y - agent1_y
    dist = np.sqrt(rel_x**2 + rel_y**2)
    u_rel_x = rel_x / dist
    u_rel_y = rel_y /dist
#    if plot: 
#        plot_timeline([dist], ['distance'], 'frames', 'distance', 'distance.png')        
    return dist, rel_x, rel_y, u_rel_x, u_rel_y
    
def relVel(agent0_vx, agent0_vy, agent1_vx, agent1_vy, u_rel_x, u_rel_y): 
    relvel0 = agent0_vx*u_rel_x + agent0_vy*u_rel_y
    relvel1 = agent1_vx*u_rel_x + agent1_vy*u_rel_y
    relvel = relvel0-relvel1
    return relvel

def my_pearson(data0, data1): 
    rho, p = pearsonr(data0,data1)
    return  rho, p

def my_spearmanr(data0, data1): 
    rho, p = spearmanr(data0, data1)
    return  rho, p
    
def correlation_relative_velocity(x0 ,y0, vx0, vy0, x1, y1, vx1, vy1, corr = 'Pearson'):
    ''' point of refrence = agent 0 '''
    dist, rel_x, rel_y, u_rel_x, u_rel_y = distance(x0, y0, x1, y1)
    relvel = relVel(vx0, vy0, vx1, vy1, u_rel_x, u_rel_y)
    
    s0 = np.sqrt(vx0**2 + vy0**2)
    s1 = np.sqrt(vx1**2 + vy1**2)

    if corr == 'Pearson': 
        rho0, p0 = my_pearson(relvel, s0)
        rho1, p1 = my_pearson(relvel, s1)
        
    elif corr == 'Spearman': 
        rho0, p0 = my_spearmanr(relvel, s0)
        rho1, p1 = my_spearmanr(relvel, s1)
        
    return rho0, p0, rho1, p1
