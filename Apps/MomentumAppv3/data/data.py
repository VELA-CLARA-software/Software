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
//  Author:      DJD
//  Last edit:   20-02-2019
//  FileName:    data.py
//  Description: data dictionary and key definitions for MomentumApp application
//
//
//*/
'''

#example_data = 'example_data'
#y = 'y'
I_c = 'I_c'
p_c = 'p_c'

I_predict = 'I_predict'
p_predict = 'p_predict'

I_rough = 'I_rough'
p_rough = 'p_rough'

I_rough_set = 'I_rough_set'
p_rough_set = 'p_rough_set'

rough_step = 'rough_step'
rough_set_step = 'rough_set_step'

I_fine = 'I_fine'
p_fine = 'p_fine'

I_fine_set = 'I_fine_set'
p_fine_set = 'p_fine_set'

fine_set_step = 'fine_set_step'

# list of all keys to use in data dict
all_value_keys = [I_c, p_c, I_predict, p_predict, I_rough, p_rough,  I_rough_set, p_rough_set,
                    rough_step, rough_set_step, I_fine, p_fine,  I_fine_set, p_fine_set, fine_set_step,
                    ]

class data(object):
    # dictionary of all data
    values = {}
    [values.update({x: 0}) for x in all_value_keys]

    previous_values = {}
    [previous_values.update({x: 0}) for x in all_value_keys]

    # don't want some to exist until set in code
    del values[I_predict]
    del values[p_predict]
    del values[I_rough]
    del values[p_rough]
    del values[I_fine]
    del values[p_fine]
    #values[ref_plotted] = False
