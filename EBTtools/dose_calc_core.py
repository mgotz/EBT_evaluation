# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 20:10:16 2016

@author: Malte

core functions to load calibration data and calculate dose from scanned films
   
"""

import codecs
from collections import OrderedDict
import ConfigParser
import logging
import numpy as np
import os
import scipy.ndimage
from math import floor, ceil

#define which array index corresponds to which color
rgbMap = {"red":0,"green":1,"blue":2}

def load_calibrations(path):
    """loads ini style calibration files from path
    
    Parameters
    ---------
    path : file path
        either a single calibration file or a folder containing only calibration
        file
    
    Returns
    -------
    calibrations : dictionary of dictionaries
        contains a named entry for each calibration with the respective values
        as a dictionary
    """
    
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
        with codecs.open(os.path.join(path,fileName),"r","utf8") as configFile:
            config = ConfigParser.ConfigParser()
            config.readfp(configFile)
            for key in config.sections():
                calibrations[key] = dict(config.items(key))
          
    if len(calibrations) == 0:
        raise IOError(255,"files contain no readable calibration",path)
    
    return calibrations
    
def calculate_dose(calibration, scan, phi0):
    """ calculates the dose from a scanned image and a given calibration
    
    Parameters
    ----------
    calibration : dictionary
        describes the calibration with the keys: argument, p1, p2, p3, function and channel
        optional keys are black and background
    scan : numpy array
        the scanned image or part thereof
    phi0 : scalar
        I0 to calculate the net optical density
        
    Returns
    -------
    dose : numpy array
        array containing the dose
    """

        
    try:
        black = calibration["black"]
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

    
    #define the argument as a function
    if calibration["argument"] == "netOD":
        arg = lambda x: np.log10((phi0-background)/
                                 (x-background))
        clip = True #limit the values later to black and phi0 to avoid negative OD
        
    elif calibration["argument"] == "direct":
        arg = lambda x: (x-background)
        clip = False #no limiting needed
        
    else:
        raise ValueError("unknown specification for argument in calibration: "
                        +calibration["argument"])


    if clip and black > phi0:
        raise ValueError(("phi0 ({:.2f}) is smaller than the black value ({:.2f}). "+
                         "Cannot procede.").format(phi0, black))

    p1 = float(calibration["p1"])
    p2 = float(calibration["p2"])
    p3 = float(calibration["p3"])
    
    #define the actual function for dose calculation
    if calibration["function"] == "exp_poly":
        function = lambda x: p1*x+p2*np.power(x,p3)
    elif calibration["function"] == "linear":
        function = lambda x: p1+p2*x
    else:
        raise ValueError("unknown specification for function in calibration: "
                        +calibration["function"])

   
   
   #calculate the dose
    if calibration["channel"] in ["red","green","blue"]:
        channel = rgbMap[calibration["channel"]]
        #take the specified function of the given argument construction 
        #(usually net optical density) and clip values to max min.
        if clip:
            dose = function(arg(np.clip(scan[:,:,channel],int(ceil(black)),int(floor(phi0)))))
        else:
            dose = function(arg(scan[:,:,channel]))
            
    elif calibration["channel"] in ["grey","gray"]:
        if  len(scan.shape) > 2:
            raise ValueError("calibration is for grey scale, but scan in multicolor")
        dose = function(arg(scan))
    else:
        raise ValueError("unknown specification for color channel in calibration: "
                        +calibration["channel"])

    #give it back    
    return dose

class dose_array(np.ndarray):
    """ class to conatain a dose distribution
    
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
            width (x-dimension) of the rectangle
        height : scalar
            height (y-dimension) of the rectangle
        angle : scalar, optional
            counter clockwise rotation angle of the rectangle
        test : bool, optional
            if true the area is set to 0 (used for testing)
            
        Returns
        -------
        mask : ndarray
            a mask to index the array an return a rectangular area
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
            width (x-dimension) of the rectangle
        height : scalar
            height (y-dimension) of the rectangle
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
            half-axies in x-direction
        b : scalar
            half-axies in y-direction
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
    calibs = load_calibrations(os.path.join(os.path.curdir,"Calibration"))
    #create a simple scan (~4x4 cm)
    scan = np.zeros((470,470,3),dtype="uint8")

    #create a coordinate grid and a 2D gaussian with noise
    x,y = np.meshgrid(np.linspace(0,470,470),np.linspace(0,470,470))
    scan[:,:,0] = (-120.0*np.exp(-np.divide(np.square(x-235)+np.square(y-235),
                                           2*50**2))
                   +200+np.random.rand(470,470)*5.0)

    doseDistribution = dose_array(300.,calibs["example"],scan,255)
    
    mask = doseDistribution.rectangle_mask(0.4,0.5,0.2,0.1,0.0)
    print doseDistribution[mask].shape

    summed, avg, std, minimum, maximum = doseDistribution.rectangle_stats(0.4,0.5,0.2,0.1,45.0,False)
    print (summed,avg,std,minimum,maximum)

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
        
        