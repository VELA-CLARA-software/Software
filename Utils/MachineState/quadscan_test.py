import os, sys
sys.path.append(os.path.abspath(__file__+'/../../../OnlineModel/'))
sys.path.append(os.path.abspath(__file__+'/../../../SimFrame/'))
import machine_state
import CATAP.HardwareFactory
import time
import matplotlib.pyplot as plt

# Get machine state class
machinestate = machine_state.MachineState()

# Set up CATAP
mode = CATAP.HardwareFactory.STATE.VIRTUAL
machinestate.initialiseCATAP(mode)
time.sleep(1)

# Get the dictionary containing all CATAP hardware objects
catapdict = machinestate.getCATAPDict(mode)
get_data_from_catap = machinestate.getDataFromCATAP


# Switch on magnets in VM
for name in catapdict['Magnet'].keys():
    catapdict['Magnet'][name].switchOn()

# Switch on RF
catapdict['L01'].setAmpMW(20 * 10 ** 6)

catapdict['LRRG_GUN'].setAmpMW(9.9 * 10 ** 6)


# Don't know if this is necessary
time.sleep(4)

# Returns the machine state dictionary from CATAP
catapdata = machinestate.getMachineStateFromCATAP(mode)
time.sleep(1)

# Saves the machine state to a .yml file
machinestate.exportParameterValuesToYAMLFile("catap-test.yaml",catapdata)

# Set up simframe
machinestate.getMachineStateFromSimFrame('test','Lattices/CLA-S02.def')
time.sleep(1)
machinestate.initialiseSimFrameData()
simframedata = machinestate.getSimFrameDataDict()
framework = machinestate.getFramework()

# Read in machine state .yml file. (Obviously you can do this directly from line 35 above)
machinestatefile = machinestate.parseParameterInputFile("catap-test.yaml")

# Set up lattice end point (default is to start at generator, at the moment we have to do it this way)
machinestate.updateLatticeEnd(machinestatefile, 'CLA-S02')

catapdata = machinestate.getMachineStateFromCATAP(mode)
    # We have to fudge this for now as the conversion between current and solenoid strength doesn't work
catapdata['INJ']['CLA-LRG1-MAG-SOL-01'].update({'field_amplitude': 0.255})
catapdata['INJ']['CLA-LRG1-MAG-BSOL-01'].update({'field_amplitude': -0.07})
# # Write machine state dictionary to simframe and runs simulation
simframefileupdate = machinestate.writeMachineStateToSimFrame('injector', framework,
                                                              'Lattices/CLA-S02.def', datadict=catapdata,
                                                              run=True, type='CATAP',
                                                              sections=['INJ', 'CLA-S01', 'L01'])
# Use the output from this simulation as input for the quad scan
file_path = os.getcwd()
framework['CLA-S02'].prefix = '../injector/'
#
# Quad settings
quadsettings = [-15,-10,0]

# Dict for beam size at s02-cam-02
s02cam02xsig = {}

lattice_start = 'CLA-S02'# machinestate.updateLatticeStart(catapdata, 'CLA-S02')
lattice_end = 'CLA-S02'# machinestate.updateLatticeEnd(catapdata, 'CLA-S02')

# Iterate over quad settings
for i in quadsettings:
    # Set magnet current; we need to check that read current ~= set current
    catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].SETI(i)
    ri_tol = catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].getREADITolerance()
    while (i - ri_tol) < catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].getREADI() < (i + ri_tol):
        time.sleep(0.1)
    # Get updated machine state from CATAP; we update the start and end so that it only runs the simulation in CLA-S02
    catapdata = machinestate.getMachineStateFromCATAP(mode, start_lattice=lattice_start, final_lattice=lattice_end)
    # We have to fudge this for now as the conversion between current and solenoid strength doesn't work
    # Write machine state dictionary to simframe and runs simulation
    simframefileupdate = machinestate.writeMachineStateToSimFrame('quadscan_test'+str(i), framework,
                                                                  'Lattices/CLA-S02.def', datadict=catapdata,
                                                                  run=True, type='CATAP', sections=['CLA-S02'])
    # Exports machine state from simframe (hardware settings and simulated data @ screens / bpms)
    machinestate.exportParameterValuesToYAMLFile("simframe-test"+str(i)+".yaml",simframefileupdate)
    # Update dictionary of beam size
    s02cam02xsig.update({i: simframefileupdate['CLA-S02']['CLA-S02-DIA-CAM-03']['x_sigma']})

print(s02cam02xsig.items())

# Plot beam size vs. quad settings
lists = sorted(s02cam02xsig.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.plot(x, y)
plt.show()