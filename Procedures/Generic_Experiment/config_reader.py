"""
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Controllers is distributed in the hope that it will be useful,       //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   27-03-2018
//  FileName:    config_reader.py
//  Description: reads in yaml config files for the generic_experiment class...
//      		 Why is parsing config files so messy? What tricks am i issing?
//  			 Why am i asking you?
//
//
"""
import yaml
from gen_ex_data import General_Experiment_Data
from gen_ex_data import HWC_data
from data_logger import Data_Logger


class Config_Reader():
	my_name = 'Config_Reader'
	_config_filename = None
	data = General_Experiment_Data()
	logger  = Data_Logger()
	def __init__(self, file_name=''):
		Config_Reader._config_filename = file_name

	def read_file(self,file_name=''):
		"""read_file reads a generic experimental config file, yaml format etc...
		   yes, two lines, that's all it takes ...
		"""
		if file_name == '':
			pass
		else:
			Config_Reader._config_filename = file_name
		# Try reading the config file
		try:
			stream = file(Config_Reader._config_filename , 'r')
		except:
			Config_Reader.logger.message(['MAJOR ERROR Can not read config file =',
			                             Config_Reader._config_filename])
		else:
			Config_Reader.data.raw_config_data = yaml.load(stream)
			# some basic parsing
			self.set_main_flags()
			# the main parsing
			self.parse_file()
		if Config_Reader.data.config_data_good:
			Config_Reader.logger.message('GOOD CONFIG DATA')
		else:
			Config_Reader.logger.message('BAD CONFIG DATA')

	def set_main_flags(self):
		# some aliases
		r = Config_Reader.data.raw_config_data
		t = Config_Reader.data.top_level_kwrds_flags
		# iterate over top level keywords and set flag = True
		# if they are found in the config file
		for word in r:
			t[word] = True
		# for key, value in t.iteritems():
		# 	print key, value

	def parse_file(self):
		"""
		This will parse the config file and extract information
		this info will be needed to check the integrity of the config
		before applying the config to an experiment
			1. which HWC to create
			2. which elements
		"""
		# some useful alises
		d = Config_Reader.data
		t = Config_Reader.data.top_level_kwrds_flags
		r = Config_Reader.data.raw_config_data
		k = Config_Reader.data.top_level_kwrds

		# step through each setting that is required
		# 1: the machine mode MUST be set
		if t[d.GLOBAL]:
			# optional
			d.log_file_set = self.set_script_log_file()
			# mandatory
			self.get_machine_mode()
		else:
			print()
		# 2. if machine_mode_set we MUST have some controllers
		if d.machine_mode_set:
			self.get_controllers()
		# 3. If we have controllers we MUST have an experiment
		if d.controller_set:
			d.experiment_set = self.get_experiment()
		# 4. do the experiment elements exist in the controllers we have?
		if d.experiment_set:
			d.elements_exist = self.get_elements()
		Config_Reader.data.config_data_good = d.elements_exist

	def get_machine_mode(self):
		Config_Reader.logger.message('Finding MachineMode', True)
		# to get here ...
		# GLOBAL must exist in the config
		# aliases
		d = Config_Reader.data
		r = Config_Reader.data.raw_config_data[d.GLOBAL]
		if d.MACHINE_MODE in r:
			d.machine_mode = d.machine_modes.get(r[d.MACHINE_MODE])
		if d.machine_mode is not  None:
			d.machine_mode_set = True
			Config_Reader.logger.message('Machine Mode = ' + r[d.MACHINE_MODE],True)
		return d.machine_mode_set

	def get_controllers(self):
		Config_Reader.logger.message('Finding Controllers', True)
		# go over these flags and get the machine area for each controller
		d = Config_Reader.data
		r = Config_Reader.data.raw_config_data
		t = Config_Reader.data.top_level_kwrds_flags
		for item in d.all_controllers:
			if t[item]:
				# the yaml file may contain a list of areas or a single area,
				# so check that here
				if isinstance(r[item].get(d.MACHINE_AREA), basestring):
					d.HWC_data_list.append(
						HWC_data(type = d.controller_types.get(item),
				                 mode = d.machine_mode,
								 area = d.machine_areas.get(r[item].get(d.MACHINE_AREA)))
					)
				elif isinstance(r[item].get(d.MACHINE_AREA), list):
					for area in r[item].get(d.MACHINE_AREA):
						d.HWC_data_list.append(
							HWC_data(type=d.controller_types.get(item),
							         mode=d.machine_mode,
							         area=d.machine_areas.get(area))
						)
			else:
				Config_Reader.logger.message(['Not using a', item,'controller'], True)
		# check d.HWC_data_list for None types, if they exist assume an error
		a = True
		for item in d.HWC_data_list:
			s = [d.controller_types_inv.get(item.type),
			     d.machine_modes_inv.get(item.mode),
			     d.machine_areas_inv.get(item.area)]
			if None in item:
				s.insert(0,'Error in HWC config:')
				a = False
			else:
				s.insert(0,'Found HWC:')
			Config_Reader.logger.message(s, True)
		d.controller_set = a

	def get_experiment(self):
		Config_Reader.logger.message('Finding Experiment', True)
		return False

	def get_elements(self):
		Config_Reader.logger.message('Finding Elements', True)
		return False

	def set_script_log_file(self):
		# aliases
		d = Config_Reader.data
		r = Config_Reader.data.raw_config_data[d.GLOBAL]
		Config_Reader.logger.set_working_directory( r.get(d.WORKING_DIRECTORY))
		Config_Reader.logger.set_log_file( r.get(d.SCRIPT_LOG_FILE))

