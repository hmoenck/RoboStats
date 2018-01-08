#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtGui, QtCore
import pandas as pd
from TableWindow import TableWindow

class mainWindow(QtGui.QMainWindow):

    def __init__(self, parent = None):
    
        super(mainWindow, self).__init__(parent)

        self.home()

    def home(self): 

        self.mainLayout = QtGui.QHBoxLayout()
        
        self.selectData = QtGui.QPushButton('Set Data Columns')
        self.selectData.clicked.connect(self.on_Button_clicked)
        
        self.mainLayout.addWidget(self.selectData)

        self.home = QtGui.QWidget()
        self.home.setLayout(self.mainLayout)
        self.setCentralWidget(self.home)

    
    def on_Button_clicked(self): 
        data = '/home/claudia/Dokumente/Uni/lab_rotation_FU/TracksRoboLife/CouzinDataOutWedMar01132818201.csv'
        self.table = TableWindow(data)
        self.table.show()
        

if __name__ == "__main__":
    import sys

    #data = '/home/claudia/Dokumente/Uni/lab_rotation_FU/TracksRoboLife/CouzinDataOutWedMar01132818201.csv'

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('main')

    #main = TableWindow(data)
    main = mainWindow()
    main.show()

    sys.exit(app.exec_())
