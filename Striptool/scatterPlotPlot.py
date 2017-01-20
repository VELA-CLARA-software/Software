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

class scatterPlotPlot(pg.PlotWidget):
    changePlotScale = pyqtSignal('PyQt_PyObject')

    def __init__(self, stripplot, parent = None):
        super(scatterPlotPlot, self).__init__(parent=parent)
        self.parent=parent
        self.stripplot = stripplot
        self.records = self.stripplot.records
        self.doingPlot = False
        self.usePlotRange = True
        self.globalPlotRange = [-1000,0]
        self.currentPlotTime = time.time()
        self.paused = False

    def createPlot(self):
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.plot = self.plotWidget.addPlot() #, axisItems = {'bottom': self.date_axis}
        self.plot.showGrid(x=True, y=True)
        self.legend = self.plot.addLegend()
        print self.legend
        return self.plot

    def timeFilter(self, datain, timescale):
        currenttime = time.time()
        data = map(lambda x: [x[0]-currenttime, x[1]], datain)
        def func1(values):
            for x in reversed(values):
                if x[0] > (self.globalPlotRange[0]) :
                    yield x
                else:
                    break
        newlist = list(func1(data))
        for x in reversed(newlist):
            if x[0] < (self.globalPlotRange[1]):
                yield x
            else:
                break

    def filterRecord(self, data, timescale):
        return list(list(self.timeFilter(data, timescale)))

    def getPlotData(self, record):
        # if not self.paused and not self.doingPlot:
        self.doingPlot = True
        plotData = self.filterRecord(record['data'],self.globalPlotRange)
        if len(plotData) > 100*self.decimateScale:
            decimationfactor = int(np.floor(len(plotData)/self.decimateScale))
            plotData = plotData[0::decimationfactor]
            return plotData
        else:
            return plotData

    def show(self):
        self.plotWidget.show()

    def update(self):
        if self.scatterPlot and not self.doingPlot:
            self.doingPlot = True
            # self.legend.setParentItem(self.plot)
            # self.legend.items = []
            scatteritemnames=[]
            scatteritems=[]
            color=0
            for name in self.records:
                scatteritemnames.append(name)
                scatteritems.append(self.getPlotData(self.records[name]))
            # print scatteritemnames
            self.plot.clear()
            start = time.clock()
            oldLegendLabels = []
            for sample, label in self.legend.items:
                oldLegendLabels.append(label.text)
            for i in range(len(scatteritemnames)):
                for j in range(i+1, len(scatteritemnames)):
                    data1 = scatteritems[i]
                    data2 = scatteritems[j]
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
                    s1 = pg.ScatterPlotItem(x=x, y=y, size=5, pen=pg.mkPen(None), brush=pg.mkBrush(Qtableau20[color]))
                    name = scatteritemnames[i]+'v'+scatteritemnames[j]
                    if not name in oldLegendLabels:
                        self.plot.legend.addItem(s1, name)
                    color += 1
                    self.plot.addItem(s1)
            self.doingPlot = False
