import sys, time, os, datetime
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
from bisect import bisect_left, bisect_right
import peakutils
from itertools import compress
import win32clipboard
import itertools
import colours as colours

def takeClosestPosition(xvalues, myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    if len(myList) < 1 or myNumber < xvalues[0]:
        return [0,(0,0)]
    pos = bisect_left(xvalues, myNumber)
    if pos == 0:
        return [0,myList[0]]
    if pos == len(myList):
        return [-1,myList[-1]]
    before = myList[pos-1]
    after = myList[pos]
    if abs(after[0] - myNumber) < abs(myNumber - before[0]):
       return [pos,after]
    else:
       return [pos-1,before]

''' This class is a PyQtGraph axis which modifies the data points from "seconds before the current time" into Hours:Mins:Secs format.
We only want to do this for linear plots, so it is turned off in the FFT and Histogram plots. Also, if we turn "autoscroll" off, the
time is relative to the moment we switched it off.
'''
class CAxisTime(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(CAxisTime, self).__init__(parent=parent, orientation=orientation, linkView=linkView)
        self.dateTicksOn = True
        self.autoscroll = True
        self.fixedtimepoint = round(time.time(),2)

    def tickStrings(self, values, scale, spacing):
        if self.dateTicksOn:
            if self.autoscroll:
                reftime = round(time.time(),2)
            else:
                reftime = self.fixedtimepoint
            return [time.strftime("%H:%M:%S", time.localtime(reftime+x)) for x in values]
        else:
            places = max(0, np.ceil(-np.log10(spacing*scale)))
            strings = []
            for v in values:
                vs = v * scale
                if abs(vs) < .001 or abs(vs) >= 10000:
                    vstr = "%g" % vs
                else:
                    vstr = ("%%0.%df" % places) % vs
                strings.append(vstr)
            return strings

''' Basic plotting class, providing Linear, Histogram and FFT plots in a PyQtGraph PlotWidget '''
class generalPlot(pg.PlotWidget):
    plotUpdated = pyqtSignal()
    signalValuesUnderCrosshairs = pyqtSignal('PyQt_PyObject')


    def __init__(self, stripplot, crosshairs=True, parent = None):
        super(generalPlot, self).__init__(parent=parent)
        self.parent=parent
        self.stripplot = stripplot
        self.paused = True
        self.linearPlot = True
        self.histogramPlot = False
        self.FFTPlot = False
        self.scatterPlot = False
        self.doingPlot = False
        self.usePlotRange = True
        self.autoscroll = True
        self.decimateScale = 5000
        self.globalPlotRange = [-10,0]
        self.currentPlotTime = round(time.time(),2)
        self.plotWidget = pg.GraphicsLayoutWidget()
        # self.label = pg.LabelItem(justify='right')
        # self.plotWidget.addItem(self.label)
        self.numberBins = 50
        self.crosshairs = crosshairs
        self.threads = {}
        self.workers = {}

    ''' This creates a PyQtGraph plot object (self.plot) and instantiates the bottom axis to be a CAxisTime axis '''
    def createPlot(self):
        self.plot = self.plotWidget.addPlot(row=0,col=0, autoDownsample=True, clipToView=True)
        self.date_axis = CAxisTime(orientation = 'bottom', parent=self.plot)
        self.plotUpdated.connect(self.date_axis.update)
        self.log_axis = pg.AxisItem('right', parent=self.plot)
        self.log_axis.setLogMode(True)
        self.plot.mouseOver = False

        nontimeaxisItems = {'bottom': self.plot.axes['bottom']['item'], 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.plot.axes['right']['item']}
        axisItems = {'bottom': self.date_axis, 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.log_axis}
        self.plot.axes = {}
        self.vb = self.plot.vb
        for k, pos in (('top', (1,1)), ('bottom', (3,1)), ('left', (2,0)), ('right', (2,2))):
            if k in axisItems:
                axis = axisItems[k]
                axis.linkToView(self.vb)
                self.plot.axes[k] = {'item': axis, 'pos': pos}
                self.plot.layout.removeItem(self.plot.layout.itemAt(*pos))
                self.plot.layout.addItem(axis, *pos)
                axis.setZValue(-1000)
                axis.setFlag(axis.ItemNegativeZStacksBehindParent)
        self.plot.showGrid(x=True, y=True)

        if self.crosshairs:
            ''' Here we create the two lines that form the crosshairs '''
            self.vLine = pg.InfiniteLine(angle=90, movable=True, pen=pg.mkPen('r'))
            self.vLine.setZValue(1000)
            self.hLine = pg.InfiniteLine(angle=0, movable=True, pen=pg.mkPen('r'))
            self.hLine.setZValue(1000)
            ''' this is a line label for the vertical crosshair line. We modify the horizontal position in the signal functions '''
            self.hvLineText = pg.TextItem() #pg.InfLineLabel(self.vLine, color='r', fill=(200,200,200,130))
            self.hvLineText.setZValue(1000)
            self.crosshairsadded = True
            self.vLine.setValue(0)
            self.hLine.setValue(0)
            self.plot.addItem(self.vLine, ignoreBounds=True)
            self.plot.addItem(self.hLine, ignoreBounds=True)
            self.plot.addItem(self.hvLineText, ignoreBounds=True)
            self.mousePoint =  QtCore.QPointF(0.0, 0.0)
            self.updateAnchor()
            ''' define some parameters and instantiate the crosshair signals. We change the crosshairs whenever the sigMouseMoved is triggered,
            whilst we must update the vertical axis if the plot autoscales, and also we must also update the horizontal axis if the time changes under the crosshairs'''
            self.proxyVLineMoved = pg.SignalProxy(self.vLine.sigPositionChanged, rateLimit=10, slot=self.updateAnchor)
            self.proxyHLineMoved = pg.SignalProxy(self.hLine.sigPositionChanged, rateLimit=10, slot=self.updateAnchor)
            self.proxyMouseClicked = pg.SignalProxy(self.plot.scene().sigMouseClicked, rateLimit=1, slot=self.mouseClicked)
            self.proxyTimeChanged = pg.SignalProxy(self.plotUpdated, rateLimit=5, slot=self.timeAxisChanged)
        return self.plot

    ''' This is used to update the location of the crosshair lines as well as the accompanyng text'''
    def updateAnchor(self, mousepoint=True, *args, **kwargs):
        if mousepoint:
            self.mousePoint = QtCore.QPointF(self.vLine.value(),self.hLine.value())
        self.timeAxisChanged()
        self.hvLineText.setPos(self.vLine.value(),self.hLine.value())
        self.hvr = self.hLine.viewRect()
        self.vvr = self.vLine.viewRect()
        if self.hvr is not None:
            if self.hvr.center().y() > 0:
                if self.vvr.center().y() > 0:
                    self.hvLineText.setAnchor((1, 1.0))
                else:
                    self.hvLineText.setAnchor((0, 1.0))
            else:
                if self.vvr.center().y() > 0:
                    self.hvLineText.setAnchor((1, 0))
                else:
                    self.hvLineText.setAnchor((-0.1, 0))

    ''' This is the event handler for a sigMouseMoved event for the viewbox '''
    def mouseClicked(self, evt):
        mouseClick = evt[0]
        mouseClick.accept()
        self.mousePos = mouseClick.scenePos()
        self.mousePoint = self.vb.mapSceneToView(self.mousePos)
        self.vLine.setValue(self.mousePoint.x())
        self.hLine.setValue(self.mousePoint.y())
        self.updateAnchor(mousepoint=False)

    ''' This is the event handler for when the horizontal axis time changes during "autoscroll" '''
    def timeAxisChanged(self):
        if self.linearPlot:
            if self.autoscroll:
                reftime = round(time.time(),2)
            else:
                reftime = self.fixedtimepoint
            self.statusTextX = time.strftime("%H:%M:%S", time.localtime(reftime + self.mousePoint.x()))
            self.statusTextY = "%0.3f" % (self.mousePoint.y())
            self.statusTextLogY = "%04.03e" % (np.power(10,self.mousePoint.y()))
            self.statusText = "&nbsp;"+self.statusTextX+", "+self.statusTextY+"("+self.statusTextLogY+")&nbsp;"
            self.statusTextClipboard = "{\""+self.statusTextX+"\", "+self.statusTextY+"}"
        else:
            self.statusTextX = "%0.3f" % (self.mousePoint.x())
            self.statusTextY = "%0.3f" % (self.mousePoint.y())
            self.statusTextClipboard = self.statusText = "{"+self.statusTextX+", "+self.statusTextY+"}"
        self.hvLineText.setHtml('<span style="color: black; background-color: rgba(255, 0, 0, 100); opacity: 0.1;">'+self.statusText+'</span>')

    ''' Sets the timescale of the plotting data '''
    def setPlotScale(self, timescale, padding=0.0):
        self.plotRange = timescale
        self.globalPlotRange = list(timescale)
        if self.linearPlot:
            self.plot.vb.setRange(xRange=self.globalPlotRange, padding=0)

    ''' Function to update timescale if the viewbox range changes - i.e. via mouse interaction or autoscale'''
    def updatePlotScale(self, padding=0.0):
        if self.linearPlot:
            vbPlotRange = self.plot.vb.viewRange()[0]
            if vbPlotRange != [0,1]:
                self.globalPlotRange = self.plot.vb.viewRange()[0]
            self.plotRange = self.globalPlotRange
        self.changePlotScale.emit(self.globalPlotRange)

    ''' Wrapper '''
    def show(self):
        self.plotWidget.show()

    ''' Wrapper '''
    def togglePause(self, value):
        self.paused = value

    ''' Toggles autoscroll on the plot '''
    def toggleAutoScroll(self, value):
        self.autoscroll = value
        if not value:
            self.currenttime = self.currentPlotTime
            self.date_axis.fixedtimepoint = self.currentPlotTime
            self.fixedtimepoint = self.currentPlotTime

    ''' Helper function to add a curve to the plot '''
    def addCurve(self, record, name):
        self.threads[name] = QtCore.QThread(self.stripplot)
        self.workers[name] = curveRecordWorker(record, self, name)
        self.workers[name].moveToThread(self.threads[name])
        self.threads[name].start()
        return self.workers[name].curve

    def toggleLegend(self, showLegend):
        if showLegend:
            self.legend = self.plot.addLegend()
            for name in self.workers:
                self.legend.addItem(self.workers[name].curve.curve, name)
        else:
            self.plot.vb.removeItem(self.legend)
            self.legend.items = []

class curveRecordWorker(QtCore.QObject):
    def __init__(self, record, plot, name):
        QtCore.QObject.__init__(self)
        self.curve = curve(record, plot, name)
        plot.stripplot.doCurveUpdate.connect(self.updateCurve)

    # @QtCore.pyqtSlot()
    def updateCurve(self):
        self.curve.update()

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
        self.lines = self.MultiLine(np.array([[0]]),np.array([[0]]),pen='w')
        self.fftTextLabels = []

    def signalValueAtX(self, xvalue):
        return takeClosestPosition(self.plotData[:,0],self.plotData,xvalue)[1][1]

    def addCurve(self):
        return self.curve

    ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
    def updateData(self, data, pen):
        self.VerticalScale = self.records[self.name]['VerticalScale']
        self.VerticalOffset = self.records[self.name]['VerticalOffset']
        self.verticalMeanSubtraction = self.records[self.name]['verticalMeanSubtraction']
        self.logscale = self.records[self.name]['logscale']
        if len(data) > 1 and not self.plot.scatterPlot:
            x,y = np.transpose(data)
            if not self.VerticalScale == 1 or not self.VerticalOffset == 0:
                y = (self.VerticalScale * y) + self.VerticalOffset
            if self.verticalMeanSubtraction or self.plot.stripplot.subtractMean:
                y = y - np.mean(y)
            if self.logscale:
                y = np.log10(np.abs(y))
            if self.plot.histogramPlot:
                y2,x2 = np.histogram(y, bins=self.plot.numberBins)
                self.curve.setData({'x': x2, 'y': y2}, pen=pen, stepMode=True, fillLevel=0, fillBrush=pen)
            elif self.plot.FFTPlot:
                self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=False, fillLevel=None)
                if(len(self.curve.yDisp) > 0):
                    indexes = peakutils.indexes(self.curve.yDisp, thres=0.75, min_dist=20)
                    if len(indexes) < 5:
                        for index in indexes:
                            fftTextlabel=pg.TextItem(html='<span style="color: '+pg.mkColor(pen).name()+';">'+str(round(self.curve.xDisp[index],2))+'</span>',anchor=(-0.7,1.2), angle=0)
                            fftTextlabel.setPos(self.curve.xDisp[index],self.curve.yDisp[index])
                            fftTextArrow=pg.ArrowItem(pos=(self.curve.xDisp[index],self.curve.yDisp[index]), angle=-45, pen=pen, brush=pg.mkBrush(pen))
                            self.fftTextLabels.append([fftTextlabel, fftTextArrow])
                            self.plot.plot.addItem(fftTextlabel)
                            self.plot.plot.addItem(fftTextArrow)
                self.plot.updateSpectrumMode(True)
            else:
                self.curve.setData({'x': [], 'y': []}, stepMode=False, fillLevel=None, pen=self.records[self.name]['pen'])
                if len(x) > self.plot.decimateScale:
                    decimationfactor = int(np.floor(len(x)/self.plot.decimateScale))
                    self.lines = self.MultiLine(x[::decimationfactor],y[::decimationfactor],pen=pen, log=self.logscale)
                else:
                    self.lines = self.MultiLine(x, y, pen=pen, log=self.logscale)
                self.plot.plot.addItem(self.lines)

    ''' This filters the data based on the plotrange of the current viewbox. For small datasets this is ~pointless, but for moderately large datasets
    and bigger it makes a noticeable speed up, despite the functions built in to PyQtGraph'''
    def timeFilter(self, datain, timescale=None):
        if self.plot.autoscroll:
            self.currenttime = round(time.time(),2)
        else:
            self.currenttime = self.plot.fixedtimepoint
        if len(datain) > 0:
            if (datain[0][0] > (self.currenttime+self.plot.globalPlotRange[0]) and datain[-1][0] <=  (self.currenttime+self.plot.globalPlotRange[1])):
                return datain
            else:
                if datain[-1][0] <=  (self.currenttime+self.plot.globalPlotRange[1]):
                    datain = datain[bisect_left(datain[:,0], self.currenttime+self.plot.globalPlotRange[0])-1:-1]
                else:
                    if datain[0][0] >= (self.currenttime+self.plot.globalPlotRange[0]):
                        datain = datain[0:bisect_left(datain[:,0], self.currenttime+self.plot.globalPlotRange[1])+1]
                    else:
                        datain = datain[bisect_left(datain[:,0], self.currenttime+self.plot.globalPlotRange[0])-1:bisect_left(datain[:,0], self.currenttime+self.plot.globalPlotRange[1])+1]
                return datain
        else:
            return datain

    ''' helper function to clear a curves points '''
    def clear(self):
        self.plot.plot.removeItem(self.lines)
        self.curve.clear()

    ''' Wrapper function which calls timefilter and updateData'''
    def update(self):
        self.plot.plot.removeItem(self.lines)
        if len(self.fftTextLabels) > 0:
            for i in range(len(self.fftTextLabels)):
                for j in range(len(self.fftTextLabels[i])):
                    self.plot.plot.removeItem(self.fftTextLabels[i][j])
            self.fftTextLabels = []
        if not self.plot.paused and not self.doingPlot:
            self.doingPlot = True
            if self.name in self.records and self.records[self.name]['ploton']:
                self.plotData = self.timeFilter(self.records[self.name]['data'], self.plot.globalPlotRange)
                if len(self.plotData) > 0:
                    x,y = np.transpose(self.plotData)
                    x = x - self.currenttime
                    self.plotData = np.transpose((x,y))
                    self.updateData(self.plotData, self.records[self.name]['pen'])
                    if self.plot.crosshairs:
                        self.plot.signalValuesUnderCrosshairs.emit((self.name, self.signalValueAtX(self.plot.vLine.value()), np.mean(y), np.std(y)))
            self.doingPlot = False
        self.plot.plotUpdated.emit()

    class MultiLine(pg.QtGui.QGraphicsPathItem):
        def __init__(self, x, y, pen, log=False):
            """x and y are 1D arrays of shape (Nplots, Nsamples)"""
            self.path = pg.arrayToQPath(x, y)
            pg.QtGui.QGraphicsPathItem.__init__(self, self.path)
            if log:
                self.setPen(pg.mkPen(pen,width=3))
            else:
                self.setPen(pg.mkPen(pen,width=2))
        def shape(self): # override because QGraphicsPathItem.shape is too expensive.
            return pg.QtGui.QGraphicsItem.shape(self)
        def boundingRect(self):
            return self.path.boundingRect()
