#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv

#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)
import sip
#from PyQt4 import QtGui, QtCore
from PyQt5 import QtWidgets 
from PyQt5 import QtGui # for QFont, QStandardItemModel

import pandas as pd
from numpy import random
import sys
from agentWindow import agentWindow
import settings.default_params as default


class tableWindow(QtWidgets.QWidget):
    ''' presents a selected .csv file, allows to identify and name relevant columns. The resulting 
    columns (with respective names) will be saved as 'tmp.csv' to be further processed by main window'''

    #the name of the resulting file will be passed back to the main window            
    TMP_FILE_TITLE = default.tmp_file

    def __init__(self, parentWindow, fileName):
    #def __init__(self, fileName):

        #super(tableWindow, self).__init__()
        super(tableWindow, self).__init__(parentWindow)
        self.parentWindow = parentWindow
        self.fileName = fileName #name of the selected csv
        
        self.AGENT_NAMES = default.agent_names #default naming for agents
        self.AGENT_DATA = default.agent_specifications #default agent info
        self.TIME_LABELS = default.time_labels   
        self.agentLEs = []
        
        # the check labels dictionary contains the lables and default values for all columns to set
        self.checkLabels = {}
        self.update_checklabels(init = True)



        self.nColumns = 0 #number of columns of the original file 
        
        self.DELIMINATER = default.csv_delim # default deliminator for reading

        self.home()
        
        
    def home(self): 
    
        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        
        self.set_table()

        # ---------------------------------------------------------------------
        # COLUMN LAYOUT
        # ---------------------------------------------------------------------

        self.checkBoxLayout = QtWidgets.QGridLayout()
        
        for j, key in enumerate(['frames', 'time']): 
            cb = QtWidgets.QLabel(self)
            cb.setText(key)
            
            le = QtWidgets.QLineEdit(self)
            le.setText(str(self.checkLabels['TIME'][key]))
            le.textChanged.connect(self.setColumn)
            le.setObjectName(key)
            le.setValidator(QtGui.QIntValidator())
            self.checkBoxLayout.addWidget(cb, 0, 2*j)
            self.checkBoxLayout.addWidget(le, 0, 2*j +1)
            

        self.draw_agent_names(init = True) # set the agent columns


        # ---------------------------------------------------------------------
        # Buttons
        # ---------------------------------------------------------------------
   
        self.saveButton = QtWidgets.QPushButton(self)
        self.saveButton.setText("Save")
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
        self.layoutVertical.addLayout(self.lowerLayout)


        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.layoutVertical)
        self.home.show()


    def set_table(self): 
        '''opens the selcted .csv and populates the table'''
        with open(self.fileName, "r") as fileInput:
        #fileInput = open(self.fileName, 'r')
            for row in csv.reader(fileInput, delimiter = self.DELIMINATER):   
                self.nColumns = len(row) 
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)
 
                
    def update_checklabels(self, init = False): 
        ''' the checkLabels dictionary conatins the names and indices of all selected columns. 
        When called with init= True, the default values (specified in settings/default_params.py) 
        will be used for initilaization, otherwise the columns will be initialized with -1.''' 

        if init == True or len(self.AGENT_NAMES)*len(self.AGENT_DATA) == len(default.agent_columns): 
            self.checkLabels = {'TIME': {self.TIME_LABELS[i] : default.time_columns[i] for i in range(len(self.TIME_LABELS))}, 
            'AGENTS': {self.AGENT_NAMES[i] + self.AGENT_DATA[k] : default.agent_columns[i*len(self.AGENT_DATA)+k] 
            for k in range(len(self.AGENT_DATA)) for i in range(len(self.AGENT_NAMES))}} 
            
        else: 
            self.checkLabels = {'TIME': {self.TIME_LABELS[i] : default.time_columns[i] for i in range(len(self.TIME_LABELS))}, 
            'AGENTS': {self.AGENT_NAMES[i] + self.AGENT_DATA[k] : -1 
            for k in range(len(self.AGENT_DATA)) for i in range(len(self.AGENT_NAMES))}} 
        
        print(self.checkLabels)            
                
    def setColumn(self): 
        ''' reacts to changes in the text-edit field for column selection'''  
        sender = self.sender()
        senderName = sender.objectName()
        print(senderName)
        for key in self.checkLabels.keys():
            if senderName in self.checkLabels[key].keys(): 
                self.checkLabels[key][senderName] = sender.text()
    
    def draw_agent_names(self, init = False): 
        ''' creates a lable and text-edit widget for each agent and agent-property (x, y, angle). Any 
        preexisting widgets are deleted. This allows to change the agent number/names dynamically. The Widgets are 
        populated with te valued found in checkLables, if a checkLabels entry is -1 the value will not e drawn.'''
        
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

                cb = QtWidgets.QLabel(self.AGENT_NAMES[i] + s)
                self.agentLEs.append(cb)
                
                le = QtWidgets.QLineEdit(self)
                
                if self.checkLabels['AGENTS'][self.AGENT_NAMES[i] + s] > 0 :              
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
                columnlist.append(int(v) -1)
         
        if any(x < 0 for x in columnlist): # check if all values were set (default = -1)
            valid = False        
        elif len(columnlist) != len(set(columnlist)): # check if no value appears twice
            valid = False        
        elif max(columnlist) > self.nColumns: # check if columns are in range of original file
            valid = False            
        return valid
        
    def send_warning(self, text): 
        ''' creates a Qt warning message with custom text''' 
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.setText(text)
        val = msg.exec_()

    def save(self):     
        ''' gets called by the save Button. Checks if selected columns are valid, if so, data is saved to a temporary csv file
        otherwise a warning is sent'''
        print(self.checkLabels)
        valid = self.check_entries()
        if valid: 
            self.build_csv(self.fileName)
        else: 
            self.send_warning('Column selection invalid: Check for empty fields, double indices and indices exceeding size of original file')
            
            

    def build_csv(self, fileName): 
        ''' uses the selected columns to build a temporary pandas frame which is saved to .csv under a default name.'''
        header_dict ={}
    
        for key in self.checkLabels.keys(): 
            for k in self.checkLabels[key].keys(): 
                header_dict[k] = self.checkLabels[key][k]
        
        df = pd.read_csv(fileName, header = None, sep = default.csv_delim , names = [str(i) for i in range(self.nColumns)])
        
        real_indices = [str(int(cl) -1) for cl in header_dict.values()]
        df_new = df.loc[:, real_indices]
        df_new.columns = list(header_dict.keys())
        df_new.to_csv(self.TMP_FILE_TITLE, sep = default.csv_delim)

        print('temporary file saved to', self.TMP_FILE_TITLE)
  
        self.parentWindow.INFO['agent_names'] = self.AGENT_NAMES
        self.parentWindow.init_Info(self.TMP_FILE_TITLE)
        self.home.close()
        
  
    def change_agents(self): 
        '''calls the agent window which allows to set number and names of agents'''
        self.aw = agentWindow(self, self.AGENT_NAMES)
        self.aw.show()   
        

        
    def addParams(self): 
        #TODO should allow to set other non agent related columns, and also change properties of the csv (existing header, deliminater etc.)
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("I can't do anything yet")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        val = msg.exec_()

        


#if __name__ == "__main__":
#    import sys

#    data = '/home/claudia/Dokumente/Uni/lab_rotation_FU/data/TracksRoboLife/CouzinDataOutWedMar01132818201.csv'

#    app = QtWidgets.QApplication(sys.argv)
#    app.setApplicationName('Table View')

#    main = tableWindow(data)
#    main.show()

#    sys.exit(app.exec_())
