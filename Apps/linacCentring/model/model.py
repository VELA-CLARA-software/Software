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
import pandas as pd

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

	def set(self, function, *args, **kwargs):
		getattr(self.machine,function)(*args, **kwargs)

	def get(self, function, *args, **kwargs):
		return getattr(self.machine,function)(*args, **kwargs)

class Model(object):

	sleepTime = 0.001
	sleepTimeDipole = 0.001

	def __init__(self, machineType, lineType, gunType):
		super(Model, self).__init__()
		self.baseMachine = machine.Machine(machineType, lineType, gunType)
		self._abort = False
		self.machine = machineSetter(self.baseMachine)
		self.machineType = machineType
		self.lineType = lineType
		self.gunType = gunType
		self.newData = emitter()
		self.logger = emitter()
		if not self.machineType == 'None':
			self.sleepTime = 0.1
			self.sleepTimeDipole = 0.25
		self.experimentalData = dataArray()
		self.parameters={}
		self.data = []
		self.calibrationPhase = {'Gun': None, 'Linac1': None}
		self.run()
		print("Model Initialized")

	def setRunning(self):
		self.running = True

	def setNotRunning(self):
		self.running = False

	def abort(self):
		self._abort = True
		self.setNotRunning()

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

	def getDataFunction(self):
		return [b() for b in self.bpms]

	def sol1Scan(self, plane, ampLower, ampUpper, corrRange, corrStep, nSamples):
		self.main = 'L01-SOL1'
		self.plane = plane
		if plane == 'Y':
			self.sub = 'fine'
			self.corrector1 = 'S01-VCOR1'
			self.corrector2 = 'S01-VCOR2'
		else:
			self.sub = 'approx'
			self.corrector1 = 'S01-HCOR1'
			self.corrector2 = 'S01-HCOR2'
		self.correctorStepSize = corrStep
		self.correctorRange = corrRange
		self.solLowerAmp = ampLower
		self.solUpperAmp = ampUpper
		self.nSamples = nSamples
		self.bpms = [partial(self.machine.getBPMPosition, 'S02-BPM01', plane)]
		self.findSOLCentre()

	def sol2Scan(self, plane, ampLower, ampUpper, corr1Range, corr2Range, corrStep, nSamples):
		self.main = 'L01-SOL2'
		self.plane = plane
		if plane == 'Y':
			self.sub = 'fine'
			self.corrector1 = 'S01-VCOR1'
			self.corrector2 = 'S01-VCOR2'
		else:
			self.sub = 'approx'
			self.corrector1 = 'S01-HCOR1'
			self.corrector2 = 'S01-HCOR2'
		self.correctorStepSize = corrStep
		self.corrector1Min, self.corrector1Max = corr1Range
		self.corrector2Min, self.corrector2Max = corr2Range
		self.solLowerAmp = ampLower
		self.solUpperAmp = ampUpper
		self.nSamples = nSamples
		self.bpms = [partial(self.machine.getBPMPosition, 'S02-BPM01', plane), partial(self.machine.getBPMPosition, 'S02-BPM02', plane)]
		self.findSOLCentre()

	def linac1Scan(self, actuator, plane, ampLower, ampUpper, corr1Range, corr2Range, corrStep, nSamples):
		self.main = 'Linac1'
		self.sub = actuator
		self.plane = plane
		if plane == 'Y':
			self.corrector1 = 'S01-VCOR1'
			self.corrector2 = 'S01-VCOR2'
		else:
			self.corrector1 = 'S01-HCOR1'
			self.corrector2 = 'S01-HCOR2'
		self.correctorStepSize = corrStep
		self.corrector1Min, self.corrector1Max = corr1Range
		self.corrector2Min, self.corrector2Max = corr2Range
		self.linacLowerAmp = ampLower
		self.linacUpperAmp = ampUpper
		self.nSamples = nSamples
		self.bpms = [partial(self.machine.getBPMPosition, 'S01-BPM01'), partial(self.machine.getBPMPosition, 'S02-BPM01'), partial(self.machine.getBPMPosition, 'S02-BPM02')]
		self.findRFCentre()

	def linac1ScanBLM(self, actuator, ampLower, ampUpper, nSamples):
		"""
			This function will perform the BLM linac fit. 2 Correctors are defined for X and Y (4 total!)
			The BPM readings are the X and Y values of the first 2 BPMs in S02.
			The camera readings for S02-YAG-03 needed to be added.
			The values of the 2 linac settings and the number of bpm samples are also defined.
		"""
		self.corrector1X = 'S01-HCOR1'
		self.corrector1Y = 'S01-VCOR1'
		self.corrector2X = 'S01-HCOR2'
		self.corrector2Y = 'S01-VCOR2'
		self.linacLowerAmp = ampLower
		self.linacUpperAmp = ampUpper
		self.nSamples = nSamples
		self.bpms = [partial(self.machine.getBPMPosition, 'S02-BPM01', plane='X'), partial(self.machine.getBPMPosition, 'S02-BPM01', plane='Y')\
					 partial(self.machine.getBPMPosition, 'S02-BPM02', plane='X'), partial(self.machine.getBPMPosition, 'S02-BPM02', plane='Y')]
		self.findRFCentreBLM()

	def printFinalValue(self):
		print self.main+' '+self.sub+' fit = '+str(self.experimentalData[self.main]['calibrationPhase'])
		self.logger.emit(self.main+' '+self.sub+' fit = '+str(self.experimentalData[self.main]['calibrationPhase']))

	def printFinalDip(self):
		print self.main+' '+self.sub+' fit = '+str(self.experimentalData[self.main]['calibrationDip'])
		self.logger.emit(self.main+' '+self.sub+' fit = '+str(self.experimentalData[self.main]['calibrationDip']))

	def resetDataArray(self):
		self.experimentalData.resetData(self.main, self.sub, ['x', 'y', 'z'])

	def setDataArray(self, x, y, z):
		self.experimentalData[self.main][self.sub]['x'].append(x)
		self.experimentalData[self.main][self.sub]['y'].append(y)
		self.experimentalData[self.main][self.sub]['z'].append(z)
		self.newData.emit()

	def getDataArray(self, column=None, zipped=True, sortKey=None):
		if column is not None:
			return self.experimentalData[self.main][self.sub][column]
		else:
			data = [self.experimentalData[self.main][self.sub]['x'],
				self.experimentalData[self.main][self.sub]['y'],
				self.experimentalData[self.main][self.sub]['z']]
			if sortKey is not None:
				data = zip(*sorted(zip(*data), key=sortKey))
			if zipped:
				return zip(*data)
			else:
				return data

	def setFinalCorr(self, corr, I):
		self.experimentalData[self.main]['calibrationCorr1'] = I
		self.machine.set('setCorr', corr, I)

	def getData(self):
		self.data = []
		while len(self.data) < 2:
			self.data.append(self.getDataFunction())
			time.sleep(self.sleepTime)
		self.data = []
		while len(self.data) < self.nSamples:
			self.data.append(self.getDataFunction())
			time.sleep(self.sleepTime)
		## This returns means in the form [bpm1, bpm2, bpm3...]
		return np.array([np.mean(a) if np.std(a) > 0.01 else 20 for a in zip(*self.data)])

