#!/usr/bin/env python
#-*- coding:utf-8 -*-
import csv


#from PyQt4 import QtGui, QtCore
from PyQt5 import QtWidgets 
from PyQt5 import QtGui
import pandas as pd
from numpy import random
import numpy as np
import sys

import settings.data_settings as ds


class coordinateWindow(QtWidgets.QWidget):

    def __init__(self, parentWindow, coordinates):
    #def __init__(self, coordinates, parent = None):
    
        '''coordinates is a dictionary with keys: 
            ['x_min', 'x_max', 'y_min', 'y_max'] '''
    
        self.COORDINATES_OLD = coordinates # we keep the original coordinates for backup
        self.COORDINATES = coordinates
        self.KEYS = ['x_min', 'x_max', 'y_min', 'y_max']
   
        super(coordinateWindow, self).__init__(parentWindow)
        #super(coordinateWindow, self).__init__()
        self.parentWindow = parentWindow
        
        self.home()
    
    def home(self): 
        
        self.TEXTBOXES = {}
        self.coordinateLayout = QtWidgets.QGridLayout()
        
        for k, key in enumerate(self.KEYS): 
            cb = QtWidgets.QLabel()
            cb.setText(key)

            le = QtWidgets.QLineEdit()
            le.setText(str(self.COORDINATES[key]))
            le.setValidator(QtGui.QDoubleValidator())
            self.TEXTBOXES[key] = le
            
            self.coordinateLayout.addWidget(cb, 0, 2*k)
            self.coordinateLayout.addWidget(le, 0, 2*k +1)

        
        self.backButton = QtWidgets.QPushButton('Back to Normal')
        self.backButton.clicked.connect(self.back2normal)
        self.coordinateLayout.addWidget(self.backButton, 3, 2)       
        
        self.okButton = QtWidgets.QPushButton('OK')
        self.okButton.clicked.connect(self.clickedOK)
        self.coordinateLayout.addWidget(self.okButton, 3, 3)
        
        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.coordinateLayout)
        self.home.show()
        
    
    def back2normal(self): 

        for key in self.TEXTBOXES: 
            self.TEXTBOXES[key].setText(str(self.COORDINATES_OLD[key]))


    def clickedOK(self): 
    
        for key in self.COORDINATES:
            self.COORDINATES[key] = float(self.TEXTBOXES[key].text())
            
            if not isinstance(self.COORDINATES[key], float):
                self.send_warning()
                break
            else: 
                if (self.COORDINATES['x_min'] >= self.COORDINATES['x_max']) or (self.COORDINATES['y_min'] >= self.COORDINATES['y_max']): 
                    self.send_warning()
                    break
                else: 
                    self.parentWindow.update_dicts(self.parentWindow.INFO, self.COORDINATES)
                    self.parentWindow.update_labels()
                    self.home.close()
                
    def send_warning(self): 
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setText("Entries missing or invalid. Please fix before leaving.")
        val = msg.exec_()

            
            



        


#if __name__ == "__main__":
#    import sys
#    import numpy as np

#    app = QtGui.QApplication(sys.argv)
#    app.setApplicationName('Time Sliders')
#   
#    dict0 = {'x_min': -1, 'x_max': -1, 'y_min': -1, 'y_max': -1}

#    main = coordinateWindow(dict0)
#    #main.show()

#    sys.exit(app.exec_())
