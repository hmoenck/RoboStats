#!/usr/bin/python3.5
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets 
from PyQt5 import QtGui
from PyQt5.QtGui import QFont   
from PyQt5.QtCore import Qt

import os
import pandas as pd
import numpy as np
import datetime
import sip
from tableWindow import tableWindow
from timeWindow import timeWindow
from plotWindow import plotWindow
import data_processing.smoothing as smoothing
import data_processing.basic_stats as basic_stats
import data_processing.time_parsers as tp
import data_processing.generate_stats_file as genStats
import data_processing.generate_data2plot as genPlotData
import json
import messages 

import matplotlib 
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import plot_functions as pf



class mainWindow(QtWidgets.QMainWindow):

    INFO = {'start_time': -1, 'start_frame': -1, 'stop_time': -1, 'stop_frame': -1, 'duration_time': -1, 'duration_frame':-1,
            'x_min': -1, 'x_max': -1, 'y_min': -1, 'y_max': -1, 'filtered': False}
    
    SMOOTHING = ['Select Filter', 'MedFilter, k=5']
    STATS_OPTIONS = ['Simple', 'Fancy']
    
    DataLoaded = False

        
    try: 
        CSV_INFO_FILE = 'settings/csv_info.json'
        PARAM_INFO_FILE = 'settings/dict_data.json'
        DATE_FORMATS_FILE = 'settings/date_formats.json'
        FILENAMES_INFO_FILE = 'settings/file_names.json'
    except FileNotFoundError:
        twoFoldersup =  os.path.dirname(os.path.dirname(os.getcwd()))
        CSV_INFO_FILE = twoFoldersup + 'settings/csv_info.json'
        PARAM_INFO_FILE = twoFoldersup + 'settings/dict_data.json'
        DATE_FORMATS_FILE = twoFoldersup +'settings/date_formats.json'
        FILENAMES_INFO_FILE = twoFoldersup + 'settings/file_names.json'
    
    file_info = json.load(open(FILENAMES_INFO_FILE))
    TMP_FILE = file_info['tmp_file']
    

    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        self.setFixedSize(650,600)
        self.home()

    def home(self): 


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.titleFont = QFont('Helvetica', 12, QFont.Bold)
        self.normalFont = QFont('Courier', 11)
        
        #------------------------------------------------------------
        # select layout: responsible for selcting and loading files
        #------------------------------------------------------------
        
        self.selectFileTitle = QtWidgets.QLabel('File Selection')
        self.selectFileTitle.setFont(self.titleFont)
        
        self.selectedFile = QtWidgets.QLineEdit()
        self.browseButton = QtWidgets.QPushButton('Browse')
        self.browseButton.clicked.connect(self.on_browse_clicked)
        self.browseButton.setToolTip('Click to select a file for analyis')  
        
        self.delimLabel = QtWidgets.QLabel('File deliminator')
        self.setDelim = QtWidgets.QLineEdit()
        self.setDelim.setToolTip('Deliminator of the datafile to be analyzed')
        
        self.skipRowsLabel = QtWidgets.QLabel('Skip rows')
        self.setSkipRows = QtWidgets.QLineEdit()
        self.setSkipRows.setValidator(QtGui.QIntValidator())
        self.setSkipRows.setToolTip('First n rows of selected file will be skipped')
        self.init_browse_info()
        
        self.openInView = QtWidgets.QCheckBox('view')
        self.openInView.setCheckState(2)
        self.openInView.setEnabled(False)
        
        self.loadButton = QtWidgets.QPushButton('Load')
        self.loadButton.clicked.connect(self.on_load_clicked)
        self.loadButton.setToolTip("Loads selcted File into TableView mode (if 'view' is checked). \nIf 'view is unchecked, the settings of previous analysis will be used.\nThis may cause errors.")
                
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
        
        self.selectLayout = QtWidgets.QVBoxLayout()
        self.selectLayout.addWidget(self.selectFileTitle)
        self.selectLayout.addLayout(self.selectUpper)
        self.selectLayout.addLayout(self.selectLower)
        
        #------------------------------------------------------------
        # time layout: responsible for setting start and stop time
        #------------------------------------------------------------

        self.timeLayout = QtWidgets.QGridLayout()
        
        self.timeTitle = QtWidgets.QLabel('Track Time Information')
        self.timeTitle.setFont(self.titleFont)
        
        self.startLabel = QtWidgets.QLabel('Start:')
        self.startInfo = QtWidgets.QLabel('----')
        self.stopLabel = QtWidgets.QLabel('Stop:')
        self.stopInfo = QtWidgets.QLabel('----')
        self.durationLabel = QtWidgets.QLabel('Duration:')
        self.durationInfo = QtWidgets.QLabel('----')
        
        self.changeTimeButton = QtWidgets.QPushButton('Change')
        self.changeTimeButton.clicked.connect(self.changeTime)
        self.changeTimeButton.setToolTip('Click to change start / stop time of analysis.\nTo change time format please reload the file')
        
        self.timeLayout.addWidget(self.timeTitle, 0, 0)
        self.timeLayout.addWidget(self.startLabel, 1, 0)
        self.timeLayout.addWidget(self.startInfo, 1, 1)
        self.timeLayout.addWidget(self.stopLabel, 2, 0)
        self.timeLayout.addWidget(self.stopInfo, 2, 1)
        self.timeLayout.addWidget(self.durationLabel, 3, 0)
        self.timeLayout.addWidget(self.durationInfo, 3, 1)
        self.timeLayout.addWidget(self.changeTimeButton, 5, 2)
        
        
        #------------------------------------------------------------
        # space layout: responsible for setting world boundaries
        #------------------------------------------------------------
        
        self.spaceLayout = QtWidgets.QGridLayout()
        
        self.spaceTitle = QtWidgets.QLabel('World boundaries')
        self.spaceTitle.setFont(self.titleFont)
        self.spaceLayout.addWidget(self.spaceTitle, 0, 0)
        
        borders = ['x_min', 'x_max', 'y_min', 'y_max']

        self.Border_sizes = {}
        
        for j, b in enumerate(borders):   
            border = QtWidgets.QLabel( b + ':')
            border_size = QtWidgets.QLabel('----')
            border_size.setObjectName(b)
            self.spaceLayout.addWidget(border, np.floor(j /2.)+1, (j%2)*2)
            self.spaceLayout.addWidget(border_size, np.floor(j /2.)+1, (j%2)*2+1)
            self.Border_sizes[b] = border_size
            
        self.changeCoordsButton = QtWidgets.QPushButton('Change')
        self.changeCoordsButton.clicked.connect(self.changeCoords)
        self.changeCoordsButton.setToolTip('Click to change borders of the analyzed region')

        self.spaceLayout.addWidget(self.changeCoordsButton, np.ceil(len(borders)), 4)
        
        
        #------------------------------------------------------------
        # smooth layout: responsible for selcting filters and smoothing the trajectory
        #------------------------------------------------------------
        self.smoothLayout = QtWidgets.QHBoxLayout()
        
        self.smoothTitle = QtWidgets.QLabel('Filtering and Smoothing')
        self.smoothTitle.setFont(self.titleFont)        

        self.selectSmoothing = QtWidgets.QComboBox()
        for s in self.SMOOTHING:    
            self.selectSmoothing.addItem(s)

        self.smoothButton =QtWidgets.QPushButton('Apply Smoothing')
        self.smoothButton.clicked.connect(self.apply_smoothing)
        
        self.smoothLayout.addWidget(self.smoothTitle)
        self.smoothLayout.addWidget(self.selectSmoothing)
        self.smoothLayout.addWidget(self.smoothButton)
        
        
        #------------------------------------------------------------
        # inspect layout: responsible for generating plots
        #------------------------------------------------------------

        self.plotLayout = QtWidgets.QGridLayout()
        self.TYPES = ['Select', 'Trajectory', 'Timeline', 'Histogramm', 'Boxplot']
        self.SPECS = {'Select': ['-------'], 'Trajectory': ['--------'], 'Timeline': ['Speed', 'Distance', 'Angle'], 
    'Histogramm': ['Speed', 'Distance', 'Angle'] , 'Boxplot': ['Speed', 'Distance']}
        
        self.plotTitle = QtWidgets.QLabel('Inspect Data')
        self.plotTitle.setFont(self.titleFont)
        
        self.selectType = QtWidgets.QComboBox(self)
        for t in self.TYPES: 
            self.selectType.addItem(t)
        self.selectType.currentIndexChanged.connect(self.setSelectSpec)
        self.selectType.setToolTip('Choose the type of plot to be created')
        
        self.selectSpec = QtWidgets.QComboBox(self)
        for t in self.SPECS['Select']: 
            self.selectSpec.addItem(t)
        self.selectSpec.setToolTip('Choose the data for display')
        
        self.inspectButton = QtWidgets.QPushButton('Inspect')
        self.inspectButton.clicked.connect(self.on_pushed_inspect)
        self.inspectButton.setToolTip('Clicking this button will open a window showing the selected plot.')
        
        self.plotLayout.addWidget(self.plotTitle, 0, 0)
        self.plotLayout.addWidget(self.selectType, 1, 0)
        self.plotLayout.addWidget(self.selectSpec, 1, 1)
        self.plotLayout.addWidget(self.inspectButton, 1, 2)
        
        #------------------------------------------------------------
        # final layout
        #------------------------------------------------------------
        self.finalLayout = QtWidgets.QHBoxLayout()

