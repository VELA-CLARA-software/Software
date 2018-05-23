import h5py
import sys, os
import numpy as np
import glob
from ruamel import yaml


_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)


with open('horizontal_response_matrix.yaml', 'r') as infile:
    hrm = yaml.load(infile)

print hrm
