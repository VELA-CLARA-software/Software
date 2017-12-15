import sys, time, os, datetime, math, collections
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import collections
# if sys.version_info<(3,0,0):
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# else:
#     from PyQt5.QtCore import *
#     from PyQt5.QtGui import *
#     from PyQt5.QtWidgets import *
import colours as colours

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

class VAxis(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(VAxis, self).__init__(parent=parent, orientation=orientation, linkView=linkView)

    def logTickStrings(self, values, scale, spacing):
        return ["%0.1g"%abs(x) for x in 10 ** np.array(values).astype(float)]

class scrollingPlot(QWidget):

    doCurveUpdate = QtCore.pyqtSignal()
    timeChangeSignal = QtCore.pyqtSignal('float')

    def __init__(self, generalplot, parent=None, plotRateBar=False, color=0):
        super(scrollingPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.plotrate = 1
        ''' create the scatterPlot as a grid layout '''
        self.scrollingPlot = QtGui.QVBoxLayout()
        self.plotThread = QTimer()
        self.generalPlot = generalplot
        self.records = self.generalPlot.records
        ''' Create generalPlot object '''
        self.scrollingPlotPlot = scrollingPlotPlot(self)
        ''' set-up plot rate slider '''
        self.setupPlotRateSlider()
        self.scrollingPlot.addWidget(self.scrollingPlotPlot.plotWidget, 5)
        if plotRateBar:
            self.setupPlotRateSlider()
            self.scrollingPlot.addLayout(self.plotRateLayout)
        self.setLayout(self.scrollingPlot)

        self.generalPlot.signalAdded.connect(self.addSignal)
        self.generalPlot.signalRemoved.connect(self.removeSignal)

    def addSignal(self, name):
        name = str(name)
        self.records[name]['scrollingplot'] = self.scrollingPlotPlot
        curve = self.scrollingPlotPlot.addCurve(name)
        self.records[name]['curve'] = curve

    def removeSignal(self, name):
        self.scrollingPlotPlot.removeCurve(name)

    def setupPlotRateSlider(self):
        self.plotRateLayout = QHBoxLayout()
        self.plotRateLabel = QtGui.QLabel()
        self.plotRateLabel.setText('Plot Update Rate ['+str(self.plotrate)+' Hz]:')
        self.plotRateLabel.setAlignment(Qt.AlignCenter)
        self.plotRateSlider = QtGui.QSlider()
        self.plotRateSlider.setOrientation(QtCore.Qt.Horizontal)
        self.plotRateSlider.setInvertedAppearance(False)
        self.plotRateSlider.setInvertedControls(False)
        self.plotRateSlider.setMinimum(1)
        self.plotRateSlider.setMaximum(50)
        self.plotRateSlider.setValue(self.plotrate)
        self.plotRateSlider.valueChanged.connect(self.setPlotRate)
        self.plotRateLayout.addWidget(self.plotRateLabel)
        self.plotRateLayout.addWidget(self.plotRateSlider)

    def setPlotRate(self, value):
        self.plotrate = value
        self.plotRateLabel.setText('Plot Update Rate [' + str(self.plotrate) + ' Hz]:')
        self.plotThread.setInterval(1000 * 1 / value)

    def start(self, timer=1000):
        self.plotUpdate()
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def plotUpdate(self):
        if self.isVisible():
            if not hasattr(self,'lastplottime'):
                self.lastplottime = round(time.time(),2)
            if not self.paused:
                self.doCurveUpdate.emit()
                lastplottime = round(time.time(),2)
                self.timeOffset = lastplottime-self.lastplottime
                self.timeChangeSignal.emit(self.timeOffset)
                self.scrollingPlotPlot.plot.vb.translateBy(x=self.timeOffset)
                self.lastplottime = lastplottime

    def pausePlotting(self, value=True):
        self.paused = value
        self.plotWidget.togglePause(self.paused)

    def setPlotScale(self, timescale):
        self.timescale = timescale
        self.scrollingPlotPlot.setPlotScale([time.time()+(-1.025*timescale),time.time()+(0.025*timescale)])

    def createAxis(self, *args, **kwargs):
        self.scrollingPlotPlot.createAxis(*args, **kwargs)

class scrollingPlotPlot(QWidget):

    plotUpdated = pyqtSignal()
    newaxis = pyqtSignal()

    def __init__(self, scrollingplot, parent = None):
        super(scrollingPlotPlot, self).__init__(parent=parent)
        self.scrollingPlot = scrollingplot
        self.records = self.scrollingPlot.records
        self.paused = False
        self.doingPlot = False
        self.paused = False
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.threads = {}
        self.workers = {}
        self.viewboxes = {}
        self.namedaxes = {}
        self.createPlot()

    ''' This creates a PyQtGraph plot object (self.plot) and instantiates the bottom axis to be a CAxisTime axis '''
    def createPlot(self):
        self.date_axis = HAxisTime(orientation = 'bottom')
        self.scrollingPlot.timeChangeSignal.connect(self.date_axis.updateTimeOffset)
        self.leftaxis = pg.AxisItem("left")
        self.plot = self.plotWidget.addPlot(row=0,col=50, autoDownsample=True, clipToView=True, antialias=False, downsampleMethod='peak', axisItems={'bottom':self.date_axis})
        self.plot.vb.setMouseEnabled(y=False)
        self.plot.disableAutoRange(False)
        self.plot.setRange(xRange=[-0.5,1.5])
        self.plot.showAxis('left', False)
        self.plot.mouseOver = False
        self.plot.showGrid(x=True, y=True)

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

    ''' Toggles autoscroll on the plot '''
    def toggleAutoScroll(self, value):
        self.autoscroll = value
        if not value:
            self.currenttime = self.currentPlotTime
            self.fixedtimepoint = self.currentPlotTime

    def createAxis(self, name='', color='k', logMode=False, verticalRange=None):
        axis = pg.AxisItem("left")
        labelStyle = {'color': '#'+pg.colorStr(pg.mkColor(color))[0:-2]}
        axis.setLabel(name,**labelStyle)
        axis.setLogMode(logMode)
        viewbox = pg.ViewBox()
        axis.linkToView(viewbox)
        viewbox.setXLink(self.plot.vb)
        self.namedaxes[name] = [axis, viewbox]
        if not verticalRange == None:
            if logMode:
                logrange = [math.log(x,10) for x in verticalRange]
                viewbox.setRange(yRange=logrange,disableAutoRange=True)
            else:
                viewbox.setRange(yRange=verticalRange,disableAutoRange=True)
        col = self.findFirstEmptyColumnInGraphicsLayout()
        self.plotWidget.ci.addItem(axis, row = 0, col = col,  rowspan=1, colspan=1)
        self.plotWidget.ci.addItem(viewbox, row=0, col=50)
        self.newaxis.emit()
        return axis, viewbox

    def getAxes(self):
        return self.namedaxes.keys()

    def changeAxis(self, name, axisname):
        record = self.records
        axis, viewbox = self.namedaxes[axisname]
        record[name]['viewbox'] = viewbox
        record[name]['axis'] = axis
        record[name]['logScale'] = axis.logMode
        record[name]['curve'].changeViewbox(viewbox)

    ''' Helper function to add a curve to the plot '''
    def addCurve(self, name):
        # Create New Axis
        record = self.records
        if record[name]['axisname'] == None:
            axis, viewbox = self.createAxis(name=name, color=record[name]['pen'], logMode=record[name]['logScale'], verticalRange=record[name]['verticalRange'])
            record[name]['axisname'] = name
        elif record[name]['axisname'] in  self.namedaxes:
            axis, viewbox = self.namedaxes[record[name]['axisname']]
        else:
            axis, viewbox = self.createAxis(name=record[name]['axisname'], color=record[name]['pen'], logMode=record[name]['logScale'],verticalRange=record[name]['verticalRange'])
        record[name]['viewbox'] = viewbox
        record[name]['axis'] = axis
        record[name]['logScale'] = axis.logMode
        self.threads[name] = QtCore.QThread(self.scrollingPlot)
        self.workers[name] = curveRecordWorker(self, name)
        self.workers[name].moveToThread(self.threads[name])
        self.threads[name].start()
        return self.workers[name].curve

    def removeCurve(self, name):
        record = self.records
        name = str(name)
        axisname = record[name]['axisname']
        axis, viewbox = self.namedaxes[record[name]['axisname']]
        self.threads[name].quit()
        self.plotWidget.ci.removeItem(axis)
        self.plotWidget.ci.removeItem(viewbox)

    def toggleAxis(self, name, visible):
        axis, viewbox = self.namedaxes[self.records[name]['axisname']]
        axis.setVisible(visible)

    def findFirstEmptyColumnInGraphicsLayout(self):
        rowsfilled =  self.plotWidget.ci.rows.get(0, {}).keys()
        for i in range(49):
            if not i in rowsfilled:
                return i

class curveRecordWorker(QtCore.QObject):
    def __init__(self, plot, name):
        QtCore.QObject.__init__(self)
        self.curve = curve(plot, name)

''' This is the curve class which enables plotting on a plotting object. Making it a class eases control of the different options for multiple curves'''
class curve(QObject):
    def __init__(self, plot, name):
        QObject.__init__(self)
        self.plot = plot
        self.records = self.plot.records
        self.name = name
        self.vb = self.records[name]['viewbox']
        self.curve = pg.PlotDataItem()
        self.vb.addItem(self.curve)
        self.scene = self.vb.scene()
        self.lines = MultiLine()
        self.lines10 = MultiLine()
        self.lines10.setVisible(False)
        self.lines100 = MultiLine()
        self.lines100.setVisible(False)
        self.lines1000 = MultiLine()
        self.lines1000.setVisible(False)
        self.points = collections.deque(maxlen=self.records[name]['maxlength'])
        self.points10 = collections.deque(maxlen=self.records[name]['maxlength'])
        self.points100 = collections.deque(maxlen=self.records[name]['maxlength'])
        self.points1000 = collections.deque(maxlen=self.records[name]['maxlength'])
        self.lineOn = False
        self.line10On = False
        self.line100On = False
        self.line1000On = False
        self.timeOffset = 0
        self.visibility = {'lines': True, 'lines10': False, 'lines100': False, 'lines1000': False}
        self.plot.scrollingPlot.timeChangeSignal.connect(self.updateTimeOffset)
        self.plot.records[name]['worker'].recordLatestValueSignal.connect(lambda x: self.updateData(x, self.points))
        self.plot.records[name]['worker'].recordMean10Signal.connect(lambda x: self.updateData(x, self.points10))
        self.plot.records[name]['worker'].recordMean100Signal.connect(lambda x: self.updateData(x, self.points100))
        self.plot.records[name]['worker'].recordMean1000Signal.connect(lambda x: self.updateData(x, self.points1000))
        self.path = None

    def setVisibility(self, linename, visible):
        self.visibility[linename] = visible
        # print self.visibility
        if linename is 'lines':
            if visible is False:
                for k in self.visibility.keys():
                    getattr(self, k).setVisible(False)
            else:
                for k,v in self.visibility.iteritems():
                    getattr(self, k).setVisible(self.visibility[k])
        else:
            self.visibility[linename] = visible
            if self.visibility['lines'] is True:
                getattr(self, linename).setVisible(visible)


    def changeViewbox(self, viewbox):
        name = self.name
        self.vb.removeItem(self.curve)
        self.vb = self.records[name]['viewbox']
        self.vb.addItem(self.curve)
        self.lineOn = False

    def redrawLines(self, points, line, lineOn, pen):
        if line.isVisible() and len(points) > 0:
            path = QPainterPath(points[0])
            for point in points:
                path.lineTo(point)
            line.setNewPath(path)
            if not lineOn:
                line.setPen(pg.mkPen(**pen))
                self.vb.addItem(line)
                lineOn = True

    def updateTimeOffset(self,time):
        self.timeOffset += time
        self.redrawLines(self.points, self.lines, self.lineOn, {'color': self.records[self.name]['pen']})
        self.redrawLines(self.points10, self.lines10, self.line10On, {'color': self.records[self.name]['pen'], 'dash': [2,2], 'width': 2})
        self.redrawLines(self.points100, self.lines100, self.line100On, {'color': self.records[self.name]['pen'], 'dash': [2,2], 'width': 3})
        self.redrawLines(self.points1000, self.lines1000, self.line1000On, {'color': self.records[self.name]['pen'], 'dash': [3,3], 'width': 4})

    def changePenColour(self):
        self.lines.setPen(pg.mkPen(color=self.records[self.name]['pen']))
        self.lines10.setPen(pg.mkPen(color=self.records[self.name]['pen'], dash=[1,1], width=2))
        self.lines100.setPen(pg.mkPen(color=self.records[self.name]['pen'], dash=[2,2], width=3))
        self.lines1000.setPen(pg.mkPen(color=self.records[self.name]['pen'], dash=[3,3], width=4))

    ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
    def updateData(self, data, points):
        val = data[1] if not self.records[self.name]['logScale'] else math.log(data[1],10)
        newpoint = QPointF(data[0], val)
        points.append(newpoint)

class MultiLine(pg.QtGui.QGraphicsPathItem):
    def __init__(self, log=False):
        """x and y are 1D arrays of shape (Nplots, Nsamples)"""
        super(MultiLine, self).__init__()

    def setNewPath(self, path):
        self.path = path
        self.setPath(self.path)

    def shape(self): # override because QGraphicsPathItem.shape is too expensive.
        return pg.QtGui.QGraphicsItem.shape(self)
    def boundingRect(self):
        return self.path.boundingRect()
