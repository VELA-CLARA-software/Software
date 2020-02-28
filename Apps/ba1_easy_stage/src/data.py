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
    '''
    data is grouped into different types, each with own dict within a dict

    '''

    # labels for dictionaries for different data-=sets

    stage_numbers = 'stage_numbers' #The stages have numbers, defined in config, makes book-keeping easier
    stage_names = 'stage_names' # The stages have numbers, defined in config, makes book-keeping easier
    stage_devices = 'stage_devices'
    read_device = 'read_device'
    set_device = 'set_device'
    move_to_dev = 'move_to_dev'
    read_pos = 'read_pos'
    is_moving = 'is_moving'
    old_read_pos = 'old_read_pos' #Memory of old vals to decide if stages are moving and  how to updat
    # widgets
    # etc.
    set_pos = 'set_pos'
    new_set_pos = 'new_set_pos'

    precision = 'precision'

    move_to_set = 'move_to_set'
    min_pos = 'min_pos'
    max_pos = 'max_pos'
    stage_read_equal_set = 'stage_read_equal_set'
    active_stage_numbers = 'active_stage_numbers'

    clear_for_beam_value = 'clear_for_beam_value'
    is_clear_for_beam = 'is_clear_for_beam'

    # WE'VE
    CLEAR_FOR_BEAM = 'CLEAR_FOR_BEAM'


    # all values go in here
    values = {}
    # for each value type go in the dictionary
    values[stage_devices] = {}
    values[stage_numbers] = {}
    values[stage_names] = {}

    values[read_device] = {}
    values[set_device] = {}

    #values[move_to_dev] = {}
    values[set_pos] = {}
    values[new_set_pos] = {}

    #
    values[min_pos] = {}
    values[max_pos] = {}
    values[precision] = {}

    # we get the read position, keep a copy of teh old od read position, and use these to set an is_moving flag,
    # is_moving is used by the GUI
    values[read_pos] = {}
    values[old_read_pos] = {}
    values[is_moving] = {}

    values[clear_for_beam_value] = {}
    values[is_clear_for_beam] = {}

    stage_number_to_name = {}

    values[active_stage_numbers] = []


    def __init__(self):
        # super(base, self).__init__()
        object.__init__(self)
        self.my_name = "data"

    def hello(self):
        print(self.my_name+ ' says hello')