#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets 
from PyQt5 import QtGui 
import pandas as pd
from numpy import random
import numpy as np
import sys
import sip
import matplotlib
matplotlib.use('Qt5Agg')


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns
sns.set()


class plotWindow(QtWidgets.QDialog):

    def __init__(self, data, plot_info1, plot_info2, parent = None):
    
        super(plotWindow, self).__init__(parent)
             
        self.data2plot = data
        self.plot_info1 = plot_info1
        self.plot_info2 = plot_info2
       
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        print('Generating: ' + plot_info1 + ' ' + plot_info2)

        
        if plot_info1 == 'Trajectory':
            self.plot_trajectory()
            self.canvas.draw()
        elif plot_info1 == 'Heatmap':
            self.plot_heatmap()
            self.canvas.draw()
        elif plot_info1 == 'Timeline':
            self.plot_timeline()
            self.canvas.draw()
        elif plot_info1 == 'Histogramm':
            self.plot_histogramm()
            self.canvas.draw()
        elif plot_info1 == 'Boxplot':
            self.plot_boxplot()
            self.canvas.draw()
        



    def plot_histogramm(self):
        keys = list(self.data2plot.keys())
        for i, key in enumerate(keys): 
            ax = self.figure.add_subplot(len(keys), 1, i+1)
            ax.hist(self.data2plot[key], 20) 
            ax.set_title(key)
            if i < len(keys) -1:
                ax.xaxis.set_ticklabels([])
            else: 
                ax.set_xlabel(self.plot_info2 )
        self.canvas.draw()

    def plot_timeline(self):
        time = self.data2plot['time'] 
        keys = list(self.data2plot.keys())
        keys.remove('time')
        for i, key in enumerate(keys): 
            ax = self.figure.add_subplot(len(keys), 1, i+1)
            ax.plot(time, self.data2plot[key]) 
            ax.set_title(key)
            if self.plot_info2 == 'Speed': 
                ax.set_ylabel(self.plot_info2 + ' [cm/s]')
            else: 
                ax.set_ylabel(self.plot_info2)
            if i < len(keys) -1:
                ax.xaxis.set_ticklabels([])
            else: 
                ax.set_xlabel('time [s]')
            
            self.canvas.draw()

    def plot_trajectory(self): 
        keys = list(self.data2plot.keys())
        ax = self.figure.add_subplot(111)
        for i, key in enumerate(keys): 
            
            ax.plot(self.data2plot[key][0, :], self.data2plot[key][1, :]) 
            ax.set_title('Trajectory')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            
            self.canvas.draw()
            
    def plot_heatmap(self):
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        bs = 30
        
        keys = list(self.data2plot.keys())
        ax = self.figure.add_subplot(111)
        x_min = np.min([np.min(self.data2plot[key][0, :]) for key in keys])
        x_max = np.max([np.max(self.data2plot[key][0, :]) for key in keys])
        y_min = np.min([np.min(self.data2plot[key][1, :]) for key in keys])
        y_max = np.max([np.max(self.data2plot[key][1, :]) for key in keys])
        
#        x_bins = int((x_max - x_min) / 20.) 
#        y_bins = int((y_max - y_min) / 20.) 
        x_bins = np.linspace(x_min, x_max, bs+1)
        y_bins = np.linspace(y_min, y_max, bs+1)
        
        hist = np.zeros((bs, bs))
        
        for i, key in enumerate(keys): 
            
            hist1, x, y = np.histogram2d(self.data2plot[key][0, :], self.data2plot[key][1, :],  bins = [x_bins, y_bins])
            hist += hist1
        
        # ignore outliers to give a sensible color distribution
        thresh = np.percentile(hist, 95)

        heat = ax.imshow(hist, cmap = 'cool', vmax = thresh, origin='lower')
        self.figure.colorbar(heat)
        self.canvas.draw()
        
    def plot_boxplot(self): 
        keys = list(self.data2plot.keys())
        ax = self.figure.add_subplot(111)
        ax.boxplot([self.data2plot[key] for key in keys])
        ax.xaxis.set_ticklabels(keys)
        
        self.canvas.draw()

