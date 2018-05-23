import h5py
import sys, os
import numpy as np
import glob
from ruamel import yaml
from collections import OrderedDict

def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

lineNames = ['S01', 'S02', 'C2V']


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def linearFit(data):
    x = [a[0] for a in data]
    y = [a[1] for a in data]
    fit=np.polyfit(x,y,deg=1)
    return float(fit[0])

def fitFileData(file):
    f = h5py.File(file, 'r')
    horizontal_group = f['horizontal']
    vertical_group = f['vertical']
    hfit = OrderedDict()
    vfit = OrderedDict()
    for l in lineNames:
        groups = [a for a in horizontal_group if l in a]
        for name in groups:
            print 'group = ', name
            name = str(name)
            hfit[name] = linearFit(horizontal_group[name])
        groups = [a for a in vertical_group if l in a]
        for name in groups:
            name = str(name)
            vfit[name] = linearFit(vertical_group[name])
    return hfit, vfit

class responseMatrix(object):

    def __init__(self):
        super(responseMatrix, self).__init__()
        files = []
        for l in lineNames:
            files += sorted(glob.glob('CLA-'+l+'-'+self.fileGlob))

        horizontal_response_matrix = OrderedDict()
        vertical_response_matrix = OrderedDict()

        for f in files:
            hrm, vrm = fitFileData(f)
            hvrm = merge_two_dicts(hrm, vrm)
            horizontal_response_matrix[f.replace('-SETI.h5','')] = hvrm

        with open(self.outputFileName, 'w') as outfile:
            ordered_dump(horizontal_response_matrix, outfile)

class horizontalResponseMatrix(responseMatrix):
    fileGlob = '*-HCOR-*-SETI.h5'
    outputFileName = 'horizontal_response_matrix.yaml'

class verticalResponseMatrix(responseMatrix):
    fileGlob = '*-VCOR-*-SETI.h5'
    outputFileName = 'vertical_response_matrix.yaml'

horizontalResponseMatrix()
verticalResponseMatrix()
