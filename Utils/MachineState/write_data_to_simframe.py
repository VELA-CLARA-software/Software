import os
import time
import unit_conversion
import aliases
import numpy
class WriteDataToSimFrame(object):

    def __init__(self):
        object.__init__(self)
        self.my_name = "WriteDataToSimFrame"
        self.unitConversion = unit_conversion.UnitConversion()
        self.energy = {}
        self.gun_pulse_length = self.unitConversion.getDefaultGunPulseLength()
        self.l01_pulse_length = self.unitConversion.getDefaultL01PulseLength()
        self.gun_position = self.unitConversion.getGunPosition()
        self.l01_position = self.unitConversion.getL01Position()
        self.lattices = self.unitConversion.getLattices()

    def updateFrameworkElements(self, framework, inputdict):
        for section in self.lattices:
            for key, value in inputdict[section].items():
                if (isinstance(value, dict)):
                    if 'simframe_alias' in inputdict[section][key].keys():
                        self.keymod = inputdict[section][key]['simframe_alias']
                    else:
                        self.keymod = key
                    if not framework.getElement(self.keymod) == {}:
                        if inputdict[section][key]['type'] == 'quadrupole':
                            framework.modifyElement(self.keymod, 'k1l', float(value['k1l']))
                        elif inputdict[section][key]['type'] == 'cavity':
                            framework.modifyElement(self.keymod, 'field_amplitude', float(value['field_amplitude']))
                            framework.modifyElement(self.keymod, 'phase', value['phase'])
                        elif inputdict[section][key]['type'] == 'solenoid':
                            if 'BSOL' in key:
                                framework.modifyElement(self.keymod, 'field_amplitude', 0.3462 * float(value['field_amplitude']))
                            else:
                                framework.modifyElement(self.keymod, 'field_amplitude', float(value['field_amplitude']))

    def getEnergyDict(self):
        return self.energy

    def getLLRFEnergyGain(self, inputdict):
        for section in self.lattices:
            for key, value in inputdict[section].items():
                if ('GUN' in key) and (value['type'] == 'cavity'):
                    value.update({'pulse_length': self.gun_pulse_length})
                    self.getenergy = self.unitConversion.getEnergyGain(key,
                                                                       float(value['field_amplitude']),
                                                                       float(value['phase']),
                                                                       self.gun_pulse_length,
                                                                       float(value['length']))
                    self.energy.update({self.gun_position: self.getenergy[0]})
                elif ('L01' in key) and (value['type'] == 'cavity'):
                    value.update({'pulse_length': self.l01_pulse_length})
                    self.getenergy = self.unitConversion.getEnergyGain(key,
                                                                       float(value['field_amplitude']),
                                                                       float(value['phase']),
                                                                       self.l01_pulse_length,
                                                                       float(value['length']))
                    self.energy.update({self.l01_position: self.getenergy[0]})

    def modifyFramework(self, framework, inputdict, scan=False, type=None, source=None, modify=None, cavity_params=None, generator_param=None):
        if not os.name == 'nt':
            framework.defineASTRACommand(scaling=int(inputdict['generator']['number_of_particles']['value']))
            framework.defineCSRTrackCommand(scaling=int(inputdict['generator']['number_of_particles']['value']))
            framework.define_gpt_command(scaling=int(inputdict['generator']['number_of_particles']['value']))

        if inputdict['simulation']['bsol_tracking']:
            famp = float(framework['CLA-LRG1-MAG-SOL-01']['field_amplitude'])
            framework.modifyElement('CLA-LRG1-MAG-BSOL-01', 'field_amplitude', float(0.3462 * 0.9 * famp))
        if scan==True and type is not None:
            print(inputdict[dictname][pv])
        framework.generator.number_of_particles = int(inputdict['generator']['number_of_particles']['value'])
        framework.generator.charge = float(inputdict['generator']['charge']['value'] * 1e-12)
        framework.generator.sig_clock = float(inputdict['generator']['sig_clock']['value'])
        # framework.generator.sig_clock = float(inputdict['generator']['sig_clock']['value']) / (2354.82)
        framework.generator.sig_x = inputdict['generator']['sig_x']['value']
        framework.generator.sig_y = inputdict['generator']['sig_y']['value']
        framework.generator.spot_size = float(numpy.mean([inputdict['generator']['sig_x']['value'],inputdict['generator']['sig_y']['value']]))
        self.updateFrameworkElements(framework, inputdict)

    def runScript(self, framework, inputdict, modify=False, track=False):
        self.update_tracking_codes(framework, inputdict)
        self.update_CSR(framework, inputdict)
        self.update_LSC(framework, inputdict)
        startLattice = inputdict['simulation']['starting_lattice']
        endLattice = inputdict['simulation']['final_lattice']
        framework.setSubDirectory(str(inputdict['simulation']['directory']))
        if modify == True:
            self.modifyFramework(framework, inputdictscan=False)
        framework.save_changes_file(filename=framework.subdirectory+'/changes.yaml')
        if inputdict['simulation']['track'] or track==True:
            framework.track(startfile=startLattice, endfile=endLattice)
        else:
            time.sleep(0.5)

    def update_tracking_codes(self, framework, inputdict):
        for l, c in inputdict['simulation']['tracking_code'].items():
            framework.change_Lattice_Code(l, c)

    def update_CSR(self, framework, inputdict):
        for l, c in inputdict['simulation']['csr'].items():
            lattice = framework[l]
            elements = lattice.elements.values()
            for e in elements:
                e.csr_enable = c
                e.sr_enable = c
                e.isr_enable = c
                e.csr_bins = inputdict['simulation']['csr_bins'][l]
                e.current_bins = 0
                e.longitudinal_wakefield_enable = c
                e.transverse_wakefield_enable = c
            lattice.csrDrifts = c

    def update_LSC(self, framework, inputdict):
        for l, c in inputdict['simulation']['lsc'].items():
            lattice = framework[l]
            elements = lattice.elements.values()
            for e in elements:
                e.lsc_enable = c
                e.lsc_bins = inputdict['simulation']['lsc_bins'][l]
            #     e.smoothing_half_width = 1
            #     e.lsc_high_frequency_cutoff_start = -1#0.25
            #     e.lsc_high_frequency_cutoff_end = -1#0.33
            # lattice.lsc_high_frequency_cutoff_start = -1#0.25
            # lattice.lsc_high_frequency_cutoff_end = -1#0.33
            lattice.lsc_bins = inputdict['simulation']['lsc_bins'][l]
            lattice.lscDrifts = c

    def setEnergyAtElement(self, inputdict):
        if "GUN" in name or "LRG1" in name:
            self.energy_at_magnet = energy[self.gun_position]
        else:
            for key, value in energy.items():
                if key < inputdict[name].position:
                    self.energy_at_magnet += value
        if self.energy_at_magnet == 0:
            self.energy_at_magnet = energy[self.l01_position]