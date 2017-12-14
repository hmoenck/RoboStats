import sys
from PyQt4 import QtGui, QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import seaborn as sns
sns.set()

import random
import numpy as np


class MyPlotWindow(QtGui.QDialog):
    def __init__(self, data, data_info,  parent=None):
        super(MyPlotWindow, self).__init__(parent)
        
        t0 = data_info['start_time']
        t1 = data_info['stop_time']
        
        self.data2plot = {}
        
        for key in data_info: 
            if key.find('agent') >= 0 and data_info[key] == True: 
                idx = key[key.find('_')+1]
                self.data2plot[key] = np.vstack((data['x'+idx][t0: t1], data['y'+idx][t0:t1]))
        

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        #data = [random.random() for i in range(10)]

        
        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        #ax.plot(data, '*-')
        for key in self.data2plot: 
            ax.plot(self.data2plot[key][0,:], self.data2plot[key][1,:], label = key)
       
        ax.legend()
        
        # refresh canvas
        self.canvas.draw()

