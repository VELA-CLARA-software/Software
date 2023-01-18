#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
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
//  Last edit:   01-07-2019
//  FileName:    vac_valve_monitor.py
//  Description: checks the state of the RF Vac Valve for the RF_STRUCTURE being conditioned
//
//*/
"""
from monitor import monitor
from VELA_CLARA_enums import CONTROLLER_TYPE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
#import src.data.rf_condition_data_base as dat
# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the protection)
# at a later date
#
class vac_valve_monitor(monitor):
    # whoami
    my_name = 'vac_valve_monitor'

    def __init__(self):
        monitor.__init__(self)
        #
        self.update_time = self.config_data[self.config.VAC_VALVE_CHECK_TIME]
        # memory of previous value for alarm
        self.old_value = None
        # create a local copy of relevant config data
        self.keep_valve_open = self.config_data[self.config.KEEP_VALVE_OPEN]
        if self.hardware.have_controller[CONTROLLER_TYPE.VAC_VALVES]:
            self.set_success = True
            self.start()
        else:
            self.set_success = False

    def check(self):
        # print 'checking valve state'
        self.data.values[self.data.vac_valve_status] = self.hardware.valve_obj[0].vacValveState

        if self.old_value != self.data.values[self.data.vac_valve_status]:
            if self.hardware.valve_obj[0].vacValveState == VALVE_STATE.VALVE_OPEN:
                self.alarm('valve open')
            elif self.hardware.valve_obj[0].vacValveState == VALVE_STATE.VALVE_CLOSED:
                self.alarm('valve closed')
            # update old value if value has changed
            self.old_value = self.data.values[self.data.vac_valve_status]

        if self.keep_valve_open:
            if self.hardware.valve_obj[0].vacValveState == VALVE_STATE.VALVE_CLOSED:
                self.hardware.valve_control.openVacValve(self.valve_name)





