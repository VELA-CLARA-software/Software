from monitor import monitor
import data.rf_condition_data_base as dat


class llrf_simple_param_monitor(monitor):
    my_name = 'llrf_gui_param_monitor'
    def __init__(self,
                 llrf_controller,
                 data_dict,
                 monitored_traces,
                 update_time = 50
                 ):
        monitor.__init__(self)
        self.llrf = llrf_controller
        self.llrfObj = [self.llrf.getLLRFObjConstRef()]
        self.data_dict = data_dict
        #
        # now match up trace names with the keys for power outputs from the 'values' dict
        self.trace_pwr_keys = {}
        for trace in monitored_traces:
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
        self.timer.start(update_time)
        self.set_success = True

    def update_value(self):
        for trace, key  in self.trace_pwr_keys.iteritems():
            self.get_mean_power(key, trace)
        self.data_dict[dat.pulse_length] = self.llrfObj[0].pulse_length
        self.data_dict[dat.llrf_ff_amp_locked] = self.llrfObj[0].ff_amp_lock_state
        self.data_dict[dat.llrf_ff_ph_locked] = self.llrfObj[0].ff_ph_lock_state
        self.data_dict[dat.llrf_output] = self.llrfObj[0].rf_output
        self.data_dict[dat.amp_sp] = self.llrfObj[0].amp_sp
        #self.data_dict[dat.amp_ff] = self.llrfObj[0].amp_ff


    def get_mean_power(self,key,trace):
        self.data_dict[key] = \
            self.llrfObj[0].trace_data[trace].traces[self.llrfObj[0].trace_data[trace].latest_trace_index].mean
