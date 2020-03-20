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
//  FileName:    rf_conditioning_data.py
//  Description: rf_condition_data, the main data class for RF Conditioning, all main classes own
//               one of these to access all data, THIS COULD BE HELD IN A MODULE NOT A CLASS???
//
//*/
'''

import numpy as np
from matplotlib import pyplot as plt
from config import config
from rf_conditioning_logger import rf_conditioning_logger
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from ramp import *
from src.data.state import state


class rf_conditioning_data(object):
    # whoami

    #
    # these are just monitors that are working
    # they are used for the main_loop
    # they are VAC,DC,BREAKDOWN,BREAKDOWN_RATE
    main_monitor_states = {}
    previous_main_monitor_states = {}

    # the items required for enable RF
    # RF_MOD, RF_PROT, LLRF
    # (pulse , rf output, interlock, trigger, amp_locked, phase_locked ...)
    enable_RF_monitor_states = {}

    # log of last million pulses including:
    current_power = 0


    """
    NOT SURE IF DEBUG DOES ANYTHING
    """
    debug = False
    def __init__(self, debug = False):
        rf_conditioning_data.debug = debug
        # config
        self.config = config()
        self.config_data = self.config.raw_config_data
        # alias for data dictionary
        self.values = rf_conditioning_data.values
        # we can straight  away set some value from config_data
        self.set_values_from_config()
        #
        # logging
        self.logger = rf_conditioning_logger()

    def set_values_from_config(self):
        """
        In this function we copy values from the config to the values
        We can also set values that need to be derived from config-data
        generally the values dict should contain values that can change,
        The config can be passed around classes to get config values where they are needed
        This is a rule-of-thumb and i expect things to get hacked in as we learn more
        :return:
        """
        # alias for shorter lines
        rcd = rf_conditioning_data
        cd = self.config_data
        v = self.values
        v[rcd.breakdown_rate_aim] = cd[config.BREAKDOWN_RATE_AIM]
        v[rcd.llrf_DAQ_rep_rate_aim] = cd[config.RF_REPETITION_RATE]
        v[rcd.llrf_DAQ_rep_rate_max] = cd[config.RF_REPETITION_RATE] + cd[
            config.RF_REPETITION_RATE_ERROR]
        v[rcd.llrf_DAQ_rep_rate_min] = cd[config.RF_REPETITION_RATE] - cd[
            config.RF_REPETITION_RATE_ERROR]

        ## set the pusle length min adn max ranges
        v[rcd.expected_pulse_length] = cd[config.PULSE_LENGTH]
        v[rcd.pulse_length_min] = cd[config.PULSE_LENGTH] + cd[
            config.PULSE_LENGTH_ERROR]
        v[rcd.pulse_length_max] = cd[config.PULSE_LENGTH] - cd[
            config.PULSE_LENGTH_ERROR]



    def setup_pulse_count_breakdown_log(self):
        """
        this is way too complicated ... but its processing the data in two ways,
        once by amp_setpoint and once by pusle count, it generates to main lists:
        1) rf_condition_data.amp_sp_history
              Sorted by amp_setpoint
              Used to define how to ramp up adn down
        2) rf_condition_data.last_million_log
              Sorted by pulse count
              used to define the Breakdown Rate etc.
        if I read through the comments, i can basically work out what is going on
        """
        # TODO AJG: we should use fitting to move down in power steps instead of next_sp_decrease in
        #  the same way we move up in power steps
        # TODO AJG: the ramp index should continue to increment, even when it as above the total
        #  number of ramp points, then we know how many steps we have actually gone up / down

        # local alias for shorter lines
        rcd = rf_conditioning_data
        message = self.logger.message
        #
        # get the pulse_break_down_log entries from file
        pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
        #
        # based on the log file we set active pulse count total,
        # the starting point is the one before the last entry  (WHY???? DJS Jan 2019)
        #
        # FIRST:
        # save the last entry, log_pulse_count and breakdown count
        # keep this seperate as pulse_count will get overwritten!!
        #
        self.values[rcd.log_pulse_count] = int(pulse_break_down_log[-1][0])
        self.values[rcd.breakdown_count] = int(pulse_break_down_log[-1][1])
        #
        # first amp is the second to last one in log file (WHY???? DJS Jan 2019,
        # maybe we should ramp to this value on startup)
        # remove values greater than than last_amp_sp_in_file
        #
        last_amp_sp_in_file = int(pulse_break_down_log[-1][2])
        indices_to_remove = []
        index_to_remove = 0
        for entry in pulse_break_down_log:
            if entry[2] >= last_amp_sp_in_file:
                indices_to_remove.append(index_to_remove)
            index_to_remove += 1
        #
        # delete index_to_remove from pulse_break_down_log
        # https://stackoverflow.com/questions/11303225/how-to-remove-multiple-indexes-from-a-list
        # -at-the-same-time
        for index in sorted(indices_to_remove, reverse=True):
            del pulse_break_down_log[index]
        #
        # sort the list by setpoint (part 2) then pulse_count (part 0)
        sorted_pulse_break_down_log_1 = sorted(pulse_break_down_log, key=lambda x: (x[2], x[0]))
        #
        # As we have all the time in the world...
        # make another list, ampSP_sorted_pulse_break_down_log, this has NO Setpoints = the final
        # sp in sorted_pulse_break_down_log_1
        # the final entry in sorted_pulse_break_down_log_1 is the sp point with highest pulse count
        ampSP_sorted_pulse_break_down_log = []
        last_i = sorted_pulse_break_down_log_1[-1]
        #
        #
        for i in sorted_pulse_break_down_log_1:
            if last_i[2] == i[2]:
                pass
            else:
                ampSP_sorted_pulse_break_down_log.append(i)
            last_i = i
        #
        # next we must insert the data in to the main data values dictionary
        #
        # set the ramp index
        self.values[rcd.current_ramp_index] = ampSP_sorted_pulse_break_down_log[-1][3]
        #
        # amp_setpoint history history, THIS is used to decide where to ramp down,
        # and what amp_setpoint to use in fitting when ramping-up
        # write this list to the main log
        rcd.amp_sp_history = [int(i[2]) for i in ampSP_sorted_pulse_break_down_log]


        """ PRINT rf_condition_data amp SP history on startup"""
        # self.logger.message(self.my_name + ' amp SP history on startup ',
        #                            add_to_text_log=True, show_time_stamp=True)
        # to_write = []
        # for value in rcd.amp_sp_history:
        #     to_write.append(str(value))
        # message(','.join(to_write), add_to_text_log=True, show_time_stamp=False)


        #
        # The next amp_setpoint to set
        self.values[rcd.log_amp_set] = rcd.amp_sp_history[-1]
        #
        # the next amp_setpoint on ramp_down
        self.values[rcd.next_sp_decrease] = rcd.amp_sp_history[-2]
        #
        # pulse length (logged but not used as pulse_length is now defined by the pulse shaping
        # table)
        self.values[rcd.log_pulse_length] = float(ampSP_sorted_pulse_break_down_log[-1][4]) / float(
            1000.0)  # warning UNIT


        # TODO I don't tihnk this is used and doesn;t make sense to me now
        self.config_data['PULSE_LENGTH_START'] = self.values[rcd.log_pulse_length]

        #
        # set the number of pulses required at this step to the default, updated later
        self.values[rcd.required_pulses] = self.config_data['DEFAULT_PULSE_COUNT']
        #
        # Write to log
        message(__name__ + ' has processed the pulse_count_breakdown_log ')
        message([rcd.log_pulse_count + ' ' + str(self.values[rcd.log_pulse_count]),
                 rcd.required_pulses + ' ' + str(self.values[rcd.required_pulses]),
                 rcd.breakdown_count + ' ' + str(self.values[rcd.breakdown_count]),
                 rcd.log_amp_set + ' ' + str(self.values[rcd.log_amp_set]),
                 rcd.current_ramp_index + ' ' + str(self.values[rcd.current_ramp_index]),
                 # hmmm what to do about pulse length chaing
                 # 'pulse length = ' + str(self._llrf_config['PULSE_LENGTH_START']),
                 rcd.next_sp_decrease + ' ' + str(self.values[rcd.next_sp_decrease])], )
        #
        # Setting the last 10^6 breakdown last_106_bd_count
        #
        # get the last million pulses from THE ORIGINAL pulse_break_down_log
        # !!! WE must use the original pulse_break_down_log, as it will have the true
        # breakdown_count and pulse number !!!
        # !!! (remember above we deleted the last entry in pulse_break_down_log to  generate
        # amp_sp_history         !!!
        pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
        one_million_pulses_ago = self.values[rcd.log_pulse_count] - self.config_data[
            'NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']
        rcd.last_million_log = [x for x in pulse_break_down_log if x[0] >= one_million_pulses_ago]
        #
        # write last_million_log to log

        """ PRINT lAST MILLION PULSES """
        # message('Last million pulses', add_to_text_log=True,show_time_stamp=False)
        # for value in rcd.last_million_log:
        #     str1 = ', '.join(str(e) for e in value)
        #     message(str1, add_to_text_log=True, show_time_stamp=False)

        message('One Million pulses ago  = ' + str(one_million_pulses_ago))
        first_entry = ' , '.join(str(x) for x in rcd.last_million_log[0])
        last_entry = ' , '.join(str(x) for x in rcd.last_million_log[-1])
        message('last_million_log[ 0] = '+first_entry)
        message('last_million_log[-1] = '+last_entry)
        #
        # sanity check
        #
        sanity_passed = True
        if rcd.last_million_log[-1][1] != self.values[rcd.breakdown_count]:
            message('Error in breakdown count')
            sanity_passed = False
        if rcd.last_million_log[-1][0] != self.values[rcd.log_pulse_count]:
            message('Error in pulse_count')
            sanity_passed = False
        if sanity_passed:
            message('Getting the pulse_breakdown_log passed sanity check')
        else:
            message('!!WARNING!! When getting the pulse_breakdown_log we failed a sanity check!!')

        #
        # Now we are free to update the breakdown stats !!
        '''MAYBE DON'T CALL THIS HERE YET!!! ????'''
        message("update_breakdown_stats here ????????????????????")
        #self.update_breakdown_stats()

    def update_breakdown_stats(self):
        '''

        :return:
        '''
        # local alias for shorter lines
        rcd = rf_conditioning_data
        message = self.logger.message

        old_last_106_bd_count = self.values[rcd.last_106_bd_count]
        self.values[rcd.breakdown_count] = rcd.last_million_log[-1][1]
        self.values[rcd.last_106_bd_count] = rcd.last_million_log[-1][1] - rcd.last_million_log[0][
            1]
        # if we have more than 1 million pulses its easy
        if rcd.last_million_log[-1][0] > self.config_data['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']:
            self.values[rcd.breakdown_rate] = self.values[rcd.last_106_bd_count]
        else:  # else do some math
            if rcd.last_million_log[-1][0] == 0:
                self.values[rcd.breakdown_rate] = 0
            else:
                # !!!!!!!!!! THIS EQUATION MAY NOT BE CORRECT !!!!!!!!!!!!!!
                self.values[rcd.breakdown_rate] = float(
                    self.values[rcd.last_106_bd_count] * self.config_data[
                        'NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']) / float(
                    rcd.last_million_log[-1][0] - rcd.last_million_log[0][0])

        # set is breakdwon rate hi
        self.values[rcd.breakdown_rate_hi] = self.values[rcd.breakdown_rate] > self.values[
            rcd.breakdown_rate_aim]

        if old_last_106_bd_count != self.values[rcd.last_106_bd_count]:
            self.logger.message_header(' NEW last_106_bd_count ', add_to_text_log=True,
                                       show_time_stamp=False)
            message('Total breakdown_count = ' + str(rcd.last_million_log[-1][1]),
                    add_to_text_log=True, show_time_stamp=False)

            message('Last million pulse count => ' + str(rcd.last_million_log[-1][0]) + ' - ' + str(
                rcd.last_million_log[0][0]) + ' = ' + str(
                rcd.last_million_log[-1][0] - rcd.last_million_log[0][0]), add_to_text_log=True,
                    show_time_stamp=False)
            message(
                'Last million breakdown_count => ' + str(rcd.last_million_log[-1][1]) + ' - ' + str(
                    rcd.last_million_log[0][1]) + ' = ' + str(self.values[rcd.last_106_bd_count]),
                add_to_text_log=True, show_time_stamp=False)

            if self.values[rcd.breakdown_rate_hi]:
                message(
                    'Breakdown rate High: ' + str(self.values[rcd.breakdown_rate]) + ' > ' + str(
                        self.values[rcd.breakdown_rate_aim]), add_to_text_log=True,
                    show_time_stamp=False)

                # ESTIMATE THE NUMBER OF PULSES BEFORE WE GO GOOD AGAIN


            else:
                message(
                    'Breakdown rate good: ' + str(self.values[rcd.breakdown_rate]) + ' <= ' + str(
                        self.values[rcd.breakdown_rate_aim]), add_to_text_log=True,
                    show_time_stamp=False)

    def update_last_million_pulse_log(self):
        """
        Every time we check te numebr of pulses / breakdown counts we update the last million log
        """
        # local alias for shorter lines
        rcd = rf_conditioning_data

        # add the next set of values to the last_million_log
        rcd.last_million_log.append(
            [self.values[rcd.pulse_count], self.values[rcd.breakdown_count],
                self.values[rcd.current_ramp_index], self.values[rcd.pulse_length]])

        # remove entries that are mor ethan 1 millino pulses ago
        # TODO should we hardcode in the million pulses??? or have it  as a config parameters,
        #  and rename everything that references 1 million???? MAYBE CALL IT
        #  recent_breakdown_history, recent_bd_history >>> ?
        #
        while rcd.last_million_log[-1][0] - rcd.last_million_log[0][0] > self.config_data[
            config.NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY]:
            rcd.last_million_log.pop(0)

        # update all the breakdown stats based on the last millino log
        self.update_breakdown_stats()  # raw_input()

    def add_to_pulse_breakdown_log(self, amp):
        """
        update the _pulse_count_log_file with latest numbers
        AMP is passed, as values dict, may not have the exact lastest value
        (e.g. after a ramp up or ramp down)
        :param amp: the amp_set point to write to file
        """
        rcd = rf_conditioning_data
        if amp > 100:  # MAGIC_NUMBER
            self.logger.add_to_pulse_count_breakdown_log(
                [rcd.values[rcd.pulse_count], rcd.values[rcd.breakdown_count], int(amp),
                    int(rcd.values[rcd.current_ramp_index]),
                    int(rcd.values[rcd.pulse_length] * 1000)  # MAGIC_NUMBER UNITS
                ])

    def initialise(self):
        """
        has to be CALLED after the config and logging is setup in main controller
        :return:
        """
        # alias for shorter lines
        rcd = rf_conditioning_data

        #
        # the pulse breakdwon log gets its own function, it's cancer
        self.setup_pulse_count_breakdown_log()
        #
        # amp_vs_kfpow_running_stat dictionary
        rcd.amp_vs_kfpow_running_stat = self.logger.get_kfpow_running_stat_log()

        #TODO AJG: bin the amp-power data here after being read in
        print 'rcd.amp_vs_kfpow_running_stat[0] = ', rcd.amp_vs_kfpow_running_stat[0]
        print 'rcd.amp_vs_kfpow_running_stat[0][0] = ', rcd.amp_vs_kfpow_running_stat[0][0]
        print 'len(rcd.amp_vs_kfpow_running_stat) = ', len(rcd.amp_vs_kfpow_running_stat)

        #TODO AJG: cycle over 'rcd.amp_vs_kfpow_running_stat' and append ...
        # [0] = amp
        # [1] = power
        # [2] = rolling variance * (num_pulses -1)  .....I think!
        AMP_preBin = []
        POW_preBin = []
        for ap in rcd.amp_vs_kfpow_running_stat:
            #print 'ap = ', ap
            if ap == [1, 2428422.90007, 0.0]:
                print 'ap[0] = ', ap[0]

            AMP_preBin.append(ap)
            POW_preBin.append(rcd.amp_vs_kfpow_running_stat[ap][1])

        bin_width = self.config.raw_config_data['BIN_WIDTH']
        max_amp = self.config.raw_config_data['MAX_AMP']
        max_pow = self.config.raw_config_data['MAX_POW']

        print 'len(AMP_preBin) = ', len(AMP_preBin)
        print 'len(POW_preBin) = ', len(POW_preBin)
        print 'bin_width = ', bin_width
        print 'max_amp = ', max_amp
        print 'max_pow = ', max_pow

        X, bin_mean, bedges, bin_pop, data_binned = self.logger.initial_bin(AMP_preBin,
                                            POW_preBin, bin_width, max_amp, max_pow)

        #TODO AJG: need to return initial_bin as a dictionary NOT a list:
        rcd.amp_vs_kfpow_binned = [X, bin_mean, bedges, bin_pop, data_binned]

        #TODO AJG: diagnostic plot saved to work folder:

        bin_plots_path = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Work\test\RF_Cond_binning_dev'
        plt.scatter(AMP_preBin, POW_preBin, c='k', s=1.0, marker='.', label='Data', zorder=1)
        plt.scatter(X, bin_mean, c='r', s=35, marker='x', label='Binned Mean', zorder=0)
        #plt.errorbar(X, bin_mean, yerr=ERR, xerr=0, fmt='none', ecolor='red', elinewidth=1.0, capsize=2.0, capthick=1.0)
        plt.xlabel('Set Point')
        plt.ylabel('Power (MW)')
        plt.legend()
        plt.grid(True)
        plt.savefig(bin_plots_path + r'\Binning_Plot_test.png')
        plt.close('all')

        #
        # set some values from teh config, DO all of them here???
        ##elf.values[dat.pulse_length_start] = self.llrf_config['PULSE_LENGTH_START']
        # self.values[rcd.pulse_length_aim] = cd['PULSE_LENGTH_AIM']
        # self.values[rcd.pulse_length_aim_error] = cd['PULSE_LENGTH_AIM_ERROR']
        # self.values[rcd.pulse_length_min] = cd['PULSE_LENGTH_AIM'] - cd['PULSE_LENGTH_AIM_ERROR']
        # self.values[rcd.pulse_length_max] = cd['PULSE_LENGTH_AIM'] + cd['PULSE_LENGTH_AIM_ERROR']




    ''' 
        The values dictionary. 
        The main data dictionary for the application almost everything goes in here, 
         apart from minor things like GUI flags, data from the config file
    
        THIS IS WHERE ALL THE MAIN DATA FOR RF CONDITIONING APPLICATION LIVES
        It is used by almost every class, to get and set data
    
        In order to not have mistakes, define a value then add it to the values dictionary, 
        Then give the values dictionary an initial value THAT IS OF THE EXPECTED TYPE FOR THE  
        REAL DATA.  
        WHEN NOT DEBUGGING: We set the values of the dictionary to be None, this is so that when 
        we start writing then to file we can check they are being updated as expected. 
    '''

    dummy_float = -9999.9999
    dummy_int   = -9999999
    dummy_state = state.UNKNOWN

    values = {} # A list of the keys for values
    all_value_keys = []  # A list of the keys for values

    # keys for all the data we monitor
    time_stamp = 'time_stamp'
    all_value_keys.append(time_stamp)
    values[time_stamp] = dummy_float # CHECK TYPE

    # STATUS PF MAIN MONITORS
    vac_spike_status = 'vac_spike_status'
    all_value_keys.append(vac_spike_status)
    values[vac_spike_status] = dummy_state

    DC_spike_status = 'DC_spike_status'
    all_value_keys.append(DC_spike_status)
    values[DC_spike_status] = dummy_state

    rev_power_spike_count = 'rev_power_spike_count'
    all_value_keys.append(rev_power_spike_count)
    values[rev_power_spike_count] = dummy_int

    # THERE are N water temps that are defined at run time!!!
    # THESE GET ADDED BY THE water_temperature_monitor

    cav_temp_gui = 'cav_temp_gui'
    water_temp_gui = 'water_temp_gui'
    all_value_keys.append(water_temp_gui)
    values[water_temp_gui] = dummy_float
    all_value_keys.append(cav_temp_gui)
    values[cav_temp_gui] = dummy_float

    pulses_to_next_ramp = 'pulses_to_next_ramp'
    all_value_keys.append(pulses_to_next_ramp)
    values[pulses_to_next_ramp] = dummy_int


    sol_value = 'sol_value'
    all_value_keys.append(sol_value)
    values[sol_value] = dummy_float

    # Mean Values of Traces # TODO: CHANGE THIS NAMES TO MORE CANONICAL ONES
    cav_temp = 'cav_temp'
    all_value_keys.append(cav_temp)
    values[cav_temp] = dummy_float

    # Mean Values of Traces # TODO: CHANGE THIS NAMES TO MORE CANONICAL ONES
    fwd_cav_pwr = 'fwd_cav_pwr'
    all_value_keys.append(fwd_cav_pwr)
    values[fwd_cav_pwr] = dummy_float

    fwd_kly_pwr = 'fwd_kly_pwr'
    all_value_keys.append(fwd_kly_pwr)
    values[fwd_kly_pwr] = dummy_float

    rev_kly_pwr = 'rev_kly_pwr'
    all_value_keys.append(vac_spike_status)
    values[rev_kly_pwr] = dummy_float

    rev_cav_pwr = 'rev_cav_pwr'
    all_value_keys.append(vac_spike_status)
    values[rev_cav_pwr] = dummy_float

    probe_pwr = 'probe_pwr'
    all_value_keys.append(vac_spike_status)
    values[probe_pwr] = dummy_float

    fwd_cav_pha = 'fwd_cav_pha'
    all_value_keys.append(vac_spike_status)
    values[fwd_cav_pha] = dummy_float

    fwd_kly_pha = 'fwd_kly_pha'
    all_value_keys.append(vac_spike_status)
    values[fwd_kly_pha] = dummy_float

    rev_kly_pha = 'rev_kly_pha'
    all_value_keys.append(vac_spike_status)
    values[rev_kly_pha] = dummy_float

    rev_cav_pha = 'rev_cav_pha'
    all_value_keys.append(vac_spike_status)
    values[rev_cav_pha] = dummy_float

    probe_pha = 'probe_pha'
    all_value_keys.append(vac_spike_status)
    values[probe_pha] = dummy_float

    vac_level = 'vac_level'
    all_value_keys.append(vac_level)
    values[vac_level] = dummy_float

    DC_level = 'DC_level'
    all_value_keys.append(DC_level)
    values[DC_level] = dummy_float

    vac_valve_status = 'vac_valve_status'
    all_value_keys.append(vac_valve_status)
    values[vac_valve_status] = state.UNKNOWN

    num_outside_mask_traces = 'num_outside_mask_traces'
    all_value_keys.append(num_outside_mask_traces)
    values[num_outside_mask_traces] = dummy_int

    probe_outside_mask_count = 'probe_outside_mask_count'
    all_value_keys.append(probe_outside_mask_count)
    values[probe_outside_mask_count] = dummy_int

    forward_outside_mask_count = 'probe_outside_mask_count'
    all_value_keys.append(forward_outside_mask_count)
    values[forward_outside_mask_count] = dummy_int

    reverse_outside_mask_count = 'reverse_outside_mask_count'
    all_value_keys.append(reverse_outside_mask_count)
    values[reverse_outside_mask_count] = dummy_int

    breakdown_status = 'breakdown_status'
    all_value_keys.append(breakdown_status)
    values[breakdown_status] = dummy_int

    breakdown_rate_aim = 'breakdown_rate_aim'
    all_value_keys.append(breakdown_rate_aim)
    values[breakdown_rate_aim] = dummy_int

    # these are values from the pulse_breakdown_log
    log_pulse_count = 'log_pulse_count'
    all_value_keys.append(log_pulse_count)
    values[log_pulse_count] = dummy_int
    #log_breakdown_count = 'log_breakdown_count'
    log_amp_set = 'log_amp_set'
    all_value_keys.append(log_amp_set)
    values[log_amp_set] = dummy_int

    current_ramp_index = 'current_ramp_index'
    all_value_keys.append(current_ramp_index)
    values[current_ramp_index] = dummy_int

    breakdown_count = 'breakdown_count'
    all_value_keys.append(breakdown_count)
    values[breakdown_count] = state.UNKNOWN

    elapsed_time = 'elapsed_time'
    all_value_keys.append(elapsed_time)
    values[elapsed_time] = state.UNKNOWN

    breakdown_rate = 'breakdown_rate'
    all_value_keys.append(breakdown_rate)
    values[breakdown_rate] = state.UNKNOWN

    breakdown_rate_hi= 'breakdown_rate_hi'
    all_value_keys.append(breakdown_rate_hi)
    values[breakdown_rate_hi] = state.UNKNOWN

    last_106_bd_count='last_106_bd_count'
    all_value_keys.append(last_106_bd_count)
    values[last_106_bd_count] = dummy_int

    pulse_count = 'pulse_count'
    all_value_keys.append(pulse_count)
    values[pulse_count] = dummy_int

    event_pulse_count = 'event_pulse_count'
    all_value_keys.append(event_pulse_count)
    values[event_pulse_count] = dummy_int

    duplicate_pulse_count = 'duplicate_pulse_count'
    all_value_keys.append(duplicate_pulse_count)
    values[duplicate_pulse_count] = dummy_int

    # Hold RF ON handle scontrolling these, we just monitor
    rfprot_state = 'rfprot_state'
    all_value_keys.append(rfprot_state)
    values[rfprot_state] = state.UNKNOWN

    modulator_state = 'modulator_state'
    all_value_keys.append(modulator_state)
    values[modulator_state] = state.UNKNOWN

    mod_output_status = 'mod_output_status'
    all_value_keys.append(mod_output_status)
    values[mod_output_status] = state.UNKNOWN

    can_rf_output_OLD = 'can_rf_output_OLD'
    all_value_keys.append(can_rf_output_OLD)
    values[can_rf_output_OLD] = state.UNKNOWN

    can_rf_output = 'can_rf_output'
    all_value_keys.append(can_rf_output)
    values[can_rf_output] = state.UNKNOWN

    # This i sthe "general interloac" and should be re-named to reflect this
    llrf_interlock = 'llrf_interlock' # The read value from EPICS
    all_value_keys.append(llrf_interlock)
    values[llrf_interlock] = state.UNKNOWN

    llrf_interlock_status = 'llrf_interlock_status' # the apps internal state, good, new_bad etc
    all_value_keys.append(llrf_interlock_status)
    values[llrf_interlock_status] = state.UNKNOWN

    # the state of the "Trace interlocks" these are where you can specify a power that disables LLRF
    llrf_trace_interlock = 'llrf_trace_interlock' # The read value from EPICS
    all_value_keys.append(llrf_trace_interlock)
    values[llrf_trace_interlock] = state.UNKNOWN


    llrf_trigger = 'llrf_trigger'
    all_value_keys.append(llrf_trigger)
    values[llrf_trigger] = state.UNKNOWN

    llrf_trigger_status = 'llrf_trigger_status'
    all_value_keys.append(llrf_trigger_status)
    values[llrf_trigger_status] = state.UNKNOWN

    ## PULSE LENGTH
    pulse_length = 'pulse_length'
    all_value_keys.append(pulse_length)
    values[pulse_length] = dummy_float

    expected_pulse_length = 'expected_pulse_length'
    all_value_keys.append(expected_pulse_length)
    values[expected_pulse_length] = dummy_float

    pulse_length_min = 'pulse_length_min'
    all_value_keys.append(pulse_length_min)
    values[pulse_length_min] = dummy_float

    pulse_length_max = 'pulse_length_max'
    all_value_keys.append(pulse_length_max)
    values[pulse_length_max] = dummy_float

    pulse_length_status = 'pulse_length_status' # the apps internal state, good, new_bad etc
    all_value_keys.append(pulse_length_status)
    values[pulse_length_status] = state.UNKNOWN

    llrf_output = 'llrf_output' # RF Output on LLRF panel
    all_value_keys.append(llrf_output)
    values[llrf_output] = state.UNKNOWN

    llrf_output_status = 'llrf_output_status' # the apps internal state, good, new_bad etc
    all_value_keys.append(llrf_output_status)
    values[llrf_output_status] = state.UNKNOWN

    llrf_ff_amp_locked = 'llrf_ff_amp_locked'
    all_value_keys.append(llrf_ff_amp_locked)
    values[llrf_ff_amp_locked] = state.UNKNOWN

    llrf_ff_amp_locked_status = 'llrf_ff_amp_locked_status' # the apps internal state, good, new_bad etc
    all_value_keys.append(llrf_ff_amp_locked_status)
    values[llrf_ff_amp_locked_status] = state.UNKNOWN

    llrf_ff_ph_locked  = 'llrf_ff_ph_locked'
    all_value_keys.append(llrf_ff_ph_locked)
    values[llrf_ff_ph_locked] = state.UNKNOWN

    llrf_ff_ph_locked_status  = 'llrf_ff_ph_locked_status' # the apps internal state, good, new_bad etc
    all_value_keys.append(llrf_ff_ph_locked_status)
    values[llrf_ff_ph_locked_status] = state.UNKNOWN

    llrf_DAQ_rep_rate = 'llrf_DAQ_rep_rate'
    all_value_keys.append(llrf_DAQ_rep_rate)
    values[llrf_DAQ_rep_rate] = dummy_float

    llrf_DAQ_rep_rate_aim = 'llrf_DAQ_rep_rate_aim'
    all_value_keys.append(llrf_DAQ_rep_rate_aim)
    values[llrf_DAQ_rep_rate_aim] = dummy_float

    llrf_DAQ_rep_rate_status = 'llrf_DAQ_rep_rate_status'
    all_value_keys.append(llrf_DAQ_rep_rate_status)
    values[llrf_DAQ_rep_rate_status] = state.UNKNOWN

    llrf_DAQ_rep_rate_status_previous = 'llrf_DAQ_rep_rate_status_previous'
    all_value_keys.append(llrf_DAQ_rep_rate_status_previous)
    values[llrf_DAQ_rep_rate_status_previous] = state.UNKNOWN

    llrf_DAQ_rep_rate_max = 'llrf_DAQ_rep_rate_max'
    all_value_keys.append(llrf_DAQ_rep_rate_max)
    values[llrf_DAQ_rep_rate_max] = state.UNKNOWN

    llrf_DAQ_rep_rate_min = 'llrf_DAQ_rep_rate_min'
    all_value_keys.append(llrf_DAQ_rep_rate_min)
    values[llrf_DAQ_rep_rate_min] = dummy_float

    required_pulses = 'required_pulses'
    all_value_keys.append(required_pulses)
    values[required_pulses] = state.UNKNOWN

    next_power_increase = 'next_power_increase'
    all_value_keys.append(next_power_increase)
    values[next_power_increase] = state.UNKNOWN

    log_pulse_length = 'log_pulse_length'
    all_value_keys.append(log_pulse_length)
    values[log_pulse_length] = state.UNKNOWN

    last_mean_power = 'last_mean_power'
    all_value_keys.append(last_mean_power)
    values[last_mean_power] = state.UNKNOWN

    amp_ff = 'amp_ff'
    all_value_keys.append(amp_ff)
    values[amp_ff] = state.UNKNOWN

    amp_sp = 'amp_sp'
    all_value_keys.append(amp_sp)
    values[amp_sp] = state.UNKNOWN

    phi_sp = 'phi_sp'
    all_value_keys.append(phi_sp)
    values[phi_sp] = state.UNKNOWN

    catap_max_amp = 'catap_max_amp'
    all_value_keys.append(catap_max_amp)
    values[catap_max_amp] = dummy_float

    # We set a flag to tell us if we have reached the limit of CATAP "hardcoded" maxampSP value
    catap_max_amp_can_ramp_status = 'catap_max_amp_can_ramp_status'
    all_value_keys.append(catap_max_amp_can_ramp_status)
    values[catap_max_amp_can_ramp_status] = True

    TOR_ACQM = 'TOR_ACQM'
    all_value_keys.append(TOR_ACQM)
    values[TOR_ACQM] = state.UNKNOWN

    TOR_SCAN = 'TOR_SCAN'
    all_value_keys.append(TOR_SCAN)
    values[TOR_SCAN] = state.UNKNOWN

    #
    # plot straight line fit values, old and current
    x_min = 'x_min'
    all_value_keys.append(x_min)
    values[x_min] = dummy_float

    x_max = 'x_max'
    all_value_keys.append(x_max)
    values[x_max] = dummy_float

    old_x_min = 'old_x_min'
    all_value_keys.append(old_x_min)
    values[old_x_min] = dummy_float

    old_x_max = 'old_x_max'
    all_value_keys.append(old_x_max)
    values[old_x_max] = dummy_float

    y_min = 'y_min'
    all_value_keys.append(y_min)
    values[y_min] = dummy_float

    y_max = 'y_max'
    all_value_keys.append(y_max)
    values[y_max] = dummy_float

    old_y_min = 'old_y_min'
    all_value_keys.append(old_y_min)
    values[old_y_min] = dummy_float

    old_y_max = 'old_y_max'
    all_value_keys.append(old_y_max)
    values[old_y_max] = dummy_float

    c = 'c'
    all_value_keys.append(c)
    values[c] = dummy_float

    m = 'm'
    all_value_keys.append(m)
    values[m] = dummy_float

    old_c = 'old_c'
    all_value_keys.append(old_c)
    values[old_c] = dummy_float

    old_m = 'old_m'
    all_value_keys.append(old_m)
    values[old_m] = dummy_float


    #latest_ramp_up_sp = 'latest_ramp_up_sp'
    last_sp_above_100 = 'last_sp_above_100'
    all_value_keys.append(last_sp_above_100)
    values[last_sp_above_100] = dummy_float

    max_sp_increase = 'max_sp_increase'
    all_value_keys.append(max_sp_increase)
    values[max_sp_increase] = dummy_float

    next_sp_decrease = 'next_sp_decrease'
    all_value_keys.append(next_sp_decrease)
    values[next_sp_decrease] = dummy_float



    vac_level_can_ramp = 'vac_level_can_ramp' # Flag which is T if we can ramp and f if we cna't base don current vac level
    all_value_keys.append(vac_level_can_ramp )
    values[vac_level_can_ramp ] = False




    # we know there will be some LLRF involved
    #llrf_type = LLRF_TYPE.UNKNOWN_TYPE

    # config
    # for logging
    log_param = None
    path = None
    time = None
    log_start = None
    should_write_header = True

    kly_fwd_power_history = []
    amp_sp_history = []
    sp_pwr_hist = []
    # fitting parameters
    previous_power = 0








    #latest_ramp_up_sp = 0


    # values = {}  # EXPLAIN THIS
    #
    # [values.update({x: 0}) for x in all_value_keys]

    #
    # values[vac_valve_status] = VALVE_STATE.VALVE_ERROR
    # #values[rev_power_spike_count] = STATE.UNKNOWN
    #
    # values[modulator_state] = GUN_MOD_STATE.UNKNOWN_STATE
    # values[rfprot_state] = RF_PROT_STATUS.UNKNOWN
    #
    # values[vac_spike_status] = state.UNKNOWN
    # values[DC_spike_status] = state.UNKNOWN
    # values[breakdown_status] = state.UNKNOWN
    # values[llrf_output_status] = state.UNKNOWN
    # values[llrf_trigger_status] = state.UNKNOWN
    # values[llrf_interlock_status] = state.UNKNOWN
    # values[llrf_ff_amp_locked] = state.UNKNOWN
    # values[llrf_ff_ph_locked] = state.UNKNOWN
    # values[can_rf_output_OLD] = state.UNKNOWN

