import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as np
import pandas as pd
from standard_stats import means_and_vars
from standard_stats import handle_data #TODO: Generealize

from plotWindow import MyPlotWindow


image = '/home/claudia/Bilder/other/frida.jpg'

class MyStream(QObject):
    message = pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))


class window(QMainWindow):
   
    NOTES_SAVE_FILE = 'Notes.txt'        # default name for file created from notepad TODO: allow customize
    DATA_SAVE_FILE = 'Data.csv'
    DATA_CLEAN = pd.DataFrame()     # a pandas df containing the data that will be worked with 
    DATA_SPECIFICATIONS = {'start_time':0, 'stop_time':0} # dict that contains all user specificaton on data
    DATA_FILE = ' '                 # name of the datafile (for reference)
    TIME = 0                        # np.array conatining the time points (for setting the sliders)

    def __init__(self):
    
        super(window, self).__init__()
        self.setWindowTitle("Doing things and stuff")
        self.setWindowIcon(QIcon(image))
        
        extractAction = QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        openFile = QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(openFile)
        
        

        self.home()
        
    def home(self):
    
        # ----------------------------------------------------- 
        # Right side of main window
        #------------------------------------------------------

        self.rightSide = QVBoxLayout()
   
        # ------------------- note pad------------------------
        self.notesSection = QHBoxLayout()
        
        self.NotePad = QTextEdit()
        self.notesSection.addWidget(self.NotePad)

        # -------------------buttons--------------------------
        self.notesButtonSection = QHBoxLayout()
        
        self.SaveButton_notePad = QPushButton("Save")
        self.SaveButton_notePad.clicked.connect(self.save_NotePad)
        
        self.ClearButton_notePad = QPushButton("Clear")
        self.ClearButton_notePad.clicked.connect(self.clear_NotePad)
        
        self.notesButtonSection.addWidget(self.SaveButton_notePad)
        self.notesButtonSection.addWidget(self.ClearButton_notePad)
        
        # ----------------arange stuff in right part----------
        self.rightSide.addLayout(self.notesSection)
        self.rightSide.addLayout(self.notesButtonSection)
    
        
        # ----------------------------------------------------- 
        # Right side of main window
        #------------------------------------------------------
    
        self.leftSide = QVBoxLayout()
        
        #--------------------data section----------------------
        self.dataSection = QGridLayout()
        
        self.FileChosen = QLabel('File Chosen: None')
        
        self.CheckRobo = QCheckBox('Robo')
        self.CheckRobo.stateChanged.connect(self.do_nothing)
        
        self.CheckFish = QCheckBox('Fish')
        self.CheckFish.stateChanged.connect(self.do_nothing)
        
        self.StartTimeSliderTitle = QLabel('Start')
        self.StartTimeSlider = QSlider(Qt.Horizontal)
        self.StartTimeSlider.valueChanged.connect(self.set_time)
        self.StartTime = QLineEdit()
        
        self.StopTimeSliderTitle = QLabel('Stop')
        self.StopTimeSlider = QSlider(Qt.Horizontal)
        self.StopTimeSlider.valueChanged.connect(self.set_time)
        self.StopTime = QLineEdit()


        self.dataSection.addWidget(self.FileChosen, 0, 0, 1, 2 )
        
        self.dataSection.addWidget(self.CheckRobo, 1, 0)
        self.dataSection.addWidget(self.CheckFish, 1, 1)
        
        self.dataSection.addWidget(self.StartTimeSliderTitle, 2, 0)
        self.dataSection.addWidget(self.StartTimeSlider, 2, 1)        
        self.dataSection.addWidget(self.StartTime, 2, 2)
        
        self.dataSection.addWidget(self.StopTimeSliderTitle, 3, 0)
        self.dataSection.addWidget(self.StopTimeSlider, 3, 1)        
        self.dataSection.addWidget(self.StopTime, 3, 2)
        
         
         #--------------------data section buttons --------------
        self.dataButtonsSection = QHBoxLayout()

        self.DataSettings = QPushButton('Settings')
        self.DataPrint = QPushButton('Print')
        
        self.DataPlot = QPushButton('Plot')
        self.DataPlot.clicked.connect(self.plot_trajectory)
        
        
        self.DataFreeze = QPushButton('Freeze')
        self.DataFreeze.clicked.connect(self.on_freeze)
        

        self.dataButtonsSection.addWidget(self.DataSettings)
        self.dataButtonsSection.addWidget(self.DataPrint)
        self.dataButtonsSection.addWidget(self.DataPlot)
        self.dataButtonsSection.addWidget(self.DataFreeze)
                                    
        
        #--------------------stats section----------------------
        self.statsSection = QGridLayout()
        
        self.SelectStats = QComboBox()
        self.SelectStats.addItem('Method 1')
        self.SelectStats.addItem('Method 2')
        #self.cb.addItems(["Java", "C#", "Python"])
        self.SelectStats.currentIndexChanged.connect(self.do_nothing)
        
        self.ParamInfoLabel = QLabel('Parameter Info')
        self.ParamInfo = QLineEdit()
        
        self.statsSection.addWidget(self.SelectStats, 1, 0, 1, 3)
        self.statsSection.addWidget(self.ParamInfoLabel, 2, 0)
        self.statsSection.addWidget(self.ParamInfo, 3, 0, 5, 3)
        
        
        #--------------------stats Button Section----------------------
        self.statsButtonSection = QHBoxLayout()
        
        self.StatsSettings = QPushButton('Settings')
        self.StatsPrint = QPushButton('Print')
        self.StatsPlot = QPushButton('Plot')
        self.StatsSave = QPushButton('Save')
        
        self.statsButtonSection.addWidget(self.StatsSettings)
        self.statsButtonSection.addWidget(self.StatsPrint)
        self.statsButtonSection.addWidget(self.StatsPlot)
        self.statsButtonSection.addWidget(self.StatsSave)
        
        
        #--------------------general Button Section----------------------
        self.generalButtonSection = QHBoxLayout()
        
        self.SaveButton_general = QPushButton('Save all')
        self.SaveButton_general.clicked.connect(self.save_all)


        self.generalButtonSection.addWidget(self.SaveButton_general)

        
        
        # ----------------arange stuff in left part----------
        self.leftSide.addLayout(self.dataSection)
        self.leftSide.addLayout(self.dataButtonsSection)
        self.leftSide.addStretch()
        self.leftSide.addLayout(self.statsSection)
        self.leftSide.addLayout(self.statsButtonSection)
        self.leftSide.addStretch()
        self.leftSide.addLayout(self.generalButtonSection)

        
        # ----------------------------------------------------- 
        # Arange Stuff in Main Window
        #------------------------------------------------------

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftSide)
        self.mainLayout.addLayout(self.rightSide)


        self.home = QWidget()
        self.home.setLayout(self.mainLayout)
        self.setCentralWidget(self.home)
        
        
    # ----------------------------------------------------- 
    # Genereal functions
    #-----------------------------------------------------

    def do_nothing(self): 
        ''' does nothing '''
        print('did nothing')
        
    def save_all(self): 
        ''' saves cleaned data to csv, notepad to txt'''
        #TODO save stats results 
        self.save_DataClean()
        self.save_NotePad()
        print('saved clean data to: ', self.DATA_SAVE_FILE)
        print('saved notes to: ', self.NOTES_SAVE_FILE) 
        
    def close_application(self):
        ''' Closes application without saving '''
        choice = QMessageBox.question(self, 'Extract!','Close without saving?', \
                 QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Leaving")
            sys.exit()
        else:
            pass
        
    # ----------------------------------------------------- 
    # Note Pad related functions
    #-----------------------------------------------------
    
    @pyqtSlot(str)
    def on_myStream_message(self, message):
        '''Writes all print commands to the notepad'''
        self.NotePad.moveCursor(QTextCursor.End)
        self.NotePad.insertPlainText(message)
        
    def clear_NotePad(self): 
        ''' Clears all Notepad output'''
        self.NotePad.clear()
        
    def save_NotePad(self): 
        ''' Saves all Notepad output to txt'''
        with open(self.NOTES_SAVE_FILE, 'w') as txt_file: 
            txt_file.write(str(self.NotePad.toPlainText()))
            
            
    # ----------------------------------------------------- 
    # Data related functions
    #-----------------------------------------------------    
            
    def file_open(self):
        ''' opens a dialog and lets the user chose a csv datafile, 
        this is then passed to the handle_data function and 
        the global variables DATA_CLEAN, TIME, DATA_SPECIFICATIONS and 
        DATA_NAME are initialized '''
    
        name = QFileDialog.getOpenFileName(self, 'Open File')
        if not name.endswith('.csv'):
        
            print('File Type not allowed')
            pass
            
        else: 
            self.DATA_CLEAN = handle_data(name)         
            self.TIME = self.DATA_CLEAN['time'].values
            self.DATA_NAME = name
            self.DATA_SPECIFICATIONS['start_time'] = self.TIME[0]
            self.DATA_SPECIFICATIONS['stop_time'] = self.TIME[-1]
            self.FileChosen.setText('File Chosen: ' + self.DATA_NAME[self.DATA_NAME.rfind('/')+1:])



    def set_time(self):
        ''' handles change of sliders'''
    
        start = self.StartTimeSlider.value()
        self.StartTime.setText(str(np.round(self.TIME[start], 2)))
        self.DATA_SPECIFICATIONS['start_time'] = start


        stop = self.StopTimeSlider.value()
        self.StopTime.setText(str(np.round(self.TIME[stop], 2)))
        self.DATA_SPECIFICATIONS['stop_time'] = stop
        
        
    def plot_trajectory(self):
        ''' plots the trajectory in the chosen time range'''
        if self.DATA_CLEAN.empty:
            print('No File Chosen')
            
        else: 
            #TODO This should be a little more general :)
            t1 = self.DATA_SPECIFICATIONS['start_time']
            t2 = self.DATA_SPECIFICATIONS['stop_time']
            data2plot = np.vstack((self.DATA_CLEAN['x0'][t1: t2], self.DATA_CLEAN['y0'][t1:t2]))
            plot_window = MyPlotWindow(data2plot)
            plot_window.exec_()
            
    def save_DataClean(self): 
        # TODO this never gets called alone, maybe single data save button?
        self.DATA_CLEAN.to_csv(self.DATA_SAVE_FILE)
        
        
    def on_freeze(self):
        ''' freezs data settings '''
        if self.DataFreeze.text() == 'Freeze':
            self.CheckRobo.setEnabled(False)
            self.CheckFish.setEnabled(False)
            self.StartTimeSliderTitle.setEnabled(False)
            self.StartTimeSlider.setEnabled(False)
            self.StartTime.setEnabled(False)
            self.StopTimeSliderTitle.setEnabled(False)
            self.StopTimeSlider.setEnabled(False)
            self.StopTime.setEnabled(False)
            
            self.DataFreeze.setText('Unfreeze')
        else: 
            self.CheckRobo.setEnabled(True)
            self.CheckFish.setEnabled(True)
            self.StartTimeSliderTitle.setEnabled(True)
            self.StartTimeSlider.setEnabled(True)
            self.StartTime.setEnabled(True)
            self.StopTimeSliderTitle.setEnabled(True)
            self.StopTimeSlider.setEnabled(True)
            self.StopTime.setEnabled(True)
            
            self.DataFreeze.setText('Freeze')
            



if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setApplicationName('window')


    main = window()
    main.show()
    
    myStream = MyStream()
    myStream.message.connect(main.on_myStream_message)

    sys.stdout = myStream        


    sys.exit(app.exec_())
