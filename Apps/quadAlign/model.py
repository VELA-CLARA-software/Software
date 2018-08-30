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
		self.baseMachine = machine.Machine(machineType, lineType, gunType, controllers=['magnets', 'bpms'])
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


	def quadAligner(self, quad, bpm, stepSize=1, nSamples=4, start=0, end=10, momentum=35):
		self.quad = quad#'S02-QUAD'+str(no)
        self.bpm = bpm
		self.momentum = momentum
		self.quadLength = self.machine.magnets.getMagneticLength(self.quad)/1000.0
		bpmpos = self.machine.bpms.getPosition(self.bpm)
		quadpos = self.machine.magnets.getPosition(self.quad)
		self.driftLength = bpmpos-quadpos
		# print bpmpos, quadpos, self.driftLength
		self.actuator = 'alignment'
		self.stepSize = stepSize
		self.nSamples = nSamples
		self.startI = start
		self.endI = end
		self.dataFunction = [partial(self.machine.getBPMPosition, self.bpm),partial(self.machine.getBPMPosition, self.bpm, plane='Y')]
		return self.doQuadAlignment()#

	def getDataFunction(self):
		return [b() for b in self.dataFunction]

	def getData(self):
		time.sleep(self.sleepTime)
		self.data = []
		while len(self.data) < self.nSamples:
			self.data.append(self.getDataFunction())
			time.sleep(self.sleepTime)
		self.data = zip(*self.data)
		self.data = [np.mean([a for a in b if not np.isnan(a)]) for b in self.data]
		return self.data

	def getK(self, magnetname, momentum):
		current = self.machine.getQuad(magnetname)
		magnet = self.machine.magnets.getMagObjConstRef(magnetname)
		sign = np.copysign(1, current)
		coeffs = np.append(magnet.fieldIntegralCoefficients[:-1] * sign, magnet.fieldIntegralCoefficients[-1])
		int_strength = np.polyval(coeffs, abs(current))
		effect = SPEED_OF_LIGHT * int_strength / momentum
		k = 1000 * effect / magnet.magneticLength  # focusing term K
		return k

	def fitting_equation(self, x, a, b):
		return a + b * x

	def doQuadAlignment(self):
		print 'Starting quadrupole ', self.quad
		self.currentData = []
		range = np.arange(self.startI, self.endI + self.stepSize, self.stepSize)
		for i, current in enumerate(range):
			self.machine.setQuad(self.quad, current)
			time.sleep(0.5)
			data = self.getData()
			k = self.getK(self.quad, self.momentum)
			print 'I = ', current, ' k = ', k, ' xy = ', data
			self.currentData.append([k, data[0], data[1]])
		self.machine.setQuad(self.quad, 0)
		k, x, y = [np.array(a) for a in zip(*self.currentData)]
		fitx = self.do_fit(k, x/1000.)
		fity = self.do_fit(k, y/1000.)
		offsetx = fitx / (self.driftLength * self.quadLength)
		offsety = fity / (self.driftLength * self.quadLength)
		print 'Quadrupole ', self.quad, ': dx = ', 1000.*offsetx, 'mm   dy=', 1000.*offsety,'mm'
		return [self.quad, 1000.*offsetx, 1000.*offsety]

	def do_fit(self, x, y):
		popt, pcov = curve_fit(self.fitting_equation, x, y)
		return popt[1]
