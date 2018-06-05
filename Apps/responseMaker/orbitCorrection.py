import os, sys, time, threading
import readResponseMatrix
sys.path.append(os.path.dirname( os.path.abspath(__file__)) + "/../../../")
from Software.Widgets.generic.pv import *
from Software.Widgets.QLabeledWidget import *
from Software.Widgets.timeAxis import *
import Software.Widgets.Striptool2.generalPlot as generalplot
import Software.Widgets.Striptool2.scrollingPlot as scrollingplot
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
from collections import deque
import numpy as np
from ruamel import yaml
import pyqtgraph as pg
pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

app = None

class monitor(PVBuffer):

    emitAverageSignal = pyqtSignal(str, float, float)

    def __init__(self, pv=None, parent=None):
        super(monitor, self).__init__(pv, parent)
        self.name = pv
        self.samples = 1

    def value(self):
        return [self.name, self.mean, self.std]

    def emitAverage(self):
        a, m, v = self.value()
        if abs(v) > 0:
            self.emitAverageSignal.emit(a, m, v)

    def takeNSamples(self):
        self.reset()
        while self.length < self.samples:
            time.sleep(0.01)
        self.emitAverage()

class monitorThread(QThread):

    startSampling = pyqtSignal()

    def __init__(self, monitorname):
        super(monitorThread, self).__init__()
        self.monitorname =  monitorname
        self.pv = monitor(self.monitorname)
        self.pv.moveToThread(self)
        self._value = 0
        self.startSampling.connect(self.pv.takeNSamples)
        self.pv.emitAverageSignal.connect(self.updateValue)
        self.start()

    def getValue(self):
        return self._value

    def updateValue(self, name, mean, std):
        self._value = mean

    def takeNSamples(self, n):
        self.pv.samples = n
        self.startSampling.emit()

class actuator(PVObject):

    emitChangedSignal = pyqtSignal(str, float, float)

    def __init__(self, pv=None, rdbk=None, parent=None):
        super(actuator, self).__init__(pv, rdbk, parent)
        self.name = pv
        self.writeAccess = True
        self.newValue.connect(self.emitChanged)

    def emitChanged(self):
        # print [self.name, self.value, 0]
        self.emitChangedSignal.emit(self.name, self.value, 0)