########### findRFCentreBLM ###############

	def findRFCentreBLM(self):
		"""
			The suggested solution (from BLM) is to scan c1 at five points in x/y at
			[[0,0], [-1,0], [1,0], [0, -1], [0,1]]
			at two energies and then solve for the zero point in x/y corrector space.
			Repeat for c2.

			Data is stored in self.experimentalData[self.main][self.sub]

			I haven't figured out how to do the fit yet...
		"""
		self.resetDataArray()
		cx = self.corrector1X
		cy = self.corrector1Y
		self.doBMLScan(cx, cy, 1)
		self.saveLinacDataBLM(corr=1)

		cx = self.corrector2X
		cy = self.corrector2Y
		self.doBMLScan(cx, cy, 2)

	def doBMLScan(self, corrx, corry, no=1):
		self.resetDataArray()
		self.machine.setLinac1Amplitude(self.linacLowerAmp)
		self.main = 'Corr1'
		self.sub = 'Low'
		for c1x, c1y in [[0,0], [-1,0], [1,0], [0, -1], [0,1]]:
			self.machine.setCorr(corrx, c1x)
			self.machine.setCorr(corry, c1y)
			time.sleep(self.sleepTime)
			data = self.getData()
			self.setDataArray(c1x, c1y, data)
		self.saveLinacDataBLM(corr=no)

		self.resetDataArray()
		self.machine.setLinac1Amplitude(self.linacUpperAmp)
		self.main = 'Corr1'
		self.sub = 'High'
		for c1x, c1y in [[0,0], [-1,0], [1,0], [0, -1], [0,1]]:
			self.machine.setCorr(corrx, c1x)
			self.machine.setCorr(corry, c1y)
			time.sleep(self.sleepTime)
			data = self.getData()
			self.setDataArray(c1x, c1y, data)
		self.saveLinacDataBLM(corr=no)

	def saveLinacDataBLM(self, corr=1):
		self.timestr = time.strftime("%Y%m%d-%H%M%S")
		c1, c2, bpms = self.getDataArray(zipped=False)
		rawData = np.array(zip(c1, c2, *zip(*bpms)))
		labels = ['BPM'+str(i+1) for i in range(len(bpms[1]))]
		df = pd.DataFrame(rawData)
		df.columns = ['cx', 'cy'] + labels
		df.to_csv(self.timestr+'_'+self.main+'_'+self.sub+'_'+str(self.linacLowerAmp)+'_'+str(self.linacUpperAmp)+'_Corr_'+str(corr)+'_rawData.csv', index=0)

