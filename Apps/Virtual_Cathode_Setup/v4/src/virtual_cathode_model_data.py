#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
              This file is part of VELA-CLARA-Software.                             //
------------------------------------------------------------------------------------//
    VELA-CLARA-Controllers is free software: you can redistribute it and/or modify  //
    it under the terms of the GNU General Public License as published by            //
    the Free Software Foundation, either version 3 of the License, or               //
    (at your option) any later version.                                             //
    VELA-CLARA-Controllers is distributed in the hope that it will be useful,       //
    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
    GNU General Public License for more details.                                    //
                                                                                    //
    You should have received a copy of the GNU General Public License               //
    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //

  Author:      DJS
  Last edit:   20-06-2019
  FileName:    virtual_cathode_model_data.py
  Description: The data dictionary (values) & key definitions for the virtual cathode operator
               application. Also has a previous_values dictionary.
               Data is static so any instance of this class gives access to the same data
'''


class model_data(object):
	'''This class holds all the model data for the app in a dictionary keyed by the strings
	defined below
	The dictionaries are static so all classes can create a data object and have access to
	the latest values. values is a dictionary of all data, initialized to  dummy values
	previous_values is the last iterations values, so we have a memory of state-changes
	This is for MODEL DATA only! it knows nothing of any GUI
	'''

	all_value_keys = []

	# keys for ALL THE DATA we monitor
	time_stamp = 'time_stamp'
	all_value_keys.append(time_stamp)
	# the mask
	mask_x_rbv = 'mask_x_rbv'
	all_value_keys.append(mask_x_rbv)
	mask_y_rbv = 'mask_y_rbv'
	all_value_keys.append(mask_y_rbv)
	mask_x_rad_rbv = 'mask_x_rad_rbv'
	all_value_keys.append(mask_x_rad_rbv)
	mask_y_rad_rbv = 'mask_y_rad_rbv'
	all_value_keys.append(mask_y_rad_rbv)
	mask_x_user = 'mask_x_user'
	all_value_keys.append(mask_x_user)
	mask_y_user = 'mask_y_user'
	all_value_keys.append(mask_y_user)
	mask_x_rad_user = 'mask_x_rad_user'
	all_value_keys.append(mask_x_rad_user)
	mask_y_rad_user = 'mask_y_rad_user'
	all_value_keys.append(mask_y_rad_user)
	mask_feedback = 'mask_feedback'
	all_value_keys.append(mask_feedback)
	# imageCollection
	num_images = 'num_images'
	all_value_keys.append(num_images)
	is_collecting_or_saving = 'is_collecting_or_saving'
	all_value_keys.append(is_collecting_or_saving)
	last_filename = 'last_filename'
	all_value_keys.append(last_filename)
	image = 'image'
	all_value_keys.append(image)
	# shutters
	shutter1_open = 'shutter1_open'
	all_value_keys.append(shutter1_open)
	shutter2_open = 'shutter2_open'
	all_value_keys.append(shutter2_open)
	# these are the names of the shutters, they are filled by the model after instantiation.
	shutter_names = ''
	# cam state
	is_acquiring = 'is_acquiring'
	all_value_keys.append(is_acquiring)
	# image levels
	min_level = 'min_level'
	all_value_keys.append(min_level)
	max_level = 'max_level'
	all_value_keys.append(max_level)
	min_level_rbv = 'min_level_rbv'
	all_value_keys.append(min_level_rbv)
	max_level_rbv = 'max_level_rbv'
	all_value_keys.append(max_level_rbv)
	# image saving
	image_save_dir_root = 'image_save_dir_root'
	all_value_keys.append(image_save_dir_root)
	last_save_dir = 'last_save_dir '
	all_value_keys.append(last_save_dir)
	last_save_file = 'last_save_file'
	all_value_keys.append(last_save_file)
	last_save_path = 'last_save_path'
	all_value_keys.append(last_save_path)
	# imageAnalysis
	is_analysing = 'is_analysing'
	all_value_keys.append(is_analysing)
	use_background = 'use_background'
	all_value_keys.append(use_background)
	use_npoint = 'use_npoint'
	all_value_keys.append(use_npoint)
	ana_step_size = 'ana_step_size'
	all_value_keys.append(ana_step_size)


	# intensity (laser beam)
	las_int = 'las_int'
	all_value_keys.append(las_int)
	las_int_mean = 'las_int_mean'
	all_value_keys.append(las_int_mean)
	las_int_sd = 'las_int_sd'
	all_value_keys.append(las_int_sd)
	las_int_sd_per = 'las_int_sd_per'
	all_value_keys.append(las_int_sd_per)

	# WCM charge
	wcm_val = 'wcm_val'
	all_value_keys.append(wcm_val)
	wcm_mean = 'wcm_mean'
	all_value_keys.append(wcm_mean)
	wcm_sd = 'wcm_sd'
	all_value_keys.append(wcm_sd)
	wcm_sd_per = 'wcm_sd_per'
	all_value_keys.append(wcm_sd_per)

	# image pixel average value
	img_avg = 'img_avg'
	all_value_keys.append(img_avg)
	img_avg_mean = 'img_avg_mean'
	all_value_keys.append(img_avg_mean)
	img_avg_sd = 'img_avg_sd'
	all_value_keys.append(img_avg_sd)
	img_avg_sd_per = 'img_avg_sd_per'
	all_value_keys.append(img_avg_sd_per)

	# analysis results  in mm
	x_mm = 'x_mm'
	all_value_keys.append(x_mm)
	x_mean_mm = 'x_mean_mm'
	all_value_keys.append(x_mean_mm)
	x_sd_mm = 'x_sd_mm'
	all_value_keys.append(x_sd_mm)
	x_sd_mm_per = 'x_sd_mm_per'
	all_value_keys.append(x_sd_mm_per)
	y_mm = 'y_mm'
	all_value_keys.append(y_mm)
	y_mean_mm = 'y_mean_mm'
	all_value_keys.append(y_mean_mm)
	y_sd_mm = 'y_sd_mm'
	all_value_keys.append(y_sd_mm)
	y_sd_mm_per = 'y_sd_mm_per'
	all_value_keys.append(y_sd_mm_per)

	sx_mm = 'sx_mm'
	all_value_keys.append(sx_mm)
	sx_mean_mm = 'sx_mean_mm'
	all_value_keys.append(sx_mean_mm)
	sx_sd_mm = 'sx_sd_mm'
	all_value_keys.append(sx_sd_mm)
	sx_sd_mm_per = 'sx_sd_mm_per'
	all_value_keys.append(sx_sd_mm_per)
	sy_mm = 'sy_mm'
	all_value_keys.append(sy_mm)
	sy_mean_mm = 'sy_mean_mm'
	all_value_keys.append(sy_mean_mm)
	sy_sd_mm = 'sy_sd_mm'
	all_value_keys.append(sy_sd_mm)
	sy_sd_mm_per = 'sy_sd_mm_per'
	all_value_keys.append(sy_sd_mm_per)
	cov_mm = 'cov_mm'
	all_value_keys.append(cov_mm)
	cov_mean_mm = 'cov_mean_mm'
	all_value_keys.append(cov_mean_mm)
	cov_sd_mm = 'cov_sd_mm'
	all_value_keys.append(cov_sd_mm)
	cov_sd_mm_per = 'cov_sd_mm_per'
	all_value_keys.append(cov_sd_mm_per)

	x_pix = 'x_pix'
	all_value_keys.append(x_pix)
	x_mean_pix = 'x_mean_pix'
	all_value_keys.append(x_mean_pix)
	x_sd_pix = 'x_sd_pix'
	all_value_keys.append(x_sd_pix)
	x_sd_pix_per = 'x_sd_pix_per'
	all_value_keys.append(x_sd_pix_per)
	y_pix = 'y_pix'
	all_value_keys.append(y_pix)
	y_mean_pix = 'y_mean_pix'
	all_value_keys.append(y_mean_pix)
	y_sd_pix = 'y_sd_pix'
	all_value_keys.append(y_sd_pix)
	y_sd_pix_per = 'y_sd_pix_per'
	all_value_keys.append(y_sd_pix_per)
	sx_pix = 'sx_pix'
	all_value_keys.append(sx_pix)
	sx_mean_pix = 'sx_mean_pix'
	all_value_keys.append(sx_mean_pix)
	sx_sd_pix = 'sx_sd_pix'
	all_value_keys.append(sx_sd_pix)
	sx_sd_pix_per = 'sx_sd_pix_per'
	all_value_keys.append(sx_sd_pix_per)
	sy_pix = 'sy_pix'
	all_value_keys.append(sy_pix)
	sy_mean_pix = 'sy_mean_pix'
	all_value_keys.append(sy_mean_pix)
	sy_sd_pix = 'sy_sd_pix'
	all_value_keys.append(sy_sd_pix)
	sy_sd_pix_per = 'sy_sd_pix_per'
	all_value_keys.append(sy_sd_pix_per)
	cov_pix = 'cov_pix'
	all_value_keys.append(cov_pix)
	cov_mean_pix = 'cov_mean_pix'
	all_value_keys.append(cov_mean_pix)
	cov_sd_pix = 'cov_sd_pix'
	all_value_keys.append(cov_sd_pix)
	cov_sd_pix_per = 'cov_sd_pix_per'
	all_value_keys.append(cov_sd_pix_per)



	avg_pix_beam_level = 'avg_pix_beam_level'
	all_value_keys.append(avg_pix_beam_level)
	# analyse buffers (not used)
	x_buf = 'x_buf'
	all_value_keys.append(x_buf)
	y_buf = 'y_buf'
	all_value_keys.append(y_buf)
	sx_buf = 'sx_buf'
	all_value_keys.append(sx_buf)
	sy_buf = 'sy_buf'
	all_value_keys.append(sy_buf)
	i_buf = 'i_buf'
	all_value_keys.append(i_buf)
	cov_buf = 'cov_buf'
	all_value_keys.append(cov_buf)
	# PIL mirror movers
	H_step_read = 'H_step_read'
	all_value_keys.append(H_step_read)
	V_step_read = 'V_step_read'
	all_value_keys.append(V_step_read)
	# PIL Half Wave Plate
	hwp_read = 'hwp_read'
	all_value_keys.append(hwp_read)
	# image constants
	num_pix_x = 'num_pix_x'
	all_value_keys.append(num_pix_x)
	num_pix_y = 'num_pix_y'
	all_value_keys.append(num_pix_y)
	x_pix_to_mm = 'x_pix_to_mm'
	all_value_keys.append(x_pix_to_mm)
	y_pix_to_mm = 'y_pix_to_mm'
	all_value_keys.append(y_pix_to_mm)
	x_pix_scale_factor = 'x_pix_scale_factor'
	all_value_keys.append(x_pix_scale_factor)
	y_pix_scale_factor = 'y_pix_scale_factor'
	all_value_keys.append(y_pix_scale_factor)
	xpix_full = 'xpix_full'
	all_value_keys.append(xpix_full)
	ypix_full = 'ypix_full'
	all_value_keys.append(ypix_full)
	is_setting_pos = 'is_setting_pos'
	all_value_keys.append(is_setting_pos)

	rs_buffer_size = 'rs_buffer_size'
	all_value_keys.append(rs_buffer_size)

	rs_buffer_count = 'rs_buffer_count'
	all_value_keys.append(rs_buffer_count)

	rs_buffer_full  = 'rs_buffer_full'
	all_value_keys.append(rs_buffer_full)

	rs_auto_reset  = 'rs_auto_reset'
	all_value_keys.append(rs_auto_reset)

	hwp_enable_state  = 'hwp_enable_state'
	all_value_keys.append(hwp_enable_state)

	# laser_buffer_full = 'laser_buffer_full'
	# all_value_keys.append(laser_buffer_full)
	# wcm_buffer_full = 'wcm_buffer_full'
	# all_value_keys.append(wcm_buffer_full)
	# pixel_avg_buffer_full = 'pixel_avg_buffer_full'
	# all_value_keys.append(pixel_avg_buffer_full)
	# x_buffer_full = 'x_buffer_full'
	# all_value_keys.append(x_buffer_full)
	# y_buffer_full = 'y_buffer_full'
	# all_value_keys.append(y_buffer_full)
	# sig_x_buffer_full = 'sig_x_buffer_full'
	# all_value_keys.append(sig_x_buffer_full)
	# sig_y_buffer_full = 'sig_y_buffer_full'
	# all_value_keys.append(sig_y_buffer_full)
	# cov_xy_buffer_full = 'cov_xy_buffer_full'
	# all_value_keys.append(cov_xy_buffer_full)


	# object names, These are the shutter names in the c++
	shut1 = 'SHUT01'
	shut2 = 'SHUT02'
	# these are object names as used in Python they will be used to reference object used in the
	# PIL
	vc_image_data = 'vc_image_data_object'
	vc_daq = 'vc_daq_object'
	pil_object = 'pil_object'
	vc_cam = 'vc_cam_object'
	vc_image = 'vc_image'
	vc_state = 'vc_state'
	vc_mask = 'vc_mask'
	pil_mirror = 'pil_mirror'


	# list of all keys to use in data dict
	# all_value_keys = [time_stamp, mask_x_rbv, mask_y_rbv, mask_x_rad_rbv, mask_y_rad_rbv,
	#                   mask_x_user, mask_y_user, mask_x_rad_user, mask_y_rad_user, mask_feedback,
	#                   num_images, is_collecting_or_saving, last_filename, is_acquiring, min_level,
	#                   min_level_rbv, max_level, max_level_rbv, is_analysing, use_background,
	#                   use_npoint, ana_step_size,
	#
	#                   x_mm, y_mm, sx_mm, sy_mm, int_val, wcm_val, avg_pix_val,
	#                   #x_val_mm, y_val_mm, sx_val_mm, sy_val_mm,
	# 				  int_val, avg_pix_val,
	#                   x_mean_mm, y_mean_mm, sx_mean_mm, sy_mean_mm,
	#                   x_mean_pix, y_mean_pix, sx_mean_pix, sy_mean_pix,
	#                   int_mean, wcm_mean,cov_val,
	#                   cov_mean, avg_pix_mean,
	#                   x_sd_mm, y_sd_mm, sx_sd_mm, sy_sd_mm, int_sd_mm, wcm_sd, cov_sd_mm,
	#                   x_sd_mm_per, y_sd_mm_per, sx_sd_mm_per, sy_sd_mm_per, int_sd_mm_per, wcm_sd_per, cov_sd_mm_per,
	#                   x_sd_per, y_sd_per, sx_sd_per, sy_sd_per, cov_sd_per,
	#                   avg_pix_sd, x_buf, y_buf, sx_buf, sy_buf, i_buf, cov_buf, image,
	#                   shutter1_open, is_setting_pos, shutter2_open, H_step_read, V_step_read,
	#                   xpix_full, ypix_full, x_pix, y_pix, sig_x_pix, sig_y_pix, last_save_dir,
	#                   last_save_file, last_save_path, num_pix_x, num_pix_y, x_pix_to_mm,
	#                   y_pix_to_mm, image_save_dir_root, rs_buffer_size, laser_buffer_full,
	#                   wcm_buffer_full, pixel_avg_buffer_full, x_buffer_full, y_buffer_full,
	#                   y_buffer_full, sig_x_buffer_full, sig_y_buffer_full, cov_xy_buffer_full,
	#                   shutter_names,avg_pix_beam_level]

	#
	# values is the main dictionary for all the data
	values = {}
	[values.update({x: 0}) for x in all_value_keys]
	#
	# manually set some values
	values[image_save_dir_root] = '\\\\claraserv3.dl.ac.uk'  # MAGIC_STRING
	#
	# values gets copied to previous_values before values is updated
	previous_values = {}
	[previous_values.update({x: 0}) for x in all_value_keys]