#sss
    #
    # values[last_sp_above_100] = 0
    # #values[latest_ramp_up_sp] = 0
    #
    # values[vac_level_can_ramp] = state.GOOD

    # dummy_float = -999.0
    # dummy_int = -999.0
    # dummy_bool = -999.0




    #
    #
    # values[pulse_length] = dummy_float + 2
    # values[rev_kly_pwr] = dummy_float + 5
    # values[rev_cav_pwr] = dummy_float + 6
    # values[probe_pwr] = dummy_float + 7
    # values[vac_level] = dummy_float
    # values[breakdown_rate_aim] = dummy_int
    # values[breakdown_rate_hi] = dummy_bool
    #
    #
    # values[breakdown_rate] = dummy_int+ 11
    # values[breakdown_count] = dummy_int +2
    # values[pulse_count] = dummy_int + 13
    # values[event_pulse_count] = dummy_int +14
    # values[duplicate_pulse_count] = dummy_int +14
    # values[elapsed_time] = dummy_int + 15
    # values[DC_level] = dummy_float + 16
    # values[rev_power_spike_count] = dummy_int
    # values[next_power_increase] = -1
    # values[phase_mask_by_power_trace_1_set] = False
    # values[phase_mask_by_power_trace_2_set] = False
    # values[phase_end_mask_by_power_trace_1_time] = -1.0
    # values[phase_end_mask_by_power_trace_2_time] = -1.0
    #
    #
    #
    #
    # values[old_x_min] = dummy_float
    # values[old_y_min] = dummy_float
    # values[old_x_max] = dummy_float
    # values[old_y_max] = dummy_float
    # values[old_m] = dummy_float
    # values[old_c] = dummy_float
    # values[x_min] = dummy_float
    # values[x_max] = dummy_float
    # values[y_min] = dummy_float
    # values[x_max] = dummy_float
    # values[m] = dummy_float
    # values[c] = dummy_float
    #
    # amp_pwr_mean_data = {} # EXPLAIN THIS
    # amp_vs_kfpow_running_stat = {} # EXPLAIN THIS
    #
    # #logger
    # logger = None
    # _llrf_config = None
    # _log_config = None
    #
    # last_fwd_kly_pwr = None
    # last_amp = None
    #
    # #THERE ARE 2 COPIES OF THE last_million_log , FIX THIS !!!!!!!!!!!
    # last_million_log = None


    '''Expert Values '''

    expert_value_keys = []
    expert_values = {}

    vac_pv_val = "vac_pv_val"
    expert_value_keys.append(vac_pv_val)
    expert_values[vac_pv_val] = "STRING"

    vac_decay_mode_val                   = "vac_decay_mode_val"
    expert_value_keys.append(vac_decay_mode_val)
    expert_values[vac_decay_mode_val] = "STRING"

    vac_decay_level                      = "vac_decay_level"
    expert_value_keys.append(vac_decay_level)
    expert_values[vac_decay_level] = dummy_float

    vac_decay_time_val                   = "vac_decay_time_val"
    expert_value_keys.append(vac_decay_time_val)
    expert_values[vac_decay_time_val] = dummy_int

    vac_drop_amp                         = "vac_drop_amp"
    expert_value_keys.append(vac_drop_amp)
    expert_values[vac_drop_amp] = dummy_int

    vac_hi_pressure                      = "vac_hi_pressure"
    expert_value_keys.append(vac_hi_pressure)
    expert_values[vac_hi_pressure] = dummy_float

    vac_spike_delta_val                  = "vac_spike_delta_val"
    expert_value_keys.append(vac_spike_delta_val)
    expert_values[vac_spike_delta_val] = dummy_float

    vac_num_samples_to_average_val       = "vac_num_samples_to_average_val"
    expert_value_keys.append(vac_num_samples_to_average_val)
    expert_values[vac_num_samples_to_average_val] = "STRING"

    vac_drop_amp_val                     = "vac_drop_amp_val"
    expert_value_keys.append(vac_drop_amp_val)
    expert_values[vac_drop_amp_val] = "STRING"

    ramp_when_hi                         = "ramp_when_hi"
    expert_value_keys.append(ramp_when_hi)
    expert_values[ramp_when_hi] = "STRING"

    vac_decay_mode                       = "vac_decay_mode"
    expert_value_keys.append(vac_decay_mode)
    expert_values[vac_decay_mode] = "STRING"

    vac_decay_level_val                  = "vac_decay_level_val"
    expert_value_keys.append(vac_decay_level_val)
    expert_values[vac_decay_level_val] = "STRING"

    vac_hi_pressure_val                  = "vac_hi_pressure_val"
    expert_value_keys.append(vac_hi_pressure_val)
    expert_values[vac_hi_pressure_val] = "STRING"

    ramp_when_hi_val                     = "ramp_when_hi_val"
    expert_value_keys.append(ramp_when_hi_val)
    expert_values[ramp_when_hi_val] = "STRING"

    vac_spike_check_time_val             = "vac_spike_check_time_val"
    expert_value_keys.append(vac_spike_check_time_val)
    expert_values[vac_spike_check_time_val] = "STRING"

    vac_spike_check_time                 = "vac_spike_check_time"
    expert_value_keys.append(vac_spike_check_time)
    expert_values[vac_spike_check_time] = "STRING"

    is_breakdown_monitor_kf_pow          = "is_breakdown_monitor_kf_pow"
    expert_value_keys.append(is_breakdown_monitor_kf_pow)
    expert_values[is_breakdown_monitor_kf_pow] = False

    is_breakdown_monitor_kr_pow          = "is_breakdown_monitor_kr_pow"
    expert_value_keys.append(is_breakdown_monitor_kr_pow)
    expert_values[is_breakdown_monitor_kr_pow] = False

    is_breakdown_monitor_cf_pow          = "is_breakdown_monitor_cf_pow"
    expert_value_keys.append(is_breakdown_monitor_cf_pow)
    expert_values[is_breakdown_monitor_cf_pow] = False

    is_breakdown_monitor_cr_pow          = "is_breakdown_monitor_cr_pow"
    expert_value_keys.append(is_breakdown_monitor_cr_pow)
    expert_values[is_breakdown_monitor_cr_pow] = False

    is_breakdown_monitor_cp_pow          = "is_breakdown_monitor_cp_pow"
    expert_value_keys.append(is_breakdown_monitor_cp_pow)
    expert_values[is_breakdown_monitor_cp_pow] = False

    is_breakdown_monitor_kf_pha          = "is_breakdown_monitor_kf_pha"
    expert_value_keys.append(is_breakdown_monitor_kf_pha)
    expert_values[is_breakdown_monitor_kf_pha] = False

    is_breakdown_monitor_kr_pha          = "is_breakdown_monitor_kr_pha"
    expert_value_keys.append(is_breakdown_monitor_kr_pha)
    expert_values[is_breakdown_monitor_kr_pha] = False

    is_breakdown_monitor_cf_pha          = "is_breakdown_monitor_cf_pha"
    expert_value_keys.append(is_breakdown_monitor_cf_pha)
    expert_values[is_breakdown_monitor_cf_pha] = False

    is_breakdown_monitor_cr_pha          = "is_breakdown_monitor_cr_pha"
    expert_value_keys.append(is_breakdown_monitor_cr_pha)
    expert_values[is_breakdown_monitor_cr_pha] = False

    is_breakdown_monitor_cp_pha          = "is_breakdown_monitor_cp_pha"
    expert_value_keys.append(is_breakdown_monitor_cp_pha)
    expert_values[is_breakdown_monitor_cp_pha] = False

    mean_start_kf_pow                    = "mean_start_kf_pow"
    expert_value_keys.append(mean_start_kf_pow)
    expert_values[mean_start_kf_pow] = "STRING"

    mean_start_kr_pow                    = "mean_start_kr_pow"
    expert_value_keys.append(mean_start_kr_pow)
    expert_values[mean_start_kr_pow] = "STRING"

    mean_start_cf_pow                    = "mean_start_cf_pow"
    expert_value_keys.append(mean_start_cf_pow)
    expert_values[mean_start_cf_pow] = "STRING"

    mean_start_cr_pow                    = "mean_start_cr_pow"
    expert_value_keys.append(mean_start_cr_pow)
    expert_values[mean_start_cr_pow] = "STRING"

    mean_start_cp_pow                    = "mean_start_cp_pow"
    expert_value_keys.append(mean_start_cp_pow)
    expert_values[mean_start_cp_pow] = "STRING"

    mean_start_kf_pha                    = "mean_start_kf_pha"
    expert_value_keys.append(mean_start_kf_pha)
    expert_values[mean_start_kf_pha] = "STRING"

    mean_start_kr_pha                    = "mean_start_kr_pha"
    expert_value_keys.append(vac_pv_val)
    expert_values[vac_pv_val] = "STRING"

    mean_start_cf_pha                    = "mean_start_cf_pha"
    expert_value_keys.append(mean_start_cf_pha)
    expert_values[mean_start_cf_pha] = "STRING"

    mean_start_cr_pha                    = "mean_start_cr_pha"
    expert_value_keys.append(mean_start_cr_pha)
    expert_values[mean_start_cr_pha] = "STRING"

    mean_start_cp_pha                    = "mean_start_cp_pha"
    expert_value_keys.append(mean_start_cp_pha)
    expert_values[mean_start_cp_pha] = "STRING"

    mean_end_kf_pow                      = "mean_end_kf_pow"
    expert_value_keys.append(mean_end_kf_pow)
    expert_values[mean_end_kf_pow] = "STRING"

    mean_end_kr_pow                      = "mean_end_kr_pow"
    expert_value_keys.append(mean_end_kr_pow)
    expert_values[mean_end_kr_pow] = "STRING"

    mean_end_cf_pow                      = "mean_end_cf_pow"
    expert_value_keys.append(mean_end_cf_pow)
    expert_values[mean_end_cf_pow] = "STRING"

    mean_end_cr_pow                      = "mean_end_cr_pow"
    expert_value_keys.append(mean_end_cr_pow)
    expert_values[mean_end_cr_pow] = "STRING"

    mean_end_cp_pow                      = "mean_end_cp_pow"
    expert_value_keys.append(mean_end_cp_pow)
    expert_values[mean_end_cp_pow] = "STRING"

    mean_end_kf_pha                      = "mean_end_kf_pha"
    expert_value_keys.append(mean_end_kf_pha)
    expert_values[mean_end_kf_pha] = "STRING"

    mean_end_kr_pha                      = "mean_end_kr_pha"
    expert_value_keys.append(mean_end_kr_pha)
    expert_values[mean_end_kr_pha] = "STRING"

    expert_value_keys.append(vac_pv_val)
    expert_values[vac_pv_val] = "STRING"

    mean_end_cf_pha                      = "mean_end_cf_pha"
    expert_value_keys.append(mean_end_cf_pha)
    expert_values[mean_end_cf_pha] = "STRING"

    mean_end_cr_pha                      = "mean_end_cr_pha"
    expert_value_keys.append(mean_end_cr_pha)
    expert_values[mean_end_cr_pha] = "STRING"

    mean_end_cp_pha                      = "mean_end_cp_pha"
    expert_value_keys.append(mean_end_cp_pha)
    expert_values[mean_end_cp_pha] = "STRING"

    mask_units_kf_pow                     = "mask_units_kf_pow"
    expert_value_keys.append(mask_units_kf_pow)
    expert_values[mask_units_kf_pow] = "STRING"

    mask_units_kr_pow                     = "mask_units_kr_pow"
    expert_value_keys.append(mask_units_kr_pow)
    expert_values[mask_units_kr_pow] = "STRING"

    mask_units_cf_pow                     = "mask_units_cf_pow"
    expert_value_keys.append(mask_units_cf_pow)
    expert_values[mask_units_cf_pow] = "STRING"

    mask_units_cr_pow                     = "mask_units_cr_pow"
    expert_value_keys.append(mask_units_cr_pow)
    expert_values[mask_units_cr_pow] = "STRING"

    mask_units_cp_pow                     = "mask_units_cp_pow"
    expert_value_keys.append(mask_units_cp_pow)
    expert_values[mask_units_cp_pow] = "STRING"

    mask_units_kf_pha                     = "mask_units_kf_pha"
    expert_value_keys.append(mask_units_kf_pha)
    expert_values[mask_units_kf_pha] = "STRING"

    mask_units_kr_pha                     = "mask_units_kr_pha"
    expert_value_keys.append(mask_units_kr_pha)
    expert_values[mask_units_kr_pha] = "STRING"

    mask_units_cf_pha                     = "mask_units_cf_pha"
    expert_value_keys.append(mask_units_cf_pha)
    expert_values[mask_units_cf_pha] = "STRING"

    mask_units_cr_pha                     = "mask_units_cr_pha"
    expert_value_keys.append(mask_units_cr_pha)
    expert_values[mask_units_cr_pha] = "STRING"

    mask_units_cp_pha                     = "mask_units_cp_pha"
    expert_value_keys.append(mask_units_cp_pha)
    expert_values[mask_units_cp_pha] = "STRING"

    mask_start_kf_pow                    = "mask_start_kf_pow"
    expert_value_keys.append(mask_start_kf_pow)
    expert_values[mask_start_kf_pow] = "STRING"

    mask_start_kr_pow                    = "mask_start_kr_pow"
    expert_value_keys.append(mask_start_kr_pow)
    expert_values[mask_start_kr_pow] = "STRING"

    mask_start_cf_pow                    = "mask_start_cf_pow"
    expert_value_keys.append(mask_start_cf_pow)
    expert_values[mask_start_cf_pow] = "STRING"

    mask_start_cr_pow                    = "mask_start_cr_pow"
    expert_value_keys.append(mask_start_cr_pow)
    expert_values[mask_start_cr_pow] = "STRING"

    mask_start_cp_pow                    = "mask_start_cp_pow"
    expert_value_keys.append(mask_start_cp_pow)
    expert_values[mask_start_cp_pow] = "STRING"

    mask_start_kf_pha                    = "mask_start_kf_pha"
    expert_value_keys.append(mask_start_kf_pha)
    expert_values[mask_start_kf_pha] = "STRING"

    mask_start_kr_pha                    = "mask_start_kr_pha"
    expert_value_keys.append(mask_start_kr_pha)
    expert_values[mask_start_kr_pha] = "STRING"

    mask_start_cf_pha                    = "mask_start_cf_pha"
    expert_value_keys.append(mask_start_cf_pha)
    expert_values[mask_start_cf_pha] = "STRING"

    mask_start_cr_pha                    = "mask_start_cr_pha"
    expert_value_keys.append(mask_start_cr_pha)
    expert_values[mask_start_cr_pha] = "STRING"

    mask_start_cp_pha                    = "mask_start_cp_pha"
    expert_value_keys.append(mask_start_cp_pha)
    expert_values[mask_start_cp_pha] = "STRING"

    mask_end_kf_pow                      = "mask_end_kf_pow"
    expert_value_keys.append(mask_end_kf_pow)
    expert_values[mask_end_kf_pow] = "STRING"

    mask_end_kr_pow                      = "mask_end_kr_pow"
    expert_value_keys.append(mask_end_kr_pow)
    expert_values[mask_end_kr_pow] = "STRING"

    mask_end_cf_pow                      = "mask_end_cf_pow"
    expert_value_keys.append(mask_end_cf_pow)
    expert_values[mask_end_cf_pow] = "STRING"

    mask_end_cr_pow                      = "mask_end_cr_pow"
    expert_value_keys.append(mask_end_cr_pow)
    expert_values[mask_end_cr_pow] = "STRING"

    mask_end_cp_pow                      = "mask_end_cp_pow"
    expert_value_keys.append(mask_end_cp_pow)
    expert_values[mask_end_cp_pow] = "STRING"

    mask_end_kf_pha                      = "mask_end_kf_pha"
    expert_value_keys.append(mask_end_kf_pha)
    expert_values[mask_end_kf_pha] = "STRING"

    mask_end_kr_pha                      = "mask_end_kr_pha"
    expert_value_keys.append(mask_end_kr_pha)
    expert_values[mask_end_kr_pha] = "STRING"

    mask_end_cf_pha                      = "mask_end_cf_pha"
    expert_value_keys.append(mask_end_cf_pha)
    expert_values[mask_end_cf_pha] = "STRING"

    mask_end_cr_pha                      = "mask_end_cr_pha"
    expert_value_keys.append(mask_end_cr_pha)
    expert_values[mask_end_cr_pha] = "STRING"

    mask_end_cp_pha                      = "mask_end_cp_pha"
    expert_value_keys.append(mask_end_cp_pha)
    expert_values[mask_end_cp_pha] = "STRING"

    mask_window_start_kf_pow             = "mask_window_start_kf_pow"
    expert_value_keys.append(mask_window_start_kf_pow)
    expert_values[mask_window_start_kf_pow] = "STRING"

    mask_window_start_kr_pow             = "mask_window_start_kr_pow"
    expert_value_keys.append(mask_window_start_kr_pow)
    expert_values[mask_window_start_kr_pow] = "STRING"

    mask_window_start_cf_pow             = "mask_window_start_cf_pow"
    expert_value_keys.append(mask_window_start_cf_pow)
    expert_values[mask_window_start_cf_pow] = "STRING"

    mask_window_start_cr_pow             = "mask_window_start_cr_pow"
    expert_value_keys.append(mask_window_start_cr_pow)
    expert_values[mask_window_start_cr_pow] = "STRING"

    mask_window_start_cp_pow             = "mask_window_start_cp_pow"
    expert_value_keys.append(mask_window_start_cp_pow)
    expert_values[mask_window_start_cp_pow] = "STRING"

    mask_window_start_kf_pha             = "mask_window_start_kf_pha"
    expert_value_keys.append(mask_window_start_kf_pha)
    expert_values[mask_window_start_kf_pha] = "STRING"

    mask_window_start_kr_pha             = "mask_window_start_kr_pha"
    expert_value_keys.append(mask_window_start_kr_pha)
    expert_values[mask_window_start_kr_pha] = "STRING"

    mask_window_start_cf_pha             = "mask_window_start_cf_pha"
    expert_value_keys.append(mask_window_start_cf_pha)
    expert_values[mask_window_start_cf_pha] = "STRING"

    mask_window_start_cr_pha             = "mask_window_start_cr_pha"
    expert_value_keys.append(mask_window_start_cr_pha)
    expert_values[mask_window_start_cr_pha] = "STRING"

    mask_window_start_cp_pha             = "mask_window_start_cp_pha"
    expert_value_keys.append(mask_window_start_cp_pha)
    expert_values[mask_window_start_cp_pha] = "STRING"

    mask_window_end_kf_pow               = "mask_window_end_kf_pow"
    expert_value_keys.append(mask_window_end_kf_pow)
    expert_values[mask_window_end_kf_pow] = "STRING"

    mask_window_end_kr_pow               = "mask_window_end_kr_pow"
    expert_value_keys.append(mask_window_end_kr_pow)
    expert_values[mask_window_end_kr_pow] = "STRING"

    mask_window_end_cf_pow               = "mask_window_end_cf_pow"
    expert_value_keys.append(mask_window_end_cf_pow)
    expert_values[mask_window_end_cf_pow] = "STRING"

    mask_window_end_cr_pow               = "mask_window_end_cr_pow"
    expert_value_keys.append(mask_window_end_cr_pow)
    expert_values[mask_window_end_cr_pow] = "STRING"

    mask_window_end_cp_pow               = "mask_window_end_cp_pow"
    expert_value_keys.append(mask_window_end_cp_pow)
    expert_values[mask_window_end_cp_pow] = "STRING"

    mask_window_end_kf_pha               = "mask_window_end_kf_pha"
    expert_value_keys.append(mask_window_end_kf_pha)
    expert_values[mask_window_end_kf_pha] = "STRING"

    mask_window_end_kr_pha               = "mask_window_end_kr_pha"
    expert_value_keys.append(mask_window_end_kr_pha)
    expert_values[mask_window_end_kr_pha] = "STRING"

    mask_window_end_cf_pha               = "mask_window_end_cf_pha"
    expert_value_keys.append(mask_window_end_cf_pha)
    expert_values[mask_window_end_cf_pha] = "STRING"

    mask_window_end_cr_pha               = "mask_window_end_cr_pha"
    expert_value_keys.append(mask_window_end_cr_pha)
    expert_values[mask_window_end_cr_pha] = "STRING"

    mask_window_end_cp_pha               = "mask_window_end_cp_pha"
    expert_value_keys.append(vac_pv_val)
    expert_values[vac_pv_val] = "STRING"

    mask_min_kf_pow                      = "mask_min_kf_pow"
    expert_value_keys.append(mask_min_kf_pow)
    expert_values[mask_min_kf_pow] = "STRING"

    mask_min_kr_pow                      = "mask_min_kr_pow"
    expert_value_keys.append(mask_min_kr_pow)
    expert_values[mask_min_kr_pow] = "STRING"

    mask_min_cf_pow                      = "mask_min_cf_pow"
    expert_value_keys.append(mask_min_cf_pow)
    expert_values[mask_min_cf_pow] = "STRING"

    mask_min_cr_pow                      = "mask_min_cr_pow"
    expert_value_keys.append(mask_min_cr_pow)
    expert_values[mask_min_cr_pow] = "STRING"

    mask_min_cp_pow                      = "mask_min_cp_pow"
    expert_value_keys.append(mask_min_cp_pow)
    expert_values[mask_min_cp_pow] = "STRING"

    mask_min_kf_pha                      = "mask_min_kf_pha"
    expert_value_keys.append(mask_min_kf_pha)
    expert_values[mask_min_kf_pha] = "STRING"

    mask_min_kr_pha                      = "mask_min_kr_pha"
    expert_value_keys.append(mask_min_kr_pha)
    expert_values[mask_min_kr_pha] = "STRING"

    mask_min_cf_pha                      = "mask_min_cf_pha"
    expert_value_keys.append(mask_min_cf_pha)
    expert_values[mask_min_cf_pha] = "STRING"

    mask_min_cr_pha                      = "mask_min_cr_pha"
    expert_value_keys.append(mask_min_cr_pha)
    expert_values[mask_min_cr_pha] = "STRING"

    mask_min_cp_pha                      = "mask_min_cp_pha"
    expert_value_keys.append(mask_min_cp_pha)
    expert_values[mask_min_cp_pha] = "STRING"

    num_averages_kf_pow                  = "num_averages_kf_pow"
    expert_value_keys.append(num_averages_kf_pow)
    expert_values[num_averages_kf_pow] = "STRING"

    num_averages_kr_pow                  = "num_averages_kr_pow"
    expert_value_keys.append(num_averages_kr_pow)
    expert_values[num_averages_kr_pow] = "STRING"

    num_averages_cf_pow                  = "num_averages_cf_pow"
    expert_value_keys.append(num_averages_cf_pow)
    expert_values[num_averages_cf_pow] = "STRING"

    num_averages_cr_pow                  = "num_averages_cr_pow"
    expert_value_keys.append(num_averages_cr_pow)
    expert_values[num_averages_cr_pow] = "STRING"

    num_averages_cp_pow                  = "num_averages_cp_pow"
    expert_value_keys.append(num_averages_cp_pow)
    expert_values[num_averages_cp_pow] = "STRING"

    num_averages_kf_pha                  = "num_averages_kf_pha"
    expert_value_keys.append(num_averages_kf_pha)
    expert_values[num_averages_kf_pha] = "STRING"

    num_averages_kr_pha                  = "num_averages_kr_pha"
    expert_value_keys.append(num_averages_kr_pha)
    expert_values[num_averages_kr_pha] = "STRING"

    num_averages_cf_pha                  = "num_averages_cf_pha"
    expert_value_keys.append(num_averages_cf_pha)
    expert_values[num_averages_cf_pha] = "STRING"

    num_averages_cr_pha                  = "num_averages_cr_pha"
    expert_value_keys.append(num_averages_cr_pha)
    expert_values[num_averages_cr_pha] = "STRING"

    num_averages_cp_pha                  = "num_averages_cp_pha"
    expert_value_keys.append(num_averages_cp_pha)
    expert_values[num_averages_cp_pha] = "STRING"

    mask_auto_set_kf_pow                 = "mask_auto_set_kf_pow"
    expert_value_keys.append(mask_auto_set_kf_pow)
    expert_values[mask_auto_set_kf_pow] = "STRING"

    mask_auto_set_kr_pow                 = "mask_auto_set_kr_pow"
    expert_value_keys.append(mask_auto_set_kr_pow)
    expert_values[mask_auto_set_kr_pow] = "STRING"

    mask_auto_set_cf_pow                 = "mask_auto_set_cf_pow"
    expert_value_keys.append(mask_auto_set_cf_pow)
    expert_values[mask_auto_set_cf_pow] = "STRING"

    mask_auto_set_cr_pow                 = "mask_auto_set_cr_pow"
    expert_value_keys.append(mask_auto_set_cr_pow)
    expert_values[mask_auto_set_cr_pow] = "STRING"

    mask_auto_set_cp_pow                 = "mask_auto_set_cp_pow"
    expert_value_keys.append(mask_auto_set_cp_pow)
    expert_values[mask_auto_set_cp_pow] = "STRING"

    mask_auto_set_kf_pha                 = "mask_auto_set_kf_pha"
    expert_value_keys.append(mask_auto_set_kf_pha)
    expert_values[mask_auto_set_kf_pha] = "STRING"

    mask_auto_set_kr_pha                 = "mask_auto_set_kr_pha"
    expert_value_keys.append(mask_auto_set_kr_pha)
    expert_values[mask_auto_set_kr_pha] = "STRING"

    mask_auto_set_cf_pha                 = "mask_auto_set_cf_pha"
    expert_value_keys.append(mask_auto_set_cf_pha)
    expert_values[mask_auto_set_cf_pha] = "STRING"

    mask_auto_set_cr_pha                 = "mask_auto_set_cr_pha"
    expert_value_keys.append(mask_auto_set_cr_pha)
    expert_values[mask_auto_set_cr_pha] = "STRING"

    mask_auto_set_cp_pha                 = "mask_auto_set_cp_pha"
    expert_value_keys.append(mask_auto_set_cp_pha)
    expert_values[mask_auto_set_cp_pha] = "STRING"

    mask_type_kf_pow                     = "mask_type_kf_pow"
    expert_value_keys.append(mask_type_kf_pow)
    expert_values[mask_type_kf_pow] = "STRING"

    mask_type_kr_pow                     = "mask_type_kr_pow"
    expert_value_keys.append(mask_type_kr_pow)
    expert_values[mask_type_kr_pow] = "STRING"

    mask_type_cf_pow                     = "mask_type_cf_pow"
    expert_value_keys.append(mask_type_cf_pow)
    expert_values[mask_type_cf_pow] = "STRING"

    mask_type_cr_pow                     = "mask_type_cr_pow"
    expert_value_keys.append(mask_type_cr_pow)
    expert_values[mask_type_cr_pow] = "STRING"

    mask_type_cp_pow                     = "mask_type_cp_pow"
    expert_value_keys.append(mask_type_cp_pow)
    expert_values[mask_type_cp_pow] = "STRING"

    mask_type_kf_pha                     = "mask_type_kf_pha"
    expert_value_keys.append(mask_type_kf_pha)
    expert_values[mask_type_kf_pha] = "STRING"

    mask_type_kr_pha                     = "mask_type_kr_pha"
    expert_value_keys.append(mask_type_kr_pha)
    expert_values[mask_type_kr_pha] = "STRING"

    mask_type_cf_pha                     = "mask_type_cf_pha"
    expert_value_keys.append(mask_type_cf_pha)
    expert_values[mask_type_cf_pha] = "STRING"

    mask_type_cr_pha                     = "mask_type_cr_pha"
    expert_value_keys.append(mask_type_cr_pha)
    expert_values[mask_type_cr_pha] = "STRING"

    mask_type_cp_pha                     = "mask_type_cp_pha"
    expert_value_keys.append(mask_type_cp_pha)
    expert_values[mask_type_cp_pha] = "STRING"

    mask_level_kf_pow                    = "mask_level_kf_pow"
    expert_value_keys.append(mask_level_kf_pow)
    expert_values[mask_level_kf_pow] = "STRING"

    mask_level_kr_pow                    = "mask_level_kr_pow"
    expert_value_keys.append(mask_level_kr_pow)
    expert_values[mask_level_kr_pow] = "STRING"

    mask_level_cf_pow                    = "mask_level_cf_pow"
    expert_value_keys.append(mask_level_cf_pow)
    expert_values[mask_level_cf_pow] = "STRING"

    mask_level_cr_pow                    = "mask_level_cr_pow"
    expert_value_keys.append(mask_level_cr_pow)
    expert_values[mask_level_cr_pow] = "STRING"

    mask_level_cp_pow                    = "mask_level_cp_pow"
    expert_value_keys.append(mask_level_cp_pow)
    expert_values[mask_level_cp_pow] = "STRING"

    mask_level_kf_pha                    = "mask_level_kf_pha"
    expert_value_keys.append(mask_level_kf_pha)
    expert_values[mask_level_kf_pha] = "STRING"

    mask_level_kr_pha                    = "mask_level_kr_pha"
    expert_value_keys.append(mask_level_kr_pha)
    expert_values[mask_level_kr_pha] = "STRING"

    mask_level_cf_pha                    = "mask_level_cf_pha"
    expert_value_keys.append(mask_level_cf_pha)
    expert_values[mask_level_cf_pha] = "STRING"

    mask_level_cr_pha                    = "mask_level_cr_pha"
    expert_value_keys.append(mask_level_cr_pha)
    expert_values[mask_level_cr_pha] = "STRING"

    mask_level_cp_pha                    = "mask_level_cp_pha"
    expert_value_keys.append(mask_level_cp_pha)
    expert_values[mask_level_cp_pha] = "STRING"




    drop_amplitude_kf_pow                      = "drop_amplitude_kf_pow"
    expert_value_keys.append(drop_amplitude_kf_pow)
    expert_values[drop_amplitude_kf_pow] = "STRING"

    drop_amplitude_kr_pow                      = "drop_amplitude_kr_pow"
    expert_value_keys.append(drop_amplitude_kr_pow)
    expert_values[drop_amplitude_kr_pow] = "STRING"

    drop_amplitude_cf_pow                      = "drop_amplitude_cf_pow"
    expert_value_keys.append(drop_amplitude_cf_pow)
    expert_values[drop_amplitude_cf_pow] = "STRING"

    drop_amplitude_cr_pow                      = "drop_amplitude_cr_pow"
    expert_value_keys.append(drop_amplitude_cr_pow)
    expert_values[drop_amplitude_cr_pow] = "STRING"

    drop_amplitude_cp_pow                      = "drop_amplitude_cp_pow"
    expert_value_keys.append(drop_amplitude_cp_pow)
    expert_values[drop_amplitude_cp_pow] = "STRING"

    drop_amplitude_kf_pha                      = "drop_amplitude_kf_pha"
    expert_value_keys.append(drop_amplitude_kf_pha)
    expert_values[drop_amplitude_kf_pha] = "STRING"

    drop_amplitude_kr_pha                      = "drop_amplitude_kr_pha"
    expert_value_keys.append(drop_amplitude_kr_pha)
    expert_values[drop_amplitude_kr_pha] = "STRING"

    drop_amplitude_cf_pha                      = "drop_amplitude_cf_pha"
    expert_value_keys.append(drop_amplitude_cf_pha)
    expert_values[drop_amplitude_cf_pha] = "STRING"

    drop_amplitude_cr_pha                      = "drop_amplitude_cr_pha"
    expert_value_keys.append(drop_amplitude_cr_pha)
    expert_values[drop_amplitude_cr_pha] = "STRING"

    drop_amplitude_cp_pha                      = "drop_amplitude_cp_pha"
    expert_value_keys.append(drop_amplitude_cp_pha)
    expert_values[drop_amplitude_cp_pha] = "STRING"

















    phase_end_by_power_kf_pow             = "phase_end_by_power_kf_pow"
    expert_value_keys.append(phase_end_by_power_kf_pow)
    expert_values[phase_end_by_power_kf_pow] = "STRING"

    phase_end_by_power_kr_pow             = "phase_end_by_power_kr_pow"
    expert_value_keys.append(phase_end_by_power_kr_pow)
    expert_values[phase_end_by_power_kr_pow] = "STRING"

    phase_end_by_power_cf_pow             = "phase_end_by_power_cf_pow"
    expert_value_keys.append(phase_end_by_power_cf_pow)
    expert_values[phase_end_by_power_cf_pow] = "STRING"

    phase_end_by_power_cr_pow             = "phase_end_by_power_cr_pow"
    expert_value_keys.append(phase_end_by_power_cr_pow)
    expert_values[phase_end_by_power_cr_pow] = "STRING"

    phase_end_by_power_cp_pow             = "phase_end_by_power_cp_pow"
    expert_value_keys.append(phase_end_by_power_cp_pow)
    expert_values[phase_end_by_power_cp_pow] = "STRING"

    phase_end_by_power_kf_pha             = "phase_end_by_power_kf_pha"
    expert_value_keys.append(phase_end_by_power_kf_pha)
    expert_values[phase_end_by_power_kf_pha] = "STRING"

    phase_end_by_power_kr_pha             = "phase_end_by_power_kr_pha"
    expert_value_keys.append(phase_end_by_power_kr_pha)
    expert_values[phase_end_by_power_kr_pha] = "STRING"

    phase_end_by_power_cf_pha             = "phase_end_by_power_cf_pha"
    expert_value_keys.append(phase_end_by_power_cf_pha)
    expert_values[phase_end_by_power_cf_pha] = "STRING"

    phase_end_by_power_cr_pha             = "phase_end_by_power_cr_pha"
    expert_value_keys.append(phase_end_by_power_cr_pha)
    expert_values[phase_end_by_power_cr_pha] = "STRING"

    phase_end_by_power_cp_pha             = "phase_end_by_power_cp_pha"
    expert_value_keys.append(phase_end_by_power_cp_pha)
    expert_values[phase_end_by_power_cp_pha] = "STRING"









    mask_end_power_kf_pow                = "mask_end_power_kf_pow"
    expert_value_keys.append(mask_end_power_kf_pow)
    expert_values[mask_end_power_kf_pow] = "STRING"

    mask_end_power_kr_pow                = "mask_end_power_kr_pow"
    expert_value_keys.append(mask_end_power_kr_pow)
    expert_values[mask_end_power_kr_pow] = "STRING"

    mask_end_power_cf_pow                = "mask_end_power_cf_pow"
    expert_value_keys.append(mask_end_power_cf_pow)
    expert_values[mask_end_power_cf_pow] = "STRING"

    mask_end_power_cr_pow                = "mask_end_power_cr_pow"
    expert_value_keys.append(mask_end_power_cr_pow)
    expert_values[mask_end_power_cr_pow] = "STRING"

    mask_end_power_cp_pow                = "mask_end_power_cp_pow"
    expert_value_keys.append(mask_end_power_cp_pow)
    expert_values[mask_end_power_cp_pow] = "STRING"

    mask_end_power_kf_pha                = "mask_end_power_kf_pha"
    expert_value_keys.append(mask_end_power_kf_pha)
    expert_values[mask_end_power_kf_pha] = "STRING"

    mask_end_power_kr_pha                = "mask_end_power_kr_pha"
    expert_value_keys.append(mask_end_power_kr_pha)
    expert_values[mask_end_power_kr_pha] = "STRING"

    mask_end_power_cf_pha                = "mask_end_power_cf_pha"
    expert_value_keys.append(mask_end_power_cf_pha)
    expert_values[mask_end_power_cf_pha] = "STRING"

    mask_end_power_cr_pha                = "mask_end_power_cr_pha"
    expert_value_keys.append(mask_end_power_cr_pha)
    expert_values[mask_end_power_cr_pha] = "STRING"

    mask_end_power_cp_pha                = "mask_end_power_cp_pha"
    expert_value_keys.append(mask_end_power_cp_pha)
    expert_values[mask_end_power_cp_pha] = "STRING"





    saved_on_breakdown_event_kf_pow      = "saved_on_breakdown_event_kf_pow"
    expert_value_keys.append(saved_on_breakdown_event_kf_pow)
    expert_values[saved_on_breakdown_event_kf_pow] = "STRING"

    saved_on_breakdown_event_kr_pow      = "saved_on_breakdown_event_kr_pow"
    expert_value_keys.append(saved_on_breakdown_event_kr_pow)
    expert_values[saved_on_breakdown_event_kr_pow] = "STRING"

    saved_on_breakdown_event_cf_pow      = "saved_on_breakdown_event_cf_pow"
    expert_value_keys.append(saved_on_breakdown_event_cf_pow)
    expert_values[saved_on_breakdown_event_cf_pow] = "STRING"

    saved_on_breakdown_event_cr_pow      = "saved_on_breakdown_event_cr_pow"
    expert_value_keys.append(saved_on_breakdown_event_cr_pow)
    expert_values[saved_on_breakdown_event_cr_pow] = "STRING"

    saved_on_breakdown_event_cp_pow      = "saved_on_breakdown_event_cp_pow"
    expert_value_keys.append(saved_on_breakdown_event_cp_pow)
    expert_values[saved_on_breakdown_event_cp_pow] = "STRING"

    saved_on_breakdown_event_kf_pha      = "saved_on_breakdown_event_kf_pha"
    expert_value_keys.append(saved_on_breakdown_event_kf_pha)
    expert_values[saved_on_breakdown_event_kf_pha] = "STRING"

    saved_on_breakdown_event_kr_pha      = "saved_on_breakdown_event_kr_pha"
    expert_value_keys.append(saved_on_breakdown_event_kr_pha)
    expert_values[saved_on_breakdown_event_kr_pha] = "STRING"

    saved_on_breakdown_event_cf_pha      = "saved_on_breakdown_event_cf_pha"
    expert_value_keys.append(saved_on_breakdown_event_cf_pha)
    expert_values[saved_on_breakdown_event_cf_pha] = "STRING"

    saved_on_breakdown_event_cr_pha      = "saved_on_breakdown_event_cr_pha"
    expert_value_keys.append(saved_on_breakdown_event_cr_pha)
    expert_values[saved_on_breakdown_event_cr_pha] = "STRING"

    saved_on_breakdown_event_cp_pha      = "saved_on_breakdown_event_cp_pha"
    expert_value_keys.append(saved_on_breakdown_event_cp_pha)
    expert_values[saved_on_breakdown_event_cp_pha] = "STRING"

    saved_on_vac_spike_kf_pow            = "saved_on_vac_spike_kf_pow"
    expert_value_keys.append(saved_on_vac_spike_kf_pow)
    expert_values[saved_on_vac_spike_kf_pow] = "STRING"

    saved_on_vac_spike_kr_pow            = "saved_on_vac_spike_kr_pow"
    expert_value_keys.append(saved_on_vac_spike_kr_pow)
    expert_values[saved_on_vac_spike_kr_pow] = "STRING"

    saved_on_vac_spike_cf_pow            = "saved_on_vac_spike_cf_pow"
    expert_value_keys.append(saved_on_vac_spike_cf_pow)
    expert_values[saved_on_vac_spike_cf_pow] = "STRING"

    saved_on_vac_spike_cr_pow            = "saved_on_vac_spike_cr_pow"
    expert_value_keys.append(saved_on_vac_spike_cr_pow)
    expert_values[saved_on_vac_spike_cr_pow] = "STRING"

    saved_on_vac_spike_cp_pow            = "saved_on_vac_spike_cp_pow"
    expert_value_keys.append(saved_on_vac_spike_cp_pow)
    expert_values[saved_on_vac_spike_cp_pow] = "STRING"

    saved_on_vac_spike_kf_pha            = "saved_on_vac_spike_kf_pha"
    expert_value_keys.append(saved_on_vac_spike_kf_pha)
    expert_values[saved_on_vac_spike_kf_pha] = "STRING"

    saved_on_vac_spike_kr_pha            = "saved_on_vac_spike_kr_pha"
    expert_value_keys.append(saved_on_vac_spike_kr_pha)
    expert_values[saved_on_vac_spike_kr_pha] = "STRING"

    saved_on_vac_spike_cf_pha            = "saved_on_vac_spike_cf_pha"
    expert_value_keys.append(saved_on_vac_spike_cf_pha)
    expert_values[saved_on_vac_spike_cf_pha] = "STRING"

    saved_on_vac_spike_cr_pha            = "saved_on_vac_spike_cr_pha"
    expert_value_keys.append(saved_on_vac_spike_cr_pha)
    expert_values[saved_on_vac_spike_cr_pha] = "STRING"

    saved_on_vac_spike_cp_pha            = "saved_on_vac_spike_cp_pha"
    expert_value_keys.append(saved_on_vac_spike_cp_pha)
    expert_values[saved_on_vac_spike_cp_pha] = "STRING"

    drop_amp_on_bd_kf_pow                = "drop_amp_on_bd_kf_pow"
    expert_value_keys.append(drop_amp_on_bd_kf_pow)
    expert_values[drop_amp_on_bd_kf_pow] = "STRING"

    drop_amp_on_bd_kr_pow                = "drop_amp_on_bd_kr_pow"
    expert_value_keys.append(drop_amp_on_bd_kr_pow)
    expert_values[drop_amp_on_bd_kr_pow] = "STRING"

    drop_amp_on_bd_cf_pow                = "drop_amp_on_bd_cf_pow"
    expert_value_keys.append(drop_amp_on_bd_cf_pow)
    expert_values[drop_amp_on_bd_cf_pow] = "STRING"

    drop_amp_on_bd_cr_pow                = "drop_amp_on_bd_cr_pow"
    expert_value_keys.append(drop_amp_on_bd_cr_pow)
    expert_values[drop_amp_on_bd_cr_pow] = "STRING"


    drop_amp_on_bd_cp_pow                = "drop_amp_on_bd_cp_pow"
    expert_value_keys.append(drop_amp_on_bd_cp_pow)
    expert_values[drop_amp_on_bd_cp_pow] = "STRING"

    drop_amp_on_bd_kf_pha                = "drop_amp_on_bd_kf_pha"
    expert_value_keys.append(drop_amp_on_bd_kf_pha)
    expert_values[drop_amp_on_bd_kf_pha] = "STRING"

    drop_amp_on_bd_kr_pha                = "drop_amp_on_bd_kr_pha"
    expert_value_keys.append(drop_amp_on_bd_kr_pha)
    expert_values[drop_amp_on_bd_kr_pha] = "STRING"

    drop_amp_on_bd_cf_pha                = "drop_amp_on_bd_cf_pha"
    expert_value_keys.append(drop_amp_on_bd_cf_pha)
    expert_values[drop_amp_on_bd_cf_pha] = "STRING"

    drop_amp_on_bd_cr_pha                = "drop_amp_on_bd_cr_pha"
    expert_value_keys.append(drop_amp_on_bd_cr_pha)
    expert_values[drop_amp_on_bd_cr_pha] = "STRING"

    drop_amp_on_bd_cp_pha                = "drop_amp_on_bd_cp_pha"
    expert_value_keys.append(drop_amp_on_bd_cp_pha)
    expert_values[drop_amp_on_bd_cp_pha] = "STRING"

    streak_kf_pow                        = "streak_kf_pow"
    expert_value_keys.append(streak_kf_pow)
    expert_values[streak_kf_pow] = "STRING"

    streak_kr_pow                        = "streak_kr_pow"
    expert_value_keys.append(streak_kr_pow)
    expert_values[streak_kr_pow] = "STRING"

    streak_cf_pow                        = "streak_cf_pow"
    expert_value_keys.append(streak_cf_pow)
    expert_values[streak_cf_pow] = "STRING"

    streak_cr_pow                        = "streak_cr_pow"
    expert_value_keys.append(streak_cr_pow)
    expert_values[streak_cr_pow] = "STRING"

    streak_cp_pow                        = "streak_cp_pow"
    expert_value_keys.append(streak_cp_pow)
    expert_values[streak_cp_pow] = "STRING"

    streak_kf_pha                        = "streak_kf_pha"
    expert_value_keys.append(streak_kf_pha)
    expert_values[streak_kf_pha] = "STRING"

    streak_kr_pha                        = "streak_kr_pha"
    expert_value_keys.append(streak_kr_pha)
    expert_values[streak_kr_pha] = "STRING"

    streak_cf_pha                        = "streak_cf_pha"
    expert_value_keys.append(streak_cf_pha)
    expert_values[streak_cf_pha] = "STRING"

    streak_cr_pha                        = "streak_cr_pha"
    expert_value_keys.append(streak_cr_pha)
    expert_values[streak_cr_pha] = "STRING"

    streak_cp_pha                        = "streak_cp_pha"
    expert_value_keys.append(streak_cp_pha)
    expert_values[streak_cp_pha] = "STRING"

    breakdown_rate_aim_val               = "breakdown_rate_aim_val"
    expert_value_keys.append(breakdown_rate_aim_val)
    expert_values[breakdown_rate_aim_val] = "STRING"

    expected_daq_rep_rate_val            = "expected_daq_rep_rate_val"
    expert_value_keys.append(expected_daq_rep_rate_val)
    expert_values[expected_daq_rep_rate_val] = "STRING"

    daq_rep_rate_error_val               = "daq_rep_rate_error_val"
    expert_value_keys.append(daq_rep_rate_error_val)
    expert_values[daq_rep_rate_error_val] = "STRING"

    number_of_pulses_in_history_val      = "number_of_pulses_in_history_val"
    expert_value_keys.append(number_of_pulses_in_history_val)
    expert_values[number_of_pulses_in_history_val] = "STRING"

    trace_buffer_size_val                = "trace_buffer_size_val"
    expert_value_keys.append(trace_buffer_size_val)
    expert_values[trace_buffer_size_val] = "STRING"

    default_pulse_count_val              = "default_pulse_count_val"
    expert_value_keys.append(default_pulse_count_val)
    expert_values[default_pulse_count_val] = "STRING"

    default_amp_increase_val             = "default_amp_increase_val"
    expert_value_keys.append(default_amp_increase_val)
    expert_values[default_amp_increase_val] = "STRING"

    max_amp_increase_val                 = "max_amp_increase_val"
    expert_value_keys.append(max_amp_increase_val)
    expert_values[max_amp_increase_val] = "STRING"

    num_fit_points_val                   = "num_fit_points_val"
    expert_value_keys.append(num_fit_points_val)
    expert_values[num_fit_points_val] = "STRING"

    active_power_val                     = "active_power_val"
    expert_value_keys.append(active_power_val)
    expert_values[active_power_val] = dummy_float

    num_future_traces_val                = "num_future_traces_val"
    expert_value_keys.append(num_future_traces_val)
    expert_values[num_future_traces_val] = dummy_int

    keep_valve_open_val                  = "keep_valve_open_val"
    expert_value_keys.append(keep_valve_open_val)
    expert_values[keep_valve_open_val] = True


    keep_valve_open_valves_val = "keep_valve_open_valves_val"
    expert_value_keys.append(keep_valve_open_valves_val)
    expert_values[keep_valve_open_valves_val] = True

    default_pulse_count_val = "default_pulse_count_val"
    expert_value_keys.append(default_pulse_count_val)
    expert_values[default_pulse_count_val] = True

    min_cool_down_time_val = "min_cool_down_time_val"
    expert_value_keys.append(min_cool_down_time_val)
    expert_values[min_cool_down_time_val] = True

    trace_buffer_size_val = "trace_buffer_size_val"
    expert_value_keys.append(trace_buffer_size_val)
    expert_values[trace_buffer_size_val] = True

    default_amp_increase_val = "default_amp_increase_val"
    expert_value_keys.append(default_amp_increase_val)
    expert_values[default_amp_increase_val] = True

    max_amp_increase_val = "max_amp_increase_val"
    expert_value_keys.append(max_amp_increase_val)
    expert_values[max_amp_increase_val] = True



















