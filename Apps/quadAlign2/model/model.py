import sys,os
import time
from functools import partial
sys.path.append("../../../")
import Software.Procedures.Machine.machine as machine
import numpy as np
from scipy import stats
from scipy import constants
import Software.Utils.dict_to_h5 as h5dict

class dataArray(dict):

    def __init__(self, *args, **kwargs):
        super(dataArray, self).__init__(*args, **kwargs)

    def checkDataArray(self, sensorName, polarity, actuator, type):
        sensor = str(sensorName)
        polarity = str(polarity)
        actuator = str(actuator)
        type = str(type)
        if not sensor in self:
            self[sensor] = {}
        if not polarity in self[sensor]:
            self[sensor][polarity] = {}
        if not actuator in self[sensor][polarity]:
            self[sensor][polarity][actuator] = {}
        if not type in self[sensor][polarity][actuator]:
            self[sensor][polarity][actuator][type] = []

    def resetData(self, sensorName, polarity, actuator, type):
        sensor = str(sensorName)
        polarity = str(polarity)
        actuator = str(actuator)
        for t in type:
            self.checkDataArray(sensor, polarity, actuator, t)
            # self[sensor][polarity][actuator][t] = []

    def setData(self, sensorName, polarity, actuator, type, data):
        sensor = str(sensorName)
        polarity = str(polarity)
        actuator = str(actuator)
        for t, d in zip(type, data):
            t = str(t)
            self.checkDataArray(sensor, polarity, actuator, t)
            self[sensor][polarity][actuator][t] = d

    def appendData(self, sensorName, polarity, actuator, type, data):
        sensor = str(sensorName)
        polarity = str(polarity)
        actuator = str(actuator)
        for t, d in zip(type, data):
            t = str(t)
            self.checkDataArray(sensor, polarity, actuator, t)
            self[sensor][polarity][actuator][t].append(d)

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

    def __getattr__(self, attr):
        return getattr(self.machine, attr)

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

    def abort(self):
        self._abort = True

    def finish(self):
        self._finished = True

    def resetAbortFinish(self):
        self._abort = False
        self._finished = False

    def resetDataArray(self, sensorName, polarity, actuator):
        self.solenoidData.resetData(sensorName, polarity, actuator, ['energy', 'xData', 'yData', 'yStd', 'xStd', 'I'])

    def appendDataArray(self, I, x, y, xStd, yStd, sensor, sensorName, polarity, actuator):
        self.solenoidData[sensorName][polarity][actuator]['I'].append(I)
        self.solenoidData[sensorName][polarity][actuator]['xData'].append(x)
        self.solenoidData[sensorName][polarity][actuator]['yData'].append(y)
        self.solenoidData[sensorName][polarity][actuator]['xStd'].append(yStd)
        self.solenoidData[sensorName][polarity][actuator]['yStd'].append(yStd)
        self.newData.emit(str(sensor), str(polarity), str(actuator), self.solenoidData[sensorName][polarity][actuator])

    def quadAligner(self, quad, bpm, stepSize=1, nSamples=4, start=0, end=10, momentum=35):
        self.resetAbortFinish()
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
            if not any([np.isnan(a) for a in data]):
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
