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
        if self.machineType is 'None':
            return True
        else:
            return self.machine.applyDBURT('GunCrest.dburt')

    def loadLinac1BURT(self):
        if self.machineType is 'None':
            return True
        else:
            return self.machine.applyDBURT('Linac1Crest.dburt')

    def turnOnGun(self, max, step):
        self.resetAbortFinish()
        max = max if max <= 16000 else 16000
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
        self.resetAbortFinish()
        max = max if max <= 13500 else 13500
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
        self.resetAbortFinish()
        self.cavity = 'Gun'
        self.actuator = 'approx'
        self.stepSize = stepSize
        self.nSamples = nSamples
        self.fitOffset = offset
        self.getDataFunction = partial(self.machine.getWCMCharge, self.parameters['scope'])
        self.findingCrestGunQuick()

    def linacCresterQuick(self, no, stepSize=5, nSamples=4, offset=0):
        self.resetAbortFinish()
        self.cavity = 'Linac'+str(no)
        self.actuator = 'approx'
        self.stepSize = stepSize
        self.nSamples = nSamples
        self.fitOffset = offset
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_rough_bpm'][no], ignoreNonLinear=True)
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
        self.sleepTimeFine = 0.1
        self.findingCrestFine()

    def linacCresterFine(self, no, phiStart, phiRange, phiSteps, nSamples):
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
        self.findingCrestFine()

    def gunCresterFineScreen(self, phiStart, phiRange, phiSteps, nSamples):
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
        self.findingCrestFine()
        self.sleepTimeFine = 0.1
        self.sleepTime = 0.1

    def linacCresterFineScreen(self, no, phiStart, phiRange, phiSteps, nSamples):
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
        self.findingCrestFine()
        self.sleepTimeFine = 0.1
        self.sleepTime = 0.1

    def gunDipoleSet(self, start=5, stop=10, step=0.1):
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
        self.resetAbortFinish()
        self.cavity = 'Linac'+str(no)
        self.actuator = 'dipole'
        self.nSamples = 3
        self.minDipoleI = start
        self.maxDipoleI = stop
        self.dipoleIStep = step
        self.initialGuess = [10, 1, (stop+start)/2]
        self.getDataFunction = partial(self.machine.getBPMPosition, self.parameters['linac_dispersive_bpm'][no])
        self.findDipoleCurrent()

    def saveData(self, cavity=None, type=None, savetoworkfolder=True):
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
            dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\' if savetoworkfolder else '.'
            try:
                os.makedirs(dir)
            except OSError:
                if not os.path.isdir(dir):
                    self.logger.emit('Error creating directory - saving to local directory')
                    dir = '.'
            for c in cavity:
                if c in self.crestingData:
                    for t in type:
                        if t in self.crestingData[c]:
                            mydata = {a: np.array(self.crestingData[c][t][a]) for a in ['xData', 'yData', 'yStd']}
                            filename = dir+timestr+'_'+c+'_'+t+'_crestingData.h5'
                            mydata = merge_two_dicts(mydata,self.RFTraces)
                            save_dict_to_hdf5(mydata, filename)

    def getRFTraces(self):
        if self.cavity == 'Gun':
            self.RFTraces = self.machine.getGunRFTraces(dict=True)
        elif self.cavity == 'Linac1':
            self.RFTraces = self.machine.getLinac1RFTraces(dict=True)

    def gunPhaser(self, gunPhaseSet=0, offset=True):
        if isinstance(self.crestingData['Gun']['calibrationPhase'],(float, int)) and isinstance(gunPhaseSet, (float, int)):
            print 'gunPhaseSet = ', gunPhaseSet
            print 'offset = ', offset
            self.machine.setGunPhase(self.crestingData['Gun']['calibrationPhase'] + (gunPhaseSet if offset else 0))

    def linac1Phaser(self, linac1PhaseSet=0, offset=True):
        if isinstance(self.crestingData['Linac1']['calibrationPhase'],(float, int)) and isinstance(linac1PhaseSet, (float, int)):
            self.machine.setLinac1Phase(self.crestingData['Linac1']['calibrationPhase'] + (linac1PhaseSet if offset else 0))

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
        if not self.machineType == 'None':
            self.getRFTraces()

    def applyFinalPhase(self, cavity=None):
        if cavity == None:
            cavity = self.cavity
        if 'calibrationPhase' in self.crestingData[self.cavity]:
                  self.machine.setPhase(self.cavity, self.crestingData[self.cavity]['calibrationPhase'])

    def setFinalDip(self, dip):
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
        # print 'before = ', self.data
        self.data = [a for a in self.data if not np.isnan(a)]
        # print 'after = ', self.data
        return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [float('nan'),0]

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
        crest_phase = np.mean(x) + self.fitOffset
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
        cutData = [a for a in allData if np.isnan(a[1])]
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
            x = [a+360 if a < 0 else a for a in x]
            # if max(x) - min(x) > 180:
            #     x = [a if a >= 0 else a+360 for a in x]
            #     phase, data, stddata = self.getDataArray(zipped=False)
            #     phase = np.array([a if a >= 0 else a+360 for a in phase])
            #     self.setDataArray(phase, data, stddata)
            # print 'x = ', x
            # print 'mean(x) = ', np.mean(x)
            crest_phase = np.mean(x) - 180 + self.fitOffset
            if crest_phase > 180:
                crest_phase -= 360
            # if crest_phase < 180:
            #     crest_phase += 360
            # x = [a if a <= 180 else a-360 for a in x]
            self.setFitArray(np.array([crest_phase,crest_phase]), np.array([-10,10]))
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
        self.scanPhaseFine()
        if not self._abort:
            self.fittingFunc()
        else:
            self.machine.setPhase(self.cavity, self.startingPhase)
        self.progress.emit(100)

    def scanPhaseFine(self):
        range = np.arange(self.minPhase, self.maxPhase, self.phiSteps)
        for i, phase in enumerate(range):
            self.progress.emit(100*i/len(range))
            if self._abort or self._finished:
                return
            self.machine.setPhase(self.cavity, phase)
            time.sleep(self.sleepTimeFine)
            currphase = phase#self.machine.getPhase(self.cavity)
            data, stddata = self.getData()
            if stddata > 0.05:
                self.appendDataArray(currphase, data, stddata)

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
        x, y, std = [np.array(a) for a in zip(*data)]
        if (max(x) - min(x)) > (self.maxPhase - self.minPhase):
            x = np.array([a if a >= 0 else a+360 for a in x])
        # f = UnivariateSpline(x, y, w=std, k=5)
        # xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
        # ynew = f(xnew)
        # crest_phase = xnew[np.argmin(ynew)]
        # xnew = [a if a <= 180 else a-360 for a in xnew]
        # if crest_phase > 180:
        #     crest_phase -= 360
        # if crest_phase < 180:
        #     crest_phase += 360
        # self.setFitArray(xnew, ynew)
        # self.setFinalPhase(crest_phase)
        # self.printFinalPhase()
        popt, pcov = curve_fit(self.fitting_equation_Linac1Fine, x, y, \
            sigma=(1+(y-min(y))) * (1+abs(x-self.approxcrest))**0.5,    p0=[0,10,self.approxcrest], bounds=[[-np.inf, -np.inf, min(x)], [np.inf, np.inf, max(x)]])

        phase = np.array(x)
        phase = np.arange(min(x), max(x),(max(x)-min(x))/1000)
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
        # return a + b * (np.sin((crest - (x + 180)) * degree)**2)
        return a + b * (crest - x)**2

    def fittingLinac1Fine(self):
        x, y, std = [np.array(a) for a in self.getDataArray(zipped=False)]
        popt, pcov = curve_fit(self.fitting_equation_Linac1Fine, x, y, \
            sigma=(1+(y-min(y))) * (1+abs(x-self.approxcrest))**0.5,    p0=[0,10,self.approxcrest], bounds=[[-np.inf, -np.inf, min(x)], [np.inf, np.inf, max(x)]])

        # phase = np.array(x)
        phase = np.arange(min(x), max(x),(max(x)-min(x))/1000)
        data = self.fitting_equation_Linac1Fine(phase, *popt)
        self.setFitArray(phase, data)
        self.setFinalPhase(((180 + popt[2]) % 360) - 180)
        self.printFinalPhase()