#        self.selectStats= QtWidgets.QComboBox()
#        for s in self.STATS_OPTIONS:    
#            self.selectStats.addItem(s)
        self.saveOptions = QtWidgets.QPushButton('Options')
        self.saveOptions.clicked.connect(self.on_save_options_clicked)
                
        self.saveButton = QtWidgets.QPushButton('Save')
        self.saveButton.clicked.connect(self.stats_and_save)
        

        self.finalLayout.addWidget(self.saveOptions)
        self.finalLayout.addWidget(self.saveButton)
        
        #------------------------------------------------------------
        # general layout
        #------------------------------------------------------------
       
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.addLayout(self.selectLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.timeLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.spaceLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.smoothLayout)
        self.mainLayout.addWidget(self.HLine())
        self.mainLayout.addLayout(self.plotLayout)
        self.mainLayout.addWidget(self.HLine())
        
        self.finalTitle = QtWidgets.QLabel('Statistics')
        self.finalTitle.setFont(self.titleFont)
        self.mainLayout.addWidget(self.finalTitle)
        self.mainLayout.addLayout(self.finalLayout)
         

        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.mainLayout)
        self.home.setFont(self.normalFont)
        self.setCentralWidget(self.home)

    
    def init_browse_info(self): 
        ''' reads information about reading csv files (i.e. seperator and number of rows to skip) from a json-dictionary
        and uses these values to initialize Line edit elemets that can be adjusted by the user'''
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        self.setDelim.setText(csv_dict['read']['delim'])
        self.setSkipRows.setText(str(csv_dict['read']['skip_rows']))
        
            
    def on_browse_clicked(self): 
        ''' When the 'Browse' Button is clicked this function opens a File selection dialog, checks wheteher the selected file is 
        of correct type (csv) and writes the filepath to the upper line edit'''
        data_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')[0]

        if data_name.find('csv') < 0: 
            messages.send_warning('Not a valid file type. Please use a file of type .csv .')
        else: 
            self.selectedFile.setText(data_name)
            self.INFO['data_file'] = data_name
            print(self.INFO['data_file'])

            
    def on_load_clicked(self):
        ''' When the 'Load' Button is clicked, this function passes the filkename to tableWindow. csv parameters are read in from 
        the respective line edits, and saved to json for further use'''
       
        if len(self.selectedFile.text()) == 0: 
            messages.send_warning('No File loaded')
            return
            
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        csv_dict['read']['delim'] = self.setDelim.text()
        csv_dict['read']['skip_rows'] = int(self.setSkipRows.text())
        with open(self.CSV_INFO_FILE, 'w') as fp:
            json.dump(csv_dict, fp)
        
        self.table = tableWindow(self, self.INFO['data_file'])
        self.table.show()        
        
    
    def init_Info(self, tmp_file): 
        ''' tableWindow calles this function, when 'Ok' is pressed. The tmp file created by table window is used to initialize
        information in mainWindow'''
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        delim = csv_dict['write']['delim']
        
        self.TMP_FILE = tmp_file
        df = pd.read_csv(tmp_file, header = 0, sep = delim)
        
        time_format = self.INFO['info']['time']
        if tp.handle_timestamp(df['time'].values[0], time_format, self.DATE_FORMATS_FILE) == None: 
            messages.send_warning('Time format invalid!')
            return False
        
        self.INFO['start_time'] = df['seconds'].values[0]    
        self.INFO['stop_time'] = df['seconds'].values[-1]
        
