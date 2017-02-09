# -*- coding: utf-8 -*-
"""
collection some functions and classes for easier work with PyQt GUIs
"""

import sys
from PyQt4 import QtCore, QtGui
import inspect

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
  import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT


from formlayout import fedit

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class easy_edit_settings():
    """a class around formlay to give easy to use settings
    
    initalized with a list of tuples that specifiy the settings it can return
    a dictionary with the settings to easly use in the application
    """
    def __init__(self, settings):
        """ initialize the advanced settings
        
        Parameters
        ----------
        setting : list of tuples
            each entry in the list is a setting with its name as the first 
            element and current value as second like for formlayout from fedit
        """
        self.settingsDict = {}
        self.settingsList = settings
        self.update_dict()

                
    def update_dict(self):
        for element in self.settingsList:
            if type(element[1]) == list:
                self.settingsDict[element[0]] = element[1][element[1][0]+1]
            else:
                self.settingsDict[element[0]] = element[1]
    
    def get_settings(self):
        return self.settingsDict
        
    def change_settings(self):
        newSettings = fedit(self.settingsList, title="Edit advanced settings")
        if newSettings != None:
            for i, newSetting in enumerate(newSettings):
                if type(self.settingsList[i][1]) == list:
                    tempList = self.settingsList[i][1]
                    tempList[0] = newSetting
                    self.settingsList[i] = (self.settingsList[i][0],tempList)
                else:
                    self.settingsList[i] = (self.settingsList[i][0],newSetting)
            self.update_dict()


class simple_plot_window(QtGui.QMainWindow):
    """a window with a matplotlib plot
    """
    def __init__(self,parent=None,name="plot window"):
        QtGui.QMainWindow.__init__(self, parent)
        
        self.setWindowTitle(name)
        self.setObjectName(name)
        self.resize(800, 600)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.imageLayout = QtGui.QVBoxLayout()
        self.imageLayout.setObjectName(_fromUtf8("imageLayout"))
        self.gridLayout.addLayout(self.imageLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(self)

        ###
        #matplotlib setup
        
        self.fig1 = Figure()
        self.ax1 = self.fig1.add_subplot(111)

        self.canvas = FigureCanvas(self.fig1)
        self.toolbar = NavigationToolbar2QT(self.canvas, None)

        self.imageLayout.addWidget(self.canvas)
        self.imageLayout.addWidget(self.toolbar)
            


#===================================================================
# save "ui" controls and values to registry "setting"
# currently only handles comboboxes, editlines & checkboxes
# ui = qmainwindow object
# settings = qsettings object
#===================================================================

def gui_save(ui, settings):

    #for child in ui.children():  # works like getmembers, but because it traverses the hierarachy, you would have to call guisave recursively to traverse down the tree
    for name, obj in inspect.getmembers(ui):
        #if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
        if isinstance(obj, QtGui.QComboBox):
            name   = obj.objectName()      # get combobox name
            index  = obj.currentIndex()    # get current index from combobox
            text   = obj.itemText(index)   # get the text for current index
            settings.setValue(name, text)   # save combobox selection to registry

        if isinstance(obj, QtGui.QLineEdit):
            name = obj.objectName()
            value = str(obj.text())
            settings.setValue(name, value)    # save ui values, so they can be restored next time
        if isinstance(obj, QtGui.QCheckBox):
            name = obj.objectName()
            state = obj.checkState()
            settings.setValue(name, state)
        if isinstance(obj, QtGui.QSpinBox):
            name = obj.objectName()
            value = obj.value()
            settings.setValue(name,value)

#===================================================================
# restore "ui" controls with values stored in registry "settings"
# currently only handles comboboxes, editlines &checkboxes
# ui = QMainWindow object
# settings = QSettings object
#===================================================================

def gui_restore(ui, settings):

    for name, obj in inspect.getmembers(ui):
        if isinstance(obj, QtGui.QComboBox):
            index  = obj.currentIndex()    # get current region from combobox
            #text   = obj.itemText(index)   # get the text for new selected index
            name   = obj.objectName()

            value = unicode(settings.value(name))  

            if value == "":
                continue

            index = obj.findText(value)   # get the corresponding index for specified string in combobox

            if index == -1:  # add to list if not found
                obj.insertItems(0,[value])
                index = obj.findText(value)
                obj.setCurrentIndex(index)
            else:
                obj.setCurrentIndex(index)   # preselect a combobox value by index    

        if isinstance(obj, QtGui.QLineEdit):
            name = obj.objectName()
            try:
                value = settings.value(name,type=str)  # get stored value from registry
            except TypeError:
                value = None
            if value != None:
                obj.setText(unicode(value))  # restore lineEditFile

        if isinstance(obj, QtGui.QCheckBox):
            name = obj.objectName()
            try:
                value = settings.value(name,type=bool)   # get stored value from registry
            except TypeError:
                value = None
            if value != None:
                obj.setChecked(value)   # restore checkbox
                
        if isinstance(obj, QtGui.QSpinBox):
            name = obj.objectName()
            try:
                value = settings.value(name,type=int)
            except TypeError:
                value = None
            if value != None:
                obj.setValue(value)
                """
                value, good = value.toInt() #int conversion returns tuple, where the second part indicates a valid conversion
                if good:
                    obj.setValue(value)
                """
        
        #if isinstance(obj, QRadioButton):                

################################################################

if __name__ == "__main__":

    # execute when run directly, but not when called as a module.
    # therefore this section allows for testing this module!

    #print "running directly, not as a module!"
    
    import numpy as np    
    
    app = QtGui.QApplication(sys.argv)
    gui = simple_plot_window()
    x = np.linspace(0,4*np.pi,100)
    y = np.sin(x)
#    gui.ax1.plot(x,y)
    gui.show()
    sys.exit(app.exec_())