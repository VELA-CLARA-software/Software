# from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import random as r
from functools import partial
sys.path.append("../../../")
import Software.Procedures.Machine.machine as machine
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
	sleepTimeDipole = 0.001

	def __init__(self, machineType, lineType, gunType):
		super(Model, self).__init__()
		self.baseMachine = machine.Machine(machineType, lineType, gunType)
		self.machine = machineSetter(self.baseMachine)
		self.machineType = machineType
		self.lineType = lineType
		self.gunType = gunType
		self.newData = emitter()
		self.logger = emitter()
		self.progress = emitter()
		if not self.machineType == 'None':
			self.sleepTime = 0.1
			self.sleepTimeDipole = 0.25
		self.crestingData = dataArray()
		self.parameters = self.baseMachine.initilise_parameters()
		self.data = []
		self.calibrationPhase = {'Gun': None, 'Linac1': None}
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

	def magnetDegausser(self):
		print('1. Setting up Magnets')
		self.setUpMagnets(self.parameters['magnets'])

	def loadGunBURT(self):
		if self.machineType is not 'Physical':
			return True
		else:
			return self.machine.magnets.applyDBURT('GunCrest.dburt')

	def loadLinac1BURT(self):
		if self.machineType is not 'Physical':
			return True
		else:
			return self.machine.magnets.applyDBURT('Linac1Crest.dburt')

	def gunWCMCrester(self, stepSize=5, nSamples=4):
		self.resetAbortFinish()
		self.cavity = 'Gun'
		self.actuator = 'approx'
		self.stepSize = stepSize
		self.nSamples = nSamples
		self.getDataFunction = partial(self.machine.getWCMCharge, self.parameters['scope'])
		self.findingCrestGunQuick()

	def linacCresterQuick(self, no, stepSize=5, nSamples=4):
		self.resetAbortFinish()
		self.cavity = 'Linac'+str(no)
		self.actuator = 'approx'
		self.stepSize = stepSize
		self.nSamples = nSamples
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_rough_bpm'][no])
		self.findingCrestLinacQuick()

	def gunCresterFine(self, phiStart, phiRange, phiSteps, nSamples):
		self.resetAbortFinish()
		self.cavity = 'Gun'
		self.actuator = 'fine'
		self.stepSize = 5
		self.nSamples = nSamples
		self.phiStart = phiStart
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['gun_dispersive_bpm'])
		self.findingCrestFine()

	def linacCresterFine(self, no, phiRange, phiSteps, nSamples):
		self.resetAbortFinish()
		self.cavity = 'Linac'+str(no)
		self.actuator = 'fine'
		self.stepSize = 5
		self.nSamples = nSamples
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_dispersive_bpm'][no])
		self.findingCrestFine()

	def gunDipoleSet(self, start=5, stop=10):
		self.resetAbortFinish()
		self.cavity = 'Gun'
		self.actuator = 'dipole'
		self.nSamples = 10
		self.minDipoleI = start
		self.maxDipoleI = stop
		self.dipoleIStep = 0.1
		self.initialGuess = [10, 1, 9]
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['gun_dispersive_bpm'])
		self.findDipoleCurrent()

	def linacDipoleSet(self, no, start=70, stop=100):
		self.resetAbortFinish()
		self.cavity = 'Linac'+str(no)
		self.actuator = 'dipole'
		self.nSamples = 3
		self.minDipoleI = start
		self.maxDipoleI = stop
		self.dipoleIStep = 1
		self.initialGuess = [10, 1, (stop+start)/2]
		self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_dispersive_bpm'][no])
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

	def appendDataArray(self, x, y, yStd):
		self.crestingData[self.cavity][self.actuator]['xData'].append(x)
		self.crestingData[self.cavity][self.actuator]['yData'].append(y)
		self.crestingData[self.cavity][self.actuator]['yStd'].append(yStd)
		self.newData.emit()

	def setDataArray(self, x, y, yStd):
		self.crestingData[self.cavity][self.actuator]['xData'] = x
		self.crestingData[self.cavity][self.actuator]['yData'] = y
		self.crestingData[self.cavity][self.actuator]['yStd'] = yStd
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
		# self.data = []
		# while len(self.data) < 2:
		# 	self.data.append(self.getDataFunction())
		# 	time.sleep(self.sleepTime)
		time.sleep(self.sleepTime)
		self.data = []
		while len(self.data) < self.nSamples:
			self.data.append(self.getDataFunction())
			time.sleep(self.sleepTime)
		return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [20,0]

	def rotate_list(self, l, n):
		return l[n:] + l[:n]

