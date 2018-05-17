from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
import random as r

degree = physics.pi/180.0


class Model(QObject):

	bpmX = pyqtSignal(float)
	wcmQ = pyqtSignal(float)

	def __init__(self, app, view, machineType, lineType, gunType, mag, scope, bpm, gunllrf, linac1llrf):
		QThread.__init__(self)
		self.app = app
		self.view = view
		self.magnets = mag
		self.scope = scope
		self.bpm = bpm
		self.gunllrf = gunllrf
		self.linac1llrf = linac1llrf
		self.machineType = machineType
		self.lineType = lineType
		self.gunType = gunType
		self.view.label_MODE.setText('MODE: '+self.machineType+' '+self.lineType+' with '+self.gunType+' Hz gun')
		self.approxPhaseData=[]
		self.approxChargeData=[]
		self.approxPhaseFit=[]
		self.approxChargeFit=[]
		self.finePhaseFit=[]
		self.fineBPMFit=[]
		self.finePhaseData=[]
		self.fineBPMData=[]
		self.parameters={}
		self.calibrationPhase = {'Gun': None, 'Linac1': None}
		self.buttons = [self.view.setupMagnetsButton, self.view.crestGunWCMButton, self.view.crestGunBPM, self.view.setGunPhaseButton,
						self.view.crestLinacButton, self.view.setLinacPhaseButton, self.view.crestLinacRoughButton]
		self.run()
		print("Model Initialized")
	#DESTRUCTOR

	def start(self):
		self.run()

	def run(self):
		if self.lineType=='VELA':
			self.velaMethod()
		elif self.lineType=='CLARA':
			self.claraMethod()

	def claraMethod(self):
		print('clara Method')
		self.parameters['magnets']=[]
		self.parameters['bpm'] = 'C2V-BPM01'
		self.parameters['scope'] = 'WCM'

	def velaMethod(self):
		print('vela Method')
		self.parameters['magnets']=['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06',
							'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05',
							'SOL', 'BSOL', 'DIP01']
		self.parameters['bpm'] = 'C2V-BPM01'
		self.parameters['scope'] = 'SCOP01'

	def magnetDegausser(self):
			print('1. Setting up Magnets')
			self.setUpMagnets(self.parameters['magnets'])

	def gunWCMCrester(self):
		print('2. Approximately Finding Crest')
		self.disableButtons()
		self.crester = findingGunCrestWCM(self, self.parameters['scope'])
		self.crester.setPhase.connect(self.setPhase)
		self.wcmQ.connect(self.crester.updateWCMCharge)

		self.timer = QTimer()
		self.timer.timeout.connect(lambda : self.getWCMCharge(self.parameters['scope']))
		self.timer.start(100)

		self.thread = QThread()  # no parent!
		self.crester.moveToThread(self.thread)
		self.thread.started.connect(self.crester.findingCrest)
		self.disableButtons()
		self.crester.finished.connect(self.printFinished)
		self.crester.finished.connect(self.timer.stop)
		self.crester.finished.connect(self.enableButtons)
		self.crester.finishedSuccesfully.connect(lambda : self.gunPhaser(offset=False))
		self.crester.finished.connect(self.thread.quit)

		self.thread.start()

	def linacCresterQuick(self):
		print('x. Approximately Finding Crest')
		self.disableButtons()
		self.crester = findingLinacCrestQuick(self)
		self.crester.setPhase.connect(self.setPhase)
		self.bpmX.connect(self.crester.updateBPMPosition)

		self.timer = QTimer()
		self.timer.timeout.connect(lambda : self.getBPMPosition(self.parameters['bpm']))
		self.timer.start(100)

		self.thread = QThread()  # no parent!
		self.crester.moveToThread(self.thread)
		self.thread.started.connect(self.crester.findingCrest)
		self.disableButtons()
		self.crester.finished.connect(self.printFinished)
		self.crester.finished.connect(self.timer.stop)
		self.crester.finished.connect(self.enableButtons)
		self.crester.finishedSuccesfully.connect(lambda : self.linac1Phaser(offset=False))
		self.crester.finished.connect(self.thread.quit)

		self.thread.start()

	def gunBPMCrester(self):
		print('3. Finding Crest of Gun')
		self.disableButtons()
		self.crester = findingGunCrest(self, self.parameters['magnets'], self.parameters['bpm'], \
			int(self.view.rangeSet.text()), int(self.view.nScanningSet.text()), int(self.view.nShotsSet.text()))
		self.crester.setPhase.connect(self.setPhase)
		self.bpmX.connect(self.crester.updateBPMPosition)

		self.timer = QTimer()
		self.timer.timeout.connect(lambda : self.getBPMPosition(self.parameters['bpm']))
		self.timer.start(100)

		self.thread = QThread()  # no parent!
		self.crester.moveToThread(self.thread)
		self.thread.started.connect(self.crester.findingCrest)
		self.disableButtons()

		self.crester.finished.connect(self.printFinished)
		self.crester.finished.connect(self.timer.stop)
		self.crester.finishedSuccesfully.connect(lambda : self.gunPhaser(offset=False))
		self.crester.finished.connect(self.enableButtons)
		self.crester.finished.connect(self.thread.quit)

		self.thread.start()

	def linacBPMCrester(self):
		print('5. Finding Crest of Linac')
		self.disableButtons()
		self.crester = findingLinacCrest(self, self.parameters['magnets'], self.parameters['bpm'], \
			int(self.view.rangeSet.text()), int(self.view.nScanningSet.text()), int(self.view.nShotsSet.text()))
		self.crester.setPhase.connect(self.setPhase)
		self.bpmX.connect(self.crester.updateBPMPosition)

		self.timer = QTimer()
		self.timer.timeout.connect(lambda : self.getBPMPosition(self.parameters['bpm']))
		self.timer.start(100)

		self.thread = QThread()  # no parent!
		self.crester.moveToThread(self.thread)
		self.thread.started.connect(self.crester.findingCrest)
		self.disableButtons()

		self.crester.finished.connect(self.printFinished)
		self.crester.finished.connect(self.timer.stop)
		self.crester.finishedSuccesfully.connect(lambda : self.linac1Phaser(offset=False))
		self.crester.finished.connect(self.enableButtons)
		self.crester.finished.connect(self.thread.quit)

		self.thread.start()

	def printFinished(self):
		print "Thread Finished!"

	def setButtonState(self, state=True):
		for b in self.buttons:
			b.setEnabled(state)

	def enableButtons(self):
		self.setButtonState(True)
		self.view.abortButton.clicked.disconnect(self.abortRunning)
		self.view.abortButton.hide()

	def disableButtons(self):
		self.setButtonState(False)
		self.view.abortButton.clicked.connect(self.abortRunning)
		self.view.abortButton.show()

	def gunPhaser(self, offset=True):
		if isinstance(self.calibrationPhase['Gun'],(float, int)) and isinstance(int(self.view.gunPhaseSet.text()), (float, int)):
			if offset == True:
				# print('Setting Gun Phase to ', str(self.calibrationPhase['Gun'] + int(self.view.gunPhaseSet.text())), ' (',self.view.gunPhaseSet.text()),')'
				self.setGunPhase(self.calibrationPhase['Gun'] + int(self.view.gunPhaseSet.text()))
			else:
				# print('Setting Gun Phase to ', str(self.calibrationPhase['Gun']))
				self.setGunPhase(self.calibrationPhase['Gun'])

	def linac1Phaser(self, offset=True):
		if isinstance(self.calibrationPhase['Linac1'],(float, int)) and isinstance(int(self.view.linac1PhaseSet.text()), (float, int)):
			if offset == True:
				# print('Setting Linac 1 Phase to ', str(self.calibrationPhase['Linac1'] + int(self.view.linac1PhaseSet.text())), ' (', self.view.linac1PhaseSet.text()),')'
				self.setLinac1Phase(self.calibrationPhase['Linac1'] + int(self.view.linac1PhaseSet.text()))
			else:
				# print('Setting Linac 1 Phase to ', str(self.calibrationPhase['Linac1']))
				self.setLinac1Phase(self.calibrationPhase['Linac1'])

	def setUpMagnets(self,magnets):
		deguassingList=[]
		print('Deguassing magnets...')
		for magnet in magnets:
			if self.view.checkBox_deguassQ.isChecked() and self.magnets.isAQuad(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassC.isChecked() and self.magnets.isACor(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassS.isChecked() and self.magnets.isASol(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassD.isChecked() and self.magnets.isADip(magnet):
				deguassingList.append(magnet)
			#else:
			#	print('Magnet '+magnet+' is off or not selected to be deguassed.')
		print('Magnet to be Deguassed: '+str(deguassingList))
		self.activeMags = mag.std_vector_string()
		self.activeMags.extend(deguassingList)
		self.magnets.degauss(self.activeMags,True)

		print('Switching off magnets...')
		switchOfFList=[]
		for magnet in magnets:
			if self.view.checkBox_quadOff.isChecked() and self.magnets.isAQuad(magnet):
				switchOfFList.append(magnet)
			elif self.view.checkBox_corrOff.isChecked() and self.magnets.isACor(magnet):
				switchOfFList.append(magnet)
			#else:
				#print('No magnets to be switched off.')
		print('Magnet to be Switched Off: '+str(switchOfFList))
		self.turnOffMags = mag.std_vector_string()
		self.turnOffMags.extend(switchOfFList)
		self.magnets.switchOFFpsu(self.turnOffMags)

		print('Setting Dipole for predicted momentum...')
		for magnet in magnets:
			if self.magnets.isADip(magnet):
				dipole=magnet
		D = self.magnets.getMagObjConstRef(dipole)
		coeffs = list(D.fieldIntegralCoefficients)
		mom = float(self.view.lineEdit_2.text())
		coeffs[-1] -= (1000000000*(mom*physics.pi*45)/(physics.c*180))
		roots = np.roots(coeffs)
		current = roots[-1].real
		while(self.magnets.isDegaussing(dipole)):
			print('Waiting for '+dipole+' to degauss...')
			time.sleep(10)
		self.magnets.setSI(dipole,-current)

	def abortRunning(self):
		if hasattr(self,'thread'):
			self.crester.stop()
			self.thread.quit()

	def setPhase(self, cavity, value):
		if cavity == 'Gun':
			self.setGunPhase(value)
		elif cavity == 'Linac1':
			self.setLinac1Phase(value)

	def getPhase(self, cavity):
		if cavity == 'Gun':
			return self.getGunPhase()
		elif cavity == 'Linac1':
			return self.getLinac1Phase()

	def setGunPhase(self, phase):
		# print 'setting Gun phase = ', phase
		self.gunllrf.setPhiSP(phase)

	def getGunPhase(self):
		return self.gunllrf.getPhiSP()

	def setLinac1Phase(self, phase):
		# print 'setting L01 phase = ', phase
		self.linac1llrf.setPhiSP(phase)

	def getLinac1Phase(self):
		return self.linac1llrf.getPhiSP()

	def getBPMPosition(self, bpm):
		self.bpmX.emit(self.bpm.getXFromPV(bpm))

	def getWCMCharge(self, scope):
		self.wcmQ.emit(self.scope.getCharge(scope))

	def saveData(self):
		data = np.array(zip(self.finePhaseData, self.fineBPMData))
		np.savetxt('fineCrestingData.txt', data, delimiter=',')
		data = np.array(zip(self.approxPhaseData, self.approxPhaseFit))
		np.savetxt('approxCrestingData.txt', data, delimiter=',')

class crestingObject(QObject):

	finished = pyqtSignal()
	finishedSuccesfully = pyqtSignal()
	setPhase = pyqtSignal(str, float)
	data = []
	_isRunning = True

	def stop(self):
		print 'stopping worker!'
		self._isRunning = False

class findingGunCrestWCM(crestingObject):

	cavity = 'Gun'

	def __init__(self, parent, scope):
		super(findingGunCrestWCM, self).__init__()
		self.parent = parent
		self.scope = scope

	def updateWCMCharge(self, value):
		self.data.append(value)

	def findingCrest(self):
		self.parent.approxPhaseFit=[]
		self.parent.approxChargeFit=[]
		self.parent.approxPhaseData=[]
		self.parent.approxChargeData=[]

		for phase in np.arange(-180,180,20):
			self.setPhase.emit(self.cavity, phase)
			while len(self.data) < 3:
				time.sleep(0.1)
			self.data = []
			while len(self.data) < 3:
				time.sleep(0.1)
			data = np.mean(self.data)
			print 'charge = ', data
			self.parent.approxChargeData.append(data)
			self.parent.approxPhaseData.append(phase)
			if not self._isRunning:
				break
		if self._isRunning:

			def func(list, a, b, c):
				x = np.array(list)
				return a*x**2 + b*x + c

			allData = zip(self.parent.approxPhaseData, self.parent.approxChargeData)
			cutData = [a for a in allData if a[1] > 10]
			phase, charge = zip(*cutData)
			print phase

			popt, pcov = curve_fit(func, *zip(*cutData), p0=None)
			self.parent.approxPhaseFit = np.array(phase)
			self.parent.approxChargeFit = func(self.parent.approxPhaseFit, *popt)

			self.parent.calibrationPhase[self.cavity] = -popt[1]/(2*popt[0]) + 15 # Assume Max Charge is -15deg from crest
			print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
			self.finishedSuccesfully.emit()
		self.finished.emit()

class findingGunCrest(crestingObject):

	cavity = 'Gun'

	def __init__(self, parent,  magnets, bpm, phiRange, phiSteps, bpmSamples):
		super(findingGunCrest, self).__init__()
		self.parent = parent
		self.magnets = magnets
		self.bpm = bpm
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.bpmSamples = bpmSamples

	def updateBPMPosition(self, value):
		self.data.append(value)

	def findingCrest(self):
		self.parent.finePhaseFit=[]
		self.parent.fineBPMFit=[]
		self.parent.finePhaseData=[]
		self.parent.fineBPMData=[]
		if self.parent.calibrationPhase[self.cavity] is None:
			self.approxcrest = self.parent.getPhase(self.cavity)
		else:
			self.approxcrest = self.parent.calibrationPhase[self.cavity]
		for phase in np.linspace(self.approxcrest-self.phiRange, self.approxcrest+self.phiRange, self.phiSteps):
			self.setPhase.emit(self.cavity, phase)
			time.sleep(0.1)
			currphase = self.parent.getPhase(self.cavity)
			while len(self.data) < 3:
				time.sleep(0.1)
			self.data = []
			while len(self.data) < self.bpmSamples:
				time.sleep(0.1)
			data = np.mean(self.data)
			if np.std(self.data) > 0.0005:
				self.parent.fineBPMData.append(data)
				self.parent.finePhaseData.append(currphase)
			if not self._isRunning:
				break

		if self._isRunning:
			self.fitting()
		else:
			self.finished.emit()

	def fitting(self):

		def fitting_equation(x, a, b, crest):
			return a + b * np.cos((crest - (x + 180)) * degree)

		popt, pcov = curve_fit(fitting_equation, self.parent.finePhaseData, self.parent.fineBPMData, p0=[0,10,self.approxcrest])
		# print 'popt = ', popt[2]
			# p0=[max(self.parent.fineBPMData), max(self.parent.fineBPMData)-min(self.parent.fineBPMData), self.approxcrest])
		self.parent.finePhaseFit = np.array(self.parent.finePhaseData)
		self.parent.fineBPMFit = fitting_equation(self.parent.finePhaseFit, *popt)

		self.parent.calibrationPhase[self.cavity] = ((180 + popt[2]) % 360) - 180
		print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
		self.finishedSuccesfully.emit()
		# except:
		# 	pass
		self.finished.emit()

class findingLinacCrestQuick(crestingObject):

	cavity = 'Linac1'

	def __init__(self, parent):
		super(findingLinacCrestQuick, self).__init__()
		self.parent = parent

	def updateBPMPosition(self, value):
		self.data.append(value)

	def findingCrest(self):
		self.parent.approxPhaseFit=[]
		self.parent.approxChargeFit=[]
		self.parent.approxPhaseData=[]
		self.parent.approxChargeData=[]

		for phase in np.arange(-180,180,5):
			self.setPhase.emit(self.cavity, phase)
			time.sleep(0.1)
			self.data = []
			while len(self.data) < 3:
				time.sleep(0.1)
			data = np.mean(self.data) if np.std(self.data) > 0.005 else 20
			self.parent.approxChargeData.append(data)
			self.parent.approxPhaseData.append(phase)
			if not self._isRunning:
				break

		if self._isRunning:

			def func(list, a, b, c):
				x = np.array(list)
				return a*x**2 + b*x + c

			allData = zip(self.parent.approxPhaseData, self.parent.approxChargeData)
			cutData = [a for a in allData if a[1] < 20]
			phase, charge = zip(*cutData)
			print charge

			popt, pcov = curve_fit(func, *zip(*cutData), p0=None)
			self.parent.approxPhaseFit = np.array(phase)
			self.parent.approxChargeFit = func(self.parent.approxPhaseFit, *popt)

			self.parent.calibrationPhase[self.cavity] = -popt[1]/(2*popt[0])
			print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
			self.finishedSuccesfully.emit()
		self.finished.emit()

class findingLinacCrest(findingGunCrest):

	cavity = 'Linac1'
	setPhase = pyqtSignal(str, float)

class setUpGun(QObject):

	def setUpGun(self, desiredPhase, bpm):
		self.gun.setPhiSP(desiredPhase+self.calibrationPhase)
		x = 1000*self.bpm.getXFromPV(bpm)
		currentAmp = self.gun.getAmpSP()
		step = 50 #(MV/m)
		time.sleep(1)
		print x
		while abs(x)>0.01:
			currentAmp = self.gun.getAmpSP()
			print 'currentAmp = ', currentAmp
			self.gun.setAmpSP(currentAmp+step)
			print 'setting  = ', currentAmp+step
			time.sleep(0.1)
			self.app.processEvents()
			x_old = x
			x = 1000*self.bpm.getXFromPV(bpm)
			print bpm,' = ', x
			if x < 0:
				step = -abs(step)
			elif x > 0:
				step = abs(step)
			if abs(x - x_old) > abs(x):
				step = 0.5*step
