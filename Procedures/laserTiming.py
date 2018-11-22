import sys, time, os
sys.path.append("../../")
from Software.Widgets.generic.pv import *


class LaserTiming(object):

    pvName = 'CLA-C17-TIM-EVR-01:FrontUnivOut4-Ena-SP'
    pvNameDetect = 'CLA-S01-DIA-BPM-01:AWAK'
    pvUsefulNames = 'AllowLaser'
    nominalTiming = 1

    def __init__(self):
        super(LaserTiming, self).__init__()
        self.pv = PVObject(self.pvName)
        self.pvDetect = PVObject(self.pvNameDetect)
        setattr(self.pv, 'writeAccess', True)

    def turnOnLaser(self):
        return setattr(self.pv, 'value', 1)

    def turnOffLaser(self):
        return setattr(self.pv, 'value', 0)

    @property
    def isLaserOn(self):
        return self.pv.value

    def turnOnForNPulse(self, n=100):
        while not self.isLaserOn == 1:
            self.turnOnLaser()
        print 'laser on ? = ', self.isLaserOn
        count = 0
        nullcount = 0
        self.detectToggle = self.pvDetect.value
        while count < n:
            if not self.pvDetect.value == self.detectToggle:
                self.detectToggle = self.pvDetect.value
                count += 1
                nullcount = 0
                print count, nullcount
            else:
                nullcount += 1
        self.turnOffLaser()
        return count