#     # these functions move up and down the ramp curve
#     # and set the next increase, decrease values,
#     # if ramping down delete previous entries that are above our new working point
#     def move_up_ramp_curve(self):
#         self.move_ramp_index(1)
#
#     def move_down_ramp_curve(self):
#         self.clear_last_sp_history()
#         self.move_ramp_index(-1)
#
#     def clear_last_sp_history(self):
#         #print('clear_last_sp_history')
#         if len(dat.rf_condition_data_base.amp_sp_history) > 1:
#             # delete last entry from amp_history
#             self.logger.message('clear_last_sp_history for values greater than ' +str(dat.rf_condition_data_base.values[dat.last_sp_above_100]))
#             dat.rf_condition_data_base.amp_sp_history  = [i for i in dat.rf_condition_data_base.amp_sp_history if i <= dat.rf_condition_data_base.values[dat.last_sp_above_100] ]
#
#             #dat.rf_condition_data_base.amp_sp_history = dat.rf_condition_data_base.amp_sp_history[:-1]
#             self.logger.message('New amp_sp_history[-1] = ' + str(dat.rf_condition_data_base.amp_sp_history[-1]), True)
#         else:
#             self.logger.message('length of amp_sp_history[-1] <=  1', True)
#         #
#         # could maybe do this more clever like
#         # if we only keep mean values, just delete last entry in mean pwr vs amp_sp data dicts
#         dat.rf_condition_data_base.sp_pwr_hist = [x for x in dat.rf_condition_data_base.sp_pwr_hist if x[0] < dat.rf_condition_data_base.amp_sp_history[-1] ]
#         # delete entries from amp_pwr_mean_data
#         dat.rf_condition_data_base.amp_pwr_mean_data = {key: value for key, value in
#                                                         dat.rf_condition_data_base.amp_pwr_mean_data.iteritems()
#                      if key > dat.rf_condition_data_base.amp_sp_history[-1]}
#
#
#     def move_ramp_index(self,val):
#         self.logger.header('move_ramp_index', True)
#         self.values[dat.current_ramp_index] += val
#         if self.values[dat.current_ramp_index] < 0:
#             self.values[dat.current_ramp_index] = 0
#         elif self.values[dat.current_ramp_index] > self.ramp_max_index:
#             self.values[dat.current_ramp_index] = self.ramp_max_index
#         self.set_ramp_values()
#
#     def set_ramp_values(self):
#         dat.rf_condition_data_base.values[dat.required_pulses] = ramp[dat.rf_condition_data_base.values[dat.current_ramp_index]][0]
#         dat.rf_condition_data_base.values[dat.next_power_increase] = float(ramp[dat.rf_condition_data_base.values[dat.current_ramp_index]][1])
#
#         # force the number of pulses to next step to be 500, DEBUG TESTING MODE ONLY!!!!!!!
#         #dat.rf_condition_data_base.values[dat.required_pulses] = 1000
#
#         # self.set_next_sp_decrease()
#         a = dat.rf_condition_data_base.values[dat.next_sp_decrease]
#         if len(dat.rf_condition_data_base.amp_sp_history) > 1:
#             dat.rf_condition_data_base.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]
#         else:
#             self.logger.message('Warning len(dat.rf_condition_data_base.amp_sp_history) not > 1')
#             dat.rf_condition_data_base.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[0]
#
#         if dat.rf_condition_data_base.values[dat.next_sp_decrease] < a:
#             self.logger.message('Changed next_sp_decrease from ' + str(a) + ' to ' + str(
#                 dat.rf_condition_data_base.values[dat.next_sp_decrease]), True)
#         else:
#             self.logger.message('!!!ERROR!!! next_sp_decrease is NOT less than previous. (' + str(a) + ' !< ' + str(
#                 dat.rf_condition_data_base.values[dat.next_sp_decrease]), True)
#
#         self.logger.header( self.my_name + ' set_ramp_values ', True)
#         self.logger.message(['current ramp index   = ' + str(dat.rf_condition_data_base.values[dat.current_ramp_index]),
#                              'next required pulses = ' + str(dat.rf_condition_data_base.values[dat.required_pulses]),
#                              'next power increase  = ' + str(dat.rf_condition_data_base.values[dat.next_power_increase]),
#                              'next sp decrease     = ' + str(dat.rf_condition_data_base.values[dat.next_sp_decrease])],True)
#
#     def get_new_sp(self):
#         return self.get_new_set_point( self.get_next_power())
# #
#
#     def get_previous_set_points(self):
#         data = dat.rf_condition_data_base.amp_vs_kfpow_running_stat
#         current_sp = dat.rf_condition_data_base.values[dat.amp_sp]
#         previous_sp = sorted(i for i in data.keys() if i <= current_sp)
#
#         if len(previous_sp) > self.llrf_config['NUM_SET_POINTS_TO_FIT']:
#             print ('get_previous_set_points found at least ' + str(self.llrf_config['NUM_SET_POINTS_TO_FIT']) + ' values in set-point history',
#                    previous_sp[-self.llrf_config['NUM_SET_POINTS_TO_FIT']:])
#             return previous_sp[-self.llrf_config['NUM_SET_POINTS_TO_FIT']:]
#
#         #print ('get_previous_set_points',previous_sp)
#         return previous_sp
#
#     def get_new_set_point(self, req_pwr_inc):
#         predicted_sp = None
#         m = 0
#         self.logger.header( self.my_name + ' running  get_new_set_point() ', True)
#         # ref  to values dictionary
#         values = dat.rf_condition_data_base.values
#         # ref to amp_vs_kfpow_running_stat
#         kfpowdata = data = dat.rf_condition_data_base.amp_vs_kfpow_running_stat
#         current_sp =  values[dat.amp_sp]
#         #
#         # we have to get the 3 set-points less than the current one (if they exist)
#         sp_to_fit = self.get_previous_set_points()
#
#         self.current_power = int(kfpowdata[current_sp][1])
#         self.requested_power = int(self.current_power + req_pwr_inc)
#
#         if len(sp_to_fit) > 1:
#             self.previous_power = int(kfpowdata[sp_to_fit[-2]][1])
#
#         if len(sp_to_fit) == self.llrf_config['NUM_SET_POINTS_TO_FIT']: # MAGIC_STRING,
#             # store previous values for Straight Line Fit
#             values[dat.old_c] = values[dat.c]
#             values[dat.old_m] = values[dat.m]
#             values[dat.old_x_max] = values[dat.x_max]
#             values[dat.old_x_min] = values[dat.x_min]
#             values[dat.old_y_max] = values[dat.y_max]
#             values[dat.old_y_min] = values[dat.y_min]
#             #
#             # fit with np.polyfit, weighted
#             x_tofit = np.array(sp_to_fit)
#             y_tofit = np.array([data[i][1] for i in sp_to_fit])
#
#             #print('fitting data x_tofit = ', x_tofit)
#             #print('fitting data y_tofit = ', y_tofit)
#
#             # we store the variances of the KFP, fitting requires sigmas
#             # this SHOULD be err = np.sqrt([data[i][2] / (data[i][0] -1 ) for i in x])
#             # but we ignore the minus 1 incase we get a div by zero
#
#             err_tofit = np.sqrt([ data[i][2] / (data[i][0] ) for i in sp_to_fit])
#
#             m, c = np.polyfit(x_tofit, y_tofit, 1, rcond=None, full=False, w=err_tofit)
#
#
#             # get next values for Straight Line Fit
#             values[dat.x_max] = sp_to_fit[-1]
#             values[dat.x_min] = sp_to_fit[0]
#             # get next values for Straight Line Fit
#             values[dat.y_max] = m * sp_to_fit[-1] + c
#             values[dat.y_min] = m * sp_to_fit[0] + c
#             values[dat.c] = c
#             values[dat.m] = m
#
#             predicted_sp = int((self.requested_power - c)/m)
#             #print(m,c,self.current_power,values[dat.last_mean_power], req_pwr_inc )
#
#             self.logger.message('x Points to fit = ' + np.array_str(x_tofit, max_line_width =500), True)
#             self.logger.message('y Points to fit = ' + np.array_str(y_tofit, max_line_width =500), True)
#             self.logger.message('y Points errors = ' + np.array_str(err_tofit, max_line_width =500), True)
#             self.logger.message('Fit m , c = ' + str(m) + ", " +  str(c), True)
#
#             self.logger.message('current   sp/W  = ' + str(current_sp)   + " / " + str(self.current_power), True)
#             self.logger.message('predict   sp/W  = ' + str(predicted_sp) + " / " + str(self.requested_power), True)
#             self.logger.message('new delta sp/W  = ' + str(predicted_sp - current_sp) + " / " +
#                                 str(self.requested_power-self.current_power) + ' (' + str(
#                                         req_pwr_inc) +')',True)
#
#             self.logger.message('last delta sp/W  = ' + str(current_sp - sp_to_fit[-2]) + " / " +
#                                 str(self.current_power -self.previous_power),True)
#         # WHAT TO RETURN
#
#         return_value = 0
#         if predicted_sp < current_sp:
#             self.logger.message('Predicted sp is less than current_sp! returning current_sp + ' + str(self.llrf_config['DEFAULT_RF_INCREASE_LEVEL']) , True)
#             return_value = current_sp + self.llrf_config['DEFAULT_RF_INCREASE_LEVEL']
#
#         elif m <= 0:
#             self.logger.message('Predicted negative gradient, returning current_sp + ' + str(self.llrf_config['DEFAULT_RF_INCREASE_LEVEL']),True)
#             self.logger.message('current sp/W  = ' + str(current_sp) + " / " + str(self.current_power), True)
#             return_value = current_sp + self.llrf_config['DEFAULT_RF_INCREASE_LEVEL']
#
#         elif predicted_sp - current_sp > self.llrf_config['MAX_DELTA_AMP_SP']:# MAGIC_STRING
#             self.logger.message('Predicted SP > ' + str(self.llrf_config['MAX_DELTA_AMP_SP']) + ', too high, returning current_sp + ' + str(self.llrf_config['MAX_DELTA_AMP_SP']) ,True)
#             return_value = current_sp + self.llrf_config['MAX_DELTA_AMP_SP']
#
#         elif predicted_sp == current_sp:
#             self.logger.message('Predicted sp == current_sp, returning current_sp + ' + str(self.llrf_config['DEFAULT_RF_INCREASE_LEVEL']),True)
#             return_value = predicted_sp + self.llrf_config['DEFAULT_RF_INCREASE_LEVEL']
#
#         elif predicted_sp is None:
#             self.logger.message('Not Enough KFP data to fit, returning current_sp + ' + str(self.llrf_config['DEFAULT_RF_INCREASE_LEVEL']), True)
#             self.logger.message('current sp/W  = ' + str(current_sp) + " / " + str(self.current_power), True)
#             return_value = current_sp + self.llrf_config['DEFAULT_RF_INCREASE_LEVEL']
#         else:
#             return_value = predicted_sp
#         self.logger.message('get_new_set_point, returning ' + str(return_value), True)
#         return return_value
#
#     def init_after_config_read(self):
#         if self.llrf_config is not None:
#             self.get_pulse_count_breakdown_log()
#             dat.rf_condition_data_base.amp_vs_kfpow_running_stat = self.logger.get_amp_power_log()
#             print 'get_amp_power_log results'
#             #for key, value in dat.rf_condition_data_base.amp_vs_kfpow_running_stat.iteritems():
#             #    print key
#             #    print value
#
#             self.values[dat.power_aim] = self.llrf_config['POWER_AIM']
#             ##elf.values[dat.pulse_length_start] = self.llrf_config['PULSE_LENGTH_START']
#             self.values[dat.pulse_length_aim] = self.llrf_config['PULSE_LENGTH_AIM']
#             self.values[dat.pulse_length_aim_error] = self.llrf_config['PULSE_LENGTH_AIM_ERROR']
#
#             self.values[dat.pulse_length_min] = self.llrf_config['PULSE_LENGTH_AIM'] - self.llrf_config['PULSE_LENGTH_AIM_ERROR']
#             self.values[dat.pulse_length_max] = self.llrf_config['PULSE_LENGTH_AIM'] + self.llrf_config['PULSE_LENGTH_AIM_ERROR']
#
#
#             #self.values[dat.pulse_length_step] = self.llrf_config['PULSE_LENGTH_STEP']
#             self.values[dat.breakdown_rate_aim] = self.llrf_config['BREAKDOWN_RATE_AIM']
#
#             self.values[dat.llrf_DAQ_rep_rate_aim] = self.llrf_config['RF_REPETITION_RATE']
#             self.values[dat.llrf_DAQ_rep_rate_max] = self.llrf_config['RF_REPETITION_RATE'] + self.llrf_config['RF_REPETITION_RATE_ERROR']
#             self.values[dat.llrf_DAQ_rep_rate_min] = self.llrf_config['RF_REPETITION_RATE'] - \
#                                                      self.llrf_config['RF_REPETITION_RATE_ERROR']
#             self.logger.header(self.my_name + ' init_after_config_read')
#             self.logger.message([dat.pulse_length_aim + ' ' + str(self.values[dat.pulse_length_aim]),
#             dat.pulse_length_aim_error + ' ' + str(self.values[dat.pulse_length_aim_error]),
#             dat.pulse_length_min + ' ' + str(self.values[dat.pulse_length_min]),
#             dat.pulse_length_max + ' ' + str(self.values[dat.pulse_length_max])
#                                  ])
#
#
#
#
#     def update_last_million_pulse_log(self):
#         # add the next set of values to the last_million_log
#         dat.rf_condition_data_base.last_million_log.append([
#             self.values[dat.pulse_count],
#             self.values[dat.breakdown_count],
#             self.values[dat.current_ramp_index],
#             self.values[dat.pulse_length]]
#         )
#         # self.logger.message('update_last_million_pulse_log ' +
#         #                     str(self.values[dat.pulse_count]) + ' ' +
#         #                     str( self.values[dat.breakdown_count]) + ' ' +
#         #                     str(self.values[dat.current_ramp_index]) + ' ' +
#         #                     str(self.values[dat.pulse_length]),True)
#         while dat.rf_condition_data_base.last_million_log[-1][0] - dat.rf_condition_data_base.last_million_log[0][0] \
#                 > \
#               self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']:
#             # temp =  ', '.join(str(x) for x in dat.rf_condition_data_base.last_million_log[0])
#             # self.logger.message('deleting ' + temp + ' from last_million_log',False)
#             dat.rf_condition_data_base.last_million_log.pop(0)
#         self.update_breakdown_stats()
#         #raw_input()
#
#

