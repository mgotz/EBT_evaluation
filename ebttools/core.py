# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2016 Malte Gotz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

While I believe due to the GPL exception provided by PyQt the enitre
package may be licensed under the MIT license, I want to make sure this module
is explicitly licensed as such, because it does not import and is therefore
independent of PyQt and the GPL


core functions to load calibration data and calculate dose from scanned films

When used outside the EBT gui, import calibrations using the load_calibrations
function. Afterwards, construct a DoseArray using one of the imported 
calibrations, the scanned image, DPI and phi0 info.
The calculate_dose function, performs the dose calculation and it is called by
DoseArray during construction.
   
"""
#get ready for python 3
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

import codecs
from collections import OrderedDict

import logging
import numpy as np
import os
import scipy.ndimage
from math import floor, ceil

try:
    from configparser import ConfigParser, MissingSectionHeaderError
except ImportError as e:
    #a compatibility hack for python2 if it does not have conifgparser
    import sys
    if sys.version_info[0] == 2:
        from ConfigParser import ConfigParser, MissingSectionHeaderError
    else:
        raise e

#define which array index corresponds to which color
rgbMap = {"red":0,"green":1,"blue":2}

def load_calibrations(path = None):
    """loads ini style calibration files from path
    
    Parameters
    ---------
    path : file path
        either a single calibration file or a folder containing only calibration
        files
    
    Returns
    -------
    calibrations : dictionary of dictionaries
        contains a named entry for each calibration with the respective values
        as a dictionary
    """
    
    #default calibrations location
    if path is None:
        path = os.path.join(os.path.dirname(__file__),"calibrations")
    
    #make a new ordered dictionary, that way keys remain in some sensible order
    #when iterating over the dict
    calibrations = OrderedDict()
    if os.path.isfile(path):
        head, tail = os.path.split(path)
        path = head
        fileList = [tail]
    elif os.path.isdir(path):
        fileList = os.listdir(path)
    else:
        raise IOError(255, "path is neither directory nor file",path)
    
    if len(fileList) == 0:
        raise IOError(255,"no files found",path)
        
    for fileName in fileList:
        with codecs.open(os.path.join(path,fileName),"r","utf-8-sig") as configFile:
            try:
                config = ConfigParser(dict_type=OrderedDict)
                config.readfp(configFile)
                for key in config.sections():
                    calibrations[key] = dict(config.items(key))
            except MissingSectionHeaderError:
                logging.warning("{!s} not a readable calibration".format(fileName))
            except UnicodeDecodeError:
                logging.warning("{!s} not a readable utf-8 file".format(fileName))
            except Exception as e:
                logging.error("Exception occured trying to read {!s}: ".format(fileName)+str(e))
          
    if len(calibrations) == 0:
        raise IOError(255,"files contain no readable calibration",path)
    
    return calibrations
    
def calculate_dose(calibration, scan, phi0):
    """ calculates the dose from a scanned image and a given calibration
    
    Parameters
    ----------
    calibration : dictionary
        describes the calibration with the keys: argument, p1, p2, p3, function 
        and channel, optional keys are black and background
    scan : numpy array
        the scanned image or part thereof
    phi0 : scalar or lenght 3 iterable
        I0 to calculate the net optical density
        
    Returns
    -------
    dose : numpy array
        array containing the dose
    """

        
    try:
        black = float(calibration["black"])
    except KeyError:
        black = 10
        logging.warning("no definition of lowest pixel value found in calibration"
                        " falling back to default 10")

    try:
        background = float(calibration["background"])
    except KeyError:
        background = 0.0
        logging.warning("no definition of background value found in calibration"
                        " falling back to default 0")   

       
    #check proper format of phi0 and allow treatement as a list in any case
    try:
        if len(phi0) != 3:
            raise ValueError("phi0 should have length 3"+
                             " (one value for each channel) or be a scalar")
    except TypeError: #raised if length is not applicable
        phi0 = [phi0]

    #get the channels in list
    channels = calibration["channel"].replace(" ","").split(",")
    
    #flags set by the different argument options, if a min and/or max is needed 
    #to ensure against matherrors. Used later to issue warning about min and max
    needsMin = False
    usesMax = False
    #define number of channels used by the argument (also used in input checking)
    numberOfChannels = 0
    
    #define the argument as a function
    if calibration["argument"] == "netOD":
        arg = lambda x, x0: np.log10((x0-background)/
                                 (np.clip(x,int(ceil(black)),int(floor(x0)))-background))

        numberOfChannels = 1
        needsMin = True #will result in log(-) otherwise
        usesMax = True #not really needed, but gives negative dose values
        
        if any(black > x0 for x0 in phi0):
            phiStr = ["{:.2f}".format(x0) for x0 in phi0]
            raise ValueError("phi0 ("+", ".join(phiStr) +") is smaller"+
                             " than the black value ({:.2f}). ".format(black) +
                             "Cannot procede.")

        
    elif calibration["argument"] == "direct":
        arg = lambda x, x0: (np.clip(x,black,None)-background)
        
        numberOfChannels = 1
        needsMin = False
        usesMax = False
    
    elif calibration["argument"] == "normalized":
        arg = lambda x, x0: np.divide(np.clip(x,int(ceil(black)),None)-background,
                                      x0-background)
        
        numberOfChannels = 1
        needsMin = False
        usesMax = False

    
    elif calibration["argument"] == "relativeNetOD":
        arg = lambda x1, x2, x01, x02: (
                np.log10((x01-background)/(np.clip(x1,int(ceil(black)),int(floor(x01)))-background))/
                 np.log10((x02-background)/(np.clip(x2,int(ceil(black)),int(floor(x02)))-background)))
        numberOfChannels = 2
        needsMin = False
        usesMax = False
        

    else:
        raise ValueError("unknown specification for argument in calibration: "
                        +calibration["argument"])

    #check for proper number of channels
    if len(channels) != numberOfChannels:
        raise ValueError(calibration["argument"] + 
                         " requires exactly {:d} channels, ".format(numberOfChannels) +
                          "{:d} given".format(len(channels)))

    #check for properly established lower limit
    if needsMin:
        if (background >= black) and np.any((scan-background) < 0):
            raise ValueError("scan contains values below the background level, "+
                             "cannot compute "+calibration["argument"])
    if needsMin and usesMax:
        if any(black > x0 for x0 in phi0):
            phiStr = ["{:.2f}".format(x0) for x0 in phi0]
            raise ValueError("phi0 ("+", ".join(phiStr) +") is smaller"+
                             " than the black value ({:.2f}). ".format(black) +
                             "Cannot procede.")

    p1 = float(calibration["p1"])
    p2 = float(calibration["p2"])
    p3 = float(calibration["p3"])
    
    #define the actual function for dose calculation
    if calibration["function"] == "exp_poly":
        function = lambda x: p1*x+p2*np.power(x,p3)
    elif calibration["function"] == "linear":
        function = lambda x: p1+p2*x
    elif calibration["function"] == "rational":
        function = lambda x: np.divide(p1+x,p2+p3*x)
    else:
        raise ValueError("unknown specification for function in calibration: "
                        +calibration["function"])

   
   
    #get the proper channels from the scan and select the corresponding phi0s
    if all(color in rgbMap for color in channels):
        chIndices = [rgbMap[color] for color in channels]
        relevantScanData = [scan[:,:,index] for index in chIndices]
        if len(chIndices) == 1 and len(phi0) == 1:
            relevantPhi0 = phi0
        elif len(phi0) != 3:
            raise ValueError("phi0 must contain 3 values or be a scalar for "+
                             "single channel evaluation")
        else:
            relevantPhi0 = [phi0[index] for index in chIndices]
    elif calibration["channel"] in ["grey","gray"]:
        if  len(scan.shape) > 2:
            raise ValueError("calibration is for grey scale, but scan in multicolor")
        relevantScanData = [scan]
        if len(phi0) != 1:
            raise ValueError("more than 1 phi0 provided for a grey-scale evaluation")
        else:    
            relevantPhi0 = phi0
    else:
        raise ValueError("unknown specification for color channel in calibration: "
                        +calibration["channel"])

    #use the function and the argument to calculate dose from the relevant data  
    return function(arg(*(relevantScanData+relevantPhi0)))

class DoseArray(np.ndarray):
    """ class to contain a dose distribution
    
    this is basically a ndarray with some additional methods and properties
    the dose can be used and accessed just like it were in a standard ndarray
    """
    def __new__(cls,DPI,calib,img,phi0):
        """ creates a dose_array from scan, calibration and phi0
        
        Parameters
        ----------
        DPI : scalar
            dots per inch of the scan
        calib : dictionary
            describes the calibration with the keys: argument, p1, p2, p3, 
            function and channel
        img : numpy array
            the scanned image or part thereof
        phi0 : scalar
            I0 to calculate the net optical density
        """
        #calculate dose and cast returned array to new class
        dist = calculate_dose(calib,img,phi0)
        obj = np.asarray(dist).view(cls)
        
        if DPI > 0:
            #set dot per centimeter
            obj.DPC = DPI/2.54
        else:
            raise ValueError("DPI must be greater than 0")
            
        try:
            obj.unit = calib["unit"]
        except KeyError:
            obj.unit = "Gy"
        
        return obj
        
    def __array_finalize__(self,obj):
        #gets called in various construction scenarios, obj is none if it is called from
        #__new__, DPC will then be properly set, othwerwise set a default for DPC and unit
        if obj is None: return
            
        self.DPC = getattr(obj,'DPC',300./2.54)
        self.unit = "Gy"
    
    def rectangle_mask(self,x0, y0, width, height, angle=0.0):
        """get a mask for a rectangular area
        
        Parameters
        ----------
        x0 : scalar
            x-value of rectangle center (in cm)
        y0 : scalar
            y-value of rectangle center (in cm)
        width : scalar
            half-width (x-dimension) of the rectangle
        height : scalar
            half-height (y-dimension) of the rectangle
        angle : scalar, optional
            counter clockwise rotation angle of the rectangle
        test : bool, optional
            if true the area is set to 0 (used for testing)
            
        Returns
        -------
        mask : ndarray
            a mask to index the array and return a rectangular area
        """
        
        angle_rad = angle*np.pi/180.
        #create a boolean mask for a rectangle
        #the mgrid creates two arrays with x and y positions of the pixels, respectively
        #(y is the first index)
        #if the lower edge of the pixels is at 0, the position of their center 
        #must be shifted by 0.5 pixels width.
        y, x = np.mgrid[-y0+0.5/self.DPC:(self.shape[0]+.5)/self.DPC-y0:1.0/self.DPC,
                        -x0+0.5/self.DPC:(self.shape[1]+.5)/self.DPC-x0:1.0/self.DPC]
        
       
        #condition for a rectangle
        mask = np.logical_and(np.abs(x*np.cos(angle_rad)-y*np.sin(angle_rad)) <= width,
                              np.abs(x*np.sin(angle_rad)+y*np.cos(angle_rad)) <= height)
        
        #ensure proper format:
        mask = mask[0:self.shape[0],0:self.shape[1]]
        
        return mask
        
    def rectangle_stats(self,x0, y0, width, height, angle=0.0, test=False):
        """ get statistics from a rectangular area
        
        Parameters
        ----------
        x0 : scalar
            x-value of rectangle center (in cm)
        y0 : scalar
            y-value of rectangle center (in cm)
        width : scalar
            half-width (x-dimension) of the rectangle
        height : scalar
            half-height (y-dimension) of the rectangle
        angle : scalar, optional
            counter clockwise rotation angle of the rectangle
        test : bool, optional
            if true the area is set to 0 (used for testing)
            
        Returns
        -------
        sum : scalar
            sum of all the pixels in the area
        mean : scalar
            average pixel value
        std : scalar
            standard devition of the pixel values
        min : scalar
            minimal pixel value in the area
        max : scalar
            maximum pixel value in the area
        """
        
        mask = self.rectangle_mask(x0, y0, width, height, angle)

        if test:
            self[mask] = 0

        return(float(self[mask].sum()), float(self[mask].mean()),
               float(self[mask].std()), float(self[mask].min()),
               float(self[mask].max()))

    def ellipse_stats(self,x0, y0, a, b, angle=0.0, test=False):
        """ get statistics from an ellipse area
        
        Parameters
        ----------
        x0 : scalar
            x-value of ellipse center (in cm)
        y0 : scalar
            y-value of ellipse center (in cm)
        a : scalar
            half-axis in x-direction
        b : scalar
            half-axis in y-direction
        angle : scalar, optional
            counter clockwise rotation angle of the ellipse
        test : bool, optional
            if true the area is set to 0 (used for testing)
            
        Returns
        -------
        sum : scalar
            sum of all the pixels in the area
        mean : scalar
            average pixel value
        std : scalar
            standard devition of the pixel values
        min : scalar
            minimal pixel value in the area
        max : scalar
            maximum pixel value in the area
        """        
        angle_rad = angle*np.pi/180
        #create a boolean mask for a circle
        #the mgrid creates two arrays with x and y positions the pixels, respectively
        #(y is the first index)
        #if the lower edge of the pixels is at 0, the position of their center 
        #must be shifted by 0.5 pixels width.
        y, x = np.mgrid[-y0+0.5/self.DPC:(self.shape[0]+.5)/self.DPC-y0:1.0/self.DPC,
                        -x0+0.5/self.DPC:(self.shape[1]+.5)/self.DPC-x0:1.0/self.DPC]
        #condition for an ellipse
              
        mask = ((x*np.cos(angle_rad)-y*np.sin(angle_rad))**2/(a*a) + 
                (-x*np.sin(angle_rad)-y*np.cos(angle_rad))**2/(b*b)) <= 1.0
        
        #ensure proper format:
        mask = mask[0:self.shape[0],0:self.shape[1]]

        if test:
            self[mask] = 0

        return(float(self[mask].sum()), float(self[mask].mean()),
               float(self[mask].std()), float(self[mask].min()),
               float(self[mask].max()))

    def profile(self, x0, y0, x1, y1, interpolation="nearest",test=False):
        """ returns a profile along a line
        
        Parameters
        ----------
        x0 : scalar
            x start of line (in cm)
        y0 : scalar
            y start of line (in cm)
        x1 : scalar
            x end of line (in cm)
        y1 : scalar
            y end of line (in cm)
        interpolation : string, optional
            interpolation method used, nearest, linear or spline
        test : bool, optional
            if true the profile is set to 0 (used for testing)
            
        Returns
        -------
        profile : ndarray
            the dose values along the specified line
        """
        
        #transform to image indexes
        coords = (np.array([y0,x0,y1,x1])*self.DPC).astype(np.int)

        #force coordinates to match array, i.e. avoid exceeding index range
        for idx, coord in enumerate(coords):
            if coord > self.shape[idx%2]:
                coord = self.shape[idx%2]-1
            while coord < 0:
                coord += self.shape[idx%2]
            coords[idx] = coord 

        #make two arrays with indexes from start to end coordinates
        length = int(np.hypot(coords[3]-coords[1], coords[2]-coords[0]))
        x, y = np.linspace(coords[1], coords[3], length), np.linspace(coords[0], coords[2], length)

        if test:
            self[y.astype(np.int),x.astype(np.int)]=0.0

        if interpolation == "nearest":
            return self[y.astype(np.int),x.astype(np.int)]
        elif interpolation == "linear":
            return scipy.ndimage.map_coordinates(self, np.vstack((x,y)),order=1)    
        elif interpolation == "spline":
            return scipy.ndimage.map_coordinates(self, np.vstack((x,y)))
        else:
            logging.warning("unkown interpolation: {!s} using nearest".format(interpolation))
            return self[y.astype(np.int),x.astype(np.int)]
        
        
# for testing
if __name__ == '__main__':
    #load some calibrations
    calibs = load_calibrations(os.path.join(os.path.abspath(os.path.curdir),"calibrations"))
    #create a simple scan (~4x4 cm)
    scan = np.zeros((470,470,3),dtype="uint8")

    #create a coordinate grid and a 2D gaussian with noise
    x,y = np.meshgrid(np.linspace(0,470,470),np.linspace(0,470,470))
    scan[:,:,0] = (-120.0*np.exp(-np.divide(np.square(x-235)+np.square(y-235),
                                           2*50**2))
                   +200+np.random.rand(470,470)*5.0)

    doseDistribution = DoseArray(300.,calibs["example"],scan,255)
    
    doseDistribution.rectangle_stats(1.0,1.0,0.5,0.5,0.,True)
    
    mask = doseDistribution.rectangle_mask(0.4,0.5,0.2,0.1,0.0)
    print (doseDistribution[mask].shape)

    summed, avg, std, minimum, maximum = doseDistribution.rectangle_stats(0.4,0.5,0.2,0.1,45.0,False)
    print (summed, avg, std, minimum, maximum)

    doseDistribution.ellipse_stats(2.0,1.0,0.5,0.2,0.0,False)    
    
    x0 = 0.5
    x1 = 3.5
    y0 = 0.5
    y1 = 3.5
    
    profile1 = doseDistribution.profile(x0,y0,x1,y1,)
    profile2 = doseDistribution.profile(x0,y0,x1,y1,interpolation="spline")
    profile3 = doseDistribution.profile(x0,y0,x1,y1,interpolation="linear")      
    
    import matplotlib.pyplot as plt
    
    fig1, ax = plt.subplots(nrows = 2)
    ax[0].imshow(doseDistribution,extent=[0,470.*2.54/300.,470.*2.54/300.,0],
                 interpolation="nearest",cmap="inferno")
    
    x = np.linspace(0,np.hypot(x1-x0,y1-y0),len(profile1))       
    ax[1].plot(x,profile1,label="nearest")
    ax[1].plot(x,profile2,label="spline")
    ax[1].plot(x,profile3,label="linear")
    ax[1].legend()


    plt.show()
        
        