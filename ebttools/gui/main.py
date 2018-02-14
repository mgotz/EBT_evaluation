# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 Malte Gotz

Main GUI class of the EBT evaluation program

Program to evaluate EBT-films
A scannend image can be loaded and an area of interest selected
From that area a dose distrubtion can be calculated using a calibration file
and that dose distrubtion is than displayed in a seperate window

calibration location into advanced settings:
    change must trigger reload
    load adv settings before loading calibration
    load gui settings after
"""
#get ready for python 3
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)


#standard modules
import logging #logging funtionality
import numpy as np
#file manipulation and path functionality
import os
#modules for exception handeling
import sys
import traceback


try:
    if os.environ['QT_API'] == 'pyqt5':
        from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication, 
                                     QMessageBox)
        
        from PyQt5 import QtCore
        from matplotlib.backends.backend_qt5agg import (FigureCanvas)
        
    else:
        from PyQt4.QtGui import (QMainWindow, QFileDialog, QApplication, 
                                 QMessageBox)            
        from PyQt4 import QtCore
        from matplotlib.backends.backend_qt4agg import (FigureCanvas)
        
except ImportError:
    raise ImportError("dosewidget requires PyQt4 or PyQt5. " 
                      "QT_API: {!s}".format(os.environ['QT_API']))

#use relative import, this should only ever run as a module

#module with the dose calculation routines
from ..core import load_calibrations, DoseArray
#my custom toolbar and main ui
if os.environ['QT_API'] == 'pyqt5':
    from .main_ui_qt5 import Ui_MainWindow
else:
    from .main_ui_qt4 import Ui_MainWindow
from .navtoolbar import MyNavigationToolbar
#the dose display window
from .dosewidget import DoseWidget, _advSettings

#load the Qt bindings

#load matplotlib for plotting
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

#image loading functionality
from PIL import Image 

#import my gui helper functions (save, load gui data, gui logger, adv settings)
from mg import pyguitools
        
#define a list with advanced settings (editable via fromLayout)
#each list entry is a setting, with the first part as identifier and second as value
settingsList = [("selection rectangle","red"),
                ("mirror on load",False),
                ("rotate on load",False),
                ("histogramm bins",256),
                ("histogramm min",0),
                ("histogramm max",255)]


class MainGui(QMainWindow):
    """Main GUI of the EBT evaluation program
    
    Provides a logging window, loads the films and the calibration files.
    Constructs the dose view from the selected film ROI.
    """
    def __init__(self):
        """Constructor
        """

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks)
        
        #add the logging window by Andreas
        self.log_dock = pyguitools.QtDockLog(datefmt=" ",infoString=False)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.log_dock)        
        # default log level to info
        self.log_dock.ui.comboBox.setCurrentIndex(1)


        
        #initialize the advanced settings (editable via formlayout, thus the list of tuples)
        self.advSettings = pyguitools.EasyEditSettings(settingsList)
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
        self.ui.browseSaveTable.clicked.connect(self.save_table_file_dialog)
        self.ui.saveTablePath.returnPressed.connect(self.save_table_path_changed)
        self.ui.saveChannelData.clicked.connect(self.save_calib_data)
        self.ui.calcPhi0Button.clicked.connect(self.get_phi0)
        
        #read the settings file
        self.load_settings() 
        
        #init the save path
        self.saveTablePath = ""

    #redefining close event
    def closeEvent(self,event):
        """save, then close
        """
        self.save_settings()
        event.accept()
        
##############################################################################
# methods (internal functions not directly called by user interaction)
    def create_mplframe(self):
        """create a matplotlib frame with toolbar and figure on canvas
        """
        #create figure and axes objects
        self.fig = Figure()
        self.subplot = self.fig.add_subplot(111)
        #disable axis, because it will only show an image
        self.subplot.get_yaxis().set_visible(False)
        self.subplot.get_xaxis().set_visible(False)
        
        #create canvas and toolbar
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = MyNavigationToolbar(self.canvas, None)

        #add the canvas and toolbar to the gui
        self.ui.imageLayout.addWidget(self.canvas)
        self.ui.imageLayout.addWidget(self.toolbar)

        #connect the toolbar selection to matploblib as a callback
        self.canvas.mpl_connect('selection_changed',self.toolbar_selection)

    def load_settings(self):
        """load the setting of the GUI (called on startup)
        """
        #create a QSettings object to store the settings
        self.QtSettings=QtCore.QSettings("OncoRay","EBT Evaluation")
        #self.QtSettings=QtCore.QSettings("settings.ini",QtCore.QSettings.IniFormat)

        #load window settings        
        self.QtSettings.beginGroup("MainWindow")
        self.restoreGeometry(self.QtSettings.value("geometry",QtCore.QByteArray(),type=QtCore.QByteArray))
        self.restoreState(self.QtSettings.value("state",QtCore.QByteArray(),type=QtCore.QByteArray))
#        self.resize(self.QtSettings.value("windowSize",QtCore.QSize(1024,1280),
#                                            type=QtCore.QSize))
        self.QtSettings.endGroup()        

        #load values for various elements        
        self.QtSettings.beginGroup("Settings")
        pyguitools.gui_restore(self.ui,self.QtSettings)
        self.QtSettings.endGroup()

    def check_save_table_path(self, path):
        """checks if the path given is different from the already saved one
        and then checks is validity and creates a header"""

        #check if path is empty and try to get something not empty
        if path == "":
            path = QFileDialog.getSaveFileName(self,caption = 'select a file to save to',
                                               directory = self.ui.saveTablePath.text(),
                                               filter="Text files (*.txt);;All files (*)",
                                               options = QFileDialog.DontConfirmOverwrite)
            
            #in pyqt5 a tuple is returned, unpack it
            if os.environ['QT_API'] == 'pyqt5':
                path, _ = path
            
            if path == "":
                return ""
            else:
                self.ui.saveTablePath.setText(path)
        
        #do nothing if path already checked
        if self.saveTablePath == path:
            return path
                
        #if it already exists ask to overwrite or append
        if os.path.isfile(path):
            title = "path already exists"
            text = path+"already exists, overwrite or append?"
            overwriteAnswer = QMessageBox.question(self,title,text,
                                                   "append","overwrite","abort")
            if overwriteAnswer == 0:
                return path
            elif overwriteAnswer == 2:
                return ""
        #should not be a dir
        elif os.path.isdir(path):
            logging.error("specified path is a directory")
            return ""
        
        #in all other cases, open it for writing and write a header to it
        headerString = ("film no\t" "filename\t" "x0\ty0\tx1\ty1\t"
                        "number of pixels\t" 
                        "R_avg\tR_std\t" "G_avg\tG_std\t" "B_avg\tB_std\n")
        with open(path,"w") as saveTableFile:
            saveTableFile.write(headerString)
            
        return path
        
    def save_settings(self):
        """save the settings of the GUI (called on exit)
        """
        self.QtSettings.beginGroup("MainWindow")
        self.QtSettings.setValue("geometry",self.saveGeometry())
        self.QtSettings.setValue("state",self.saveState())
        self.QtSettings.endGroup()
        
        #save element content
        self.QtSettings.beginGroup("Settings")
        pyguitools.gui_save(self.ui,self.QtSettings)
        self.QtSettings.endGroup()
        
    def load_calibrations(self):
        """Load the calibration files (for dose calculation)
        """
        try:
            self.calibrations = load_calibrations(os.path.join(os.path.dirname(__file__),
                                                               "..",
                                                               "calibrations"))
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
# slots (user interaction functions, all connected to a signal emitted by some
# GUI element)
    def area_stats(self):
        """calculate and log simple stats of the selected area (e.g, average)
        """
        x0 = self.ui.x0.value()
        x1 = self.ui.x1.value()
        y0 = self.ui.y0.value()
        y1 = self.ui.y1.value()
        
        channel = self.ui.channel_selection.itemData(self.ui.channel_selection.currentIndex())

        avg = np.average(self.npImg[y0:y1,x0:x1,channel])
        std = np.std(self.npImg[y0:y1,x0:x1,channel])
        minimum = np.min(self.npImg[y0:y1,x0:x1,channel])
        maximum = np.max(self.npImg[y0:y1,x0:x1,channel])
        
        n = (max(x1,x0)-min(x1,x0))*(max(y1,y0)-min(y1,y0))

            
        logging.info("### Statistics for area x: {:d} - {:d}; y: {:d} - {:d} ###".format(x0,x1,y0,y1))
        logging.info("channel: {!s}".format(self.ui.channel_selection.currentText()))
        logging.info("average: {:.3f} +- {:.3f}".format(avg,std/np.sqrt(n)))
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
    
    def get_phi0(self):
        """uses the stats from currently selected area to fill the phi0 fields
        """
        x0 = self.ui.x0.value()
        x1 = self.ui.x1.value()
        y0 = self.ui.y0.value()
        y1 = self.ui.y1.value()        
        
        channels = [self.ui.channel_selection.itemData(i) for i in range(self.ui.channel_selection.count())]
        
        for ch, field in zip(channels,[self.ui.phi0Ch1,self.ui.phi0Ch2,self.ui.phi0Ch3]):
            avg = np.average(self.npImg[y0:y1,x0:x1,ch])
            field.setValue(avg)
        
    
    def histogram(self):
        """show a histgram of the selected channel
        """
        channel = self.ui.channel_selection.itemData(self.ui.channel_selection.currentIndex())

        #create a window, the reference must be stored, because the window
        #gets destroyed when its reference is garbage collected
        #make plotWindow a list and append to that if multiple windows should be possible
        title = "histogram of {:s} channel".format(self.ui.channel_selection.currentText())
        self.plotWindow = pyguitools.SimplePlotWindow(name = title)
        self.plotWindow.ax1.hist(self.npImg[self.ui.y0.value():self.ui.y1.value(),
                                            self.ui.x0.value():self.ui.x1.value(), 
                                            channel].flatten(),
                                 bins=self.settings["histogramm bins"],
                                 range=(self.settings["histogramm min"],self.settings["histogramm max"]))
        self.plotWindow.ax1.set_xlim(self.settings["histogramm min"],self.settings["histogramm max"]) 
        self.plotWindow.show()


    def image_file_dialog(self):
        """open dialog to select a scan (browsing)
        """
        extensionFilter=("TIFF files (*.tiff *.TIFF *.tif *.TIF)"
                         "Image files (*.tiff *.TIFF *.tif *.jpg *.jpeg *.png *.bmp *.gif);;"
                         "All files (*)")
        
        filePath =QFileDialog.getOpenFileName(self,
                                              caption = 'select a scanned image',
                                              directory = self.ui.imagePath.text(),
                                              filter = extensionFilter)
        #in pyqt5 a tuple is returned, unpack it
        if os.environ['QT_API'] == 'pyqt5':
            filePath, _ = filePath
            
        if filePath != '':
            self.ui.imagePath.setText(filePath)
            self.image_path_changed()
        else:
            logging.info('file selection canceled')
        
    def image_path_changed(self):
        """trys to load a new scan
        """
        #load the image, if no path given open dialog
        if self.ui.imagePath.text() == "":
            self.image_file_dialog()
        
        #catch wrong path and permission errors
        try:
            img = Image.open(str(self.ui.imagePath.text()))
        except (IOError, OSError) as e:
            logging.error("failed to open file: "+str(e))
            return ()

        #check the format of the loaded image and adjust the input field accordingly
        logging.debug("image mode: "+img.mode)
        self.ui.channel_selection.clear()
        
        if img.mode == "RGB":
            self.ui.channel_selection.addItem("red",0)
            self.ui.channel_selection.addItem("green",1)
            self.ui.channel_selection.addItem("blue",2)
            
            #set the phi0 input
            for field in [self.ui.phi0Ch1,self.ui.phi0Ch2,self.ui.phi0Ch3]:
                field.setMaximum(255)
                field.setMinimum(0)
                field.setEnabled(True)
            self.ui.phi0LabelCh1.setText("red:")
            self.ui.phi0LabelCh2.setText("green:")
            self.ui.phi0LabelCh3.setText("blue:")
        elif img.mode == "L" or img.mode == "I":
            #none because there is no third dimension in greyscale
            self.ui.channel_selection.addItem("grey",None)
            modeMax = {"L":255,"I":2**31}
            modeMin = {"L":0,"I":-2**31}
        
            
            #set the phi0 input
            self.ui.phi0Ch1.setEnabled(True)
            self.ui.phi0Ch1.setMaximum(modeMax[img.mode])
            self.ui.phi0Ch1.setMinimum(modeMin[img.mode])
            self.ui.phi0Ch2.setDisabled(True)
            self.ui.phi0Ch3.setDisabled(True)
            
            self.ui.phi0LabelCh1.setText("phi0:")
        else:
            logging.warning("unsupported image mode "+img.mode+
                            " (check pillow docs for details) "+
                            "expected RGB or greyscale image, proceed with caution")

        #create np array from image and rotate if needed
        if self.settings["rotate on load"]:
            self.npImg = np.rot90(np.array(img))
        else:
            self.npImg = np.array(img)
        
        #mirror the image if desired
        if self.settings["mirror on load"]:
            self.npImg = np.fliplr(self.npImg)

             
        

        
        #check for dpi info
        try:
            dpi = img.info['dpi']
            
            #try string conversion and tuple first and then deal with type of number
            if type(dpi) == str:
                try:
                    dpi = float(dpi)
                except ValueError:
                    logging.warning("Can not parse dpi info: "+dpi)
                    dpi = 0
            elif type(dpi) == tuple:
                if len(dpi) == 1:
                    dpi = dpi[0]
                elif len(dpi) == 2:
                    if dpi[0] == dpi[1]:
                        dpi = dpi[0]
                    else:
                        logging.warning("different DPI for the two dimensions found " +
                                        repr(dpi)+ " THIS IS NOT SUPPORTED")
                        dpi = 0
                else:
                    logging.warning("dpi has more than 2 dimensions" +
                                    repr(dpi)+ " DONT KNOW WHAT TO DO")
                    dpi=0
            
            try:
                dpi = float(dpi)
                if not dpi.is_integer():
                    logging.warning("non integer DPI of {:.4f} is not supported".format(dpi))
            except TypeError: #unkown type of dpi
                logging.warning("Can not parse dpi info: "+repr(dpi))
                dpi = 0
        except KeyError:
            logging.debug("no dpi info")
            dpi=0

        logging.debug("loaded image of dimensions: "+str(self.npImg.shape)+
                      " and type: "+str(self.npImg.dtype)+
                      ", with DPI: "+str(dpi))
            
        if dpi > 0:
            self.ui.DPI.setValue(int(dpi))
              
        #adjust UI elements to image properties
        self.ui.x0.setMaximum(self.npImg.shape[1])
        self.ui.x0.setValue(0)
        self.ui.y0.setMaximum(self.npImg.shape[0])
        self.ui.y0.setValue(0)
        self.ui.x1.setMaximum(self.npImg.shape[1])
        self.ui.x1.setValue(self.npImg.shape[1])
        self.ui.y1.setMaximum(self.npImg.shape[0])
        self.ui.y1.setValue(self.npImg.shape[0])

        #plot the image
        self.subplot.imshow(self.npImg,cmap="gray")
        self.canvas.draw()

    def save_calib_data(self):
        """save the average of each channel in the selection area to a file"""
        x0 = self.ui.x0.value()
        x1 = self.ui.x1.value()
        y0 = self.ui.y0.value()
        y1 = self.ui.y1.value()
        
        directory, fileName = os.path.split(self.ui.imagePath.text())
        
        saveStr = self.ui.filmNumber.text()
        saveStr += "\t"+fileName
        
        #save coordinates
        saveStr += "\t{:d}\t{:d}\t{:d}\t{:d}".format(x0,y0,x1,y1)
        #save area in pixels
        nofpixels = (max(x0,x1)-min(x0,x1))*(max(y0,y1)-min(y0,y1))
        saveStr += "\t{:d}".format(nofpixels)        
        
        #save the channel data
        for channel in [0,1,2]:
            avg = np.average(self.npImg[y0:y1,x0:x1,channel])
            std = np.std(self.npImg[y0:y1,x0:x1,channel])
            saveStr += "\t{:.3f}".format(avg)
            saveStr += "\t{:.3f}".format(std)
        
        saveStr += "\n"        
        
        self.saveTablePath = self.check_save_table_path(self.ui.saveTablePath.text())
        
        if self.saveTablePath == "":
            logging.warning("nothing written to file")
        else:
            with open(self.saveTablePath,"a") as saveTable:
                saveTable.write(saveStr)
                logging.info(("info for "+self.ui.filmNumber.text()+" written to file"))

    def save_table_file_dialog(self):
        filePath =QFileDialog.getSaveFileName(self,
                                              caption = 'select a file to save to',
                                              directory = self.ui.saveTablePath.text(),
                                              options = QFileDialog.DontConfirmOverwrite)
        
        #in pyqt5 a tuple is returned, unpack it
        if os.environ['QT_API'] == 'pyqt5':
            filePath, _ = filePath
            
        if filePath != '':
            self.ui.saveTablePath.setText(filePath)
            self.save_table_path_changed()
        else:
            logging.info('file selection canceled')

    def save_table_path_changed(self):
        self.saveTablePath = ""
        self.saveTablePath = self.check_save_table_path(self.ui.saveTablePath.text())

    def selection_changed(self):
        #the point here is to redraw the marker as efficiently as possible, i.e.
        #change as little of the existing plot as possible
        
        #try to update the old marker
        try:
            self.selectionMarker.set_bounds(self.ui.x0.value(),self.ui.y0.value(),
                                            self.ui.x1.value()-self.ui.x0.value(),
                                            self.ui.y1.value()-self.ui.y0.value())
            self.subplot.draw_artist(self.selectionMarker)
        except AttributeError:
        #marker does not exist, create a new rectangle marker and draw it
            rect = Rectangle((self.ui.x0.value(),self.ui.y0.value()),
                             self.ui.x1.value()-self.ui.x0.value(),
                             self.ui.y1.value()-self.ui.y0.value(),
                             fill=False,color=self.settings["selection rectangle"],
                             linewidth=2.0)
            self.selectionMarker = self.subplot.add_artist(rect)

        self.canvas.draw()
        self.canvas.flush_events()        

    def show_dose(self):
        logging.debug("calculating dose")
        idx = self.ui.calibration_selection.currentIndex()
        try:
            #get the phi0 value from all currently allowed fields
            phi0 = []
            for inputField in [self.ui.phi0Ch1, self.ui.phi0Ch2, self.ui.phi0Ch3]:
                if inputField.isEnabled():
                    phi0.append(inputField.value())
            
            #undo the  dimension expansion for grey scale images
            if self.ui.channel_selection.count() == 1:
                doseDistribution = DoseArray(self.ui.DPI.value(),
                                             self.ui.calibration_selection.itemData(idx),
                                             self.npImg[self.ui.y0.value():self.ui.y1.value(),
                                                        self.ui.x0.value():self.ui.x1.value()],
                                             phi0)
            else:
                doseDistribution = DoseArray(self.ui.DPI.value(),
                                             self.ui.calibration_selection.itemData(idx),
                                             self.npImg[self.ui.y0.value():self.ui.y1.value(),
                                                        self.ui.x0.value():self.ui.x1.value(),
                                                        :],
                                             phi0)
            self.tabCounter += 1  
            index = self.ui.tabWidget.addTab(DoseWidget(doseDistribution,settings=self.doseViewSettings.get_settings()),
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
    app = QApplication(sys.argv)
    gui = MainGui()
    gui.show()
    sys.exit(app.exec_())
     