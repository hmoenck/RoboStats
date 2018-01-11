#!/usr/bin/env python

from PyQt4 import QtGui, QtCore
import pandas as pd
import numpy as np
from tableWindow import tableWindow
from timeWindow import timeWindow
from coordinateWindow import coordinateWindow
import settings.data_settings as ds

class mainWindow(QtGui.QMainWindow):

    INFO = {'start_time': -1, 'start_frame': -1, 'stop_time': -1, 'stop_frame': -1, 'duration_time': -1, 'duration_frame':-1,
            'x_min': -1, 'x_max': -1, 'y_min': -1, 'y_max': -1}
            
    TMP_FILE = ' '

    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        self.home()

    def home(self): 


        self.mainLayout = QtGui.QVBoxLayout()
        
        #------------------------------------------------------------
        # select layout
        #------------------------------------------------------------
        
        self.selectLayout = QtGui.QHBoxLayout()
        
        self.selectData = QtGui.QPushButton('Set Data Columns')
        self.selectData.clicked.connect(self.on_Button_clicked)
        
        self.selectLayout.addWidget(self.selectData)       
        
        #------------------------------------------------------------
        # time layout
        #------------------------------------------------------------
        
        self.timeLayout = QtGui.QVBoxLayout()
        
        self.startInfo = QtGui.QLabel('Start: ----')
        self.stopInfo = QtGui.QLabel('Stop: ----')
        self.durationInfo = QtGui.QLabel('Duration: ----')
        
        self.changeTimeButton = QtGui.QPushButton('Change')
        self.changeTimeButton.setFixedWidth(100)
        self.changeTimeButton.clicked.connect(self.changeTime)
        
        
        self.timeLayout.addWidget(self.startInfo)
        self.timeLayout.addWidget(self.stopInfo)
        self.timeLayout.addWidget(self.durationInfo)
        self.timeLayout.addWidget(self.changeTimeButton)
        
        
        #------------------------------------------------------------
        # space layout
        #------------------------------------------------------------
        
        self.spaceLayout = QtGui.QGridLayout()
        
        borders = ['x_min', 'x_max', 'y_min', 'y_max']
        self.Border_info = []
        
        for j, b in enumerate(borders):   
            border = QtGui.QLabel( b +': ----')
            border.setObjectName(b)
            self.spaceLayout.addWidget(border, 0, j)
            self.Border_info.append(border)
            
        self.changeCoordsButton = QtGui.QPushButton('Change')
        self.changeCoordsButton.setFixedWidth(100)
        self.changeCoordsButton.clicked.connect(self.changeCoords)

        self.spaceLayout.addWidget(self.changeCoordsButton)
        
        
        #------------------------------------------------------------
        # general layout
        #------------------------------------------------------------
       
        self.mainLayout.addLayout(self.selectLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.timeLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.spaceLayout)
         

        self.home = QtGui.QWidget()
        self.home.setLayout(self.mainLayout)
        self.setCentralWidget(self.home)

    
    def on_Button_clicked(self): 
    
        data_name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        print('selected file: ', data_name)
        self.table = tableWindow(self, data_name)
        self.table.show()        
        #self.updateInfo(self.TMP_FILE_INFO)


    def init_Info(self, tmp_file): 
    
        # up to now this function gets only called by TableWindow
        self.TMP_FILE = tmp_file
        df = pd.read_csv(tmp_file, header = 0, sep = ',')

        self.INFO['start_time'] = ds.handle_timestamp(df['time'].values[0])
        self.INFO['stop_time'] = ds.handle_timestamp(df['time'].values[-1])
        
        self.INFO['start_frame'] = df['frames'].values[0]
        self.INFO['stop_frame'] = df['frames'].values[-1]
        
        self.INFO['duration_time'] = type(df['time'].values[-1])
        self.INFO['duration_frame'] = int(df['frames'].values[-1]) - int(df['frames'].values[0])
        
        #TODO THIS PART HAS TO BE UPDATED FOR MORE THAN TWO AGENTS 
        self.INFO['x_min'] = min(min(df['agent0_x'].values), min(df['agent1_x'].values))
        self.INFO['y_min'] = min(min(df['agent0_y'].values), min(df['agent1_y'].values))
        self.INFO['x_max'] = max(max(df['agent0_x'].values), max(df['agent1_x'].values))
        self.INFO['y_max'] = max(max(df['agent0_y'].values), max(df['agent1_y'].values))
        
        self.update_labels()
        
    def update_labels(self): 

        self.startInfo.setText('Start: ' + str(self.INFO['start_time']) + '\t(' + str(self.INFO['start_frame']) + ')')
        self.stopInfo.setText('Stop: '+ str(self.INFO['stop_time']) + '\t(' + str(self.INFO['stop_frame']) + ')')
        self.durationInfo.setText('Duration: ' + str(self.INFO['stop_time'] - self.INFO['start_time']) + '\t(' + str(self.INFO['stop_frame'] - self.INFO['start_frame']) + ')')
        
        for border in self.Border_info: 
            border.setText(border.objectName() + ': ' + str(np.round(self.INFO[border.objectName()], 2)))

        
    def HLine(self):
    
        toto = QtGui.QFrame()
        toto.setFrameShape(QtGui.QFrame.HLine)
        toto.setFrameShadow(QtGui.QFrame.Sunken)
        return toto
        
    def changeTime(self):
        df = pd.read_csv(self.TMP_FILE, header = 0, sep = ',')
        t = df['time'].values
        f = df['frames'].values
        
        self.time = timeWindow(self, t, f)
        self.time.show()   
        
    def changeCoords(self): 
        borders = ['x_min', 'x_max', 'y_min', 'y_max']
        coords = {}
        for b in borders: 
            coords[b] = self.INFO[b]
            
        self.coordinates = coordinateWindow(self, coords)
        self.coordinates.show()  

    def update_dicts(self, dict1, dict2): 
    
        for key in dict2: 
             dict1[key] = dict2[key]

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('main')

    main = mainWindow()
    main.show()

    sys.exit(app.exec_())
