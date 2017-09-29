import sys, time, os, datetime, copy, random
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
from bisect import bisect_left, bisect_right
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
        self.paused = False
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.plots = {}
        self.color = 0
        self.paused = False
        self.selectionNameX = 0
        self.selectionNameY = 0
        self.decimateScale = 10000
        self.scatterplot.scatterSelectionChanged.connect(self.setSelectionIndex)
        self.plot = self.plotWidget.addPlot(row=0, col=0)
        self.scatterPlot = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None))
        self.plot.addItem(self.scatterPlot)
        self.scatterPlot.sigClicked.connect(self.printPoints)

    def printPoints(self,scatterPlot, points):
        point = points[0]
        text =  "{%0.3f, %0.3f}" % (point.pos()[0], point.pos()[1])
        self.statusChanged.emit(text)

    def setSelectionIndex(self, x, y):
        self.selectionNameX = str(x)
        self.selectionNameY = str(y)
        if self.selectionNameX in self.records and self.selectionNameY in self.records:
            self.signalDelayTime1 =  self.records[self.selectionNameX]['timer']
            self.signalDelayTime2 =  self.records[self.selectionNameY]['timer']
            self.data1 = self.records[self.selectionNameX]['data']
            self.data2 = self.records[self.selectionNameY]['data']
            self.createPlot(self.selectionNameX, self.selectionNameY, self.color)

    def togglePause(self, value):
        self.paused = value

    def getPlotData(self, record):
        plotData = list(record['data'])
        return plotData

    def show(self):
        self.plotWidget.show()

    def createPlot(self, label1, label2, color):
        name = label1+' vs '+label2
        self.plot.setLabel('bottom',label1)
        self.plot.setLabel('left',label2)
        self.plot.setTitle(name)
        self.plot.showGrid(x=True, y=True)

    def removePlot(self, name):
        self.plotWidget.removeItem(self.plotWidget.getItem(0,0))

    def update(self):
        start = time.time()
        if not self.paused and not self.doingPlot and hasattr(self,'data1') and hasattr(self,'data2'):
            self.doingPlot  = True
            self.plot.disableAutoRange()
            data1 = list(self.data1)
            data2 = list(self.data2)
            if len(data1) > 1 and len(data2) > 1:
                if data1[0][0] < data2[0][0]:
                    ans = takeClosestPosition(zip(*data1)[0], data1, data2[0][0])
                    starttime = ans[1]
                    startpos1 = ans[0]
                    startpos2 = 0
                elif data1[0][0] > data2[0][0]:
                    ans = takeClosestPosition(zip(*data2)[0], data2, data1[0][0])
                    starttime = ans[1]
                    startpos1 = 0
                    startpos2 = ans[0]
                else:
                    startpos1 = startpos2 = 0
                del data1[:startpos1]
                del data2[:startpos2]
                if len(data1) > len(data2):
                    del data1[len(data2) - len(data1):]
                elif len(data2) > len(data1):
                    del data2[len(data1) - len(data2):]
                if len(data1) > 1 and len(data2) > 1:
                    x1,x = zip(*data1)
                    x2,y = zip(*data2)
                    if len(x) > self.decimateScale:
                        xy = zip(x,y)
                        del xy[:len(x)-self.decimateScale]
                        x, y = zip(*xy)
                    self.scatterPlot.setData(x, y, pxMode=True, pen=None)
            self.doingPlot = False
        self.plot.enableAutoRange()
