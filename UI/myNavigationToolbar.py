# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:37:42 2016

@author: gotzm

a custom matplotlib toolbar for qt backend
"""

import logging
import os.path as pathTools

from matplotlib.backends.backend_qt4agg \
  import NavigationToolbar2QT
from matplotlib import rcParams as mplParams  


from matplotlib.backend_tools import Cursors
cursors = Cursors()

class myNavigationToolbar(NavigationToolbar2QT):
    """a toolbar with subplots and save removed and a selection tool added
       connect a callback to "selection_changed" to get notified when the 
       selection is changed
    """
    
    #remove unwanted items from the toolbar
    toolitems = [t for t in NavigationToolbar2QT.toolitems if t[0] not in ('Subplots', 'Save')]
    #create a path of the selection icon relative to where qt5 backend looks
    try:
        iconPath = pathTools.relpath(pathTools.join(pathTools.curdir,"UI","select_icon"),
                                     start=pathTools.join(mplParams["datapath"],'images'))
    #on windows a relative path from e.g. c: to d: is not possible, so no path
    #can be constructed this way and no icon will be used                                     
    except ValueError:
        iconPath = "select_icon"

    #add selection icon and seperator in front of other icons
    toolitems = [("Select","make a slection",iconPath,"select"),(None,None,None,None)]+toolitems
    
    def __init__(self, canvas,parent):
        NavigationToolbar2QT.__init__(self,canvas,parent)

        #set the selection button as a toggle and initialize the mode
        self._actions["select"].setCheckable(True)
       
       
        self._ids_selection = []
        self.currentSelection = (0,0,0,0)
   
    #pretty much a copy of the zoom method from backend_bases
    def select(self):
        """Activate the select tool."""
        # set the button press funcs to the appropriate callbacks

        if self._active == 'SELECT':
            self._active = None
        else:
            self._active = 'SELECT'
        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)
            self.mode = ''

        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)
            self.mode = ''

        if self._active:
            self._idPress = self.canvas.mpl_connect(
                'button_press_event', self.selection_clicked)
            self._idRelease = self.canvas.mpl_connect(
                'button_release_event', self.selection_released)
            self.mode = 'select'
            self.canvas.widgetlock(self)
        else:
            self.canvas.widgetlock.release(self)

        self.set_message(self.mode)        

        self._update_buttons_checked()    

    #overwrite parent method to include the select button
    def _update_buttons_checked(self):
        # sync button checkstates to match active mode
        self._actions['pan'].setChecked(self._active == 'PAN')
        self._actions['zoom'].setChecked(self._active == 'ZOOM')
        self._actions['select'].setChecked(self._active == 'SELECT')
    
    #also overwrite to get different cursor for selection
    def _set_cursor(self, event):
        if not event.inaxes or not self._active:
            if self._lastCursor != cursors.POINTER:
                self.set_cursor(cursors.POINTER)
                self._lastCursor = cursors.POINTER
        else:
            if self._active == 'ZOOM':
                if self._lastCursor != cursors.SELECT_REGION:
                    self.set_cursor(cursors.SELECT_REGION)
                    self._lastCursor = cursors.SELECT_REGION
            elif (self._active == 'PAN' and
                  self._lastCursor != cursors.MOVE):
                self.set_cursor(cursors.MOVE)
                self._lastCursor = cursors.MOVE
            elif (self._active == 'SELECT' and
                  self._lastCursor != cursors.SELECT_REGION):
                self.set_cursor(cursors.SELECT_REGION)
                self._lastCursor = cursors.SELECT_REGION

    def get_selection(self):
        """return the current selection"""
        return self.currentSelection    
    
    def selection_clicked(self, event):
        """the press mouse button for selection callback"""
        # return if in not in selection mode 
        if self._active != 'SELECT': return

        # If we're already in the middle of a selection, pressing another
        # button works to "cancel"            
        if self._ids_selection != []:
            for selection_id in self._ids_selection:
                self.canvas.mpl_disconnect(selection_id)
            self.release(event)
            self.draw()
            self._selectionStart = None
            self._button_pressed = None
            self._ids_selection = []
            return

        if event.button == 1:
            self._button_pressed = 1
        elif event.button == 3:
            self._button_pressed = 3
        else:
            self._button_pressed = None
            return

        self._selectionStart = []
        
        x, y = event.x, event.y
        for a in self.canvas.figure.get_axes():
            if (x is not None and y is not None and a.in_axes(event)):
                self._selectionStart.append((x, y, a))

        id1 = self.canvas.mpl_connect('motion_notify_event', self.selection_move)

        self._ids_selection = [id1]

        self.press(event)
        
    def selection_move(self, event):
        """the move mouse for selection callback"""
        if self._selectionStart:
            
            x, y = event.x, event.y
            lastx, lasty, a = self._selectionStart[0]
            
            x1, y1, x2, y2 = a.bbox.extents
            x, lastx = max(min(x, lastx), x1), min(max(x, lastx), x2)
            y, lasty = max(min(y, lasty), y1), min(max(y, lasty), y2)         
            
            self.draw_rubberband(event, x, y, lastx, lasty)
                                 
    def selection_released(self, event):
        """the release mouse for selection callback"""
        
        # return if in not in selection mode
        if self._active != 'SELECT': return
            
        x, y = event.x, event.y
        firstx, firsty, a = self._selectionStart[0]
        inv = a.transData.inverted()
        
        #ensure that mouse has not moved beyond the axis
        x1, y1, x2, y2 = a.bbox.extents
        x, firstx = max(min(x, firstx), x1), min(max(x, firstx), x2)
        y, firsty = max(min(y, firsty), y1), min(max(y, firsty), y2)         
        
        #transform display coordinates to data coordinates
        x0, y0 = inv.transform_point((firstx, firsty))
        x1, y1 = inv.transform_point((x, y))
        
        #sort the values in data coordinates
        x0, x1 = int(min(x0, x1)), int(max(x0,x1))        
        y0, y1 = int(min(y0, y1)), int(max(y0,y1)) 
        
        self.currentSelection = (x0,y0,x1,y1)        
        
        logging.debug("x0: {:d}, x1: {:d}, y0: {:d}, y1: {:d}".format(x0,x1,
                                                                      y0,y1))
                                                                      
        for selection_id in self._ids_selection:
            self.canvas.mpl_disconnect(selection_id)                                                              
        self.release(event)
        self.draw()
        self._selectionStart = None
        self._button_pressed = None
        self._ids_selection = []
        
        #fire event
        self.canvas.callbacks.process("selection_changed")
