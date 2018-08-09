from collections import OrderedDict
import simplejson as json
import yaml
import argparse

def setup_yaml():
  """ https://stackoverflow.com/a/8661021 """
  represent_dict_order = lambda self, data:  self.represent_mapping('tag:yaml.org,2002:map', data.items())
  yaml.add_representer(OrderedDict, represent_dict_order)
setup_yaml()

parser = argparse.ArgumentParser(description='JSON to YAML Converter')
parser.add_argument('inputfile')
parser.add_argument('-o', '--outputfile', default='')
args = parser.parse_args()

f = open(args.inputfile, 'r')
jsonData = json.load(f, object_pairs_hook=OrderedDict)
f.close()

if args.outputfile == '':
    args.outputfile = str(args.inputfile).replace('json','yaml')
ff = open(args.outputfile, 'w+')
yaml.dump(jsonData, ff, allow_unicode=True)
ff.close()
