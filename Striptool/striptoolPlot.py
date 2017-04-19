import sys, time, os, datetime
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import colours as colours
import striptoolCurve as stcurve

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
            try:
                ticks = [time.strftime("%H:%M:%S", time.localtime(x)) for x in values]
            except:
                ticks = []
            return ticks
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
        self.autoscroll = True
        self.globalPlotRange = [time.time()-10,time.time()]
        self.currentPlotTime = round(time.time(),2)
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.crosshairs = crosshairs
        self.threads = {}
        self.workers = {}

    ''' This creates a PyQtGraph plot object (self.plot) and instantiates the bottom axis to be a CAxisTime axis '''
    def createPlot(self):
        self.date_axis = CAxisTime(orientation = 'bottom')
        self.plotUpdated.connect(self.date_axis.update)
        self.log_axis = pg.AxisItem('right')
        self.log_axis.setLogMode(True)
        self.plot = self.plotWidget.addPlot(row=0,col=0, autoDownsample=True, clipToView=True, antialias=False, downsampleMethod='peak',
        axisItems={'bottom':self.date_axis,'right': self.log_axis})
        self.plot.showAxis('right', True)
        self.plot.mouseOver = False
        self.proxyAxisChanged = pg.SignalProxy(self.plot.vb.sigXRangeChanged, rateLimit=20, slot=self.updatePlotScale)

        # nontimeaxisItems = {'bottom': self.plot.axes['bottom']['item'], 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.plot.axes['right']['item']}
        # axisItems = {'bottom': self.date_axis, 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.log_axis}
        # self.plot.axes = {}
        self.vb = self.plot.vb
        # for k, pos in (('top', (1,1)), ('bottom', (3,1)), ('left', (2,0)), ('right', (2,2))):
        #     if k in axisItems:
        #         axis = axisItems[k]
        #         axis.linkToView(self.vb)
        #         self.plot.axes[k] = {'item': axis, 'pos': pos}
        #         self.plot.layout.removeItem(self.plot.layout.itemAt(*pos))
        #         self.plot.layout.addItem(axis, *pos)
        #         axis.setZValue(-1000)
        #         axis.setFlag(axis.ItemNegativeZStacksBehindParent)
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
            self.vLine.setValue(time.time())
            self.hLine.setValue(0)
            self.plot.addItem(self.vLine, ignoreBounds=True)
            self.plot.addItem(self.hLine, ignoreBounds=True)
            self.plot.addItem(self.hvLineText, ignoreBounds=True)
            self.mousePoint =  QtCore.QPointF(time.time(), 0.0)
            self.updateAnchor()
            ''' define some parameters and instantiate the crosshair signals. We change the crosshairs whenever the sigMouseMoved is triggered,
            whilst we must update the vertical axis if the plot autoscales, and also we must also update the horizontal axis if the time changes under the crosshairs'''
            # self.proxyVLineMoved = pg.SignalProxy(self.vLine.sigPositionChanged, rateLimit=1, slot=self.updateAnchor)
            # self.proxyHLineMoved = pg.SignalProxy(self.hLine.sigPositionChanged, rateLimit=1, slot=self.updateAnchor)
            self.proxyMouseClicked = pg.SignalProxy(self.plot.scene().sigMouseClicked, rateLimit=1, slot=self.mouseClicked)
            # self.proxyTimeChanged = pg.SignalProxy(self.plotUpdated, rateLimit=5, slot=self.timeAxisChanged)
        return self.plot

    def moveCrosshairsWithViewBox(self,deltax):
        if self.crosshairs and deltax > 0.01:
            self.vLine.setValue(self.vLine.value()+deltax)
            self.hvLineText.setPos(self.vLine.value(),self.hLine.value())
            self.timeAxisChanged()

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
            self.statusTextX = time.strftime("%H:%M:%S", time.localtime(self.vLine.value()))
            self.statusTextY = "%0.3f" % (self.hLine.value())
            self.statusTextLogY = "%04.03e" % (np.power(10,self.hLine.value()))
            self.statusText = "&nbsp;"+self.statusTextX+", "+self.statusTextY+"("+self.statusTextLogY+")&nbsp;"
            self.statusTextClipboard = "{\""+self.statusTextX+"\", "+self.statusTextY+"}"
        else:
            self.statusTextX = "%0.3f" % (self.vLine.value())
            self.statusTextY = "%0.3f" % (self.hLine.value())
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
            vbPlotRange = self.vb.viewRange()[0]
            self.globalPlotRange = self.vb.viewRange()[0]
            self.plotRange = self.globalPlotRange

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
        self.curve = stcurve.curve(record, plot, name)
        plot.stripplot.doCurveUpdate.connect(self.updateCurve)

    # @QtCore.pyqtSlot()
    def updateCurve(self):
        self.curve.update()
