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
from hardware_base import MACHINE_AREA
from hardware_base import MACHINE_MODE
import VELA_CLARA_Magnet_Control as mag
import time

class magnet(hardware_base):
    _my_name = 'magnet_setter'
    init = None
    #controller = None

    def __init__(self,mode=MACHINE_MODE.PHYSICAL,area=MACHINE_AREA.CLARA_PH1):
        hardware_base.__init__(self,mode=mode,area=area)
        self._my_name = magnet._my_name
        self.init_magnet()
        self.get_controller_mode_and_area(self.init.getMagnetController)
        self.get_names(self.controller.getMagnetNames)
        print(magnet._my_name + ' has controller, testing procedure')
        self.test_procedure()
        if self.procedure_good:
            print(magnet._my_name + ' Procedure Good')
        else:
            print(magnet._my_name + ' Procedure Bad')
        # self.get_controller(magnet.init.getMagnetController)
        # self.get_names(self.controller.getMagnetNames)
        # print(magnet._my_name + ' has controller')

    def init_magnet(self):
        magnet.init = mag.init()
        magnet.init.setQuiet()
        # magnet.init.setVerbose()

    def test_procedure(self):
        'assumes [names,state] for each iteration'
        if self.parse_procedure(self.config.magnet_data):
            self.test_names_are_good()
            self.test_mag_values_are_good()
        self.procedure_good = self.names_good & self.values_good

    def test_mag_values_are_good(self):
        '''magnets have their own check for values to allow for degauss'''
        self.values_good = True
        for v in self.proc_values:
            if isinstance(v, float):
                pass
            elif v == 'DEGAUSS':
                pass
            else:
                self.values_good = False
                print('Values Bad')
                break

    '''apply the next iteration'''

    def next_step(self, num):
        self.iteration = self.get_it_names_values(self.config.magnet_data[num])
        print self.iteration
        for it in self.iteration:
            self.apply_value(name=it[0], value=it[1])
        print(magnet._my_name + ' iteration applied')

    def apply_value(self, name, value):
        if value == 'DEGAUSS_TO_ZERO':
            self.controller.degauss(name,True)
        if value == 'DEGAUSS':
            self.controller.degauss(name,False)
        elif isinstance(value,float):
            self.controller.switchONpsu(name)
            self.controller.setSI(name,value)
    '''if is_busy then self.iteration has not complete'''

    def is_busy(self):
        if self.is_working:
            '''beware the negatives'''
            self.is_working = not all(self.has_complete(x[0], x[1]) for x in self.iteration)
        return self.is_working

    def has_complete(self, name, value):
        if value == 'DEGAUSS_TO_ZERO':
            if self.controller.isNotDegaussing(name):
                print(name + ' magnet is isNotDegaussing')
                return True
            else:
                print(name + ' magnet is not isNotDegaussing')
                return False
        if value == 'DEGAUSS':
            if self.controller.isNotDegaussing(name):
                if self.controller.isNotDegaussing(name):
                    print(name + ' magnet is isNotDegaussing')
                    return True
                else:
                    print(name + ' magnet is not isNotDegaussing')
                    return False
        elif isinstance(value,float):
            if self.controller.isRIequalSI(name):
                print(name + ' magnet is isRIequalSI')
                return True
            else:
                print(name + ' magnet is not isRIequalSI')
                return False
        else:
            print('MAJOR ERROR')
