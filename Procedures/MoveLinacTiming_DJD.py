import sys, time, os
sys.path.append("../Widgets/")
from generic.pv import *

import argparse

parser = argparse.ArgumentParser(description='Move LINAC01 timing signals together')
parser.add_argument('offset', metavar='timing offset',
                   help='How much to offset the Linac01 timing (in microseconds)', type=int)
args = parser.parse_args()


modulatorPVName = 'CLA-C18-TIM-EVR-01:Pul3-Delay-SP'
amplifierPVName = 'CLA-C18-TIM-EVR-01:Pul4-Delay-SP'
llrfPVName = 'CLA-C18-TIM-EVR-02:Pul1-Delay-SP'

modulatorPV = PVObject(modulatorPVName)
modulatorPV.writeAccess = True
amplifierPV = PVObject(amplifierPVName)
amplifierPV.writeAccess = True
llrfPV = PVObject(llrfPVName)
llrfPV.writeAccess = True

print ' Starting Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
print 'Setting ', args.offset, ' microsecond offset!'
modulatorPV.value = modulatorPV.value + args.offset
amplifierPV.value = amplifierPV.value + args.offset
llrfPV.value = llrfPV.value + args.offset
time.sleep(0.1)
print ' New Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
