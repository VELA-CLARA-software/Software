# from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import random as r
from functools import partial
import machine
degree = physics.pi/180.0

class dataArray(dict):

	def __init__(self):
		super(dataArray, self).__init__()

	def checkDataArray(self, cavity, actuator, type):
		cavity = str(cavity)
		actuator = str(actuator)
		type = str(type)
		if not cavity in self:
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

	def setData(self, cavity, actuator, type, data):
		cavity = str(cavity)
		actuator = str(actuator)
		for t, d in zip(type, data):
			t = str(t)
			self.checkDataArray(cavity, actuator, t)
			self[cavity][actuator][t] = d

	def appendData(self, cavity, actuator, type, data):
		cavity = str(cavity)
		actuator = str(actuator)
		for t, d in zip(type, data):
			t = str(t)
			self.checkDataArray(cavity, actuator, t)
			self[cavity][actuator][t].append(d)

class emitter(object):

	def __init__(self, signal=None):
		super(emitter, self).__init__()
		self.signal = signal

	def emit(self, *args, **kwargs):
		if self.signal is not None:
			self.signal.emit(*args, **kwargs)

class machineSetter(object):
	def __init__(self, machine):
		super(machineSetter, self).__init__()
		self.machine = machine

	def __getattr__(self, attr):
		return getattr(self.machine,attr)

