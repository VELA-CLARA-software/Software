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


class llrf_monitor(monitor):
    """
    This class handles monitoring of the 'simple' llrf parameters, its gets values for states,
    and means, set-points etc. that are kept in the data.values dictionary.
    It is a passive class and does not control anything (control is in the llrf_handler)
    """


    def __init__(self):
        monitor.__init__(self)

        # aliases
        self.llrf_control = self.hardware.llrf_control
        self.llrf_obj = self.hardware.llrf_obj

        #
        # now match up trace names with the keys for power outputs from the 'values' dict
        self.trace_mean_keys = {}
        #
        # only update new values
        self.old_mean_values = {}
        self.set_mean_dictionaries()

        self.timer.timeout.connect(self.update_value)
        self.timer.start( self.config_data[self.config.LLRF_CHECK_TIME])
        #self.timer.start( 1000 )
        self.set_success = True

        self.old_rf_output = None

        # reference to the values dictionaries
        self.data = rf_conditioning_data.rf_conditioning_data()
        self.values = self.data.values
        self.expert_values = self.data.expert_values
        # new feature, the setting phase end index by remote...
        # if self.llrf_control.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_PHASE_TRACE_1'):
        #     self.phase_trace_1 = monitor.config.breakdown_config['PHASE_MASK_BY_POWER_PHASE_TRACE_1']
        # if monitor.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_PHASE_TRACE_2'):
        #     self.phase_trace_2 = monitor.config.breakdown_config['PHASE_MASK_BY_POWER_PHASE_TRACE_2']
        """ WARNING"""
        # min kyl fwd power to enable incrementing the pulse RF counter
        # THIS SHOULD GO IN THE HANDLER
        # monitor.llrf_control.setActivePulsePowerLimit(monitor.config.llrf_config[
        #        'KLY_PWR_FOR_ACTIVE_PULSE'])
        #; number extra traces to save after an out_side_mask_trace is detected
 #       monitor.llrf_control.setNumExtraTracesOnOutsideMaskEvent(monitor.config.llrf_config[
    #       'EXTRA_TRACES_ON_BREAKDOWN'])

    def set_mean_dictionaries(self):
        # manually set up dicts to monitor trace 'means'
        for trace in self.config_data[self.config.MEAN_TRACES]:
            trace2 = self.llrf_control.fullLLRFTraceName(trace)

            if self.is_cav_reverse_power(trace):
                self.trace_mean_keys[trace2] = self.data.rev_cav_pwr

            elif self.is_cav_forward_power(trace):
                self.trace_mean_keys[trace2] = self.data.fwd_cav_pwr

            elif self.is_kly_forward_power(trace):
                self.trace_mean_keys[trace2] = self.data.fwd_kly_pwr

            elif self.is_kly_forward_phase(trace):
                self.trace_mean_keys[trace2] = self.data.fwd_kly_pha

            elif self.is_kly_reverse_power(trace):
                self.trace_mean_keys[trace2] = self.data.rev_kly_pwr

            elif self.is_probe_power(trace):
                self.trace_mean_keys[trace2] = self.data.probe_pwr

            elif self.is_cav_reverse_phase(trace):
                self.trace_mean_keys[trace2] = self.data.rev_cav_pha

            elif self.is_cav_forward_phase(trace):
                self.trace_mean_keys[trace2] = self.data.fwd_cav_pha

            elif self.is_kly_reverse_phase(trace):
                self.trace_mean_keys[trace2] = self.data.rev_kly_pha

            elif self.is_probe_phase(trace):
                self.trace_mean_keys[trace2] = self.data.probe_pha

            self.old_mean_values[self.llrf_control.fullLLRFTraceName(trace)] = 0

            self.logger.message(__name__ + ' adding ' + trace2 + ' to mean trace list  '
                                   'trace_mean_keys[trace2] = ' + self.trace_mean_keys[trace2])

    def get_cav_pwr_ratio(self):
        '''
            Calculates the cavity reverse power / cavity forward power ratio * 100 ( = cav_pwr_ratio)
            Compares cav_pwr_ratio with minimum allowed ratio as set in the config.yaml
            if cav_pwr_ratio > max allowed then cav_pwr_ratio_status set to state.BAD and cav_pwr_ratio_can_ramp set to False
            if cav_pwr_ratio <= max allowed then cav_pwr_ratio_status set to state.GOOD and cav_pwr_ratio_can_ramp set to True
        '''

        fwd_cav_pwr = self.values[self.data.fwd_cav_pwr]
        rev_cav_pwr = self.values[self.data.rev_cav_pwr]
        cav_pwr_ratio = rev_cav_pwr / fwd_cav_pwr * 100
        self.values[self.data.cav_pwr_ratio] = cav_pwr_ratio
        max_cav_pwr_ratio = self.config.raw_config_data['CAV_PWR_RATIO']

        #print('fwd_cav_pwr = {}\nrev_cav_pwr = {}\ncav_pwr_ratio = {}\nmax_cav_pwr_ratio = {}'.format(fwd_cav_pwr, rev_cav_pwr, cav_pwr_ratio,
        # max_cav_pwr_ratio))

        if cav_pwr_ratio > max_cav_pwr_ratio:
            self.data.values[self.data.cav_pwr_ratio_can_ramp] = state.BAD
            self.data.values[self.data.cav_pwr_ratio_can_ramp] = False
        else:
            self.data.values[self.data.cav_pwr_ratio_can_ramp] = state.GOOD
            self.data.values[self.data.cav_pwr_ratio_can_ramp] = True

        #return cav_pwr_ratio


    def update_value(self):
        """
        Update all the 'simple' LLRF parameters, these are generally states and single numbers.
        The states can be the LLRF state, and/or a derived state (good bad, NEW_Good, NEW_BAD etc)
        required for the control of the main conditioning loop
        """
        #print("update_value LLRF clalled")
        #
        ''' send keep alive pulse'''
        # NO - do this on a seperate timeer!
        #self.llrf_control.keepAlive()

        ''' get the mean value for each trace '''
        for trace, key in self.trace_mean_keys.iteritems():
            #print("Get mean power for ", trace)
            self.get_mean_power(key, trace)

        # Check the cavity power ratio
        self.get_cav_pwr_ratio()

        ''' UPDATE LLRF values that are REQUIRED TO BE ABLE TO RAMP '''
        self.update_interlock_state()
        self.update_trigsource_state()
        self.update_rf_output_state()
        self.update_ff_amp_lock_state()
        self.update_ff_phase_lock_state()
        #self.update_daq_rep_rate()

        self.update_pulse_length()

        ''' update simple values '''
        self.values[self.data.amp_sp] = self.llrf_obj[0].amp_ff
        # TODO THIS SHOULD BE THE AMP_SP we're not sure wy, but the Libera controls the SP is now
        #  "broke"
        # print( int(self.llrf_obj[0].amp_sp) ) # does not work
        # print( int(self.llrf_obj[0].amp_sp) ) # does not work
        # print( int(self.llrf_obj[0].amp_ff) ) # does not work
        # print( int(self.llrf_obj[0].amp_ff) ) # does not work
        # print 'amp_sp = {}'.format(self.values[self.data.amp_sp])
        self.values[self.data.phi_sp] = int(self.llrf_obj[0].phi_sp)
        self.values[self.data.TOR_ACQM] = self.llrf_control.getTORACQM()
        self.values[self.data.TOR_SCAN] = self.llrf_control.getTORSCAN()
        self.values[self.data.duplicate_pulse_count] = self.llrf_obj[0].duplicate_pulse_count
        self.values[self.data.llrf_trace_interlock] = self.llrf_control.areLLRFTraceInterlocksGood()

        # CATAP max amp setpoint value
        # This number CANNOT CHANGE WHILE RUNNING !!
        self.values[self.data.catap_max_amp] = self.llrf_control.getMaxAmpSP()
        ''' the latest running stats for this amp_set (from the c++) '''
        ## THIS GETS UPDATED TOO FREQUENTLY
        # if(self.llrf_control.isKeepingKlyFwdPwrRS()):
        #     self.update_amp_vs_kfpow_running_stat()
        #
        """WARNING"""
        # if setting phase trace end masks by value get those values...
        # if self.values[self.data.phase_mask_by_power_trace_1_set]:
        #     self.values[self.data.phase_end_mask_by_power_trace_1_time] = \
        #         monitor.llrf_control.getMaskInfiniteEndByPowerTime(self.phase_trace_1 )
        # if self.values[self.data.phase_mask_by_power_trace_2_set]:
        #     self.values[self.data.phase_end_mask_by_power_trace_2_time] = \
        #         monitor.llrf_control.getMaskInfiniteEndByPowerTime( self.phase_trace_1 )

        # get delta_power  last setpoint power - current setpoint power (last_sp values set in set_amp in llrf_control
        ''' it can happen that we've changed amp_sp but there have been no pulses when  we get here,  amp_vs_kfpow_running_stat can be empty '''
        if self.values[self.data.amp_sp] in self.data.amp_vs_kfpow_running_stat:
            self.values[self.data.delta_kfpow] = self.data.get_kf_running_stat_power_at_current_set_point() - self.values[
                self.data.kfpower_at_last_amp_sp]

    # def update_daq_rep_rate(self):
    #     ''' DATA ACQUISIATION REP RATE
    #     The llrf controller estimates the daq frequency from the timestamps of the trace data
    #     previous observed behaviour has shown this rate can change due to:
    #         something happening in the llrf box,
    #         something happening on the network,
    #         something else.
    #     If the daq_rep_rate deviates from what is expected we want to disable RF power until it
    #     returns. We also  keep a memory of the previous state, and compare. If previous state was
    #     BAD and now state is GOOD we call this NEW_GOOD, similarly GOOD to BAD is a NEW_BAD
    #     we use a NEW_GOOD to enable us to respond to changes in daq_rep_rate
    #     '''
    #     DAQ_rep_rate = self.data.llrf_DAQ_rep_rate
    #     DAQ_rep_rate_status = self.data.llrf_DAQ_rep_rate_status
    #     self.values[DAQ_rep_rate] = self.llrf_obj[0].trace_rep_rate
    #
    #     if self.values[DAQ_rep_rate] < self.values[self.data.llrf_DAQ_rep_rate_min]:
    #         self.values[DAQ_rep_rate_status] = state.BAD
    #
    #     elif self.values[DAQ_rep_rate] > self.values[self.data.llrf_DAQ_rep_rate_max]:
    #         self.values[DAQ_rep_rate_status] = state.BAD
    #     else:
    #         self.values[self.data.llrf_DAQ_rep_rate_status] = state.GOOD
    #
    #     if self.values[self.data.llrf_DAQ_rep_rate_status_previous] == state.BAD:
    #         if self.values[DAQ_rep_rate_status] == state.GOOD:
    #             self.values[DAQ_rep_rate_status] = state.NEW_GOOD
    #     self.values[self.data.llrf_DAQ_rep_rate_status_previous] = self.values[DAQ_rep_rate_status]

    def update_pulse_length(self):
        '''
        HOW DO WE ACTUALLY DEFINE PULSE LENGTH!!!!!!!!!!!!

        :return:
        '''
        #

        # pulse length
        # THIS OLD WAY IS NOW BROKE, we use an RF RAMP table Instead we now use the  getPulseShape vector and count the number of 1.0s (SketchyAF)
        # pulse length

        # TODO: Is this the same method for the linac and the gun ???

        #self.values[self.data.pulse_length] = self.llrf_control.getPulseShape().count(1) * 0.009 * 1000
        self.values[self.data.pulse_length] = self.llrf_control.getPulseShape().count(1) * 9
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # MAGIC THIS IS NOT EXACTLY CORRECT,
        if self.values[self.data.pulse_length] < self.values[self.data.pulse_length_min]:
            self.values[self.data.pulse_length_status] = state.BAD
        elif self.values[self.data.pulse_length] > self.values[self.data.pulse_length_max]:
            self.values[self.data.pulse_length_status] = state.BAD
        else:
            self.values[self.data.pulse_length_status] = state.GOOD

    def update_interlock_state(self):
        '''

        :return:
        '''
        self.values[self.data.llrf_interlock] = self.llrf_obj[0].interlock_state
        if self.values[self.data.llrf_interlock] == INTERLOCK_STATE.NON_ACTIVE:
            self.values[self.data.llrf_interlock_status] = state.GOOD
        else:
            self.values[self.data.llrf_interlock_status] = state.BAD

    def update_trigsource_state(self):
        '''

        :return:
        '''
        #
        #
        self.values[self.data.llrf_trigger] = self.llrf_obj[0].trig_source
        if self.values[self.data.llrf_trigger] == TRIG.OFF:
            self.values[self.data.llrf_trigger_status] = state.BAD
        elif self.values[self.data.llrf_trigger] == TRIG.UNKNOWN_TRIG:
            self.values[self.data.llrf_trigger_status] = state.BAD
        else:
            self.values[self.data.llrf_trigger_status] = state.GOOD

    def update_rf_output_state(self):
        '''

        :return:
        '''
        self.values[self.data.llrf_output] = self.llrf_obj[0].rf_output
        if self.values[self.data.llrf_output]:
            self.values[self.data.llrf_output_status] = state.GOOD
        else:
            self.values[self.data.llrf_output_status] = state.BAD

        if self.llrf_obj[0].rf_output != self.old_rf_output:
            if self.llrf_obj[0].rf_output:
                self.alarm('rf_on')
            else:
                self.alarm('rf_off')
            self.old_rf_output = self.llrf_obj[0].rf_output

    def update_ff_amp_lock_state(self):
        '''

        '''
        self.values[self.data.llrf_ff_amp_locked] = self.llrf_obj[0].ff_amp_lock_state
        if self.values[self.data.llrf_ff_amp_locked]:
            self.values[self.data.llrf_ff_amp_locked_status] = state.GOOD
        else:
            self.values[self.data.llrf_ff_amp_locked_status] = state.BAD
        #

    def update_ff_phase_lock_state(self):
        '''

        '''
        self.values[self.data.llrf_ff_ph_locked] =  self.llrf_obj[0].ff_ph_lock_state
        if self.values[self.data.llrf_ff_ph_locked]:
            self.values[self.data.llrf_ff_ph_locked_status] = state.GOOD
        else:
            self.values[self.data.llrf_ff_ph_locked_status] = state.BAD

    def update_amp_vs_kfpow_running_stat(self):
        '''
            This function is updating the python dictionary  amp_vs_kfpow_running_stat with teh
            values form the c++ amp_vs_kfpow_running_stat data
            The c++ data includes every pulse, and so is the "most accurate"
            TODO: we could  expose the c++ data to python and NEVER use a local copy in python

            TODO how often does amp_vs_kfpow_running_stat get "synchronized" with the c++ data?

        '''

        # I lost the thread at the C++ here...
        # print("Looking in c++ amp_v_kfpow for {}".format(self.values[self.data.amp_sp]))
        self.data.amp_vs_kfpow_running_stat[self.values[self.data.amp_sp]] = \
            self.llrf_control.getKlyFwdPwrRSState( int(self.values[self.data.amp_sp])) # TODO THIS HAS TO BE AN INT IN THE C++ ??? WTF
        # TODO need c++ to return zeros if the key does not exist
        #print("update amp_vs_kfpow_running_stat with amp_sp = {}".format(self.values[self.data.amp_sp]))

    def get_mean_power(self,key,trace):
        """
        get the mean reading for trace-trace and append it to values dict with key=key
        :param key: key fro values dictionary, where to put the data
        :param trace: trace identifier, which trace to get data for
        """
        v = self.llrf_obj[0].trace_data[trace].mean
        #print "key = " + str(key) + ", " + trace + " mean value = " +  str(v)
        if  self.old_mean_values[trace] == v:
            pass
        else:
            self.values[key] = self.llrf_obj[0].trace_data[trace].mean
            self.old_mean_values[trace] = self.values[key]

            # i probably dont need to do this anymore as we're now doing it in the c++
            # if self.is_kly_forward_power(trace):
            #     if self.old_mean_values[trace] > monitor.config.llrf_config['KLY_PWR_FOR_ACTIVE_PULSE']:
            #         self.update_amp_pwr_mean_dict(monitor.data.values[dat.amp_sp],self.old_mean_values[trace])

    ''' The below were made as function in case i had to use them elsewhere, then perhaps they
    could go in a utiliites space, so far they are only used here'''
    def is_kly_forward_power(self,str):
        return 'KLYSTRON_FORWARD_POWER' in str

    def is_kly_reverse_power(self,str):
        return 'KLYSTRON_REVERSE_POWER' in str

    def is_cav_forward_power(self,str):
        return 'CAVITY_FORWARD_POWER' in str

    def is_cav_reverse_power(self,str):
        return 'CAVITY_REVERSE_POWER' in str

    def is_probe_power(self, str):
        return 'PROBE_POWER' in str

    def is_kly_forward_phase(self,str):
        return 'KLYSTRON_FORWARD_PHASE' in str

    def is_kly_reverse_phase(self,str):
        return 'KLYSTRON_REVERSE_PHASE' in str

    def is_cav_forward_phase(self,str):
        return 'CAVITY_FORWARD_PHASE' in str

    def is_cav_reverse_phase(self,str):
        return 'CAVITY_REVERSE_PHASE' in str

    def is_probe_phase(self,str):
        return 'PROBE_PHASE' in str


    def get_llrf_expert_values(self):
        '''
        The "expert_panel" parameters are only updated when the button is clicked and this
        function is  called. They are all stored in expert_values dict
        :return:
        '''
        # DUMMY
        # get Trace info
        # for trace in  self.llrf_control.getTraceNames():
        #     print("Getting Expert values for ", trace)

        ev = self.expert_values

        trace = 'KLYSTRON_FORWARD_POWER'
        ev[self.data.mask_level_kf_pow] = self.llrf_control.getMaskValue(trace)
        ev[self.data.mask_start_kf_pow] = self.llrf_control.getMaskStartIndex(trace)
        ev[self.data.mask_end_kf_pow] = self.llrf_control.getMaskEndIndex(trace)
        ev[self.data.mask_min_kf_pow] = self.llrf_control.getMaskFloor(trace)
        ev[self.data.mask_window_start_kf_pow] = self.llrf_control.getMaskWindowStartIndex(trace)
        ev[self.data.mask_window_end_kf_pow] = self.llrf_control.getMaskWindowEndIndex(trace)
        ev[self.data.streak_kf_pow] = self.llrf_control.getNumContinuousOutsideMaskCount(trace)


        trace = 'CAVITY_FORWARD_POWER'
        ev[self.data.mask_level_cf_pow] = self.llrf_control.getMaskValue(trace)
        ev[self.data.mask_start_cf_pow] = self.llrf_control.getMaskStartIndex(trace)
        ev[self.data.mask_end_cf_pow] = self.llrf_control.getMaskEndIndex(trace)
        ev[self.data.mask_min_cf_pow] = self.llrf_control.getMaskFloor(trace)
        ev[self.data.mask_window_start_cf_pow] = self.llrf_control.getMaskWindowStartIndex(trace)
        ev[self.data.mask_window_end_cf_pow] = self.llrf_control.getMaskWindowEndIndex(trace)
        ev[self.data.streak_cf_pow] = self.llrf_control.getNumContinuousOutsideMaskCount(trace)

        trace = 'CAVITY_REVERSE_POWER'
        ev[self.data.mask_level_cr_pow] = self.llrf_control.getMaskValue(trace)
        ev[self.data.mask_start_cr_pow] = self.llrf_control.getMaskStartIndex(trace)
        ev[self.data.mask_end_cr_pow] = self.llrf_control.getMaskEndIndex(trace)
        ev[self.data.mask_min_cr_pow] = self.llrf_control.getMaskFloor(trace)
        ev[self.data.mask_window_start_cr_pow] = self.llrf_control.getMaskWindowStartIndex(trace)
        ev[self.data.mask_window_end_cr_pow] = self.llrf_control.getMaskWindowEndIndex(trace)
        ev[self.data.streak_cr_pow] = self.llrf_control.getNumContinuousOutsideMaskCount(trace)

        trace = 'CAVITY_PROBE_POWER'
        ev[self.data.mask_level_cp_pow] = self.llrf_control.getMaskValue(trace)
        ev[self.data.mask_start_cp_pow] = self.llrf_control.getMaskStartIndex(trace)
        ev[self.data.mask_end_cp_pow] = self.llrf_control.getMaskEndIndex(trace)
        ev[self.data.mask_min_cp_pow] = self.llrf_control.getMaskFloor(trace)
        ev[self.data.mask_window_start_cp_pow] = self.llrf_control.getMaskWindowStartIndex(trace)
        ev[self.data.mask_window_end_cp_pow] = self.llrf_control.getMaskWindowEndIndex(trace)
        ev[self.data.streak_cp_pow] = self.llrf_control.getNumContinuousOutsideMaskCount(trace)


        trace = 'KLYSTRON_FORWARD_PHASE'
        ev[self.data.mask_level_kf_pha] = self.llrf_control.getMaskValue(trace)
        ev[self.data.mask_start_kf_pha] = self.llrf_control.getMaskStartIndex(trace)
        ev[self.data.mask_end_kf_pha] = self.llrf_control.getMaskEndIndex(trace)
        ev[self.data.mask_min_kf_pha] = self.llrf_control.getMaskFloor(trace)
        ev[self.data.mask_window_start_kf_pha] = self.llrf_control.getMaskWindowStartIndex(trace)
        ev[self.data.mask_window_end_kf_pha] = self.llrf_control.getMaskWindowEndIndex(trace)
        ev[self.data.streak_kf_pha] = self.llrf_control.getNumContinuousOutsideMaskCount(trace)


        trace = 'CAVITY_FORWARD_PHASE'
        ev[self.data.mask_level_cf_pha] = self.llrf_control.getMaskValue(trace)
        ev[self.data.mask_start_cf_pha] = self.llrf_control.getMaskStartIndex(trace)
        ev[self.data.mask_end_cf_pha] = self.llrf_control.getMaskEndIndex(trace)
        ev[self.data.mask_min_cf_pha] = self.llrf_control.getMaskFloor(trace)
        ev[self.data.mask_window_start_cf_pha] = self.llrf_control.getMaskWindowStartIndex(trace)
        ev[self.data.mask_window_end_cf_pha] = self.llrf_control.getMaskWindowEndIndex(trace)
        ev[self.data.streak_cf_pha] = self.llrf_control.getNumContinuousOutsideMaskCount(trace)

        trace = 'CAVITY_REVERSE_PHASE'
        ev[self.data.mask_level_cr_pha] = self.llrf_control.getMaskValue(trace)
        ev[self.data.mask_start_cr_pha] = self.llrf_control.getMaskStartIndex(trace)
        ev[self.data.mask_end_cr_pha] = self.llrf_control.getMaskEndIndex(trace)
        ev[self.data.mask_min_cr_pha] = self.llrf_control.getMaskFloor(trace)
        ev[self.data.mask_window_start_cr_pha] = self.llrf_control.getMaskWindowStartIndex(trace)
        ev[self.data.mask_window_end_cr_pha] = self.llrf_control.getMaskWindowEndIndex(trace)
        ev[self.data.streak_cr_pha] = self.llrf_control.getNumContinuousOutsideMaskCount(trace)

        trace = 'CAVITY_PROBE_PHASE'
        ev[self.data.mask_level_cp_pha] = self.llrf_control.getMaskValue(trace)
        ev[self.data.mask_start_cp_pha] = self.llrf_control.getMaskStartIndex(trace)
        ev[self.data.mask_end_cp_pha] = self.llrf_control.getMaskEndIndex(trace)
        ev[self.data.mask_min_cp_pha] = self.llrf_control.getMaskFloor(trace)
        ev[self.data.mask_window_start_cp_pha] = self.llrf_control.getMaskWindowStartIndex(trace)
        ev[self.data.mask_window_end_cp_pha] = self.llrf_control.getMaskWindowEndIndex(trace)
        ev[self.data.streak_cp_pha] = self.llrf_control.getNumContinuousOutsideMaskCount(trace)


        print(
        self.data.mask_level_cp_pha,  ev[self.data.mask_level_cp_pha],
        self.data.mask_start_cp_pha ,  ev[self.data.mask_start_cp_pha] ,
        self.data.mask_end_cp_pha   ,  ev[self.data.mask_end_cp_pha]   ,
        self.data.mask_min_cp_pha   ,  ev[self.data.mask_min_cp_pha]   ,
        self.data.mask_window_start_cp_pha,  ev[self.data.mask_window_start_cp_pha],
        self.data.mask_window_end_cp_pha ,  ev[self.data.mask_window_end_cp_pha] ,
        self.data.streak_cp_pha ,  ev[self.data.streak_cp_pha]
        )



        # bool isGlobalCheckMask()const;
        # bool isPercentMask(const std::string& name)const;
        # bool isAbsoluteMask(const std::string& name)const;
        # bool isCheckingMask(const std::string& name)const;
        # bool isNotCheckingMask(const std::string& name)const;
        # bool isCheckingMask(const llrfStructs::LLRF_PV_TYPE pv)const;
        # bool isNotCheckingMask(const llrfStructs::LLRF_PV_TYPE pv)const;



        #
        # self.expert_values[self.data.is_breakdown_monitor_kf_pow] = False
        # self.expert_values[self.data.is_breakdown_monitor_kr_pow] = False
        # self.expert_values[self.data.is_breakdown_monitor_cf_pow] = False
        # self.expert_values[self.data.is_breakdown_monitor_cr_pow] = False
        # self.expert_values[self.data.is_breakdown_monitor_cp_pow] = False
        # self.expert_values[self.data.is_breakdown_monitor_kf_pha] = False
        # self.expert_values[self.data.is_breakdown_monitor_kr_pha] = False
        # self.expert_values[self.data.is_breakdown_monitor_cf_pha] = False
        # self.expert_values[self.data.is_breakdown_monitor_cr_pha] = False
        # self.expert_values[self.data.is_breakdown_monitor_cp_pha] = False


        # THIS IS THE NEW WAY TO GET POWER DATA
    # we should check the value has changed !
    # this needs to go into the c++ (!)
    # this needs to go into the c++ (!)
    # this needs to go into the c++ (!)
    # this needs to go into the c++ (!)
    # def update_amp_pwr_mean_dict(self,x,x2):
    #     # amp_pwr_mean_data[amp_sp] { pwr_total,pwr_total_count, current_mean, max, min]
    #     #print('called')
    #     if x not in monitor.data.amp_pwr_mean_data:
    #         monitor.data.amp_pwr_mean_data.update({x :[0,0,0,0,0]})
    #         monitor.data.amp_pwr_mean_data[x][0] += x2
    #         monitor.data.amp_pwr_mean_data[x][1] += 1
    #         monitor.data.amp_pwr_mean_data[x][2] = float(monitor.data.amp_pwr_mean_data[x][0]) / float(monitor.data.amp_pwr_mean_data[x][1])
    #     if monitor.data.amp_pwr_mean_data[x][3] > x:
    #         monitor.data.amp_pwr_mean_data[x][3] = x
    #     elif monitor.data.amp_pwr_mean_data[x][4] < x:
    #         monitor.data.amp_pwr_mean_data[x][4] = x
    #     monitor.data.values[dat.last_mean_power] = monitor.data.amp_pwr_mean_data[x][2]