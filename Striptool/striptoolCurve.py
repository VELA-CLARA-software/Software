import time
import pyqtgraph as pg
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import striptoolFunctions as stfunctions
import numpy as np
import peakutils

''' This is the curve class which enables plotting on a plotting object. Making it a class eases control of the different options for multiple curves'''
class curve(QObject):
    def __init__(self, record, plot, name):
        QObject.__init__(self)
        self.records = record
        self.name = name
        self.plotScale = None
        self.plot = plot
        self.doingPlot = False
        self.curve = self.plot.plot.plot()
        self.curve.setData({'x': [], 'y': []}, pen=self.records[self.name]['pen'])
        self.lines = QGraphicsPathItem()
        self.plot.plot.addItem(self.lines)
        self.fftTextLabels = []
        self.setVerticalScale(self.records[self.name]['VerticalScale'])
        self.setVerticalOffset(self.records[self.name]['VerticalOffset'])
        self.setVerticalMeanSubtraction(self.records[self.name]['verticalMeanSubtraction'])
        self.setLogScale(self.records[self.name]['logscale'])
        self.setHistogramBins()
        self.setDecimateScale()
        # self.lineOn = False
        # self.records[self.name]['signal'].dataReady.connect(self.addToPath)

    def signalValueAtX(self, xvalue):
        return stfunctions.takeClosestPosition(self.plotData[:,0],self.plotData,xvalue)[1][1]

    def setVerticalScale(self,scale=1):
        self.VerticalScale = scale

    def setVerticalOffset(self,offset=0):
        self.VerticalOffset = offset

    def setVerticalMeanSubtraction(self, subtractmean=False):
        self.verticalMeanSubtraction =  subtractmean

    def setLogScale(self,logscale=False):
        self.logscale = logscale

    def setHistogramBins(self,bins=10):
        self.numberBins = bins

    def setDecimateScale(self,scale=10000):
        self.decimateScale = scale

    ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
    def updateData(self, data, pen):
        if len(data) > 1:
            x,y = np.transpose(data)
            if self.logscale:
                y = np.log10(np.abs(y))
            if not self.VerticalScale == 1 or not self.VerticalOffset == 0:
                y = (self.VerticalScale * y) + self.VerticalOffset
            if self.verticalMeanSubtraction:
                y = y - np.mean(y)
            if self.plot.stripplot.histogramPlot:
                # if self.lineOn:
                #     self.plot.plot.removeItem(self.lines)
                # self.curve.setFftMode(False)
                y2,x2 = np.histogram(y, bins=self.numberBins)
                self.curve.setData({'x': x2, 'y': y2}, pen=pen, stepMode=True, fillLevel=0, fillBrush=pen)
            elif self.plot.stripplot.FFTPlot:
                # if self.lineOn:
                #     self.plot.plot.removeItem(self.lines)
                x, y = self.curve._fourierTransform(x,y)
                # self.curve.setData({'x': [0,1], 'y': [0,1]}, pen=pen, stepMode=False, fillLevel=None)
                # self.curve.setFftMode(True)
                self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=False, fillLevel=None)
                if len(self.curve.yDisp) > 0:
                    indexes = peakutils.indexes(y, thres=0.5, min_dist=10)
                    if len(indexes) < 5:
                        for index in indexes:
                            fftTextlabel=pg.TextItem(html='<span style="color: '+pg.mkColor(pen).name()+';">'+str(round(x[index],2))+'</span>',anchor=(-0.7,1.2), angle=0)
                            fftTextlabel.setPos(x[index],y[index])
                            fftTextArrow=pg.ArrowItem(pos=(x[index],y[index]), angle=-45, pen=pen, brush=pg.mkBrush(pen))
                            self.fftTextLabels.append([fftTextlabel, fftTextArrow])
                            self.plot.plot.addItem(fftTextlabel)
                            self.plot.plot.addItem(fftTextArrow)
                # self.curve.setFftMode(True)
            else:
                data = np.transpose([x,y])
                self.curve.setData({'x': x, 'y': y}, stepMode=False, fillLevel=None)
            if self.plot.crosshairs:
                self.plot.signalValuesUnderCrosshairs.emit((self.name, self.signalValueAtX(self.plot.vLine.value()), np.mean(y), np.std(y)))
    #
    # def createPath(self, data):
    #     path = QPainterPath(QPointF(data[0][0],data[0][1]))
    #     for x,y in data:
    #         path.lineTo(x,y)
    #     return path
    #
    # def addToPath(self, data):
    #     if hasattr(self,'path'):
    #         self.path.lineTo(data[0],data[1])
    #     else:
    #         self.path = QPainterPath(QPoint(data[0],data[1]))

    ''' helper function to clear a curves points '''
    def clear(self):
        self.plot.plot.removeItem(self.lines)
        self.curve.clear()

    ''' Wrapper function which calls timefilter and updateData'''
    def update(self):
        # self.plot.plot.removeItem(self.lines)
        if len(self.fftTextLabels) > 0:
            for i in range(len(self.fftTextLabels)):
                for j in range(len(self.fftTextLabels[i])):
                    self.plot.plot.removeItem(self.fftTextLabels[i][j])
            self.fftTextLabels = []
        if not self.plot.paused and not self.doingPlot:
            self.doingPlot = True
            if self.name in self.records and self.records[self.name]['ploton']:
                if self.plot.autoscroll:
                    self.currenttime = round(time.time(),2)
                else:
                    self.currenttime = self.plot.fixedtimepoint
                self.plotData = stfunctions.timeFilter(self.records[self.name]['data'], timescale=self.plot.globalPlotRange, offset=1)
                # self.plotData = self.records[self.name]['data']
                # if hasattr(self,'lasttime'):
                    # print 'updaterate = ', 1.0/(time.time()-self.lasttime), '  [', len(self.plotData), ']'
                self.lasttime = time.time()
                if len(self.plotData) > 0:
                    self.updateData(self.plotData, self.records[self.name]['pen'])
                    # if self.plot.crosshairs:
                        # self.plot.signalValuesUnderCrosshairs.emit((self.name, self.signalValueAtX(self.plot.vLine.value()), np.mean(y), np.std(y)))
            self.doingPlot = False
        self.plot.plotUpdated.emit()

# class MultiLine(pg.QtGui.QGraphicsPathItem):
#     def __init__(self, x, y, pen, log=False):
#         """x and y are 1D arrays of shape (Nplots, Nsamples)"""
#         self.path = pg.arrayToQPath(x, y)
#         self.setPath(self.path)
#         if log:
#             self.setPen(pg.mkPen(pen,width=3))
#         else:
#             self.setPen(pg.mkPen(pen,width=2))
#     def shape(self): # override because QGraphicsPathItem.shape is too expensive.
#         return pg.QtGui.QGraphicsItem.shape(self)
#     def boundingRect(self):
#         return self.path.boundingRect()
