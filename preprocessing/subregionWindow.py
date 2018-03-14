#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
from PyQt5 import QtWidgets 
from PyQt5 import QtGui 
import pandas as pd
from numpy import random
import messages
import numpy as np
import sys
import sip
import json


class subregionWindow(QtWidgets.QWidget):
    ''' '''

    def __init__(self, parentWindow, borders, subreg_file):
    #def __init__(self, borders, subreg_file):
    
        self.superRegion = borders # world boundaries as specified by the x/y - min/max values in main window
                
        self.subregions_file = subreg_file # json file containing subregion specifications from previos uses
        self.subRegions = json.load(open(self.subregions_file))
        
        self.nsubRegions = len(self.subRegions.keys()) # number of predefined subregions 
        self.Xs = ['x_min', 'x_max', 'y_min', 'y_max']
        
        self.labels = [] # holds the labels i.e Subregion0, Subregion1, ...
        self.custom_names = [] # holds the line edit elements for entering new borders
    
        super(subregionWindow, self).__init__(parentWindow)

        self.home()
        
    def home(self): 
        self.nsubRegionsEdit = QtWidgets.QLineEdit() # line edit element for changing agent number
        self.nsubRegionsEdit.setText(str(self.nsubRegions))
        self.nsubRegionsEdit.setValidator(QtGui.QIntValidator())

        self.nsubRegionsChange = QtWidgets.QPushButton('Change')
        self.nsubRegionsChange.clicked.connect(self.change_region_number)
        
        self.OKButton = QtWidgets.QPushButton('OK')
        self.OKButton.clicked.connect(self.pushed_ok)

        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addWidget(QtWidgets.QLabel('Number of Subregions:'), 0, 0)
        self.mainLayout.addWidget(self.nsubRegionsEdit, 0, 1)
        self.mainLayout.addWidget(self.nsubRegionsChange, 0, 2)
        self.mainLayout.addWidget(self.OKButton, 10, 10)

        self.mainLayout.addWidget(QtWidgets.QLabel('World Borders:'), 2, 1)
                
        for i, x in enumerate(self.Xs): 
            self.mainLayout.addWidget(QtWidgets.QLabel(x), 1, 2 + i)
            self.mainLayout.addWidget(QtWidgets.QLabel(str(np.round(self.superRegion[x], 2))), 2, 2 + i)
                    
        self.draw_region_edits()
        
        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.mainLayout)
        #self.home.setFont(self.parentWindow.normalFont)
        self.home.show()
        
        
        
        
    def change_region_number(self): 
        '''gets called by the Change button, changes number of selected subregions and calls the 
        draw_region_edits() function to adapt the section for specification of new subregions.'''
        
        self.nsubRegions = int(self.nsubRegionsEdit.text())
        self.draw_region_edits()

   
   
    def draw_region_edits(self): 
        ''' creates for each subregion a label and 4 line edit element. If the subregions had been 
        previously specified, respective border vaulues will be displayed. '''

        # delete previos labels and line edits, does nothing at first call
        for l in self.labels: 
            self.mainLayout.removeWidget(l)
            sip.delete(l)
            
        for cn in self.custom_names: 
            self.mainLayout.removeWidget(cn)
            sip.delete(cn)
            
        self.labels = []
        self.custom_names = []
        
        # for each subregion create 4 line edits
        for k in range(self.nsubRegions): 
            l = QtWidgets.QLabel('Subregion' + str(k))
            l.setObjectName('Subregion' + str(k))
            self.mainLayout.addWidget(l, k+3, 1)
            self.labels.append(l)
            
            for i in range(4):
                cn = QtWidgets.QLineEdit()
                cn.setObjectName('Subregion' + str(k) + self.Xs[i])
                cn.setValidator(QtGui.QDoubleValidator())
                
                if 'Subregion' + str(k) in self.subRegions.keys(): # fill with border values if known
                    cn.setText(str(np.round(self.subRegions['Subregion' + str(k)][self.Xs[i]], 2)))
                    
                self.mainLayout.addWidget(cn, k+3, 2+i)
                self.custom_names.append(cn)

            
    def pushed_ok(self): 
        ''' the subregion borders from line edit elements, checks for validity (no empty fields, 
        not exceeding world borders, min < max, ...) and dumps the results to the subregion file.
        Note that overlapping subregions are permitted. '''

        self.subRegions = {}
        
        for l in self.labels: 
            subreg = l.objectName()
            self.subRegions[subreg] = {}
            for x in self.Xs: 
                child = self.home.findChild(QtWidgets.QLineEdit, subreg + x)
                self.subRegions[subreg][x] = child.text()
        
        print(self.subRegions) 
         
        for key in self.subRegions:
            for x in self.Xs: 
            
                try: self.subRegions[key][x]= float(self.subRegions[key][x]) # check if all selcted fields are selected 
                
                except ValueError: 
                    messages.send_warning("{} has missing or invalid values".format(key))
                    return
                
                # check if selected subregions fall into world boundaries
                if (x.find('min') > -1) and (self.subRegions[key][x] < self.superRegion[x]): 
                    messages.send_warning("Borders of {}  exceed world boundaries".format(key)) 
                    return
                    
                elif (x.find('max') > -1) and (self.subRegions[key][x] > self.superRegion[x]): 
                    messages.send_warning("Borders of {}  exceed world boundaries".format(key)) 
                    return
                    
            # check if selected subregions are self consistent i.e. always min < max
            if (self.subRegions[key]['x_min'] > self.subRegions[key]['x_max']) or \
                        (self.subRegions[key]['y_min'] > self.subRegions[key]['y_max']): 
                        
                messages.send_warning("Borders of {} are inconsistent".format(key)) 
                return                 
        
        # save results to json and close application 
        with open(self.subregions_file, 'w') as sf: 
            json.dump(self.subRegions, sf) 
        
        self.home.close()

    

#if __name__ == "__main__":
#    import sys
#    import numpy as np
#    import json

#    app = QtWidgets.QApplication(sys.argv)
#    app.setApplicationName('Agent window')
#    
#    subreg_file = '/home/claudia/Dokumente/Uni/lab_rotation_FU/pyQt/preprocessing/settings/subregions.json'
#    borders = {'x_min':0, 'x_max': 100, 'y_min':0, 'y_max': 100 }
#    main = subregionWindow(borders, subreg_file)

#    #main.show()

#    sys.exit(app.exec_())       
#        
#        
