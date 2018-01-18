#!/usr/bin/env python

from PyQt4 import QtGui, QtCore
import pandas as pd
import numpy as np
import datetime
from tableWindow import tableWindow
from timeWindow import timeWindow
from coordinateWindow import coordinateWindow
from plotWindow import plotWindow
import data_processing.smoothing as smoothing
import data_processing.basic_stats as basic_stats
import settings.data_settings as ds

class mainWindow(QtGui.QMainWindow):

    INFO = {'start_time': -1, 'start_frame': -1, 'stop_time': -1, 'stop_frame': -1, 'duration_time': -1, 'duration_frame':-1,
            'x_min': -1, 'x_max': -1, 'y_min': -1, 'y_max': -1, 'filtered': False, 'agent_names':[]}
            
    TMP_FILE = ' '
    
    SMOOTHING = ['None', 'MedFilter, k=5']

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
        # smooth layout
        #------------------------------------------------------------
        self.smoothLayout = QtGui.QHBoxLayout()

        self.selectSmoothing = QtGui.QComboBox()
        for s in self.SMOOTHING:    
            self.selectSmoothing.addItem(s)

        self.smoothButton = QtGui.QPushButton('Apply Smoothing')
        self.smoothButton.clicked.connect(self.apply_smoothing)
        
        self.smoothLayout.addWidget(self.selectSmoothing)
        self.smoothLayout.addWidget(self.smoothButton)
        
        
        
        #------------------------------------------------------------
        # final layout
        #------------------------------------------------------------
        self.finalLayout = QtGui.QVBoxLayout()

        
        self.plotButton = QtGui.QPushButton('Plot')
        self.plotButton.clicked.connect(self.plot_trajectory)
        
        self.saveButton = QtGui.QPushButton('Stats and save')
        self.saveButton.clicked.connect(self.stats_and_save)
        
        self.finalLayout.addWidget(self.plotButton)
        self.finalLayout.addWidget(self.saveButton)
        
        #------------------------------------------------------------
        # general layout
        #------------------------------------------------------------
       
        self.mainLayout.addLayout(self.selectLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.timeLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.spaceLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.smoothLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.finalLayout)
         

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
        
        print([min(df[an + '_x'].values) for an in self.INFO['agent_names']])
        self.INFO['x_min'] = min(min(df[an + '_x'].values) for an in self.INFO['agent_names'])
        self.INFO['y_min'] = min(min(df[an + '_y'].values) for an in self.INFO['agent_names'])
        self.INFO['x_max'] = max(max(df[an + '_x'].values) for an in self.INFO['agent_names'])
        self.INFO['y_max'] = max(max(df[an + '_y'].values)for an in self.INFO['agent_names'])

        
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
             
             
    def plot_trajectory(self): 
        
        r = [(self.INFO['x_min'], self.INFO['y_min']), self.INFO['x_max'] - self.INFO['x_min'], self.INFO['y_max'] - self.INFO['y_min']]
        df = pd.read_csv(self.TMP_FILE, header = 0, sep = ',')
                
        d = {}
        start_idx = np.where(df['frames'].values == self.INFO['start_frame'])[0][0]
        stop_idx = np.where(df['frames'].values == self.INFO['stop_frame'])[0][0]
        
        for an in self.INFO['agent_names']:
            d[an] = (df[an + '_x'].values[start_idx:stop_idx], df[an + '_y'].values[start_idx:stop_idx])
        
        
        self.trajectoryWindow = plotWindow(d, r)
        self.trajectoryWindow.exec_()
        
    def stats_and_save(self): 
        df = basic_stats.stats_and_save(self.TMP_FILE, self.INFO)
        
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        df.to_csv(name)
        
        

        now = datetime.datetime.now()
        now_str = now.strftime("%Y_%m_%d_%H_%M")
        with open('info' + now_str + '.txt', 'w') as info_file: 
            for key in self.INFO: 
                info_file.write(key + '\t' + str(self.INFO[key]) + '\n')
                
        self.home.close()
        
        
    def apply_smoothing(self):
        smooth = str(self.selectSmoothing.currentText())
        if smooth == None: 
            pass
        else: 
            df = pd.read_csv(self.TMP_FILE, header = 0, sep = ',')
            if smooth ==  'MedFilter, k=5': 
                for an in self.INFO['agent_names']:
                    df[an + '_x'] = smoothing.medfilt(df[an + '_x'].values)
                    df[an + '_y'] = smoothing.medfilt(df[an + '_y'].values)
                    self.send_info('Trajectory is now smooth !')
                    self.INFO['filtered'] = True
                    
                    
    def send_info(self, text): 
        
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("INFO")
        retval = msg.exec_()

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('main')

    main = mainWindow()
    main.show()

    sys.exit(app.exec_())
