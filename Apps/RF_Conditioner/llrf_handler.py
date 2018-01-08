# llrf_handler.py

from VELA_CLARA_enums import MACHINE_AREA
import VELA_CLARA_LLRF_Control
from VELA_CLARA_LLRF_Control import LLRF_TYPE



class llrf_handler():
    def __init__(self,llrf_controller,trace_to_save
    # ,
                 # gen_mon,
                 # settings_dict,
                 # id_key,
                 # gui_dict,
                 # gui_dict_key,
                 # update_time
                 ):
        self.llrf = llrf_controller
        self.llrfObj = [self.llrf.getLLRFObjConstRef()]
        self.llrf_type = self.llrfObj[0].type
        self.trace_to_save = []

        self.timevector = self.llrfObj[0].time_vector.value


        # assume true, but next loops will set to false if it fails
        self.trace_monitoring = True
        if "error" not in trace_to_save:
            for trace in trace_to_save:
                print 'trace = ' + trace
                a = self.llrf.startTraceMonitoring(trace)
                if a:
                    print 'monitoring ' + trace
                else:
                    print 'ERROR MONITORING ' + trace
                    self.trace_monitoring = False

                if 'CAVITY_REVERSE_POWER' in trace:
                    self.CRPow = trace
                    print 'self.CRPow ' + self.CRPow
                elif 'CAVITY_FORWARD_POWER' in trace:
                    self.CFPow = trace
                    print 'self.CFPow ' + self.CFPow
                elif 'KLYSTRON_FORWARD_POWER' in trace:
                    self.KFPow = trace
                    print 'self.KFPow ' + self.KFPow
                elif 'KLYSTRON_REVERSE_POWER' in trace:
                    self.KRPow = trace
                    print 'self.KRPow ' + self.KRPow

        self.kly_fwd_pwr_data = []

        self.set_mean_position()


        def start_trace_monitoring(self):
            print 'set_trace_monitoring'
        # start th etrace momnitoring
        # the average taking
        #

    def set_masks(self):
        print 'set_masks'
        # use the aut function in the LLRF controller

    def start_trace_mean_monitoring(self):
        print 'set_trace_mean_monitoring'
        # this is based on the pulse length and parameters from the config
        # llrf controller needs start adn stop index and flag setting
        # we need to confirm what 100ns from pulse end means
        # i think we should do an avergae between some points

    def set_pulse_length(self,value):
        self.llrf.setPulseLength(value)
        # is the pulse length changes update the trace mean values n
        self.set_mean_position()

    def set_mean_position(self):
        print('llrfObj[0].pulse_latency = ',self.llrfObj[0].pulse_latency)
        pulse_end  = self.timevector[self.llrfObj[0].pulse_latency] + self.llrf.getPulseLength()
        pulse_end_index = len([x for x in self.timevector if x <= pulse_end ])
        trace_mean_start = pulse_end_index - 50
        trace_mean_end   = pulse_end_index - 20
        print('rf pulse end time = ',pulse_end)
        print('rf pulse end index = ', pulse_end_index)
        print('trace_mean_start = ', trace_mean_start)
        print('trace_mean_end = ', trace_mean_end)
        self.llrf.setMeanStartIndex(self.CRPow, trace_mean_start)
        self.llrf.setMeanStopIndex(self.CRPow, trace_mean_end)
        self.llrf.setMeanStartIndex(self.KFPow, trace_mean_start)
        self.llrf.setMeanStopIndex(self.KFPow, trace_mean_end)