import sys, os
from PyQt5.QtCore import *
from  PyQt5.QtGui import *
from  PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import random, time
sys.path.append(os.path.dirname( os.path.abspath(__file__)) + "/../../../")
from Software.Widgets.generic.pv import *
pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
from collections import OrderedDict
import yaml
import tables as tables


_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

with open(os.path.dirname( os.path.abspath(__file__))+'/responseSettings.yaml', 'r') as infile:
    responseSettings = yaml.load(infile)

monitors = responseSettings['monitors']
actuators = responseSettings['actuators']

class responseMaker(QMainWindow):
    def __init__(self, parent = None):
        super(responseMaker, self).__init__(parent)

        stdicon = self.style().standardIcon
        style = QStyle
        self.setWindowTitle("RF Cavity Cresting Application")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.newButton = QPushButton('Reset')

        self.tabs = QTabWidget()
        for a in actuators:
            self.tabs.addTab(responsePlotterTab(a), a)
        # self.layout.addWidget(self.newButton,0,0)
        self.layout.addWidget(self.tabs,0,0,6,6)

class monitor(PVBuffer):

    emitAverageSignal = pyqtSignal(str, str, list)

    def __init__(self, pv=None, actuator=None, parent=None):
        super(monitor, self).__init__(pv, parent)
        self.name = pv
        self.actuator = actuator
        #self._value = random.random()-0.5

    def value(self):
        return [self.actuator.name, self.name, [self.actuator.value, self.mean]]

    def emitAverage(self):
        a, m, v = self.value()
        self.emitAverageSignal.emit(a,m,v)

class corrector(PVObject):
    def __init__(self, pv=None, rdbk=None, parent=None):
        super(corrector, self).__init__(pv, rdbk, parent)
        self.name = pv
        self.writeAccess = False

class recordRMData(tables.IsDescription):
    actuator  = tables.Float64Col()     # double (double-precision)
    monitor  = tables.Float64Col()

class responsePlotterTab(QWidget):
    def __init__(self, actuator=None, parent=None):
        super(responsePlotterTab, self).__init__(parent)
        self.name = actuator
        self.pv = corrector(self.name, self.name.replace(':SETI',':READI'))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.buttonLayout = QHBoxLayout()
        self.runButton = QPushButton('Run')
        self.runButton.setMaximumWidth(100)
        self.runButton.clicked.connect(self.runResponse)
        self.buttonLayout.addWidget(self.runButton)
        self.progressBar = QProgressBar()
        self.progressBar.setMaximumWidth(100)
        self.progressBar.hide()
        self.buttonLayout.addWidget(self.progressBar)
        self.saveButton = QPushButton('Save Data')
        self.saveButton.setMaximumWidth(100)
        self.saveButton.clicked.connect(self.saveData)
        self.buttonLayout.addWidget(self.saveButton)

        self.layout.addLayout(self.buttonLayout)

        self.plotTabs = QTabWidget()
        self.plots = {}
        self.layout.addWidget(self.plotTabs)

        self.horizontalPlot = responsePlot(self.name)
        self.plotTabs.addTab(self.horizontalPlot, 'Horizontal')
        self.verticalPlot = responsePlot(self.name)
        self.plotTabs.addTab(self.verticalPlot, 'Vertical')

        self.monitors = []
        type = '_H'
        for m in monitors:
            self.monitors.append(monitor(m+type, self.pv))
            self.horizontalPlot.newLine(m+type)
            self.monitors[-1].emitAverageSignal.connect(self.horizontalPlot.newBPMReading)
        type = '_V'
        for m in monitors:
            self.monitors.append(monitor(m+type, self.pv))
            self.verticalPlot.newLine(m+type)
            self.monitors[-1].emitAverageSignal.connect(self.verticalPlot.newBPMReading)

    def saveData(self):
        self.h5file = tables.open_file(self.name+'.h5', mode = "w", title = self.name)
        self.rootnode = self.h5file.get_node('/')
        for m in ['horizontal','vertical']:
            group = self.h5file.create_group('/', m, m+' Data')
            self.savePlotData(group, getattr(self,m+'Plot'))
        self.h5file.close()

    def savePlotData(self, group, plot):
        for d in plot.data:
            table = self.h5file.create_table(group, d, recordRMData, d)
            row = table.row
            data = plot.data[d]
            self.saveRow(row, data)
            table.flush()

    def saveRow(self, row, data):
        for a, m in data:
            row['actuator'], row['monitor'] = a, m
            row.append()

    def resetPlots(self):
        self.horizontalPlot.reset()
        self.verticalPlot.reset()
        self.phasePlot.reset()
        self.intensityPlot.reset()

    def runResponse(self):
        global app
        self.resetPlots()
        self.runButton.setEnabled(False)
        self.runButton.clicked.disconnect(self.runResponse)
        min = -0.1#self.pv.pv.lower_disp_limit
        max = 0.1#self.pv.pv.upper_disp_limit
        range = self.generateRange(min, max)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(range))
        self.progressBar.setValue(0)
        self.runButton.hide()
        self.progressBar.show()
        startValue = self.pv.value
        for j, i in enumerate(range):
            self.pv.setValue(startValue+i)
            for m in self.monitors:
                m.reset()
            length = np.min([m.length for m in self.monitors])
            while length < 3:
                length = np.min([m.length for m in self.monitors])
                app.processEvents()
            # print ('i = ', i)
            for m in self.monitors:
                m.emitAverage()
            self.progressBar.setValue(j)
        self.pv.value = startValue
        self.runButton.setEnabled(True)
        self.runButton.clicked.connect(self.runResponse)
        self.runButton.show()
        self.progressBar.hide()

    def generateRange(self, min, max):
        data = []
        value = 10.0
        while abs(value) > 0.1:
            data.append(value)
            data.append(-1. * value)
            value = value / np.sqrt(2)
        data.append(0)
        data = np.array(data)
        data = ((data + 10) * ((max-min)/20)) + min
        return list(sorted(data))

class responsePlot(pg.PlotWidget):
    def __init__(self, actuator=None, parent=None):
        super(responsePlot, self).__init__(parent)
        self.actuator = actuator
        self.plotItem = self.getPlotItem()
        self.plotItem.showGrid(x=True, y=True)
        self.bpmPlots = {}
        self.fittedPlots = {}
        self.data = {}
        self.color = 0

    def newLine(self, monitor):
        self.data[monitor] = np.empty((0,2),int)
        self.bpmPlots[monitor] = self.plotItem.plot(symbol='+', symbolPen=pg.mkColor(self.color))
        self.fittedPlots[monitor] = self.plotItem.plot(pen=pg.mkColor(self.color))
        self.color += 1

    def reset(self):
        for p in self.bpmPlots:
            self.data[p] = np.empty((0,2),int)
            self.bpmPlots[p].clear()
            self.fittedPlots[p].clear()

    def newBPMReading(self, actuator, monitor, data):
        if actuator == self.actuator and monitor in self.data:
            self.data[monitor] = np.append(self.data[monitor], [data], axis=0)
            self.bpmPlots[monitor].setData(self.data[monitor])

    def newFittedReading(self, actuator, monitor, data):
        if actuator == self.actuator and monitor in self.data:
            self.fittedPlots[monitor].setData(np.array(data))

def main():
    global app
    app = QApplication(sys.argv)
    ex = responseMaker()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
