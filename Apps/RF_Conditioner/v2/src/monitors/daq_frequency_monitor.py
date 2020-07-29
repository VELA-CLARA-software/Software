#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify  //
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
//  Last edit:   03-07-2018
//  FileName:    monitor_hub.py
//  Description: The llrf_simple_param_monitor, creates and holds all CATAP hardware controllers,
//                they get passed to where they are needed
//
//*/
'''
from monitor import monitor
import src.data.rf_conditioning_data as rf_conditioning_data
from src.data.state import state
from VELA_CLARA_LLRF_Control import TRIG
from VELA_CLARA_LLRF_Control import INTERLOCK_STATE
from matplotlib import pyplot as plt
import time


class daq_frequency_monitor(monitor):
    """
    This class handles monitoring of the 'simple' llrf parameters, its gets values for states,
    and means, set-points etc. that are kept in the data.values dictionary.
    It is a passive class and does not control anything (control is in the llrf_handler)
    """


    def __init__(self):
        monitor.__init__(self)
        self.set_success = False
        # aliases
        self.llrf_control = self.hardware.llrf_control
        self.llrf_obj = self.hardware.llrf_obj

        self.timer.timeout.connect(self.update_daq_rep_rate)
        self.timer.start( self.config_data[self.config.LLRF_CHECK_TIME])
        self.should_show_reset_daq_freg = True
        self.set_iointr_counter = 0
        self.set_success = True


    def update_daq_rep_rate(self):
        ''' DATA ACQUISIATION REP RATE
        The llrf controller estimates the daq frequency from the timestamps of the trace data
        previous observed behaviour has shown this rate can change due to:
            something happening in the llrf box,
            something happening on the network,
            something else.
        If the daq_rep_rate deviates from what is expected we want to disable RF power until it
        returns. We also keep a memory of the previous state, and compare. If previous state was
        BAD and now state is GOOD we call this NEW_GOOD, similarly GOOD to BAD is a NEW_BAD
        we use a NEW_GOOD to enable us to respond to changes in daq_rep_rate
        '''
        DAQ_rep_rate = self.data.llrf_DAQ_rep_rate
        DAQ_rep_rate_status = self.data.llrf_DAQ_rep_rate_status
        self.values[DAQ_rep_rate] = self.llrf_obj[0].trace_rep_rate
        if self.values[DAQ_rep_rate] < self.values[self.data.llrf_DAQ_rep_rate_min]:
            self.values[DAQ_rep_rate_status] = state.BAD

        elif self.values[DAQ_rep_rate] > self.values[self.data.llrf_DAQ_rep_rate_max]:
            self.values[DAQ_rep_rate_status] = state.BAD
        else:
            self.values[self.data.llrf_DAQ_rep_rate_status] = state.GOOD
        if self.values[self.data.llrf_DAQ_rep_rate_status_previous] == state.BAD:
            if self.values[DAQ_rep_rate_status] == state.GOOD:
                self.values[DAQ_rep_rate_status] = state.NEW_GOOD
        self.values[self.data.llrf_DAQ_rep_rate_status_previous] = self.values[DAQ_rep_rate_status]

        if self.values[self.data.llrf_DAQ_rep_rate_status] == state.BAD:
            self.reset_daq_freg()


    def reset_daq_freg(self):
        if self.data.values[self.data.llrf_DAQ_rep_rate_status]  == state.BAD:
            if self.should_show_reset_daq_freg:
                self.logger.message('reset_daq_freg, llrf_DAQ_rep_rate_status == BAD')
                self.should_show_reset_daq_freg = False
            # for a
            if self.llrf_control.llrfObj[0].amp_sp != 0:
                self.logger.message('reset_daq_freg forcing set_amp(0)')
                self.set_amp(0)
            self.set_iointr_counter += 1
            #print('reset_daq_freg = ', self.set_iointr_counter)
            if self.set_iointr_counter == 100000: # MAGIC_NUMBER
                self.logger.message('reset_daq_freg, set_iointr_counter = 100000')

                self.llrf_control.resetTORSCANToIOIntr()
                time.sleep(0.02) # TODO meh ...
                self.llrf_control.setTORACQMEvent()
                self.set_iointr_counter = 0
        else:
            if self.should_show_reset_daq_freg == False:
                self.logger.message('reset_daq_freg, llrf_DAQ_rep_rate_status != BAD')
                self.should_show_reset_daq_freg = True