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
import Software.Procedures.Machine.machine as Machine
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

    def __init__(self, machineType, lineType, gunType, machine=None):
        super(Model, self).__init__()
        if machine is None:
            self.baseMachine = Machine.Machine(machineType, lineType, gunType)
            self.parameters = self.baseMachine.initialise_parameters()
        else:
            self.baseMachine = machine
            self.parameters = self.baseMachine.parameters
        self.machine = machineSetter(self.baseMachine)
        self.machineType = machineType
        self.lineType = lineType
        self.gunType = gunType
        self.newData = emitter()
        self.logger = emitter()
        self.progress = emitter()
        if not self.machineType == 'None': #If we are NOT using a virtual machine, set timeout's
            self.sleepTime = 0.1
            self.sleepTimeDipole = 0.25
            self.sleepTimeFine = 0.1
        self.crestingData = dataArray()
        self.parameters = self.baseMachine.initialise_parameters()
        self.data = []
        self.calibrationPhase = {'Gun': None, 'Linac1': None}
        self.settings = {'Gun':{'Amp_Set': 71000}, 'Linac1': {'PID': True, 'Amp_Set': 41000}}
        print("Model Initialized")

    def debugLogging(self, function=None, **kwargs):
        string = str(function)+':'
        for kw, val in kwargs.items():
            string += ' '+str(kw)+'='+str(val)
        self.logger.emit(string, 'debug')

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
        self.logger.emit('Loading DBURT: GunCrest.dburt','info')
        if self.machineType == 'None':
            time.sleep(1)
            return False
        else:
            return self.machine.applyDBURT('GunCrest.dburt')

    def loadLinac1BURT(self):
        self.logger.emit('Loading DBURT: Linac1Crest.dburt', 'info')
        if self.machineType == 'None':
            time.sleep(3)
            return True
        else:
            return self.machine.applyDBURT('Linac1Crest.dburt')

    def turnOnGun(self, max, step):
        self.debugLogging(function='turnOnGun', max=max, step=step)
        self.resetAbortFinish()
        max = max if max <= self.settings['Gun']['Amp_Set'] else self.settings['Gun']['Amp_Set']
        start = self.machine.getGunAmplitude()
        range =  np.arange(start, max+1, step)
        for i, set in enumerate(range):
            self.progress.emit(100*i/len(range))
            if self._abort or self._finished:
                return
            self.machine.setGunAmplitude(set)
            time.sleep(1)
        self.machine.setGunAmplitude(max)

    def turnOnLinac1(self, max, step):
        self.debugLogging(function='turnOnLinac1', max=max, step=step)
        self.resetAbortFinish()
        max = max if max <= self.settings['Linac1']['Amp_Set'] else self.settings['Linac1']['Amp_Set']
        start = self.machine.getLinac1Amplitude()
        range =  np.arange(start, max+1, step)
        for i, set in enumerate(range):
            self.progress.emit(100*i/len(range))
            if self._abort or self._finished:
                return
            self.machine.setLinac1Amplitude(set)
            time.sleep(1)
        self.machine.setLinac1Amplitude(max)

    def gunWCMCrester(self, stepSize=5, nSamples=4, offset=10):
        self.debugLogging(function='gunWCMCrester', stepSize=stepSize, nSamples=nSamples, offset=offset)
        self.resetAbortFinish()
        self.cavity = 'Gun'
        self.actuator = 'approx'
        self.stepSize = stepSize
        self.nSamples = nSamples
        self.fitOffset = offset
        self.getDataFunction = partial(self.machine.getWCMCharge, self.parameters['scope'])
        self.machine.set_PID(self.cavity, False)
        self.findingCrestGunQuick()

    def linacCresterQuick(self, no, stepSize=5, nSamples=4, offset=0, PID=True):
        self.debugLogging(function='linacCresterQuick', no=no, stepSize=stepSize, nSamples=nSamples, offset=offset)
        self.resetAbortFinish()
        self.cavity = 'Linac'+str(no)
        self.actuator = 'approx'
        self.stepSize = stepSize
        self.nSamples = nSamples
        self.fitOffset = offset
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_rough_bpm'][no], ignoreNonLinear=True)
        self.machine.set_PID(self.cavity, False)
        self.disable_Linac_PID(no=1)
        self.findingCrestLinacQuick()

    def gunCresterFine(self, phiStart, phiRange, phiSteps, nSamples):
        self.debugLogging(function='gunCresterFine', phiStart=phiStart, phiRange=phiRange, phiSteps=phiSteps, nSamples=nSamples)
        self.resetAbortFinish()
        self.cavity = 'Gun'
        self.actuator = 'fine'
        self.stepSize = 5
        self.nSamples = nSamples
        self.phiStart = phiStart
        self.phiRange = phiRange
        self.phiSteps = phiSteps
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['gun_dispersive_bpm'])
        self.sleepTimeFine = 0.1
        self.machine.set_PID(self.cavity, False)
        self.findingCrestFine()

    def linacCresterFine(self, no, phiStart, phiRange, phiSteps, nSamples, PID=True):
        self.debugLogging(function='linacCresterFine', no=no, phiStart=phiStart, phiRange=phiRange, phiSteps=phiSteps, nSamples=nSamples, PID=PID)
        self.resetAbortFinish()
        self.cavity = 'Linac'+str(no)
        self.actuator = 'fine'
        self.stepSize = 5
        self.phiStart = phiStart
        self.nSamples = nSamples
        self.phiRange = phiRange
        self.phiSteps = phiSteps
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_dispersive_bpm'][no])
        self.sleepTimeFine = 0.1
        self.machine.set_PID(self.cavity, PID)
        if PID:
            self.initialise_Linac_PID(cavity=no, initialPhase=phiStart)
        else:
            self.disable_Linac_PID(no=1)
        self.findingCrestFine()

    def gunCresterFineScreen(self, phiStart, phiRange, phiSteps, nSamples):
        self.debugLogging(function='gunCresterFineScreen', phiStart=phiStart, phiRange=phiRange, phiSteps=phiSteps, nSamples=nSamples)
        self.resetAbortFinish()
        self.cavity = 'Gun'
        self.actuator = 'screen'
        self.stepSize = 5
        self.nSamples = nSamples
        self.phiStart = phiStart
        self.phiRange = phiRange
        self.phiSteps = phiSteps
        self.getDataFunction = partial(self.machine.getScreenPosition, self.parameters['gun_dispersive_screen'])
        self.machine.cameras.startAcquiring(self.parameters['gun_dispersive_screen'])
        self.sleepTimeFine = 1.5
        self.sleepTime = 0.2
        self.machine.set_PID(self.cavity, False)
        self.findingCrestFine()
        self.sleepTimeFine = 0.1
        self.sleepTime = 0.1

    def linacCresterFineScreen(self, no, phiStart, phiRange, phiSteps, nSamples):
        self.debugLogging(function='linacCresterFineScreen',no=no, phiStart=phiStart, phiRange=phiRange, phiSteps=phiSteps, nSamples=nSamples)
        self.resetAbortFinish()
        self.cavity = 'Linac'+str(no)
        self.actuator = 'screen'
        self.stepSize = 5
        self.phiStart = phiStart
        self.nSamples = nSamples
        self.phiRange = phiRange
        self.phiSteps = phiSteps
        self.machine.cameras.startAcquiring(self.parameters['linac_dispersive_screen'][no])
        self.getDataFunction = partial(self.machine.getScreenPosition, self.parameters['linac_dispersive_screen'][no])
        self.sleepTimeFine = 1.5
        self.sleepTime = 0.2
        self.machine.set_PID(self.cavity, True)
        self.initialise_Linac_PID(cavity=no, startingValue=phiStart)
        self.findingCrestFine()
        self.sleepTimeFine = 0.1
        self.sleepTime = 0.1

    def gunDipoleSet(self, start=5, stop=10, step=0.1):
        self.debugLogging(function='gunDipoleSet', start=start, stop=stop, step=step)
        self.resetAbortFinish()
        self.cavity = 'Gun'
        self.actuator = 'dipole'
        self.nSamples = 10
        self.minDipoleI = start
        self.maxDipoleI = stop
        self.dipoleIStep = step
        self.initialGuess = [10, 1, 9]
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['gun_dispersive_bpm'])
        self.findDipoleCurrent()

    def linacDipoleSet(self, no, start=70, stop=100, step=1):
        self.debugLogging(function='linacDipoleSet', no=no, start=start, stop=stop, step=step)
        self.resetAbortFinish()
        self.cavity = 'Linac'+str(no)
        self.actuator = 'dipole'
        self.nSamples = 3
        self.minDipoleI = start
        self.maxDipoleI = stop
        self.dipoleIStep = step
        self.initialGuess = [10, 5, (stop+start)/2]
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_dispersive_bpm'][no])
        self.findDipoleCurrent()

    def gunMomentumSet(self, dipole=8.08):
        self.debugLogging(function='gunDipoleSet', dipole=dipole)
        self.resetAbortFinish()
        self.cavity = 'Gun'
        self.nSamples = 3
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['gun_dispersive_bpm'])
        self.Correct_Momentum(dipole=dipole, dipoleStep=0.1, RFstep=50, maxRF=67000)

    def linacMomentumSet(self, no, dipole=66.18):
        self.debugLogging(function='linacDipoleSet', no=no, dipole=dipole)
        self.resetAbortFinish()
        self.cavity = 'Linac'+str(no)
        self.nSamples = 3
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_dispersive_bpm'][no])
        self.Correct_Momentum(dipole=dipole, dipoleStep=0.5, RFstep=50, maxRF=62000)

    def initialise_Linac_PID(self, *args, **kwargs):
        self.debugLogging(function='initialise_Linac_PID', **kwargs)
        self.machine.initialise_Linac_PID(*args, **kwargs)

    def disable_Linac_PID(self, no=1):
        self.debugLogging(function='disable_Linac_PID', no=no)
        self.machine.disable_Linac_PID(cavity=no)

    def initialise_Gun_PID(self, *args, **kwargs):
        self.machine.initialise_Gun_PID(*args, **kwargs)

    def disable_Gun_PID(self):
        self.machine.disable_Gun_PID()

    def saveData(self, cavity=None, type=None, savetoworkfolder=True):
        self.debugLogging(function='saveData', cavity=cavity, type=type, savetoworkfolder=savetoworkfolder)
        if not self.machineType == 'None':
            if cavity is not None and not isinstance(cavity, (tuple, list)):
                cavity = [cavity]
            elif cavity is None:
                cavity = ['Gun', 'Linac1']
            if type is not None and not isinstance(type, (tuple, list)):
                type = [type]
            elif type is None:
                type = ['approx', 'fine', 'dipole','screen']
            timestr = time.strftime("%H%M%S")
            dir = '\\\\claraserv3\\claranet\\apps\\legacy\\logs\\autoCrester\\'+time.strftime("%Y\\%m\\%d")+'\\' if savetoworkfolder else '.'
            try:
                os.makedirs(dir)
            except OSError:
                if not os.path.isdir(dir):
                    self.logger.emit('Error creating directory - saving to local directory','warning')
                    dir = '.'
            for c in cavity:
                if c in self.crestingData:
                    for t in type:
                        if t in self.crestingData[c]:
                            mydata = {a: np.array(self.crestingData[c][t][a]) for a in ['xData', 'yData', 'yStd']}
                            mydata['calibrationPhase'] = self.crestingData[c]['calibrationPhase']
                            filename = dir+timestr+'_'+c+'_'+t+'_crestingData.h5'
                            # mydata = merge_two_dicts(mydata,self.RFTraces)
                            save_dict_to_hdf5(mydata, filename)

    def getRFTraces(self):
        self.debugLogging(function='getRFTraces', cavity=self.cavity)
        if self.cavity == 'Gun':
            self.RFTraces = self.machine.getGunRFTraces(dict=True)
        elif self.cavity == 'Linac1':
            self.RFTraces = self.machine.getLinac1RFTraces(dict=True)


    def gunPhaser(self, gunPhaseSet=0, offset=True):
        self.debugLogging(function='gunPhaser', gunPhaseSet=gunPhaseSet, offset=offset)
        if isinstance(self.crestingData['Gun']['calibrationPhase'],(float, int)) and isinstance(gunPhaseSet, (float, int)):
            self.machine.setGunPhase(self.crestingData['Gun']['calibrationPhase'] + (gunPhaseSet if offset else 0))

    def linac1Phaser(self, linac1PhaseSet=0, offset=True):
        self.debugLogging(function='linac1Phaser', linac1PhaseSet=linac1PhaseSet, offset=offset)
        if isinstance(self.crestingData['Linac1']['calibrationPhase'],(float, int)) and isinstance(linac1PhaseSet, (float, int)):
            self.machine.setLinac1Phase(self.crestingData['Linac1']['calibrationPhase'] + (linac1PhaseSet if offset else 0))

    def setUpMagnets(self,magnets):
        self.debugLogging(function='setUpMagnets', magnets=magnets)
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
        self.debugLogging(function='printFinalPhase', cavity=self.cavity, actuator=self.actuator, fit=self.crestingData[self.cavity]['calibrationPhase'])
        print(self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationPhase']))
        self.logger.emit(self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationPhase']),'info')

    def printFinalDip(self):
        self.debugLogging(function='printFinalDip', cavity=self.cavity, actuator=self.actuator, fit=self.crestingData[self.cavity]['calibrationDip'])
        print(self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationDip']))
        self.logger.emit(self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationDip']), 'info')

    def resetDataArray(self):
        self.debugLogging(function='resetDataArray', cavity=self.cavity, actuator=self.actuator)
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
        self.debugLogging(function='getDataArray', cavity=self.cavity, actuator=self.actuator, column=column, zipped=zipped, sortKey=sortKey)
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
        self.debugLogging(function='getDataArray', cavity=self.cavity, actuator=self.actuator, zipped=zipped)
        data = [self.crestingData[self.cavity][self.actuator]['xFit'],
            self.crestingData[self.cavity][self.actuator]['yFit']]
        if zipped:
            return zip(*data)
        else:
            return data

    def setFinalPhase(self, phase):
        phase = np.round(np.mod(180+phase,360)-180, decimals=1)
        self.debugLogging(function='setFinalPhase', cavity=self.cavity, actuator=self.actuator, phase=phase)
        self.crestingData[self.cavity]['calibrationPhase'] = phase
        if not self.machineType == 'None':
            self.getRFTraces()


    def applyFinalPhase(self, cavity=None):
        if cavity == None:
            cavity = self.cavity
        self.debugLogging(function='applyFinalPhase', cavity=cavity)
        if cavity in self.crestingData and 'calibrationPhase' in self.crestingData[cavity]:
            self.machine.setPhase(self.cavity, self.crestingData[cavity]['calibrationPhase'])

    def setFinalDip(self, dip):
        self.debugLogging(function='setFinalDip', cavity=self.cavity, dip=dip)
        self.crestingData[self.cavity]['calibrationDip'] = dip
        self.machine.setDip(dip)

    def getData(self):
        # self.data = []
        # while len(self.data) < 2:
        #     self.data.append(self.getDataFunction())
        #     time.sleep(self.sleepTime)
        time.sleep(self.sleepTime)
        self.data = []
        while len(self.data) < self.nSamples:
            self.data.append(self.getDataFunction())
            time.sleep(self.sleepTime)
        # print('before = ', self.data)
        self.data = [a for a in self.data if not np.isnan(a)]
        # print('after = ', [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [float('nan'),0])
        return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [float('nan'),0]

    def rotate_list(self, l, n):
        return l[n:] + l[:n]

########### findingCrestGunQuick ###############

    def findingCrestQuick(self):
        self.debugLogging(function='findingCrestQuick', cavity=self.cavity, stepSize=self.stepSize)
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
        self.debugLogging(function='findingCrestGunQuick', cavity=self.cavity)
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
        self.debugLogging(function='cutDataGunQuick', cavity=self.cavity, stepSize=self.stepSize)
        allData = self.getDataArray()
        max_charge = max(self.getDataArray('yData'))
        cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 10]
        alllist = []
        newlist = []
        for i, pt in enumerate(cutData):
            if i < (len(cutData)-1):
                if not cutData[i+1][0] - pt[0] > 2*self.stepSize:
                    newlist.append(pt)
                else:
                    alllist.append(newlist)
                    newlist = []
            elif i == (len(cutData)-1):
                newlist.append(pt)
                alllist.append(newlist)
        # print 'alllist = ', alllist
        if len(alllist) < 1:
            self.logger[str, str].emit('Error in fitting! Is the gun on?', 'warning')
        return max(alllist, key=len)

    def doFitGunQuick(self):
        self.debugLogging(function='doFitGunQuick', cavity=self.cavity, fitOffset=self.fitOffset)
        cutData = self.cutDataGunQuick()
        x, y, std = zip(*cutData)
        if max(x) - min(x) > 180:
            print('####  Gun Quick Scan range > 90  ####')
            x = [a if a >= 0 else a+360 for a in x]
            phase, data, stddata = self.getDataArray(zipped=False)
            phase = np.array([a if a >= 0 else a+360 for a in phase])
            self.setDataArray(phase, data, stddata)
        crest_phase = np.mean(x) + self.fitOffset
        if crest_phase > 180:
            crest_phase -= 360
        self.setFitArray(np.array(x), np.array(y))
        crest_phase = np.round(crest_phase, decimals=1)
        self.setFinalPhase(crest_phase)
        self.printFinalPhase()

########### findingCrestLinac1Quick ###############

    def findingCrestLinacQuick(self):
        self.debugLogging(function='findingCrestLinacQuick', cavity=self.cavity)
        self.startingPhase = self.machine.getPhase(self.cavity)
        self.findingCrestQuick()
        if not self._abort:
            self.doFitLinacQuick()
        else:
             self.machine.setPhase(self.cavity, self.startingPhase)

    def cutDataLinacQuick(self):
        self.debugLogging(function='cutDataLinacQuick', cavity=self.cavity, stepSize=self.stepSize)
        allData = self.getDataArray()
        cutData = [a for a in allData if np.isnan(a[1])]
        alllist = []
        newlist = []
        for i, pt in enumerate(cutData):
            if i < (len(cutData)-1):
                if not cutData[i+1][0] - pt[0] > 2*self.stepSize:
                    newlist.append(pt)
                else:
                    alllist.append(newlist)
                    newlist = []
            elif i == (len(cutData)-1):
                newlist.append(pt)
                alllist.append(newlist)
        # print 'alllist = ', alllist
        if len(alllist) < 1:
            self.logger[str, str].emit('Error in fitting! Is the linac on?', 'warning')
        return max(alllist, key=len)

    def doFitLinacQuick(self):
        self.debugLogging(function='doFitLinacQuick', cavity=self.cavity, fitOffset=self.fitOffset)
        try:
            cutData = self.cutDataLinacQuick()
            x, y, std = zip(*cutData)
            crest_phase = np.mean(x) - 180 + self.fitOffset
            if crest_phase > 180:
                crest_phase -= 360
            if crest_phase < -180:
                crest_phase += 360
            crest_phase = np.round(crest_phase, decimals=1)
            self.setFitArray(np.array([crest_phase,crest_phase]), np.array([-10,10]))
            crest_phase = np.round(crest_phase, decimals=1)
            self.setFinalPhase(crest_phase)
            self.printFinalPhase()
        except Exception as e:
            print(e)

########### findingCrestGunFine ###############

    def findingCrestFine(self):
        self.debugLogging(function='findingCrestFine', cavity=self.cavity, phiStart=self.phiStart, phiRange=self.phiRange, phiSteps=self.phiSteps)
        self.startingPhase = self.machine.getPhase(self.cavity)
        self.resetDataArray()
        self.approxcrest = self.phiStart
        self.minPhase = self.approxcrest-self.phiRange
        self.maxPhase = self.approxcrest+self.phiRange+self.phiSteps
        self.scanPhaseFine()
        if not self._abort:
            self.fittingFunc()
        else:
            self.machine.setPhase(self.cavity, self.startingPhase)
        self.progress.emit(100)

    def scanPhaseFine(self):
        self.debugLogging(function='scanPhaseFine', cavity=self.cavity, minPhase=self.minPhase, maxPhase=self.maxPhase, phiSteps=self.phiSteps)
        range = np.arange(self.minPhase, self.maxPhase, self.phiSteps)
        for i, phase in enumerate(range):
            self.progress.emit(100*i/len(range))
            if self._abort or self._finished:
                return
            self.machine.setPhase(self.cavity, phase)
            time.sleep(self.sleepTimeFine)
            currphase = phase#self.machine.getPhase(self.cavity)
            data, stddata = self.getData()
            if stddata > 0.01:
                self.appendDataArray(currphase, data, stddata)

    def fittingFunc(self):
        if self.cavity == 'Gun':
            self.fittingLinac1Fine()
        elif self.cavity == 'Linac1':
            self.fittingLinac1Fine()

    def cutDataGunFine(self):
        """Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
        self.debugLogging(function='cutDataGunFine', cavity=self.cavity)
        allData = self.getDataArray(sortKey=lambda x: x[0])
        cutData = [a for a in allData if a[-1] < 1]
        return cutData

    def fittingGunFine(self):
        self.debugLogging(function='fittingGunFine', cavity=self.cavity, approxcrest=self.approxcrest, minPhase=self.minPhase, maxPhase=self.maxPhase)
        data = self.cutDataGunFine()
        x, y, std = [np.array(a) for a in zip(*data)]
        if (max(x) - min(x)) > (self.maxPhase - self.minPhase):
            x = np.array([a if a >= 0 else a+360 for a in x])
        popt, pcov = curve_fit(self.fitting_equation_Linac1Fine, x, y, \
            sigma=(1+(y-min(y))) * (1+abs(x-self.approxcrest))**0.5,    p0=[0,10,self.approxcrest], bounds=[[-np.inf, 0, min(x)], [np.inf, np.inf, max(x)]])

        phase = np.array(x)
        phase = np.arange(min(x), max(x),(max(x)-min(x))/1000)
        data = self.fitting_equation_Linac1Fine(phase, *popt)
        self.setFitArray(phase, data)
        crest_phase = ((180 + popt[2]) % 360) - 180
        if crest_phase > 180:
            crest_phase -= 360
        if crest_phase < 180:
            crest_phase += 360
        crest_phase = np.round(crest_phase, decimals=1)
        self.setFinalPhase(crest_phase)
        self.printFinalPhase()

    def fitting_equation_Linac1Fine(self, x, a, b, crest):
        # return a + b * (np.sin((crest - (x + 180)) * degree)**2)
        return a + b * (crest - x)**2


    def fittingLinac1Fine(self):
        self.debugLogging(function='fittingLinac1Fine', cavity=self.cavity, approxcrest=self.approxcrest)
        x, y, std = [np.array(a) for a in self.getDataArray(zipped=False)]
        popt, pcov = curve_fit(self.fitting_equation_Linac1Fine, x, y, \
            sigma=(1+(y-min(y))) * (1+abs(x-self.approxcrest))**0.5,    p0=[0,10,self.approxcrest], bounds=[[-np.inf, 0, min(x)], [np.inf, np.inf, max(x)]])

        # phase = np.array(x)
        phase = np.arange(min(x), max(x),(max(x)-min(x))/1000)
        data = self.fitting_equation_Linac1Fine(phase, *popt)
        self.setFitArray(phase, data)
        crest_phase = ((180 + popt[2]) % 360) - 180
        if crest_phase > 180:
            crest_phase -= 360
        if crest_phase < 180:
            crest_phase += 360
        crest_phase = np.round(crest_phase, decimals=1)
        self.setFinalPhase(crest_phase)
        self.printFinalPhase()

########### findingDipoleCurrent ###############

    def findDipoleCurrent(self):
        self.debugLogging(function='findDipoleCurrent', cavity=self.cavity)
        self.startingDipole = self.machine.getDip()
        self.resetDataArray()
        self.scanDipole()
        if not self._abort:
            self.doFitDipoleCurrent()
        else:
             self.machine.setDip(self.startingDipole)
             while abs(self.machine.getDip() - self.startingDipole) > 0.2:
                 time.sleep(self.sleepTimeDipole)
        self.progress.emit(100)


    def scanDipole(self):
        self.debugLogging(function='findDipoleCurrent', cavity=self.cavity, minDipoleI=self.minDipoleI, maxDipoleI=self.maxDipoleI, dipoleIStep=self.dipoleIStep)
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


    def cutDataDipoleCurrent(self):
        self.debugLogging(function='cutDataDipoleCurrent', cavity=self.cavity, dipoleIStep=self.dipoleIStep)
        allData = self.getDataArray()
        cutData = [a for a in allData if a[1] is not float('nan') and a[2] is not 0]
        # print cutData
        newlist = []
        for i, pt in enumerate(cutData):
            if i < (len(cutData)-1):
                if not cutData[i+1][0] - pt[0] > 2*self.dipoleIStep:
                    newlist.append(pt)
            elif i == (len(cutData)-1):
                newlist.append(pt)
        return newlist

    def fitting_equation_DipoleCurrent(self, x, b, c, crest):
        # return -6 + b * (x - crest)
        return b * (np.sin(c * (x - crest)))


    def doFitDipoleCurrent(self):
        self.debugLogging(function='doFitDipoleCurrent', cavity=self.cavity, initialGuess=self.initialGuess)
        cutData = self.cutDataDipoleCurrent()
        x, y, std = zip(*cutData)
        xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)

        if max(x) < self.initialGuess[-1]:
            self.initialGuess[-1] = max(x)

        popt, pcov = curve_fit(self.fitting_equation_DipoleCurrent, x, y, sigma=std, \
        bounds=([0, -np.inf, min(x)], [max(y)-min(y), np.inf, max(x)]))

        self.setFitArray(np.array(xnew), self.fitting_equation_DipoleCurrent(xnew, *popt))
        self.finalDipoleI = np.round(popt[-1], decimals=2)
        self.setFinalDip(self.finalDipoleI)
        while abs(self.machine.getDip() - self.finalDipoleI) > 0.2:
            time.sleep(self.sleepTimeDipole)
        self.printFinalDip()

########### SetDipoleMomentum ###############

    def SetDipoleMomentum(self, mom):
        self.debugLogging(function='doFitDipoleCurrent', mom=mom)
        current = self.machine.calculateDipoleMomentum(mom)
        self.machine.setDip(current)

    def calculateDipoleFromMomentum(self, mom):
        self.debugLogging(function='calculateDipoleFromMomentum', mom=mom)
        if not self.machineType == 'None':
            D = self.machine.magnets.getMagObjConstRef(self.machine.parameters['dipole'])
            coeffs = list(D.fieldIntegralCoefficients)
            coeffs[-1] -= (1000000000*(mom*physics.pi*45)/(physics.c*180))
            roots = np.roots(coeffs)
            return roots[-1].real
        return 8.19

    def calculateMomentumFromDipole(self, current):
        self.debugLogging(function='calculateDipoleFromMomentum', current=current)
        if not self.machineType == 'None':
            D = self.machine.magnets.getMagObjConstRef(self.machine.parameters['dipole'])
            sign = np.copysign(1, current)
            coeffs = np.append(D.fieldIntegralCoefficients[:-1] * sign, D.fieldIntegralCoefficients[-1])
            int_strength = np.polyval(coeffs, abs(current))
            angle = 45  # reset to 45
            # print 1e-6*0.001 * physics.c * int_strength / np.radians(angle)
            return 1e-6*0.001 * physics.c * int_strength / np.radians(angle)
        return 35.5

    def Correct_Momentum(self, dipole, dipoleStep=0.5, RFstep=50, maxRF=40000):
        self.debugLogging(function='Correct_Momentum', dipole=dipole, dipoleStep=dipoleStep, RFstep=RFstep, maxRF=maxRF)
        currentDip = self.machine.getDip()
        finalDip = dipole
        direction = 1 if finalDip > currentDip else -1
        mean, std = self.getData()
        if self.machineType == 'Physical' and direction*mean > 0:
            self.correctBPMUsingRFAmplitude(step=RFstep, target=0, stdTarget=1, maxRF=maxRF)
        while (direction*(finalDip - self.machine.getDip())) > 0.01 and abs(finalDip - self.machine.getDip()) > dipoleStep and not self._abort:
            currentDip += direction*dipoleStep
            self.debugLogging(function='Correct_Momentum', currentDip=currentDip)
            self.machine.setDip(currentDip)
            mean, std = self.getData()
            if self.machineType == 'Physical' and direction*mean > 0:
                self.correctBPMUsingRFAmplitude(step=RFstep, target=0, stdTarget=1, maxRF=maxRF)
        self.machine.setDip(finalDip)
        self.debugLogging(function='Correct_Momentum', currentDip=finalDip)
        if self.machineType == 'Physical':
            self.correctBPMUsingRFAmplitude(step=RFstep, target=0, stdTarget=0.1, maxRF=maxRF)

    def correctBPMUsingRFAmplitude(self, step=50, target=0, stdTarget=None, maxRF=60000):
        self.debugLogging(function='correctBPMUsingRFAmplitude', step=step, target=target, stdTarget=stdTarget, maxRF=maxRF)
        # maxRF = maxRF if self.maxRF is None else self.maxRF
        amplitude = self.machine.getAmplitude(self.cavity)
        self.debugLogging(function='correctBPMUsingRFAmplitude', cavity=self.cavity, amplitude=amplitude)
        mean, std = self.getData()
        std = stdTarget if stdTarget is not None else std if std > 0.01 else 0.1
        self.debugLogging(function='correctBPMUsingRFAmplitude', cavity=self.cavity, BPM_mean=mean, BPM_std=std)
        direction = 1 if mean > target else -1
        self.debugLogging(function='correctBPMUsingRFAmplitude', cavity=self.cavity, new_direction=direction)
        oscillate = 0
        while (abs(mean-target) > std) and not self._abort:
            amplitude += step * direction
            self.debugLogging(function='correctBPMUsingRFAmplitude', cavity=self.cavity, amplitude=amplitude)
            if amplitude > maxRF:
                self.debugLogging(function='correctBPMUsingRFAmplitude', cavity=self.cavity, maxRF=maxRF, reached_Max_RF=True)
                return False
            self.machine.setAmplitude(self.cavity, amplitude)
            time.sleep(self.sleepTimeFine)
            mean, std = self.getData()
            std = stdTarget if stdTarget is not None else std if std > 0.01 else 0.1
            self.debugLogging(function='correctBPMUsingRFAmplitude', cavity=self.cavity, BPM_mean=mean, BPM_std=std)
            new_direction = 1 if mean > target else -1
            if not new_direction == direction:
                self.debugLogging(function='correctBPMUsingRFAmplitude', cavity=self.cavity, new_direction=new_direction)
                oscillate += 1
            if oscillate > 1:
                self.debugLogging(function='correctBPMUsingRFAmplitude', cavity=self.cavity, step=step)
                step = step / np.sqrt(2)
            direction = new_direction
        return True
