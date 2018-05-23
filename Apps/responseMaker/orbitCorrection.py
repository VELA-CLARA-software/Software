import os, sys, time, threading
import readResponseMatrix
sys.path.append(os.path.dirname( os.path.abspath(__file__)) + "/../../../")
from Software.Widgets.generic.pv import *
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *

import numpy as np
from ruamel import yaml

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

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
        self.emitAverageSignal.emit(a,m,v)

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
        self.startSampling.connect(self.pv.takeNSamples)
        self.start()

    def takeNSamples(self, n):
        self.pv.samples = n
        self.startSampling.emit()

class actuator(PVObject):
    def __init__(self, pv=None, rdbk=None, parent=None):
        super(actuator, self).__init__(pv, rdbk, parent)
        self.name = pv
        self.writeAccess = True

class orbitCorrection(QMainWindow):

    def __init__(self):
        super(orbitCorrection, self).__init__()
        self.hrm = readResponseMatrix.horizontalResponseMatrix()
        self.vrm = readResponseMatrix.verticalResponseMatrix()
        self.resetBPMReadings()
        self.readResponseMatrixData()

        self.pushbutton = QPushButton('Start')
        self.pushbutton.clicked.connect(self.startCorrection)
        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.bpmListWidget = QListWidget()
        self.bpmListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        for m in self.hmonitors:
            item = QListWidgetItem(m, self.bpmListWidget)
            item.setCheckState(Qt.Checked)
        self.bpmListWidget.itemDoubleClicked.connect(self.toggleChecked)

        self.actuatorListWidget = QListWidget()
        self.actuatorListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        for a in self.hactuators:
            item = QListWidgetItem(a, self.actuatorListWidget)
            item.setCheckState(Qt.Checked)

        self.selectionWidget = QWidget()
        self.selectionWidgetLayout = QHBoxLayout()
        self.selectionWidget.setLayout(self.selectionWidgetLayout)
        self.selectionWidgetLayout.addWidget(self.bpmListWidget)
        self.selectionWidgetLayout.addWidget(self.actuatorListWidget)
        self.layout.addWidget(self.selectionWidget)
        self.layout.addWidget(self.pushbutton)

    def toggleChecked(self, item):
        state = 0 if item.checkState() == 2 else 2
        item.setCheckState(state)

    def readResponseMatrixData(self):
        self.hactuators = OrderedDict()
        for a in self.hrm.actuators:
            self.hactuators[a] = actuator(a+':SETI')

        self.vactuators = OrderedDict()
        for a in self.vrm.actuators:
            self.vactuators[a] = actuator(a+':SETI')

        self.hmonitors = OrderedDict()
        for a in self.hrm.monitors:
            self.hmonitors[a] = monitorThread(a.replace('-X',':X'))

        self.vmonitors = OrderedDict()
        for a in self.vrm.monitors:
            self.vmonitors[a] = monitorThread(a.replace('-Y',':Y'))

    def getStartingHActuators(self):
        return [a.value for a in self.hactuators.values()]

    def getStartingVActuators(self):
        return [a.value for a in self.vactuators.values()]

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

    def checkBPMReadings(self):
        if len(self.BPMHReadings) == len(self.hmonitors):
            self.finishedBPMReadings = True
            self.timer.stop()

    def SVDInverse(self):
        u, s, vh = np.linalg.svd(np.transpose(self.hrm.responseMatrix), full_matrices=False)
        sinv = [1/a if abs(a) > 0 else 0 for a in s]
        # print sinv
        sinv[0] = 0
        smat = np.diag(sinv)
        # print 's = ', smat
        # print ' inverse = ', np.dot(vh.conj().T, np.dot(smat, u.conj().T))
        # print 'linalg = ',  np.linalg.pinv(np.transpose(self.hrm.responseMatrix), rcond=0.5)
        return np.linalg.pinv(np.transpose(self.hrm.responseMatrix), rcond=0.5)
        # return  np.dot(vh.conj().T, np.dot(smat, u.conj().T))

    def doCorrection(self):
        global app
        self.startBPMHReadings()
        while not self.finishedBPMReadings:
            time.sleep(0.01)
            app.processEvents()
        selectedActuators = self.checkedItems(self.actuatorListWidget)
        selectedBPMs = self.checkedItems(self.bpmListWidget)
        print selectedBPMs, selectedActuators
        hrm = self.hrm.createResponseMatrix(actuators=selectedActuators, monitors=selectedBPMs)
        invmat = self.SVDInverse()
        startingactuators = np.array(self.getStartingHActuators())
        print self.hrm.monitors
        x = [-1*self.BPMHReadings[a.replace('-X',':X')][0] for a in self.hrm.monitors]
        # x[0] = 0
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
        self.pushbutton.setText('Start')
        self.pushbutton.clicked.connect(self.startCorrection)
        self.pushbutton.clicked.disconnect(self.stopCorrection)

    def startCorrection(self):
        self.pushbutton.setFlat(True)
        self.pushbutton.setText('Stop')
        self.pushbutton.clicked.disconnect(self.startCorrection)
        self.pushbutton.clicked.connect(self.stopCorrection)
        self.corrTimer = QTimer()
        self.corrTimer.timeout.connect(self.doCorrection)
        self.corrTimer.start(100)

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
