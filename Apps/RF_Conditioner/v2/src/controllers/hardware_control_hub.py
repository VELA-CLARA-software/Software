#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify  //
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
//  Last edit:   03-07-2018
//  FileName:    main_controller.py
//  Description: The hardware_control_hub, creates and holds all CATAP hardware controllers,
//                they get passed to where they are needed
//
//*/
'''

from VELA_CLARA_enums import MACHINE_MODE
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_LLRF_Control
import VELA_CLARA_Vac_Valve_Control
import VELA_CLARA_RF_Modulator_Control
import VELA_CLARA_RF_Protection_Control
import VELA_CLARA_Magnet_Control
import subprocess


from src.data import config
from src.data import rf_conditioning_logger







class hardware_control_hub(object):


    # init LLRF Hardware Controllers
    #
    # vaccum valves
    valve_init = None
    valve_control = None
    #
    mod_init = None
    mod_control = None
    #
    # RF protection
    prot_init = None
    prot_control = None

    llrf_init = None
    llrf_control = None

    mag_init = None
    mag_control = None

    alarm_process = subprocess.Popen('pause', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    def __init__(self):
        # config and logging
        self.config = config.config()
        self.config_data = self.config.raw_config_data
        self.logger = rf_conditioning_logger.rf_conditioning_logger()


    def initialise(self):
        # RF protection
        self.start_RF_protection()


        hardware_control_hub.llrf_init = VELA_CLARA_LLRF_Control.init()
        hardware_control_hub.llrf_init.setVerbose()
        # init LLRF Hardware Controllers
        # llrf_init.setQuiet()
        # _llrf_control = None  # LLRF HWC
        # _llrfObj = None  # LLRF HWC
        # _llrf_handler = None
        # #
        # other attributes that need default values
        # they are used in function below
        # config file read successfully
        #
        # vaccume valves
        hardware_control_hub.valve_init = VELA_CLARA_Vac_Valve_Control.init()
        hardware_control_hub.valve_init.setQuiet()
        # valve_init.setVerbose()
        #
        hardware_control_hub.mod_init = VELA_CLARA_RF_Modulator_Control.init()
        hardware_control_hub.mod_init.setQuiet()
        # mod_init.setVerbose()
        #

        #
        # Magnets
        hardware_control_hub.mag_init = VELA_CLARA_Magnet_Control.init()
        hardware_control_hub.mag_init.setQuiet()


    def start_RF_protection(self):
        rf_structure = self.config_data[self.config.RF_STRUCTURE]
        hardware_control_hub.prot_init = VELA_CLARA_RF_Protection_Control.init()
        hardware_control_hub.prot_init.setQuiet()
        '''Creates the requested RF Protection control object '''
        if self.is_gun_type(rf_structure ):
            hardware_control_hub.prot_control = hardware_control_hub.prot_init.physical_Gun_Protection_Controller()
            self.logger.message('start_RF_protection created a GUN protection control object', True)
        elif rf_structure  == LLRF_TYPE.L01:
            #
            # we don't have a linac protection controller yet ..
            self.prot_control = hardware_control_hub.prot_init.physical_L01_Protection_Controller()
            #self.prot_control = None
            self.logger.message('start_rf_prot_control did not create a L01 protection '
                                'control  object', True)
        else:
            self.logger.message('Unknown LLRF TYPE passed create protection control object',
                                True)



    def is_gun_type(self, type):
        if type == LLRF_TYPE.CLARA_HRRG:
            return True
        elif type == LLRF_TYPE.CLARA_LRRG:
            return True
        elif type == LLRF_TYPE.VELA_HRRG:
            return True
        elif type == LLRF_TYPE.VELA_LRRG:
            return True
        else:
            return False
