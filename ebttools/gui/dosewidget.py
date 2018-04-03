# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 Malte Gotz

This contains mainly the DoseWidget class to display a dose in a QWidget
and acess its methods

ToDo:
    save advanced settings?

ideas:
    click and drag for selection of area
    or click and drag moves center for new input style, and area selection for old
"""
#get ready for python 3
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

from collections import OrderedDict
import logging
import numpy as np
import os
import traceback

#enable compatibility to both pyqt4 and pyqt5 and load the proper modules
try:
    if os.environ['QT_API'] == 'pyqt5':
        from PyQt5.QtWidgets import (QWidget, QFileDialog, qApp)
        
        from PyQt5 import QtCore
        from matplotlib.backends.backend_qt5agg import FigureCanvas
        
    else:
        from PyQt4.QtGui import (QWidget, QFileDialog, qApp)            
        from PyQt4 import QtCore
        from matplotlib.backends.backend_qt4agg import FigureCanvas
   
except ImportError:
    raise ImportError("dosewidget requires PyQt4 or PyQt5. " 
                      "QT_API: {!s}".format(os.environ['QT_API']))

#load qt design UI, use relative import if run as a module
if os.environ["QT_API"] == "pyqt5":     
    from .dosewidget_ui_qt5 import Ui_DoseWidget 
else:
    from .dosewidget_ui_qt4 import Ui_DoseWidget 
from .navtoolbar import MyNavigationToolbar

from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.patches import Ellipse, Rectangle
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
from scipy.optimize import curve_fit

# simple edit of additional settings and gui helper functions
from mg.pyguitools import EasyEditSettings, SimplePlotWindow, gui_save, gui_restore
#2D gauss fitting
from mg.dataprocessing import (gauss2D, fit_2D_gauss, cross, FitError)
#the DoseArray from ebttools provides the core of the backend    
from ebttools.core import DoseArray

class ScalarFormatterWithUnit(ticker.ScalarFormatter):
    """extension of the ScalarFormatter appending a unit to each tick label"""
    def __init__(self, unit="Gy", useOffset=None, useMathText=None, useLocale=None):
        self.unit=unit
        super(ScalarFormatterWithUnit,self).__init__(useOffset, useMathText, useLocale)
    
    def __call__(self, x, pos=None):
        """
        Return the format for tick value `x` at position `pos`.
        """
        if len(self.locs) == 0:
            return ''
        else:
            s = self.pprint_val(x)+" "+self.unit
            return self.fix_minus(s)


def gauss(x, A, x0, sigma, offset):
    return A*np.exp(-np.square(x-x0)/(2*sigma**2))+offset

#define possibilities for color maps and filter for their availability
#on the current installation
import matplotlib.cm as cm
  
possibleCmapChoices = ["inferno","viridis","hot","gnuplot","spectral","jet",
                   "rainbow","gray","seismic"]

colorMapChoices = []
for cmap in possibleCmapChoices:
    try:
        cm.get_cmap(cmap)
        colorMapChoices.append(cmap)
    except ValueError:
        pass

_advSettings = EasyEditSettings([("area stat linecolor","red"),
                                 ("area stat linewidth",2.0),
                                 ("isodose color","yellow"),
                                 ("isodose linewidth",2.0),
                                 ("isodose fontsize",14),
                                 ("label axes",True), 
                                 ("color map",[0]+colorMapChoices),
                                 ("show grid",False),
                                 ("profile interpolation",
                                  [0,"nearest","linear","spline"])])

_defaultSettings = _advSettings.get_settings()


class DoseWidget(QWidget):
    """Class to display a dose distribution
    
    The DoseArray provided at construction is displayed in a matplotlib plot
    embedded in a QWidget. The widget may be inserted into a PyQt UI as any
    other widget would.
    In addition it provides GUI interfaces to calculate and fit aspects of the
    dose distribution by calling the methods of the DoseArray.
    """
    def __init__(self, doseDistribution, settings=_defaultSettings, 
                 calculationSettings = None, loadUI = False):
        """Constructor
        
        Parameters
        ---------------
        doseDistribtuion : DoseArray
            A DoseArray object to be displayed here
        settings : dict of the settings, optional
            _defaultSettings is a dict of the settings used here, constructed
            using the EasyEditSettings. See the _advSettings as to what keys the
            dict should contain
        calculationData : dict, optional
            should contain the settings used to calculate the doseDistribution
            from a film. It will be saved using the dict_keys as headers
        loadUI: bool, optional
            load saved ui settings
        """

        QWidget.__init__(self)
        
        #save local copy of dose                
        self.doseDistribution = doseDistribution
        self.calculationSettings = calculationSettings

        # Set up the user interface from Designer.
        self.ui =  Ui_DoseWidget()
        self.ui.setupUi(self)

        self.settings = settings               
        
        self.set_ui_limits()
        
        
        
        # setup the selection of evaluation functions:
        # key of first level dict is the combo box text (order dict so that they appear in defined order in combobox)
        # each entry should be another dictionary with the elements eval pointing
        # to the evaluation function, marker which is a function returning an appropriate
        # marker artist and tip which is a tooltip string
        functions = OrderedDict([("Rectangle",{"eval":self.rectangle,
                                              "marker":self.rectangle_marker,
                                              "tip":"rectangular selection area"}),
                                 ("Ellipse",{"eval":self.ellipse,
                                            "marker":self.ellipse_marker,
                                            "tip":"elliptical selection area"}),
                                 ("Profile",{"eval":self.profile,
                                             "marker":self.line_marker,
                                             "tip":"get a profile"}),
                                 ("Profile: Parabola Fit",{"eval":self.profile_with_parabola,
                                                           "marker":self.line_marker,
                                                           "tip":"get a profile and fit a parabola"}),
                                 ("Profile: Gauss Fit",{"eval":self.profile_with_gauss,
                                                        "marker":self.line_marker,
                                                        "tip":"get a profile and fit a gaussian"}),
                                 ("2D Gauss Fit",{"eval":self.fit_2D_gauss,
                                                  "marker":self.axis_parallel_rectangle_marker,
                                                  "tip":"fit the entire distribution with a 2D Gaussian"})])
        
        #set up combobox with functions dictionary
        for key in functions:
            self.ui.evalFunction.addItem(key,functions[key])
            idx = self.ui.evalFunction.count()-1
            self.ui.evalFunction.setItemData(idx,functions[key]["tip"],
                                             QtCore.Qt.ToolTipRole)
        
        #load UI before connecting slots to avoid needless on change firing
        if loadUI:
            self.load_ui_values()
        #matplotlib frame setup
        self.create_mplframe()
        self.make_dose_plot()

        #connect slots
        #value changes
        self.ui.xCenter.valueChanged.connect(self.ROI_value_change)
        self.ui.yCenter.valueChanged.connect(self.ROI_value_change)
        self.ui.width.valueChanged.connect(self.ROI_value_change)
        self.ui.height.valueChanged.connect(self.ROI_value_change)
        self.ui.angle.valueChanged.connect(self.ROI_value_change)
        self.ui.evalFunction.currentIndexChanged.connect(self.ROI_value_change)
        self.ui.x0.valueChanged.connect(self.ROI_value_change)
        self.ui.x1.valueChanged.connect(self.ROI_value_change)
        self.ui.y0.valueChanged.connect(self.ROI_value_change)
        self.ui.y1.valueChanged.connect(self.ROI_value_change)

        qApp.focusChanged.connect(self.focus_change)
        
        #buttons
        self.ui.alternateSpecToggle.stateChanged.connect(self.toggle_ROI_spec)
        self.ui.refreshButton.clicked.connect(self.refresh)
        self.ui.bestLimits.clicked.connect(self.set_optimal_scale)
        self.ui.calculateButton.clicked.connect(self.calculate)        
        self.ui.exportTxtButton.clicked.connect(self.save_as_txt)
        self.ui.exportNpButton.clicked.connect(self.save_as_numpy)
        self.ui.clearFitButton.clicked.connect(self.clear_2D_fit)
        self.ui.showIsoLines.stateChanged.connect(self.isodose_change)
        self.ui.browseSaveTable.clicked.connect(self.save_file_dialog)
        self.ui.saveCalculationData.clicked.connect(self.save_calc_to_file)
        
        #call some slots explicitly to properly apply loaded values
        if loadUI:
            self.toggle_ROI_spec()
            self.isodose_change()
            self.update_dose_plot()
            self.update_marker()
        
        #initialize some variables
        self.savePath = ""
       
       
##############################################################################
# setup methods for the window and update settings
    def create_mplframe(self):
        """creates the matplotlib canvas and figure with colorbar
        """
        ### create matplotlib figure and canvas as central widget
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        divider = make_axes_locatable(self.ax1)
        self.clbAxes = divider.append_axes("right", size="5%", pad=0.6)

        self.canvas = FigureCanvas(self.fig)
        self.toolbar = MyNavigationToolbar(self.canvas, None)
        self.toolbar.centeredSelection = True

        self.ui.imageLayout.addWidget(self.canvas)
        self.ui.imageLayout.addWidget(self.toolbar)
        
        #connect the toolbar selection to matploblib as a callback
        self.canvas.mpl_connect('selection_changed',self.toolbar_selection)

    def set_ui_limits(self):
        """set the limits of the various UI elements depending on the dose distribution
        """

        #set dose limits
        doseMax = np.max(self.doseDistribution)
        self.ui.doseMin.setMaximum(doseMax*10.)
        self.ui.doseMax.setMaximum(doseMax*10.)
        self.ui.nominalDose.setMaximum(doseMax*10.)
        self.ui.doseMin.setMinimum(0.0)
        self.ui.doseMax.setMinimum(0.0)
        self.ui.nominalDose.setMinimum(0.0)
        
        
        self.set_optimal_scale()        
        
        #set ROI limits
        xMax = self.doseDistribution.shape[1]/self.doseDistribution.DPC
        yMax = self.doseDistribution.shape[0]/self.doseDistribution.DPC
        
        self.ui.xCenter.setMaximum(xMax)
        self.ui.xCenter.setMinimum(0.0)
        self.ui.yCenter.setMaximum(yMax)
        self.ui.yCenter.setMinimum(0.0)
        self.ui.height.setMinimum(0.0)
        self.ui.height.setMaximum(yMax)
        self.ui.width.setMaximum(xMax)
        self.ui.width.setMinimum(0.0)
        
        self.ui.x0.setMinimum(0.0)
        self.ui.x1.setMinimum(0.0)
        self.ui.y0.setMinimum(0.0)
        self.ui.y1.setMinimum(0.0)
        
        self.ui.x0.setMaximum(xMax)
        self.ui.x1.setMaximum(xMax)
        self.ui.y0.setMaximum(yMax)
        self.ui.y1.setMaximum(yMax)

    def set_settings(self, settings):
        self.settings = settings

    def get_settings(self):
        return self.settings

    def load_ui_values(self):
        """load values of previously stored session"""
        #create a QSettings object to store the settings
        QtSettings=QtCore.QSettings("OncoRay","EBT Evaluation")
        
        #load values for various elements        
        QtSettings.beginGroup("DoseWidget")
        gui_restore(self.ui,QtSettings)
        QtSettings.endGroup()
        
    def save_ui_values(self):
        """save the settings of the GUI
        """
        #create a QSettings object to store the settings
        QtSettings=QtCore.QSettings("OncoRay","EBT Evaluation")
        
        #save element content
        QtSettings.beginGroup("DoseWidget")
        gui_save(self.ui,QtSettings)
        QtSettings.endGroup()        
##############################################################################
# UI update methods
    def get_iso_list(self):
        text = self.ui.isoListField.toPlainText()
        textList = text.split("\n")
        isoLines = []
        for line in textList:
            try:
                value = float(line)
                if value < 0:
                    raise ValueError
                isoLines.append(value)
            except ValueError:
                logging.error("{!s} is not a senisble percentage".format(line))
        
        isoLines.sort()            
        return np.array(isoLines)
                    
    def match_ui_inputs(self,newIsMaster=True):
        """caculate the old style ROI specification from the new or vice versa
           depending on who is master
        """
        idx = self.ui.evalFunction.currentIndex()
        currentMarkerFunction = self.ui.evalFunction.itemData(idx)["marker"]
        if newIsMaster:
            if currentMarkerFunction == self.line_marker:
                phi_rad = self.ui.angle.value()*np.pi/180.
                x0 = self.ui.xCenter.value() - np.cos(phi_rad)*self.ui.width.value()/2.0
                y0 = self.ui.yCenter.value() + np.sin(phi_rad)*self.ui.width.value()/2.0
                x1 = self.ui.xCenter.value() + np.cos(phi_rad)*self.ui.width.value()/2.0
                y1 = self.ui.yCenter.value() - np.sin(phi_rad)*self.ui.width.value()/2.0
            else:
                x0 = self.ui.xCenter.value()-self.ui.width.value()/2.0
                x1 = self.ui.xCenter.value()+self.ui.width.value()/2.0
                y0 = self.ui.yCenter.value()-self.ui.height.value()/2.0
                y1 = self.ui.yCenter.value()+self.ui.height.value()/2.0
            
            #update but block triggering of further updates
            self.ui.x0.blockSignals(True)
            self.ui.x0.setValue(x0)
            self.ui.x0.blockSignals(False)
            self.ui.x1.blockSignals(True)
            self.ui.x1.setValue(x1)
            self.ui.x1.blockSignals(False)
            self.ui.y0.blockSignals(True)
            self.ui.y0.setValue(y0)
            self.ui.y0.blockSignals(False)
            self.ui.y1.blockSignals(True)
            self.ui.y1.setValue(y1)
            self.ui.y1.blockSignals(False)
            
        else:
            xCenter = (self.ui.x0.value()+self.ui.x1.value())/2.0
            yCenter = (self.ui.y0.value()+self.ui.y1.value())/2.0
            if currentMarkerFunction == self.line_marker:
                width = np.hypot(self.ui.x0.value()-self.ui.x1.value(),
                                 self.ui.y0.value()-self.ui.y1.value())
                height = 0.0
                try:
                    angle = np.arctan((self.ui.y0.value()-self.ui.y1.value())/
                                      (self.ui.x1.value()-self.ui.x0.value()))*180./np.pi
                except ZeroDivisionError:
                    angle = 90.0
            else:
                width = np.abs(self.ui.x0.value()-self.ui.x1.value())
                height = np.abs(self.ui.y0.value()-self.ui.y1.value())
                angle = 0.0
            
            #update but block triggering of further updates
            elements = [self.ui.xCenter,self.ui.yCenter,self.ui.width,
                        self.ui.height,self.ui.angle]
            for element in elements:
                element.blockSignals(True)

            self.ui.xCenter.setValue(xCenter)
            self.ui.yCenter.setValue(yCenter)
            self.ui.width.setValue(width)
            self.ui.height.setValue(height)
            self.ui.angle.setValue(angle)
            
            for element in elements:
                element.blockSignals(False)

    def make_dose_plot(self):
        """draw the dose distribution in the plot
        """
        shape = self.doseDistribution.shape
        yMax = shape[0]/self.doseDistribution.DPC
        xMax = shape[1]/self.doseDistribution.DPC
        #plot the dose distrubtion
        self.dosePlot = self.ax1.imshow(self.doseDistribution,
                                        interpolation="nearest",
                                        extent=[0,xMax,yMax,0],
                                        zorder=-1)#image should be lowest zorder
                    
        self.clb = self.fig.colorbar(self.dosePlot, cax = self.clbAxes,
                                     orientation="vertical", 
                                     format=ScalarFormatterWithUnit(unit=self.doseDistribution.unit))
                                     

        self.ax1.minorticks_on()
        for axis in ['top','bottom','left','right']:
            self.ax1.spines[axis].set_linewidth(2.0)
            
        self.ax1.tick_params(which='major',direction="out",width=2.0,length=6,
                                 bottom=True,top=True,left=True,right=True,
                                 labelbottom=True,labeltop=True,labelleft=True,labelright=True)        
        self.ax1.tick_params(which='minor',direction="out",width=1.5,length=4,
                                 bottom=True,top=True,left=True,right=True)
        
        self.update_dose_plot()
            
            
    def plot_isodose(self):
        percentages = self.get_iso_list()
        if len(percentages) == 0:
            return None
        shape = self.doseDistribution.shape
        yMax = shape[0]/self.doseDistribution.DPC
        xMax = shape[1]/self.doseDistribution.DPC
        
        levels = percentages*self.ui.nominalDose.value()/100.
        cPlot = self.ax1.contour(self.doseDistribution,
                                 levels = levels,
                                 colors=self.settings["isodose color"],
                                 linewidths=self.settings["isodose linewidth"],
                                 origin='image',
                                 extent=[0,xMax,yMax,0],
                                 zorder=0)#set relatively low zorder, so they are just above the image
        labels = {}
        for level, percentage in zip(cPlot.levels, percentages):
            labels[level] = "{:.0f}".format(percentage)
            
        cLabels = self.ax1.clabel(cPlot,fmt=labels, 
                                  fontsize= self.settings["isodose fontsize"])
        return (cPlot, cLabels)
                    
    
    def update_dose_plot(self):
        """set limits and colormap of the dose plot
        """

        #set limits of the color map                    
        self.dosePlot.set_clim(self.ui.doseMin.value(),
                               self.ui.doseMax.value())
        #set the colormap and add it to the plot
        self.dosePlot.set_cmap(self.settings["color map"])

        self.clb.update_normal(self.dosePlot)

        #isodoses
        #remove old isodoses if there are any
        if hasattr(self,"contourPlot"):
            for coll, label in zip(self.contourPlot[0].collections, self.contourPlot[1]):
                coll.remove()
                label.remove()
            del self.contourPlot
        if self.ui.showIsoLines.isChecked():
            cPlot = self.plot_isodose()
            if cPlot is not None:
                self.contourPlot = cPlot
        
        #labels and grid
        if self.settings["label axes"]:
            self.ax1.set_xlabel("x-position in cm")
            self.ax1.set_ylabel("y-position in cm")
        else:
            self.ax1.set_xlabel("")
            self.ax1.set_ylabel("")

        self.ax1.grid(self.settings["show grid"])

    def update_marker(self):
        #try removing old marker, attribute error is raised when the variable is
        #not set and value error when it has already been removed
        
        if hasattr(self,"area_marker"):
            try:
                self.area_marker.remove()
            except (ValueError) as e:
                logging.debug("ignored "+e.message)
        
        #get the appropriate new marker artist
        idx = self.ui.evalFunction.currentIndex()
        artist = self.ui.evalFunction.itemData(idx)["marker"]()
        #add new marker to plot
        if artist != None:
            self.area_marker = self.ax1.add_artist(artist)
        self.canvas.draw()

##############################################################################
# markers of the ROI. Each evaluation methods specificies one of these to mark
# the region of interest and they are then called by the update_marker method
# whenever the input changes

    def axis_parallel_rectangle_marker(self):
        """rectangle marker that forces axis parallelity
        """
        if self.ui.angle.value() != 0.0:
            logging.warning("this ROI is axis parallel only and does not support rotation")
            #if signals are not blocked and the angle is forced to zero
            #going back to some non zero angle causes the marker gets somehow duplicated
            self.ui.angle.blockSignals(True)
            self.ui.angle.setValue(0.0)
            self.ui.angle.blockSignals(False)
        
        return self.rectangle_marker()
  
    def ellipse_marker(self):
        """returns a matplotlib artist for an ellipse
        """
        #create a marker
        artist = Ellipse((self.ui.xCenter.value(),self.ui.yCenter.value()),
                         self.ui.width.value(),self.ui.height.value(),
                         angle=-self.ui.angle.value(),
                         color=self.settings["area stat linecolor"],
                         linewidth=self.settings["area stat linewidth"],
                         fill=False)
        return artist
    
    def line_marker(self):
        """returns a matplotlib artist for a line
        """

        #use the convieniently already calculated old style coordinates for the line
        artist = Line2D([self.ui.x0.value(),self.ui.x1.value()],
                        [self.ui.y0.value(),self.ui.y1.value()],
                        color=self.settings["area stat linecolor"],
                        linewidth=self.settings["area stat linewidth"])
        return artist

    def no_marker(self):
        return None     
    
    def rectangle_marker(self):
        """return a matplotlib artist for a rectangle
        """
        #calculate the lower left corner for the given center, width, height and angle
        phi_rad = self.ui.angle.value()*np.pi/180.
        
        lowerLeftY = (self.ui.yCenter.value() - 
                      (self.ui.height.value()/2.0*np.cos(phi_rad) - 
                       self.ui.width.value()/2.0*np.sin(phi_rad)))
                      
        lowerLeftX = (self.ui.xCenter.value() - 
                      (self.ui.width.value()/2.0*np.cos(phi_rad) + 
                       self.ui.height.value()/2.0*np.sin(phi_rad)))
        
        #create a rectangle artist	               
        artist = Rectangle((lowerLeftX,lowerLeftY),
                           self.ui.width.value(),
                           self.ui.height.value(),
                           angle=-self.ui.angle.value(),
                           color=self.settings["area stat linecolor"],
                           linewidth=self.settings["area stat linewidth"],
                           fill=False)
        return artist

##############################################################################
# evaluation methods which are called upon when clicking calcualte
        
    def rectangle(self):
        """calculate and print the stats for a rectangle area
        """
        stats = self.doseDistribution.rectangle_stats(self.ui.xCenter.value(),
                                                      self.ui.yCenter.value(),
                                                      self.ui.width.value()/2.0, 
                                                      self.ui.height.value()/2.0,
                                                      self.ui.angle.value())
        logging.debug(stats)                                              
        logging.info("### Statistics for rectangle ###")
        logging.info("sum: {:.4e} Gy*cm^2".format(stats[0]/self.doseDistribution.DPC**2))
        logging.info("average: {:.4e} Gy".format(stats[1]))
        logging.info("standard deviation: {:.4e} Gy".format(stats[2]))
        logging.info("minimum: {:.4e} Gy".format(stats[3]))        
        logging.info("maximum: {:.4e} Gy".format(stats[4]))
        logging.info("--------------------------------------------------------------")
        return stats
        

    def ellipse(self):
        """calculate and print the stats for an ellipse area
        """

        #get the stats
        stats = self.doseDistribution.ellipse_stats(self.ui.xCenter.value(),
                                                    self.ui.yCenter.value(),
                                                    self.ui.width.value()/2.0, 
                                                    self.ui.height.value()/2.0,
                                                    self.ui.angle.value())
                                            
        logging.info("### Statistics for ellipse ###")
        logging.info("sum: {:.4e} Gy*cm^2".format(stats[0]/self.doseDistribution.DPC**2))
        logging.info("average: {:.4e} Gy".format(stats[1]))
        logging.info("standard deviation: {:.4e} Gy".format(stats[2]))
        logging.info("minimum: {:.4e} Gy".format(stats[3]))        
        logging.info("maximum: {:.4e} Gy".format(stats[4]))
        logging.info("--------------------------------------------------------------")
        
        return stats
    
    def profile(self):
        """get a profile of the image
        """
        #construct the window
        windowName = "profile ({:.3e},{:.3e}) - ({:.3e},{:.3e})".format(self.ui.x0.value(),
                                                                        self.ui.y0.value(),
                                                                        self.ui.x1.value(),
                                                                        self.ui.y1.value())
        self.profileWindow = SimplePlotWindow(name=windowName)
        
        #get the x and y profile data and plot it
        y = self.doseDistribution.profile(self.ui.x0.value(),
                                          self.ui.y0.value(),
                                          self.ui.x1.value(),
                                          self.ui.y1.value(),
                                          interpolation=self.settings["profile interpolation"])
        x = np.linspace(0,self.ui.width.value(),len(y))
        self.profileWindow.ax1.plot(x,y,label="profile")
        
        #show the window
        self.profileWindow.show()
    
    def profile_with_parabola(self):
        """get a profile of the image and fit it with a 2nd order polynomial
        """
        #construct the window
        windowName = "profile ({:.3e},{:.3e}) - ({:.3e},{:.3e})".format(self.ui.x0.value(),
                                                                        self.ui.y0.value(),
                                                                        self.ui.x1.value(),
                                                                        self.ui.y1.value())
        self.profileWindow = SimplePlotWindow(name=windowName)
        
        #get the x and y profile data and plot it
        y = self.doseDistribution.profile(self.ui.x0.value(),
                                          self.ui.y0.value(),
                                          self.ui.x1.value(),
                                          self.ui.y1.value(),
                                          interpolation=self.settings["profile interpolation"])
        x = np.linspace(0,self.ui.width.value(),len(y))
        self.profileWindow.ax1.plot(x,y,label="profile")
        
        #fit, construct and plot function
        p = np.polyfit(x,y,2)
        func = np.poly1d(p)
        fittedY = func(x)

        self.profileWindow.ax1.plot(x,fittedY,label="fit")

        #log the results
        logging.info("### Fit results ###")
        logging.info("y = {:.4e}*x^2 + {:.4e}*x + {:.4e}".format(*p))
        self.log_fit_points_of_interest(x,y,fittedY)
        logging.info("--------------------------------------------------------------")
        
        self.profileWindow.show()

    def profile_with_gauss(self):
        """get a profile of the image and fit it with a gaussian
        """
        #construct the window
        windowName = "profile ({:.3e},{:.3e}) - ({:.3e},{:.3e})".format(self.ui.x0.value(),
                                                                        self.ui.y0.value(),
                                                                        self.ui.x1.value(),
                                                                        self.ui.y1.value())
        self.profileWindow = SimplePlotWindow(name=windowName)
        
        #get the x and y profile data and plot it
        y = self.doseDistribution.profile(self.ui.x0.value(),
                                          self.ui.y0.value(),
                                          self.ui.x1.value(),
                                          self.ui.y1.value(),
                                          interpolation=self.settings["profile interpolation"])
        x = np.linspace(0,self.ui.width.value(),len(y))
        self.profileWindow.ax1.plot(x,y,label="profile")
        
        
        #make some educated guesses for start parameters
        center = (y*x).sum()/y.sum() #expected value
        width = ((x - center)**2).sum()/len(x)
        p0 = [float((np.max(y)-np.min(y))),float(center),float(width),
              float(np.min(y))]
        logging.debug("Parameter guess: {:.4e}, {:.4e}, {:.4e}, {:.4e}".format(*p0))        
        
        #fit and plot function
        p, cov, info, msg, success = curve_fit(gauss,x,y,p0=p0, full_output=True)
        
        if success != 1 and success != 2 and success != 3 and success !=4:
            logging.error("Fit failed with message: "+msg)
        elif cov is None:
            logging.error("None covariance matrix after {:d} iterations".format(info["nfev"]))
        else:
            fittedY = gauss(x,*p)
    
            self.profileWindow.ax1.plot(x,fittedY,label="fit")
    
            #log the results
            logging.info("### Fit results ###")
            logging.info("y = A*exp(-(x-x0)/2*sigma^2) + offset".format(*p))
            logging.info("A = {:.4e} +- {:.4e}".format(p[0],np.sqrt(cov[0][0])))
            logging.info("x0 = {:.4e} +- {:.4e}".format(p[1],np.sqrt(cov[1][1])))
            logging.info("sigma = {:.4e} +- {:.4e}".format(p[2],np.sqrt(cov[2][2])))
            logging.info("offset = {:.4e} +- {:.4e}".format(p[3],np.sqrt(cov[3][3])))
            self.log_fit_points_of_interest(x,y,fittedY)
            logging.info("--------------------------------------------------------------")
        
        self.profileWindow.show()
    
    def log_fit_points_of_interest(self,x, y, fittedY):
        """print the results of a 1D fit on a profile
           outputs maximum and left and right edge of the profile and fit
        """
        dataMax = float(np.max(y)) #don't know why it's not float already, but it is not
        fitMax = np.max(fittedY)
        
        logging.info("points of interest of the fit (profile data)")
        logging.info("max / position: {:.4e} ({:.4e}) / "
                     "{:.4e} ({:.4e})".format(fitMax, dataMax, 
                                              x[np.argmax(fittedY)], 
                                              x[np.argmax(y)]))
        logging.info("left edge / % of max:  {:.4e} ({:.4e}) / "
                     "{:.3f} ({:.3f})".format(fittedY[0],y[0],
                                              100.*fittedY[0]/fitMax,
                                              100.*y[0]/dataMax))
        logging.info("right edge / % of max:  {:.4e} ({:.4e}) / "
                     "{:.3f} ({:.3f})".format(fittedY[-1],y[-1],
                                              100.*fittedY[-1]/fitMax,
                                              100.*y[-1]/dataMax))

    def fit_2D_gauss(self):
        # get resolution and calculate ROI
        DPC = self.doseDistribution.DPC
        xlim = sorted([int(self.ui.x0.value()*DPC),int(self.ui.x1.value()*DPC)])
        ylim = sorted([int(self.ui.y0.value()*DPC),int(self.ui.y1.value()*DPC)])
        
        """ debug code to check if ROI works
        self.testWindow = SimplePlotWindow(name="test")
        self.testWindow.ax1.imshow(self.doseDistribution[ylim[0]:ylim[1],
                                                         xlim[0]:xlim[1]])        
        self.testWindow.show()
        """
        try:
            popt, cov = fit_2D_gauss(self.doseDistribution[ylim[0]:ylim[1],
                                                           xlim[0]:xlim[1]],
                                     useRotation=False)
            
            logging.info("### Results of 2D Guassian fit ###")
            logging.info("A*exp(-(x-x0)^2/(2*sigmaX^2)-(y-y0)^2/(2*sigmaY^2)) + offset")
            logging.info("A = {:.4e} +- {:.4e}".format(popt[0],np.sqrt(cov[0][0])))
            logging.info(("x0/y0 = {:.4e}/{:.4e} +- {:.4e}/{:.4e}"+
                         "").format((popt[1]+xlim[0])/DPC,(popt[2]+ylim[0])/DPC,
                                    np.sqrt(cov[1][1])/DPC,np.sqrt(cov[2][2])/DPC))        
            logging.info(("simgaX/sigmaY = {:.4e}/{:.4e} +- {:.4e}/{:.4e}"+
                         "").format(popt[3]/DPC,popt[4]/DPC,np.sqrt(cov[3][3])/DPC,np.sqrt(cov[4][4])/DPC))
            logging.info("offset = {:.4e} +- {:.4e}".format(popt[5],np.sqrt(cov[5][5])))
            logging.info("--------------------------------------------------------------")
            
            #create a 2D Gauss function using the fitted parameters
            gauss = gauss2D(*popt)
            
            #clear old contour and make new
            self.clear_2D_fit()
                    
            #use the limits to create a grid as coordinates for the plot,
            #imshow uses 1st index as y, therefor y comes first
            #use extent to align the contour with the original plot            
            self.contour = self.ax1.contour(gauss(*np.mgrid[0:ylim[1]-ylim[0],0:xlim[1]-xlim[0]]),
                                                extent=(xlim[0]/DPC, xlim[1]/DPC,
                                                        ylim[0]/DPC, ylim[1]/DPC))

            centerMarker = cross((popt[1]+xlim[0])/DPC,(popt[2]+ylim[0])/DPC,
                                 popt[3]/DPC,popt[4]/DPC,
                                 self.settings["area stat linecolor"])
                                      
            self.gauss_center = self.ax1.add_artist(centerMarker) 
            
            self.canvas.draw()
        except FitError as e:
            logging.error("error fitting 2D Gaussian: "+e.message)


###############################################################################
    # slots
    def calculate(self):
        idx = self.ui.evalFunction.currentIndex()
        try:
            calcResult = self.ui.evalFunction.itemData(idx)["eval"]()
            return calcResult
        except ValueError as e:
            logging.error("Value Error: "+str(e))
            logging.debug("Tracback: " + traceback.format_exc().replace("\n"," - "))
            logging.error("check evaluation method and ROI")

    def clear_2D_fit(self):
        if hasattr(self,"contour"):
            try:
                for coll in self.contour.collections:
                    coll.remove()
            except ValueError as e:
                logging.debug("excepted: "+e.message)
                
        if hasattr(self,"gauss_center"):
            try: 
                self.gauss_center.remove()
            except ValueError as e:
                logging.debug("excepted: "+e.message)

        self.canvas.draw()                

    #three callbacks to connect to matplotlib button press events
    #they put the click coordinates into the input fields
    def click_to_center(self, event):
        if self.toolbar.mode == "" and event.inaxes != None:
            self.ui.xCenter.setValue(event.xdata)
            self.ui.yCenter.setValue(event.ydata)

    def click_to_pos0(self, event):
        if self.toolbar.mode == "" and event.inaxes != None:
            self.ui.x0.setValue(event.xdata)
            self.ui.y0.setValue(event.ydata)

    def click_to_pos1(self, event):
        if self.toolbar.mode == "" and event.inaxes != None:
            self.ui.x1.setValue(event.xdata)
            self.ui.y1.setValue(event.ydata)

    #catch if the focus leaves or enters a certain widget and connect matplotlib
    #button press callbacks accordingly
    def focus_change(self, old, new):
        if (old == self.ui.xCenter or old == self.ui.yCenter or 
            old == self.ui.x0 or old == self.ui.y0 or 
            old == self.ui.x1 or old == self.ui.y1):
            self.canvas.mpl_disconnect(self.cid) 
             
        
        if new == self.ui.xCenter or new == self.ui.yCenter:
            self.cid = self.canvas.mpl_connect('button_press_event', 
                                               self.click_to_center)
        elif new == self.ui.x0 or new == self.ui.y0:
            self.cid = self.canvas.mpl_connect('button_press_event', 
                                               self.click_to_pos0)
        elif new == self.ui.x1 or new == self.ui.y1:
            self.cid = self.canvas.mpl_connect('button_press_event', 
                                               self.click_to_pos1) 
    def isodose_change(self):
        self.ui.nominalDose.setEnabled(self.ui.showIsoLines.isChecked())
        self.ui.isoListField.setEnabled(self.ui.showIsoLines.isChecked())
        
    def refresh(self):
        self.update_dose_plot()
        self.canvas.draw()
        
    def ROI_value_change(self):
        self.match_ui_inputs((not self.ui.alternateSpecToggle.isChecked()))
        self.update_marker()

    def save_as_numpy(self):
        self.savePath = QFileDialog.getSaveFileName(self,
                                                    caption = "select a save file",
                                                    directory = self.savePath,
                                                    filter="Numpy files (*.npy);;All files (*)")

        #in pyqt5 a tuple is returned, unpack it
        if os.environ['QT_API'] == 'pyqt5':
            self.savePath, _ = self.savePath
        
        if self.savePath != "":
            np.save(self.savePath,self.doseDistribution)
        else:
            logging.debug("save canceled")
    
    def save_as_txt(self):
        self.savePath = QFileDialog.getSaveFileName(self,
                                                    caption = "select a save file",
                                                    directory = self.savePath,
                                                    filter="Text files (*.txt);;All files (*)")

        #in pyqt5 a tuple is returned, unpack it
        if os.environ['QT_API'] == 'pyqt5':
            self.savePath, _ = self.savePath
        if self.savePath != "":
            np.savetxt(self.savePath,self.doseDistribution,delimiter="\t")
        else:
            logging.debug("save canceled")
            
    def save_calc_to_file(self):

        #check if selected evaluation is compatible
        idx = self.ui.evalFunction.currentIndex()
        evalFunction = self.ui.evalFunction.itemText(idx)
        if evalFunction not in ('Rectangle','Ellipse'):
            logging.error(evalFunction + ' not supported for saving to file, '
                          'select Rectangle or Ellipse')
            return
        
        filePath = self.ui.saveTablePath.text()
        if filePath == '':
            logging.error("please specifiy file path")
            return

        
        #calculate the values
        stats = self.calculate()
        
        #names of the value isn correct order
        statNames = ["sum",
                     "avg",
                     "std",
                     "min",
                     "max"]
        
        #names of the ui fields to be saved
        uiElementNames = ["xCenter",
                          "yCenter",
                          "height",
                          "width",
                          "angle"]
        
        #combine the names of everything that should be saved             
        header = ["Film No."] + statNames + ['area type'] + uiElementNames
        #list of empty strings to take the data
        saveContent = ['']*len(header)
        
        saveContent[header.index('Film No.')] = self.ui.filmNumber.text()       
        
        #put values from the stats in the correct list position according to their name
        for (name, value) in zip(statNames, stats):
            saveContent[header.index(name)] = str(value)
            
        saveContent[header.index('area type')] = evalFunction
        
        #get values from the desired ui fields and put them in the list
        for name in uiElementNames:
            element = getattr(self.ui,name)
            saveContent[header.index(name)] = str(element.value())

        #add the data from the dose calculation, if present
        if self.calculationSettings is not None:
            keys = list(self.calculationSettings.keys())
            keys.sort()
            for key in keys:
                header.append(key)
                saveContent.append(str(self.calculationSettings[key]))
                
        #create strings
        headerStr = "\t".join(header)+"\n"
        saveStr = "\t".join(saveContent)+"\n"

        try:
            if os.path.isfile(filePath):
                with open(filePath,mode="a") as saveFile:
                    saveFile.write(saveStr)
                    logging.info(("info for "+self.ui.filmNumber.text()+" written to file"))
            else:
                with open(filePath,mode="w") as saveFile:
                    saveFile.write(headerStr)
                    saveFile.write(saveStr)
                    logging.info(("info for "+self.ui.filmNumber.text()+" written to file"))
                    
        except (OSError, IOError) as e:
            logging.error("failed to write to file"+filePath)
            logging.debug("Error: "+str(e))
    
        
    def save_file_dialog(self):
        filePath =QFileDialog.getSaveFileName(self,
                                              caption = 'select a file to save to',
                                              directory = self.ui.saveTablePath.text(),
                                              options = QFileDialog.DontConfirmOverwrite)
        
        #in pyqt5 a tuple is returned, unpack it
        if os.environ['QT_API'] == 'pyqt5':
            filePath, _ = filePath
            
        if filePath != '':
            self.ui.saveTablePath.setText(filePath)
        else:
            logging.info('file selection canceled')

        
    def set_optimal_scale(self):
        doseMax = np.max(self.doseDistribution)
        self.ui.doseMin.setValue(0.0)
        self.ui.doseMax.setValue(doseMax)
        self.ui.nominalDose.setValue(doseMax)
        
        
    def toggle_ROI_spec(self):
        """switch between the two blocks of defining the ROI
        """
        if self.ui.alternateSpecToggle.isChecked():
            self.ui.x0.setEnabled(True)
            self.ui.y0.setEnabled(True)
            self.ui.x1.setEnabled(True)
            self.ui.y1.setEnabled(True)
            
            self.ui.xCenter.setDisabled(True)
            self.ui.yCenter.setDisabled(True)
            self.ui.height.setDisabled(True)
            self.ui.width.setDisabled(True)
            self.ui.angle.setDisabled(True)
            
            self.toolbar.centeredSelection=False
             
        else:
            self.ui.x0.setDisabled(True)
            self.ui.y0.setDisabled(True)
            self.ui.x1.setDisabled(True)
            self.ui.y1.setDisabled(True)
            
            self.ui.xCenter.setEnabled(True)
            self.ui.yCenter.setEnabled(True)
            self.ui.height.setEnabled(True)
            self.ui.width.setEnabled(True)
            self.ui.angle.setEnabled(True)
            
            self.toolbar.centeredSelection=True
            
        self.ROI_value_change()
        
    def toolbar_selection(self):
        #get selection
        selection = self.toolbar.get_selection()
        #check for ROI specification scheme
        if self.ui.alternateSpecToggle.isChecked(): #with simple corners
            
            #tuple of elements that need updating (in same order as selection)
            elements = (self.ui.x0,self.ui.y0,self.ui.x1,self.ui.y1)
            #block the signals from the elements while updating, then call
            #the update slot manually. (avoids circular and repeated updates)
            
            for element, value in zip(elements, selection):
                element.blockSignals(True)
                element.setValue(value)
                element.blockSignals(False)
            self.ROI_value_change()
        else: #with width and center, needs additional calculation
            
            #returned values should be ordered (lower value x0, highvalue x1)
            centerX = (selection[2] + selection[0])/2.0
            centerY = (selection[3] + selection[1])/2.0
            
            #simplify the angle possibilities by using the cyclic nature of rotation
            #and convert to rad
            angle = np.pi*(self.ui.angle.value()%180.)/180. 
            
            deltaX = selection[2] - selection[0]
            deltaY = selection[3] - selection[1]
            
            
            
            if angle >= np.pi/2.0: #greater than 90 is the same as smaller, but switching widht and height
                angle = angle%(np.pi/2.0)
                switch = True
            else:
                switch = False
     
            if angle == 0: # zero is easy
                width = deltaX
                height = deltaY
                
            #everything else needs special conditions, because there will not 
            #exist a rotated rectangle for all possible combinations of angles
            #and widht and height selected
            else:
                if angle <= np.pi/4.0: 
                    deltaY = max(deltaY,np.tan(angle)*deltaX)
                    deltaX = max(deltaX,np.tan(angle)*deltaY)
                else:#i.e. pi/4 < angle < pi/2
                    deltaY = max(deltaY,deltaY/np.tan(angle))
                    deltaX = max(deltaX,deltaY/np.tan(angle))
                
                height = ((np.cos(angle)*deltaY-np.sin(angle)*deltaX) / 
                          (np.cos(angle)**2-np.sin(angle)**2))
                
                width = ((np.cos(angle)*deltaX-np.sin(angle)*deltaY) / 
                          (np.cos(angle)**2-np.sin(angle)**2))

            
            if switch:
                width, height = height, width #amazingly, this works, yeah python
            
            for element, value in zip((self.ui.xCenter,self.ui.yCenter,
                                       self.ui.height, self.ui.width),
                                      (centerX, centerY, height, width)):
                element.blockSignals(True)
                element.setValue(value)
                element.blockSignals(False)
            self.ROI_value_change()            
