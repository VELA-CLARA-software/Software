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
//  Last edit:   03-07-2019
//  FileName:    main_controller.py
//  Description: The main_controller, holds all objects adn passes data/messsages betwen them
//
//
//
//
//*/
'''
#from PyQt4.QtGui import QApplication
#from PyQt4.QtCore import QTimer
#from controller_base import controller_base
#from src.gui.gui_conditioning import gui_conditioning
#import src.data.rf_condition_data_base as dat
#from src.data.state import state
import sys
import time
import os

print('main_controller: import hardware_control_hub')
from src.controllers.hardware_control_hub import hardware_control_hub
print('main_controller: import config')
from src.data.config import config
print('main_controller: import rf_conditioning_logger')
from src.data.rf_conditioning_logger import rf_conditioning_logger
print('main_controller: import rf_conditioning_data')
from src.data.rf_conditioning_data import rf_conditioning_data
print('main_controller: import monitor_hub')
from src.monitors.monitor_hub import monitor_hub
from src.view.rf_condition_view import rf_condition_view

import random

from PyQt4.QtGui import QApplication

from src.data.state import *
from src.data.state import ramp_method

#class main_controller(controller_base):
class main_controller(object):


    #
    # other attributes will be initialised in base-class
    #
    # We are going to have multiple debug modes so that you can set it from the command line,
    # hardcoded in to the source code, etc, PLUS in the config file
    def __init__(self, argv, config_file, debug=True, debug2=True):
        print(__name__, " init ")
        self.debug = True
        if debug == False:
            if debug2 == False:
                self.debug = False

        # args passed in from command line
        self.argv = argv

        # pop the view so we can display startup messages
        #
        self.view = rf_condition_view()
        self.view.show()


        QApplication.processEvents()
        #
        # Create config reader, and get configuration
        print(__name__ + ', attempting to read config: ' + config_file)
        self.config = config()
        self.get_config(config_file)
        print(__name__ + ', got Config, starting Logging\n')

        # Set the config for the GUI
        self.view.config = self.config
        self.view.start_gui_update()

        #
        # start logging, sets up main text file logging, and logs the config
        self.logger = rf_conditioning_logger(debug=self.debug, column_width=80)
        self.logger.setup_text_log_files()
        self.logger.log_config()

        #
        # create a data object
        self.logger.message_header(__name__ + ', create rf_conditioning_data object',
                                   add_to_text_log=True, show_time_stamp=True)
        self.data = rf_conditioning_data(debug=self.debug)

        self.logger.excluded_key_list = self.data.excluded_key_list
        print("self.data.excluded_key_list = {}".format( self.data.excluded_key_list))
        print(" self.logger.excluded_key_list = {}".format(  self.logger.excluded_key_list))

        #raw_input()

        self.data.initialise()
        self.values = self.data.values


        # should thios happen here, or in the view?
        self.view.data = self.data
        self.view.values = self.data.values
        self.view.start_gui_update()
        #
        # CATAP hardware controllers, these live here and are passed to where they are needed
        # self.hardware.start_up() actually creates the objects, this should only be done once,
        # here! so that we don't create multiple controllers
        self.logger.message_header(__name__ + ', create hardware_control_hub object',
                                   add_to_text_log=True,show_time_stamp=True)
        self.hardware = hardware_control_hub()
        self.hardware.start_up()

        # set the activ epulse count in teh c++ to the value in the pulse_breakdown_log
        self.hardware.llrf_control.setActivePulseCount(self.values[rf_conditioning_data.log_pulse_count])
        self.hardware.llrf_controller.set_trace_mean_positions()
        # SET TRACE SCAN Paramaters
        self.hardware.llrf_controller.set_trace_SCAN()
        #
        # CATAP hardware controllers, these live here and are passed to where they are needed
        self.logger.message_header(__name__ + ', create monitor_hub object',
                                   add_to_text_log=True,show_time_stamp=True)
        self.monitor_hub = monitor_hub()
        self.monitor_hub.start_monitors()
        # the vac monitor, DB monitor etc,keep a local state, at the mina_loop level we derive a state from them (
        # e.g. new_good, new_bad, etc
        self.conditioning_states = {}
        self.conditioning_states[self.data.vac_spike_status] = state.UNKNOWN
        self.conditioning_states[self.data.breakdown_status] = state.UNKNOWN

        # connect buttons
        self.view.update_expert_values_button.clicked.connect(self.update_expert_values) # MUST
        # BE CONNECTED AFTER MONITOR_HUB is created
        #
        # Start Data Logging
        self.logger.start_binary_data_logging(self.data.values)
        self.main_loop()

    def main_loop(self):
        self.values[rf_conditioning_data.required_pulses] = self.config.raw_config_data['DEFAULT_PULSE_COUNT']

        # for testing, enable ramping
        self.view.handle_can_ramp_button()
        # set the active pulse count to the value read in from the pulse-breakdown log file
        # set event_pulse_count_zero to be the active pulse count, then set the active pulse count to zero
        #print("Set Pulse counts in main loop")
        # self.values[rf_conditioning_data.event_pulse_count_zero] = self.values[rf_conditioning_data.log_pulse_count]
        # self.values[rf_conditioning_data.event_pulse_count] = 0
        # reset the event pulse count to zero (this function should achieve the same as the above lines ... )
        self.data.reset_event_pulse_count()

        self.logger.message_header(
            __name__ + ' The RF Conditioning is Preparing to Entering Main_Loop !',
            add_to_text_log=True, show_time_stamp=True)

        self.hardware.llrf_control.keepKlyFwdPwrRS()
        self.hardware.llrf_controller.enable_trigger()

        #  enable the RF
        self.hardware.llrf_controller.enable_llrf()
        # TODO amp_sp on startup needs to be this value, i'm not sure exactly where value is set ??
        # rcd.log_amp_set
        # continue on the last but entry from the pusle_breakdown_log
        # pulse_breakdown has chosen start values, so continue, see get_pulse_count_breakdown_log()
        #

        # TODO This needs to be the RELATIVELY-FAST-RAMP FUNCTiION
        # print("START-UP first active amp_sp = {}".format(self.values[rf_conditioning_data.log_amp_set]))
        # self.hardware.llrf_controller.set_amp( self.values[rf_conditioning_data.log_amp_set] )

        while 1:
            QApplication.processEvents()

            self.update_main_states()


            if is_bad_or_new_bad(self.data.values[rf_conditioning_data.can_rf_output_state]):
                print("State is bad")

            elif self.data.values[rf_conditioning_data.can_rf_output_state] == state.NEW_GOOD:

                print("State is new_good, settign LOG_RAMP adn resstign pulse counters ")
                self.values[rf_conditioning_data.ramp_mode] = ramp_method.LOG_RAMP
                self.values[rf_conditioning_data.event_pulse_count] = 1
                self.values[rf_conditioning_data.required_pulses] = 0



            elif is_good(self.data.values[rf_conditioning_data.can_rf_output_state]):

                if self.reached_min_pulse_count_for_this_step():
                    print("reached_min_pulse_count_for_this_step")

                    if self.values[rf_conditioning_data.ramp_mode] == ramp_method.LOG_RAMP:

                        # we always ramp in LOG_RAMP mode
                        self.log_ramp_up()

                    elif self.values[rf_conditioning_data.main_can_ramp]:

                        estimated_ramp_index = self.data.get_ramp_index_from_power(self.data.get_kf_running_stat_power_at_current_set_point())
                        print("power = {}, estimated_ramp_index = {}".format(self.data.get_kf_running_stat_power_at_current_set_point(), estimated_ramp_index))
                        self.ramp_up()
                                # print("Calling ramp / random up or down")
                                #  if random.randint(0,1) > 0.5:
                                #     print("ml ramp_up")
                                #     self.ramp_up()  # TODO better name??, ramp_up from a normal stae
                                # else:
                                #     print("ml ramp_down")
                                #     self.ramp_down()
                else:
                    # continue (do some logging)
                    self.monitor_hub.llrf_monitor.update_amp_vs_kfpow_running_stat()

    def update_main_states(self):
        '''
            There are two sets of states to check, those related to if we can produce RF POWER and those related to
            state of the conditonning (vac level, breakdown count etc ... )
        '''
        self.check_LLRF_state()
        self.check_conditioning_state()
        self.check_ramping_status()


    def check_ramping_status(self):
        '''
            ATM there are 3 state that can disable ramping, the gui, the BD_rate, and vac level
            TODO there should also be cavity_ratio
        '''
        if self.values[rf_conditioning_data.gui_can_ramp]:
            if self.values[rf_conditioning_data.breakdown_rate_low]:
                if self.values[rf_conditioning_data.gui_can_ramp]:
                    self.values[rf_conditioning_data.main_can_ramp] = True
                else:
                    self.values[rf_conditioning_data.main_can_ramp] = False
            else:
                self.values[rf_conditioning_data.main_can_ramp] = False
        else:
            self.values[rf_conditioning_data.main_can_ramp] = False


    def check_conditioning_state(self):
        '''
            the main_loop needs ot know if we are in "good, new_good, bad or new_bad"
        :return:
        '''
        rcd = rf_conditioning_data

        # update 'last' values
        self.values[rcd.last_breakdown_status] = self.conditioning_states[rcd.breakdown_status]
        self.values[rcd.last_vac_spike_status] = self.conditioning_states[rcd.vac_spike_status]
        # get new values (and set to new_good / new_bad if approprioate
        self.conditioning_states[rcd.breakdown_status] = compare_states(self.values[rcd.breakdown_status],
                                                                              self.values[rcd.last_breakdown_status])
        self.conditioning_states[rcd.vac_spike_status] = compare_states(self.values[rcd.vac_spike_status],
                                                                              self.values[rcd.last_vac_spike_status])

    def check_LLRF_state(self):
        '''
            checks everything to enable RF power
        '''
        rcd = rf_conditioning_data
        #
        # set the old value to the current value
        self.data.values[rcd.can_rf_output_state_OLD] = self.data.values[rcd.can_rf_output_state]

        # check the state of teh RF protection and modulator, if they are bad we have decided NO-ARC does not intervene
        mod_and_prot_good = False
        if self.data.values[self.data.modulator_good]:
            if self.data.values[self.data.rfprot_good]:
                mod_and_prot_good = True

        if mod_and_prot_good:

            daq_freq_good = True
            if self.values[self.data.llrf_DAQ_rep_rate_status] == state.BAD:
                daq_freq_good = False
            #
            # Go through each LLRF setting  that effect if there is RF power (feel free to add more)

            if daq_freq_good:
                all_good = True
                if self.data.values[rcd.llrf_interlock_status] != state.GOOD:
                    print("llrf_interlock_status is not good")
                    all_good = False
                elif self.data.values[rcd.llrf_trigger_status] != state.GOOD:
                    print("llrf_trigger_status is not good")
                    all_good = False
                elif self.data.values[rcd.pulse_length_status] != state.GOOD:
                    print("pulse_length_status is not good")
                    all_good = False
                elif self.data.values[rcd.llrf_output_status] != state.GOOD:
                    print("llrf_output_status is not good")
                    all_good = False
                elif self.data.values[rcd.llrf_ff_amp_locked_status] != state.GOOD:
                    print("llrf_ff_amp_locked_status is not good")
                    all_good = False
                elif self.data.values[rcd.llrf_ff_ph_locked_status] != state.GOOD:
                    print("llrf_ff_ph_locked_status is not good")
                    all_good = False

                if all_good:
                    self.data.values[rcd.can_rf_output_state] = state.GOOD
                else:
                    self.data.values[rcd.can_rf_output_state] = state.BAD
                # NOW check to see if this is a new good or a new bad
                if is_new_good(self.data.values[rcd.can_rf_output_state], self.data.values[rcd.can_rf_output_state_OLD] ):
                    self.data.values[rcd.can_rf_output_state] = state.NEW_GOOD

                if is_new_bad(self.data.values[rcd.can_rf_output_state], self.data.values[rcd.can_rf_output_state_OLD] ):
                    self.data.values[rcd.can_rf_output_state] = state.NEW_BAD
                # now we check if the GUI has requested RF off
                if self.values[rf_conditioning_data.gui_can_rf_output]:
                    if is_bad_or_new_bad(self.data.values[rcd.can_rf_output_state]):
                        self.hardware.llrf_controller.enable_llrf()
                else:
                    print("GUI SAYS We should disable RF ")
                    if is_good_or_new_good(self.data.values[rcd.can_rf_output_state]):
                        print("GUI SAYS We should disable RF AND RF IS GOOD disable RF")
                        self.hardware.llrf_controller.disableRFOutput()

    def log_ramp_up(self):
        # # log data at the new setpoint MUST BE BEFORE  move_up_ramp_curve()
        # update pulse breakdown log
        self.data.add_to_pulse_breakdown_log(self.hardware.llrf_obj[0].amp_sp)
        self.monitor_hub.llrf_monitor.update_amp_vs_kfpow_running_stat()
        self.data.log_kly_fwd_power_vs_amp()

        # someshort aliases
        lrc = self.data.log_ramp_curve
        lrci = self.values[self.data.log_ramp_curve_index]


        # switch here to set up curve if
        if lrc is None:

            # WE assume the ramp index is set correctly !

            # GET NEW SET_POINT
            # new amp always returns a value!!

            power_finish = self.data.get_log_ramp_power_finsh()

            print("log_curve power finsh = {}".format(power_finish))



            self.data.generate_log_ramp_curve(p_start  = self.config.raw_config_data['LOG_RAMP_START_POWER'],
                                              p_finish =  power_finish ,
                                              ramp_rate =  self.config.raw_config_data['LOG_RAMP_CURVE_RAMP_RATE'],
                                              numsteps =  self.config.raw_config_data['LOG_RAMP_CURVE_NUMSTEPS'],
                                              pulses_per_step =  self.config.raw_config_data['LOG_RAMP_CURVE_PULSES_PER_STEP'])

        # someshort aliases
        lrc = self.data.log_ramp_curve
        lrci = self.values[self.data.log_ramp_curve_index]


        if lrc is None:
            print("ERROR lrc is None")
            raw_input()

        # # set new_amp
        if self.hardware.llrf_controller.set_amp( lrc[ lrci][1], update_last_amp_sp = True):

            if self.values[self.data.log_ramp_curve_index] == len(self.data.log_ramp_curve) -1:
                print("Log Ramp finished, setting log_ramp_curve to None")
                self.data.log_ramp_curve = None
                self.values[self.data.log_ramp_curve_index] = -1
                # reset active pulse counters
                self.data.reset_event_pulse_count()
                self.values[rf_conditioning_data.ramp_mode] = ramp_method.NORMAL_RAMP
            else:
                ''' set the number of pulses '''
                rcd = rf_conditioning_data
                rcd.values[rcd.required_pulses] = self.data.log_ramp_curve[ self.values[self.data.log_ramp_curve_index] ][0]
                rcd.values[rcd.last_power_change] = 0.0
                rcd.values[rcd.next_power_change] = 0.0
                rcd.values[rcd.event_pulse_count_zero] = rcd.values[rcd.pulse_count]
                rcd.values[rcd.event_pulse_count] = 0
                self.logger.message_header(__name__ + ' reset_event_pulse_count')
                self.logger.message('new event_pulse_count_zero = {}'.format(rcd.values[rcd.event_pulse_count_zero]))

            self.values[self.data.log_ramp_curve_index] +=1

        else:
             # we failed to set the requested amplitude .... erm.... not sure what to do ????
             pass




    def ramp_up(self):
        self.logger.message_header(' Ramp Up ')
        setpoint_before_ramp = self.hardware.llrf_obj[0].amp_sp
        if setpoint_before_ramp < 100:
            self.logger.message('!!WARNING!! Current setpoint before Ramp Up = ' + str(
                setpoint_before_ramp) + ' suspect a breakdown has very recently occurred! ')
        #
        # #
        # # log data at the new setpoint MUST BE BEFORE  move_up_ramp_curve()
        # update pulse breakdown log
        self.data.add_to_pulse_breakdown_log(self.hardware.llrf_obj[0].amp_sp)
        self.monitor_hub.llrf_monitor.update_amp_vs_kfpow_running_stat()
        self.data.log_kly_fwd_power_vs_amp()

        # dynamically set ramp index based on measured power at this amp_set_point
        self.data.set_ramp_index_for_current_power()

        # GET NEW SET_POINT
        # new amp always returns a value!!
        # the function to get the next set-point depends on the ramp_method
        new_amp = self.data.get_new_set_point(self.values[rf_conditioning_data.next_power_change])  # value from ramp.py and ramp_index
        # #
        # # set new_amp
        if self.hardware.llrf_controller.set_amp(new_amp, update_last_amp_sp = True):
             pass
        else:
             # we failed to set the requested amplitude .... erm.... not sure what to do ????
             pass
        # #
        # # move up curve (when below ~1MW
        # ''' !!! also calls set_next_sp_decrease !!!'''
        # we ONLY call the below function, if we have actually ramped with enough to data to attmept fitting

        if self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__TOO_FEW_BINS \
            or self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__ENOUGH_BINS__ZERO_IN_LIST__NOT_ENOUGH_NON_ZERO \
            or self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__DELTA_GTRTHN_MAX \
            or self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__NEG_RAMP \
            or self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__FLAT_RAMP:
            pass
        elif self.values[rf_conditioning_data.last_ramp_method] == ramp_method.UNKNOWN:
            print("!!!MAJOR ERROR!!!!\nramp_method = {}".format(self.values[rf_conditioning_data.last_ramp_method]))
        else:
            pass

        # else: # probably should not be this, there are (will be) more possible ramp_method values to consider
        #     self.data.move_up_ramp_curve()


        # #
        # '''Sanity Check '''
        # if setpoint_before_ramp != controller_base.data.values[dat.next_sp_decrease]:
        #     self.logger.message('!!! Warning Unexpected next_sp_decrease ' + str(
        #         setpoint_before_ramp) + ' != ' + str(
        #         controller_base.data.values[dat.next_sp_decrease]), True)
        # #
        # update the plot with new values
        print("Calling update_plot")
        self.view.update_plot()
        QApplication.processEvents()
        #
        # reset active pulse counters
        self.data.reset_event_pulse_count()
        #self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
        #
        self.logger.message('ramp_up FINISHED, we went from ' + str(setpoint_before_ramp) + ' to ' + str(new_amp))




    def ramp_down(self):
        self.logger.message_header('Ramp Down')
        setpoint_before_ramp = self.hardware.llrf_obj[0].amp_sp
        if setpoint_before_ramp < 100:
            self.logger.message(
                '!!WARNING!! Current setpoint before Ramp Down = ' + str(setpoint_before_ramp) + ' suspect a breakdown has very recently occurred! ')
        #
        # #
        # # log data at the new setpoint MUST BE BEFORE  move_up_ramp_curve()
        # update pulse breakdown log
        self.data.add_to_pulse_breakdown_log(self.hardware.llrf_obj[0].amp_sp)
        self.monitor_hub.llrf_monitor.update_amp_vs_kfpow_running_stat()
        self.data.log_kly_fwd_power_vs_amp()
        # dynamically set ramp index based on measured power at this amp_set_point
        self.data.set_ramp_index_for_current_power()

        # GET NEW SET_POINT
        # new amp always returns a value!!
        new_amp = self.data.get_new_set_point(-self.values[rf_conditioning_data.next_power_change]) # value from ramp.py and ramp_index
        # #
        # # set new_amp
        if self.hardware.llrf_controller.set_amp(new_amp, update_last_amp_sp = True):
            pass
        else:
            # we failed to set the requested amplitude .... erm.... not sure what to do ????
            pass
        # update the plot with new values
        self.view.update_plot()
        QApplication.processEvents()
        #
        # reset active pulse counters
        # why does this function  happen in the outside_mask_trace_monitor ??
        self.data.reset_event_pulse_count()
        #self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
        #
        self.logger.message('ramp_down FINISHED, we went from ' + str(setpoint_before_ramp) + ' to ' + str(new_amp))


    def reached_min_pulse_count_for_this_step(self):
        #print("reached_min_pulse_count_for_this_step, {}, {}".format(self.values[rf_conditioning_data.event_pulse_count],
        # self.values[rf_conditioning_data.required_pulses] ))
        return self.values[rf_conditioning_data.event_pulse_count] >= self.values[rf_conditioning_data.required_pulses]

    def toggle_RF_output(self):
        ''' this function should be connected to the GUI enable / diasable LLRF, but MUST be run
        AFTER rf_conditioning_data.gui_can_rf_output is changed to the requested value '''
        if self.values[rf_conditioning_data.gui_can_rf_output]:
            print("toggle_RF_output(), gui.can_rf_output_state, so calling enable_llrf ")
            self.hardware.llrf_controller.enable_llrf()
        else:
            self.hardware.llrf_controller.disableRFOutput()

    def quit_app(self, message=""):
        print(message)
        quit()


    def get_config(self, config_file):
        self.config.config_file = config_file
        self.config.read_config()

    def update_expert_values(self):
        # get all teh expert values from the various places that want them
        print("self.update_expert_values called")
        self.monitor_hub.llrf_monitor.get_llrf_expert_values()
        # update the gui with the latest values
        self.view.update_expert_values_in_gui()

