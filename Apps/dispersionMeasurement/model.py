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
SPEED_OF_LIGHT = physics.constants.c / 1e6

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
	sleepTimeFine = 0.001

	def __init__(self, machineType='Physical', lineType='CLARA', gunType='10Hz'):
		super(Model, self).__init__()
		self.baseMachine = machine.Machine(machineType, lineType, gunType, controllers=['magnets', 'bpms', 'linac1llrf'])
		self.machine = self.baseMachine#machineSetter(self.baseMachine)
		self.machineType = machineType
		self.lineType = lineType
		self.gunType = gunType
		self.newData = emitter()
		self.logger = emitter()
		self.progress = emitter()
		if not self.machineType == 'None':
			self.sleepTime = 0.1
			self.sleepTimeDipole = 0.25
			self.sleepTimeFine = 0.1
		self.crestingData = dataArray()
		self.data = []
		print("Model Initialized")


	def measureDispersion(self, nSamples=4, start=12000, end=13000, stepSize=200, BA1=False):
		self.bpms = ['INJ-BPM04', 'INJ-BPM05']
		if BA1:
			self.bpms = self.bpms + ['BA1-BPM01', 'BA1-BPM02', 'BA1-BPM03', 'BA1-BPM04']
		self.actuator = 'dispersion'
		self.stepSize = stepSize
		self.nSamples = nSamples
		self.startSET = start
		self.endSET = end
		self.dataFunction = [partial(self.machine.getBPMPosition, bpm, plane='X') for bpm in self.bpms]
		return self.doDispersionMeasurement()#

	def getDataFunction(self):
		return [b() for b in self.dataFunction]

	def getData(self):
		time.sleep(self.sleepTime)
		self.data = []
		while len(self.data) < self.nSamples:
			self.data.append(self.getDataFunction())
			time.sleep(self.sleepTime)
		print self.data
		self.data = zip(*self.data)
		self.data = [np.mean([a for a in b if not np.isnan(a)]) for b in self.data]
		return self.data

	def fitting_equation(self, x, a, b, c):
		return a + b * x + c * x**2

	def doDispersionMeasurement(self):
		print 'Starting measurement'
		self.currentData = []
		range = np.arange(self.startSET, self.endSET + self.stepSize, self.stepSize)
		for i, set in enumerate(range):
			self.machine.setLinac1Amplitude(set)
			time.sleep(1)
			data = self.getData()
			print 'SET = ', set, ' x = ', data
			if not any([np.isnan(a) for a in data]):
				dataarray = [set]
				dataarray = dataarray + data
				self.currentData.append(dataarray)
		self.machine.setLinac1Amplitude(13000)
		self.currentData = np.array(self.currentData)
		self.fits = {}
		fits = []
		for i,b in enumerate(self.bpms):
			self.fits[b] = {}
			x = self.currentData[:,0]
			y = self.currentData[:, i+1]
			xy = zip(x,y)
			xy = [a for a in xy if not np.isnan(a[1])]
			x,y = zip(*xy)
			self.fits[b]['data'] = [x,y]
			self.fits[b]['fit'] = self.do_fit(x,y)
		return self.currentData, self.fits

	def do_fit(self, x, y):
		popt, pcov = curve_fit(self.fitting_equation, x, y)
		return popt
