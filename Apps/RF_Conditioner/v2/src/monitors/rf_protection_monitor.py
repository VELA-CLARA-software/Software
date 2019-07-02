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
//  FileName:    rf_protection_monitor.py
//  Description: checks the state of the RF protectino fro the RF_STRUCTURE being conditioned
//
//*/
"""
from state_monitor import state_monitor
from VELA_CLARA_enums import CONTROLLER_TYPE

# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the protection)
# at a later date
#
class rf_protection_monitor(state_monitor):
    # whoami
    my_name = 'rf_protection_monitor'
    old_value = None
    def __init__(self):
        #
        state_monitor.__init__(self)
        self.update_time = self.config_data[self.config.RF_PROT_CHECK_TIME]
        if self.hardware.have_controller[CONTROLLER_TYPE.RF_PROT]:
            self.set_success = True
            self.start()
        else:
            self.set_success = False


    def check(self):
        if self.set_success:
            self.data.values[self.data.rfprot_state] = self.hardware.prot_object[0].status
            #print('RF prot',self.data.values[self.data.rfprot_state])
