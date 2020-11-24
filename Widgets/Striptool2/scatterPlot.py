import sys, time, os, datetime, signal
import numpy as np
import pyqtgraph as pg
sys.path.append("../../../")
import Software.Procedures.qt as qt
from bisect import bisect_left
from scipy.stats import pearsonr
from collections import deque
# logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


# def logthread(caller):
#     print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
#                               threading.current_thread().ident))

class scatterPlot(qt.QWidget):
    scatterSelectionChanged = qt.pyqtSignal('QString', 'QString', int, int)

    def __init__(self, generalplot, parent=None, plotRateBar=False):
        super(scatterPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.plotrate = 1
        ''' create the scatterPlot as a grid layout '''
        self.scatterPlot = qt.QVBoxLayout()
        self.plotThread = qt.QTimer()
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

    def setupSelectionBar(self):
        spacer = qt.QSpacerItem(25, 20)
        self.combobox1 = qt.QComboBox()
        self.combobox1.setMaximumWidth(200)
        self.combobox1.setMinimumWidth(100)
        self.combobox1.currentIndexChanged.connect(self.selectionBarChanged)
        self.combobox2 = qt.QComboBox()
        self.combobox2.setMaximumWidth(200)
        self.combobox2.setMinimumWidth(100)
        self.combobox2.currentIndexChanged.connect(self.selectionBarChanged)
        for name in sorted(self.records):
            self.combobox1.addItem(name)
            self.combobox2.addItem(name)
        self.combobox1.setCurrentIndex(0)
        self.combobox2.setCurrentIndex(1)
        self.resetButton = qt.QPushButton('Clear')
        self.resetButton.clicked.connect(self.resetButtonPushed)
        self.offsetSpinBox = qt.QSpinBox()
        self.offsetSpinBox.setMinimum(-1000000)
        self.offsetSpinBox.setMaximum(1000000)
        self.offsetSpinBox.setSingleStep(1)
        self.offsetSpinBoxLabel = qt.QPushButton('Offset')
        self.offsetSpinBoxLabel.setFlat(True)
        self.offsetSpinBoxLabel.clicked.connect(lambda x: self.offsetSpinBox.setValue(0))
        self.offsetSpinBoxWidget = qt.QWidget()
        self.offsetSpinBoxWidgetLayout = qt.QHBoxLayout()
        self.offsetSpinBoxWidgetLayout.addWidget(self.offsetSpinBoxLabel)
        self.offsetSpinBoxWidgetLayout.addWidget(self.offsetSpinBox)
        self.offsetSpinBox.valueChanged.connect(self.selectionBarChanged)
        #
        self.decimateSpinBox = qt.QComboBox()
        for i in range(4,20):
            val = int((2**(i)))
            if val < 2000:
                self.decimateSpinBox.addItem(str(val)+'', val)
            else:
                self.decimateSpinBox.addItem(str(int(val/1000))+'k', val)
        self.decimateSpinBox.setCurrentIndex(11)
        self.decimateSpinBox.currentIndexChanged.connect(self.selectionBarChanged)
        #
        self.selectionBarLayout = qt.QHBoxLayout()
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.combobox1)
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.combobox2)
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.resetButton)
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addLayout(self.offsetSpinBoxWidgetLayout)
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.decimateSpinBox)

    def selectionBarChanged(self, index):
        decimate = 2**(4+self.decimateSpinBox.currentIndex())
        self.scatterSelectionChanged.emit(self.combobox1.currentText(), self.combobox2.currentText(), self.offsetSpinBox.value(), decimate)
        self.plotWidget.update()

    def updateSelectionBar(self):
        combobox1text = self.combobox1.currentText()
        combobox2text = self.combobox2.currentText()
        allnames = []
        for name in sorted(self.records):
            if not str(name) == str(self.removedname):
                for append in ['','Mean10', 'Mean100', 'Mean1000']:
                    newname = name+append
                    allnames.append(newname)
                    if self.combobox1.findText(newname) == -1:
                        self.combobox1.addItem(newname)
                        self.combobox2.addItem(newname)
        for index in range(self.combobox1.count()):
            if not self.combobox1.itemText(index) in allnames:
                self.combobox1.removeItem(index)
                self.combobox2.removeItem(index)
            else:
                if self.combobox1.itemText(index) == combobox1text:
                    self.combobox1.setCurrentIndex(index)
                if self.combobox2.itemText(index) == combobox2text:
                    self.combobox2.setCurrentIndex(index)
        self.removedname = ''

    def setPlotRate(self, value):
        self.plotrate = value
        self.plotRateLabel.setText('Plot Update Rate [' + str(self.plotrate) + ' Hz]:')
        self.plotThread.setInterval(1000 * 1 / value)

    def start(self, timer=1000, offset=500):
        if not hasattr(self, 'slept'):
            time.sleep(offset/1000.)
            self.slept = True
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

    def resetButtonPushed(self):
        self.plotWidget.setCutoff()

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

    statusChanged = qt.pyqtSignal(str)

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
        self.decimateScale = 32768
        self.scatterplot.scatterSelectionChanged.connect(self.setSelectionIndex)
        self.plot = self.plotWidget.addPlot(row=0, col=0)
        self.scatterPlot = pg.ScatterPlotItem(size=5, pen=pg.mkPen(None))
        self.plot.addItem(self.scatterPlot)
        self.scatterPlot.sigClicked.connect(self.printPoints)
        self.data1 = []
        self.data2 = []
        self.cutoff = 0

    def printPoints(self,scatterPlot, points):
        point = points[0]
        text =  "{%0.3f, %0.3f}" % (point.pos()[0], point.pos()[1])
        # print(text)
        self.statusChanged.emit(text)

    def isSelectionInRecords(self, selection):
        if 'Mean1000' in selection:
            selection = selection.replace('Mean1000','')
        elif 'Mean100' in selection:
            selection = selection.replace('Mean100','')
        elif 'Mean10' in selection:
            selection = selection.replace('Mean10','')
        return selection in self.records

    def getDataIfMean(self, selection):
        recordname = 'data'
        if 'Mean1000' in selection:
            selection = selection.replace('Mean1000','')
            recordname = 'dataMean1000'
        elif 'Mean100' in selection:
            selection = selection.replace('Mean100','')
            recordname = 'dataMean100'
        elif 'Mean10' in selection:
            selection = selection.replace('Mean10','')
            recordname = 'dataMean10'
        return self.records[selection]['timer'], self.records[selection][recordname]

    def setSelectionIndex(self, x, y, offset, decimate):
        self.selectionNameX = str(x)
        self.selectionNameY = str(y)
        self.selectionOffset = int(offset)
        # print(decimate)
        self.decimateScale = int(decimate)
        if self.isSelectionInRecords(self.selectionNameX) and self.isSelectionInRecords(self.selectionNameY):
            self.signalDelayTime1, self.data1 = self.getDataIfMean(self.selectionNameX)
            self.signalDelayTime2, self.data2 = self.getDataIfMean(self.selectionNameY)
            self.createPlot(self.selectionNameX, self.selectionNameY, self.color)
        else:
            self.data1 = []
            self.data2 = []
            self.scatterPlot.clear()
            self.createPlot('', '', 'w')

    def togglePause(self, value):
        self.paused = value

    def show(self):
        self.plotWidget.show()

    def createPlot(self, label1, label2, color):
        self.titleBaseName = label1+' vs '+label2
        self.plot.setLabel('bottom',label1)
        self.plot.setLabel('left',label2)
        self.plot.setTitle(self.titleBaseName)
        self.plot.showGrid(x=True, y=True)
        self.plot.enableAutoRange()

    def removePlot(self, name):
        self.plotWidget.removeItem(self.plotWidget.getItem(0,0))

    def setCutoff(self):
        self.cutoff = time.time()

    def rotate(self, l, x):
      return l[-x:] + l[:-x]

    def update(self):
        start = time.time()
        if not self.paused and not self.doingPlot:
            self.doingPlot  = True
            # self.plot.disableAutoRange()
            data1 = list(self.data1)
            if len(data1) > self.decimateScale:
                del data1[:len(data1)-self.decimateScale]
            data2 = list(self.data2)
            if len(data2) > self.decimateScale:
                del data2[:len(data2)-self.decimateScale]
            if len(data1) > 1 and len(data2) > 1:
                cutpos = takeClosestPosition(next(iter(zip(*data1))), data1, self.cutoff)
                del data1[:cutpos[0]]
                cutpos = takeClosestPosition(next(iter(zip(*data2))), data2, self.cutoff)
                del data2[:cutpos[0]]
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
                if self.signalDelayTime1 != self.signalDelayTime2:
                    if self.signalDelayTime1 < self.signalDelayTime2:
                        tmpdata1 = list(zip(*data1))[0]
                        data1 = [takeClosestPosition(tmpdata1, data1, timeval[0])[1] for timeval in data2]
                    else:
                        tmpdata2 = list(zip(*data2))[0]
                        data2 = [takeClosestPosition(tmpdata2, data2, timeval[0])[1] for timeval in data1]
                    # if self.signalDelayTime1 > self.signalDelayTime2:
                    #     ratio = int(self.signalDelayTime1 / self.signalDelayTime2)
                    #     print('ratio = ', ratio)
                    #     data1 = list(reversed(list(reversed(data1))[0::ratio]))
                    # else:
                    #     ratio = int(self.signalDelayTime2 / self.signalDelayTime1)
                    #     print('ratio = ', ratio)
                    #     data2 = list(reversed(list(reversed(data2))[0::ratio]))
                if self.selectionOffset > 0:
                    del data1[-abs(self.selectionOffset):]
                    del data2[:abs(self.selectionOffset)]
                if self.selectionOffset < 0:
                    del data2[-abs(self.selectionOffset):]
                    del data1[:abs(self.selectionOffset)]
                # if self.selectionOffset < 0:
                #     data2d = deque(data2)
                #     data2d.rotate(self.selectionOffset)
                #     data2 = list(data2d)
                # del data1[:abs(self.selectionOffset)]
                # del data2[:abs(self.selectionOffset)]
                if len(data1) > len(data2):
                    del data1[len(data2) - len(data1):]
                elif len(data2) > len(data1):
                    del data2[len(data1) - len(data2):]
                if len(data1) > 1 and len(data2) > 1:
                    x1,x = list(zip(*data1))
                    x=list(x)
                    x2,y = list(zip(*data2))
                    y=list(y)
                    start = time.time()
                    pr = pearsonr(x,y)
                    try:
                        self.scatterPlot.setData(x, y, pxMode=True, pen=None)
                    except:
                        pass
                    self.plot.setTitle(self.titleBaseName + ' (pr='+str(np.round(pr[0], decimals=3))+')')
            self.doingPlot = False
        # self.plot.enableAutoRange()
