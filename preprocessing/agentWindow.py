import csv


from PyQt4 import QtGui, QtCore
import pandas as pd
from numpy import random
import numpy as np
import sys
import sip

#import settings.data_settings as ds

class agentWindow1(QtGui.QWidget):

    def __init__(self, parentWindow):
    #def __init__(self, parent = None):
    
        self.nAgents = 2
        self.AGENT_NAMES = ['agent'+ str(i) for i in range(self.nAgents)]
        self.labels = []
    
        super(agentWindow1, self).__init__(parentWindow)
        #super(agentWindow1, self).__init__(parent)
        self.parentWindow = parentWindow

        self.home()
        
    def home(self): 
        self.nAgentsEdit = QtGui.QLineEdit()
        self.nAgentsEdit.setText(str(self.nAgents))
        self.nAgentsEdit.setValidator(QtGui.QIntValidator())

        self.nAgentsRename = QtGui.QPushButton('Rename')
        self.nAgentsRename.clicked.connect(self.change_agent_name)
        
        self.OKButton = QtGui.QPushButton('OK')
        self.OKButton.clicked.connect(self.pushed_ok)

        self.mainLayout = QtGui.QGridLayout()
        self.mainLayout.addWidget(QtGui.QLabel('Agents:'), 0, 0)
        self.mainLayout.addWidget(self.nAgentsEdit, 0, 1)
        self.mainLayout.addWidget(self.nAgentsRename, 0, 2)
        self.mainLayout.addWidget(self.OKButton, 10, 10)
        
        self.draw_agent_names()
        
        self.home = QtGui.QWidget()
        self.home.setLayout(self.mainLayout)
        self.home.show()
    
    def pushed_ok(self): 
        self.parentWindow.AGENT_NAMES = self.AGENT_NAMES
        self.parentWindow.draw_agent_names()
        self.home.close()
            
    def change_agent_name(self): 
        self.nAgents = int(self.nAgentsEdit.text())
        aw2 = agentWindow2(self, self.nAgents, self.AGENT_NAMES)
        aw2.show()
   
    def draw_agent_names(self): 
        
        self.mainLayout.addWidget(QtGui.QLabel('Names:'), 1, 0)
        
        for l in self.labels: 
            self.mainLayout.removeWidget(l)
            sip.delete(l)
            
        self.labels = []
        for k, an in enumerate(self.AGENT_NAMES): 
            aa = QtGui.QLabel(an)
            self.mainLayout.addWidget(aa, k+2, 1)
            self.labels.append(aa)
        
        
        
class agentWindow2(QtGui.QWidget):

    def __init__(self, parentWindow, n, names):
    
        self.nAgents = n
        self.AGENT_NAMES = names

        
        super(agentWindow2, self).__init__(parentWindow)

        self.parentWindow = parentWindow
        
        self.home()

    def home(self): 
        self.mainLayout = QtGui.QGridLayout()
        
        self.agentLEs = []
        
        for i in range(self.nAgents): 
            cb = QtGui.QLabel(self)
            cb.setText('agent' + str(i))
            
            le = QtGui.QLineEdit(self)
            le.setText(self.AGENT_NAMES[i])                
            self.agentLEs.append(le)
    #                le.setValidator(QtGui.QIntValidator())
            self.mainLayout.addWidget(cb, i+1, 0)
            self.mainLayout.addWidget(le, i+1, 1)


        self.OKButton = QtGui.QPushButton('OK')
        self.OKButton.clicked.connect(self.on_ok)
        self.mainLayout.addWidget(self.OKButton, i+2, 1)

        self.home = QtGui.QWidget()
        self.home.setLayout(self.mainLayout)
        self.home.show()
        
    def on_ok(self): 
        self.AGENT_NAMES = []
        print(self.AGENT_NAMES)
        for le in self.agentLEs: 
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
            self.parentWindow.AGENT_NAMES = self.AGENT_NAMES
            self.parentWindow.draw_agent_names()
            self.home.close()            
        else: 
            self.send_warning()
            
            
                
    def send_warning(self): 
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Warning)
        msg.setText("Invalid or empty agent names")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        retval = msg.exec_()

        

#if __name__ == "__main__":
#    import sys
#    import numpy as np

#    app = QtGui.QApplication(sys.argv)
#    app.setApplicationName('Time Sliders')

#    main = agentWindow1()
#    #main.show()

#    sys.exit(app.exec_())       
#        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
