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
//
//
//*/
'''
from VELA_CLARA_Screen_Control import SCREEN_STATE
import VELA_CLARA_Screen_Control as scr


class procedure(object):
    # initDAQ = daq.init()
    scrInit = scr.init()
    scrInit.setVerbose()
    scrInit.setQuiet()

    sc = scrInit.physical_Screen_Controller()

    # get names
    scr_names = sc.getScreenNames()

    # get valve-obj references
    scr_state_refs = {}
    for name in scr_names:
        print('Adding ', name)
        scr_state_refs[name] = sc.getScreenObject(name)


    # this list will be used by the view to update states
    states = {}
    previous_states = {}


    devices = {}
    m = {}
    m['SCREEN_MOVING'    ] = SCREEN_STATE.SCREEN_MOVING
    m['V_RETRACTED'      ] = SCREEN_STATE.V_RETRACTED
    m['V_MAX'            ] = SCREEN_STATE.V_MAX
    m['V_MIRROR'         ] = SCREEN_STATE.V_MIRROR
    m['V_YAG'            ] = SCREEN_STATE.V_YAG
    m['V_GRAT'           ] = SCREEN_STATE.V_GRAT
    m['V_SLIT_1'         ] = SCREEN_STATE.V_SLIT_1
    m['V_RF'             ] = SCREEN_STATE.V_RF
    m['V_COL'            ] = SCREEN_STATE.V_COL
    m['H_RETRACTED'      ] = SCREEN_STATE.H_RETRACTED
    m['H_SLIT_1'         ] = SCREEN_STATE.H_SLIT_1
    m['H_SLIT_2'         ] = SCREEN_STATE.H_SLIT_2
    m['H_SLIT_3'         ] = SCREEN_STATE.H_SLIT_3
    m['H_APT_1'          ] = SCREEN_STATE.H_APT_1
    m['H_APT_2'          ] = SCREEN_STATE.H_APT_2
    m['H_APT_3'          ] = SCREEN_STATE.H_APT_3


    def __init__(self):
        self.my_name = 'procedure'
        self.get_screen_device_map()

        # map of scren state enum to string verion of enum
        temp = procedure.sc.get_SCREEN_STATE_Definition()
        # we need to reverse this
        self.screen_state_map ={}
        for key, value in temp.iteritems():
            print("screen_state_map addinmg", value, key)
            self.screen_state_map[value] = key



    def get_screen_device_map(self):
        for name in procedure.scr_names:
            procedure.devices[name] = [str(x) for x in procedure.sc.getAvailableDevices(name)]
            print(name, ' has ', procedure.devices[name])

    def get_screen_devices(self, scr_name):
        return [str(x) for x in procedure.sc.getAvailableDevices(scr_name)]


    def is_moving(self, name):
        return procedure.sc.isScreenMoving(name)


    # called external to update states
    def update_states(self):
        for name in procedure.scr_names:
            procedure.states[name] = procedure.scr_state_refs[name].screenState
            # check for moving:
            # if procedure.sc.isScreenMoving(name):
            #     procedure.states[name] = scr.DRIVER_STATE.H_DRIVER_MOVING
           # print name + ' state = ' + str(procedure.states[name])
        procedure.previous_states = procedure.states

    # called external, toggle open or close
    def in_out(self,name):
        procedure.states[name] = 'CLICKED'
        if procedure.sc.isClearForBeam(name):
            print(name+' is clear for beam, move screen in?')
            self.screen_in(name)
        else:
            print(name+' is NOT clear for beam, move screen OUT?')
            self.screen_out(name)

    # called external, open name
    def screen_in(self,name):
        procedure.sc.insertYAG(name)

    # called external, close name
    def screen_out(self, name):
        dev = procedure.sc.getAvailableDevices(name)
        if scr.SCREEN_STATE.V_RF in dev:
            procedure.sc.moveScreenTo(name, scr.SCREEN_STATE.V_RF)
        else:
            procedure.sc.moveScreenOut(name)

    # called external, close all valves
    def all_out(self):
        for name in procedure.scr_names:
            self.stop(name)

    def move_screen_to(self, scr, state):
        print("move_screen_to passed, ",scr, state, procedure.m[state])
        #procedure.sc.moveScreenTo( scr,  procedure.m[state])
        procedure.sc.moveScreenTo( scr,  )