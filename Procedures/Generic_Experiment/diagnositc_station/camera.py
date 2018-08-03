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
import VELA_CLARA_Camera_Control as cam
import time

class camera(hardware_base):
    _my_name = 'camera'
    init = None
    #controller = None

    def __init__(self, mode=MACHINE_MODE.PHYSICAL, area=MACHINE_AREA.CLARA_PH1):
        hardware_base.__init__(self, mode=mode, area=area)
        self._my_name = camera._my_name
        self.init_camera()
        self.get_controller_func(self.init.physical_Camera_Controller)
        self.get_names(self.controller.getCameraNames)
        print(camera._my_name + ' has controller, testing procedure')
        self.test_procedure()
        if self.procedure_good:
            print(camera._my_name + ' Procedure Good')
        else:
            print(magnet._my_name + ' Procedure Bad')
        # self.get_controller(camera.init.physical_CLARA_Camera_DAQ_Controller)
        # self.get_names(self.controller.getCameraNames)
        # print(camera._my_name + ' has controller')

    def init_camera(self):
        camera.init = cam.init()
        camera.init.setQuiet()

    def test_procedure(self):
        'assumes [names,state] for each iteration'
        if self.parse_procedure(self.config.camera_data):
            self.test_names_are_good()
            self.test_values_are_good(type(1))
        self.procedure_good = self.names_good & self.values_good

    '''apply the next iteration'''
    def next_step(self, num):
        self.iteration = self.get_it_names_values(self.config.camera_data[num])
        print self.iteration
        for it in self.iteration:
            self.activate(name=it[0],value=it[1])

        print(camera._my_name + ' iteration applied')

    def activate(self,name,value):
        if name == 'VC':
            self.controller.startVCAcquiring()
            while self.controller.isNotAcquiring(name):
                time.sleep(0.1)
                print(name + ' Is not acquiring')
            self.controller.collectAndSaveVC(value)
        else:
            n = self.controller.selectedCamera()
            print('Active camera = ' + n)
            self.controller.stopAcquiring()
            self.controller.setCamera(name)
            self.controller.startAcquiring()
            while self.controller.isNotAcquiring(name):
                time.sleep(0.1)
                print(name + ' Is not acquiring')
            self.controller.collectAndSave(value)

    def is_busy(self):
        if self.is_working:
            self.is_working = self.controller.isCollectingOrSaving(self.iteration[0][0])
        if self.is_working:
            print(self.iteration[0][0] + ' isCollectingOrSaving')
        else:
            print(self.iteration[0][0] + ' has finished isCollectingOrSaving')
        return self.is_working


#
#
# # init
# h = daq.init()
# cameras = h.physical_CLARA_Camera_DAQ_Controller()
#
# # input data
# num_images = 100
# my_cam = 'VC'
#
# # set camera and start acquiring
# cameras.setCamera(my_cam)
# cameras.startAcquiring()
# time.sleep(1.5)
# if cameras.isAcquiring(my_cam):
# 	print my_cam + ' is acquiring!'
# else:
# 	print my_cam + ' is NOT acquiring!'
#
# # try collecting and saving ...
# print 'press key to collectAndSave ... '
# raw_input()
#
# cameras.collectAndSave(num_images)
# # while loop that waits until collecting and saving has finished
# print 'entering while loop'
# while cameras.isCollectingOrSaving(my_cam):
# 	print my_cam + ' isCollectingOrSaving'
# 	time.sleep(1)
#
# # get directory adn filename for last saved data
# print 'press key to get directory and filename'
# raw_input()
# print my_cam + ' has acquired ' + str(num_images) + ' images'
# print my_cam + ', data saved to directory  = ' + cameras.getLatestDirectory(my_cam)
# print my_cam + ', data saved to Filename   = ' + cameras.getLatestFilename(my_cam)
#
# print('press key to end')
# raw_input()
#
#
# # IF MY CAM iS VC then you can use:
# #isCollectingOrSavingVC()
# #getLatestDirectoryVC()
# #getLatestFilenameVC()
# # IF you just want data from the selected cam (not VC) you can use :
# #isCollectingOrSaving()
# #getLatestDirectory()
# #getLatestFilename()
#
#











#
#
#
#
# from hardware_base import MACHINE_AREA
# from hardware_base import MACHINE_MODE
# import VELA_CLARA_Magnet_Control as mag
# import time
#
#
# class magnet(hardware_base):
#     _my_name = 'magnet_setter'
#     init = mag.init()
#     init.setQuiet()
#     # init.setVerbose()
#     # controller = None
#     names = None
#     iteration = None
#
#     def __init__(self, mode=MACHINE_MODE.PHYSICAL, area=MACHINE_AREA.CLARA_PH1):
#         hardware_base.__init__(self, mode=mode, area=area)
#         self.get_controller(magnet.init.getMagnetController)
#         self.get_names(self.controller.getMagnetNames)
#         print(magnet._my_name + ' has controller')
#
#     def test_procedure(self, procedure):
#         'assumes [names,state] for each iteration'
#         names = []
#         values = []
#         for it in procedure:
#             t = map(list, zip(*it))
#             names.extend(t[0])
#             values.extend(t[1])
#
#             need
#             to
#             add in degaussing
#         names_good = set(names).issubset(self.names)
#         if not names_good:
#             print('Names bad')
#         states_good = all(isinstance(x, float) for x in values)
#         if not states_good:
#             print('states bad')
#         return names_good & states_good
#
#     def next_step(self, iteration):
#         self.iteration = iteration
#         for it in iteration:
#             self.moveScreen(name=it[0], state=it[1])
#
#     def moveScreen(self, name, state):
#         if state == scr.SCREEN_STATE.SCREEN_IN:
#             print('moving in  ' + name)
#             self.controller.insertYAG(name)
#         if state == scr.SCREEN_STATE.SCREEN_OUT:
#             print('moving out ' + name)
#             self.controller.moveScreenOut(name)
#             print 22
#
#     def is_in_state(self, name, state):
#         if state == scr.SCREEN_STATE.SCREEN_IN:
#             return self.controller.isScreenIN(name)
#         if state == scr.SCREEN_STATE.SCREEN_OUT:
#             return self.controller.is_HandV_OUT(name)
#
#     def is_busy(self):
#         if self.is_working:
#             self.is_working = not all(self.is_in_state(x[0], x[1]) for x in self.iteration)
#         return self.is_working
#
