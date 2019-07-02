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
from VELA_CLARA_enums import CONTROLLER_TYPE
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_LLRF_Control
import VELA_CLARA_Vac_Valve_Control
import VELA_CLARA_RF_Modulator_Control
import VELA_CLARA_RF_Protection_Control
import VELA_CLARA_Magnet_Control
import VELA_CLARA_General_Monitor
import subprocess
from collections import defaultdict

from src.data import config
from src.data import rf_conditioning_logger


class hardware_control_hub(object):
    """
    This class creates and holds all the CATAP objects
    These are held in static variables that can be passed to where-ever they are needed
    This class's funcitons all look very similar and so they could be a lot fo refactor ing to
    once hardware Objects are created this class does nothing else
    """
    # we create static objects for init, control (and sometimes object constant references)
    # these objects live here and will be passed ot other classes as needed
    #
    # vaccum valves
    print('import VELA_CLARA_Vac_Valve_Control')
    valve_init = VELA_CLARA_Vac_Valve_Control.init()
    valve_init.setQuiet()
    valve_control = None
    # RF modualtor
    print('import VELA_CLARA_RF_Modulator_Control')
    mod_init = VELA_CLARA_RF_Modulator_Control.init()
    mod_init.setQuiet()
    mod_control = None
    mod_obj = None
    # RF protection
    print('import VELA_CLARA_RF_Protection_Control')
    prot_init = VELA_CLARA_RF_Protection_Control.init()
    prot_init.setQuiet()
    prot_object = None
    prot_control = None
    prot_succes = False
    # llrf
    print('import VELA_CLARA_LLRF_Control')
    llrf_init = VELA_CLARA_LLRF_Control.init()
    llrf_init.setQuiet()
    llrf_control = None
    llrf_obj = None
    # magnets
    print('import VELA_CLARA_Magnet_Control')
    mag_init = VELA_CLARA_Magnet_Control.init()
    mag_init.setQuiet()
    mag_control = None
    # general monitoring
    print('import VELA_CLARA_General_Monitor')
    gen_mon = VELA_CLARA_General_Monitor.init()
    gen_mon_keys = {}
    user_gen_mon_dict = {}

    # dictionary to keep state of each controller (for sanity checks etc)
    have_controller = {CONTROLLER_TYPE.VAC_VALVES: False, CONTROLLER_TYPE.RF_PROT: False,
        CONTROLLER_TYPE.MAGNET: False, CONTROLLER_TYPE.RF_MOD: False, CONTROLLER_TYPE.LLRF: False,
        CONTROLLER_TYPE.GENERAL_MONITOR: True}

    # TODO: move into an app utilities space
    is_gun_type = {LLRF_TYPE.CLARA_HRRG: True, LLRF_TYPE.CLARA_LRRG: True,
                   LLRF_TYPE.VELA_HRRG: True, LLRF_TYPE.VELA_LRRG: True}
    is_gun_type = defaultdict(lambda: MACHINE_AREA.UNKNOWN_AREA, is_gun_type)

    def __init__(self):
        self.my_name = 'hardware_control_hub'
        # owns a config and logging class
        self.config = config.config()
        self.config_data = self.config.raw_config_data
        self.logger = rf_conditioning_logger.rf_conditioning_logger()


    def start_up(self):
        """
        This NEEDS to be a serpete function. Many clases create one of these objects but the
        hardware controls should only be created ONCE! The main_controller will call this
        function, then every other class just creates a hardware_control_hub to have access to
        the controllers (or objects)
        :return:
        """
        self.logger.message(self.my_name + ' Starting CATAP Hardware Interfaces',
                                   add_to_text_log=True,show_time_stamp=False)
        self.start_RF_protection()
        self.start_magnet_control()
        self.start_valve_control()
        self.start_mod_control()
        self.start_llrf_control()

    def start_RF_protection(self):
        '''
        Creates the requested RF Protection control object
        '''
        rf_structure = self.config_data[self.config.RF_STRUCTURE]
        rf_prot_type = self.config.get_rf_prot_type[self.config_data[self.config.RF_STRUCTURE]]
        # alias for shorter lines
        hch = hardware_control_hub
        message = 'start_RF_protection() '
        if self.is_gun_type[rf_structure]:
            hch.prot_control = hch.prot_init.physical_Gun_Protection_Controller()
            hch.have_controller[CONTROLLER_TYPE.RF_PROT] = True
            message += ' successfully created a GUN protection control object'
        elif rf_structure == LLRF_TYPE.L01:
            # THE Linac protection controller IS NOT YET TESTED
            hch.prot_control = hch.prot_init.physical_L01_Protection_Controller()
            hch.have_controller[CONTROLLER_TYPE.RF_PROT] = True
            message += ' successfully created a L01 protection control  object'
        else:
            message = ' FAILED to create a RF Protection object'
        # get an protection object if we have a controller
        if hch.have_controller[CONTROLLER_TYPE.RF_PROT]:
            hch.prot_object = [hch.prot_control.getRFProtObjConstRef(rf_prot_type)]

        self.logger.message(message)

    def start_magnet_control(self):
        '''
        Creates the requested Magnet Control object
        '''
        # alias for shorter lines
        hch = hardware_control_hub
        machine_area = self.config_data[self.config.MAGNET_MACHINE_AREA]
        message = 'start_mod_control() '
        if machine_area == MACHINE_AREA.VELA_INJ:  # MAGIC_STRING
            hch.mag_control = hch.mag_init.physical_CLARA_Ph1_Magnet_Controller()
            hch.have_controller[CONTROLLER_TYPE.MAGNET] = True
            message += ' successfully created a CLARA_PH1 magnet control object'
        elif machine_area == MACHINE_AREA.CLARA_PH1:  # MAGIC_STRING
            hch.mag_control = hch.mag_init.physical_VELA_INJ_Magnet_Controller()
            hch.have_controller[CONTROLLER_TYPE.MAGNET] = True
            message += ' successfully created a VELA_INJ magnet control object'
        else:
            message = ' FAILED to create a magnet Control object'
        self.logger.message(message)

    def start_valve_control(self):
        '''
        Creates the requested Valve Control object
        '''
        machine_area = self.config_data[self.config.VAC_VALVE_AREA]
        valve = self.config_data[self.config.VAC_VALVE]
        # alias for shorter lines
        hch = hardware_control_hub
        message = 'start_mod_control() '
        if machine_area == MACHINE_AREA.CLARA_PH1:
            hch.valve_control = hch.valve_init.physical_CLARA_PH1_Vac_Valve_Controller()
            hch.have_controller[CONTROLLER_TYPE.VAC_VALVES] = True
            message = ' successfully created a CLARA_PH1 valve control object'
        elif machine_area == MACHINE_AREA.VELA_INJ:
            hch.valve_control = hch.valve_init.physical_VELA_INJ_Vac_Valve_Controller()
            hch.have_controller[CONTROLLER_TYPE.VAC_VALVES] = True
            message = ' successfully created a VELA_INJ valve control object'
        else:
            message = ' FAILED to create a valve Control object'
        if hch.have_controller[CONTROLLER_TYPE.VAC_VALVES]:
            hch.valve_obj = [hch.valve_control.getVacValveObjConstRef(valve)]

        self.logger.message(message)

    def start_mod_control(self):
        '''
        Creates the requested Modulator Control object
        '''
        # alias for shorter lines
        hch = hardware_control_hub
        message = 'start_mod_control() '
        if hch.is_gun_type[self.config_data[self.config.RF_STRUCTURE]]:
            hch.mod_control = hch.mod_init.physical_GUN_MOD_Controller()
            hch.have_controller[CONTROLLER_TYPE.RF_MOD] = True
            message = ' successfully created a ' + str(
                self.config_data[self.config.RF_STRUCTURE]) + ' modulator control object'
        elif self.config_data[self.config.RF_STRUCTURE] == LLRF_TYPE.L01:
            hch.mod_control = hch.mod_init.physical_L01_MOD_Controller()
            hch.have_controller[CONTROLLER_TYPE.RF_MOD] = True
            message = ' successfully created a L01 modulator control object'
        else:
            message = ' FAILED to create a modulator Control object'
        self.logger.message(message)

    def start_llrf_control(self):
        '''
        Creates the requested LLRF Control object
        '''
        # alias for shorter lines
        hch = hardware_control_hub
        rf_structure = self.config_data[self.config.RF_STRUCTURE]
        message = 'start_llrf_control() '
        if rf_structure == LLRF_TYPE.UNKNOWN_TYPE:
            message += ' FAILED to create a LLRF  Control object'
        else:
            hch.llrf_control = hch.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL, rf_structure)
            hch.llrf_obj = [hch.llrf_control.getLLRFObjConstRef()]
            hch.have_controller[CONTROLLER_TYPE.LLRF] = True
            message += ' successfully created a ' + str(rf_structure) + ' LLRF control object'
        self.logger.message(message)
