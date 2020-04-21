import time, os, sys
import numpy as np
from collections import OrderedDict
from itertools import product
import ruamel.yaml as yaml
sys.path.append("../../../")
from Software.Widgets.generic.pv import *

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(iter(list(data.items())))

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

class scriptRunner(object):

    def __init__(self, script=None):
        super(scriptRunner, self).__init__()
        self.filename = script
        self.settings = self.load_yaml(self.filename)
        self.variables, self.measurables = self.analyse_settings(self.settings)
        self.variable_pvs, self.variable_ranges = self.interpret_variables(self.variables)
        self.measurables_pvs = self.interpret_measurables(self.measurables)
        self.run(self.variable_pvs, self.variable_ranges, self.measurables_pvs)

    def load_yaml(self, filename):
        settings = OrderedDict()
        if os.path.exists(filename):
            stream = open(filename, 'r')
        else:
            stream = open(master_lattice_location+filename, 'r')
        settings = yaml.load(stream, Loader=yaml.UnsafeLoader)
        stream.close()
        return settings

    def check_settings(self, settings, type):
        if type in settings:
            return settings[type]
        else:
            raise ValueError('No ' + type + ' defined in YAML file.')

    def analyse_settings(self, settings):
        variables = self.check_settings(settings, 'variables')
        measurables = self.check_settings(settings, 'measurables')
        return variables, measurables

    def interpret_variables(self, variables):
        variable_pvs = [PVObject(v['pv']) for k, v in variables.items()]
        variable_ranges = list(product(*[np.arange(v['start'],v['end']+v['step'],v['step']) for k, v in variables.items()]))
        # print('Variable PVs = ', variable_pvs, [p.value for p in variable_pvs])
        # print('Variable Ranges = ', variable_ranges)
        return variable_pvs, variable_ranges

    def interpret_measurables(self, measurables):
        measurables_pvs = [[PVBuffer(v['pv'], v['counts']), v['functions']] for k, v in measurables.items()]
        # print('Measurable PVs = ', measurables_pvs, [[getattr(p[0], f) for f in p[1]] for p in measurables_pvs])
        # variable_ranges = list(product(*[np.arange(v['start'],v['end']+v['step'],v['step']) for k, v in variables.items()]))
        return measurables_pvs

    def run(self, variable_pvs, variable_ranges, measurables_pvs):
        for values in variable_ranges:
            print(list(zip(*[variable_pvs, values])))
            

if __name__ == '__main__':
    scriptR = scriptRunner('q_vs_hwp.yaml')
    exit()
