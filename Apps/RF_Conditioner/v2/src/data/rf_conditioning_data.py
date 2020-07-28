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

import numpy as np, sys
import matplotlib.pyplot as plt
from config import config
from rf_conditioning_logger import rf_conditioning_logger
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from ramp import *
from src.data.state import state
from src.data.state import ramp_method
from numpy import float64 as np_float64
import math


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

    amp_vs_kfpow_running_stat = None

    last_fwd_kly_pwr = None

    excluded_key_list = []

    # this curve is going to be redefined every time we switch back on, when not in use set to None!!
    log_ramp_curve = None
    log_ramp_curve_index = None

    ramp_power_sum = None

    """
    NOT SURE IF DEBUG DOES ANYTHING
    """
    debug = False

    def __init__(self, debug=False):
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
        #
        # previous entry in kfp running stat, so we don't duplicate too much in the file
        self.last_kfp_running_stat_entry = None

        self.ramp_max_index = len(ramp) - 1

        ramp_powers = [p[1] for p in ramp]
        
        if rf_conditioning_data.ramp_power_sum is None:
            rf_conditioning_data.ramp_power_sum = [sum(ramp_powers[:y]) for y in range(1, len(ramp_powers) + 1)]
            print("self.ramp_power_sum =",  rf_conditioning_data.ramp_power_sum)

    def get_ramp_index_from_power(self, power):
        '''
            we can get the place on the ramp curve
        '''
        return len([p for p in rf_conditioning_data.ramp_power_sum if p < power])

    def set_ramp_index_for_current_power(self):
        rcd = rf_conditioning_data

        self.values[rcd.current_ramp_index] = self.get_ramp_index_from_power(self.get_kf_running_stat_power_at_current_set_point())

        rcd.values[rcd.last_power_change] = rcd.values[rcd.next_power_change]

        [rcd.values[rcd.required_pulses], rcd.values[rcd.next_power_change] ] = self.get_power_and_num_pulses_for_ramp_index(rcd.values[rcd.current_ramp_index])

        # rcd.values[rcd.required_pulses] = ramp[rcd.values[rcd.current_ramp_index]][0]
        # rcd.values[rcd.next_power_change] = float(ramp[rcd.values[rcd.current_ramp_index]][1])

        self.logger.message_header(__name__ + ' set_ramp_values ')
        self.logger.message(
            'current ramp index = {}\nnext required pulses = {}\nnext power increase = {}'.format(rcd.values[rcd.current_ramp_index],
                                                                                                         rcd.values[rcd.required_pulses], rcd.values[
                                                                                                             rcd.next_power_change]))  #  #

    def get_power_and_num_pulses_for_ramp_index(self, index):
        if index < 0:
            return ramp[0]
        elif index > len(ramp) - 1:
            return ramp[-1]
        else:
            return ramp[index]

    def get_log_ramp_power_finsh(self):
        print("get_log_ramp_power_finsh")

        if rf_conditioning_data.values[rf_conditioning_data.last_amp_sp] > 500:
            print("last_amp_sp > 500")
            return self.get_kf_running_stat_power_at_set_point(rf_conditioning_data.values[rf_conditioning_data.last_amp_sp])
        else:
            print("last_amp_sp = {}".format( rf_conditioning_data.values[rf_conditioning_data.last_amp_sp]) )
            return self.get_kf_running_stat_power_at_set_point( self.values[rf_conditioning_data.log_amp_set] )

    def get_kf_running_stat_power_at_current_set_point(self):
        return self.get_kfp_running_stat_at_current_set_point()[1]

    def get_kf_running_stat_power_at_set_point(self, sp):
        r = self.get_kfp_running_stat_at_set_point(sp)
        if r:
            return r[1]
        return r

    def get_kfp_running_stat_at_current_set_point(self):
        r = self.get_kfp_running_stat_at_set_point(rf_conditioning_data.values[rf_conditioning_data.amp_sp])
        if type(r) == float:
            return [0,0,0,0]
        return r

    def get_kfp_running_stat_at_set_point(self, sp):
        if sp in rf_conditioning_data.amp_vs_kfpow_running_stat:
            return self.amp_vs_kfpow_running_stat[sp]
        return [0,0,0,0]

    def reset_event_pulse_count(self):
        rcd = rf_conditioning_data
        rcd.values[rcd.event_pulse_count_zero] = rcd.values[rcd.pulse_count]
        rcd.values[rcd.event_pulse_count] = 0
        self.logger.message_header(__name__ + ' reset_event_pulse_count')
        self.logger.message('new event_pulse_count_zero = {}'.format(rcd.values[rcd.event_pulse_count_zero]))

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
        v[rcd.llrf_DAQ_rep_rate_max] = cd[config.RF_REPETITION_RATE] + cd[config.RF_REPETITION_RATE_ERROR]
        v[rcd.llrf_DAQ_rep_rate_min] = cd[config.RF_REPETITION_RATE] - cd[config.RF_REPETITION_RATE_ERROR]

        ## set the pusle length min adn max ranges
        v[rcd.expected_pulse_length] = cd[config.PULSE_LENGTH]
        v[rcd.pulse_length_min] = cd[config.PULSE_LENGTH] + cd[config.PULSE_LENGTH_ERROR]
        v[rcd.pulse_length_max] = cd[config.PULSE_LENGTH] - cd[config.PULSE_LENGTH_ERROR]

    def log_kly_fwd_power_vs_amp(self):
        '''
            update the KFP running stats log file, with some checking to only update the file if we have new data
        '''
        rcd = rf_conditioning_data
        next_log_entry = self.last_kfp_running_stat_entry
        if rcd.values[rcd.amp_sp] in rcd.amp_vs_kfpow_running_stat.keys():
            next_log_entry = [rcd.values[rcd.amp_sp]] + rcd.amp_vs_kfpow_running_stat[rcd.values[rcd.amp_sp]]
        # if the numbers have changed since the last time we ran this function then write to text log
        if next_log_entry != self.last_kfp_running_stat_entry:
            self.logger.add_to_kfpow_running_stat_log(next_log_entry)
        self.last_kfp_running_stat_entry = next_log_entry

        ''' This past is updating the amp_sp_history, howeverr for verison 2 i con't think we need it  '''
        if rcd.values[rcd.amp_sp] > 100.0:  # MAGIC_NUMBER so we don't log low settings due to BD events
            if self.kly_power_changed():
                if rcd.values[rcd.fwd_kly_pwr] > self.config.raw_config_data['KLY_PWR_FOR_ACTIVE_PULSE']:
                    rcd.sp_pwr_hist.append([rcd.values[rcd.amp_sp], rcd.values[rcd.fwd_kly_pwr]])
            # cancer
            if rcd.values[rcd.amp_sp] not in rcd.amp_sp_history:
                rcd.amp_sp_history.append(rcd.values[rcd.amp_sp])
                self.logger.message('New amp_sp_history value = ' + str(rcd.values[rcd.amp_sp]))

    def kly_power_changed(self):
        '''
            this is checking to see if the current kfpow is different to the last time this function was called
            We do this because the LLRF can get in a state were it continuously sends out the same data (due to ACQM and SCAN settings)
        '''
        rcd = rf_conditioning_data
        r = False
        if rcd.last_fwd_kly_pwr != rcd.values[rcd.fwd_kly_pwr]:
            r = True
        rcd.last_fwd_kly_pwr = rcd.values[rcd.fwd_kly_pwr]
        return r

    def setup_pulse_count_breakdown_log(self):
        """
        this is way too complicated ... but its processing the data in two ways,
        once by amp_setpoint and once by pulse count, it generates to main lists:
        1) rf_condition_data.amp_sp_history
              Sorted by amp_setpoint
              Used to define how to ramp up and down
        2) rf_condition_data.last_million_log
              Sorted by pulse count
              used to define the Breakdown Rate etc.
        if I read through the comments, i can basically work out what is going on
        """
        # TODO: we should use fitting to move down in power steps instead of next_sp_decrease in the same way we move up in power steps
        # TODO: the ramp index should continue to increment, even when it as above the total number of ramp points, then we know how many steps we
        #  have actually gone up / down

        # local alias for shorter lines
        rcd = rf_conditioning_data
        message = self.logger.message
        #
        # get the pulse_break_down_log entries from file (this is just the raw entries from the file )
        pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
        #
        # based on the log file we set active pulse count total,
        # the starting point is the one before the last entry  (WHY???? DJS Jan 2019)
        #
        # FIRST:
        # save the last entry, log_pulse_count and breakdown count
        # keep this seperate as pulse_count will get overwritten!!
        # TODO use small helper functions to get pulse-count, amp_sp, bd, from an entry, so we don't make mistakes  with indexes
        self.values[rcd.log_pulse_count] = int(pulse_break_down_log[-1][0])

        # we **can** set these here,
        self.values[rcd.pulse_count] = self.values[rcd.log_pulse_count]
        self.values[rcd.event_pulse_count_zero] = self.values[rcd.log_pulse_count]
        self.values[rcd.event_pulse_count] = 0


        self.values[rcd.breakdown_count] = int(pulse_break_down_log[-1][1])

        #
        # next we must insert the data in to the main data values dictionary
        # set the ramp index
        self.values[rcd.current_ramp_index] = int(pulse_break_down_log[-1][3])
        #self.set_ramp_values()

        #
        # pulse length (logged but not used as pulse_length is now defined by the pulse shaping
        # table)
        self.values[rcd.log_pulse_length] = float(int(pulse_break_down_log[-1][3])) / float(1000.0)  # warning UNIT

        # TODO I don't think this is used and doesn't make sense to me now
        self.config_data['PULSE_LENGTH_START'] = self.values[rcd.log_pulse_length]

        #
        # The Frist amp_setpoint to set on start-up
        self.values[rcd.log_amp_set] =  int(pulse_break_down_log[-1][2])

        # TODO djs: i don't think we need the below, (apart from to get some numbers out), this data should be ratinoalises (cut to just what we
        #  need ) which is when a BD event happened, and the last point we were at
        # first amp_sp to use is the is the  last one in log file ( IT USED TO BE THE  2nd to last one)
        # remove values greater than than last_amp_sp_in_file
        last_amp_sp_in_file = int(pulse_break_down_log[-1][2])
        indices_to_remove = []
        index_to_remove = 0
        for entry in pulse_break_down_log:
            #if entry[2] >= last_amp_sp_in_file:
            if entry[2] > last_amp_sp_in_file:
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
        # set the number of pulses required at this step to the default, updated later
        self.values[rcd.required_pulses] = self.config_data['DEFAULT_PULSE_COUNT']
        #
        # Write to log
        message(__name__ + ' has processed the pulse_count_breakdown_log ')
        message([rcd.log_pulse_count + ' ' + str(self.values[rcd.log_pulse_count]), rcd.required_pulses + ' ' + str(self.values[rcd.required_pulses]),
                 rcd.breakdown_count + ' ' + str(self.values[rcd.breakdown_count]), rcd.log_amp_set + ' ' + str(self.values[rcd.log_amp_set]),
                 rcd.current_ramp_index + ' ' + str(self.values[rcd.current_ramp_index]), # hmmm what to do about pulse length chaing
                 # 'pulse length = ' + str(self._llrf_config['PULSE_LENGTH_START']),
                 rcd.next_sp_decrease + ' ' + str(self.values[rcd.next_sp_decrease])], )

        # TODO we can overright the puslebreakdwon log with a trimmed/rationlized version if we want ...
                        #
        # Setting the last 10^6 breakdown last_106_bd_count
        #
        # get the last million pulses from THE ORIGINAL pulse_break_down_log
        # !!! WE must use the original pulse_break_down_log, as it will have the true
        # breakdown_count and pulse number !!!
        # !!! (remember above we deleted the last entry in pulse_break_down_log to  generate
        # amp_sp_history         !!!
        pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
        one_million_pulses_ago = self.values[rcd.log_pulse_count] - self.config_data['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']
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
        message('last_million_log[ 0] = ' + first_entry)
        message('last_million_log[-1] = ' + last_entry)
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
        self.update_breakdown_stats()

    def update_breakdown_stats(self):
        '''

        :return:
        '''
        # local alias for shorter lines
        rcd = rf_conditioning_data
        message = self.logger.message

        old_last_106_bd_count = self.values[rcd.last_106_bd_count]
        self.values[rcd.breakdown_count] = rcd.last_million_log[-1][1]
        self.values[rcd.last_106_bd_count] = rcd.last_million_log[-1][1] - rcd.last_million_log[0][1]
        # if we have more than 1 million pulses its easy
        if rcd.last_million_log[-1][0] > self.config_data['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']:
            self.values[rcd.breakdown_rate] = self.values[rcd.last_106_bd_count]
        else:  # else do some math
            if rcd.last_million_log[-1][0] == 0:
                self.values[rcd.breakdown_rate] = 0
            else:
                # !!!!!!!!!! THIS EQUATION MAY NOT BE CORRECT !!!!!!!!!!!!!!
                self.values[rcd.breakdown_rate] = float(
                    self.values[rcd.last_106_bd_count] * self.config_data['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']) / float(
                    rcd.last_million_log[-1][0] - rcd.last_million_log[0][0])

        # set is breakdwon rate hi
        self.values[rcd.breakdown_rate_low] = self.values[rcd.breakdown_rate] <= self.values[rcd.breakdown_rate_aim]

        if old_last_106_bd_count != self.values[rcd.last_106_bd_count]:
            self.logger.message_header(' NEW last_106_bd_count ', add_to_text_log=True, show_time_stamp=False)
            message('Total breakdown_count = ' + str(rcd.last_million_log[-1][1]), add_to_text_log=True, show_time_stamp=False)

            message('Last million pulse count => ' + str(rcd.last_million_log[-1][0]) + ' - ' + str(rcd.last_million_log[0][0]) + ' = ' + str(
                rcd.last_million_log[-1][0] - rcd.last_million_log[0][0]), add_to_text_log=True, show_time_stamp=False)
            message('Last million breakdown_count => ' + str(rcd.last_million_log[-1][1]) + ' - ' + str(rcd.last_million_log[0][1]) + ' = ' + str(
                self.values[rcd.last_106_bd_count]), add_to_text_log=True, show_time_stamp=False)

            if self.values[rcd.breakdown_rate_low]:
                message('Breakdown rate Low: ' + str(self.values[rcd.breakdown_rate]) + ' <= ' + str(self.values[rcd.breakdown_rate_aim]),
                    add_to_text_log=True, show_time_stamp=False)
            else:
                message('Breakdown rate High: ' + str(self.values[rcd.breakdown_rate]) + ' > ' + str(self.values[rcd.breakdown_rate_aim]),
                    add_to_text_log=True, show_time_stamp=False)  # ESTIMATE THE NUMBER OF PULSES BEFORE WE GO GOOD AGAIN

    def update_last_million_pulse_log(self):
        """
        Every time we check te numebr of pulses / breakdown counts we update the last million log
        """
        # local alias for shorter lines
        rcd = rf_conditioning_data

        # add the next set of values to the last_million_log
        rcd.last_million_log.append(
            [self.values[rcd.pulse_count], self.values[rcd.breakdown_count], self.values[rcd.current_ramp_index], self.values[rcd.pulse_length]])

        # remove entries that are mor ethan 1 millino pulses ago
        # TODO should we hardcode in the million pulses??? or have it  as a config parameters,
        #  and rename everything that references 1 million???? MAYBE CALL IT
        #  recent_breakdown_history, recent_bd_history >>> ?
        #
        while rcd.last_million_log[-1][0] - rcd.last_million_log[0][0] > self.config_data[config.NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY]:
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
                [rcd.values[rcd.pulse_count], rcd.values[rcd.breakdown_count], int(amp), int(rcd.values[rcd.current_ramp_index]),
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
        #
        # set some values from teh config, DO all of them here???
        ##elf.values[dat.pulse_length_start] = self.llrf_config['PULSE_LENGTH_START']
        # self.values[rcd.pulse_length_aim] = cd['PULSE_LENGTH_AIM']
        # self.values[rcd.pulse_length_aim_error] = cd['PULSE_LENGTH_AIM_ERROR']
        # self.values[rcd.pulse_length_min] = cd['PULSE_LENGTH_AIM'] - cd['PULSE_LENGTH_AIM_ERROR']
        # self.values[rcd.pulse_length_max] = cd['PULSE_LENGTH_AIM'] + cd['PULSE_LENGTH_AIM_ERROR']

        #  Binning data
        # BIN_data = 'BIN_data'
        # bin_keys.append(BIN_data)
        # binned_amp_vs_kfpow[BIN_data] = dummy_float
        # TODO: AT SOMe POINT WE NEED TO INCLUDE ERRORS IN THE BIN VALUE, BUT THIS NEEDS TO BE
        #  DONE 'PROPERLY' USING THE FULL PULSE COUNTS
        # BIN_error = 'BIN_error'
        # bin_keys.append(BIN_error)
        # binned_amp_vs_kfpow[BIN_error] = dummy_float

        # TODO AJG: bin the amp-power data here after being read in
        # print 'rcd.amp_vs_kfpow_running_stat[0] = ', rcd.amp_vs_kfpow_running_stat[0]
        # print 'rcd.amp_vs_kfpow_running_stat[0][0] = ', rcd.amp_vs_kfpow_running_stat[0][0]
        # print 'len(rcd.amp_vs_kfpow_running_stat) = ', len(rcd.amp_vs_kfpow_running_stat)

        # TODO AJG: cycle over 'rcd.amp_vs_kfpow_running_stat' and append ...
        # key = amp **
        # [0] = num_pulses (with beam)
        # [1] = power **
        # [2] = rolling variance * (num_pulses -1)  .....I think!


        bin_X, bin_mean, bin_edges, bin_pop, bin_data, bin_std, bin_pulses = self.initial_bin()

        rcd.binned_amp_vs_kfpow['BIN_X'] = bin_X
        rcd.binned_amp_vs_kfpow['BIN_mean'] = bin_mean

        #print('bin_X = {}\nbin_mean = {}'.format(bin_X, bin_mean))


        rcd.binned_amp_vs_kfpow['BIN_edges'] = bin_edges
        rcd.binned_amp_vs_kfpow['BIN_pop'] = bin_pop
        rcd.binned_amp_vs_kfpow['BIN_pulses'] = bin_pulses
        # binned_amp_vs_kfpow[BIN_data] = bin_data
        # binned_amp_vs_kfpow[BIN_error] = bin_error

        # TODO AJG: diagnostic plot saved to work folder:

        AMP_preBin = []
        POW_preBin = []

        for key in rcd.amp_vs_kfpow_running_stat.keys():
            AMP_preBin.append(key)
            POW_preBin.append(rcd.amp_vs_kfpow_running_stat[key][1])

        bin_plots_path = r'C:\Users\dlerlp\Documents\RF_Conditioning_20200720'
        POW_preBin_MW = [i / 10 ** 6 for i in POW_preBin]
        bin_mean = [i / 10 ** 6 for i in bin_mean]
        plt.scatter(AMP_preBin, POW_preBin_MW, c='k', s=1.0, marker='.', label='Data', zorder=1)
        plt.scatter(bin_X, bin_mean, c='r', s=25, marker='x', label='Binned Mean', zorder=0)
        # plt.errorbar(bin_X, bin_mean, yerrbin_error, xerr=0, fmt='none', ecolor='red',
        # elinewidth=0.5, capsize=2.0, capthick=0.5)
        plt.xlabel('Set Point')
        plt.ylabel('Power (MW)')
        plt.legend()
        plt.grid(True)
        plt.savefig(bin_plots_path + r'\Binning_Plot.png')
        plt.close('all')

        plt.scatter(AMP_preBin, POW_preBin_MW, c='k', s=1.0, marker='.', label='Data', zorder=1)
        plt.scatter(bin_X, bin_mean, c='r', s=25, marker='x', label='Binned Mean', zorder=0)
        # plt.errorbar(bin_X, bin_mean, yerrbin_error, xerr=0, fmt='none', ecolor='red',
        # elinewidth=0.5, capsize=2.0, capthick=0.5)
        plt.xlim(0.0, max(AMP_preBin))
        plt.xlabel('Set Point')
        plt.ylabel('Power (MW)')
        plt.legend()
        plt.grid(True)
        plt.savefig(bin_plots_path + r'\Binning_Plot_zoom.png')
        plt.close('all')

    def initial_bin(self):

        '''This reads in the data from the amp_power log and bins all available data.
        The power values are already mean so need multiplying by the # of pulses, summing then dividing by the total number of pulses
        to get the genuine mean.
        '''

        rcd = rf_conditioning_data

        # cycle through amp_vs_kfpow_running_stat to populate amp_sp, kfpwr and number-of-pulses lists
        x = amp_sp_raw = []
        num_pulses_prebin = []
        y = mean_kfpwr_raw = []



        for key in rcd.amp_vs_kfpow_running_stat.keys():
            amp_sp_raw.append(key)
            num_pulses_prebin.append(rcd.amp_vs_kfpow_running_stat[key][0])
            mean_kfpwr_raw.append(rcd.amp_vs_kfpow_running_stat[key][1])
            #print("init_bin set_up data = ", amp_sp_raw[-1], num_pulses_prebin[-1], mean_kfpwr_raw[-1])



        #print('mean_kfpwr_raw = {}'.format(mean_kfpwr_raw))

        # Call in config parameters
        bin_width = self.config.raw_config_data['BIN_WIDTH']
        max_pow = self.config.raw_config_data['MAX_POW']
        min_amp = self.config.raw_config_data['MIN_AMP']
        max_amp = self.config.raw_config_data['MAX_AMP']

        # append max_amp & max_pow to list of amp & power. This is done so bins can be created ahead of the current amp_sp/kfpwr data point.
        #x = [x[i] for i in range(len(x) - 1) if x[i] != x[i + 1]]
        x.append(max_amp)
        #y = [y[i] for i in range(len(x) - 1) if x[i] != x[i + 1]]
        y.append(max_pow)

        # Create list of bin edges starting at min_amp and ending at max_amp (max_amp now last element of x list)
        bedges = np.arange(int(min_amp), int(x[-1]), bin_width).tolist()  # Not happy with np.arange.tolist() but it works!?!

        # create arrays of zeros of length len(bedges)-1 ready to be populated by the main calculator
        bin_pulses = np.zeros(len(bedges) - 1)
        bin_mean =  np.zeros(len(bedges) - 1)
        bin_pop = np.zeros(len(bedges) - 1)
        bin_std = np.zeros(len(bedges) - 1)
        bin_pulses = np.zeros(len(bedges) - 1)

        # Create dictionary of empty lists ready to be populated by all the raw kfpwr data sorted by bins where the bin index is the dict key
        keyList = [i for i in range(len(bedges) - 1)]
        data_binned = {}
        for i in keyList:
            data_binned[i] = []

        # MAIN CALCULATOR: cycle over data and assign it to bins
        for i in range(0, len(x)):
            for j in range(0, len(bin_mean)):
                if x[i] >= bedges[j] and x[i] < bedges[j + 1]:
                    # multiply the number of pulses by the mean kfpowr to get the product (used in MEAN_EQN)
                    bin_pulse_x_mean =  num_pulses_prebin[i] * y[i]
                    # Define the new total number of pulses in the bin (used in MEAN_EQN)
                    bin_pulses_new = (bin_pulses[j] +  num_pulses_prebin[i])
                    # MEAN_EQN:
                    bin_mean[j] = ((bin_mean[j] * bin_pulses[j]) + (bin_pulse_x_mean)) / bin_pulses_new
                    # Update the total number of pulses in the bin with new value
                    bin_pulses[j] = bin_pulses_new
                    # Add one to bin population
                    bin_pop[j] += 1.0
                    # Add datapoint to data_binned dictionary
                    data_binned[j].append(y[i])
                    # Calculate the standard deviation of the data in each bin (needs to be weighted properly)
                    bin_std[j] = np.std(data_binned[j])

        # Create a list of mid-bin amp set point values for use with the GUI plotter
        X = [k + bin_width / 2.0 for k in bedges[:-1]]

        #print('X = {}\nbin_mean = {}\nbin_pulses = {}\nbin_pop = {}\ndata_binned = {}\nbin_error = {}'.format(X[0:10], bin_mean[0:10],
        # bin_pulses[0:10], bin_pop[0:10],data_binned, bin_std[0:10]))

        return X, bin_mean, bedges, bin_pop, data_binned, bin_std, bin_pulses

    def update_binned_data(self):
        '''
        This function reads in the latest amp_sp - kfpow values as well as the output from
        initial_bin() or the previous dynamic_bin().

        Finds the relevant bin for the new amp_sp value and updates BIN_pop & BIN_mean in that bin.
        updates the binning dictionary with new values.
        '''

        # TODO: how often do we update the binned data, and do we just use the current
        #  amp_setpoint data or do we re-bin all the data ???
        # TODO Lets update the binned data with amp_vs_kfpow_running_stat
        # TODO it seems like there maybe a 'cleaner' way to do this

        # new_amp = int(self.amp_vs_kfpow_running_stat[self.values[self.data.amp_sp]])

        # Acquire latest amp_sp, mean_kfpwr & number of pulses at amp_sp:
        new_kfp_pulses_list = rf_conditioning_data.amp_vs_kfpow_running_stat[self.values[rf_conditioning_data.amp_sp]]
        new_amp = self.values[rf_conditioning_data.amp_sp]
        new_kfp = new_kfp_pulses_list[1]
        new_pulses = new_kfp_pulses_list[0]

        # Collate new data into newdata list
        newdata = [new_amp, new_kfp, new_pulses]
        print('new_kfp_list = {}\ntype(new_kfp_list) = {}'.format(new_kfp_pulses_list, type(new_kfp_pulses_list)))

        # Call in data from binned_amp_vs_kfpow distionary already populated by initial_bin() ind subsequently here.
        bin_mean = rf_conditioning_data.binned_amp_vs_kfpow['BIN_mean']
        bedges = rf_conditioning_data.binned_amp_vs_kfpow['BIN_edges']
        bin_pop = rf_conditioning_data.binned_amp_vs_kfpow['BIN_pop']
        bin_pulses = rf_conditioning_data.binned_amp_vs_kfpow['BIN_pulses']

        # Cycle through bin edges until the x-axis (amp_sp) data sits between current and next bin edge.
        for i in range(int(len(bin_mean))):
            if newdata[0] >= bedges[i] and newdata[0] < bedges[i + 1]:
                # multiply the number of pulses by the mean kfpowr to get the product (used in MEAN_EQN)
                bin_pulse_x_mean =  newdata[1] * newdata[2]
                # Define the new total number of pulses in the bin (used in MEAN_EQN)
                bin_pulses_new = (bin_pulses[i] + newdata[2])
                # MEAN_EQN:
                bin_mean[i] = ((bin_mean[i] * bin_pulses[i]) + (bin_pulse_x_mean)) / bin_pulses_new
                # Update the total number of pulses in the bin with new value
                bin_pulses[i] = bin_pulses_new
                # Add one to bin population
                bin_pop[i] += 1.0
                # Once found no need to continue, so break.
                break
            else:
                pass

        # Update dictionary with new values
        rf_conditioning_data.binned_amp_vs_kfpow['BIN_mean'] = bin_mean
        rf_conditioning_data.binned_amp_vs_kfpow['BIN_pop'] = bin_pop
        rf_conditioning_data.binned_amp_vs_kfpow['BIN_pulses'] = bin_pulses

        '''
        bin_plots_path = r'C:\Users\dlerlp\Documents\RF_Conditioning_20200720'
        plt.scatter(newdata[0], newdata[0], c='g', s=35, marker='x', label='Data', zorder=1)
        plt.scatter(BIN_X_dyn, BIN_mean, c='r', s=25, marker='x', label='Binned Mean', zorder=0)
        plt.xlabel('Set Point')
        plt.ylabel('Power (MW)')
        plt.legend()
        plt.grid(True)
        plt.savefig(bin_plots_path + r'\Dynamic_Binning_Plot.png')
        plt.close('all')
        '''

    def generate_log_ramp_curve(self, p_start, p_finish, ramp_rate, numsteps, pulses_per_step):
        '''

        '''
        # we work in base ramp_rate
        curve_p_finish = 1.01 * p_finish
        x_start = math.log(1 - (p_start / curve_p_finish), ramp_rate)
        x_finish = math.log(1 - (p_finish / curve_p_finish) / ramp_rate)

        x_step = (x_finish - x_start) / numsteps
        curve_powers = [curve_p_finish * (1.00 - ramp_rate ^ (x_start + x * x_step)) for x in range(0, numsteps + 1)]
        print(rf_conditioning_data.log_ramp_curve )

        x = np.linspace(0, 2 * np.pi, 10)
        y = np.sin(x)
        bin_X = rf_conditioning_data.binned_amp_vs_kfpow['BIN_X']
        bin_Y = rf_conditioning_data.binned_amp_vs_kfpow['BIN_mean']

        required_set_points = np.interp( curve_powers, bin_Y, bin_X)

        print("required_set_points = ", required_set_points)

        rf_conditioning_data.log_ramp_curve = [ [pulses_per_step, amp_sp] for amp_sp in  required_set_points  ]

        rf_conditioning_data.log_ramp_curve_index = 0

    def get_new_set_point(self, req_delta_pwr):
        '''
            using the binned data and the current amp_sp kf_power, estimate teh setpoint required to change the power by req_delta_pwr

        get_new_set_point(req_delta_pwr)
                               
            if req_delta_pwr < 0: ramping_down
            if req_delta_pwr > 0: ramping_up
            
            get the binned data to fit, this shoudl be a function
            
            if binned data is bad : 
                if ramping_down: return negative default
                if ramping_up  : return positive default

            if binned data is good: fit
                estimate amp_sp for current_power +  req_delta_pwr  (!!req_delta_pwr can be negative!!)
                do the fit to get predicted_sp

                check the valididty of the predicted_sp
                
                    if  ramping_down and predicted_sp >= current_sp: default 
                    if  ramping_up and predicted_sp <= current_sp: default
                    
                    if ramping_up and predicted_sp - current_sp   > 'MAX_DELTA_AMP_SP': default (or max?)
                    if ramping_down and current_sp - predicted_sp > 'MAX_DELTA_AMP_SP': default (or max?)

        '''
        set_point_to_return = ramping_down = ramping_up = None
        if req_delta_pwr < 0:
            ramping_down = True
            ramping_up = False
        elif req_delta_pwr > 0:
            ramping_down = False
            ramping_up = True
        else:
            print("ERROR req_delta_pwr == 0")
        [data_to_fit_x, data_to_fit_y, num_bin_y_equal_zero] = self.get_populated_fullbins_below_current_sp()

        current_amp_sp = int(self.values[rf_conditioning_data.amp_sp])  # i dn't think we should do int here
        current_power = rf_conditioning_data.amp_vs_kfpow_running_stat[current_amp_sp][1]
        requested_power = int(current_power + req_delta_pwr)
        num_full_bins_fit = self.config.raw_config_data['NUM_SET_POINTS_TO_FIT']
        default_increase = current_amp_sp + self.config.raw_config_data['DEFAULT_RF_INCREASE_LEVEL']
        default_decrease = current_amp_sp - self.config.raw_config_data['DEFAULT_RF_INCREASE_LEVEL']
        max_delta_power = self.config.raw_config_data['MAX_DELTA_AMP_SP']

        if len(data_to_fit_x) < num_full_bins_fit:
            self.values[rf_conditioning_data.last_ramp_method] = ramp_method.DEFAULT__TOO_FEW_BINS
            if ramping_up:
                set_point_to_return = default_increase
            elif ramping_down:
                set_point_to_return = default_decrease
            print('Not enough non-zero buns to fit to. Current number of non-zero bins = {}'.format(num_bin_y_equal_zero))
        elif (len(data_to_fit_x) - num_bin_y_equal_zero) < num_full_bins_fit:
            self.values[rf_conditioning_data.last_ramp_method] = ramp_method.DEFAULT__ENOUGH_BINS__ZERO_IN_LIST__NOT_ENOUGH_NON_ZERO
            if ramping_up:
                set_point_to_return = default_increase
            elif ramping_down:
                set_point_to_return = default_decrease
            self.logger.message('Less than {} non-zero data points in the binned data to fit.'.format(num_full_bins_fit))
            self.logger.message(
                'Ramping using default value of {} from {} to {}'.format(self.config.raw_config_data['DEFAULT_RF_INCREASE_LEVEL'], current_amp_sp,
                                                                         set_point_to_return))
        else:
            # crop to numer set points to fit
            data_to_fit_x2 = data_to_fit_x[-self.config.raw_config_data['NUM_SET_POINTS_TO_FIT']:]
            data_to_fit_y2 = data_to_fit_y[-self.config.raw_config_data['NUM_SET_POINTS_TO_FIT']:]

            # Call in various fit methods
            sp_slf = self.slf_amp_kfpow_data(requested_power)
            sp_quad_all = self.poly_amp_kfpow_all_data(requested_power)
            sp_quad_current = self.poly_amp_kfpow_current_sp(requested_power)
            sp_quad_current_sp_to_fit = self.poly_amp_kfpow_current_sp_to_fit(requested_power)

            print('sp_slf = {}\nsp_quad_all = {}\nsp_quad_current = {}\nsp_quad_current_sp_to_fit = {}\n'
                  .format(sp_slf, sp_quad_all, sp_quad_current,  sp_quad_current_sp_to_fit))



            print('\ntype(sp_slf) = {}\ntype(sp_quad_all) = {}\ntype(sp_quad_current) = {}\ntype('
                  'sp_quad_current_sp_to_fit) = {}'.format(type(sp_slf), type(sp_quad_all), type(sp_quad_current), type(sp_quad_current_sp_to_fit)))


            # Recor returned fit results to values dict:

            self.values[rf_conditioning_data.SP_SLF] = sp_slf
            self.values[rf_conditioning_data.SP_QUAD_ALL] = sp_quad_all
            self.values[rf_conditioning_data.SP_QUAD_CURRENT] = sp_quad_current
            self.values[rf_conditioning_data.SP_QUAD_CURRENT_SP_TO_FIT] = sp_quad_current_sp_to_fit


            # assign which fitting method amp_sp to use
            predicted_sp = sp_slf

            # check the valididty of the predicted_sp
            if abs(predicted_sp - current_amp_sp) > max_delta_power:
                self.values[rf_conditioning_data.last_ramp_method] = ramp_method.DEFAULT__DELTA_GTRTHN_MAX
                self.logger.message('')
                if ramping_up:
                    set_point_to_return = default_increase
                    self.logger.message('DEFAULT__DELTA_GTRTHN_MAX deafault = {}'.format(default_increase))
                if ramping_down:
                    set_point_to_return = default_decrease
                    self.logger.message('DEFAULT__DELTA_GTRTHN_MAX deafault = {}'.format(default_decrease))

            elif ramping_up and predicted_sp < current_amp_sp:
                self.values[rf_conditioning_data.last_ramp_method] = ramp_method.PREDICTED_SP_GRTRTHN_CURRENT_SP
                self.logger.message('Predicted sp is less than current_sp! returning current_sp + {}'.format(default_increase))

                set_point_to_return = default_increase

            elif ramping_down and predicted_sp > current_amp_sp:
                self.values[rf_conditioning_data.last_ramp_method] = ramp_method.PREDICTED_SP_GRTRTHN_CURRENT_SP
                self.logger.message('Predicted sp is less than current_sp! returning current_sp + {}'.format(default_decrease))

                set_point_to_return = default_decrease

            elif ramping_up and predicted_sp == current_amp_sp:
                self.values[rf_conditioning_data.last_ramp_method] = ramp_method.DEFAULT__FLAT_RAMP
                self.logger.message('Predicted sp ==  current_sp! returning current_sp + {}'.format(default_increase))

                set_point_to_return = default_increase

            elif ramping_down and predicted_sp == current_amp_sp:
                self.values[rf_conditioning_data.last_ramp_method] = ramp_method.DEFAULT__FLAT_RAMP
                self.logger.message('Predicted sp ==  current_sp! returning current_sp + {}'.format(default_decrease))
                set_point_to_return = default_decrease
            else:
                set_point_to_return = predicted_sp
        return set_point_to_return

    def get_populated_fullbins_below_current_sp(self):
        '''
            return bins, whose entire width is below the current amp_sp AND that haeve real data in them
        '''
        # make sure the bin data is up to date
        self.update_binned_data()
        current_amp_sp = self.values[rf_conditioning_data.amp_sp]
        num_fullbins_below_current_sp = len([b for b in self.binned_amp_vs_kfpow['BIN_edges'] if b < current_amp_sp]) -1 #-1 due to  bin edges
        bin_x_to_fit = self.binned_amp_vs_kfpow['BIN_X'][0:num_fullbins_below_current_sp]
        bin_y_to_fit = self.binned_amp_vs_kfpow['BIN_mean'][0:num_fullbins_below_current_sp]
        # now remove unpopulated bins, (i.e bin_mean = 0 (bin_mean is the Y value (the mean power for this bin)
        data_to_fit_x = []
        data_to_fit_y = []
        num_bin_y_equal_zero = 0
        for (bin_x,bin_mean) in zip(bin_x_to_fit,bin_y_to_fit):
            if bin_mean > 0.0:
                data_to_fit_x.append(bin_x)
                data_to_fit_y.append(bin_mean)
            else:
                num_bin_y_equal_zero += 1
        data_to_fit_x = np.array(data_to_fit_x)
        data_to_fit_y = np.array(data_to_fit_y)
        print('FINAL DATA TO FIT x  = {}\ny = {}, num_y_zeroes = {}'.format(data_to_fit_x, data_to_fit_y,num_bin_y_equal_zero))
        return [data_to_fit_x, data_to_fit_y, num_bin_y_equal_zero]

    def slf_amp_kfpow_data(self, requested_power):

        num_sp_to_fit = self.config.raw_config_data['NUM_SET_POINTS_TO_FIT']
        use_max_sp = False
        data_to_fit_x, data_to_fit_y = self.get_data_for_polyfit(num_sp_to_fit,  use_max_sp)

        # Exclude the origin from X and Y data:
        data_to_fit_x = data_to_fit_x[1:]
        data_to_fit_y = data_to_fit_y[1:]

        self.values[rf_conditioning_data.old_c] = self.values[rf_conditioning_data.c]
        self.values[rf_conditioning_data.old_m] = self.values[rf_conditioning_data.m]
        self.values[rf_conditioning_data.old_x_min] = self.values[rf_conditioning_data.x_min]
        self.values[rf_conditioning_data.old_y_max] = self.values[rf_conditioning_data.y_max]
        self.values[rf_conditioning_data.old_y_min] = self.values[rf_conditioning_data.y_min]
        self.values[rf_conditioning_data.old_x_max] = self.values[rf_conditioning_data.x_max]
        # NOW WE MUST FIT
        p = np.polyfit(data_to_fit_x, data_to_fit_y, 1, rcond=None, full=False)  # , w=np.array(err_tofit))  # [0][1]
        m = p[0]
        c = p[1]
        predicted_sp = int((requested_power - c) / m)
        #print 'm = {}\nc = {}\nPredicted SP = {}'.format(m, c, predicted_sp)
        self.values[rf_conditioning_data.x_min] = min(data_to_fit_x)
        self.values[rf_conditioning_data.x_max] = max(data_to_fit_x)
        self.values[rf_conditioning_data.y_min] = min(data_to_fit_y)
        self.values[rf_conditioning_data.y_max] = max(data_to_fit_y)
        self.values[rf_conditioning_data.c] = c
        self.values[rf_conditioning_data.m] = m
        predicted_sp = int(predicted_sp)
        return float(predicted_sp)

    def poly_fit_2order(self, x, y, requested_power):
        '''
            Takes in x and y data then fits a quadratic function to data
            Using that fitted function it then gives a precicted x-value (amp_sp) for a given y-value (reqwuested_power)
            the predicted_sp is then converted into an integer to remove any fractional value then converted into a float to have the form xxxx.0
        '''

        p = np.polyfit(x, y, 2, rcond=None, full=False)
        p0 = c = p[0]
        p1 = b = p[1]
        p2 = a = p[2]

        #I think it might be the formula, can't see any other errors.. although the plots are looking iffy!
        #i like that answer

        predicted_sp = -b + np.sqrt(b**2.0 - 4.0*a*c + 4.0 * c * requested_power ) / (2.0 * c)

        polyfit_2order = [p0*i**2 + p1*i + p2 for i in x]

        predicted_sp = int(predicted_sp)
        return float(predicted_sp), p0, p1, p2, polyfit_2order

    def poly_amp_kfpow_all_data(self, requested_power):
        '''
            Uses all available non-zero binned data for a quadratic fit
        '''
        rcd = rf_conditioning_data
        use_max_sp = True
        num_sp_to_fit = 0
        data_to_fit_x, data_to_fit_y = self.get_data_for_polyfit(num_sp_to_fit,  use_max_sp)

        # NOW WE MUST FIT
        predicted_sp, p0, p1, p2, polyfit_2order = self.poly_fit_2order(data_to_fit_x, data_to_fit_y, requested_power)

        print('From poly_amp_kfpow_all_data:\npredicted_sp = {}\np0 = {}\np1 = {}\np2 = {}\n'.format(predicted_sp, p0, p1, p2))

        self.values[rcd.p0_all] = p0
        self.values[rcd.p1_all] = p1
        self.values[rcd.p2_all] = p2
        self.values[rcd.polyfit_2order_X_all] = data_to_fit_x
        self.values[rcd.polyfit_2order_Y_all] = polyfit_2order

        bin_plots_path = r'C:\Users\dlerlp\Documents\RF_Conditioning_20200720'

        #bin_mean = [i / 10 ** 6 for i in data_to_fit_y]
        polyfit_2order = [p0*i**2 + p1 for i in data_to_fit_x]
        plt.scatter(data_to_fit_x, data_to_fit_y, c='k', s=25, marker='x', label='Binned Mean', zorder=0)
        plt.plot(data_to_fit_x, polyfit_2order, ls='--', lw=0.7, color='r', label='2nd order np.polyfit')
        plt.scatter(predicted_sp, requested_power, marker='x', s=80, c='c', label='Predicted data point')
        plt.xlabel('Set Point')
        plt.ylabel('Power (MW)')
        plt.legend()
        plt.grid(True)
        plt.savefig(bin_plots_path + r'\Second_order_np_polyfit_all_data.png')
        plt.close('all')

        predicted_sp = int(predicted_sp)
        return float(predicted_sp)

    def poly_amp_kfpow_current_sp_to_fit(self, requested_power):
        rcd = rf_conditioning_data
        use_max_sp = False
        num_sp_to_fit = self.config.raw_config_data['NUM_SET_POINTS_TO_FIT']
        data_to_fit_x, data_to_fit_y = self.get_data_for_polyfit(num_sp_to_fit, use_max_sp)

        print('From poly_amp_kfpow_current_sp_to_fit:\ndata_to_fit_x_no_zero = {}\ndata_to_fit_y_no_zero = {}'.format(data_to_fit_x,
                                                                                                         data_to_fit_y))

        # NOW WE MUST FIT
        predicted_sp, p0, p1, p2, polyfit_2order = self.poly_fit_2order(data_to_fit_x, data_to_fit_y, requested_power)

        print('From poly_amp_kfpow_current_sp_to_fit:\npolyfit_2order = {}\npredicted_sp = {}\np0 = {}\np1 = {}\np2 = {}\n'.format(polyfit_2order,predicted_sp,
                                                                                                                                   p0,p1, p2))

        self.values[rcd.p0_current_sp_to_fit] = p0
        self.values[rcd.p1_current_sp_to_fit] = p1
        self.values[rcd.p2_current_sp_to_fit] = p2
        self.values[rcd.polyfit_2order_X_current_sp_to_fit] = data_to_fit_x
        self.values[rcd.polyfit_2order_Y_current_sp_to_fit] = polyfit_2order


        #self.values[rcd.polyfit_2order_X_current_sp_to_fit] = np.insert(self.values[rcd.polyfit_2order_X_current_sp_to_fit], -1, predicted_sp)
        #self.values[rcd.polyfit_2order_Y_current_sp_to_fit] = np.insert(self.values[rcd.polyfit_2order_Y_current_sp_to_fit], -1, requested_power)

        bin_plots_path = r'C:\Users\dlerlp\Documents\RF_Conditioning_20200720'

        #bin_mean = [i / 10 ** 6 for i in data_to_fit_y]

        plt.scatter(data_to_fit_x, data_to_fit_y, c='k', s=25, marker='x', label='Binned Mean', zorder=0)
        plt.plot(data_to_fit_x, polyfit_2order, ls='--', lw=0.7, color='r', label='2nd order np.polyfit')
        plt.scatter(predicted_sp, requested_power, marker='x', s=80, c='c', label='Predicted data point')
        plt.xlabel('Set Point')
        plt.ylabel('Power (MW)')
        plt.legend()
        plt.grid(True)
        plt.savefig(bin_plots_path + r'\Second_order_np_polyfit_num_sp_data.png')
        plt.close('all')

        predicted_sp = int(predicted_sp)
        return float(predicted_sp)

    def poly_amp_kfpow_current_sp(self, requested_power):
        rcd = rf_conditioning_data
        use_max_sp = False
        num_sp_to_fit = 0
        data_to_fit_x, data_to_fit_y = self.get_data_for_polyfit( num_sp_to_fit,  use_max_sp)

        print('From poly_amp_kfpow_current_sp:\ndata_to_fit_x_no_zero = {}\ndata_to_fit_y_no_zero = {}'.format(data_to_fit_x,
                                                                                                         data_to_fit_y))

        # NOW WE MUST FIT
        predicted_sp, p0, p1, p2, polyfit_2order = self.poly_fit_2order(data_to_fit_x, data_to_fit_y, requested_power)

        print('From poly_amp_kfpow_current_sp:\npredicted_sp = {}\np0 = {}\np1 = {}\np2 = {}\n'.format(predicted_sp, p0, p1, p2))

        self.values[rcd.p0_current_sp] = p0
        self.values[rcd.p1_current_sp] = p1
        self.values[rcd.p2_current_sp] = p2
        self.values[rcd.polyfit_2order_X_current_sp] = data_to_fit_x
        self.values[rcd.polyfit_2order_Y_current_sp] = polyfit_2order

        self.values[rcd.polyfit_2order_X_current_sp] = np.insert(self.values[rcd.polyfit_2order_X_current_sp], -1, predicted_sp)
        self.values[rcd.polyfit_2order_Y_current_sp] = np.insert(self.values[rcd.polyfit_2order_Y_current_sp], -1, requested_power)

        bin_plots_path = r'C:\Users\dlerlp\Documents\RF_Conditioning_20200720'

        #bin_mean = [i / 10 ** 6 for i in data_to_fit_y]

        plt.scatter(data_to_fit_x, data_to_fit_y, c='k', s=25, marker='x', label='Binned Mean', zorder=0)
        plt.plot(data_to_fit_x, polyfit_2order, ls='--', lw=0.7, color='r', label='2nd order np.polyfit')
        plt.scatter(predicted_sp, requested_power, marker='x', s=80, c='c', label='Predicted data point')
        plt.xlabel('Set Point')
        plt.ylabel('Power (MW)')
        plt.legend()
        plt.grid(True)
        plt.savefig(bin_plots_path + r'\Second_order_np_polyfit_num_sp_data.png')
        plt.close('all')

        predicted_sp = int(predicted_sp)
        return float(predicted_sp)

    def get_data_for_polyfit(self, num_sp_to_fit,  use_max_sp):
        '''
            This returns the binned data required for various fitting methods
            if max_sp == True then ALL available non-zero binned data will be used.
            if max_sp == False AND if sp_to_fit == 0 then ALL available non-zero binned data BELOW current amp_sp will be used.
            if max_sp == False AND if sp_to_fit == 0 then the trailing [num_sp_to_fit] non-zero binned data BELOW current will be
            used.
        '''

        rcd = rf_conditioning_data
        self.update_binned_data()
        current_amp_sp = self.values[rcd.amp_sp]
        data_to_fit_x = rcd.binned_amp_vs_kfpow['BIN_X']
        data_to_fit_y = rcd.binned_amp_vs_kfpow['BIN_mean']

        # Find all non-zero binnded data
        data_to_fit_x = [data_to_fit_x[i] for i in range(len(data_to_fit_x)) if data_to_fit_y[i] > 0.0]
        data_to_fit_y = [data_to_fit_y[i] for i in range(len(data_to_fit_y)) if data_to_fit_y[i] > 0.0]

        # Prepend with origin (amp_sp =0 Crocodiles, kfpwr = 0.0W)
        data_to_fit_x.insert(0, 0.0)
        data_to_fit_y.insert(0, 0.0)
        #data_to_fit_x.tolist()
        #data_to_fit_y.tolist()

        print('\n\nFrom get_data_for_polyfit\ndata_to_fit_x = {}\ndata_to_fit_y = {}'.format(data_to_fit_x, data_to_fit_y))

        # If max_sp == True return ALL viable binned data
        if use_max_sp:
            return data_to_fit_x, data_to_fit_y

        # If max_sp == False use only viable binned data that is below the current amp_sp
        else:
            num_fullbins_below_current_sp = len([b for b in self.binned_amp_vs_kfpow['BIN_edges'] if b < current_amp_sp]) -1 #-1 due to  bin edges
            data_to_fit_x = data_to_fit_x[0:num_fullbins_below_current_sp]
            data_to_fit_y = data_to_fit_y[0:num_fullbins_below_current_sp]

            # If max_sp == False AND if sp_to_fit == 0 then ALL available non-zero binned data BELOW current amp_sp will be returned.
            #if max_sp == False AND if sp_to_fit > 0 then the trailing [num_sp_to_fit] non-zero binned data BELOW current will be returned.
            if num_sp_to_fit > 0: #TODO replace sp_to_fit ==  0 = 'use all data' with something more logical

                data_to_fit_x = data_to_fit_x[-num_sp_to_fit:]
                data_to_fit_y = data_to_fit_y[-num_sp_to_fit:]
                data_to_fit_x.insert(0, 0.0)
                data_to_fit_y.insert(0, 0.0)

            return data_to_fit_x, data_to_fit_y

























    '''Bining dictionary'''

    dummy_np_float_64 = np_float64(-9999.9999)
    dummy_float = -9999.9999
    dummy_int = -9999999
    dummy_state = state.UNKNOWN

    binned_amp_vs_kfpow = {}  # A list of the keys for values
    bin_keys = []  # A list of the keys for values

    '''  This is a list of teh amp_sp value at the center of each bin '''
    BIN_X = 'BIN_X'
    bin_keys.append(BIN_X)
    binned_amp_vs_kfpow[BIN_X] = [dummy_float]

    ''' this a list of the mean kfpow for each bin  '''
    BIN_mean = 'BIN_mean'
    bin_keys.append(BIN_mean)
    binned_amp_vs_kfpow[BIN_mean] = dummy_float

    ''' This is a list of the  amp_sp edges for each bin edge (plus the right had bin)  '''
    BIN_edges = 'BIN_edges'
    bin_keys.append(BIN_edges)
    binned_amp_vs_kfpow[BIN_edges] = dummy_float

    ''' This is hpow mnay data points are in each bin '''
    BIN_pop = 'BIN_pop'
    bin_keys.append(BIN_pop)
    binned_amp_vs_kfpow[BIN_pop] = dummy_float

    BIN_pulses = 'BIN_pulses'
    bin_keys.append(BIN_pulses)
    binned_amp_vs_kfpow[BIN_pulses] = dummy_float

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

    values = {}  # A list of the keys for values
    all_value_keys = []  # A list of the keys for values

    ramp_mode = "ramp_mode"
    all_value_keys.append(ramp_mode)
    values[ramp_mode] = ramp_method.LOG_RAMP
    values[ramp_mode] = ramp_method.NORMAL_RAMP

    # keys for all the data we monitor
    main_can_ramp = 'main_can_ramp'
    all_value_keys.append(main_can_ramp)
    values[main_can_ramp] = False # CHECK TYPE

    # keys for all the data we monitor
    time_stamp = 'time_stamp'
    all_value_keys.append(time_stamp)
    values[time_stamp] = dummy_float  # CHECK TYPE

    # STATUS PF MAIN MONITORS
    vac_spike_status = 'vac_spike_status'
    all_value_keys.append(vac_spike_status)
    values[vac_spike_status] = dummy_state

    # STATUS PF MAIN MONITORS
    last_vac_spike_status = 'last_vac_spike_status'
    all_value_keys.append(last_vac_spike_status)
    values[last_vac_spike_status] = dummy_state

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
    all_value_keys.append(rev_kly_pwr)
    values[rev_kly_pwr] = dummy_float

    rev_cav_pwr = 'rev_cav_pwr'
    all_value_keys.append(rev_cav_pwr)
    values[rev_cav_pwr] = dummy_float

    probe_pwr = 'probe_pwr'
    all_value_keys.append(probe_pwr)
    values[probe_pwr] = dummy_float

    fwd_cav_pha = 'fwd_cav_pha'
    all_value_keys.append(fwd_cav_pha)
    values[fwd_cav_pha] = dummy_float

    fwd_kly_pha = 'fwd_kly_pha'
    all_value_keys.append(fwd_kly_pha)
    values[fwd_kly_pha] = dummy_float

    rev_kly_pha = 'rev_kly_pha'
    all_value_keys.append(rev_kly_pha)
    values[rev_kly_pha] = dummy_float

    rev_cav_pha = 'rev_cav_pha'
    all_value_keys.append(rev_cav_pha)
    values[rev_cav_pha] = dummy_float

    probe_pha = 'probe_pha'
    all_value_keys.append(probe_pha)
    values[probe_pha] = dummy_float


    delta_kfpow = 'delta_kfpow'
    all_value_keys.append(delta_kfpow)
    values[delta_kfpow] = dummy_float



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
    values[breakdown_status] = state.UNKNOWN

    last_breakdown_status = 'last_breakdown_status'
    all_value_keys.append(last_breakdown_status)
    values[last_breakdown_status] = state.UNKNOWN

    breakdown_rate_aim = 'breakdown_rate_aim'
    all_value_keys.append(breakdown_rate_aim)
    values[breakdown_rate_aim] = dummy_int

    # these are values from the pulse_breakdown_log
    log_pulse_count = 'log_pulse_count'
    all_value_keys.append(log_pulse_count)
    values[log_pulse_count] = dummy_int
    # log_breakdown_count = 'log_breakdown_count'

    event_pulse_count_zero = 'event_pulse_count_zero'
    all_value_keys.append(event_pulse_count_zero)
    values[event_pulse_count_zero] = dummy_int

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

    breakdown_rate_low = 'breakdown_rate_low'
    all_value_keys.append(breakdown_rate_low)
    values[breakdown_rate_low] = state.UNKNOWN

    last_106_bd_count = 'last_106_bd_count'
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

    rfprot_good = 'rfprot_good'
    all_value_keys.append(rfprot_good)
    values[rfprot_good] = False

    modulator_state = 'modulator_state'
    all_value_keys.append(modulator_state)
    values[modulator_state] = state.UNKNOWN

    modulator_good = 'modulator_good'
    all_value_keys.append(modulator_good)
    values[modulator_good] = False

    can_rf_output_state_OLD = 'can_rf_output_state_OLD'
    all_value_keys.append(can_rf_output_state_OLD)
    values[can_rf_output_state_OLD] = state.UNKNOWN

    can_rf_output_state = 'can_rf_output_state'
    all_value_keys.append(can_rf_output_state)
    values[can_rf_output_state] = state.UNKNOWN

    # This i sthe "general interloac" and should be re-named to reflect this
    llrf_interlock = 'llrf_interlock'  # The read value from EPICS
    all_value_keys.append(llrf_interlock)
    values[llrf_interlock] = state.UNKNOWN

    llrf_interlock_status = 'llrf_interlock_status'  # the apps internal state, good, new_bad etc
    all_value_keys.append(llrf_interlock_status)
    values[llrf_interlock_status] = state.UNKNOWN

    # the state of the "Trace interlocks" these are where you can specify a power that disables LLRF
    llrf_trace_interlock = 'llrf_trace_interlock'  # The read value from EPICS
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

    pulse_length_status = 'pulse_length_status'  # the apps internal state, good, new_bad etc
    all_value_keys.append(pulse_length_status)
    values[pulse_length_status] = state.UNKNOWN

    llrf_output = 'llrf_output'  # RF Output on LLRF panel
    all_value_keys.append(llrf_output)
    values[llrf_output] = state.UNKNOWN

    llrf_output_status = 'llrf_output_status'  # the apps internal state, good, new_bad etc
    all_value_keys.append(llrf_output_status)
    values[llrf_output_status] = state.UNKNOWN

    llrf_ff_amp_locked = 'llrf_ff_amp_locked'
    all_value_keys.append(llrf_ff_amp_locked)
    values[llrf_ff_amp_locked] = state.UNKNOWN

    llrf_ff_amp_locked_status = 'llrf_ff_amp_locked_status'  # the apps internal state, good, new_bad etc
    all_value_keys.append(llrf_ff_amp_locked_status)
    values[llrf_ff_amp_locked_status] = state.UNKNOWN

    llrf_ff_ph_locked = 'llrf_ff_ph_locked'
    all_value_keys.append(llrf_ff_ph_locked)
    values[llrf_ff_ph_locked] = state.UNKNOWN

    llrf_ff_ph_locked_status = 'llrf_ff_ph_locked_status'  # the apps internal state, good, new_bad etc
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
    values[required_pulses] = dummy_int

    next_power_change = 'next_power_change'
    all_value_keys.append(next_power_change)
    values[next_power_change] = dummy_float

    last_power_change = 'last_power_change'
    all_value_keys.append(last_power_change)
    values[last_power_change] = dummy_float


    log_pulse_length = 'log_pulse_length'
    all_value_keys.append(log_pulse_length)
    values[log_pulse_length] = dummy_float

    last_mean_power = 'last_mean_power'
    all_value_keys.append(last_mean_power)
    values[last_mean_power] = dummy_float

    gui_can_rf_output = 'gui_can_rf_output'
    all_value_keys.append(gui_can_rf_output)
    values[gui_can_rf_output] = True

    amp_ff = 'amp_ff'
    all_value_keys.append(amp_ff)
    values[amp_ff] = dummy_int

    amp_sp = 'amp_sp'
    all_value_keys.append(amp_sp)
    values[amp_sp] = dummy_float

    kfpower_at_last_amp_sp = 'kfpower_at_last_amp_sp'
    all_value_keys.append(kfpower_at_last_amp_sp)
    values[kfpower_at_last_amp_sp] = dummy_float

    last_amp_sp = 'last_amp_sp'
    all_value_keys.append(last_amp_sp)
    values[last_amp_sp] = dummy_float

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
    #values[x_min] = dummy_np_float_64
    values[x_min] = dummy_float

    x_max = 'x_max'
    all_value_keys.append(x_max)
    #values[x_max] = dummy_np_float_64
    values[x_max] = dummy_float

    old_x_min = 'old_x_min'
    all_value_keys.append(old_x_min)
    values[old_x_min] = dummy_float

    old_x_max = 'old_x_max'
    all_value_keys.append(old_x_max)
    values[old_x_max] = dummy_float

    y_min = 'y_min'
    all_value_keys.append(y_min)
    #values[y_min] = dummy_np_float_64
    values[y_min] = dummy_np_float_64

    y_max = 'y_max'
    all_value_keys.append(y_max)
    values[y_max] = dummy_np_float_64

    old_y_min = 'old_y_min'
    all_value_keys.append(old_y_min)
    values[old_y_min] = dummy_np_float_64

    old_y_max = 'old_y_max'
    all_value_keys.append(old_y_max)
    values[old_y_max] = dummy_np_float_64

    c = 'c'
    all_value_keys.append(c)
    values[c] = dummy_np_float_64

    m = 'm'
    all_value_keys.append(m)
    values[m] = dummy_np_float_64

    p0_current_sp = 'p0_current_sp'
    all_value_keys.append(p0_current_sp)
    values[p0_current_sp] = dummy_np_float_64

    p1_current_sp = 'p1_current_sp'
    all_value_keys.append(p1_current_sp)
    values[p1_current_sp] = dummy_np_float_64

    p2_current_sp = 'p2_current_sp'
    all_value_keys.append(p2_current_sp)
    values[p2_current_sp] = dummy_np_float_64

    p0_current_sp_to_fit = 'p0_current_sp_to_fit'
    all_value_keys.append(p0_current_sp_to_fit)
    values[p0_current_sp_to_fit] = dummy_np_float_64

    p1_current_sp_to_fit = 'p1_current_sp_to_fit'
    all_value_keys.append(p1_current_sp_to_fit)
    values[p1_current_sp_to_fit] = dummy_np_float_64

    p2_current_sp_to_fit = 'p2_current_sp_to_fit'
    all_value_keys.append(p2_current_sp_to_fit)
    values[p2_current_sp_to_fit] = dummy_np_float_64

    p0_all = 'p0_all'
    all_value_keys.append(p0_all)
    values[p0_all] = dummy_np_float_64

    p1_all = 'p1_all'
    all_value_keys.append(p1_all)
    values[p1_all] = dummy_np_float_64

    p2_all = 'p2_all'
    all_value_keys.append(p2_all)
    values[p2_all] = dummy_np_float_64


    # TODO: this is temporary! remove asap

    polyfit_2order_X_all = 'polyfit_2order_X_all'
    all_value_keys.append(polyfit_2order_X_all)
    values[polyfit_2order_X_all] = [dummy_np_float_64]
    excluded_key_list.append(polyfit_2order_X_all)

    polyfit_2order_Y_all = 'polyfit_2order_Y_all'
    all_value_keys.append(polyfit_2order_Y_all)
    values[polyfit_2order_Y_all] = [dummy_np_float_64]
    excluded_key_list.append(polyfit_2order_Y_all)

    polyfit_2order_X_current_sp = 'polyfit_2order_X_current_sp'
    all_value_keys.append(polyfit_2order_X_current_sp)
    values[polyfit_2order_X_current_sp] = [dummy_np_float_64]
    excluded_key_list.append(polyfit_2order_X_current_sp)

    polyfit_2order_Y_current_sp = 'polyfit_2order_Y_current_sp'
    all_value_keys.append(polyfit_2order_Y_current_sp)
    values[polyfit_2order_Y_current_sp] = [dummy_np_float_64]
    excluded_key_list.append(polyfit_2order_Y_current_sp)

    polyfit_2order_X_current_sp_to_fit = 'polyfit_2order_X_current_sp_to_fit'
    all_value_keys.append(polyfit_2order_X_current_sp_to_fit)
    values[polyfit_2order_X_current_sp_to_fit] = [dummy_np_float_64]
    excluded_key_list.append(polyfit_2order_X_current_sp_to_fit)


    polyfit_2order_Y_current_sp_to_fit = 'polyfit_2order_Y_current_sp_to_fit'
    all_value_keys.append(polyfit_2order_Y_current_sp_to_fit)
    values[polyfit_2order_Y_current_sp_to_fit] = [dummy_np_float_64]
    excluded_key_list.append(polyfit_2order_Y_current_sp_to_fit)
    # TODO ^^^^^ ##########################

    SP_SLF = 'SP_SLF'
    all_value_keys.append(SP_SLF)
    values[SP_SLF] = dummy_float

    SP_QUAD_ALL = 'SP_QUAD_ALL'
    all_value_keys.append(SP_QUAD_ALL)
    values[SP_QUAD_ALL] = dummy_float

    SP_QUAD_CURRENT = 'SP_QUAD_CURRENT'
    all_value_keys.append(SP_QUAD_CURRENT)
    values[SP_QUAD_CURRENT] = dummy_float

    SP_QUAD_CURRENT_SP_TO_FIT = 'SP_QUAD_CURRENT_SP_TO_FIT'
    all_value_keys.append(SP_QUAD_CURRENT_SP_TO_FIT)
    values[SP_QUAD_CURRENT_SP_TO_FIT] = dummy_float

    old_c = 'old_c'
    all_value_keys.append(old_c)
    values[old_c] = dummy_np_float_64

    old_m = 'old_m'
    all_value_keys.append(old_m)
    values[old_m] = dummy_np_float_64

    # latest_ramp_up_sp = 'latest_ramp_up_sp'
    last_sp_above_100 = 'last_sp_above_100'
    all_value_keys.append(last_sp_above_100)
    values[last_sp_above_100] = dummy_float

    max_sp_increase = 'max_sp_increase'
    all_value_keys.append(max_sp_increase)
    values[max_sp_increase] = dummy_float

    next_sp_decrease = 'next_sp_decrease'
    all_value_keys.append(next_sp_decrease)
    values[next_sp_decrease] = dummy_float

    vac_level_can_ramp = 'vac_level_can_ramp'  # Flag which is T if we can ramp and f if we cna't base don current vac level
    all_value_keys.append(vac_level_can_ramp)
    values[vac_level_can_ramp] = False

    gui_can_ramp = 'gui_can_ramp'  # Flag which is T if we can ramp and f if we
    # cna't base don current vac level
    all_value_keys.append(gui_can_ramp)
    values[gui_can_ramp] = False

    gui_can_ramp = 'gui_can_ramp'  # Flag which is T if we can ramp and f if we
    # cna't base don current vac level
    all_value_keys.append(gui_can_ramp)
    values[gui_can_ramp] = False

    last_ramp_method = '_ramp_method'  # Flag which is T if we can ramp and f if we
    # cna't base don current vac level
    all_value_keys.append(last_ramp_method)
    values[last_ramp_method] = ramp_method.UNKNOWN

    # we know there will be some LLRF involved
    # llrf_type = LLRF_TYPE.UNKNOWN_TYPE

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

    # latest_ramp_up_sp = 0

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
    # values[can_rf_output_state_OLD] = state.UNKNOWN

    # sss
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
    # values[breakdown_rate_low] = dummy_bool
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
    # values[next_power_change] = -1
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

    vac_decay_mode_val = "vac_decay_mode_val"
    expert_value_keys.append(vac_decay_mode_val)
    expert_values[vac_decay_mode_val] = "STRING"

    vac_decay_level = "vac_decay_level"
    expert_value_keys.append(vac_decay_level)
    expert_values[vac_decay_level] = dummy_float

    vac_decay_time_val = "vac_decay_time_val"
    expert_value_keys.append(vac_decay_time_val)
    expert_values[vac_decay_time_val] = dummy_int

    vac_drop_amp = "vac_drop_amp"
    expert_value_keys.append(vac_drop_amp)
    expert_values[vac_drop_amp] = dummy_int

    vac_hi_pressure = "vac_hi_pressure"
    expert_value_keys.append(vac_hi_pressure)
    expert_values[vac_hi_pressure] = dummy_float

    vac_spike_delta_val = "vac_spike_delta_val"
    expert_value_keys.append(vac_spike_delta_val)
    expert_values[vac_spike_delta_val] = dummy_float

    vac_num_samples_to_average_val = "vac_num_samples_to_average_val"
    expert_value_keys.append(vac_num_samples_to_average_val)
    expert_values[vac_num_samples_to_average_val] = "STRING"

    vac_drop_amp_val = "vac_drop_amp_val"
    expert_value_keys.append(vac_drop_amp_val)
    expert_values[vac_drop_amp_val] = "STRING"

    ramp_when_hi = "ramp_when_hi"
    expert_value_keys.append(ramp_when_hi)
    expert_values[ramp_when_hi] = "STRING"

    vac_decay_mode = "vac_decay_mode"
    expert_value_keys.append(vac_decay_mode)
    expert_values[vac_decay_mode] = "STRING"

    vac_decay_level_val = "vac_decay_level_val"
    expert_value_keys.append(vac_decay_level_val)
    expert_values[vac_decay_level_val] = "STRING"

    vac_hi_pressure_val = "vac_hi_pressure_val"
    expert_value_keys.append(vac_hi_pressure_val)
    expert_values[vac_hi_pressure_val] = "STRING"

    ramp_when_hi_val = "ramp_when_hi_val"
    expert_value_keys.append(ramp_when_hi_val)
    expert_values[ramp_when_hi_val] = "STRING"

    vac_spike_check_time_val = "vac_spike_check_time_val"
    expert_value_keys.append(vac_spike_check_time_val)
    expert_values[vac_spike_check_time_val] = "STRING"

    vac_spike_check_time = "vac_spike_check_time"
    expert_value_keys.append(vac_spike_check_time)
    expert_values[vac_spike_check_time] = "STRING"

    is_breakdown_monitor_kf_pow = "is_breakdown_monitor_kf_pow"
    expert_value_keys.append(is_breakdown_monitor_kf_pow)
    expert_values[is_breakdown_monitor_kf_pow] = False

    is_breakdown_monitor_kr_pow = "is_breakdown_monitor_kr_pow"
    expert_value_keys.append(is_breakdown_monitor_kr_pow)
    expert_values[is_breakdown_monitor_kr_pow] = False

    is_breakdown_monitor_cf_pow = "is_breakdown_monitor_cf_pow"
    expert_value_keys.append(is_breakdown_monitor_cf_pow)
    expert_values[is_breakdown_monitor_cf_pow] = False

    is_breakdown_monitor_cr_pow = "is_breakdown_monitor_cr_pow"
    expert_value_keys.append(is_breakdown_monitor_cr_pow)
    expert_values[is_breakdown_monitor_cr_pow] = False

    is_breakdown_monitor_cp_pow = "is_breakdown_monitor_cp_pow"
    expert_value_keys.append(is_breakdown_monitor_cp_pow)
    expert_values[is_breakdown_monitor_cp_pow] = False

    is_breakdown_monitor_kf_pha = "is_breakdown_monitor_kf_pha"
    expert_value_keys.append(is_breakdown_monitor_kf_pha)
    expert_values[is_breakdown_monitor_kf_pha] = False

    is_breakdown_monitor_kr_pha = "is_breakdown_monitor_kr_pha"
    expert_value_keys.append(is_breakdown_monitor_kr_pha)
    expert_values[is_breakdown_monitor_kr_pha] = False

    is_breakdown_monitor_cf_pha = "is_breakdown_monitor_cf_pha"
    expert_value_keys.append(is_breakdown_monitor_cf_pha)
    expert_values[is_breakdown_monitor_cf_pha] = False

    is_breakdown_monitor_cr_pha = "is_breakdown_monitor_cr_pha"
    expert_value_keys.append(is_breakdown_monitor_cr_pha)
    expert_values[is_breakdown_monitor_cr_pha] = False

    is_breakdown_monitor_cp_pha = "is_breakdown_monitor_cp_pha"
    expert_value_keys.append(is_breakdown_monitor_cp_pha)
    expert_values[is_breakdown_monitor_cp_pha] = False

    mean_start_kf_pow = "mean_start_kf_pow"
    expert_value_keys.append(mean_start_kf_pow)
    expert_values[mean_start_kf_pow] = "STRING"

    mean_start_kr_pow = "mean_start_kr_pow"
    expert_value_keys.append(mean_start_kr_pow)
    expert_values[mean_start_kr_pow] = "STRING"

    mean_start_cf_pow = "mean_start_cf_pow"
    expert_value_keys.append(mean_start_cf_pow)
    expert_values[mean_start_cf_pow] = "STRING"

    mean_start_cr_pow = "mean_start_cr_pow"
    expert_value_keys.append(mean_start_cr_pow)
    expert_values[mean_start_cr_pow] = "STRING"

    mean_start_cp_pow = "mean_start_cp_pow"
    expert_value_keys.append(mean_start_cp_pow)
    expert_values[mean_start_cp_pow] = "STRING"

    mean_start_kf_pha = "mean_start_kf_pha"
    expert_value_keys.append(mean_start_kf_pha)
    expert_values[mean_start_kf_pha] = "STRING"

    mean_start_kr_pha = "mean_start_kr_pha"
    expert_value_keys.append(vac_pv_val)
    expert_values[vac_pv_val] = "STRING"

    mean_start_cf_pha = "mean_start_cf_pha"
    expert_value_keys.append(mean_start_cf_pha)
    expert_values[mean_start_cf_pha] = "STRING"

    mean_start_cr_pha = "mean_start_cr_pha"
    expert_value_keys.append(mean_start_cr_pha)
    expert_values[mean_start_cr_pha] = "STRING"

    mean_start_cp_pha = "mean_start_cp_pha"
    expert_value_keys.append(mean_start_cp_pha)
    expert_values[mean_start_cp_pha] = "STRING"

    mean_end_kf_pow = "mean_end_kf_pow"
    expert_value_keys.append(mean_end_kf_pow)
    expert_values[mean_end_kf_pow] = "STRING"

    mean_end_kr_pow = "mean_end_kr_pow"
    expert_value_keys.append(mean_end_kr_pow)
    expert_values[mean_end_kr_pow] = "STRING"

    mean_end_cf_pow = "mean_end_cf_pow"
    expert_value_keys.append(mean_end_cf_pow)
    expert_values[mean_end_cf_pow] = "STRING"

    mean_end_cr_pow = "mean_end_cr_pow"
    expert_value_keys.append(mean_end_cr_pow)
    expert_values[mean_end_cr_pow] = "STRING"

    mean_end_cp_pow = "mean_end_cp_pow"
    expert_value_keys.append(mean_end_cp_pow)
    expert_values[mean_end_cp_pow] = "STRING"

    mean_end_kf_pha = "mean_end_kf_pha"
    expert_value_keys.append(mean_end_kf_pha)
    expert_values[mean_end_kf_pha] = "STRING"

    mean_end_kr_pha = "mean_end_kr_pha"
    expert_value_keys.append(mean_end_kr_pha)
    expert_values[mean_end_kr_pha] = "STRING"

    expert_value_keys.append(vac_pv_val)
    expert_values[vac_pv_val] = "STRING"

    mean_end_cf_pha = "mean_end_cf_pha"
    expert_value_keys.append(mean_end_cf_pha)
    expert_values[mean_end_cf_pha] = "STRING"

    mean_end_cr_pha = "mean_end_cr_pha"
    expert_value_keys.append(mean_end_cr_pha)
    expert_values[mean_end_cr_pha] = "STRING"

    mean_end_cp_pha = "mean_end_cp_pha"
    expert_value_keys.append(mean_end_cp_pha)
    expert_values[mean_end_cp_pha] = "STRING"

    mask_units_kf_pow = "mask_units_kf_pow"
    expert_value_keys.append(mask_units_kf_pow)
    expert_values[mask_units_kf_pow] = "STRING"

    mask_units_kr_pow = "mask_units_kr_pow"
    expert_value_keys.append(mask_units_kr_pow)
    expert_values[mask_units_kr_pow] = "STRING"

    mask_units_cf_pow = "mask_units_cf_pow"
    expert_value_keys.append(mask_units_cf_pow)
    expert_values[mask_units_cf_pow] = "STRING"

    mask_units_cr_pow = "mask_units_cr_pow"
    expert_value_keys.append(mask_units_cr_pow)
    expert_values[mask_units_cr_pow] = "STRING"

    mask_units_cp_pow = "mask_units_cp_pow"
    expert_value_keys.append(mask_units_cp_pow)
    expert_values[mask_units_cp_pow] = "STRING"

    mask_units_kf_pha = "mask_units_kf_pha"
    expert_value_keys.append(mask_units_kf_pha)
    expert_values[mask_units_kf_pha] = "STRING"

    mask_units_kr_pha = "mask_units_kr_pha"
    expert_value_keys.append(mask_units_kr_pha)
    expert_values[mask_units_kr_pha] = "STRING"

    mask_units_cf_pha = "mask_units_cf_pha"
    expert_value_keys.append(mask_units_cf_pha)
    expert_values[mask_units_cf_pha] = "STRING"

    mask_units_cr_pha = "mask_units_cr_pha"
    expert_value_keys.append(mask_units_cr_pha)
    expert_values[mask_units_cr_pha] = "STRING"

    mask_units_cp_pha = "mask_units_cp_pha"
    expert_value_keys.append(mask_units_cp_pha)
    expert_values[mask_units_cp_pha] = "STRING"

    mask_start_kf_pow = "mask_start_kf_pow"
    expert_value_keys.append(mask_start_kf_pow)
    expert_values[mask_start_kf_pow] = "STRING"

    mask_start_kr_pow = "mask_start_kr_pow"
    expert_value_keys.append(mask_start_kr_pow)
    expert_values[mask_start_kr_pow] = "STRING"

    mask_start_cf_pow = "mask_start_cf_pow"
    expert_value_keys.append(mask_start_cf_pow)
    expert_values[mask_start_cf_pow] = "STRING"

    mask_start_cr_pow = "mask_start_cr_pow"
    expert_value_keys.append(mask_start_cr_pow)
    expert_values[mask_start_cr_pow] = "STRING"

    mask_start_cp_pow = "mask_start_cp_pow"
    expert_value_keys.append(mask_start_cp_pow)
    expert_values[mask_start_cp_pow] = "STRING"

    mask_start_kf_pha = "mask_start_kf_pha"
    expert_value_keys.append(mask_start_kf_pha)
    expert_values[mask_start_kf_pha] = "STRING"

    mask_start_kr_pha = "mask_start_kr_pha"
    expert_value_keys.append(mask_start_kr_pha)
    expert_values[mask_start_kr_pha] = "STRING"

    mask_start_cf_pha = "mask_start_cf_pha"
    expert_value_keys.append(mask_start_cf_pha)
    expert_values[mask_start_cf_pha] = "STRING"

    mask_start_cr_pha = "mask_start_cr_pha"
    expert_value_keys.append(mask_start_cr_pha)
    expert_values[mask_start_cr_pha] = "STRING"

    mask_start_cp_pha = "mask_start_cp_pha"
    expert_value_keys.append(mask_start_cp_pha)
    expert_values[mask_start_cp_pha] = "STRING"

    mask_end_kf_pow = "mask_end_kf_pow"
    expert_value_keys.append(mask_end_kf_pow)
    expert_values[mask_end_kf_pow] = "STRING"

    mask_end_kr_pow = "mask_end_kr_pow"
    expert_value_keys.append(mask_end_kr_pow)
    expert_values[mask_end_kr_pow] = "STRING"

    mask_end_cf_pow = "mask_end_cf_pow"
    expert_value_keys.append(mask_end_cf_pow)
    expert_values[mask_end_cf_pow] = "STRING"

    mask_end_cr_pow = "mask_end_cr_pow"
    expert_value_keys.append(mask_end_cr_pow)
    expert_values[mask_end_cr_pow] = "STRING"

    mask_end_cp_pow = "mask_end_cp_pow"
    expert_value_keys.append(mask_end_cp_pow)
    expert_values[mask_end_cp_pow] = "STRING"

    mask_end_kf_pha = "mask_end_kf_pha"
    expert_value_keys.append(mask_end_kf_pha)
    expert_values[mask_end_kf_pha] = "STRING"

    mask_end_kr_pha = "mask_end_kr_pha"
    expert_value_keys.append(mask_end_kr_pha)
    expert_values[mask_end_kr_pha] = "STRING"

    mask_end_cf_pha = "mask_end_cf_pha"
    expert_value_keys.append(mask_end_cf_pha)
    expert_values[mask_end_cf_pha] = "STRING"

    mask_end_cr_pha = "mask_end_cr_pha"
    expert_value_keys.append(mask_end_cr_pha)
    expert_values[mask_end_cr_pha] = "STRING"

    mask_end_cp_pha = "mask_end_cp_pha"
    expert_value_keys.append(mask_end_cp_pha)
    expert_values[mask_end_cp_pha] = "STRING"

    mask_window_start_kf_pow = "mask_window_start_kf_pow"
    expert_value_keys.append(mask_window_start_kf_pow)
    expert_values[mask_window_start_kf_pow] = "STRING"

    mask_window_start_kr_pow = "mask_window_start_kr_pow"
    expert_value_keys.append(mask_window_start_kr_pow)
    expert_values[mask_window_start_kr_pow] = "STRING"

    mask_window_start_cf_pow = "mask_window_start_cf_pow"
    expert_value_keys.append(mask_window_start_cf_pow)
    expert_values[mask_window_start_cf_pow] = "STRING"

    mask_window_start_cr_pow = "mask_window_start_cr_pow"
    expert_value_keys.append(mask_window_start_cr_pow)
    expert_values[mask_window_start_cr_pow] = "STRING"

    mask_window_start_cp_pow = "mask_window_start_cp_pow"
    expert_value_keys.append(mask_window_start_cp_pow)
    expert_values[mask_window_start_cp_pow] = "STRING"

    mask_window_start_kf_pha = "mask_window_start_kf_pha"
    expert_value_keys.append(mask_window_start_kf_pha)
    expert_values[mask_window_start_kf_pha] = "STRING"

    mask_window_start_kr_pha = "mask_window_start_kr_pha"
    expert_value_keys.append(mask_window_start_kr_pha)
    expert_values[mask_window_start_kr_pha] = "STRING"

    mask_window_start_cf_pha = "mask_window_start_cf_pha"
    expert_value_keys.append(mask_window_start_cf_pha)
    expert_values[mask_window_start_cf_pha] = "STRING"

    mask_window_start_cr_pha = "mask_window_start_cr_pha"
    expert_value_keys.append(mask_window_start_cr_pha)
    expert_values[mask_window_start_cr_pha] = "STRING"

    mask_window_start_cp_pha = "mask_window_start_cp_pha"
    expert_value_keys.append(mask_window_start_cp_pha)
    expert_values[mask_window_start_cp_pha] = "STRING"

    mask_window_end_kf_pow = "mask_window_end_kf_pow"
    expert_value_keys.append(mask_window_end_kf_pow)
    expert_values[mask_window_end_kf_pow] = "STRING"

    mask_window_end_kr_pow = "mask_window_end_kr_pow"
    expert_value_keys.append(mask_window_end_kr_pow)
    expert_values[mask_window_end_kr_pow] = "STRING"

    mask_window_end_cf_pow = "mask_window_end_cf_pow"
    expert_value_keys.append(mask_window_end_cf_pow)
    expert_values[mask_window_end_cf_pow] = "STRING"

    mask_window_end_cr_pow = "mask_window_end_cr_pow"
    expert_value_keys.append(mask_window_end_cr_pow)
    expert_values[mask_window_end_cr_pow] = "STRING"

    mask_window_end_cp_pow = "mask_window_end_cp_pow"
    expert_value_keys.append(mask_window_end_cp_pow)
    expert_values[mask_window_end_cp_pow] = "STRING"

    mask_window_end_kf_pha = "mask_window_end_kf_pha"
    expert_value_keys.append(mask_window_end_kf_pha)
    expert_values[mask_window_end_kf_pha] = "STRING"

    mask_window_end_kr_pha = "mask_window_end_kr_pha"
    expert_value_keys.append(mask_window_end_kr_pha)
    expert_values[mask_window_end_kr_pha] = "STRING"

    mask_window_end_cf_pha = "mask_window_end_cf_pha"
    expert_value_keys.append(mask_window_end_cf_pha)
    expert_values[mask_window_end_cf_pha] = "STRING"

    mask_window_end_cr_pha = "mask_window_end_cr_pha"
    expert_value_keys.append(mask_window_end_cr_pha)
    expert_values[mask_window_end_cr_pha] = "STRING"

    mask_window_end_cp_pha = "mask_window_end_cp_pha"
    expert_value_keys.append(vac_pv_val)
    expert_values[vac_pv_val] = "STRING"

    mask_min_kf_pow = "mask_min_kf_pow"
    expert_value_keys.append(mask_min_kf_pow)
    expert_values[mask_min_kf_pow] = "STRING"

    mask_min_kr_pow = "mask_min_kr_pow"
    expert_value_keys.append(mask_min_kr_pow)
    expert_values[mask_min_kr_pow] = "STRING"

    mask_min_cf_pow = "mask_min_cf_pow"
    expert_value_keys.append(mask_min_cf_pow)
    expert_values[mask_min_cf_pow] = "STRING"

    mask_min_cr_pow = "mask_min_cr_pow"
    expert_value_keys.append(mask_min_cr_pow)
    expert_values[mask_min_cr_pow] = "STRING"

    mask_min_cp_pow = "mask_min_cp_pow"
    expert_value_keys.append(mask_min_cp_pow)
    expert_values[mask_min_cp_pow] = "STRING"

    mask_min_kf_pha = "mask_min_kf_pha"
    expert_value_keys.append(mask_min_kf_pha)
    expert_values[mask_min_kf_pha] = "STRING"

    mask_min_kr_pha = "mask_min_kr_pha"
    expert_value_keys.append(mask_min_kr_pha)
    expert_values[mask_min_kr_pha] = "STRING"

    mask_min_cf_pha = "mask_min_cf_pha"
    expert_value_keys.append(mask_min_cf_pha)
    expert_values[mask_min_cf_pha] = "STRING"

    mask_min_cr_pha = "mask_min_cr_pha"
    expert_value_keys.append(mask_min_cr_pha)
    expert_values[mask_min_cr_pha] = "STRING"

    mask_min_cp_pha = "mask_min_cp_pha"
    expert_value_keys.append(mask_min_cp_pha)
    expert_values[mask_min_cp_pha] = "STRING"

    num_averages_kf_pow = "num_averages_kf_pow"
    expert_value_keys.append(num_averages_kf_pow)
    expert_values[num_averages_kf_pow] = "STRING"

    num_averages_kr_pow = "num_averages_kr_pow"
    expert_value_keys.append(num_averages_kr_pow)
    expert_values[num_averages_kr_pow] = "STRING"

    num_averages_cf_pow = "num_averages_cf_pow"
    expert_value_keys.append(num_averages_cf_pow)
    expert_values[num_averages_cf_pow] = "STRING"

    num_averages_cr_pow = "num_averages_cr_pow"
    expert_value_keys.append(num_averages_cr_pow)
    expert_values[num_averages_cr_pow] = "STRING"

    num_averages_cp_pow = "num_averages_cp_pow"
    expert_value_keys.append(num_averages_cp_pow)
    expert_values[num_averages_cp_pow] = "STRING"

    num_averages_kf_pha = "num_averages_kf_pha"
    expert_value_keys.append(num_averages_kf_pha)
    expert_values[num_averages_kf_pha] = "STRING"

    num_averages_kr_pha = "num_averages_kr_pha"
    expert_value_keys.append(num_averages_kr_pha)
    expert_values[num_averages_kr_pha] = "STRING"

    num_averages_cf_pha = "num_averages_cf_pha"
    expert_value_keys.append(num_averages_cf_pha)
    expert_values[num_averages_cf_pha] = "STRING"

    num_averages_cr_pha = "num_averages_cr_pha"
    expert_value_keys.append(num_averages_cr_pha)
    expert_values[num_averages_cr_pha] = "STRING"

    num_averages_cp_pha = "num_averages_cp_pha"
    expert_value_keys.append(num_averages_cp_pha)
    expert_values[num_averages_cp_pha] = "STRING"

    mask_auto_set_kf_pow = "mask_auto_set_kf_pow"
    expert_value_keys.append(mask_auto_set_kf_pow)
    expert_values[mask_auto_set_kf_pow] = "STRING"

    mask_auto_set_kr_pow = "mask_auto_set_kr_pow"
    expert_value_keys.append(mask_auto_set_kr_pow)
    expert_values[mask_auto_set_kr_pow] = "STRING"

    mask_auto_set_cf_pow = "mask_auto_set_cf_pow"
    expert_value_keys.append(mask_auto_set_cf_pow)
    expert_values[mask_auto_set_cf_pow] = "STRING"

    mask_auto_set_cr_pow = "mask_auto_set_cr_pow"
    expert_value_keys.append(mask_auto_set_cr_pow)
    expert_values[mask_auto_set_cr_pow] = "STRING"

    mask_auto_set_cp_pow = "mask_auto_set_cp_pow"
    expert_value_keys.append(mask_auto_set_cp_pow)
    expert_values[mask_auto_set_cp_pow] = "STRING"

    mask_auto_set_kf_pha = "mask_auto_set_kf_pha"
    expert_value_keys.append(mask_auto_set_kf_pha)
    expert_values[mask_auto_set_kf_pha] = "STRING"

    mask_auto_set_kr_pha = "mask_auto_set_kr_pha"
    expert_value_keys.append(mask_auto_set_kr_pha)
    expert_values[mask_auto_set_kr_pha] = "STRING"

    mask_auto_set_cf_pha = "mask_auto_set_cf_pha"
    expert_value_keys.append(mask_auto_set_cf_pha)
    expert_values[mask_auto_set_cf_pha] = "STRING"

    mask_auto_set_cr_pha = "mask_auto_set_cr_pha"
    expert_value_keys.append(mask_auto_set_cr_pha)
    expert_values[mask_auto_set_cr_pha] = "STRING"

    mask_auto_set_cp_pha = "mask_auto_set_cp_pha"
    expert_value_keys.append(mask_auto_set_cp_pha)
    expert_values[mask_auto_set_cp_pha] = "STRING"

    mask_type_kf_pow = "mask_type_kf_pow"
    expert_value_keys.append(mask_type_kf_pow)
    expert_values[mask_type_kf_pow] = "STRING"

    mask_type_kr_pow = "mask_type_kr_pow"
    expert_value_keys.append(mask_type_kr_pow)
    expert_values[mask_type_kr_pow] = "STRING"

    mask_type_cf_pow = "mask_type_cf_pow"
    expert_value_keys.append(mask_type_cf_pow)
    expert_values[mask_type_cf_pow] = "STRING"

    mask_type_cr_pow = "mask_type_cr_pow"
    expert_value_keys.append(mask_type_cr_pow)
    expert_values[mask_type_cr_pow] = "STRING"

    mask_type_cp_pow = "mask_type_cp_pow"
    expert_value_keys.append(mask_type_cp_pow)
    expert_values[mask_type_cp_pow] = "STRING"

    mask_type_kf_pha = "mask_type_kf_pha"
    expert_value_keys.append(mask_type_kf_pha)
    expert_values[mask_type_kf_pha] = "STRING"

    mask_type_kr_pha = "mask_type_kr_pha"
    expert_value_keys.append(mask_type_kr_pha)
    expert_values[mask_type_kr_pha] = "STRING"

    mask_type_cf_pha = "mask_type_cf_pha"
    expert_value_keys.append(mask_type_cf_pha)
    expert_values[mask_type_cf_pha] = "STRING"

    mask_type_cr_pha = "mask_type_cr_pha"
    expert_value_keys.append(mask_type_cr_pha)
    expert_values[mask_type_cr_pha] = "STRING"

    mask_type_cp_pha = "mask_type_cp_pha"
    expert_value_keys.append(mask_type_cp_pha)
    expert_values[mask_type_cp_pha] = "STRING"

    mask_level_kf_pow = "mask_level_kf_pow"
    expert_value_keys.append(mask_level_kf_pow)
    expert_values[mask_level_kf_pow] = "STRING"

    mask_level_kr_pow = "mask_level_kr_pow"
    expert_value_keys.append(mask_level_kr_pow)
    expert_values[mask_level_kr_pow] = "STRING"

    mask_level_cf_pow = "mask_level_cf_pow"
    expert_value_keys.append(mask_level_cf_pow)
    expert_values[mask_level_cf_pow] = "STRING"

    mask_level_cr_pow = "mask_level_cr_pow"
    expert_value_keys.append(mask_level_cr_pow)
    expert_values[mask_level_cr_pow] = "STRING"

    mask_level_cp_pow = "mask_level_cp_pow"
    expert_value_keys.append(mask_level_cp_pow)
    expert_values[mask_level_cp_pow] = "STRING"

    mask_level_kf_pha = "mask_level_kf_pha"
    expert_value_keys.append(mask_level_kf_pha)
    expert_values[mask_level_kf_pha] = "STRING"

    mask_level_kr_pha = "mask_level_kr_pha"
    expert_value_keys.append(mask_level_kr_pha)
    expert_values[mask_level_kr_pha] = "STRING"

    mask_level_cf_pha = "mask_level_cf_pha"
    expert_value_keys.append(mask_level_cf_pha)
    expert_values[mask_level_cf_pha] = "STRING"

    mask_level_cr_pha = "mask_level_cr_pha"
    expert_value_keys.append(mask_level_cr_pha)
    expert_values[mask_level_cr_pha] = "STRING"

    mask_level_cp_pha = "mask_level_cp_pha"
    expert_value_keys.append(mask_level_cp_pha)
    expert_values[mask_level_cp_pha] = "STRING"

    drop_amplitude_kf_pow = "drop_amplitude_kf_pow"
    expert_value_keys.append(drop_amplitude_kf_pow)
    expert_values[drop_amplitude_kf_pow] = "STRING"

    drop_amplitude_kr_pow = "drop_amplitude_kr_pow"
    expert_value_keys.append(drop_amplitude_kr_pow)
    expert_values[drop_amplitude_kr_pow] = "STRING"

    drop_amplitude_cf_pow = "drop_amplitude_cf_pow"
    expert_value_keys.append(drop_amplitude_cf_pow)
    expert_values[drop_amplitude_cf_pow] = "STRING"

    drop_amplitude_cr_pow = "drop_amplitude_cr_pow"
    expert_value_keys.append(drop_amplitude_cr_pow)
    expert_values[drop_amplitude_cr_pow] = "STRING"

    drop_amplitude_cp_pow = "drop_amplitude_cp_pow"
    expert_value_keys.append(drop_amplitude_cp_pow)
    expert_values[drop_amplitude_cp_pow] = "STRING"

    drop_amplitude_kf_pha = "drop_amplitude_kf_pha"
    expert_value_keys.append(drop_amplitude_kf_pha)
    expert_values[drop_amplitude_kf_pha] = "STRING"

    drop_amplitude_kr_pha = "drop_amplitude_kr_pha"
    expert_value_keys.append(drop_amplitude_kr_pha)
    expert_values[drop_amplitude_kr_pha] = "STRING"

    drop_amplitude_cf_pha = "drop_amplitude_cf_pha"
    expert_value_keys.append(drop_amplitude_cf_pha)
    expert_values[drop_amplitude_cf_pha] = "STRING"

    drop_amplitude_cr_pha = "drop_amplitude_cr_pha"
    expert_value_keys.append(drop_amplitude_cr_pha)
    expert_values[drop_amplitude_cr_pha] = "STRING"

    drop_amplitude_cp_pha = "drop_amplitude_cp_pha"
    expert_value_keys.append(drop_amplitude_cp_pha)
    expert_values[drop_amplitude_cp_pha] = "STRING"

    phase_end_by_power_kf_pow = "phase_end_by_power_kf_pow"
    expert_value_keys.append(phase_end_by_power_kf_pow)
    expert_values[phase_end_by_power_kf_pow] = "STRING"

    phase_end_by_power_kr_pow = "phase_end_by_power_kr_pow"
    expert_value_keys.append(phase_end_by_power_kr_pow)
    expert_values[phase_end_by_power_kr_pow] = "STRING"

    phase_end_by_power_cf_pow = "phase_end_by_power_cf_pow"
    expert_value_keys.append(phase_end_by_power_cf_pow)
    expert_values[phase_end_by_power_cf_pow] = "STRING"

    phase_end_by_power_cr_pow = "phase_end_by_power_cr_pow"
    expert_value_keys.append(phase_end_by_power_cr_pow)
    expert_values[phase_end_by_power_cr_pow] = "STRING"

    phase_end_by_power_cp_pow = "phase_end_by_power_cp_pow"
    expert_value_keys.append(phase_end_by_power_cp_pow)
    expert_values[phase_end_by_power_cp_pow] = "STRING"

    phase_end_by_power_kf_pha = "phase_end_by_power_kf_pha"
    expert_value_keys.append(phase_end_by_power_kf_pha)
    expert_values[phase_end_by_power_kf_pha] = "STRING"

    phase_end_by_power_kr_pha = "phase_end_by_power_kr_pha"
    expert_value_keys.append(phase_end_by_power_kr_pha)
    expert_values[phase_end_by_power_kr_pha] = "STRING"

    phase_end_by_power_cf_pha = "phase_end_by_power_cf_pha"
    expert_value_keys.append(phase_end_by_power_cf_pha)
    expert_values[phase_end_by_power_cf_pha] = "STRING"

    phase_end_by_power_cr_pha = "phase_end_by_power_cr_pha"
    expert_value_keys.append(phase_end_by_power_cr_pha)
    expert_values[phase_end_by_power_cr_pha] = "STRING"

    phase_end_by_power_cp_pha = "phase_end_by_power_cp_pha"
    expert_value_keys.append(phase_end_by_power_cp_pha)
    expert_values[phase_end_by_power_cp_pha] = "STRING"

    mask_end_power_kf_pow = "mask_end_power_kf_pow"
    expert_value_keys.append(mask_end_power_kf_pow)
    expert_values[mask_end_power_kf_pow] = "STRING"

    mask_end_power_kr_pow = "mask_end_power_kr_pow"
    expert_value_keys.append(mask_end_power_kr_pow)
    expert_values[mask_end_power_kr_pow] = "STRING"

    mask_end_power_cf_pow = "mask_end_power_cf_pow"
    expert_value_keys.append(mask_end_power_cf_pow)
    expert_values[mask_end_power_cf_pow] = "STRING"

    mask_end_power_cr_pow = "mask_end_power_cr_pow"
    expert_value_keys.append(mask_end_power_cr_pow)
    expert_values[mask_end_power_cr_pow] = "STRING"

    mask_end_power_cp_pow = "mask_end_power_cp_pow"
    expert_value_keys.append(mask_end_power_cp_pow)
    expert_values[mask_end_power_cp_pow] = "STRING"

    mask_end_power_kf_pha = "mask_end_power_kf_pha"
    expert_value_keys.append(mask_end_power_kf_pha)
    expert_values[mask_end_power_kf_pha] = "STRING"

    mask_end_power_kr_pha = "mask_end_power_kr_pha"
    expert_value_keys.append(mask_end_power_kr_pha)
    expert_values[mask_end_power_kr_pha] = "STRING"

    mask_end_power_cf_pha = "mask_end_power_cf_pha"
    expert_value_keys.append(mask_end_power_cf_pha)
    expert_values[mask_end_power_cf_pha] = "STRING"

    mask_end_power_cr_pha = "mask_end_power_cr_pha"
    expert_value_keys.append(mask_end_power_cr_pha)
    expert_values[mask_end_power_cr_pha] = "STRING"

    mask_end_power_cp_pha = "mask_end_power_cp_pha"
    expert_value_keys.append(mask_end_power_cp_pha)
    expert_values[mask_end_power_cp_pha] = "STRING"

    saved_on_breakdown_event_kf_pow = "saved_on_breakdown_event_kf_pow"
    expert_value_keys.append(saved_on_breakdown_event_kf_pow)
    expert_values[saved_on_breakdown_event_kf_pow] = "STRING"

    saved_on_breakdown_event_kr_pow = "saved_on_breakdown_event_kr_pow"
    expert_value_keys.append(saved_on_breakdown_event_kr_pow)
    expert_values[saved_on_breakdown_event_kr_pow] = "STRING"

    saved_on_breakdown_event_cf_pow = "saved_on_breakdown_event_cf_pow"
    expert_value_keys.append(saved_on_breakdown_event_cf_pow)
    expert_values[saved_on_breakdown_event_cf_pow] = "STRING"

    saved_on_breakdown_event_cr_pow = "saved_on_breakdown_event_cr_pow"
    expert_value_keys.append(saved_on_breakdown_event_cr_pow)
    expert_values[saved_on_breakdown_event_cr_pow] = "STRING"

    saved_on_breakdown_event_cp_pow = "saved_on_breakdown_event_cp_pow"
    expert_value_keys.append(saved_on_breakdown_event_cp_pow)
    expert_values[saved_on_breakdown_event_cp_pow] = "STRING"

    saved_on_breakdown_event_kf_pha = "saved_on_breakdown_event_kf_pha"
    expert_value_keys.append(saved_on_breakdown_event_kf_pha)
    expert_values[saved_on_breakdown_event_kf_pha] = "STRING"

    saved_on_breakdown_event_kr_pha = "saved_on_breakdown_event_kr_pha"
    expert_value_keys.append(saved_on_breakdown_event_kr_pha)
    expert_values[saved_on_breakdown_event_kr_pha] = "STRING"

    saved_on_breakdown_event_cf_pha = "saved_on_breakdown_event_cf_pha"
    expert_value_keys.append(saved_on_breakdown_event_cf_pha)
    expert_values[saved_on_breakdown_event_cf_pha] = "STRING"

    saved_on_breakdown_event_cr_pha = "saved_on_breakdown_event_cr_pha"
    expert_value_keys.append(saved_on_breakdown_event_cr_pha)
    expert_values[saved_on_breakdown_event_cr_pha] = "STRING"

    saved_on_breakdown_event_cp_pha = "saved_on_breakdown_event_cp_pha"
    expert_value_keys.append(saved_on_breakdown_event_cp_pha)
    expert_values[saved_on_breakdown_event_cp_pha] = "STRING"

    saved_on_vac_spike_kf_pow = "saved_on_vac_spike_kf_pow"
    expert_value_keys.append(saved_on_vac_spike_kf_pow)
    expert_values[saved_on_vac_spike_kf_pow] = "STRING"

    saved_on_vac_spike_kr_pow = "saved_on_vac_spike_kr_pow"
    expert_value_keys.append(saved_on_vac_spike_kr_pow)
    expert_values[saved_on_vac_spike_kr_pow] = "STRING"

    saved_on_vac_spike_cf_pow = "saved_on_vac_spike_cf_pow"
    expert_value_keys.append(saved_on_vac_spike_cf_pow)
    expert_values[saved_on_vac_spike_cf_pow] = "STRING"

    saved_on_vac_spike_cr_pow = "saved_on_vac_spike_cr_pow"
    expert_value_keys.append(saved_on_vac_spike_cr_pow)
    expert_values[saved_on_vac_spike_cr_pow] = "STRING"

    saved_on_vac_spike_cp_pow = "saved_on_vac_spike_cp_pow"
    expert_value_keys.append(saved_on_vac_spike_cp_pow)
    expert_values[saved_on_vac_spike_cp_pow] = "STRING"

    saved_on_vac_spike_kf_pha = "saved_on_vac_spike_kf_pha"
    expert_value_keys.append(saved_on_vac_spike_kf_pha)
    expert_values[saved_on_vac_spike_kf_pha] = "STRING"

    saved_on_vac_spike_kr_pha = "saved_on_vac_spike_kr_pha"
    expert_value_keys.append(saved_on_vac_spike_kr_pha)
    expert_values[saved_on_vac_spike_kr_pha] = "STRING"

    saved_on_vac_spike_cf_pha = "saved_on_vac_spike_cf_pha"
    expert_value_keys.append(saved_on_vac_spike_cf_pha)
    expert_values[saved_on_vac_spike_cf_pha] = "STRING"

    saved_on_vac_spike_cr_pha = "saved_on_vac_spike_cr_pha"
    expert_value_keys.append(saved_on_vac_spike_cr_pha)
    expert_values[saved_on_vac_spike_cr_pha] = "STRING"

    saved_on_vac_spike_cp_pha = "saved_on_vac_spike_cp_pha"
    expert_value_keys.append(saved_on_vac_spike_cp_pha)
    expert_values[saved_on_vac_spike_cp_pha] = "STRING"

    drop_amp_on_bd_kf_pow = "drop_amp_on_bd_kf_pow"
    expert_value_keys.append(drop_amp_on_bd_kf_pow)
    expert_values[drop_amp_on_bd_kf_pow] = "STRING"

    drop_amp_on_bd_kr_pow = "drop_amp_on_bd_kr_pow"
    expert_value_keys.append(drop_amp_on_bd_kr_pow)
    expert_values[drop_amp_on_bd_kr_pow] = "STRING"

    drop_amp_on_bd_cf_pow = "drop_amp_on_bd_cf_pow"
    expert_value_keys.append(drop_amp_on_bd_cf_pow)
    expert_values[drop_amp_on_bd_cf_pow] = "STRING"

    drop_amp_on_bd_cr_pow = "drop_amp_on_bd_cr_pow"
    expert_value_keys.append(drop_amp_on_bd_cr_pow)
    expert_values[drop_amp_on_bd_cr_pow] = "STRING"

    drop_amp_on_bd_cp_pow = "drop_amp_on_bd_cp_pow"
    expert_value_keys.append(drop_amp_on_bd_cp_pow)
    expert_values[drop_amp_on_bd_cp_pow] = "STRING"

    drop_amp_on_bd_kf_pha = "drop_amp_on_bd_kf_pha"
    expert_value_keys.append(drop_amp_on_bd_kf_pha)
    expert_values[drop_amp_on_bd_kf_pha] = "STRING"

    drop_amp_on_bd_kr_pha = "drop_amp_on_bd_kr_pha"
    expert_value_keys.append(drop_amp_on_bd_kr_pha)
    expert_values[drop_amp_on_bd_kr_pha] = "STRING"

    drop_amp_on_bd_cf_pha = "drop_amp_on_bd_cf_pha"
    expert_value_keys.append(drop_amp_on_bd_cf_pha)
    expert_values[drop_amp_on_bd_cf_pha] = "STRING"

    drop_amp_on_bd_cr_pha = "drop_amp_on_bd_cr_pha"
    expert_value_keys.append(drop_amp_on_bd_cr_pha)
    expert_values[drop_amp_on_bd_cr_pha] = "STRING"

    drop_amp_on_bd_cp_pha = "drop_amp_on_bd_cp_pha"
    expert_value_keys.append(drop_amp_on_bd_cp_pha)
    expert_values[drop_amp_on_bd_cp_pha] = "STRING"

    streak_kf_pow = "streak_kf_pow"
    expert_value_keys.append(streak_kf_pow)
    expert_values[streak_kf_pow] = "STRING"

    streak_kr_pow = "streak_kr_pow"
    expert_value_keys.append(streak_kr_pow)
    expert_values[streak_kr_pow] = "STRING"

    streak_cf_pow = "streak_cf_pow"
    expert_value_keys.append(streak_cf_pow)
    expert_values[streak_cf_pow] = "STRING"

    streak_cr_pow = "streak_cr_pow"
    expert_value_keys.append(streak_cr_pow)
    expert_values[streak_cr_pow] = "STRING"

    streak_cp_pow = "streak_cp_pow"
    expert_value_keys.append(streak_cp_pow)
    expert_values[streak_cp_pow] = "STRING"

    streak_kf_pha = "streak_kf_pha"
    expert_value_keys.append(streak_kf_pha)
    expert_values[streak_kf_pha] = "STRING"

    streak_kr_pha = "streak_kr_pha"
    expert_value_keys.append(streak_kr_pha)
    expert_values[streak_kr_pha] = "STRING"

    streak_cf_pha = "streak_cf_pha"
    expert_value_keys.append(streak_cf_pha)
    expert_values[streak_cf_pha] = "STRING"

    streak_cr_pha = "streak_cr_pha"
    expert_value_keys.append(streak_cr_pha)
    expert_values[streak_cr_pha] = "STRING"

    streak_cp_pha = "streak_cp_pha"
    expert_value_keys.append(streak_cp_pha)
    expert_values[streak_cp_pha] = "STRING"

    breakdown_rate_aim_val = "breakdown_rate_aim_val"
    expert_value_keys.append(breakdown_rate_aim_val)
    expert_values[breakdown_rate_aim_val] = "STRING"

    expected_daq_rep_rate_val = "expected_daq_rep_rate_val"
    expert_value_keys.append(expected_daq_rep_rate_val)
    expert_values[expected_daq_rep_rate_val] = "STRING"

    daq_rep_rate_error_val = "daq_rep_rate_error_val"
    expert_value_keys.append(daq_rep_rate_error_val)
    expert_values[daq_rep_rate_error_val] = "STRING"

    number_of_pulses_in_history_val = "number_of_pulses_in_history_val"
    expert_value_keys.append(number_of_pulses_in_history_val)
    expert_values[number_of_pulses_in_history_val] = "STRING"

    trace_buffer_size_val = "trace_buffer_size_val"
    expert_value_keys.append(trace_buffer_size_val)
    expert_values[trace_buffer_size_val] = "STRING"

    default_pulse_count_val = "default_pulse_count_val"
    expert_value_keys.append(default_pulse_count_val)
    expert_values[default_pulse_count_val] = "STRING"

    default_amp_increase_val = "default_amp_increase_val"
    expert_value_keys.append(default_amp_increase_val)
    expert_values[default_amp_increase_val] = "STRING"

    max_amp_increase_val = "max_amp_increase_val"
    expert_value_keys.append(max_amp_increase_val)
    expert_values[max_amp_increase_val] = "STRING"

    num_fit_points_val = "num_fit_points_val"
    expert_value_keys.append(num_fit_points_val)
    expert_values[num_fit_points_val] = "STRING"

    active_power_val = "active_power_val"
    expert_value_keys.append(active_power_val)
    expert_values[active_power_val] = dummy_float

    num_future_traces_val = "num_future_traces_val"
    expert_value_keys.append(num_future_traces_val)
    expert_values[num_future_traces_val] = dummy_int

    keep_valve_open_val = "keep_valve_open_val"
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
