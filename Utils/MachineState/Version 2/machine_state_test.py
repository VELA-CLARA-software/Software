import os, sys
sys.path.append(os.path.abspath(__file__+'/srs/'))
#sys.path.append(os.path.abspath(__file__+'/../../../OnlineModel/'))
#sys.path.append(os.path.abspath(__file__+'/../../../SimFrame/'))
import src.machine_state
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

catapdict['Magnet']['CLA-LRG1-MAG-SOL-01'].SETI(150)
catapdict['Magnet']['CLA-LRG1-MAG-BSOL-01'].SETI(-130)

time.sleep(4)

catapdata = machinestate.getMachineStateFromCATAP(mode)
time.sleep(1)

machinestate.exportParameterValuesToYAMLFile("catap-test.yaml",catapdata)
# #
# machinestate.getMachineStateFromSimFrame('test','Lattices/CLA10-BA1_OM.def')
# # # # # print(1)
# # # # # time.sleep(1)
# machinestate.initialiseSimFrameData()
# simframedata = machinestate.getSimFrameDataDict()
# # # print(2)
# machinestate.exportParameterValuesToYAMLFile("simframe-test.yaml",simframedata)
# # #
# framework = machinestate.getFramework()
# # #
# #
# machinestatefile = machinestate.parseParameterInputFile("simframe-test.yaml")
#
# machinestate.updateLatticeEnd(machinestatefile, 'INJ')
#
# simframefileupdate = machinestate.writeMachineStateToSimFrame('test', framework,
#                                                               'Lattices/CLA10-BA1_OM.def', datadict=machinestatefile,
#                                                               run=True)