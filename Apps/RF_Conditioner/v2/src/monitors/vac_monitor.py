#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
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
//  Last edit:   01-07-2019
//  FileName:    vac_monitor.py
//  Description: checks the state of the RF Vac Valve for the RF_STRUCTURE being conditioned
//
//*/
"""
from monitor import monitor
from src.data.state import state
from PyQt4.QtCore import QTimer
import src.data.rf_condition_data_base as dat
from numpy import mean


class vac_monitor(monitor):
    """
    This class has been through a few iterations. Originally there was a generic spike monitor,
    so we could look for spikes in different signals (e.g. vacuum and dark_current (DC) However,
    DC goes at the RF rep rate (up to 100Hz) and, in general, python is not the appropriate place to
    look for signals at that rep-rate. Plus the RF traces and vac are more than enough to actual
    trigger events
    #########################
    This class, monitors the vacuum level and keeps a rolling mean, if the level "spikes" by
    an amount set in the config then a BAD state is set, which the conditioning_main_loop
    responds to. The state goes back to GOOD either when a time limit has passed, or,
    more commonly, the vacuum level returns below the limit
    If the vacuum level gets above VAC_MAX_LEVEL  vac_hi_limit_status is set to BAD,
    when the vacuum level is <= VAC_MAX_LEVEL vac_hi_limit_status is set to GOOD
    """
    def __init__(self,):
        monitor.__init__(self)
        #
        # Local copies for some important  settings from the config file
        self.spike_delta = self.config_data[self.config.VAC_SPIKE_DELTA]
        self.spike_decay_level = self.config_data[self.config.VAC_SPIKE_DECAY_LEVEL]
        self.spike_decay_time = self.config_data[self.config.VAC_SPIKE_DECAY_TIME]
        self.num_samples_to_average = self.config_data[self.config.VAC_NUM_SAMPLES_TO_AVERAGE]
        self.should_drop_amp = self.config_data[self.config.VAC_SHOULD_DROP_AMP]
        self.amp_drop_value = self.config_data[self.config.VAC_SPIKE_AMP_DROP]
        self.max_level = self.config_data[self.config.VAC_MAX_LEVEL]

        # Count how many spikes we have detected:
        self.spike_count = 0

        # shorthand aliases
        self.gen_mon = self.hardware.gen_mon

        # connect to the vac PV
        self.id_key = 'VAC_ID'# MAGIC_STRING  The key for the gen_mon keys dictionary
        self.id = ''          # MAGIC_STRING, The value returned by gen_mon after connecting
        self.vac_connected = self.hardware.connectPV(self.id_key, self.config_data[
            self.config.VAC_PV])
        if self.vac_connected:
            self.id = self.hardware.gen_mon_keys[self.id_key]

        # These are the relevant keys for the data dictionary
        # Key for the vacuum level
        self.data_dict_val_key = self.data.vac_level
        # Key for the state of the vacuum (spike or not spike)
        self.data_dict_state_key = self.data.vac_spike_status

        """some variables  for the vacuum data"""
        self._reading_counter = -1  # counter for latest value acquired from control system
        self._latest_value = None   # latest value acquired from control system
        self._mean_level = None     # current mean of _value_history
        self._value_history = []    # list of previous values used to calculate the rolling mean

        # check if we should drop amp on a spike
        if self.should_drop_amp:
            self.logger.message(__name__ + ' will drop amp on spike detection',True)
        else:
            self.logger.message(__name__ + ' will NOT drop amp on spike detection',True)

        # set cool-down mode based on config, default will be LEVEL (monitor base class function)
        self.set_cooldown_mode(self.config_data[self.config.VAC_DECAY_MODE])

        # a timer to run check_signal automatically every self.update_time
        # this gets the vacuum data and checks it, it's the "main loop" for this class
        self.timer.timeout.connect(self.check_signal)

        # A timer for TIME cooldowns, (not generally sued for vacuum) the spike  detcetin will
        # start the timer, when the timer runs out it calls self.cooldown_function
        self.cooldown_timer.timeout.connect(self.cooldown_finished)


        # a timer for the minimum cooldown period, when a vac spike occurs this timer is
        # started to, give a minimum time before we can set a GOOD state.
        self.min_cooldown_timer = QTimer()
        self.min_cooldown_timer.setSingleShot(True)
        self.min_cooldown_timer.timeout.connect(self.min_cooldown_finished)
        self.min_time_good = True

        # the amount above baseline (self._mean_level) that triggers a vacuum spike event
        try:
            self.spike_delta = self.config_data[self.config.VAC_SPIKE_DELTA]
        except:
            self.spike_delta = None
        # factor applied to _mean_level to set the "recovered from spike" value
        # we're setting a recovery based on vacuum level not time here
        # this is for 'level' cool-down mode
        try:
            self.spike_decay_level = self.config_data[self.config.VAC_SPIKE_DECAY_LEVEL]
        except:
            self.spike_decay_level = 1.1


        # set-up if we are disabling ramping based on  passed level
        self.should_check_level_is_hi = False
        try:
            if self.max_level:
                if self.data_dict_val_limit_status_key:
                    self.should_check_level_is_hi = True
        except:
            self.should_check_level_is_hi = False


        # initialise data to state unknown
        self.data.values[self.data.vac_spike_status] = state.UNKNOWN
        # now we're ready to start run-this
        self.run()

    def run(self):
        """
        This function actually starts the main timer that gets data
        call this fucntion when ready to start checking vacuum

        """
        m = self.logger.message
        dssk = self.data.vac_spike_status
        item = [self.spike_delta, self.spike_decay_level, self.cool_down_time]
        if self.sanity_checks(item):
            self.timer.start(self.config_data[self.config.VAC_CHECK_TIME])
            m(__name__ + ' STARTED running')
            m(__name__ + ' ' + self.data_dict_state_key + ' = ' + str(self.values[dssk]))
            self.set_good()
            m(__name__ + ' ' + self.data_dict_state_key + ' = ' + str(self.values[dssk]))
        else:
            m(__name__ + ' NOT STARTED running')

    def check_signal(self):
        """
        This is the main function that is called in a loop by self.timer
        It's the vacuum monitor main_loop
        get a new vacuum value,
            if in cool-down,
                check if cool-down should end (based on value or time)
            else:
                checks for a spike
            if we are checking for hi vacuum levels
                check for high vacuum level
        """
        if self.update_value():              # if we get a new value

            self.update_mean_value()


            if self._in_cooldown:            # if in cool-down,
                self.check_has_cooled_down() # check to see if we should stay in cool-down
            else:
                self.check_for_spike()       # check if new value is a vacuum  spike
            if self.should_check_level_is_hi:
                self.check_if_level_is_hi()

    def update_mean_value(self):
        """
        update the _value_history, if buffer full, remove oldest value then calculate the next
        mean value
        :return:
        """
        # update _values_history,
        self._value_history.append(self._latest_value)
        if len(self._value_history) > self.num_samples_to_average:
            self._value_history.pop(0)
            self._mean_level = sum(self._value_history)/self.num_samples_to_average


    def update_value(self):
        """
        This function tried to get the latest value from the gen_mon,
        The gen_mon can return a counter and a value, if the counter has increased since the last
        check, the value MUST be new (even if it is the same value).
        :return: is the value new or not?
        """
        # v is a dict of {counter : value }
        v = self.gen_monitor.getCounterAndValue(self.id)
        # the gen_monitor will just pass back the last value it has
        # value is a new value if counter has increased since last check
        if v.keys()[0] != self._reading_counter: # value must be new
            # update _latest_value
            self._latest_value = v.values()[0]
            # update main data dictionary
            self.data.values[self.data_dict_val_key] = self._latest_value
            # set new _reading_counter
            self._reading_counter = v.keys()[0]
            # return True, we got a new value
            return True
        # Return false, we did not get a new value
        return False

    def check_if_level_is_hi(self):
        """
        If the vacuum goes above self.max_level, we set vac_hi_limit_status to BAD, else it is
        GOOD. We also message the log each time the state changes
        :return:
        """
        old_state = self.data.values[self.data.vac_hi_limit_status]
        if self._latest_value > self.max_level:  # if level is hi
            self.data.values[self.data.vac_hi_limit_status] = state.BAD  # Set BAD status

            if old_state == state.GOOD: # If state changed write message
                m = __name__ + ' level hi, {} > {} '.format(self._latest_value,self.max_level)
                self.logger.message(m, add_to_text_log=True, show_time_stamp=True)

        else: # else level is NOT hi
            self.data.values[self.data.vac_hi_limit_status] = state.GOOD

            if old_state == state.BAD: # If state changed write message
                m = __name__ + ' level ok, {} < {} '.format(self._latest_value,self.max_level)
                self.logger.message(m, add_to_text_log=True, show_time_stamp=True)

    def check_has_cooled_down(self):
        """
        For LEVEL mode cool-down ends when the level returns to good
        """
        if self.level_cooldown:
            if self._latest_value < self.spike_decay_level * self._mean_level:
                if self.min_time_good:
                    self.logger.message(__name__+' has_cooled_down', add_to_text_log=True,
                                        show_time_stamp=True)
                    self.in_cooldown = False

    def check_for_spike(self):
        """
        A spike is defined as:  value > current_mean_value + self.spike_delta
        self.spike_delta is defined in the config 'VAC_SPIKE_DELTA'
        current_mean_value is a rolling mean of the previous  self._num_samples_to_average
        self._num_samples_to_average 'VAC_NUM_SAMPLES_TO_AVERAGE'
        :return:
        """
        if self._mean_level is not None: # If we have a mean value
            # check for a spike
            if self._latest_value > self.spike_delta + self._mean_level:
                # this is the first place we can detect a vacuum spike,
                # so drop amp here if we are in a GOOD state
                if self.should_drop_amp:
                    if self.values[self.data.breakdown_status] == state.GOOD:
                        self.hardware.llrf_control.setAmpHP(self.amp_drop_value)
                self.spike_count += 1
                m = __name__ + ' NEW vacuum spike, #{}: '.format(self.spike_count)
                m += "{} > {} + {}.".format(self._latest_value, self.spike_delta, self._mean_level)
                self.logger.header(m, add_to_text_log=True, show_time_stamp=True)
                self.dump_data()
                self.start_cooldown()


    def min_cooldown_finished(self):
        self.min_time_good = True

    def start_cooldown(self):
        """
        sets cooldown conditions:
        in_cooldown flag to true
        starts min_cooldown_timer
        if in times cooldown mode start cooldown_timer
        :return:
        """
        # SHOULD WE FORCE AN INCREASE IN THE BREAKDOWN COUNT???? NOPE,unless we need to  ... meh
        # I have commented this out for now, but in the FUTURE we'll ... DEBUG
        self.in_cooldown = True
        self.min_time_good = False
        self.min_cooldown_timer.start(self.config_data[self.config.MINIMUM_COOLDOWN_TIME])
        if self.timed_cooldown:         # if in timed_cooldown mode start the cooldown timer
            self.cooldown_timer.start(self.config_data[self.config.VAC_SPIKE_DECAY_TIME])

    def cooldown_finished(self):
        # when the cooldown timer ends this function is called,  pass false to in_cooldown
        # property, which then sets vac_spike_status STATUS
        self.in_cooldown = False

    @property
    def in_cooldown(self):
        return self._in_cooldown

    @property
    def latest_value(self):
        return self._latest_value

    @in_cooldown.setter
    def in_cooldown(self,value):
        """
        This property is a flag for if we are in cooldown or not. The vac state  is inverse to the
        in_cooldown state
        If in_cooldown == TRUE, then the vac_spike_status = BAD
        If in_cooldown == FALSE, then the vac_spike_status = GOOD
        :param value: True or False
        :return:
        """
        self._in_cooldown = value
        if value:
            self.set_bad()
        else:
            self.set_good()

    def set_bad(self):
        self.data.values[self.data.vac_spike_status] = state.BAD

    def set_good(self):
        self.data.values[self.data.vac_spike_status] = state.GOOD

    def dump_data(self):
        """
        Get RF trace data from llrf_control and Pickle dump the vacuum data + other stuff
        """
        new = self.hardware.llrf_control.getCutOneTraceData() # get data from CATAP llrf_control
        new.update({'vacuum': self._value_history})
        new.update({'DC': self.data.values[self.data.DC_level]})
        new.update({'SOL': self.data.values[self.data.sol_value]})
        self.logger.pickle_file(__name__ + '_' + str(self.spike_count), new)

