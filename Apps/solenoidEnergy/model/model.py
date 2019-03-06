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
    sleepTimeCORR = 0.001
    sleepTimeFine = 0.001

    def __init__(self, machineType, lineType, gunType, verbose=True):
        super(Model, self).__init__()
        self.baseMachine = machine.Machine(machineType, lineType, gunType, controllers=['magnets', 'bpms'])
        self._abort = False
        self.verbose = verbose
        self.machine = machineSetter(self.baseMachine)
        self.machineType = machineType
        self.lineType = lineType
        self.gunType = gunType
        self.logger = emitter()
        self.progress = emitter()
        self.newData = emitter()
        if not self.machineType == 'None':
            self.sleepTime = 0.1
            self.sleepTimeDipole = 0.25
            self.sleepTimeFine = 0.1
        # self.crestingData = dataArray()
        self.parameters = {'energy_BPM': 'S02-BPM01'}
        self.clearDataArray()
        print("Model Initialized")

    def clearDataArray(self):
        self.solenoidData = dataArray()

    def abort(self):
        self._abort = True

    def finish(self):
        self._finished = True

    def resetAbortFinish(self):
        self._abort = False
        self._finished = False

    def loadGunBURT(self):
        self.logger.emit('Loading DBURT: GunCrest.dburt')
        if self.machineType == 'None':
            time.sleep(1)
            return False
        else:
            return self.machine.applyDBURT('GunCrest.dburt')

    def bpmSol1Scan(self, *args, **kwargs):
        self.bpmSol1Negative(*args, **kwargs)
        self.bpmSol1Positive(*args, **kwargs)
        if self.machineType == 'None':
            self.load_data_file()
        self.calculate_Momentum()

    def bpmSol1Negative(self, *args, **kwargs):
        self.polarity = 'negative'
        self.bpmSol1(solenoid1I=kwargs['solenoid1Inegative'], solenoid2I=kwargs['solenoid2Inegative'], *args, **kwargs)
        self.calculate_Momentum()

    def bpmSol1Positive(self, *args, **kwargs):
        self.polarity = 'positive'
        self.bpmSol1(solenoid1I=kwargs['solenoid1Ipositive'], solenoid2I=kwargs['solenoid2Ipositive'], *args, **kwargs)
        self.calculate_Momentum()

    def bpmSol1(self, startx=0, rangex=1, starty=0, rangey=1, steps=11, solenoid1I=50, solenoid2I=50, sensor='BPM', sensorName='S02-BPM01', **kwargs):
        self.resetAbortFinish()
        self.sensor = sensor
        self.sensorName = sensorName
        self.actuator = 'S01-HCOR2'
        self.solenoid1 = 'L01-SOL1'
        self.solenoid2 = 'L01-SOL2'
        self.solenoid1I = solenoid1I
        self.solenoid2I = solenoid2I
        self.range = rangex
        self.nSteps = steps
        self.startI = startx
        self.nSamples = 10
        self.getDataFunction = [partial(self.machine.getBPMPosition, self.parameters['energy_BPM'], plane='X'), partial(self.machine.getBPMPosition, self.parameters['energy_BPM'], plane='Y')]
        self.bpmSolEnergy()
        self.actuator = 'S01-VCOR2'
        self.range = rangey
        self.nSteps = steps
        self.startI = starty
        self.bpmSolEnergy()

    def resetDataArray(self, sensorName, polarity, actuator):
        self.solenoidData.resetData(sensorName, polarity, actuator, ['energy', 'xData', 'yData', 'yStd', 'xStd', 'I'])

    def appendDataArray(self, I, x, y, xStd, yStd, sensor, sensorName, polarity, actuator):
        self.solenoidData[sensorName][polarity][actuator]['I'].append(I)
        self.solenoidData[sensorName][polarity][actuator]['xData'].append(x)
        self.solenoidData[sensorName][polarity][actuator]['yData'].append(y)
        self.solenoidData[sensorName][polarity][actuator]['xStd'].append(yStd)
        self.solenoidData[sensorName][polarity][actuator]['yStd'].append(yStd)
        self.newData.emit(str(sensor), str(polarity), str(actuator), self.solenoidData[sensorName][polarity][actuator])

    def getData(self):
        if not self.machineType == 'None':
            time.sleep(self.sleepTime)
        self.data = []
        while len(self.data) < self.nSamples:
            if isinstance(self.getDataFunction, (list, tuple)):
                data = [f() for f in self.getDataFunction]
                self.data.append(data)
            else:
                self.data.append(self.getDataFunction())
            if not self.machineType == 'None':
                time.sleep(self.sleepTime)
        if isinstance(self.getDataFunction, (list, tuple)):
            data = zip(*self.data)
            data2 = [[a for a in d if not np.isnan(a)] for d in data]
            data3 = [[np.mean(d), np.std(d)] if np.std(d) > 0.001 else [float('nan'),0] for d in data2]
            # print 'data3 = ', zip(*data3)
            return zip(*data3)
        else:
            self.data = [a for a in self.data if not np.isnan(a)]
            return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [float('nan'),0]

    def rotate_list(self, l, n):
        return l[n:] + l[:n]

