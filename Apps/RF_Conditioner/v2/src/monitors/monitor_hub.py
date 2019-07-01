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
import vac_valve_monitor
import modulator_monitor
import rf_protection_monitor
import llrf_simple_param_monitor


class monitor_hub(object):
    """
    This class creates and holds all the data monitoring classes
    RF Protection Monitor
    """
    vacuum_monitor = None
    DC_monitor = None
    modulator_monitor = None
    cavity_temp_monitor = None
    outside_mask_trace_monitor = None
    llrf_simple_param_monitor = None
    water_temp_monitor = None
    rf_prot_monitor = None
    vac_valve_monitor = None
    sol_monitor = None
    user_gen_monitor = None

    def __init__(self):
        self.my_name = 'data_monitoring'
        # owns a config and logging class
        self.config = config.config()
        self.config_data = self.config.raw_config_data
        self.logger = rf_conditioning_logger.rf_conditioning_logger()

        self.logger.message_header(self.my_name + ' Starting Data Monitoring',
                                   add_to_text_log=True,show_time_stamp=False)


    def rfprot_monitor(self):
        data_monitoring.rf_prot_monitor = rf_protection_monitor.rf_protection_monitor()
        data_monitoring.is_monitoring[
            dat.rfprot_state] = data_monitoring_base.rf_prot_monitor.set_success
        return data_monitoring_base.rf_prot_monitor.set_success
