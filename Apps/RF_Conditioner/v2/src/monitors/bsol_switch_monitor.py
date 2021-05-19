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
//  Last edit:   17-05-2021
//  FileName:    bsol_switch_monitor.py
//  Description: The BSOL has a switched  and it can be on HRRG or LRRG, so we monitor it to
//               check it is set  to the correct magnet!
//
//*/
'''
from monitor import monitor
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from src.data.state import state


class bsol_switch_monitor(monitor):
    def __init__(self):
        # init base-ccaget lass
        monitor.__init__(self)


        # the gen mon keys will get stored here, keyed by the key from the data.values dict (meh!!)
        self._bsol_keys = []


        self.set_success = False
        """
        connects to the PVs and sets up the timer to get new values
        sets set_success flag
        :return:
        """
        # the pvs form the config file
        pv_list = self.config_data[self.config.BSOL_SWITCH_SET_PV]
        # TODO: 1st line below  is a sanity check and should go in the config class

        # TODO: this is a sanity check and should go in the config class
        if len(pv_list) == self.config_data[self.config.BSOL_SWITCH_SET_PV_COUNT]:
            for i, pv in enumerate(pv_list):
                key = 'BSOL_SWITCH_ID_{}'.format(i)  # MAGIC_STRING  The key for the gen_mon
                # keys
                self.logger.message_header("Connecting to BSOL Switch PVs", show_time_stamp=False,
                                           add_to_text_log=True)

                if self.hardware.connectPV(pvKey=key, pvValue=pv):
                    self._bsol_keys.append(key)
                    self.values[key] = self.data.dummy_int
                    self.logger.message("Connected to " + pv + ' id = ' + key)
                else:
                    self.logger.message("!!!ERROR!!! Failed to connect to " + pv)

        if len(self._bsol_keys) == len(pv_list):
            # The timer runs update_values
            self.timer.timeout.connect(self.update)
            self.timer.start(self.config_data[self.config.BSOL_SWITCH_SET_PV_COUNT_CHECK_TIME])
            self.set_success = True
        else:
            print("bsol_switch_monitor, FAILED")
            print(pv_list)
            print(self._bsol_keys)

    def update(self):
        """
        gets the latest values from the gen_mon and adds them to the rf_condition_data.values dict
        TODO THIS NEEDS TO BE UPDATED WHEN HRRG / LRRG
         are switched etc. there is a potential time bomb sitting here
        """
        for i, key  in enumerate(self._bsol_keys):
            self.values[key] = self.hardware.gen_mon.getValue(self.hardware.gen_mon_keys[key])
            # print("Cavity Temp Monitor, key = ",key,"  value = ", self.values[key])
            if i == 0:
                switch_mode = self.values[key]
                if self.llrf_type == LLRF_TYPE.CLARA_LRRG:
                    if switch_mode == 1:
                        self.values[self.data.bosl_switch_set_good] = state.GOOD
                    else:
                        self.values[self.data.bosl_switch_set_good] = state.BAD
                elif self.llrf_type  ==  LLRF_TYPE.VELA_HRRG:
                    if switch_mode == 0:
                        self.values[self.data.bosl_switch_set_good] = state.GOOD
                    else:
                        self.values[self.data.bosl_switch_set_good] = state.BAD
                elif self.llrf_type  ==  LLRF_TYPE.CLARA_HRRG:
                    self.values[self.data.bosl_switch_set_good] = state.BAD
                elif self.llrf_type  ==  LLRF_TYPE.VELA_LRRG:
                    self.values[self.data.bosl_switch_set_good] = state.BAD
                else:
                    self.values[self.data.bosl_switch_set_good] = state.GOOD

    # bosl_switch_set  = 'bosl_switch_set'
    # all_value_keys.append(bosl_switch_set)
    # values[bosl_switch_set] = dummy_int
    # bosl_switch_set_good  = 'bosl_switch_set_good'
    # all_value_keys.append(bosl_switch_set_good)
    # values[bosl_switch_set_good] = False
    # excluded_key_list.append(bosl_switch_set_good)