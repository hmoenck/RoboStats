#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv

#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

#from PyQt4 import QtGui, QtCore
from PyQt5 import QtWidgets 
from PyQt5 import QtGui # for QFont, QStandardItemModel

import pandas as pd
from numpy import random
import sys
from agentWindow import agentWindow1


class tableWindow(QtWidgets.QWidget):
    ''' presents a selected .csv file, allows to identify and name relevant columns. The resulting 
    columns (with respective names) will be saved as 'tmp.csv' to be further processed by main window'''

    #the name of the resulting file will be passed back to the main window            
    TMP_FILE_TITLE = 'tmp.csv'

    def __init__(self, parentWindow, fileName):
    #def __init__(self, fileName):

        #super(tableWindow, self).__init__()
        super(tableWindow, self).__init__(parentWindow)
        self.parentWindow = parentWindow
        self.fileName = fileName #name of the selected csv
        
        self.checkLabels = {'TIME': {'time': 2, 'frames': 1}, 'AGENTS':{ 'agent0_x': 5, 'agent0_y': 6, 'agent0_angle': 7, 
                            'agent1_x': 10, 'agent1_y': 11, 'agent1_angle': 12}} # labels for the selcted columns
        
        self.AGENT_NAMES = ['agent0', 'agent1'] # default naming for agents
        self.AGENT_DATA = ['_x', '_y', '_angle'] # default agent info   
        self.agentLEs = []
                            
        self.nColumns = 0 # number of columns of the original file 
        
        self.DELIMINATER = ';' # default deliminator for reading

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
            

        self.draw_agent_names() # set the agent columns


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
                
    def setColumn(self): 
        ''' reacts to changes in the text-edit field for column selection'''  
        sender = self.sender()
        senderName = sender.objectName()
        for key in self.checkLabels.keys():
            if senderName in self.checkLabels[key].keys(): 
                self.checkLabels[key][senderName] = sender.text()
    
    def draw_agent_names(self): 
        ''' creates a lable and text-edit widget for each agent and agent-property (x, y, angle). Any 
        preexisting widgets are deleted. This allows to change the agent number/names dynamically. If 
        the agentWindow is not called we use the default values as specified in self.checkLabels['AGENTS']'''
        
        # this block deletes old widgets if there are any
        if len(self.agentLEs) != 0:
            for l in self.agentLEs: 
                self.checkBoxLayout.removeWidget(l)
                sip.delete(l) 
            self.agentLEs = []
        
        # this block produces the new widgets (or default widgets when called the first time
        # widget IDs are saved in self.agentLEs
        AGENTS_COLUMNS = {}
        for i in range(len(self.AGENT_NAMES)): 
            for k, s in enumerate(self.AGENT_DATA ): 

                cb = QtWidgets.QLabel(self.AGENT_NAMES[i] + s)
                self.agentLEs.append(cb)
                
                le = QtWidgets.QLineEdit(self)                
                #le.setText(str(self.checkLabels['AGENTS'][label]))
                le.textChanged.connect(self.setColumn)
                le.setObjectName(self.AGENT_NAMES[i] + s)
                le.setValidator(QtGui.QIntValidator())
                self.agentLEs.append(le)
                
                
                self.checkBoxLayout.addWidget(cb, i+1, 2*k)
                self.checkBoxLayout.addWidget(le, i+1, 2*k+1)
                
                AGENTS_COLUMNS[self.AGENT_NAMES[i] + s] = -1
        
        self.checkLabels['AGENTS'] = AGENTS_COLUMNS

    def check_entries(self): 
        ''' checks if the user entries are valid and returns a boolean value'''
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
        ''' gets called by the save Button. Checks if selected columns are valid, if so, the tmp.csv is created
        otherwise a warning is sent'''
        print(self.checkLabels)
        valid = self.check_entries()
        if valid: 
            self.build_final_csv(self.fileName)
        else: 
            self.send_warning('Column selection invalid')
            
            

    def build_final_csv(self, fileName): 
        header_dict ={}
    
        for key in self.checkLabels.keys(): 
            for k in self.checkLabels[key].keys(): 
                header_dict[k] = self.checkLabels[key][k]
        
        df = pd.read_csv(fileName, header = None, sep = ';', names = [str(i) for i in range(self.nColumns)])
        
        real_indices = [str(int(cl) -1) for cl in header_dict.values()]
        df_new = df.loc[:, real_indices]
        df_new.columns = list(header_dict.keys())
        df_new.to_csv(self.TMP_FILE_TITLE, sep = ',')

        print('temporary file saved to', self.TMP_FILE_TITLE)
        
        
        self.parentWindow.INFO['agent_names'] = self.AGENT_NAMES
        self.parentWindow.init_Info(self.TMP_FILE_TITLE)
        self.home.close()
        
        
        
    def addParams(self): 
        #TODO should allow to set other non agent related columns, and also change properties of the csv (existing header, deliminater etc.)
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("I can't do anything yet")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        val = msg.exec_()
   
    def change_agents(self): 
        '''calls the agent window which allows to set number and names of agents'''
        self.aw = agentWindow1(self)
        self.aw.show()       


        


#if __name__ == "__main__":
#    import sys

#    data = '/home/claudia/Dokumente/Uni/lab_rotation_FU/data/TracksRoboLife/CouzinDataOutWedMar01132818201.csv'

#    app = QtWidgets.QApplication(sys.argv)
#    app.setApplicationName('Table View')

#    main = tableWindow(data)
#    main.show()

#    sys.exit(app.exec_())