class orbitCorrection(QMainWindow):

    def __init__(self):
        super(orbitCorrection, self).__init__()
        self.hrm = readResponseMatrix.horizontalResponseMatrix()
        self.vrm = readResponseMatrix.verticalResponseMatrix()
        self.resetBPMReadings()
        self.readResponseMatrixData()

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)

        self.pushbutton = QPushButton('Start Correction Loop')
        self.pushbutton.clicked.connect(self.startCorrection)
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.tikhonovValueWidget = QLabeledWidget(QDoubleSpinBox(), 'Tikhonov Setting')
        self.tikhonovValueWidget.setMaximumWidth(200)
        self.tikhonovValueWidget.widget.setRange(0.1,100)
        self.tikhonovValueWidget.widget.setSingleStep(0.1)
        self.tikhonovValueWidget.widget.setKeyboardTracking(False)

        self.bpmGroupBox = QGroupBox('Monitors')
        self.bpmGroupBox.setSizePolicy(sizePolicy)
        self.bpmGroupBox.setLayout(QVBoxLayout())
        self.bpmListWidget = QListWidget()
        self.bpmListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.bpmListWidget.itemDoubleClicked.connect(self.toggleChecked)
        self.bpmGroupBox.layout().addWidget(self.bpmListWidget)

        self.actuatorGroupBox = QGroupBox('Actuators')
        self.bpmGroupBox.setSizePolicy(sizePolicy)
        self.actuatorGroupBox.setLayout(QVBoxLayout())
        self.actuatorListWidget = QListWidget()
        self.actuatorListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.actuatorListWidget.itemDoubleClicked.connect(self.toggleChecked)
        # self.actuatorListWidget.itemDoubleClicked.connect(lambda x: self.toggleChecked)
        self.actuatorGroupBox.layout().addWidget(self.actuatorListWidget)

        self.generalBPMPlot = generalplot.generalPlot()
        self.bpmPlotWidget = self.generalBPMPlot.scrollingPlot()
        self.bpmPlotWidget.setPlotScale(60)
        self.generalActuatorPlot = generalplot.generalPlot()
        self.actuatorPlotWidget = self.generalActuatorPlot.scrollingPlot()
        self.actuatorPlotWidget.setPlotScale(60)

        # self.actuatorPlotWidget = bpmPlotter('Actuators')
        for p, a in enumerate(self.hactuators):
            item = QListWidgetItem(a, self.actuatorListWidget)
            item.setCheckState(Qt.Checked)
            self.generalActuatorPlot.addSignal(name=a, pen=p, timer=1.0/10.0, function=self.hactuators[a].getValue)
            item.setBackground(pg.mkColor(pg.mkColor(p)))

        for p,m in enumerate(self.hmonitors):
            item = QListWidgetItem(m, self.bpmListWidget)
            item.setCheckState(Qt.Checked)
            self.generalBPMPlot.addSignal(name=m, pen=p, timer=1.0/10.0, function=self.hmonitors[m].getValue)
            item.setBackground(pg.mkColor(pg.mkColor(p)))

        self.generalBPMPlot.start()
        self.bpmPlotWidget.start()
        self.generalActuatorPlot.start()
        self.actuatorPlotWidget.start()
        self.bpmPlotWidget.setYRange(-10,10)
        self.actuatorPlotWidget.setYRange(-6,6)

        self.plotGroupBox = QGroupBox('Plots')
        self.plotGroupBox.setLayout(QVBoxLayout())
        self.plotTabWidget = QTabWidget()
        self.plotTabWidget.addTab(self.bpmPlotWidget, 'BPMs')
        self.plotTabWidget.addTab(self.actuatorPlotWidget, 'Actuators')
        self.plotGroupBox.layout().addWidget(self.plotTabWidget)

        self.settingsGroupBox = QGroupBox('Settings')
        self.settingsGroupBox.setSizePolicy(sizePolicy)
        self.settingsGroupBox.setLayout(QVBoxLayout())
        self.selectionWidget = QWidget()
        self.selectionWidgetLayout = QHBoxLayout()
        self.selectionWidget.setLayout(self.selectionWidgetLayout)
        self.selectionWidgetLayout.addWidget(self.actuatorGroupBox)
        self.selectionWidgetLayout.addWidget(self.bpmGroupBox)
        self.settingsGroupBox.layout().addWidget(self.tikhonovValueWidget)
        self.settingsGroupBox.layout().addWidget(self.selectionWidget)
        self.settingsGroupBox.layout().addWidget(self.pushbutton)
        self.layout.addWidget(self.settingsGroupBox)
        self.layout.addWidget(self.plotGroupBox,0,1,5,3)
        self.startBPMTimer()

    def toggleChecked(self, item):
        state = 0 if item.checkState() == 2 else 2
        item.setCheckState(state)
        name = str(item.text())
        if name in self.generalBPMPlot.records.keys():
            self.generalBPMPlot.records[name]['axis'].setVisible(bool(state))
            self.generalBPMPlot.records[name]['curve'].curve.setVisible(bool(state))
        elif name in self.generalActuatorPlot.records.keys():
            self.generalActuatorPlot.records[name]['axis'].setVisible(bool(state))
            self.generalActuatorPlot.records[name]['curve'].curve.setVisible(bool(state))

    def readResponseMatrixData(self):
        self.hactuators = OrderedDict()
        for a in self.hrm.actuators:
            self.hactuators[a] = actuator(a+':SETI')

        self.vactuators = OrderedDict()
        for a in self.vrm.actuators:
            self.vactuators[a] = actuator(a+':SETI')

        self.hmonitors = OrderedDict()
        for a in self.hrm.monitors:
            name = a.replace('-X',':X')
            self.hmonitors[a] = monitorThread(name)
            app.aboutToQuit.connect(self.hmonitors[a].quit)

        self.vmonitors = OrderedDict()
        for a in self.vrm.monitors:
            self.vmonitors[a] = monitorThread(a.replace('-Y',':Y'))
            app.aboutToQuit.connect(self.vmonitors[a].quit)

    def getStartingHActuators(self, actuators):
        return [self.hactuators[a].value for a in actuators]

    def getStartingVActuators(self, actuators):
        return [self.vactuators[a].value for a in actuators]

    def resetBPMReadings(self):
        self.BPMHReadings = {}

    def addBPMReading(self, name, mean, std):
        self.BPMHReadings[str(name)] = [mean,std]

    def startBPMHReadings(self):
        self.finishedBPMReadings = False
        self.resetBPMReadings()
        for m in self.hmonitors.values():
            m.pv.emitAverageSignal.connect(self.addBPMReading)
            m.takeNSamples(10)
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkBPMReadings)
        self.timer.start(10)

    def setBPMPlotXRange(self):
        current_time = time.time()
        # self.bpmPlotWidget.plot.vb.setXRange(current_time-30, current_time)

    def startBPMTimer(self):
        self.bpmTimer = QTimer()
        self.bpmTimer.timeout.connect(self.startBPMHReadings)
        self.bpmTimer.timeout.connect(self.setBPMPlotXRange)
        self.bpmTimer.start(100)

    def checkBPMReadings(self):
        if len(self.BPMHReadings) == len(self.hmonitors):
            self.finishedBPMReadings = True
            self.timer.stop()

    def SVDInverse(self, hrm, tikhonov=1):
        u, s, vh = np.linalg.svd(np.transpose(hrm), full_matrices=False)
        sinv = [(a/(a**2 + tikhonov)) if abs(a) > 0 else 0 for a in s]
        sinv[0] = 0
        smat = np.diag(sinv)
        # return np.linalg.pinv(np.transpose(hrm), rcond=0.5)
        return  np.dot(vh.conj().T, np.dot(smat, u.conj().T))

    def doCorrection(self):
        # self.startBPMHReadings()
        while not self.finishedBPMReadings:
            time.sleep(0.01)
            app.processEvents()
        selectedActuators = self.checkedItems(self.actuatorListWidget)
        selectedBPMs = self.checkedItems(self.bpmListWidget)

        hrm = self.hrm.createResponseMatrix(actuators=selectedActuators, monitors=selectedBPMs)
        invmat = self.SVDInverse(hrm)
        startingactuators = np.array(self.getStartingHActuators(selectedActuators))

        x = [-1*self.BPMHReadings[a.replace('-X',':X')][0] for a in selectedBPMs]
        new_values = startingactuators + np.dot(invmat, x)
        # for n, o, a,v in zip(self.hactuators.keys(), startingactuators, self.hactuators.values(), new_values):
            # a.put(v)

    def checkedItems(self, list):
        checked_items = []
        for index in range(list.count()):
            if list.item(index).checkState() == Qt.Checked:
                checked_items.append(str(list.item(index).text()) )
        return checked_items

    def stopCorrection(self):
        self.corrTimer.stop()
        self.pushbutton.setFlat(False)
        self.pushbutton.setText('Start Correction Loop')
        self.pushbutton.clicked.connect(self.startCorrection)
        self.pushbutton.clicked.disconnect(self.stopCorrection)

    def startCorrection(self):
        self.pushbutton.setFlat(True)
        self.pushbutton.setText('Stop Correction Loop')
        self.pushbutton.clicked.disconnect(self.startCorrection)
        self.pushbutton.clicked.connect(self.stopCorrection)
        self.corrTimer = QTimer()
        self.corrTimer.timeout.connect(self.doCorrection)
        self.corrTimer.start(100)

