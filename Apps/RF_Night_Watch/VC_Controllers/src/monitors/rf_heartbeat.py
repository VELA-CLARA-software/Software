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
//  Last edit:   03-07-2020
//  FileName:    rf_heartbeat.py
//  Description: The hardware_control_hub, creates and holds all CATAP hardware controllers,
//                they get passed to where they are needed
//
//*/
'''
from monitor import monitor
from VELA_CLARA_enums import CONTROLLER_TYPE

class rf_heartbeat(monitor):
    """
        just sends RF keep alive signal every few seconds
    """
    def __init__(self):
        monitor.__init__(self)

        self.update_time = 5000

        # safety check teh controller exists
        if self.hardware.have_controller[CONTROLLER_TYPE.LLRF]:
            self.llrf_control = self.hardware.llrf_control
            # if it exists start timer, which calls self.check function every self.update_time
            self.start()
            self.set_success = True
        else:
            self.set_success = False

    def check(self):
        # force keep
        self.hardware.llrf_control.setKeepAlive(True)
        self.hardware.llrf_control.keepAlive()
        self.data.values[self.data.llrf_heart_beat_value] = self.llrf_control.getKeepAliveValue()
        #print('getKeepAliveValue = ', self.llrf_control.getKeepAliveValue())
        #print("hearbeat mon =  ", self.data.values[self.data.llrf_heart_beat_value])