########### findRFCentre ###############

	def findRFCentre(self):
		"""
			This function will scan corrector 1 (c1) to minimise the average difference between the BPM readings
			at high and low amplitude of the linac RF. This is simply the mean value of the differences.
			Once found for c1, it does the same for corrector 2 (c2).
			Currently this function only works in one plane at a time.

			Data is stored in self.experimentalData[self.main][self.sub]
		"""
		self.resetDataArray()
		for c1 in np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize):
			self.machine.setCorr(self.corrector1, c1)
			self.machine.setCorr(self.corrector2, 0)
			self.machine.setLinac1Amplitude(self.linacLowerAmp)
			time.sleep(self.sleepTime)
			dataLow = self.getData()
			self.machine.setLinac1Amplitude(self.linacUpperAmp)
			time.sleep(self.sleepTime)
			dataHigh = self.getData()
			self.setDataArray(c1, 0, dataLow - dataHigh)
		c1Min = self.findC1Min()
		print 'c1Min = ', c1Min
		self.resetDataArray()
		for c2 in np.arange(self.corrector2Min, self.corrector2Max+self.correctorStepSize, self.correctorStepSize):
			self.machine.setCorr(self.corrector1, c1Min)
			self.machine.setCorr(self.corrector2, c2)
			self.machine.setLinac1Amplitude(self.linacLowerAmp)
			time.sleep(self.sleepTime)
			dataLow = self.getData()
			self.machine.setLinac1Amplitude(self.linacUpperAmp)
			time.sleep(self.sleepTime)
			dataHigh = self.getData()
			self.setDataArray(c1Min, c2, dataLow - dataHigh)
		c2Min = self.findC2Min()
		print 'c2Min = ', c2Min
		self.machine.setCorr(self.corrector1, c1Min)
		self.machine.setCorr(self.corrector2, c2Min)

	def findC1Min(self):
		self.timestr = time.strftime("%Y%m%d-%H%M%S")
		c1, c2, bpms = self.getDataArray(zipped=False)
		# This is the mean of the BPMs for each value of corrector
		BPMMean = [np.mean(b) for b in bpms]
		index = BPMMean.index(min(BPMMean))
		self.saveLinacData(1)
		return c1[index]

	def findC2Min(self):
		c1, c2, bpms = self.getDataArray(zipped=False)
		# This is the mean of the BPMs for each value of corrector
		BPMMean = [np.mean(b) for b in bpms]
		index = BPMMean.index(min(BPMMean))
		self.saveLinacData(2)
		return c2[index]

	def saveLinacData(self, corr=1):
		self.timestr = time.strftime("%Y%m%d-%H%M%S")
		c1, c2, bpms = self.getDataArray(zipped=False)
		rawData = np.array(zip(c1, c2, *zip(*bpms)))
		labels = ['BPM'+str(i+1) for i in range(len(bpms[1]))]
		df = pd.DataFrame(rawData)
		df.columns = ['c1', 'c2'] + labels
		df.to_csv(self.timestr+'_'+self.main+'_'+self.plane+'_'+str(self.linacLowerAmp)+'_'+str(self.linacUpperAmp)+'_Corr_'+str(corr)+'_rawData.csv', index=0)

