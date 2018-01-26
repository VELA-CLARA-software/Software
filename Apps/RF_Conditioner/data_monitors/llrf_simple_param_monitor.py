from monitor import monitor
import data.rf_condition_data_base as dat
from VELA_CLARA_LLRF_Control import TRIG

class llrf_simple_param_monitor(monitor):
    my_name = 'llrf_gui_param_monitor'
    def __init__(self):
        monitor.__init__(self)
        #
        # now match up trace names with the keys for power outputs from the 'values' dict
        self.trace_pwr_keys = {}
        for trace in monitor.config.llrf_config['TRACES_TO_SAVE']:
            print(self.my_name + ' adding ' + trace + ' to mean power list')
            if self.is_cav_reverse_power(trace):
                self.trace_pwr_keys[trace] = dat.rev_cav_pwr
            elif self.is_cav_forward_power(trace):
                self.trace_pwr_keys[trace] = dat.fwd_cav_pwr
            elif self.is_kly_forward_power(trace):
                self.trace_pwr_keys[trace] = dat.fwd_kly_pwr
            elif self.is_kly_reverse_power(trace):
                self.trace_pwr_keys[trace] = dat.rev_kly_pwr
            elif self.is_probe(trace):
                self.trace_pwr_keys[trace] = dat.probe_pwr

        self.timer.timeout.connect(self.update_value)
        self.timer.start( monitor.config.llrf_config['LLRF_CHECK_TIME'])
        #self.timer.start( 1000 )
        self.set_success = True


        ## WARNING
        # min kyl fwd power to enable incrementing the pulse RF counter
        monitor.llrf_control.setActivePulsePowerLimit( monitor.config.llrf_config['KLY_PWR_FOR_ACTIVE_PULSE'] )
        #; number extra traces to save after an out_side_mask_trace is detected
        monitor.llrf_control.setNumExtraTraces( monitor.config.llrf_config['EXTRA_TRACES_ON_BREAKDOWN'])

    def update_value(self):
        for trace, key  in self.trace_pwr_keys.iteritems():
            self.get_mean_power(key, trace)
        monitor.data.values[dat.pulse_length] = monitor.llrfObj[0].pulse_length
        #self.values[dat.pulse_length] = self.llrfObj[0].pulse_length
        monitor.data.values[dat.llrf_ff_amp_locked] =  monitor.llrfObj[0].ff_amp_lock_state
        monitor.data.values[dat.llrf_ff_ph_locked] = monitor.llrfObj[0].ff_ph_lock_state
        monitor.data.values[dat.llrf_output] = monitor.llrfObj[0].rf_output
        monitor.data.values[dat.amp_sp] = int(monitor.llrfObj[0].amp_sp)

        if monitor.llrfObj[0].trig_source == TRIG.OFF:
            monitor.data.values[dat.llrf_trigger] = False
        elif monitor.llrfObj[0].trig_source == TRIG.UNKNOWN_TRIG:
            monitor.data.values[dat.llrf_trigger] = False
        else:
            monitor.data.values[dat.llrf_trigger] = True


    def get_mean_power(self,key,trace):
        llrf_simple_param_monitor.data.values[key] = \
            monitor.llrfObj[0].trace_data[trace].traces[monitor.llrfObj[0].trace_data[trace].latest_trace_index].mean
