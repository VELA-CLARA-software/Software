# llrf_handler.py
from llrf_handler_base import llrf_handler_base
from VELA_CLARA_enums import MACHINE_AREA
import VELA_CLARA_LLRF_Control
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import time



class llrf_handler(llrf_handler_base):
    #whoami
    my_name= 'llrf_handler'
    def __init__(self):
        #super(llrf_handler_base,self).__init__()
        llrf_handler_base.__init__(self)
        # assume true, but next loops will set to false if it fails
        # start the timer (at the ms level
        llrf_handler_base.llrf_control.startTimer()
        self.kly_fwd_pwr_data = []



    def check_masks_OLD(self):
        for trace in self.outside_mask_traces:
            a = llrf_handler_base.llrf_control.setShouldCheckMask(trace)
            if a:
                print('mask checking  for ' + trace)
            else:
                print('mask NOT checking for ' + trace)
        llrf_handler_base.llrf_control.setGlobalCheckMask(True)


    def set_pulse_length(self,value):
        llrf_handler_base.llrf_control.setPulseLength(value)
        # is the pulse length changes update the trace mean values n
        time.sleep(0.2)
        self.set_mean_pwr_position()
        # and mask positions!
        self.set_outside_mask_trace_param()



    def stop_keep_average_trace(self):
        print('def stop_keep_average_trace')


    def set_amp(self, val):
        print('set_amp = ' + str(val))
        llrf_handler_base.llrf_control.setAmpSP(val)
        ## ???
        llrf_handler_base.llrf_control.resetAverageTraces()


    def set_amp_hp(self, val):
        llrf_handler_base.llrf_control.setAmpHP(val)
        ## ???

