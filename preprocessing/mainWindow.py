#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets 
from PyQt5 import QtGui
from PyQt5.QtGui import QFont   

import os
import pandas as pd
import numpy as np
import datetime
import sip
from tableWindow import tableWindow
from timeWindow import timeWindow
#from coordinateWindow import coordinateWindow
from plotWindow import plotWindow
import data_processing.smoothing as smoothing
import data_processing.basic_stats as basic_stats
import settings.data_settings as ds
import settings.default_params as default
import data_processing.generate_stats_file as genStats
#import plot_functions as my_plt
import json


class mainWindow(QtWidgets.QMainWindow):

    INFO = {'start_time': -1, 'start_frame': -1, 'stop_time': -1, 'stop_frame': -1, 'duration_time': -1, 'duration_frame':-1,
            'x_min': -1, 'x_max': -1, 'y_min': -1, 'y_max': -1, 'filtered': False}
            
    TMP_FILE = default.tmp_file
    
    SMOOTHING = ['Select Filter', 'MedFilter, k=5']
    CSV_INFO_FILE = 'settings/csv_info.json'
    PARAM_INFO_FILE = 'settings/dict_data.json'
    DATE_FORMATS_FILE = 'settings/date_formats.json'

    

    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        self.setFixedSize(500,400)
        self.home()

    def home(self): 


        self.mainLayout = QtWidgets.QVBoxLayout()
        
        #------------------------------------------------------------
        # select layout
        #------------------------------------------------------------
        
        #self.selectLayout = QtWidgets.QHBoxLayout()
        
        self.selectedFile = QtWidgets.QLineEdit()
        self.browseButton = QtWidgets.QPushButton('Browse')
        self.browseButton.clicked.connect(self.on_browse_clicked)
        
        self.delimLabel = QtWidgets.QLabel('File deliminator')
        self.setDelim = QtWidgets.QLineEdit()
        self.skipRowsLabel = QtWidgets.QLabel('Skip rows')
        self.setSkipRows = QtWidgets.QLineEdit()
        self.setSkipRows.setValidator(QtGui.QIntValidator())
        self.init_browse_info()
        
        self.openInView = QtWidgets.QCheckBox('view')
        self.openInView.setCheckState(2)
        self.openInView.setEnabled(False)
        
        self.loadButton = QtWidgets.QPushButton('Load')
        self.loadButton.clicked.connect(self.on_load_clicked)
        
        
        self.selectUpper = QtWidgets.QHBoxLayout()
        self.selectUpper.addWidget(self.selectedFile)
        self.selectUpper.addWidget(self.browseButton)
        
        self.selectLower = QtWidgets.QHBoxLayout()
        self.selectLower.addWidget(self.delimLabel)
        self.selectLower.addWidget(self.setDelim)
        self.selectLower.addWidget(self.skipRowsLabel)
        self.selectLower.addWidget(self.setSkipRows)
        self.selectLower.addWidget(self.openInView)
        self.selectLower.addWidget(self.loadButton)
        #self.selectData = QtWidgets.QPushButton('Set Data Columns')
        #self.selectData.clicked.connect(self.on_Button_clicked)
        
        #self.selectLayout.addWidget(self.selectData)       
        self.selectLayout = QtWidgets.QVBoxLayout()
        self.selectLayout.addLayout(self.selectUpper)
        self.selectLayout.addLayout(self.selectLower)
        
        #------------------------------------------------------------
        # time layout
        #------------------------------------------------------------
        
        self.timeLayout = QtWidgets.QVBoxLayout()
        
        self.startInfo = QtWidgets.QLabel('Start: ----')
        self.stopInfo = QtWidgets.QLabel('Stop: ----')
        self.durationInfo = QtWidgets.QLabel('Duration: ----')
        
        self.changeTimeButton = QtWidgets.QPushButton('Change')
        self.changeTimeButton.setFixedWidth(100)
        self.changeTimeButton.clicked.connect(self.changeTime)
        self.changeTimeButton.setEnabled(False)
        
        
        self.timeLayout.addWidget(self.startInfo)
        self.timeLayout.addWidget(self.stopInfo)
        self.timeLayout.addWidget(self.durationInfo)
        self.timeLayout.addWidget(self.changeTimeButton)
        
        
        #------------------------------------------------------------
        # space layout
        #------------------------------------------------------------
        
        self.spaceLayout = QtWidgets.QGridLayout()
        
        borders = ['x_min', 'x_max', 'y_min', 'y_max']

        self.Border_sizes = {}
        
        for j, b in enumerate(borders):   
            border = QtWidgets.QLabel( b + ':')
            border_size = QtWidgets.QLabel('----')
            border_size.setObjectName(b)
            self.spaceLayout.addWidget(border, np.floor(j /2.), (j%2)*2)
            self.spaceLayout.addWidget(border_size, np.floor(j /2.), (j%2)*2+1)
            self.Border_sizes[b] = border_size
            
        self.changeCoordsButton = QtWidgets.QPushButton('Change')
        self.changeCoordsButton.setFixedWidth(100)
        self.changeCoordsButton.setEnabled(False)
        self.changeCoordsButton.clicked.connect(self.changeCoords)

        self.spaceLayout.addWidget(self.changeCoordsButton)
        
        #------------------------------------------------------------
        # smooth layout
        #------------------------------------------------------------
        self.smoothLayout = QtWidgets.QHBoxLayout()

        self.selectSmoothing = QtWidgets.QComboBox()
        for s in self.SMOOTHING:    
            self.selectSmoothing.addItem(s)

        self.smoothButton =QtWidgets.QPushButton('Apply Smoothing')
        self.smoothButton.clicked.connect(self.apply_smoothing)
        
        self.smoothLayout.addWidget(self.selectSmoothing)
        self.smoothLayout.addWidget(self.smoothButton)
        
        
        
        #------------------------------------------------------------
        # final layout
        #------------------------------------------------------------
        self.finalLayout = QtWidgets.QVBoxLayout()
  
        self.plotButton = QtWidgets.QPushButton('Plot')
        self.plotButton.clicked.connect(self.plot_trajectory)
        
        self.saveButton = QtWidgets.QPushButton('Stats and save')
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
         

        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.mainLayout)
        self.setCentralWidget(self.home)

    
    def init_browse_info(self): 
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        self.setDelim.setText(csv_dict['delim_read'])
        self.setSkipRows.setText(str(csv_dict['skip_rows_read']))
        
            
    def on_browse_clicked(self): 
        data_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')[0]

        if data_name.find('csv') < 0: 
            self.send_warning('Not a valid file type. Please use a file of type .csv .')
        else: 
            self.selectedFile.setText(data_name)
            self.INFO['data_file'] = data_name
            print( self.INFO['data_file'])
            
    def on_load_clicked(self): 
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        csv_dict['delim_read'] = self.setDelim.text()
        print(self.setDelim.text())
        csv_dict['skip_rows_read'] = int(self.setSkipRows.text())
        with open(self.CSV_INFO_FILE, 'w') as fp:
            json.dump(csv_dict, fp)
        
        self.table = tableWindow(self, self.INFO['data_file'])
        self.table.show()        
        
    

    def init_Info(self, tmp_file): 
        # called only by tableWindow
    
        # up to now this function gets only called by TableWindow
        self.TMP_FILE = tmp_file
        df = pd.read_csv(tmp_file, header = 0, sep = default.csv_delim)
        
        time_format = self.INFO['info']['time']
        self.INFO['start_time'] = ds.handle_timestamp(df['time'].values[0], time_format, self.DATE_FORMATS_FILE)
        self.INFO['stop_time'] = ds.handle_timestamp(df['time'].values[-1], time_format, self.DATE_FORMATS_FILE)
        
        self.INFO['start_frame'] = df['frames'].values[0]
        self.INFO['stop_frame'] = df['frames'].values[-1]
        
        self.INFO['duration_time'] = self.INFO['start_time'] - self.INFO['stop_time']
        self.INFO['duration_frame'] = int(df['frames'].values[-1]) - int(df['frames'].values[0])
        
        print([min(df[an + '_x'].values) for an in self.INFO['agent_names']])
        self.INFO['x_min'] = min(min(df[an + '_x'].values) for an in self.INFO['agent_names'])
        self.INFO['y_min'] = min(min(df[an + '_y'].values) for an in self.INFO['agent_names'])
        self.INFO['x_max'] = max(max(df[an + '_x'].values) for an in self.INFO['agent_names'])
        self.INFO['y_max'] = max(max(df[an + '_y'].values)for an in self.INFO['agent_names'])

        
        self.update_labels()
        
    def update_labels(self): 

        self.startInfo.setText('Start: ' + str(self.INFO['start_time']) + '\t (' + str(self.INFO['start_frame']) + ')')
        self.stopInfo.setText('Stop: '+ str(self.INFO['stop_time']) + '\t (' + str(self.INFO['stop_frame']) + ')')
        if self.INFO['info']['time'] in ['s', 'ms']: 
            dur = np.round(self.INFO['stop_time'] - self.INFO['start_time'], 2)
        elif self.INFO['info']['time'] == 'dt': 
            dur = self.INFO['stop_time'] - self.INFO['start_time']
            
        self.durationInfo.setText('Duration: ' + str(dur) + '\t (' + str(self.INFO['stop_frame'] - self.INFO['start_frame']) + ')')
        
        for key in self.Border_sizes: 
            self.Border_sizes[key].setText(str(np.round(float(self.INFO[key]), 2)))
        self.changeCoordsButton.setEnabled(True)
        self.changeTimeButton.setEnabled(True)
        
    def HLine(self):
    
        toto = QtWidgets.QFrame()
        toto.setFrameShape(QtWidgets.QFrame.HLine)
        toto.setFrameShadow(QtWidgets.QFrame.Sunken)
        return toto
        
    def changeTime(self):
        df = pd.read_csv(self.TMP_FILE, header = 0, sep = default.csv_delim)
        t = df['time'].values
        f = df['frames'].values
        
        self.time = timeWindow(self, t, f)
        self.time.show()   
        
    def changeCoords(self):
     
        borders = ['x_min', 'x_max', 'y_min', 'y_max']
        print(self.INFO)
        for key in self.Border_sizes: 
            self.INFO[key] = np.round(float(self.Border_sizes[key].text()), 2)
            self.spaceLayout.removeWidget(self.Border_sizes[key])
            sip.delete(self.Border_sizes[key])
            
        self.Border_sizes = {}
        
        if self.changeCoordsButton.text() == 'Change':
        
            for i, b in enumerate(borders): 
                le = QtWidgets.QLineEdit(str(self.INFO[b]))
                le.setValidator(QtGui.QDoubleValidator())
                self.Border_sizes[b] = le
                self.spaceLayout.addWidget(le, np.floor(i /2.), (i%2)*2+1)
            self.changeCoordsButton.setText('Ok')
            
        elif self.changeCoordsButton.text() == 'Ok':
        
            for i, b in enumerate(borders): 
                l = QtWidgets.QLabel(str(self.INFO[b]))
                self.Border_sizes[b] = l
                self.spaceLayout.addWidget(l, np.floor(i /2.), (i%2)*2+1)
            self.changeCoordsButton.setText('Change')
        print(self.INFO)

    def update_dicts(self, dict1, dict2): 
    
        for key in dict2: 
             dict1[key] = dict2[key]
             
             
    def plot_trajectory(self): 
        
        r = [(self.INFO['x_min'], self.INFO['y_min']), self.INFO['x_max'] - self.INFO['x_min'], self.INFO['y_max'] - self.INFO['y_min']]
        df = pd.read_csv(self.TMP_FILE, header = 0, sep = default.csv_delim)
                
        d = {}
        start_idx = np.where(df['frames'].values == self.INFO['start_frame'])[0][0]
        stop_idx = np.where(df['frames'].values == self.INFO['stop_frame'])[0][0]
        
        for an in self.INFO['agent_names']:
            d[an] = (df[an + '_x'].values[start_idx:stop_idx], df[an + '_y'].values[start_idx:stop_idx])
        
        
        self.trajectoryWindow = plotWindow(d, r)
        self.trajectoryWindow.exec_()
        
    def stats_and_save(self): 
        df, single_value_stats, indiv_stats, coll_stats = basic_stats.stats_and_save(self.TMP_FILE, self.INFO, self.CSV_INFO_FILE, self.PARAM_INFO_FILE)
        
        #name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', filter ='*.csv')[0]
        
        # order columns of df
        time = ['frames', 'time', 'seconds']
        agents = self.INFO['agent_names']
        specs = ['_x', '_y', '_angle']

        cols = df.columns
        new_order = []
        for t in time: 
            new_order.append(t)

        for a in agents: 
            for sp in specs: 
                new_order.append(a + sp)
            for in_st in indiv_stats: 
                new_order.append(a + in_st)
        for c in coll_stats: 
            for col in cols: 
                if col.find(c) > 0: 
                    new_order.append(col)

        df = df.reindex_axis(new_order, axis = 1)
        print(new_order)
        
        results_folder = self.makeResultsDir(default.results)
        
        
        df.to_csv(results_folder + '/timelines.csv', sep = default.csv_delim)   
        genStats.makeFile(results_folder, results_folder + '/timelines.csv', self.INFO, single_value_stats)
        self.home.close()
        
        
    def apply_smoothing(self):
        smooth = str(self.selectSmoothing.currentText())
        if smooth == None: 
            pass
        else: 
            df = pd.read_csv(self.TMP_FILE, header = 0, sep = default.csv_delim)
            if smooth ==  'MedFilter, k=5': 
                for an in self.INFO['agent_names']:
                    df[an + '_x'] = smoothing.medfilt(df[an + '_x'].values)
                    df[an + '_y'] = smoothing.medfilt(df[an + '_y'].values)
                    self.send_info('Trajectory is now smooth !')
                    self.INFO['filtered'] = True
                    
                    
    def send_info(self, text): 
        '''Sends information dialogue '''
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("INFO")
        retval = msg.exec_()
        
    def send_warning(self, text): 
        '''Sends information dialogue '''
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("Warning")
        retval = msg.exec_()
        
        
    def makeResultsDir(self, base_folder):
        '''Creates a folder labeled with the current date. Each calling of the processing unit will create a 
        new numbered subfolder '''

        now = datetime.datetime.now()
        now_str = now.strftime("%Y_%m_%d")
        dir_str = base_folder + now_str

        try:
            os.makedirs(dir_str)
        except OSError:
            pass
            
        created_subfolder = False
        i = 0
        while not created_subfolder: 
            subfolder_name = '{0:03}'.format(i)
            try:
                os.makedirs(dir_str + '/' + subfolder_name)
                created_subfolder = True
            except OSError:
                i +=1
                
        return dir_str + '/' + subfolder_name

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('main')
    #app.setGeometry(500, 600)

    main = mainWindow()
    main.show()

    sys.exit(app.exec_())
