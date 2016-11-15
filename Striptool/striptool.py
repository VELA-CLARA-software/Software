import sys, time, os, datetime
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import threading
from threading import Thread, Event, Timer
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
import signal, datetime
from bisect import bisect_left, bisect_right

signal.signal(signal.SIGINT, signal.SIG_DFL)

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

def logthread(caller):
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
                              threading.current_thread().ident))

class repeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = 1000*interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.thread = QtCore.QThread()
        self.worker = repeatedWorker(interval, function, *args, **kwargs)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.loop)
        self.thread.start()
        self.thread.setPriority(QThread.TimeCriticalPriority)

    def setInterval(self, interval):
        self.worker.setInterval(interval)


class repeatedWorker(QtCore.QObject):
    def __init__(self, interval, function, *args, **kwargs):
        super(repeatedWorker, self).__init__()
        self.interval = 1000.0*interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.prev = 1000.0*time.clock();

    def loop(self):
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        newinterval = self.interval - ((1000.0*time.clock()) % self.interval)
        self.prev = 1000.0*time.clock()
        if newinterval < 0:
            self.timer.singleShot(0, self._target)
        else:
            self.timer.singleShot(newinterval, self._target)

    def stop(self):
        self.timer.stop()

    def _target(self):
        self.function(*self.args, **self.kwargs)
        newinterval = self.interval - ((1000.0*time.clock()) % self.interval)
        while newinterval < 0.2*self.interval:
            time.sleep(0.001)
            newinterval = self.interval - ((1000.0*time.clock()) % self.interval)
        self.timer.singleShot(newinterval, self._target)

    def setInterval(self, interval):
        self.interval = 1000*interval

class threadedFunction:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, worker):
        self.interval = 1000*interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.thread = QtCore.QThread()
        self.worker = worker
        self.worker.moveToThread(self.thread)
        self.thread.start()

class createSignalTimer(QObject):

    dataReady = QtCore.pyqtSignal(list)

    def __init__(self, name, function, *args):
        # Initialize the signal as a QObject
        QObject.__init__(self)
        self.function = function
        self.args = args
        self.name = name

    def startTimer(self, interval=1):
        self.timer = repeatedTimer(interval, self.update)

    def update(self):
        ''' call signal generating Function '''
        value = self.function(*self.args)
        self.dataReady.emit([time.time(),value])

class recordWorker(QtCore.QObject):
    def __init__(self, signal, name):
        super(recordWorker, self).__init__()
        self.signal = signal
        self.name = name
        self.signal.dataReady.connect(self.updateRecord)

    @QtCore.pyqtSlot(list)
    def updateRecord(self, value):
        global records
        if len(records[self.name]['data']) > 1 and value[1] == records[self.name]['data'][-1][1]:
            records[self.name]['data'][-1] = value
        else:
            records[self.name]['data'].append(value)

class createSignalRecord(QObject):

    def __init__(self, name, timer, function, *args):
        # Initialize the PunchingBag as a QObject
        QObject.__init__(self)
        global records
        if not 'records' in globals():
            records = {}
        records[name] = {'name': name, 'pen': 'r', 'timer': timer, 'function': function, 'ploton': True, 'data': []}
        self.name = name
        self.signal = createSignalTimer(name, function, *args)
        self.thread = QtCore.QThread()
        self.worker = recordWorker(self.signal, name)
        self.worker.moveToThread(self.thread)
        self.thread.start()
        self.signal.startTimer(timer)

    def setInterval(self, newinterval):
        self.signal.timer.setInterval(newinterval)

    def stop(self):
        self.signal.timer.stop()

