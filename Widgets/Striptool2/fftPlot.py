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

# logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


# def logthread(caller):
#     print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
#                               threading.current_thread().ident))


class fftPlot(QWidget):
    fftSelectionChanged = QtCore.pyqtSignal('QString')

    def __init__(self, generalplot, parent=None, plotRateBar=False):
        super(fftPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.plotrate = 1
        ''' create the fftPlot as a grid layout '''
        self.fftPlot = QtGui.QVBoxLayout()
        self.plotThread = QTimer()
        self.generalPlot = generalplot
        self.records = self.generalPlot.records
        ''' Create generalPlot object '''
        self.plotWidget = fftPlotPlot(self)
        ''' set-up setupSelectionBar '''
        self.selectionBar = self.setupSelectionBar()
        ''' set-up plot rate slider '''
        self.setupPlotRateSlider()
        self.fftPlot.addLayout(self.selectionBarLayout, 1)
        self.generalPlot.signalAdded.connect(self.updateSelectionBar)
        self.generalPlot.signalRemoved.connect(self.updateSelectionBar)
        self.fftPlot.addWidget(self.plotWidget.plotWidget, 5)
        if plotRateBar:
            self.setupPlotRateSlider()
            self.fftPlot.addLayout(self.plotRateLayout)
        self.setLayout(self.fftPlot)
        # logger.debug('fftPlot initiated!')

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

    def setupSelectionBar(self):
        spacer = QtGui.QSpacerItem(100, 20)
        self.combobox1 = QtGui.QComboBox()
        self.combobox1.setMaximumWidth(200)
        self.combobox1.setMinimumWidth(100)
        self.combobox1.currentIndexChanged.connect(self.selectionBarChanged)
        for name in sorted(self.records):
            self.combobox1.addItem(name)
        self.combobox1.setCurrentIndex(0)
        self.selectionBarLayout = QtGui.QHBoxLayout()
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.combobox1)
        self.selectionBarLayout.addSpacerItem(spacer)

    def selectionBarChanged(self, index):
        self.fftSelectionChanged.emit(self.combobox1.currentText())
        self.plotWidget.update()

    def updateSelectionBar(self):
        combobox1text = self.combobox1.currentText()
        allnames = []
        for name in sorted(self.records):
            allnames.append(name)
            if self.combobox1.findText(name) == -1:
                self.combobox1.addItem(name)
        for index in range(self.combobox1.count()):
            if not self.combobox1.itemText(index) in allnames:
                self.combobox1.removeItem(index)
        self.setSelectionBar

    def setSelectionBar(self, combo1text):
        for index in range(self.combobox1.count()):
            if self.combobox1.itemText(index) == combobox1text:
                    self.combobox1.setCurrentIndex(index)

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
            self.plotWidget.update()

    def pausePlotting(self, value=True):
        self.paused = value
        self.plotWidget.togglePause(self.paused)

class fftPlotPlot(pg.PlotWidget):

    statusChanged = pyqtSignal(str)

    def __init__(self, fftplot, parent = None):
        super(fftPlotPlot, self).__init__(parent=parent)
        self.parent=parent
        self.fftplot = fftplot
        self.records = self.fftplot.records
        self.doingPlot = False
        self.paused = False
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.plots = {}
        self.color = 0
        self.paused = False
        self.selectionNameX = 0
        self.selectionNameY = 0
        self.decimateScale = 1000
        self.fftplot.fftSelectionChanged.connect(self.setSelectionIndex)
        self.fftPlot = self.plotWidget.addPlot(row=0, col=0)
        self.fftPlotPlot = self.fftPlot.plot()
        self.fftPlot.ctrl.fftCheck.setChecked(True)
        self.fftPlot.setLabel('bottom','Frequency (Hz)')
        self.fftPlot.setLabel('left','Amplitude')


    def setSelectionIndex(self, x):
        self.selectionNameX = str(x)
        if self.selectionNameX in self.records:
            self.data1 = self.records[self.selectionNameX]['data']
            self.createPlot(self.selectionNameX, self.records[self.selectionNameX]['pen'])

    def togglePause(self, value):
        self.paused = value

    def getPlotData(self, record):
        plotData = list(record['data'])
        return plotData

    def show(self):
        self.plotWidget.show()

    def createPlot(self, label1, color):
        self.fftPlot.setTitle('FFT of '+label1)
        self.fftPlotPlot.setPen(color)
        self.fftPlot.showGrid(x=True, y=True)

    def removePlot(self, name):
        self.plotWidget.removeItem(self.plotWidget.getItem(0,0))

    def update(self):
        start = time.time()
        if not self.paused and not self.doingPlot and hasattr(self,'data1') and len(self.data1) > 1:
            self.doingPlot  = True
            data1 = list(self.data1)
            if len(data1) > self.decimateScale:
                del data1[:len(data1)-self.decimateScale]
            x, y = zip(*data1)
            self.fftPlotPlot.setData({'x': x, 'y': y})
            self.doingPlot = False
        # self.fftPlot.enableAutoRange()
