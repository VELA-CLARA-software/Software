import sys
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
# for i in sys.path:
#     print i

import general_experiment

if __name__ == '__main__':
    fn = 'test_input.yaml'
    general_experiment = general_experiment.general_experiment(filename=fn)


#
#
#
#
#
# from yaml import load, dump
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper
# f=open("test_input.yml")
# data = load(f, Loader=Loader)
#
#
# import yaml
# document = """
#   a: 1
#   b:
#     c: 3
#     d: 4
# """
# print yaml.dump(yaml.load(document))