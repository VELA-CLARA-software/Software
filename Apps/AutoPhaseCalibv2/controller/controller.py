from PyQt4.QtCore import *
from PyQt4.QtGui import *
# import PyQt4.QApplication
import sys,os
import time
import numpy as np
import pyqtgraph as pg
from  functools import partial
sys.path.append("../../../")
from Software.Utils.dict_to_h5 import *
from Software.Procedures.Machine.signaller import machineReciever, machineSignaller
import Software.Widgets.loggerWidget.loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

class GenericThread(QThread):
	def __init__(self, function, *args, **kwargs):
		QThread.__init__(self)
		self.function = function
		self.args = args
		self.kwargs = kwargs

	def run(self):
		self.object = self.function(*self.args, **self.kwargs)
		print 'finished!'

class plotWidgets(pg.GraphicsView):

	actuators = ['approx', 'dipole', 'fine']

	def __init__(self, cavity, approximateText='Charge', approximateUnits='pC'):
		super(plotWidgets, self).__init__()
		self.cavity = cavity
		self.layout = pg.GraphicsLayout(border=(100,100,100))
		self.setCentralItem(self.layout)
		self.mainPlot = {}
		self.subPlots = {}
		self.mainPlot['approx'] = self.layout.addPlot(title="Approximate Callibration")
		self.mainPlot['approx'].showGrid(x=True, y=True)
		self.mainPlot['approx'].setLabel('left', approximateText, approximateUnits)
		self.mainPlot['approx'].setLabel('bottom', text='Phase', units='Degrees')
		self.subPlots['approx'] = {}
		self.layout.nextRow()
		self.mainPlot['dipole'] = self.layout.addPlot(title="Dipole Current Set")
		self.mainPlot['dipole'].showGrid(x=True, y=True)
		self.mainPlot['dipole'].setLabel('left', text='X BPM Position', units='mm')
		self.mainPlot['dipole'].setLabel('bottom', text='Dipole Current', units='Amps')
		self.subPlots['dipole'] = {}
		self.layout.nextRow()
		self.mainPlot['fine'] = self.layout.addPlot(title="Callibration")
		self.mainPlot['fine'].showGrid(x=True, y=True)
		self.mainPlot['fine'].setLabel('left', text='X BPM Position', units='mm')
		self.mainPlot['fine'].setLabel('bottom', text='Phase', units='Degrees')
		self.subPlots['fine'] = {}

		for a in self.actuators:
			self.subPlots[a]['data'] = self.mainPlot[a].plot(symbolPen = 'b', symbol='o', width=0, symbolSize=1, pen=None)
			self.subPlots[a]['fit'] = self.mainPlot[a].plot(pen = 'r', width=50)
			self.subPlots[a]['std'] = pg.ErrorBarItem(x=np.array([]), y=np.array([]), height=np.array([]), beam=None, pen={'color':'b', 'width':2})
			self.mainPlot[a].addItem(self.subPlots[a]['std'])

	def newData(self, cavity, actuator, data):
		actuator = str(actuator)
		try:
			if str(cavity) == self.cavity:
				if 'xData' in data and 'yData' in data and 'yStd' in data:
					self.subPlots[actuator]['data'].setData(x=data['xData'], y=data['yData'])
					self.subPlots[actuator]['std'].setData(x=data['xData'], y=data['yData'], height=np.array(data['yStd']))
				if 'xFit' in data and 'yFit' in data:
					self.subPlots[actuator]['fit'].setData(x=data['xFit'], y=data['yFit'])
		except:
			pass

class updatingTimer(QThread):
	def __init__(self, name, function, *args, **kwargs):
		super(updatingTimer, self).__init__()
		self.name = name
		self.function = function
		self.args = args
		self.kwargs = kwargs

	def run(self):
		self.timer = QTimer()
		self.timer.moveToThread(self)
		self.timer.timeout.connect(self.update_monitor)
		self.timer.start(250)
		self.exec_()

	def printer(self):
		print 'here!'

	def update_monitor(self):
		val = self.function(*self.args, **self.kwargs)
		self.name.setValue(val)

