import sys, os
import numpy
import unit_conversion

class WriteDataToCATAP(object):

    def __init__(self):
        object.__init__(self)
        self.my_name = "WriteDataToCATAP"
        self.unitConversion = unit_conversion.UnitConversion()
        self.diagnosticTypes = ['bpm', 'charge', 'camera', 'pil']
        self.magnettypes = ['quadrupole', 'solenoid', 'kicker', 'dipole']

    def writeMachineStateToCATAP(self, mode, datadict, allbeamfiles, catap):
        for key, value in datadict.items():
            # if value['type'] in self.diagnosticTypes:
            if isinstance(value, dict):
                if 'type' in value.keys():
                    if value['type'] == 'bpm':
                        if key in allbeamfiles.keys():
                            datadict[key]['x'] = allbeamfiles[key]['x']['mean']
                            datadict[key]['y'] = allbeamfiles[key]['y']['mean']
                            catap['BPM'][key].x = datadict[key]['x']
                            catap['BPM'][key].y = datadict[key]['y']
                    # if value['type'] == 'charge':
                    #     datadict[key]['q'] = allbeamfiles[key]['q']
                    #     catap['Charge'][key].q = datadict[key]['q']
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
                            if forward_power > 9.9 * 10 ** 6:
                                forward_power = 9.9 * 10 ** 6
                        catap[key].setAmpMW(forward_power)
                        catap[key].setPhiDEG(phase)
                    if value['type'] in self.magnettypes:
                        self.combined_kicker = False
                        if value['psu_state'] == "ON":
                            catap[key].switchOn()
                        if value['type'] == 'solenoid':
                            strength = value['field_amplitude']
                        elif value['type'] == 'dipole':
                            strength = value['angle']
                        elif (value['type'] == 'kicker'):
                            if ('Horizontal_PV' in value.keys()):
                                vstrength = value['vangle']
                                hstrength = value['hangle']
                                self.combined_kicker = True
                            else:
                                strength = value['angle']
                        elif value['type'] == 'quadrupole':
                            strength = value['k1l']
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
                            catap['Magnet'][key].SETI(current)
            # if value['type'] == "screen":
            #     datadict[key].state = value['state']
