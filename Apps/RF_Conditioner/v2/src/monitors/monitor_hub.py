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
//  FileName:    monitor_hub.py
//  Description: The hardware_control_hub, creates and holds all CATAP hardware controllers,
//                they get passed to where they are needed
//
//*/
'''

# from VELA_CLARA_enums import MACHINE_MODE
# from VELA_CLARA_enums import MACHINE_AREA
# from VELA_CLARA_enums import CONTROLLER_TYPE
# from VELA_CLARA_LLRF_Control import LLRF_TYPE
# import VELA_CLARA_LLRF_Control
# import VELA_CLARA_Vac_Valve_Control
# import VELA_CLARA_RF_Modulator_Control
# import VELA_CLARA_RF_Protection_Control
# import VELA_CLARA_Magnet_Control
# import VELA_CLARA_General_Monitor
import subprocess
from collections import defaultdict

print('monitor_hub: import config')
from src.data.config import config
print('monitor_hub: import rf_conditioning_logger')
from src.data.rf_conditioning_logger import rf_conditioning_logger
print('monitor_hub: import vac_valve_monitor')
from vac_valve_monitor import vac_valve_monitor
print('monitor_hub: import modulator_monitor')
import modulator_monitor
print('monitor_hub: import rf_protection_monitor')
from rf_protection_monitor import rf_protection_monitor
print('monitor_hub: import llrf_monitor')
from llrf_monitor import llrf_monitor
print('monitor_hub: import llrf_monitor')
from modulator_monitor import modulator_monitor
print('monitor_hub: import vac_monitor')
from vac_monitor import vac_monitor
print('monitor_hub: import vac_monitor')
from src.data.rf_conditioning_data import rf_conditioning_data


class monitor_hub(object):
    """
    This class creates and holds all the data monitoring classes
    RF Protection Monitor

    There seems like a lot of repeated code for each function ....
    """
    vacuum_monitor = None
    DC_monitor = None
    modulator_monitor = None
    cavity_temp_monitor = None
    outside_mask_trace_monitor = None
    llrf_monitor = None
    water_temp_monitor = None
    rf_prot_monitor = None
    vac_valve_monitor = None
    sol_monitor = None
    user_gen_monitor = None

    # state of each possible data monitor

    is_vac_monitoring = 'is_vac_monitoring'
    is_DC_monitoring = 'is_DC_monitoring'
    is_modulator_monitoring = 'is_modulator_monitoring'
    is_cavity_temp_monitoring = 'is_cavity_temp_monitoring'
    is_outside_mask_trace_monitoring = 'is_outside_mask_trace_monitoring'
    is_llrf_monitoring = 'is_llrf_monitoring'
    is_water_temp_monitoring = 'is_water_temp_monitoring'
    is_rf_prot_monitoring = 'is_rf_prot_monitoring'
    is_vac_valve_monitor = 'is_vac_valve_monitor'
    is_sol_monitoring = 'is_sol_monitoring'
    is_user_gen_monitoring = 'is_user_gen_monitoring'

    is_monitoring = {is_vac_monitoring: False, is_DC_monitoring: False,
        is_modulator_monitoring: False, is_cavity_temp_monitoring: False,
        is_outside_mask_trace_monitoring: False, is_llrf_monitoring: False,
        is_water_temp_monitoring: False, is_rf_prot_monitoring: False, is_vac_valve_monitor: False,
        is_sol_monitoring: False, is_user_gen_monitoring: False}

    def __init__(self):
        self.my_name = 'data_monitoring'
        # owns a config and logging class
        self.config = config()
        self.config_data = self.config.raw_config_data
        self.logger = rf_conditioning_logger()
        # create a data object
        self.data = rf_conditioning_data()

    def start_monitors(self):
        self.logger.message(__name__ + ' Starting Data Monitoring',add_to_text_log=True,
                            show_time_stamp=False)
        self.start_rfprot_monitor()
        self.start_vac_valve()
        self.start_modulator_monitor()
        self.start_llrf_monitor()

    def start_modulator_monitor(self):
        '''

        :return:
        '''
        mh = monitor_hub
        self.logger.message(__name__ + ' start_modulator_monitor()')
        mh.modulator_monitor = modulator_monitor()
        mh.is_monitoring[mh.is_modulator_monitoring] = mh.modulator_monitor.set_success
        message = 'start_rfprot_monitor '
        if mh.is_monitoring[mh.is_modulator_monitoring]:
            message += ' successfully started RF Modulator Monitoring'
        else:
            message += ' FAILED to start RF Modulator Monitoring'
        self.logger.message(message)

    def start_rfprot_monitor(self):
        mh = monitor_hub
        self.logger.message(__name__ + ' start_rfprot_monitor()')
        mh.rf_prot_monitor = rf_protection_monitor()
        mh.is_monitoring[mh.is_rf_prot_monitoring] = mh.rf_prot_monitor.set_success
        message = 'start_rfprot_monitor '
        if mh.is_monitoring[mh.is_rf_prot_monitoring]:
            message += ' successfully started RF Protection Monitoring'
        else:
            message += ' FAILED to start RF Protection Monitoring'
        self.logger.message(message)

    def start_vac_valve(self):
        mh = monitor_hub
        self.logger.message(__name__ + ' start_vac_valve()')
        mh.vac_valve_monitor = vac_valve_monitor()
        mh.is_monitoring[mh.is_vac_valve_monitor] = mh.rf_prot_monitor.set_success
        message = 'start_vac_valve '
        if mh.is_monitoring[mh.is_vac_valve_monitor]:
            message += ' successfully started Vac Valve Monitoring'
        else:
            message += ' FAILED to start Vac Valve Monitoring'
        self.logger.message(message)

    def start_llrf_monitor(self):
        mh = monitor_hub
        self.logger.message(__name__ + ' start_llrf_monitor()')
        mh.llrf_monitor = llrf_monitor()
        mh.is_monitoring[mh.is_llrf_monitoring] = mh.rf_prot_monitor.set_success
        message = 'start_llrf_monitor '
        if mh.is_monitoring[mh.is_llrf_monitoring]:
            message += ' successfully started LLRF Monitoring'
        else:
            message += ' FAILED to start LLRF Monitoring'
        self.logger.message(message)

    def vac_monitor(self):
        mh = monitor_hub
        self.logger.message(__name__ + ' vac_monitor()')
        mh.vac_monitor = vac_monitor()
        mh.is_monitoring[mh.is_vac_monitoring] = mh.vac_monitor.set_success
        message = 'start_rfprot_monitor '
        if mh.is_monitoring[mh.is_vac_monitoring]:
            message += ' successfully started Vacuum Monitoring'
        else:
            message += ' FAILED to start Vacuum  Monitoring'
        self.logger.message(message)