class Controller(QObject):

	newDataSignal = pyqtSignal()
	loggerSignal = pyqtSignal(str)
	progressSignal = pyqtSignal(int)

	def __init__(self, view, model):
		super(Controller, self).__init__()
		'''define model and view'''
		self.view = view
		self.model = model
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
		pg.setConfigOption('background', 'w')
		# Gun
		self.plots['Gun'] = plotWidgets('Gun', approximateText='Charge', approximateUnits='pC')
		self.view.Gun_Plots_Layout.addWidget(self.plots['Gun'])
		# LINAC1
		self.plots['Linac1'] = plotWidgets('Linac1', approximateText='BPM X Position', approximateUnits='mm')
		self.view.Linac1_Plots_Layout.addWidget(self.plots['Linac1'])

		self.view.actionExit.triggered.connect(qApp.quit)

		self.log = lw.loggerWidget()
		self.view.logTabLayout.addWidget(self.log)
		self.log.addLogger(logger)

		self.buttons = [self.view.setupMagnetsButton,
		self.view.Gun_Rough_Button, self.view.Gun_Dipole_Button,self.view.Gun_Fine_Button, self.view.Gun_SetPhase_Button,
		self.view.Linac1_Rough_Button, self.view.Linac1_Dipole_Button, self.view.Linac1_Fine_Button, self.view.Linac1_SetPhase_Button,
		# self.view.Gun_TurnOn_Button, self.view.Linac1_TurnOn_Button,
		]

		# self.view.setupMagnetsButton.clicked.connect(self.model.magnetDegausser)
		# self.view.Gun_TurnOn_Button.clicked.connect(self.model.turnOnGun)
		self.view.Gun_LoadBURT_Button.clicked.connect(self.loadGunBURT)
		self.view.Gun_Rough_Button.clicked.connect(self.gunWCMCrester)
		self.view.Gun_Dipole_Button.clicked.connect(self.setDipoleCurrentForGun)
		self.view.Gun_Fine_Button.clicked.connect(self.gunBPMCrester)
		self.view.Gun_SetPhase_Button.clicked.connect(lambda : self.model.gunPhaser(gunPhaseSet=self.view.Gun_OffCrest_Phase_Set.value(), offset=True))
		self.view.Gun_Momentum_Set.valueChanged[float].connect(self.updateGunDipoleSet)
		self.view.Gun_Dipole_Set.valueChanged[float].connect(self.updateGunMomentumSet)
		self.view.Gun_Fine_Update_Start_Button.clicked.connect(self.updateStartingGunPhaseCurrent)
		# self.view.Linac1_TurnOn_Button.clicked.connect(self.model.turnOnLinac)
		self.view.Linac1_LoadBURT_Button.clicked.connect(self.loadLinac1BURT)
		self.view.Linac1_Rough_Button.clicked.connect(self.linac1CresterQuick)
		self.view.Linac1_Dipole_Button.clicked.connect(self.setDipoleCurrentForLinac1)
		self.view.Linac1_Fine_Button.clicked.connect(self.linac1BPMCrester)
		self.view.Linac1_SetPhase_Button.clicked.connect(lambda : self.model.linac1Phaser(linac1PhaseSet=self.view.Linac1_OffCrest_Phase_Set.value(), offset=True))
		self.view.Linac1_Momentum_Set.valueChanged[float].connect(self.updateLinac1DipoleSet)
		self.view.Linac1_Dipole_Set.valueChanged[float].connect(self.updateLinac1MomentumSet)
		self.view.Linac1_Fine_Update_Start_Button.clicked.connect(self.updateStartingLinac1PhaseCurrent)

		self.view.Abort_Button.hide()
		self.view.Abort_Button.clicked.connect(self.abortRunning)
		self.view.Finish_Button.hide()
		self.view.Finish_Button.clicked.connect(self.finishRunning)

		self.view.actionSave_Calibation_Data.triggered.connect(self.saveData)

		self.setLabel('MODE: '+self.model.machineType+' '+self.model.lineType+' with '+self.model.gunType+' gun')

		self.progressSignal.connect(self.updateStartingGunPhaseCurrent)

		self.monitors = {}
		self.monitors['gun_phase'] = updatingTimer(self.view.Gun_Phase_Monitor, self.model.machine.getGunPhase)
		self.monitors['gun_phase'].start()
		self.monitors['gun_dipole'] = updatingTimer(self.view.Dipole_Monitor, self.model.machine.getDip)
		self.monitors['gun_dipole'].start()
		self.monitors['linac1_phase'] = updatingTimer(self.view.Linac1_Phase_Monitor, self.model.machine.getLinac1Phase)
		self.monitors['linac1_phase'].start()

	def closeEvent(self, event):
		for t in self.monitors:
			t.quit()

	def loadBURT(self, function, button):
		success = getattr(self.model,function)()
		if success:
			getattr(self.view,button).setStyleSheet("background-color: green")
		else:
			getattr(self.view,button).setStyleSheet("background-color: red")
		QTimer.singleShot(1000, lambda: getattr(self.view,button).setStyleSheet("background-color: None"))

	def loadGunBURT(self):
		self.loadBURT('loadGunBURT','Gun_LoadBURT_Button')

	def loadLinac1BURT(self):
		self.loadBURT('loadLinac1BURT', 'Linac1_LoadBURT_Button')

	def updateGunDipoleSet(self, mom):
		self.view.Gun_Dipole_Set.valueChanged[float].disconnect(self.updateGunMomentumSet)
		self.view.Gun_Dipole_Set.setValue(self.model.calculateDipoleFromMomentum(mom))
		self.view.Gun_Dipole_Set.valueChanged[float].connect(self.updateGunMomentumSet)

	def updateGunMomentumSet(self, I):
		self.view.Gun_Momentum_Set.valueChanged[float].disconnect(self.updateGunDipoleSet)
		self.view.Gun_Momentum_Set.setValue(self.model.calculateMomentumFromDipole(I))
		self.view.Gun_Momentum_Set.valueChanged[float].connect(self.updateGunDipoleSet)

	def updateLinac1DipoleSet(self, mom):
		self.view.Linac1_Dipole_Set.valueChanged[float].disconnect(self.updateLinac1MomentumSet)
		self.view.Linac1_Dipole_Set.setValue(self.model.calculateDipoleFromMomentum(mom))
		self.view.Linac1_Dipole_Set.valueChanged[float].connect(self.updateLinac1MomentumSet)

	def updateLinac1MomentumSet(self, I):
		self.view.Linac1_Momentum_Set.valueChanged[float].disconnect(self.updateLinac1DipoleSet)
		self.view.Linac1_Momentum_Set.setValue(self.model.calculateMomentumFromDipole(I))
		self.view.Linac1_Momentum_Set.valueChanged[float].connect(self.updateLinac1DipoleSet)

	def setButtonState(self, state=True):
		for b in self.buttons:
			b.setEnabled(state)

	def enableButtons(self):
		self.setButtonState(True)
		self.view.Finish_Button.clicked.disconnect(self.finishRunning)
		self.view.Finish_Button.hide()
		self.view.Abort_Button.clicked.disconnect(self.abortRunning)
		self.view.Abort_Button.hide()

	def disableButtons(self):
		self.setButtonState(False)
		self.view.Finish_Button.clicked.connect(self.finishRunning)
		self.view.Finish_Button.show()
		self.view.Abort_Button.clicked.connect(self.abortRunning)
		self.view.Abort_Button.show()

	def abortRunning(self):
		self.model.abort()

	def finishRunning(self):
		self.model.finish()

	def updatePlot(self):
		self.plots[self.cavity].newData(self.model.cavity, self.model.actuator, self.model.crestingData[self.model.cavity][self.model.actuator])

	def gunWCMCrester(self):
		self.disableButtons()
		self.cavity = 'Gun'
		self.actuator = 'approx'
		self.thread = GenericThread(self.model.gunWCMCrester, self.view.Gun_Rough_PointSeperation_Set.value(), self.view.Gun_Rough_NShots_Set.value())
		self.newDataSignal.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.finished.connect(self.updateStartingGunPhaseCalibration)
		self.thread.finished.connect(self.autoSaveData)
		self.thread.start()

	def linac1CresterQuick(self):
		self.disableButtons()
		self.cavity = 'Linac1'
		self.actuator = 'approx'
		self.thread = GenericThread(self.model.linacCresterQuick, 1, self.view.Linac1_Rough_PointSeperation_Set.value(), self.view.Linac1_Rough_NShots_Set.value())
		self.newDataSignal.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.finished.connect(self.updateStartingLinac1updateStartingLinac1PhaseCalibration)
		self.thread.finished.connect(self.autoSaveData)
		self.thread.start()

	def gunBPMCrester(self):
		self.disableButtons()
		self.cavity = 'Gun'
		self.actuator = 'fine'
		self.thread = GenericThread(self.model.gunCresterFine, self.view.Gun_Fine_Range_Start.value(), self.view.Gun_Fine_Range_Set.value(), self.view.Gun_Fine_PointSeperation_Set.value(), self.view.Gun_Fine_NShots_Set.value())
		self.newDataSignal.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.finished.connect(self.autoSaveData)
		self.thread.start()

	def linac1BPMCrester(self):
		self.disableButtons()
		self.cavity = 'Linac1'
		self.actuator = 'fine'
		self.thread = GenericThread(self.model.linacCresterFine, 1, self.view.Linac1_Fine_Range_Set.value(), self.view.Linac1_Fine_PointSeperation_Set.value(), self.view.Linac1_Fine_NShots_Set.value())
		self.newDataSignal.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.finished.connect(self.autoSaveData)
		self.thread.start()

	def setDipoleCurrentForGun(self):
		self.disableButtons()
		self.cavity = 'Gun'
		self.actuator = 'dipole'
		self.thread = GenericThread(self.model.gunDipoleSet, self.view.Gun_Dipole_Start_Set.value(), self.view.Gun_Dipole_End_Set.value())
		self.newDataSignal.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.finished.connect(self.autoSaveData)
		self.thread.finished.connect(lambda : self.view.Gun_Dipole_Set.setValue(self.model.finalDipoleI))
		self.thread.start()

	def setDipoleCurrentForLinac1(self):
		self.disableButtons()
		self.cavity = 'Linac1'
		self.actuator = 'dipole'
		self.thread = GenericThread(self.model.linacDipoleSet, 1, self.view.Linac1_Dipole_Start_Set.value(), self.view.Linac1_Dipole_End_Set.value())
		self.newDataSignal.connect(self.updatePlot)
		self.thread.finished.connect(self.enableButtons)
		self.thread.finished.connect(self.autoSaveData)
		self.thread.finished.connect(lambda : self.view.Linac1_Dipole_Set.setValue(self.model.finalDipoleI))
		self.thread.start()

	def updateStartingGunPhaseCalibration(self):
		self.view.Gun_Fine_Range_Start.setValue(self.model.crestingData['Gun']['calibrationPhase'])

	def updateStartingGunPhaseCurrent(self):
		self.view.Gun_Fine_Range_Start.setValue(self.model.machine.getGunPhase())

	def updateStartingLinac1PhaseCalibration(self):
		self.view.Linac1_Fine_Range_Start.setValue(self.model.crestingData['Linac1']['calibrationPhase'])

	def updateStartingLinac1PhaseCurrent(self):
		self.view.Linac1_Fine_Range_Start.setValue(self.model.machine.getLinac1Phase())


	def updateProgress(self, progress):
		self.view.Progress_Monitor.setValue(progress)

	def setLabel(self, string):
		logger.info(string)
		self.view.label_MODE.setText('Status: <font color="red">' + string + '</font>')

	def autoSaveData(self):
		if self.view.actionAuto_Save_Data.isChecked():
			self.saveData(cavity=[self.cavity], type=[self.actuator])

	def saveData(self, cavity=None, type=None):
		if cavity is not None and not isinstance(cavity, (tuple, list)):
			cavity = [cavity]
		elif cavity is None:
			cavity = ['Gun', 'Linac1']
		if type is not None and not isinstance(type, (tuple, list)):
			type = [type]
		elif type is None:
			type = ['approx', 'fine', 'dipole']
		timestr = time.strftime("%H%M%S")
		dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\' if self.view.actionSave_to_Work_Folder.isChecked() else '.'
		try:
			os.makedirs(dir)
		except OSError:
			if not os.path.isdir(dir):
				self.loggerSignal.emit('Error creating directory - saving to local directory')
				dir = '.'
		for c in cavity:
			if c in self.model.crestingData:
				for t in type:
					if t in self.model.crestingData[c]:
						mydata = {a: np.array(self.model.crestingData[c][t][a]) for a in ['xData', 'yData', 'yStd']}
						filename = dir+timestr+'_'+c+'_'+t+'_crestingData.h5'
						save_dict_to_hdf5(mydata, filename)
