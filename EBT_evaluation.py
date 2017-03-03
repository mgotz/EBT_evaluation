# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 Malte Gotz

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.



Program to evaluate EBT-films
A scannend image can be loaded and an area of interest selected
From that area a dose distrubtion can be calculated using a calibration file
and that dose distrubtion is than displayed in a seperate window

calibration location into advanced settings:
    change must trigger reload
    load adv settings before loading calibration
    load gui settings after
    
specify units in calib
"""
#modules for exception handeling
import sys
import traceback

#file manipulation and path functionality
import os

#add the modules to the search path
sys.path.append(os.path.join(sys.path[0],"common modules"))

#standard modules
import logging #logging funtionality
import sys
import numpy as np



#Qt stuff, with API variant that does not use QtVariables like QString but regular
#Python variables (saves a lot of conversion headaches)
import sip
API_NAMES = ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]
API_VERSION = 2
for name in API_NAMES:
    sip.setapi(name, API_VERSION)
    
from PyQt4 import QtCore, QtGui


from matplotlib import use
use("Qt4Agg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
  import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle


from PIL import Image #image loading functionality, could also use Pillow?

#Log widget by Andreas
import Log
#load and save GUI values
from GUI_tools import gui_save, gui_restore, simple_plot_window, easy_edit_settings
#my custom toolbar
from UI.myNavigationToolbar import myNavigationToolbar
#module with the dose calculation routines
from EBTtools.dose_calc_core import load_calibrations, dose_array
#the dose display window
from EBTtools.dose_widget import doseWidget, _advSettings
        
from UI.FilmScanMainUI import Ui_MainWindow


#define a list with advanced settings (editable via fromLayout)
#each list entry is a setting, with the first part as identifier and second as value
settingsList = [("selection rectangle","red"),
                ("legacy mode",True),
                ("histogramm bins",256),
                ("histogramm min",0),
                ("histogramm max",255)]


class MainGui(QtGui.QMainWindow):
    def __init__(self):
        """
            Constructor
        """

        QtGui.QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        self.setDockOptions(QtGui.QMainWindow.AnimatedDocks | QtGui.QMainWindow.AllowNestedDocks)
        
        #add the logging window by Andreas
        self.log_dock = Log.Log(datefmt=" ",infoString=False)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.log_dock)        
        # default log level to info
        self.log_dock.ui.comboBox.setCurrentIndex(1)


        
        #initialize the advanced settings (editable via formlayout, thus the list of tuples)
        self.advSettings = easy_edit_settings(settingsList)
        #convert settings to a dictionary for easier access                    
        self.settings = self.advSettings.get_settings()                   
        
        self.doseViewSettings = _advSettings        
         
        self.tabCounter = 0
      
        
        #matplotlib frame setup
        self.create_mplframe()

        self.load_calibrations()        

        #connect slots
        #menu items
        self.ui.actionShow_Log.triggered.connect(self.show_log)
        self.ui.actionShow_Scan.triggered.connect(self.show_scan)
        self.ui.actionScan_View_Settings.triggered.connect(self.change_advSettings)
        self.ui.actionDose_View_Settings.triggered.connect(self.change_doseViewSettings)
        #value changes
        self.ui.x0.valueChanged.connect(self.selection_changed)
        self.ui.x1.valueChanged.connect(self.selection_changed)
        self.ui.y0.valueChanged.connect(self.selection_changed)
        self.ui.y1.valueChanged.connect(self.selection_changed)
        
        #buttons
        self.ui.browseImageButton.clicked.connect(self.image_file_dialog)
        self.ui.imagePath.returnPressed.connect(self.image_path_changed)
        self.ui.loadButton.clicked.connect(self.image_path_changed)
        self.ui.showDose_button.clicked.connect(self.show_dose)    
        self.ui.calcStatsButton.clicked.connect(self.area_stats)
        self.ui.showHistoButton.clicked.connect(self.histogram)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        
        #read the settings file
        self.load_settings() 

    #redefining close event
    def closeEvent(self,event):
        #save, then close
        self.save_settings()
        event.accept()
        
##############################################################################
# methods
    ### create matplotlib frame first, then connect all the things
    def create_mplframe(self):

        ### create matplotlib figure and canvas as central widget
        self.fig = Figure()
        self.subplot = self.fig.add_subplot(111)
        #disable axis, because it will only show an image
        self.subplot.get_yaxis().set_visible(False)
        self.subplot.get_xaxis().set_visible(False)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = myNavigationToolbar(self.canvas, None)

        self.ui.imageLayout.addWidget(self.canvas)
        self.ui.imageLayout.addWidget(self.toolbar)

        #connect to the selection from the toolbar
        self.canvas.mpl_connect('selection_changed',self.toolbar_selection)

    def load_settings(self):
        #create a QSettings object from ini file
        self.QtSettings=QtCore.QSettings("settings.ini",QtCore.QSettings.IniFormat)

        #load window settings        
        self.QtSettings.beginGroup("MainWindow")
        self.restoreGeometry(self.QtSettings.value("geometry",QtCore.QByteArray(),type=QtCore.QByteArray))
        self.restoreState(self.QtSettings.value("state",QtCore.QByteArray(),type=QtCore.QByteArray))
#        self.resize(self.QtSettings.value("windowSize",QtCore.QSize(1024,1280),
#                                            type=QtCore.QSize))
        self.QtSettings.endGroup()        

        #load values for various elements        
        self.QtSettings.beginGroup("Settings")
        gui_restore(self.ui,self.QtSettings)
        self.QtSettings.endGroup()
        
    def save_settings(self):
        #save window settings
        self.QtSettings.beginGroup("MainWindow")
        self.QtSettings.setValue("geometry",self.saveGeometry())
        self.QtSettings.setValue("stat",self.saveState())
        self.QtSettings.endGroup()
        
        #save element content
        self.QtSettings.beginGroup("Settings")
        gui_save(self.ui,self.QtSettings)
        self.QtSettings.endGroup()
        
    def load_calibrations(self):
        #laod the calibration files
        try:
            self.calibrations = load_calibrations(os.path.join(os.curdir,"Calibration"))
            for key in self.calibrations:
                self.ui.calibration_selection.addItem(key,self.calibrations[key])
                idx = self.ui.calibration_selection.count()-1
                self.ui.calibration_selection.setItemData(idx,
                                                          self.calibrations[key]["tooltip"],
                                                          QtCore.Qt.ToolTipRole)
            self.ui.calibration_selection.setCurrentIndex(0)
        except (IOError, OSError) as e:                        
            logging.error("failure while reading calibration files: " + 
                           e.strerror+" at "+e.filename)                
            

        

    
##############################################################################
# slots
    
    def area_stats(self):
        x0 = self.ui.x0.value()
        x1 = self.ui.x1.value()
        y0 = self.ui.y0.value()
        y1 = self.ui.y1.value()
        
        channel = self.ui.channel_selection.itemData(self.ui.channel_selection.currentIndex())
        avg = np.average(self.npImg[y0:y1,x0:x1,channel])
        std = np.std(self.npImg[y0:y1,x0:x1,channel])
        minimum = np.min(self.npImg[y0:y1,x0:x1,channel])
        maximum = np.max(self.npImg[y0:y1,x0:x1,channel])

        logging.info("### Statistics for area x: {:d} - {:d}; y: {:d} - {:d} ###".format(x0,x1,y0,y1))
        logging.info("channel: {!s}".format(self.ui.channel_selection.currentText()))
        logging.info("average: {:.3f}".format(avg))
        logging.info("standard deviation: {:.3f}".format(std))
        logging.info("maximum: {:d}".format(maximum))        
        logging.info("minimum: {:d}".format(minimum))
        logging.info("--------------------------------------------------------------")
        
    def change_advSettings(self):
        self.advSettings.change_settings(title="advanced scan settings")
        self.settings = self.advSettings.get_settings()
    
    def change_doseViewSettings(self):
        self.doseViewSettings.change_settings(title="dose view settings")
        tabs = self.ui.tabWidget.count()
        for i in range(0,tabs):
            if self.ui.tabWidget.tabText(i) != "scan view":
                widget = self.ui.tabWidget.widget(i)
                widget.set_settings(self.doseViewSettings.get_settings())
        
    def close_tab(self, index):
        self.ui.tabWidget.removeTab(index)
        
    def histogram(self):
        #show a histgram of the selected channel
        channel = self.ui.channel_selection.itemData(self.ui.channel_selection.currentIndex())

        #create a window, the reference must be stored, because the window
        #gets destroyed when its reference is garbage collected
        #make plotWindow a list and append to that if multiple windows should be possible
        self.plotWindow = simple_plot_window(name = "histogram of {:s} channel".format(self.ui.channel_selection.currentText()))
        self.plotWindow.ax1.hist(self.npImg[self.ui.y0.value():self.ui.y1.value(),
                                            self.ui.x0.value():self.ui.x1.value(), 
                                            channel].flatten(),
                                 bins=self.settings["histogramm bins"],
                                 range=(self.settings["histogramm min"],self.settings["histogramm max"]))
        self.plotWindow.ax1.set_xlim(self.settings["histogramm min"],self.settings["histogramm max"]) 
        self.plotWindow.show()


    def image_file_dialog(self):
        filePath =QtGui.QFileDialog.getOpenFileName(self,'select a scanned image',
                                                    self.ui.imagePath.text())

        if filePath != '':
            self.ui.imagePath.setText(filePath)
            self.image_path_changed()
        else:
            logging.info('file selection canceled')
        
    def image_path_changed(self):
        #laod the image, if no path given open dialog
        if self.ui.imagePath.text() == "":
            self.image_file_dialog()
        
        #catch wrong path and permission errors
        try:
            img = Image.open(str(self.ui.imagePath.text()))
        except (IOError, OSError) as e:
            logging.error("failed to open file: "+str(e))
            return ()
        
        if self.settings["legacy mode"]:
            self.npImg = np.array(img)
        else:
            self.npImg = np.fliplr(np.array(img))
        
        logging.debug("loaded image of dimensions: "+str(self.npImg.shape)+
                      " and type: "+str(self.npImg.dtype))
                      
        #adjust UI elements to image properties
        self.ui.x0.setMaximum(self.npImg.shape[1])
        self.ui.x0.setValue(0)
        self.ui.y0.setMaximum(self.npImg.shape[0])
        self.ui.y0.setValue(0)
        self.ui.x1.setMaximum(self.npImg.shape[1])
        self.ui.x1.setValue(self.npImg.shape[1])
        self.ui.y1.setMaximum(self.npImg.shape[0])
        self.ui.y1.setValue(self.npImg.shape[0])
        
        self.ui.channel_selection.clear()
        if len(self.npImg.shape) > 2:
            if self.npImg.shape[2] == 3:
                self.ui.channel_selection.addItem("red",0)
                self.ui.channel_selection.addItem("green",1)
                self.ui.channel_selection.addItem("blue",2)
            else:
                for i in range(0,self.npImg.shape[2]):
                    self.ui.channel_selection.addItem("channel {:d}".format(i),i)
            self.ui.channel_selection.setCurrentIndex(0)
        else:
            self.ui.channel_selection.addItem("grey",0)

        #plot the image
        self.subplot.imshow(self.npImg)
        self.canvas.draw()

    def selection_changed(self):
        #try to remove old marker
        try:
            self.selectionMarker.remove()
        except AttributeError:
            pass

        #create a rectangle marker and draw it
        rect = Rectangle((self.ui.x0.value(),self.ui.y0.value()),
                         self.ui.x1.value()-self.ui.x0.value(),
                         self.ui.y1.value()-self.ui.y0.value(),
                         fill=False,color=self.settings["selection rectangle"],
                         linewidth=2.0)
        self.selectionMarker = self.subplot.add_artist(rect)
        self.canvas.draw()        

    def show_dose(self):
        logging.debug("calculating dose")
        idx = self.ui.calibration_selection.currentIndex()
        try:
            doseDistribution = dose_array(self.ui.DPI.value(),
                                          self.ui.calibration_selection.itemData(idx),
                                          self.npImg[self.ui.y0.value():self.ui.y1.value(),
                                                     self.ui.x0.value():self.ui.x1.value(),
                                                     :],
                                          self.ui.phi0.value())
            self.tabCounter += 1  
            index = self.ui.tabWidget.addTab(doseWidget(doseDistribution,settings=self.doseViewSettings.get_settings()),
                                             "dose view {:d}".format(self.tabCounter))
            self.ui.tabWidget.setCurrentIndex(index)

        except ValueError as e:
            logging.error("dose calculation failed: "+e.message)
        except KeyError as e:
            logging.error("dose calculation failed, missing key in calibration?: "+e.message)
        except Exception as e:
            logging.critical("unknown exception in dose calculation or dose display construction")
            logging.critical(traceback.format_exc())
                                         
        

       

    def toolbar_selection(self):
        #get and set selection
        selection = self.toolbar.get_selection()
        self.ui.x0.setValue(selection[0])
        self.ui.y0.setValue(selection[1]) 
        self.ui.x1.setValue(selection[2]) 
        self.ui.y1.setValue(selection[3])         




                                      

    #to show docks again, if they were closed
    def show_log(self):
        self.log_dock.setVisible(True)  

    def show_scan(self):
        if self.ui.tabWidget.tabText(0) == "scan view":
            self.ui.tabWidget.setCurrentIndex(0)
        else:
            self.ui.tabWidget.insertTab(0,self.ui.scanTab,"scan view")
      
       

###############################################################################
# run

def run():
    app = QtGui.QApplication(sys.argv)
    gui = MainGui()
    gui.show()
    sys.exit(app.exec_())

#run the gui
if __name__ == '__main__':
    run()         