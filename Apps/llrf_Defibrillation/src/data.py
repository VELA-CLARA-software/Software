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
//  Description: template for class for gui_source class in generic High Level Application
//
//
//*/
'''





class data(object):

    gun_keep_alive_value = "gun_keep_alive_value"
    linac_keep_alive_value = "linac_keep_alive_value"

    old_gun_keep_alive_value = "old_gun_keep_alive_value"
    old_linac_keep_alive_value = "old_linac_keep_alive_value"


    should_keep_linac_alive = "should_keep_linac_alive"
    should_keep_gun_alive = "should_keep_gun_alive"

    values = {}

    values[gun_keep_alive_value] = 0
    values[linac_keep_alive_value] = 0
    values[old_gun_keep_alive_value] = 0
    values[old_linac_keep_alive_value] = 0
    values[should_keep_linac_alive] = False
    values[should_keep_gun_alive] = False


    def __init__(self):
        # super(base, self).__init__()
        object.__init__(self)
        pass


