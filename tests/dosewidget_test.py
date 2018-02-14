# -*- coding: utf-8 -*-
"""
a simple wrapper to run/test the dosewidget
not really an automated test of any kind (yet?)
"""

#get ready for python 3
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

import logging
import numpy as np
import os
import sys

os.environ["QT_API"] = "pyqt5"

#add base to path and load
sys.path.append(os.path.join(sys.path[0],".."))
from ebttools.gui.dosewidget import DoseWidget
from ebttools.core import DoseArray

#the init should ensure that this is set correctly
if os.environ["QT_API"] == "pyqt5":     
    from testwindow_ui_qt5 import Ui_MainWindow
    from PyQt5.QtWidgets import (QMainWindow, QApplication)
else:
 
    from testwindow_ui_qt4 import Ui_MainWindow
    from PyQt4.QtGui import (QMainWindow, QApplication) 




#a simple window to take the dosewidget
class TestGUI(QMainWindow):
    """simple main window to test the widget
    """
    def __init__(self):
        """
            Constructor
        """

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self) 
        
        xDim = 470 
        yDim = 470
        
        #create a noise gaussian for test data
        x,y = np.meshgrid(np.linspace(0,xDim,yDim),np.linspace(0,xDim,yDim))
        dose = (5.0*np.exp(-np.divide(np.square(x-100),2*50**2)-np.divide(np.square(y-235),2*100**2))
            +np.random.rand(xDim,yDim)*0.1)
    
        dose = dose.view(DoseArray)
        widget = DoseWidget(dose)
        
        self.ui.tabWidget.addTab(widget,"DoseView 1")

def run():
    #setup a basic logger and start the app
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)
    gui = TestGUI()

    gui.show()
    sys.exit(app.exec_())

#run the gui
if __name__ == '__main__':
    run() 