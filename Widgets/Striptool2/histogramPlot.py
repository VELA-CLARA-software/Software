import sys, time, os, datetime, signal
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import peakutils
import numpy as np
# logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


# def logthread(caller):
#     print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
#                               threading.current_thread().ident))


class histogramPlot(QWidget):

    def __init__(self, generalplot, parent=None, plotRateBar=False):
        super(histogramPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.plotrate = 1
        ''' create the histogramPlot as a grid layout '''
        self.layout = QtGui.QVBoxLayout()
        self.plotThread = QTimer()
        self.generalPlot = generalplot
        self.records = self.generalPlot.records
        ''' Create generalPlot object '''
        self.plotWidget = pg.GraphicsLayoutWidget()
        ''' set-up plot rate slider '''
        self.setupPlotRateSlider()
        self.layout.addWidget(self.plotWidget, 5)

        ''' Create plot for curves '''
        self.histogramPlot = self.plotWidget.addPlot(row=0, col=0)
        self.histogramPlot.setLabel('bottom','Value')
        self.histogramPlot.setLabel('left','Count')
        self.histogramPlot.showGrid(x=True, y=True)
        self.histogramPlotCurves = {}
        if plotRateBar:
            self.setupPlotRateSlider()
            self.layout.addLayout(self.plotRateLayout)
        self.setLayout(self.layout)
        # logger.debug('histogramPlot initiated!')

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
            for curve in self.histogramPlotCurves.values():
                curve.update()

    def pausePlotting(self, value=True):
        self.paused = value
        self.plotWidget.togglePause(self.paused)

    def addCurve(self, name):
        name = str(name)
        self.histogramPlotCurves[name] = histogramPlotCurve(self.histogramPlot, self.records[name])

    def removeCurve(self, name):
        self.histogramPlot.removeItem(self.histogramPlotCurves[name].plot)
        del self.histogramPlotCurves[name]

    def selectionChange(self, name, value):
        name = str(name)
        if name in self.histogramPlotCurves:
            if not value:
                print('removing Curve = ', name)
                self.removeCurve(name)
        elif value == True:
            self.addCurve(name)

class histogramPlotCurve(QObject):

    statusChanged = pyqtSignal(str)

    def __init__(self, histogramplot, records, parent = None):
        super(histogramPlotCurve, self).__init__(parent=parent)
        self.parent=parent
        self.histogramplot = histogramplot
        self.color = records['pen']
        self.data = records['data']
        self.mean = records['worker'].mean
        self.stddev = records['worker'].stddeviation
        self.doingPlot = False
        self.paused = False
        self.paused = False
        self.numberBins = 10
        self.decimateScale = 1000
        self.plot = self.histogramplot.plot()

    def togglePause(self, value):
        self.paused = value

    def show(self):
        self.plotWidget.show()

    def removePlot(self, name):
        self.histogramplot.removeItem(self.plotWidget.getItem(0,0))

    def update(self):
        start = time.time()
        if not self.paused and not self.doingPlot and hasattr(self,'data') and len(self.data) > 1:
            self.doingPlot  = True
            data = list(self.data)
            if len(data) > self.decimateScale:
                del data[:len(data)-self.decimateScale]
            x, y = zip(*data)
            y2,x2 = np.histogram(y, bins=self.numberBins)
            self.plot.setData({'x': x2, 'y': y2}, pen=self.color, stepMode=True, fillLevel=0, fillBrush=self.color)
        self.doingPlot = False
        # self.histogramPlot.enableAutoRange()
