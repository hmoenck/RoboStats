import numpy as np
import pandas as pd
import settings.default_params as default

def makeFile(folder, csv_file, info, single_values): 
    print(single_values)
    name = folder + '/'+ default.info_file
    sep = default.csv_delim
    with open(name, 'w') as f: 
        
        df = pd.read_csv(csv_file, header = 0, sep = default.csv_delim)
        cols = df.columns


        data_name = info['data_file'][info['data_file'].rfind('/')+1:]
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
            sv = [s for s in single_values.keys() if s.find(agent) > -1]
            for s in sv: 
                f.write('trajectory_length' + str(agent) + sep + str(single_values[s]) + '\n')
            f.write('mean_speed_' + str(agent) + sep + str(np.mean(df[agent + '_speed'].values)) + '\n')
            f.write('var_speed_' + str(agent) + sep + str(np.var(df[agent + '_speed'].values)) + '\n')
            f.write('min_speed_' + str(agent) + sep + str(np.min(df[agent + '_speed'].values)) + '\n')
            f.write('25%_speed_' + str(agent) + sep + str(np.percentile(df[agent + '_speed'].values, 25)) + '\n')
            f.write('median_speed_' + str(agent) + sep + str(np.median(df[agent + '_speed'].values)) + '\n')
            f.write('75%_speed_' + str(agent) + sep + str(np.percentile(df[agent + '_speed'].values, 75)) + '\n')
            f.write('max_speed_' + str(agent) + sep + str(np.max(df[agent + '_speed'].values)) + '\n')
            
        dist_cols = [c for c in cols if c.find('dist') > 0]
        for dist in dist_cols: 
            idx = dist.find('dist')
            print(dist)
            print(idx)
            f.write('mean_dist_' + dist[:idx] + sep + str(np.mean(df[dist].values)) + '\n')
            f.write('var_dist_' + dist[:idx] + sep + str(np.var(df[dist].values)) + '\n')
            f.write('min_dist_' + dist[:idx] + sep + str(np.min(df[dist].values)) + '\n')
            f.write('25%_dist_' + dist[:idx] + sep + str(np.percentile(df[dist].values, 25)) + '\n')
            f.write('median_dist_' + dist[:idx] + sep + str(np.median(df[dist].values)) + '\n')
            f.write('75%_dist_' + dist[:idx] + sep + str(np.percentile(df[dist].values, 75)) + '\n')
            f.write('max_dist_' + dist[:idx] + sep + str(np.max(df[dist].values)) + '\n')
        
    # transpose csv
    pd.read_csv(name).T.to_csv(name,header=False)
    
  
    
    