########### findSOLCentre ###############

	def findSOLCentre(self):
		self.timestr = time.strftime("%Y%m%d-%H%M%S")
		with open(self.timestr+'_'+self.main+'_'+self.plane+'_'+str(self.solLowerAmp)+'A_'+str(self.solUpperAmp)+'A_rawData_log.csv', 'w') as logfile:
			self.resetDataArray()
			self.data1 = {}
			self.data2 = {}
			self.rawData = {'x':[], 'y': [], 'z1':[], 'z2': []}
			self.machine.setSol(self.main, self.solLowerAmp)
			while abs(self.machine.getSol(self.main) - self.solLowerAmp) > 0.2:
				time.sleep(0.1)
			flip = -1
			for c1 in np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize):
				self.machine.setCorr(self.corrector1, c1)
				self.data1[c1] = {}
				flip = -1*flip
				for c2 in np.arange(flip*self.corrector2Min, flip*(self.corrector2Max+self.correctorStepSize), flip*self.correctorStepSize):
					self.machine.setCorr(self.corrector2, c2)
					while abs(self.machine.getCorr(self.corrector1) - c1) > 0.05 or abs(self.machine.getCorr(self.corrector2) - c2) > 0.05:
						# print self.machine.get('getCorr', self.corrector1) , c1, self.machine.get('getCorr', self.corrector2) , c2
						time.sleep(0.1)
					if self._abort:
						self._abort = False
						return 0
					print 'sol = ', self.solLowerAmp, '  c1 = ', c1, '  c2 = ', c2
					data1 = self.getData()
					logfile.write('data1,'+str(self.solLowerAmp)+','+str(c1)+','+str(c2)+','+str(data1))
					self.data1[c1][c2] = data1

			self.machine.setSol(self.main, self.solUpperAmp)
			while abs(self.machine.getSol(self.main) - self.solUpperAmp) > 0.2:
				time.sleep(0.1)
			flip = -1
			for c1 in np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize):
				self.machine.setCorr(self.corrector1, c1)
				self.data2[c1] = {}
				flip = -1*flip
				for c2 in np.arange(flip*self.corrector2Min, flip*(self.corrector2Max+self.correctorStepSize), flip*self.correctorStepSize):
					self.machine.setCorr(self.corrector2, c2)
					while abs(self.machine.getCorr(self.corrector1) - c1) > 0.05 or abs(self.machine.getCorr(self.corrector2) - c2) > 0.05:
						time.sleep(0.1)
					print 'sol = ', self.solUpperAmp, '  c1 = ', c1, '  c2 = ', c2
					data2 = self.getData()
					logfile.write('data2,'+str(self.solLowerAmp)+','+str(c1)+','+str(c2)+','+str(data2))
					self.data2[c1][c2] = data2

			self.machine.set('setSol', self.main, 0)
			while abs(self.machine.getSol(self.main) - 0) > 0.2:
				time.sleep(0.1)

			flip = -1
			for c1 in np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize):
				flip = -1*flip
				for c2 in np.arange(flip*self.corrector2Min, flip*(self.corrector2Max+self.correctorStepSize), flip*self.correctorStepSize):
					self.rawData['x'].append(c1)
					self.rawData['y'].append(c2)
					data1 = self.data1[c1][c2]
					data2 = self.data2[c1][c2]
					self.rawData['z1'].append(data1)
					self.rawData['z2'].append(data2)
					diff = np.mean(np.array([abs(a[1] - a[0]) if a[0] < 20 and a[1] < 20 else 20 for a in zip(data1,data2)]))
					logfile.write('diff,'+str(self.solLowerAmp)+','+str(c1)+','+str(c2)+','+str(data1)+','+str(data2)+','+str(diff))
					self.setDataArray(c1, c2, diff)
		self.saveSOLData()
		# self.doFitRFCentre()

	def saveSOLData(self):
		# my_dict = {}
		# for name in ['x', 'y', 'z1','z2']:
		# 	my_dict[name] = self.rawData[name]
		# with open(self.main+'_'+self.sub+'_rawData.csv', 'wb') as f:  # Just use 'w' mode in 3.x
		# 	w = csv.DictWriter(f, my_dict.keys())
		# 	w.writeheader()
		# 	w.writerow(my_dict)
		df = pd.DataFrame(self.rawData)
		df.columns = ['x', 'y', 'z1','z2']
		df.to_csv(self.timestr+'_'+self.main+'_'+self.plane+'_'+str(self.solLowerAmp)+'A_'+str(self.solUpperAmp)+'A_rawData.csv', index=0)

	def cutDataRFCentre(self):
		"""Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
		allData = self.getDataArray()
		max_charge = max(self.getDataArray('yData'))

		cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 10 and a[2] < 2]
		return cutData

	def doFitRFCentre(self):
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
