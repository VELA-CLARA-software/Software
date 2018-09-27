from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import csv
from  functools import partial
sys.path.append("../../../")
import Software.Widgets.loggerWidget.loggerWidget as lw
from Software.Procedures.Machine.signaller import machineReciever, machineSignaller
import logging
logger = logging.getLogger(__name__)
from plots import *

class GenericThread(QThread):
    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.object = self.function(*self.args,**self.kwargs)
        print 'finished!'

class Controller(QObject):

    newDataSignal = pyqtSignal()
    loggerSignal = pyqtSignal(str)

    def __init__(self, view, model):
        super(Controller, self).__init__()
        '''define model and view'''
        self.view = view
        self.model = model
        self.model.logger = self.loggerSignal
        self.model.newData = self.newDataSignal
        self.machineSignaller = machineSignaller(self.model.baseMachine)
        self.machineReciever = machineReciever(self.model.baseMachine)
        self.model.machine = self.machineSignaller
        self.machineSignaller.toMachine.connect(self.machineReciever.toMachine)
        self.machineReciever.fromMachine.connect(self.machineSignaller.fromMachine)
        self.loggerSignal.connect(self.setLabel)
        self.plots = {}

        '''Plots'''
        pg.setConfigOption('background', 'w')
        # Gun
        # LINAC1
        self.plots['Linac1'] = plotWidgets('Linac1', self.view.tabWidget_plotsLinac1)

        self.plots['Linac1BLM'] = plotWidgetsBLM('Linac1BLM', self.view.tabWidget_plotsLinac1BLM)

        self.plots['L01-SOL1'] = plotWidgets('L01-SOL1', self.view.tabWidget_plotsSol1)

        self.plots['L01-SOL2'] = plotWidgets('L01-SOL2', self.view.tabWidget_plotsSol2)

        self.buttons = [
        self.view.linac1StartRoughScanButton, self.view.linac1StartFineScanButton, self.view.linac1SetRFCentreButton,
        self.view.linac1BLMStartRoughScanButton, self.view.linac1BLMStartFineScanButton,
        self.view.sol1StartRoughScanButton, self.view.sol1StartFineScanButton,
        self.view.sol2StartRoughScanButton, self.view.sol2StartFineScanButton
        ]

        self.log = lw.loggerWidget()
        self.view.logTabLayout.addWidget(self.log)
        self.log.addLogger(logger)

        self.view.linac1StartRoughScanButton.clicked.connect(self.linac1RoughScan)
        self.view.linac1StartFineScanButton.clicked.connect(self.linac1FineScan)
        self.view.linac1SetRFCentreButton.clicked.connect(self.linac1SetRFCentre)
        self.view.linac1BLMStartRoughScanButton.clicked.connect(self.linac1BLMRoughScan)
        self.view.linac1BLMStartFineScanButton.clicked.connect(self.linac1BLMFineScan)
        self.view.sol1StartRoughScanButton.clicked.connect(self.sol1RoughScan)
        self.view.sol1StartFineScanButton.clicked.connect(self.sol1FineScan)
        self.view.sol2StartRoughScanButton.clicked.connect(self.sol2RoughScan)
        self.view.sol2StartFineScanButton.clicked.connect(self.sol2FineScan)
        self.view.abortButton.hide()
        self.view.abortButton.clicked.connect(self.abortRunning)
        self.view.finishButton.hide()
        self.view.finishButton.clicked.connect(self.finishRunning)
        self.view.actionSave_Calibation_Data.triggered.connect(self.saveData)
        self.toggleVerbose(self.view.saveDataCheckbox.isChecked())
        self.view.saveDataCheckbox.toggled.connect(self.toggleVerbose)
        self.setLabel('MODE: '+self.model.machineType+' '+self.model.lineType+' with '+self.model.gunType+' gun')

        ''' this loads some data to make the plot for Linac'18 paper'''
        # self.fakePlot()

    def toggleVerbose(self, state):
        print 'state = ', state
        self.model.verbose = state

    def setButtonState(self, state=True):
        for b in self.buttons:
            b.setEnabled(state)

    def enableButtons(self):
        self.setButtonState(True)
        try:
            self.view.finishButton.clicked.disconnect(self.finishRunning)
            self.view.finishButton.hide()
        except:
            pass
        try:
            self.view.abortButton.clicked.disconnect(self.abortRunning)
            self.view.abortButton.hide()
        except:
            pass

    def disableButtons(self):
        self.setButtonState(False)
        self.view.finishButton.clicked.connect(self.finishRunning)
        self.view.finishButton.show()
        self.view.abortButton.clicked.connect(self.abortRunning)
        self.view.abortButton.show()

    def abortRunning(self):
        if hasattr(self,'thread'):
            self.model.abort()
            self.thread.quit()
            self.enableButtons()

    def finishRunning(self):
        if hasattr(self,'thread'):
            self.thread.function.finish()

    def updatePlot(self):
        self.plots[self.cavity].plot(self.model.sub, self.plane, self.model.experimentalData[self.model.main][self.model.sub])

    def fakePlot(self):
        ''' this function is used to load some data to make the plot for Linac'18 paper'''
        columns = ['x', 'y', 'z1', 'z2', 'diff']
        fakedata = []
        with open('20180810-190936_LinacCentring_Linac1_X_10000_17000_rawData - FINE Scan In X With Cameras.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                line = []
                for c in columns:
                    line.append(row[c])
                fakedata.append(line)
        x,y,z1,z2,diff = zip(*fakedata)
        x = map(float, x)
        y = map(float,y)
        diff = map(eval, diff)
        diff = map(lambda x: x if x == 100 else x, diff)
        print x, diff
        self.plots['Linac1'].plot('approx', 'X', {'x': x, 'y': y, 'z': diff})

    def solScan(self, scanfunction, stepsize):
        self.disableButtons()
        self.thread = GenericThread(scanfunction, self.plane,
            self.view.sol1LowerSet.value(), \
            self.view.sol1UpperSet.value(), \
            [self.view.Corr1_Min.value(), self.view.Corr1_Max.value()], \
            [self.view.Corr2_Min.value(), self.view.Corr2_Max.value()], \
            stepsize, \
            self.view.nSamples.value() \
        )
        self.thread.finished.connect(self.updatePlot)
        self.thread.finished.connect(self.enableButtons)
        self.thread.start()

    def sol1RoughScan(self):
        self.cavity = 'L01-SOL1'
        self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
        self.solScan(self.model.sol1Scan, self.view.roughStepSetCorrector.value())

    def sol2RoughScan(self):
        self.cavity = 'L01-SOL2'
        self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
        self.solScan(self.model.sol2Scan, self.view.roughStepSetCorrector.value())

    def sol1FineScan(self):
        self.cavity = 'L01-SOL1'
        self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
        self.solScan(self.model.sol1Scan, self.view.fineStepSetCorrector.value())

    def sol2FineScan(self):
        self.cavity = 'L01-SOL2'
        self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
        self.solScan(self.model.sol2Scan, self.view.fineStepSetCorrector.value())

    def linac1Scan(self, scanfunction, actuator, stepsize):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.thread = GenericThread(scanfunction, actuator, self.plane, \
            self.view.linac1LowerSet.value(), \
            self.view.linac1UpperSet.value(), \
            [self.view.Corr1_Min.value(), self.view.Corr1_Max.value()], \
            [self.view.Corr2_Min.value(), self.view.Corr2_Max.value()], \
            stepsize, \
            self.view.nSamples.value() \
        )
        self.thread.finished.connect(self.updatePlot)
        self.thread.finished.connect(self.enableButtons)
        self.thread.start()

    def linac1SetRFCentre(self):
        self.disableButtons()
        self.thread = GenericThread(self.model.setRFCentreFit)
        self.thread.finished.connect(self.enableButtons)
        self.thread.start()

    def linac1RoughScan(self):
        self.cavity = 'Linac1'
        self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
        self.linac1Scan(self.model.linac1Scan, 'approx', self.view.roughStepSetCorrector.value())

    def linac1FineScan(self):
        self.cavity = 'Linac1'
        self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
        self.linac1Scan(self.model.linac1Scan, 'fine', self.view.fineStepSetCorrector.value())

    def updatePlotBLM(self):
        self.plots[self.cavity].plot(self.model.experimentalData[self.model.main])

    def linac1ScanBLM(self, scanfunction, actuator, stepsize):
        self.disableButtons()
        self.cavity = 'Linac1BLM'
        self.thread = GenericThread(scanfunction, actuator, \
            self.view.linac1LowerSet.value(), \
            self.view.linac1UpperSet.value(), \
            self.view.nSamples.value() \
        )
        self.thread.finished.connect(self.updatePlotBLM)
        self.thread.finished.connect(self.enableButtons)
        self.thread.start()

    def linac1BLMRoughScan(self):
        self.cavity = 'Linac1BLM'
        self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
        self.linac1ScanBLM(self.model.linac1BLMScan, 'approx', self.view.roughStepSetCorrector.value())

    def linac1BLMFineScan(self):
        self.cavity = 'Linac1BLM'
        self.plane = 'X' if self.view.horizontalRadio.isChecked() else 'Y'
        self.linac1ScanBLM(self.model.linac1BLMScan, 'fine', self.view.fineStepSetCorrector.value())

    def setLabel(self, string):
        logger.info(string)
        self.view.label_MODE.setText('Status: <font color="red">' + string + '</font>')

    def saveData(self):
        for cavity in ['Linac1', 'L01-SOL1',  'L01-SOL2']:
            if cavity in self.model.experimentalData:
                print cavity
                my_dict = {}
                for name in ['x', 'y', 'z']:
                    my_dict[name] = self.model.experimentalData[cavity]['approx'][name]
                print my_dict
                with open(cavity+'_approx_experimentalData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
                    w = csv.DictWriter(f, my_dict.keys())
                    w.writeheader()
                    w.writerow(my_dict)
                my_dict = {}
                for name in ['x', 'y', 'z']:
                    my_dict[name] = self.model.experimentalData[cavity]['fine'][name]
                with open(cavity+'_fine_experimentalData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
                    w = csv.DictWriter(f, my_dict.keys())
                    w.writeheader()
                    w.writerow(my_dict)
