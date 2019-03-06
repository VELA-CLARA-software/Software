from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
import numpy as np
import csv
from  functools import partial
from plots import plotWidgets
sys.path.append("../../../")
import Software.Procedures.qt as qt
import Software.Widgets.loggerWidget.loggerWidget as lw
from Software.Procedures.Machine.signaller import machineReciever, machineSignaller
import Software.Utils.dict_to_h5 as h5dict
import Software.Procedures.linacTiming as linacTiming

import logging
logger = logging.getLogger(__name__)

class GenericThread(QThread):
    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.object = self.function(*self.args,**self.kwargs)
        print 'finished!'

class updatingTimer(qt.QThread):
    def __init__(self, name, type, delay, function, *args, **kwargs):
        super(updatingTimer, self).__init__()
        self.name = name
        self.type = type
        self.delay = delay
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.timer = qt.QTimer()
        self.timer.moveToThread(self)
        if self.type == 'widget':
            self.timer.timeout.connect(self.update_monitor_widget)
        elif self.type == 'function':
            self.timer.timeout.connect(self.update_monitor_function)
        self.timer.start(self.delay)
        self.exec_()

    def update_monitor_widget(self):
        val = self.function(*self.args, **self.kwargs)
        self.name.setValue(val)

    def update_monitor_function(self):
        val = self.function(*self.args, **self.kwargs)
        self.name(val)

