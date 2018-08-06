"""
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Controllers is distributed in the hope that it will be useful,       //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   27-03-2018
//  FileName:    screen.py
//  Description: reads in yaml config files for the generic_experiment class...
//      		 Why is parsing config files so messy? What tricks am i issing?
//  			 Why am i asking you?
//
//
"""
import yaml
from VELA_CLARA_Screen_Control import SCREEN_STATE
from VELA_CLARA_Shutter_Control import SHUTTER_STATE
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_enums import MACHINE_MODE
from data_logger import Data_Logger


#config key-words
header = 'header'
project_name = "project_name"
author = "author"
version = "version"
working_directory = "working_directory"
log_file = "log_file"

machine_mode = "machine_mode"
machine_area = "machine_area"

magnet = 'magnet'
llrf    = 'llrf'
screen  = 'screen'
camera  = 'camera'
shutter = 'shutter'

set_ = 'set_'
get_ = 'get_'
experiment_key_base = [set_, get_]
#machine modes
physical = 'physical'
virtual = 'virtual'

C2B ='C2B'
PI_LASER ='PI_LASER'
CLARA_PH1 ='CLARA_PH1'


class gen_ex_config(object):
    names = 'names'
    states = 'states'
    values = 'values'
    '''
        Individual dictionaries for each hardware type
        The dictionaries contain the procedures for each step
    '''
    screen_data = None
    magnet_data = None
    shutter_data = None
    camera_data = None

    header_data = None
    got_header  = False


    _config_filename = ''
    _raw_config_data = None
    _machine_mode = None
    def __init__(self, filename = ''):
        self.logger = Data_Logger()
        self.read_file(filename)


    def read_file(self, file_name=''):
        """read_file reads a generic experimental config file, yaml format etc...
           yes, two lines, that's all it takes ...
        """
        if file_name == '':
            pass
        else:
            gen_ex_config._config_filename = file_name
            # Try reading the config file
            try:
                stream = file(gen_ex_config._config_filename, 'r')
            except:
                self.logger.message(['MAJOR ERROR Can not read config file =',
                                              gen_ex_config._config_filename],True)
            else:
                gen_ex_config._raw_config_data = yaml.load(stream)
                if self.parse_config_headers():
                    self.parse_HWC_controller()
                    self.parse_procedure()

    def parse_config_headers(self):
        if header in gen_ex_config._raw_config_data:
            gen_ex_config.header_data = gen_ex_config._raw_config_data[header]
            # at a minimum we need to know the machine mode
            gen_ex_config.got_header = True
        else:
            self.logger.message('MAJOR ERROR No header in config', True)
        return gen_ex_config.got_header

    def parse_HWC_controller(self):
        if magnet in gen_ex_config._raw_config_data:
            m = self.get_machine_mode(gen_ex_config._raw_config_data[magnet])
            a = self.get_machine_area(gen_ex_config._raw_config_data[magnet])
            gen_ex_config.magnet_data = {machine_mode: m, machine_area: a}
            self.logger.message(['Found magnet', m, a], True)

        if screen in gen_ex_config._raw_config_data:
            m = self.get_machine_mode(gen_ex_config._raw_config_data[screen])
            a = self.get_machine_area(gen_ex_config._raw_config_data[screen])
            gen_ex_config.screen_data = {machine_mode: m, machine_area: a}
            self.logger.message(['Found screen', m, a], True)

        if shutter in gen_ex_config._raw_config_data:
            m = self.get_machine_mode(gen_ex_config._raw_config_data[shutter])
            a = self.get_machine_area(gen_ex_config._raw_config_data[shutter])
            gen_ex_config.shutter_data = {machine_mode: m, machine_area: a}
            self.logger.message(['Found shutter', m, a], True)

        if camera in gen_ex_config._raw_config_data:
            m = self.get_machine_mode(gen_ex_config._raw_config_data[camera])
            a = self.get_machine_area(gen_ex_config._raw_config_data[camera])
            gen_ex_config.camera_data = {machine_mode: m, machine_area: a}
            self.logger.message(['Found camera', m, a], True)





    def parse_procedure(self):
        experiment_keys = []
        for key in experiment_key_base:
            experiment_keys.extend( [s for s in gen_ex_config._raw_config_data if key in s] )

        for key in experiment_keys:
            if magnet in gen_ex_config._raw_config_data[key]:
                gen_ex_config.magnet_data[key] = gen_ex_config._raw_config_data[key][magnet]
                self.logger.message(['Found magnet', key], True)
            if screen in gen_ex_config._raw_config_data[key]:
                gen_ex_config.screen_data[key] = gen_ex_config._raw_config_data[key][screen]
                self.logger.message(['Found screen', key], True)
            if shutter in gen_ex_config._raw_config_data[key]:
                gen_ex_config.shutter_data[key] = gen_ex_config._raw_config_data[key][shutter]
                self.logger.message(['Found shutter', key], True)
            if camera in gen_ex_config._raw_config_data[key]:
                gen_ex_config.camera_data[key] = gen_ex_config._raw_config_data[key][camera]
                self.logger.message(['Found camera', key], True)

        # # to be read from file
        # #
        # gen_ex_config.screen_data =\
        #     {1:{gen_ex_config.names:  ['S02-SCR-01','S02-SCR-02'],
        #               gen_ex_config.values: [SCREEN_STATE.SCREEN_IN,SCREEN_STATE.SCREEN_OUT]},
        #      2: {gen_ex_config.names : ['S02-SCR-01', 'S02-SCR-02'],
        #          gen_ex_config.values: [SCREEN_STATE.SCREEN_OUT, SCREEN_STATE.SCREEN_IN]}
        #      }
        #
        # gen_ex_config.magnet_data =\
        #     {1: {gen_ex_config.names: ['S02-QUAD1','S02-QUAD2'],
        #          gen_ex_config.values:[6.23,6.33]},
        #      2: {gen_ex_config.names: ['S02-QUAD1','S02-QUAD2'],
        #          gen_ex_config.values:[-9.23,-7.33]}}
        #
        # gen_ex_config.shutter_data =\
        #     {1: {gen_ex_config.names: ['SHUT01'],
        #          gen_ex_config.values:[SHUTTER_STATE.OPEN]},
        #      2: {gen_ex_config.names: ['SHUT01'],
        #          gen_ex_config.values:[SHUTTER_STATE.OPEN]}}
        #
        # gen_ex_config.camera_data =\
        #     {1: {gen_ex_config.names: ['VC'],
        #          gen_ex_config.values:[1]},
        #      2: {gen_ex_config.names:  ['S02-CAM-01'],
        #          gen_ex_config.values: [10]}}


    def get_machine_mode(self,dict):
        if machine_mode in dict:
            str = dict[machine_mode]
            if str == physical:
                return  MACHINE_MODE.PHYSICAL
            elif str == virtual:
                return MACHINE_MODE.VIRTUAL
        return MACHINE_MODE.UNKNOWN_MACHINE_MODE


    def get_machine_area(self, dict):
        if machine_area in dict:
            str = dict[machine_area]
            if str == C2B:
                return MACHINE_AREA.CLARA_2_BA1_BA2
            elif str == PI_LASER:
                return MACHINE_AREA.PIL
            elif str == CLARA_PH1:
                return MACHINE_AREA.CLARA_PH1
        return MACHINE_AREA.UNKNOWN_AREA