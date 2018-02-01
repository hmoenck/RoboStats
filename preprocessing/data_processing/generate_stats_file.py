import numpy as np
import pandas as pd
import settings.default_params as default

def makeFile(folder, csv_file, info): 

    with open(folder + '/'+ default.info_file, 'w') as f: 
        
        df = pd.read_csv(csv_file, header = 0, sep = default.csv_delim)
        cols = df.columns
        print(cols)

        data_name = info['data_file'][info['data_file'].rfind('/')+1:]
        f.write('Source,' + data_name + '\n')
        f.write('x_min,' + str(info['x_min']) + '\n')
        f.write('x_max,' + str(info['x_max']) + '\n')
        f.write('y_min,' + str(info['y_min']) + '\n')
        f.write('y_max,' + str(info['y_max']) + '\n')
        
        f.write('start,' + str(info['start_time']) + '\n')
        f.write('stop,' + str(info['stop_time']) + '\n')
        f.write('filtered,' + str(info['filtered']) + '\n')
gi
        for agent in info['agent_names']: 
            print(agent)
            f.write('mean_speed_' + str(agent) + ',' + str(np.mean(df[agent + '_speed'].values)) + '\n')
            f.write('var_speed_' + str(agent) + ',' + str(np.var(df[agent + '_speed'].values)) + '\n')
            f.write('min_speed_' + str(agent) + ',' + str(np.min(df[agent + '_speed'].values)) + '\n')
            f.write('25%_speed_' + str(agent) + ',' + str(np.percentile(df[agent + '_speed'].values, 25)) + '\n')
            f.write('median_speed_' + str(agent) + ',' + str(np.median(df[agent + '_speed'].values)) + '\n')
            f.write('75%_speed_' + str(agent) + ',' + str(np.percentile(df[agent + '_speed'].values, 75)) + '\n')
            f.write('max_speed_' + str(agent) + ',' + str(np.max(df[agent + '_speed'].values)) + '\n')
    
    
    

