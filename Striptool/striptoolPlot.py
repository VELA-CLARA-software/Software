import sys, time, os, datetime
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
from bisect import bisect_left, bisect_right
import peakutils

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

Qtableau20 = [QColor(i,j,k) for (i,j,k) in tableau20]

def takeClosestPosition(xvalues, myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
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

class generalPlot(pg.PlotWidget):
    changePlotScale = pyqtSignal('PyQt_PyObject')

    def __init__(self, stripplot, parent = None):
        super(generalPlot, self).__init__(parent=parent)
        self.parent=parent
        self.stripplot = stripplot
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

    def createPlot(self):
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.date_axis = CAxisTime(orientation = 'bottom')
        self.plot = self.plotWidget.addPlot() #, axisItems = {'bottom': self.date_axis}
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
        return self.plot

    def addCurve(self, record, plot, name):
        curve = self.curve(record, plot, name)
        return curve

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
            self.addCurve()

        def addCurve(self):
            return self.curve

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
                    self.plot.updateSpectrumMode(True)
                else:
                    self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=False)

        def timeFilter(self, datain, timescale):
            if self.plot.autoscroll:
                currenttime = time.time()
            else:
                currenttime =  self.plot.currenttime
            data = map(lambda x: [x[0]-currenttime, x[1]], datain)
            def func1(values):
                for x in reversed(values):
                    if x[0] > (self.plot.globalPlotRange[0]) :
                        yield x
                    else:
                        break
            newlist = list(func1(data))
            for x in reversed(newlist):
                if x[0] < (self.plot.globalPlotRange[1]):
                    yield x
                else:
                    break

        def filterRecord(self, data, timescale):
            return list(list(self.timeFilter(data, timescale)))

        def clear(self):
            self.curve.clear()

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
    def setPlotScale(self, timescale, padding=0.0):
        if self.linearPlot:
            self.plotRange = timescale
            self.globalPlotRange = list(timescale)
            self.plot.vb.setRange(xRange=self.globalPlotRange, padding=0)

    def updatePlotScale(self, padding=0.0):
        if self.linearPlot:
            vbPlotRange = self.plot.vb.viewRange()[0]
            if vbPlotRange != [0,1]:
                self.globalPlotRange = self.plot.vb.viewRange()[0]
            self.plotRange = self.globalPlotRange

    def show(self):
        self.plotWidget.show()

    def togglePause(self, value):
        self.paused = value

    def toggleAutoScroll(self, value):
        self.autoscroll = value
        if not value:
            self.currenttime = self.currentPlotTime
            self.date_axis.fixedtimepoint = self.currentPlotTime

    def updateScatterPlot(self):
        if self.scatterPlot and not self.doingPlot:
            self.doingPlot = True
            # self.legend.setParentItem(self.plot)
            # self.legend.items = []
            scatteritemnames=[]
            scatteritems=[]
            color=0
            for name in self.records:
                if self.records[name]['ploton']:
                    scatteritemnames.append(name)
            self.plot.clear()
            start = time.clock()
            for i in range(len(scatteritemnames)):
                for j in range(i+1, len(scatteritemnames)):
                    data1 = self.records[scatteritemnames[i]]['curve'].plotData
                    data2 = self.records[scatteritemnames[j]]['curve'].plotData
                    signalDelayTime1 = self.records[scatteritemnames[i]]['timer']
                    signalDelayTime2 = self.records[scatteritemnames[j]]['timer']
                    if data1[0] < data2[0]:
                        ans = takeClosestPosition(zip(*data1)[0], data1, data2[0][0])
                        starttime = ans[1]
                        startpos1 = ans[0]
                        startpos2 = 0
                    else:
                        ans = takeClosestPosition(zip(*data2)[0], data2, data1[0][0])
                        starttime = ans[1]
                        startpos1 = 0
                        startpos2 = ans[0]
                    data1 = data1[startpos1:-1]
                    data2 = data2[startpos2:-1]
                    if len(data1) > len(data2):
                        data1 = data1[0:len(data2)]
                    elif len(data2) > len(data1):
                        data2 = data2[0:len(data1)]
                    # if signalDelayTime1 != signalDelayTime2:
                    # if signalDelayTime1 > signalDelayTime2:
                    #     tmpdata1 = zip(*data1)[0]
                    #     data1 = [takeClosestPosition(tmpdata1, data1, timeval[0])[1] for timeval in data2]
                    # else:
                    #     tmpdata2 = zip(*data2)[0]
                    #     data2 = [takeClosestPosition(tmpdata2, data2, timeval[0])[1] for timeval in data1]
                    x1,x = zip(*data1)
                    x2,y = zip(*data2)
                    plotname = str(i+1)+" vs "+str(j+1)
                    s1 = pg.ScatterPlotItem(x=x, y=y, size=2, pen=pg.mkPen(None), brush=pg.mkBrush(Qtableau20[color]))
                    # self.legend.addItem(s1, plotname)
                    color += 1
                    self.plot.addItem(s1)
            self.doingPlot = False
