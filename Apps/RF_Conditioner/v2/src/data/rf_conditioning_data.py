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
//               one of these to access all data,
//
//*/
'''

import numpy as np
import matplotlib.pyplot as plt
import config
from rf_conditioning_logger import rf_conditioning_logger
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from ramp import *
from src.data.state import state



class rf_conditioning_data(object):
    # whoami
    my_name = 'rf_condition_data'
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

    debug = False
    def __init__(self, debug = False):
        rf_conditioning_data.debug = debug
        # config
        self.config = config.config()
        # alias for daa dictionary
        self.values = rf_conditioning_data.values
        #
        # logging
        self.logger = rf_conditioning_logger()

        #self.ramp_max_index = len(ramp) -1


    def setup_pulse_count_breakdown_log(self):
        """
        this is way too complicated ... but its processing the data in two ways,
        once by amp_setpioint and once by pusle count, it generates to main lists:
        1) dat.rf_condition_data_base.amp_sp_history
              Sorted by amp_setpoint
              Used to define how to ramp up adn down
        2) dat.rf_condition_data_base.last_million_log
              Sorted by pulse count
              used to define the Breakdown Rate etc.

        :return:
        """
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
        self.values[rf_conditioning_data.log_pulse_count] = int(pulse_break_down_log[-1][0])
        self.values[rf_conditioning_data.breakdown_count] = int(pulse_break_down_log[-1][1])
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
        # https://stackoverflow.com/questions/11303225/how-to-remove-multiple-indexes-from-a-list-at-the-same-time
        for index in sorted(indices_to_remove, reverse=True):
            del pulse_break_down_log[index]
        #
        # sort the list by setpoint (part 2) then pulse_count (part 0)
        sorted_pulse_break_down_log_1 = sorted(pulse_break_down_log, key=lambda x: (x[2], x[0]))
        #
        # As we have all the time in the world...
        # make another list, ampSP_sorted_pulse_break_down_log, this has NO Setpoints = the final sp in sorted_pulse_break_down_log_1
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

        # #
        # #
        # # next we must insert the data in to the main data values dictionary
        # #
        # # set the ramp index
        # self.values[rf_conditioning_data.current_ramp_index] = ampSP_sorted_pulse_break_down_log[-1][3]
        # #
        # # amp_setpoint history history, THIS is used to decide where to ramp down,
        # # and what amp_setpoint to use in fitting when ramping-up
        # # write this list to the main log
        # rf_conditioning_data.rf_condition_data_base.amp_sp_history = [int(i[2]) for i in ampSP_sorted_pulse_break_down_log ]
        # self.logger.header(self.my_name + ' amp SP history on startup ', True)
        # to_write = []
        # for value in rf_conditioning_data.rf_condition_data_base.amp_sp_history:
        #     to_write.append(str(value))
        # self.logger.message(','.join(to_write),True)
        # #
        # # The next amp_setpoint to set
        # self.values[dat.log_amp_set] = dat.rf_condition_data_base.amp_sp_history[-1]
        # #
        # # the next amp_setpoint on ramp_down
        # self.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]
        # #
        # # pulse length (logged but not used as pulse_length is now defined by the pulse shaping table)
        # self.values[dat.log_pulse_length] = float(ampSP_sorted_pulse_break_down_log[-1][4]) / float(1000.0)# warning UNIT
        # self.llrf_config['PULSE_LENGTH_START'] = self.values[dat.log_pulse_length]
        # #
        # # set the number of pulses required at this step to the defualt (will be checked later)
        # self.values[dat.required_pulses] = self.llrf_config['DEFAULT_PULSE_COUNT']
        # #
        # # Write to log
        # self.logger.header( self.my_name + ' has processed the pulse_count_breakdown_log ', True)
        # self.logger.message([
        #     dat.log_pulse_count + ' ' + str(self.values[dat.log_pulse_count]),
        #     dat.required_pulses + ' ' + str(self.values[dat.required_pulses]),
        #     dat.breakdown_count + ' ' + str(self.values[dat.breakdown_count]),
        #     dat.log_amp_set + ' ' + str(self.values[dat.log_amp_set]),
        #     dat.current_ramp_index + ' ' + str(self.values[dat.current_ramp_index]),
        #     'pulse length = ' + str(self._llrf_config['PULSE_LENGTH_START']),
        #     dat.next_sp_decrease + ' ' + str(self.values[dat.next_sp_decrease])
        # ],True)
        # #
        # # Setting the last 10^6 breakdown last_106_bd_count
        # #
        # # get the last million pulses from THE ORIGINAL pulse_break_down_log
        # # !!! WE must use the original pulse_break_down_log, as it will have the true breakdown_count and pulse number !!!
        # # !!! (remember above we deleted the last entry in pulse_break_down_log to get generate amp_sp_history         !!!
        # pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
        # one_million_pulses_ago = self.values[dat.log_pulse_count] - self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']
        # dat.rf_condition_data_base.last_million_log = [x for x in pulse_break_down_log if x[0] >= one_million_pulses_ago ]
        # #
        # # write last_million_log to log
        # self.logger.header('Last million pulses', True)
        # for value in dat.rf_condition_data_base.last_million_log:
        #     str1 = ', '.join(str(e) for e in value)
        #     self.logger.message( str1, True)
        # self.logger.message('One Million pulses ago  = ' + str(one_million_pulses_ago),True)
        # first_entry = ' , '.join(str(x) for x in dat.rf_condition_data_base.last_million_log[0])
        # last_entry  = ' , '.join(str(x) for x in dat.rf_condition_data_base.last_million_log[-1])
        # self.logger.message('last_million_log[ 0] = ' + first_entry ,True)
        # self.logger.message('last_million_log[-1] = ' + last_entry ,True)
        # #
        # # sanity check
        # #
        # sanity_passed = True
        # if dat.rf_condition_data_base.last_million_log[-1][1] != self.values[dat.breakdown_count]:
        #     self.logger.message('Error in breakdown count',True)
        #     sanity_passed = False
        # if dat.rf_condition_data_base.last_million_log[-1][0] != self.values[dat.log_pulse_count]:
        #     self.logger.message('Error in pulse_count',True)
        #     sanity_passed = False
        # if sanity_passed:
        #     self.logger.message('Getting the pulse_breakdown_log passed sanity check', True)
        # else:
        #     self.logger.message('!!WARNING!! When getting the pulse_breakdown_log we failed a sanity check!!', True)
        #
        # #
        # # Now we are free to update the breakdown stats !!
        # #
        # self.update_breakdown_stats()




    def init_after_config_read(self):
        if self.llrf_config is not None:
            self.get_pulse_count_breakdown_log()
            dat.rf_condition_data_base.amp_vs_kfpow_running_stat = self.logger.get_amp_power_log()




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
#     def update_breakdown_stats(self):
#         old_last_106_bd_count = self.values[dat.last_106_bd_count]
#
#         self.values[dat.breakdown_count]   = dat.rf_condition_data_base.last_million_log[-1][1]
#         self.values[dat.last_106_bd_count] = dat.rf_condition_data_base.last_million_log[-1][1] - \
#                                              dat.rf_condition_data_base.last_million_log[0][1]
#         # if we have mor ethan 1 million pulses its easy
#         if dat.rf_condition_data_base.last_million_log[-1][0] > self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']:
#             self.values[dat.breakdown_rate] = self.values[dat.last_106_bd_count]
#         else: # else do some math
#             if dat.rf_condition_data_base.last_million_log[-1][0] == 0:
#                 self.values[dat.breakdown_rate] = 0
#             else:
#                 # !!!!!!!!!! THIS EQUATION MAY NOT BE CORRECT !!!!!!!!!!!!!!
#                 self.values[dat.breakdown_rate] = \
#             float(self.values[dat.last_106_bd_count] * self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']) \
#             / \
#             float(dat.rf_condition_data_base.last_million_log[-1][0] - dat.rf_condition_data_base.last_million_log[0][0])
#
#         # set is breakdwon rate hi
#         self.values[dat.breakdown_rate_hi] = self.values[dat.breakdown_rate] > self.values[dat.breakdown_rate_aim]
#
#
#         if old_last_106_bd_count != self.values[dat.last_106_bd_count]:
#             self.logger.header(' NEW last_106_bd_count ', True)
#             self.logger.message('Total breakdown_count = ' + str(dat.rf_condition_data_base.last_million_log[-1][1]),True)
#
#             self.logger.message('Last million pulse count => ' +
#                                 str(dat.rf_condition_data_base.last_million_log[-1][0]) + ' - ' +
#                                 str(dat.rf_condition_data_base.last_million_log[0][0])  + ' = ' +
#                                 str(dat.rf_condition_data_base.last_million_log[-1][0] - dat.rf_condition_data_base.last_million_log[0][0])
#                                 ,True)
#             self.logger.message('Last million breakdown_count => ' +
#                                 str(dat.rf_condition_data_base.last_million_log[-1][1]) + ' - ' +
#                                 str(dat.rf_condition_data_base.last_million_log[0][1])  + ' = ' +
#                                 str(self.values[dat.last_106_bd_count])
#                                 ,True)
#
#             if self.values[dat.breakdown_rate_hi]:
#                 self.logger.message('Breakdown rate High: ' +
#                                     str(self.values[dat.breakdown_rate]) + ' > ' +
#                                     str(self.values[dat.breakdown_rate_aim])
#                                     ,True)
#             else:
#                 self.logger.message('Breakdown rate good: ' +
#                                     str(self.values[dat.breakdown_rate]) + ' <= ' +
#                                     str(self.values[dat.breakdown_rate_aim])
#                                     ,True)
#
#
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




    # keys for all the data we monitor
    time_stamp = 'time_stamp'

    # STATUS PF MAIN MONITORS
    vac_spike_status = 'vac_spike_status'
    DC_spike_status = 'DC_spike_status'
    rev_power_spike_count = 'rev_power_spike_count'
    cav_temp = 'cav_temp'
    water_temp = 'water_temp'


    # Mean Values of Traces # TODO: CHANGE THIS NAMES TO MORE CANONICAL ONES
    fwd_cav_pwr = 'fwd_cav_pwr'
    fwd_kly_pwr = 'fwd_kly_pwr'
    rev_kly_pwr = 'rev_kly_pwr'
    rev_cav_pwr = 'rev_cav_pwr'
    probe_pwr = 'probe_pwr'
    fwd_cav_pha = 'fwd_cav_pha'
    fwd_kly_pha = 'fwd_kly_pha'
    rev_kly_pha = 'rev_kly_pha'
    rev_cav_pha = 'rev_cav_pha'
    probe_pha = 'probe_pha'
    krpow = 'krpow'
    krpha = 'krpha'
    kfpow = 'kfpow'
    kfpha = 'kfpha'
    crpow = 'crpow'
    crpha = 'crpha'
    cppow = 'cppow'
    cppha = 'cppha'
    cfpow = 'cfpow'
    cfpha = 'cfpha'


    vac_level = 'vac_level'
    DC_level = 'DC_level'
    vac_valve_status = 'vac_valve_status'
    num_outside_mask_traces = 'num_outside_mask_traces'

    probe_outside_mask_count = 'probe_outside_mask_count'
    forward_outside_mask_count = 'probe_outside_mask_count'
    reverse_outside_mask_count = 'reverse_outside_mask_count'

    breakdown_status = 'breakdown_status'
    breakdown_rate_aim = 'breakdown_rate_aim'

    # these are values from the pulse_breakdown_log
    log_pulse_count = 'log_pulse_count'
    #log_breakdown_count = 'log_breakdown_count'
    log_amp_set = 'log_amp_set'
    current_ramp_index = 'current_ramp_index'

    breakdown_count = 'breakdown_count'
    elapsed_time = 'elapsed_time'
    breakdown_rate = 'breakdown_rate'
    breakdown_rate_hi= 'breakdown_rate_hi'
    last_106_bd_count='last_106_bd_count'

    pulse_count = 'pulse_count'
    event_pulse_count = 'event_pulse_count'
    duplicate_pulse_count = 'duplicate_pulse_count'

    # Hold RF ON handle scontrolling these, we just monitor
    rfprot_state = 'rfprot_state'
    modulator_state = 'modulator_state'
    mod_output_status = 'mod_output_status'

    can_rf_output_OLD = 'can_rf_output_OLD'
    can_rf_output = 'can_rf_output'

    llrf_interlock = 'llrf_interlock' # The read value from EPICS
    llrf_interlock_status = 'llrf_interlock_status' # the apps internal state, good, new_bad etc


    llrf_trigger = 'llrf_trigger'
    llrf_trigger_status = 'llrf_trigger_status'

    pulse_length = 'pulse_length'
    pulse_length_status = 'pulse_length_status' # the apps internal state, good, new_bad etc

    llrf_output = 'llrf_output' # RF Output on LLRF panel
    llrf_output_status = 'llrf_output_status' # the apps internal state, good, new_bad etc

    llrf_ff_amp_locked = 'llrf_ff_amp_locked'
    llrf_ff_amp_locked_status = 'llrf_ff_amp_locked_status' # the apps internal state, good, new_bad etc
    llrf_ff_ph_locked  = 'llrf_ff_ph_locked'
    llrf_ff_ph_locked_status  = 'llrf_ff_ph_locked_status' # the apps internal state, good, new_bad etc

    llrf_DAQ_rep_rate = 'llrf_DAQ_rep_rate'
    llrf_DAQ_rep_rate_aim = 'llrf_DAQ_rep_rate_aim'
    llrf_DAQ_rep_rate_status = 'llrf_DAQ_rep_rate_status'
    llrf_DAQ_rep_rate_status_previous = 'llrf_DAQ_rep_rate_status_previous'
    llrf_DAQ_rep_rate_max = 'llrf_DAQ_rep_rate_max'
    llrf_DAQ_rep_rate_min = 'llrf_DAQ_rep_rate_min'


    power_aim = 'power_aim'
    pulse_length_aim = 'pulse_length_aim'
    pulse_length_aim_error = 'pulse_length_aim_error'
    pulse_length_min = 'pulse_length_min'
    pulse_length_max = 'pulse_length_max'

    required_pulses = 'required_pulses'
    next_power_increase = 'next_power_increase'


    log_pulse_length = 'log_pulse_length'


    last_mean_power = 'last_mean_power'
    sol_value = 'sol_value'

    amp_ff = 'amp_ff'
    amp_sp = 'amp_sp'
    phi_sp = 'phi_sp'


    TOR_ACQM = 'TOR_ACQM'
    TOR_SCAN = 'TOR_SCAN'

    #
    # plot straight line fit values, old and current
    x_min = 'x_min'
    x_max = 'x_max'
    old_x_min = 'old_x_min'
    old_x_max = 'old_x_max'
    y_min = 'y_min'
    y_max = 'y_max'
    old_y_min = 'old_y_min'
    old_y_max = 'old_y_max'
    c = 'c'
    m = 'm'
    old_c = 'old_c'
    old_m = 'old_m'

    #latest_ramp_up_sp = 'latest_ramp_up_sp'
    last_sp_above_100 = 'last_sp_above_100'
    max_sp_increase = 'max_sp_increase'
    next_sp_decrease = 'next_sp_decrease'


    #latest_ramp_up_sp_key = 'latest_ramp_up_sp_key'


    vac_val_limit_status = 'vac_val_limit'



    # meh ...
    phase_mask_by_power_trace_1_set = 'phase_mask_by_power_trace_1_set'
    phase_mask_by_power_trace_2_set = 'phase_mask_by_power_trace_2_set'

    phase_end_mask_by_power_trace_1_time = 'phase_end_mask_by_power_trace_1_time'
    phase_end_mask_by_power_trace_2_time = 'phase_end_mask_by_power_trace_2_time'

    all_value_keys = [rev_power_spike_count,
                      num_outside_mask_traces,
                      breakdown_rate_aim,
                      vac_spike_status,
                      vac_valve_status,
                      DC_spike_status,
                      DC_level,
                      modulator_state,
                      breakdown_count,
                      breakdown_status,
                      breakdown_rate_hi,
                      breakdown_rate,
                      max_sp_increase,
                      fwd_cav_pwr,
                      fwd_kly_pwr,
                      rev_kly_pwr,
                      rev_cav_pwr,
                      probe_pwr,
                      fwd_kly_pha,
                      rev_kly_pha,
                      rev_cav_pha,
                      fwd_cav_pha,
                      probe_pha,
                      pulse_length,
                      rfprot_state,
                      llrf_output,
                      elapsed_time,
                      llrf_ff_amp_locked,
                      llrf_ff_ph_locked,
                      pulse_count,
                      event_pulse_count,
                      duplicate_pulse_count,
                      water_temp,
                      vac_level,
                      cav_temp,
                      time_stamp,
                      log_pulse_count,
                      llrf_DAQ_rep_rate,
                      llrf_DAQ_rep_rate_status,
                      llrf_DAQ_rep_rate_status_previous,
                      llrf_DAQ_rep_rate_aim,
                      llrf_DAQ_rep_rate_max,
                      llrf_DAQ_rep_rate_min,
                      vac_val_limit_status,
                      can_rf_output_OLD,
                      can_rf_output,
                      log_amp_set,
                      current_ramp_index,
                      power_aim,
                      pulse_length_aim,
                      pulse_length_aim_error,
                      pulse_length_min,
                      pulse_length_max,

                      last_sp_above_100,

                      amp_sp,
                      phi_sp,

                      last_106_bd_count,
                      log_pulse_length,

                      llrf_trigger,
                      llrf_trigger_status,
                      llrf_interlock_status,
                      llrf_interlock,
                      llrf_output_status,
                      llrf_ff_amp_locked_status,
                      llrf_ff_ph_locked_status,
                      pulse_length_status,

                      next_sp_decrease,
                      last_mean_power,
                      next_power_increase,
                      sol_value,
                      phase_mask_by_power_trace_1_set,
                      phase_mask_by_power_trace_2_set,
                      phase_end_mask_by_power_trace_1_time,
                      phase_end_mask_by_power_trace_2_time,
                      x_min,
                      x_max,
                      old_x_min,
                      old_x_max,
                      y_min,
                      y_max,
                      old_y_min,
                      old_y_max,
                      c,
                      m,
                      old_c,
                      old_m,
                      TOR_ACQM,
                      TOR_SCAN,
                      pulse_length_status
                          ]

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
    sp_pwr_hist =[]
    # fitting parameters
    previous_power = 0

    #latest_ramp_up_sp = 0


    values = {}
    [values.update({x: 0}) for x in all_value_keys]


    values[vac_valve_status] = VALVE_STATE.VALVE_ERROR
    #values[rev_power_spike_count] = STATE.UNKNOWN

    values[modulator_state] = GUN_MOD_STATE.UNKNOWN_STATE
    values[rfprot_state] = RF_PROT_STATUS.UNKNOWN

    values[vac_spike_status] = state.UNKNOWN
    values[DC_spike_status] = state.UNKNOWN
    values[breakdown_status] = state.UNKNOWN
    values[llrf_output_status] = state.UNKNOWN
    values[llrf_trigger_status] = state.UNKNOWN
    values[llrf_interlock_status] = state.UNKNOWN
    values[llrf_ff_amp_locked] = state.UNKNOWN
    values[llrf_ff_ph_locked] = state.UNKNOWN
    values[can_rf_output_OLD] = state.UNKNOWN

#sss

    values[last_sp_above_100] = 0
    #values[latest_ramp_up_sp] = 0

    values[vac_val_limit_status] = state.GOOD

    dummy_float = -999.0
    dummy_int = -999.0
    dummy_bool = -999.0



    values[cav_temp] = dummy_float
    values[water_temp] = dummy_float + 1



    values[pulse_length] = dummy_float + 2
    values[rev_kly_pwr] = dummy_float + 5
    values[rev_cav_pwr] = dummy_float + 6
    values[probe_pwr] = dummy_float + 7
    values[vac_level] = dummy_float
    values[breakdown_rate_aim] = dummy_int
    values[breakdown_rate_hi] = dummy_bool


    values[breakdown_rate] = dummy_int+ 11
    values[breakdown_count] = dummy_int +2
    values[pulse_count] = dummy_int + 13
    values[event_pulse_count] = dummy_int +14
    values[duplicate_pulse_count] = dummy_int +14
    values[elapsed_time] = dummy_int + 15
    values[DC_level] = dummy_float + 16
    values[rev_power_spike_count] = dummy_int
    values[next_power_increase] = -1
    values[phase_mask_by_power_trace_1_set] = False
    values[phase_mask_by_power_trace_2_set] = False
    values[phase_end_mask_by_power_trace_1_time] = -1.0
    values[phase_end_mask_by_power_trace_2_time] = -1.0




    values[old_x_min] = dummy_float
    values[old_y_min] = dummy_float
    values[old_x_max] = dummy_float
    values[old_y_max] = dummy_float
    values[old_m] = dummy_float
    values[old_c] = dummy_float
    values[x_min] = dummy_float
    values[x_max] = dummy_float
    values[y_min] = dummy_float
    values[x_max] = dummy_float
    values[m] = dummy_float
    values[c] = dummy_float

    amp_pwr_mean_data = {}
    amp_vs_kfpow_running_stat = {}

    #logger
    logger = None
    _llrf_config = None
    _log_config = None

    last_fwd_kly_pwr = None
    last_amp = None

    #THERE ARE 2 COPIES OF THE last_million_log , FIX THIS !!!!!!!!!!!
    last_million_log = None