class bpmPlotter(pg.PlotWidget):

    date_axis = HAxisTime(orientation = 'bottom')

    def __init__(self, title=None, parent=None):
        super(bpmPlotter, self).__init__(parent, axisItems={'bottom':self.date_axis})
        if title is not None:
            self.setLabels(title=title)
        self.plotItem = self.getPlotItem()
        self.plotItem.showGrid(x=True, y=True)
        self.bpmPlots = {}
        self.bpmLinePlots = {}
        self.data = {}
        self.colors = {}
        self.color = 0

    def newLine(self, monitor):
        monitor = str(monitor).replace(':X','-X')
        print 'new Line = ', monitor
        self.colors[monitor] = self.color
        self.data[monitor] = deque(maxlen=50)
        self.bpmLinePlots[monitor] = self.plotItem.plot(pen=pg.mkColor(self.colors[monitor]))
        self.color += 1

    def reset(self):
        for p in self.bpmPlots:
            self.data[p] = deque(maxlen=20)
            self.bpmPlots[p].clear()

    def newBPMReading(self, monitor, mean, std):
        monitor = str(monitor).replace(':X','-X')
        if monitor in self.data.keys():
            self.data[monitor].append([time.time(), mean, std])
            x, y, h = map(lambda x: np.array(x), zip(*self.data[monitor]))
            if not monitor in self.bpmPlots:
                self.bpmPlots[monitor] = pg.ErrorBarItem(x=x, y=y, height=h, beam=None, pen=pg.mkColor(self.colors[monitor]))
                self.addItem(self.bpmPlots[monitor])
            else:
                self.bpmPlots[monitor].setData(x=x, y=y, height=h)
            self.bpmLinePlots[monitor].setData(x=x, y=y)
        else:
            print monitor, monitor in self.data.keys()

def main():
    global app
    app = QApplication(sys.argv)
    oc = orbitCorrection()
    oc.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()

# for m in self.monitors:
#     m.reset()
# length = np.min([m.length for m in self.monitors])
# while length < 100:
#     length = np.min([m.length for m in self.monitors])
#     app.processEvents()
