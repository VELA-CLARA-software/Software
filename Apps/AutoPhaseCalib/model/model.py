from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import random as r
import csv
from  functools import partial

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
		self.view.label_MODE.setText('MODE: '+self.machineType+' '+self.lineType+' with '+self.gunType+' gun')
		self.crestingData = {}
		for cavity in ['Gun', 'Linac1']:
			self.crestingData[cavity]={'approxPhaseData': [], 'approxChargeData': [], 'approxPhaseFit': [], 'approxChargeFit': [], 'finePhaseFit': [],
										'fineBPMFit': [], 'finePhaseData': [], 'fineBPMData': [], 'approxChargeStd': [], 'fineBPMStd': []}
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
		self.parameters['dispersive_bpm'] = 'C2V-BPM01'
		self.parameters['linac_rough_bpm'] = 'S02-BPM01'
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

	def startWCMTimer(self, crester):
		self.wcmQ.connect(crester.updateWCMCharge)
		self.timer = QTimer()
		self.timer.timeout.connect(lambda : self.getWCMCharge(self.parameters['scope']))
		self.timer.start(100)

	def startBPMTimer(self, crester, bpm):
		self.bpmX.connect(crester.updateBPMPosition)
		self.timer = QTimer()
		self.timer.timeout.connect(lambda : self.getBPMPosition(bpm))
		self.timer.start(100)

	class crestingMethod(QObject):
		def __init__(self, parent, timer, phaser, crestingfunction, *args, **kwargs):
			parent.disableButtons()
			self.crester = crestingfunction(parent, *args, **kwargs)
			self.crester.setPhase.connect(parent.setPhase)

			timer(self.crester)

			self.thread = QThread()  # no parent!
			self.crester.moveToThread(self.thread)
			self.thread.started.connect(self.crester.findingCrest)

			self.crester.finished.connect(parent.printFinished)
			self.crester.finished.connect(parent.timer.stop)
			self.crester.finished.connect(parent.enableButtons)
			self.crester.finishedSuccesfully.connect(lambda : phaser(offset=False))
			self.crester.finished.connect(self.thread.quit)

			self.thread.start()

	def gunWCMCrester(self):
		print('2. Approximately Finding Crest')
		self.cresterObject = self.crestingMethod(self, self.startWCMTimer, self.gunPhaser, findingGunCrestWCM)

	def linacCresterQuick(self):
		print('4. Approximately Finding Crest')
		timer = partial(self.startBPMTimer, bpm=self.parameters['linac_rough_bpm'])
		self.cresterObject = self.crestingMethod(self, timer, self.linac1Phaser, findingLinacCrestQuick)

	def gunBPMCrester(self):
		print('3. Finding Crest of Gun')
		timer = partial(self.startBPMTimer, bpm=self.parameters['dispersive_bpm'])
		self.cresterObject = self.crestingMethod(self, timer, self.gunPhaser, findingGunCrest, self.parameters['magnets'], self.parameters['dispersive_bpm'], \
			int(self.view.rangeSetGun.text()), int(self.view.nScanningSetGun.text()), int(self.view.nShotsSetGun.text()))

	def linacBPMCrester(self):
		print('5. Finding Crest of Linac')
		timer = partial(self.startBPMTimer, bpm=self.parameters['dispersive_bpm'])
		self.cresterObject = self.crestingMethod(self, timer, self.linac1Phaser, findingLinacCrest, self.parameters['magnets'], self.parameters['dispersive_bpm'], \
			int(self.view.rangeSetLinac1.text()), int(self.view.nScanningSetLinac1.text()), int(self.view.nShotsSetLinac1.text()))

	def printFinished(self):
		print "Thread Finished!"

	def setButtonState(self, state=True):
		for b in self.buttons:
			b.setEnabled(state)

	def enableButtons(self):
		self.setButtonState(True)
		self.view.finishButton.clicked.disconnect(self.finishRunning)
		self.view.finishButton.hide()
		self.view.abortButton.clicked.disconnect(self.abortRunning)
		self.view.abortButton.hide()

	def disableButtons(self):
		self.setButtonState(False)
		self.view.finishButton.clicked.connect(self.finishRunning)
		self.view.finishButton.show()
		self.view.abortButton.clicked.connect(self.abortRunning)
		self.view.abortButton.show()

	def gunPhaser(self, offset=True):
		if isinstance(self.calibrationPhase['Gun'],(float, int)) and isinstance(int(self.view.gunPhaseSet.text()), (float, int)):
			set_phase = self.calibrationPhase['Gun'] + (float(self.view.gunPhaseSet.text()) if offset else 0)
			# print('Setting Gun Phase to ', set_phase)
			self.setGunPhase(set_phase)

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
		print('Degaussing magnets...')
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
		print('Magnet to be Degaussed: '+str(deguassingList))
		# self.activeMags = mag.std_vector_string()
		# self.activeMags.extend(deguassingList)
		self.magnets.degauss(deguassingList,True)

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
			self.cresterObject.crester.stop()
			self.cresterObject.thread.quit()

	def finishRunning(self):
		if hasattr(self,'thread'):
			self.cresterObject.crester.stop()

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
		for cavity in ['Gun', 'Linac1']:
			my_dict = self.crestingData[cavity]
			with open(cavity+'_CrestingData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
			    w = csv.DictWriter(f, my_dict.keys())
			    w.writeheader()
			    w.writerow(my_dict)

class crestingObject(QObject):

	finished = pyqtSignal()
	finishedSuccesfully = pyqtSignal()
	setPhase = pyqtSignal(str, float)
	data = []
	_isRunning = True
	_finish = False

	def stop(self):
		print 'stopping worker!'
		self._isRunning = False

	def finish(self):
		print 'finishing worker!'
		self._finish = True

class crestingObjectQuick(crestingObject):

	stepSize = 5

	def __init__(self, parent):
		super(crestingObjectQuick, self).__init__()
		self.parent = parent
		self.resetDataArray()
		self.offset = 0

	def resetDataArray(self):
		self.parent.crestingData[self.cavity]['approxPhaseFit'] = []
		self.parent.crestingData[self.cavity]['approxChargeFit'] = []
		self.parent.crestingData[self.cavity]['approxPhaseData'] = []
		self.parent.crestingData[self.cavity]['approxChargeData'] = []
		self.parent.crestingData[self.cavity]['approxChargeStd'] = []

	def findingCrest(self):
		for phase in np.arange(-180,180,self.stepSize):
			self.setPhase.emit(self.cavity, phase)
			data, stddata = self.getData()
			self.setData(phase, data, stddata)
			if not self._isRunning or self._finish:
				break
		if self._isRunning:
			self.doFit()
			self.finished.emit()

	def setData(self, phase, data, stddata):
		self.parent.crestingData[self.cavity]['approxChargeData'].append(data)
		self.parent.crestingData[self.cavity]['approxPhaseData'].append(phase)
		self.parent.crestingData[self.cavity]['approxChargeStd'].append(stddata)

	def setFitData(self, phase, data):
		self.parent.crestingData[self.cavity]['approxPhaseFit'] = phase
		self.parent.crestingData[self.cavity]['approxChargeFit'] = data

	def setFinalPhase(self, phase):
		self.parent.calibrationPhase[self.cavity] = phase + self.offset

	def fitness_function(self, list, a, b, c, d, e, f):
		x = np.array(list)
		return f*x**5 + e*x**4 + d*x**3 + a*x**2 + b*x + c

	def doFit(self):
		try:
			cutData = self.cutData()
			xData, yData = zip(*cutData)
			popt, pcov = curve_fit(self.fitness_function, xData, yData, p0=None)
			self.setFitData(np.array(xData), self.fitness_function(np.array(xData), *popt))
			# print(popt)
			# Find the peak, assuming the fit function is a polynomial
			# We have to take the derivative, so e*x**4 -> 4*e*x**3 etc.
			crest_phase = np.real(np.roots(np.multiply(range(len(popt) - 1, 0, -1), popt[:-1]))[0])
			print 'Crest phase is ', crest_phase

			# self.setFinalPhase(-popt[1]/(2*popt[0])) # Assume Max Charge is -15deg from crest
			self.setFinalPhase(crest_phase)
			print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
			self.finishedSuccesfully.emit()
		except Exception as e:
			print(e)
			print 'Error in fitting!'

class findingGunCrestWCM(crestingObjectQuick):

	cavity = 'Gun'
	offset = 0

	def __init__(self, parent):
		super(findingGunCrestWCM, self).__init__(parent)

	def updateWCMCharge(self, value):
		self.data.append(value)

	def getData(self):
		while len(self.data) < 3:
			time.sleep(0.1)
		self.data = []
		while len(self.data) < 3:
			if not self._isRunning:
				break
			time.sleep(0.1)
		return [np.mean(self.data), np.std(self.data)]

	def cutData(self):
		"""Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
		max_charge = max(self.parent.crestingData[self.cavity]['approxChargeData'])
		allData = zip(self.parent.crestingData[self.cavity]['approxPhaseData'], self.parent.crestingData[self.cavity]['approxChargeData'], self.parent.crestingData[self.cavity]['approxChargeStd'])
		cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 2]
		return cutData

	def doFit(self):
		try:
			cutData = self.cutData()
			x, y, std = zip(*cutData)
			# f = UnivariateSpline(x, y, w=std, k=5)

			# xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
			# ynew = f(xnew)

			self.setFitData(np.array(x), np.array(y))

			crest_phase = (x[-1] + x[0]) / 2.0

			print 'Crest phase is ', crest_phase

			self.setFinalPhase(crest_phase)
			print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
			self.finishedSuccesfully.emit()
		except Exception as e:
			print(e)
			print 'Error in fitting!'

class findingLinacCrestQuick(crestingObjectQuick):

	cavity = 'Linac1'
	offset = 0
	stepSize = 5

	def updateBPMPosition(self, value):
		self.data.append(value)

	def getData(self):
		self.data = []
		while len(self.data) < 3:
			time.sleep(0.1)
			if not self._isRunning:
				break
		return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [20,0]

	def cutData(self):
		allData = zip(self.parent.crestingData[self.cavity]['approxPhaseData'], self.parent.crestingData[self.cavity]['approxChargeData'], self.parent.crestingData[self.cavity]['approxChargeStd'])
		cutData = [a for a in allData if a[1] == 20]
		return cutData

	def doFit(self):
		try:
			cutData = self.cutData()
			x, y, std = zip(*cutData)
			#crest_phase = np.mean(x)-180
			crest_phase = ((x[-1] + x[0]) / 2.0)-180

			print 'Crest phase is ', crest_phase

			self.setFinalPhase(crest_phase)
			print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
			self.finishedSuccesfully.emit()
		except Exception as e:
			print(e)
			print 'Error in fitting!'

class crestingObjectFine(crestingObject):
	def __init__(self, parent, magnets, bpm, phiRange, phiSteps, bpmSamples):
		super(crestingObjectFine, self).__init__()
		self.parent = parent
		self.magnets = magnets
		self.bpm = bpm
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.bpmSamples = bpmSamples
		self.resetDataArray()

	def resetDataArray(self):
		self.parent.crestingData[self.cavity]['finePhaseFit'] = []
		self.parent.crestingData[self.cavity]['fineBPMFit'] = []
		self.parent.crestingData[self.cavity]['finePhaseData'] = []
		self.parent.crestingData[self.cavity]['fineBPMData'] = []
		self.parent.crestingData[self.cavity]['fineBPMStd'] = []

	def updateBPMPosition(self, value):
		self.data.append(value)

	def findingCrest(self):
		if self.parent.calibrationPhase[self.cavity] is None:
			self.approxcrest = self.parent.getPhase(self.cavity)
		else:
			self.approxcrest = self.parent.calibrationPhase[self.cavity]
		self.approxcrest = self.parent.getPhase(self.cavity)
		self.minPhase = self.approxcrest-self.phiRange
		self.maxPhase = self.approxcrest+self.phiRange
		for phase in np.linspace(self.minPhase, self.maxPhase, self.phiSteps):
			self.setPhase.emit(self.cavity, phase)
			time.sleep(0.1)
			currphase = self.parent.getPhase(self.cavity)
			self.data = []
			while len(self.data) < 3:
				time.sleep(0.1)
			self.data = []
			while len(self.data) < self.bpmSamples:
				time.sleep(0.1)
				if not self._isRunning:
					break
			data = np.mean(self.data)
			if np.std(self.data) > 0.0005:
				self.parent.crestingData[self.cavity]['fineBPMData'].append(data)
				self.parent.crestingData[self.cavity]['fineBPMStd'].append(np.std(self.data))
				self.parent.crestingData[self.cavity]['finePhaseData'].append(currphase)
			if not self._isRunning or self._finish:
				break

		if self._isRunning:
			self.fitting()
		else:
			self.finished.emit()

	def fitting_equation(self, x, a, b, crest):
		return a + b * (np.sin((crest - (x + 180)) * degree)**2)

	def calculateCrest(self, popt):
		return ((180 + popt[2]) % 360) - 180

	def fitting(self):

		popt, pcov = curve_fit(self.fitting_equation, self.parent.crestingData[self.cavity]['finePhaseData'], self.parent.crestingData[self.cavity]['fineBPMData'], \
			sigma=self.parent.crestingData[self.cavity]['fineBPMStd'],	p0=[0,10,self.approxcrest])

		self.parent.crestingData[self.cavity]['finePhaseFit'] = np.array(self.parent.crestingData[self.cavity]['finePhaseData'])
		self.parent.crestingData[self.cavity]['fineBPMFit'] = self.fitting_equation(self.parent.crestingData[self.cavity]['finePhaseFit'], *popt)

		self.parent.calibrationPhase[self.cavity] = ((180 + popt[2]) % 360) - 180
		print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
		self.finishedSuccesfully.emit()
		self.finished.emit()

class findingGunCrest(crestingObjectFine):

	cavity = 'Gun'

	def fitting(self):
		x = self.parent.crestingData[self.cavity]['finePhaseData']
		y = self.parent.crestingData[self.cavity]['fineBPMData']
		f = UnivariateSpline(x, y, w=self.parent.crestingData[self.cavity]['fineBPMStd'], k=5)

		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
		ynew = f(xnew)

		crest = xnew[np.argmin(ynew)]

		self.parent.crestingData[self.cavity]['finePhaseFit'] = xnew
		self.parent.crestingData[self.cavity]['fineBPMFit'] = ynew

		self.parent.calibrationPhase[self.cavity] = crest
		print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
		self.finishedSuccesfully.emit()
		self.finished.emit()

class findingLinacCrest(crestingObjectFine):

	cavity = 'Linac1'

	def fitting(self):
		x = self.parent.crestingData[self.cavity]['finePhaseData']
		y = self.parent.crestingData[self.cavity]['fineBPMData']
		f = UnivariateSpline(x, y, w=self.parent.crestingData[self.cavity]['fineBPMStd'], k=5)

		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
		ynew = f(xnew)

		crest = xnew[np.argmin(ynew)]

		self.parent.crestingData[self.cavity]['finePhaseFit'] = xnew
		self.parent.crestingData[self.cavity]['fineBPMFit'] = ynew

		self.parent.calibrationPhase[self.cavity] = crest
		print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
		self.finishedSuccesfully.emit()
		self.finished.emit()

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
