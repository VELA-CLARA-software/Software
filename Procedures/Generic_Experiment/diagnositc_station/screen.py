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
import VELA_CLARA_Screen_Control as scr
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_enums import MACHINE_MODE


class screen(hardware_base):
	_my_name = 'screen_mover'

	init = None

	def __init__(self,mode=MACHINE_MODE.PHYSICAL,area=MACHINE_AREA.CLARA_PH1):
		hardware_base.__init__(self,mode=mode,area=area)
		self._my_name = screen._my_name
		self.init_screen()
		print 'get_controller_mode_and_area'

		self.get_controller_mode_and_area(screen.init.getScreenController)
		print 'get names'

		self.get_names(self.controller.getScreenNames)
		print(screen._my_name + ' has controller, testing procedure')
		self.test_procedure()
		if self.procedure_good:
			print(screen._my_name + ' Procedure Good')
		else:
			print(screen._my_name + ' Procedure Bad')


	def init_screen(self):
		print 'screen init'
		screen.init = scr.init()
		screen.init.setQuiet()
		#screen.init.setVerbose()
		print 'screen init fin'


	def test_procedure(self):
			'assumes [names,state] for each iteration'
			if self.parse_procedure(self.config.screen_data):
				self.test_names_are_good()
				self.test_values_are_good(type(scr.SCREEN_STATE.SCREEN_IN))
			self.procedure_good = self.names_good & self.values_good

	'''apply the next iteration'''
	def next_step(self,num):
		print self.config.screen_data[num]
		self.iteration = self.get_it_names_values(self.config.screen_data[num])
		print self.iteration
		for it in self.iteration:
			self.moveScreen(name = it[0], vaue = it[1])
		print(screen._my_name + ' iteration applied')

	def moveScreen(self, name, vaue):
		if vaue == scr.SCREEN_STATE.SCREEN_IN:
			print('moving in  ' + name)
			self.controller.insertYAG(name)
		if vaue == scr.SCREEN_STATE.SCREEN_OUT:
			print('moving out ' + name)
			self.controller.moveScreenOut(name)

	'''if is_busy then self.iteration has not complet'''
	def is_busy(self):
		if self.is_working:
			self.is_working =not all(self.is_in_state(x[0], x[1]) for x in self.iteration)
		return self.is_working

	def is_in_state(self,name,state):
		if state == scr.SCREEN_STATE.SCREEN_IN:
			if self.controller.isScreenIn(name):
				print(name + ' screen is IN')
				return True
			else:
				print(name + ' screen is not IN')
				return False
		if state == scr.SCREEN_STATE.SCREEN_OUT:
			if self.controller.is_HandV_OUT(name):
				print(name +  ' screen is OUT')
				return True
			else:
				print(name + ' screen is not OUT')
				return False
