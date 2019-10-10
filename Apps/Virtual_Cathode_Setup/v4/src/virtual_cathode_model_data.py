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

	# keys for ALL THE DATA we monitor
	time_stamp = 'time_stamp'
	# the mask
	mask_x_rbv = 'mask_x_rbv'
	mask_y_rbv = 'mask_y_rbv'
	mask_x_rad_rbv = 'mask_x_rad_rbv'
	mask_y_rad_rbv = 'mask_y_rad_rbv'
	mask_x_user = 'mask_x_user'
	mask_y_user = 'mask_y_user'
	mask_x_rad_user = 'mask_x_rad_user'
	mask_y_rad_user = 'mask_y_rad_user'
	mask_feedback = 'mask_feedback'
	# imageCollection
	num_images = 'num_images'
	is_collecting_or_saving = 'is_collecting_or_saving'
	last_filename = 'last_filename'
	image = 'image'
	# shutters
	shutter1_open = 'shutter1_open'
	shutter2_open = 'shutter2_open'
	# these are the names of the shutters, they are filled by the model after instantiation.
	shutter_names = ''
	# cam state
	is_acquiring = 'is_acquiring'
	# image levels
	min_level = 'min_level'
	max_level = 'max_level'
	min_level_rbv = 'min_level_rbv'
	max_level_rbv = 'max_level_rbv'
	# image saving
	image_save_dir_root = 'image_save_dir_root'
	last_save_dir = 'last_save_dir '
	last_save_file = 'last_save_file'
	last_save_path = 'last_save_path'
	# imageAnalysis
	is_analysing = 'is_analysing'
	use_background = 'use_background'
	use_npoint = 'use_npoint'
	ana_step_size = 'ana_step_size'
	# analysis results in pixels
	x_pix = 'x_pix'
	y_pix = 'y_pix'
	sig_x_pix = 'sig_x_pix'
	sig_y_pix = "sig_y_pix"
	# analysis results  in mm
	x_val = 'x_val'
	y_val = 'y_val'
	sx_val = 'sx_val'
	sy_val = 'sy_val'
	cov_val = 'cov_val'
	avg_pix_val = 'avg_val'
	# intensity (laser beam)
	int_val = 'int_val'
	# WCm charge
	wcm_val = 'wcm_val'
	# The below come from running stats in c++ controller)
	# analyse means (mm)
	x_mean = 'x_mean'
	y_mean = 'y_mean'
	sx_mean = 'sx_mean'
	sy_mean = 'sy_mean'
	int_mean = 'int_mean'
	wcm_mean = 'wcm_mean'
	cov_mean = 'cov_mean'
	avg_pix_mean = 'avg_mean'
	# analyse standard deviation (mm)
	x_sd = 'x_sd'
	y_sd = 'y_sd'
	sx_sd = 'sx_sd'
	sy_sd = 'sy_sd'
	int_sd = 'int_sd'
	wcm_sd = 'wcm_sd'
	cov_sd = 'cov_sd'
	avg_pix_sd = 'avg_pix_sd'
	# analyse buffers (not used)
	x_buf = 'x_buf'
	y_buf = 'y_buf'
	sx_buf = 'sx_buf'
	sy_buf = 'sy_buf'
	i_buf = 'i_buf'
	cov_buf = 'cov_buf'
	# PIL mirror movers
	H_step_read = 'H_step_read'
	V_step_read = 'V_step_read'
	# PIL Half Wave Plate
	hwp_read = 'hwp_read'
	# image constants
	num_pix_x = 'num_pix_x'
	num_pix_y = 'num_pix_y'
	x_pix_to_mm = 'x_pix_to_mm'
	y_pix_to_mm = 'y_pix_to_mm'
	x_pix_scale_factor = 'x_pix_scale_factor'
	y_pix_scale_factor = 'y_pix_scale_factor'
	xpix_full = 'xpix_full'
	ypix_full = 'ypix_full'
	is_setting_pos = 'is_setting_pos'
	rs_buffer_size = 'rs_buffer_size'

	laser_buffer_full = 'laser_buffer_full'
	wcm_buffer_full = 'wcm_buffer_full'
	pixel_avg_buffer_full = 'pixel_avg_buffer_full'
	x_buffer_full = 'x_buffer_full'
	y_buffer_full = 'y_buffer_full'
	sig_x_buffer_full = 'sig_x_buffer_full'
	sig_y_buffer_full = 'sig_y_buffer_full'
	cov_xy_buffer_full = 'cov_xy_buffer_full'

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
	all_value_keys = [time_stamp, mask_x_rbv, mask_y_rbv, mask_x_rad_rbv, mask_y_rad_rbv,
	                  mask_x_user, mask_y_user, mask_x_rad_user, mask_y_rad_user, mask_feedback,
	                  num_images, is_collecting_or_saving, last_filename, is_acquiring, min_level,
	                  min_level_rbv, max_level, max_level_rbv, is_analysing, use_background,
	                  use_npoint, ana_step_size, x_val, y_val, sx_val, sy_val, int_val, wcm_val,
	                  cov_val, avg_pix_val, x_mean, y_mean, sx_mean, sy_mean, int_mean, wcm_mean,
	                  cov_mean, avg_pix_mean, x_sd, y_sd, sx_sd, sy_sd, int_sd, wcm_sd, cov_sd,
	                  avg_pix_sd, x_buf, y_buf, sx_buf, sy_buf, i_buf, cov_buf, image,
	                  shutter1_open, is_setting_pos, shutter2_open, H_step_read, V_step_read,
	                  xpix_full, ypix_full, x_pix, y_pix, sig_x_pix, sig_y_pix, last_save_dir,
	                  last_save_file, last_save_path, num_pix_x, num_pix_y, x_pix_to_mm,
	                  y_pix_to_mm, image_save_dir_root, rs_buffer_size, laser_buffer_full,
	                  wcm_buffer_full, pixel_avg_buffer_full, x_buffer_full, y_buffer_full,
	                  y_buffer_full, sig_x_buffer_full, sig_y_buffer_full, cov_xy_buffer_full,
	                  shutter_names]
	#
	# values is the main dictionary for all the data
	values = {}
	[values.update({x: 0}) for x in all_value_keys]
	#
	# manually set some values
	values[image_save_dir_root] = '\\\\claraserv3'  # MAGIC_STRING
	#
	# values gets copied to previous_values before values is updated
	previous_values = {}
	[previous_values.update({x: 0}) for x in all_value_keys]