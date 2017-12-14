import numpy as np
import pandas as pd

def handle_data(filename): 
    # TODO: allow to clean data and check column names
    # expected data format: 'time', 'x0', 'y0', 'x1', 'y1'
    
    df = pd.DataFrame.from_csv(filename, header = 0, sep = '\t', index_col = 0) 
    cols = df.columns[~df.columns.str.startswith('Unnamed:')]
    df_new = df[cols]

    
    t = df_new['time'].values
    positions = ['x0', 'y0','x1','y1']
    velocities = ['v_x0', 'v_y0','v_x1','v_y1']
    distances = ['d']
    
    # calculate velocities
    for i, p in enumerate(positions): 
        v = np.diff(df_new[p].values)/np.diff(t)
        df_new[velocities[i]] = pd.Series(np.append(v, np.nan), index = df_new.index)
        
    # calculate distance
    for d in distances: 
        dist = np.sqrt((df_new['x0'].values - df_new['x1'].values)**2 +
                        (df_new['y0'].values - df_new['y1'].values)**2 )
        df_new[d] = pd.Series(dist, index = df_new.index)
    
    return df_new
