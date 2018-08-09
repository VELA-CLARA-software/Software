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
//  Last edit:   05-06-2018
//  FileName:    procedure.oy
//  Description: Generic template for procedure class for High Level Application
//
//
//*/
'''
import VELA_CLARA_Camera_Control as cam


class procedure(object):
    # initDAQ = daq.init()
    camInit = cam.init()
    camInit.setVerbose()
    camInit.setQuiet()

    cc = camInit.physical_Camera_Controller()

    # get names
    cam_names = cc.getCameraScreenNames()

    # get valve-obj references
    cam_state_refs = {}
    for name in cam_names:
        print('Adding ', name)
        cam_state_refs[name] = cc.getStateObj(name)

    # this list will be used by the view to update states
    states = {}

    def __init__(self):
        self.my_name = 'procedure'

    # called external to update states
    def update_states(self):
        for name in procedure.cam_names:
            procedure.states[name] = procedure.cam_state_refs[name].acquire
            #print name + ' state = ' + str(procedure.states[name])

    # called external, toggle open or close
    def start_stop(self,name):
        if procedure.states[name] == cam.ACQUIRE_STATE.ACQUIRING:
            self.stop(name)
        elif procedure.states[name] == cam.ACQUIRE_STATE.NOT_ACQUIRING:
            self.start(name)

    # called external, open name
    def stop(self,name):
        procedure.cc.stopAcquiring(name)

    # called external, close name
    def start(self, name):
        procedure.cc.startAcquiring(name)

    # called external, close all valves
    def stop_all(self):
        for name in procedure.cam_names:
            self.stop(name)