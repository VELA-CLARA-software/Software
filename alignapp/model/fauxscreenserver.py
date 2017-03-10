#This is bespkoe for Frank
# v1.0 (10.11.2016)
# To use this import is into you code that is connected to VM
# Import into the model section of your App
#
#import fauxlaser as fl
#
#laser = fl.fauxLaserController(66)
#
##now to change laser position (lets say in y) and have it effect BPM01 and YAG01
#
#laser.setYposition(-9)
##This will set the Y value on the Virtual cathode to be -9, and -594 (using the factor '66' which was set when initiating the controller) for BPM01 and YAG01

from epics import caget,caput
import numpy as np

class fauxScreenServer():
    def __init__(self):
        self.x = 333.0
        self.y = 444.0
        print 'Using Faux Screen Server ...',

    def getX(self,scrname):
        if scrname != 'YAG01':
            print 'you can only have YAG01, not', scrname
        return self.x

    def getY(self,scrname):
        if scrname != 'YAG01':
            print 'you can only have YAG01, not', scrname
        return self.y 
