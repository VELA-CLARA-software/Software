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
//  FileName:    rf_heartbeat.py
//  Description: The hardware_control_hub, creates and holds all CATAP hardware controllers,
//                they get passed to where they are needed
//
//*/
'''
from monitor import monitor


class rf_heartbeat(monitor):
    """
        just sends RF keep alive signal every few seconds
    """
    def __init__(self):
        monitor.__init__(self)

        self.update_time = 5

        if self.hardware.have_controller[CONTROLLER_TYPE.RF_MOD]:
            self.mod = self.hardware.mod_obj
            self.start()
            self.set_success = True
        else:
            self.set_success = False

    def check(self):
        self.llrf_control.setKeepAlive(True)
        self.llrf_control.keepAlive()


        self.data.values[self.data.modulator_state] = self.mod[0].main_state
        # print("self.data.values[self.data.modulator_state] = ", self.data.values[
        #     self.data.modulator_state] )

        # assume there is one PV that gives the RF state,
        # MODULATOR, INTERLOCKS, LLRF
        # wich MAY NOT be true
        if self.data.values[self.data.modulator_state] == GUN_MOD_STATE.RF_ON:
            self.data.values[self.data.modulator_good] = True
        elif self.data.values[self.data.modulator_state] == L01_MOD_STATE.L01_RF_ON:
            self.data.values[self.data.modulator_good] = True
        else:
            self.data.values[self.data.modulator_good] = False





