import sys, os
import numpy
import src.unit_conversion as unit_conversion
import src.aliases as aliases

# Class for writing machine state data to CATAP
class WriteDataToCATAP(object):

    def __init__(self):
        object.__init__(self)
        self.my_name = "WriteDataToCATAP"
        self.unitConversion = unit_conversion.UnitConversion()
        self.diagnosticTypes = ['bpm', 'charge', 'camera', 'pil']
        self.magnettypes = ['quadrupole', 'solenoid', 'kicker', 'dipole']
        self.lattices = ['BA1', 'INJ', 'S01', 'S02', 'L01', 'C2V']
        self.bsol_alias = aliases.bsol_alias
        self.screen_alias = aliases.screen_alias
        self.gun_kly_fwd_power_max = aliases.gun_kly_fwd_power_max
        self.gun_pulse_length = 2.5
        self.linac_pulse_length = 0.75
        self.unitConversion = unit_conversion.UnitConversion()
        self.energy = {}
        self.gun_position = 0.17  # MAGIC NUMBER (BUT IT WON'T CHANGE)
        self.l01_position = 3.2269  # MAGIC NUMBER (BUT IT WON'T CHANGE)

    # Calculates the energy at all of the magnets in inputdict based on a dictionary of energy values
    # See WriteDataToSimFrame.getLLRFEnergyGain() and WriteDataToSimFrame.getEnergyDict()
    def getEnergyAtMagnet(self, inputdict, energy):
        for key, value in inputdict.items():
            if isinstance(inputdict[key], dict):
                if 'type' in inputdict[key].keys():
                    if (value['type'] in self.magnettypes):
                        self.energy_at_magnet = 0
                        if ("GUN" in key) or ("LRG1" in key):
                            self.energy_at_magnet = energy[self.gun_position]
                        else:
                            for k, v in energy.items():
                                if k < value['position']:
                                    self.energy_at_magnet += v
                        if self.energy_at_magnet == 0:
                            self.energy_at_magnet = energy[self.l01_position]
                        inputdict[key].update({'energy': self.energy_at_magnet})

    # Write the charge value to all CATAP charge PVs. The simulation does not incorporate beam loss,
    # so the charge is the same everywhere
    def writeCharge(self, q, catap):
        if not self.charge_written:
            for key in catap['Charge'].keys():
                catap['Charge'][key].q = q

    # Main function for writing data from SimFrame to CATAP.
    # Inputs: mode: CATAP STATE: physical or virtual
    #         datadict: the machine state file w/ simulation inputs/outputs  (see MachineState.parseParameterInputFile())
    #         allbeamfiles: simulated beam distributions at screens (see WriteDataToSimFrame.getAllBeamFiles())
    #         catap: main CATAP dict with all hardware objects (see getDataFromCATAP.setAllDicts())
    #         energy: energy dictionary (see WriteDataToSimFrame.getEnergyDict())
    def writeMachineStateToCATAP(self, mode, datadict, allbeamfiles, catap, energy):
        self.charge_written = False
        self.getEnergyAtMagnet(datadict, energy)
        for key, value in datadict.items():
            # if value['type'] in self.diagnosticTypes:
            if isinstance(value, dict):
                if 'type' in value.keys():
                    if value['type'] == 'camera':
                        if (value['screen'] in allbeamfiles.keys()):
                            datadict[key]['x'] = allbeamfiles[value['screen']]['x']['mean']
                            datadict[key]['y'] = allbeamfiles[value['screen']]['y']['mean']
                            datadict[key]['x_dist'] = allbeamfiles[value['screen']]['x']['dist']
                            datadict[key]['y_dist'] = allbeamfiles[value['screen']]['y']['dist']
                            datadict[key]['x_sigma'] = allbeamfiles[value['screen']]['x']['sigma']
                            datadict[key]['y_sigma'] = allbeamfiles[value['screen']]['y']['sigma']
                            catap['Camera'][key].setX(datadict[key]['x'])
                            catap['Camera'][key].setY(datadict[key]['y'])
                            catap['Camera'][key].setSigX(datadict[key]['x_sigma'])
                            catap['Camera'][key].setSigY(datadict[key]['y_sigma'])
                    if value['type'] == 'bpm':
                        if key in allbeamfiles.keys():
                            datadict[key]['x'] = allbeamfiles[key]['x']['mean']
                            datadict[key]['y'] = allbeamfiles[key]['y']['mean']
                            catap['BPM'][key].x = datadict[key]['x']
                            catap['BPM'][key].y = datadict[key]['y']
                            self.q = allbeamfiles[key]['q']['total']
                            self.writeCharge(self.q, catap)
                            self.charge_written = True
                    if value['type'] == 'cavity':
                        phase = value['phase']
                        field_amplitude = value['field_amplitude']
                        length = value['length']
                        pulse_length = value['pulse_length']
                        if ("GUN" in value['catap_alias']):
                            pulse_length = 2.5
                        elif ("L01" in value['catap_alias']):
                            pulse_length = 0.75
                        forward_power = self.unitConversion.getPowerFromFieldAmplitude(value['catap_alias'],
                                                                                       field_amplitude,
                                                                                       phase,
                                                                                       pulse_length,
                                                                                       length)
                        if ("GUN" in value['catap_alias']):
                            if forward_power > self.gun_kly_fwd_power_max:
                                forward_power = self.gun_kly_fwd_power_max
                        catap[value['catap_alias']].setAmpMW(forward_power)
                        catap[value['catap_alias']].setPhiDEG(phase)
                    if value['type'] in self.magnettypes:
                        self.combined_kicker = False
                        if value['psu_state'] == "ON":
                            if ('Horizontal_PV' in value.keys()):
                                catap['Magnet'][value['Horizontal_PV']].switchOn()
                                catap['Magnet'][value['Vertical_PV']].switchOn()
                        if value['type'] == 'solenoid':
                            strength = value['field_amplitude']
                        elif value['type'] == 'dipole':
                            strength = value['angle']
                        elif (value['type'] == 'kicker'):
                            break
                            # if ('Horizontal_PV' in value.keys()):
                            #     vstrength = value['vangle']
                            #     hstrength = value['hangle']
                            #     self.combined_kicker = True
                            # else:
                            #     strength = value['angle']
                        elif value['type'] == 'quadrupole':
                            strength = value['k1']
                        if self.combined_kicker:
                            vcurrent = self.unitConversion.kToCurrent(value['type'],
                                                                      vstrength,
                                                                      catap[value[
                                                                          'Vertical_PV']].field_integral_coefficients,
                                                                      catap[value['Vertical_PV']].magnetic_length,
                                                                      value['energy'])
                            hcurrent = self.unitConversion.kToCurrent(value['type'],
                                                                      hstrength,
                                                                      catap[value[
                                                                          'Horizontal_PV']].field_integral_coefficients,
                                                                      catap[value['Horizontal_PV']].magnetic_length,
                                                                      value['energy'])
                            catap['Magnet'][value['Horizontal_PV']].SETI(hcurrent)
                            catap['Magnet'][value['Vertical_PV']].SETI(vcurrent)
                        else:
                            current = self.unitConversion.kToCurrent(value['type'],
                                                                     strength,
                                                                     value['field_integral_coefficients'],
                                                                     value['magnetic_length'],
                                                                     value['energy'])
                            if 'bsol' in value.keys():
                                if value['bsol']:
                                    catap['Magnet'][self.bsol_alias[key]].SETI(current)
                            else:
                                catap['Magnet'][key].SETI(current)
            # if value['type'] == "screen":
            #     datadict[key].state = value['state']
