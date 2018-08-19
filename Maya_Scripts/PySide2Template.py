# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds  as mc
import maya.OpenMayaUI as omui

# Parsing PySide2 with Qt_py_master.Qt
from Qt_py_master.Qt import QtCore
from Qt_py_master.Qt import QtGui
from Qt_py_master.Qt import QtWidgets
from Qt_py_master.Qt import QtCompat

mainWindow = None

def getMayaWindow():
   '''
   Get the maya main window as a QMainWindow instance
   '''
   ptr = omui.MQtUtil.mainWindow()
   return QtCompat.wrapInstance(long(ptr), QtWidgets.QMainWindow)

def getMainWindow():
    """
    Get Maya Main window
    :return: main window 
    """
    mainWindow = QtWidgets.QApplication.activeWindow()
    while True:
        parentWin = mainWindow.parent()
        if parentWin:
            mainWindow = parentWin
        else:
            break
    return mainWindow
   
class BasicDialog(QtWidgets.QMainWindow):
    '''
    A basic demo of a Maya PyQt Window.
    '''
    def __init__(self, parent=getMayaWindow()):
        '''
        Initialize the window.
        '''
        super(BasicDialog, self).__init__(parent)#parent???

        #Window title
        self.setWindowTitle('Maya PyQt Basic Dialog Demo')
        self.createUI()

    def createUI(self):        
        ########################################################################
        #Create Widgets
        ########################################################################
        #: A QComboBox (i.e., drop-down menu) for displaying the possible shape
        #: types.
        shapeTypeCB = QtWidgets.QComboBox(parent=self)

        #: A QLineEdit (i.e., input text box) for allowing the user to specify
        #: a name for the new shape.
        nameLE = QtWidgets.QLineEdit('newShape', parent=self)

        #: A button for when the user is ready to create the new shape.
        makeButton = QtWidgets.QPushButton("Make Shape", parent=self)

        #: A descriptive label for letting the user know what his current settings
        #: will do.
        descLabel = QtWidgets.QLabel("This is a description", parent=self)

        ########################################################################
        #Layout the widgets
        ########################################################################
        central_Widget = QtWidgets.QWidget()
        self.setCentralWidget(central_Widget)
        layout = QtWidgets.QVBoxLayout(central_Widget)
        layout.addWidget(shapeTypeCB)
        layout.addWidget(nameLE)
        layout.addWidget(makeButton)
        layout.addWidget(descLabel)

def run():
    global mainWindow
    if not mainWindow or not mc.window(mainWindow, q=True, exist=True):
        mainWindow = BasicDialog() 

    print ("Opening...")
    mainWindow.show()

if __name__ == '__main__':
    run()
 