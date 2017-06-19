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






ToDo:
save advanced settings?

ideas:
    click and drag for selection of area
    or click and drag moves center for new input style, and area selection for old

"""

import logging
import numpy as np
import os
import sys
sys.path.append(os.path.join(sys.path[0],".."))
from collections import OrderedDict

#Qt stuff
import sip
sip.setapi('QVariant', 2) #use python types instead of qt types (e.g. string insted of Qstring)
from PyQt4 import QtCore, QtGui

from matplotlib import use
use("Qt4Agg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
  import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.pyplot import colormaps
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.patches import Ellipse, Rectangle
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
from scipy.optimize import curve_fit


# simple edit of additional settings
from GUI_tools import easy_edit_settings, simple_plot_window

#2D gauss fitting
import fit_tools

#load qt design UI
from UI.DoseWidgetUI import Ui_DoseWidget

from dose_calc_core import dose_array

def gray_tick(x, pos):
    """prints ticks with a Gy as unit appended"""
    return "{:.2f} Gy".format(x)


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

def cross(x,y,width,height):
    "returns a matplotlib artist the shape of a cross"
    return "blubb"

#define possibilities for color maps and check their availability on 
#the current installation
colorMapChoices = ["inferno","viridis","hot","gnuplot","spectral","jet",
                   "rainbow","gray","seismic"]

for cmap in colorMapChoices:
    if cmap not in colormaps():
        colorMapChoices.remove(cmap)

_advSettings = easy_edit_settings([("area stat linecolor","red"),
                                   ("area stat linewidth",2.0),
                                   ("label axes",True), 
                                   ("color map",[0]+colorMapChoices),
                                   ("show grid",False),
                                   ("profile interpolation",
                                    [0,"nearest","linear","spline"])])

_defaultSettings = _advSettings.get_settings()


class doseWidget(QtGui.QWidget):
    """This class displays a dose distribution in a matplotlib plot and provides
        several ways to perform calculations and fits on that dose distribution
    """
    def __init__(self, doseDistribution, settings=_defaultSettings):
        """
            Constructor
        """

        QtGui.QWidget.__init__(self)
        
        #save local copy of dose and DPI                    
        self.doseDistribution = doseDistribution
#        self.DPC = DPI/2.54

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
                                 ("Parabola profile",{"eval":self.profile_with_parabola,
                                                     "marker":self.line_marker,
                                                     "tip":"get a profile and fit a parabola"}),
                                 ("Gauss profile",{"eval":self.profile_with_gauss,
                                                   "marker":self.line_marker,
                                                   "tip":"get a profile and fit a gaussian"}),
                                 ("2D Gauss fit",{"eval":self.fit_2D_gauss,
                                                  "marker":self.axis_parallel_rectangle_marker,
                                                  "tip":"fit the entire distribution with a 2D Gaussian"})])
        
        #set up combobox with functions dictionary
        for key in functions:
            self.ui.evalFunction.addItem(key,functions[key])
            idx = self.ui.evalFunction.count()-1
            self.ui.evalFunction.setItemData(idx,functions[key]["tip"],
                                             QtCore.Qt.ToolTipRole)
        
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

        QtGui.qApp.focusChanged.connect(self.focus_change)
        
        #buttons
        self.ui.alternateSpecToggle.stateChanged.connect(self.toggle_ROI_spec)
        self.ui.refreshButton.clicked.connect(self.refresh)
        self.ui.bestLimits.clicked.connect(self.set_optimal_scale)
        self.ui.calculateButton.clicked.connect(self.calculate)        
        self.ui.exportTxtButton.clicked.connect(self.save_as_txt)
        self.ui.exportNpButton.clicked.connect(self.save_as_numpy)
        self.ui.clearFitButton.clicked.connect(self.clear_2D_fit)
        
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
        self.toolbar = NavigationToolbar2QT(self.canvas, None)

        self.ui.imageLayout.addWidget(self.canvas)
        self.ui.imageLayout.addWidget(self.toolbar)

    def set_ui_limits(self):
        """set the limits of the various UI elements depending on the dose distribution
        """

        #set dose limits
        doseMax = np.max(self.doseDistribution)
        self.ui.doseMin.setMaximum(doseMax*10.)
        self.ui.doseMax.setMaximum(doseMax*10.)
        self.ui.doseMin.setMinimum(0.0)
        self.ui.doseMax.setMinimum(0.0)
        
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
##############################################################################
# UI update methods
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
                                            extent=[0,xMax,yMax,0])
                    
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
            

    def update_dose_plot(self):
        """set limits and colormap of the dose plot
        """

        #set limits of the color map                    
        self.dosePlot.set_clim(self.ui.doseMin.value(),
                               self.ui.doseMax.value())
        #set the colormap and add it to the plot
        self.dosePlot.set_cmap(self.settings["color map"])

        self.clb.update_normal(self.dosePlot)

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
# evaluation methods which are called upon clicking calcualte
        
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
        

    def ellipse(self):
        """calculate and print the stats for an ellipse area
        """

        #get the stats
        stats = self.doseDistribution.ellipse_stats(self.ui.xCenter.value(),
                                                    self.ui.yCenter.value(),
                                                    self.ui.width.value()/2.0, 
                                                    self.ui.height.value()/2.0,
                                                    self.ui.angle.value())
        print stats                                            
        logging.info("### Statistics for ellipse ###")
        logging.info("sum: {:.4e} Gy*cm^2".format(stats[0]/self.doseDistribution.DPC**2))
        logging.info("average: {:.4e} Gy".format(stats[1]))
        logging.info("standard deviation: {:.4e} Gy".format(stats[2]))
        logging.info("minimum: {:.4e} Gy".format(stats[3]))        
        logging.info("maximum: {:.4e} Gy".format(stats[4]))
        logging.info("--------------------------------------------------------------")
    
    def profile_with_parabola(self):
        """get a profile of the image and fit it with a 2nd order polynomial
        """
        #construct the window
        windowName = "profile ({:.3e},{:.3e}) - ({:.3e},{:.3e})".format(self.ui.x0.value(),
                                                                        self.ui.y0.value(),
                                                                        self.ui.x1.value(),
                                                                        self.ui.y1.value())
        self.profileWindow = simple_plot_window(name=windowName)
        
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
        self.profileWindow = simple_plot_window(name=windowName)
        
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
        elif cov == None:
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
        self.testWindow = simple_plot_window(name="test")
        self.testWindow.ax1.imshow(self.doseDistribution[ylim[0]:ylim[1],
                                                         xlim[0]:xlim[1]])        
        self.testWindow.show()
        """
        try:
            popt, cov = fit_tools.fit_2D_gauss(self.doseDistribution[ylim[0]:ylim[1],
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
            gauss = fit_tools.gauss2D(*popt)
            
            #clear old contour and make new
            self.clear_2D_fit()
                    
            #use the limits to create a grid as coordinates for the plot,
            #imshow uses 1st index as y, therefor y comes first
            #use extent to align the contour with the original plot            
            self.contour = self.ax1.contour(gauss(*np.mgrid[0:ylim[1]-ylim[0],0:xlim[1]-xlim[0]]),
                                                extent=(xlim[0]/DPC, xlim[1]/DPC,
                                                        ylim[0]/DPC, ylim[1]/DPC))

            cross = fit_tools.cross((popt[1]+xlim[0])/DPC,(popt[2]+ylim[0])/DPC,
                                      popt[3]/DPC,popt[4]/DPC,
                                      self.settings["area stat linecolor"])
                                      
            self.gauss_center = self.ax1.add_artist(cross) 
            
            self.canvas.draw()
        except fit_tools.FitError as e:
            logging.error("error fitting 2D Gaussian: "+e.message)


###############################################################################
    # slots
    def calculate(self):
        idx = self.ui.evalFunction.currentIndex()
        try:
            self.ui.evalFunction.itemData(idx)["eval"]()
        except ValueError as e:
            logging.error("Value Error: "+e.message)
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
    
    def refresh(self):
        self.update_dose_plot()
        self.canvas.draw()
        
    def ROI_value_change(self):
        self.match_ui_inputs((not self.ui.alternateSpecToggle.isChecked()))
        self.update_marker()

    def save_as_numpy(self):
        self.savePath = QtGui.QFileDialog.getSaveFileName(self,"select a save file",
                                                          self.savePath)
        if self.savePath != "":
            np.save(self.savePath,self.doseDistribution)
        else:
            logging.debug("save canceled")
    
    def save_as_txt(self):
        self.savePath = QtGui.QFileDialog.getSaveFileName(self,"select a save file",
                                                          self.savePath)
        if self.savePath != "":
            np.savetxt(self.savePath,self.doseDistribution,delimiter="\t")
        else:
            logging.debug("save canceled")
            
            
    def set_optimal_scale(self):
        doseMax = np.max(self.doseDistribution)
        self.ui.doseMin.setValue(0.0)
        self.ui.doseMax.setValue(doseMax)
        
        
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
            
        self.ROI_value_change()


###############################################################################
# run (for testing purposes)

from UI.TestWindowUI import Ui_MainWindow

class TestGUI(QtGui.QMainWindow):
    def __init__(self):
        """
            Constructor
        """

        QtGui.QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self) 
        
        xDim = 4000 
        yDim = 4000
        
        x,y = np.meshgrid(np.linspace(0,xDim,yDim),np.linspace(0,xDim,yDim))
        dose = (5.0*np.exp(-np.divide(np.square(x-100),2*50**2)-np.divide(np.square(y-235),2*100**2))
            +np.random.rand(xDim,yDim)*0.1)
    
        dose = dose.view(dose_array)
        widget = doseWidget(dose)
        
        self.ui.tabWidget.addTab(widget,"DoseView 1")
        
        


def run():
    #setup a basic logger and create a noisy gaussian
    logging.basicConfig(level=logging.DEBUG)


    app = QtGui.QApplication(sys.argv)
    gui = TestGUI()
   

#    gui.addDockWidget(QtCore.Qt.BottomDockWidgetArea,doseDock(dose))
    gui.show()
    sys.exit(app.exec_())

#run the gui
if __name__ == '__main__':
    run()         