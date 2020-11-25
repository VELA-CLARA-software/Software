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
sys.path.append(os.path.dirname( os.path.abspath(__file__)) + "/../../../")
from Software.Widgets.generic.pv import *
from Software.Widgets.QLabeledWidget import *
import pyqtgraph as pg
import tables as tables

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

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
        self.modulator_timing_initial, self.amplifier_timing_initial, self.LLRF_timing_initial = [397.0, 382.5, 401.0]
        self.initialValues = self.modulator_timing_initial, self.amplifier_timing_initial, self.LLRF_timing_initial
        return self.initialValues

    def changeTiming(self, actuator, offset=0):
        for a, initial in zip(self.setList, self.initialValues):
            if a.name == actuator or a.name in actuator:
                print 'setting timing ', a.name, ' = ', initial+offset
                a.put(initial+offset)

    def reset(self):
        for a, initial in zip(self.setList, self.initialValues):
            print 'setting timing ', a.name, ' = ', initial
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

    newBPMReading = pyqtSignal('PyQt_PyObject', list)
    scanFinished = pyqtSignal()

    def __init__(self, actuator):
        super(Accelerator, self).__init__()
        self.bpm = BPM()
        self.linac = Linac()
        self.actuator = actuator
        self.stopScanning = False

    def emitSignal(self, offset=0, bpmReading=0):
        self.newBPMReading.emit(self.actuator, [offset, bpmReading])

    def setTiming(self, offset=0, nsamples=10):
        self.linac.changeTiming(self.actuator, offset)
        lastbpmreading = self.bpm.get_reading(nsamples)
        print 'bpm = ', lastbpmreading
        self.emitSignal(offset, lastbpmreading)
        self.saveData(offset)

    def saveData(self, offset=0):
        if isinstance(self.actuator, list):
            filename = str('combined_timing_'+("%.2f" % offset)+'_bpm_C2V.h5')
        else:
            filename = str(self.actuator.replace(':','.'))+'_timing_'+("%.2f" % offset)+'_bpm_C2V.h5'
        print 'filename = ', filename
        self.h5file = tables.open_file(filename, mode = "w")
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

    def scan(self, start=-0.05, stop=0.05, step=0.01, nsamples=10):
        self.stopScanning = False
        self.linac.reset()
        for i in np.arange(start,stop,step):
            self.setTiming(i, nsamples)
            if self.stopScanning == True:
                print 'stopping scan = ', self.stopScanning
                break
        self.linac.reset()
        self.scanFinished.emit()
        self.stopScanning = False

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

        self.widget = QTabWidget()
        self.widget.addTab(linacPhaseScanWidget(actuators), "Combined")
        for a in actuators:
            self.widget.addTab(linacPhaseScanWidget(a), a)
        self.setCentralWidget(self.widget)

class linacPhaseScanWidget(QWidget):
    def __init__(self, actuator = None, parent = None):
        super(linacPhaseScanWidget, self).__init__(parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.actuator = actuator
        self.accelerator = Accelerator(actuator)

        self.resetButton = QPushButton('Reset Timing')
        self.resetButton.clicked.connect(self.accelerator.linac.reset)

        self.runButton = QPushButton('Scan')
        self.runButton.clicked.connect(self.doScan)

        self.saveButton = QPushButton('Save Data')
        self.saveButton.clicked.connect(self.saveData)

        self.start = QLabeledWidget(QLineEdit(),"Start")
        self.stop = QLabeledWidget(QLineEdit(),"Stop")
        self.step = QLabeledWidget(QLineEdit(),"Step")
        self.nsamples = QLabeledWidget(QLineEdit(),"Samples")
        self.start.widget.setValidator(QDoubleValidator())
        self.stop.widget.setValidator(QDoubleValidator())
        self.step.widget.setValidator(QDoubleValidator())
        self.nsamples.widget.setValidator(QIntValidator(0,1000))
        self.start.widget.setText('-0.06')
        self.stop.widget.setText('0.1')
        self.step.widget.setText('0.01')
        self.nsamples.widget.setText('100')


        self.settingsLayout = QHBoxLayout()
        self.settingsLayout.addWidget(self.start)
        self.settingsLayout.addWidget(self.stop)
        self.settingsLayout.addWidget(self.step)
        self.settingsLayout.addWidget(self.nsamples)

        self.plot = plotter(actuator)
        self.accelerator.newBPMReading.connect(self.plot.newBPMReading)
        self.layout.addWidget(self.resetButton,0,0)
        self.layout.addWidget(self.runButton,0,1)
        self.layout.addWidget(self.saveButton,0,2)
        self.layout.addLayout(self.settingsLayout,1,0,1,4)
        # self.layout.addWidget(self.stop,1,1)
        # self.layout.addWidget(self.step,1,2)
        self.layout.addWidget(self.plot,2,0,6,6)

    def doScan(self):
        self.runButton.setText("Stop!")
        self.runButton.clicked.disconnect(self.doScan)
        self.runButton.clicked.connect(self.stopScan)
        self.accelerator.scanFinished.connect(self.scanFinished)
        self.accelerator.scan(float(self.start.widget.text()), float(self.stop.widget.text()), float(self.step.widget.text()), int(self.nsamples.widget.text()))

    def scanFinished(self):
        self.runButton.setText("Scan")
        self.runButton.clicked.connect(self.doScan)
        print 'Scan Finished!'

    def stopScan(self):
        self.accelerator.stopScanning = True

    def saveData(self):
        if isinstance(self.actuator, list):
            self.h5file = tables.open_file('combined_energy_vs_timing.h5', mode = "w")
        else:
            self.h5file = tables.open_file(self.actuator+'_energy_vs_timing.h5', mode = "w")
        self.rootnode = self.h5file.get_node('/')
        group = self.h5file.create_group('/', 'c2vbpm01', 'c2v-bpm-01')
        self.savePlotData(group, self.plot)
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
