import sys, time, os
sys.path.append("../../")
from Software.Widgets.generic.pv import *


class Linac01Timing(object):

    pvNames = ['CLA-C18-TIM-EVR-01:Pul3-Delay-SP', 'CLA-C18-TIM-EVR-01:Pul4-Delay-SP', 'CLA-C18-TIM-EVR-02:Pul1-Delay-SP']
    pvUsefulNames = ['Modulator', 'Amplifier', 'LLRF']
    nominalTiming = [396.46, 384.06, 400.96]

    def __init__(self):
        super(Linac01Timing, self).__init__()
        self.pvs = [PVObject(x) for x in self.pvNames]
        [setattr(x, 'writeAccess', True) for x in self.pvs]

    def offsetTiming(self, offset):
        return [setattr(x, 'value', y+offset) for x,y in zip(self.pvs, self.nominalTiming)]

    def resetTiming(self):
        return [setattr(x, 'value', y) for x,y in zip(self.pvs, self.nominalTiming)]

    def isLinacOn(self):
        return all([getattr(x,'value') == y for x,y in zip(self.pvs, self.nominalTiming)])
