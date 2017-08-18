import time
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
        self.plotScale = None
        self.plot = plot
        self.doingPlot = False
        self.axis = axis
        self.vb = viewbox
        # self.curve = self.plot.plot.plot()
        self.curve = pg.PlotDataItem()
        # self.curve.setData({'x': [], 'y': []}, pen=self.records[self.name]['pen'])
        self.vb.addItem(self.curve)
        self.lines = QGraphicsPathItem()
        # self.plot.plot.addItem(self.lines)
        self.fftTextLabels = []
        self.setVerticalMeanSubtraction(self.records[self.name]['verticalMeanSubtraction'])
        self.setLogScale(self.records[self.name]['logScale'])
        self.setHistogramBins()
        self.setDecimateScale()
        self.lineOn = False

    def signalValueAtX(self, xvalue):
        return stfunctions.takeClosestPosition(self.plotData[:,0],self.plotData,xvalue)[1][1]

    def setVerticalMeanSubtraction(self, subtractmean=False):
        self.verticalMeanSubtraction = subtractmean

    def setLogScale(self,logscale=False):
        pass
        # self.axis.setLogMode(logscale)
        # self.vb.enableAutoRange(axis= pg.ViewBox.YAxis, enable=True)

    def setHistogramBins(self,bins=10):
        self.numberBins = bins

    def setDecimateScale(self,scale=10000):
        self.decimateScale = scale

    ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
    def updateData(self, data, pen):
        if len(data) > 1:
            if len(data) > self.decimateScale:
                decimationfactor = int(np.floor(len(data)/self.decimateScale))
                data = data[::decimationfactor].copy()
            x,y = np.transpose(data)
            if self.records[self.name]['logScale']:
                y = np.log10(np.abs(y))
            if self.records[self.name]['verticalMeanSubtraction']:
                y = y - np.mean(y)
            self.curve.setData({'x': [], 'y': []}, stepMode=False, fillLevel=None, pen=pen)
            path = pg.arrayToQPath(x, y)
            self.lines.setPath(path)
            if not self.lineOn:
                self.lines.setPen(pg.mkPen(pen))
                self.vb.addItem(self.lines)
                self.lineOn = True

    ''' helper function to clear a curves points '''
    def clear(self):
        self.plot.plot.removeItem(self.lines)
        self.curve.clear()

    ''' Wrapper function which calls timefilter and updateData'''
    def update(self):
        self.plot.plot.removeItem(self.lines)
        if not self.plot.paused and not self.doingPlot:
            self.doingPlot = True
            if self.name in self.records and self.records[self.name]['ploton']:
                if self.plot.autoscroll:
                    self.currenttime = round(time.time(),2)
                else:
                    self.currenttime = self.plot.fixedtimepoint
                self.plotData = stfunctions.timeFilter(self.records[self.name]['data'], timescale=self.plot.globalPlotRange, offset=1)
                self.lasttime = time.time()
                if len(self.plotData) > 0:
                    self.updateData(self.plotData, self.records[self.name]['pen'])
            self.doingPlot = False
        self.plot.plotUpdated.emit()

class MultiLine(pg.QtGui.QGraphicsPathItem):
    def __init__(self, x, y, pen, log=False):
        """x and y are 1D arrays of shape (Nplots, Nsamples)"""
        self.path = pg.arrayToQPath(x, y)
        pg.QtGui.QGraphicsPathItem.__init__(self, self.path)
        # self.setPath(self.path)
        if log:
            self.setPen(pg.mkPen(pen,width=3))
        else:
            self.setPen(pg.mkPen(pen,width=2))
    def shape(self): # override because QGraphicsPathItem.shape is too expensive.
        return pg.QtGui.QGraphicsItem.shape(self)
    def boundingRect(self):
        return self.path.boundingRect()
