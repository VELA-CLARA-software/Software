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
//  FileName:    data.py
//  Description: template for class for gui class in generic High Level Application
//
//
//*/
'''




class data(object):
    stage_names = 'stage_names'
    stage_positions = 'stage_positions'
    stage_read_equal_set = 'stage_read_equal_set'
    stage_set_positions = 'stage_set_positions'
    stage_devices = 'stage_devices'

    values = {}
    values[stage_names] = []
    values[stage_positions] = {}
    values[stage_set_positions] = {}
    values[stage_read_equal_set] = {}
    values[stage_devices] = {}



    def __init__(self):
        # super(base, self).__init__()
        object.__init__(self)
        self.my_name = "data"

    def hello(self):
        print(self.my_name+ ' says hello')