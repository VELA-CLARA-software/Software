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

from VELA_CLARA_Screen_Control import SCREEN_STATE
from VELA_CLARA_Shutter_Control import SHUTTER_STATE
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_enums import MACHINE_MODE


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
    camdaq_data = None
    shutter_data = None

    screen_type = None
    magnet_type = None
    shutter_type = None
    camdaq_type = None


    def __init__(self, filename = ''):

        self.read_config(filename)




    def read_config(self,filename):
        # to be read from file
        gen_ex_config.screen_type = {'mode': MACHINE_MODE.PHYSICAL,
                                     'area':MACHINE_AREA.CLARA_PH1}
        gen_ex_config.magnet_type = {'mode': MACHINE_MODE.PHYSICAL,
                                     'area':MACHINE_AREA.CLARA_2_BA1_BA2}
        gen_ex_config.shutter_type = {'mode': MACHINE_MODE.PHYSICAL,
                                      'area':MACHINE_AREA.CLARA_2_BA1_BA2}
        gen_ex_config.camdaq_type = {'mode': MACHINE_MODE.PHYSICAL,
                                     'area':MACHINE_AREA.CLARA_2_BA1_BA2}

        #
        gen_ex_config.screen_data =\
            {1:{gen_ex_config.names:  ['S02-SCR-01','S02-SCR-02'],
                      gen_ex_config.values: [SCREEN_STATE.SCREEN_IN,SCREEN_STATE.SCREEN_OUT]},
             2: {gen_ex_config.names : ['S02-SCR-01', 'S02-SCR-02'],
                 gen_ex_config.values: [SCREEN_STATE.SCREEN_OUT, SCREEN_STATE.SCREEN_IN]}
             }

        gen_ex_config.magnet_data =\
            {1: {gen_ex_config.names: ['S02-QUAD1','S02-QUAD2'],
                 gen_ex_config.values:[6.23,6.33]},
             2: {gen_ex_config.names: ['S02-QUAD1','S02-QUAD2'],
                 gen_ex_config.values:[-9.23,-7.33]}}

        gen_ex_config.shutter_data =\
            {1: {gen_ex_config.names: ['SHUT01'],
                 gen_ex_config.values:[SHUTTER_STATE.OPEN]},
             2: {gen_ex_config.names: ['SHUT01'],
                 gen_ex_config.values:[SHUTTER_STATE.OPEN]}}

        gen_ex_config.camdaq_data =\
            {1: {gen_ex_config.names: ['VC'],
                 gen_ex_config.values:[1]},
             2: {gen_ex_config.names:  ['S02-CAM-01'],
                 gen_ex_config.values: [10]}}