import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import sys, time, os, datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class stripLegend(pg.TreeWidget):

    logScaleChanged = pyqtSignal('PyQt_PyObject','PyQt_PyObject')

    def __init__(self, stripTool, parent = None):
        super(stripLegend, self).__init__(parent)
        self.stripTool = stripTool
        self.records = stripTool.records
        self.layout = pg.TreeWidget()
        self.layout.header().close()
        self.layout.setColumnCount(2)
        self.layout.header().setResizeMode(0,QtGui.QHeaderView.Stretch)
        self.layout.setColumnWidth(2,50)
        self.layout.header().setStretchLastSection(False)
        self.newRowNumber = 0
        self.deleteIcon  = QtGui.QIcon(str(os.path.dirname(os.path.abspath(__file__)))+'\icons\delete.png')

    def addTreeWidget(self, parent, name, text, widget):
        child = QtGui.QTreeWidgetItem()
        child.setText(0, text)
        parent.addChild(child)
        self.layout.setItemWidget(child,1,widget)
        return child

    def addLegendItem(self, name):
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
            if self.records[name]['timer'] == 1.0/rate:
                selected = i
            i += 1
        signalRate.setCurrentIndex(selected)
        signalRate.currentIndexChanged.connect(lambda x: self.changeSampleRate(name, signalRate))
        self.addTreeWidget(parentTreeWidget, name, "Signal Rate", signalRate)
        maxlength = QSpinBox()
        maxlength.setMinimum(1)
        maxlength.setMaximum(pow(2,24))
        maxlength.setValue(self.records[name]['maxlength'])
        maxlength.editingFinished.connect(lambda: self.changeMaxLength(name, maxlength))
        self.addTreeWidget(parentTreeWidget, name, "Signal Length", maxlength)
        ''' Vertical LOG Scale'''
        verticallogscale = QCheckBox()
        verticallogscale.setChecked(self.records[name]['logscale'])
        verticallogscale.toggled.connect(lambda x: self.toggleLogScale(name, x))
        self.addTreeWidget(parentTreeWidget, name, "Log Scale", verticallogscale)
        ''' Vertical Scale'''
        verticalscale = QDoubleSpinBox()
        verticalscale.setDecimals(12)
        verticalscale.setMinimum(0.000000000001)
        verticalscale.setMaximum(10000000000000)
        verticalscale.setSingleStep(0.1)
        verticalscale.setValue(self.records[name]['VerticalScale'])
        verticalscale.setKeyboardTracking(False)
        verticalscale.valueChanged.connect(lambda: self.changeVerticalScale(name, verticalscale))
        self.addTreeWidget(parentTreeWidget, name, "Signal Scale", verticalscale)
        ''' Vertical Offset'''
        verticaloffset = QDoubleSpinBox ()
        verticaloffset.setMinimum(-1000)
        verticaloffset.setMaximum(1000)
        verticaloffset.setSingleStep(0.01)
        verticaloffset.setValue(self.records[name]['VerticalOffset'])
        verticaloffset.setKeyboardTracking(False)
        verticaloffset.valueChanged.connect(lambda: self.changeVerticalOffset(name, verticaloffset))
        self.addTreeWidget(parentTreeWidget, name, "Signal Offset", verticaloffset)
        ''' Signal Centered'''
        verticalMeanSubtraction = QCheckBox()
        verticalMeanSubtraction.setChecked(self.records[name]['verticalMeanSubtraction'])
        verticalMeanSubtraction.toggled.connect(lambda x: self.toggleVerticalMeanSubtraction(name, x))
        self.addTreeWidget(parentTreeWidget, name, "SubtractMean", verticalMeanSubtraction)
        ''' Signal Plot Color'''
        colorbox = pg.ColorButton()
        colorbox.setFixedSize(30,25)
        colorbox.setFlat(True)
        colorbox.setColor(self.records[name]['pen'])
        colorbox.sigColorChanged.connect(lambda x: self.changePenColor(name, x))
        colorbox.sigColorChanging.connect(lambda x: self.changePenColor(name, x))
        self.addTreeWidget(parentTreeWidget, name, "Plot Color", colorbox)
        saveButton = QPushButton('Save Data')
        saveButton.setFixedSize(74,20)
        saveButton.setFlat(True)
        saveButton.clicked.connect(lambda x: self.saveCurve(name))
        self.addTreeWidget(parentTreeWidget, name, "Save Signal", saveButton)
        resetButton = QPushButton('Clear')
        resetButton.setFixedSize(50,20)
        resetButton.setFlat(True)
        resetButton.clicked.connect(lambda x: self.clearCurve(name))
        self.addTreeWidget(parentTreeWidget, name, "Clear Signal", resetButton)
        deleteRowButton = QPushButton()
        deleteRowButton.setFixedSize(50,20)
        deleteRowButton.setFlat(True)
        deleteRowButton.setIcon(self.deleteIcon)
        self.addTreeWidget(parentTreeWidget, name, "Delete Signal", deleteRowButton)
        deleteRowButton.clicked.connect(lambda x: self.deleteRow(name, parentTreeWidget))
        self.newRowNumber += 1

    def changeVerticalScale(self, name, verticalscale):
        self.records[name]['VerticalScale'] = verticalscale.value()
        if verticalscale.value() < 1:
            verticalscale.setSingleStep(0.01)
        if verticalscale.value() < 0.1:
            verticalscale.setSingleStep(0.001)
        if verticalscale.value() < 0.01:
            verticalscale.setSingleStep(0.0001)

    def changeVerticalOffset(self, name, verticaloffset):
        self.records[name]['VerticalOffset'] = verticaloffset.value()

    def changeMaxLength(self, name, maxlength):
        self.records[name]['maxlength'] = maxlength.value()

    def toggleVerticalMeanSubtraction(self, name, value):
        self.records[name]['verticalMeanSubtraction'] = value

    def formatCurveData(self, name):
        # return [(str(time.strftime('%Y/%m/%d', time.localtime(x[0]))),str(datetime.datetime.fromtimestamp(x[0]).strftime('%H:%M:%S.%f')),x[1]) for x in self.records[name]['data']]
        return self.records[name]['data']

    def saveCurve(self, name, saveFileName=None):
        if saveFileName == None:
            saveFileName = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Array ['+name+']', name, filter="CSV files (*.csv);; Binary Files (*.bin)", selectedFilter="CSV files (*.csv)"))
        filename, file_extension = os.path.splitext(saveFileName)
        saveData = self.formatCurveData(name)
        if file_extension == '.csv':
            # fmt='%s,%s,%.18e'
            fmt='%.11e,%.6e'
            target = open(saveFileName,'w')
            for row in saveData:
                target.write((fmt % tuple(row))+'\n')
            target.close()
        elif file_extension == '.bin':
            np.array(self.records[name]['data']).tofile(saveFileName)
        else:
            np.save(saveFileName,np.array(self.records[name]['data']))

    def changePenColor(self, name, widget):
        self.records[name]['pen'] = widget._color

    def togglePlotOnOff(self, name, value):
        self.records[name]['ploton'] = value

    def toggleLogScale(self, name, value):
        self.records[name]['logscale'] = value
        self.logScaleChanged.emit(name,value)

    def changeSampleRate(self, name, widget):
        string = str(widget.currentText())
        number = [int(s) for s in string.split() if s.isdigit()]
        number = string[0:-3]
        print 'number = ', number
        if len(number) > 0:
            number = float(number)
            value = 1.0/float(number)
            self.records[name]['timer'] = value
            self.records[name]['record'].setInterval(value)

    def clearCurve(self, name):
        self.records[name]['data'] = []
        self.records[name]['curve'].clear()

    def deleteRow(self, name, child):
        row = self.layout.indexOfTopLevelItem(child)
        self.layout.takeTopLevelItem(row)
        self.clearCurve(name)
        self.stripTool.removeSignal(name)
