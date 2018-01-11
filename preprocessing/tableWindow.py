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


class tableWindow(QtGui.QWidget):

    #the name of the resulting file will be passed back to the main window            
    TMP_FILE_TITLE = 'tmp.csv'

    def __init__(self, parentWindow, fileName):

        super(tableWindow, self).__init__(parentWindow)
        self.parentWindow = parentWindow
        self.fileName = fileName #name of the selected csv
        
        self.checkLabels = {'time': 2, 'frames': 1, 'agent0_x': 5, 'agent0_y': 6, 'agent0_angle': 7, 
                            'agent1_x': 10, 'agent1_y': 11, 'agent1_angle': 12} # labels for the selcted columns
                            
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
        nAgents = 2
        base = 'agent'
        specs = ['_x', '_y', '_angle']
        
        #for j, key in enumerate(self.checkLabels): 
        
        for j, key in enumerate(['frames', 'time']): 
            cb = QtGui.QLabel(self)
            cb.setText(key)
            
            le = QtGui.QLineEdit(self)
            le.setText(str(self.checkLabels[key]))
            le.textChanged.connect(self.setColumn)
            le.setObjectName(key)
            le.setValidator(QtGui.QIntValidator())
            self.checkBoxLayout.addWidget(cb, 0, 2*j)
            self.checkBoxLayout.addWidget(le, 0, 2*j +1)
            
        for i in range(nAgents): 
            for k, s in enumerate(specs): 
                label = base + str(i) + s
                cb = QtGui.QLabel(self)
                cb.setText(label)
                
                le = QtGui.QLineEdit(self)
                le.setText(str(self.checkLabels[label]))
                le.textChanged.connect(self.setColumn)
                le.setObjectName(label)
                le.setValidator(QtGui.QIntValidator())
                self.checkBoxLayout.addWidget(cb, i+1, 2*k)
                self.checkBoxLayout.addWidget(le, i+1, 2*k+1)


        # ---------------------------------------------------------------------
        # Buttons
        # ---------------------------------------------------------------------
   
        self.saveButton = QtGui.QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.save)
        
        self.addParamsButton = QtGui.QPushButton(self)
        self.addParamsButton.setText("Add Parameters")
        self.addParamsButton.clicked.connect(self.addParams)
        

        self.layoutVertical = QtGui.QVBoxLayout()
        
        self.upperLayout = QtGui.QVBoxLayout()
        self.upperLayout.addWidget(self.tableView)

        
        self.lowerLayout = QtGui.QHBoxLayout()
        self.lowerLayout.addWidget(self.addParamsButton)
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
        self.checkLabels[senderName] = sender.text()

        
    def save(self):     
        warning = False
        overlap = False
        columnlist = list(self.checkLabels.values())
        
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
        df = pd.read_csv(fileName, header = None, sep = ';', names = [str(i) for i in range(self.nColumns)])
        
        real_indices = [str(int(cl) -1) for cl in self.checkLabels.values()]
        df_new = df.loc[:, real_indices]
        df_new.columns = list(self.checkLabels.keys())
        df_new.to_csv(self.TMP_FILE_TITLE, sep = ',')

        print('temporary file saved to', self.TMP_FILE_TITLE)
        
        self.parentWindow.init_Info(self.TMP_FILE_TITLE)
        self.home.close()
        
        
        
    def addParams(self): 
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("I can't do anything yet")
        msg.setWindowTitle("I do nothing")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        val = msg.exec_()
        


        


#if __name__ == "__main__":
#    import sys

#    data = '/home/claudia/Dokumente/Uni/lab_rotation_FU/TracksRoboLife/CouzinDataOutWedMar01132818201.csv'

#    app = QtGui.QApplication(sys.argv)
#    app.setApplicationName('Table View')

#    main = TableWindow(data)
#    main.show()

#    sys.exit(app.exec_())
