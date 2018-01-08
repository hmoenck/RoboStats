#!/usr/bin/env python
#-*- coding:utf-8 -*-
import csv

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui, QtCore
import pandas as pd


class TableWindow(QtGui.QMainWindow):

    def __init__(self, fileName, parent=None):
    
        super(TableWindow, self).__init__(parent)
        
        self.fileName = fileName
        self.checkLabels = {'time': -1, 'agent0_x': -1, 'agent0_y': -1, 'agent0_angle': -1, 
                            'agent1_x': -1, 'agent1_y': -1, 'agent1_angle': -1}
        self.nColumns = 0

        

        self.home()
        
        
        
    def home(self): 
    
        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtGui.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.pushButtonLoad = QtGui.QPushButton(self)
        self.pushButtonLoad.setText("Load Csv File!")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)
        
        self.checkBoxLayout = QtGui.QGridLayout()
        for j, key in enumerate(self.checkLabels): 
            #if key == 'time': 
            cb = QtGui.QLabel(self)
            cb.setText(key)
            
            le = QtGui.QLineEdit(self)
            le.textChanged.connect(self.setColumn)
            le.setObjectName(key)
            le.setValidator(QtGui.QIntValidator())
            self.checkBoxLayout.addWidget(cb, 0, 2*j)
            self.checkBoxLayout.addWidget(le, 0, 2*j +1)
            #print(key)
                
                
        self.saveButton = QtGui.QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.save)

        self.layoutVertical = QtGui.QVBoxLayout()
        
        self.upperLayout = QtGui.QVBoxLayout()
        self.upperLayout.addWidget(self.tableView)
        self.upperLayout.addWidget(self.pushButtonLoad)
        
        self.lowerLayout = QtGui.QHBoxLayout()
        self.lowerLayout.addWidget(self.saveButton)
        
        self.layoutVertical.addLayout(self.upperLayout)
        self.layoutVertical.addLayout(self.checkBoxLayout)
        self.layoutVertical.addLayout(self.lowerLayout)


        self.home = QtGui.QWidget()
        self.home.setLayout(self.layoutVertical)
        self.setCentralWidget(self.home)
        
        

    def loadCsv(self, fileName):
    
        
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput, delimiter = ';'):   
                self.nColumns = len(row) 
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)
        
                
    def setColumn(self): 
        sender = self.sender()
        senderName = sender.objectName()
        
        self.checkLabels[senderName] = sender.text()
        #print(self.checkLabels)
        
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
        
        df_new = df.loc[:, list(self.checkLabels.values())]
        df_new.columns = list(self.checkLabels.keys())
        df_new.to_csv('selected_data.csv', sep = ',')
        
        print('saved')
        

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv(self.fileName)

        


if __name__ == "__main__":
    import sys

    data = '/home/claudia/Dokumente/Uni/lab_rotation_FU/TracksRoboLife/CouzinDataOutWedMar01132818201.csv'

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Table View')

    main = TableWindow(data)
    main.show()

    sys.exit(app.exec_())
