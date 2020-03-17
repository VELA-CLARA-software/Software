# -*- coding: utf-8 -*-
import sys
import os
import fnmatch
import time
import ruamel.yaml
sys.path.append("../../../")
from Software.Apps.CTRApp.controller.plots import *
from Software.Utils.dict_to_h5 import *
from  functools import partial
import Software.Procedures.qt as qt
from Software.Procedures.Machine.signaller import machineReciever, machineSignaller
import Software.Widgets.loggerWidget.loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

class GenericThread(qt.QThread):

    result = qt.pyqtSignal(object)

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

    newDataSignal = qt.pyqtSignal(str, str)
    # loggerSignal = qt.pyqtSignal(str)
    loggerSignal = qt.pyqtSignal(['QString'], ['QString','QString'])
    progressSignal = qt.pyqtSignal(int)

    defaults = {}

    def save_config(self):
        for w in self.defaults:
            self.settings[w] = getattr(self.view, w).value()
        with open('CTRApp.yaml', 'w') as stream:
            yaml.dump(self.settings, stream, default_flow_style=False)

    def load_config(self):
        try:
            with open('CTRApp.yaml', 'r') as stream:
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
        # CTR
        self.plots['CTR'] = plotWidgets('CTR')
        self.view.CTR_Plots_Layout.addWidget(self.plots['CTR'])
        # DelE
        # self.plots['DelE'] = plotWidgets('DelE', approximateText='BPM X Position', approximateUnits='mm')
        # self.view.DelE_Plots_Layout.addWidget(self.plots['DelE'])

        self.view.actionExit.triggered.connect(qt.qApp.quit)
        self.view.actionReload_Defaults.triggered.connect(self.load_config)
        self.view.actionSave_Defaults.triggered.connect(self.save_config)
        self.view.actionApply_Default_Settings.triggered.connect(self.apply_defaults)

        self.log = lw.loggerWidget(autosave=True, logdirectory='\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\Application_Logs\\CTRApp\\', appname='CTRApp')
        self.log.setFilterLevel('Info')
        # sys.stdout = lw.redirectLogger(self.log, 'stdout')
        # sys.stderr = lw.redirectLogger(self.log, 'stderr')

        self.view.logTabLayout.addWidget(self.log)
        self.log.addLogger(logger)

        self.buttons = [self.view.CTR_Gun_Load_Crest_Button, self.view.CTR_Linac_Load_Crest_Button,
        self.view.CTR_Correct_Momentum_Button, self.view.CTR_Detector_Sensitivity_1, self.view.CTR_Detector_Sensitivity_2, self.view.CTR_Detector_Sensitivity_3,
        self.view.CTR_Detector_Sensitivity_4, self.view.CTR_Detector_Sensitivity_5, self.view.CTR_Do_Scan_Button, self.view.CTR_Save_Button,
        self.view.CTR_Gun_Crest_Set, self.view.CTR_Linac_Crest_Set, self.view.CTR_Auto_Correct_Set, self.view.CTR_C2V_Position_Set, self.view.CTR_Max_Linac_Set,
        self.view.CTR_Phase_Start_Set, self.view.CTR_Phase_End_Set, self.view.CTR_Phase_Step_Set, self.view.CTR_NShots_Set, self.view.CTR_Linac_Step_Set,
        ]

        self.view.CTR_Gun_Load_Crest_Button.clicked.connect(self.CTR_Gun_Load_Crest)
        self.view.CTR_Linac_Load_Crest_Button.clicked.connect(self.CTR_Linac_Load_Crest)
        self.view.CTR_Correct_Momentum_Button.clicked.connect(self.CTR_Correct_Momentum)
        # self.view.CTR_Detector_Sensitivity_1.clicked.connect(self.CTR_Detector_Sensitivity_1)
        # self.view.CTR_Detector_Sensitivity_2.clicked.connect(self.CTR_Detector_Sensitivity_2)
        # self.view.CTR_Detector_Sensitivity_3.clicked.connect(self.CTR_Detector_Sensitivity_3)
        # self.view.CTR_Detector_Sensitivity_4.clicked.connect(self.CTR_Detector_Sensitivity_4)
        # self.view.CTR_Detector_Sensitivity_5.clicked.connect(self.CTR_Detector_Sensitivity_5)
        self.view.CTR_Do_Scan_Button.clicked.connect(self.CTR_Do_Scan)
        self.view.CTR_Save_Button.setEnabled(False)
        self.view.CTR_Save_Button.clicked.connect(lambda: self.saveData(source='CTR'))

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

        self.setLabel('MODE: '+self.model.machineType+' '+self.model.lineType+' with '+self.model.gunType+' gun')

        self.progressSignal.connect(self.updateProgress)

        self.monitors = {}
        self.monitors['gun_phase'] = updatingTimer(self.view.Gun_Phase_Monitor, 'widget', 100, self.model.machine.getGunPhase)
        self.monitors['gun_phase'].start()
        self.monitors['gun_amp'] = updatingTimer(self.view.Gun_Amp_Monitor, 'widget', 100, self.model.machine.getGunAmplitude)
        self.monitors['gun_amp'].start()
        self.monitors['c2v_bpm'] = updatingTimer(self.view.C2V_BPM_Monitor, 'widget', 100, lambda: self.model.machine.getBPMPosition('C2V-BPM01', plane='X', ignoreNonLinear=False))
        self.monitors['c2v_bpm'].start()
        self.monitors['linac1_phase'] = updatingTimer(self.view.Linac1_Phase_Monitor, 'widget', 100, self.model.machine.getLinac1Phase)
        self.monitors['linac1_phase'].start()
        self.monitors['linac1_amp'] = updatingTimer(self.view.Linac1_Amp_Monitor, 'widget', 100, self.model.machine.getLinac1Amplitude)
        self.monitors['linac1_amp'].start()

        self.enableSaveTimer = qt.QTimer()
        self.enableSaveTimer.setSingleShot(True)
        self.enableSaveTimer.timeout.connect(self.enableButtons)

    def closeEvent(self, event):
        for t in self.monitors:
            t.quit()

    def setGunPhaseOffset(self):
        self.model.gunPhaser(gunPhaseSet=self.view.Gun_OffCrest_Phase_Set.value(), offset=True)
        time.sleep(0.5)
        pm = '' if self.view.Gun_OffCrest_Phase_Set.value() < 0 else '+'
        self.loggerSignal.emit('Set '+pm+str(self.view.Gun_OffCrest_Phase_Set.value())+'deg to '+self.cavity+' = '+str(self.model.machine.getPhase(self.cavity)))

    def setLinac1PhaseOffset(self):
        self.model.linac1Phaser(linac1PhaseSet=self.view.Linac1_OffCrest_Phase_Set.value(), offset=True)
        time.sleep(0.5)
        pm = '' if self.view.Linac1_OffCrest_Phase_Set.value() < 0 else '+'
        self.loggerSignal.emit('Set '+pm+str(self.view.Linac1_OffCrest_Phase_Set.value())+'deg to '+self.cavity+' = '+str(self.model.machine.getPhase(self.cavity)))

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

    def abortRunning(self):
        self.model.abort()

    def finishRunning(self):
        self.model.finish()

    def updatePlot(self, source, type):
        source = str(source)
        type = str(type)
        self.plots[source].newData(source, type, self.model.dataArray[source][type])

    def CTR_Gun_Load_Crest(self):
        self.CTR_Load_Crest('Gun')

    def CTR_Linac_Load_Crest(self):
        self.CTR_Load_Crest('Linac1')

    def CTR_Load_Crest(self, type='Gun'):
        savetoworkfolder = self.view.actionSave_to_Work_Folder.isChecked()
        dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\' if savetoworkfolder else '.'
        fine_files = []
        approx_files = []
        for file in os.listdir(dir):
            if fnmatch.fnmatch(file, '*_'+type+'_fine_crestingData.h5'):
                fine_files.append([os.path.getmtime(os.path.join(dir,file)),os.path.join(dir,file)])
            elif fnmatch.fnmatch(file, '*_'+type+'_approx_crestingData.h5'):
                approx_files.append([os.path.getmtime(os.path.join(dir,file)),os.path.join(dir,file)])
        fine_files =  sorted(fine_files, key=lambda l: l[0])
        approx_files = sorted(approx_files, key=lambda l: l[0])
        if len(fine_files) > 0:
            crest_files = fine_files
        elif len(approx_files) > 0:
            self.setLabel('No ' + type + ' fine cresting files found - using approximate', severity='warning')
            crest_files = approx_files
        else:
            self.setLabel('No ' + type + ' fine OR approximate cresting files found - crest not modified', severity='warning')
            crest_files = []
        for c in reversed(crest_files):
            dict = load_dict_from_hdf5(c[1])
            if 'calibrationPhase' in dict:
                self.set_Crest(type, dict['calibrationPhase'])
                break
            self.setLabel('No valid ' + type + ' cresting file found - crest not modified', severity='warning')

    def set_Crest(self, type, crest=0):
        self.setLabel('Setting ' + type + ' crest to ' + str(crest))
        getattr(self.view, 'CTR_'+type+'_Crest_Set').setValue(crest)

    def CTR_Correct_Momentum(self):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.actuator = 'CTR'
        self.thread = GenericThread(self.model.Correct_Momentum, self.view.CTR_C2V_Position_Set.value(), self.view.CTR_Linac_Step_Set.value(), self.view.CTR_Max_Linac_Set.value())
        self.thread.finished.connect(self.enableButtons)
        self.thread.start()

    def CTR_Do_Scan(self):
        self.disableButtons()
        self.cavity = 'Linac1'
        self.actuator = 'CTR'
        self.thread = GenericThread(self.model.CTR_Scan, self.view.CTR_Phase_Start_Set.value(), self.view.CTR_Phase_End_Set.value(),
                                    self.view.CTR_Phase_Step_Set.value(), self.view.CTR_NShots_Set.value(),
                                    self.view.CTR_Gun_Crest_Set.value(), self.view.CTR_Linac_Crest_Set.value(),
                                    self.view.CTR_Auto_Correct_Set.isChecked(), self.view.CTR_C2V_Position_Set.value(), self.view.CTR_Linac_Step_Set.value(),
                                    self.view.CTR_Max_Linac_Set.value())
        self.newDataSignal.connect(self.updatePlot)
        self.thread.finished.connect(self.enableSaveButtons)
        self.thread.finished.connect(self.updateCTRMaxCompressionPhase)
        self.thread.start()

    def updateCTRMaxCompressionPhase(self):
        self.view.CTR_Max_Compression.setValue(self.model.calibrationPhase['CTR'])

    def updateStartingGunPhaseCurrent(self):
        self.view.Gun_Fine_Range_Start.setValue(self.model.machine.getGunPhase())

    def updateStartingLinac1PhaseCalibration(self):
        if 'calibrationPhase' in self.model.crestingData['Linac1']:
            self.view.Linac1_Fine_Range_Start.setValue(self.model.crestingData['Linac1']['calibrationPhase'])

    def updateStartingLinac1PhaseCurrent(self):
        self.view.Linac1_Fine_Range_Start.setValue(self.model.machine.getLinac1Phase())

    def updateProgress(self, progress):
        self.view.Progress_Monitor.setValue(progress)

    def setLabel(self, string, severity='info'):
        getattr(logger, str(severity))(string)
        self.view.label_MODE.setText('<font color="red">' + string + '</font>')

    def cancelSave(self):
        self.model.machine.setPhase(self.cavity, self.model.calibrationPhase[self.actuator])
        self.enableButtons()

    def autoSaveData(self):
        # self.model.applyFinalPhase(self.cavity)
        self.saveData(source=[self.actuator])

    def saveData(self, source=None, type=None):
        self.enableButtons()
        source = self.actuator if source is None else source
        self.model.saveData(source=source, type=type, savetoworkfolder=self.view.actionSave_to_Work_Folder.isChecked())
