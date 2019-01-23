import sys
import argparse
import os
import scipy.constants as physics
import numpy as np
import math
sys.path.append("../../")
import Software.Procedures.Machine.machine as spmm
degree = physics.pi/180.0
SPEED_OF_LIGHT = physics.constants.c / 1e6


parser = argparse.ArgumentParser(description='Converts DBURT to framework')
parser.add_argument('filename')

class getMagnetProperties(object):
    def __init__(self, filename=None, machine=None, machineType='Physical', lineType='CLARA', gunType='10Hz'):
        super(getMagnetProperties, self).__init__()
        if machine is None:
            self.machine = spmm.Machine(machineType, lineType, gunType, controllers=['magnets'])
        else:
            self.machine = machine
        self.loadDBURT(filename)
        self.momentum = self.calculateMomentumFromDipole('S02-DIP01')

    def loadDBURT(self, filename=None):
        dict = {}
        # read in entire file
        with open(filename) as burt_file:
            content = burt_file.readlines()
        # look for the lines with required format and add to dict
        # [assumed to be those with 4 data points, when split by colon]
        for i, line in enumerate(content):
            content_split = line.split(':')
            if len(content_split) == 4:
                stripstring = '\n\r\w;'
                dict[content_split[0]] = [content_split[1].strip(stripstring), content_split[2].strip(stripstring), content_split[3].strip(stripstring)]
        self.BURTdict = dict
        return dict

    def getK(self, magnetname, current=None):
        """Perform the calculation of K value (or bend angle)."""
        if current is None:
            current = float(self.BURTdict[magnetname][1])
        # print 'current = ', current
        magnet = self.machine.magnets.getMagObjConstRef(magnetname)
        mag_type = str(magnetname)
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
        if 'DIP' in mag_type:
            # Get deflection in degrees
            # int_strength was in T.mm so we divide by 1000
            k = effect / 1000
        elif 'QUAD' in mag_type or 'SEXT' in mag_type:
            k = 1000 * effect / magnet.magneticLength  # focusing term K
        elif 'HCOR' in mag_type or 'VCOR' in mag_type:
            k = effect/1000  # deflection in mrad
        elif 'SOL' in mag_type: # solenoids
            # Getting peak B field
            sign = np.copysign(1, current)
            coeffs = np.append(magnet.fieldIntegralCoefficients[-4:-1] * sign, magnet.fieldIntegralCoefficients[-1])
            int_strength = np.polyval(coeffs, abs(current))
            k = int_strength / magnet.magneticLength
        else:
            k = 0
        return k

    def calculateMomentumFromDipole(self, magnetname):
        magnet = self.machine.magnets.getMagObjConstRef(magnetname)
        current = magnet.SI
        sign = np.copysign(1, current)
        coeffs = np.append(magnet.fieldIntegralCoefficients[:-1] * sign, magnet.fieldIntegralCoefficients[-1])
        int_strength = np.polyval(coeffs, abs(current))
        angle = 45  # reset to 45
        return 1e-6*0.001 * physics.c * int_strength / np.radians(angle)

    def getMagnetParameterType(self, magnetname):
        mag_type = str(magnetname)
        if 'DIP' in mag_type:
            param = 'angle'
        elif 'QUAD' in mag_type:
            param = 'k1'
        elif 'SEXT' in mag_type:
            param = 'k2'
        elif 'HCOR' in mag_type or 'VCOR' in mag_type:
            param = 'angle'
        elif 'SOL' in mag_type: # solenoids
            param = 'field_amplitude'
        else:
            param = None
        return param

    def getMagnetNames(self):
        return self.BURTdict.keys()

    def getNamesK(self):
        names = self.getMagnetNames()
        data = [[self.getMagnetName(m), self.getMagnetParameterType(m), self.getK(m)] for m in names]
        return data

if __name__ == "__main__":
    args = parser.parse_args()
    magprop = getMagnetProperties(args.filename)
    # magprop.momentum = 31.5
    print magprop.momentum
    print magprop.getK('C2V-QUAD1')
    print magprop.getK('C2V-QUAD2')
    print magprop.getK('C2V-QUAD3')
