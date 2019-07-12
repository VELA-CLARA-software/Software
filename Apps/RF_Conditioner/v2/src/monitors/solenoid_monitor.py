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
//  FileName:    solenoid_monitor.py
//  Description: The water_temperature_monitor monitors cavity temperature PVs, these are passed
//               in from the config file. Its basically the same as cavity_temperature_monitor
//
//*/
'''
from monitor import monitor


class solenoid_monitor(monitor):
    def __init__(self):
        # init base-ccaget lass
        monitor.__init__(self)
        self.set_success = False
        """
        connects to the PVs and sets up the timer to get new values
        sets set_success flag
        :return:
        """
        # the pvs form the config file
        self.sol_objects = {}

        self.set_success = False
        # TODO:sanity check in config NOT HERE
        if len(self.config_data[self.config.SOL_NAMES]) == self.config_data[self.config.SOL_COUNT]:
            for solenoid in self.config_data[self.config.SOL_NAMES]:
                # get magnet  object const ref
                self.sol_objects[solenoid] = self.hardware.mag_control.getMagObjConstRef(solenoid)
                # add entry to data dictionary
                self.values[solenoid] = None
            self.set_success = True
        # The timer runs update_values
        self.timer.timeout.connect(self.update)
        self.timer.start(self.config_data[self.config.SOL_CHECK_TIME])

    def update(self):
        """
        gets the latest values from the gen_mon and adds them to the rf_condition_data.values dict
        """
        for key in self.sol_objects.keys():
            self.values[key] = self.sol_objects[key].SI
