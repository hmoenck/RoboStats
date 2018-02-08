import numpy as np
import pandas as pd
from collections import Counter
import settings.default_params as default
import json
from scipy.stats import mode

# when calculating speed or velocity check for  long sequences of zeros, this might indicate measure problems. suggest to omit the respective frames

# build dict with single value stats!

def stats_and_save(filename, info): 

    INDIVIDUAL_STATS = ['_vx', '_vy', '_speed']
    COLLECTIVE_STATS = ['_dist']
    SINGLE_VALUE_STATS = {'order':[]}
    
    csv_info = json.load(open(default.csv_info))
    delim = csv_info['delim_write']
    
    data_info = json.load(open(default.params))
    time_format = data_info['info']['time']

    df = pd.read_csv(filename, header = 0, sep = delim)
    df_new = df
    
    print(df['time'].values)
    # add an additional column in seconds starting from 0
    seconds, DT, FPS = get_seconds_from_time(df['time'].values, time_format)
    df_new['seconds'] = seconds

    for i, an in enumerate(info['agent_names']): 
        df_new[an + '_vx'] = velocity(df[an + '_x'].values, DT)
        df_new[an + '_vy'] = velocity(df[an + '_y'].values, DT)
        df_new[an + '_speed'] = speed(df_new[an + '_vx'].values, df_new[an + '_vy'].values)
        
        for j, bn in enumerate(info['agent_names']): 
            if j >= i+1: 
                df_new[an + '/' + bn + '_dist'] = distance(df[an+'_x'].values, df[an+'_y'].values, df[bn+'_x'].values, df[bn+'_y'].values)
        
        SINGLE_VALUE_STATS['order'].append(an + '_trajectory_legth')
        SINGLE_VALUE_STATS[an + 'tl'] = trajectory_length(df_new[an +'_speed'].values, DT)  
    # slice in time 
    idx_min = np.where(df['frames'].values == info['start_frame'])[0][0]
    idx_max = np.where(df['frames'].values == info['stop_frame'])[0][0]   
    df_new = time_slicer(df, idx_min, idx_max)
    
    # slice in space 
    df_new = space_slicer(df_new, info['agent_names'], info['x_min'], info['x_max'], info['y_min'], info['y_max'])

    return df_new, SINGLE_VALUE_STATS, INDIVIDUAL_STATS, COLLECTIVE_STATS


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
    
def trajectory_length(s, dt): 
    return(sum(s*dt))
    
    
def get_seconds_from_time(timestamps, time_format): 
    '''this function takes the vector of timestamps from the original file and the corresponding time format and 
    calculates the corresponding vector in seconds (starting from 0)as well as frames per second (FPS) and its inverse DT = 1/FPS'''

    if time_format == 'dt': #datetime format up to seconds precision
        print('convert dt to s ')
        c = np.array(list(Counter(timestamps).values())) # count how often the same timestamp appears
        FPS = mode(c)[0][0]
        DT = 1./FPS
        seconds = np.arange(0., len(timestamps)*DT, DT)
        return seconds, DT, FPS
        
    elif time_format == 'ms': 
        print('convert ms to s ')
        seconds = timestamps/1000 
        seconds = seconds - seconds[0]
        c = np.array(list(Counter(np.round(seconds)).values())) #count all appearances of full seconds
        FPS = mode(c)[0][0]
        DT = 1./FPS
        return seconds, DT, FPS
        
    elif time_format == 's': 
        print('convert s to s')
        seconds = timestamps - timestamps[0]
        c = np.array(list(Counter(np.round(seconds)).values())) #count all appearances of full seconds
        FPS = mode(c)[0][0]
        DT = 1./FPS
        return seconds, DT, FPS
        
    
        
        