########### findingCrestGunQuick ###############

	def findingCrestQuick(self):
		self.resetDataArray()
		self.approxcrest = self.machine.getPhase(self.cavity)
		range = np.arange(-180, 181, self.stepSize)
		for i,phase in enumerate(range):
			self.progress.emit(100*i/len(range))
			if self._abort or self._finished:
				return
			self.machine.setPhase(self.cavity, phase)
			data, stddata = self.getData()
			self.appendDataArray(phase, data, stddata)
		self.progress.emit(100)

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
		cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 10]
		return cutData

	def doFitGunQuick(self):
		cutData = self.cutDataGunQuick()
		x, y, std = zip(*cutData)
		if max(x) - min(x) > 90:
			x = [a if a >= 0 else a+360 for a in x]
			phase, data, stddata = self.getDataArray(zipped=False)
			phase = np.array([a if a >= 0 else a+360 for a in phase])
			self.setDataArray(phase, data, stddata)
		crest_phase = np.mean(x)
		if crest_phase > 180:
			crest_phase -= 360
		self.setFitArray(np.array(x), np.array(y))
		self.setFinalPhase(crest_phase)
		self.printFinalPhase()

########### findingCrestLinac1Quick ###############

	def findingCrestLinacQuick(self):
		self.startingPhase = self.machine.getPhase(self.cavity)
		self.findingCrestQuick()
		if not self._abort:
			self.doFitLinacQuick()
		else:
			 self.machine.setPhase(self.cavity, self.startingPhase)

	def cutDataLinacQuick(self):
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

	def doFitLinacQuick(self):
		try:
			cutData = self.cutDataLinacQuick()
			x, y, std = zip(*cutData)
			if max(x) - min(x) > 180:
				x = [a if a >= 0 else a+360 for a in x]
				phase, data, stddata = self.getDataArray(zipped=False)
				phase = np.array([a if a >= 0 else a+360 for a in phase])
				self.setDataArray(phase, data, stddata)
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
		self.approxcrest = self.phiStart
		self.minPhase = self.approxcrest-self.phiRange
		self.maxPhase = self.approxcrest+self.phiRange+self.phiSteps
		range = np.arange(self.minPhase, self.maxPhase, self.phiSteps)
		for i, phase in enumerate(range):
			self.progress.emit(100*i/len(range))
			if self._abort or self._finished:
				return
			self.machine.setPhase(self.cavity, phase)
			time.sleep(self.sleepTime)
			currphase = self.machine.getPhase(self.cavity)
			data, stddata = self.getData()
			if stddata > 0.05:
				self.appendDataArray(currphase, data, stddata)
		if not self._abort:
			self.fittingFunc()
		else:
			self.machine.setPhase(self.cavity, self.startingPhase)
		self.progress.emit(100)

	def fittingFunc(self):
		if self.cavity == 'Gun':
			self.fittingGunFine()
		elif self.cavity == 'Linac1':
			self.fittingLinac1Fine()

	def cutDataGunFine(self):
		"""Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
		allData = self.getDataArray(sortKey=lambda x: x[0])
		cutData = [a for a in allData if a[-1] < 1]
		return cutData

	def fittingGunFine(self):
		data = self.cutDataGunFine()
		x, y, std = zip(*data)
		if (max(x) - min(x)) > (self.maxPhase - self.minPhase):
			x = [a if a >= 0 else a+360 for a in x]
		# f = UnivariateSpline(x, y, w=std, k=5)
		# xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
		# ynew = f(xnew)
		# crest_phase = xnew[np.argmin(ynew)]
		# xnew = [a if a <= 180 else a-360 for a in xnew]
		# if crest_phase > 180:
		# 	crest_phase -= 360
		# if crest_phase < 180:
		# 	crest_phase += 360
		# self.setFitArray(xnew, ynew)
		# self.setFinalPhase(crest_phase)
		# self.printFinalPhase()
		popt, pcov = curve_fit(self.fitting_equation_Linac1Fine, x, y, \
			sigma=std,	p0=[0,10,self.approxcrest], bounds=[[-np.inf, -np.inf, min(x)], [np.inf, np.inf, max(x)]])

		phase = np.array(x)
		data = self.fitting_equation_Linac1Fine(phase, *popt)
		self.setFitArray(phase, data)
		crest_phase = ((180 + popt[2]) % 360) - 180
		if crest_phase > 180:
			crest_phase -= 360
		if crest_phase < 180:
			crest_phase += 360
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

########### findingDipoleCurrent ###############

	def findDipoleCurrent(self):
		self.startingDipole = self.machine.getDip()
		self.resetDataArray()
		range = np.arange(self.minDipoleI, self.maxDipoleI, self.dipoleIStep)
		for i,I in enumerate(range):
			self.progress.emit(100*i/len(range))
			if self._abort or self._finished:
				return
			self.machine.setDip(I)
			while abs(self.machine.getDip() - I) > 0.2:
				time.sleep(self.sleepTimeDipole)
			data, stddata = self.getData()
			self.appendDataArray(I, data, stddata)
		if not self._abort:
			self.doFitDipoleCurrent()
		else:
			 self.machine.setDip(self.startingDipole)
			 while abs(self.machine.getDip() - self.startingDipole) > 0.2:
 				time.sleep(self.sleepTimeDipole)
		self.progress.emit(100)

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

	def fitting_equation_DipoleCurrent(self, x, b, c, crest):
		# return 0 + b * (x - crest)
		return b * (np.sin(c * (x - crest)))

	def doFitDipoleCurrent(self):
		cutData = self.cutDataDipoleCurrent()
		x, y, std = zip(*cutData)
		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)

		if max(x) < self.initialGuess[-1]:
			self.initialGuess[-1] = max(x)

		popt, pcov = curve_fit(self.fitting_equation_DipoleCurrent, x, y, sigma=std, \
		p0=self.initialGuess, bounds=([-np.inf, -np.inf, min(x)], [np.inf, np.inf, max(x)]))

		self.setFitArray(np.array(xnew), self.fitting_equation_DipoleCurrent(xnew, *popt))
		self.finalDipoleI = popt[-1]
		self.setFinalDip(self.finalDipoleI)
		while abs(self.machine.getDip() - self.finalDipoleI) > 0.2:
			time.sleep(self.sleepTimeDipole)
		self.printFinalDip()

########### SetDipoleMomentum ###############

	def SetDipoleMomentum(self, mom):
		current = self.machine.calculateDipoleMomentum(mom)
		self.machine.setDip(current)

	def calculateDipoleFromMomentum(self, mom):
		D = self.machine.magnets.getMagObjConstRef('DIP01')
		coeffs = list(D.fieldIntegralCoefficients)
		coeffs[-1] -= (1000000000*(mom*physics.pi*45)/(physics.c*180))
		roots = np.roots(coeffs)
		return roots[-1].real

	def calculateMomentumFromDipole(self, current):
		D = self.machine.magnets.getMagObjConstRef('DIP01')
		sign = np.copysign(1, current)
		coeffs = np.append(D.fieldIntegralCoefficients[:-1] * sign, D.fieldIntegralCoefficients[-1])
		int_strength = np.polyval(coeffs, abs(current))
		angle = 45  # reset to 45
		print 1e-6*0.001 * physics.c * int_strength / np.radians(angle)
		return 1e-6*0.001 * physics.c * int_strength / np.radians(angle)
