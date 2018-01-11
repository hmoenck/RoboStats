#!/usr/bin/env python
#-*- coding:utf-8 -*-
import csv


from PyQt4 import QtGui, QtCore
import pandas as pd
from numpy import random
import numpy as np
import sys

import settings.data_settings as ds


class timeWindow(QtGui.QWidget):

    def __init__(self, parentWindow, time, frames):
    #def __init__(self, time, parent = None):
    
        self.TIME = time
        self.FRAMES = frames
        self.START_STOP = {'start_time': time[0], 'stop_time': time[-1], 'start_frame': frames[0], 'stop_frame': frames[-1]}
    
        super(timeWindow, self).__init__(parentWindow)
        #super(timeWindow, self).__init__()
        self.parentWindow = parentWindow
        
        self.home()
    
    def home(self): 

        self.timeLayout = QtGui.QGridLayout()

        self.StartTimeSliderTitle = QtGui.QLabel('Start')
        
        self.StartTimeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.StartTimeSlider.setObjectName('start')
        self.StartTimeSlider.valueChanged.connect(self.set_time)
        self.StartTimeSlider.setRange(0, len(self.TIME))
        
        self.StartTime = QtGui.QLineEdit(self.START_STOP['start_time'])
        self.StartFrame = QtGui.QLineEdit(str(self.START_STOP['start_frame']))
        
        
        
        self.StopTimeSliderTitle = QtGui.QLabel('Stop')
        
        self.StopTimeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.StopTimeSlider.setObjectName('stop')
        self.StopTimeSlider.setRange(0, len(self.TIME))
        self.StopTimeSlider.setSliderPosition(len(self.TIME))
        self.StopTimeSlider.valueChanged.connect(self.set_time)
        
        
        self.StopTime = QtGui.QLineEdit(self.START_STOP['stop_time'])
        self.StopFrame = QtGui.QLineEdit(str(self.START_STOP['stop_frame']))
        
        
        
        self.okButton = QtGui.QPushButton('OK')
        self.okButton.clicked.connect(self.clickedOK)
        
        
        self.timeLayout.addWidget(self.StartTimeSliderTitle, 0, 0)
        self.timeLayout.addWidget(self.StartTimeSlider, 0, 1)
        self.timeLayout.addWidget(self.StartTime, 0, 2)
        self.timeLayout.addWidget(self.StartFrame, 0, 3)
        
        self.timeLayout.addWidget(self.StopTimeSliderTitle, 1, 0)
        self.timeLayout.addWidget(self.StopTimeSlider, 1, 1)
        self.timeLayout.addWidget(self.StopTime, 1, 2)
        self.timeLayout.addWidget(self.StopFrame, 1, 3)
        
        self.timeLayout.addWidget(self.okButton, 3, 3)
        
        self.home = QtGui.QWidget()
        self.home.setLayout(self.timeLayout)
        self.home.show()
        
        
    def set_time(self): 
        sender = self.sender()
        senderName = sender.objectName()
        
        self.START_STOP[senderName + '_time'] = self.TIME[sender.value()]
        self.START_STOP[senderName + '_frame'] = self.FRAMES[sender.value()]
        
        if senderName.find('start') > -1: 
            self.StartTime.setText(self.TIME[sender.value()])
            self.StartFrame.setText(str(self.FRAMES[sender.value()]))
            
        elif senderName.find('stop') > -1: 
            self.StopTime.setText(self.TIME[sender.value()])
            self.StopFrame.setText(str(self.FRAMES[sender.value()]))
            
        self.parentWindow.update_dicts(self.parentWindow.INFO, self.START_STOP)


    def clickedOK(self): 
    
        self.START_STOP['start_time'] = ds.handle_timestamp(self.START_STOP['start_time'])
        self.START_STOP['stop_time'] = ds.handle_timestamp(self.START_STOP['stop_time'])
    
        self.parentWindow.update_dicts(self.parentWindow.INFO, self.START_STOP)
        self.parentWindow.update_labels()
        self.home.close()


        


#if __name__ == "__main__":
#    import sys
#    import numpy as np

#    app = QtGui.QApplication(sys.argv)
#    app.setApplicationName('Time Sliders')
#   
#    t = np.random.randn(100)

#    main = timeWindow(t)
#    main.show()

#    sys.exit(app.exec_())
