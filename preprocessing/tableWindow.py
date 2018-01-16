#!/usr/bin/env python
#-*- coding:utf-8 -*-
import csv

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui, QtCore
import pandas as pd
from numpy import random
import sys
from agentWindow import agentWindow1


class tableWindow(QtGui.QWidget):

    #the name of the resulting file will be passed back to the main window            
    TMP_FILE_TITLE = 'tmp.csv'

    def __init__(self, parentWindow, fileName):

        super(tableWindow, self).__init__(parentWindow)
        self.parentWindow = parentWindow
        self.fileName = fileName #name of the selected csv
        
        self.checkLabels = {'TIME': {'time': 2, 'frames': 1}, 'AGENTS':{ 'agent0_x': 5, 'agent0_y': 6, 'agent0_angle': 7, 
                            'agent1_x': 10, 'agent1_y': 11, 'agent1_angle': 12}} # labels for the selcted columns
        
        self.AGENT_NAMES = ['agent0', 'agent1']
        self.AGENT_DATA = ['_x', '_y', '_angle']   
        self.agentLEs = []
                            
        self.nColumns = 0 #number of columns of the original file 

        self.home()
        
        
    def home(self): 
    
        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtGui.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        
        with open(self.fileName, "r") as fileInput:
            for row in csv.reader(fileInput, delimiter = ';'):   
                self.nColumns = len(row) 
                items = [QtGui.QStandardItem(field) for field in row]
                self.model.appendRow(items)
        
 

        self.checkBoxLayout = QtGui.QGridLayout()
        
        # ---------------------------------------------------------------------
        # this can be done smarter...
        # ---------------------------------------------------------------------

        
        #for j, key in enumerate(self.checkLabels): 
        
        for j, key in enumerate(['frames', 'time']): 
            cb = QtGui.QLabel(self)
            cb.setText(key)
            
            le = QtGui.QLineEdit(self)
            le.setText(str(self.checkLabels['TIME'][key]))
            le.textChanged.connect(self.setColumn)
            le.setObjectName(key)
            le.setValidator(QtGui.QIntValidator())
            self.checkBoxLayout.addWidget(cb, 0, 2*j)
            self.checkBoxLayout.addWidget(le, 0, 2*j +1)
            
            
            
        
            
        self.draw_agent_names()


        # ---------------------------------------------------------------------
        # Buttons
        # ---------------------------------------------------------------------
   
        self.saveButton = QtGui.QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.save)
        
        self.addParamsButton = QtGui.QPushButton(self)
        self.addParamsButton.setText("Add Parameters")
        self.addParamsButton.clicked.connect(self.addParams)
        
        self.changeAgentsButton = QtGui.QPushButton(self)
        self.changeAgentsButton.setText("Add/Remove Agents")
        self.changeAgentsButton.clicked.connect(self.change_agents)
        

        self.layoutVertical = QtGui.QVBoxLayout()
        
        self.upperLayout = QtGui.QVBoxLayout()
        self.upperLayout.addWidget(self.tableView)

        
        self.lowerLayout = QtGui.QHBoxLayout()
        self.lowerLayout.addWidget(self.addParamsButton)
        self.lowerLayout.addWidget(self.changeAgentsButton)
        self.lowerLayout.addWidget(self.saveButton)
        
        self.layoutVertical.addLayout(self.upperLayout)
        self.layoutVertical.addLayout(self.checkBoxLayout)
        self.layoutVertical.addLayout(self.lowerLayout)


        self.home = QtGui.QWidget()
        self.home.setLayout(self.layoutVertical)
        self.home.show()

                
    def setColumn(self): 
    
        sender = self.sender()
        senderName = sender.objectName()
        for key in self.checkLabels.keys():
            if senderName in self.checkLabels[key].keys(): 
                self.checkLabels[key][senderName] = sender.text()
    
    def draw_agent_names(self): 
    
        if len(self.agentLEs) != 0:
            for l in self.agentLEs: 
                self.checkBoxLayout.removeWidget(l)
                sip.delete(l) 
            self.agentLEs = []
        
        AGENTS_COLUMNS = {}
        for i in range(len(self.AGENT_NAMES)): 
            for k, s in enumerate(self.AGENT_DATA ): 

                cb = QtGui.QLabel(self.AGENT_NAMES[i] + s)
                self.agentLEs.append(cb)
                
                le = QtGui.QLineEdit(self)
                
                #le.setText(str(self.checkLabels['AGENTS'][label]))
                le.textChanged.connect(self.setColumn)
                le.setObjectName(self.AGENT_NAMES[i] + s)
                le.setValidator(QtGui.QIntValidator())
                self.agentLEs.append(le)
                
                
                self.checkBoxLayout.addWidget(cb, i+1, 2*k)
                self.checkBoxLayout.addWidget(le, i+1, 2*k+1)
                
                AGENTS_COLUMNS[self.AGENT_NAMES[i] + s] = -1
        
        self.checkLabels['AGENTS'] = AGENTS_COLUMNS

        
    def save(self):     
        warning = False
        overlap = False
        columnlist = []

        for key in self.checkLabels.keys(): 
            for v in self.checkLabels[key].values(): 
                columnlist.append(v)
        print(columnlist)
        
        if any(int(x) < 0 for x in columnlist):
        # check if all values were set
            warning = True
            
        elif len(columnlist) != len(set(columnlist)): 
        # check if no value appears twice
            warning = True
            overlap = True
            
        #TODO: Allow for only one agent as well as more than two agents 
        #TODO: check if selected column idxs don't exceed length
                
        msg = QtGui.QMessageBox()
               
        if warning: 
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
              
            if overlap == True: 
                msg.setText("Some columns have been multipely defined. Please resolve bevor saving.")
            else: 
                msg.setText("Please define all columns you want to use")

        else:        
            msg.setIcon(QtGui.QMessageBox.Question)
            msg.setText("Are you sure you want to save?")
            msg.setWindowTitle("Confirm Save")
            msg.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        
        val = msg.exec_()
        
        if warning == False and overlap == False and val == 1024: 
        # 1024 means 'Ok'
            self.build_final_csv(self.fileName)
            

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
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("I can't do anything yet")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        val = msg.exec_()
   
    def change_agents(self): 
        self.aw = agentWindow1(self)
        self.aw.show()       


        


#if __name__ == "__main__":
#    import sys

#    data = '/home/claudia/Dokumente/Uni/lab_rotation_FU/TracksRoboLife/CouzinDataOutWedMar01132818201.csv'

#    app = QtGui.QApplication(sys.argv)
#    app.setApplicationName('Table View')

#    main = TableWindow(data)
#    main.show()

#    sys.exit(app.exec_())
