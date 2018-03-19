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
from optionsWindow import optionsWindow
from subregionWindow import subregionWindow
import data_processing.smoothing as smoothing
import data_processing.basic_stats as basic_stats
import data_processing.time_parsers as tp
import data_processing.generate_stats_file as genStats
import data_processing.generate_data2plot as genPlotData
import stats.TE as TE
import json
import messages 

import matplotlib 
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import plot_functions as pf



class mainWindow(QtWidgets.QMainWindow):

    INFO = {'start_time': -1, 'start_frame': -1, 'stop_time': -1, 'stop_frame': -1, 'duration_time': -1, 'duration_frame':-1,
            'x_min': -1, 'x_max': -1, 'y_min': -1, 'y_max': -1, 'filtered': False}
            
    WORLD_BORDERS= ['x_min', 'x_max', 'y_min', 'y_max']
    
    SMOOTHING = ['Select Filter', 'MedFilter, k=5']
    STATS_OPTIONS = ['Simple', 'Fancy']
    
    
    DataLoaded = False

        
    try: 
        CSV_INFO_FILE = 'settings/csv_info.json'
        PARAM_INFO_FILE = 'settings/dict_data.json'
        DATE_FORMATS_FILE = 'settings/date_formats.json'
        OPTIONS_INFO_FILE = 'settings/options.json'
        SUBREGIONS_INFO_FILE = 'settings/subregions.json'
        TE_PARAMS_FILE = 'settings/TE_params.json'
        options = json.load(open(OPTIONS_INFO_FILE))
        
    except FileNotFoundError:
        twoFoldersup =  os.path.dirname(os.path.dirname(os.getcwd()))
        CSV_INFO_FILE = twoFoldersup + 'settings/csv_info.json'
        PARAM_INFO_FILE = twoFoldersup + 'settings/dict_data.json'
        DATE_FORMATS_FILE = twoFoldersup +'settings/date_formats.json'
        OPTIONS_INFO_FILE = twoFoldersup + 'settings/options.json'
        SUBREGIONS_INFO_FILE = twoFoldersup + 'settings/subregions.json'
        TE_PARAMS_FILE = twoFoldersup + 'settings/TE_params.json'
    
    options = json.load(open(OPTIONS_INFO_FILE))
    TMP_FILE = options['tmp_file']
    
    

    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        self.setFixedSize(650,600)  
        
