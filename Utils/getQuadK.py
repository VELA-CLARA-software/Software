import sys
import scipy.constants as physics
import numpy as np
import math
import time
sys.path.append("../../")
import Software.Procedures.Machine.machine as spmm
from Software.Procedures.Machine.machine import Bunch as Bunch
degree = physics.pi/180.0
SPEED_OF_LIGHT = physics.constants.c / 1e6

class localMachine(dict):

    def __init__(self, magref):
        super(localMachine, self).__init__()
        global globalMachine
        self.magRef = magref
        self.magnets = Bunch()
        self.magnets.getMagObjConstRef = self.getMagnet
        for name, psu, si in zip(self.magRef.magNames, self.magRef.psuStates, self.magRef.siValues):
            self[name] = Bunch()
            self[name].SI = si
            self[name].getMagPSUState = psu
            self[name].name = name
            self[name].position = globalMachine.magnets.getMagObjConstRef(name).position
            self[name].fieldIntegralCoefficients = globalMachine.magnets.getMagObjConstRef(name).fieldIntegralCoefficients

    def getMagnet(self, magnetName):
        return self[magnetName]

class getMagnetProperties(object):
    def __init__(self, filename=None, machine=None, machineType='Physical', lineType='CLARA', gunType='10Hz'):
        super(getMagnetProperties, self).__init__()
        global globalMachine
        if machine is None:
            globalMachine = spmm.Machine(machineType, lineType, gunType, controllers=['magnets'])
        else:
            globalMachine = machine
        if filename is not None:
            self.getDBURT(filename)
        else:
            self.machine = globalMachine

    def getDBURT(self, DBURT):
        print('loading DBURT ', DBURT)
        self.magRef = globalMachine.magnets.getDBURT(DBURT)
        self.machine = localMachine(self.magRef)

    def getMachine(self):
        self.machine = globalMachine

    def getS(self, magnetname):
        magnet = self.machine.magnets.getMagObjConstRef(magnetname)
        return magnet.position

    def getK(self, magnetname, current=None, integrated=False):
        """Perform the calculation of K value (or bend angle)."""
        magnet = self.machine.magnets.getMagObjConstRef(magnetname)
        print('fieldIntegralCoefficients = ', magnet.fieldIntegralCoefficients)
        if current is None:
            current = magnet.SI
        # print 'current = ', current
        mag_type = str(magnet.magType)
        # Get the integrated strength, based on an excitation curve
        # This is in T.mm for dipoles, T for quads, T/m for sextupoles
        # Note that excitation curves are defined with positive current,
        # so we invert the coefficients (except the offset) for negative current
        # This gives a smooth transition through zero
        sign = np.copysign(1, current)
        coeffs = np.append(magnet.fieldIntegralCoefficients[:-1] * sign, magnet.fieldIntegralCoefficients[-1])
        int_strength = np.polyval(coeffs, abs(current))
        # Calculate the normalised effect on the beam
        # effect = np.copysign(SPEED_OF_LIGHT * int_strength / momentum, current)
        effect = SPEED_OF_LIGHT * int_strength / self.momentum
        # Depending on the magnet type, convert to meaningful units
        if mag_type == 'DIP':
            # Get deflection in degrees
            # int_strength was in T.mm so we divide by 1000
            k = effect / 1000
        elif mag_type in ('QUAD', 'SEXT'):
            k = 1000 * effect
            k = k / magnet.magneticLength  if not integrated else k # focusing term K
        elif mag_type in ('HCOR', 'VCOR'):
            k = effect/1000  # deflection in mrad
        elif mag_type == 'SOL': # solenoids
            # Getting peak B field
            sign = np.copysign(1, current)
            coeffs = np.append(magnet.fieldIntegralCoefficients[-4:-1] * sign, magnet.fieldIntegralCoefficients[-1])
            int_strength = np.polyval(coeffs, abs(current))
            k = int_strength / magnet.magneticLength
        else:
            k = 0
        return current, k

    def calculateMomentumFromDipole(self, magnetname, current=None):
        magnet = self.machine.magnets.getMagObjConstRef(magnetname)
        if current is None:
            current = magnet.SI
        sign = np.copysign(1, current)
        coeffs = np.append(magnet.fieldIntegralCoefficients[:-1] * sign, magnet.fieldIntegralCoefficients[-1])
        int_strength = np.polyval(coeffs, abs(current))
        angle = 45  # reset to 45
        return 1e-6*0.001 * physics.c * int_strength / np.radians(angle)

    def calculateMomentaFromDipole(self, magnetname, currents=[]):
        return [self.calculateMomentumFromDipole(magnetname, I) for I in currents]

    def getMagnetParameterType(self, magnetname):
        magnet = self.machine.magnets.getMagObjConstRef(magnetname)
        mag_type = str(magnet.magType)
        if mag_type == 'DIP':
            param = 'angle'
        elif mag_type == 'QUAD':
            param = 'k1'
        elif mag_type == 'SEXT':
            param = 'k2'
        elif mag_type in ('HCOR', 'VCOR'):
            param = 'angle'
        elif mag_type == 'SOL': # solenoids
            param = 'field_amplitude'
        else:
            param = None
        return param

    def getMagnetName(self, magnetname):
        magnet = self.machine.magnets.getMagObjConstRef(magnetname)
        return magnet.pvRoot[:magnet.pvRoot.find(':')]

    def getMagnetControllerNames(self):
        return self.machine.magnets.getMagnetNames()

    def getMagnetNames(self):
        magnetcontrollernames = self.getMagnetControllerNames()
        return [self.getMagnetName(m) for m in magnetcontrollernames]

    def getNamesK(self):
        magnetcontrollernames = self.getMagnetControllerNames()
        names = self.getMagnetNames()
        data = [[self.getMagnetName(m), self.getMagnetParameterType(m), self.getK(m), self.getS(m)] for m in magnetcontrollernames]
        return list(zip(*list(zip(*list(sorted(data,key=lambda l:l[-1]))))[:-1]))

if __name__ == "__main__":
    magprop = getMagnetProperties()#'CLARA_2_BA1_BA2_2018-11-20-1951.dburt')
    en1 = magprop.calculateMomentumFromDipole('BA1-DIP01', 56.485)
    en2 = magprop.calculateMomentumFromDipole('BA1-DIP01', 57.765)
    print('energy1 = ', en1, '  energy2 = ', en2, '   diff = ', en2-en1)
    # exit()
    # # magprop.momentum = 31.5
    # print magprop.momentum
    magprop = getMagnetProperties()
    magprop.momentum = 35.5
    print(magprop.getK('BA1-QUAD07', 10, integrated=True)[1]/1000)
    # print magprop.getK('C2V-QUAD2')
    # print magprop.getK('C2V-QUAD3')
    # with open('CLARA_2_BA1_BA2_2018-11-20-1951.'+str(np.round(magprop.momentum,decimals=2))+'.txt', 'w') as f:
    #     for item in magprop.getNamesK():
    #         for d in item:
    #             f.write("%s\t" % d)
    #         f.write("\n")
    # magprop.momentum = 31.5
    # with open('CLARA_2_BA1_BA2_2018-11-20-1951.31.5MeV.txt', 'w') as f:
    #     for item in magprop.getNamesK():
    #         for d in item:
    #             f.write("%s\t" % d)
    #         f.write("\n")
