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
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
import VELA_CLARA_BA1_Stages_Control as stage
from src.data import data


class procedure(object):
    # INITIALIZATION

    def __init__(self):
        # super(base, self).__init__()
        object.__init__(self)
        self.data = data()
        self.values = self.data.values
        self.stage_number_to_name = self.data.stage_number_to_name

        self.init = stage.init()
        self.init.setVerbose()  # comment out if too much noise
        self.stage_control = self.init.physical_BA1_Stages_Controller()

        self.initilaise()

    def initilaise(self):
        """
        Get the values that do not dynamically change
        :return:
        """
        # self.values[stage_active] =1
        # self.values[self.data.stage_names] = procedure.stage_control.getStageNames()
        for stage in self.stage_control.getStageNames():
            self.values[self.data.stage_names][stage] = stage
            self.values[data.stage_devices][stage] = self.stage_control.getDevices(stage)
            self.values[data.stage_numbers][stage] = self.stage_control.getStageNumber(stage)
            self.values[data.active_stage_numbers].append(self.values[data.stage_numbers][stage])
            self.values[data.min_pos][stage] = self.stage_control.getMinPos(stage)
            self.values[data.max_pos][stage] = self.stage_control.getMaxPos(stage)
            # This dictionary is used to go from stage numbers to stage names
            self.stage_number_to_name[self.values[data.stage_numbers][stage]] = stage
            self.values[data.read_pos][stage] = self.stage_control.getStagePosition(stage)
            self.values[data.old_read_pos][stage] = self.stage_control.getStagePosition(stage)
            self.values[data.set_pos][stage] = self.stage_control.getStagePosition(stage)
            self.values[data.precision][stage] = self.stage_control.getStagePrecision(stage)
            self.values[data.clear_for_beam_value][stage] = self.stage_control.getDevicePos(stage, data.CLEAR_FOR_BEAM)

    def update_values(self):
        """
            update values for set and read
        :return:
        """
        for stage in self.values[data.stage_names]:
            self.values[data.read_pos][stage] = self.stage_control.getStagePosition(stage)
            self.values[data.is_moving][stage] = self.values[data.read_pos][stage] != self.values[data.old_read_pos][
                stage]
            self.values[data.is_clear_for_beam][stage] =  self.values[data.read_pos][stage] == self.values[data.clear_for_beam_value][
                stage]
            self.values[data.set_pos][stage] = self.stage_control.getStageSetPosition(stage)
        # we make a copy of old values here, this could be done in a different place, but you will need to change the
        # logic where the is_moving flag is set
        self.values[data.old_read_pos] = self.values[data.read_pos].copy()

    def move(self,stage, value):
        self.stage_control.setStagePosition(stage, value)

    def move_device(self,stage, device):
        self.stage_control.setDevice(stage, device)

    def set_clear_for_beam(self):
        for stage in self.values[data.stage_names]:
            self.move_device(stage, data.CLEAR_FOR_BEAM)

