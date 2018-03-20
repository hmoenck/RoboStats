#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv

import sip

from PyQt5 import QtWidgets 
from PyQt5 import QtGui 
from PyQt5 import QtCore
import numpy as np
import pandas as pd
from numpy import random
import sys
from agentWindow import agentWindow
from settingsWindow import settingsWindow
import data_processing.basic_stats as basic_stats
import messages
import json


class PandasModel(QtCore.QAbstractTableModel):
    """ Class to populate a table view with a pandas dataframe """
    
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def setheaderData(self, col, orientation, role):
#        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
#            return self._data.columns[col]
        return None


class tableWindow(QtWidgets.QWidget):
    ''' presents a selected .csv file, allows to identify and name relevant columns. The resulting 
    columns (with respective names) will be saved as 'tmp.csv' to be further processed by mainWindow'''


    def __init__(self, parentWindow, fileName):
    #def __init__(self, fileName):

        #super(tableWindow, self).__init__()
        super(tableWindow, self).__init__(parentWindow)
        self.parentWindow = parentWindow
        self.fileName = fileName #name of the selected csv
        self.nColumns = 0 #number of columns of the original file 
        
        self.PARAM_INFO_FILE = self.parentWindow.PARAM_INFO_FILE
        self.CSV_INFO_FILE = self.parentWindow.CSV_INFO_FILE
        self.TMP_FILE_TITLE = self.parentWindow.TMP_FILE
        
        self.initParams()


        self.home()
        
        
    def home(self): 
    
        df = self.open_data()
        
        self.nColumns = len(df.columns)
        self.model = PandasModel(df)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        


        # ---------------------------------------------------------------------
        # COLUMN LAYOUT
        # ---------------------------------------------------------------------

        self.checkBoxLayout = QtWidgets.QGridLayout()
        
        self.draw_time_labels(init = True)
        self.draw_agent_names(init = True) # set the agent columns
        
        
        self.otherParamsLayout = QtWidgets.QGridLayout()
        self.draw_additional_labels(init = True)


        # ---------------------------------------------------------------------
        # Buttons
        # ---------------------------------------------------------------------
   
        self.saveButton = QtWidgets.QPushButton(self)
        self.saveButton.setText("OK")
        self.saveButton.clicked.connect(self.save)
        
        self.addParamsButton = QtWidgets.QPushButton(self)
        self.addParamsButton.setText("Add Parameters")
        self.addParamsButton.clicked.connect(self.addParams)
        
        self.changeAgentsButton = QtWidgets.QPushButton(self)
        self.changeAgentsButton.setText("Add/Remove Agents")
        self.changeAgentsButton.clicked.connect(self.change_agents)
        

        self.layoutVertical = QtWidgets.QVBoxLayout()
        
        self.upperLayout = QtWidgets.QVBoxLayout()
        self.upperLayout.addWidget(self.tableView)

        
        self.lowerLayout = QtWidgets.QHBoxLayout()
        self.lowerLayout.addWidget(self.addParamsButton)
        self.lowerLayout.addWidget(self.changeAgentsButton)
        self.lowerLayout.addWidget(self.saveButton)
        
        self.layoutVertical.addLayout(self.upperLayout)
        self.layoutVertical.addLayout(self.checkBoxLayout)
        self.layoutVertical.addLayout(self.otherParamsLayout)
        self.layoutVertical.addLayout(self.lowerLayout)


        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.layoutVertical)
        self.normalFont = self.parentWindow.normalFont
        self.home.setFont(self.normalFont)
        self.home.show()



 
                
    def update_checklabels(self, key): 
        ''' this function gets called whenever parameters are changed e.g. when agent names are changed 
        or a new uni for time measurement is selected. The values are set to -1 and the labels and line edits
        are redrawn.''' 
        
        if key == 'AGENTS':
            self.checkLabels['AGENTS'] = {self.AGENT_NAMES[i] + self.AGENT_DATA[k] : -1 
            for k in range(len(self.AGENT_DATA)) for i in range(len(self.AGENT_NAMES))} 
            self.draw_agent_names(init = False) 

        elif key == 'TIME':
            self.draw_time_labels(init = False) 
        
        elif key == 'OTHER': 
            self.checkLabels['OTHER'] = {self.OTHER[i] : -1 for i in range(len(self.OTHER))}
            self.draw_additional_labels(init = False)
        
                
    def setColumn(self): 
        ''' reacts to changes in the text-edit field for column selection'''  
        sender = self.sender()
        senderName = sender.objectName()
        for key in self.checkLabels.keys():
            if senderName in self.checkLabels[key].keys(): 
                self.checkLabels[key][senderName] = sender.text()
                
    
    def draw_additional_labels(self, init = True): 
    
        if init == False:   
            for k in range(len(self.otherLEs)): 
                self.otherParamsLayout.removeWidget(self.otherLEs[k])
                sip.delete(self.otherLEs[k])
                
                self.otherParamsLayout.removeWidget(self.otherLabels[k])
                sip.delete(self.otherLabels[k])
            
        self.otherLEs = []
        self.otherLabels = []
        
        if len(self.OTHER) < 1: 
            pass
        else: 
            for j, key in enumerate(self.OTHER): 
                cb = QtWidgets.QLabel(self)
                cb.setText(key)
                self.otherLabels.append(cb)
                
                le = QtWidgets.QLineEdit(self)
                print(self.checkLabels)
                if int(self.checkLabels['OTHER'][key]) > 0: 
                    le.setText(str(self.checkLabels['OTHER'][key]))
                le.textChanged.connect(self.setColumn)
                le.setObjectName(key)
                le.setValidator(QtGui.QIntValidator())
                self.otherLEs.append(le)
                self.otherParamsLayout.addWidget(cb, 0, 2*j)
                self.otherParamsLayout.addWidget(le, 0, 2*j +1)
            
                
    def draw_time_labels(self, init = False): 
        if init == False: 
            for l in self.timeLables: 
                self.checkBoxLayout.removeWidget(l)
                sip.delete(l) 
            self.timeLables = []
            for l in self.timeLEs: 
                self.checkBoxLayout.removeWidget(l)
                sip.delete(l) 
            self.timeLEs = []
                
    
        for j, key in enumerate(self.TIME_LABELS): 
            cb = QtWidgets.QLabel(self)
            if key == 'time': 
                cb.setText(key + '(' + self.PARAM_INFO['time'] + ')')
            else: 
                cb.setText(key)
            self.timeLables.append(cb)
            
            le = QtWidgets.QLineEdit(self)
            if int(self.checkLabels['TIME'][key]) > 0: 
                le.setText(str(self.checkLabels['TIME'][key]))
            le.textChanged.connect(self.setColumn)
            le.setObjectName(key)
            le.setValidator(QtGui.QIntValidator())
            self.timeLEs.append(le)
            self.checkBoxLayout.addWidget(cb, 0, 2*j)
            self.checkBoxLayout.addWidget(le, 0, 2*j +1)
        
    
    def draw_agent_names(self, init = False): 
        ''' creates a label and text-edit widget for each agent and agent-property (x, y, angle). Any 
        preexisting widgets are deleted. This allows to change the agent number/names dynamically. The Widgets are 
        populated with te valued found in checkLabels, if a checkLabels entry is -1 the value will not e drawn.'''
        
        # this block deletes old widgets if there are any
        if init == False: 
            for l in self.agentLEs: 
                self.checkBoxLayout.removeWidget(l)
                sip.delete(l) 
            self.agentLEs = []
        
        # this block produces the new widgets (or default widgets when called the first time
        # widget IDs are saved in self.agentLEs
        for i in range(len(self.AGENT_NAMES)): 
            for k, s in enumerate(self.AGENT_DATA): 
                
                if s == '_angle':
                    cb = QtWidgets.QLabel(self.AGENT_NAMES[i] + s + '(' + self.PARAM_INFO['angle'] + ')')
                else: 
                    cb = QtWidgets.QLabel(self.AGENT_NAMES[i] + s)
                self.agentLEs.append(cb)
                
                le = QtWidgets.QLineEdit(self)
                
                if int(self.checkLabels['AGENTS'][self.AGENT_NAMES[i] + s]) > 0 :              
                    le.setText(str(self.checkLabels['AGENTS'][self.AGENT_NAMES[i] + s]))
                le.textChanged.connect(self.setColumn)
                le.setObjectName(self.AGENT_NAMES[i] + s)
                le.setValidator(QtGui.QIntValidator())
                self.agentLEs.append(le)
                
                self.checkBoxLayout.addWidget(cb, i+1, 2*k)
                self.checkBoxLayout.addWidget(le, i+1, 2*k+1)

        
    def check_entries(self): 
        ''' called from the save function. 
        checks if the user entries are valid and returns a boolean value'''
        valid = True        
        columnlist = []# bulid a list of all columns of the final csv

        for key in self.checkLabels.keys(): 
            for v in self.checkLabels[key].values():
                try:  
                    columnlist.append(int(v) -1)
                except ValueError: 
                    valid = False 
         
        if any(x < 0 for x in columnlist): # check if all values were set (default = -1)
            valid = False        
        elif len(columnlist) != len(set(columnlist)): # check if no value appears twice
            valid = False        
        elif max(columnlist) > self.nColumns: # check if columns are in range of original file
            valid = False            
        return valid


    def save(self):     
        ''' gets called by the save Button. Checks if selected columns are valid, if so, data is saved to a temporary csv file
        otherwise a warning is sent'''
        print(self.checkLabels)
        valid = self.check_entries()
        if valid: 
            if self.build_csv(self.fileName) == False: 
                return
            self.parentWindow.INFO['agent_names'] = self.AGENT_NAMES
            basic_stats.speed_and_dist(self.TMP_FILE_TITLE, self.parentWindow.INFO, self.CSV_INFO_FILE, self.PARAM_INFO_FILE)
            self.parentWindow.INFO['info'] = self.PARAM_INFO
            if self.parentWindow.init_Info(self.TMP_FILE_TITLE) == False: 
                return
            #basic_stats.speed_and_dist(self.TMP_FILE_TITLE, self.parentWindow.INFO, self.CSV_INFO_FILE, self.PARAM_INFO_FILE)
            self.home.close()
        else: 
            messages.send_warning('Column selection invalid: Check for empty fields, double indices and indices exceeding size of original file')
            
            

    def build_csv(self, fileName): 
        ''' uses the selected columns to build a temporary pandas frame which is saved to .csv under a default name.'''
        header_dict ={}
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        delim = csv_dict['read']['delim']
        skip_rows = csv_dict['read']['skip_rows']
        comment = csv_dict['read']['comment']
        
        for key in self.checkLabels.keys(): 
            for k in self.checkLabels[key].keys(): 
                header_dict[k] = self.checkLabels[key][k]
        
        df = pd.read_csv(fileName, header = None, sep = delim, 
                         skiprows = skip_rows, 
                         comment = comment, 
                         names = [str(i) for i in range(self.nColumns)])
        
        real_indices = [str(int(cl) -1) for cl in header_dict.values()]
        df_new = df.loc[:, real_indices]
        df_new.columns = list(header_dict.keys())
        df_new = df_new.dropna(how = 'any')    
        
        #print(header_dict)

        if type(df_new['frames'].values[0]) == str: #drop original header
            df_new = df_new.drop(df.index[0])
        
        
        
        # check for invalid values in selcted columns 
        should_be_floats = ['_x', '_y', '_angle']
        for an in self.AGENT_NAMES: 
            for sbf in should_be_floats: 
                if not self.is_float(df_new[an + sbf].values[3]): 
                    messages.send_warning('Data type of column {} not understood'.format(an+sbf))
                    return False
                    
        if not self.is_float(df_new['frames'].values[3]):
            messages.send_warning('Data type of column frames not understood')
            return False
        
        # save to tmp
        delim = csv_dict['write']['delim']
        df_new.to_csv(self.TMP_FILE_TITLE, sep = delim)
        print('temporary file saved to', self.TMP_FILE_TITLE)
        
        #save paramter settings to json
        param_dict = {}
        param_dict['agent_names'] = self.AGENT_NAMES
        param_dict['time_labels'] = self.TIME_LABELS
        param_dict['agent_specifications'] = self.AGENT_DATA
        param_dict['other'] = self.OTHER
        param_dict['info'] = self.PARAM_INFO
        
        for key1 in self.checkLabels: 
            for key2 in self.checkLabels[key1]:
                param_dict[key2] = self.checkLabels[key1][key2]
        
        with open(self.PARAM_INFO_FILE, 'w') as fp:
            json.dump(param_dict, fp)
        
  
    def change_agents(self): 
        '''calls the agent window which allows to set number and names of agents'''
        self.aw = agentWindow(self, self.AGENT_NAMES)
        self.aw.show()   

        
    def addParams(self): 
    
        self.sw = settingsWindow(self)
        self.sw.show() 
        
    def initParams(self): 
    
        # maybe check should be saved to json as a whole
        param_dict = json.load(open(self.PARAM_INFO_FILE))
        
        self.AGENT_NAMES = param_dict['agent_names'] 
        self.TIME_LABELS = param_dict['time_labels']
        self.AGENT_DATA = param_dict['agent_specifications']
        self.OTHER = param_dict['other']
        self.PARAM_INFO = param_dict['info']
        self.agentLEs = []
        self.timeLEs = []
        self.timeLables = []
        self.otherLabels = []
        self.otherLEs= []
        
        self.checkLabels = {'TIME': {self.TIME_LABELS[i] : param_dict[self.TIME_LABELS[i]] for i in range(len(self.TIME_LABELS))}, 
            'AGENTS': {}, 
            'OTHER': {self.OTHER[i] : param_dict[self.OTHER[i]] for i in range(len(self.OTHER))} } 
                
        for k in range(len(self.AGENT_NAMES)): 
            for j in range(len(self.AGENT_DATA)): 
                key = self.AGENT_NAMES[k]+self.AGENT_DATA[j]    
                self.checkLabels['AGENTS'][key] = param_dict[key]
        

    def open_data(self):
        ''' uses the parameters from self.CSV_INFO_FILE and tries to open the datafile with pandas. If NaN values are 
            detected, the user is informed and the corresponding rows will be ignored in processing. If an error occurs 
            while opening with pandas a warning is sent'''
        
        csv_dict = json.load(open(self.CSV_INFO_FILE))
        
        try: 
            delim = csv_dict['read']['delim']
            skip_rows = csv_dict['read']['skip_rows']
            comment = csv_dict['read']['comment']
            df = pd.read_csv(self.fileName, sep = delim, comment = comment, skiprows = skip_rows)
            vals = df.count(axis = 1).values # number of non-NaN values per row
            maxx = df.count(axis = 1).max() # maximum number of non-NaN values per row
            delete_rows = len(np.where(vals < maxx)[0])
            messages.send_info_detail('(1)To speed up the display process only the first 100 rows of data will be shown. \n(2)NaN values have been detected in {} rows. These rows will be ignored in the following process.'.format(str(delete_rows)), 
            detail = 'Indices of ignored rows: {}'.format(np.where(vals < maxx)[0]))
            df = df.dropna(how = 'any')
            df = df.head(100)

        except pd.errors.ParserError: 
            messages.send_warning("There seems to be a problem with the file you're trying to open.\n\n \
            This is usually due to missing values. Please delete incomplete rows and try again.")
            return
            self.close()

        return df

    def is_float(self, data): 
        try: 
            float(data) 
            return True
        except ValueError:
            return False

#if __name__ == "__main__":
#    import sys
#    import numpy as np

#    app = QtWidgets.QApplication(sys.argv)
#    app.setApplicationName('Table')

#    main = tableWindow('CouzinDataOutWedMar01121659201.csv')


#    sys.exit(app.exec_())          

