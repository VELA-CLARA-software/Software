'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Software is distributed in the hope that it will be useful,          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   11-01-2019
//  FileName:    procedure.py
//  Description: template for class for gui_source class in generic High Level Application
//
//
//*/
'''
import data

import VELA_CLARA_LLRF_Control as llrf


class procedure(object):

    llrf_init = llrf.init()
    #llrf_init.setVerbose()
    llrf_init.setQuiet()
    gun_llrf_control = llrf_init.getLLRFController(llrf.MACHINE_MODE.PHYSICAL, llrf.LLRF_TYPE.CLARA_LRRG)
    linac_llrf_control = llrf_init.getLLRFController(llrf.MACHINE_MODE.PHYSICAL, llrf.LLRF_TYPE.L01)
    data = data.data()

    def __init__(self):
        # super(base, self).__init__()
        object.__init__(self)
        self.data = procedure.data
        self.values = self.data.values

    def set_keep_alive_gun(self, value):
        procedure.gun_llrf_control.setKeepAlive(value)

    def set_keep_alive_linac(self, value):
        procedure.linac_llrf_control.setKeepAlive(value)

    def update_data(self):
        self.values[self.data.should_keep_linac_alive] = procedure.linac_llrf_control.canKeepAlive()
        self.values[self.data.should_keep_gun_alive] = procedure.gun_llrf_control.canKeepAlive()

        if self.values[self.data.should_keep_linac_alive]:
            print("Send keep alive LINAC")
            procedure.linac_llrf_control.keepAlive()
        if self.values[self.data.should_keep_gun_alive]:
            procedure.gun_llrf_control.keepAlive()
            print("Send keep alive GUN")

        self.values[self.data.old_gun_keep_alive_value] = self.values[self.data.gun_keep_alive_value]
        self.values[self.data.old_linac_keep_alive_value] = self.values[self.data.linac_keep_alive_value]
        self.values[self.data.gun_keep_alive_value] = procedure.gun_llrf_control.getKeepAliveValue()
        self.values[self.data.linac_keep_alive_value] = procedure.linac_llrf_control.getKeepAliveValue()
        #
        # for key,value in self.values.iteritems():
        #     print("proc",key,"=",value)