class Controller(QObject):

    newDataSignal = pyqtSignal(str, str, str, dict)
    loggerSignal = pyqtSignal(object)
    progressSignal = qt.pyqtSignal(int)

    def __init__(self, app, view, model):
        super(Controller, self).__init__()
        '''define model and view'''
        self.view = view
        self.model = model
        self.app = app
        self.model.logger = self.loggerSignal
        self.model.newData = self.newDataSignal
        self.model.progress = self.progressSignal
        self.machineSignaller = machineSignaller(self.model.baseMachine)
        self.machineReciever = machineReciever(self.model.baseMachine)
        self.model.machine = self.machineSignaller
        self.machineSignaller.toMachine.connect(self.machineReciever.toMachine)
        self.machineReciever.fromMachine.connect(self.machineSignaller.fromMachine)
        self.loggerSignal.connect(self.setLabel)
        self.plots = {}

        '''Plots'''
        # Gun
        self.plots['BPM'] = plotWidgets('BPM')
        self.view.BPM_Plots_Layout.addWidget(self.plots['BPM'])

        self.buttons = [
        self.view.HCORRButton, self.view.VCORRButton,
        self.view.runScanButton, self.view.runNegativeScanButton, self.view.runPositiveScanButton,
        self.view.LinacTiming_Off_Button, self.view.LinacTiming_On_Button
        ]

        self.log = lw.loggerWidget()
        self.view.logTabLayout.addWidget(self.log)
        self.log.addLogger(logger)


        self.view.scanWidget.layout().setSpacing(0)
        self.view.abortButton.setVisible(False)
        self.view.HCORRButton.clicked.connect(self.updateStartingHCORRRange)
        self.view.VCORRButton.clicked.connect(self.updateStartingVCORRRange)
        self.view.runScanButton.clicked.connect(self.runScan)
        self.view.individualScanWidget.hide()
        self.view.showIndividualScansButton.clicked.connect(self.toggleIndividualScansWidget)
        self.view.showIndividualScansButton.setArrowType(qt.Qt.DownArrow)
        self.view.runNegativeScanButton.clicked.connect(self.runNegativeScan)
        self.view.runPositiveScanButton.clicked.connect(self.runPositiveScan)
        self.view.actionSave_Data.triggered.connect(self.saveData)
        self.view.actionExit.triggered.connect(sys.exit)

        self.view.LinacTiming_On_Button.clicked.connect(self.setLinac1TimingOn)
        self.view.LinacTiming_Off_Button.clicked.connect(self.setLinac1TimingOff)

        self.view.Linac1_Timing_Monitor.clicked.connect(self.toggleLinac1Timing)


        self.setLabel('MODE: '+self.model.machineType+' '+self.model.lineType+' with '+self.model.gunType+' gun')

        self.progressSignal.connect(self.updateProgress)

        self.monitors = {}
        if not self.model.machineType == 'None':
            self.Linac01Timing = linacTiming.Linac01Timing()
            self.monitors['linac1_timing'] = updatingTimer(self.Linac1_Timing_Monitor, 'function', 250, self.Linac01Timing.isLinacOn)
            self.monitors['linac1_timing'].start()

        self.updateStartingHCORRRange()
        self.updateStartingVCORRRange()

    def toggleVerbose(self, state):
        print 'state = ', state
        self.model.verbose = state

    def setButtonState(self, state=True):
        for b in self.buttons:
            b.setEnabled(state)

    def enableButtons(self):
        self.view.abortButton.setVisible(False)
        self.view.Progress_Monitor.setValue(0)
        self.setButtonState(True)

    def disableButtons(self):
        self.view.abortButton.setVisible(True)
        self.setButtonState(False)

    def updateStartingHCORRRange(self):
        print 'HCORR = ', self.model.machine.getCorr('S01-HCOR2')
        self.view.HCORRStartValue.setValue(self.model.machine.getCorr('S01-HCOR2'))

    def updateStartingVCORRRange(self):
        print 'VCORR = ', self.model.machine.getCorr('S01-VCOR2')
        self.view.VCORRStartValue.setValue(self.model.machine.getCorr('S01-VCOR2'))

    def setLinacTimingOff(self):
        self.setLinac1TimingOff()

    def setLinac1TimingOn(self):
        if not self.model.machineType == 'None':
            self.Linac01Timing.resetTiming()

    def setLinac1TimingOff(self):
        if not self.model.machineType == 'None':
            self.Linac01Timing.offsetTiming(100)

    def toggleLinac1Timing(self):
        if self.Linac01Timing.isLinacOn:
            self.setLinac1TimingOff()
        else:
            self.setLinac1TimingOn()

    def Linac1_Timing_Monitor(self, state):
        if state:
            self.view.LinacTiming_Off_Button.setStyleSheet("background-color: red")
            self.view.LinacTiming_On_Button.setStyleSheet("background-color: green")
            self.view.Linac1_Timing_Monitor.setStyleSheet("background-color: green")
        else:
            self.view.LinacTiming_Off_Button.setStyleSheet("background-color: green")
            self.view.LinacTiming_On_Button.setStyleSheet("background-color: red")
            self.view.Linac1_Timing_Monitor.setStyleSheet("background-color: red")

    def toggleIndividualScansWidget(self):
        if self.view.individualScanWidget.isVisible():
            self.view.individualScanWidget.hide()
            self.view.showIndividualScansButton.setArrowType(qt.Qt.DownArrow)
        else:
            self.view.individualScanWidget.show()
            self.view.showIndividualScansButton.setArrowType(qt.Qt.UpArrow)

    def updatePlot(self, sensor, polarity, actuator, data):
        self.plots[str(sensor)].newData(str(actuator), str(polarity), data)

    def updatePositiveNegativeMomentum(self):
        self.updateNegativeMomentum()
        self.updatePositiveMomentum()
        self.updateAverageMomentum()

    def updateNegativeMomentum(self):
        self.view.negativeMomentumBox.setValue(self.model.solenoidData['negative']['energy'])
        self.updateAverageMomentum()

    def updatePositiveMomentum(self):
        self.view.positiveMomentumBox.setValue(self.model.solenoidData['positive']['energy'])
        self.updateAverageMomentum()

    def updateAverageMomentum(self):
        if 'positive' in self.model.solenoidData and self.model.solenoidData['positive']['energy'] > 0:
            if 'negative' in self.model.solenoidData and self.model.solenoidData['negative']['energy'] > 0:
                self.view.meanMomentumBox.setValue(np.mean([self.model.solenoidData['negative']['energy'], self.model.solenoidData['positive']['energy']]))
            else:
                self.view.meanMomentumBox.setValue(self.model.solenoidData['positive']['energy'])
        elif 'negative' in self.model.solenoidData and  self.model.solenoidData['negative']['energy'] > 0:
            self.view.meanMomentumBox.setValue(self.model.solenoidData['negative']['energy'])

    def runScan(self):
        self.disableButtons()
        self.sensor = 'BPM'
        self.newDataSignal.connect(self.updatePlot)
        # self.model.clearDataArray()
        self.thread = GenericThread(self.model.bpmSol1Scan, self.view.HCORRStartValue.value(), self.view.HCORRRange.value(),
                                    self.view.VCORRStartValue.value(), self.view.VCORRRange.value(), self.view.NSteps.value(),
                                    solenoidInegative=self.view.SolCurrent1.value(), solenoidIpositive=self.view.SolCurrent2.value())
        self.thread.finished.connect(self.enableButtons)
        self.thread.finished.connect(self.saveData)
        self.thread.finished.connect(self.updatePositiveNegativeMomentum)
        self.thread.start()

    def runNegativeScan(self):
        self.disableButtons()
        self.sensor = 'BPM'
        self.newDataSignal.connect(self.updatePlot)
        # self.model.clearDataArray()
        self.thread = GenericThread(self.model.bpmSol1Negative, self.view.HCORRStartValue.value(), self.view.HCORRRange.value(),
                                    self.view.VCORRStartValue.value(), self.view.VCORRRange.value(), self.view.NSteps.value(),
                                    solenoidInegative=self.view.SolCurrent1.value(), solenoidIpositive=self.view.SolCurrent2.value())
        self.thread.finished.connect(self.enableButtons)
        self.thread.finished.connect(self.saveData)
        self.thread.finished.connect(self.updateNegativeMomentum)
        self.thread.start()

    def runPositiveScan(self):
        self.disableButtons()
        self.sensor = 'BPM'
        self.newDataSignal.connect(self.updatePlot)
        # self.model.clearDataArray()
        self.thread = GenericThread(self.model.bpmSol1Positive, self.view.HCORRStartValue.value(), self.view.HCORRRange.value(),
                                    self.view.VCORRStartValue.value(), self.view.VCORRRange.value(), self.view.NSteps.value(),
                                    solenoidInegative=self.view.SolCurrent1.value(), solenoidIpositive=self.view.SolCurrent2.value())
        self.thread.finished.connect(self.enableButtons)
        self.thread.finished.connect(self.saveData)
        self.thread.finished.connect(self.updatePositiveMomentum)
        self.thread.start()

    def updateProgress(self, progress):
        self.view.Progress_Monitor.setValue(progress)

    def setLabel(self, string, severity='info'):
        getattr(logger,severity)(string)
        self.view.label_MODE.setText('Status: <font color="red">' + string + '</font>')

    def saveData(self):
        if self.view.actionAuto_Save_Data.isChecked():
            timestr = time.strftime("%H%M%S")
            savetoworkfolder = self.view.actionSave_to_Work_Folder.isChecked()
            dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\' if savetoworkfolder else './'
            try:
                os.makedirs(dir)
            except OSError:
                if not os.path.isdir(dir):
                    self.logger.emit('Error creating directory - saving to local directory')
                    dir = './'
            filename = dir+timestr+'_SolenoidEnergyScan.h5'
            h5dict.save_dict_to_hdf5(self.model.solenoidData, filename)
