#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt
import pandas as pd
from numpy import random
import numpy as np
import sys
import json
import settings.data_settings as ds



class timeWindow(QtWidgets.QWidget):
    '''This window shows the current settings of start and stop time (frame) and allows to change them using a slider object'''

    def __init__(self, parentWindow, time, frames, init_params):
    #def __init__(self, time, frames, init_params, parent = None):
    
        
    
        self.TIME = time
        self.FRAMES = frames
        
        self.START_STOP = {'start_time': init_params['start_time'], 'stop_time': init_params['stop_time'], 
                          'start_frame': init_params['start_frame'], 'stop_frame': init_params['stop_frame']}
    
        super(timeWindow, self).__init__(parentWindow)
        #super(timeWindow, self).__init__()
        self.parentWindow = parentWindow
        
        self.DATE_FORMATS_FILE = self.parentWindow.DATE_FORMATS_FILE
        self.PARAM_INFO_FILE = self.parentWindow.PARAM_INFO_FILE

        self.home()

    
    def home(self): 
    
        param_info = json.load(open(self.PARAM_INFO_FILE))
        self.time_format = param_info['info']['time']

        self.timeLayout = QtWidgets.QGridLayout()
        
        self.timeTitle = QtWidgets.QLabel('Adjust Start and Stop Time for evaluation')
        self.timeTitle.setFont(self.parentWindow.titleFont)
        
        # add widgets: 2 lines (start /stop each containing: name-label, slider and line 7
        # edits and labels for time and frames)
        for k, lab in enumerate(['start', 'stop']):
        
            # label (start or stop)
            label  = QtWidgets.QLabel(lab) 
            
            # slider object
            slider =  QtWidgets.QSlider(Qt.Horizontal) #
            slider.setObjectName(lab)            
            value = np.where(self.FRAMES == self.START_STOP[lab + '_frame'])[0][0]
            slider.setValue(value)            
            slider.valueChanged.connect(self.set_time)
            slider.setRange(0, len(self.TIME)-1) 
            
            # line edit for time value
            time = QtWidgets.QLineEdit()
            time.setObjectName(lab + '_time')
            time.setReadOnly(True)
            time.setText(str(self.START_STOP[lab +'_time']))
            
            # label for time value
            timelabel = QtWidgets.QLabel(self.time_format)
            
            # line edit for frame value
            frame = QtWidgets.QLineEdit()
            frame.setReadOnly(True)
            frame.setObjectName(lab + '_frame')
            frame.setText(str(self.START_STOP[lab + '_frame']))
            
            # label for frame value        
            framelabel = QtWidgets.QLabel('frames')
            
            # add widgets to layout
            self.timeLayout.addWidget(label, k+1, 0)        
            self.timeLayout.addWidget(slider, k+1, 1, 1, 2)
            self.timeLayout.addWidget(time, k+1, 3, 1, 1)
            self.timeLayout.addWidget(timelabel, k+1, 4, 1, 1)
            self.timeLayout.addWidget(frame, k+1, 5, 1, 1)
            self.timeLayout.addWidget(framelabel, k+1, 6, 1, 1)
            
        # Ok button which when pressed will send the selected values back to the parent
        self.okButton = QtWidgets.QPushButton('OK')
        self.okButton.clicked.connect(self.on_pushed_ok)      
        
        self.timeLayout.addWidget(self.timeTitle, 0, 0, 1, 5)
        self.timeLayout.addWidget(self.okButton, 3, 6)
        
        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.timeLayout)
        self.home.setFont(self.parentWindow.normalFont)
        self.home.show()

                    
    def set_time(self): 
        ''' this function gets called every time a slider is changed. It deteremines which slider was
        and updates the corresponding line edits as well as the START_STOP dictionary'''

        sender = self.sender()
        senderName = sender.objectName()
        
        # update START_STOP dictionary
        self.START_STOP[senderName + '_time'] = self.TIME[sender.value()]
        self.START_STOP[senderName + '_frame'] = self.FRAMES[sender.value()]
        
        # update time display
        time_box  = self.home.findChild(QtWidgets.QLineEdit, senderName + '_time')
        if self.time_format in ['s', 'ms']:
            time = np.round(self.TIME[sender.value()], 2)
        else: 
            time = self.TIME[sender.value()]
        time_box.setText(str(time))
        
        # update frame display 
        frame_box  = self.home.findChild(QtWidgets.QLineEdit, senderName + '_frame')
        frame_box.setText(str(self.FRAMES[sender.value()]))
           


    def on_pushed_ok(self): 
        ''' this function gets called by the OK button. It checks if the selected values are reasonable
        (i.e. start < stop) and then updates the parent window and closes timeWindow'''
        
        # check if selection is reasonable, 
        if self.START_STOP['start_frame'] > self.START_STOP['stop_frame']: 
            return
        
        # update parent window
        time_format = self.parentWindow.INFO['info']['time']
        self.START_STOP['start_time'] = ds.handle_timestamp(self.START_STOP['start_time'], time_format, self.DATE_FORMATS_FILE)
        self.START_STOP['stop_time'] = ds.handle_timestamp(self.START_STOP['stop_time'], time_format, self.DATE_FORMATS_FILE)
        self.parentWindow.update_dicts(self.parentWindow.INFO, self.START_STOP)
        self.parentWindow.update_labels()
        
        # close application
        self.home.close()


        


#if __name__ == "__main__":
#    import sys
#    import numpy as np

#    app = QtWidgets.QApplication(sys.argv)
#    app.setApplicationName('Time Sliders')
#   
#    t = np.random.randn(100)
#    f = np.arange(0, 100, 1)
#    
#    inits = {'start_time': 9, 'stop_time': 11, 'start_frame':7, 'stop_frame':70}
#    
#    
#    main = timeWindow(t, f, inits)
#    #main.show()

#    sys.exit(app.exec_())
