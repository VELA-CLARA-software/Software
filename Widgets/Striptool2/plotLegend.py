import pyqtgraph as pg
import sys, time, os, datetime, sip
sys.path.append("../../../")
import Software.Procedures.qt as qt
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

class plotLegend(qt.QWidget):

    pausePlottingSignal = qt.pyqtSignal(bool)

    def __init__(self, generalplot):
        super(plotLegend, self).__init__()
        self.tree = plotLegendTree(generalplot)
        self.layout = qt.QVBoxLayout()
        self.layout.addWidget(self.tree)
        self.buttonLayout = qt.QHBoxLayout()
        self.pauseButton = qt.QPushButton('Pause')
        self.pauseButton.setCheckable(True)
        self.pauseButton.clicked.connect(self.pauseButtonClicked)
        self.buttonLayout.addWidget(self.pauseButton)
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)

    def pauseButtonClicked(self, value):
        if self.pauseButton.text() == 'Pause':
            self.pauseButton.setText('Resume')
            self.pausePlottingSignal.emit(True)
        else:
            self.pauseButton.setText('Pause')
            self.pausePlottingSignal.emit(False)

class plotLegendTree(ParameterTree):

    fftselectionchange = qt.pyqtSignal('QString',bool)
    histogramplotselectionchange = qt.pyqtSignal('QString',bool)
    axisselectionchanged = qt.pyqtSignal('QString')
    legendselectionchanged = qt.pyqtSignal(list)
    savecurve = qt.pyqtSignal(str)

    def __init__(self, generalplot):
        super(plotLegendTree, self).__init__(generalplot)
        ''' Create Parameter Tree'''
        self.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
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
        self.proxyMean10 = {}
        self.proxyMean100 = {}
        self.proxyMean1000 = {}
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
                pos = [pos for pos, char in enumerate(text) if char == ':']
                if len(pos) > 0:
                    pos = pos[-1]
                else:
                    pos = -1
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
        # print 'Signal Removed! Name = ', parameter
        self.proxyLatestValue[name].disconnect()
        self.proxyLatestValue[name].disconnect()
        self.proxyMean[name].disconnect()
        self.proxySTD[name].disconnect()
        self.proxyMin[name].disconnect()
        self.proxyMax[name].disconnect()
        self.proxyHeaderText[name].disconnect()
        pChild = self.parameterChildren[name]
        self.records[name]['viewbox'].sigStateChanged.disconnect()
        try:
            self.generalPlot.removeSignal(str(name))
        except Exception as e:
            print 'Exception in signal removal: ', e
        finally:
            for i in range(self.topLevelItemCount()):
                item = self.topLevelItem(i)
                if item is not None and item.childCount() < 1:
                    index =  self.indexOfTopLevelItem(item)
                    try:
                        self.takeTopLevelItem(index)
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
                    {'name': 'Mean10', 'title': 'Moving Average 10 Shots', 'type': 'bool', 'value': False},
                    {'name': 'Mean100', 'title': 'Moving Average 100 Shots', 'type': 'bool', 'value': False},
                    {'name': 'Mean1000', 'title': 'Moving Average 1000 Shots', 'type': 'bool', 'value': False},
                    {'name': 'ClearStats', 'title': 'Clear Statistics', 'type': 'action', 'tip': "Reset Statistics"},
                ]},
                {'name': 'Options', 'type': 'group', 'removable': False, 'expanded': False, 'children': [
                    {'name': 'Plot_Colour', 'title': 'Line Colour', 'type': 'color', 'value': self.records[name]['pen'], 'tip': "Line Colour"},
                    # {'name': 'Axis', 'title': 'Choose Axis', 'type': 'list', 'values': {}, 'value': self.records[name]['axisname'], 'tip': "Choose which axis to display on"},
                    {'name': 'AxisAutoScale', 'title': 'Enable Autoscaling', 'type': 'bool', 'value': True, 'tip': "Enable autoscaling for this axis"},
                    {'name': 'Plot Range', 'type': 'group', 'removable': False, 'expanded': False, 'children': [
                        {'name': 'AxisZero', 'title': 'Set Axis to Zero', 'type': 'bool', 'tip': "Set Axis to start from 0"},
                        {'name': 'RangeLower', 'title': 'From:', 'type': 'float', 'tip': "Set axis lower range"},
                        {'name': 'RangeUpper', 'title': 'To:', 'type': 'float', 'tip': "Set axis upper range"},
                    ]},
                    {'name': 'Log_Mode', 'title': 'Log Mode', 'type': 'bool', 'value': self.records[name]['logScale'], 'tip': "Set Log mode scaling"},
                    {'name': 'Show_Axis', 'title': 'Show Axis?', 'type': 'bool', 'value': False, 'tip': "Show or Remove the Axis"},
                    {'name': 'Show_Plot', 'title': 'Show Plot?', 'type': 'bool', 'value': True, 'tip': "Show or Remove the plot lines"},
                    {'name': 'FFT_Plot', 'title': 'Plot FFT', 'type': 'bool', 'value': False, 'tip': "Show or Remove the FFT Plot"},
                    {'name': 'Histogram_Plot', 'title': 'Plot Histogram', 'type': 'bool', 'value': False, 'tip': "Show or Remove the Histogram Plot"},
                ]},
                {'name': 'Save_Curve', 'type': 'action', 'tip': "Save Curve Data"},
            ]}
        ]
        p = Parameter.create(parent=self, name='params', type='group', children=params)
        self.addParameters(p, showTop=False)
        pChild = p.child(name)
        pChild.sigRemoved.connect(self.parameterSignalRemoved)
        self.parameterChildren[name] = pChild
        self.proxyLatestValue[name] = pg.SignalProxy(self.records[name]['worker'].recordLatestValueSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Value').setValue(x[0][1]))
        self.proxyMean[name] = pg.SignalProxy(self.records[name]['worker'].recordMeanSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Mean').setValue(x[0]))
        self.proxySTD[name] = pg.SignalProxy(self.records[name]['worker'].recordStandardDeviationSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Standard Deviation').setValue(x[0]))
        self.proxyMin[name] = pg.SignalProxy(self.records[name]['worker'].recordMinSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Min').setValue(x[0]))
        self.proxyMax[name] = pg.SignalProxy(self.records[name]['worker'].recordMaxSignal, rateLimit=1, slot=lambda x: pChild.child('Statistics').child('Max').setValue(x[0]))
        pChild.child('Statistics').child('Mean10').sigValueChanged.connect(lambda x: self.records[name]['curve'].setVisibility('curve10', x.value()))
        pChild.child('Statistics').child('Mean100').sigValueChanged.connect(lambda x: self.records[name]['curve'].setVisibility('curve100', x.value()))
        pChild.child('Statistics').child('Mean1000').sigValueChanged.connect(lambda x: self.records[name]['curve'].setVisibility('curve1000', x.value()))
        pChild.child('Statistics').child('ClearStats').sigActivated.connect(lambda x: self.records[name]['worker'].resetStatistics(True))
        # self.setupAxisList(name, pChild)
        pChild.child('Options').child('Show_Axis').sigValueChanged.connect(lambda x: self.records[name]['axis'].setVisible(x.value()))
        pChild.child('Options').child('Plot Range').child('AxisZero').sigValueChanged.connect(lambda x: self.setAxisFromZero(name, pChild))

        list(pChild.child('Options').child('Plot Range').child('RangeLower').items.keys())[0].widget.editingFinished.connect(lambda : self.setAxisLowRange(name, pChild))
        list(pChild.child('Options').child('Plot Range').child('RangeUpper').items.keys())[0].widget.editingFinished.connect(lambda : self.setAxisHighRange(name, pChild))
        self.records[name]['viewbox'].sigStateChanged.connect(lambda x: self.vbRangeChanged(x, pChild))

        pChild.child('Options').child('Log_Mode').sigValueChanged.connect(lambda x: self.records[name]['curve'].setLogMode(x.value()))
        pChild.child('Options').child('Show_Plot').sigValueChanged.connect(lambda x: self.records[name]['curve'].setVisibility('curve', x.value()))
        pChild.child('Options').child('FFT_Plot').sigValueChanged.connect(lambda x: self.fftselectionchange.emit(name, x.value()))
        pChild.child('Options').child('Histogram_Plot').sigValueChanged.connect(lambda x: self.histogramplotselectionchange.emit(name, x.value()))
        self.records[name]['viewbox'].sigStateChanged.connect(lambda x: pChild.child('Options').child('AxisAutoScale').setValue(x.state['autoRange'][1]))
        pChild.child('Options').child('AxisAutoScale').sigValueChanged.connect(lambda x: self.records[name]['viewbox'].enableAutoRange(y=x.value()))
        pChild.child('Save_Curve').sigActivated.connect(lambda x: self.savecurve.emit(str(name)))

        header = self.findItems(name,qt.Qt.MatchContains | qt.Qt.MatchRecursive)[0]
        header.setSelected(False)
        header.setExpanded(False)
        header.setForeground(0,self.contrasting_text_color(self.records[name]['pen']))
        header.setBackground(0,pg.mkBrush(self.records[name]['pen']))
        self.proxyHeaderText[name] = pg.SignalProxy(self.records[name]['worker'].recordLatestValueSignal, rateLimit=1, slot=lambda x: header.setText(0,name + ': ' + "{:.4}".format(x[0][1])))
        pChild.child('Options').child('Plot_Colour').sigValueChanging.connect(lambda x, y: self.changePenColour(header,name,y))

    def setAxisFromZero(self, name, pChild):
        if pChild.child('Options').child('Plot Range').child('AxisZero').value() is True:
            self.records[name]['viewbox'].enableAutoRange(y=False)
            currentrange = self.records[name]['viewbox'].viewRange()
            self.records[name]['viewbox'].setYRange(0, currentrange[1][1], padding=0)
            self.setAxisZeroState(self.records[name]['viewbox'], pChild)

    def setAxisLowRange(self, name, pChild):
            lowrange = pChild.child('Options').child('Plot Range').child('RangeLower').value()
            self.records[name]['viewbox'].enableAutoRange(y=False)
            currentrange = self.records[name]['viewbox'].viewRange()
            self.records[name]['viewbox'].setYRange(lowrange, currentrange[1][1], padding=0)

    def setAxisHighRange(self, name, pChild):
        highrange = pChild.child('Options').child('Plot Range').child('RangeUpper').value()
        self.records[name]['viewbox'].enableAutoRange(y=False)
        currentrange = self.records[name]['viewbox'].viewRange()
        self.records[name]['viewbox'].setYRange(currentrange[1][0], highrange, padding=0)

    def vbRangeChanged(self, vb, pChild):
        currentrange = vb.state['viewRange'][1]
        pChild.child('Options').child('Plot Range').child('RangeLower').setValue(currentrange[0])
        pChild.child('Options').child('Plot Range').child('RangeUpper').setValue(currentrange[1])
        self.setAxisZeroState(vb, pChild)

    def setAxisZeroState(self, vb, pChild):
        try:
            if not abs(vb.state['viewRange'][1][0]) == 0:
                list(pChild.child('Options').child('Plot Range').child('AxisZero').items.keys())[0].widget.setCheckState(False)
        except:
            pass

    def setupAxisList(self, name, pChild):
        if 'scrollingplot' in self.records[name]:
            pChild.child('Options').child('Axis').setLimits(self.records[name]['scrollingplot'].getAxes())
            self.records[name]['scrollingplot'].toggleAxis(name, False)
            self.records[name]['scrollingplot'].newaxis.connect(lambda: pChild.child('Options').child('Axis').setLimits(self.records[name]['scrollingplot'].getAxes()))
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
        return qt.RectF(0, 0, 10, 10)

    def paint(self, p, *args):
        p.setPen(self.pen)
        p.drawRect(self.boundingRect())


    # On right-click, raise the context menu
    def mouseClickEvent(self, ev):
        if ev.button() == qt.t.RightButton:
            if self.raiseContextMenu(ev):
                ev.accept()

    def raiseContextMenu(self, ev):
        menu = self.getContextMenus()

        # Let the scene add on to the end of our context menu
        # (this is optional)
        menu = self.scene().addParentContextMenus(self, menu, ev)

        pos = ev.screenPos()
        menu.popup(qt.Point(pos.x(), pos.y()))
        return True

    # This method will be called when this item's _children_ want to raise
    # a context menu that includes their parents' menus.
    def getContextMenus(self, event=None):
        if self.menu is None:
            self.menu = qt.Menu()
            self.menu.setTitle(self.name+ " options..")

            green = qt.Action("Turn green", self.menu)
            green.triggered.connect(self.setGreen)
            self.menu.addAction(green)
            self.menu.green = green

            blue = qt.Action("Turn blue", self.menu)
            blue.triggered.connect(self.setBlue)
            self.menu.addAction(blue)
            self.menu.green = blue

            alpha = qt.WidgetAction(self.menu)
            alphaSlider = qt.Slider()
            alphaSlider.setOrientation(qt.t.Horizontal)
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
