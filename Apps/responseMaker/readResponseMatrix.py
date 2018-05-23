import h5py
import sys, os
import numpy as np
import glob
from ruamel import yaml
from collections import OrderedDict

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

class responseMatrix(object):

    def __init__(self, filename=None):
        super(responseMatrix, self).__init__()
        self.filename = filename if filename is not None else self.filename

        with open(self.filename, 'r') as infile:
            self.rm = yaml.load(infile, Loader=yaml.Loader)

        self.actuators = self.rm.keys()
        self.monitors = [m for m in self.rm[self.rm.keys()[0]].keys() if self.plane in m]

        self.responseMatrix = []
        for act in self.actuators:
            rm = self.rm[act]
            line = []
            for m in self.monitors:
                ans = rm[m] if abs(rm[m]) > 0.1 else 0
                line.append(ans)
            self.responseMatrix.append(line)

    def createResponseMatrix(self, actuators=None, monitors=None):
        actuators = self.actuators if actuators is None else actuators
        monitors = self.monitors if monitors is None else monitors
        responseMatrix = []
        for act in actuators:
            rm = self.rm[act]
            line = []
            for m in monitors:
                ans = rm[m] if abs(rm[m]) > 0.1 else 0
                line.append(ans)
            responseMatrix.append(line)

class horizontalResponseMatrix(responseMatrix):

    filename='horizontal_response_matrix.yaml'
    plane ='-X'

class verticalResponseMatrix(responseMatrix):

    filename='vertical_response_matrix.yaml'
    plane ='-Y'
