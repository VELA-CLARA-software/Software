# SAM to Python Conversion
# DJS August 2017
# Version 0.1
import math
from ..Particles import Electron

from ..SAMPLlab import PhysicalConstants
# from ..SAMPLlab import PhysicalUnits
import numpy as np
# import math


class Beam(object):
    def __init__(self, species=Electron.Electron, bunchcharge=0, distance=[],
                 globaltime=0, spins=0, energy=0,
                 momentum=0, rigidity=0):
        # particle type, e.g. electron, positron, proton
        self.species = species()
        # bunch charge in coulombs
        self.bunchcharge = bunchcharge
        # 2xN array, recording total distance travelled by each particle%
        # this is s - the independant coordinate
        self.distance = np.array(distance)
        # global time in seconds
        self.globaltime = globaltime
        # 2xN array, polar angles of spin vector of N particles
        self.spins = spins
        # 6xN array, phase space variables of N particles
        # self.particles = particles

        # reference energy in joules
        if energy != 0:
            # print 'calling energy setter??'
            self.energy = energy

        # reference momentum in kilogram metres/second
        if momentum != 0:
            self.momentum = momentum

        # beam rigidity in tesla metres
        # this is called last - if energy and momentum are also passed and not
        # consistent with rigidity, rigidity is assumed to be correct
        if rigidity != 0:
            self.__rigidity = rigidity

        # do we really need this... ?
        self.__brho = 0  # ??
        # Dependent=true properties get a __ prefix
        # relativistic beta (v/c)
        self.__beta = 0
        # relativistic gamma factor
        self.__gamma = 0
        # phase space coordinates of particles
        self.__phasespace = 0
        # why not have phase space as explicit lists?
        # that are accessed anywhere?
        self.x = np.array([1, 1])
        self.px = np.array([2, 2])
        self.y = np.array([3, 3])
        self.py = np.array([4, 4])
        self.ct = np.array([5, 5])
        self.dp = np.array([6, 7])
        self.__particles = np.column_stack((self.x, self.px, self.y,
                                            self.py, self.ct, self.dp))
        # https://softwareengineering.stackexchange.com/questions/283514/python-best-way-to-have-interdependant-variable-in-a-class

    @property
    def particles(self):
        return np.transpose([self.x, self.px, self.y, self.py, self.ct, self.dp])

    @particles.setter
    def particles(self, particles):
        if type(particles).__module__ == np.__name__:
            # print 'setting particles'
            [self.x, self.px, self.y, self.py, self.ct, self.dp] = np.column_stack((particles))
            # distance is whether they are in the aperture or not at each stage (!)
            self.distance = np.array([[0.0] * len(particles),
                                     [1.0] * len(particles)])
        else:
            print 'particles should be a numpy array'

    def gamma(self):
        return self.__gamma

    @property
    def energy(self):
        return math.sqrt(math.pow(self.__rigidity * self.species.charge, 2)
                         * PhysicalConstants.SpeedOfLight2 +
                         self.species.mass2 * PhysicalConstants.SpeedOfLight4)

    @energy.setter
    def energy(self, energy):
        self.__rigidity = (math.sqrt(energy**2 / PhysicalConstants.SpeedOfLight2
                                     - (self.species.mass2 *
                                        PhysicalConstants.SpeedOfLight2)) /
                           self.species.charge)
        #print (math.sqrt(energy**2 / PhysicalConstants.SpeedOfLight2 - (self.species.mass2 * PhysicalConstants.SpeedOfLight2)) /self.species.charge)

    @property
    def momentum(self):
        return self.__rigidity * self.species.charge

    @momentum.setter
    def momentum(self, momentum):
        self.__rigidity = momentum / self.species.charge

    @property
    def rigidity(self):
        return self.__rigidity

    @rigidity.setter
    def rigidity(self, rigidity):
        self.__rigidity = abs(rigidity) * np.sign(self.species.charge)
        # if ~isempty(beam.phasespace) && beam.brho~=0
        if not self.phasespace and self.__brho != 0:
            # if we have some particles and we are scaling their momentum
            # (maybe after emitting radiation, or passing though an
            # rf structure? )

            P0 = self.__brho * self.species.charge;
            P1 = self.__rigidity * self.species.charge

            E0 = math.sqrt(math.pow(P0, 2) * PhysicalConstants.SpeedOfLight2 \
             + self.species.mass2 * PhysicalConstants.SpeedOfLight4 )

            E1 = math.sqrt(math.pow(P1,2)* PhysicalConstants.SpeedOfLight2 \
             + self.species.mass2 * PhysicalConstants.SpeedOfLight4 )

            b0 = P0*PhysicalConstants.SpeedOfLight/E0
            b1 = P1*PhysicalConstants.SpeedOfLight/E1

            #self.phasespace([2,4],:) = self.phasespace([2,4],:)*P0/P1;
            #self.phasespace(6,:) = (self.phasespace(6,:) + 1/b0)*P0/P1 - 1/b1;

            #self.brho = self.__rigidity

    @property
    def beta(self):
        bg = self.__rigidity * self.species.charge / self.species.mass / PhysicalConstants.SpeedOfLight
        self.__beta = bg / math.sqrt(1+bg*bg)
        return self.__beta

    @property
    def gamma(self):
        bg = self.__rigidity * self.species.charge / self.species.mass / PhysicalConstants.SpeedOfLight
        self.__gamma = math.sqrt(1+bg*bg)
        return self.__gamma
