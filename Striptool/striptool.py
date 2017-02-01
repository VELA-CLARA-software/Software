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
import logging
from striptoolRecord import *
from striptoolLegend import *
from striptoolPlot import *

logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)

def logthread(caller):
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
                              threading.current_thread().ident))

class stripPlot(QWidget):

    signalAdded = QtCore.pyqtSignal('QString')
    signalRemoved = QtCore.pyqtSignal('QString')

    def __init__(self, parent = None, plotRateBar=True):
        super(stripPlot, self).__init__(parent)
        self.pg = pg
        self.paused = True
        self.signalLength = 10
        self.plotrate = 1
        self.plotScaleConnection = True
        self.pauseIcon  =  QtGui.QIcon(str(os.path.dirname(os.path.abspath(__file__)))+'\icons\pause.png')

        ''' create the stripPlot.stripPlot as a grid layout '''
        self.stripPlot = QtGui.QGridLayout()
        self.plotThread = QTimer()
        ''' Create generalPlot object '''
        self.plotWidget = generalPlot(self)
        ''' Create the plot as part of the plotObject '''
        self.plot = self.plotWidget.createPlot()
        ''' Create the signalRecord object '''
        self.records = {}

        ''' Sidebar for graph type selection '''
        self.buttonLayout = QtGui.QGridLayout()
        self.linearRadio = QRadioButton("Linear")
        self.linearRadio.setChecked(True)
        self.linearRadio.toggled.connect(lambda: self.setPlotType(linear=True))
        ''' Histogram '''
        self.HistogramRadio = QRadioButton("Histogram")
        self.HistogramRadio.toggled.connect(lambda: self.setPlotType(histogram=True))
        self.histogramCheckbox = QCheckBox("Subtract Mean")
        self.histogramCheckbox.stateChanged.connect(self.setSubtractMean)
        self.histogramCheckbox.setChecked(False)
        self.histogramBinsLabel = QLabel('NBins')
        self.histogramBinsEdit = QLineEdit(str(self.plotWidget.numberBins))
        self.histogramBinsEdit.setMaxLength(4)
        self.histogramBinsEdit.setInputMask('0000')
        self.histogramBinsEdit.editingFinished.connect(self.setHistogramBins)
        ''' FFT'''
        self.FFTRadio = QRadioButton("FFT")
        self.FFTRadio.toggled.connect(lambda: self.setPlotType(FFT=True))
        ''' Create H Layout for scroll/pause '''
        self.autoscrollPauseLayout = QtGui.QHBoxLayout()
        ''' Add Autoscroll checkbox '''
        self.scrollButton = QCheckBox("Autoscroll")
        self.scrollButton.setChecked(True)
        self.scrollButton.toggled.connect(self.toggleAutoScroll)
        ''' Add Pause Button '''
        self.pauseButton = QPushButton()
        self.pauseButton.setIcon(self.pauseIcon)
        self.pauseButton.setFixedSize(50,20)
        self.pauseButton.setStyleSheet("border: 5px; background-color: white")
        self.pauseButton.clicked.connect(self.togglePause)
        ''' Initialise stripLegend Object '''
        self.legend = stripLegend(stripTool=self)
        ''' Set Layout '''
        self.buttonLayout.addWidget(self.linearRadio,      0,0,1,4)
        self.buttonLayout.addWidget(self.HistogramRadio,   1,0,1,1)
        self.buttonLayout.addWidget(self.histogramCheckbox,1,1,1,1)
        self.buttonLayout.addWidget(self.histogramBinsLabel,1,3,1,1)
        self.buttonLayout.addWidget(self.histogramBinsEdit,1,2,1,1)
        self.buttonLayout.addWidget(self.FFTRadio,         2,0,1,4)
        self.buttonLayout.addWidget(self.scrollButton,     3,0,1,1)
        self.buttonLayout.addWidget(self.pauseButton,      3,3,1,1)
        self.buttonLayout.addWidget(self.legend.layout,4,0,3,4)
        ''' Add sidebar  to main layout'''
        self.GUISplitter = QtGui.QSplitter()
        self.GUISplitter.setHandleWidth(10)
        self.GUISplitter.addWidget(self.plotWidget.plotWidget)
        self.buttonFrame = QtGui.QFrame()
        self.buttonFrame.setLayout(self.buttonLayout)
        self.GUISplitter.addWidget(self.buttonFrame)
        self.GUISplitter.setStyleSheet("QSplitter::handle{background-color:transparent;}");
        handle = self.GUISplitter.handle(1)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.splitterbutton = QtGui.QToolButton(handle)
        self.splitterbutton.setArrowType(QtCore.Qt.LeftArrow)
        self.splitterbutton.clicked.connect(
            lambda: self.handleSplitterButton(False))
        self.GUISplitter.splitterMoved.connect(self.handleSplitterButtonArrow)
        layout.addWidget(self.splitterbutton)
        handle.setLayout(layout)
        self.GUISplitter.setStretchFactor(0,4)
        self.GUISplitter.setStretchFactor(1,1)
        self.handleSplitterButton(left=True)
        self.stripPlot.addWidget(self.GUISplitter,0,0,5,2)
        self.setupPlotRateSlider()
        if plotRateBar:
            self.stripPlot.addWidget(self.plotRateLabel,5, 0)
            self.stripPlot.addWidget(self.plotRateSlider,5, 1)
        self.setLayout(self.stripPlot)
        self.plotThread.timeout.connect(lambda: self.plotWidget.date_axis.linkedViewChanged(self.plotWidget.date_axis.linkedView()))
        self.plotWidget.plot.vb.sigXRangeChanged.connect(self.setPlotScaleLambda)
        logger.debug('stripPlot initiated!')

    def setHistogramBins(self):
        self.plotWidget.numberBins = int(self.histogramBinsEdit.text())

    def setSubtractMean(self):
        self.subtractMean = self.histogramCheckbox.isChecked()

    def saveAllCurves(self, saveFileName=None):
        for name in self.records:
            if self.records[name]['parent'] == self:
                filename, file_extension = os.path.splitext(saveFileName)
                saveFileName2 = filename + '_' + self.records[name]['name'] + file_extension
                self.legend.saveCurve(self.records[name]['name'],saveFileName2)

    def saveCurve(self, name, saveFileName=None):
        self.legend.saveCurve(name,saveFileName)

    def setWidth(self, width=16777215):
        self.stripPlot.setMaximumWidth(width)

    def setHeight(self, height=16777215):
        self.stripPlot.setMaximumHeight(height)

    def setWidthHeight(self, height, width):
        self.setWidth(width)
        self.setHeight(height)

    def setQSize(self, heightwidth):
        self.setWidth(0.95*heightwidth.width())
        self.setHeight(0.95*heightwidth.height())

    def handleSplitterButton(self, left=True):
        # width = self.GUISplitter.size().width()
        if left:
            self.GUISplitter.setStretchFactor(0,1)
            self.GUISplitter.setStretchFactor(1,0)
            self.GUISplitter.setSizes([1,0])
        elif not all(self.GUISplitter.sizes()):
            self.GUISplitter.setStretchFactor(0,4)
            self.GUISplitter.setStretchFactor(1,1)
            self.GUISplitter.setSizes([1000,1])
        else:
            self.GUISplitter.setStretchFactor(0,1)
            self.GUISplitter.setStretchFactor(1,0)
            self.GUISplitter.setSizes([1,0])
        self.handleSplitterButtonArrow()

    def handleSplitterButtonArrow(self):
        sizes = self.GUISplitter.sizes()
        if self.GUISplitter.sizes()[1] > 0:
            self.splitterbutton.setArrowType(QtCore.Qt.RightArrow)
        else:
            self.splitterbutton.setArrowType(QtCore.Qt.LeftArrow)

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
        self.plotScaleConnection = False
        if not(self.plotWidget.linearPlot == linear and self.plotWidget.histogramPlot == histogram and self.plotWidget.FFTPlot == FFT and self.plotWidget.scatterPlot == scatter):
            self.plotWidget.linearPlot = linear
            self.plotWidget.histogramPlot = histogram
            self.plotWidget.FFTPlot = FFT
            self.plotWidget.scatterPlot = scatter
            if linear:
                logger.debug('LinearPlot enabled')
            if histogram:
                logger.debug('Histogram enabled')
            if FFT:
                logger.debug('FFTPlot enabled')
            for name in self.records:
                if self.records[name]['parent'] == self:
                    self.plot.removeItem(self.records[name]['curve'].curve)
                    self.plot.addItem(self.records[name]['curve'].curve)
                    self.records[name]['curve'].update()
            if FFT:
                self.plot.updateSpectrumMode(True)
            else:
                self.plot.updateSpectrumMode(False)
            if not linear:
                self.plotWidget.date_axis.dateTicksOn = False
                self.plot.enableAutoRange()
            else:
                for name in self.records:
                    if self.records[name]['parent'] == self:
                        self.records[name]['curve'].curve.setData({'x': [0], 'y': [0]}, pen='w', stepMode=False)
                self.plotWidget.date_axis.dateTicksOn = True
                self.plot.disableAutoRange()
                self.plotWidget.setPlotScale([self.plotWidget.plotRange[0],self.plotWidget.plotRange[1]])
                self.plotScaleConnection = True

    def start(self, timer=1000):
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def addSignal(self, name, pen, timer, function, *args):
        if not name in self.records:
            signalrecord = createSignalRecord(records=self.records, name=name, timer=timer, function=function, *args)
            self.records[name]['record'] = signalrecord
            curve = self.plotWidget.addCurve(self.records, self.plotWidget, name)
            self.records[name]['curve'] = curve
            self.records[name]['parent'] = self
            self.records[name]['pen'] = pen
            self.legend.addLegendItem(name)
            self.signalAdded.emit(name)
            logger.info('Signal '+name+' added!')
        else:
            logger.warning('Signal '+name+' already exists!')
            # nameorig = name
            # name = name + '_2'
            # signalrecord = createSignalRecord(records=self.records, name=name, timer=timer, function=function, *args)
            # self.records[name]['record'] = signalrecord

    def plotUpdate(self):
        autorangeX, autorangeY = self.plotWidget.vb.state['autoRange']
        self.plotWidget.plot.disableAutoRange()
        # self.plotWidget.plot.clear()
        self.plotWidget.currentPlotTime = time.time()
        for name in self.records:
            self.records[name]['curve'].update()
        self.plotWidget.vb.enableAutoRange(x=autorangeX, y=autorangeY)

    def removeSignal(self,name):
        self.records[name]['record'].stop()
        del self.records[name]
        self.signalRemoved.emit(name)
        logger.info('Signal '+name+' removed!')

    def setPlotScale(self, timescale):
        self.plotWidget.setPlotScale([-1.05*timescale, 0.05*timescale])

    def pausePlotting(self, value=True):
        self.paused = value
        self.setPauseButtonState()
        self.plotWidget.togglePause(self.paused)

    def togglePause(self):
        if self.paused:
            self.paused = False
            logger.debug('Plot un-paused!')
        else:
            self.paused = True
            logger.debug('Plot Paused!')
        self.setPauseButtonState()
        self.plotWidget.togglePause(self.paused)

    def setPauseButtonState(self):
        if not self.paused:
            self.pauseButton.setStyleSheet("border: 5px; background-color: white")
        else:
            self.pauseButton.setStyleSheet("border: 5px; background-color: red")

    def toggleAutoScroll(self):
        self.plotWidget.date_axis.autoscroll = self.scrollButton.isChecked()
        self.plotWidget.toggleAutoScroll(self.scrollButton.isChecked())

    def setDecimateLength(self, value=5000):
        self.plotWidget.decimateScale = value
