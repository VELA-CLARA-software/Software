import time
import numpy as np
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4 import QtTest
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import scipy.constants as constants
from scipy.optimize import curve_fit
import inspect

degree = constants.pi/180.0
q_e = constants.elementary_charge
c = constants.speed_of_light

import VELA_CLARA_Magnet_Control as vcmag
maginit = vcmag.init()
Cmagnets = maginit.physical_CLARA_PH1_Magnet_Controller()
import VELA_CLARA_BPM_Control as vcbpmc
bpms = vcbpmc.init()
Cbpms = bpms.physical_CLARA_PH1_BPM_Controller()
# print zip(*inspect.getmembers(Cbpms, predicate=inspect.ismethod))[0]
# exit()
import VELA_CLARA_LLRF_Control as vcllrf
llrf = vcllrf.init()
Cllrf = llrf.physical_LRRG_LLRF_Controller()
print zip(*inspect.getmembers(Cbpms, predicate=inspect.ismethod))[0]
exit()

def qSleep(time):
    QtTest.QTest.qWait(time)


class RF_Cavity(QObject):

    def __init__(self, name, crest):
        super(RF_Cavity, self).__init__()
        self.name = name
        self._phase = 0

    @property
    def phase(self):
        #Cllrf.getPhiLLRF()
        return self._phase
    @phase.setter
    def phase(self, value):
        # Cllrf.setPhiLLRF()
        self._phase = value

    @property
    def amplitude(self):
        return Cllrf.getAmpLLRF()
    @amplitude.setter
    def amplitude(self, value):
        pass
        # self._amplitude = value

class dipole(object):

    def __init__(self, name, length):
        super(dipole, self).__init__()
        self.name = name
        self.length = length

    @property
    def I(self):
        return Cmagnets.getRI(self.name)
    @I.setter
    def I(self, value):
        pass
        # Cmagnets.setSI(self.name, value)

class bpm(object):

    def __init__(self, name, length):
        super(bpm, self).__init__()
        self.name = name
        self.length = length
        self.startBuffer = Cbpms.getBPMXBuffer(self.name)

    @property
    def x(self):
        if Cbpms.getBPMXBuffer(self.name) == self.startBuffer:
            return -100
        else:
            return Cbpms.getXFromPV(self.name)