########### findingDipoleCurrent ###############

    def findDipoleCurrent(self):
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
        cutData = self.cutDataDipoleCurrent()
        x, y, std = zip(*cutData)
        xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)

        if max(x) < self.initialGuess[-1]:
            self.initialGuess[-1] = max(x)

        popt, pcov = curve_fit(self.fitting_equation_DipoleCurrent, x, y, sigma=std, \
        bounds=([0, -np.inf, min(x)], [max(y)-min(y), np.inf, max(x)]))

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
        D = self.machine.magnets.getMagObjConstRef(self.machine.parameters['dipole'])
        coeffs = list(D.fieldIntegralCoefficients)
        coeffs[-1] -= (1000000000*(mom*physics.pi*45)/(physics.c*180))
        roots = np.roots(coeffs)
        return roots[-1].real

    def calculateMomentumFromDipole(self, current):
        D = self.machine.magnets.getMagObjConstRef(self.machine.parameters['dipole'])
        sign = np.copysign(1, current)
        coeffs = np.append(D.fieldIntegralCoefficients[:-1] * sign, D.fieldIntegralCoefficients[-1])
        int_strength = np.polyval(coeffs, abs(current))
        angle = 45  # reset to 45
        # print 1e-6*0.001 * physics.c * int_strength / np.radians(angle)
        return 1e-6*0.001 * physics.c * int_strength / np.radians(angle)
