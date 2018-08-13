from ..sourceCode.SAMPLcore.SAMPLlab import Beam
from ..sourceCode.SAMPLcore.Particles import Electron
from ..sourceCode.SAMPLcore.Particles import Positron
# from SAMMcore.Particles import Proton
from ..sourceCode.SAMPLcore.SAMPLlab import PhysicalUnits
from ..sourceCode.SAMPLcore.SAMPLlab import PhysicalConstants
import numpy as np
import math


class createBeam():

    def __init__(self, PIL_Ctrl=None):
        self.PIL_Ctrl = PIL_Ctrl

    def guassian(self, x=0.0, y=0.0, sigmaX=0.001, sigmaY=0.001,
                 particle='Electron', number=1000,
                 Energy=12 * PhysicalUnits.MeV, charge=250e-9):
        if particle == 'Electron':
            beam = Beam.Beam(species=Electron.Electron, energy=Energy)
        if particle == 'Positron':
            beam = Beam.Beam(species=Positron.Positron, energy=Energy,
                             bunchcharge=charge)
        # if particle == 'Proton':
        #     beam = Beam.Beam(species=Proton.Proton, energy = Energy)
        # Generate particles
        xArray = np.random.normal(loc=x, scale=sigmaX, size=number)
        yArray = np.random.normal(loc=y, scale=sigmaY, size=number)
        ctArray = np.zeros(number)
        pxArray = np.zeros(number)
        pyArray = np.zeros(number)
        dpArray = np.zeros(number)

        p = np.array([xArray, pxArray, yArray, pyArray, ctArray, dpArray])
        p = p.transpose()
        beam.particles = p

        return beam

    def useASTRAFile(self, fileName='None', particle='Electron'):
        # Read in file
        print ('Using an ASTRA *.ini file to create SAMPL distrtibution...')
        distribution = np.loadtxt(fileName)
        charge = abs(np.sum(distribution[:, 7]) * 1e-9)
        print('Charge of bunch is ' + str(charge) + ' nC.')
        print('No. of particle in bunch is ' + str(len(distribution)) + '.')
        if particle == 'Electron':
            beam = Beam.Beam(species=Electron.Electron,
                             bunchcharge=charge)
        if particle == 'Positron':
            beam = Beam.Beam(species=Positron.Positron,
                             bunchcharge=charge)
        # if particle == 'Proton':
    #        beam = Beam.Beam(species=Proton.Proton, energy = Energy)
        beam.energy = math.sqrt((beam.species.mass2 *
                                 PhysicalConstants.SpeedOfLight2**2) +
                                (distribution[0][5] * PhysicalUnits.eV)**2 +
                                (distribution[0][4] * PhysicalUnits.eV)**2 +
                                (distribution[0][3] * PhysicalUnits.eV)**2)
        print('Bunch energy: ' + str(beam.energy / PhysicalUnits.eV) + 'eV')
        # Generate particles
        distribution[0][5] = 0.0
        xArray = distribution[:, 0]
        yArray = distribution[:, 1]
        ctArray = distribution[:, 2]
        pxArray = distribution[:, 3] * PhysicalUnits.eV/PhysicalConstants.SpeedOfLight
        pyArray = distribution[:, 4] * PhysicalUnits.eV/PhysicalConstants.SpeedOfLight
        dpArray = distribution[:, 5] * PhysicalUnits.eV/PhysicalConstants.SpeedOfLight

        p = np.array([xArray, pxArray, yArray, pyArray, ctArray, dpArray])
        p = p.transpose()
        beam.particles = p

        return beam
