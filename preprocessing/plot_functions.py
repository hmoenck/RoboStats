import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_histogramm(data, filename, folder, x_label, y_label, title = None, bins = 30):
    ''' data has format (agents/agent_pairs x samples).'''
    plt.figure(figsize = (16, 4))
    N = data.shape[0]
    for i in range(N): 
        plt.subplot(N, 1, i+1)
        plt.hist(data[i, :], bins = bins) 
        plt.ylabel(y_label)
    plt.xlabel(x_label)
    if not title == None: 
        plt.title(title)
    plt.savefig(folder + filename)

def plot_timelines(data, filename, folder, labels, x_label, y_label, title = None):
    ''' timelines has format lines x time '''
    plt.figure(figsize = (16, 4))
    N = data.shape[0]
    time = data[0, :]
    for i in range(N-1): 
        plt.subplot(N-1, 1, i+1)
        plt.plot(time, data[i+1, :], label = labels[i])
        plt.ylabel(y_label)
        plt.legend()
    plt.xlabel(x_label)
    if not title == None: 
        plt.title(title)
    plt.savefig(folder + filename)
    
def plot_boxplot(data, filename, folder, y_label, title = None): 

    plt.figure(figsize = (12, 4))
    N = data.shape[0]
    plt.boxplot([data[i,:] for i in range(N)])
    plt.ylabel(y_label)
    if not title == None: 
        plt.title(title)
    plt.savefig(folder + filename)
    
def plot_trajectory(data, filename, folder, agent_names):
    plt.figure(figsize = (8,8))
    for i, an in enumerate(agent_names):
        plt.plot(data[i*2, :], data[i*2 +1, :], label = an)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig(folder + filename)


def prepare_data_trajectory(data, agent_names): 
    cols = [ c for c in data.columns if c.find('_x')>=0 or c.find('_y') >=0]
    data2plot = np.zeros((len(cols), len(data[cols[0]].values)))
    for i, an in enumerate(agent_names):
        data2plot[i*2, :]  = data[an + '_x'].values
        data2plot[i*2 + 1, :]  = data[an + '_y'].values
    return data2plot
   
def prepare_data(data, keyword, include_time = False): 
    # data is a pd. dataframe
    cols = [ c for c in data.columns if c.find(keyword)>=0]
    data2plot = np.zeros((len(cols), len(data[cols[0]].values)))
    labels = []
    for i, c in enumerate(cols):
        data2plot[i, :]  = data[c].values
        labels.append(c[:c.find(keyword)-1])
    if include_time:
        data2plot = np.vstack((data['seconds'].values, data2plot))
    return data2plot, labels
            


def plot_things(data, folder, agent_names, plot_instructions):  
    ''' this function plots things''' 
    
    
    if  plot_instructions[0] == 'none': 
        return
               
    for plot_instruction in plot_instructions: 
        print('generating: ', plot_instruction)
    
        if plot_instruction.find('Trajectory') >= 0: 
            data2plot = prepare_data_trajectory(data, agent_names)
            plot_trajectory(data2plot, '/trajectory.jpg', folder, agent_names)
            
        elif plot_instruction.find('Histogramm') >= 0:
        
            if plot_instruction.find('Speed') >= 0:
                data2plot, l = prepare_data(data, 'speed')
                plot_histogramm(data2plot, '/speed_histgramm.jpg', folder, 'speed', 'frequency')
                
            elif plot_instruction.find('Distance') >= 0:
                data2plot, l = prepare_data(data, 'dist')
                plot_histogramm(data2plot, '/dist_histgramm.jpg', folder, 'distance', 'frequency')
                
            elif plot_instruction.find('Angle') >= 0:
                data2plot, l = prepare_data(data, 'angle')
                plot_histogramm(data2plot, '/angle_histgramm.jpg', folder, 'angle', 'frequency')
        
        elif plot_instruction.find('Timeline') >= 0: 
        
            if plot_instruction.find('Speed') >= 0:
                data2plot, lables = prepare_data(data, 'speed', include_time = True)
                plot_timelines(data2plot, '/speed_timeline.jpg', folder, lables, 'time', 'speed')
                
            elif plot_instruction.find('Distance') >= 0:
                data2plot, lables = prepare_data(data, 'dist', include_time = True)
                plot_timelines(data2plot, '/dist_timeline.jpg', folder, lables, 'time', 'distance')
                
            elif plot_instruction.find('Angle') >= 0:
                data2plot, lables = prepare_data(data, 'angle', include_time = True)
                plot_timelines(data2plot, '/angle_timeline.jpg', folder, lables, 'time', 'angle')
            
        elif plot_instruction.find('Boxplot') >= 0:
            
            if plot_instruction.find('Speed') >= 0:
                data2plot, l = prepare_data(data, 'speed')
                plot_boxplot(data2plot, '/speed_boxplot.jpg', folder, 'speed')
                
            elif plot_instruction.find('Distance') >= 0:
                data2plot, l = prepare_data(data, 'dist')
                plot_boxplot(data2plot, '/dist_boxplot.jpg', folder, 'distance')
        
        else: 
            pass

        
#    speed = data['one_speed'].values
#    plot_histogramm(speed, '/speed_hist.jpg', folder, 'speed', 'frequency')
#    
#    
#    ls = []
#    speed_data = np.zeros((len(agent_names), len(speed)))
#    
#    for k, an in enumerate(agent_names): 
#        ls.append(an)
#        speed_data[k, :] = data[an + '_speed'].values
#    plot_timelines(speed_data, '/speed_timeline.jpg', folder, ls, 'time [s]', 'speed [cm/s]')    
#    
#    cols = data.columns
#    dist_labels = [c for c in cols if c.find('dist') > 0]
#    dist_data = np.zeros((len(dist_labels), len(speed)))
#    for k, dl in enumerate(dist_labels): 
#        dist_data[k, :] = data[dl].values
#    
#    plot_timelines(dist_data, '/dist_timeline.jpg', folder, dist_labels, 'time [s]', 'distance [cm]')
#    
#    plot_boxplot(speed, '/speed_boxplot.jpg', folder, 'speed')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    

    

