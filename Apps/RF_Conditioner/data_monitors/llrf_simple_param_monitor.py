from monitor import monitor
import data.rf_condition_data_base as dat


class llrf_simple_param_monitor(monitor):
    my_name = 'llrf_gui_param_monitor'
    def __init__(self):
        monitor.__init__(self)
        #
        # now match up trace names with the keys for power outputs from the 'values' dict
        self.trace_pwr_keys = {}
        for trace in monitor.config.llrf_config['TRACES_TO_SAVE']:
            print(self.my_name + ' adding ' + trace + ' to mean power list')
            if 'CAVITY_REVERSE_POWER' in trace:#MAGIC_STRING
                self.trace_pwr_keys[trace] = dat.rev_cav_pwr
            elif 'CAVITY_FORWARD_POWER' in trace:#MAGIC_STRING
                self.trace_pwr_keys[trace] = dat.fwd_cav_pwr
            elif 'KLYSTRON_FORWARD_POWER' in trace:#MAGIC_STRING
                self.trace_pwr_keys[trace] = dat.fwd_kly_pwr
            elif 'KLYSTRON_REVERSE_POWER' in trace:#MAGIC_STRING
                self.trace_pwr_keys[trace] = dat.rev_kly_pwr
            elif 'PROBE_POWER' in trace:#MAGIC_STRING
                self.trace_pwr_keys[trace] = dat.probe_pwr

        self.timer.timeout.connect(self.update_value)
        #self.timer.start( monitor.config.llrf_config['LLRF_CHECK_TIME'])
        self.timer.start( 1000 )
        self.set_success = True


        ## WARNING
        monitor.llrf_control.setActivePulsePowerLimit(2.0)



    def update_value(self):
        for trace, key  in self.trace_pwr_keys.iteritems():
            self.get_mean_power(key, trace)
        monitor.data.values[dat.pulse_length] = monitor.llrfObj[0].pulse_length
        #self.values[dat.pulse_length] = self.llrfObj[0].pulse_length
        monitor.data.values[dat.llrf_ff_amp_locked] =  monitor.llrfObj[0].ff_amp_lock_state
        monitor.data.values[dat.llrf_ff_ph_locked] = monitor.llrfObj[0].ff_ph_lock_state
        monitor.data.values[dat.llrf_output] = monitor.llrfObj[0].rf_output
        monitor.data.values[dat.amp_sp] = monitor.llrfObj[0].amp_sp
        #self.values[dat.amp_ff] = self.llrfObj[0].amp_ff


    def get_mean_power(self,key,trace):
        llrf_simple_param_monitor.data.values[key] = \
            monitor.llrfObj[0].trace_data[trace].traces[monitor.llrfObj[0].trace_data[trace].latest_trace_index].mean
