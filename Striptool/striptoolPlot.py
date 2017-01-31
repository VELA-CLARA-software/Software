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

''' Some nice colours for the plots '''
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
''' This just turns the colours into QColor specifications '''
Qtableau20 = [QColor(i,j,k) for (i,j,k) in tableau20]

''' This class is a PyQtGraph axis which modifies the data points from "seconds before the current time" into Hours:Mins:Secs format.
We only want to do this for linear plots, so it is turned off in the FFT and Histogram plots. Also, if we turn "autoscroll" off, the
time is relative to the moment we switched it off.
'''
class CAxisTime(pg.AxisItem):
    ## Formats axis label to human readable time.
    # @param[in] values List of \c time_t.
    # @param[in] scale Not used.
    # @param[in] spacing Not used.
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(CAxisTime, self).__init__(parent=parent, orientation=orientation, linkView=linkView)
        self.dateTicksOn = True
        self.autoscroll = True
        self.fixedtimepoint = time.time()

    def tickStrings(self, values, scale, spacing):
        if self.dateTicksOn:
            if self.autoscroll:
                reftime = time.time()
            else:
                reftime = self.fixedtimepoint
            strns = []
            for x in values:
                try:
                    strns.append(time.strftime("%H:%M:%S", time.localtime(reftime+x)))    # time_t --> time.struct_time
                except ValueError:  # Windows can't handle dates before 1970
                    strns.append('')
            return strns
        else:
            return values