#
#
#
#
#
#
#
#     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     # MEH, processing of log file basically done by hand
#     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     def get_pulse_count_breakdown_log(self):
#         # this is aaay too complicated ... (but its processing the data in tow ways, once by amp_setpioint
#         # and once by pusle count, it generates to main lists:
#         # 1) dat.rf_condition_data_base.amp_sp_history
#         #       Sorted by amp_setpoint
#         #       Used to define how to ramp up adn down
#         # 2) dat.rf_condition_data_base.last_million_log
#         #       Sorted by pulse count
#         #       used to define the Breakdown Rate etc.
#         #
#         # get the pulse_break_down_log entries from file
#         pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
#         #
#         # based on the log file we set active pulse count total,
#         # the starting point is the one before the last entry  (WHY???? DJS Jan 2019)
#         #
#         # FIRST:
#         # save the last entry, log_pulse_count and breakdown count
#         # keep this seperate as pulse_count will get overwritten!!
#         #
#         self.values[dat.log_pulse_count] = int(pulse_break_down_log[-1][0])
#         self.values[dat.breakdown_count] = int(pulse_break_down_log[-1][1])
#         #
#         # first amp is the second to last one in log file (WHY???? DJS Jan 2019,
#         # maybe we should ramp to this value on startup)
#         # remove values greater than than last_amp_sp_in_file
#         #
#         last_amp_sp_in_file = int(pulse_break_down_log[-1][2])
#         indices_to_remove = []
#         index_to_remove = 0
#         for entry in pulse_break_down_log:
#             if entry[2] >= last_amp_sp_in_file:
#                 indices_to_remove.append(index_to_remove)
#             index_to_remove += 1
#         #
#         # delete index_to_remove from pulse_break_down_log
#         # https://stackoverflow.com/questions/11303225/how-to-remove-multiple-indexes-from-a-list-at-the-same-time
#         for index in sorted(indices_to_remove, reverse=True):
#             del pulse_break_down_log[index]
#         #
#         # sort the list by setpoint (part 2) then pulse_count (part 0)
#         sorted_pulse_break_down_log_1 = sorted(pulse_break_down_log, key=lambda x: (x[2], x[0]))
#         #
#         # As we have all the time in the world...
#         # make another list, ampSP_sorted_pulse_break_down_log, this has NO Setpoints = the final sp in sorted_pulse_break_down_log_1
#         # the final entry in sorted_pulse_break_down_log_1 is the sp point with highest pulse count
#         ampSP_sorted_pulse_break_down_log = []
#         last_i = sorted_pulse_break_down_log_1[-1]
#         #
#         #
#         for i in sorted_pulse_break_down_log_1:
#             if last_i[2] == i[2]:
#                 pass
#             else:
#                 ampSP_sorted_pulse_break_down_log.append(i)
#             last_i = i
#         #
#         #
#         # next we must insert the data in to the main data values dictionary
#         #
#         # set the ramp index
#         self.values[dat.current_ramp_index] = ampSP_sorted_pulse_break_down_log[-1][3]
#         #
#         # amp_setpoint history history, THIS is used to decide where to ramp down,
#         # and what amp_setpoint to use in fitting when ramping-up
#         # write this list to the main log
#         dat.rf_condition_data_base.amp_sp_history = [int(i[2]) for i in ampSP_sorted_pulse_break_down_log ]
#         self.logger.header(self.my_name + ' amp SP history on startup ', True)
#         to_write = []
#         for value in dat.rf_condition_data_base.amp_sp_history:
#             to_write.append(str(value))
#         self.logger.message(','.join(to_write),True)
#         #
#         # The next amp_setpoint to set
#         self.values[dat.log_amp_set] = dat.rf_condition_data_base.amp_sp_history[-1]
#         #
#         # the next amp_setpoint on ramp_down
#         self.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]
#         #
#         # pulse length (logged but not used as pulse_length is now defined by the pulse shaping table)
#         self.values[dat.log_pulse_length] = float(ampSP_sorted_pulse_break_down_log[-1][4]) / float(1000.0)# warning UNIT
#         self.llrf_config['PULSE_LENGTH_START'] = self.values[dat.log_pulse_length]
#         #
#         # set the number of pulses required at this step to the defualt (will be checked later)
#         self.values[dat.required_pulses] = self.llrf_config['DEFAULT_PULSE_COUNT']
#         #
#         # Write to log
#         self.logger.header( self.my_name + ' has processed the pulse_count_breakdown_log ', True)
#         self.logger.message([
#             dat.log_pulse_count + ' ' + str(self.values[dat.log_pulse_count]),
#             dat.required_pulses + ' ' + str(self.values[dat.required_pulses]),
#             dat.breakdown_count + ' ' + str(self.values[dat.breakdown_count]),
#             dat.log_amp_set + ' ' + str(self.values[dat.log_amp_set]),
#             dat.current_ramp_index + ' ' + str(self.values[dat.current_ramp_index]),
#             'pulse length = ' + str(self._llrf_config['PULSE_LENGTH_START']),
#             dat.next_sp_decrease + ' ' + str(self.values[dat.next_sp_decrease])
#         ],True)
#         #
#         # Setting the last 10^6 breakdown last_106_bd_count
#         #
#         # get the last million pulses from THE ORIGINAL pulse_break_down_log
#         # !!! WE must use the original pulse_break_down_log, as it will have the true breakdown_count and pulse number !!!
#         # !!! (remember above we deleted the last entry in pulse_break_down_log to get generate amp_sp_history         !!!
#         pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
#         one_million_pulses_ago = self.values[dat.log_pulse_count] - self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']
#         dat.rf_condition_data_base.last_million_log = [x for x in pulse_break_down_log if x[0] >= one_million_pulses_ago ]
#         #
#         # write last_million_log to log
#         self.logger.header('Last million pulses', True)
#         for value in dat.rf_condition_data_base.last_million_log:
#             str1 = ', '.join(str(e) for e in value)
#             self.logger.message( str1, True)
#         self.logger.message('One Million pulses ago  = ' + str(one_million_pulses_ago),True)
#         first_entry = ' , '.join(str(x) for x in dat.rf_condition_data_base.last_million_log[0])
#         last_entry  = ' , '.join(str(x) for x in dat.rf_condition_data_base.last_million_log[-1])
#         self.logger.message('last_million_log[ 0] = ' + first_entry ,True)
#         self.logger.message('last_million_log[-1] = ' + last_entry ,True)
#         #
#         # sanity check
#         #
#         sanity_passed = True
#         if dat.rf_condition_data_base.last_million_log[-1][1] != self.values[dat.breakdown_count]:
#             self.logger.message('Error in breakdown count',True)
#             sanity_passed = False
#         if dat.rf_condition_data_base.last_million_log[-1][0] != self.values[dat.log_pulse_count]:
#             self.logger.message('Error in pulse_count',True)
#             sanity_passed = False
#         if sanity_passed:
#             self.logger.message('Getting the pulse_breakdown_log passed sanity check', True)
#         else:
#             self.logger.message('!!WARNING!! When getting the pulse_breakdown_log we failed a sanity check!!', True)
#
#         #
#         # Now we are free to update the breakdown stats !!
#         #
#         self.update_breakdown_stats()
#
#     # REPLACE WITH LOOKUP TABLE FO RPOWER - EVENT PULSES
#     def ceiling(self,x, base=1000):
#         if base ==0:
#             print 'MAJOR ERROR'
#         return int(base * np.ceil(float(x) / base))
#
#     def power_increase(self):
#         # will break if setting in config have not been passed
#         if self.values[dat.pulse_count] < self.power_increase_2:
#             a = self.power_increase_1 * self.values[dat.pulse_count]
#         else:
#             a = self._llrf_config['NORMAL_POWER_INCREASE']
#         print(self.my_name + ' power_increase = ' + str(a) + ' ' + str(self.ceiling(a,
#                                                                                     self._llrf_config['LOW_POWER_INCREASE'])) )
#         return self.ceiling(a, self._llrf_config['LOW_POWER_INCREASE'])
#
#
#     # neaten up, do we have to redraw each time?
#     def plot(self,x,y,m,c,x0,x1,predict):
#         plt.clf()
#         plt.plot(x, y, '.')
#         plt.plot( np.unique([self.old_x_min,self.old_x_max]), self.old_m * np.unique([self.old_x_min,self.old_x_max]) + self.old_c, '-')
#         plt.plot( np.unique([x0,x1]), m * np.unique([x0,x1]) + c, '-')
#         plt.plot(predict[0],predict[1], '*')
#         plt.draw()
#         plt.pause(0.00001)
#         self.old_x_min = x0
#         self.old_x_max = x1
#         self.old_m = m
#         self.old_c = c
#
#
#     #close function
#     def close(self):
#         plt.close()
#


    # OLD BASE ClASS FUNCIONS
    # OLD BASE ClASS FUNCIONS
    # OLD BASE ClASS FUNCIONS
    # OLD BASE ClASS FUNCIONS
    # OLD BASE ClASS FUNCIONS
    # OLD BASE ClASS FUNCIONS
    # OLD BASE ClASS FUNCIONS
