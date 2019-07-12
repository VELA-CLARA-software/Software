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
import src.data.rf_condition_data_base as dat
from src.data.state import state
from VELA_CLARA_LLRF_Control import TRIG
from VELA_CLARA_LLRF_Control import INTERLOCK_STATE

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

        # new feature, the setting phase end index by remote...
        # if self.llrf_control.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_PHASE_TRACE_1'):
        #     self.phase_trace_1 = monitor.config.breakdown_config['PHASE_MASK_BY_POWER_PHASE_TRACE_1']
        # if monitor.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_PHASE_TRACE_2'):
        #     self.phase_trace_2 = monitor.config.breakdown_config['PHASE_MASK_BY_POWER_PHASE_TRACE_2']

        """ WARNING"""
        # min kyl fwd power to enable incrementing the pulse RF counter
        # THIS SHOULD GO IN THE HANDLER
#        monitor.llrf_control.setActivePulsePowerLimit(monitor.config.llrf_config[
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

    def update_value(self):
        """
        Update all the 'simple' LLRF parameters, these are generally states and single numbers.
        The states can be the LLRF state, and/or a derived state (good bad, NEW_Good, NEW_BAD etc)
        required for the control of the main conditioning loop
        """
        #
        ''' send keep alive pulse'''
        self.llrf_control.keepAlive()

        ''' get the mean value for each trace '''
        for trace, key  in self.trace_mean_keys.iteritems():
            self.get_mean_power(key, trace)

        ''' UPDATE LLRF values that are REQUIRED TO BE ABLE TO RAMP '''
        self.update_interlock_state()
        self.update_trigsource_state()
        self.update_rf_output_state()
        self.update_ff_amp_lock_state()
        self.update_ff_phase_lock_state()
        self.update_daq_rep_rate()

        self.update_pulse_length()

        ''' update simple values '''
        self.values[self.data.amp_sp] = int(self.llrf_obj[0].amp_sp)
        self.values[self.data.phi_sp] = int(self.llrf_obj[0].phi_sp)
        self.values[self.data.TOR_ACQM] = self.llrf_control.getTORACQM()
        self.values[self.data.TOR_SCAN] = self.llrf_control.getTORSCAN()
        self.values[self.data.duplicate_pulse_count] = self.llrf_obj[0].duplicate_pulse_count


        ''' the latest running stats for this amp_set (from the c++) '''
        ## THIS GETS UPDATED TOO FREQUENTLY
        if(self.llrf_control.isKeepingKlyFwdPwrRS()):
            self.update_amp_vs_kfpow_running_stat()

        #
        """WARNING"""
        # if setting phase trace end masks by value get those values...
        # if self.values[self.data.phase_mask_by_power_trace_1_set]:
        #     self.values[self.data.phase_end_mask_by_power_trace_1_time] = \
        #         monitor.llrf_control.getMaskInfiniteEndByPowerTime(self.phase_trace_1 )
        # if self.values[self.data.phase_mask_by_power_trace_2_set]:
        #     self.values[self.data.phase_end_mask_by_power_trace_2_time] = \
        #         monitor.llrf_control.getMaskInfiniteEndByPowerTime( self.phase_trace_1 )


    def update_daq_rep_rate(self):
        ''' DATA ACQUISIATION REP RATE
        The llrf controller estimates the daq frequency from the timestamps of the trace data
        previous observed behaviour has shown this rate can change due to:
            something happening in the llrf box,
            something happening on the network,
            something else.
        If the daq_rep_rate deviates from what is expected we want to disable RF power until it
        returns. We also  keep a memory of the previous state, and compare. If previous state was
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

    def update_pulse_length(self):
        '''
        HOW DO WE ACTUALLY DEFEIN PULSE LENGTH!!!!!!!!!!!!

        :return:
        '''
        #
        # pulse length
        # THIS OLD WAY IS NOW BROKE, we use an RF RAMP table Instead we now use the  getPulseShape vector and count the number of 1.0s (SketchyAF)
        # pulse length
        self.values[self.data.pulse_length] = self.llrf_control.getPulseShape().count(1) * 0.009
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # MAGIC THIS IS NOT EXACTLY CORRECT,
        # if self.values[self.data.pulse_length] < self.values[self.data.pulse_length_min]:
        #     self.values[self.data.pulse_length_status] = state.BAD
        # elif self.values[self.data.pulse_length] > self.values[self.data.pulse_length_max]:
        #     self.values[self.data.pulse_length_status] = state.BAD
        # else:
        #     self.values[self.data.pulse_length_status] = state.GOOD

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
        self.values[self.data.llrf_ff_amp_locked] =  self.llrf_obj[0].ff_amp_lock_state
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
        self.amp_vs_kfpow_running_stat[self.values[self.data.amp_sp]] = \
            self.llrf_control.getKlyFwdPwrRSState(self.values[self.data.amp_sp])


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