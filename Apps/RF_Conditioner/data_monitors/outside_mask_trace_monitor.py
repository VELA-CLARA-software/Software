from  monitor import monitor
import data.rf_condition_data_base as dat
import os
import datetime
#from VELA_CLARA_enums import STATE
from data.state import state
import time


class outside_mask_trace_monitor(monitor):
    #whoami
    my_name = 'outside_mask_trace_monitor'
    outside_mask_trace_count = 0
    previous_outside_mask_trace_count = 0
    forward_power_data = []
    reverse_power_data = []
    probe_power_data = []
    CFP = None
    CRP = None
    CPP = None

    # this is the 'zero' value (i.e. subtracted from pulse count to give event_pulse_count
    event_pulse_count_zero = 0

    def __init__(self):
        # init base-class
        monitor.__init__(self,timed_cooldown=True)
        # breakdown param
        self.breakdown_config = outside_mask_trace_monitor.config.breakdown_config
        self.logger = monitor.logger

        # output file info
        for trace in monitor.config.llrf_config['TRACES_TO_SAVE']:
            if "CAVITY_REVERSE_POWER" in trace:
                self.CRP = trace
                print(self.my_name + ' has ' + self.CRP)
            if "CAVITY_FORWARD_POWER" in trace:
                self.CFP = trace
                print(self.my_name + ' has ' + self.CFP)
            if "PROBE_POWER" in trace:
                self.CPP = trace
                print(self.my_name + ' has ' + self.CPP)

        #monitor.llrf_control = monitor.llrf_control
        #monitor.llrfObj[0] = monitor.llrfObj#[monitor.llrf_control.getLLRFObjConstRef()]
        #monitor.data.values = monitor.data.values

        self.timer.timeout.connect(self.update_value)
        self.timer.start(self.breakdown_config['OUTSIDE_MASK_CHECK_TIME'])
        monitor.data.values[dat.breakdown_status] = state.GOOD
        #monitor.data.values[dat.breakdown_rate_aim] = llrf_param['BREAKDOWN_RATE_AIM']

    def reset_event_pulse_count(self):
        self.event_pulse_count_zero = monitor.data.values[dat.pulse_count]
        monitor.data.values[dat.event_pulse_count] = 0
        print('*')
        print('**** reset_event_pulse_count ***')
        print('event_pulse_count_zero = ' +str(self.event_pulse_count_zero ))


    def cooldown_function(self):
        print self.my_name + ' monitor function called, cool down ended'
        self.incool_down = False
        monitor.data.values[dat.breakdown_status] = state.GOOD

    def update_value(self):
        monitor.data.values[dat.pulse_count] = monitor.llrfObj[0].activePulseCount
        monitor.data.values[dat.event_pulse_count] = monitor.data.values[dat.pulse_count] - self.event_pulse_count_zero
        #~print ('pulse count  ', monitor.llrf_control.getActivePulseCount())
        monitor.data.values[dat.elapsed_time] = monitor.llrf_control.elapsedTime()
        monitor.data.values[dat.num_outside_mask_traces] = monitor.llrfObj[0].num_outside_mask_traces
        _count = monitor.llrfObj[0].num_outside_mask_traces
        #print(self.my_name + ' checking, cont = ' +str(_count))
        if _count > self.previous_outside_mask_trace_count:
            print(self.my_name +' NEW OUTSIDE MASK TRACE DETECTED, entering cooldown')
            monitor.data.values[dat.breakdown_status] = state.BAD
            self.cooldown_timer.start(self.breakdown_config['OUTSIDE_MASK_COOLDOWN_TIME'])
            self.get_new_outside_mask_traces(_count)
            self.previous_outside_mask_trace_count = _count
        monitor.data.update_last_million_pulse_log()


    def get_new_outside_mask_traces(self, _count):
        for i in range(self.previous_outside_mask_trace_count, _count):
            print(self.my_name + ' getting outside_mask_trace ' + str(i))
            new = monitor.llrf_control.getOutsideMaskDataPart(i)
            print(self.my_name + ' new outside_mask_trace = ' + new['trace_name'])

            if 'FORWARD' in new['trace_name']:
                self.forward_power_data.append(new)
                print(self.my_name + ' forward trace outside mask! count = ' + str(len(self.forward_power_data)))
                self.logger.dump_forward(new,len(self.forward_power_data) )

            elif 'REVERSE' in new['trace_name']:
                self.reverse_power_data.append(new)
                print(self.my_name + ' reverse trace outside mask! count = ' + str(len(self.reverse_power_data)))
                self.logger.dump_reverse(new, len(self.reverse_power_data))
                monitor.data.values[dat.breakdown_count] += 1


            elif 'PROBE' in new['trace_name']:
                self.probe_power_data.append(new)
                print(self.my_name + ' probe trace outside mask! count = ' + str(len(self.probe_power_data)))
                self.logger.dump_probe(new, len(self.probe_power_data))
                monitor.data.values[dat.breakdown_count] += 1


