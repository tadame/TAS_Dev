#===============================================================================
# By Tomas Adame Salguero
# t4dame@gmail.com
# Last Updated: 2018/08/19
#
# Maya - Object counter utility UI
#
# V0.4 - To be ported to Pyside2
#===============================================================================
## Importing
import pymel.core as pm
import maya.cmds  as mc
import maya.OpenMayaUI as omui

# Parsing PySide2 with Qt_py_master.Qt
from Qt_py_master.Qt import QtCore
from Qt_py_master.Qt import QtGui
from Qt_py_master.Qt import QtWidgets
from Qt_py_master.Qt import QtCompat

import os
import sys

#import Utilities.ObjectCounter.objectCounter as oCounter;reload(oCounter)
import objectCounter as oCounter;reload(oCounter)
reload(oCounter)

## Empty Vars
selMode     = "All"
dialog      = None


def getMayaWindow():
   '''
   Get the maya main window as a QMainWindow instance
   '''
   ptr = omui.MQtUtil.mainWindow()
   return QtCompat.wrapInstance(long(ptr), QtWidgets.QMainWindow)

    
class SVCreatorWindow(QtWidgets.QDialog):
    def __init__(self, parent=getMayaWindow()):
        super(SVCreatorWindow, self).__init__(parent)
        #Window title
        self.setWindowTitle('Selection counter')
        self.setFixedWidth(250)
        self.setFixedHeight(190)

        self.create_layout()
        self.create_connections()

        # Help Button
        # self.helpTool = QtWidgets.Qt.WindowContextHelpButtonHint
        # self.helpTool.exec_()

    def create_layout(self):
        """
        Create Widgets
        """
        # Help Button
        self.helpButton = QtWidgets.QPushButton("Help")
        self.helpButton.setFixedHeight(15)
        self.helpButton.setFixedWidth(40)
        self.helpButton.setStyleSheet("background:transparent")
        self.helpButton.setFlat(True)

        # FilterBox Label and LineEdit
        self.svNameLabel = QtWidgets.QLabel("Keywords:", parent=self)
        self.nameLE = QtWidgets.QLineEdit(parent=self)
        self.nameLE.setFixedWidth(150)
        self.nameLE.setAlignment(QtCore.Qt.AlignLeft)
        self.nameLE.setPlaceholderText("Keywords to search?")

        # reg_ex = QtCore.QRegExp("^(?!^_)[\w__][a-zA-Z_]+")
        reg_ex = QtCore.QRegExp("[a-zA-Z_]+")
        text_validator = QtGui.QRegExpValidator(reg_ex, self.nameLE)
        self.nameLE.setValidator(text_validator)

        # Filter CheckBox
        self.filterCheck = QtWidgets.QCheckBox('Use filter:', parent=self)
        self.filterCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.filterCheck.setFixedWidth(85)

        # All/Selection Buttons
        self.selMode     = QtWidgets.QLabel('Selection Mode:')
        self.allRadio    = QtWidgets.QRadioButton('All')
        self.allRadio.setFixedHeight(19)
        self.allRadio.setChecked(False)
        self.selectedRadio = QtWidgets.QRadioButton('Selected')
        self.selectedRadio.setFixedHeight(19)
        self.selectedRadio.setChecked(True)

        # Button Widgets
        self.runButton    = QtWidgets.QPushButton("Run")
        self.closeButton  = QtWidgets.QPushButton("Close")

        #Description
        self.descLabel = QtWidgets.QLabel("This tool will help to count elements \nin the scene.", parent=self)
        self.descLabel.setAlignment(QtCore.Qt.AlignBottom)

        """
        Layout the widgets
        """
        # Help Layout
        helpButtonLayout = QtWidgets.QHBoxLayout()
        helpButtonLayout.setContentsMargins(4,0,4,0)
        helpButtonLayout.setSpacing(2)
        helpButtonLayout.addStretch()
        helpButtonLayout.addWidget(self.helpButton)

        # Name Layout
        nameLayout = QtWidgets.QHBoxLayout()
        nameLayout.setContentsMargins(4,0,4,0)
        nameLayout.setSpacing(2)
        nameLayout.addWidget(self.svNameLabel)
        spacerItem = QtWidgets.QSpacerItem(5,5,QtWidgets.QSizePolicy.Expanding)
        nameLayout.addSpacerItem(spacerItem)
        nameLayout.addWidget(self.nameLE)

        # CheckBox Layout
        checkboxLayout = QtWidgets.QHBoxLayout()
        checkboxLayout.addStretch()
        checkboxLayout.setContentsMargins(4,0,4,0)
        checkboxLayout.setSpacing(2)
        checkboxLayout.addWidget(self.filterCheck)

        #ALL/Selection Layout
        selectionLayout = QtWidgets.QHBoxLayout()
        selectionLayout.addWidget(self.selMode)
        selectionLayout.setContentsMargins(4,0,4,0)
        selectionLayout.setSpacing(2)
        spacerItem = QtWidgets.QSpacerItem(5,5,QtWidgets.QSizePolicy.Expanding)
        selectionLayout.addSpacerItem(spacerItem)
        selectionLayout.addWidget(self.allRadio)
        selectionLayout.addWidget(self.selectedRadio)

        #Button Layout
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.runButton)
        buttonLayout.addWidget(self.closeButton)

        #Splitter Layout
        uiSplitter = Splitter()
        spliterLayout = QtWidgets.QHBoxLayout()
        spliterLayout.layout().addWidget(uiSplitter)

        #Description Layout
        descriptionLayout = QtWidgets.QHBoxLayout()
        descriptionLayout.addWidget(self.descLabel)


        #Layout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(5,5,5,5)
        mainLayout.setSpacing(5)
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.layout().addLayout(helpButtonLayout)
        mainLayout.layout().addLayout(SplitterLayout())
        mainLayout.addLayout(nameLayout)
        mainLayout.addLayout(checkboxLayout)
        mainLayout.layout().addLayout(SplitterLayout())
        mainLayout.addLayout(selectionLayout)
        mainLayout.layout().addLayout(SplitterLayout())
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(spliterLayout)
        mainLayout.addLayout(descriptionLayout)

        self.setLayout(mainLayout)

    ###############################################
    #Geters
    ###############################################
    def setSearchFilter(self):
        searchFilter = str(self.nameLE.text())
        if not searchFilter:
            return "None"
        #print "Your selection is %s" % variantName
        return searchFilter

    def getSearchFilterCB(self):
        if self.filterCheck.isChecked():
            searchFilterCB = "True"
        else:
            searchFilterCB = "False"
        return searchFilterCB

    def selectionMode(self):
        if self.allRadio.isChecked():
            selMode = "All"
        else:
            selMode = "Selection"
        #print "Your selection is %s" % selMode
        return selMode

    ###############################################
    #Connections
    ###############################################

    def create_connections(self):
        searchFilter = self.nameLE.editingFinished.connect(self.setSearchFilter)
        self.helpButton.clicked.connect(self.openConfluencePage)
        self.runButton.clicked.connect(self.runScript)
        self.closeButton.clicked.connect(self.close_dialog)        


    ###############################################
    #RUN
    ###############################################
    def openConfluencePage(self):
        # helpPage = "Confluence URL Removed"
        help_page = "https://github.com/tadame/TAS_Dev/tree/master/Maya_Scripts/Tools/Utilities/ObjectCounter"
        QtGui.QDesktopServices.openUrl(helpPage)

    def runScript(self):
        searchForFilter = self.setSearchFilter()
        #print searchForFilter
        searchFilterCB = self.getSearchFilterCB()
        #print searchFilterCB
        selMode = self.selectionMode()
        print "Running tool on: %s, %s & %s" %(selMode, searchForFilter, searchFilterCB)
        try:
            oCounter.printResults(selMode, searchForFilter, searchFilterCB)
        except:
            pass

    def close_dialog(self):
        print "Closing"
        self.close()

