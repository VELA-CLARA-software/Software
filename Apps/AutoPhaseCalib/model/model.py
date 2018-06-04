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

class dataArray(QObject):

	newDataSignal = pyqtSignal(str, str, object)

	def __init__(self):
		super(dataArray, self).__init__()
		self.dict = dict()

	def emitSignal(self, cavity, actuator):
		cavity = str(cavity)
		actuator = str(actuator)
		self.newDataSignal.emit(cavity, actuator, self[cavity][actuator])

	def checkDataArray(self, cavity, actuator, type):
		cavity = str(cavity)
		actuator = str(actuator)
		type = str(type)
		if not cavity in self.dict:
			self[cavity] = {}
		if not actuator in self[cavity]:
			self[cavity][actuator] = {}
		if not type in self[cavity][actuator]:
			self[cavity][actuator][type] = []

	def resetData(self, cavity, actuator, type):
		cavity = str(cavity)
		actuator = str(actuator)
		for t in type:
			self.checkDataArray(cavity, actuator, t)
			self[cavity][actuator][t] = []
		self.emitSignal(cavity, actuator)

	def setData(self, cavity, actuator, type, data):
		cavity = str(cavity)
		actuator = str(actuator)
		for t, d in zip(type, data):
			t = str(t)
			self.checkDataArray(cavity, actuator, t)
			self[cavity][actuator][t] = d
		self.emitSignal(cavity, actuator)

	def appendData(self, cavity, actuator, type, data):
		cavity = str(cavity)
		actuator = str(actuator)
		for t, d in zip(type, data):
			t = str(t)
			self.checkDataArray(cavity, actuator, t)
			self[cavity][actuator][t].append(d)
		self.emitSignal(cavity, actuator)

	def __getitem__(self, key):
		return self.dict[str(key)]

	def __setitem__(self, key, value):
		self.dict[str(key)] = value

