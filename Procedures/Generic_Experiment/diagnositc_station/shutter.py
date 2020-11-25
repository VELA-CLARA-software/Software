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
//  FileName:    screen.py
//  Description: reads in yaml config files for the generic_experiment class...
//      		 Why is parsing config files so messy? What tricks am i issing?
//  			 Why am i asking you?
//
//
"""
from hardware_base import hardware_base
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_enums import MACHINE_MODE
import VELA_CLARA_Shutter_Control as shut
import time

class shutter(hardware_base):
	_my_name = 'shutter'
	# init = shut.init()
	# init.setQuiet()
	#init.setVerbose()
	#controller = None
	init = None
	def __init__(self,mode=MACHINE_MODE.PHYSICAL,area=MACHINE_AREA.CLARA_PH1):
		hardware_base.__init__(self,mode=mode,area=area)
		self._my_name = shutter._my_name
		self.init_shutter()
		self.get_controller_func(self.init.physical_PIL_Shutter_Controller)
		self.get_names(self.controller.getShutterNames)
		print(shutter._my_name + ' has controller, testing procedure')
		self.test_procedure()
		if self.procedure_good:
			print(shutter._my_name + ' Procedure Good')
		else:
			print(shutter._my_name + ' Procedure Bad')

	def init_shutter(self):
		shutter.init = shut.init()
		shutter.init.setQuiet()
		# init.setVerbose()


	def test_procedure(self):
		'assumes [names,state] for each iteration'
		if self.parse_procedure(self.config.shutter_data):
			self.test_names_are_good()
			self.test_values_are_good(type(shut.SHUTTER_STATE.ERROR))
		self.procedure_good = self.names_good & self.values_good

	def next_step(self, num):
		self.iteration = self.get_it_names_values(self.config.shutter_data[num])
		print self.iteration
		for it in self.iteration:
			self.move_shutter(name  =it[0], value = it[1])
		print(shutter._my_name + ' iteration applied')

	def move_shutter(self, name, value):
		if value == shut.SHUTTER_STATE.OPEN:
			self.controller.open(name)
		if value == shut.SHUTTER_STATE.CLOSED:
			self.controller.close(name)

	def is_busy(self):
		if self.is_working:
			self.is_working =not all(self.is_in_state(x[0], x[1]) for x in self.iteration)
		if self.is_working:
			print(shutter._my_name + ' is working')
			print(self.iteration)
		else:
			print(shutter._my_name + ' has finished working')
		return self.is_working

	def is_in_state(self,name,state):
		print(shutter._my_name + ' checking ' + name + ' = ' + str(state) )
		if state == shut.SHUTTER_STATE.OPEN:
			return self.controller.isOpen(name)
		if state == shut.SHUTTER_STATE.CLOSED:
			return self.controller.isClosed(name)