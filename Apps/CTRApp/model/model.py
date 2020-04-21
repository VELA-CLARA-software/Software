import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import random as r
from functools import partial
sys.path.append("../../../")
from Software.Utils.dict_to_h5 import *
import Software.Procedures.Machine.machine as machine
degree = physics.pi/180.0

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

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
            self.sleepTimeFine = 0.1
        self.dataArray = dataArray()
        self.parameters = self.baseMachine.initilise_parameters()
        self.data = []
        self.getDataFunction = {}
        self.calibrationPhase = {'CTR': None, 'delE': None}
        self.settings = {'Gun_Amp_Set': 71000, 'Linac1_Amp_Set': 41000}
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

    def CTR_Scan(self, startPhase=-20, endPhase=20, stepPhase=2, nShots=10, gunCrest=0, linacCrest=0, correctRFAmplitude=True, bpmtarget=0, linacstep=50, maxRF=40000):
        self.resetAbortFinish()
        self.source = 'CTR'
        self.cavity = 'Linac1'
        self.startPhase = startPhase if endPhase >= startPhase else endPhase
        self.endPhase = endPhase if endPhase >= startPhase else startPhase
        self.stepPhase = stepPhase if stepPhase < abs(endPhase - startPhase) and abs(endPhase - startPhase) > 0 else abs(endPhase - startPhase)/3.0 if abs(endPhase - startPhase) > 0 else 0
        self.nShots = nShots
        self.calibrationPhase['Gun'] = gunCrest
        self.calibrationPhase['Linac1'] = linacCrest
        self.getDataFunction = {}
        self.getDataFunction['setpoint'] = partial(self.machine.getLinac1Amplitude)
        self.getDataFunction['bpmpos'] = partial(self.machine.getBPMPosition, 'C2V-BPM01')
        self.getDataFunction['ctrsignal'] = partial(self.machine.getCTRSignal)
        self.getDataFunction['wcmq'] = partial(self.machine.getWCMCharge, self.parameters['scope'])
        self.correctRFAmplitude = correctRFAmplitude
        if self.correctRFAmplitude:
            self.getCorrectDataFunction = partial(self.machine.getBPMPosition, 'C2V-BPM01')
            self.getCorrectDataTarget = bpmtarget
            self.getCorrectDataStep = linacstep
            self.maxRF = maxRF
        self.do_CTR_Scan()

    def Correct_Momentum(self, bpmtarget=0, linacstep=50, maxRF=40000):
        self.resetAbortFinish()
        self.source = 'CTR'
        self.cavity = 'Linac1'
        self.getCorrectDataFunction = partial(self.machine.getBPMPosition, 'C2V-BPM01')
        self.getCorrectDataTarget = bpmtarget
        self.getCorrectDataStep = linacstep
        self.maxRF = maxRF
        self.correctBPMUsingRFAmplitude(step=self.getCorrectDataStep, target=self.getCorrectDataTarget)

    def saveData(self, source=None, type=None, savetoworkfolder=True):
        # print('###  SAVING DATA  ###')
        if not self.machineType == 'aNone':
            if source is not None and not isinstance(source, (tuple, list)):
                source = [source]
            elif source is None:
                source = ['CTR']
            if type is not None and not isinstance(type, (tuple, list)):
                type = [type]
            elif type is None:
                type = self.getDataFunction.keys()
            timestr = time.strftime("%H%M%S")
            if not self.machineType == 'None':
                dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\' if savetoworkfolder else './'
            else:
                dir = './'
            try:
                os.makedirs(dir)
            except OSError:
                if not os.path.isdir(dir):
                    self.logger.emit('Error creating directory - saving to local directory')
                    dir = './'
            # print('###  SAVING DATA  ###   dir = ', dir)
            for s in source:
                mydata = {}
                if s in self.dataArray:
                    mydata[s] = {}
                    for t in type:
                        if t in self.dataArray[s]:
                            mydata[s][t] = {a: np.array(self.dataArray[s][t][a]) for a in ['xData', 'yData', 'yStd']}
                    mydata[s]['calibrationPhase'] = self.calibrationPhase[s]
                    filename = dir+timestr+'_'+s+'_crestingData.h5'
                    save_dict_to_hdf5(mydata, filename)

    def gunPhaser(self, gunPhaseSet=0, offset=True):
        if isinstance(self.dataArray['Gun']['calibrationPhase'],(float, int)) and isinstance(gunPhaseSet, (float, int)):
            self.machine.setGunPhase(self.dataArray['Gun']['calibrationPhase'] + (gunPhaseSet if offset else 0))

    def linac1Phaser(self, linac1PhaseSet=0, offset=True):
        if isinstance(self.dataArray['Linac1']['calibrationPhase'],(float, int)) and isinstance(linac1PhaseSet, (float, int)):
            self.machine.setLinac1Phase(self.dataArray['Linac1']['calibrationPhase'] + (linac1PhaseSet if offset else 0))

    def printFinalPhase(self):
        print(self.source+' '+' fit = '+str(self.calibrationPhase[self.source]))
        self.logger.emit(self.source+' '+' fit = '+str(self.calibrationPhase[self.source]))

    def resetDataArray(self, source, type):
        self.dataArray.resetData(source, type, ['xFit', 'yFit', 'xData', 'yData', 'yStd'])

    def appendDataArray(self, source, type, x, y, yStd):
        self.dataArray[source][type]['xData'].append(x)
        self.dataArray[source][type]['yData'].append(y)
        self.dataArray[source][type]['yStd'].append(yStd)
        self.newData.emit(source, type)

    def setDataArray(self, source, type, x, y, yStd):
        self.dataArray[source][type]['xData'] = x
        self.dataArray[source][type]['yData'] = y
        self.dataArray[source][type]['yStd'] = yStd
        self.newData.emit(source, type)

    def setFitArray(self, source, type, x, y):
        self.dataArray[source][type]['xFit'] = x
        self.dataArray[source][type]['yFit'] = y
        self.newData.emit(source, type)

    def getDataArray(self, source, type, column=None, zipped=True, sortKey=None):
        if column is not None:
            return self.dataArray[source][type][column]
        else:
            data = [self.dataArray[source][type]['xData'],
                self.dataArray[source][type]['yData'],
                self.dataArray[source][type]['yStd']]
            if sortKey is not None:
                data = zip(*sorted(zip(*data), key=sortKey))
            if zipped:
                return zip(*data)
            else:
                return data

    def getFitArray(self, source, type, zipped=True):
        data = [self.dataArray[source][type]['xFit'],
            self.dataArray[source][type]['yFit']]
        if zipped:
            return zip(*data)
        else:
            return data

    def getData(self):
        time.sleep(self.sleepTime)
        data = {}
        result = {}
        for d in self.getDataFunction:
            data[d] = []
        while len(data[self.getDataFunction.keys()[-1]]) < self.nShots:
            for d in self.getDataFunction:
                # print('getting ', d, ' data')
                val = self.getDataFunction[d]()
                # print('getting ', d, ' data = ', val)
                data[d].append(val)
            time.sleep(self.sleepTime)
        for d in self.getDataFunction:
            data[d] = [a for a in data[d] if not np.isnan(a)]
            result[d] = [np.mean(data[d]), np.std(data[d])] #if np.std(data[d]) > 0.001 else [float('nan'),0]
            # print(d, ' = ', result[d])
        return result

    def getRFCorrectionData(self, nSamples=None):
        if nSamples is None:
            nSamples = self.nShots
        time.sleep(self.sleepTime)
        result = {}
        data = []
        while len(data) < nSamples:
            val = self.getCorrectDataFunction()
            data.append(val)
            time.sleep(self.sleepTime)
        data = [a for a in data if not np.isnan(a)]
        result = [np.mean(data), np.std(data)]
        # print(d, ' = ', result[d])
        return result

    def rotate_list(self, l, n):
        return l[n:] + l[:n]


