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
catapdata = machinestate.getMachineStateFromCATAP(mode)
time.sleep(1)
print(2)
machinestate.exportParameterValuesToYAMLFile("catap-test.yaml",catapdata)
#
# machinestate.getMachineStateFromSimFrame('test','Lattices/CLA10-BA1_OM.def')
# print(1)
# time.sleep(1)
# machinestate.initialiseSimFrameData()
# simframedata = machinestate.getSimFrameDataDict()
# print(2)
# machinestate.exportParameterValuesToYAMLFile("simframe-test.yaml",simframedata)
#
# framework = machinestate.getFramework()
# #
#
# machinestatefile = machinestate.parseParameterInputFile("catap-test.yaml")
#
# machinestate.writeMachineStateToSimFrame('test', framework, 'Lattices/CLA10-BA1_OM.def', datadict=machinestatefile, run=True)
#
machinestatefile = machinestate.parseParameterInputFile("catap-test.yaml")

machinestate.writeMachineStateToCATAP(mode, machinestatefile, os.path.join(os.getcwd(), 'test'))