########### bpmSolEnergy ###############

    def bpmSolEnergy(self):
        self.resetDataArray(self.sensorName, self.polarity, self.actuator)
        self.solenoidData[self.sensorName][self.polarity]['value1'] = self.solenoid1I
        self.solenoidData[self.sensorName][self.polarity]['value2'] = self.solenoid2I
        print 'Setting ', self.solenoid1, ' to ', self.solenoid1I,'A'
        print 'Setting ', self.solenoid2, ' to ', self.solenoid2I,'A'
        self.machine.setSol(self.solenoid1, self.solenoid1I)
        self.machine.setSol(self.solenoid2, self.solenoid2I)
        self.solenoidData[self.sensorName][self.actuator] = {}
        self.solenoidData[self.sensorName][self.actuator]['startI'] = self.startI
        self.solenoidData[self.sensorName][self.actuator]['range'] = self.range
        self.solenoidData[self.sensorName][self.actuator]['nSteps'] = self.nSteps
        range = np.arange(self.startI - self.range, self.startI + self.range + 1e-6, 2*self.range / self.nSteps)
        for i,I in enumerate(range):
            I = np.round(I, decimals=3)
            self.progress.emit(100*i/len(range))
            if self._abort or self._finished:
                return
            print self.actuator, ' = ', I
            # time.sleep(0.1)
            self.machine.setCorr(self.actuator, I)
            if i == 0 and not self.machineType == 'None':
                time.sleep(1)
            data, stddata = self.getData()
            x,y = data
            stdx, stdy = stddata
            self.appendDataArray(I, x, y, stdx, stdy, self.sensor, self.sensorName, self.polarity, self.actuator)
        self.machine.setCorr(self.actuator, self.startI)
        self.progress.emit(100)

    def calculate_theta(self, x, y):
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        return np.arctan(slope)

    def calculate_B(self, I1, I2):
        return 0.00012171419 + 0.00037651102 * I1 + 0.00012171419 + 0.00037651102 * I2

    def calculate_p(self, I1, I2, theta):
        return constants.c * self.calculate_B(I1, I2) / (2.0 * theta) / 1e6

    def fit_data(self, I1, I2, x, y):
        theta = self.calculate_theta(x,y)
        return self.calculate_p(I1, I2, theta)

    def calculate_Momentum(self):
        energies = []
        data = self.solenoidData[self.sensorName]
        if 'positive' in data and len(data['positive']['S01-VCOR2']['yData']) > 1:
            p1 = self.fit_data(data['positive']['value1'], data['positive']['value2'], data['positive']['S01-VCOR2']['yData'], data['positive']['S01-VCOR2']['xData'])
            p2 = -1*self.fit_data(data['positive']['value1'],data['positive']['value2'], data['positive']['S01-HCOR2']['xData'], data['positive']['S01-HCOR2']['yData'])
            data['positive']['energy'] = np.mean([p1, p2])
            energies.append(p1)
            energies.append(p2)
        if 'negative' in data and len(data['negative']['S01-VCOR2']['yData']) > 1:
            n1 = self.fit_data(data['negative']['value1'], data['negative']['value2'], data['negative']['S01-VCOR2']['yData'], data['negative']['S01-VCOR2']['xData'])
            n2 = -1*self.fit_data(data['negative']['value1'], data['negative']['value2'], data['negative']['S01-HCOR2']['xData'], data['negative']['S01-HCOR2']['yData'])
            data['negative']['energy'] = np.mean([n1, n2])
            energies.append(n1)
            energies.append(n2)
        return np.mean(energies)

################################# LOAD DATA ##############################
    def load_data_file(self):
        self.solenoidData = h5dict.load_dict_from_hdf5(r"C:\Users\jkj62\Documents\GitHub\Software\Apps\solenoidEnergy\124620_SolenoidEnergyScan.h5")
        self.solenoidData = dataArray(self.solenoidData)
        print self.calculate_Momentum()
