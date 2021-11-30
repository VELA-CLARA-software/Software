import sys
import os
import time
import ruamel.yaml
sys.path.append("../../../")
from Software.Apps.AutoPhaseCalibv2.controller.plots import *
from  functools import partial
import Software.Procedures.qt as qt
from Software.Procedures.Machine.signaller import machineReciever, machineSignaller
import Software.Widgets.loggerWidget.loggerWidget as lw

import logging
logger = logging.getLogger(__name__)

import functools
def debugLog(func):
    @functools.wraps(func)
    def logfunction(*args, **kwargs):
        debugStr = str(func.__name__)+' called'
        if len(args) > 1:
            debugStr += ' args='+str(args[1:])
        if len(kwargs) > 0:
            debugStr += ' kwargs='+str(kwargs)
        getattr(logger, 'debug')(debugStr)
        value = func(*args, **kwargs)
        return value
    return logfunction

class GenericThread(qt.QThread):

    result = qt.pyqtSignal(object)

    @debugLog
    def __init__(self, function, *args, **kwargs):
        qt.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.function(*self.args, **self.kwargs)
        self.result.emit(result)

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

class Controller(qt.QObject):

    newDataSignal = qt.pyqtSignal()
    # loggerSignal = qt.pyqtSignal(str)
    loggerSignal = qt.pyqtSignal(['QString','QString'], ['QString'])
    progressSignal = qt.pyqtSignal(int)

    defaults = {'Gun_Amp_Step_Set': 100,
    'Gun_Amp_Set': 16000,
    'Gun_Rough_NShots_Set': 3,
    'Gun_Rough_PointSeperation_Set': 5,
    'Gun_Rough_Fit_Offset': 10,
    'Gun_Dipole_Start_Set': 7,
    'Gun_Dipole_End_Set': 8.9,
    'Gun_Dipole_Step_Set': 0.1,
    'Gun_Fine_NShots_Set': 10,
    'Gun_Fine_PointSeperation_Set': 2,
    'Gun_Fine_Range_Set': 20,
    'Gun_OffCrest_Phase_Set': 0,
    'Linac1_Amp_Step_Set': 100,
    'Linac1_Amp_Set': 13400,
    'Linac1_Rough_NShots_Set': 3,
    'Linac1_Rough_PointSeperation_Set': 5,
    'Linac1_Rough_Fit_Offset': 0,
    'Linac1_Dipole_Start_Set': 60,
    'Linac1_Dipole_End_Set': 90,
    'Linac1_Dipole_Step_Set': 1,
    'Linac1_Fine_NShots_Set': 10,
    'Linac1_Fine_PointSeperation_Set': 2,
    'Linac1_Fine_Range_Set': 10,
    'Linac1_OffCrest_Phase_Set': 0,
    }

    def debugArgs(self, func, *args, **kwargs):
        debugStr = str(func)+' called'
        if len(args) > 0:
            debugStr += ' args='+str(args)
        if len(kwargs) > 0:
            debugStr += ' kwargs='+str(kwargs)
        getattr(logger, 'debug')(debugStr)

    @debugLog
    def save_config(self):
        for w in self.defaults:
            self.settings[w] = getattr(self.view, w).value()
        with open('autocrester.yaml', 'w') as stream:
            yaml.dump(self.settings, stream, default_flow_style=False)

    @debugLog
    def load_config(self):
        try:
            with open('autocrester.yaml', 'r') as stream:
                self.settings = yaml.load(stream)
            self.apply_config()
        except:
            self.apply_defaults()

    def apply_config(self):
        for w in self.settings:
            getattr(self.view, w).setValue(self.settings[w])
            if w in self.model.settings:
                self.model.settings[w] = self.settings[w]

    def apply_defaults(self):
        for w in self.defaults:
            getattr(self.view, w).setValue(self.defaults[w])

    @debugLog
    def __init__(self, view, model, L01timing=None):
        super(Controller, self).__init__()
        '''define model and view'''
        self.view = view
        self.model = model
        self.Linac01Timing = L01timing
        self.load_config()
        self.model.logger = self.loggerSignal
        self.model.newData = self.newDataSignal
        self.model.progress = self.progressSignal
        model.debugLog = debugLog
        self.machineSignaller = machineSignaller(self.model.baseMachine)
        self.machineReciever = machineReciever(self.model.baseMachine)
        self.model.machine = self.machineSignaller
        self.machineSignaller.toMachine.connect(self.machineReciever.toMachine)
        self.machineReciever.fromMachine.connect(self.machineSignaller.fromMachine)
        self.loggerSignal[str].connect(self.setLabel)
        self.loggerSignal[str, str].connect(self.setLabel)
        self.plots = {}

        '''Plots'''
        pg.setConfigOption('background', 'w')
        # Gun
        self.plots['Gun'] = plotWidgets('Gun', approximateText='Charge', approximateUnits='pC')
        self.view.Gun_Plots_Layout.addWidget(self.plots['Gun'])
        # LINAC1
        self.plots['Linac1'] = plotWidgets('Linac1', approximateText='BPM X Position', approximateUnits='mm')
        self.view.Linac1_Plots_Layout.addWidget(self.plots['Linac1'])

        self.view.actionExit.triggered.connect(qt.qApp.quit)
        self.view.actionReload_Defaults.triggered.connect(self.load_config)
        self.view.actionSave_Defaults.triggered.connect(self.save_config)
        self.view.actionApply_Default_Settings.triggered.connect(self.apply_defaults)

        self.log = lw.loggerWidget(autosave=True, logdirectory='\\\\claraserv3\\claranet\\apps\\legacy\\logs\\autoCrester\\', appname='AutoCrester')
        self.log.setFilterLevel('Info')
        # sys.stdout = lw.redirectLogger(self.log, 'stdout')
        # sys.stderr = lw.redirectLogger(self.log, 'stderr')

        self.view.logTabLayout.addWidget(self.log)
        self.log.addLogger(logger)

        self.buttons = [self.view.setupMagnetsButton, self.view.Gun_LoadBURT_Button,
        self.view.Gun_Rough_Button, self.view.Gun_Fine_Button, self.view.Gun_SetPhase_Button, self.view.Gun_Dipole_Button,
        self.view.Linac1_Rough_Button, self.view.Linac1_Fine_Button, self.view.Linac1_SetPhase_Button, self.view.Linac1_Dipole_Button,
        self.view.Linac1_LoadBURT_Button, self.view.Linac1_Fine_Screen_Button, self.view.Gun_Fine_Screen_Button,
        self.view.Linac1_TurnOn_Button, self.view.Gun_TurnOn_Button, self.view.Gun_Fine_Update_Start_Button, self.view.Linac1_Fine_Update_Start_Button,
        self.view.Gun_LinacTiming_Off_Button, self.view.Linac1_LinacTiming_On_Button, self.view.Linac1_LinacTiming_Off_Button, self.view.L01_PID_Checkbox,
        self.view.Gun_EnergySet_Button, self.view.Linac1_EnergySet_Button
        ]

        # self.view.setupMagnetsButton.clicked.connect(self.model.magnetDegausser)
        self.view.Gun_TurnOn_Button.clicked.connect(self.gunRamp)
        self.view.Gun_LoadBURT_Button.clicked.connect(self.loadGunBURT)
        self.view.Gun_Rough_Button.clicked.connect(self.gunWCMCrester)
        self.view.Gun_Dipole_Button.clicked.connect(self.setDipoleCurrentForGun)
        self.view.Gun_Fine_Button.clicked.connect(self.gunBPMCrester)
        self.view.Gun_Fine_Screen_Button.clicked.connect(self.gunScreenCrester)
        self.view.Gun_SetPhase_Button.clicked.connect(self.setGunPhaseOffset)
        self.view.Gun_Momentum_Set.valueChanged[float].connect(self.updateGunDipoleSet)
        self.view.Gun_Dipole_Set.valueChanged[float].connect(self.updateGunMomentumSet)
        self.view.Gun_Fine_Update_Start_Button.clicked.connect(self.updateStartingGunPhaseCurrent)
        self.view.Gun_LinacTiming_Off_Button.clicked.connect(self.setLinacTimingOff)
        self.view.Gun_EnergySet_Button.clicked.connect(self.setGunMomentum)
        self.view.Linac1_TurnOn_Button.clicked.connect(self.linac1Ramp)
        self.view.Linac1_LoadBURT_Button.clicked.connect(self.loadLinac1BURT)
        self.view.Linac1_Rough_Button.clicked.connect(self.linac1CresterQuick)
        self.view.Linac1_Dipole_Button.clicked.connect(self.setDipoleCurrentForLinac1)
        self.view.Linac1_Fine_Button.clicked.connect(self.linac1BPMCrester)
        self.view.Linac1_Fine_Screen_Button.clicked.connect(self.linac1ScreenCrester)
        self.view.Linac1_SetPhase_Button.clicked.connect(self.setLinac1PhaseOffset)
        self.view.Linac1_Momentum_Set.valueChanged[float].connect(self.updateLinac1DipoleSet)
        self.view.Linac1_Dipole_Set.valueChanged[float].connect(self.updateLinac1MomentumSet)
        self.view.Linac1_Fine_Update_Start_Button.clicked.connect(self.updateStartingLinac1PhaseCurrent)
        self.view.Linac1_LinacTiming_On_Button.clicked.connect(self.setLinac1TimingOn)
        self.view.Linac1_LinacTiming_Off_Button.clicked.connect(self.setLinac1TimingOff)
        self.view.Linac1_EnergySet_Button.clicked.connect(self.setLinac1Momentum)

        self.view.Linac1_Timing_Monitor.clicked.connect(self.toggleLinac1Timing)

        self.view.topbutton_widget.hide()
        self.view.Abort_Button.hide()
        self.view.Abort_Button.clicked.connect(self.abortRunning)
        self.view.Finish_Button.hide()
        self.view.Finish_Button.clicked.connect(self.finishRunning)
        self.view.Save_Data_Buttons.hide()
        self.view.Save_Data_Buttons.button(qt.QDialogButtonBox.Cancel).setStyleSheet('background-color: red')
        self.view.Save_Data_Buttons.button(qt.QDialogButtonBox.Save).setStyleSheet('background-color: green')
        self.view.Save_Data_Buttons.accepted.connect(self.autoSaveData)
        self.view.Save_Data_Buttons.rejected.connect(self.cancelSave)
        self.view.actionSave_Calibation_Data.triggered.connect(self.saveData)

        self.setLabel('Mode: '+self.model.machineType+' '+self.model.lineType+' with '+self.model.gunType+' gun')

        self.progressSignal.connect(self.updateProgress)

        self.monitors = {}
        self.monitors['gun_phase'] = updatingTimer(self.view.Gun_Phase_Monitor, 'widget', 100, self.model.machine.getGunPhase)
        self.monitors['gun_phase'].start()
        self.monitors['gun_amp'] = updatingTimer(self.view.Gun_Amp_Monitor, 'widget', 100, self.model.machine.getGunAmplitude)
        self.monitors['gun_amp'].start()
        self.monitors['gun_dipole'] = updatingTimer(self.view.Dipole_Monitor, 'widget', 100, self.model.machine.getDip)
        self.monitors['gun_dipole'].start()
        self.monitors['linac1_phase'] = updatingTimer(self.view.Linac1_Phase_Monitor, 'widget', 100, self.model.machine.getLinac1Phase)
        self.monitors['linac1_phase'].start()
        self.monitors['linac1_amp'] = updatingTimer(self.view.Linac1_Amp_Monitor, 'widget', 100, self.model.machine.getLinac1Amplitude)
        self.monitors['linac1_amp'].start()

        if not self.model.machineType == 'None':
            # self.Linac01Timing = linacTiming.Linac01Timing()
            self.monitors['linac1_timing'] = updatingTimer(self.Linac1_Timing_Monitor, 'function', 250, self.Linac01Timing.isLinacOn)
            self.monitors['linac1_timing'].start()

        self.enableSaveTimer = qt.QTimer()
        self.enableSaveTimer.setSingleShot(True)
        self.enableSaveTimer.timeout.connect(self.enableButtons)

    def closeEvent(self, event):
        for t in self.monitors:
            t.quit()

    @debugLog
    def setGunPhaseOffset(self, *args):
        self.model.gunPhaser(gunPhaseSet=self.view.Gun_OffCrest_Phase_Set.value(), offset=True)
        self.cavity = 'Gun'
        time.sleep(0.5)
        pm = '' if self.view.Gun_OffCrest_Phase_Set.value() < 0 else '+'
        self.loggerSignal.emit('Set '+pm+str(self.view.Gun_OffCrest_Phase_Set.value())+'deg to '+self.cavity+' = '+str(self.model.machine.getPhase(self.cavity)), 'info')

    @debugLog
    def setLinac1PhaseOffset(self, *args):
        self.model.linac1Phaser(linac1PhaseSet=self.view.Linac1_OffCrest_Phase_Set.value(), offset=True)
        self.cavity = 'Linac1'
        time.sleep(0.5)
        pm = '' if self.view.Linac1_OffCrest_Phase_Set.value() < 0 else '+'
        self.loggerSignal.emit('Set '+pm+str(self.view.Linac1_OffCrest_Phase_Set.value())+'deg to '+self.cavity+' = '+str(self.model.machine.getPhase(self.cavity)), 'info')

    @debugLog
    def loadBURT(self, function, button):
        self.disableButtons()
        self.thread = GenericThread(getattr(self.model,function))
        self.thread.finished.connect(self.enableButtons)
        self.thread.started.connect(lambda: getattr(self.view,button).setStyleSheet("background-color: yellow"))
        self.thread.result.connect(lambda x: self.loadedBurt(button, x))
        self.thread.start()

    @debugLog
    def loadedBurt(self, button, success):
        if success:
            self.loggerSignal.emit('Successfully applied DBURT!', 'info')
            getattr(self.view,button).setStyleSheet("background-color: green")
        else:
            self.setLabel('FAILED to apply DBURT!','warning')
            getattr(self.view,button).setStyleSheet("background-color: red")
        qt.QTimer.singleShot(60*1000, lambda: getattr(self.view,button).setStyleSheet("background-color: None"))

    @debugLog
    def loadGunBURT(self, *args, **kwargs):
        self.setLabel('loadGunBURT called','debug')
        self.loadBURT('loadGunBURT','Gun_LoadBURT_Button')

    @debugLog
    def loadLinac1BURT(self, *args, **kwargs):
        self.setLabel('loadLinac1BURT called','debug')
        self.loadBURT('loadLinac1BURT', 'Linac1_LoadBURT_Button')

    @debugLog
    def setLinacTimingOff(self, *args, **kwargs):
        self.setLabel('setLinacTimingOff called','debug')
        self.setLinac1TimingOff()

    @debugLog
    def setLinac1TimingOn(self, *args, **kwargs):
        if not self.model.machineType == 'None':
            self.Linac01Timing.resetTiming()

    @debugLog
    def setLinac1TimingOff(self, *args, **kwargs):
        if not self.model.machineType == 'None':
            self.Linac01Timing.offsetTiming(100)

    @debugLog
    def toggleLinac1Timing(self, *args, **kwargs):
        if self.Linac01Timing.isLinacOn:
            self.setLinac1TimingOff()
        else:
            self.setLinac1TimingOn()

    def Linac1_Timing_Monitor(self, state):
        if state:
            self.view.Gun_LinacTiming_Off_Button.setStyleSheet("background-color: red")
            self.view.Linac1_LinacTiming_On_Button.setStyleSheet("background-color: green")
            self.view.Linac1_LinacTiming_Off_Button.setStyleSheet("background-color: red")
            self.view.Linac1_Timing_Monitor.setStyleSheet("background-color: green")
        else:
            self.view.Gun_LinacTiming_Off_Button.setStyleSheet("background-color: green")
            self.view.Linac1_LinacTiming_On_Button.setStyleSheet("background-color: red")
            self.view.Linac1_LinacTiming_Off_Button.setStyleSheet("background-color: green")
            self.view.Linac1_Timing_Monitor.setStyleSheet("background-color: red")

    @debugLog
    def updateGunDipoleSet(self, mom):
        try:
            self.view.Gun_Dipole_Set.valueChanged[float].disconnect(self.updateGunMomentumSet)
        except:
            pass
        self.view.Gun_Dipole_Set.setValue(self.model.calculateDipoleFromMomentum(mom))
        self.view.Gun_Dipole_Set.valueChanged[float].connect(self.updateGunMomentumSet)

    @debugLog
    def updateGunMomentumSet(self, I):
        try:
            self.view.Gun_Momentum_Set.valueChanged[float].disconnect(self.updateGunDipoleSet)
        except:
            pass
        self.view.Gun_Momentum_Set.setValue(self.model.calculateMomentumFromDipole(I))
        self.view.Gun_Momentum_Set.valueChanged[float].connect(self.updateGunDipoleSet)

    @debugLog
    def updateLinac1DipoleSet(self, mom):
        try:
            self.view.Linac1_Dipole_Set.valueChanged[float].disconnect(self.updateLinac1MomentumSet)
        except:
            pass
        self.view.Linac1_Dipole_Set.setValue(self.model.calculateDipoleFromMomentum(mom))
        self.view.Linac1_Dipole_Set.valueChanged[float].connect(self.updateLinac1MomentumSet)

    @debugLog
    def updateLinac1MomentumSet(self, I):
        try:
            self.view.Linac1_Momentum_Set.valueChanged[float].disconnect(self.updateLinac1DipoleSet)
        except:
            pass
        self.view.Linac1_Momentum_Set.setValue(self.model.calculateMomentumFromDipole(I))
        self.view.Linac1_Momentum_Set.valueChanged[float].connect(self.updateLinac1DipoleSet)

    def setButtonState(self, state=True):
        for b in self.buttons:
            b.setEnabled(state)

    def enableButtons(self):
        self.setButtonState(True)
        self.view.Finish_Button.hide()
        self.view.Abort_Button.hide()
        self.view.Save_Data_Buttons.hide()
        self.view.topbutton_widget.hide()
        self.view.Progress_Monitor.setValue(0)
        self.enableSaveTimer.stop()

    def disableButtons(self):
        self.setButtonState(False)
        self.view.Finish_Button.show()
        self.view.Abort_Button.show()
        self.view.topbutton_widget.show()

    def enableSaveButtons(self):
        self.view.Finish_Button.hide()
        self.view.Abort_Button.hide()
        self.view.Save_Data_Buttons.show()
        self.view.topbutton_widget.show()
        self.enableSaveTimer.start(60*1000) #timer in msec
        # print self.enableSaveTimer.isActive()
        # print self.enableSaveTimer

    @debugLog
    def abortRunning(self, *args, **kwargs):
        self.model.abort()

    @debugLog
    def finishRunning(self, *args, **kwargs):
        self.model.finish()

    def updatePlot(self):
        # print('Plot Update Called! - ', self.model.cavity, self.model.actuator)
        self.plots[self.cavity].newData(self.cavity, self.model.actuator, self.model.crestingData[self.model.cavity][self.model.actuator])

    @debugLog
    def gunRamp(self, *args):
        self.disableButtons()
        self.cavity = 'Gun'
        self.actuator = 'approx'
        self.thread = GenericThread(self.model.turnOnGun, self.view.Gun_Amp_Set.value(), self.view.Gun_Amp_Step_Set.value())
        self.thread.finished.connect(self.enableButtons)
        self.thread.start()

    @debugLog
    def linac1Ramp(self, *args):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.actuator = 'approx'
        self.thread = GenericThread(self.model.turnOnLinac1, self.view.Linac1_Amp_Set.value(), self.view.Linac1_Amp_Step_Set.value())
        self.thread.finished.connect(self.enableButtons)
        self.thread.start()

    @debugLog
    def gunWCMCrester(self, *args):
        self.disableButtons()
        self.cavity = 'Gun'
        self.actuator = 'approx'
        self.thread = GenericThread(self.model.gunWCMCrester, self.view.Gun_Rough_PointSeperation_Set.value(), self.view.Gun_Rough_NShots_Set.value(), self.view.Gun_Rough_Fit_Offset.value())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        self.thread.finished.connect(self.updateStartingGunPhaseCalibration)
        self.thread.start()

    @debugLog
    def linac1CresterQuick(self, *args):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.actuator = 'approx'
        self.thread = GenericThread(self.model.linacCresterQuick, 1, self.view.Linac1_Rough_PointSeperation_Set.value(), self.view.Linac1_Rough_NShots_Set.value(), self.view.Linac1_Rough_Fit_Offset.value(), PID=self.view.L01_PID_Checkbox.isChecked())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        self.thread.finished.connect(self.updateStartingLinac1PhaseCalibration)
        self.thread.start()

    @debugLog
    def gunBPMCrester(self, *args):
        self.disableButtons()
        self.cavity = 'Gun'
        self.actuator = 'fine'
        self.thread = GenericThread(self.model.gunCresterFine, self.view.Gun_Fine_Range_Start.value(), self.view.Gun_Fine_Range_Set.value(), self.view.Gun_Fine_PointSeperation_Set.value(), self.view.Gun_Fine_NShots_Set.value())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        self.thread.finished.connect(self.updateStartingLinac1PhaseCalibration)
        self.thread.start()

    @debugLog
    def linac1BPMCrester(self, *args):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.actuator = 'fine'
        self.thread = GenericThread(self.model.linacCresterFine, 1, self.view.Linac1_Fine_Range_Start.value(),
                                    self.view.Linac1_Fine_Range_Set.value(), self.view.Linac1_Fine_PointSeperation_Set.value(),
                                    self.view.Linac1_Fine_NShots_Set.value(), PID=self.view.L01_PID_Checkbox.isChecked())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        self.thread.finished.connect(self.updateStartingLinac1PhaseCalibration)
        self.thread.start()

    @debugLog
    def gunScreenCrester(self, *args):
        self.disableButtons()
        self.cavity = 'Gun'
        self.actuator = 'screen'
        self.thread = GenericThread(self.model.gunCresterFineScreen, self.view.Gun_Fine_Range_Start.value(), self.view.Gun_Fine_Range_Set.value(), self.view.Gun_Fine_PointSeperation_Set.value(), self.view.Gun_Fine_NShots_Set.value())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        self.thread.finished.connect(self.updateStartingLinac1PhaseCalibration)
        self.thread.start()

    @debugLog
    def linac1ScreenCrester(self, *args):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.actuator = 'screen'
        self.thread = GenericThread(self.model.linacCresterFineScreen, 1, self.view.Linac1_Fine_Range_Start.value(), self.view.Linac1_Fine_Range_Set.value(), self.view.Linac1_Fine_PointSeperation_Set.value(), self.view.Linac1_Fine_NShots_Set.value())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        self.thread.finished.connect(self.updateStartingLinac1PhaseCalibration)
        self.thread.start()

    @debugLog
    def setDipoleCurrentForGun(self, *args):
        self.disableButtons()
        self.cavity = 'Gun'
        self.actuator = 'dipole'
        self.thread = GenericThread(self.model.gunDipoleSet, self.view.Gun_Dipole_Start_Set.value(), self.view.Gun_Dipole_End_Set.value(), self.view.Gun_Dipole_Step_Set.value())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        self.thread.finished.connect(lambda : self.view.Gun_Dipole_Set.setValue(self.model.finalDipoleI))
        self.thread.start()

    @debugLog
    def setDipoleCurrentForLinac1(self, *args):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.actuator = 'dipole'
        self.thread = GenericThread(self.model.linacDipoleSet, 1, self.view.Linac1_Dipole_Start_Set.value(), self.view.Linac1_Dipole_End_Set.value(), self.view.Linac1_Dipole_Step_Set.value())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        # self.thread.finished.connect(self.autoSaveData)
        self.thread.finished.connect(lambda : self.view.Linac1_Dipole_Set.setValue(self.model.finalDipoleI))
        self.thread.start()

    @debugLog
    def setGunMomentum(self, *args):
        self.disableButtons()
        self.cavity = 'Gun'
        self.actuator = 'momentum'
        self.thread = GenericThread(self.model.gunMomentumSet, self.view.Gun_Dipole_Set.value())
        # self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        # self.thread.finished.connect(self.autoSaveData)
        self.thread.start()

    @debugLog
    def setLinac1Momentum(self, *args):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.actuator = 'momentum'
        self.thread = GenericThread(self.model.linacMomentumSet, 1, self.view.Linac1_Dipole_Set.value())
        # self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        # self.thread.finished.connect(self.autoSaveData)
        self.thread.start()

    @debugLog
    def updateStartingGunPhaseCalibration(self, *args, **kwargs):
        self.view.Gun_Fine_Range_Start.setValue(self.model.crestingData['Gun']['calibrationPhase'])

    @debugLog
    def updateStartingGunPhaseCurrent(self, *args, **kwargs):
        self.view.Gun_Fine_Range_Start.setValue(self.model.machine.getGunPhase())

    @debugLog
    def updateStartingLinac1PhaseCalibration(self):
        if 'calibrationPhase' in self.model.crestingData['Linac1']:
            self.view.Linac1_Fine_Range_Start.setValue(self.model.crestingData['Linac1']['calibrationPhase'])

    @debugLog
    def updateStartingLinac1PhaseCurrent(self, *args, **kwargs):
        self.view.Linac1_Fine_Range_Start.setValue(self.model.machine.getLinac1Phase())

    def updateProgress(self, progress):
        self.view.Progress_Monitor.setValue(progress)

    def setLabel(self, string, severity='info'):
        getattr(logger, str(severity))(string)
        if not str(severity).lower() == 'debug':
            self.view.label_MODE.setText('Status: <font color="red">' + string + '</font>')

    @debugLog
    def cancelSave(self):
        if self.model.machineType is not None:
            if self.actuator == 'dipole':
                if hasattr(self.model, 'startingDipole'):
                    self.model.machine.setDip(self.model.startingDipole)
            else:
                if hasattr(self.model, 'approxcrest'):
                    self.model.machine.setPhase(self.cavity, self.model.approxcrest)
        self.enableButtons()

    @debugLog
    def autoSaveData(self):
        self.model.applyFinalPhase(self.cavity)
        self.saveData(cavity=[self.cavity], type=[self.actuator])

    @debugLog
    def saveData(self, cavity=None, type=None):
        self.enableButtons()
        self.model.saveData(cavity=cavity, type=type, savetoworkfolder=self.view.actionSave_to_Work_Folder.isChecked())
