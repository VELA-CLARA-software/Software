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
//  Last edit:   05-06-2018
//  FileName:    procedure.oy
//  Description: Generic template for procedure class for High Level Application
//               has simple interface (i.e. just an dictionary, and well-named functions)
//
//*/
'''
import VELA_CLARA_Vac_Valve_Control as valve


class procedure(object):
    # init HWC
    valveInit = valve.init()
    #valveInit.setVerbose()
    vv = valveInit.physical_Vac_Valve_Controller()

    # get names
    valve_names = vv.getNames()

    # get valve-obj references
    valve_refs = {}
    for name in valve_names:
        print('Adding ', name)
        valve_refs[name] = vv.getVacValveObjConstRef(name)

    # empty dict to store latest state in
    valve_states = {}

    def __init__(self):
        self.my_name = 'procedure'
        print(self.my_name + ', class initiliazed')

    # called external to update states
    def update_states(self):
        for name in procedure.valve_names:
            procedure.valve_states[name] = procedure.valve_refs[name].state
            #print name + ' state = ' + str(procedure.valve_states[name])

    # called external, toggle open or close
    def open_or_close(self,name):
        if procedure.valve_states[name] == valve.VALVE_STATE.VALVE_OPEN:
            self.close(name)
        elif procedure.valve_states[name] == valve.VALVE_STATE.VALVE_CLOSED:
            self.open(name)

    # called external, open name
    def open(self,name):
        procedure.vv.open(name)

    # called external, close name
    def close(self, name):
        procedure.vv.close(name)

    # called external, open all valves
    def open_all(self):
        for name in procedure.valve_names:
            procedure.vv.open(name)

    # called external, close all valves
    def close_all(self):
        for name in procedure.valve_names:
            procedure.vv.close(name)