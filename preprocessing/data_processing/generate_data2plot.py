import numpy as np
import pandas as pd 
import json


def makeData2Plot(df, representation, datatype, info, params): 
    '''This function gets called if the inspect button in mainWindow is pushed. makeData2Plot
    used the plot settings from the dropdown menu and prepares the data accordingly. If None is 
    returnd this triggers and Error Message in main'''

    if representation == 'Trajectory': 
        data2plot = {an : np.vstack((df[an +'_x'], df[an +'_y'])) for an in info['agent_names']}
        
    elif representation == 'Timeline': 
        if datatype == 'Speed': 
            data2plot = {an : df[an + '_speed'] for an in info['agent_names']}
        elif datatype == 'Distance': 
            dist_cols = [c for c in df.columns if c.find('dist') >= 0]
            data2plot = {c : df[c] for c in dist_cols}
        elif datatype == 'Angle':
            params = json.load(open(params))
            rep = params['info']['angle']
            datatype += ' [' +rep + ']'
            data2plot = {an : df[an + '_angle'] for an in info['agent_names']}   
        data2plot['time'] = df['seconds']
        
    elif representation == 'Histogramm': 
        if datatype == 'Speed': 
            data2plot = {an : df[an + '_speed'] for an in info['agent_names']}
        elif datatype == 'Distance': 
            dist_cols = [c for c in df.columns if c.find('dist') >= 0]
            data2plot = {c : df[c] for c in dist_cols}
        elif datatype == 'Angle':
            data2plot = {an : df[an + '_angle'] for an in info['agent_names']}
            params = json.load(open(params))
            rep = params['info']['angle']
            datatype += ' [' +rep + ']'
            
    elif representation == 'Boxplot': 
        if datatype == 'Speed': 
            data2plot = {an : df[an + '_speed'] for an in info['agent_names']}
        elif datatype == 'Distance': 
            dist_cols = [c for c in df.columns if c.find('dist') >= 0]
            data2plot = {c : df[c] for c in dist_cols}
    else: 
        data2plot = None 
            
    return data2plot              

