import time, sys, os
import numpy as np
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4 import QtTest
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import scipy.constants as constants
from scipy.optimize import curve_fit
sys.path.append(os.path.dirname( os.path.abspath(__file__)) + "/../../../")
from Software.Widgets.generic.pv import *
import pyqtgraph as pg
import numpy as np
import tables as tables

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

degree = constants.pi/180.0
q_e = constants.elementary_charge
c = constants.speed_of_light

def qSleep(time):
    QtTest.QTest.qWait(time)

actuators = ['CLA-C18-TIM-EVR-01:Pul3-Delay-SP', 'CLA-C18-TIM-EVR-01:Pul4-Delay-SP', 'CLA-C18-TIM-EVR-02:Pul1-Delay-SP']

class Linac(QObject):

    def __init__(self):
        super(Linac, self).__init__()
        self.modulator_timing = PVObject(actuators[0])
        self.modulator_timing.writeAccess = True
        self.modulator_timing_readback = PVObject(actuators[0].replace('SP','RB'))
        self.amplifier_timing = PVObject(actuators[1])
        self.amplifier_timing.writeAccess = True
        self.amplifier_timing_readback = PVObject(actuators[1].replace('SP','RB'))
        self.LLRF_timing = PVObject(actuators[2])
        self.LLRF_timing.writeAccess = True
        self.LLRF_timing_readback = PVObject(actuators[2].replace('SP','RB'))

        self.setList = [self.modulator_timing, self.amplifier_timing, self.LLRF_timing]
        self.readbackList = [self.modulator_timing_readback, self.amplifier_timing_readback, self.LLRF_timing_readback]

        self.initialValues()

    def initialValues(self):
        self.modulator_timing_initial, self.amplifier_timing_initial, self.LLRF_timing_initial = [a.getValue() for a in self.setList]
        self.initialValues = self.modulator_timing_initial, self.amplifier_timing_initial, self.LLRF_timing_initial
        return self.initialValues

    def changeTiming(self, offset=0):
        for a, initial in zip(self.setList, self.initialValues):
            print 'setting timing ', a, ' = ', initial+offset
            a.put(initial+offset)

    def reset(self):
        for a, initial in zip(self.setList, self.initialValues):
            print 'setting timing ', a, ' = ', initial
            a.put(initial)

class recordRMData(tables.IsDescription):
    offset  = tables.Float64Col()     # double (double-precision)
    bpmReading  = tables.Float64Col()

class BPM(QObject):
    def __init__(self):
        super(BPM, self).__init__()
        self.pv = PVBuffer("CLA-C2V-DIA-BPM-01:X")

    def get_reading(self, nsamples=10):
        self.pv.reset()
        length = self.pv.length
        while length < nsamples:
            length = self.pv.length
            qSleep(0.1)
        return self.pv.mean

class recordBPMData(tables.IsDescription):
    time  = tables.Float64Col()     # double (double-precision)
    bpmReading  = tables.Float64Col()


class Accelerator(QObject):

    newBPMReading = pyqtSignal(str, list)

    def __init__(self):
        super(Accelerator, self).__init__()
        self.bpm = BPM()
        self.linac = Linac()

    def emitSignal(self, offset=0, bpmReading=0):
        for a in actuators:
            self.newBPMReading.emit(a, [offset, bpmReading])

    def setTiming(self, offset=0):
        self.linac.changeTiming(offset)
        lastbpmreading = self.bpm.get_reading(300)
        print 'bpm = ', lastbpmreading
        self.emitSignal(offset, lastbpmreading)
        self.saveData(offset)

    def saveData(self, offset=0):
        self.h5file = tables.open_file('timing_'+("%.2f" % offset)+'_bpm_C2V.h5', mode = "w")
        self.rootnode = self.h5file.get_node('/')
        group = self.h5file.create_group('/', 'c2vbpm01', 'c2v-bpm-01')
        self.savebpmData(group, self.bpm.pv.buffer)
        self.h5file.close()

    def savebpmData(self, group, data):
        table = self.h5file.create_table(group, 'data', recordBPMData, 'data')
        row = table.row
        self.saveRow(row, data)
        table.flush()

    def saveRow(self, row, data):
        for a, m, g in data:
            row['time'], row['bpmReading'] = a, m
            row.append()

    def scan(self):
        self.linac.reset()
        for i in np.arange(-0.06,0.1,0.01):
            self.setTiming(i)
        self.linac.reset()

class linacPhaseScan(QMainWindow):
    def __init__(self, parent = None):
        super(linacPhaseScan, self).__init__(parent)

        stdicon = self.style().standardIcon
        style = QStyle
        self.setWindowTitle("RF Timing Application")

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

        self.newButton = QPushButton('Scan')
        self.accelerator = Accelerator()
        self.newButton.clicked.connect(self.accelerator.scan)

        self.saveButton = QPushButton('Save Data')
        self.saveButton.clicked.connect(self.saveData)

        self.tabs = QTabWidget()
        self.plots = {}
        for a in actuators:
            plot = plotter(a)
            self.plots[a] = plot
            self.tabs.addTab(plot, a)
            self.accelerator.newBPMReading.connect(plot.newBPMReading)
        self.layout.addWidget(self.newButton,0,0)
        self.layout.addWidget(self.saveButton,0,1)
        self.layout.addWidget(self.tabs,1,0,6,6)

    def saveData(self):
        self.h5file = tables.open_file('energy_vs_timing.h5', mode = "w")
        self.rootnode = self.h5file.get_node('/')
        group = self.h5file.create_group('/', 'c2vbpm01', 'c2v-bpm-01')
        self.savePlotData(group, self.plots[actuators[0]])
        self.h5file.close()

    def savePlotData(self, group, plot):
        table = self.h5file.create_table(group, 'data', recordRMData, 'data')
        row = table.row
        data = plot.data
        self.saveRow(row, data)
        table.flush()

    def saveRow(self, row, data):
        for a, m in data:
            row['offset'], row['bpmReading'] = a, m
            row.append()

class plotter(pg.PlotWidget):
    def __init__(self, actuator=None, parent=None):
        super(plotter, self).__init__(parent)
        self.actuator = actuator
        self.plotItem = self.getPlotItem()
        self.plotItem.showGrid(x=True, y=True)
        self.color = 0
        self.data = np.empty((0,2),int)
        self.bpmPlot = self.plotItem.plot(symbol='+', symbolPen=pg.mkColor(self.color))
        self.fittedPlot = self.plotItem.plot(pen=pg.mkColor(self.color))

    def reset(self):
        self.data = np.empty((0,2),int)
        self.bpmPlots.clear()
        self.fittedPlots.clear()

    def newBPMReading(self, actuator, data):
        if actuator == self.actuator:
            self.data = np.append(self.data, [data], axis=0)
            self.bpmPlot.setData(self.data)

def main():
    app = QApplication(sys.argv)
    ex = linacPhaseScan()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()

# linac = Linac()
# print linac.initialValues()
# bpm = BPM()
# print bpm.get_reading()
