import sys, time, os, datetime, signal
import pyqtgraph as pg
sys.path.append("../../../")
import Software.Procedures.qt as qt
# import peakutils
import numpy as np
# logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


# def logthread(caller):
#     print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
#                               threading.current_thread().ident))


class histogramPlot(qt.QWidget):

    def __init__(self, generalplot, parent=None, plotRateBar=False):
        super(histogramPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.plotrate = 1
        ''' create the histogramPlot as a grid layout '''
        self.layout = qt.QVBoxLayout()
        self.plotThread = qt.QTimer()
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
        self.setupOptionsBox()
        self.subtractMeans = False
        self.normalise = False
        self.layout.addLayout(self.subtractMeanLayout)
        self.layout.addLayout(self.normaliseLayout)
        if plotRateBar:
            self.setupPlotRateSlider()
            self.layout.addLayout(self.plotRateLayout)
        self.setLayout(self.layout)
        # logger.debug('histogramPlot initiated!')
        self.generalPlot.signalRemoved.connect(self.removeCurve)

    def setupOptionsBox(self):
        self.subtractMeanLayout = qt.QHBoxLayout()
        self.subtractMeanLabel = qt.QLabel()
        self.subtractMeanLabel.setText('Subtract Means')
        self.subtractMeanLabel.setAlignment(qt.Qt.AlignCenter)
        self.subtractMeanCheckbox = qt.QCheckBox()
        self.subtractMeanCheckbox.setChecked(False)
        self.subtractMeanCheckbox.stateChanged.connect(self.setSubtractMeans)
        self.subtractMeanLayout.addWidget(self.subtractMeanLabel)
        self.subtractMeanLayout.addWidget(self.subtractMeanCheckbox)
        self.normaliseLayout = qt.QHBoxLayout()
        self.normaliseLabel = qt.QLabel()
        self.normaliseLabel.setText('Normalise')
        self.normaliseLabel.setAlignment(qt.Qt.AlignCenter)
        self.normaliseCheckbox = qt.QCheckBox()
        self.normaliseCheckbox.setChecked(False)
        self.normaliseCheckbox.stateChanged.connect(self.setNormalise)
        self.normaliseLayout.addWidget(self.normaliseLabel)
        self.normaliseLayout.addWidget(self.normaliseCheckbox)

    def setupPlotRateSlider(self):
        self.plotRateLayout = qt.QHBoxLayout()
        self.plotRateLabel = qt.QLabel()
        self.plotRateLabel.setText('Plot Update Rate ['+str(self.plotrate)+' Hz]:')
        self.plotRateLabel.setAlignment(qt.Qt.AlignCenter)
        self.plotRateSlider = qt.QSlider()
        self.plotRateSlider.setOrientation(qt.Qt.Horizontal)
        self.plotRateSlider.setInvertedAppearance(False)
        self.plotRateSlider.setInvertedControls(False)
        self.plotRateSlider.setMinimum(1)
        self.plotRateSlider.setMaximum(50)
        self.plotRateSlider.setValue(self.plotrate)
        self.plotRateSlider.valueChanged.connect(self.setPlotRate)
        self.plotRateLayout.addWidget(self.plotRateLabel)
        self.plotRateLayout.addWidget(self.plotRateSlider)

    def setSubtractMeans(self, value):
        self.subtractMeans = value

    def setNormalise(self, value):
        self.normalise = value

    def setPlotRate(self, value):
        self.plotrate = value
        self.plotRateLabel.setText('Plot Update Rate [' + str(self.plotrate) + ' Hz]:')
        self.plotThread.setInterval(1000 * 1 / value)

    def start(self, timer=1000):
        self.plotUpdate()
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def plotUpdate(self):
        if self.isVisible() and not self.paused:
            for curve in self.histogramPlotCurves.values():
                curve.update()

    def pausePlotting(self, value=True):
        self.paused = value

    def addCurve(self, name):
        name = str(name)
        self.histogramPlotCurves[name] = histogramPlotCurve(self.histogramPlot, self.records[name], parent=self)
        self.histogramPlotCurves[name].update()

    def removeCurve(self, name):
        name = str(name)
        if name in self.histogramPlotCurves:
            self.histogramPlot.removeItem(self.histogramPlotCurves[name].plot)
            del self.histogramPlotCurves[name]

    def selectionChange(self, name, value):
        name = str(name)
        if name in self.histogramPlotCurves:
            if not value:
                # print('removing Curve = ', name)
                self.removeCurve(name)
        elif value == True:
            self.addCurve(name)

class histogramPlotCurve(qt.QObject):

    statusChanged = qt.pyqtSignal(str)

    def __init__(self, histogramplot, records, parent = None):
        super(histogramPlotCurve, self).__init__(parent=parent)
        self.parent=parent
        self.histogramplot = histogramplot
        self.recordspen = records['pen']
        self.data = records['data']
        self.mean = records['worker'].mean
        self.stddev = records['worker'].stddeviation
        self.doingPlot = False
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
            if self.parent.subtractMeans:
                x2 = x2 - np.mean(x2)
            if self.parent.normalise:
                mean = np.mean(x2)
                x2 = x2 - mean
                x2 = x2 / np.std(x2)
                x2 = x2 + mean
            r,g,b,a = pg.colorTuple(pg.mkColor(self.recordspen))
            self.pencolor = pg.mkColor(r,g,b,255)
            self.brushcolor = pg.mkColor(r,g,b,64)
            self.plot.setData({'x': x2, 'y': y2}, pen=self.pencolor, stepMode=True, fillLevel=0, fillBrush=self.brushcolor)
        self.doingPlot = False
        # self.histogramPlot.enableAutoRange()