''' Basic plotting class, providing Linear, Histogram and FFT plots in a PyQtGraph PlotWidget '''
class generalPlot(pg.PlotWidget):
    changePlotScale = pyqtSignal('PyQt_PyObject')
    plotUpdated = pyqtSignal()
    statusChanged = pyqtSignal(str)

    def __init__(self, stripplot, parent = None):
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
        self.legend = pg.LegendItem(size=(100,100))
        self.legend.setParentItem(None)
        self.globalPlotRange = [-10,0]
        self.currentPlotTime = time.time()
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.label = pg.LabelItem(justify='right')
        self.plotWidget.addItem(self.label)

    ''' This creates a PyQtGraph plot object (self.plot) and instantiates the bottom axis to be a CAxisTime axis '''
    def createPlot(self):
        self.date_axis = CAxisTime(orientation = 'bottom')
        self.plot = self.plotWidget.addPlot(row=0,col=0)
        self.plot.mouseOver = False
        self.plot.scene().installEventFilter(self)
        nontimeaxisItems = {'bottom': self.plot.axes['bottom']['item'], 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.plot.axes['right']['item']}
        axisItems = {'bottom': self.date_axis, 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.plot.axes['right']['item']}
        self.plot.axes = {}
        for k, pos in (('top', (1,1)), ('bottom', (3,1)), ('left', (2,0)), ('right', (2,2))):
            if k in axisItems:
                axis = axisItems[k]
                axis.linkToView(self.plot.vb)
                self.plot.axes[k] = {'item': axis, 'pos': pos}
                self.plot.layout.removeItem(self.plot.layout.itemAt(*pos))
                self.plot.layout.addItem(axis, *pos)
                axis.setZValue(-1000)
                axis.setFlag(axis.ItemNegativeZStacksBehindParent)
        self.plot.showGrid(x=True, y=True)
        ''' Here we create the two lines that form the crosshairs '''
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('r'))
        self.vLine.setZValue(1000)
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('r'))
        self.hLine.setZValue(1000)
        ''' this is a lina label for the vertical crosshair line. We modify the horizontal position in the signal functions '''
        self.hvLineText = pg.InfLineLabel(self.vLine, color='r', fill=(200,200,200,130))
        self.hvLineText.setZValue(1000)
        self.plot.addItem(self.vLine, ignoreBounds=True)
        self.plot.addItem(self.hLine, ignoreBounds=True)
        self.plot.addItem(self.hvLineText, ignoreBounds=True)
        ''' define some parameters and instantiate the crosshair signals. We change the crosshairs whenever the sigMouseMoved is triggered,
        whilst we must update the vertical axis if the plot autoscales, and also we must also update the horizontal axis if the time changes under the crosshairs'''
        self.vb = self.plot.vb
        self.mousePos = QtCore.QPointF(0.01, 0.01)
        self.proxyMouseMoved = pg.SignalProxy(self.plot.scene().sigMouseMoved, rateLimit=20, slot=self.mouseMoved)
        self.proxyAxisChanged = pg.SignalProxy(self.plot.vb.sigYRangeChanged, rateLimit=20, slot=self.axisChanged)
        self.proxyTimeChanged = pg.SignalProxy(self.plotUpdated, rateLimit=20, slot=self.timeAxisChanged)
        return self.plot

    ''' This defines a general eventFilter for the self.plot object that we use to update the crosshairs'''
    def eventFilter(self, object, event):
        ''' This just allows me to confirm which plot we are in, in case there are many '''
        if event.type() == QtCore.QEvent.GraphicsSceneMouseMove and self.plot.scene() == object:
            self.plot.mouseOver = True
        else:
            self.plot.mouseOver = False
        ''' this will copy the crosshairs location to the clipboard '''
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(self.statusTextClipboard)
                win32clipboard.CloseClipboard()
            except:
                pass
        return False

    ''' This is used to update the location of the crosshair lines as well as the accompanyng text'''
    def updateLines(self):
        try:
            self.vLine.setValue(self.mousePoint.x())
            self.hLine.setValue(self.mousePoint.y())
            self.hvLineText.setText(self.statusText)
            self.hvLineText.setPos(self.mousePoint.x(),self.mousePoint.y())
            vr = self.hLine.viewRect()
            if vr is not None:
                if vr.center().y() > 0:
                    self.hvLineText.anchors = [(-0.1, 1.0), (1.0, 1.0)]
                else:
                    self.hvLineText.anchors = [(-0.1, -0.1), (1.0, -0.1)]
            self.hvLineText.updateTextPos()
        except:
            pass

    ''' This is the event handler for a sigMouseMoved event for the viewbox '''
    def mouseMoved(self, evt):
        self.mousePos = evt[0]
        self.mousePoint = self.vb.mapSceneToView(self.mousePos)
        index = int(self.mousePoint.x())
        self.timeAxisChanged()
        self.updateLines()
        if self.plot.mouseOver:
            self.statusChanged.emit(self.statusText)

    ''' This is the event handler for if the vertical axis autoscales '''
    def axisChanged(self, evt):
        self.mousePoint = self.vb.mapSceneToView(self.mousePos)
        index = int(self.mousePoint.x())
        self.timeAxisChanged()
        self.updateLines()

    ''' This is the event handler for when the horizontal axis time changes during "autoscroll" '''
    def timeAxisChanged(self):
        if not self.paused:
            self.mousePoint = self.vb.mapSceneToView(self.mousePos)
            if self.linearPlot:
                if self.autoscroll:
                    reftime = time.time()
                else:
                    reftime = self.fixedtimepoint
                self.statusText = "{"+time.strftime("%H:%M:%S", time.localtime(reftime + self.mousePoint.x()))+", %0.3f}" % (self.mousePoint.y())
                self.statusTextClipboard = "{\""+time.strftime("%H:%M:%S", time.localtime(reftime + self.mousePoint.x()))+"\", %0.3f}" % (self.mousePoint.y())
            else:
                self.statusTextClipboard = self.statusText = "{%0.3f, %0.3f}" % (self.mousePoint.x(), self.mousePoint.y())
        self.updateLines()

    ''' Helper function to add a curve to the plot '''
    def addCurve(self, record, plot, name):
        curve = self.curve(record, plot, name)
        return curve

    ''' Sets the timescale of the plotting data '''
    def setPlotScale(self, timescale, padding=0.0):
        if self.linearPlot:
            self.plotRange = timescale
            self.globalPlotRange = list(timescale)
            self.plot.vb.setRange(xRange=self.globalPlotRange, padding=0)
        self.changePlotScale.emit(self.globalPlotRange)

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

    ''' This is the curve class which enables plotting on a plotting object. Making it a class eases control of the different options for multiple curves'''
    class curve(QObject):
        def __init__(self, record, plot, name):
            QObject.__init__(self)
            self.plotScale = None
            self.name = name
            self.plot = plot
            self.records = record
            # self.globalPlotRange = self.plot.globalPlotRange
            self.doingPlot = False
            self.curve = self.plot.plot.plot()

        def addCurve(self):
            return self.curve

        ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
        def updateData(self, data, pen):
            if len(data) > 1 and not self.plot.scatterPlot:
                if self.plot.histogramPlot:
                    x,y = np.transpose(data)
                    y,x = np.histogram(y, bins=50)
                else:
                    x,y = np.transpose(data)
                if self.plot.histogramPlot:
                    if(self.plot.stripplot.histogramCheckbox.isChecked()):
                        self.curve.setData({'x': x-np.mean(x), 'y': y}, pen=pen, stepMode=True, fillLevel=0)
                    else:
                        self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=True, fillLevel=0)
                elif self.plot.FFTPlot:
                    self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=False)
                    if(len(self.curve.yDisp) > 0):
                        indexes = peakutils.indexes(self.curve.yDisp, thres=0.75, min_dist=1)
                        for index in indexes:
                            pass# print self.curve.xDisp[index]
                    self.plot.updateSpectrumMode(True)
                else:
                    self.curve.setData(x=x, y=y, pen=pen, stepMode=False)

        ''' This filters the data based on the plotrange of the current viewbox. For small datasets this is ~pointless, but for moderately large datasets
        and bigger it makes a noticeable speed up, despite the functions built in to PyQtGraph'''
        def timeFilter(self, datain, timescale):
            if self.plot.autoscroll:
                currenttime = time.time()
            else:
                currenttime =  self.plot.currenttime
            tdata = np.array(list(map(lambda x: [x[0]-currenttime, x[1]], datain)))
            if len(tdata) > 0:
                times, data = zip(*tdata)
                if times[0] > self.plot.globalPlotRange[0] and times[-1] < self.plot.globalPlotRange[1]:
                    # print 'All Data!'
                    return tdata
                else:
                    if len(times) > 0:
                        idx = (np.array(times) > self.plot.globalPlotRange[0]) * (np.array(times) < self.plot.globalPlotRange[1])
                        timescut = list(compress(times, idx))
                        datacut = list(compress(data, idx))
                    finaldata = zip(*(timescut,datacut))
                    return finaldata
            else:
                return tdata

        ''' simple helper function to run the timeFilter function'''
        def filterRecord(self, data, timescale):
            return list(list(self.timeFilter(data, timescale)))

        ''' helper function to clear a curves points '''
        def clear(self):
            self.curve.clear()

        ''' Wrapper function which calls timefilter and updateData'''
        def update(self):
            if not self.plot.paused and not self.doingPlot:
                self.doingPlot = True
                if self.records[self.name]['ploton']:
                    # start = time.clock()
                    self.plotData = self.filterRecord(self.records[self.name]['data'],self.plot.globalPlotRange)
                    if len(self.plotData) > 100*self.plot.decimateScale:
                        decimationfactor = int(np.floor(len(self.plotData)/self.plot.decimateScale))
                        self.plotData = self.plotData[0::decimationfactor]
                        self.updateData(self.plotData, self.records[self.name]['pen'])
                    else:
                        self.updateData(self.plotData, self.records[self.name]['pen'])
                else:
                    self.clear()
                self.doingPlot = False
            self.plot.plotUpdated.emit()
