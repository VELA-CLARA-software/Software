import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__)))))
from SimulationFramework.Framework import *
from SimulationFramework.FrameworkHelperFunctions import *
# sys.path.append('../../ElegantWriter')
from ELEGANT.ElegantWriter.elegantWriter_objects import *
import SimulationFramework.Modules.read_beam_file as rbf
import sdds

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return OrderedDict(z)

class Elegant(object):

    beam = rbf.beam()

    def __init__(self, framework=None, directory='test'):
        super(Elegant, self).__init__()
        self.subdir = directory
        self.framework = framework
        self.elegantCommand = ['elegant']

    type_conversion_rules = {'dipole': 'csrcsbend', 'quadrupole': 'kquad', 'beam_position_monitor': 'moni', 'screen': 'watch', 'aperture': 'rcol',
                             'collimator': 'ecol', 'monitor': 'moni', 'solenoid': 'mapsolenoid', 'wall_current_monitor': 'charge', 'cavity': 'rfcw',
                             'rf_deflecting_cavity': 'rfdf'}
    keyword_conversion_rules = {'length': 'l','entrance_edge_angle': 'e1', 'exit_edge_angle': 'e2', 'edge_field_integral': 'fint', 'horizontal_size': 'x_max', 'vertical_size': 'y_max',
                                'field_amplitude': 'volt', 'frequency': 'freq'}

    default_parameters = {'rfcw': {'change_p0': 1, 'end1_focus': 1, 'end2_focus': 1, 'body_focus_model': 'SRS'}}

    def addElement(self, name):
        elem = self.framework.getElement(name)
        if getParameter(elem,'entrance_edge_angle') == 'angle':
            self.framework.modifyElement(name,'entrance_edge_angle', getParameter(elem,'angle') )
        if getParameter(elem,'exit_edge_angle') == 'angle':
            self.framework.modifyElement(name,'exit_edge_angle', getParameter(elem,'angle') )
        element_dict = dict(self.framework.getElement(name))
        if 'type' in element_dict:

            if element_dict['type'] == 'cavity':
                element_dict['phase'] = 90+self.framework.getElement(name,'phase')
                element_dict['field_amplitude'] = 3*self.framework.getElement(name,'field_amplitude')
            if element_dict['type'] in self.type_conversion_rules and self.type_conversion_rules[element_dict['type']] == 'watch':
                element_dict['filename'] = name+'.sdds'
                self.screens.append(name)

            if element_dict['type'] in self.type_conversion_rules:
                element_dict['type'] = self.type_conversion_rules[element_dict['type']]
            element_dict = dict((self.keyword_conversion_rules[k] if k in self.keyword_conversion_rules else k, v) for k, v in element_dict.iteritems())
            if element_dict['type'] in self.default_parameters:
                element_dict = merge_two_dicts(element_dict, self.default_parameters[element_dict['type']])
            try:
                self.testlattice.addElement(name=name, **element_dict)
            # print getattr(testlattice, name).properties
            except:
                print name
        else:
            print name

    def defineElegantCommand(self,command=['elegant']):
        """Modify the defined Elegant command variable"""
        self.elegantCommand = command

    def _runElegant(self, filename=''):
        """Run the Elegant program with input 'filename'"""
        command = self.elegantCommand + [os.path.relpath(filename,self.subdir)]
        with open(os.path.relpath(filename+'.log', '.'), "w") as f:
            subprocess.call(command, stdout=f, cwd=self.subdir)

    def createElegantFile(self, f):
        self.filename = f
        originaloutput = self.framework.getFileSettings(f,'output')
        self.screens = []# print 'screens = ', screens

        originaloutput = self.framework.getFileSettings(self.filename,'output')
        output = copy.deepcopy(originaloutput)
        screens = self.framework.getElementsBetweenS('screen', output=output)
        bpms = self.framework.getElementsBetweenS('beam_position_monitor', output=output)

        zstart = getParameter(output,'zstart',default=None)
        if zstart is None:
            startelem = getParameter(output,'start_element',default=None)
            if startelem is None or startelem not in self.framework.elements:
                zstart = [0,0,0]
                self.zstart = [None, zstart, zstart]
            else:
                zstart = self.framework.elements[startelem]['position_start']
                originaloutput['zstart'] = zstart[2]
                self.zstart = [startelem, zstart, zstart]
        elif not isinstance(zstart, (list, tuple)):
            zstart = [0,0, zstart]
            self.zstart = [None, zstart, zstart]
        else:
            self.zstart = [None, zstart, zstart]
        zstop = None#getParameter(output,'zstop',default=None)
        if zstop is None:
            endelem = getParameter(output,'end_element',default=None)
            if endelem is None or endelem not in self.framework.elements:
                zstop = [0,0,0]
            else:
                zstop = self.framework.elements[endelem]['position_end']
                originaloutput['zstop'] = zstop[2]
        elif not isinstance(zstop, (list, tuple)):
            zstop = [0,0,zstop]

        # print 'zstart before = ', zstart
        # zstart = self.rotateAndOffset(zstart, self.global_offset, self.global_rotation)
        # print 'zstart after = ', zstart
        self.zstart[1] = zstart
        output['zstart'] = zstart[2]
        self.zstop = [endelem, zstop, zstop]
        # zstop = self.rotateAndOffset(zstop, self.global_offset, self.global_rotation)
        output['zstop'] = zstop[2]
        self.zstop[1] = zstop

        lattice_filename = f+'.lte'
        command_filename = self.subdir+'/'+f+'.ele'
        self.testlattice = elegantLattice()
        elements = self.framework.getElementsBetweenS(None, originaloutput)
        selectedelements = [[e, self.framework.getElement(e)] for e in elements]

        HDF5filename = self.zstart[0] + '.hdf5'
        self.elegantbeamfilename = self.zstart[0] + '.sdds'
        self.beam.read_HDF5_beam_file(self.subdir + '/' + HDF5filename)

        lattice = self.framework.createDrifts(selectedelements)
        map(self.addElement, lattice.keys())
        self.testlattice.addElement(name='START',type='charge', TOTAL=abs(self.beam.beam['total_charge']))
        self.testlattice.addElement(name='END',type='watch', filename=selectedelements[-1][0]+'.sdds')
        self.testlattice.addLine(name=f, line=['START']+lattice.keys()+['END'])
        self.screens += [selectedelements[-1][0]]
        self.testlattice.writeLatticeFile(self.subdir+'/'+lattice_filename, f)
        # self.testlattice.addCommand(type='global_settings',log_file="elegant.log",error_log_file="elegant.err")
        self.testlattice.addCommand(type='run_setup',lattice=lattice_filename,use_beamline=f,p_central=np.mean(self.beam.BetaGamma),centroid='%s.cen',always_change_p0 = 1)
        self.testlattice.addCommand(type='run_control',n_steps=1, n_passes=1)
        self.testlattice.addCommand(type='twiss_output',matched = 0,output_at_each_step=0,radiation_integrals=1,statistics=1,filename="%s.twi",
        beta_x  = self.beam.beta_x,
        alpha_x = self.beam.alpha_x,
        beta_y  = self.beam.beta_y,
        alpha_y = self.beam.alpha_y)
        # self.testlattice.addCommand(type='bunched_beam', n_particles_per_bunch=512, use_twiss_command_values=1, bunch="%s.bun",
        # emit_nx=self.beam.normalized_horizontal_emittance, emit_ny=self.beam.normalized_vertical_emittance, sigma_s=self.beam.sigma_z, momentum_chirp=self.beam.linear_chirp_z)
        self.testlattice.addCommand(type='sdds_beam', input=self.elegantbeamfilename)
        self.testlattice.addCommand(type='track')
        self.testlattice.writeCommandFile(command_filename)

    def runElegant(self, f):
        command_filename = self.subdir+'/'+f+'.ele'
        self._runElegant(command_filename)
        # self.loadSDDSFile(f)

    def preProcesssElegant(self):
        if self.zstart[0] is not None:
            self.convert_HDF5_beam_to_elegant_beam(self.subdir, self.filename, self.zstart)

    def convert_HDF5_beam_to_elegant_beam(self, subdir, filename, screen):
        if len(screen) > 2:
            name, pos, pos0 = screen
        else:
            name, pos = screen
            pos0 = pos
        HDF5filename = name + '.hdf5'
        self.elegantbeamfilename = name + '.sdds'
        self.beam.read_HDF5_beam_file(subdir + '/' + HDF5filename)
        self.beam.write_SDDS_file(subdir + '/' + self.elegantbeamfilename)

    def postProcesssElegant(self):
        if hasattr(self, 'screens'):
            for s in self.screens:
                self.convert_elegant_beam_to_HDF5_beam(self.subdir, self.filename, s)
        # self.convert_elegant_beam_to_HDF5_beam(self.subdir, self.filename, self.zstop, self.runno)

    def convert_elegant_beam_to_HDF5_beam(self, subdir, filename, screen, runno=1):
        self.beam.read_SDDS_beam_file(subdir + '/' + screen + '.sdds')
        print 'total charge = ', self.beam.beam['total_charge']
        HDF5filename = screen + '.hdf5'
        self.beam.write_HDF5_beam_file(subdir + '/' + HDF5filename, centered=False, sourcefilename=(screen + '.sdds'))
