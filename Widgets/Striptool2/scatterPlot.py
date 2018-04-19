import sys, time, os, datetime, signal
import pyqtgraph as pg
# from pyqtgraph.Qt import QtGui, QtCore
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
from bisect import bisect_left
# logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


# def logthread(caller):
#     print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
#                               threading.current_thread().ident))

class scatterPlot(QWidget):
    scatterSelectionChanged = pyqtSignal('QString', 'QString')

    def __init__(self, generalplot, parent=None, plotRateBar=False):
        super(scatterPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.plotrate = 1
        ''' create the scatterPlot as a grid layout '''
        self.scatterPlot = QVBoxLayout()
        self.plotThread = QTimer()
        self.generalPlot = generalplot
        self.records = self.generalPlot.records
        ''' Create generalPlot object '''
        self.plotWidget = scatterPlotPlot(self)
        ''' set-up setupSelectionBar '''
        self.selectionBar = self.setupSelectionBar()
        self.removedname = ''
        ''' set-up plot rate slider '''
        self.setupPlotRateSlider()
        self.scatterPlot.addLayout(self.selectionBarLayout, 1)
        self.generalPlot.signalAdded.connect(self.updateSelectionBar)
        self.generalPlot.signalRemoved.connect(self.removeSignal)
        self.scatterPlot.addWidget(self.plotWidget.plotWidget, 5)
        if plotRateBar:
            self.setupPlotRateSlider()
            self.scatterPlot.addLayout(self.plotRateLayout)
        self.setLayout(self.scatterPlot)
        # logger.debug('scatterPlot initiated!')

    def removeSignal(self, name):
        self.removedname = name
        self.updateSelectionBar()

    def setupPlotRateSlider(self):
        self.plotRateLayout = QHBoxLayout()
        self.plotRateLabel = QLabel()
        self.plotRateLabel.setText('Plot Update Rate ['+str(self.plotrate)+' Hz]:')
        self.plotRateLabel.setAlignment(Qt.AlignCenter)
        self.plotRateSlider = QSlider()
        self.plotRateSlider.setOrientation(Qt.Horizontal)
        self.plotRateSlider.setInvertedAppearance(False)
        self.plotRateSlider.setInvertedControls(False)
        self.plotRateSlider.setMinimum(1)
        self.plotRateSlider.setMaximum(50)
        self.plotRateSlider.setValue(self.plotrate)
        self.plotRateSlider.valueChanged.connect(self.setPlotRate)
        self.plotRateLayout.addWidget(self.plotRateLabel)
        self.plotRateLayout.addWidget(self.plotRateSlider)

    def setupSelectionBar(self):
        spacer = QSpacerItem(100, 20)
        self.combobox1 = QComboBox()
        self.combobox1.setMaximumWidth(200)
        self.combobox1.setMinimumWidth(100)
        self.combobox1.currentIndexChanged.connect(self.selectionBarChanged)
        self.combobox2 = QComboBox()
        self.combobox2.setMaximumWidth(200)
        self.combobox2.setMinimumWidth(100)
        self.combobox2.currentIndexChanged.connect(self.selectionBarChanged)
        for name in sorted(self.records):
            self.combobox1.addItem(name)
            self.combobox2.addItem(name)
        self.combobox1.setCurrentIndex(0)
        self.combobox2.setCurrentIndex(1)
        self.selectionBarLayout = QHBoxLayout()
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.combobox1)
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.combobox2)
        self.selectionBarLayout.addSpacerItem(spacer)

    def selectionBarChanged(self, index):
        self.scatterSelectionChanged.emit(self.combobox1.currentText(), self.combobox2.currentText())
        self.plotWidget.update()

    def updateSelectionBar(self):
        combobox1text = self.combobox1.currentText()
        combobox2text = self.combobox2.currentText()
        allnames = []
        for name in sorted(self.records):
            if not str(name) == str(self.removedname):
                allnames.append(name)
                if self.combobox1.findText(name) == -1:
                    self.combobox1.addItem(name)
                    self.combobox2.addItem(name)
        for index in range(self.combobox1.count()):
            if not self.combobox1.itemText(index) in allnames:
                self.combobox1.removeItem(index)
                self.combobox2.removeItem(index)
            else:
                if self.combobox1.itemText(index) == combobox1text:
                    self.combobox1.setCurrentIndex(index)
                if self.combobox2.itemText(index) == combobox2text:
                    self.combobox2.setCurrentIndex(index)

    def setPlotRate(self, value):
        self.plotrate = value
        self.plotRateLabel.setText('Plot Update Rate [' + str(self.plotrate) + ' Hz]:')
        self.plotThread.setInterval(1000 * 1 / value)

    def start(self, timer=1000):
        self.plotUpdate()
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def stop(self):
        self.plotThread.stop()

    def plotUpdate(self):
        if self.isVisible():
            self.plotWidget.update()

    def pausePlotting(self, value=True):
        self.paused = value
        self.plotWidget.togglePause(self.paused)

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

    def __init__(self, scatterplot, parent = None):
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
        self.decimateScale = 5000
        self.scatterplot.scatterSelectionChanged.connect(self.setSelectionIndex)
        self.plot = self.plotWidget.addPlot(row=0, col=0)
        self.scatterPlot = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None))
        self.plot.addItem(self.scatterPlot)
        self.scatterPlot.sigClicked.connect(self.printPoints)
        self.data1 = []
        self.data2 = []

    def printPoints(self,scatterPlot, points):
        point = points[0]
        text =  "{%0.3f, %0.3f}" % (point.pos()[0], point.pos()[1])
        print(text)
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
        else:
            self.data1 = []
            self.data2 = []
            self.scatterPlot.clear()
            self.createPlot('', '', 'w')

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
        self.plot.enableAutoRange()

    def removePlot(self, name):
        self.plotWidget.removeItem(self.plotWidget.getItem(0,0))

    def update(self):
        start = time.time()
        if not self.paused and not self.doingPlot:
            self.doingPlot  = True
            # self.plot.disableAutoRange()
            data1 = list(self.data1)
            # if len(data1) > self.decimateScale:
            #     del data1[:len(data1)-self.decimateScale]
            data2 = list(self.data2)
            # if len(data2) > self.decimateScale:
            #     del data2[:len(data2)-self.decimateScale]
            if len(data1) > 1 and len(data2) > 1:
                if data1[0][0] < data2[0][0]:
                    ans = takeClosestPosition(next(iter(zip(*data1))), data1, data2[0][0])
                    starttime = ans[1]
                    startpos1 = ans[0]
                    startpos2 = 0
                elif data1[0][0] > data2[0][0]:
                    ans = takeClosestPosition(next(iter(zip(*data2))), data2, data1[0][0])
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
                    x=list(x)
                    x2,y = zip(*data2)
                    y=list(y)
                    if len(x) > self.decimateScale:
                        # xy = zip(x,y)
                        del x[:len(x)-self.decimateScale]
                        del y[:len(y)-self.decimateScale]
                    self.scatterPlot.setData(x, y, pxMode=True, pen=None)
            self.doingPlot = False
        # self.plot.enableAutoRange()
