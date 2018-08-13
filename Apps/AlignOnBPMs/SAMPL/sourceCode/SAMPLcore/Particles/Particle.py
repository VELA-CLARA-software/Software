# SAM to Python Conversion
# DJS August 2017
# Version 0.1
#

class Particle(object):
    def __init__(self):
        self.__charge = 1
        self.__mass   = 1
        self.__Cq     = 1
        self.__Cgamma = 1
        self.__mass2  = 1

    @property
    def charge(self):
        return self.__charge

    @property
    def mass(self):
        return self.__mass

    @property
    def mass2(self):
        return self.__mass2
