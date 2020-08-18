[4:15 PM] Castaneda Cortes, Hector Mauricio (STFC,DL,AST)
    

def quad_scan(self,rows,catapdict, currents_array):
    """
:parameter catapdict: Dictionary with all the PVs extracted from CATAP
:parameter currents_array: Dictionary of optimised quad currents
:return    """
for i_currents, currents in enumerate(currents_array):
        catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].SETI(currents)
        ri_tol = catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].getREADITolerance()
        while (currents - ri_tol) < catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].getREADI() < (
                currents + ri_tol):
            time.sleep(0.1)
        print('CLA-S02-MAG-QUAD-0' + str(i_currents + 1), currents, catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].getREADI())
        time.sleep(2)
        self.machinestate.exportParameterValuesToYAMLFile(
            os.path.abspath(os.path.join(os.getcwd(), "test","catap-test_quad_"+str(rows)+".yaml")),self.machinestate.getMachineStateFromCATAP(self.mode))

