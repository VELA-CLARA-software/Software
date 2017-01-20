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


    def __init__(self, parent = None, plotRateBar=True):
        super(scatterPlot, self).__init__(parent)
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
        self.records = {}
        self.plotWidget = scatterPlotPlot(self)
        ''' Create the plot as part of the plotObject '''
        self.plot = self.plotWidget.createPlot()
        ''' Create the signalRecord object '''

        self.setupPlotRateSlider()
        self.stripPlot.addWidget(self.plotWidget.plotWidget,0,0,5,1)
        if plotRateBar:
            self.stripPlot.addWidget(self.plotRateLabel,5, 0)
            self.stripPlot.addWidget(self.plotRateSlider,5, 1)
        self.setLayout(self.stripPlot)
        # self.togglePause()
        logger.debug('scatterPlot initiated!')
        # self.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)

    def saveAllCurves(self, saveFileName=None):
        for name in self.records:
            if self.records[name]['parent'] == self:
                filename, file_extension = os.path.splitext(saveFileName)
                saveFileName2 = filename + '_' + self.records[name]['name'] + file_extension
                self.legend.saveCurve(self.records[name]['name'],saveFileName2)

    def saveCurve(self, name, saveFileName=None):
        self.legend.saveCurve(name,saveFileName)

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

    def start(self, timer=1000):
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def addSignal(self, name, pen, timer, function, *args):
        if not name in self.records:
            signalrecord = createSignalRecord(records=self.records, name=name, timer=timer, function=function, *args)
            self.records[name]['record'] = signalrecord
            self.records[name]['parent'] = self
            self.records[name]['pen'] = pen
            self.signalAdded.emit(name)
            logger.info('Signal '+name+' added!')
        else:
            logger.warning('Signal '+name+' already exists!')

    def plotUpdate(self):
        self.plotWidget.currentPlotTime = time.time()
        self.plotWidget.update()

    def removeSignal(self,name):
        del self.records[name]
        logger.info('Signal '+name+' removed!')

    # def pausePlotting(self, value=True):
    #     self.paused = value
    #     self.plotWidget.togglePause(self.paused)

    # def togglePause(self):
    #     if self.paused:
    #         self.paused = False
    #         self.pauseButton.setStyleSheet("border: 5px; background-color: white")
    #         logger.debug('Plot un-paused!')
    #     else:
    #         self.paused = True
    #         self.pauseButton.setStyleSheet("border: 5px; background-color: red")
    #         logger.debug('Plot Paused!')
    #     self.plotWidget.togglePause(self.paused)

    def setDecimateLength(self, value=5000):
        self.plotWidget.decimateScale = value
