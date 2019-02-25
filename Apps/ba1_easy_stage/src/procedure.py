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
//  Last edit:   11-01-2019
//  FileName:    procedure.py
//  Description: template for class for gui class in generic High Level Application
//
//
//*/
'''
# Add the release folder to the path to get latest HWC
import sys
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
import VELA_CLARA_BA1_Stages_Control as stage
from src.data import data


class procedure(object):
    # INITIALIZATION
    init = stage.init()
    init.setVerbose()  # comment out if too much noise
    stage_control = init.physical_BA1_Stages_Controller()

    def __init__(self):
        # super(base, self).__init__()
        object.__init__(self)
        self.my_name = "procedure"
        self.data = data()
        self.values = self.data.values
        self.initilaise()


    def initilaise(self):
        self.values[self.data.stage_names] = procedure.stage_control.getStageNames()
        for stage in self.values[data.stage_names]:
            self.values[data.stage_devices][stage] = procedure.stage_control.getDevices(stage)
            print('dev = ', self.values[data.stage_devices][stage])

    def update_values(self):
        for stage in self.values[data.stage_names]:
            self.values[data.stage_positions][stage]=procedure.stage_control.getStagePosition(stage)
            self.values[data.stage_set_positions][stage]=procedure.stage_control.getStageSetPosition(stage)
            self.values[data.stage_read_equal_set]=procedure.stage_control.isReadPosEqualSetPos(
                    stage, 0.001)

    def move(self,stage, value):
        procedure.stage_control.setStagePosition(stage, value)

    def move_device(self,stage, device):
        procedure.stage_control.setDevice(stage, device)

    def hello(self):
        print(self.my_name+ ' says hello')