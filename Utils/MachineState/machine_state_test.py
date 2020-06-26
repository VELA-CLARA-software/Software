import os, sys
sys.path.append(os.path.abspath(__file__+'/../../../OnlineModel/'))
sys.path.append(os.path.abspath(__file__+'/../../../SimFrame/'))
import machine_state
import CATAP.HardwareFactory
import time

machinestate = machine_state.MachineState()

mode = CATAP.HardwareFactory.STATE.VIRTUAL

machinestate.initialiseCATAP(mode)
print(1)
time.sleep(1)

catapdict = machinestate.getCATAPDict(mode)

for name in catapdict['Magnet'].keys():
    catapdict['Magnet'][name].switchOn()

time.sleep(4)

# catapdict['Magnet']['CLA-LRG1-MAG-SOL-01'].SETI(150)
# catapdict['Magnet']['CLA-LRG1-MAG-BSOL-01'].SETI(-130)
#
# time.sleep(4)
#
# catapdata = machinestate.getMachineStateFromCATAP(mode)
# time.sleep(1)
#
# machinestate.exportParameterValuesToYAMLFile("catap-test.yaml",catapdata)
# #
machinestate.getMachineStateFromSimFrame('test','Lattices/CLA10-BA1_OM.def')
# # # # print(1)
# # # # time.sleep(1)
# machinestate.initialiseSimFrameData()
# simframedata = machinestate.getSimFrameDataDict()
# # # print(2)
# machinestate.exportParameterValuesToYAMLFile("simframe-test.yaml",simframedata)
# #
framework = machinestate.getFramework()
# #
#
machinestatefile = machinestate.parseParameterInputFile("catap-test.yaml")

machinestate.updateLatticeEnd(machinestatefile, 'C2V')

quadsettings = [0]

s02cam02xsig = {}

for i in quadsettings:
    machinestatefile['S02']['CLA-S02-MAG-QUAD-01'].update({'k1l': i})
    simframefileupdate = machinestate.writeMachineStateToSimFrame('quadscan_test'+str(i), framework, 'Lattices/CLA10-BA1_OM.def', datadict=machinestatefile, run=True)
    machinestate.exportParameterValuesToYAMLFile("simframe-test"+str(i)+".yaml",simframefileupdate)
    s02cam02xsig.update({i: simframefileupdate['S02']['CLA-S02-DIA-CAM-02']['x_sigma']})

print(s02cam02xsig.items())
#
# machinestatefile = machinestate.parseParameterInputFile("simframe-test.yaml")
#
# machinestate.writeMachineStateToCATAP(mode, machinestatefile, os.path.join(os.getcwd(), 'test'))