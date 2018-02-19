import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_histogramm(data, filename, folder, x_label, y_label, title = None, bins = 20):
    ''' data is a one-dim array'''
    plt.figure(figsize = (16, 4))
    plt.hist(data, bins = bins) 
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if not title == None: 
        plt.title(title)
    plt.savefig(folder + filename)

def plot_timelines(timelines, filename, folder, labels, x_label, y_label, title = None):
    ''' timelines has format lines x time '''
    plt.figure(figsize = (16, 4))
    for k in range(timelines.shape[0]): 
        plt.plot(timelines[k, :], label = labels[k])
    plt.legend()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if not title == None: 
        plt.title(title)
    plt.savefig(folder + filename)
    
def plot_boxplot(data, filename, folder, y_label, title = None): 

    plt.figure(figsize = (12, 4))
    plt.boxplot(data)
    plt.ylabel(y_label)
    if not title == None: 
        plt.title(title)
    plt.savefig(folder + filename)


def plot_things(data, folder, agent_names):  
    ''' this function plots things'''  
    speed = data['one_speed'].values
    plot_histogramm(speed, '/speed_hist.jpg', folder, 'speed', 'frequency')
    
    
    ls = []
    speed_data = np.zeros((len(agent_names), len(speed)))
    
    for k, an in enumerate(agent_names): 
        ls.append(an)
        speed_data[k, :] = data[an + '_speed'].values
    plot_timelines(speed_data, '/speed_timeline.jpg', folder, ls, 'time [s]', 'speed [cm/s]')    
    
    cols = data.columns
    dist_labels = [c for c in cols if c.find('dist') > 0]
    dist_data = np.zeros((len(dist_labels), len(speed)))
    for k, dl in enumerate(dist_labels): 
        dist_data[k, :] = data[dl].values
    
    plot_timelines(dist_data, '/dist_timeline.jpg', folder, dist_labels, 'time [s]', 'distance [cm]')
    
    plot_boxplot(speed, '/speed_boxplot.jpg', folder, 'speed')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    

    