class Model(object):

	sleepTime = 0.001
	sleepTimeDipole = 0.01

	def __init__(self, machineType, lineType, gunType):
		super(Model, self).__init__()
		self.baseMachine = machine.Machine(machineType, lineType, gunType)
		self.machine = machineSetter(self.baseMachine)
		self.machineType = machineType
		self.lineType = lineType
		self.gunType = gunType
		self.newData = emitter()
		self.logger = emitter()
		if not self.machineType == 'None':
			self.sleepTime = 0.1
			self.sleepTimeDipole = 0.25
		self.crestingData = dataArray()
		self.parameters={}
		self.data = []
		self.calibrationPhase = {'Gun': None, 'Linac1': None}
		self.run()
		print("Model Initialized")

	def abort(self):
		self._abort = True

	def finish(self):
		self._finished = True

	def resetAbortFinish(self):
		self._abort = False
		self._finished = False

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

	def gunWCMCrester(self, stepSize=5, nSamples=4):
		self.resetAbortFinish()
		self.cavity = 'Gun'
		self.actuator = 'approx'
		self.stepSize = stepSize
		self.nSamples = nSamples
		self.getDataFunction = partial(self.machine.getWCMCharge, self.parameters['scope'])
		self.findingCrestGunQuick()

	def linac1CresterQuick(self, stepSize=5, nSamples=4):
		self.resetAbortFinish()
		self.cavity = 'Linac1'
		self.actuator = 'approx'
		self.stepSize = stepSize
		self.nSamples = nSamples
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_rough_bpm'])
		self.findingCrestLinac1Quick()

	def gunCresterFine(self, phiRange, phiSteps, nSamples):
		self.resetAbortFinish()
		self.cavity = 'Gun'
		self.actuator = 'fine'
		self.stepSize = 5
		self.nSamples = nSamples
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['dispersive_bpm'])
		self.findingCrestFine()

	def linac1CresterFine(self, phiRange, phiSteps, nSamples):
		self.resetAbortFinish()
		self.cavity = 'Linac1'
		self.actuator = 'fine'
		self.stepSize = 5
		self.nSamples = nSamples
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['dispersive_bpm'])
		self.findingCrestFine()

	def gunDipoleSet(self, start=5, stop=10):
		self.resetAbortFinish()
		self.cavity = 'Gun'
		self.actuator = 'dipole'
		self.nSamples = 3
		self.minDipoleI = start
		self.maxDipoleI = stop
		self.dipoleIStep = 0.1
		self.initialGuess = [0, 10, 0.3, 9]
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['dispersive_bpm'])
		self.findDipoleCurrent()

	def linac1DipoleSet(self, start=70, stop=100):
		self.resetAbortFinish()
		self.cavity = 'Linac1'
		self.actuator = 'dipole'
		self.nSamples = 3
		self.minDipoleI = start
		self.maxDipoleI = stop
		self.dipoleIStep = 1
		self.initialGuess = [0, 10, 0.3, 89]
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['dispersive_bpm'])
		self.findDipoleCurrent()

	def gunPhaser(self, gunPhaseSet=0, offset=True):
		if isinstance(self.calibrationPhase['Gun'],(float, int)) and isinstance(gunPhaseSet, (float, int)):
			self.machine.setGunPhase(self.calibrationPhase['Gun'] + (gunPhaseSet if offset else 0))

	def linac1Phaser(self, linac1PhaseSet=0, offset=True):
		if isinstance(self.calibrationPhase['Linac1'],(float, int)) and isinstance(linac1PhaseSet, (float, int)):
			self.machine.setLinac1Phase(self.calibrationPhase['Linac1'] + (linac1PhaseSet if offset else 0))

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

	def printFinalPhase(self):
		print self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationPhase'])
		self.logger.emit(self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationPhase']))

	def printFinalDip(self):
		print self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationDip'])
		self.logger.emit(self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationDip']))

	def resetDataArray(self):
		self.crestingData.resetData(self.cavity, self.actuator, ['xFit', 'yFit', 'xData', 'yData', 'yStd'])

	def setDataArray(self, x, y, yStd):
		self.crestingData[self.cavity][self.actuator]['xData'].append(x)
		self.crestingData[self.cavity][self.actuator]['yData'].append(y)
		self.crestingData[self.cavity][self.actuator]['yStd'].append(yStd)
		self.newData.emit()

	def setFitArray(self, x, y):
		self.crestingData[self.cavity][self.actuator]['xFit'] = x
		self.crestingData[self.cavity][self.actuator]['yFit'] = y
		self.newData.emit()

	def getDataArray(self, column=None, zipped=True, sortKey=None):
		if column is not None:
			return self.crestingData[self.cavity][self.actuator][column]
		else:
			data = [self.crestingData[self.cavity][self.actuator]['xData'],
				self.crestingData[self.cavity][self.actuator]['yData'],
				self.crestingData[self.cavity][self.actuator]['yStd']]
			if sortKey is not None:
				data = zip(*sorted(zip(*data), key=sortKey))
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
		phase = np.mod(180+phase,360)-180
		self.crestingData[self.cavity]['calibrationPhase'] = phase
		self.machine.setPhase(self.cavity, phase)

	def setFinalDip(self, dip):
		self.crestingData[self.cavity]['calibrationDip'] = dip
		self.machine.setDip(dip)

	def getData(self):
		self.data = []
		while len(self.data) < 2:
			self.data.append(self.getDataFunction())
			time.sleep(self.sleepTime)
		self.data = []
		while len(self.data) < self.nSamples:
			self.data.append(self.getDataFunction())
			time.sleep(self.sleepTime)
		return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [20,0]

########### findingCrestGunQuick ###############

	def findingCrestQuick(self):
		self.resetDataArray()
		self.approxcrest = self.machine.getPhase(self.cavity)
		for phase in np.arange(-180, 181, self.stepSize):
			if self._abort or self._finished:
				return
			self.machine.setPhase(self.cavity, phase)
			data, stddata = self.getData()
			self.setDataArray(phase, data, stddata)

	def findingCrestGunQuick(self):
		self.startingPhase = self.machine.getPhase(self.cavity)
		self.findingCrestQuick()
		if not self._abort:
			self.doFitGunQuick()
		else:
			 self.machine.setPhase(self.cavity, self.startingPhase)

	def updateWCMCharge(self, value):
		self.data.append(value)

	def cutDataGunQuick(self):
		"""Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
		allData = self.getDataArray()
		max_charge = max(self.getDataArray('yData'))

		cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 10 and a[2] < 2]
		return cutData

	def doFitGunQuick(self):
		cutData = self.cutDataGunQuick()
		x, y, std = zip(*cutData)
		if max(x) - min(x) > 90:
			x = [a if a >= 0 else a+360 for a in x]
		crest_phase = (x[-1] + x[0]) / 2.0
		if crest_phase > 180:
			crest_phase -= 360
		x = [a if a <= 180 else a-360 for a in x]
		self.setFitArray(np.array(x), np.array(y))
		self.setFinalPhase(crest_phase)
		self.printFinalPhase()

########### findingCrestLinac1Quick ###############

	def findingCrestLinac1Quick(self):
		self.startingPhase = self.machine.getPhase(self.cavity)
		self.findingCrestQuick()
		if not self._abort:
			self.doFitLinac1Quick()
		else:
			 self.machine.setPhase(self.cavity, self.startingPhase)

	def cutDataLinac1Quick(self):
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

	def doFitLinac1Quick(self):
		try:
			cutData = self.cutDataLinac1Quick()
			x, y, std = zip(*cutData)
			if max(x) - min(x) > 180:
				x = [a if a >= 0 else a+360 for a in x]
			crest_phase = np.mean(x)-180
			if crest_phase > 180:
				crest_phase -= 360
			if crest_phase < 180:
				crest_phase += 360
			x = [a if a <= 180 else a-360 for a in x]
			self.setFitArray(np.array(x), np.array(y))
			self.setFinalPhase(crest_phase)
			self.printFinalPhase()
		except Exception as e:
			print(e)

########### findingCrestGunFine ###############

	def findingCrestFine(self):
		self.startingPhase = self.machine.getPhase(self.cavity)
		self.resetDataArray()
		if self.calibrationPhase[self.cavity] is None:
			self.approxcrest = self.machine.getPhase(self.cavity)
		else:
			self.approxcrest = self.calibrationPhase[self.cavity]
		self.approxcrest = self.machine.getPhase(self.cavity)
		self.minPhase = self.approxcrest-self.phiRange
		self.maxPhase = self.approxcrest+self.phiRange+self.phiSteps
		for phase in np.arange(self.minPhase, self.maxPhase, self.phiSteps):
			if self._abort or self._finished:
				return
			self.machine.setPhase(self.cavity, phase)
			time.sleep(self.sleepTime)
			currphase = self.machine.getPhase(self.cavity)
			data, stddata = self.getData()
			if stddata > 0.0005:
				self.setDataArray(currphase, data, stddata)
		if not self._abort:
			self.fittingFunc()
		else:
			 self.machine.setPhase(self.cavity, self.startingPhase)

	def fittingFunc(self):
		if self.cavity == 'Gun':
			self.fittingGunFine()
		elif self.cavity == 'Linac1':
			self.fittingLinac1Fine()

	def fittingGunFine(self):
		x, y, std = self.getDataArray(zipped=False, sortKey=lambda x: x[0])
		if (max(x) - min(x)) > (self.maxPhase - self.minPhase):
			x = [a if a >= 0 else a+360 for a in x]
		f = UnivariateSpline(x, y, w=std, k=5)
		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
		ynew = f(xnew)
		crest_phase = xnew[np.argmin(ynew)]
		xnew = [a if a <= 180 else a-360 for a in xnew]
		if crest_phase > 180:
			crest_phase -= 360
		if crest_phase < 180:
			crest_phase += 360
		self.setFitArray(xnew, ynew)
		self.setFinalPhase(crest_phase)
		self.printFinalPhase()

	def fitting_equation_Linac1Fine(self, x, a, b, crest):
		return a + b * (np.sin((crest - (x + 180)) * degree)**2)

	def fittingLinac1Fine(self):
		x, y, std = self.getDataArray(zipped=False)
		popt, pcov = curve_fit(self.fitting_equation_Linac1Fine, x, y, \
			sigma=std,	p0=[0,10,self.approxcrest], bounds=[[-np.inf, -np.inf, min(x)], [np.inf, np.inf, max(x)]])

		phase = np.array(x)
		data = self.fitting_equation_Linac1Fine(phase, *popt)
		self.setFitArray(phase, data)
		self.setFinalPhase(((180 + popt[2]) % 360) - 180)
		self.printFinalPhase()

########### findingCrestGunFine ###############

	def findDipoleCurrent(self):
		self.startingDipole = self.machine.getDip()
		self.resetDataArray()
		for I in np.arange(self.minDipoleI, self.maxDipoleI, self.dipoleIStep):
			# print 'setting I = ', I
			if self._abort or self._finished:
				return
			self.machine.setDip(I)
			while abs(self.machine.getDip() - I) > 0.2:
				time.sleep(self.sleepTimeDipole)
			data, stddata = self.getData()
			self.setDataArray(I, data, stddata)
		if not self._abort:
			self.doFitDipoleCurrent()
		else:
			 self.machine.setDip(self.startingDipole)
			 while abs(self.machine.getDip() - self.startingDipole) > 0.2:
 				time.sleep(self.sleepTimeDipole)

	def cutDataDipoleCurrent(self):
		allData = self.getDataArray()
		cutData = [a for a in allData if not a[1] == 20]
		newlist = []
		for i, pt in enumerate(cutData):
			if i < (len(cutData)-1):
				if not cutData[i+1][0] - pt[0] > 2*self.dipoleIStep:
					newlist.append(pt)
			elif i == (len(cutData)-1):
				newlist.append(pt)
		return newlist

	def fitting_equation_DipoleCurrent(self, x, a, b, c, crest):
		return a + b * (np.sin(c * (x - crest)))

	def doFitDipoleCurrent(self):
		cutData = self.cutDataDipoleCurrent()
		x, y, std = zip(*cutData)
		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)

		if max(x) < self.initialGuess[-1]:
			self.initialGuess[-1] = max(x)

		popt, pcov = curve_fit(self.fitting_equation_DipoleCurrent, x, y, sigma=std, \
		p0=self.initialGuess, bounds=([-np.inf, -np.inf, -np.inf, min(x)], [np.inf, np.inf, np.inf, max(x)]))

		self.setFitArray(np.array(xnew), self.fitting_equation_DipoleCurrent(xnew, *popt))
		self.finalDipoleI = popt[3]
		self.setFinalDip(self.finalDipoleI)
		while abs(self.machine.getDip() - self.finalDipoleI) > 0.2:
			time.sleep(self.sleepTimeDipole)
		self.printFinalDip()
