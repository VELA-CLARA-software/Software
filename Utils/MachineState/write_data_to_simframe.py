import os
import time

class WriteDataToSimFrame(object):

    def __init__(self):
        object.__init__(self)
        self.my_name = "WriteDataToSimFrame"
        self.lattices = ['BA1', 'INJ', 'S01', 'S02', 'L01', 'C2V']

    def updateFrameworkElements(self, framework, inputdict):
        for lattice in self.lattices:
            for key, value in inputdict[lattice].items():
                if isinstance(value, dict):
                    if 'simframe_alias' in inputdict[lattice][key].keys():
                        self.keymod = inputdict[lattice][key]['simframe_alias']
                    else:
                        self.keymod = key
                    if inputdict[lattice][key]['type'] == 'quadrupole':
                        framework.modifyElement(self.keymod, 'k1l', float(value['k1l']))
                    elif inputdict[lattice][key]['type'] == 'cavity':
                        framework.modifyElement(self.keymod, 'field_amplitude', 1e6*float(value['field_amplitude']))
                        framework.modifyElement(self.keymod, 'phase', value['phase'])
                    elif inputdict[lattice][key]['type'] == 'solenoid':
                        if 'BSOL' in key:
                            framework.modifyElement(self.keymod, 'field_amplitude', 0.3462 * float(value['field_amplitude']))
                        else:
                            framework.modifyElement(self.keymod, 'field_amplitude', float(value['field_amplitude']))

    def modifyFramework(self, framework, inputdict, scan=False, type=None, modify=None, cavity_params=None, generator_param=None):
        if not os.name == 'nt':
            framework.defineASTRACommand(scaling=int(inputdict['generator']['number_of_particles']['value']))
            framework.defineCSRTrackCommand(scaling=int(inputdict['generator']['number_of_particles']['value']))
            framework.define_gpt_command(scaling=int(inputdict['generator']['number_of_particles']['value']))

        self.updateFrameworkElements(framework, inputdict)
        if inputdict['simulation']['bsol_tracking']:
            framework.modifyElement('CLA-LRG1-MAG-BSOL-01', 'field_amplitude', 0.3462 * 0.9 * framework['CLA-LRG1-MAG-SOL-01']['field_amplitude'])
        if scan==True and type is not None:
            print(inputdict[dictname][pv])
        framework.generator.number_of_particles = int(inputdict['generator']['number_of_particles']['value'])
        framework.generator.charge = 1e-9*float(inputdict['generator']['charge']['value'])
        framework.generator.sig_clock = float(inputdict['generator']['sig_clock']['value']) / (2354.82)
        framework.generator.sig_x = inputdict['generator']['sig_x']['value']
        framework.generator.sig_y = inputdict['generator']['sig_y']['value']

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