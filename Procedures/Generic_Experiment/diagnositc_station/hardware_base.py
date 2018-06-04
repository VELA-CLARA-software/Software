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
from VELA_CLARA_enums import MACHINE_MODE
from VELA_CLARA_enums import MACHINE_AREA

import gen_ex_config
import time

class hardware_base(object):
    _my_name = 'hardware_base'
    config = gen_ex_config.gen_ex_config()
    def __init__(self,mode = MACHINE_MODE.OFFLINE, area = MACHINE_AREA.CLARA_PH1):
                 #controller_func = None, name_func = None
        self._my_name = hardware_base._my_name
        self._mode = None
        self._area = None
        self._controller = None
        self._names = None
        self._iteration = None
        self._procedure_good = False

        self.is_working = False

        self._start_time = None
        self._has_controller = None
        self._has_names = None
        self._time_limit = None
        #
        self.names_good = False
        self.values_good = False

        self.mode = mode
        self.area = area


    def get_controller_mode_and_area(self,controller_func):
        try:
            self.controller = controller_func(self.mode, self.area)
            self.has_controller = True
        except:
            print('error in creating controller')
            self.has_controller = False

    def get_controller_func(self,controller_func):
        try:
            self.controller = controller_func()
            self.has_controller = True
        except:
            print('error in creating controller')
            self.has_controller = False

    def parse_procedure(self, procedure):
        'assumes standard dict passed in'
        'these values are then used in individual hardware functions'
        self.proc_names = []
        #self.proc_states = []
        self.proc_values = []
        for key, value in procedure.iteritems():
            if hardware_base.config.names in value.keys():
                self.proc_names.extend(value[hardware_base.config.names])
            # if hardware_base.config.states in value.keys():
            #     self.proc_values.extend(value[hardware_base.config.states])
            if hardware_base.config.values in value.keys():
                self.proc_values.extend(value[hardware_base.config.values])
        return len(self.proc_names) == len(self.proc_values)

    def get_names(self, name_func):
        if self.has_controller:
            try:
                self.names = name_func()
                # for name in self.names:
                #     print self._my_name  + ' found ' +  name
                self.has_names = True
            except:
                print('error in getting names')
                self.has_names = False

    def test_names_are_good(self):
        self.names_good = set(self.proc_names).issubset(self.names)
        if not self.names_good:
            print(self._my_name + ' procedure names are bad')

    # def test_states_are_good(self, type):
    #     self.states_good = all(isinstance(x, type) for x in self.proc_states)
    #     if not self.states_good:
    #         print(self._my_name + ' procedure states are bad')

    def test_values_are_good(self, type):
        self.values_good = all(isinstance(x, type) for x in self.proc_values)
        if not self.values_good:
            print(self._my_name + ' procedure values are bad')

    def get_it_names_values(self,dict):
        self.is_working = True
        return zip(dict[self.config.names],dict[self.config.values])


    @property
    def procedure_good(self):
        return self._procedure_good

    @procedure_good.setter
    def procedure_good(self,v):
        self._procedure_good = v

    @property
    def has_names(self):
        return self._has_names

    @has_names.setter
    def has_names(self,v):
        self._has_names = v

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self,v):
        self._controller = v

    @property
    def time_limit(self):
        return self._time_limit

    @time_limit.setter
    def time_limit(self,v):
        self._time_limit = v

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self,v):
        self._mode = v

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self,v):
        self._area = v

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self,v):
        self._start_time = time.time()

    # @property
    # def is_working(self):
    #     return self._is_working
    #
    # @is_working.setter
    # def is_working(self ,v):
    #     self._is_working = v

    @property
    def has_controller(self):
        return self._has_controller

    @has_controller.setter
    def has_controller(self ,v):
        self._has_controller = v

    @property
    def iteration(self):
        return self._iteration

    @iteration.setter
    def iteration(self ,v):
        self._iteration = v

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self ,v):
        self._names = v

    @property
    def elapsed_time(self):
        return time.time() - self._start_time

    @property
    def has_timed_out(self):
        return self.time_limit > self.elapsed_time

    def start_work(self):
        self.start_time = 1
        self.is_working = True