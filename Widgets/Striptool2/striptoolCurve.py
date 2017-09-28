import time, math
import pyqtgraph as pg
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import striptoolFunctions as stfunctions

''' This is the curve class which enables plotting on a plotting object. Making it a class eases control of the different options for multiple curves'''
class curve(QObject):
    def __init__(self, record, plot, name):
        QObject.__init__(self)
        self.records = record
        self.name = name
        self.plot = plot
        self.vb = record[name]['viewbox']
        self.axis = record[name]['axis']
        self.curve = pg.PlotDataItem()
        self.vb.addItem(self.curve)
        self.scene = self.vb.scene()
        self.lines = MultiLine()
        self.lineOn = False
        self.timeOffset = 0

    def updateTimeOffset(self,time):
        self.timeOffset += time
        if hasattr(self,'path') and self.lines.isVisible():
            self.lines.setNewPath(self.path)
            if not self.lineOn:
                self.lines.setPen(pg.mkPen(self.records[self.name]['pen']))
                self.scenePath = self.vb.addItem(self.lines)
                # self.lines.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
                self.lineOn = True

    def changePenColour(self):
        self.lines.setPen(pg.mkPen(self.records[self.name]['pen']))

    ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
    def updateData(self, data):
        val = math.log(data[1],10) if self.records[self.name]['logScale'] else data[1]
        newpoint = QPointF(data[0], val)
        if not hasattr(self,'path'):
            self.lastplottime = self.starttime = round(time.time(),2)
            self.path = QPainterPath(newpoint)
        self.path.lineTo(data[0], val)


    ''' helper function to clear a curves points '''
    def clear(self):
        self.plot.plot.removeItem(self.lines)
        self.curve.clear()

class MultiLine(pg.QtGui.QGraphicsPathItem):
    def __init__(self, log=False):
        """x and y are 1D arrays of shape (Nplots, Nsamples)"""
        super(MultiLine, self).__init__()

    def setNewPath(self, path):
        self.path = path
        self.setPath(path)

    def shape(self): # override because QGraphicsPathItem.shape is too expensive.
        return pg.QtGui.QGraphicsItem.shape(self)
    def boundingRect(self):
        return self.path.boundingRect()
