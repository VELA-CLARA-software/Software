import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import sys, time, os, datetime
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

class plotLegend(ParameterTree):

    fftselectionchange = pyqtSignal('QString',bool)
    histogramplotselectionchange = pyqtSignal('QString',bool)
    axisselectionchanged = pyqtSignal('QString')


    def __init__(self, generalplot):
        super(plotLegend, self).__init__(generalplot)
        ''' Create Parameter Tree'''
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.selectionModel().selectionChanged.connect(self.enableSelectedAxis)
        self.parameters = {}
        self.generalPlot = generalplot
        self.records = self.generalPlot.records
        # setup some dicts
        self.proxyHeaderText = {}
        self.proxyLatestValue = {}
        self.proxyMean = {}
        self.proxySTD = {}
        self.proxyMin = {}
        self.proxyMax = {}
        self.parameterChildren = {}
        self.generalPlot.signalAdded.connect(self.addParameterSignal)
        self.generalPlot.signalRemoved.connect(self.removeParameterSignal)

    def updateValue(self, param, value):
        param.setValue(value)

    def contrasting_text_color(self, color):
        # (r, g, b) = (hex_str[:2], hex_str[2:4], hex_str[4:])
        r, g, b, a = pg.colorTuple(pg.mkColor(color))
        return pg.mkBrush('000' if 1 - (r * 0.299 + g * 0.587 + b * 0.114) / 255 < 0.5 else 'fff')

    def valueFormatter(self, value):
        return "{:.4}".format(value)

    def printValue(self, param):
        print param

    def enableSelectedAxis(self, header):
        headers = self.selectedItems()
        axesdata = {}
        for i in range(self.topLevelItemCount()):
            child = self.topLevelItem(i).child(0)
            if child in headers:
                name, onoff = self.toggleAxisVisible(child, True)
            else:
                name, onoff = self.toggleAxisVisible(child, False)
            if name not in axesdata:
                axesdata[name] = []
            axesdata[name].append(onoff)
        # print 'axesdata = ', axesdata
        for axis, booles in axesdata.iteritems():
            axis.setVisible(any(booles))
        # print 'axis on = ', any([pvisible,visible])
        # self.records[name]['scrollingplot'].toggleAxis(name, any([pvisible,visible]))

    def toggleAxisVisible(self, header, visible=False):
        text = header.text(0)
        pos = [pos for pos, char in enumerate(text) if char == ':'][-1]
        name = str(text[0:pos])
        for i in range(header.childCount()):
            if header.child(i).text(0) == 'Show Axis?':
                pvisible = header.child(i).widget.value()
        # self.records[name]['axis'].setVisible(any([pvisible,visible]))
        return self.records[name]['axis'], any([pvisible,visible])


    def setLogModeSignals(self, signal, name):
        signal.sigValueChanged.connect(lambda x: self.plotWidget.viewboxes[name]['axis'].setLogMode(x.value()))
        signal.sigValueChanged.connect(lambda x: self.records[name]['record'].setLogMode(x.value()))
        # signal.sigValueChanged.connect(lambda: self.plotWidget.toggleLogMode(self.records,name))

    def addParameterSignal(self, name):
        params = [
            {'name': name, 'type': 'group', 'children': [
                {'name': 'Value', 'type': 'float', 'readonly': True, 'title': 'Value'},
                {'name': 'Mean', 'type': 'float', 'readonly': True},
                {'name': 'Standard Deviation', 'type': 'float', 'readonly': True},
                {'name': 'Max', 'type': 'float', 'readonly': True},
                {'name': 'Min', 'type': 'float', 'readonly': True},
                {'name': 'Plot_Colour', 'title': 'Line Colour', 'type': 'color', 'value': self.records[name]['pen'], 'tip': "Line Colour"},
                {'name': 'Axis', 'title': 'Choose Axis', 'type': 'list', 'values': {}, 'value': self.records[name]['axisname'], 'tip': "Choose which axis to display on"},
                {'name': 'Show_Axis', 'title': 'Show Axis?', 'type': 'bool', 'value': False, 'tip': "Show or Remove the Axis"},
                {'name': 'Show_Plot', 'title': 'Show Plot?', 'type': 'bool', 'value': True, 'tip': "Show or Remove the plot lines"},
                {'name': 'FFT_Plot', 'title': 'Plot FFT', 'type': 'bool', 'value': False, 'tip': "Show or Remove the FFT Plot"},
                {'name': 'Histogram_Plot', 'title': 'Plot Histogram', 'type': 'bool', 'value': False, 'tip': "Show or Remove the Histogram Plot"},
            ]}
        ]
        p = Parameter.create(name='params', type='group', children=params)
        pChild = p.child(name)
        self.parameterChildren[name] = pChild
        self.proxyLatestValue[name] = pg.SignalProxy(self.records[name]['worker'].recordLatestValueSignal, rateLimit=1, slot=lambda x: pChild.child('Value').setValue(x[0][1]))
        self.proxyMean[name] = pg.SignalProxy(self.records[name]['worker'].recordMeanSignal, rateLimit=1, slot=lambda x: pChild.child('Mean').setValue(x[0]))
        self.proxySTD[name] = pg.SignalProxy(self.records[name]['worker'].recordStandardDeviationSignal, rateLimit=1, slot=lambda x: pChild.child('Standard Deviation').setValue(x[0]))
        self.proxyMin[name] = pg.SignalProxy(self.records[name]['worker'].recordMinSignal, rateLimit=1, slot=lambda x: pChild.child('Min').setValue(x[0]))
        self.proxyMax[name] = pg.SignalProxy(self.records[name]['worker'].recordMaxSignal, rateLimit=1, slot=lambda x: pChild.child('Max').setValue(x[0]))
        self.setupAxisList(name, pChild)
        pChild.child('Show_Axis').sigValueChanged.connect(lambda x: self.records[name]['axis'].setVisible(x.value()))
        pChild.child('Show_Plot').sigValueChanged.connect(lambda x: self.records[name]['curve'].lines.setVisible(x.value()))
        pChild.child('FFT_Plot').sigValueChanged.connect(lambda x: self.fftselectionchange.emit(name, x.value()))
        pChild.child('Histogram_Plot').sigValueChanged.connect(lambda x: self.histogramplotselectionchange.emit(name, x.value()))
        self.addParameters(p, showTop=False)
        header = self.findItems(name,Qt.MatchContains | Qt.MatchRecursive)[0]
        header.setSelected(False)
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.records[name]['pen']))
        self.proxyHeaderText[name] = pg.SignalProxy(self.records[name]['worker'].recordLatestValueSignal, rateLimit=1, slot=lambda x: header.setText(0,name + ': ' + "{:.4}".format(x[0][1])))
        pChild.child('Plot_Colour').sigValueChanging.connect(lambda x, y: self.changePenColour(header,name,y))

    def setupAxisList(self, name, pChild):
        if 'scrollingplot' in self.records[name]:
            pChild.child('Axis').setLimits(self.records[name]['scrollingplot'].getAxes())
            self.records[name]['scrollingplot'].toggleAxis(name, False)
            self.records[name]['scrollingplot'].newaxis.connect(lambda x: pChild.child('Axis').setValue(self.records[name]['scrollingplot'].getAxes()))
            pChild.child('Axis').sigValueChanged.connect(lambda x: self.records[name]['scrollingplot'].changeAxis(name,x.value()))

    def changePenColour(self, header, name, colourWidget):
        colour = colourWidget.value()
        header.setBackground(0,pg.mkBrush(colour))
        header.setForeground(0,self.contrasting_text_color(colour))
        self.records[name]['pen'] = colour
        self.records[name]['curve'].changePenColour()

    def removeParameterSignal(self,name):
        self.parameterChildren[name].remove()
