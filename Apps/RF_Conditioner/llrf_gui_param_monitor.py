from monitor import monitor
import VELA_CLARA_LLRF_Control

# This class runs in a separate Qthread
# so after instantiation you must call start on it (!)
# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the protection)
# at a later date

class llrf_gui_param_monitor(monitor):
    my_name = 'llrf_gui_param_monitor'
    def __init__(self,
                 llrf_controller,
                 gui_dict,
                 enable_key,
                 lock_key,
                 pulse_length_key,
                 kly_fwd_pwr_key,
                 kly_rev_pwr_key,
                 cav_fwd_pwr_key,
                 cav_rev_pwr_key,
                 pulse_count_key,
                 probe_pwr,
                 monitored_traces
                 ):
        monitor.__init__(self)
        self.llrf = llrf_controller
        self.llrfObj = [self.llrf.getLLRFObjConstRef()]
        self.gui_dict = [gui_dict]

        self.gui_keys_traces = {}
        for trace in monitored_traces:
            if 'CAVITY_REVERSE_POWER' in trace:#MAGIC_STRING
                self.gui_keys_traces[trace] = cav_rev_pwr_key
            elif 'CAVITY_FORWARD_POWER' in trace:#MAGIC_STRING
                self.gui_keys_traces[trace] = cav_fwd_pwr_key
            elif 'KLYSTRON_FORWARD_POWER' in trace:#MAGIC_STRING
                self.gui_keys_traces[trace] = kly_fwd_pwr_key
            elif 'KLYSTRON_REVERSE_POWER' in trace:#MAGIC_STRING
                self.gui_keys_traces[trace] = kly_rev_pwr_key

        self.gui_dict[0][pulse_length_key] = self.llrfObj[0].pulse_length
        self.gui_dict[0][lock_key] = self.llrfObj[0].rf_output
        self.gui_dict[0][enable_key] = self.llrfObj[0].ff_lock_state

        self.timer.timeout.connect(self.update_value)
        self.timer.start(1000)

    def update_value(self):
        for trace, gui_key  in self.gui_keys_traces.iteritems():
          self.get_mean_power(gui_key, trace)

    def get_mean_power(self,gui_key,trace):
        self.gui_dict[0][gui_key] = self.llrfObj[0].trace_data[trace].traces[self.llrfObj[0].trace_data[trace].latest_trace_index].mean