class accelerator(QObject):

    newBPMReading = pyqtSignal(int, list)
    newGradient = pyqtSignal(int, int, float)
    newBfield = pyqtSignal(float)

    def __init__(self):
        super(accelerator, self).__init__()
        self.cavs = []
        for i in range(1):
            self.cavs.append(RF_Cavity('cav' + str(i + 1), 0))
        self.dip = dipole('DIP01', 0.400003)
        self.bpm = bpm('C2V-BPM01', 0.31)
        self.bpmReadings = np.empty((0,2),int)
        self.offset = 0
        self.cavityNumber = 0
        self.cavityPower = 14800
        self.maxPower = 1 * self.cavityPower

    def turnOnCavity(self):
        self.amplitude = self.cavityPower

    def turnOffCavity(self):
        self.amplitude = 0

    @property
    def multiplier(self):
        return 2 * self.cavityPower / self.maxPower

    @property
    def crest(self):
        return self.cavs[self.cavityNumber].crest
    @crest.setter
    def crest(self, value):
        self.cavs[self.cavityNumber].crest = value

    @property
    def phase(self):
        return self.cavs[self.cavityNumber].phase
    @phase.setter
    def phase(self, value):
        self.cavs[self.cavityNumber].phase = value

    @property
    def amplitude(self):
        return self.cavs[self.cavityNumber].amplitude
    @amplitude.setter
    def amplitude(self, value):
        self.cavs[self.cavityNumber].amplitude = value

    @property
    def I(self):
        return self.dip.I
    @I.setter
    def I(self, value):
        self.dip.I = value
        self.newBfield.emit(self.dip.I)

    def x(self):
        return 1e3*self.bpm.x

    def bpmReading(self):
        self.bpmReadings = np.append(self.bpmReadings, [[self.phase, self.x() + self.offset]], axis=0)

    def findStartingPhase(self, phase=0):
        print ('finding start phase!')
        self.phase = phase
        while((self.x() > 10 or self.x() < -10) and self.phase < 355):
            self.phase += 5
            qSleep(250)
            print ('phase = ', self.phase)
        print ('starting phase = ', self.phase)

    def gradient(self):
        return np.polyfit(x=self.bpmReadings[-5:,0], y=self.bpmReadings[-5:,1], deg=1)[0] * self.multiplier

    def initialPoints(self):
        for i in range(5):
            self.phase += 1
            self.bpmReading()

    def center_beam(self, acc=3):
        startx = self.x()
        if self.x() > acc:
            while(self.x() > acc):
                self.I += 0.1
                qSleep(250)
        else:
            while(self.x() < -1*acc):
                self.I -= 0.1
                qSleep(250)
        self.offset += startx - self.x()
        self.bpmReading()

    def guess_crest(self):
        return self.bpmReadings[:,0][list(self.bpmReadings[:,1]).index(np.max(self.bpmReadings[:,1]))]

    def reset(self):
        self.phasesign = 1
        self.offset = 0
        self.bpmReadings = np.empty((0,2),int)

    def findCrest(self, phase=0):
        self.offset = 0
        self.findStartingPhase(phase)
        self.initialPoints()
        if self.gradient() < 0:
            self.phasesign = -1*self.phasesign
        self.setStartPosition()

    def setStartPosition(self):
        if((self.phasesign * self.gradient()) < 1):
            while((self.phasesign * self.gradient()) < 1):
                self.phase -= self.phasesign * np.max([0.5, 1*np.abs(self.gradient())])
                qSleep(250)
                self.center_beam()
                self.newBPMReading.emit(self.cavityNumber, [self.phase, self.x() + self.offset])

    def optimise(self):
        while((self.phasesign * self.gradient()) > -1):
            self.step()

    def step(self):
        if((self.phasesign * self.gradient()) > -1):
            self.phase += self.phasesign * np.max([1, 1*np.abs(self.gradient())])
            qSleep(250)
            self.center_beam()
            self.newBPMReading.emit(self.cavityNumber, [self.phase, self.x() + self.offset])
        self.newGradient.emit(self.cavityNumber, self.phasesign, self.gradient())
        # self.set_on_phase(self.calculated_crest)

    def set_on_phase(self, crest):
        while(np.abs(crest - self.phase) > 0.1):
            phasesign = np.sign(crest - self.phase)
            self.phase += phasesign*np.max([1, 1*np.abs(crest - self.phase)])
            qSleep(250)
            self.center_beam(acc=0.1)

    def calculate_crest(self):
        fit = self.fit_curve()
        self.calculated_crest = fit[2]
        return fit

    def fitting_equation(self, x, a, b, crest):
        return a + b * np.cos((crest - x) * degree)

    def fit_curve(self):
        popt, pcov = curve_fit(self.fitting_equation, self.bpmReadings[:,0], self.bpmReadings[:,1], p0=[1, 4,self.guess_crest()],
        bounds=([-np.inf, -np.inf, self.guess_crest()-20],[np.inf, np.inf, self.guess_crest()+20]))
        return popt

    def fittedData(self):
        if len(self.bpmReadings) > 5:
            minx = np.min(self.bpmReadings[:,0])
            maxx = np.max(self.bpmReadings[:,0])
            fitting_params = self.fit_curve()
            fittedData = [[x, self.fitting_equation(x, *fitting_params)] for x in np.arange(minx, maxx, 0.1)]
        else:
            fittedData = []
        return fittedData

def main():
    acc = accelerator()
    acc.I = 80
    for i in [0]:
        acc.cavityNumber = i
        acc.turnOnCavity()
        acc.reset()
        acc.findCrest(0)
        # acc.optimise()
        # print 'guess crest = ', acc.guess_crest(), acc.crest
        # acc.calculate_crest()
        # acc.set_on_phase(acc.calculated_crest)
        # print 'momentum = ', acc.momentum()/1e6, acc.B
        # print (i+1, acc.crest - np.mod(acc.phase,360))
    exit()

if __name__ == '__main__':
   main()
