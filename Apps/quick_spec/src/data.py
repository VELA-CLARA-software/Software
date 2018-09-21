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
//  Last edit:   21-09-2018
//  FileName:    data.py
//  Description: data dictionary and key definitions for quick_spec application
//
//
//*/
'''

image_data = 'image_data'
x_proj = 'x_proj'
y_proj = 'y_proj'

y_proj_max_index= 'y_proj_max_index'
x_proj_max_index= 'x_proj_max_index'

y_proj_max = 'y_proj_max'
x_proj_max = 'x_proj_max'

x_proj_rolling_sum = 'x_proj_rolling_sum'
y_proj_rolling_sum = 'y_proj_rolling_sum'
x_proj_mean = 'x_proj_mean'
y_proj_mean = 'y_proj_mean'
rolling_count = 'rolling_count'
fwhm = 'fwhm'

y_ref = 'y_ref'
x_ref = 'x_ref'

y_proj_max = 'y_proj_max'
x_proj_max = 'x_proj_max'

y_proj_min = 'y_proj_min'
x_proj_min = 'x_proj_min'

sub_min = 'sub_min'
use_ROI = 'use_ROI'
average = 'average'

has_ref = 'has_ref'
ref_plotted = 'ref_plotted'

num_x_pix = 'num_x_pix'
num_y_pix = 'num_y_pix'

current_cam = 'current_cam'
last_cam  = 'last_cam'

got_image = 'got_image'

fwhm_lo = 'fwhm_lo'
fwhm_hi = 'fwhm_hi'


# list of all keys to use in data dict
all_value_keys = [image_data,x_proj, y_proj, x_proj_rolling_sum ,y_proj_rolling_sum ,x_proj_mean ,
                  y_proj_mean ,rolling_count,y_proj_max,x_proj_max,y_proj_min,x_proj_min,
                  sub_min, use_ROI, average, has_ref, num_x_pix, num_y_pix, current_cam, y_ref,
                  x_ref,ref_plotted, y_proj_max, y_proj_max,y_proj_max_index,
                  y_proj_max_index, fwhm, fwhm_lo, fwhm_hi, got_image]

class data(object):
    # dictionary of all data
    values = {}
    [values.update({x: 0}) for x in all_value_keys]

    previous_values = {}
    [previous_values.update({x: 0}) for x in all_value_keys]

    values[ref_plotted] = False