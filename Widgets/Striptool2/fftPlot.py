import sys, time, os, datetime, signal
import pyqtgraph as pg
import numpy as np
from scipy import interpolate
from scipy import signal as sp
sys.path.append("../../../")
import Software.Procedures.qt as qt
import peakutils
# logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)

from math import log10, floor
def round_sig(x, sig=4):
    return round(x, sig-int(floor(log10(abs(x))))-1)

# def logthread(caller):
#     print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
#                               threading.current_thread().ident))


class fftPlot(qt.QWidget):
    fftSelectionChanged = qt.pyqtSignal('QString')

    def __init__(self, generalplot, parent=None, plotRateBar=False):
        super(fftPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.plotrate = 5
        ''' create the fftPlot as a grid layout '''
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
        self.fftPlot = self.plotWidget.addPlot(row=0, col=0)
        # self.fftPlot.ctrl.fftCheck.setChecked(True)
        self.fftPlot.setLabel('bottom','Frequency (Hz)')
        self.fftPlot.setLabel('left','Amplitude')
        self.fftPlot.showGrid(x=True, y=True)
        self.fftPlotCurves = {}
        if plotRateBar:
            self.setupPlotRateSlider()
            self.layout.addLayout(self.plotRateLayout)
        self.setLayout(self.layout)
        # logger.debug('fftPlot initiated!')
        self.generalPlot.signalRemoved.connect(self.removeCurve)

    def setupPlotRateSlider(self):
        self.plotRateLayout = qt.QHBoxLayout()
        self.plotRateLabel = qt.QLabel()
        self.plotRateLabel.setText('Plot Update Rate ['+str(self.plotrate)+' Hz]:')
        self.plotRateLabel.setAlignment(qt.Qt.AlignCenter)
        self.plotRateSlider =qt.QSlider()
        self.plotRateSlider.setOrientation(qt.Qt.Horizontal)
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

    def start(self, timer=1000, offset=250):
        if not hasattr(self, 'slept'):
            time.sleep(offset/1000.)
            self.slept = True
        self.plotUpdate()
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def plotUpdate(self):
        if self.isVisible() and not self.paused:
            for curve in self.fftPlotCurves.values():
                curve.update()

    def pausePlotting(self, value=True):
        self.paused = value

    def addCurve(self, name):
        name = str(name)
        self.fftPlotCurves[name] = fftPlotCurve(self.fftPlot, self.records[name])
        self.fftPlotCurves[name].update()

    def removeCurve(self, name):
        name = str(name)
        if name in self.fftPlotCurves:
            self.fftPlotCurves[name].removeFFTLabels()
            self.fftPlot.removeItem(self.fftPlotCurves[name].plot)
            del self.fftPlotCurves[name]

    def selectionChange(self, name, value):
        name = str(name)
        if name in self.fftPlotCurves:
            if not value:
                # print('removing curve = ', name)
                self.removeCurve(name)
        elif value:
            self.addCurve(name)

class fftPlotCurve(qt.QObject):

    statusChanged = qt.pyqtSignal(str)

    def __init__(self, fftplot, records, parent = None):
        super(fftPlotCurve, self).__init__(parent=parent)
        self.parent=parent
        self.fftplot = fftplot
        self.color = records['pen']
        self.data = records['data']
        self.mean = records['worker'].mean
        self.stddev = records['worker'].stddeviation
        self.timer = records['timer']
        # print 'self.timer = ', self.timer
        self.doingPlot = False
        self.paused = False
        self.decimateScale = 2**14
        self.plot = self.fftplot.plot()
        self.fftTextLabels = []

    def togglePause(self, value):
        self.paused = value

    def show(self):
        self.plotWidget.show()

    def removePlot(self, name):
        self.fftplot.removeItem(self.plotWidget.getItem(0,0))

    def _fourierTransform(self, x, y):
        ## Perform fourier transform. If x values are not sampled uniformly,
        ## then use np.interp to resample before taking fft.
        # print 'length x = ', len(x)
        # dx = np.diff(x)
        # print ('mean dx = ', round_sig(np.mean(dx),6), ' sigma = ', round_sig(np.std(dx),6), ' = ', round_sig(100*np.std(dx) / np.mean(dx),3),'%   min = ', np.min(dx), ' / max = ', np.max(dx))
        # uniform = not np.any(np.abs(dx-dx[0]) > (abs(dx[0]) / 100.))
        # starttime = time.clock()
        # if not uniform:
        #     # print('FFT not uniform!  ', max(np.abs(dx-dx[0])), ' > ', (abs(dx[0]) / 1000.))
        #     # x2 = np.linspace(x[0], x[0] + len(x)*self.timer, len(x))
        #     x2 = np.linspace(x[0], x[-1], len(x))
        #     y = np.interp(x2, x, y)
        #     x = x2
        # f = np.fft.fft(y) / len(y)
        # y = abs(f[1:int(len(f)/2)])
        # dt = x[-1] - x[0]
        # x = np.linspace(0, 0.5*len(x)/dt, len(y))
        # print 'FFT took ', time.clock() - starttime
        nperseg = len(y) if len(y) < 2**12 else 2**12
        fs = 1.0/self.timer
        x,y = sp.welch(y, fs=fs, nperseg=nperseg)
        return x, y

    def update(self):
        start = time.time()
        self.removeFFTLabels()
        if not self.paused and not self.doingPlot and hasattr(self,'data') and len(self.data) > 1:
            self.doingPlot  = True
            data = list(self.data)
            if len(data) > self.decimateScale:
                data = data[-self.decimateScale:]
            x, y = zip(*data)
            x, yf = self._fourierTransform(x, y)
            y = yf/max(yf)
            self.plot.setData({'x': x, 'y': y}, pen=self.color)
            if len(self.plot.yDisp) > 0:
                indexes = peakutils.indexes(self.plot.yDisp, thres=0.75, min_dist=10)
                for index in indexes[:5]:
                    fftTextlabel=pg.TextItem(html='<span style="color: '+pg.mkColor(self.color).name()+';">'+str(round_sig(self.plot.xDisp[index],4))+'</span>',anchor=(-0.7,1.2), angle=0)
                    fftTextlabel.setPos(self.plot.xDisp[index],self.plot.yDisp[index])
                    fftTextArrow=pg.ArrowItem(pos=(self.plot.xDisp[index],self.plot.yDisp[index]), angle=-45, pen=self.color, brush=pg.mkBrush(self.color))
                    self.fftTextLabels.append([fftTextlabel, fftTextArrow])
                    self.fftplot.addItem(fftTextlabel)
                    self.fftplot.addItem(fftTextArrow)
            self.doingPlot = False
        # self.fftPlot.enableAutoRange()

    def removeFFTLabels(self):
        for t, a in self.fftTextLabels:
            self.fftplot.removeItem(t)
            self.fftplot.removeItem(a)
        self.fftTextLabels = []
