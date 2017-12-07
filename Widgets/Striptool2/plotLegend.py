import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import sys, time, os, datetime
# if sys.version_info<(3,0,0):
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# else:
#     from PyQt5.QtCore import *
#     from PyQt5.QtGui import *
#     from PyQt5.QtWidgets import *
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

class plotLegend(ParameterTree):

    fftselectionchange = pyqtSignal('QString',bool)
    histogramplotselectionchange = pyqtSignal('QString',bool)
    axisselectionchanged = pyqtSignal('QString')
    legendselectionchanged = pyqtSignal(list)

    def __init__(self, generalplot):
        super(plotLegend, self).__init__(generalplot)
        ''' Create Parameter Tree'''
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.selectionModel().selectionChanged.connect(self.enableSelectedAxis)
        self.selectionModel().selectionChanged.connect(self.emitSelectedAxis)
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
        print(param)

    def emitSelectedAxis(self, header):
        headers = self.selectedItems()
        names = []
        for i in range(self.topLevelItemCount()):
            child = self.topLevelItem(i).child(0)
            if child in headers:
                text = child.text(0)
                pos = [pos for pos, char in enumerate(text) if char == ':'][-1]
                name = str(text[0:pos])
                names.append(name)
        self.legendselectionchanged.emit(names)

    def enableSelectedAxis(self, header):
        headers = self.selectedItems()
        axesdata = {}
        for i in range(self.topLevelItemCount()):
            try:
                child = self.topLevelItem(i).child(0)
                if child in headers:
                    name, onoff = self.toggleAxisVisible(child, True)
                else:
                    name, onoff = self.toggleAxisVisible(child, False)
                if name not in axesdata:
                    axesdata[name] = []
                axesdata[name].append(onoff)
            except:
                pass
            for axis, booles in axesdata.items():
                axis.setVisible(any(booles))

    def toggleAxisVisible(self, header, visible=False):
        text = header.text(0)
        pos = [pos for pos, char in enumerate(text) if char == ':'][-1]
        name = str(text[0:pos])
        # print header.findItems('Show Axis?')
        for i in range(header.childCount()):
            for j in range(header.child(i).childCount()):
                if header.child(i).child(j).text(0) == 'Show Axis?':
                    pvisible = header.child(i).child(j).widget.value()
        self.records[name]['axis'].setVisible(any([pvisible,visible]))
        return self.records[name]['axis'], any([pvisible,visible])

    def returnTitleValue(self, name, titletext):
        headers = self.selectedItems()
        for i in range(self.topLevelItemCount()):
            try:
                header = self.topLevelItem(i).child(0)
                text = header.text(0)
                pos = [pos for pos, char in enumerate(text) if char == ':'][-1]
                childname = str(text[0:pos])
                if name == childname:
                    for i in range(header.childCount()):
                        if header.child(i).text(0) == titletext:
                            return header.child(i).widget.value()
            except:
                pass

    def isFFTEnabled(self,name):
        return self.returnTitleValue(name, 'Plot FFT')

    def isHistogramEnabled(self,name):
        return self.returnTitleValue(name, 'Plot Histogram')

    def setLogModeSignals(self, signal, name):
        signal.sigValueChanged.connect(lambda x: self.plotWidget.viewboxes[name]['axis'].setLogMode(x.value()))
        signal.sigValueChanged.connect(lambda x: self.records[name]['record'].setLogMode(x.value()))
        # signal.sigValueChanged.connect(lambda: self.plotWidget.toggleLogMode(self.records,name))

    def parameterSignalRemoved(self, parameter):
        text = parameter.name()
        pos = [pos for pos, char in enumerate(text) if char == ':'][-1]
        name = str(text[0:pos])
        # print 'Signal Removed! Name = ', name
        try:
            self.generalPlot.removeSignal(str(name))
        except:
            pass

    def addParameterSignal(self, name):
        name = str(name)
        params = [
            {'name': name, 'type': 'group', 'removable': True, 'children': [
                {'name': 'Statistics', 'type': 'group', 'removable': False, 'expanded': False, 'children': [
                    {'name': 'Value', 'type': 'float', 'readonly': True, 'title': 'Value'},
                    {'name': 'Mean', 'type': 'float', 'readonly': True},
                    {'name': 'Standard Deviation', 'type': 'float', 'readonly': True},
                    {'name': 'Max', 'type': 'float', 'readonly': True},
                    {'name': 'Min', 'type': 'float', 'readonly': True},
                ]},
                {'name': 'Options', 'type': 'group', 'removable': False, 'expanded': False, 'children': [
                    {'name': 'Plot_Colour', 'title': 'Line Colour', 'type': 'color', 'value': self.records[name]['pen'], 'tip': "Line Colour"},
                    {'name': 'Axis', 'title': 'Choose Axis', 'type': 'list', 'values': {}, 'value': self.records[name]['axisname'], 'tip': "Choose which axis to display on"},
                    {'name': 'Show_Axis', 'title': 'Show Axis?', 'type': 'bool', 'value': False, 'tip': "Show or Remove the Axis"},
                    {'name': 'Show_Plot', 'title': 'Show Plot?', 'type': 'bool', 'value': True, 'tip': "Show or Remove the plot lines"},
                    {'name': 'FFT_Plot', 'title': 'Plot FFT', 'type': 'bool', 'value': False, 'tip': "Show or Remove the FFT Plot"},
                    {'name': 'Histogram_Plot', 'title': 'Plot Histogram', 'type': 'bool', 'value': False, 'tip': "Show or Remove the Histogram Plot"},
                ]},
            ]}
        ]
        p = Parameter.create(name='params', type='group', children=params)
        pChild = p.child(name)
        pChild.sigRemoved.connect(self.parameterSignalRemoved)
        self.parameterChildren[name] = pChild
        self.proxyLatestValue[name] = pg.SignalProxy(self.records[name]['worker'].recordLatestValueSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Value').setValue(x[0][1]))
        self.proxyMean[name] = pg.SignalProxy(self.records[name]['worker'].recordMeanSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Mean').setValue(x[0]))
        self.proxySTD[name] = pg.SignalProxy(self.records[name]['worker'].recordStandardDeviationSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Standard Deviation').setValue(x[0]))
        self.proxyMin[name] = pg.SignalProxy(self.records[name]['worker'].recordMinSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Min').setValue(x[0]))
        self.proxyMax[name] = pg.SignalProxy(self.records[name]['worker'].recordMaxSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Max').setValue(x[0]))
        self.setupAxisList(name, pChild)
        pChild.child('Options').child('Show_Axis').sigValueChanged.connect(lambda x: self.records[name]['axis'].setVisible(x.value()))
        pChild.child('Options').child('Show_Plot').sigValueChanged.connect(lambda x: self.records[name]['curve'].lines.setVisible(x.value()))
        pChild.child('Options').child('FFT_Plot').sigValueChanged.connect(lambda x: self.fftselectionchange.emit(name, x.value()))
        pChild.child('Options').child('Histogram_Plot').sigValueChanged.connect(lambda x: self.histogramplotselectionchange.emit(name, x.value()))
        self.addParameters(p, showTop=False)
        header = self.findItems(name,Qt.MatchContains | Qt.MatchRecursive)[0]
        header.setSelected(False)
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.records[name]['pen']))
        self.proxyHeaderText[name] = pg.SignalProxy(self.records[name]['worker'].recordLatestValueSignal, rateLimit=1, slot=lambda x: header.setText(0,name + ': ' + "{:.4}".format(x[0][1])))
        pChild.child('Options').child('Plot_Colour').sigValueChanging.connect(lambda x, y: self.changePenColour(header,name,y))

    def setupAxisList(self, name, pChild):
        if 'scrollingplot' in self.records[name]:
            pChild.child('Options').child('Axis').setLimits(self.records[name]['scrollingplot'].getAxes())
            self.records[name]['scrollingplot'].toggleAxis(name, False)
            self.records[name]['scrollingplot'].newaxis.connect(lambda x: pChild.child('Options').child('Axis').setValue(self.records[name]['scrollingplot'].getAxes()))
            pChild.child('Options').child('Axis').sigValueChanged.connect(lambda x: self.records[name]['scrollingplot'].changeAxis(name,x.value()))

    def changePenColour(self, header, name, colourWidget):
        colour = colourWidget.value()
        header.setBackground(0,pg.mkBrush(colour))
        header.setForeground(0,self.contrasting_text_color(colour))
        self.records[name]['pen'] = colour
        self.records[name]['curve'].changePenColour()

    def removeParameterSignal(self,name):
        pass
        # name = str(name)
        # self.parameterChildren[name].remove()

class MenuBox(pg.GraphicsObject):
    """
    This class draws a rectangular area. Right-clicking inside the area will
    raise a custom context menu which also includes the context menus of
    its parents.
    """
    def __init__(self, name):
        self.name = name
        self.pen = pg.mkPen('r')

        # menu creation is deferred because it is expensive and often
        # the user will never see the menu anyway.
        self.menu = None

        # note that the use of super() is often avoided because Qt does not
        # allow to inherit from multiple QObject subclasses.
        pg.GraphicsObject.__init__(self)


    # All graphics items must have paint() and boundingRect() defined.
    def boundingRect(self):
        return QtCore.QRectF(0, 0, 10, 10)

    def paint(self, p, *args):
        p.setPen(self.pen)
        p.drawRect(self.boundingRect())


    # On right-click, raise the context menu
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            if self.raiseContextMenu(ev):
                ev.accept()

    def raiseContextMenu(self, ev):
        menu = self.getContextMenus()

        # Let the scene add on to the end of our context menu
        # (this is optional)
        menu = self.scene().addParentContextMenus(self, menu, ev)

        pos = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))
        return True

    # This method will be called when this item's _children_ want to raise
    # a context menu that includes their parents' menus.
    def getContextMenus(self, event=None):
        if self.menu is None:
            self.menu = QtGui.QMenu()
            self.menu.setTitle(self.name+ " options..")

            green = QtGui.QAction("Turn green", self.menu)
            green.triggered.connect(self.setGreen)
            self.menu.addAction(green)
            self.menu.green = green

            blue = QtGui.QAction("Turn blue", self.menu)
            blue.triggered.connect(self.setBlue)
            self.menu.addAction(blue)
            self.menu.green = blue

            alpha = QtGui.QWidgetAction(self.menu)
            alphaSlider = QtGui.QSlider()
            alphaSlider.setOrientation(QtCore.Qt.Horizontal)
            alphaSlider.setMaximum(255)
            alphaSlider.setValue(255)
            alphaSlider.valueChanged.connect(self.setAlpha)
            alpha.setDefaultWidget(alphaSlider)
            self.menu.addAction(alpha)
            self.menu.alpha = alpha
            self.menu.alphaSlider = alphaSlider
        return self.menu

    # Define context menu callbacks
    def setGreen(self):
        self.pen = pg.mkPen('g')
        # inform Qt that this item must be redrawn.
        self.update()

    def setBlue(self):
        self.pen = pg.mkPen('b')
        self.update()

    def setAlpha(self, a):
        self.setOpacity(a/255.)
