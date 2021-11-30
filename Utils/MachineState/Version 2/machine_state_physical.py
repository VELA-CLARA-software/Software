import os, sys
sys.path.append(os.path.join(sys.path[0],'src'))
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\packages\\CATAP\\bin')
# sys.path.append('E:\\CATAP-build\\PythonInterface\\Release\\CATAP')
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\test\\SimFrame')
import src.machine_state as machine_state
from CATAP.HardwareFactory import *
import time

# Get machine state class
machinestate = machine_state.MachineState()

gun_name = 'CLA-LRG1-GUN-CAV'
l01_name = 'CLA-L01-CAV'

crest_phases = {}
crest_phases.update({gun_name: 8.2})
crest_phases.update({l01_name: -117})

# Set up CATAP
mode = STATE.PHYSICAL
machinestate.initialiseCATAP(mode, crest_phases=crest_phases)
time.sleep(1)

# Get the dictionary containing all CATAP hardware objects (used for controlling and monitoring the machine)
catapdict = machinestate.getCATAPDict(mode)

# Returns the machine state dictionary from CATAP
catapdata = machinestate.getMachineStateFromCATAP(mode)
time.sleep(1)
#
# # We have to set some values manually, since we don't know crest phase or RF centre
# catapdata['INJ']['CLA-GUN-LRF-CTRL-01']['phase'] = 0 # INSERT YOUR PHASE RELATIVE TO CREST
# catapdata['L01']['L01']['phase'] = 0 # INSERT YOUR PHASE RELATIVE TO CREST
# catapdata['VCA']['CLA-VCA-DIA-CAM-01']['x_mm'] = 0 # INSERT THE POSITION ON VIRTUAL CATHODE RELATIVE TO RF CENTRE
# catapdata['VCA']['CLA-VCA-DIA-CAM-01']['y_mm'] = 0 # INSERT THE POSITION ON VIRTUAL CATHODE RELATIVE TO RF CENTRE

# Saves the physical machine state to a .yml file
machinestate.exportParameterValuesToYAMLFile("catap-test.yaml",catapdata)

# # Reads the machine state file
# machinestatefile = machinestate.parseParameterInputFile("catap-test.yaml")

# # Set the end point of the simulation (by machine area)
# machinestate.updateLatticeEnd(machinestatefile, 'CLA-C2V')

# # Set up simframe
# machinestate.getMachineStateFromSimFrame('test','Lattices/CLA10-BA1_OM.def')
# time.sleep(1)
# machinestate.initialiseSimFrameData()
# simframedata = machinestate.getSimFrameDataDict()
# framework = machinestate.getFramework()

# # We have to fudge this for now as the conversion between current and solenoid strength doesn't work
# catapdata['INJ']['CLA-GUN-MAG-SOL-02'].update({'field_amplitude': 0.255})
# catapdata['INJ']['CLA-LRG1-MAG-SOL-01'].update({'field_amplitude': -0.07})

# # # Write machine state dictionary to simframe and runs simulation to the 'test' directory
# simframefileupdate = machinestate.writeMachineStateToSimFrame('test', framework,
                                                              # 'Lattices/CLA10-BA1_OM.def', datadict=catapdata,
                                                              # run=True, type='CATAP',
                                                              # sections=['INJ', 'CLA-S02', 'CLA-C2V'])

# # Saves the machine state from the simulation to a .yml file
# machinestate.exportParameterValuesToYAMLFile("simframe-test.yaml", simframefileupdate)