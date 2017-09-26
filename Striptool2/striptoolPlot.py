import sys, time, os, datetime, math
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
class HAxisTime(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(HAxisTime, self).__init__(parent=parent, orientation=orientation, linkView=linkView)
        self.dateTicksOn = True
        self.autoscroll = True

    def updateTimeOffset(self,time):
        self.timeOffset = time
        self.resizeEvent()
        self.update()

    def tickStrings(self, values, scale, spacing):
        if not hasattr(self, 'fixedtimepoint'):
            self.fixedtimepoint = round(time.time(),2)
        if self.dateTicksOn:
            if self.autoscroll:
                reftime = round(time.time(),2)
            else:
                reftime = self.fixedtimepoint
            try:
                ticks = [time.strftime("%H:%M:%S", time.localtime(round(time.time(),2)+x)) for x in values]
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

class VAxis(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(VAxis, self).__init__(parent=parent, orientation=orientation, linkView=linkView)

    def logTickStrings(self, values, scale, spacing):
        return ["%0.1g"%abs(x) for x in 10 ** np.array(values).astype(float)]

''' Basic plotting class, providing Linear, Histogram and FFT plots in a PyQtGraph PlotWidget '''
class generalPlot(pg.PlotWidget):
    plotUpdated = pyqtSignal()

    def __init__(self, stripplot, crosshairs=True, parent = None):
        super(generalPlot, self).__init__(parent=parent)
        self.parent=parent
        self.stripplot = stripplot
        self.paused = False
        self.linearPlot = True
        self.autoscroll = True
        self.globalPlotRange = [0-10,0+0.5]
        self.currentPlotTime = round(time.time(),2)
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.crosshairs = crosshairs
        self.threads = {}
        self.workers = {}
        self.viewboxes = {}

    ''' This creates a PyQtGraph plot object (self.plot) and instantiates the bottom axis to be a CAxisTime axis '''
    def createPlot(self):
        self.date_axis = HAxisTime(orientation = 'bottom')
        # self.plotUpdated.connect(self.date_axis.update)
        self.stripplot.timeChangeSignal.connect(self.date_axis.updateTimeOffset)
        self.leftaxis = pg.AxisItem("left")
        self.plot = self.plotWidget.addPlot(row=0,col=50, autoDownsample=True, clipToView=True, antialias=False, downsampleMethod='peak')#, axisItems={'bottom':self.date_axis})
        self.plot.vb.setMouseEnabled(y=False)
        self.plot.disableAutoRange(False)
        self.plot.setRange(xRange=[-0.5,1.5])
        self.plot.showAxis('left', False)
        self.plot.mouseOver = False
        self.plot.showGrid(x=True, y=True)
        return self.plot

    ''' Sets the timescale of the plotting data '''
    def setPlotScale(self, timescale, padding=0.0):
        self.plotRange = timescale
        self.globalPlotRange = list(timescale)
        self.plot.vb.setRange(xRange=self.globalPlotRange, padding=0)

    ''' Function to update timescale if the viewbox range changes - i.e. via mouse interaction or autoscale'''
    def updatePlotScale(self, padding=0.0):
        vbPlotRange = self.vb.viewRange()[0]
        self.globalPlotRange = self.vb.viewRange()[0]
        self.plotRange = self.globalPlotRange

    ''' Wrapper '''
    def show(self):
        self.plotWidget.show()

    ''' Toggles autoscroll on the plot '''
    def toggleAutoScroll(self, value):
        self.autoscroll = value
        if not value:
            self.currenttime = self.currentPlotTime
            # self.date_axis.fixedtimepoint = self.currentPlotTime
            self.fixedtimepoint = self.currentPlotTime

    ''' Helper function to add a curve to the plot '''
    def addCurve(self, record, name):
        # Create New Axis
        axis = pg.AxisItem("left")
        viewbox = pg.ViewBox()
        axis.linkToView(viewbox)
        if record[name]['logScale']:
            axis.setLogMode(True)
        if not record[name]['verticalRange'] == False:
            if record[name]['logScale']:
                logrange = [math.log(x,10) for x in record[name]['verticalRange']]
                print 'logrange = ', logrange
                viewbox.setRange(yRange=logrange,disableAutoRange=True)
            else:
                viewbox.setRange(yRange=record[name]['verticalRange'],disableAutoRange=True)
        labelStyle = {'color': '#'+pg.colorStr(pg.mkColor(record[name]['pen']))[0:-2]}
        axis.setLabel(name,**labelStyle)
        viewbox.setXLink(self.plot.vb)
        self.viewboxes[name] = {'viewbox': viewbox, 'axis': axis}
        self.plotWidget.ci.addItem(axis, row = 0, col = len(self.viewboxes)+1,  rowspan=1, colspan=1)
        self.plotWidget.ci.addItem(viewbox, row=0, col=50)
        self.threads[name] = QtCore.QThread(self.stripplot)
        self.workers[name] = curveRecordWorker(record, self, name, axis, viewbox)
        self.workers[name].moveToThread(self.threads[name])
        self.threads[name].start()
        return self.workers[name].curve

    def toggleLogMode(self, record, name):
        vb = self.viewboxes[name]['viewbox']
        verticalRange = vb.viewRange()[1]
        if record[name]['logScale']:
            if verticalRange[0] < 0:
                verticalRange[0] = 1e-12
            logrange = [math.log(x,10) for x in verticalRange]
            vb.setRange(yRange=logrange,disableAutoRange=True)
        else:
            normalrange = [10.0**x for x in verticalRange]
            vb.setRange(yRange=normalrange,disableAutoRange=True)


class curveRecordWorker(QtCore.QObject):
    def __init__(self, record, plot, name, axis, viewbox):
        QtCore.QObject.__init__(self)
        self.vb = viewbox
        self.axis = axis
        self.curve = stcurve.curve(record, plot, name, self.axis, self.vb)
        # plot.stripplot.doCurveUpdate.connect(self.curve.update)
        record[name]['worker'].recordLatestValueSignal.connect(self.curve.updateData)
        plot.stripplot.timeChangeSignal.connect(self.curve.updateTimeOffset)
