from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import pyqtgraph as pg
pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release")
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_Charge_Control as scope
import VELA_CLARA_PILaser_Control as laser

class testApp(QMainWindow):

    actuator = 'DIP01'
    #actuator = 'linac1'
    monitor = 'C2V-BPM01'
    samplesPerReading = 3
    start = 5
    stop = 12
    stepSize = 0.1
    data = []

    def __init__(self, parent=None):
        super(testApp, self).__init__(parent)
        self.setUp_Controllers()

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widgetLayout = QVBoxLayout()
        self.widget.setLayout(self.widgetLayout)

        self.startButton = QPushButton('Start Scan')
        self.startButton.clicked.connect(self.crestingFunction)

        self.plotWidget = responsePlot()

        self.widgetLayout.addWidget(self.startButton)
        self.widgetLayout.addWidget(self.plotWidget)
        self.crestingData = {}
        for cavity in [self.actuator]:
            self.crestingData[cavity]={'approxPhaseData': [], 'approxChargeData': [], 'approxPhaseFit': [], 'approxChargeFit': [], 'finePhaseFit': [],
                                        'fineBPMFit': [], 'finePhaseData': [], 'fineBPMData': [], 'approxChargeStd': [], 'fineBPMStd': []}
        self.calibrationPhase = {self.actuator: None}

    def setUp_Controllers(self):
        self.magInit = mag.init()
        self.magInit.setQuiet()
        self.bpmInit = bpm.init()
        self.bpmInit.setVerbose()
        self.llrfInit = llrf.init()
        self.llrfInit.setQuiet()
        self.scopeInit = scope.init()
        self.scopeInit.setQuiet()

        self.magnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
        self.scope = self.scopeInit.physical_CLARA_PH1_Charge_Controller()
        self.bpm = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
        self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
        self.linac1llrf = self.llrfInit.physical_L01_LLRF_Controller()

    def changeActuator(self, value):
        #self.linac1llrf.setPhiSP(value)
        print(testApp.actuator)
        print(value)
        self.magnets.setSI(testApp.actuator,value)


    def readMonitor(self):
        return self.bpm.getXFromPV(self.monitor)
        #return self.bpm.getCharge(self.monitor)

    def crestingFunction(self):
        self.startButton.setEnabled(False)
        self.startButton.clicked.disconnect(self.crestingFunction)
        self.resetDataArray()
        self.doActuatorMonitorScan()
        self.doFit()
        self.startButton.setEnabled(True)
        self.startButton.clicked.connect(self.crestingFunction)

    def resetDataArray(self):
        self.crestingData[self.actuator]['approxPhaseFit'] = []
        self.crestingData[self.actuator]['approxChargeFit'] = []
        self.crestingData[self.actuator]['approxPhaseData'] = []
        self.crestingData[self.actuator]['approxChargeData'] = []
        self.crestingData[self.actuator]['approxChargeStd'] = []

    def doActuatorMonitorScan(self):
        for actuatorValue in np.arange(self.start, self.stop, self.stepSize):
            global app
            app.processEvents()
            self.changeActuator(actuatorValue)
            data, stddata = self.getData()
            self.setData(actuatorValue, data, stddata)

    def setData(self, phase, data, stddata):
        self.plotWidget.newReading([phase, data])
        self.crestingData[self.actuator]['approxChargeData'].append(data)
        self.crestingData[self.actuator]['approxPhaseData'].append(phase)
        self.crestingData[self.actuator]['approxChargeStd'].append(stddata)

    def setFitData(self, phase, data):
        self.plotWidget.newFittedReading(zip(phase,data))

    def getData(self):
        global app
        self.data = []
        while len(self.data) < self.samplesPerReading:
            time.sleep(0.1)
            app.processEvents()
            self.data.append(self.readMonitor())
        return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.01 else [20,0]

    def cutData(self):
        allData = zip(self.crestingData[self.actuator]['approxPhaseData'], self.crestingData[self.actuator]['approxChargeData'], self.crestingData[self.actuator]['approxChargeStd'])
        cutData = [a for a in allData if a[1] < 15 and a[1] > -15 ]
        return cutData

    def doFit(self):
        try:
            cutData = self.cutData()
            x, y, std = zip(*cutData)
            crest_phase = np.mean(x)

            print 'Crest phase is ', crest_phase

            # self.setFinalPhase(crest_phase)
            print 'Calibration phase is', self.calibrationPhase[self.actuator]
            # self.finishedSuccesfully.emit()
        except Exception as e:
            print(e)
            print 'Error in fitting!'


class responsePlot(pg.PlotWidget):
    def __init__(self, parent=None):
        super(responsePlot, self).__init__(parent)
        self.plotItem = self.getPlotItem()
        self.plotItem.showGrid(x=True, y=True)
        self.bpmPlots = {}
        self.fittedPlots = {}
        self.data = {}
        self.color = 0
        self.line = self.newLine('a')

    def newLine(self, monitor):
        print 'new Line = ', monitor
        self.data[monitor] = np.empty((0,2),int)
        self.bpmPlots[monitor] = self.plotItem.plot(symbol='+', symbolPen=pg.mkColor(self.color))
        self.fittedPlots[monitor] = self.plotItem.plot(pen=pg.mkColor(self.color))
        print 'Lines = ', self.data
        self.color += 1

    def reset(self):
        for p in self.bpmPlots:
            self.data[p] = np.empty((0,2),int)
            self.bpmPlots[p].clear()
            self.fittedPlots[p].clear()

    def newReading(self, data):
        monitor = 'a'
        self.data[monitor] = np.append(self.data[monitor], [data[:2]], axis=0)
        self.bpmPlots[monitor].setData(self.data[monitor])

    def newFittedReading(self, monitor, data):
        if monitor in self.data:
            self.fittedPlots[monitor].setData(np.array(data))


def main():
    global app
    app = QApplication(sys.argv)
    ex = testApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
