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
from scatterPlotPlot import *

logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


def logthread(caller):
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
                              threading.current_thread().ident))


class scatterPlot(QWidget):
    signalAdded = QtCore.pyqtSignal('QString')
    scatterSelectionChanged = QtCore.pyqtSignal('QString', 'QString')

    def __init__(self, stripplot=None, parent=None, plotRateBar=False, selectionBar=True, color=0):
        super(scatterPlot, self).__init__(parent)
        self.pg = pg
        self.paused = True
        self.signalLength = 10
        self.plotrate = 1
        self.plotScaleConnection = True
        self.pauseIcon = QtGui.QIcon(str(os.path.dirname(os.path.abspath(__file__))) + '\icons\pause.png')
        ''' create the scatterPlot as a grid layout '''
        self.scatterPlot = QtGui.QVBoxLayout()
        self.plotThread = QTimer()
        if not stripplot == None:
            self.stripPlot = stripplot
            self.records = stripplot.records
        else:
            self.stripPlot = self
            self.records = {}
        self.globalPlotRange = [-1000, 0]
        ''' Create generalPlot object '''
        self.plotWidget = scatterPlotPlot(self, color=color)
        ''' If connected to stripplot - link plotranges '''
        if not stripplot == None:
            self.stripPlot.plotWidget.changePlotScale.connect(self.plotWidget.setPlotRange)
        ''' set-up setupSelectionBar '''
        self.selectionBar = self.setupSelectionBar()
        ''' set-up plot rate slider '''
        self.setupPlotRateSlider()
        selectionBarOffset = 0
        if selectionBar:
            self.scatterPlot.addLayout(self.selectionBarLayout, 1)
            self.stripPlot.signalAdded.connect(self.updateSelectionBar)
            self.stripPlot.signalRemoved.connect(self.updateSelectionBar)
            selectionBarOffset = 1
        self.scatterPlot.addWidget(self.plotWidget.plotWidget, 5)
        if plotRateBar:
            self.scatterPlot.addWidget(self.plotRateLabel, selectionBarOffset + 5, 0)
            self.scatterPlot.addWidget(self.plotRateSlider, selectionBarOffset + 5, 1)
        self.setLayout(self.scatterPlot)
        logger.debug('scatterPlot initiated!')

    def saveAllCurves(self, saveFileName=None):
        for name in self.records:
            if self.records[name]['parent'] == self:
                filename, file_extension = os.path.splitext(saveFileName)
                saveFileName2 = filename + '_' + self.records[name]['name'] + file_extension
                self.legend.saveCurve(self.records[name]['name'], saveFileName2)

    def saveCurve(self, name, saveFileName=None):
        self.legend.saveCurve(name, saveFileName)

    def setupSelectionBar(self):
        spacer = QtGui.QSpacerItem(100, 20)
        self.combobox1 = QtGui.QComboBox()
        self.combobox1.setMaximumWidth(200)
        self.combobox1.setMinimumWidth(100)
        # self.combobox1.setMaximumHeight(20)
        self.combobox1.currentIndexChanged.connect(self.selectionBarChanged)
        self.combobox2 = QtGui.QComboBox()
        self.combobox2.setMaximumWidth(200)
        self.combobox2.setMinimumWidth(100)
        # self.combobox2.setMaximumHeight(20)
        self.combobox2.currentIndexChanged.connect(self.selectionBarChanged)
        for name in sorted(self.records):
            self.combobox1.addItem(name)
            self.combobox2.addItem(name)
        self.combobox1.setCurrentIndex(0)
        self.combobox2.setCurrentIndex(1)
        self.selectionBarLayout = QtGui.QHBoxLayout()
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.combobox1)
        self.selectionBarLayout.addSpacerItem(spacer)
        self.selectionBarLayout.addWidget(self.combobox2)
        self.selectionBarLayout.addSpacerItem(spacer)

    def selectionBarChanged(self, index):
        # print 'index = ', index
        self.scatterSelectionChanged.emit(self.combobox1.currentText(), self.combobox2.currentText())
        self.plotWidget.update()

    def updateSelectionBar(self):
        combobox1text = self.combobox1.currentText()
        combobox2text = self.combobox2.currentText()
        allnames = []
        for name in sorted(self.records):
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

    def setupPlotRateSlider(self):
        self.plotRateLabel = QtGui.QLabel()
        self.plotRateLabel.setText('Plot Update Rate [' + str(self.plotrate) + ' Hz]:')
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
        self.plotRateLabel.setText('Plot Update Rate [' + str(self.plotrate) + ' Hz]:')
        self.plotThread.setInterval(1000 * 1 / value)

    def start(self, timer=1000):
        self.plotUpdate()
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def addSignal(self, name, pen, timer, function, *args):
        if not name in self.records:
            signalrecord = createSignalRecord(records=self.records, name=name, timer=timer, function=function, *args)
            self.records[name]['record'] = signalrecord
            self.records[name]['parent'] = self
            self.records[name]['pen'] = pen
            self.signalAdded.emit(name)
            logger.info('Signal ' + name + ' added!')
        else:
            logger.warning('Signal ' + name + ' already exists!')

    def plotUpdate(self):
        self.plotWidget.currentPlotTime = time.time()
        self.plotWidget.update()

    def removeSignal(self, name):
        del self.records[name]
        logger.info('Signal ' + name + ' removed!')

    def pausePlotting(self, value=True):
        self.paused = value
        self.plotWidget.togglePause(self.paused)

    def setDecimateLength(self, value=5000):
        self.plotWidget.decimateScale = value

    def setPlotRange(self, plotrange):
        self.plotWidget.setPlotRange(plotrange)

    def setPlotScale(self, xRange=None, yRange=None):
        self.plotWidget.setPlotScale(xRange=xRange, yRange=yRange)
