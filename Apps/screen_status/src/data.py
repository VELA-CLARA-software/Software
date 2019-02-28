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
    screen_state_refs = {}
    devices = {}
    state_string_to_state = {}

    def __init__(self):
        object.__init__(self)
        self.my_name = "data"

    def hello(self):
        print(self.my_name+ ' says hello')



