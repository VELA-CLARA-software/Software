from monitor import monitor
import src.data.rf_condition_data_base as dat
from src.data.state import state
from VELA_CLARA_LLRF_Control import TRIG

class llrf_simple_param_monitor(monitor):
    my_name = 'llrf_simple_param_monitor'
    old_rf_output = None
    def __init__(self):
        monitor.__init__(self)
        #
        # now match up trace names with the keys for power outputs from the 'values' dict
        self.trace_mean_keys = {}
        #
        # only update new values
        self.old_mean_values = {}
        # manually set up dicts to monitor trace 'means'
        for trace in monitor.config.llrf_config['MEAN_TRACES']:
            trace2 = monitor.llrf_control.fullLLRFTraceName(trace)

            if self.is_cav_reverse_power(trace):
                self.trace_mean_keys[trace2] = dat.rev_cav_pwr

            elif self.is_cav_forward_power(trace):
                self.trace_mean_keys[trace2] = dat.fwd_cav_pwr

            elif self.is_kly_forward_power(trace):
                self.trace_mean_keys[trace2] = dat.fwd_kly_pwr

            elif self.is_kly_forward_phase(trace):
                self.trace_mean_keys[trace2] = dat.fwd_kly_pha

            elif self.is_kly_reverse_power(trace):
                self.trace_mean_keys[trace2] = dat.rev_kly_pwr

            elif self.is_probe_power(trace):
                self.trace_mean_keys[trace2] = dat.probe_pwr

            elif self.is_cav_reverse_phase(trace):
                self.trace_mean_keys[trace2] = dat.rev_cav_pha

            elif self.is_cav_forward_phase(trace):
                self.trace_mean_keys[trace2] = dat.fwd_cav_pha


            elif self.is_kly_reverse_phase(trace):
                self.trace_mean_keys[trace2] = dat.rev_kly_pha

            elif self.is_probe_phase(trace):
                self.trace_mean_keys[trace2] = dat.probe_pha

            self.old_mean_values[monitor.llrf_control.fullLLRFTraceName(trace)]  = 0

            monitor.logger.message(self.my_name + ' adding ' + trace2 + ' to mean trace list  '
                                   'trace_mean_keys[trace2] = ' + self.trace_mean_keys[trace2]
                                   ,True)


        self.timer.timeout.connect(self.update_value)
        self.timer.start( monitor.config.llrf_config['LLRF_CHECK_TIME'])
        #self.timer.start( 1000 )
        self.set_success = True

        # new feature, the setting phase end index by remote...
        if monitor.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_PHASE_TRACE_1'):
            self.phase_trace_1 = monitor.config.breakdown_config['PHASE_MASK_BY_POWER_PHASE_TRACE_1']
        if monitor.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_PHASE_TRACE_2'):
            self.phase_trace_2 = monitor.config.breakdown_config['PHASE_MASK_BY_POWER_PHASE_TRACE_2']


        ## WARNING
        # min kyl fwd power to enable incrementing the pulse RF counter
        monitor.llrf_control.setActivePulsePowerLimit(monitor.config.llrf_config['KLY_PWR_FOR_ACTIVE_PULSE'])
        #; number extra traces to save after an out_side_mask_trace is detected
        monitor.llrf_control.setNumExtraTracesOnOutsideMaskEvent(monitor.config.llrf_config['EXTRA_TRACES_ON_BREAKDOWN'])

    def update_value(self):
        # get the mean power for each trace
        for trace, key  in self.trace_mean_keys.iteritems():
            self.get_mean_power(key, trace)
        #self.values[dat.pulse_length] = self.llrfObj[0].pulse_length
        # lock state
        monitor.data.values[dat.llrf_ff_amp_locked] =  monitor.llrfObj[0].ff_amp_lock_state
        monitor.data.values[dat.llrf_ff_ph_locked] = monitor.llrfObj[0].ff_ph_lock_state


        monitor.data.values[dat.duplicate_pulse_count] = monitor.llrfObj[0].duplicate_pulse_count

        # is rf_ouput enabled
        monitor.data.values[dat.llrf_output] = monitor.llrfObj[0].rf_output
        if monitor.llrfObj[0].rf_output != llrf_simple_param_monitor.old_rf_output:
            if monitor.llrfObj[0].rf_output:
                #monitor.data.values[dat.breakdown_status] = state.GOOD
                self.alarm('rf_on')
            else:
                #monitor.data.values[dat.breakdown_status] = state.BAD
                self.alarm('rf_off')
            llrf_simple_param_monitor.old_rf_output = monitor.llrfObj[0].rf_output

        # amplitude set point
        monitor.data.values[dat.amp_sp] = int(monitor.llrfObj[0].amp_sp)
        monitor.data.values[dat.phi_sp] = int(monitor.llrfObj[0].phi_sp)

        # LLRF trigger state
        if monitor.llrfObj[0].trig_source == TRIG.OFF:
            monitor.data.values[dat.llrf_trigger] = False
        elif monitor.llrfObj[0].trig_source == TRIG.UNKNOWN_TRIG:
            monitor.data.values[dat.llrf_trigger] = False
        else:
            monitor.data.values[dat.llrf_trigger] = True

        # if setting phase trace end masks by value get those values...
        if monitor.data.values[dat.phase_mask_by_power_trace_1_set]:
            monitor.data.values[dat.phase_end_mask_by_power_trace_1_time] = \
                monitor.llrf_control.getMaskInfiniteEndByPowerTime(self.phase_trace_1 )
        if monitor.data.values[dat.phase_mask_by_power_trace_2_set]:
            monitor.data.values[dat.phase_end_mask_by_power_trace_2_time] = \
                monitor.llrf_control.getMaskInfiniteEndByPowerTime( self.phase_trace_1 )

        # the latest running stats for this amp_set (from the c++)

        if(monitor.llrf_control.isKeepingKlyFwdPwrRS()):
            monitor.data.amp_vs_kfpow_running_stat[ monitor.data.values[dat.amp_sp] ] = \
                monitor.llrf_control.getKlyFwdPwrRSState( monitor.data.values[dat.amp_sp] )

        #
        # pulse length
        # THIS OLD WAY IS NOW BORKE,
        # monitor.data.values[dat.pulse_length] = monitor.llrfObj[0].pulse_length
        # Instead we now use the  getPulseShape vector and count the number of 1.0s

        # pulse length

        monitor.data.values[dat.pulse_length] = monitor.llrf_control.getPulseShape().count(1) * 0.009 # MAGUC THIS IS NOT EXACTLY CORRECT,




    def get_mean_power(self,key,trace):
        v = monitor.llrfObj[0].trace_data[trace].mean
        #print "key = " + str(key) + ", " + trace + " mean value = " +  str(v)
        if  self.old_mean_values[trace] == v:
            pass
        else:
            llrf_simple_param_monitor.data.values[key] = \
            monitor.llrfObj[0].trace_data[trace].mean
            self.old_mean_values[trace] = llrf_simple_param_monitor.data.values[key]

            # i probably dont need to do this anymore as we're now doing it in the c++
            # if self.is_kly_forward_power(trace):
            #     if self.old_mean_values[trace] > monitor.config.llrf_config['KLY_PWR_FOR_ACTIVE_PULSE']:
            #         self.update_amp_pwr_mean_dict(monitor.data.values[dat.amp_sp],self.old_mean_values[trace])





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