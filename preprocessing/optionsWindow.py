import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont   
from PyQt5 import QtGui 
import json
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import messages

class optionsWindow(QtWidgets.QWidget): 

    def __init__(self, parentWindow):
    #def __init__(self, optionsFile, parent = None):

        super(optionsWindow, self).__init__(parentWindow)
        #super(optionsWindow, self).__init__(parent)
        self.parentWindow = parentWindow
        self.optionsFile = parentWindow.OPTIONS_INFO_FILE
        self.setFixedSize(300,200)
        self.TE_PARAMS_FILE = self.parentWindow.TE_PARAMS_FILE
        #self.optionsFile = optionsFile
        self.home()
        
    def home(self):
    
        self.layout = QtWidgets.QVBoxLayout(self)
 
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()	
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        #self.tab4 = QtWidgets.QWidget()
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.tab1,"Plots")
        self.tabs.addTab(self.tab2,"Folders")
        self.tabs.addTab(self.tab3, "Transfer Entropy")
        #self.tabs.addTab(self.tab4, "Subregions")
 
        #--------------------------------------------------------------------
        # Plot Tab
        #--------------------------------------------------------------------
        self.Tab1layout = QtWidgets.QVBoxLayout()       
        
        # use previously selected plot options for initialization
        options = json.load(open(self.optionsFile))
        plot_options = options['plot_options']
        plot_selection = options['plot_selection']
        
        # select all plot options
        self.checkAll = QtWidgets.QCheckBox('all')
        self.checkAll.clicked.connect(self.clicked_checkBox)
        if plot_selection[0] == "all" or len(plot_selection) == len(plot_options): 
            self.checkAll.setCheckState(2)
        
        # select no plot option 
        self.checkNone = QtWidgets.QCheckBox('none')
        self.checkNone.clicked.connect(self.clicked_checkBox)
        if plot_selection[0] == "none": 
            self.checkNone.setCheckState(2)

        # list all plot options for individual selection 
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSelectionMode(2)
        self.listWidget.clicked.connect(self.clicked_list)

        
        for i in range(len(plot_options)):
            item = QtWidgets.QListWidgetItem(plot_options[i])
            self.listWidget.addItem(item)
            if self.checkAll.checkState == 2 or plot_options[i] in plot_selection: 
                item.setSelected(True)
        
        # ok button to save selection         
        self.okButton = QtWidgets.QPushButton('ok')
        self.okButton.clicked.connect(self.save_selection)

        self.Tab1layout.addWidget(self.checkAll)
        self.Tab1layout.addWidget(self.checkNone)
        self.Tab1layout.addWidget(self.listWidget)
        self.Tab1layout.addWidget(self.okButton)
        
        self.tab1.setLayout(self.Tab1layout)


        #--------------------------------------------------------------------
        # Folder Tab
        #--------------------------------------------------------------------
        self.Tab2layout = QtWidgets.QGridLayout()
        
        bold_font = QFont('Helvetica', 10, QFont.Bold)
        self.DataSourceLabel = QtWidgets.QLabel('Data Folder:')
        self.DataSourceLabel.setFont(bold_font)
        self.DataSource = QtWidgets.QLabel(options['data_folder'])
        
        self.SaveFolderLabel = QtWidgets.QLabel('Save Folder:')
        self.SaveFolderLabel.setFont(bold_font)
        self.SaveFolder = QtWidgets.QLabel(options['save_folder'])
        
        self.SaveStatsLabel = QtWidgets.QLabel('Statistcis File:')
        self.SaveStatsLabel.setFont(bold_font)
        self.SaveStats = QtWidgets.QLabel(options['info_file'])
        
        self.SaveTimeLabel = QtWidgets.QLabel('Timeline File:')
        self.SaveTimeLabel.setFont(bold_font)
        self.SaveTime = QtWidgets.QLabel(options['timeline_file'])
        
        
        self.Tab2layout.addWidget(self.DataSourceLabel, 0, 0)
        self.Tab2layout.addWidget(self.DataSource, 0, 1)        
        self.Tab2layout.addWidget(self.SaveFolderLabel, 1, 0)        
        self.Tab2layout.addWidget(self.SaveFolder, 1, 1)
        self.Tab2layout.addWidget(self.SaveStatsLabel, 2, 0)        
        self.Tab2layout.addWidget(self.SaveStats, 2, 1)
        self.Tab2layout.addWidget(self.SaveTimeLabel, 3, 0)        
        self.Tab2layout.addWidget(self.SaveTime, 3, 1)
        
        
        self.tab2.setLayout(self.Tab2layout)
        
        
        #--------------------------------------------------------------------
        # Statistics Tab
        #--------------------------------------------------------------------
        self.Tab3layout = QtWidgets.QGridLayout()
        
        self.checkTE = QtWidgets.QCheckBox('Transfer Entropy')
        self.checkTE.setCheckState(options['TE'])
        self.checkTE.toggled.connect(self.selectTE)
        
        self.TE_info = QtWidgets.QPushButton('Info')
        self.TE_info.clicked.connect(self.display_TE_Info)


        self.paramLabel = QtWidgets.QLabel('Note: Calculating transfer entropy is computationally\nexpensive and may take several seconds!')
       
        self.okTEButton = QtWidgets.QPushButton('OK')
        self.okTEButton.clicked.connect(self.TE_ok_pressed)
        self.resetButton = QtWidgets.QPushButton('Reset')
        self.resetButton.clicked.connect(self.TE_reset_pressed)
        
        self.Tab3layout.addWidget(self.checkTE, 0, 0)
        self.Tab3layout.addWidget(self.TE_info, 0, 5)
        self.Tab3layout.addWidget(self.paramLabel, 2, 0)
        
        self.init_TE_params()
        
        self.Tab3layout.addWidget(self.resetButton, 7, 4)
        self.Tab3layout.addWidget(self.okTEButton, 7, 5)


        self.tab3.setLayout(self.Tab3layout)

        
        

        #--------------------------------------------------------------------
        # FInal Tab
        #--------------------------------------------------------------------    
        self.layout.addWidget(self.tabs)
        self.home = QtWidgets.QWidget()
        self.home.setLayout(self.layout)
        self.home.setFont(self.parentWindow.normalFont)
        self.home.show()
    
        
    def save_selection(self): 
        '''When OK is pressed the current selction of plit options will be saved to the options file 
        to be used in all further calls to the plot function until changed again.'''
        options = json.load(open(self.optionsFile))
        
        plot_selection = [item.text() for item in self.listWidget.selectedItems()]
        
        if len(plot_selection) > 0: 
            options['plot_selection'] = plot_selection
        else: 
            if self.checkAll.checkState() == 2: 
                options['plot_selection'] = options['plot_options']
            else: 
                options['plot_selection'] = ["none"]
       
        with open(self.optionsFile, 'w') as of: 
            json.dump(options, of)

            
    def clicked_list(self): 
        ''' If the list widget is clicked for individual selection, both checkboxes will be unchecked'''
        self.checkAll.setCheckState(0) 
        self.checkNone.setCheckState(0)
        
            
    def clicked_checkBox(self): 
        ''' Selecting the all or none Checkbox will either select or deselect all list items.'''
        if self.sender().text() == 'all': 
            self.checkAll.setCheckState(2) 
            self.checkNone.setCheckState(0)
            self.listWidget.selectAll()
            
        elif self.sender().text() == 'none': 
            self.checkAll.setCheckState(0) 
            self.checkNone.setCheckState(2)
            self.listWidget.clearSelection()
        
        else: 
    
            pass
            
    def init_TE_params(self): 
    
        self.TE_lineEdits = []
        labels = ['Start Frame', 'Frame Step', 'Max Time', 'K']
        names = ['start_frame', 'frame_step', 'max_time', 'k_te']
        toolTips = ['Frame to take as starting point for calculation', 'Stepsize for downsampling.\nE.g. if Frame Step = 3 only every third frame is considered for calculation.\nFor large datasets this may speed up calculation', 'Maximum time lag in seconds.', 'Length of vectors'
        ]
        te_params = json.load(open(self.TE_PARAMS_FILE))

        
        for i in range(len(names)): 
            label = QtWidgets.QLabel(labels[i])
            label.setToolTip(toolTips[i])
            le = QtWidgets.QLineEdit(str(te_params[names[i]]))
            le.setObjectName(names[i])
            le.setFixedWidth(70)
            le.setValidator(QtGui.QDoubleValidator())
            
            self.TE_lineEdits.append(le)
            
            self.Tab3layout.addWidget(label, 3 +i, 0, 1, 1)
            self.Tab3layout.addWidget(le, 3 +i, 1, 1, 1)

               
    def TE_ok_pressed(self):
        '''saved the user specific TE values to dictionary'''   
        te_params = json.load(open(self.TE_PARAMS_FILE))
        for le in self.TE_lineEdits: 
            try: 
                float(le.text())
            except ValueError: 
                messages.send_warning('Parameter fields can not be empty!')
            te_params[le.objectName()] = le.text()
        
        print(te_params)
        
        with open(self.TE_PARAMS_FILE, 'w') as tf: 
            json.dump(te_params, tf)
            
        
    def TE_reset_pressed(self):
        '''Writes the default values for TE to the respective line edit elements '''   
        te_params = json.load(open(self.TE_PARAMS_FILE))
        te_reset = te_params['reset']
        
        for key in enumerate(te_reset.keys()): 
            te_params[key[1]] = te_reset[key[1]]#child = self.home.findChild(QtWidgets.QLineEdit, subreg + x)
            le = self.tab3.findChild(QtWidgets.QLineEdit, key[1])
            le.setText(str(te_reset[key[1]]))

        with open(self.TE_PARAMS_FILE, 'w') as tf: 
            json.dump(te_params, tf)
    
    
    def selectTE(self): 
        options = json.load(open(self.optionsFile))
        options['TE'] = self.checkTE.checkState()
        with open(self.optionsFile, 'w') as of: 
            json.dump(options, of)

    def display_TE_Info(self):        
