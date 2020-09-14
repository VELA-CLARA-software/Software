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

for i in range(1,4):
    mag_name = 'CLA-S02-MAG-QUAD-0' + str(i)
    mag_names.append(mag_name)
    catapdict['Magnet'][mag_name].switchOn()
    time.sleep(1)
    catapdict['Magnet'][mag_name].SETI(-i)

# Returns the machine state dictionary from CATAP
catapdata = machinestate.getMachineStateFromCATAP(mode)
time.sleep(1)

for i in mag_names:
    print(i)
    print(catapdict['Magnet'][i].READI)
    unitconversion.currentToK(catapdata['CLA-S02'][i]['type'],
                                    catapdict['Magnet'][i].READI,
                                    catapdict['Magnet'][i].getFieldIntegralCoefficients(),
                                    catapdict['Magnet'][i].magnetic_length,
                                    catapdata['CLA-S02'][i]['energy'],
                                    catapdata['CLA-S02'][i])
    x=unitconversion.kToCurrent(catapdata['CLA-S02'][i]['type'],
                                    catapdata['CLA-S02'][i]['k1'],
                                    catapdict['Magnet'][i].getFieldIntegralCoefficients(),
                                    catapdict['Magnet'][i].magnetic_length,
                                    catapdata['CLA-S02'][i]['energy'])
