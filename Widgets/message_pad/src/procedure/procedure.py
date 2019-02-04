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
//  Description: template for class for gui class in generic High Level Application
//
//
//*/
'''
import VELA_CLARA_Vac_Valve_Control as valve

class procedure(object):

    hwc_controller_init = None
    hwc_controller = None

    def __init__(self):
        # super(base, self).__init__()
        object.__init__(self)
        self.my_name = "procedure"
        self.message = None
        #pasds in message function

    def hello(self):
        print(self.my_name + ' says hello')

    def do_something(self):
        self.proc_message(self.my_name + ' running procedure do_something')
        self.init_controller()
        self.proc_message(self.my_name + ' procedure do_something complete')

    def proc_message(self, message, priority = 0):
        if self.message is None:
            self.message(message, priority)
        else:
            print(message, priority)

    def init_controller(self):
        procedure.hwc_controller_init = valve.init()
        procedure.hwc_controller_init = procedure.hwc_controller_init.physical_Vac_Valve_Controller()