#            self.explainTE = QtWidgets.QLabel("If enabled the Transfer Entropy (TE) between two agent's velocity vectors will be calculated. For reliabale results make sure that only two agents are selcted and sufficintly many datapoints are available. Results include TE.csv containing a TE values for different lag-times and directions (Information flow from agent 1 to agent 2 as well as from agent 2 to agent 1)  as well as a plot. Calculation uses entropy estimators by Greg Ver Steeg (http://www.isi.edu/~gregv/npeet.html). ")
#        self.explainTE.setWordWrap(True)
        text = "If enabled the Transfer Entropy (TE) between two agent's velocity vectors will be calculated. For reliabale results make sure that only two agents are selcted and sufficintly many datapoints are available. Results include TE.csv containing a TE values for different lag-times and directions (Information flow from agent 1 to agent 2 as well as from agent 2 to agent 1)  as well as a plot. Calculation uses entropy estimators by Greg Ver Steeg (http://www.isi.edu/~gregv/npeet.html). "
        messages.send_info(text)
#if __name__ == "__main__":
#    import sys
#    import numpy as np

#    app = QtWidgets.QApplication(sys.argv)
#    app.setApplicationName('Options')
#    data = '/home/claudia/Dokumente/Uni/lab_rotation_FU/pyQt/preprocessing/settings/options.json'
#    main = optionsWindow(data)
#    #main.show()

#    sys.exit(app.exec_())       























