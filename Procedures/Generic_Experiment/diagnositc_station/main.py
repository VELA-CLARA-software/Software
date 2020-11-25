import sys
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
# for i in sys.path:
#     print i

import general_experiment

if __name__ == '__main__':
    '''
        Entire procedure is contained in a YAML config-file 
    '''
    experiment_config_file = 'D:\\VELA\\GIT ' \
                              'Projects\\Software\\Procedures\\Generic_Experiment' \
                              '\\diagnositc_station' \
                              '\\test_input.yml'
    log_dir = 'D:\VELA\GIT Projects\Software\Procedures\Generic_Experiment\diagnositc_station\log\\'
    '''
        Create a generic experiment object and pass in config file        
    '''
    general_experiment = \
        general_experiment.general_experiment(config_file = experiment_config_file,log_dir =
        log_dir )


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