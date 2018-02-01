import numpy as np
import pandas as pd
from collections import Counter
import settings.default_params as default


# when calculating speed or velocity check for  long sequences of zeros, this might indicate measure problems. suggest to omit the respective frames


def stats_and_save(filename, info): 

    INDIVIDUAL_STATS = ['_vx', '_vy', '_speed']
    COLLECTIVE_STATS = ['_dist']

    df = pd.read_csv(filename, header = 0, sep = default.csv_delim)
    df_new = df
    
    # calculate speed and distance
    #FPS = np.mean([len(list(group)) for key, group in groupby(df['time'].values)]) #count how often the same time entry appears to find fps
    c = Counter(df['time'].values)
    FPS = np.mean(np.array(list(c.values())))
    print('FPS', FPS)

    
    DT  = 1. / FPS #timedelta is time per frame 
    for i, an in enumerate(info['agent_names']): 
        df_new[an + '_vx'] = velocity(df[an + '_x'].values, DT)
        df_new[an + '_vy'] = velocity(df[an + '_y'].values, DT)
        df_new[an + '_speed'] = speed(df_new[an + '_vx'].values, df_new[an + '_vy'].values)
        
        for j, bn in enumerate(info['agent_names']): 
            if j >= i+1: 
                df_new[an + '/' + bn + '_dist'] = distance(df[an+'_x'].values, df[an+'_y'].values, df[bn+'_x'].values, df[bn+'_y'].values)
    
    # slice in time 
    idx_min = np.where(df['frames'].values == info['start_frame'])[0][0]
    idx_max = np.where(df['frames'].values == info['stop_frame'])[0][0]   
    df_new = time_slicer(df, idx_min, idx_max)
    
    # slice in space 
    df_new = space_slicer(df_new, info['agent_names'], info['x_min'], info['x_max'], info['y_min'], info['y_max'])
    
    return df_new, INDIVIDUAL_STATS, COLLECTIVE_STATS
    #save to csv
    #df_new.to_csv('first_stats.csv')

def time_slicer(df, t_min, t_max): 
    df_new = df.loc[t_min : t_max]
    return df_new

def space_slicer(df, agent_names, x_min, x_max, y_min, y_max): 
    df_new = df
    idx = []
    
    for an in agent_names:
        x = df[an + '_x'].values
        y = df[an + '_y'].values
        for i in range(len(x)): 
            if x[i] < x_min or x[i] > x_max: 
                idx.append(i)
            if y[i] < y_min or y[i] > y_max: 
                idx.append(i)
    idx = list(set(idx)) # eliminate multiple indices
    df_new = df_new.drop(df_new.index[idx])
    return df_new 
    
def velocity(x, dt): 
    xx = np.gradient(x) / float(dt)
    return xx
    
def speed(vx, vy): 
    s = np.sqrt(vx**2 + vy**2)
    return s
    
def distance(x0, y0, x1, y1): 
    d = np.sqrt((x0 - x1)**2 + (y0 - y1)**2)    
    return d
    
#if __name__ == "__main__":

#    FILE_NAME = '/home/claudia/Dokumente/Uni/lab_rotation_FU/pyQt/preprocessing/tmp.csv'
#    INFO = {'start_time': -1, 'start_frame': 8, 'stop_time': 3000, 'stop_frame':3000, 'duration_time': -1, 'duration_frame':-1,
#            'x_min': 20, 'x_max': 70, 'y_min':20, 'y_max': 80, 'filtered': False, 'agent_names':['agent0', 'agent1']}

#    stats_and_save(FILE_NAME, INFO)
    
