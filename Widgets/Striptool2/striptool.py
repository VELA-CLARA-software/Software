import sys, time, os, datetime, math, collections, signal
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import numpy as np
import threading
from threading import Thread, Event, Timer
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
    timeChangeSignal = QtCore.pyqtSignal('float')

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
        self.timeOffset = 0

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
        # self.plotWidget.plot.vb.sigXRangeChanged.connect(self.setPlotScaleLambda)
        logger.debug('stripPlot initiated!')

        # setup some dicts
        self.proxyHeaderText = {}
        self.proxyLatestValue = {}
        self.proxyMean = {}
        self.proxySTD = {}
        self.proxyMin = {}
        self.proxyMax = {}

    def deleteAllCurves(self, reply=False):
        if reply == False:
            delete_msg = "This will delete ALL records!"
            reply = QtGui.QMessageBox.question(self, 'Message',
                             delete_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes or reply == True:
            noitems = self.parameterTree.topLevelItemCount()
            for i in reversed(range(noitems)):
                item = self.parameterTree.topLevelItem(i)
                name = item.text(0)
                self.parameterTree.deleteRow(str(name), item)

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
        for name in self.records:
            self.records[name]['record'].start()
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
        print param
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
        text = header.text(0)
        pos = [pos for pos, char in enumerate(text) if char == ':'][-1]
        name = str(text[0:pos])
        for i in range(header.childCount()):
            if header.child(i).text(0) == 'Show Axis?':
                pvisible = header.child(i).widget.value()
        self.records[name]['axis'].setVisible(any([pvisible,visible]))

    def setLogModeSignals(self, signal, name):
        signal.sigValueChanged.connect(lambda x: self.plotWidget.viewboxes[name]['axis'].setLogMode(x.value()))
        signal.sigValueChanged.connect(lambda x: self.records[name]['record'].setLogMode(x.value()))
        signal.sigValueChanged.connect(lambda: self.plotWidget.toggleLogMode(self.records,name))

    def addParameterSignal(self, name):
        params = [
            {'name': name, 'type': 'group', 'children': [
                {'name': 'Value', 'type': 'float', 'readonly': True, 'title': 'Value'},
                {'name': 'Mean', 'type': 'float', 'readonly': True},
                {'name': 'Standard Deviation', 'type': 'float', 'readonly': True},
                {'name': 'Max', 'type': 'float', 'readonly': True},
                {'name': 'Min', 'type': 'float', 'readonly': True},
                {'name': 'Plot_Colour', 'title': 'Line Colour', 'type': 'color', 'value': self.records[name]['pen'], 'tip': "Line Colour"},
                {'name': 'Log_Mode', 'title': 'Log Mode', 'type': 'bool', 'value': self.records[name]['logScale'], 'tip': "Enable Log Mode"},
                {'name': 'Show_Axis', 'title': 'Show Axis?', 'type': 'bool', 'value': False, 'tip': "Show or Remove the Axis"},
                {'name': 'Show_Plot', 'title': 'Show Plot?', 'type': 'bool', 'value': True, 'tip': "Show or Remove the plot lines"},
            ]}
        ]
        p = Parameter.create(name='params', type='group', children=params)
        pChild = p.child(name)
        # self.records[name]['worker'].recordLatestValueSignal.connect(lambda x: pChild.child('Value').setValue(x[1]))
        self.proxyLatestValue[name] = pg.SignalProxy(self.records[name]['worker'].recordLatestValueSignal, rateLimit=1, slot=lambda x: pChild.child('Value').setValue(x[0][1]))
        self.proxyMean[name] = pg.SignalProxy(self.records[name]['worker'].recordMeanSignal, rateLimit=1, slot=lambda x: pChild.child('Mean').setValue(x[0]))
        self.proxySTD[name] = pg.SignalProxy(self.records[name]['worker'].recordStandardDeviationSignal, rateLimit=1, slot=lambda x: pChild.child('Standard Deviation').setValue(x[0]))
        self.proxyMin[name] = pg.SignalProxy(self.records[name]['worker'].recordMinSignal, rateLimit=1, slot=lambda x: pChild.child('Min').setValue(x[0]))
        self.proxyMax[name] = pg.SignalProxy(self.records[name]['worker'].recordMaxSignal, rateLimit=1, slot=lambda x: pChild.child('Max').setValue(x[0]))
        self.records[name]['axis'].setVisible(False)
        self.setLogModeSignals(pChild.child('Log_Mode'), name)
        pChild.child('Show_Axis').sigValueChanged.connect(lambda x: self.records[name]['axis'].setVisible(x.value()))
        pChild.child('Show_Plot').sigValueChanged.connect(lambda x: self.records[name]['curve'].lines.setVisible(x.value()))
        self.parameterTree.addParameters(p, showTop=False)
        header = self.parameterTree.findItems(name,Qt.MatchContains | Qt.MatchRecursive)[0]
        header.setSelected(False)
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.records[name]['pen']))
        self.proxyHeaderText[name] = pg.SignalProxy(self.records[name]['worker'].recordLatestValueSignal, rateLimit=1, slot=lambda x: header.setText(0,name + ': ' + "{:.4}".format(x[0][1])))
        pChild.child('Plot_Colour').sigValueChanging.connect(lambda x, y: self.changePenColour(header,name,y))

    def changePenColour(self, header, name, colourWidget):
        colour = colourWidget.value()
        header.setBackground(0,pg.mkBrush(colour))
        header.setForeground(0,self.contrasting_text_color(colour))
        self.records[name]['pen'] = colour
        self.records[name]['curve'].changePenColour()

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
        if not self.paused:
            self.doCurveUpdate.emit()
            if self.plotWidget.autoscroll:
                lastplottime = round(time.time(),2)
                self.timeOffset = lastplottime-self.lastplottime
                # self.plotWidget.globalPlotRange[0]+=(time.time()-self.lastplottime)
                # self.plotWidget.globalPlotRange[1]+=(time.time()-self.lastplottime)
                self.plotWidget.plot.vb.translateBy(x=self.timeOffset)
                self.timeChangeSignal.emit(self.timeOffset)
                self.lastplottime = lastplottime

    def pausePlotting(self, value=True):
        self.paused = value

    def removeSignal(self,name):
        self.records[name]['record'].close()
        del self.records[name]
        self.signalRemoved.emit(name)
        logger.info('Signal '+name+' removed!')

    def setPlotScale(self, timescale):
        self.timescale = timescale
        self.plotWidget.setPlotScale([time.time()+(-1.025*timescale),time.time()+(0.025*timescale)])

    def setDecimateLength(self, value=5000):
        for name in self.records:
            self.records[name]['data'] = collections.deque(self.records[name]['data'], maxlen=value)

    def close(self):
        for name in self.records:
            self.records[name]['record'].close()