#------------------------------------------------------------------------------#

class Splitter(QtWidgets.QWidget):
    def __init__(self, text=None, shadow=True, color=(150, 150, 150)):
        QtWidgets.QWidget.__init__(self)

        self.setMinimumHeight(2)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignVCenter)

        first_line = QtWidgets.QFrame()
        first_line.setFrameStyle(QtWidgets.QFrame.HLine)
        self.layout().addWidget(first_line)

        main_color   = 'rgba( %s, %s, %s, 255)' %color
        shadow_color = 'rgba( 45,  45,  45, 255)'

        bottom_border = ''
        if shadow:
            bottom_border = 'border-bottom:1px solid %s;' %shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color: %s; \
                       max-height:1px; \
                       %s" %(main_color, bottom_border)

        first_line.setStyleSheet(style_sheet)

        if text is None:
            return

        first_line.setMaximumWidth(5)

        font = QtWidgets.QFont()
        font.setBold(True)

        text_width = QtWidgets.QFontMetrics(font)
        width = text_width.width(text) + 6

        label = QtWidgets.QLabel()
        label.setText(text)
        label.setFont(font)
        label.setMaximumWidth(width)
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.layout().addWidget(label)

        second_line = QtWidgets.QFrame()
        second_line.setFrameStyle(QtWidgets.QFrame.HLine)
        second_line.setStyleSheet(style_sheet)
        self.layout().addWidget(second_line)


class SplitterLayout(QtWidgets.QHBoxLayout):
    def __init__(self):
        QtWidgets.QHBoxLayout.__init__(self)
        self.setContentsMargins(5,2,5,2)

        splitter = Splitter(shadow=False, color=(60,60,60))
        splitter.setFixedHeight(1)

        self.addWidget(splitter)


#------------------------------------------------------------------------------#

def create():
    global my_window
    try:
        my_window.close()
        my_window.deleteLater()
    except: pass
    my_window = SVCreatorWindow()
    my_window.show()

create()