class Model(QObject):

	bpmX = pyqtSignal(float)
	wcmQ = pyqtSignal(float)

	def __init__(self, machineType, lineType, gunType, mag, scope, bpm, gunllrf, linac1llrf, cameras=None):
		super(Model, self).__init__()
		self.magnets = mag
		self.scope = scope
		self.bpm = bpm
		self.gunllrf = gunllrf
		self.linac1llrf = linac1llrf
		self.cameras = cameras
		self.machineType = machineType
		if self.machineType == 'Virtual':
			self.virtualSetUp()
		self.lineType = lineType
		self.gunType = gunType
		self.crestingData = dataArray()
		self.parameters={}
		self.calibrationPhase = {'Gun': None, 'Linac1': None}
		self.run()
		print("Model Initialized")

	def virtualSetUp(self):
		sys.path.append('C:\\anaconda32\\Work\\OnlineModel')
		import SAMPL.v2_developing.sampl as sampl
		self.magnets.switchONpsu('DIP01')
		self.cameras.setCamera('C2V-CAM-01')
		self.selectedCamera = self.cameras.getSelectedIARef()
		self.magnets.setSI('DIP01',-91.6)
		self.gunllrf.setAmpMVM(100)
		self.gunllrf.setPhiDEG(0)
		self.linac1llrf.setAmpMVM(0)
		self.linac1llrf.setPhiDEG(-9)
		self.SAMPL = sampl.Setup(V_MAG_Ctrl=None,
		                    C_S01_MAG_Ctrl=self.magnets,
		                    C_S02_MAG_Ctrl=self.magnets,
		                    C2V_MAG_Ctrl=self.magnets,
		                    LRRG_RF_Ctrl=None,
		                    HRRG_RF_Ctrl=self.gunllrf,
		                    L01_RF_Ctrl=self.linac1llrf,
		                    messages=True)

		self.SAMPL.startElement = 'CLA-HRG1-GUN-CAV'
		self.SAMPL.stopElement = 'CLA-C2V-DIA-SCR-01-W'
		self.SAMPL.initDistribFile = '4k-250pC.ini'

	def runSAMPLE(self):
		if self.machineType == 'Virtual':
			self.SAMPL.run()

	def run(self):
		if self.lineType=='VELA':
			self.velaMethod()
		elif self.lineType=='CLARA':
			self.claraMethod()

	def claraMethod(self):
		print('clara Method')
		self.parameters['magnets']=['S02-QUAD01', 'S02-QUAD02', 'S02-QUAD03', 'S02-QUAD04',
							'S01-HCOR1', 'S01-VCOR1', 'S01-HCOR2', 'S01-VCOR2',
							'S02-HCOR1', 'S02-VCOR1', 'S02-HCOR2', 'S02-VCOR2',
							'LRG-SOL', 'LRG-BSOL', 'DIP01']
		self.parameters['dispersive_bpm'] = 'C2V-BPM01'
		self.parameters['linac_rough_bpm'] = 'S02-BPM01'
		self.parameters['scope'] = 'WCM'

	def velaMethod(self):
		print('vela Method')
		self.parameters['magnets']=['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06',
							'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05',
							'SOL', 'BSOL', 'DIP01']
		self.parameters['bpm'] = 'C2V-BPM01'
		self.parameters['scope'] = 'WCM'

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

	class crestingMethod(QThread):
		def __init__(self, parent, timer, phaser, crestingclass, crestingfunction, *args, **kwargs):
			QThread.__init__(self)
			self.crester = crestingclass(parent, *args, **kwargs)
			try:
				self.crester.setPhase.connect(parent.setPhase)
			except:
				pass
			self.crester.resetDataSignal.connect(parent.crestingData.resetData)
			self.crester.setDataSignal.connect(parent.crestingData.setData)
			self.crester.appendDataSignal.connect(parent.crestingData.appendData)
			self.crester.runSAMPLESignal.connect(parent.runSAMPLE)

			if timer is not None:
				timer(crester=self.crester)

			# self.thread = QThread()  # no parent!
			self.crester.moveToThread(self)
			self.crestfunc = getattr(self.crester, crestingfunction)
			self.started.connect(self.crestfunc)

			self.crester.finished.connect(parent.printFinished)
			if timer is not None:
				self.crester.finished.connect(parent.timer.stop)

			if phaser is not None:
				self.crester.finishedSuccesfully.connect(lambda : phaser(offset=False))
			self.crester.finished.connect(self.quit)

	def gunWCMCrester(self, gunPhaseSet=0):
		print('2. Approximately Finding Crest')
		self.cresterObject = self.crestingMethod(self, timer=self.startWCMTimer, phaser=self.gunPhaser, crestingclass=findingGunCrestWCM, crestingfunction='findingCrest')
		return self.cresterObject

	def linac1CresterQuick(self, linac1PhaseSet=0):
		print('4. Approximately Finding Crest')
		timer = partial(self.startBPMTimer, bpm=self.parameters['linac_rough_bpm'])
		self.cresterObject = self.crestingMethod(self, timer, self.linac1Phaser, findingLinac1CrestQuick, 'findingCrest')
		return self.cresterObject

	def gunBPMCrester(self, range, npoints, nsamples, gunPhaseSet=0):
		print('3. Finding Crest of Gun')
		timer = partial(self.startBPMTimer, bpm=self.parameters['dispersive_bpm'])
		self.cresterObject = self.crestingMethod(self, timer, self.gunPhaser, findingGunCrest, 'findingCrest', \
			self.parameters['magnets'], self.parameters['dispersive_bpm'], \
			range, npoints, nsamples)
		return self.cresterObject

	def linac1BPMCrester(self, range, npoints, nsamples, linac1PhaseSet=0):
		print('5. Finding Crest of Linac')
		timer = partial(self.startBPMTimer, bpm=self.parameters['dispersive_bpm'])
		self.cresterObject = self.crestingMethod(self, timer, self.linac1Phaser, findingLinac1Crest, 'findingCrest', \
		self.parameters['magnets'], self.parameters['dispersive_bpm'], \
		range, npoints, nsamples)
		return self.cresterObject

	def printFinished(self):
		print "Thread Finished!"

	def gunPhaser(self, gunPhaseSet=0, offset=True):
		if isinstance(self.calibrationPhase['Gun'],(float, int)) and isinstance(gunPhaseSet, (float, int)):
			self.setGunPhase(self.calibrationPhase['Gun'] + (gunPhaseSet if offset else 0))

	def linac1Phaser(self, linac1PhaseSet=0, offset=True):
		if isinstance(self.calibrationPhase['Linac1'],(float, int)) and isinstance(linac1PhaseSet, (float, int)):
			self.setLinac1Phase(self.calibrationPhase['Linac1'] + (linac1PhaseSet if offset else 0))

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
		print('Magnet to be Degaussed: '+str(deguassingList))
		self.magnets.degauss(deguassingList, True)
		while(self.magnets.isDegaussing(dipole)):
			print('Waiting for '+dipole+' to degauss...')
			time.sleep(0.1)
			app.processEvents()
		print('Switching off magnets...')
		switchOfFList=[]
		for magnet in magnets:
			if self.view.checkBox_quadOff.isChecked() and self.magnets.isAQuad(magnet):
				switchOfFList.append(magnet)
			elif self.view.checkBox_corrOff.isChecked() and self.magnets.isACor(magnet):
				switchOfFList.append(magnet)
		print('Magnet to be Switched Off: '+str(switchOfFList))
		self.magnets.switchOFFpsu(switchOfFList)

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
		self.magnets.setSI(dipole,current)

	def setAmplitude(self, cavity, value):
		print cavity, value
		if cavity == 'Gun':
			self.setGunAmplitude(value)
		elif cavity == 'Linac1':
			self.setLinac1Amplitude(value)

	def getAmplitude(self, cavity):
		if cavity == 'Gun':
			return self.getGunAmplitude()
		elif cavity == 'Linac1':
			return self.getLinac1Amplitude()

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

	def getKlystronForwardPower(self, cavity):
		if cavity == 'Gun':
			return self.getGunKlystronForwardPower()
		elif cavity == 'Linac1':
			return self.getLinac1KlystronForwardPower()

	def setGunPhase(self, phase):
		self.gunllrf.setPhiSP(phase)

	def getGunPhase(self):
		return self.gunllrf.getPhiSP()

	def setGunAmplitude(self, amp):
		print 'setting gun to ', amp
		self.gunllrf.setAmpSP(amp)

	def getGunAmplitude(self):
		return self.gunllrf.getAmpSP()

	def getGunKlystronForwardPower(self):
		return self.gunllrf.getKlyFwdPower()

	def getLinac1KlystronForwardPower(self):
		return self.linac1llrf.getKlyFwdPower()

	def setLinac1Phase(self, phase):
		if self.machineType == 'None':
			self.linac1PhiSp = phase
		else:
			self.linac1llrf.setPhiSP(phase)

	def getLinac1Phase(self):
		if self.machineType == 'None':
			return self.linac1PhiSp if hasattr(self, 'linac1PhiSp') else 0
		else:
			return self.linac1llrf.getPhiSP()

	def setLinac1Amplitude(self, amp):
		self.linac1llrf.setAmpFF(amp)

	def getLinac1Amplitude(self):
		return self.linac1llrf.getAmpSP()

	def getBPMPosition(self, bpm):
		if self.machineType == 'None':
			value = np.random.random_sample()
			self.bpmX.emit(value)
		else:
			print 'BPM X = ', self.bpm.getXFromPV(bpm)
			self.bpmX.emit(self.bpm.getXFromPV(bpm))

	def getWCMCharge(self, scope):
		self.wcmQ.emit(self.scope.getCharge(scope))

	def saveData(self):
		for cavity in ['Gun', 'Linac1']:
			my_dict = {}
			for name in ['approxPhaseData', 'approxChargeData', 'approxPhaseFit', 'approxChargeFit', 'approxChargeStd']:
				my_dict[name] = self.crestingData[cavity][name]
			with open(cavity+'_approx_CrestingData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
			    w = csv.DictWriter(f, my_dict.keys())
			    w.writeheader()
			    w.writerow(my_dict)
			my_dict = {}
			for name in ['finePhaseFit', 'fineBPMFit', 'finePhaseData', 'fineBPMData', 'fineBPMStd']:
				my_dict[name] = self.crestingData[cavity][name]
			with open(cavity+'_fine_CrestingData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
			    w = csv.DictWriter(f, my_dict.keys())
			    w.writeheader()
			    w.writerow(my_dict)

	def turnOnGun(self):
		self.crester = turnGunOn(self)
		self.crester.setAmp.connect(self.setAmplitude)

		self.gunThread = QThread()  # no parent!
		self.crester.moveToThread(self.gunThread)
		self.gunThread.started.connect(self.crester.rampGun)

		self.crester.finished.connect(self.printFinished)
		self.crester.finished.connect(self.gunThread.quit)

		self.gunThread.start()

	class dipoleSettingMethod(QThread):
		def __init__(self, parent, dipoleclass):
			QThread.__init__(self)
			self.crester = dipoleclass(parent)
			self.crester.setDip.connect(parent.setDIP01I)
			self.crester.degaussDip.connect(parent.degaussDIP01)

			self.crester.resetDataSignal.connect(parent.crestingData.resetData)
			self.crester.setDataSignal.connect(parent.crestingData.setData)
			self.crester.appendDataSignal.connect(parent.crestingData.appendData)
			self.crester.runSAMPLESignal.connect(parent.runSAMPLE)

			timer = partial(parent.startBPMTimer, bpm=parent.parameters['dispersive_bpm'])
			timer(self.crester)

			self.crester.moveToThread(self)
			self.started.connect(self.crester.findDipoleCurrent)

			self.crester.finished.connect(parent.timer.stop)
			self.crester.finished.connect(parent.printFinished)
			self.crester.finished.connect(self.quit)

	def setDipoleCurrentForGun(self):
		self.cresterObject = self.dipoleSettingMethod(self, setUpGunDipole)
		return self.cresterObject

	def setDipoleCurrentForLinac1(self):
		self.cresterObject = self.dipoleSettingMethod(self, setUpLinac1Dipole)
		return self.cresterObject

	def setDIP01I(self, I):
		# print 'setting dip01 = ', I
		if self.machineType == 'None':
			self.dipoleSI = I
		elif self.machineType == 'Virtual':
			self.magnets.setSI('DIP01', -1*I)
		elif self.machineType == 'Physical':
			self.magnets.setSI('DIP01', I)

	def getDIP01I(self):
		if self.machineType == 'None':
			return self.dipoleSI if hasattr(self, 'dipoleSI') else 0
		else:
			return self.magnets.getSI('DIP01')

	def degaussDIP01(self):
		self.magnets.degauss(['DIP01'], True)

	def isDIP01Degaussing(self):
		return self.magnets.isDegaussing('DIP01')

class turnGunOn(QObject):

	cavity = 'Gun'
	klystronData = []
	finished = pyqtSignal()
	setAmp = pyqtSignal(str, float)

	def __init__(self, parent=None):
		super(turnGunOn, self).__init__()
		self.parent = parent

	def rampGun(self):
		self.setAmp.emit('Linac1', 0)
		amp = self.parent.getAmplitude('Gun')
		if amp < 12000:
			for a in np.arange(amp, 12000, 1000):
				self.setAmp.emit('Gun', a)
				time.sleep(0.5)
			self.setAmp.emit('Gun', 12000)
			time.sleep(0.5)
		amp = self.parent.getAmplitude('Gun')
		if amp < 16200:
			for a in np.arange(amp, 16200, 500):
				self.setAmp.emit('Gun', a)
				time.sleep(0.5)
			self.setAmp.emit('Gun', 16200)
			time.sleep(0.5)
		self.finished.emit()

	def resetKlystronData(self):
		self.klystronData = []

	def storeKlystronData(self):
		self.klystronData.append(self.parent.getKlystronForwardPower(self.cavity))
		print self.klystronData

	def klystronTimer(self):
		self.klystronTimer = QTimer()
		self.klystronTimer.timeout.connect(self.storeKlystronData)
		self.klystronTimer.start(100)

	def checkKlystronSettled(self):
		print np.gradient(self.klystronData)

class crestingObject(QObject):

	finished = pyqtSignal()
	finishedSuccesfully = pyqtSignal()
	setPhase = pyqtSignal(str, float)
	setDip = pyqtSignal(float)
	degaussDip = pyqtSignal()
	setLabel = pyqtSignal(str)
	resetDataSignal = pyqtSignal(str, str, 'PyQt_PyObject')
	setDataSignal = pyqtSignal(str, str, 'PyQt_PyObject', 'PyQt_PyObject')
	appendDataSignal = pyqtSignal(str, str, 'PyQt_PyObject', 'PyQt_PyObject')
	crestingData = dataArray()
	data = []
	runSAMPLESignal = pyqtSignal()
	_isRunning = True
	_finish = False

	def __init__(self, parent=None):
		super(crestingObject, self).__init__()
		self.resetDataSignal.connect(self.crestingData.resetData)
		self.setDataSignal.connect(self.crestingData.setData)
		self.appendDataSignal.connect(self.crestingData.appendData)

	def printFinalPhase(self):
		print 'Calibration phase is', self.crestingData[self.cavity][self.actuator]['calibrationPhase']

	def abort(self):
		print 'stopping worker!'
		self._isRunning = False

	def finish(self):
		print 'finishing worker!'
		self._finish = True

	def resetDataArray(self):
		self.resetDataSignal.emit(self.cavity, self.actuator, ['xFit', 'yFit', 'xData', 'yData', 'yStd'])

	def setDataArray(self, x, y, ystd):
		self.appendDataSignal.emit(self.cavity, self.actuator, ['xData', 'yData', 'yStd'], [x, y, ystd])

	def setFitArray(self, x, y):
		self.setDataSignal.emit(self.cavity, self.actuator, ['xFit', 'yFit'], [x, y])

	def getDataArray(self, column=None, zipped=True):
		if column is not None:
			return self.crestingData[self.cavity][self.actuator][column]
		else:
			data = [self.crestingData[self.cavity][self.actuator]['xData'],
				self.crestingData[self.cavity][self.actuator]['yData'],
				self.crestingData[self.cavity][self.actuator]['yStd']]
			if zipped:
				return zip(*data)
			else:
				return data

	def getFitArray(self, zipped=True):
		data = [self.crestingData[self.cavity][self.actuator]['xFit'],
			self.crestingData[self.cavity][self.actuator]['yFit']]
		if zipped:
			return zip(*data)
		else:
			return data

	def setFinalPhase(self, phase):
		self.setDataSignal.emit(self.cavity, self.actuator, ['calibrationPhase'], [phase])

class setUpGunDipole(crestingObject):

	cavity = 'Gun'
	actuator = 'dipole'
	start = 5
	stop = 11
	step = 0.1
	initialGuess = [0, 10, 0.3, 9]

	def __init__(self, parent=None):
		super(setUpGunDipole, self).__init__()
		self.parent = parent

	def findDipoleCurrent(self):
		# self.degaussDipole()
		self.setLabel.emit('<b>Scanning Dipole!</b>')
		self.setDip.emit(self.start)
		while (self.parent.getDIP01I() / self.start) < 0.95 or (self.parent.getDIP01I() / self.start) > 1.05:
			time.sleep(0.1)
		self.resetDataArray()
		for dipI in np.arange(self.start, self.stop, self.step):
			self.setDip.emit(dipI)
			time.sleep(0.5)
			data, stddata = self.getData()
			self.setDataArray(dipI, data, stddata)
			if not self._isRunning or self._finish:
				break
		if self._isRunning:
			self.doFit()
			# self.degaussDipole()
			time.sleep(0.2)
			for i in range(3):
				self.setDip.emit(self.finalDipoleI)
				time.sleep(0.2)
			self.setLabel.emit('Ready')
			self.finishedSuccesfully.emit()
		self.finished.emit()

	def degaussDipole(self):
		self.degaussDip.emit()
		self.setLabel.emit('<b>Degaussing Dipole!</b>')
		while not self.parent.isDIP01Degaussing():
			time.sleep(0.5)
		while self.parent.isDIP01Degaussing():
			time.sleep(0.5)
		self.setLabel.emit('Ready')

	def cutData(self):
		allData = self.getDataArray()
		cutData = [a for a in allData if not a[1] == 20]
		newlist = []
		for i, pt in enumerate(cutData):
			if i < (len(cutData)-1):
				if not cutData[i+1][0] - pt[0] > 2*self.step:
					newlist.append(pt)
			elif i == (len(cutData)-1):
				newlist.append(pt)
		return newlist

	def fitting_equation(self, x, a, b, c, crest):
			return a + b * (np.sin(c * (x - crest)))

	def doFit(self):
		cutData = self.cutData()
		x, y, std = zip(*cutData)
		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)

		if max(x) < self.initialGuess[-1]:
			self.initialGuess[-1] = max(x)

		popt, pcov = curve_fit(self.fitting_equation, x, y, sigma=std, \
		p0=self.initialGuess, bounds=([-np.inf, -np.inf, -np.inf, min(x)], [np.inf, np.inf, np.inf, max(x)]))

		print 'Calibration dipole Sin fit is', popt[3]

		self.setFitArray(np.array(xnew), self.fitting_equation(xnew, *popt))
		self.finalDipoleI = popt[3]

	def updateBPMPosition(self, value):
		self.data.append(value)

	def getData(self):
		self.data = []
		while len(self.data) < 3:
			self.runSAMPLESignal.emit()
			time.sleep(0.1)
			if not self._isRunning:
				break
		return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [20,0]

class setUpLinac1Dipole(setUpGunDipole):

	cavity = 'Linac1'
	actuator = 'dipole'
	start = 70
	stop = 100
	step = 1
	initialGuess = [0, 10, 0.3, 89]

class crestingObjectQuick(crestingObject):

	stepSize = 5

	def __init__(self, parent):
		super(crestingObjectQuick, self).__init__()
		self.parent = parent
		self.resetDataArray()
		self.offset = 0

	def findingCrest(self):
		self.setLabel.emit('Starting Thread!')
		self.approxcrest = self.parent.getPhase(self.cavity)
		for phase in np.arange(-180,180,self.stepSize):
			self.setPhase.emit(self.cavity, phase)
			data, stddata = self.getData()
			self.setDataArray(phase, data, stddata)
			if not self._isRunning or self._finish:
				break
			self.setPhase.emit(self.cavity, self.approxcrest)
		if self._isRunning:
			self.doFit()
		self.finished.emit()

	def fitness_function(self, list, a, b, c, d, e, f):
		x = np.array(list)
		return f*x**5 + e*x**4 + d*x**3 + a*x**2 + b*x + c

	def doFit(self):
		try:
			cutData = self.cutData()
			xData, yData = zip(*cutData)
			popt, pcov = curve_fit(self.fitness_function, xData, yData, p0=None)
			self.setFitArray(np.array(xData), self.fitness_function(np.array(xData), *popt))
			# print(popt)
			# Find the peak, assuming the fit function is a polynomial
			# We have to take the derivative, so e*x**4 -> 4*e*x**3 etc.
			crest_phase = np.real(np.roots(np.multiply(range(len(popt) - 1, 0, -1), popt[:-1]))[0])

			# self.setFinalPhase(-popt[1]/(2*popt[0])) # Assume Max Charge is -15deg from crest
			self.setFinalPhase(crest_phase)
			self.printFinalPhase()
			self.finishedSuccesfully.emit()
		except Exception as e:
			print(e)
			print 'Error in fitting!'

class findingGunCrestWCM(crestingObjectQuick):

	cavity = 'Gun'
	actuator = 'approx'
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
			self.runSAMPLESignal.emit()
			if not self._isRunning:
				break
			time.sleep(0.1)
		return [np.mean(self.data), np.std(self.data)]

	def cutData(self):
		"""Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
		allData = self.getDataArray()
		max_charge = max(getDataArray('yData'))

		cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 10]
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

			self.setFinalPhase(crest_phase)
			self.printFinalPhase()
			self.finishedSuccesfully.emit()
		except Exception as e:
			print(e)
			print 'Error in fitting!'

class findingLinac1CrestQuick(crestingObjectQuick):

	cavity = 'Linac1'
	actuator = 'approx'
	offset = 0
	stepSize = 5

	def updateBPMPosition(self, value):
		self.data.append(value)

	def getData(self):
		self.data = []
		while len(self.data) < 3:
			self.runSAMPLESignal.emit()
			time.sleep(0.1)
			if not self._isRunning:
				break
		return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [20,0]

	def cutData(self):
		allData = self.getDataArray()
		cutData = [a for a in allData if a[1] == 20]
		newlist = []
		for i, pt in enumerate(cutData):
			if i < (len(cutData)-1):
				if not cutData[i+1][0] - pt[0] > 2*self.stepSize:
					newlist.append(pt)
			elif i == (len(cutData)-1):
				newlist.append(pt)
		return newlist

	def doFit(self):
		try:
			cutData = self.cutData()
			x, y, std = zip(*cutData)
			crest_phase = np.mean(x)-180
			self.setFitData(np.array(x), np.array(y))
			self.setFinalPhase(crest_phase)
			self.printFinalPhase()
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
				self.runSAMPLESignal.emit()
				time.sleep(0.1)
			self.data = []
			while len(self.data) < self.bpmSamples:
				self.runSAMPLESignal.emit()
				time.sleep(0.1)
				if not self._isRunning:
					break
			data = np.mean(self.data)
			if np.std(self.data) > 0.0005:
				self.setDataArray(currphase, data, np.std(self.data))
			if not self._isRunning or self._finish:
				break

		if self._isRunning:
			self.fitting()
		self.finished.emit()

	def fitting_equation(self, x, a, b, crest):
		return a + b * (np.sin((crest - (x + 180)) * degree)**2)

	def calculateCrest(self, popt):
		return ((180 + popt[2]) % 360) - 180

	def fitting(self):
		x, y, std = self.getDataArray(zipped=False)
		popt, pcov = curve_fit(self.fitting_equation, x, y, \
			sigma=std,	p0=[0,10,self.approxcrest])

		phase = np.array(self.crestingData[self.cavity]['finePhaseData'])
		data = self.fitting_equation(phase, *popt)
		self.setFitData(phase, data)

		self.setFinalPhase(((180 + popt[2]) % 360) - 180)
		self.printFinalPhase()
		self.finishedSuccesfully.emit()

class findingGunCrest(crestingObjectFine):

	cavity = 'Gun'
	actuator = 'fine'

	def fitting(self):
		x, y, std = self.getDataArray(zipped=False)
		k = 5 if len(x) < 6 else (len(x) - 1)
		f = UnivariateSpline(x, y, w=std, k=k)

		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
		ynew = f(xnew)

		crest = xnew[np.argmin(ynew)]

		self.setFitArray(xnew, ynew)

		self.setFinalPhase(crest)
		self.printFinalPhase()
		self.finishedSuccesfully.emit()

class findingLinac1Crest(crestingObjectFine):

	cavity = 'Linac1'
	actuator = 'fine'

	def fitting(self):
		x, y, std = self.getDataArray(zipped=False)
		k = 5 if len(x) > 6 else (len(x) - 2)
		print 'k = ', k
		if k > 0:
			f = UnivariateSpline(x, y, w=std, k=k)

			xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
			ynew = f(xnew)

			crest = xnew[np.argmin(ynew)]

			self.setFitArray(xnew, ynew)

			self.setFinalPhase(crest)
			self.printFinalPhase()
			self.finishedSuccesfully.emit()
