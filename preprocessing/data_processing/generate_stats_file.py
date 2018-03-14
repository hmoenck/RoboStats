import numpy as np
import pandas as pd
from stats.correlations import correlation_relative_velocity
import stats.simple as stats
import json

#def makeFile(folder, csv_file, info, csv_info, file_names, region = 'Main'): 
def makeFile(folder, df, info, csv_info, file_names, region = 'Main'): 

    file_info = json.load(open(file_names))
    INFO_FILE = file_info['info_file']
    name = folder + '/'+ INFO_FILE

    csv_dict = json.load(open(csv_info))
    sep = csv_dict['write']['delim']
    
    distance_thresholds = [5,10,15,20]
    
    with open(name, 'w') as f: 
        
        #df = pd.read_csv(csv_file, header = 0, sep = sep)
        cols = df.columns
        dt = np.gradient(df['seconds'].values)

        data_name = info['data_file'][info['data_file'].rfind('/')+1:]
        f.write('Region,'+ region + '\n')
        f.write('Source,' + data_name + '\n')
        f.write('x_min,' + str(info['x_min']) + '\n')
        f.write('x_max,' + str(info['x_max']) + '\n')
        f.write('y_min,' + str(info['y_min']) + '\n')
        f.write('y_max,' + str(info['y_max']) + '\n')
        
        f.write('start,' + str(info['start_time']) + '\n')
        f.write('stop,' + str(info['stop_time']) + '\n')
        f.write('filtered,' + str(info['filtered']) + '\n')

        # speed results
        for agent in info['agent_names']: 
            
            speed = df[agent + '_speed'].values
            
            # claculate length of trajectory
            trajectory = stats.trajectory_length(speed, dt)
            f.write('trajectory_length' + str(agent) + sep + str(trajectory) + '\n')

            # calculate speed statistics
            speed_values = stats.basic_vector_stats(speed)
            for key in speed_values['keys']: 
                f.write(agent + '_speed_' + key + sep + str(speed_values[key]) + '\n')
        
        # calculate distance statistics    
        dist_cols = [c for c in cols if c.find('dist') > 0]
        for d in dist_cols: 
            idx = d.find('dist')
            dist = df[d].values
            
            dist_values = stats.basic_vector_stats(dist)
            for key in dist_values['keys']: 
                f.write(d[:idx] + 'dist_' + key + sep + str(dist_values[key]) + '\n')
            
            # calculate amount of time agents were closer than a threshold
            for dist_t in distance_thresholds: 
                time_close = stats.time_close(dist, dist_t, dt, percent = False)  
                percent_close = stats.time_close(dist, dist_t, dt, percent = True)  
                f.write(d[:idx] + 'closer_' + str(dist_t) + 'cm_(s)' + sep + str(time_close) +'\n')
                f.write(d[:idx] + 'closer_' + str(dist_t) + 'cm_(%)' + sep + str(percent_close) + '\n')

        
        for i in range(len(info['agent_names'])): 
            for j in range(i+1, len(info['agent_names'])): 
                print('Calculating Pearson correlation of realtive velocity between {} and {}'.format(info['agent_names'][i], info['agent_names'][j]))
                
                a0 = info['agent_names'][i]
                a1 = info['agent_names'][j]
                
                rho0, p0, rho1, p1 = correlation_relative_velocity(df[a0 + '_x'].values, df[a0 + '_y'].values, 
                                                                         df[a0 + '_vx'].values, df[a0 + '_vy'].values, 
                                                                         df[a1 + '_x'].values, df[a1 + '_y'].values, 
                                                                         df[a1 + '_vx'].values, df[a1 + '_vy'].values, 
                                                                         corr = 'Pearson')
                print(rho0, p0, rho1, p1)                                               
                f.write(a0 + '/' + a1 + '_relvel_corr0_rho(P)' + sep + str(rho0) + '\n' )
                f.write(a0 + '/' + a1 + '_relvel_corr0_p(P)' + sep + str(p0) + '\n')
                f.write(a0 + '/' + a1 + '_relvel_corr1_rho(P)' + sep + str(rho1) + '\n')
                f.write(a0 + '/' + a1 + '_relvel_corr1_p(P)' + sep + str(p1) + '\n')
        
        
    # transpose csv
    pd.read_csv(name).T.to_csv(name,header=False)
    
  
    
    

