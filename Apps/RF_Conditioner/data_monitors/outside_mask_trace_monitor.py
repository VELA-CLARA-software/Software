import monitor
import data.rf_condition_data_base as dat
import os
import datetime
#from VELA_CLARA_enums import STATE
from data.state import state
import time


class outside_mask_trace_monitor(monitor.monitor):
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

    def __init__(self,
                 llrf_control,
                 data_dict,
                 llrf_param,
                 breakdown_param,
                 logger
                ):
        # init base-class
        monitor.monitor.__init__(self,timed_cooldown=True)
        # breakdown param
        self.breakdown_param = breakdown_param
        self.logger = logger

        # output file info
        for trace in llrf_param['TRACES_TO_SAVE']:
            if "CAVITY_REVERSE_POWER" in trace:
                self.CRP = trace
                print(self.my_name + ' has ' + self.CRP)
            if "CAVITY_FORWARD_POWER" in trace:
                self.CFP = trace
                print(self.my_name + ' has ' + self.CFP)
            if "PROBE_POWER" in trace:
                self.CPP = trace
                print(self.my_name + ' has ' + self.CPP)

        self.llrf = llrf_control
        self.llrfObj = [self.llrf.getLLRFObjConstRef()]
        self.data_dict = data_dict
        self.timer.timeout.connect(self.update_value)
        self.timer.start(breakdown_param['OUTSIDE_MASK_CHECK_TIME'])
        self.data_dict[dat.breakdown_status] = state.GOOD
        #self.data_dict[dat.breakdown_rate_aim] = llrf_param['BREAKDOWN_RATE_AIM']

    def reset_event_pulse_count(self):
        self.event_pulse_count_zero = self.data_dict[dat.pulse_count]
        self.data_dict[dat.event_pulse_count] = 0


    def cooldown_function(self):
        print self.my_name + ' monitor function called, cool down ended'
        self.incool_down = False
        self.data_dict[dat.breakdown_status] = state.GOOD

    def update_value(self):
        self.data_dict[dat.pulse_count] = self.llrfObj[0].activePulseCount
        self.data_dict[dat.event_pulse_count] = self.data_dict[dat.pulse_count] - self.event_pulse_count_zero
        #~print ('pulse count  ', self.llrf.getActivePulseCount())
        self.data_dict[dat.elapsed_time] = self.llrf.elapsedTime()
        self.data_dict[dat.num_outside_mask_traces] = self.llrfObj[0].num_outside_mask_traces
        _count = self.llrfObj[0].num_outside_mask_traces
        #print(self.my_name + ' checking, cont = ' +str(_count))
        if _count > self.previous_outside_mask_trace_count:
            print(self.my_name +' NEW OUTSIDE MASK TRACE DETECTED, entering cooldown')
            self.data_dict[dat.breakdown_status] = state.BAD
            self.cooldown_timer.start(self.breakdown_param['OUTSIDE_MASK_COOLDOWN_TIME'])
            self.get_new_outside_mask_traces(_count)
            self.previous_outside_mask_trace_count = _count


    def get_new_outside_mask_traces(self, _count):
        for i in range(self.previous_outside_mask_trace_count, _count):
            print(self.my_name + ' getting outside_mask_trace ' + str(i))
            new = self.llrf.getOutsideMaskDataPart(i)
            print(self.my_name + ' new outside_mask_trace = ' + new['trace_name'])

            if 'FORWARD' in new['trace_name']:
                self.forward_power_data.append(new)
                print(self.my_name + ' forward trace outside mask! count = ' + str(len(self.forward_power_data)))
                self.logger.dump_forward(new,len(self.forward_power_data) )

            elif 'REVERSE' in new['trace_name']:
                self.reverse_power_data.append(new)
                print(self.my_name + ' reverse trace outside mask! count = ' + str(len(self.reverse_power_data)))
                self.logger.dump_reverse(new, len(self.reverse_power_data))
                self.data_dict[dat.breakdown_count] += 1


            elif 'PROBE' in new['trace_name']:
                self.probe_power_data.append(new)
                print(self.my_name + ' probe trace outside mask! count = ' + str(len(self.probe_power_data)))
                self.logger.dump_probe(new, len(self.probe_power_data))
                self.data_dict[dat.breakdown_count] += 1


