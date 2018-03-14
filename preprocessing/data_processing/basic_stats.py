import numpy as np
import pandas as pd
from collections import Counter
import json
from scipy.stats import mode
import stats.simple as simple


def speed_and_dist(filename, info, csv_info_file, param_info_file): 
    '''This function gets called by the ok button in tableWindow. It calculates seconds from the chosen 
    time format, velocity and speed of each agent and the distance between agent pairs. The results 
    are saved in a temporary file. '''
    
    # what to calculate 
    INDIVIDUAL_STATS = ['_vx', '_vy', '_speed']
    COLLECTIVE_STATS = ['_dist']
    
    # deliminater for the resulting csv
    csv_info = json.load(open(csv_info_file))
    delim = csv_info['write']['delim']
    
    # get the time format
    data_info = json.load(open(param_info_file))
    time_format = data_info['info']['time']
    
    #read csv to pandas
    df = pd.read_csv(filename, header = 0, sep = delim)
    df_new = df
    
    # use the timeformat of the data to create a column called 'seconds'
    seconds, DT, FPS = get_seconds_from_time(df['time'].values, time_format)
    df_new['seconds'] = seconds
    
    # calculate speed and velocity
    for i, an in enumerate(info['agent_names']): 
        df_new[an + '_vx'] = simple.velocity(df[an + '_x'].values, DT)
        df_new[an + '_vy'] = simple.velocity(df[an + '_y'].values, DT)
        df_new[an + '_speed'] = simple.speed(df_new[an + '_vx'].values, df_new[an + '_vy'].values)
    
    # calculate distance between agent pairs
        for j, bn in enumerate(info['agent_names']): 
            if j >= i+1: 
                df_new[an + '/' + bn + '_dist'] = simple.distance(df[an+'_x'].values, df[an+'_y'].values, df[bn+'_x'].values, df[bn+'_y'].values)
    
    # save dataframe  
    df_new.to_csv(filename, sep = delim)


def cut_timelines(filename, info, csv_info_file):  

    csv_info = json.load(open(csv_info_file))
    delim = csv_info['write']['delim']
    
    df = pd.read_csv(filename, header = 0, sep = delim)
    df_new = df
    
    idx_min = np.where(df['frames'].values == info['start_frame'])[0][0]
    idx_max = np.where(df['frames'].values == info['stop_frame'])[0][0]   
    df_new = time_slicer(df, idx_min, idx_max)
    
    df_new = space_slicer(df_new, info['agent_names'], info['x_min'], info['x_max'], info['y_min'], info['y_max'])
    
    return df_new


def time_slicer(df, t_min, t_max): 
    df_new = df.loc[t_min : t_max]
    return df_new


def space_slicer(df, agent_names, x_min, x_max, y_min, y_max): 
    df_new = df
    idx = []
    for an in agent_names:
        x = df_new[an + '_x'].values
        y = df_new[an + '_y'].values
        for i in range(len(x)): 
            if x[i] < x_min or x[i] > x_max: 
                idx.append(i)
            if y[i] < y_min or y[i] > y_max: 
                idx.append(i)
    idx = list(set(idx)) # eliminate multiple indices
#    print('I space cut these inidces:', idx)
#    print('this corresponds to frames: ', df_new['frames'].values[idx])
    df_new = df_new.drop(df_new.index[idx])
    return df_new 


def get_seconds_from_time(timestamps, time_format): 
    '''this function takes the vector of timestamps from the original file and the corresponding time format and 
    calculates the corresponding vector in seconds (starting from 0)as well as frames per second (FPS) and its inverse DT = 1/FPS'''

    if time_format == 'dt': #datetime format up to seconds precision
        print('convert dt to s ')

        c = np.array(list(Counter(timestamps).values())) # count how often the same timestamp appears
        FPS = mode(c)[0][0]
        DT = 1./FPS
        seconds = np.arange(0., len(timestamps)*DT, DT)
        seconds = seconds[:len(timestamps)]
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
        
    
        
        

