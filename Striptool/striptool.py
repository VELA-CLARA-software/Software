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

def curveUpdate(self, curve):
    curve.update()

def logthread(caller):
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
                              threading.current_thread().ident))

class stripPlot(QWidget):

    signalAdded = QtCore.pyqtSignal('QString')
    signalRemoved = QtCore.pyqtSignal('QString')
    doCurveUpdate = QtCore.pyqtSignal()

    def __init__(self, parent = None, plotRateBar=True, crosshairs=True, **kwargs):
        super(stripPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.signalLength = 10
        self.plotrate = 1
        self.plotScaleConnection = True
        self.crosshairs = crosshairs
        self.subtractMean = False
        self.pauseIcon  =  QtGui.QIcon(str(os.path.dirname(os.path.abspath(__file__)))+'\icons\pause.png')
        self.linearPlot = True
        self.histogramPlot = False
        self.FFTPlot = False

        ''' create the stripPlot.stripPlot as a grid layout '''
        self.stripPlot = QtGui.QGridLayout()
        self.plotThread = QTimer()
        ''' Create generalPlot object '''
        self.plotWidget = generalPlot(self, crosshairs=self.crosshairs, **kwargs)
        ''' Create the plot as part of the plotObject '''
        self.plot = self.plotWidget.createPlot()
        ''' Create the signalRecord object '''
        self.records = {}

        ''' Sidebar for graph type selection '''
        self.buttonLayout = QtGui.QGridLayout()
        self.linearRadio = QRadioButton("Linear")
        self.linearRadio.setChecked(True)
        self.linearRadio.toggled.connect(lambda: self.setPlotType(linear=True))
        self.linearCheckbox = QCheckBox("Subtract Mean")
        self.linearCheckbox.stateChanged.connect(self.setSubtractMean)
        self.linearCheckbox.setChecked(False)
        ''' Histogram '''
        self.HistogramRadio = QRadioButton("Histogram")
        self.HistogramRadio.toggled.connect(lambda: self.setPlotType(histogram=True))
        self.histogramBinsLabel = QLabel('NBins')
        self.histogramBinsLabel.hide()
        self.histogramBinsEdit = QSpinBox()
        self.histogramBinsEdit.setValue(10)
        self.setHistogramBins(10)
        self.histogramBinsEdit.setMinimum(1)
        self.histogramBinsEdit.hide()
        # self.histogramBinsEdit.setMaxLength(4)
        # self.histogramBinsEdit.setInputMask('0000')
        self.histogramBinsEdit.valueChanged.connect(self.setHistogramBins)
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
        ''' add Save All Data Button '''
        self.saveAllButton = QPushButton('Save All Data')
        self.saveAllButton.clicked.connect(self.saveAllCurves)
        ''' add Clear All Data Button '''
        self.clearAllButton = QPushButton('Clear All Data')
        self.clearAllButton.clicked.connect(self.clearAllCurves)
        ''' add Delete All Data Button '''
        self.deleteAllButton = QPushButton('Delete All Curves')
        self.deleteAllButton.clicked.connect(self.deleteAllCurves)
        ''' Add legend checkbox '''
        self.legendCheckBox = QCheckBox("Show Legend")
        self.legendCheckBox.setChecked(False)
        self.legendCheckBox.toggled.connect(self.plotWidget.toggleLegend)
        ''' Set Layout '''
        self.buttonLayout.addWidget(self.linearRadio,      0,0,1,1)
        self.buttonLayout.addWidget(self.linearCheckbox,   0,2,1,1)
        self.buttonLayout.addWidget(self.FFTRadio,         1,0,1,2)
        self.buttonLayout.addWidget(self.legendCheckBox,   1,2,1,2)
        self.buttonLayout.addWidget(self.HistogramRadio,   2,0,1,1)
        self.buttonLayout.addWidget(self.histogramBinsEdit,2,2,1,1)
        self.buttonLayout.addWidget(self.histogramBinsLabel,2,3,1,1)
        self.buttonLayout.addWidget(self.scrollButton,     3,0,1,1)
        self.buttonLayout.addWidget(self.pauseButton,      3,3,1,1)
        self.buttonLayout.addWidget(self.legend.layout,    4,0,3,4)
        self.buttonLayout.addWidget(self.saveAllButton,    7,0)
        self.buttonLayout.addWidget(self.clearAllButton,   7,1)
        self.buttonLayout.addWidget(self.deleteAllButton,  7,2)

        if self.crosshairs:
            ''' create signalValueTable '''
            self.signalValueTableOpen = False

            self.signalValueWidget = QWidget()
            self.signalValueLayout = QVBoxLayout()
            self.signalValueTable = QTableWidget(0,2)
            self.signalValueTable.setHorizontalHeaderLabels(('Signal', 'Value'))
            self.signalValueWidget.setLayout(self.signalValueLayout)

            self.signalValueTableSelectorWidget = QWidget()
            self.signalValueTableSelector = QButtonGroup()
            signalValueTableSelectorValueButton = QRadioButton('Value')
            signalValueTableSelectorValueButton.setChecked(True)
            signalValueTableSelectorMeanButton = QRadioButton('Mean')
            signalValueTableSelectorRMSButton = QRadioButton('RMS')
            self.signalValueTableSelector.addButton(signalValueTableSelectorValueButton)
            self.signalValueTableSelector.addButton(signalValueTableSelectorMeanButton)
            self.signalValueTableSelector.addButton(signalValueTableSelectorRMSButton)
            self.signalValueTableSelectorLayout = QHBoxLayout()
            self.signalValueTableSelectorLayout.addWidget(signalValueTableSelectorValueButton)
            self.signalValueTableSelectorLayout.addWidget(signalValueTableSelectorMeanButton)
            self.signalValueTableSelectorLayout.addWidget(signalValueTableSelectorRMSButton)
            self.signalValueTableSelectorWidget.setLayout(self.signalValueTableSelectorLayout)

            self.signalValueLayout.addWidget(self.signalValueTable)
            self.signalValueLayout.addWidget(self.signalValueTableSelectorWidget)


        ''' Add sidebar  to main layout'''
        self.GUISplitter = QtGui.QSplitter()
        self.GUISplitter.setHandleWidth(10)

        if self.crosshairs:
            ''' Add signalValueTable to GUISplitter '''
            self.GUISplitter.addWidget(self.signalValueWidget)

        ''' Add main plot widget to GUISplitter'''
        self.GUISplitter.addWidget(self.plotWidget.plotWidget)

        ''' Create a frame for the sidebar '''
        self.buttonFrame = QtGui.QFrame()
        ''' set the frame layout to the sidebar buttons '''
        self.buttonFrame.setLayout(self.buttonLayout)
        ''' add the sidebar buttons to the GUISplitter '''
        self.GUISplitter.addWidget(self.buttonFrame)

        ''' Mess with the GUISplitter Handles '''
        self.GUISplitter.setStyleSheet("QSplitter::handle{background-color:transparent;}");

        if self.crosshairs:
            ''' signalValueTable Handle '''
            handle = self.GUISplitter.handle(1)
            layout = QtGui.QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            self.signalValueTableSplitterbutton = QtGui.QToolButton(handle)
            self.signalValueTableSplitterbutton.setArrowType(QtCore.Qt.RightArrow)
            self.signalValueTableSplitterbutton.clicked.connect(
                lambda: self.handleSignalValueTableSplitterButton(False))
            self.GUISplitter.splitterMoved.connect(self.handleSignalValueTableSplitterButtonArrow)
            layout.addWidget(self.signalValueTableSplitterbutton)
            handle.setLayout(layout)
            self.plotWidget.signalValuesUnderCrosshairs.connect(self.updateSignalValueTable)

        ''' Legend Handle '''
        if self.crosshairs:
            self.legendnumber = 2
        else:
            self.legendnumber = 1
        handle = self.GUISplitter.handle(self.legendnumber)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.legendSplitterbutton = QtGui.QToolButton(handle)
        self.legendSplitterbutton.setArrowType(QtCore.Qt.LeftArrow)
        self.legendSplitterbutton.clicked.connect(
            lambda: self.handleLegendSplitterButton(False))
        self.GUISplitter.splitterMoved.connect(self.handleLegendSplitterButtonArrow)
        layout.addWidget(self.legendSplitterbutton)
        handle.setLayout(layout)

        ''' Setting stretch factors '''
        if self.crosshairs:
            self.GUISplitter.setStretchFactor(0,1)
            self.GUISplitter.setStretchFactor(1,4)
            self.GUISplitter.setStretchFactor(2,1)
            self.GUISplitter.setSizes([0,1,0])
        else:
            self.GUISplitter.setStretchFactor(0,4)
            self.GUISplitter.setStretchFactor(1,1)
            self.GUISplitter.setSizes([1,0])

        ''' putting it all together '''
        self.handleLegendSplitterButton(left=True)
        self.stripPlot.addWidget(self.GUISplitter,0,0,5,2)
        self.setupPlotRateSlider()
        if plotRateBar:
            self.stripPlot.addWidget(self.plotRateLabel,5, 0)
            self.stripPlot.addWidget(self.plotRateSlider,5, 1)
        self.setLayout(self.stripPlot)
        # self.plotThread.timeout.connect(lambda: self.plotWidget.date_axis.linkedViewChanged(self.plotWidget.date_axis.linkedView()))
        self.plotWidget.plot.vb.sigXRangeChanged.connect(self.setPlotScaleLambda)
        logger.debug('stripPlot initiated!')
        self.legend.logScaleChanged.connect(self.toggleCurveLogScale)

    def toggleCurveLogScale(self,name,value):
        self.records[name]['curve'].setLogScale(value)

    def keyPressEvent(self, e):
            if e.key() == QtCore.Qt.Key_F11:
                print "Maximise!"
                self.handleSignalValueTableSplitterButton(left=True)
                self.handleLegendSplitterButton(left=True)

    def updateSignalValueTable(self, signallist):
        name, value, mean, rms = signallist
        if self.signalValueTableOpen:
            radiobuton = self.signalValueTableSelector.checkedButton().text()
            row = self.signalValueTable.findItems(name, QtCore.Qt.MatchExactly)[0].row()
            if radiobuton == 'Value':
                value = str(value)
            elif radiobuton == 'Mean':
                value = str(mean)
            elif radiobuton == 'RMS':
                value = str(rms)
            self.signalValueTable.setItem(row,1,QtGui.QTableWidgetItem(value))

    def setHistogramBins(self, value):
        for name in self.records:
            self.records[name]['curve'].setHistogramBins(value)

    def setSubtractMean(self, value):
        if value ==2:
            ischecked = True
        else:
            ischecked = False
        self.linearCheckbox.setChecked(ischecked)
        self.subtractMean = ischecked
        for name in self.records:
            self.records[name]['curve'].setVerticalMeanSubtraction(self.subtractMean)

    def deleteAllCurves(self, reply=False):
        if reply == False:
            delete_msg = "This will delete ALL records!"
            reply = QtGui.QMessageBox.question(self, 'Message',
                             delete_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes or reply == True:
            noitems = self.legend.layout.topLevelItemCount()
            for i in reversed(range(noitems)):
                item = self.legend.layout.topLevelItem(i)
                name =  item.text(0)
                self.legend.deleteRow(str(name), item)

    def clearAllCurves(self):
        for name in self.records:
            self.legend.clearCurve(name)

    def saveAllCurves(self, saveFileName=False):
        if not saveFileName:
            saveFileName = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Arrays', '', filter="CSV files (*.csv);; Binary Files (*.bin)", selectedFilter="CSV files (*.csv)"))
        if not saveFileName == None:
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

    def handleSignalValueTableSplitterButton(self, left=True):
        sizes = self.GUISplitter.sizes()
        sizes[0]=0
        if left:
            self.GUISplitter.setStretchFactor(0,0)
            self.GUISplitter.setSizes(sizes)
        elif not self.GUISplitter.sizes()[0] > 0:
            sizes[0]=275
            self.GUISplitter.setStretchFactor(0,1)
            self.GUISplitter.setSizes(sizes)
        else:
            self.GUISplitter.setStretchFactor(0,0)
            self.GUISplitter.setSizes(sizes)
        self.handleSignalValueTableSplitterButtonArrow()

    def handleSignalValueTableSplitterButtonArrow(self):
        sizes = self.GUISplitter.sizes()
        if self.GUISplitter.sizes()[0] > 0:
            self.signalValueTableOpen = True
            self.signalValueTableSplitterbutton.setArrowType(QtCore.Qt.LeftArrow)
        else:
            self.signalValueTableOpen = False
            self.signalValueTableSplitterbutton.setArrowType(QtCore.Qt.RightArrow)

    def handleLegendSplitterButton(self, left=True):
        sizes = self.GUISplitter.sizes()
        sizes[self.legendnumber]=0
        if left:
            self.GUISplitter.setStretchFactor(self.legendnumber,0)
            self.GUISplitter.setSizes(sizes)
        elif not self.GUISplitter.sizes()[self.legendnumber] > 0:
            sizes[self.legendnumber]=1
            self.GUISplitter.setStretchFactor(self.legendnumber,1)
            self.GUISplitter.setSizes(sizes)
        else:
            self.GUISplitter.setStretchFactor(self.legendnumber,0)
            self.GUISplitter.setSizes(sizes)
        self.handleLegendSplitterButtonArrow()

    def handleLegendSplitterButtonArrow(self):
        sizes = self.GUISplitter.sizes()
        if self.GUISplitter.sizes()[self.legendnumber] > 0:
            self.legendSplitterbutton.setArrowType(QtCore.Qt.RightArrow)
        else:
            self.legendSplitterbutton.setArrowType(QtCore.Qt.LeftArrow)

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
        if not self.plotRateSlider.value() == value:
            self.plotRateSlider.setValue(value)
        self.plotRateLabel.setText('Plot Update Rate ['+str(self.plotrate)+' Hz]:')
        self.plotThread.setInterval(1000*1/value)

    def setPlotScaleLambda(self, widget, timescale):
        if self.plotScaleConnection:
            self.plotWidget.setPlotScale(timescale)

    def setPlotType(self, linear=False, histogram=False, FFT=False, scatter=False):
        self.plotScaleConnection = False
        if not(self.linearPlot == linear and self.histogramPlot == histogram and self.FFTPlot == FFT):
            self.linearPlot = linear
            self.plotWidget.linearPlot = linear
            self.histogramPlot = histogram
            self.FFTPlot = FFT
            self.scatterPlot = scatter
            if linear:
                logger.debug('LinearPlot enabled')
            if histogram:
                logger.debug('Histogram enabled')
                self.histogramBinsEdit.show()
                self.histogramBinsLabel.show()
            else:
                self.histogramBinsEdit.hide()
                self.histogramBinsLabel.hide()
            if FFT:
                logger.debug('FFTPlot enabled')
            for name in self.records:
                if self.records[name]['parent'] == self:
                    self.records[name]['curve'].curve.setClipToView(False)
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
                self.plotWidget.date_axis.dateTicksOn = True
                self.plot.disableAutoRange()
                self.plotWidget.setPlotScale([self.plotWidget.plotRange[0],self.plotWidget.plotRange[1]])

    def start(self, timer=1000):
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def addSignal(self, name='', pen='r', timer=1, maxlength=pow(2,20), function=None, arg=[], **kwargs):
        if not name in self.records:
            signalrecord = createSignalRecord(records=self.records, name=name, pen=pen, timer=timer, maxlength=maxlength, function=function, arg=arg, **kwargs)
            self.records[name]['record'] = signalrecord
            curve = self.plotWidget.addCurve(self.records, name)
            self.records[name]['curve'] = curve
            self.records[name]['parent'] = self
            self.legend.addLegendItem(name)
            self.signalAdded.emit(name)
            logger.info('Signal '+name+' added!')
            if self.crosshairs:
                rownumber = self.signalValueTable.rowCount()
                self.signalValueTable.insertRow(rownumber)
                self.signalValueTable.setItem(rownumber,0,QtGui.QTableWidgetItem(name))
        else:
            logger.warning('Signal '+name+' already exists!')

    def plotUpdate(self):
        if not self.plotWidget.paused:
            autorangeX, autorangeY = self.plotWidget.vb.state['autoRange']
            self.plotWidget.plot.disableAutoRange()
            self.plotWidget.currentPlotTime = round(time.time(),2)
            self.doCurveUpdate.emit()
            ''' this forces the date_axis to redraw '''
            self.plotWidget.date_axis.linkedViewChanged(self.plotWidget.date_axis.linkedView())
            self.plotWidget.vb.enableAutoRange(x=autorangeX, y=autorangeY)

    def removeSignal(self,name):
        self.records[name]['record'].close()
        try:
            self.plotWidget.legend.removeItem(name)
        except:
            pass
        del self.records[name]
        self.signalRemoved.emit(name)
        if self.crosshairs:
            row = self.signalValueTable.findItems(name, QtCore.Qt.MatchExactly)[0].row()
            self.signalValueTable.removeRow(row)
        logger.info('Signal '+name+' removed!')

    def setPlotScale(self, timescale):
        self.plotWidget.setPlotScale([-1.05*timescale, 0.05*timescale])

    def pausePlotting(self, value=True):
        self.paused = value
        self.setPauseButtonState()
        self.plotWidget.togglePause(self.paused)

    def togglePause(self):
        if self.paused:
            self.pausePlotting(value=False)
            logger.debug('Plot Resumed!')
        else:
            self.pausePlotting(value=True)
            logger.debug('Plot Paused!')

    def setPauseButtonState(self):
        if not self.paused:
            self.pauseButton.setStyleSheet("border: 5px; background-color: white")
        else:
            self.pauseButton.setStyleSheet("border: 5px; background-color: red")

    def toggleAutoScroll(self):
        self.plotWidget.date_axis.autoscroll = self.scrollButton.isChecked()
        self.plotWidget.toggleAutoScroll(self.scrollButton.isChecked())

    def setDecimateLength(self, value=5000):
        for names in self.records:
            self.records[name]['curve'].setDecimateScale(value)

    def close(self):
        for name in self.records:
            self.records[name]['record'].close()
