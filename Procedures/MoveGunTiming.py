import sys, time, os
sys.path.append("../Widgets/")
<<<<<<< HEAD
sys.path.append("../../")
=======
>>>>>>> parent of 903bfae1... Added handle_update_individual_trace button to NO-ARCv2 GUI that toggles the updating of individual traces between passive and 10Hz.
from generic.pv import *
import numpy as np
np.set_printoptions(threshold=np.inf)

import argparse

###############################################################################
# arguments
<<<<<<< HEAD
=======
filename = 'test.txt'
if os.path.exists(filename):
    print 'deleting file'
    os.remove(filename)
#filename2 = 'traces.txt'
#if os.path.exists(filename2):
#    print 'deleting file'
#    os.remove(filename2)
>>>>>>> parent of 903bfae1... Added handle_update_individual_trace button to NO-ARCv2 GUI that toggles the updating of individual traces between passive and 10Hz.

parser = argparse.ArgumentParser(description='Move LINAC01 timing signals together')
parser.add_argument('offset0', metavar='timing offset',
                   help='How much to offset the Gun timing (in microseconds)', type=float)
<<<<<<< HEAD
args = parser.parse_args()
###############################################################################

###############################################################################
modulatorPVName = 'CLA-C18-TIM-EVR-01:Pul0-Delay-SP'
amplifierPVName = 'CLA-C18-TIM-EVR-01:Pul3-Delay-SP'
=======
parser.add_argument('step', metavar='timing step size',
                   help='The value of the increments for stepping the Gun timing (in microseconds)', type=float)
parser.add_argument('points_per_step', metavar='points per step',
                   help='The number of data points per step when stepping the Gun timing (in seconds)', type=int)
args = parser.parse_args()
settling_time = 0.1 #seconds
#print args.offset0
#print args.step
#print args.time_per_step

###############################################################################
# checks
#if args.offset0*args.step > 0:
#    print 'Offset and step arguments should be opposite signs'
#    exit()
if args.offset0 >= 0:
    print 'Offset should be negative'
    exit()
if args.step <= 0:
    print 'Step should be positive'
    exit()
if args.points_per_step <= 0:
    print 'Points per step should be positive'
    exit()
###############################################################################
#print 'passed'
#exit()


#print offset
#print -args.offset0

###############################################################################
modulatorPVName = 'CLA-C18-TIM-EVR-01:Pul2-Delay-SP'
amplifierPVName = 'CLA-C18-TIM-EVR-01:Pul5-Delay-SP'
>>>>>>> parent of 903bfae1... Added handle_update_individual_trace button to NO-ARCv2 GUI that toggles the updating of individual traces between passive and 10Hz.
llrfPVName = 'CLA-C18-TIM-EVR-02:Pul0-Delay-SP'

modulatorPV = PVObject(modulatorPVName)
modulatorPV.writeAccess = True
amplifierPV = PVObject(amplifierPVName)
amplifierPV.writeAccess = True
llrfPV = PVObject(llrfPVName)
llrfPV.writeAccess = True
print ' Original Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
<<<<<<< HEAD
#397.1 396.46 398.68
modPV0 = 397.1#modulatorPV.value
ampPV0 = 396.46#amplifierPV.value
llrfPV0 = 398.68#llrfPV.value
=======
modPV0 = modulatorPV.value
ampPV0 = amplifierPV.value
llrfPV0 = llrfPV.value

###############################################################################
# to monitor
wcmPVName = 'CLA-S01-DIA-WCM-01:Q'
wcmPV = PVObject(wcmPVName)
wcmPV.writeAccess = True

bpmPVName = 'CLA-C2V-DIA-BPM-01:X'
bpmPV = PVObject(bpmPVName)
bpmPV.writeAccess = True

dip01PVName = 'CLA-C2V-MAG-DIP-01:SETI'
dip01PV = PVObject(dip01PVName)
dip01PV.writeAccess = True