#
# self.data_log_timer = QTimer()
# self.amp_pwr_log_timer = QTimer()
# #
# # previous entry in kfp running stat, so we don't duplicate too much in the file
# self.last_kfp_running_stat_entry = None
# #
# # This i sa counter to update the pulse_break_down log with the data.log (bunary)
# # its used to write the pulse_break_down less frequently than data.log
# self.counter_add_to_pulse_breakdown_log = 0
#
#
# @property
# def llrf_config(self):
#     return rf_condition_data_base._llrf_config
#
#
# @llrf_config.setter
# def llrf_config(self, value):
#     rf_condition_data_base._llrf_config = value
#
#
# def start_logging(self):
#     self.logger.start_data_logging()
#     self.data_log()
#     self.data_log_timer.timeout.connect(self.data_log)
#     self.data_log_timer.start(rf_condition_data_base.config.log_config['DATA_LOG_TIME'])
#     self.amp_pwr_log_timer.timeout.connect(self.log_kly_fwd_power_vs_amp)
#     self.amp_pwr_log_timer.start(rf_condition_data_base.config.log_config['AMP_PWR_LOG_TIME'])
#
#
# def timestamp(self):
#     ts = datetime.datetime.now() - self.logger.log_start
#     # print 'time = ' + str(ts.total_seconds())
#     rf_condition_data_base.values[time_stamp] = ts.total_seconds()
#
#
# def update_break_down_count(self, count):
#     # if all status are not bad then add to breakdown count
#     if state.BAD not in [rf_condition_data_base.values[DC_spike_status],
#                          rf_condition_data_base.values[vac_spike_status],
#                          rf_condition_data_base.values[breakdown_status]]:
#         self.force_update_breakdown_count(count)
#     else:
#         self.logger.message(
#             self.my_name + ' NOT increasing breakdown count, already in cooldown, = ' + str(
#                 rf_condition_data_base.values[breakdown_count]), True)
#
#
# def force_update_breakdown_count(self, count):
#     rf_condition_data_base.values[breakdown_count] += count
#
#     self.logger.message(self.my_name + ' increasing breakdown count = ' + str(
#         rf_condition_data_base.values[breakdown_count]) + ', at pulse count = ' + str(
#         rf_condition_data_base.values[pulse_count]), True)
#     self.beep(count)  # self.add_to_pulse_breakdown_log(rf_condition_data_base.amp_sp_history[-1])
#
#
# def beep(self, count):
#     winsound.Beep(2000, 150)  ## MAGIC_NUMBER
#
#
# def reached_min_pulse_count_for_this_step(self):
#     return self.values[event_pulse_count] >= self.values[required_pulses]
#
#
# # the main logging data file is binary(!)
# # With the amount of data etc. I think this is the only practical way
# # to save it, the header for each file with give types and names
# def data_log(self):
#     self.timestamp()
#     if self.should_write_header:
#         self.logger.write_data_log_header(rf_condition_data_base.values)
#         self.should_write_header = False
#     self.logger.write_data(rf_condition_data_base.values)
#     if self.counter_add_to_pulse_breakdown_log % 10 == 0:  ## MAGIC_NUMBER
#         self.add_to_pulse_breakdown_log(rf_condition_data_base.values[amp_sp])
#         self.update_breakdown_stats()
#     self.counter_add_to_pulse_breakdown_log += 1  ## MAGIC_NUMBER
#
#
# def log_kly_fwd_power_vs_amp(self):
#     next_log_entry = self.last_kfp_running_stat_entry
#     if rf_condition_data_base.values[
#         amp_sp] in rf_condition_data_base.amp_vs_kfpow_running_stat.keys():
#         next_log_entry = [rf_condition_data_base.values[amp_sp]] + \
#                          rf_condition_data_base.amp_vs_kfpow_running_stat[
#                              rf_condition_data_base.values[amp_sp]]
#
#     if next_log_entry != self.last_kfp_running_stat_entry:
#         self.logger.add_to_KFP_Running_stat_log(next_log_entry)
#     self.last_kfp_running_stat_entry = next_log_entry
#
#     if rf_condition_data_base.values[amp_sp] > 100:  # MAGIC_NUMBER
#         if self.kly_power_changed():
#             # rf_condition_data_base.kly_fwd_power_history.append( rf_condition_data_base.values[
#             # fwd_kly_pwr] )
#             if rf_condition_data_base.values[fwd_kly_pwr] > \
#                     rf_condition_data_base.config.llrf_config['KLY_PWR_FOR_ACTIVE_PULSE']:
#                 rf_condition_data_base.sp_pwr_hist.append([rf_condition_data_base.values[amp_sp],
#                                                            rf_condition_data_base.values[
#                                                                fwd_kly_pwr]])  #
#                 # self.update_amp_pwr_mean_dict(rf_condition_data_base.values[amp_sp],  #                               rf_condition_data_base.values[fwd_kly_pwr])
#         # cancer
#         if rf_condition_data_base.values[amp_sp] not in rf_condition_data_base.amp_sp_history:
#             rf_condition_data_base.amp_sp_history.append(rf_condition_data_base.values[amp_sp])
#             self.logger.message(
#                 'New amp_sp_history value = ' + str(rf_condition_data_base.values[amp_sp]), True)
#
#
# def kly_power_changed(self):
#     r = False
#     if rf_condition_data_base.last_fwd_kly_pwr != rf_condition_data_base.values[fwd_kly_pwr]:
#         r = True
#     rf_condition_data_base.last_fwd_kly_pwr = rf_condition_data_base.values[fwd_kly_pwr]
#     return r
#
#
# def add_to_pulse_breakdown_log(self, amp):
#     if amp > 100:  # MAGIC_NUMBER
#         self.logger.add_to_pulse_breakdown_log([rf_condition_data_base.values[pulse_count],
#                                                 rf_condition_data_base.values[breakdown_count],
#                                                 int(amp), int(
#                 rf_condition_data_base.values[current_ramp_index]), int(
#                 rf_condition_data_base.values[pulse_length] * 1000)  # MAGIC_NUMMBER UNITS
#                                                 ])
#     else:
#         self.logger.message('Not adding to pulse_breakdown_log, amp = ' + str(amp), True)

    # @staticmethod
    # def add_data_key( key, initial_value = None):
    #     '''
    #     Function that adds a key to the main data dictionaries, we do this so that we are less
    #     likely to forget to add a new key
    #     :param key: new key to be added
    #     :param initial_value: an intial value for the key, THIS SHOULD BE None, or, when debugging
    #     of the correct type
    #     '''
    #     rf_conditioning_data.all_value_keys.append( key )
    #     rf_conditioning_data.values[key] = initial_value

    # meh ...
    # phase_mask_by_power_trace_1_set = 'phase_mask_by_power_trace_1_set'
    # all_value_keys.append(phase_mask_by_power_trace_1_set)
    # values[phase_mask_by_power_trace_1_set] = False
    #
    # phase_mask_by_power_trace_2_set = 'phase_mask_by_power_trace_2_set'
    # all_value_keys.append(phase_mask_by_power_trace_2_set)
    # values[phase_mask_by_power_trace_2_set] = False
    #
    # phase_end_mask_by_power_trace_1_time = 'phase_end_mask_by_power_trace_1_time'
    # all_value_keys.append(phase_end_mask_by_power_trace_1_time)
    # values[phase_end_mask_by_power_trace_1_time] = bool
    #
    # phase_end_mask_by_power_trace_2_time = 'phase_end_mask_by_power_trace_2_time'
    # all_value_keys.append(phase_end_mask_by_power_trace_2_time)
    # values[phase_end_mask_by_power_trace_2_time] = state.UNKNOWN
