import sys, time, os, datetime, copy
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
from bisect import bisect_left, bisect_right
import peakutils
from itertools import compress
import colours as colours

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

class scatterPlotPlot(pg.PlotWidget):

    statusChanged = pyqtSignal(str)

    def __init__(self, scatterplot, color=0, parent = None):
        super(scatterPlotPlot, self).__init__(parent=parent)
        self.parent=parent
        self.scatterplot = scatterplot
        self.records = self.scatterplot.records
        self.doingPlot = False
        self.usePlotRange = True
        self.currentPlotTime = time.time()
        self.paused = False
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.plots = {}
        self.color = 0
        self.decimateScale = 1000000
        self.globalPlotRange = [-100000,0]
        self.paused = False
        self.selectionNameX = 0
        self.selectionNameY = 0
        self.scatterplot.scatterSelectionChanged.connect(self.setSelectionIndex)
        self.plot = self.plotWidget.addPlot(row=0, col=0) #, axisItems = {'bottom': self.date_axis}
        self.scatterPlot = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None), brush=pg.mkBrush(colours.Qtableau20[color]))
        self.plot.addItem(self.scatterPlot)
        self.scatterPlot.sigClicked.connect(self.printPoints)

    def printPoints(self,scatterPlot, points):
        point = points[0]
        text =  "{%0.3f, %0.3f}" % (point.pos()[0], point.pos()[1])
        self.statusChanged.emit(text)

    def setSelectionIndex(self, x, y):
        self.selectionNameX = str(x)
        self.selectionNameY = str(y)

    def setPlotRange(self, plotrange):
        self.globalPlotRange = plotrange

    def setPlotScale(self, xRange=None, yRange=None):
        self.plot.vb.setRange(xRange=xRange, yRange=yRange)

    def togglePause(self, value):
        self.paused = value

    def timeFilter(self, datain, timescale):
        tdata = np.array(list(map(lambda x: [x[0]-self.currenttime, x[1]], datain)))
        times, data = zip(*tdata)
        if (times[0] > self.globalPlotRange[0] and times[-1] < self.globalPlotRange[1]) or not len(times) > 0:
            # print 'All Data!'
            finaldata = zip(*(times,data))
        else:
            if len(times) > 0:
                idx = (np.array(times) > self.globalPlotRange[0]) * (np.array(times) < self.globalPlotRange[1])
                timescut = list(compress(times, idx))
                datacut = list(compress(data, idx))
                finaldata = zip(*(timescut,datacut))
        return finaldata

    def timeFilter2(self, datain, timescale):
        tdata = np.array(list(map(lambda x: [x[0]-self.currenttime, x[1]], datain)))
        times, data = zip(*tdata)
        if len(times) > 0:
            idx = (np.array(times) > self.globalPlotRange[0]) * (np.array(times) < self.globalPlotRange[1])
            timescut = list(compress(times, idx))
            datacut = list(compress(data, idx))
        finaldata = zip(*(timescut,datacut))
        return finaldata

    def filterRecord(self, data, timescale):
        return list(list(self.timeFilter(data, timescale)))

    def getPlotData(self, record):
        if self.scatterplot.stripPlotConnected:
            return record['curve'].plotData
        else:
            plotData = self.filterRecord(record['data'],self.globalPlotRange)
            x,y = np.transpose(plotData)
            if record['logscale']:
                y = np.log10(np.abs(y))
            meany = np.mean(y)
            if record['verticalMeanSubtraction']:
                y = y - meany
            plotData = zip(*[x,y])
            if len(plotData) > 100*self.decimateScale:
                decimationfactor = int(np.floor(len(plotData)/self.decimateScale))
                plotData = plotData[0::decimationfactor]
                return plotData
            else:
                return plotData

    def show(self):
        self.plotWidget.show()

    def createPlot(self, label1, label2, color):
        name = label1+' vs '+label2
        row = len(self.plots) / 3
        col = len(self.plots) % 3
        self.plot.setLabel('bottom',label1)
        self.plot.setLabel('left',label2)
        self.plot.setTitle(name)
        self.plot.showGrid(x=True, y=True)
        return [self.plot, self.scatterPlot]

    def removePlot(self, name):
        # self.plots[name][0].removeItem(self.plots[name][1])
        self.plotWidget.removeItem(self.plotWidget.getItem(0,0))

    def update(self):
        start = time.time()
        if not self.paused and not self.doingPlot:
            self.doingPlot  = True
            self.currenttime = time.time()
            scatteritems = []
            for name in [self.selectionNameX,self.selectionNameY]:
                if name in self.records and len(self.records[name]['data']) > 1:
                    scatteritems.append([name, self.getPlotData(self.records[name])])
            # print 'freq 1 = ', 1.0/(time.time()-start)
            if (len(scatteritems) > 1):
                name = scatteritems[0][0]+' vs '+scatteritems[1][0]
                self.createPlot(scatteritems[0][0], scatteritems[1][0], self.color)
                data1 = scatteritems[0][1]
                data2 = scatteritems[1][1]
                if len(data1) > 1 and len(data2) > 1:
                    signalDelayTime1 =  self.records[scatteritems[0][0]]['timer']
                    signalDelayTime2 =  self.records[scatteritems[1][0]]['timer']
                    if list(data1[0])[0] < list(data2[0])[0]:
                        # print 'less than'
                        ans = takeClosestPosition(zip(*data1)[0], data1, data2[0][0])
                        starttime = ans[1]
                        startpos1 = ans[0]
                        startpos2 = 0
                    elif list(data1[0])[0] > list(data2[0])[0]:
                        # print 'more than', data1[0],' > ', data2[0]
                        ans = takeClosestPosition(zip(*data2)[0], data2, data1[0][0])
                        starttime = ans[1]
                        startpos1 = 0
                        startpos2 = ans[0]
                    else:
                        # print 'equal'
                        startpos1 = startpos2 = 0
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
                    if len(data1) > 1 and len(data2) > 1:
                        x1,x = zip(*data1)
                        x2,y = zip(*data2)
                        self.scatterPlot.setData(x=x, y=y)
            self.doingPlot = False
            # if not self.paused and time.time() > start:
            #     print 'freq = ', 1.0/(time.time()-start)
