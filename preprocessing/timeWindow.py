#!/usr/bin/env python
#-*- coding:utf-8 -*-
import csv


#from PyQt4 import QtGui, QtCore
from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt
import pandas as pd
from numpy import random
import numpy as np
import sys
import json
import settings.data_settings as ds



#TODO: breaks if slider is moved too far
class timeWindow(QtWidgets.QWidget):

    def __init__(self, parentWindow, time, frames):
    #def __init__(self, time, frames, parent = None):
    
        self.TIME = time
        self.FRAMES = frames
        self.START_STOP = {'start_time': time[0], 'stop_time': time[-1], 'start_frame': frames[0], 'stop_frame': frames[-1]}
    
        super(timeWindow, self).__init__(parentWindow)
        #super(timeWindow, self).__init__()
        self.parentWindow = parentWindow
        self.DATE_FORMATS_FILE = self.parentWindow.DATE_FORMATS_FILE
        self.PARAM_INFO_FILE = self.parentWindow.PARAM_INFO_FILE
        #self.DATE_FORMATS_FILE = 'settings/date_formats.json'
        #self.PARAM_INFO_FILE = 'settings/dict_data.json'
        
        
        
        self.home()
    
    def home(self): 
    
        param_info = json.load(open(self.PARAM_INFO_FILE))
        self.time_format = param_info['info']['time']

        self.timeLayout = QtWidgets.QGridLayout()

        self.timeTitle = QtWidgets.QLabel('Adjust Start and Stop Time for evaluation')
        #self.timeTitle.setFont(self.parentWindow.titleFont)

        self.StartTimeSliderTitle = QtWidgets.QLabel('Start')
        
        self.StartTimeSlider = QtWidgets.QSlider(Qt.Horizontal)
        self.StartTimeSlider.setObjectName('start')
        self.StartTimeSlider.valueChanged.connect(self.set_time)
        self.StartTimeSlider.setRange(0, len(self.TIME))        
        self.StartTime = QtWidgets.QLineEdit()
        self.StartTimeLabel = QtWidgets.QLabel(self.time_format)
        self.StartFrame = QtWidgets.QLineEdit(str(self.START_STOP['start_frame']))
        self.StartFrameLabel = QtWidgets.QLabel('frames')
        
        self.StopTimeSliderTitle = QtWidgets.QLabel('Stop')
        
        self.StopTimeSlider = QtWidgets.QSlider(Qt.Horizontal)
        self.StopTimeSlider.setObjectName('stop')
        self.StopTimeSlider.setRange(0, len(self.TIME))
        self.StopTimeSlider.setSliderPosition(len(self.TIME))
        self.StopTimeSlider.valueChanged.connect(self.set_time)
                
        self.StopTime = QtWidgets.QLineEdit(str(self.START_STOP['stop_time']))
        self.StopTimeLabel = QtWidgets.QLabel(self.time_format)
        self.StopFrame = QtWidgets.QLineEdit(str(self.START_STOP['stop_frame']))
        self.StopFrameLabel = QtWidgets.QLabel('frames')
        
        self.okButton = QtWidgets.QPushButton('OK')
        self.okButton.clicked.connect(self.clickedOK)       
        
        self.timeLayout.addWidget(self.timeTitle, 0, 0, 1, 5)
        
        self.timeLayout.addWidget(self.StartTimeSliderTitle, 1, 0)        
        self.timeLayout.addWidget(self.StartTimeSlider, 1, 1, 1, 2)
        self.timeLayout.addWidget(self.StartTime, 1, 3, 1, 1)
        self.timeLayout.addWidget(self.StartTimeLabel, 1, 4, 1, 1)
        self.timeLayout.addWidget(self.StartFrame, 1, 5, 1, 1)
        self.timeLayout.addWidget(self.StartFrameLabel, 1, 6, 1, 1)
        
        self.timeLayout.addWidget(self.StopTimeSliderTitle, 2, 0)
        self.timeLayout.addWidget(self.StopTimeSlider, 2, 1, 1, 2)
        self.timeLayout.addWidget(self.StopTime, 2, 3, 1, 1)
        self.timeLayout.addWidget(self.StopTimeLabel, 2, 4, 1, 1)
        self.timeLayout.addWidget(self.StopFrame, 2, 5, 1, 1)
        self.timeLayout.addWidget(self.StopFrameLabel, 2, 6, 1, 1)
        
        self.timeLayout.addWidget(self.okButton, 3, 6)
        
        self.init_labels()
        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.timeLayout)
        self.home.show()
    
    def init_labels(self): 
        
        if self.time_format in ['ms', 's']: 
            start_time = str(np.round(self.TIME[0], 2))
            stop_time = str(np.round(self.TIME[-1], 2))
        else: 
            start_time = str(self.TIME[0])
            stop_time = str(self.TIME[-1])
            
        self.StartTime.setText(start_time)
        self.StartFrame.setText(str(self.FRAMES[0]))
        
        self.StopTime.setText(stop_time)
        self.StopFrame.setText(str(self.FRAMES[-1]))
            
        
    def set_time(self): 
        sender = self.sender()
        senderName = sender.objectName()
        
        self.START_STOP[senderName + '_time'] = self.TIME[sender.value()]
        self.START_STOP[senderName + '_frame'] = self.FRAMES[sender.value()]
        
        if self.time_format in ['s', 'ms']:
            time = np.round(self.TIME[sender.value()], 2)
        else: 
            time = self.TIME[sender.value()]
        
        
        if senderName.find('start') > -1: 
            self.StartTime.setText(str(time))
            self.StartFrame.setText(str(self.FRAMES[sender.value()]))
            
        elif senderName.find('stop') > -1: 
            self.StopTime.setText(str(time))
            self.StopFrame.setText(str(self.FRAMES[sender.value()]))
            
        #self.parentWindow.update_dicts(self.parentWindow.INFO, self.START_STOP)


    def clickedOK(self): 

        time_format = self.parentWindow.INFO['info']['time']
    
        self.START_STOP['start_time'] = ds.handle_timestamp(self.START_STOP['start_time'], time_format, self.DATE_FORMATS_FILE)
        self.START_STOP['stop_time'] = ds.handle_timestamp(self.START_STOP['stop_time'], time_format, self.DATE_FORMATS_FILE)
    
        self.parentWindow.update_dicts(self.parentWindow.INFO, self.START_STOP)
        self.parentWindow.update_labels()
        self.home.close()


        


#if __name__ == "__main__":
#    import sys
#    import numpy as np

#    app = QtWidgets.QApplication(sys.argv)
#    app.setApplicationName('Time Sliders')
#   
#    t = np.random.randn(100)
#    f = np.arange(0, 100, 1)

#    main = timeWindow(t, f)
#    #main.show()

#    sys.exit(app.exec_())
