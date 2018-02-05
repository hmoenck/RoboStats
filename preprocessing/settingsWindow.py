#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
from PyQt5 import QtWidgets 
from PyQt5 import QtGui 
from PyQt5 import QtCore
import pandas as pd
from numpy import random
import numpy as np
import sys
import sip



class settingsWindow(QtWidgets.QWidget):
    ''' takes a list of default agent names from parent window and allows to change agent number and names'''

    #def __init__(self, parentWindow):
    def __init__(self):
    

        self.TimeOptions = ['Frames', 'Datetime', 'Milliseconds', 'Seconds']
        self.TimeOptionsDict = {'Frames':2, 'Datetime':2, 'Milliseconds':0, 'Seconds':0}
        self.AngleOptions = ['deg', 'rad']
        self.AngleOptionsDict = {'deg':2, 'rad':0}
        self.AdditionalOptions = ['Region', 'RoboMode']
        self.AdditionalOptionsDict = {'Region':0, 'RoboMode':0}
        self.AdditionalOptionsEmpty = 3
        
        self.labels = []
        self.custom_names = []
    
        #super(settingsWindow, self).__init__(parentWindow)
        super(settingsWindow, self).__init__()
        #self.parentWindow = parentWindow

        self.home()
        
    def home(self): 

        self.mainLayout = QtWidgets.QVBoxLayout()
        
        self.timeLayout = QtWidgets.QGridLayout()
        self.timeBG = QtWidgets.QButtonGroup()
        self.initCheckBoxLayout(self.TimeOptions, 'time')
        
        self.angleLayout = QtWidgets.QGridLayout()
        self.angleBG = QtWidgets.QButtonGroup()
        self.initCheckBoxLayout(self.AngleOptions,'angle')
        
        self.additionalLayout = QtWidgets.QVBoxLayout()
        self.initCheckBoxLayout2()
        
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.applyButton = QtWidgets.QPushButton('Apply')
        self.applyButton.clicked.connect(self.pushed_ok)
        self.defaultButton = QtWidgets.QPushButton('Set as Default')
        self.defaultButton.clicked.connect(self.pushed_ok)
        
        self.buttonLayout.addWidget(self.defaultButton)
        self.buttonLayout.addWidget(self.applyButton)

        self.mainLayout.addWidget(QtWidgets.QLabel('Time:'))
        self.mainLayout.addLayout(self.timeLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addWidget(QtWidgets.QLabel('Angle representation:'))
        self.mainLayout.addLayout(self.angleLayout)       
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addWidget(QtWidgets.QLabel('Additional cateories:'))
        self.mainLayout.addLayout(self.additionalLayout)
        self.mainLayout.addWidget(self.HLine())  
        self.mainLayout.addLayout(self.buttonLayout)
        
        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.mainLayout)
        self.home.show()


    
    def pushed_ok(self): 
        self.min_checked()
        pass
            
    def initCheckBoxLayout(self, lables, layout): 

        for k, t in enumerate(lables):    
            to = QtWidgets.QCheckBox(t)
            
            if layout == 'time':
                self.timeLayout.addWidget(to, np.floor(k/2.),k%2) 
                if to.text() == 'Frames': 
                    to.setCheckState(True)
                    to.setEnabled(False)
                else: 
                    self.timeBG.addButton(to)

            elif layout == 'angle':
                self.angleLayout.addWidget(to, np.floor(k/2.),k%2)
                self.angleBG.addButton(to) 

         
        if layout == 'time': 
            self.timeBG.buttonClicked[QtWidgets.QAbstractButton].connect(self.btnstate)
        else: 
            self.angleBG.buttonClicked[QtWidgets.QAbstractButton].connect(self.btnstate)
         
         
        #self.angleBG.buttonClicked[QtWidgets.QAbstractButton].connect(self.btnstate)
#        self.bg = QtWidgets.QButtonGroup()
#        #bg.setExclusive(True)
#        for k, t in enumerate(lables):    
#            to = QtWidgets.QCheckBox(t)
#            #to.setObjectName(t)
#            #to.setCheckState(values[t])
#            #to.stateChanged.connect(self.update_checkbox)

#            if layout == 'time':
#                self.timeLayout.addWidget(to, np.floor(k/2.),k%2) 
#                self.bg.addButton(to)     
##                if to.objectName() == 'Frames': 
##                    to.setEnabled(False)
##                else: self.bg.addButton(to)
#                #self.bg.buttonClicked[QtWidgets.QAbstractButton].connect(self.update_checkbox)

#                      
#            elif layout == 'angle':             
#                self.angleLayout.addWidget(to, np.floor(k/2.),k%2)
#        print(self.bg.buttons)##
    def btnstate(self, b): 
        print(b.text())
     
        
    def initCheckBoxLayout2(self): 
        
        for k, opt in enumerate(self.AdditionalOptions): 
            to = QtWidgets.QCheckBox(opt)
            to.setObjectName(opt)
            to.setCheckState(self.AdditionalOptionsDict[opt])
            to.stateChanged.connect(self.update_checkbox)
            self.additionalLayout.addWidget(to)
        
        for empt in range(self.AdditionalOptionsEmpty): 
            le = QtWidgets.QLineEdit('Enter additional category')
            self.additionalLayout.addWidget(le)

                
    def update_checkbox(self):
        ''' updated the values in the TimeOptionsDict whenever a checkbox value is changed'''
        pass
#        sender = self.sender()
#        name = sender.objectName()
#        state = sender.checkState()
#        print(state)
#        if name in self.TimeOptions: 
#            self.TimeOptionsDict[name] = state
#            print(self.TimeOptionsDict)
#        elif name in self.AngleOptions: 
#            self.AngleOptionsDict[name] = state
#            print(self.AngleOptionsDict)
        
    def min_checked(self): 
        ''' checks whether at least one of the time options was selected '''
        if sum(list(self.TimeOptionsDict.values())) <= 0: 
            self.send_warning('you must select at least one')

            
    def send_warning(self, text): 
        ''' opens a Qt Warning Dialog'''
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        
    def HLine(self):
        ''' adds a sunken horizontal line to the display'''
        toto = QtWidgets.QFrame()
        toto.setFrameShape(QtWidgets.QFrame.HLine)
        toto.setFrameShadow(QtWidgets.QFrame.Sunken)
        return toto
        

            
        
        
        
    

if __name__ == "__main__":
    import sys
    import numpy as np

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Settings')

    main = settingsWindow()
    #main.show()

    sys.exit(app.exec_())       
        
        
