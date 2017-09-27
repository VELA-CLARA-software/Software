import time, math
import pyqtgraph as pg
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import striptoolFunctions as stfunctions
import numpy as np
import peakutils

''' This is the curve class which enables plotting on a plotting object. Making it a class eases control of the different options for multiple curves'''
class curve(QObject):
    def __init__(self, record, plot, name, axis, viewbox):
        QObject.__init__(self)
        self.records = record
        self.name = name
        self.plot = plot
        self.axis = axis
        self.vb = viewbox
        self.curve = pg.PlotDataItem()
        self.vb.addItem(self.curve)
        self.scene = self.vb.scene()
        self.lines = MultiLine()
        self.lineOn = False
        self.timeOffset = 0

    def updateTimeOffset(self,time):
        self.timeOffset += time
        if hasattr(self,'path'):
            self.lines.setNewPath(self.path)
            if not self.lineOn:
                self.lines.setPen(pg.mkPen(self.records[self.name]['pen']))
                self.scenePath = self.vb.addItem(self.lines)
                self.lineOn = True

    def setDecimateScale(self,scale=10000):
        self.decimateScale = scale

    ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
    def updateData(self, data):
        val = math.log(data[1],10) if self.records[self.name]['logScale'] else data[1]
        newpoint = QPointF(0, val)
        if not hasattr(self,'path'):
            self.lastplottime = self.starttime = round(time.time(),2)
            self.path = QPainterPath(newpoint)
        newtime = data[0]
        self.path.lineTo(newpoint)
        self.path.translate(-1*(newtime-self.lastplottime),0)
        self.lastplottime = newtime

    ''' helper function to clear a curves points '''
    def clear(self):
        self.plot.plot.removeItem(self.lines)
        self.curve.clear()

class MultiLine(pg.QtGui.QGraphicsPathItem):
    def __init__(self, log=False):
        """x and y are 1D arrays of shape (Nplots, Nsamples)"""
        super(MultiLine, self).__init__()

    def setNewPath(self, path):
        self.path = path
        self.setPath(path)

    def shape(self): # override because QGraphicsPathItem.shape is too expensive.
        return pg.QtGui.QGraphicsItem.shape(self)
    def boundingRect(self):
        return self.path.boundingRect()
