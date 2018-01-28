# llrf_handler.py
from llrf_handler_base import llrf_handler_base
from VELA_CLARA_LLRF_Control import TRIG
import time
from timeit import default_timer as timer



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
        self.mask_set = False
        self.mask_not_set_message = True

    def enable_trigger(self):
        if llrf_handler_base.llrfObj[0].trig_source == TRIG.OFF:
            llrf_handler_base.llrf_control.trigExt()

    def set_pulse_length(self,value):
        llrf_handler_base.llrf_control.setPulseLength(value)
        # is the pulse length changes update the trace mean values n
        time.sleep(0.2)
        self.set_mean_pwr_position()
        # and mask positions!
        self.setup_outside_mask_trace_param()

    def stop_keep_average_trace(self):
        print('def stop_keep_average_trace')

    def get_lo_masks_max(self):
        for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:
            t = llrf_handler_base.llrf_control.getLoMask(trace)
            ##sort([v for v in t if v < max(t)][-1]
            x = [v for v in t if v < max(t)]
            x.sort()
            try:
                llrf_handler_base.logger.message(trace + ' lo max =  ' + str(x[-1]))
            except:
                llrf_handler_base.logger.message(trace + ' lo max except =  ' + str(max(t)))

    def get_hi_masks_max(self):
        for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:
            # x.append(trace)
            t = llrf_handler_base.llrf_control.getHiMask(trace)
            ##sort([v for v in t if v < max(t)][-1]
            x = [v for v in t if v < max(t)]
            x.sort()
            try:
                llrf_handler_base.logger.message(trace + ' hi max =  ' + str(x[-1]))
            except:
                llrf_handler_base.logger.message(trace + ' hi max except =  ' + str(max(t)))

    def set_amp(self, val):
        llrf_handler_base.llrf_control.setAmpSP(val)
        self.mask_set = False
        start = timer()
        end = start
        while llrf_handler_base.llrfObj[0].amp_sp != val:
            end = timer()
        llrf_handler_base.logger.message('set_amp = ' + str(val) + ', took ' + str(end - start)+\
                                         'time,  averages NOT reset, mask_set = False', True)
        # traces get added to the average when they pass the mask
        #self.start_trace_average_no_reset(True)

    def set_amp_hp(self, val):
        llrf_handler_base.llrf_control.setAmpHP(val)

    # !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP!
    def set_mask(self):
        if self.mask_set:
            pass
        else:
            #
            r = True

            #if llrf_handler_base.llrfObj[0].amp_sp > 100: #'MAGIC'
            if self.have_averages():
            # cancerous name, chnage !!!!!
                self.set_trace_masks()
                for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:
                        if llrf_handler_base.llrfObj[0].trace_data[trace].check_mask:
                            pass
                        else:
                            llrf_handler_base.logger.message(self.my_name + ' check_mask = False ' + trace, True)
                            r = False
            else:
                if self.mask_not_set_message:
                    llrf_handler_base.logger.message(self.my_name + ' cant set mask, NO AVERAGE Traces')
                self.mask_not_set_message = False
                r = False
                # pass
            if r:
                llrf_handler_base.logger.message(self.my_name + ' has set mask ')
                self.mask_not_set_message = True
            self.mask_set = r
