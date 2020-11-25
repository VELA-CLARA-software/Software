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
//  Last edit:   04-08-2020
//  FileName:    main_controller.py
//  Description: The main_controller, holds all objects and passes data/messsages between them
//               runes main_loop, which gets and checks all relevant states, and  decides how to ramp
//
//
//
//*/
'''
from src.data.ramp import ramp
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
from PyQt4.QtGui import QApplication
from src.data.state import *
from src.data.state import ramp_method
import inspect

class main_controller(object):

    # We are going to have multiple debug modes so that you can set it from the command line,
    # hardcoded in to the source code, etc, PLUS in the config file
    def __init__(self, argv, config_file, debug=True, debug2=True):
        print(__name__, " init ")
        print(debug, debug2)
        print(debug, debug2)
        print(debug, debug2)
        self.debug = True
        if debug == False:
            if debug2 == False:
                self.debug = False
        if self.debug:
            print("main_controller is in debug mode")
        else:
            print("main_controller is NOT in debug mode")
        # args passed in from command line
        self.argv = argv

        ''' The order of calls in  this __init__ is important, if you change the order that classes get instantiated things may break   '''

        ''' Create the main view GUI class  '''
        self.view = rf_condition_view()
        # pop the view so we can display startup messages, adn process some QT events
        self.view.show()
        QApplication.processEvents()

        ''' Create config reader, and get configuration '''
        print(__name__ + ', attempting to read config: ' + config_file)
        self.config = config()
        self.get_config(config_file)
        print(__name__ + ', got Config, starting Logging\n')

        ''' Each main class gets a references to  config so they can access the config dats   
            As we create the gui first we set the config in here         '''
        self.view.config = self.config  # Set the config for the GUI
        self.view.start_gui_update()

        ''' start logging, sets up main text file logging, and logs the config '''
        self.logger = rf_conditioning_logger(debug=self.debug, column_width=80)
        self.logger.setup_text_log_files()
        self.logger.log_config()

        # create a data object
        self.logger.message_header(__name__ + ', create rf_conditioning_data object',
                                   add_to_text_log=True, show_time_stamp=True)
        if self.debug:
            self.logger.message("Started in debug mode = True ")
        else:
            self.logger.message("Started in debug mode = False")

        ''' Create the main data class '''
        self.data = rf_conditioning_data(debug=self.debug)
        self.values = self.data.values

        self.logger.values = self.data.values           # set the logger values dict to data.values
        self.logger.excluded_key_list = self.data.excluded_key_list         # pass the exclued key list for data (hardcoded there) to logger
        # print("self.data.excluded_key_list = {}".format( self.data.excluded_key_list))
        # print(" self.logger.excluded_key_list = {}".format( self.logger.excluded_key_list))
        self.data.initialise()

        # set the data in the gui class,   should this happen here, or in the view? its here, because the view is created before data
        self.view.data = self.data
        self.view.values = self.data.values
        self.view.start_gui_update()


        # CATAP hardware controllers, these live here and are passed to where they are needed
        # self.hardware.start_up() actually creates the objects, this should only be done once,
        # here! so that we don't create multiple controllers
        self.logger.message_header(__name__ + ', create hardware_control_hub object',
                                   add_to_text_log=True,show_time_stamp=True)
        self.hardware = hardware_control_hub()
        self.hardware.start_up()

        # this was for debugging error in the values dict
        # print("after hardware_control_hub 1")
        # val_dict_len = len(self.values.keys() )
        # val_key_types = set([ type(x) for x in self.values.keys()])
        # print(val_dict_len, val_key_types)
        # for key, value in self.values.iteritems():
        #     print("key = {}, val = {}".format(key, value))


        # CATAP hardware controllers, these live here and are passed to where they are needed
        self.logger.message_header(__name__ + ', create monitor_hub object',
                                   add_to_text_log=True,show_time_stamp=True)
        self.monitor_hub = monitor_hub()
        self.monitor_hub.start_monitors()
        ''' !!WARNING!! 
            After we start monitoring the main data values dictionary can have entries added that are defined in the config file
            This means the size of this dict can increase !!   
        '''
        # the vac monitor, DB monitor etc,keep a local state, at the mina_loop level we derive a state from them (
        # e.g. new_good, new_bad, etc
        # self.conditioning_states = {}
        # self.conditioning_states[self.data.vac_spike_status] = state.UNKNOWN
        # self.conditioning_states[self.data.breakdown_status] = state.UNKNOWN
        # # TODO: move llrf_DAQ from conditioning states... but where to??
        # self.conditioning_states[self.data.llrf_DAQ_rep_rate_status] = state.UNKNOWN
        # connect buttons
        self.view.update_expert_values_button.clicked.connect(self.update_expert_values)

        # MUST BE CONNECTED AFTER MONITOR_HUB is created
        # Start Data Logging
        self.logger.start_binary_data_logging()
        self.main_loop()

    def main_loop(self):
        rcd = rf_conditioning_data

        self.values[rf_conditioning_data.required_pulses] = self.config.raw_config_data['DEFAULT_PULSE_COUNT']

        # for testing, enable ramping
        #self.view.handle_can_ramp_button()
        # set the active pulse count to the value read in from the pulse-breakdown log file
        # set event_pulse_count_zero to be the active pulse count, then set the active pulse count to zero

        #print("Set Pulse counts in main loop")

        # self.values[rf_conditioning_data.event_pulse_count_zero] = self.values[rf_conditioning_data.log_pulse_count]
        # self.values[rf_conditioning_data.event_pulse_count] = 0
        # reset the event pulse count to zero (this function should achieve the same as the above lines ... )
        self.data.reset_event_pulse_count()

        self.logger.message_header(__name__ + ' The RF Conditioning is Preparing to Entering Main_Loop !', add_to_text_log=True, show_time_stamp=True)

        self.hardware.llrf_control.keepKlyFwdPwrRS()
        self.hardware.llrf_controller.enable_trigger()
        # turn on llrf c++ messages
        self.hardware.llrf_init.setVerbose()

        #  enable the RF
        #self.hardware.llrf_controller.enable_llrf()
        # TODO amp_sp on startup needs to be this value, i'm not sure exactly where value is set ??
        # rcd.log_amp_set
        # continue on the last but entry from the pusle_breakdown_log
        # pulse_breakdown has chosen start values, so continue, see get_pulse_count_breakdown_log()
        #
        # TODO This needs to be the RELATIVELY-FAST-RAMP FUNCTiION
        # print("START-UP first active amp_sp = {}".format(self.values[rf_conditioning_data.log_amp_set]))
        # self.hardware.llrf_controller.set_amp( self.values[rf_conditioning_data.log_amp_set] )

        # TODO before we start this while loop, we should check all the settings have been set correctly, (depending how paranoid we are)

        while 1:
            QApplication.processEvents()

            self.update_main_states()

            current_state = self.data.values[rcd.can_rf_output_status]



            # disable Global Mask Checking
            if is_bad_or_new_bad(self.data.values[rcd.BD_state]):



                self.hardware.llrf_controller.set_global_check_mask(False)

                # Only clear log ramp curve if new.BAD / log_ramp_curve != None
                if self.data.log_ramp_curve is not None:
                    self.clear_log_ramp_curve()
                else:
                    pass

            if self.data.values[rcd.GUI_mod_and_prot_good] == False: # TODO false == false ! better  bname
                self.hardware.llrf_controller.disableRFOutput()

            elif is_bad_or_new_bad(self.data.values[rcd.can_llrf_output_state]):
                self.hardware.llrf_controller.enable_llrf()
                self.hardware.llrf_controller.set_global_check_mask(False)


                #self.clear_log_ramp_curve()
                # TODO AJG: Double check enable_llrf enables everything needed

            elif current_state == state.NEW_GOOD:
                # the amp_sp should "always be zero (or an amp_drop value) when we get to here
                self.values[rf_conditioning_data.ramp_mode] = ramp_method.LOG_RAMP
                self.values[rf_conditioning_data.event_pulse_count] = 1
                self.values[rf_conditioning_data.required_pulses] = 0
                #self.hardware.llrf_controller.set_infinite_hi_mask() # we set inifntie hi masks, before log_ramping, we call set_nominal_masks
                self.hardware.llrf_control.fastRampModeOn() # in fast ramp mode,  the hi mask is the KFP max for that shot
                # after log_ramping  finished which happens in the log_ramp_up function when we check the log ramp index
                self.hardware.llrf_controller.clear_all_rolling_averages()
                self.hardware.llrf_controller.set_infinite_masks()

                # print('1 KLYSTRON_FORWARD_POWER num ra = {}'.format(self.hardware.llrf_control.getTraceRollingAverageCount(
                #     'KLYSTRON_FORWARD_POWER')))
                # print('1 CAVITY_REVERSE_POWER num ra = {}'.format(self.hardware.llrf_control.getTraceRollingAverageCount(
                #     'CAVITY_REVERSE_POWER')))

                #
                # clear and reset the rolling averages
                # set infinite  hi mask
                # we set this to true!
                self.hardware.llrf_controller.set_global_check_mask(True)


            elif current_state == state.GOOD:
                # TODO update this (maybe we should put this on a timer, and just forget about it?)
                self.monitor_hub.llrf_monitor.update_amp_vs_kfpow_running_stat()
                if self.reached_min_pulse_count_for_this_step():

                    # print('2 KLYSTRON_FORWARD_POWER num ra = {}'.format(self.hardware.llrf_control.getTraceRollingAverageCount(
                    #     'KLYSTRON_FORWARD_POWER')))
                    # print('2 CAVITY_REVERSE_POWER num ra = {}'.format(self.hardware.llrf_control.getTraceRollingAverageCount(
                    #     'CAVITY_REVERSE_POWER')))


                    # follow the ramp curve (either the log_ramp or normal_ramp)
                    if self.data.values[rcd.ramp_mode] == ramp_method.LOG_RAMP:
                        self.log_ramp_up()

                    elif self.data.values[rcd.ramp_mode] == ramp_method.NORMAL_RAMP:
                        if is_good_or_new_good(self.data.values[rcd.can_ramp_status]):
                            estimated_ramp_index = self.data.get_ramp_index_from_power(self.data.get_kf_running_stat_power_at_current_set_point())
                            print("power = {}, estimated_ramp_index = {}".format(self.data.get_kf_running_stat_power_at_current_set_point(), estimated_ramp_index))
                            self.ramp_up()
                        else:
                            pass
                            # TODO setup a a flag here to print message once per change of state (and log it)
                            #print('can_ramp_status = {}'.format(self.data.values[rcd.can_ramp_status]))

                    else:
                        pass
                else:
                    pass
                    #print('reached_min_pulse_count_for_this_step = {}'.format(self.reached_min_pulse_count_for_this_step()))
            else:
                pass

    def update_main_states(self):
            '''
                There are three mid-level states:-
                    1. check_LLRF_state()
                    2. check_BD_state()
                    3. can_ramp_state()

                The two mid-level states 1. check_LLRF_state() & 2. check_BD_state() are combined into a high-level state "can_rf_output_state()"
                This decides whether the RF is turned/kept on.

            '''


            '''
                check the state of LLRF output, (if gui allows and there is a bad state) reset the LLRF states
                sets a high level "LLRF_CAN_OUTPUT" state         
            '''
            self.check_LLRF_state()


            '''
                check the state of BD events 
                sets a high level "BD_STATE"         
            '''

            self.check_BD_state()

            '''
                Check if able to ramp
            '''
            self.can_ramp_state()


            '''
                Highest level state for RF able to output True/False.
                This combines check_LLRF_state() and check_BD_state().
                If both state.GOOD / state.NEW_GOOD then can_rf_output_state() returns state.GOOD / state.NEW_GOOD.
            '''

            self.can_rf_output_state()

    def can_rf_output_state(self):
        '''
            This is the highest level state for can RF output or not.
            It combines "check_BD_state()" and "can_ramp_state()" functions and decides whether the RF is turned/kept on

        '''

        rcd = rf_conditioning_data

        # set the old status to the current status
        self.data.values[rcd.can_rf_output_status_OLD] = self.data.values[rcd.can_rf_output_status]

        #print('\nFrom can_rf_output_state\ncan_rf_output_status_OLD = {}\ncan_rf_output_status = {}'.format(self.data.values[
        #        rcd.can_rf_output_status_OLD], self.data.values[rcd.can_rf_output_status]))

        # set all_BD_good = True and if ANY (doesn't have to be ALL) of the OMED, vac spikes, DC
        # are state.BAD / state.NEW_BAD then all_BD_good gets set to False
        all_rf_outputs = True
        if is_bad_or_new_bad(self.data.values[rcd.can_llrf_output_state]):
            all_rf_outputs = False
            #print('can_llrf_output_state = {}'.format(self.data.values[rcd.can_llrf_output_state]))
        if is_bad_or_new_bad(self.data.values[rcd.BD_state]):
            all_rf_outputs = False
            #print('BD_state = {}'.format(self.data.values[rcd.BD_state]))
        if all_rf_outputs:
            self.data.values[rcd.can_rf_output_status] = state.GOOD
        else:
            self.data.values[rcd.can_rf_output_status] = state.BAD


        # NOW check to see if this is a State.NEW_GOOD or state.NEW_BAD
        if is_new_good(self.data.values[rcd.can_rf_output_status], self.data.values[rcd.can_rf_output_status_OLD]):
            self.data.values[rcd.can_rf_output_status] = state.NEW_GOOD

        if is_new_bad(self.data.values[rcd.can_rf_output_status], self.data.values[rcd.can_rf_output_status_OLD]):
            self.data.values[rcd.can_rf_output_status] = state.NEW_BAD

        #print('After logic tree:\ncan_rf_output_status = {}'.format(self.data.values[rcd.can_rf_output_status]))

    def check_ramping_status(self):
        '''
            ATM there are 4 states that can disable ramping, the gui, the BD_rate, vac level & cavity power ratio (Detuned)
            TODO there should also be cavity_ratio
        '''
        if self.values[rf_conditioning_data.gui_can_ramp]:
            if self.values[rf_conditioning_data.breakdown_rate_low]:
                if self.values[rf_conditioning_data.vac_level_can_ramp]:
                    if self.values[rf_conditioning_data.cav_pwr_ratio_can_ramp]:
                        self.values[rf_conditioning_data.main_can_ramp] = True

                    else:
                        self.values[rf_conditioning_data.main_can_ramp] = False
                else:
                    self.values[rf_conditioning_data.main_can_ramp] = False
            else:
                self.values[rf_conditioning_data.main_can_ramp] = False
        else:
            self.values[rf_conditioning_data.main_can_ramp] = False

    def check_BD_state(self):
        '''
            This checks the states of OMED, vac spikes, DC GOOD/BAD
            and returns a higher level state of GOOD, BAD, NEW_GOOD or NEW_BAD
        '''
        rcd = rf_conditioning_data



        #print('\nFrom check_BD_state\nBD_state_OLD = {}\nBD_state = {}'.format(self.data.values[rcd.BD_state_OLD],  self.data.values[rcd.BD_state]))
        # set the old status to the current status
        self.data.values[rcd.BD_state_OLD] = self.data.values[rcd.BD_state]
        # set all_BD_good = True and if ANY (doesn't have to be ALL) of the OMED, vac spikes, DC
        # are state.BAD / state.NEW_BAD then all_BD_good gets set to False
        # TODO AJG: take DC_state out here and in self.data.values[rcd.DC_state]
        if is_bad_or_new_bad(self.data.values[rcd.breakdown_status]): # breakdown_status bad name ,but OMED
            all_BD_good = False
            #print("breakdown_status is not good")
        #elif is_bad_or_new_bad(self.data.values[rcd.DC_state]):
        #    all_BD_good = False
        elif is_bad_or_new_bad(self.data.values[rcd.vac_spike_status]):
            all_BD_good = False
            #print("vac_spike_status is not good")
        else:
            all_BD_good = True
            #print("breakdown_status & vac_spike_status are good")
        # if set all_BD_good = True then set BD_state to state.GOOD
        # Else set BD_state to state.BAD
        if all_BD_good:
            self.data.values[rcd.BD_state] = state.GOOD
        else:
            self.data.values[rcd.BD_state] = state.BAD

        # NOW check to see if this is a State.NEW_GOOD or state.NEW_BAD
        if is_new_good(self.data.values[rcd.BD_state], self.data.values[rcd.BD_state_OLD]):
            self.data.values[rcd.BD_state] = state.NEW_GOOD

        if is_new_bad(self.data.values[rcd.BD_state], self.data.values[rcd.BD_state_OLD]):
            self.data.values[rcd.BD_state] = state.NEW_BAD


        #print('After logic tree:\nBD_state = {}\n'.format(self.data.values[rcd.BD_state]))

    def can_ramp_state(self):
        '''
            This is a mid-level state that checks the gui_button state, vac level, cavity ratio, BD rate.
            If all components are True the this function returns state.good / state.NEW_GOOD.
        '''
        rcd = rf_conditioning_data


        #TODO AJG: update the time/pulses until BDR is low enough to ramp countdowns

        if self.data.values[rcd.breakdown_rate_low] == False:

            self.data.breakdown_rate_able_to_ramp_countdown()

        #print('\nFrom can_ramp_state\ncan_ramp_status_OLD = {}\ncan_ramp_status = {}'.format(self.data.values[rcd.BD_state_OLD],
        # self.data.values[rcd.BD_state]))

        # set the old status to the current status
        self.data.values[rcd.can_ramp_status_OLD] = self.data.values[rcd.can_ramp_status]

        # set all_BD_good = True and if ANY (doesn't have to be ALL) of the OMED, vac spikes, DC
        # are state.BAD / state.NEW_BAD then all_BD_good gets set to False

        # This is a compact expression which returns True if ALL components in the list are tTrue, otherwise False is returned
        all_can_ramps_good = all([self.data.values[rcd.gui_can_ramp], self.data.values[rcd.vac_level_can_ramp ], self.data.values[
            rcd.cav_pwr_ratio_can_ramp], self.data.values[rcd.breakdown_rate_low]])

        #print("gui_can_ramp = {}\nvac_level_can_ramp = {}\ncav_pwr_ratio_can_ramp = {}\nbreakdown_rate_low = {}".format(
        #    self.data.values[rcd.gui_can_ramp], self.data.values[rcd.vac_level_can_ramp ], self.data.values[
        #        rcd.cav_pwr_ratio_can_ramp], self.data.values[rcd.breakdown_rate_low]))

        # if set all_can_ramps_good = True then set can_ramp_status to state.GOOD
        # Else set can_ramp_status to state.BAD
        if all_can_ramps_good:
            self.data.values[rcd.can_ramp_status] = state.GOOD
        else:
            self.data.values[rcd.can_ramp_status] = state.BAD

        # NOW check to see if these are State.NEW_GOOD or state.NEW_BAD
        if is_new_good(self.data.values[rcd.can_ramp_status], self.data.values[rcd.can_ramp_status_OLD]):
            self.data.values[rcd.can_ramp_status] = state.NEW_GOOD

        if is_new_bad(self.data.values[rcd.can_ramp_status], self.data.values[rcd.can_ramp_status_OLD]):
            self.data.values[rcd.can_ramp_status] = state.NEW_BAD

        #print('After logic tree:\ncan_ramp_status = {}\n'.format(self.data.values[rcd.can_ramp_status]))

    def check_LLRF_state(self):
        '''
            check the state of LLRF output, (if gui allows and there is a bad state) reset the LLRF states
            sets a high level "LLRF_CAN_OUTPUT" state

            Checks if "modulator_good", "rfprot_good" & "gui_can_rf_output" are ALL True.
            Checks if "llrf_DAQ_rep_rate_status" is

            It then checks:

                llrf_interlock_status
                llrf_trigger_status
                rcd.pulse_length_status
                rcd.llrf_output_status
                rcd.llrf_ff_amp_locked_status
                rcd.llrf_ff_ph_locked_status
                rcd.llrf_DAQ_rep_rate_status

            If everything is True / state.GOOD / state.NEW_GOOD then function returns state.GOOD / state.NEW_GOOD
        '''

        rcd = rf_conditioning_data

        # set the old value to the current value
        self.data.values[rcd.can_llrf_output_state_OLD] = self.data.values[rcd.can_llrf_output_state]

        #print('\nFrom check_LLRF_state:\ncan_llrf_output_state_OLD = {}\ncan_llrf_output_state = {}'.format(self.data.values[
        #                                                                                                      rcd.can_llrf_output_state_OLD],
        #                                                                             self.data.values[rcd.can_llrf_output_state]))

        # check the state of the "ENABLE / DISABLE LLRF RF" button on GUI, the  RF protection and modulator, if they are bad we have decided NO-ARC
        # does not intervene

        if self.data.values[rcd.modulator_good]:
            if self.data.values[rcd.rfprot_good]:
                if self.data.values[rcd.gui_can_rf_output]:
                    self.data.values[rcd.GUI_mod_and_prot_good] = True
                else:
                    self.data.values[rcd.GUI_mod_and_prot_good] = False
            else:
                self.data.values[rcd.GUI_mod_and_prot_good] = False
        else:
            self.data.values[rcd.GUI_mod_and_prot_good] = False

        #print('GUI_mod_and_prot_good = {}'.format(GUI_mod_and_prot_good))

        if self.data.values[rcd.GUI_mod_and_prot_good]:

            # Go through each LLRF setting  that effect if there is RF power (feel free to add more)
            all_good = True
            if self.values[rcd.llrf_DAQ_rep_rate_status] == state.BAD:
                all_good = False
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
            elif self.data.values[rcd.llrf_DAQ_rep_rate_status] != state.GOOD:
                print("llrf_DAQ_rep_rate_status is not good")
                all_good = False

            #print('From check_LLRF_state:\nall_good = {}'.format(all_good))

            if all_good:
                self.data.values[rcd.can_llrf_output_state] = state.GOOD
            else:
                self.data.values[rcd.can_llrf_output_state] = state.BAD
            # NOW check to see if this is a new good or a new bad
            if is_new_good(self.data.values[rcd.can_llrf_output_state], self.data.values[rcd.can_llrf_output_state_OLD]):
                self.data.values[rcd.can_llrf_output_state] = state.NEW_GOOD

            if is_new_bad(self.data.values[rcd.can_llrf_output_state], self.data.values[rcd.can_llrf_output_state_OLD]):
                self.data.values[rcd.can_llrf_output_state] = state.NEW_BAD

        #print('After logic tree:\ncan_llrf_output_state = {}\n'.format(self.data.values[rcd.can_llrf_output_state]))

    def clear_log_ramp_curve(self):
        self.logger.message('clear_log_ramp_curve called from ' + str(inspect.stack()[1][3]))
        self.data.log_ramp_curve = None
        self.values[self.data.log_ramp_curve_index] = -1
        self.data.reset_event_pulse_count()
        self.values[self.data.ramp_mode] = ramp_method.NORMAL_RAMP



    def log_ramp_up(self):
        # # log data at the new setpoint MUST BE BEFORE  move_up_ramp_curve()
        # update pulse breakdown log

        self.hardware.llrf_controller.enable_trigger()

        self.data.add_to_pulse_breakdown_log(self.hardware.llrf_obj[0].amp_sp)
        self.monitor_hub.llrf_monitor.update_amp_vs_kfpow_running_stat()
        self.data.log_kly_fwd_power_vs_amp()

        '''
        /* FAST RAMP WE SET THE HI MASK FOR POWERS TO BE prop-to THE KFP MAX */
        if  (llrf.fast_ramp_mode)
        {
            if( stringIsSubString( data.name, "POWER"))
            {
                //message("Setting fast_ramp_hi_mask for ", data.name, " to ", llrf.fast_ramp_power_factor  * llrf.kly_fwd_power_max);
                std::fill(hi_mask.begin(), hi_mask.end(), llrf.fast_ramp_power_factor  * llrf.kly_fwd_power_max); // MAGIC NUMBER
            }
        }
        # setFastRampHiMaskPowerFactor( float )
        # getFastRampHiMaskPowerFactor()

        '''

        # someshort aliases
        #lrc = self.data.log_ramp_curve
        #lrci = self.values[self.data.log_ramp_curve_index]

        # switch here to set up curve if
        if self.data.log_ramp_curve is None:
            self.logger.message("!!Log Ramp curve is NONE, generating a new one", show_time_stamp = False)


            # WE assume the ramp index is set correctly !
            # GET NEW SET_POINT
            # new amp always returns a value!!
            power_finish = self.data.get_log_ramp_power_finsh()

            self.logger.message("power_finish = {}".format(power_finish, show_time_stamp = False))
            self.logger.message("breakdown_rate_low = {}".format(self.values[self.data.breakdown_rate_low], show_time_stamp = False))


            if self.values[self.data.breakdown_rate_low]:
                self.logger.message("Breakdown rate LO, log_ramp power_finish = {}".format(power_finish), show_time_stamp = False)
                #pass
            else:
                delta_power = self.data.get_power_and_num_pulses_for_ramp_index(self.data.get_ramp_index_from_power(power_finish))[1]

                power_finish -=  delta_power
                self.logger.message("Breakdown rate HI, delta_power = {}, final_power_finish = {}".format(delta_power, power_finish),
                                    show_time_stamp = False)


            # TODO power_finish add to values dict and the GUI

            self.logger.message("Log Ramp curve is NONE, generating a new one", show_time_stamp = False)
            self.data.generate_log_ramp_curve(p_start  = self.config.raw_config_data['LOG_RAMP_START_POWER'],
                                              p_finish =  power_finish ,
                                              ramp_rate =  self.config.raw_config_data['LOG_RAMP_CURVE_RAMP_RATE'],
                                              numsteps =  self.config.raw_config_data['LOG_RAMP_CURVE_NUMSTEPS'],
                                              pulses_per_step =  self.config.raw_config_data['LOG_RAMP_CURVE_PULSES_PER_STEP'])

            #self.logger.message("self.data.log_ramp_curve in maIn_controller = {}".format(self.data.log_ramp_curve))

        if self.data.log_ramp_curve is None:
            self.logger.message("!!ERROR!! Log Ramp curve is NONE, this should not happen ", show_time_stamp = True)
            raw_input()

        # # set new_amp
        lrci = self.values[self.data.log_ramp_curve_index]

        # we need to set the next setFastRampHiMaskPowerFactor before we call set_amp
        hi_mask_factor = self.data.log_ramp_curve[lrci][2]
        self.hardware.llrf_control.setFastRampHiMaskPowerFactor(hi_mask_factor)
        #print('hi_mask_power = {}'.format(hi_mask_power))

        #raw_input()

        if self.hardware.llrf_controller.set_amp(self.data.log_ramp_curve[lrci][1], update_last_amp_sp = False):
            # print('self.hardware.llrf_controller.set_amp(lrc[lrci][1] = {}'.format( self.hardware.llrf_controller.set_amp(
            # self.data.log_ramp_curve[lrci][1])))
            # if we have reached teh end of the log ramp curve ...
            if self.values[self.data.log_ramp_curve_index] == len(self.data.log_ramp_curve) -1:
                self.logger.message("Log Ramp finished, calling clear_log_ramp_curve()", show_time_stamp = False)
                self.clear_log_ramp_curve()
                self.hardware.llrf_control.fastRampModeOff() # set the masks back to nominal after infinite +_hi masks for log_ramping
                self.values[rf_conditioning_data.ramp_mode] = ramp_method.NORMAL_RAMP
                current_normal_ramp_index = self.data.get_ramp_index_from_power(self.data.get_kf_running_stat_power_at_current_set_point())

                if current_normal_ramp_index > len(ramp) - 1:
                    self.values[rf_conditioning_data.required_pulses] = ramp[-1][0]
                else:
                    self.values[rf_conditioning_data.required_pulses] = ramp[current_normal_ramp_index][0]

                # set the ramp index when we reahc teh top of teh rmap curve
                self.data.set_ramp_index_for_current_power()

                # print('\n#From log_ramp_up\nrequired_pulses = {}\nramp[current_normal_ramp_index][0] = {}'.format(self.values[
                #                                                                                                   rf_conditioning_data.required_pulses], ramp[current_normal_ramp_index][0]))
            else:
                ''' set the number of pulses '''
                rcd = rf_conditioning_data
                rcd.values[rcd.required_pulses] = self.data.log_ramp_curve[self.values[self.data.log_ramp_curve_index]][0]
                #print('required_pulses = {}'.format(rcd.values[rcd.required_pulses]))
                #print('self.data.log_ramp_curve[self.values[self.data.log_ramp_curve_index]] = {}'.format(self.data.log_ramp_curve[self.values[
                # self.data.log_ramp_curve_index]]))
                #raw_input()
                # Be careful manually setting parameters, are these the correct type?
                rcd.values[rcd.last_requested_power_change] = 0
                rcd.values[rcd.next_requested_power_change] = 0
                rcd.values[rcd.event_pulse_count_zero] = rcd.values[rcd.pulse_count]
                rcd.values[rcd.event_pulse_count] = 0
                #self.logger.message(__name__ + ' reset_event_pulse_count')
                #self.logger.message('new event_pulse_count_zero = {}'.format(rcd.values[rcd.event_pulse_count_zero]))
                # print('self.values[self.data.log_ramp_curve_index] = {}'.format(self.values[self.data.log_ramp_curve_index]))
            self.values[self.data.log_ramp_curve_index] += 1
        else:
            self.logger.message("we failed to set the requested amplitude .... erm.... not sure what to do ????\n*** LAST TIME THIS HAPPENED THE LIBERA AMP_SP "
                                "HARD LIMIT WAS REACHED (10000) - LSC can change this ***", show_time_stamp = False)
             #pass


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
        new_amp = self.data.get_new_set_point(self.values[rf_conditioning_data.next_requested_power_change])  # value from ramp.py and ramp_index
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
            or self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__ENOUGH_BINS__NOT_ENOUGH_NON_ZERO \
            or self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__DELTA_GTRTHN_MAX \
            or self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__NEG_RAMP \
            or self.values[rf_conditioning_data.last_ramp_method] == ramp_method.DEFAULT__FLAT_RAMP:
            pass
        elif self.values[rf_conditioning_data.last_ramp_method] == ramp_method.UNKNOWN:
            self.logger.message("!!!MAJOR ERROR!!!!\nramp_method = {}".format(self.values[rf_conditioning_data.last_ramp_method]))
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
        #print("Calling update_plot")
        self.view.update_plot()
        QApplication.processEvents()
        #
        # reset active pulse counters
        self.data.reset_event_pulse_count()

        # reset self.values[self.data.pulses_to_next_ramp])
        #current_normal_ramp_index = self.data.get_ramp_index_from_power(self.data.get_kf_running_stat_power_at_current_set_point())
        #self.values[rf_conditioning_data.required_pulses] = ramp[current_normal_ramp_index][0]
        #self.values[self.data.pulses_to_next_ramp] =
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
        new_amp = self.data.get_new_set_point(-self.values[rf_conditioning_data.next_requested_power_change]) # value from ramp.py and ramp_index
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
        ''' this function should be connected to the GUI enable / disable LLRF, but MUST be run
        AFTER rf_conditioning_data.gui_can_rf_output is changed to the requested value '''
        if self.values[rf_conditioning_data.gui_can_rf_output]:
            self.logger.message("toggle_RF_output(), gui.can_rf_output_state, so calling enable_llrf ")
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
        print()
        self.logger.message("self.update_expert_values called")
        self.monitor_hub.llrf_monitor.get_llrf_expert_values()
        # update the gui with the latest values
        self.view.update_expert_values_in_gui()

