# llrf_handler.py
from llrf_handler_base import llrf_handler_base
from VELA_CLARA_enums import MACHINE_AREA
import VELA_CLARA_LLRF_Control
from VELA_CLARA_LLRF_Control import LLRF_TYPE



class llrf_handler(llrf_handler_base):
    #whoami
    my_name= 'llrf_handler'
    def __init__(self,
                 llrf_controller,
                 breakdown_param,
                 llrf_param
                 ):
        llrf_handler_base.__init__(self,
                                   llrf_controller=llrf_controller,
                                   breakdown_param=breakdown_param,
                                   llrf_param=llrf_param)

        # assume true, but next loops will set to false if it fails
        # start the timer (at the ms level
        self.llrf.startTimer()
        self.kly_fwd_pwr_data = []



    def check_masks_OLD(self):
        for trace in self.outside_mask_traces:
            a = self.llrf.setShouldCheckMask(trace)
            if a:
                print('mask checking  for ' + trace)
            else:
                print('mask NOT checking for ' + trace)
        self.llrf.setGlobalCheckMask(True)


    def set_pulse_length(self,value):
        self.llrf.setPulseLength(value)
        # is the pulse length changes update the trace mean values n
        self.set_mean_pwr_position()



    def stop_keep_average_trace(self):
        print('def stop_keep_average_trace')


    def set_amp(self, val):
        self.llrf.setAmpSP(val)
        ## ???
        self.llrf.resetAverageTraces()


