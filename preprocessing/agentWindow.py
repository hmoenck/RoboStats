#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv

#from PyQt4 import QtGui, QtCore
from PyQt5 import QtWidgets 
from PyQt5 import QtGui 
import pandas as pd
from numpy import random
import numpy as np
import sys
import sip

#import settings.data_settings as ds

class agentWindow(QtWidgets.QWidget):
    ''' takes a list of default agent names from parent window and allows to change agent number and names'''

    def __init__(self, parentWindow, agent_names = []):
    #def __init__(self, parent = None, agent_names = []):
    
        self.nAgents = len(agent_names)
        self.AGENT_NAMES = agent_names
        
        self.labels = []
        self.custom_names = []
    
        super(agentWindow, self).__init__(parentWindow)
        #super(agentWindow, self).__init__(parent)
        self.parentWindow = parentWindow

        self.home()
        
    def home(self): 
        self.nAgentsEdit = QtWidgets.QLineEdit()
        self.nAgentsEdit.setText(str(self.nAgents))
        self.nAgentsEdit.setValidator(QtGui.QIntValidator())

        self.nAgentsChange = QtWidgets.QPushButton('Change')
        self.nAgentsChange.clicked.connect(self.change_agent_number)
        
        self.OKButton = QtWidgets.QPushButton('OK')
        self.OKButton.clicked.connect(self.pushed_ok)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addWidget(QtWidgets.QLabel('Agents:'), 0, 0)
        self.mainLayout.addWidget(self.nAgentsEdit, 0, 1)
        self.mainLayout.addWidget(self.nAgentsChange, 0, 2)
        self.mainLayout.addWidget(self.OKButton, 10, 10)
        
        self.mainLayout.addWidget(QtWidgets.QLabel('Names:'), 1, 0)
        
        self.draw_agent_names()
        
        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.mainLayout)
        self.home.show()
        
        
        
        
    def change_agent_number(self): 
        '''gets called by the Change button, changes agent number 
            and calls the draw_agent_names() function to adapt the 
            section for agent name setting.'''
        
        self.nAgents = int(self.nAgentsEdit.text())
        
        if len(self.AGENT_NAMES) < self.nAgents: # nAgent was increased, add default names
            for k in range(self.nAgents -len(self.AGENT_NAMES)): 
                self.AGENT_NAMES.append('agent'+ str(self.nAgents -1 +k))
        elif len(self.AGENT_NAMES) > self.nAgents:
            self.AGENT_NAMES = self.AGENT_NAMES[:self.nAgents]
        self.draw_agent_names(first_call = False)

    
    def pushed_ok(self): 
        ''' reads agent names from line edit elements, checks for validity (no empty fields, 
        no name starting with an integer, no double names) and sends the new names to parent window. '''
        self.AGENT_NAMES = []

        for le in self.custom_names: 
            text = le.text()

            if len(text) > 0: # don't allow empty names
                if text[0].isdigit(): # don't allow names to start with int
                    self.send_warning()
                    pass
                else: 
                    self.AGENT_NAMES.append(text)
            else: 
                self.send_warning()
                pass
                
        if len(list(set(self.AGENT_NAMES))) == self.nAgents: # no duplicates   
            print(self.AGENT_NAMES)     
            self.parentWindow.AGENT_NAMES = self.AGENT_NAMES   
            self.parentWindow.update_checklabels(init = False)
            self.parentWindow.draw_agent_names(init = False) 
            self.home.close()      
        else: 
            self.send_warning()
            
            

   
    def draw_agent_names(self, first_call = True): 
        ''' creates for each agent name a label and line edit element. When called the first time
        those elemnts are disabled, to avoid unintentional changes'''

        if first_call == False: # if the function has already been called, 
                                # previously build lists of labels and line edits have to be deleted
            for l in self.labels: 
                self.mainLayout.removeWidget(l)
                sip.delete(l)
                
            for cn in self.custom_names: 
                self.mainLayout.removeWidget(cn)
                sip.delete(cn)
                
            self.labels = []
            self.custom_names = []
        
        
        for k, an in enumerate(self.AGENT_NAMES): 
            l = QtWidgets.QLabel('agent' + str(k))

            cn = QtWidgets.QLineEdit()
            cn.setText(an)
            cn.setObjectName(an)
            if first_call == True: cn.setEnabled(False)
            
            self.mainLayout.addWidget(l, k+2, 1)
            self.mainLayout.addWidget(cn, k+2, 2)
            
            self.labels.append(l)
            self.custom_names.append(cn)

            
            
    def send_warning(self): 
        ''' opens a Qt Warning Dialog'''
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Invalid or empty agent names")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        
        
        
    

#if __name__ == "__main__":
#    import sys
#    import numpy as np

#    app = QtWidgets.QApplication(sys.argv)
#    app.setApplicationName('Agent window')

#    main = agentWindow(agent_names = ['hi', 'hu'])
#    #main.show()

#    sys.exit(app.exec_())       
        
        
