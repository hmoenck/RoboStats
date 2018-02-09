#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
#from PyQt4 import QtGui, QtCore

from PyQt5 import QtWidgets 
#from PyQt5 import QtGui

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.figure import Figure

from matplotlib.figure import Figure
import matplotlib.patches as patches

import seaborn as sns
sns.set()

import random
import numpy as np





class plotWindow(QtWidgets.QDialog):
#TODO make more general
    def __init__(self, data, rect, parent = None):
        ''' 'data' is a dictionary and for every agent it contains an xy tuple, strt/stop time is 
        according to the settings in main window. 
        'rect' is a list contaiing lower left corner of the rectangle (as a tuple) and width and height paramters i.e. [(x,y), width,   height], this is in accordance with the arena settings from main window. '''
        super(plotWindow, self).__init__(parent)
             
        self.rect = rect #format = [(x,y), width, height]
        self.data2plot = data
        

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)


        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        ax = self.figure.add_subplot(111)
        
        self.plot(ax)
        self.canvas.draw()

    def plot(self, ax):
        ''' plot trajectory '''
        #ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        for key in self.data2plot: 
            ax.plot(self.data2plot[key][0], self.data2plot[key][1], label = key)
       
        ax.add_patch(patches.Rectangle(*self.rect, fill = False, linewidth = 5))
        
        ax.legend()
        #ax.savefig('fig.png')
        #ax.xlim(self.rect[0][0]-5, self.rect[0][0] +self.rect[1] +5)
        #ax.ylim(self.rect[0][1]-5, self.rect[0][1] +self.rect[2] +5)
       
        self.canvas.draw()

