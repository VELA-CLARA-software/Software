import sys, time, os
sys.path.append("../Widgets/")
sys.path.append("../../")
from generic.pv import *
import numpy as np
np.set_printoptions(threshold=np.inf)

import argparse

###############################################################################
# arguments

parser = argparse.ArgumentParser(description='Move LINAC01 timing signals together')
parser.add_argument('offset0', metavar='timing offset',
                   help='How much to offset the Gun timing (in microseconds)', type=float)
args = parser.parse_args()
###############################################################################

###############################################################################
modulatorPVName = 'CLA-C18-TIM-EVR-01:Pul0-Delay-SP'
amplifierPVName = 'CLA-C18-TIM-EVR-01:Pul3-Delay-SP'
llrfPVName = 'CLA-C18-TIM-EVR-02:Pul0-Delay-SP'

modulatorPV = PVObject(modulatorPVName)
modulatorPV.writeAccess = True
amplifierPV = PVObject(amplifierPVName)
amplifierPV.writeAccess = True
llrfPV = PVObject(llrfPVName)
llrfPV.writeAccess = True
print ' Original Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
#397.1 396.46 398.68
modPV0 = 397.1#modulatorPV.value
ampPV0 = 396.46#amplifierPV.value
llrfPV0 = 398.68#llrfPV.value

offset = args.offset0
modulatorPV.value = modulatorPV.value + args.offset0
amplifierPV.value = amplifierPV.value + args.offset0
llrfPV.value = llrfPV.value + args.offset0
time.sleep(0.1)
print ' New Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
# raw_input('Centre beam on C2V dipole')