########### findingCrestGunFine ###############

    def do_CTR_Scan(self):
        for d in self.getDataFunction:
            self.resetDataArray('CTR', d)
        alldata = self.getData()
        if not alldata['bpmpos'][1] > 0:
            self.logger[str, str].emit('C2V BPM not reading - cancelling scan!', 'error')
            return
        for d in self.getDataFunction:
            self.resetDataArray('CTR', d)
        prePhase = self.machine.getPhase('Linac1')
        # self.machine.setPhase('Gun', self.calibrationPhase['Gun'])
        self.machine.setPhase('Linac1', self.calibrationPhase['Linac1'])
        # self.machine.setAmplitude('Linac1', 35000)
        self.startingPhase = self.calibrationPhase['Linac1'] + self.startPhase
        self.endingPhase = self.calibrationPhase['Linac1'] + self.endPhase
        self.movePhaseTo(self.startingPhase)
        self.scanPhaseFine()
        compression_phase_idx = np.array(self.dataArray['CTR']['ctrsignal']['yData']).argmax()
        compression_phase = self.dataArray['CTR']['ctrsignal']['xData'][compression_phase_idx]
        self.calibrationPhase['CTR'] = compression_phase
        self.printFinalPhase()
        self.progress.emit(100)

    def scanPhaseFine(self):
        range = np.arange(self.startingPhase, self.endingPhase+self.stepPhase, self.stepPhase)
        for i, phase in enumerate(range):
            self.progress.emit(100*i/len(range))
            if self._abort or self._finished:
                return
            self.machine.setPhase(self.cavity, phase)
            time.sleep(self.sleepTimeFine)
            if self.correctRFAmplitude:
                self.correctBPMUsingRFAmplitude(step=self.getCorrectDataStep, target=self.getCorrectDataTarget)
            currphase = phase#self.machine.getPhase(self.cavity)
            alldata = self.getData()
            alldata['ctrsignal'][0] = alldata['ctrsignal'][0] / (alldata['wcmq'][0]**2)
            alldata['ctrsignal'][1] = alldata['ctrsignal'][1] / (alldata['wcmq'][0]**2)
            for d in alldata:
                data, stddata = alldata[d]
                self.appendDataArray(self.source, d, currphase, data, stddata)

    def movePhaseTo(self, finalphase):
        prePhase = self.machine.getPhase('Linac1')
        if finalphase < prePhase:
            range = np.arange(prePhase, finalphase-0.1, -1)
        else:
            range = np.arange(finalphase, prePhase+0.1, 1)
        for i, phase in enumerate(range):
            print('SETTING PHASE ', phase)
            self.machine.setPhase(self.cavity, phase)
            time.sleep(self.sleepTimeFine)
            success = self.correctBPMUsingRFAmplitude(step=250, target=0, stdTarget=3)
            if not success:
                self.startingPhase = phase
                return

    def correctBPMUsingRFAmplitude(self, step=50, target=0, stdTarget=None, maxRF=60000):
        maxRF = maxRF if self.maxRF is None else self.maxRF
        amplitude = self.machine.getAmplitude(self.cavity)
        print('STARTING AMPLITUDE = ', amplitude)
        mean, std = self.getRFCorrectionData(nSamples=3)
        print('MEAN = ', mean, '  STD = ', std)
        std = stdTarget if stdTarget is not None else std if std > 0.01 else 0.1
        direction = 1 if mean > target else -1
        self.logger[str, str].emit('Starting RF Correction target='+str(target)+'  current_value='+str(mean), 'debug')
        oscillate = 0
        while (abs(mean-target) > std):
            self.logger[str, str].emit('Stepping RF='+str(step)+' target='+str(target)+'  current_value='+str(mean), 'debug')
            amplitude += step * direction
            print('AMPLITUDE = ', amplitude)
            if amplitude > maxRF:
                self.logger[str, str].emit('RF Amplitude limit reached!', 'error')
                return False
            self.machine.setAmplitude(self.cavity, amplitude)
            time.sleep(self.sleepTimeFine)
            mean, std = self.getRFCorrectionData(nSamples=1)
            std = stdTarget if stdTarget is not None else std if std > 0.01 else 0.1
            new_direction = 1 if mean > target else -1
            if not new_direction == direction:
                oscillate += 1
            if oscillate > 1:
                step = step / np.sqrt(2)
            direction = new_direction
        return True
