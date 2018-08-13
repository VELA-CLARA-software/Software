import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__)))))
from SimulationFramework.Framework import *
from SimulationFramework.FrameworkHelperFunctions import *
# sys.path.append('../../ElegantWriter')
from ELEGANT.ElegantWriter.elegantWriter_objects import *
import SimulationFramework.Modules.read_beam_file as rbf
beam = rbf.beam()

beam.read_astra_beam_file('CLARA/injector400.0337.001')

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return OrderedDict(z)

class Elegant(object):


    type_conversion_rules = {'dipole': 'csrcsbend', 'quadrupole': 'kquad', 'beam_position_monitor': 'moni', 'screen': 'watch', 'aperture': 'rcol',
                             'collimator': 'ecol', 'monitor': 'moni', 'solenoid': 'mapsolenoid', 'wall_current_monitor': 'charge', 'cavity': 'rfcw',
                             'rf_deflecting_cavity': 'rfdf'}
    keyword_conversion_rules = {'length': 'l','entrance_edge_angle': 'e1', 'exit_edge_angle': 'e2', 'edge_field_integral': 'fint', 'horizontal_size': 'x_max', 'vertical_size': 'y_max',
                                'field_amplitude': 'volt', 'frequency': 'freq'}

    default_parameters = {'rfcw': {'change_p0': 1, 'end1_focus': 1, 'end2_focus': 1, 'body_focus_model': 'SRS'}}

    def addElement(self, name):
        elem = framework.getElement(name)
        if getParameter(elem,'entrance_edge_angle') == 'angle':
            framework.modifyElement(name,'entrance_edge_angle', getParameter(elem,'angle') )
        if getParameter(elem,'exit_edge_angle') == 'angle':
            framework.modifyElement(name,'exit_edge_angle', getParameter(elem,'angle') )
        if getParameter(elem,'type') == 'cavity':
            framework.modifyElement(name, 'phase', 90+framework.getElement(name,'phase'))
            framework.modifyElement(name, 'field_amplitude', 3*framework.getElement(name,'field_amplitude'))
        element_dict = dict(framework.getElement(name))
        if 'type' in element_dict:
            if element_dict['type'] in type_conversion_rules:
                element_dict['type'] = type_conversion_rules[element_dict['type']]
            element_dict = dict((keyword_conversion_rules[k] if k in keyword_conversion_rules else k, v) for k, v in element_dict.iteritems())
            if element_dict['type'] in default_parameters:
                element_dict = merge_two_dicts(element_dict, default_parameters[element_dict['type']])
            try:
                testlattice.addElement(name=name, **element_dict)
            # print getattr(testlattice, name).properties
            except:
                print name
        else:
            print name

    def createElegantFile(self, file):

        self.testlattice = elegantLattice()
        output = self.framework.getFileSettings(file,'output')
        elements = self.framework.getElementsBetweenS(None, output)
        print 'elements = ', elements
        exit()
        selectedelements = framework.selectElementsBetween('CLA-S02-APER-01','CLA-L02-CAV')
        lattice = framework.createDrifts(selectedelements)
        map(addElement, lattice.keys())
        testlattice.addLine(name='CLA', line=lattice.keys())
        testlattice.writeLatticeFile('CLA.lte', 'CLA')
        testlattice.addCommand(type='global_settings',log_file="elegant.log",error_log_file="elegant.err")
        testlattice.addCommand(type='run_setup',lattice="cla.lte",use_beamline="CLA",p_central=70.31,centroid='%s.cen',always_change_p0 = 1)
        testlattice.addCommand(type='run_control',n_steps=1, n_passes=1)
        testlattice.addCommand(type='twiss_output',matched = 0,output_at_each_step=0,radiation_integrals=1,statistics=1,filename="%s.twi",beta_x  =  beam.beta_x,
        alpha_x = beam.alpha_x,
        beta_y  =  beam.beta_y,
        alpha_y = beam.alpha_y)
        testlattice.writeCommandFile('CLA.ele')
        testlattice.runElegant('CLA.ele')
