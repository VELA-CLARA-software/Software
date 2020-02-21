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
//  Last edit:   26-02-2019
//  FileName:    data.py
//  Description: screen_stats data
//
//
//*/
'''


class data(object):

    # all screen names
    screen_names = []

    # this list will be used by the view to update states
    states = {}
    previous_states = {}

    # references to each screen object, from which to read th estate
    devices = {}
    state_string_to_state = {}

    # The control system takes an appreciable amount of time before a diagnostic station starts moving
    # therefore we will keep a record fo when buttons are clicked,
    # this will be used to set a "clicked" state to the gui, so that operators do not get impatient and click
    # multiple times, we will also set a time_when_clicked so that we can disable the clicked state
    move_attempt_wait_time = 8
    move_attempted = {}

    # THE ONLY (?) way to know that a screen has FINISHED moving is to check that both the H and V drives are not
    # enabled (but what about pnuematic screens???)
    v_enabled = {}
    h_enabled = {}

    clara_led_state = False
    vela_led_state = False

    def __init__(self):
        object.__init__(self)


    def hello(self):
        print(__name,' says hello')



