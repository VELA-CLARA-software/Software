import sys, time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import threading
from threading import Thread, Event, Timer
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
import signal, datetime

signal.signal(signal.SIGINT, signal.SIG_DFL)

class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = 0.0 #time.time()
        self.event = Event()
        self.thread = threading.Thread(target=self._target)
        self.thread.daemon = True
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)
            time.sleep(0.0001)

    @property
    def _time(self):
        if (self.interval) - ((time.time()) % self.interval) < 0.0001:
            return self.interval
        else:
            return (self.interval) - ((time.time()) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()

class createSignalTimer(QObject):

    def __init__(self, name, function, *args):
        # Initialize the signal as a QObject
        QObject.__init__(self)
        self.function = function
        self.args = args
        self.name = name

    def startTimer(self, interval=1):
        self.timer = RepeatedTimer(interval, self.update)

    def update(self):
        ''' call signal generating Function '''
        value = self.function(*self.args)
        global records
        records[self.name]['data'].append([time.time(), value])

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
        self.signal.startTimer(timer)

    def setInterval(self, newinterval):
        self.signal.timer.interval = newinterval

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
        global dateTicksOn, currenttime, autoscroll
        if dateTicksOn:
            if autoscroll:
                reftime = time.time()
            else:
                reftime = currenttime
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
        self.usePlotRange = True
        self.autoscroll = True
        self.decimateScale = 5000

    def createPlot(self):
        global dateTicksOn
        dateTicksOn = True
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.date_axis = CAxisTime(orientation = 'bottom')
        self.plot = self.plotWidget.addPlot(row=0, column=0, axisItems = {'bottom': self.date_axis}) #, axisItems = {'bottom': self.date_axis}
        # self.plot.vb.setMouseEnabled(False, True)
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
            self.curve = self.plot.plot.plot()
            self.addCurve()

        def addCurve(self):
            return self.curve

        def updateData(self, data, pen):
            global currenttime
            if self.plot.autoscroll:
                currenttime = time.time()
            else:
                currenttime = self.plot.currenttime
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
            return list(self.timeFilter(data, timescale))

        def clear(self):
            self.curve.clear()

        def time_it(f, *args):
            start = time.clock()
            f(*args)
            return (time.clock() - start)*1000

        def update(self):
            global records, plotRange
            if not self.plot.paused:
                if records[self.name]['ploton']:
                    data = self.filterRecord(records[self.name]['data'],plotRange)
                    if len(data) > 2*self.plot.decimateScale:
                        decimate = int(np.floor(len(data)/self.plot.decimateScale))
                        print "decimate[", len(data), "] = ", decimate
                        self.updateData(data[0::decimate], records[self.name]['pen'])
                    else:
                        self.updateData(data, records[self.name]['pen'])
                    # self.updateData(records[self.name]['data'],records[self.name]['pen'])
                else:
                    self.clear()

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
        self.autoscroll = value
        if not value:
            self.currenttime = time.time()

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
        self.deleteIcon  = QtGui.QIcon('delete.png')

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
        # self.layout.setCellWidget(self.newRowNumber, 0, self.plotOnOff)
        # self.layout.setCellWidget(self.newRowNumber, 1, self.rowLabel)
        # self.layout.setCellWidget(self.newRowNumber, 2, signalRate)
        # self.layout.setCellWidget(self.newRowNumber, 3, self.colorbox)
        # self.layout.setCellWidget(self.newRowNumber, 4, resetButton)
        # self.layout.setCellWidget(self.newRowNumber, 5, deleteRowButton)
        # # item = self.layout.takeItem(self.newRowNumber, 4)
        # # deleteRowButton.clicked.connect(lambda x: self.deleteRow(name))
        self.newRowNumber += 1

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
        self.pauseIcon  = QtGui.QIcon('pause.png')
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

    def setPlotType(self, linear=False, histogram=False, FFT=False):
        global dateTicksOn
        self.plotScaleConnection = False
        if not(self.plotWidget.linearPlot == linear and self.plotWidget.histogramPlot == histogram and self.plotWidget.FFTPlot == FFT):
            self.plotWidget.linearPlot = linear
            self.plotWidget.histogramPlot = histogram
            self.plotWidget.FFTPlot = FFT
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

    def addSignal(self, name, pen, timer, function, *args):
        global records
        signalrecord = createSignalRecord(name=name, timer=timer, function=function, *args)
        records[name]['record'] = signalrecord
        curve = self.plotWidget.addCurve(self.plotWidget, name)
        records[name]['curve'] = curve
        records[name]['pen'] = pen
        self.plotThread.timeout.connect(records[name]['curve'].update)
        self.legend.addLegendItem(name)

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
