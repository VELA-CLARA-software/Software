import time
import numpy as np
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import scipy.constants as constants
from scipy.optimize import curve_fit

degree = constants.pi/180.0
q_e = constants.elementary_charge
c = constants.speed_of_light

p0 = 5e6

class RF_Cavity(object):

    def __init__(self, name, crest):
        super(RF_Cavity, self).__init__()
        self.phase = 

    @property
    def phase(self):
        return self._phase
    @phase.setter
    def phase(self, value):
        self._phase = value

    @property
    def crest(self):
        return self._crest
    @crest.setter
    def crest(self, value):
        self._crest = value

    @property
    def amplitude(self):
        return self._amplitude
    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = value

    @property
    def p(self):
        return self.amplitude * np.cos((self.crest - self.phase) * degree)

class dipole(PVObject):

    def __init__(self, name, length):
        super(dipole, self).__init__(name)

class bpm(PVBuffer):

    def __init__(self, name, length):
        super(bpm, self).__init__(name)
        self.name = name
        self.length = length

    @property
    def x(self):
        return self.mean

class accelerator(QObject):

    newBPMReading = pyqtSignal(int, list)
    newGradient = pyqtSignal(int, int, float)
    newBfield = pyqtSignal(float)
    newP = pyqtSignal(float)

    def __init__(self):
        super(accelerator, self).__init__()
        self.cavs = []
        for i in range(6):
            self.cavs.append(RF_Cavity('cav' + str(i + 1), 0))
        self.dip = dipole('dip1', 0.400003)
        self.bpm = bpm('bpm1', 0.31)
        self.bpmReadings = np.empty((0,2),int)
        self.offset = 0
        self.cavityNumber = 0
        self.cavityPower = 45e6
        self.maxPower = 1 * self.cavityPower

    def turnOnCavity(self):
        self.amplitude = self.cavityPower

    def turnOffCavity(self):
        self.amplitude = 0

    @property
    def multiplier(self):
        power = np.sum([self.cavs[i].amplitude for i in range(1)])
        return 2 * power / self.maxPower

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

    def momentum(self):
        p = float(p0 + np.sum(np.array([getattr(x, 'p') for x in self.cavs])))
        p = p if p > 0 else p0
        self.newP.emit(p)
        return p

    @property
    def B(self):
        return self.dip.B
    @B.setter
    def B(self, value):
        self.dip.B = value
        self.newBfield.emit(self.dip.B)

    @property
    def x(self):
        self.dip.p = self.momentum()
        self.bpm.dipole_angle = self.dip.angle
        return 1e3*self.bpm.x

    def bpmReading(self):
        self.bpmReadings = np.append(self.bpmReadings, [[self.phase, self.x + self.offset]], axis=0)

    def findStartingPhase(self, phase=0):
        self.phase = phase
        # self.B += 0.05
        bpmpos = self.x
        while((self.x > 10 or self.x < -10) and self.phase < 355):
            self.phase += 1
        print ('starting phase = ', self.phase, self.crest)

    def gradient(self):
        return np.polyfit(x=self.bpmReadings[-5:,0], y=self.bpmReadings[-5:,1], deg=1)[0] * self.multiplier

    def initialPoints(self):
        for i in range(5):
            self.phase += 1
            self.bpmReading()

    def center_beam(self, acc=3):
        startx = self.x
        if self.x > acc:
            while(self.x > acc):
                self.B += 0.001
        else:
            while(self.x < -1*acc):
                self.B -= 0.001
        self.offset += startx - self.x
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
                self.center_beam()
                self.newBPMReading.emit(self.cavityNumber, [self.phase, self.x + self.offset])

    def optimise(self):
        while((self.phasesign * self.gradient()) > -1):
            self.step()

    def step(self):
        if((self.phasesign * self.gradient()) > -1):
            self.phase += self.phasesign * np.max([1, 1*np.abs(self.gradient())])
            self.center_beam()
            self.newBPMReading.emit(self.cavityNumber, [self.phase, self.x + self.offset])
        self.newGradient.emit(self.cavityNumber, self.phasesign, self.gradient())
        # self.set_on_phase(self.calculated_crest)

    def set_on_phase(self, crest):
        while(np.abs(crest - self.phase) > 0.1):
            phasesign = np.sign(crest - self.phase)
            self.phase += phasesign*np.max([1, 1*np.abs(crest - self.phase)])
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
    acc.B = 0.05
    for i in [5,4,3,2,1,0]:
        acc.cavityNumber = i
        acc.crest = 360.0*np.random.random()
        acc.turnOnCavity()
        acc.reset()
        acc.findCrest(0)
        acc.optimise()
        # print 'guess crest = ', acc.guess_crest(), acc.crest
        acc.calculate_crest()
        acc.set_on_phase(acc.calculated_crest)
        # print 'momentum = ', acc.momentum()/1e6, acc.B
        print (i+1, acc.crest - np.mod(acc.phase,360))

if __name__ == '__main__':
   main()