ch3AmpPVName = 'CLA-GUN-LRF-CTRL-01:ad1:ch3:amp_phase.AMP_REMOTE'
ch3AmpPV = PVObject(ch3AmpPVName)
ch3AmpPV.writeAccess = True
ch3PhsPVName = 'CLA-GUN-LRF-CTRL-01:ad1:ch3:amp_phase.PHASE_REMOTE'
ch3PhsPV = PVObject(ch3PhsPVName)
ch3PhsPV.writeAccess = True
ch3PowPVName = 'CLA-GUN-LRF-CTRL-01:ad1:ch3:power_remote.POWER'
ch3PowPV = PVObject(ch3PowPVName)
ch3PowPV.writeAccess = True
ch4AmpPVName = 'CLA-GUN-LRF-CTRL-01:ad1:ch4:amp_phase.AMP_REMOTE'
ch4AmpPV = PVObject(ch4AmpPVName)
ch4AmpPV.writeAccess = True
ch4PhsPVName = 'CLA-GUN-LRF-CTRL-01:ad1:ch4:amp_phase.PHASE_REMOTE'
ch4PhsPV = PVObject(ch4PhsPVName)
ch4PhsPV.writeAccess = True
ch4PowPVName = 'CLA-GUN-LRF-CTRL-01:ad1:ch4:power_remote.POWER'
ch4PowPV = PVObject(ch4PowPVName)
ch4PowPV.writeAccess = True

time_vectorPVName = 'CLA-GUN-LRF-CTRL-01:app:time_vector'
time_vectorPV = PVObject(time_vectorPVName)
time_vectorPV.writeAccess = True
#print ch3AmpPhsPV.__dict__.keys()
#'CLA-GUN-LRF-CTRL-01:ad1:ch3:amp_phase.AMP_REMOTE'
#'CLA-GUN-LRF-CTRL-01:ad1:ch3:amp_phase.PHASE_REMOTE'
#'CLA-GUN-LRF-CTRL-01:ad1:ch3:power_remote.POWER'
#'CLA-GUN-LRF-CTRL-01:ad1:ch4:amp_phase.AMP_REMOTE'
#'CLA-GUN-LRF-CTRL-01:ad1:ch4:amp_phase.PHASE_REMOTE'
#'CLA-GUN-LRF-CTRL-01:ad1:ch4:power_remote.POWER'
#print ch3AmpPhsPV.value
#exit()
tracedict =  {'ch3AmpPV': ch3AmpPV, 'ch3PhsPV': ch3PhsPV, 'ch3PowPV': ch3PowPV, 'ch4AmpPV': ch4AmpPV, 'ch4PhsPV': ch4PhsPV, 'ch4PowPV': ch4PowPV, 'time_vectorPV': time_vectorPV}
for key, value in tracedict.iteritems():
    #print key, value
    file = key+'.txt'
    #print file
    #print item.value
    with open(file, 'w') as f:
        for item in value.value:
            f.write("%s\n" % item)
#exit()
#######################################################################
# Scan offsets and record data
>>>>>>> parent of 903bfae1... Added handle_update_individual_trace button to NO-ARCv2 GUI that toggles the updating of individual traces between passive and 10Hz.

offset = args.offset0
modulatorPV.value = modulatorPV.value + args.offset0
amplifierPV.value = amplifierPV.value + args.offset0
llrfPV.value = llrfPV.value + args.offset0
<<<<<<< HEAD
time.sleep(0.1)
print ' New Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
# raw_input('Centre beam on C2V dipole')
=======
time.sleep(settling_time)
print ' New Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
raw_input('Centre beam on C2V dipole')

while offset < -args.offset0+args.step:
    for i in range(0, args.points_per_step):
        print wcmPV.value, bpmPV.value
        with open(filename, 'a') as f:
            f.write("%f %f %f %f %f %f %f\n" % (offset, modulatorPV.value, amplifierPV.value, llrfPV.value, dip01PV.value, wcmPV.value, bpmPV.value))
        time.sleep(settling_time)
    #print 'stepping', offset, -args.offset0
    offset += args.step
    modulatorPV.value = modulatorPV.value + args.step
    amplifierPV.value = amplifierPV.value + args.step
    llrfPV.value = llrfPV.value + args.step
    time.sleep(settling_time)
    print ' New Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
    raw_input('Centre beam on C2V dipole')


#exit()
modulatorPV.value = modPV0
amplifierPV.value = ampPV0
llrfPV.value = llrfPV0
time.sleep(settling_time)
print ' Final Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
exit()








# print ' Starting Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
# print 'Setting ', args.offset, ' microsecond offset!'
# modulatorPV.value = modulatorPV.value + args.offset
# amplifierPV.value = amplifierPV.value + args.offset
# llrfPV.value = llrfPV.value + args.offset
# time.sleep(0.1)
# print ' New Values = ', modulatorPV.value, amplifierPV.value, llrfPV.value
>>>>>>> parent of 903bfae1... Added handle_update_individual_trace button to NO-ARCv2 GUI that toggles the updating of individual traces between passive and 10Hz.
