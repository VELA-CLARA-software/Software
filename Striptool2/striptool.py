import sys, time, os, datetime, math
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
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)

def curveUpdate(self, curve):
    curve.update()

def logthread(caller):
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
                              threading.current_thread().ident))

styleSheet = """
QTreeView {
    alternate-background-color: #f6fafb;
    background: #e8f4fc;
}
QTreeView::item:open {
    background-color: #c5ebfb;
    color: blue;
}
QTreeView::item:selected {
    background-color: #1d3dec;
    color: white;
}
QTreeView::branch {
    background-color: grey;
}
QTreeView::branch:open {
    image: url(branch-open.png);
}
QTreeView::branch:closed:has-children {
    image: url(branch-closed.png);
}
"""

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

        ''' Create Parameter Tree'''
        self.parameterTree = ParameterTree()
        self.parameterTree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.parameterTree.selectionModel().selectionChanged.connect(self.enableSelectedAxis)
        self.parameters = {}

        ''' Create Splitter'''
        self.GUISplitter = QtGui.QSplitter()
        self.GUISplitter.setHandleWidth(10)

        ''' Add widgets to GUISplitter'''
        self.GUISplitter.addWidget(self.plotWidget.plotWidget)
        self.GUISplitter.addWidget(self.parameterTree)

        ''' Mess with the GUISplitter Handles '''
        # self.GUISplitter.setStyleSheet("QSplitter::handle{background-color:transparent;}");

        ''' putting it all together '''
        self.stripPlot.addWidget(self.GUISplitter,0,0,5,2)
        self.setupPlotRateSlider()
        if plotRateBar:
            self.stripPlot.addWidget(self.plotRateLabel,5, 0)
            self.stripPlot.addWidget(self.plotRateSlider,5, 1)
        self.setLayout(self.stripPlot)
        # self.plotThread.timeout.connect(lambda: self.plotWidget.date_axis.linkedViewChanged(self.plotWidget.date_axis.linkedView()))
        self.plotWidget.plot.vb.sigXRangeChanged.connect(self.setPlotScaleLambda)
        logger.debug('stripPlot initiated!')

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

    def start(self, timer=1000):
        self.plotThread.start(timer)
        self.plotThread.timeout.connect(self.plotUpdate)

    def updateValue(self, param, value):
        param.setValue(value)

    def contrasting_text_color(self, color):
        # (r, g, b) = (hex_str[:2], hex_str[2:4], hex_str[4:])
        r, g, b, a = pg.colorTuple(pg.mkColor(color))
        return pg.mkBrush('000' if 1 - (r * 0.299 + g * 0.587 + b * 0.114) / 255 < 0.5 else 'fff')

    def valueFormatter(self, value):
        # if math.log(value,10) < -4 or math.log(value,10) > 4:
        #     print value, '  ', math.log(value,10)
        #     return "{:.3E}".format(value)
        # else:
            return "{:.4}".format(value)

    def printValue(self, param):
        print param.text(0).split(':')[0]
        # print param.childCount()

    def enableSelectedAxis(self, header):
        headers = self.parameterTree.selectedItems()
        for i in range(self.parameterTree.topLevelItemCount()):
            child = self.parameterTree.topLevelItem(i).child(0)
            if child in headers:
                self.toggleAxisVisible(child, True)
            else:
                self.toggleAxisVisible(child, False)

    def toggleAxisVisible(self, header, visible=False):
        name = str(header.text(0).split(':')[0])
        self.plotWidget.viewboxes[name]['axis'].setVisible(any([header.child(5).widget.value(),visible]))

    def addParameterSignal(self, name):
        params = [
            {'name': name, 'type': 'group', 'children': [
                {'name': 'Value', 'type': 'float', 'readonly': True, 'title': 'Value'},
                {'name': 'Mean', 'type': 'float', 'readonly': True},
                {'name': 'Standard Deviation', 'type': 'float', 'readonly': True},
                {'name': 'Max', 'type': 'float', 'readonly': True},
                {'name': 'Min', 'type': 'float', 'readonly': True},
                {'name': 'Show_Axis', 'title': 'Show Axis?', 'type': 'bool', 'value': False, 'tip': "Show or Remove the Axis"},
            ]}
        ]
        p = Parameter.create(name='params', type='group', children=params)
        pChild = p.child(name)
        self.records[name]['worker'].recordLatestValueSignal.connect(pChild.child('Value').setValue)
        self.records[name]['worker'].recordMeanSignal.connect(pChild.child('Mean').setValue)
        self.records[name]['worker'].recordStandardDeviationSignal.connect(pChild.child('Standard Deviation').setValue)
        self.records[name]['worker'].recordMinSignal.connect(pChild.child('Min').setValue)
        self.records[name]['worker'].recordMaxSignal.connect(pChild.child('Max').setValue)
        self.plotWidget.viewboxes[name]['axis'].setVisible(False)
        pChild.child('Show_Axis').sigValueChanged.connect(lambda x: self.plotWidget.viewboxes[name]['axis'].setVisible(x.value()))
        self.parameterTree.addParameters(p, showTop=False)
        header = self.parameterTree.findItems(name,Qt.MatchContains | Qt.MatchRecursive)[0]
        header.setSelected(False)
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.records[name]['pen']))
        self.records[name]['worker'].recordLatestValueSignal.connect(lambda x :header.setText(0,name + ': ' + "{:.4}".format(x)))

    def addSignal(self, name='', pen='r', timer=1, maxlength=pow(2,20), function=None, arg=[], **kwargs):
        if not name in self.records:
            signalrecord = SignalRecord(records=self.records, name=name, pen=pen, timer=timer, maxlength=maxlength, function=function, arg=arg, **kwargs)
            self.records[name]['record'] = signalrecord
            curve = self.plotWidget.addCurve(self.records, name)
            self.records[name]['curve'] = curve
            self.records[name]['parent'] = self
            self.signalAdded.emit(name)
            self.addParameterSignal(name)
            logger.info('Signal '+name+' added!')
        else:
            logger.warning('Signal '+name+' already exists!')

    def getLastPlotTime():
        lastpoints = []
        for names in self.records:
            self.records[name]['data'][-1]

    def plotUpdate(self):
        if not hasattr(self,'lastplottime'):
            self.lastplottime = round(time.time(),2)
        if not self.plotWidget.paused:
            # self.plotWidget.currentPlotTime = round(time.time(),2)
            self.doCurveUpdate.emit()
            if self.plotWidget.autoscroll:
                lastplottime = round(time.time(),2)
                self.plotWidget.globalPlotRange[0]+=(time.time()-self.lastplottime)
                self.plotWidget.globalPlotRange[1]+=(time.time()-self.lastplottime)
                if self.linearPlot:
                    self.plotWidget.plot.vb.translateBy(x=(lastplottime-self.lastplottime))
                self.lastplottime = lastplottime

    def removeSignal(self,name):
        self.records[name]['record'].close()
        del self.records[name]
        self.signalRemoved.emit(name)
        logger.info('Signal '+name+' removed!')

    def setPlotScale(self, timescale):
        self.timescale = timescale
        self.plotWidget.setPlotScale([time.time()+(-1.025*timescale), time.time()+(0.025*timescale)])

    def setDecimateLength(self, value=5000):
        for names in self.records:
            self.records[name]['curve'].setDecimateScale(value)

    def close(self):
        for name in self.records:
            self.records[name]['record'].close()
