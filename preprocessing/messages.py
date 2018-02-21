from PyQt5 import QtWidgets 

def send_info(text): 
    '''Sends information dialogue '''
    
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("INFO")
    retval = msg.exec_()

def send_info_detail(text, detail = 'Sometimes more is better. But not always.'): 
    ''' creates a Qt info message with custom text''' 
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setWindowTitle("Info")
    msg.setDetailedText(detail)
    #msg.setInformativeText(detail)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setText(text)
    val = msg.exec_()
    
def send_warning(text): 
    '''Sends warning dialogue '''
    
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle("Warning")
    retval = msg.exec_()

    
def send_goodbye(folder): 
    '''Sends information dialogue '''
    
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Question)
    msg.setText("Results have been saved to {}. \n Press 'OK' to continue analysis with a new dataset or press 'Cancel' to close the application.".format(folder))
    msg.setWindowTitle("Continue?")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
    retval = msg.exec_()
    
    if retval == 1024:
        pass
    else: 
        self.close()
