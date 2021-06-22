import sys, os, random, time

sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\development\\CATAP\\djs56\\new_pc\\build\\PythonInterface\\Release\\CATAP')
from CATAP.Shutter import *
from CATAP.EPICSTools import *

run_state = STATE.PHYSICAL
test_passed = True

ET = EPICSTools(STATE.PHYSICAL)


### TESTING VIRTUAL BPM FUNCTIONS ####
shf = ShutterFactory(run_state)
shf.messagesOff()
shf.debugMessagesOff()
shf.setup("")

sh1 = 'EBT-INJ-LSR-SHUT-01'
sh2 = 'EBT-INJ-LSR-SHUT-02'

sh_list = [sh1, sh2]

for name in sh_list:
    print(name)
    print(shf.getState(name)
    if shf.isOpen(name):
        shf.close(name)
        time.sleep(1)
        print(shf.getState(name))
    if shf.isClosede(name):
        shf.open(name)
        time.sleep(1)
        print(shf.getState(name))
   
for name in BPM_names:
    bpm = BPMF.getBPM(name)
    try:
        assert(bpm.x == ET.get(name+":X"))
    except AssertionError:
        test_passed = False
        print("{BPM}:X Did not get set properly. Test failed :(".format(BPM = name))
        sys.exit()

### TESTING VIRTUAL CHARGE FUNCTIONS ####

CF = ChargeFactory(run_state)
CF.messagesOff()
CF.debugMessagesOff()
CF.setup("")
charge_names = CF.getAllChargeDiagnosticNames()
charge = 75.0

for name in charge_names:
    diagnostic = CF.getChargeDiagnostic(name)
    diagnostic.q = charge

for name in charge_names:
    diagnostic = CF.getChargeDiagnostic(name)
    try:
        assert(diagnostic.q == ET.get(name+":Q"))
    except AssertionError:
        test_passed = False
        print("{diagnostic}:Q Did not get set properly. Test failed :(".format(diagnostic = name))
        sys.exit()

#### TESTING VIRTUAL MAGNET FUNCTIONS ####
MF = MagnetFactory(run_state)
MF.messagesOff()
MF.debugMessagesOff()
MF.setup("")
magnet_names = MF.getAllMagnetNames()
for name in magnet_names:
    magnet = MF.getMagnet(name)
    try:
        assert(isinstance(magnet.position, float))
        assert(isinstance(magnet.magnetic_length, float))
        assert(isinstance(magnet.getFieldIntegralCoefficients(), list))
    except AssertionError:
        test_passed = False
        print("{magnet} did not get set properly. Test failed :(".format(magnet = name))
        sys.exit()


if test_passed:
    print("All tests passed :) ")
    input()
else:
    print("Some tests failed.. try again")
    input()
