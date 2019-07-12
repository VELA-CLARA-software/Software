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
//  Last edit:   03-07-2019
//  FileName:    water_temperature_monitor.py
//  Description: The water_temperature_monitor monitors cavity temperature PVs, these are passed
//               in from the config file. Its basically the same as cavity_temperature_monitor
//
//*/
'''
from monitor import monitor


class water_temperature_monitor(monitor):
    def __init__(self):
        # init base-ccaget lass
        monitor.__init__(self)
        # the gen mon keys will get stored here
        self._water_temp_keys   = []
        self.set_success = False
        """
        connects to the PVs and sets up the timer to get new values
        sets set_success flag
        :return:
        """
        # the pvs form the config file
        pv_list = self.config_data[self.config.WATER_TEMPERATURE_PV]
        # TODO: 1st line below  is a sanity check and should go in the config class
        if len(pv_list) == self.config_data[self.config.WATER_TEMPERATURE_PV_COUNT]:
            for i, pv in enumerate(pv_list):
                key = 'WATER_TEMP_ID_{}'.format(i)  # MAGIC_STRING  The key for the gen_mon keys


                if self.hardware.connectPV(pvKey=key, pvValue=pv):
                    self._water_temp_keys.append(key)
                    self.values[key] = None

        if len(self._water_temp_keys) == len(pv_list):
            # The timer runs update_values
            self.timer.timeout.connect(self.update)
            self.timer.start(self.config_data[self.config.WATER_TEMPERATURE_CHECK_TIME])
            self.set_success = True
        else:
            self.logger.message("Error  len(self._water_temp_keys) != len(pv_list)")

    def update(self):
        """
        gets the latest values from the gen_mon and adds them to the rf_condition_data.values dict
        """
        for key in self._water_temp_keys:
            self.values[key] = self.hardware.gen_mon.getValue(key)
