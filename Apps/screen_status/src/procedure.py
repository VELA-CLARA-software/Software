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
import sys,os
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release\\')

from VELA_CLARA_Screen_Control import SCREEN_STATE
from VELA_CLARA_Screen_Control import SCREEN_TYPE
import VELA_CLARA_Screen_Control as scr
import VELA_CLARA_Camera_Control as cam
import data as data
import time

class procedure(object):
    # keep this static, there can be only 1
    scrInit = scr.init()
    scrInit.setVerbose()
    #scrInit.setQuiet()
    sc = scrInit.physical_Screen_Controller()


    camInit = cam.init()
    camInit.setQuiet()
    cc = camInit.physical_Camera_Controller()

    screen_state_refs = {}


    data = data.data()

    #devices = {}
    states = {}
    states['SCREEN_MOVING'    ] = scr.SCREEN_STATE.SCREEN_MOVING
    states['V_RETRACTED'      ] = scr.SCREEN_STATE.V_RETRACTED
    states['V_MAX'            ] = scr.SCREEN_STATE.V_MAX
    states['V_MIRROR'         ] = scr.SCREEN_STATE.V_MIRROR
    states['V_YAG'            ] = scr.SCREEN_STATE.V_YAG
    states['V_GRAT'           ] = scr.SCREEN_STATE.V_GRAT
    states['V_SLIT_1'         ] = scr.SCREEN_STATE.V_SLIT_1
    states['V_RF'             ] = scr.SCREEN_STATE.V_RF
    states['V_COL'            ] = scr.SCREEN_STATE.V_COL
    states['H_RETRACTED'      ] = scr.SCREEN_STATE.H_RETRACTED
    states['H_SLIT_1'         ] = scr.SCREEN_STATE.H_SLIT_1
    states['H_SLIT_2'         ] = scr.SCREEN_STATE.H_SLIT_2
    states['H_SLIT_3'         ] = scr.SCREEN_STATE.H_SLIT_3
    states['H_APT_1'          ] = scr.SCREEN_STATE.H_APT_1
    states['H_APT_2'          ] = scr.SCREEN_STATE.H_APT_2
    states['H_APT_3'          ] = scr.SCREEN_STATE.H_APT_3
    states['YAG'          ] = scr.SCREEN_STATE.YAG
    states['RETRACTED'          ] = scr.SCREEN_STATE.RETRACTED


    # The control system takes an appreciable amount of time before a diagnostic station starts moving
    # therefore we will keep a record fo when buttons are clicked,
    # this will be used to set a "clicked" state to the gui, so that operators do not get impatient and click
    # multiple times, we will also set a time_when_clicked so that we can disable the clicked state
    move_attmepted = {}



    def __init__(self):
        self.my_name = 'procedure'

        self.data = data.data
        print('pro __init__ ', self.data.screen_names)

        self.inititialize_values()

        # map of scren state enum to string verion of enum
        #temp = procedure.sc.get_SCREEN_STATE_Definition()
        # we need to reverse this
        self.screen_state_map ={}
        for key, value in procedure.sc.get_SCREEN_STATE_Definition().iteritems():
            print("screen_state_map adding ", value, key)
            self.screen_state_map[value] = key


    def clara_led_on(self):
        procedure.cc.claraLEDOn()

    def clara_led_off(self):
        procedure.cc.claraLEDOff()

    def vela_led_on(self):
        procedure.cc.velaLEDOn()

    def vela_led_off(self):
        procedure.cc.velaLEDOff()

    def inititialize_values(self):
        # get names
        self.data.screen_names = procedure.sc.getScreenNames()
        procedure.screen_state_refs = {}
        for name in self.data.screen_names:
            print('Adding ', name)
            # get valve-obj references
            procedure.screen_state_refs[name] = procedure.sc.getScreenObject(name)
            # get devices for each stage
            self.data.devices[name] = [str(x) for x in procedure.sc.getAvailableDevices(name)]

            print(name, ' has these devices: ', self.data.devices[name])
            self.data.move_attempted[name] = [False, time.time()]

            self.data.v_enabled[name] = procedure.sc.isVEnabled(name)
            self.data.h_enabled[name] = procedure.sc.isHEnabled(name)

        # we have a map of SCREEN_STATE to string
        # state_string_to_state = {v: k for k, v in procedure.sc.get_SCREEN_STATE_Definition().
        #         iteritems()}

    def set_move_attempted(self, name):
        self.data.move_attempted[name] = [True, time.time()]

    def get_screen_devices(self, scr_name):
        #return [str(x) for x in procedure.sc.getAvailableDevices(scr_name)]
        return self.data.devices[scr_name]

    def is_moving(self, name):
        return procedure.sc.isScreenMoving(name)


    # called external to update states
    def update_states(self):
        for name in self.data.screen_names:
            self.data.states[name] = procedure.screen_state_refs[name].screenState


            self.data.v_enabled[name] = procedure.sc.isVEnabled(name)

            if procedure.screen_state_refs[name].screenType is SCREEN_TYPE.CLARA_HV_MOVER:
                self.data.h_enabled[name] = procedure.sc.isHEnabled(name)
            else:
                self.data.h_enabled[name] = False

            #set_state = procedure.screen_state_refs[name].screenSetState
            # if set_state != self.data.states[name]:
            #     pass
                #print(name,set_state,procedure.states[name])
                # if self.data.states[name] != self.m['SCREEN_MOVING'    ]:
                #     self.data.states[name] = 'CLICKED'
            self.data.previous_states = self.data.states

            self.data.clara_led_state = procedure.cc.isClaraLEDOn()
            self.data.vela_led_state = procedure.cc.isVelaLEDOn()



    def make_read_equal_set_all(self):
        procedure.sc.makeSetEqualReadAll()

    def set_state_equal_read_state(self, name):
        return procedure.screen_state_refs[name].screenSetState == procedure.screen_state_refs[name].screenState

    def set_state_NOT_equal_read_state(self, name):
        return rocedure.screen_state_refs[name].screenSetState != procedure.screen_state_refs[name].screenState

    #
    def all_out(self):
        for name in self.data.screen_names:
            self.set_move_attempted(name)
            self.screen_out(name)

    # called external, toggle open or close
    def in_out(self,name):
        print("in_out ", name)
        procedure.states[name] = 'CLICKED'
        if procedure.sc.isYAGIn(name):
            print("try self.screen_in(name)")
            self.screen_out(name)
        else:
            self.screen_in(name)
            print("try self.screen_out(name)")

        #
        # if procedure.sc.isClearForBeam(name):
        #     print(name+' is clear for beam, moving screen in')
        #     self.screen_in(name)
        # else:
        #     print(name+' is NOT clear for beam, moving screen OUT')
        #     self.screen_out(name)

    # called external, open name
    def screen_in(self,name):
        print("procedure screen_in ")
        procedure.sc.insertYAG(name)

    # called external, close name
    def screen_out(self, name):
        dev = procedure.sc.getAvailableDevices(name)
        if scr.SCREEN_STATE.V_RF in dev:
            print("move_screen_to, scr.SCREEN_STATE.V_RF")
            self.move_screen_to(name, scr.SCREEN_STATE.V_RF)
            #procedure.sc.moveScreenTo(name, scr.SCREEN_STATE.V_RF)
        else:
            print("moveScreenOut")
            procedure.sc.moveScreenOut(name)

    def move_screen_to(self, scr, state):
        if procedure.screen_state_refs[scr].screenSetState != state:
            #print("move_screen_to passed, ",scr, state, procedure.states[state])
            #procedure.sc.moveScreenTo( scr,  procedure.m[state])1
            print(procedure.states[state])
            procedure.sc.moveScreenTo( scr, procedure.states[state] )




    # def get_screen_device_map(self):
    #     for name in procedure.scr_names:
    #         procedure.devices[name] = [str(x) for x in procedure.sc.getAvailableDevices(name)]
    #         print(name, ' has ', procedure.devices[name])