#        self.INFO['start_time'] = tp.handle_timestamp(df['time'].values[0], time_format, self.DATE_FORMATS_FILE)
#        self.INFO['stop_time'] = tp.handle_timestamp(df['time'].values[-1], time_format, self.DATE_FORMATS_FILE)
        
        self.INFO['start_frame'] = df['frames'].values[0]
        self.INFO['stop_frame'] = df['frames'].values[-1]
        
        self.INFO['duration_time'] = self.INFO['start_time'] - self.INFO['stop_time']
        self.INFO['duration_frame'] = int(df['frames'].values[-1]) - int(df['frames'].values[0])        

        
        self.INFO['x_min'] = min(min(df[an + '_x'].values) for an in self.INFO['agent_names'])
        self.INFO['y_min'] = min(min(df[an + '_y'].values) for an in self.INFO['agent_names'])
        self.INFO['x_max'] = max(max(df[an + '_x'].values) for an in self.INFO['agent_names'])
        self.INFO['y_max'] = max(max(df[an + '_y'].values)for an in self.INFO['agent_names'])
        
        self.update_labels()
        self.DataLoaded = True

        
    def update_labels(self): 
        ''' Updates the labels displayed in mainWindow (start/stop/duration time, x/y - min/max). Gets called by timeWindow
        and the changeCoords function as well as when initializing the disply after loading a new dataset'''
        
