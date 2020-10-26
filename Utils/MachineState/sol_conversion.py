import os, sys
sys.path.append(os.path.abspath(__file__+'/../../../../../simframe/'))
# sys.path.append(os.path.abspath(__file__+'/../../../SimFrame/'))
import machine_state
import CATAP.HardwareFactory
import unit_conversion
import time

# Get machine state class
machinestate = machine_state.MachineState()

unitconversion = unit_conversion.UnitConversion()

# Set up CATAP
mode = CATAP.HardwareFactory.STATE.VIRTUAL
machinestate.initialiseCATAP(mode)
time.sleep(1)

# Get the dictionary containing all CATAP hardware objects
catapdict = machinestate.getCATAPDict(mode)
get_data_from_catap = machinestate.getDataFromCATAP

mag_names = []

catapdict['L01'].setAmpMW(20 * 10 ** 6)

catapdict['LRRG_GUN'].setAmpMW(9.9 * 10 ** 6)


# Returns the machine state dictionary from CATAP
catapdata = machinestate.getMachineStateFromCATAP(mode)
time.sleep(1)

mag_name = 'CLA-LRG1-MAG-SOL-01'

catapdict['Magnet'][mag_name].SETI(100)
time.sleep(2)

print(mag_name)
print(catapdict['Magnet'][mag_name].READI)
unitconversion.currentToK(catapdata['INJ'][mag_name]['type'],
                                catapdict['Magnet'][mag_name].READI,
                                catapdict['Magnet'][mag_name].getFieldIntegralCoefficients(),
                                catapdict['Magnet'][mag_name].magnetic_length,
                                catapdata['INJ'][mag_name]['energy'],
                                catapdata['INJ'][mag_name])
print(catapdata['INJ'][mag_name]['field_amplitude'])