#        self.statusBar().showMessage('Ready')
#        self.progressBar = QtWidgets.QProgressBar()
        

        
        
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
        options = json.load(open(self.OPTIONS_INFO_FILE))
        self.openInView.setCheckState(options['view'])
        
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
        
        

        self.Border_sizes = {}
        
        for j, b in enumerate(self.WORLD_BORDERS):   
            border = QtWidgets.QLabel( b + ':')
            border_size = QtWidgets.QLabel('----')
            border_size.setObjectName(b)
            self.spaceLayout.addWidget(border, np.floor(j /2.)+1, (j%2)*2)
            self.spaceLayout.addWidget(border_size, np.floor(j /2.)+1, (j%2)*2+1)
            self.Border_sizes[b] = border_size
            
        self.addSubregionsButton = QtWidgets.QPushButton('Add Subregions')
        self.addSubregionsButton.clicked.connect(self.addSubregions)
        self.addSubregionsButton.setToolTip('Click to add subregions for further analysis')
        self.spaceLayout.addWidget(self.addSubregionsButton, np.ceil(len(self.WORLD_BORDERS)), 2)

        self.changeCoordsButton = QtWidgets.QPushButton('Change')
        self.changeCoordsButton.clicked.connect(self.changeCoords)
        self.changeCoordsButton.setToolTip('Click to change borders of the analyzed region')
        self.spaceLayout.addWidget(self.changeCoordsButton, np.ceil(len(self.WORLD_BORDERS)), 3)
        
        
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
        self.TYPES = ['Select', 'Trajectory', 'Heatmap', 'Timeline', 'Histogramm', 'Boxplot']
        self.SPECS = {'Select': ['-------'], 'Trajectory': ['--------'], 'Heatmap': ['--------'], 'Timeline': ['Speed', 'Distance', 'Angle'], 'Histogramm': ['Speed', 'Distance', 'Angle'] , 'Boxplot': ['Speed', 'Distance']}
        
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
        
        self.finalTitle = QtWidgets.QLabel('Finalize')
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
        of correct type (csv) and writes the filepath to the upper line edit. Additionally the path to the selected datafile will be a
        added to the options dictionary, containing default paths. '''
        options = json.load(open(self.OPTIONS_INFO_FILE))
        data_folder = options['data_folder']
        
        if len(data_folder) == 0: 
            data_folder = os.getenv("HOME")
            
        data_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',  data_folder)[0]
        options['data_folder'] = data_name[:data_name.rfind('/')]
        
        with open(self.OPTIONS_INFO_FILE, 'w') as op:
            json.dump(options, op)
        
        if data_name.find('csv') < 0: 
            messages.send_warning('Not a valid file type. Please use a file of type .csv .')
        else: 
            self.selectedFile.setText(data_name)
            self.INFO['data_file'] = data_name
            print(self.INFO['data_file'])

            
    def on_load_clicked(self):
        ''' When the 'Load' Button is clicked the data file specified in the line edit nest to the 
        Browse Buttonis loaded for further processing. If view is checked this is done via the display 
        in table window. Else the loading is done internally. In any case csv parameters are read from 
        the respective line edits in mainWindow and and saved to json for further use.'''
       
        # check if file was selected
        if len(self.selectedFile.text()) == 0: 
            messages.send_warning('No File loaded')
            return
        
        # read csv parameters and save to json    
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        csv_dict['read']['delim'] = self.setDelim.text()
        csv_dict['read']['skip_rows'] = int(self.setSkipRows.text())
        
        with open(self.CSV_INFO_FILE, 'w') as fp:
            json.dump(csv_dict, fp)
        
        # if view is checked open tableWindow    
        if self.openInView.checkState() == 2:    
            self.table = tableWindow(self, self.INFO['data_file'])
            self.table.show()        
        
        else: 
        #------------------------------------------------------------------------------------------- 
        # in this section the file is loaded using settings from previous uses. The procedure is 
        # similar to tableWindow's build_csv()-function.
        #------------------------------------------------------------------------------------- -----
            # use column labels from previos session
            columns = json.load(open(self.PARAM_INFO_FILE))
            time_labels = columns['time_labels']
            agent_names = columns['agent_names']
            agent_specs = columns['agent_specifications']
            other = columns['other']
            
            # use csv params from mainWindow to load selected csv into pandas
            try:
                df = pd.read_csv(self.selectedFile.text(), 
                                header = 0, 
                                sep = csv_dict['read']['delim'], 
                                skiprows = csv_dict['read']['skip_rows'], 
                                comment = csv_dict['read']['comment'])
            except ValueError: 
                messages.send_warning("Something went wrong ! \nPlease enable 'view' and try again.")
                return
                
            # define columns 
            df_columns = {
            'TIME': {time_labels[i] : columns[time_labels[i]] for i in range(len(time_labels))}, 
            'AGENTS': {}, 
            'OTHER': {other[i] : columns[other[i]] for i in range(len(other))} } 
                
            for k in range(len(agent_names)): 
                for j in range(len(agent_specs)): 
                    key = agent_names[k]+agent_specs[j]    
                    df_columns['AGENTS'][key] = columns[key]
            
            # read the indices and names of columns of interest into a list
            real_indices = []
            titles = []
            for key1 in df_columns.keys(): 
                for key2 in df_columns[key1].keys(): 
                    titles.append(key2)
                    real_indices.append(int(df_columns[key1][key2])-1)

            # try to select the columns of interest in the loaded pandas
            try:
                df_new = df.iloc[:, real_indices]
            except IndexError: 
                messages.send_warning("Something went wrong ! \nPlease enable 'view' and try again.")
                return
            
            # check for NaN values and delete the respective rows    
            df_new.columns = titles
            df_new = df_new.dropna(how = 'any') 
            
            # save pandas to temporary csv file 
            df_new.to_csv(self.TMP_FILE, sep = csv_dict['write']['delim'])
            print('temporary file saved to', self.TMP_FILE)
            
            # perform basic_stats i.e convert time to seconds and calc speed and dist 
            self.INFO['agent_names'] = agent_names
            try: 
                basic_stats.speed_and_dist(self.TMP_FILE, self.INFO, self.CSV_INFO_FILE, self.PARAM_INFO_FILE)
            except TypeError: 
                messages.send_warning("Something went wrong ! \nPlease enable 'view' and try again.")
                return 
            
            # init the display of mainWindow and self.INFO with values read from datafile   
            self.INFO['info'] = columns['info']
            if self.init_Info(self.TMP_FILE) == False:
                messages.send_warning("Something went wrong ! \nPlease enable 'view' and try again.")
                return
            
            # save the state of the view button
            options = json.load(open(self.OPTIONS_INFO_FILE))
            options['view'] = self.openInView.checkState()
            with open(self.OPTIONS_INFO_FILE, 'w') as fp:
                json.dump(options, fp)
        
    
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
        
        self.INFO['start_frame'] = df['frames'].values[0]
        self.INFO['stop_frame'] = df['frames'].values[-1]
        
        
        try: 
            self.INFO['duration_time'] = self.INFO['start_time'] - self.INFO['stop_time']
            self.INFO['duration_frame'] = int(df['frames'].values[-1]) - int(df['frames'].values[0])        
        except (TypeError, ValueError) as e: 
            return False
        
        self.INFO['x_min'] = min(min(df[an + '_x'].values) for an in self.INFO['agent_names'])
        self.INFO['y_min'] = min(min(df[an + '_y'].values) for an in self.INFO['agent_names'])
        self.INFO['x_max'] = max(max(df[an + '_x'].values) for an in self.INFO['agent_names'])
        self.INFO['y_max'] = max(max(df[an + '_y'].values)for an in self.INFO['agent_names'])
        
        self.update_labels()
        self.DataLoaded = True

        
    def update_labels(self): 
        ''' Updates the labels displayed in mainWindow (start/stop/duration time, x/y - min/max). Gets called by timeWindow
        and the changeCoords function as well as when initializing the disply after loading a new dataset'''
        

        dur = str(np.round(self.INFO['stop_time'] - self.INFO['start_time'], 2))
        start = str(np.round(self.INFO['start_time'], 2))
        stop = str(np.round(self.INFO['stop_time'], 2))
        
        self.startInfo.setText(start + ' s \t (' + str(self.INFO['start_frame']) + ' frames)')
        self.stopInfo.setText(stop + ' s \t (' + str(self.INFO['stop_frame']) + ' frames)')
        self.durationInfo.setText(dur + ' s \t (' + str(self.INFO['stop_frame'] - self.INFO['start_frame']) + ' frames)')
        
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
        t = df['seconds'].values
        f = df['frames'].values
        
        self.tW = timeWindow(self, t, f, self.INFO)
        self.tW.show()   
        
    def changeCoords(self):
        ''' when the 'Change'Button is clicked on the space Layout, this function changes the labels for x and y borders 
        to Line edits where individula changes can be made. The label of the 'Change' Button is set to ok and when presed, the 
        line edits are switched back to labels and the selected coordinate values are save d to the INFO dictionary.'''
        
        if self.DataLoaded == False: 
            messages.send_warning('No File loaded')
            return
     
        for key in self.Border_sizes: 
            self.INFO[key] = np.round(float(self.Border_sizes[key].text()), 2)
            self.spaceLayout.removeWidget(self.Border_sizes[key])
            sip.delete(self.Border_sizes[key])
            
        self.Border_sizes = {}
        
        if self.changeCoordsButton.text() == 'Change':
        
            for i, b in enumerate(self.WORLD_BORDERS): 
                le = QtWidgets.QLineEdit(str(self.INFO[b]))
                le.setValidator(QtGui.QDoubleValidator())
                self.Border_sizes[b] = le
                self.spaceLayout.addWidget(le, np.floor(i /2.) +1, (i%2)*2+1)
            self.changeCoordsButton.setText('Ok')
            
        elif self.changeCoordsButton.text() == 'Ok':
            self.checkSubregions()
            for i, b in enumerate(self.WORLD_BORDERS): 
                l = QtWidgets.QLabel(str(self.INFO[b]))
                self.Border_sizes[b] = l
                self.spaceLayout.addWidget(l, np.floor(i /2.) +1, (i%2)*2+1)
            self.changeCoordsButton.setText('Change')


    def addSubregions(self): 
        if self.DataLoaded == False: 
            messages.send_warning('No File loaded')
            return
         
        else: 
            world_borders = {}
            for wb in self.WORLD_BORDERS:
                world_borders[wb] = self.INFO[wb]
                
            self.srW = subregionWindow(self, world_borders, self.SUBREGIONS_INFO_FILE)
            self.srW.show()   
                

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
        
        # This is simply to show the bar
#        self.progressBar.setGeometry(30, 40, 200, 25)
#        self.progressBar.setValue(0)
#        self.statusBar().addPermanentWidget(self.progressBar)    
        #-------------------------------------------------------------------------------------------
        # saving preparation section
        #-------------------------------------------------------------------------------------------   
        
        #check if subregions are in agreement with current world_borders
        self.checkSubregions()

        
        options = json.load(open(self.OPTIONS_INFO_FILE))
        
        # read prefered save folder from options file, default is HOME
        save_folder = options['save_folder']
        if len(save_folder) == 0: 
            save_folder = os.getenv("HOME")
        
        # open prefered save folder (or HOME) and let user confirm
        results_folder_super = \
             str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", save_folder, QtWidgets.QFileDialog.ShowDirsOnly))
        options['save_folder'] = results_folder_super
        
        # save new prefered save folder
        with open(self.OPTIONS_INFO_FILE, 'w') as of: 
            json.dump(options, of)
        
        # create results folder within save folder 
        results_folder = self.makeResultsDir(results_folder_super + '/')
        
        # read parameters for saving from options file
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        delim = csv_dict['write']['delim']
        time_file = options['timeline_file']
        
        #self.progressBar.setValue(10)
        #-------------------------------------------------------------------------------------------
        # create timelines.csv and info.csv
        #------------------------------------------------------------------------------------------- 
        
        # cut data dataframe according to current time and space settings
        df = basic_stats.cut_timelines(self.TMP_FILE, self.INFO, self.CSV_INFO_FILE)   
        
        # sort the columns of dataframe
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

        df = df.reindex(new_order, axis = 1)

        # save ordered dataframe and create info.csv
        df.to_csv(results_folder + '/' + time_file, sep = delim)   
        
        #genStats.makeFile(results_folder, results_folder + '/' + time_file, self.INFO, self.CSV_INFO_FILE, self.OPTIONS_INFO_FILE)
        genStats.makeFile(results_folder, df, self.INFO, self.CSV_INFO_FILE, self.OPTIONS_INFO_FILE)
        
        #self.progressBar.setValue(20)
        #-------------------------------------------------------------------------------------------
        # plotting section
        #------------------------------------------------------------------------------------------- 
        plot_instructions = options['plot_selection']
        pf.plot_things(df, results_folder, self.INFO['agent_names'], plot_instructions)

        #self.progressBar.setValue(30)
        #-------------------------------------------------------------------------------------------
        # TE section
        #-------------------------------------------------------------------------------------------
        if options['TE']: 
            te_params = json.load(open(self.TE_PARAMS_FILE))
            
            TE_done = TE.TE(results_folder + '/' + time_file, results_folder, '/TE.csv', '/TE.jpg', start_frame = te_params['start_frame'], maxtime = te_params['max_time'], k_te = te_params['k_te'], frame_step = te_params['frame_step'])
            
        #self.progressBar.setValue(70)
        #-------------------------------------------------------------------------------------------
        # Subregions section
        #-------------------------------------------------------------------------------------------
        
        sub_info = {'start_frame':self.INFO['start_frame'], 'stop_frame':self.INFO['stop_frame'],\
                    'start_time':self.INFO['start_time'], 'stop_time':self.INFO['stop_time'],\
                    'agent_names':self.INFO['agent_names'], 'data_file':self.INFO['data_file'], 'filtered':self.INFO['filtered']}
        subregions = json.load(open(self.SUBREGIONS_INFO_FILE))
        for sub in subregions.keys():
            for wb in self.WORLD_BORDERS:
                sub_info[wb] = subregions[sub][wb]
            
            sub_df = basic_stats.cut_timelines(self.TMP_FILE, sub_info, self.CSV_INFO_FILE) 
            
            genStats.makeFile(os.getcwd(), sub_df, sub_info, self.CSV_INFO_FILE, self.OPTIONS_INFO_FILE, region = sub)
            
            info1 = pd.read_csv(results_folder + '/info.csv')
            info2 = pd.read_csv('info.csv')
            infofiles = [info1, info2]
            combined = pd.concat(infofiles)
            combined = combined[info1.columns]
            combined = combined.dropna(axis=1)
            combined.to_csv(results_folder + '/info.csv')
            
        #self.progressBar.setValue(100)
        
#            from scipy.stats import spearmanr
#            from scipy.stats import pearsonr
#            for i in range(len(self.INFO['agent_names'])): 
#                for j in range(i+1, len(self.INFO['agent_names'])): 
#                    a0 = self.INFO['agent_names'][i]
#                    a1 = self.INFO['agent_names'][j]
#                    
#                
#                    print(a0 + ''+ a1 )
#                    print('Pearson Corr Speed:  ', pearsonr(df[a0 + '_speed'].values, df[a1 + '_speed'].values))
#                    print('Pearson Corr vx:  ', pearsonr(df[a0 + '_vx'].values, df[a1 + '_vx'].values))           
#                    print('Pearson Corr vy:  ', pearsonr(df[a0 + '_vy'].values, df[a1 + '_vy'].values))      
#                    print('Np.Corr Speed: ', np.correlate(df[a0 + '_speed'].values, df[a1 + '_speed'].values))   
#                    
#                    print('Pearson x: ', pearsonr(df[a0 + '_x'].values, df[a1 + '_x'].values))     
#                    print('Np.Corr x: ', np.correlate(df[a0 + '_x'].values, df[a1 + '_x'].values))   
        messages.send_goodbye(self, results_folder)

        
        
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
        self.oW = optionsWindow(self)  
        self.oW.show()                

    def checkSubregions(self): 
        subregions = json.load(open(self.SUBREGIONS_INFO_FILE))
        for sub in subregions.keys():
            for wb in self.WORLD_BORDERS:
                if (wb.find('min') > -1) and (subregions[sub][wb] < self.INFO[wb]): 
                    messages.send_warning('Currently selcted Subregions exceed world borders')
                    return
                elif (wb.find('max') > -1) and (subregions[sub][wb] > self.INFO[wb]): 
                    messages.send_warning('Currently selcted Subregions exceed world borders')
                    return
                else: 
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