class CAxisTime(pg.AxisItem):
    ## Formats axis label to human readable time.
    # @param[in] values List of \c time_t.
    # @param[in] scale Not used.
    # @param[in] spacing Not used.
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(CAxisTime, self).__init__(parent=parent, orientation=orientation, linkView=linkView)

    def tickStrings(self, values, scale, spacing):
        global dateTicksOn, fixedtimepoint, autoscroll
        if dateTicksOn:
            if autoscroll:
                reftime = time.time()
            else:
                reftime = fixedtimepoint
            strns = []
            for x in values:
                try:
                    strns.append(time.strftime("%H:%M:%S", time.localtime(reftime+x)))    # time_t --> time.struct_time
                except ValueError:  # Windows can't handle dates before 1970
                    strns.append('')
            return strns
        else:
            return values

class generalPlot(pg.PlotWidget):
    changePlotScale = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent = None):
        super(generalPlot, self).__init__(parent=parent)
        self.parent=parent
        self.linearPlot = True
        self.histogramPlot = False
        self.FFTPlot = False
        self.scatterPlot = False
        self.doingPlot = False
        self.usePlotRange = True
        self.autoscroll = True
        self.decimateScale = 5000
        self.legend = pg.LegendItem(size=(100,100))
        self.legend.setParentItem(None)

    def createPlot(self):
        global dateTicksOn
        dateTicksOn = True
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.date_axis = CAxisTime(orientation = 'bottom')
        self.plot = self.plotWidget.addPlot() #, axisItems = {'bottom': self.date_axis}
        nontimeaxisItems = {'bottom': self.plot.axes['bottom']['item'], 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.plot.axes['right']['item']}
        axisItems = {'bottom': self.date_axis, 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.plot.axes['right']['item']}
        self.plot.axes = {}
        for k, pos in (('top', (1,1)), ('bottom', (3,1)), ('left', (2,0)), ('right', (2,2))):
            if k in axisItems:
                axis = axisItems[k]
                axis.linkToView(self.plot.vb)
                self.plot.axes[k] = {'item': axis, 'pos': pos}
                self.plot.layout.removeItem(self.plot.layout.itemAt(*pos))
                self.plot.layout.addItem(axis, *pos)
                axis.setZValue(-1000)
                axis.setFlag(axis.ItemNegativeZStacksBehindParent)
        self.plot.showGrid(x=True, y=True)
        return self.plot

    def addCurve(self, plot, name):
        curve = self.curve(plot, name)
        return curve

    class curve(QObject):
        def __init__(self, plot, name):
            QObject.__init__(self)
            self.plotScale = None
            self.name = name
            self.plot = plot
            self.doingPlot = False
            self.curve = self.plot.plot.plot()
            self.addCurve()

        def addCurve(self):
            return self.curve

        def updateData(self, data, pen):
            if len(data) > 0 and not self.plot.scatterPlot:
                if self.plot.histogramPlot:
                    x,y = np.transpose(data)
                    y,x = np.histogram(y, bins=50)
                else:
                    x,y = np.transpose(data)
                if self.plot.histogramPlot:
                    self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=True, fillLevel=0)
                elif self.plot.FFTPlot:
                    self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=False)
                    self.plot.updateSpectrumMode(True)
                else:
                    self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=False)

        def timeFilter(self, datain, timescale):
            global plotRange
            if self.plot.autoscroll:
                currenttime = time.time()
            else:
                currenttime =  self.plot.currenttime#list(reversed(data))[0][0]#self.plot.currenttime
            data = map(lambda x: [x[0]-currenttime, x[1]], datain)
            def func1(values):
                for x in reversed(values):
                    if x[0] > (plotRange[0]) :
                        yield x
                    else:
                        break
            newlist = list(func1(data))
            for x in reversed(newlist):
                if x[0] < (plotRange[1]):
                    yield x
                else:
                    break

        def filterRecord(self, data, timescale):
            return list(list(self.timeFilter(data, timescale)))

        def clear(self):
            self.curve.clear()

        def update(self):
            global records, plotRange
            if not self.plot.paused and not self.doingPlot:
                self.doingPlot = True
                if records[self.name]['ploton']:
                    # start = time.clock()
                    self.plotData = self.filterRecord(records[self.name]['data'],plotRange)
                    if len(self.plotData) > 100*self.plot.decimateScale:
                        decimationfactor = int(np.floor(len(self.plotData)/self.plot.decimateScale))
                        self.plotData = self.plotData[0::decimationfactor]
                        # x,y = zip(*self.plotData)
                        # interp = scipy.interpolate.Akima1DInterpolator(x, y)
                        # xx = np.linspace(x[0], x[-1], self.plot.decimateScale)
                        # yy = interp(xx)
                        # self.plotData = zip(*[xx,yy])
                        # print self.plotData[0]
                        # print "decimated[", len(self.plotData), "] = ", decimationfactor
                        self.updateData(self.plotData, records[self.name]['pen'])
                    else:
                        self.updateData(self.plotData, records[self.name]['pen'])
                    # print "curve update = ", time.clock()- start,"[",1.0/(time.clock()- start)," Hz]"
                else:
                    self.clear()
                self.doingPlot = False
    def setPlotScale(self, timescale, padding=0.0):
        global plotRange
        if self.linearPlot:
            self.plotRange = timescale
            plotRange = list(timescale)
            self.plot.vb.setRange(xRange=plotRange, padding=0)

    def updatePlotScale(self, padding=0.0):
        global plotRange
        if self.linearPlot:
            vbPlotRange = self.plot.vb.viewRange()[0]
            if vbPlotRange != [0,1]:
                plotRange = self.plot.vb.viewRange()[0]
            self.plotRange = plotRange

    def show(self):
        self.plotWidget.show()

    def togglePause(self, value):
        self.paused = value

    def toggleAutoScroll(self, value):
        global fixedtimepoint
        self.autoscroll = value
        if not value:
            self.currenttime = currentPlotTime
            fixedtimepoint = currentPlotTime
    #
    def updateScatterPlot(self):
        if self.scatterPlot and not self.doingPlot:
            self.doingPlot = True
            # self.legend.setParentItem(self.plot)
            # self.legend.items = []
            scatteritemnames=[]
            scatteritems=[]
            color=0
            global records
            for name in records:
                if records[name]['ploton']:
                    scatteritemnames.append(name)
            self.plot.clear()
            start = time.clock()
            for i in range(len(scatteritemnames)):
                for j in range(i+1, len(scatteritemnames)):
                    data1 = records[scatteritemnames[i]]['curve'].plotData
                    # print len(data1)
                    data2 = records[scatteritemnames[j]]['curve'].plotData
                    # print len(data2)
                    signalDelayTime1 = records[scatteritemnames[i]]['timer']
                    signalDelayTime2 = records[scatteritemnames[j]]['timer']
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
                    s1 = pg.ScatterPlotItem(x=x, y=y, size=2, pen=pg.mkPen(None), brush=pg.mkBrush(Qtableau20[color]))
                    # self.legend.addItem(s1, plotname)
                    color += 1
                    self.plot.addItem(s1)
            # print "histogram = ", time.clock()- start,"[",1.0/(time.clock()- start)," Hz]"
            self.doingPlot = False