#        if self.INFO['info']['time'] in ['s', 'ms']: 
#            dur = str(np.round(self.INFO['stop_time'] - self.INFO['start_time'], 2))
#            start = str(np.round(self.INFO['start_time'], 2))
#            stop = str(np.round(self.INFO['stop_time'], 2))
#            
#        elif self.INFO['info']['time'] == 'dt': 
#            dur = str(self.INFO['stop_time'] - self.INFO['start_time'])
#            start = str(self.INFO['start_time'])
#            stop = str(self.INFO['stop_time'])

        dur = str(np.round(self.INFO['stop_time'] - self.INFO['start_time'], 2))
        start = str(np.round(self.INFO['start_time'], 2))
        stop = str(np.round(self.INFO['stop_time'], 2))
        
        self.startInfo.setText(start + ' s \t (' + str(self.INFO['start_frame']) + ' frames)')
        self.stopInfo.setText(stop + ' s \t (' + str(self.INFO['stop_frame']) + ' frames)')
        self.durationInfo.setText(dur + ' s \t (' + str(self.INFO['stop_frame'] - self.INFO['start_frame']) + ' frames)')

#        self.startInfo.setText(start + ' ' + str(self.INFO['info']['time']) + '\t (' + str(self.INFO['start_frame']) + ' frames)')
#        self.stopInfo.setText(stop + ' ' + str(self.INFO['info']['time']) +'\t (' + str(self.INFO['stop_frame']) + ' frames)')
#        self.durationInfo.setText(dur + ' ' + str(self.INFO['info']['time']) +'\t (' + str(self.INFO['stop_frame'] - self.INFO['start_frame']) + ' frames)')
        
        for key in self.Border_sizes: 
            self.Border_sizes[key].setText(str(np.round(float(self.INFO[key]), 2)))


    def changeTime(self):
        ''' when the 'Change'Button is clicked on the time Layout, this function opens a 
        window with sliders to set start and stop time. The selected values are passed back 
        to mainWindows INFO dictionary'''
        
        if self.DataLoaded == False: 
            messages.send_warning('No File loaded')
            return
        
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        delim = csv_dict['write']['delim']
        df = pd.read_csv(self.TMP_FILE, header = 0, sep = delim)
        #t = df['time'].values
        t = df['seconds'].values
        f = df['frames'].values
        
        self.time = timeWindow(self, t, f, self.INFO)
        self.time.show()   
        
    def changeCoords(self):
        ''' when the 'Change'Button is clicked on the space Layout, this function changes the labels for x and y borders 
        to Line edits where individula changes can be made. The label of the 'Change' Button is set to ok and when presed, the 
        line edits are switched back to labels and the selected coordinate values are save d to the INFO dictionary.'''
        
        if self.DataLoaded == False: 
            messages.send_warning('No File loaded')
            return
     
        borders = ['x_min', 'x_max', 'y_min', 'y_max']
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
                self.spaceLayout.addWidget(le, np.floor(i /2.) +1, (i%2)*2+1)
            self.changeCoordsButton.setText('Ok')
            
        elif self.changeCoordsButton.text() == 'Ok':
        
            for i, b in enumerate(borders): 
                l = QtWidgets.QLabel(str(self.INFO[b]))
                self.Border_sizes[b] = l
                self.spaceLayout.addWidget(l, np.floor(i /2.) +1, (i%2)*2+1)
            self.changeCoordsButton.setText('Change')


    def update_dicts(self, dict1, dict2): 
        ''' updates the values of one dictionary with the values of another, gets called by tableWindow'''
    
        for key in dict2: 
             dict1[key] = dict2[key]

    
    def setSelectSpec(self, index): 
        ''' Updates the second dropdown menu in the inspect layout accourding to the value of the first'''
        self.selectSpec.clear()
        data = str(self.selectType.currentText())
        self.selectSpec.addItems(self.SPECS[data])   

    
    def on_pushed_inspect(self): 
        '''When the inspect Button is clicked this function cuts the data accoring to the current 
        temporal and spatial borders. Then the data is prepared for plotting depending on the chosen 
        format finally plotWindow is called for display.'''
        
        if self.DataLoaded == False: 
            messages.send_warning('No File loaded')
            return
        
        df = basic_stats.cut_timelines(self.TMP_FILE, self.INFO, self.CSV_INFO_FILE)  
        representation = str(self.selectType.currentText())
        datatype = str(self.selectSpec.currentText())
        
        data2plot = genPlotData.makeData2Plot(df, representation, datatype, self.INFO, self.PARAM_INFO_FILE)
        
        if data2plot == None: 
            messages.send_warning('selection invalid')
            return
        else:
            self.pW = plotWindow(data2plot, representation, datatype)
            self.pW.exec_()

        
    def stats_and_save(self): 
        ''' when clickig the 'Stats and Save' Button this function calles the stats and save method 
        from basic stats which creates two csv files: one with timelines and another with single values 
        (like mean, var, borders, etc.). Then a File selection dialog is opened and at the chosen 
        location a folder is created where the results are saved. Finally a 'goodbye' dialog is sent
        informing the user where results were saved and asking wheter they want to continue or close 
        the application'''
            
        if self.DataLoaded == False: 
            messages.send_warning('No File loaded')
            return

        if False: 
            pass
        else:
            df = basic_stats.cut_timelines(self.TMP_FILE, self.INFO, self.CSV_INFO_FILE)   
            
            indiv_stats = ['_vx', '_vy', '_speed']
            coll_stats = ['_dist']
            
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
            
            
            results_folder_super = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
            results_folder = self.makeResultsDir(results_folder_super + '/')
            
            csv_dict = json.load(open(self.CSV_INFO_FILE))
            delim = csv_dict['write']['delim']
            df.to_csv(results_folder + '/timelines.csv', sep = delim)   
            genStats.makeFile(results_folder, results_folder + '/timelines.csv', self.INFO, self.CSV_INFO_FILE, self.FILENAMES_INFO_FILE)

            #pf.plot_things(df, results_folder, self.INFO['agent_names'])
            
            messages.send_goodbye(results_folder)

        
        
    def apply_smoothing(self):
        ''' If a filter is selected in the dropdown menu and the 'Apply Smoothing' button is pressed, the respective 
        smoothing function is applied on the whole trajectory (not only the selected parts). '''
        
        if self.DataLoaded == False: 
            messages.send_warning('No File loaded')
            return
        
        smooth = str(self.selectSmoothing.currentText())
        if smooth == None: 
            pass
        else: 
            csv_dict = json.load(open(self.CSV_INFO_FILE))
            delim = csv_dict['write']['delim']
            
            df = pd.read_csv(self.TMP_FILE, header = 0, sep = delim)
            if smooth ==  'MedFilter, k=5': 
                for an in self.INFO['agent_names']:
                    df[an + '_x'] = smoothing.medfilt(df[an + '_x'].values)
                    df[an + '_y'] = smoothing.medfilt(df[an + '_y'].values)

                messages.send_info('Trajectory is now smooth !')
                self.INFO['filtered'] = True
                    
    def on_save_options_clicked(self): 
        pass                    


        
    def makeResultsDir(self, base_folder):
        '''Creates a folder labeled with the current date. Each calling of the processing unit will create a
        new numbered subfolder '''

        now = datetime.datetime.now()
        now_str = now.strftime("%Y_%m_%d")
        dir_str = base_folder + 'BioTrackerAnalysis_' + now_str

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
        
        
    def HLine(self):
        '''Creates a sunken horizontal line.'''
    
        toto = QtWidgets.QFrame()
        toto.setFrameShape(QtWidgets.QFrame.HLine)
        toto.setFrameShadow(QtWidgets.QFrame.Sunken)
        return toto




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('BioTrackerAnalysis')

    main = mainWindow()
    main.show()

    sys.exit(app.exec_())
