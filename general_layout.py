import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


image = '/home/claudia/Bilder/other/frida.jpg'

class MyStream(QObject):
    message = pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))


class window(QMainWindow):
   
    NOTES_FILE = 'Notes.txt'

    def __init__(self):
    
        super(window, self).__init__()
        self.setWindowTitle("Doing things and stuff")
        self.setWindowIcon(QIcon(image))
        
        extractAction = QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.do_nothing)

        openFile = QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.do_nothing)

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
        self.SaveButton_notePad.clicked.connect(self.saveNotePad)
        
        self.ClearButton_notePad = QPushButton("Clear")
        self.ClearButton_notePad.clicked.connect(self.clearNotePad)
        
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
        self.StartTimeSlider.valueChanged.connect(self.do_nothing)
        self.StartTime = QLineEdit()
        
        self.StopTimeSliderTitle = QLabel('Stop')
        self.StopTimeSlider = QSlider(Qt.Horizontal)
        self.StopTimeSlider.valueChanged.connect(self.do_nothing)
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
        self.DataFreeze = QPushButton('Freeze')

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
        
        self.GeneralSave = QPushButton('Save all')

        self.generalButtonSection.addWidget(self.GeneralSave)

        
        
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
        

    def do_nothing(self): 
        print('did nothing')
        
    # ----------------------------------------------------- 
    # Note Pad related functions
    #-----------------------------------------------------
    
    @pyqtSlot(str)
    def on_myStream_message(self, message):
        '''Writes all print commands to the notepad'''
        self.NotePad.moveCursor(QTextCursor.End)
        self.NotePad.insertPlainText(message)
        
    def clearNotePad(self): 
        ''' Clears all Notepad output'''
        self.NotePad.clear()
        
    def saveNotePad(self): 
        ''' Saves all Notepad output to txt'''
        with open(self.NOTES_FILE, 'w') as txt_file: 
            txt_file.write(str(self.NotePad.toPlainText()))

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setApplicationName('window')


    main = window()
    main.show()
    
    myStream = MyStream()
    myStream.message.connect(main.on_myStream_message)

    sys.stdout = myStream        


    sys.exit(app.exec_())