class stripLegend(pg.TreeWidget):
    def __init__(self, parent = None):
        super(stripLegend, self).__init__(parent)
        self.layout = pg.TreeWidget()
        self.layout.header().close()
        self.layout.setColumnCount(2)
        self.layout.header().setResizeMode(0,QtGui.QHeaderView.Stretch)
        self.layout.setColumnWidth(2,50)
        self.layout.header().setStretchLastSection(False)
        self.newRowNumber = 0
        self.deleteIcon  = QtGui.QIcon(str(os.path.dirname(os.path.abspath(__file__)))+'\delete.png')

    def addTreeWidget(self, parent, name, text, widget):
        child = QtGui.QTreeWidgetItem()
        child.setText(0, text)
        parent.addChild(child)
        self.layout.setItemWidget(child,1,widget)
        return child

    def addLegendItem(self, name):
        global records
        parentTreeWidget = QtGui.QTreeWidgetItem([name])
        self.layout.addTopLevelItem(parentTreeWidget)
        plotOnOff = QCheckBox()
        plotOnOff.setChecked(True)
        plotOnOff.toggled.connect(lambda x: self.togglePlotOnOff(name, x))
        self.addTreeWidget(parentTreeWidget, name, "Plot On?", plotOnOff)
        signalRate = QComboBox()
        signalRate.setFixedSize(80,25)
        signalRate.setStyleSheet("subcontrol-origin: padding;\
        subcontrol-position: top right;\
        width: 15px;\
        border-left-width: 0px;\
        border-left-color: darkgray;\
        border-left-style: solid;\
        border-top-right-radius: 3px; /* same radius as the QComboBox */\
        border-bottom-right-radius: 3px;\
         ")
        i = 0
        selected = 0
        for rate in [0.1,1,5,10,25,50,100]:
            signalRate.addItem(str(rate)+' Hz')
            if records[name]['timer'] == 1.0/rate:
                selected = i
            i += 1
        signalRate.setCurrentIndex(selected)
        signalRate.currentIndexChanged.connect(lambda x: self.changeSampleRate(name, signalRate))
        self.addTreeWidget(parentTreeWidget, name, "Signal Rate", signalRate)
        colorbox = pg.ColorButton()
        colorbox.setFixedSize(30,25)
        colorbox.setFlat(True)
        colorbox.setColor(records[name]['pen'])
        colorbox.sigColorChanged.connect(lambda x: self.changePenColor(name, x))
        colorbox.sigColorChanging.connect(lambda x: self.changePenColor(name, x))
        self.addTreeWidget(parentTreeWidget, name, "Plot Color", colorbox)
        saveButton = QPushButton('Save Data')
        saveButton.setFixedSize(74,20)
        saveButton.setFlat(True)
        saveButton.clicked.connect(lambda x: self.saveCurve(name))
        self.addTreeWidget(parentTreeWidget, name, "Save Signal", saveButton)
        resetButton = QPushButton('Clear')
        resetButton.setFixedSize(50,20)
        resetButton.setFlat(True)
        resetButton.clicked.connect(lambda x: self.clearCurve(name))
        self.addTreeWidget(parentTreeWidget, name, "Clear Signal", resetButton)
        deleteRowButton = QPushButton()
        deleteRowButton.setFixedSize(50,20)
        deleteRowButton.setFlat(True)
        deleteRowButton.setIcon(self.deleteIcon)
        deleteRowChild = self.addTreeWidget(parentTreeWidget, name, "Delete Signal", deleteRowButton)
        deleteRowButton.clicked.connect(lambda x: self.deleteRow(name, deleteRowChild))
        self.newRowNumber += 1

    def formatCurveData(self, name):
        return [(str(time.strftime('%Y/%m/%d', time.localtime(x[0]))),str(datetime.datetime.fromtimestamp(x[0]).strftime('%H:%M:%S.%f')),x[1]) for x in records[name]['data']]

    def saveCurve(self, name):
        global records
        saveFileName = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Array ['+name+']', name, filter="CSV files (*.csv);; Binary Files (*.bin)", selectedFilter="CSV files (*.csv)"))
        filename, file_extension = os.path.splitext(saveFileName)
        saveData = self.formatCurveData(name)
        if file_extension == '.csv':
        #     print "csv!"
            fmt='%s, %s, %.18e'
            target = open(saveFileName,'w')
            for row in saveData:
                target.write((fmt % tuple(row))+'\n')
            target.close()
        elif file_extension == '.bin':
            # print "bin!"
            np.array(records[name]['data']).tofile(saveFileName)
        else:
            # print "other..."
            np.save(saveFileName,np.array(records[name]['data']))

    def changePenColor(self, name, widget):
        global records
        records[name]['pen'] = widget._color

    def togglePlotOnOff(self, name, value):
        global records
        records[name]['ploton'] = value

    def changeSampleRate(self, name, widget):
        global records
        string = str(widget.currentText())
        number = [int(s) for s in string.split() if s.isdigit()][0]
        value = 1.0/float(number)
        records[name]['timer'] = value
        records[name]['record'].setInterval(value)

    def clearCurve(self, name):
        records[name]['data'] = []
        records[name]['curve'].clear()

    def deleteRow(self, name, child):
        global records
        row = self.layout.indexOfTopLevelItem(child.parent())
        self.layout.takeTopLevelItem(row)
        records[name]['record'].stop()
        self.clearCurve(name)
        del records[name]

