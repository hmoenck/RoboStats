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
import json
import settings.default_params as default




class settingsWindow(QtWidgets.QWidget):
    ''' Allows to set time format (datetime, milliseconds or seconds), angle format (deg or rad), and additional parameters'''

    def __init__(self, parentWindow):
    #def __init__(self):
    

        self.TimeOptions = ['frames', 'datetime', 'milliseconds', 'seconds']
        self.TimeOptionsShort = {'datetime':'dt', 'milliseconds':'ms', 'seconds':'s'}
        self.AngleOptions = ['deg', 'rad']
        self.AdditionalOptions = ['Region', 'RoboMode']
    
        super(settingsWindow, self).__init__(parentWindow)
        #super(settingsWindow, self).__init__()
        self.parentWindow = parentWindow

        self.home()
        
    def home(self): 

        self.mainLayout = QtWidgets.QVBoxLayout()
        
        # ---------------------------------------------------------------------
        # TIME LAYOUT
        # ---------------------------------------------------------------------
        self.timeLayout = QtWidgets.QGridLayout()
        self.timeBG = QtWidgets.QButtonGroup() # button group for exclusive selection of one option
        self.initCheckBoxLayout(self.TimeOptions, 'time')
        
        # ---------------------------------------------------------------------
        # ANGLE LAYOUT
        # ---------------------------------------------------------------------       
        self.angleLayout = QtWidgets.QGridLayout()
        self.angleBG = QtWidgets.QButtonGroup() # button group for exclusive selection of one option
        self.initCheckBoxLayout(self.AngleOptions,'angle')
                
        # ---------------------------------------------------------------------
        # ADDITIONAL PARAMS LAYOUT
        # ---------------------------------------------------------------------     
        self.additionalLayout = QtWidgets.QVBoxLayout()
        self.AdditionalOptionsCB = [] # list of all checkboxes for additional parameters
        self.initCheckBoxLayout2()
        
        # ---------------------------------------------------------------------
        # ADDITIONAL PARAMS LAYOUT
        # ---------------------------------------------------------------------   
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.applyButton = QtWidgets.QPushButton('Apply')
        self.applyButton.clicked.connect(self.pushed_apply)
        self.buttonLayout.addWidget(self.applyButton)
        
        # ---------------------------------------------------------------------
        # ADD SUBLAYOUTS TO MAIN LAYOUT
        # ---------------------------------------------------------------------
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

            
    def initCheckBoxLayout(self, lables, layout): 
        ''' initialization of time and angle layout'''
        
        param_dict = json.load(open(default.params))
        defaults = param_dict['info']
        
        chosen_time_format = self.key_by_value(self.TimeOptionsShort, defaults['time']) 
        chosen_angle_format = defaults['angle']
        
        for k, t in enumerate(lables):    
            cb = QtWidgets.QCheckBox(t)
            
            if layout == 'time':
                self.timeLayout.addWidget(cb, np.floor(k/2.),k%2) 
                if cb.text() == 'frames': 
                    cb.setCheckState(2)
                    cb.setEnabled(False)
                else: 
                    if cb.text() == chosen_time_format:
                        cb.setCheckState(2)
                    self.timeBG.addButton(cb)

            elif layout == 'angle':
                if cb.text() == chosen_angle_format:
                    cb.setCheckState(2)
                self.angleLayout.addWidget(cb, np.floor(k/2.),k%2)

                self.angleBG.addButton(cb) 


    def initCheckBoxLayout2(self): 
        ''' initialization of the additionalLayout. All Options listed in AdditionalOptions are displayed with a checkBox, 
        multiple selection is possible'''

        for k, opt in enumerate(self.AdditionalOptions): 
            cb = QtWidgets.QCheckBox(opt)
            if opt in self.parentWindow.OTHER: 
                cb.setCheckState(2)
            self.additionalLayout.addWidget(cb)
            self.AdditionalOptionsCB.append(cb)       
            
            
    def pushed_apply(self): 
        ''' if applyButton is pushed, the selected settings are sent to parent window. settingsWindow is closed'''
        
        param_dict = json.load(open(default.params))
        param_dict['info']['time'] = self.TimeOptionsShort[self.timeBG.checkedButton().text()]
        param_dict['info']['angle'] = self.angleBG.checkedButton().text()
        
        with open(default.params, 'w') as fp:
            json.dump(param_dict, fp)

        self.parentWindow.PARAM_INFO['time'] = self.TimeOptionsShort[self.timeBG.checkedButton().text()]
        self.parentWindow.draw_time_labels(init = False) 
        
        self.parentWindow.PARAM_INFO['angle'] = self.angleBG.checkedButton().text()
        self.parentWindow.draw_agent_names(init = False) 
        
        self.parentWindow.OTHER = [b.text() for b in self.AdditionalOptionsCB if b.isChecked()]
        self.parentWindow.update_checklabels('OTHER')
        self.home.close()

            
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
        
        
    def key_by_value(self, dictionary, goal_value): 

        for key, value in dictionary.items():
            if value == goal_value:
                return key

            
        
        
        
    

if __name__ == "__main__":
    import sys
    import numpy as np

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Settings')

    main = settingsWindow()
    #main.show()

    sys.exit(app.exec_())       
        
        
