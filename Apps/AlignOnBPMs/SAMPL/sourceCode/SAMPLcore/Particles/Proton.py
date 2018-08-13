# SAM to Python Conversion
# DJS August 2017
# Version 0.1
#
import math
from ..SAMPLlab import PhysicalConstants


class Proton(object):
    def __init__(self):
        # Particle.__init__(self)
        # print 'Positron created'
        self.__charge = PhysicalConstants.PositronCharge
        self.__mass = PhysicalConstants.ProtonMass
        self.__mass2 = self.__mass * self.__mass
        # g-factor
        self.__g = 5.585694713
        self.__Cq = (55 * PhysicalConstants.PlanckConstant / 32 /
                     math.sqrt(3) / 2 / math.pi /
                     PhysicalConstants.SpeedOfLight /
                     PhysicalConstants.ProtonMass)
        self.__Cgamma = (PhysicalConstants.PositronCharge2 / 3 /
                         PhysicalConstants.VacuumPermittivity /
                         math.pow(PhysicalConstants.ProtonMass *
                                  PhysicalConstants.SpeedOfLight2, 4))

    @property
    def Positron(self):
        return Positron()

    @property
    def charge(self):
        return self.__charge

    @property
    def mass(self):
        return self.__mass

    @property
    def mass2(self):
        return self.__mass2

    @property
    def g(self):
        return self.__g