class stripPlot(QWidget):

    def __init__(self, parent = None):
        super(stripPlot, self).__init__(parent)
        global plotRange, usePlotRange, autoscroll
        usePlotRange = True
        plotRange = None
        autoscroll = True
        self.paused = True
        self.signalLength = 10
        self.plotrate = 1
        self.plotScaleConnection = True
        self.pauseIcon  = QtGui.QIcon(str(os.path.dirname(os.path.abspath(__file__)))+'\pause.png')
        self.stripPlot = QtGui.QGridLayout()
        self.plotThread = QTimer()
        self.plotWidget = generalPlot(self.parent())
        self.plot = self.plotWidget.createPlot()
        self.stripPlot.addWidget(self.plotWidget.plotWidget,0, 0,5,8)
        ''' Sidebar for graph type selection '''
        self.buttonLayout = QtGui.QVBoxLayout()
        self.linearRadio = QRadioButton("Linear")
        self.linearRadio.setChecked(True)
        self.linearRadio.toggled.connect(lambda: self.setPlotType(linear=True))
        self.buttonLayout.addWidget(self.linearRadio,0)
        self.HistogramRadio = QRadioButton("Histogram")
        self.HistogramRadio.toggled.connect(lambda: self.setPlotType(histogram=True))
        self.buttonLayout.addWidget(self.HistogramRadio,1)
        self.FFTRadio = QRadioButton("FFT")
        self.FFTRadio.toggled.connect(lambda: self.setPlotType(FFT=True))
        self.buttonLayout.addWidget(self.FFTRadio,2)
        self.ScatterRadio = QRadioButton("Scatter")
        self.ScatterRadio.toggled.connect(lambda: self.setPlotType(scatter=True))
        self.buttonLayout.addWidget(self.ScatterRadio,3)
        ''' Create H Layout for scroll/pause '''
        self.autoscrollPauseLayout = QtGui.QHBoxLayout()
        ''' Add Autoscroll checkbox '''
        self.scrollButton = QCheckBox()
        self.scrollButton.setChecked(True)
        self.scrollButtonLabel = QtGui.QLabel()
        self.scrollButtonLabel.setText('Autoscroll')
        self.scrollButtonLabel.setAlignment(Qt.AlignCenter)
        self.scrollButton.toggled.connect(self.toggleAutoScroll)
        self.autoscrollPauseLayout.addWidget(self.scrollButtonLabel,0)
        self.autoscrollPauseLayout.addWidget(self.scrollButton,1)
        ''' Add Pause Button '''
        self.pauseButton = QPushButton()
        self.pauseButton.setIcon(self.pauseIcon)
        self.pauseButton.setFixedSize(50,20)
        self.pauseButton.setStyleSheet("border: 5px; background-color: white")
        # self.pauseButton.setFlat(False)
        self.pauseButton.clicked.connect(self.togglePause)
        self.autoscrollPauseLayout.addWidget(self.pauseButton,2)
        ''' Add scroll/pause to main layout '''
        self.buttonLayout.addLayout(self.autoscrollPauseLayout,3)
        self.legend = stripLegend()
        self.buttonLayout.addWidget(self.legend.layout,4)
        ''' Add sidebar  to main layout'''
        self.stripPlot.addLayout(self.buttonLayout,0, 8,5,2)
        self.setupPlotRateSlider()
        self.stripPlot.addWidget(self.plotRateLabel,5, 2,1,1)
        self.stripPlot.addWidget(self.plotRateSlider,5, 3,1,1)
        self.setLayout(self.stripPlot)
        self.togglePause()
        self.plotThread.timeout.connect(lambda: self.plotWidget.date_axis.linkedViewChanged(self.plotWidget.date_axis.linkedView()))
        self.plotWidget.plot.vb.sigXRangeChanged.connect(self.setPlotScaleLambda)
        # self.plotThread.timeout.connect(self.plotWidget.updateScatterPlot)


    def setupPlotRateSlider(self):
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

    def setPlotRate(self, value):
        self.plotrate = value
        self.plotRateLabel.setText('Plot Update Rate ['+str(self.plotrate)+' Hz]:')
        self.plotThread.setInterval(1000*1/value)

    def setPlotScaleLambda(self, widget, timescale):
        if self.plotScaleConnection:
            self.plotWidget.setPlotScale(timescale)

    def setPlotType(self, linear=False, histogram=False, FFT=False, scatter=False):
        global dateTicksOn
        self.plotScaleConnection = False
        if not(self.plotWidget.linearPlot == linear and self.plotWidget.histogramPlot == histogram and self.plotWidget.FFTPlot == FFT and self.plotWidget.scatterPlot == scatter):
            self.plotWidget.linearPlot = linear
            self.plotWidget.histogramPlot = histogram
            self.plotWidget.FFTPlot = FFT
            self.plotWidget.scatterPlot = scatter
            if scatter:
                dateTicksOn = False
                self.plotWidget.updateScatterPlot()
                self.plot.enableAutoRange()
                # self.plotWidget.updateScatterPlot()
            else:
                try:
                    self.plotWidget.legend.scene().removeItem(self.plotWidget.legend)
                except:
                    pass
                self.plot.clear()
                for name in records:
                    # print records[name]['curve'].curve
                    self.plot.addItem(records[name]['curve'].curve)
                self.plot.updateSpectrumMode(False)
                for name in records:
                    records[name]['curve'].update()
                if FFT:
                    self.plot.updateSpectrumMode(True)
                else:
                    self.plot.updateSpectrumMode(False)
                if not linear:
                    dateTicksOn = False
                    self.plot.enableAutoRange()
                else:
                    dateTicksOn = True
                    self.plot.disableAutoRange()
                    self.plotWidget.setPlotScale([self.plotWidget.plotRange[0],self.plotWidget.plotRange[1]])
                    self.plotScaleConnection = True

    def start(self, timer=1000):
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def addSignal(self, name, pen, timer, function, *args):
        global records
        signalrecord = createSignalRecord(name=name, timer=timer, function=function, *args)
        records[name]['record'] = signalrecord
        curve = self.plotWidget.addCurve(self.plotWidget, name)
        records[name]['curve'] = curve
        records[name]['pen'] = pen
        self.legend.addLegendItem(name)

    def plotUpdate(self):
        global records, currentPlotTime
        currentPlotTime = time.time()
        for name in records:
            records[name]['curve'].update()
        self.plotWidget.updateScatterPlot()

    def removeSignal(self,name):
        global records
        self.plotThread.timeout.disconnect(records[name]['curve'].update)
        del records[name]

    def setPlotScale(self, timescale):
        self.plotWidget.setPlotScale([-1.05*timescale, 0.05*timescale])

    def pausePlotting(self, value=True):
        self.paused = value
        self.plotWidget.togglePause(self.paused)

    def togglePause(self):
        if self.paused:
            self.paused = False
            self.pauseButton.setStyleSheet("border: 5px; background-color: white")
        else:
            self.paused = True
            self.pauseButton.setStyleSheet("border: 5px; background-color: red")
        self.plotWidget.togglePause(self.paused)

    def toggleAutoScroll(self):
        global autoscroll
        autoscroll = self.scrollButton.isChecked()
        self.plotWidget.toggleAutoScroll(self.scrollButton.isChecked())

    def setDecimateLength(self, value=5000):
        self.plotWidget.decimateScale = value
