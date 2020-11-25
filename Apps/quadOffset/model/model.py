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
import pandas as pd
from collections import OrderedDict

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

	def __init__(self, machineType, lineType, gunType, verbose=False):
		super(Model, self).__init__()
		self.baseMachine = machine.Machine(machineType, lineType, gunType)
		self._abort = False
		self.verbose = verbose
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
		self.parameters = self.baseMachine.initilise_parameters()
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

	def getDataFunction(self):
		return [b() for b in self.bpms]

	def degaussQuads(self):
		quads = ['S02-QUAD01', 'S02-QUAD02', 'S02-QUAD03', 'S02-QUAD04', 'S02-QUAD05']
		self.machine.setDegaussMagnet(quads, degaussToZero=True)
		while self.machine.isMagnetDegaussing(quads):
			time.sleep(0.1)

	def turnOffQuadsCorrs(self):
		quads = ['S02-QUAD01', 'S02-QUAD02', 'S02-QUAD03', 'S02-QUAD04', 'S02-QUAD05']
		hcorrs = self.machine.magnets.getHCorNames()
		hcorrs = [a for a in hcorrs if 'S02' in a]
		vcorrs = self.machine.magnets.getVCorNames()
		vcorrs = [a for a in vcorrs if 'S02' in a]
		self.machine.magnets.switchOFFpsu(quads+hcorrs+vcorrs)

	def quadScan(self, main, lower, upper, step, nSamples):
		self.main = main
		# self.position = self.machine.magnets.getMagObjConstRef(self.main).position
		self.sub = 'experimental'
		self.stepSize = step
		self.lowerAmp = lower
		self.upperAmp = upper
		self.nSamples = nSamples
		self.bpms = [partial(self.machine.getBPMPosition, 'S02-BPM01', 'X'), partial(self.machine.getBPMPosition, 'S02-BPM01', 'Y'), \
					 partial(self.machine.getBPMPosition, 'S02-BPM02', 'X'), partial(self.machine.getBPMPosition, 'S02-BPM02', 'Y')]
		# self.bpmPos = [self.machine.bpms.getBPMDataObject(bpm).position for bpm in ['S02-BPM01','S02-BPM02']]
		self.findQuadOffset()

	def resetDataArray(self):
		self.experimentalData.resetData(self.main, self.sub, ['x', 'y', 'z'])

	def setDataArray(self, x, y, z=[]):
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

########### findQuadOffset ###############

	def findQuadOffset(self):
		self.timestr = time.strftime("%Y%m%d-%H%M%S")
		with open(self.timestr+'_QuadOffsets_'+self.main+'_'+str(self.lowerAmp)+'A_'+str(self.upperAmp)+'A_rawData_log.csv', 'w') as logfile:
			self.resetDataArray()
			self.machine.setQuad(self.main, 0.0)
			data1 = self.getData()
			self.logger.emit(self.main+' = '+ str(0) + ' BPMs = '+str(data1))
			logfile.write(str(0))
			for d in data1:
				logfile.write(','+str(d))
			logfile.write('\n')
			self.setDataArray(0, data1)

			self.machine.setQuad(self.main, self.lowerAmp)
			while abs(self.machine.getQuad(self.main) - self.lowerAmp) > 0.2:
				print 'wait'
				time.sleep(self.sleepTime)
			for amp in np.arange(self.lowerAmp, self.upperAmp+self.stepSize, self.stepSize):
				self.machine.setQuad(self.main, amp)
				if self._abort:
					self._abort = False
					return 0
				data1 = self.getData()
				self.logger.emit(self.main+' = '+ str(amp) + ' BPMs = '+str(data1))
				logfile.write(str(amp))
				for d in data1:
					logfile.write(','+str(d))
				logfile.write('\n')
				self.setDataArray(amp, data1)
		if self.verbose:
			self.saveQuadData()
		# self.doFitRFCentre()

	def saveQuadData(self):
		df = pd.DataFrame(self.rawData)
		df.columns = ['x', 'y', 'z1','z2']
		df.to_csv(self.timestr+'_QuadOffsets_'+self.main+'_'+self.plane+'_'+str(self.solLowerAmp)+'A_'+str(self.solUpperAmp)+'A_rawData.csv', index=0)

	def cutDataRFCentre(self):
		"""Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
		allData = self.getDataArray()
		max_charge = max(self.getDataArray('yData'))

		cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 10 and a[2] < 2]
		return cutData

	def doFitQuadOffset(self):
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
