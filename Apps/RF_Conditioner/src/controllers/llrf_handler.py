# llrf_handler.py
from llrf_handler_base import llrf_handler_base
from VELA_CLARA_LLRF_Control import TRIG
import time
from timeit import default_timer as timer
from VELA_CLARA_LLRF_Control import LLRF_SCAN


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

    def stop_keep_average_trace(self):
        print('def stop_keep_average_trace')

    def get_lo_masks_max(self):
        for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:
            t = llrf_handler_base.llrf_control.getLoMask(trace)
            ##sort([v for v in t if v < max(t)][-1]
            x = [v for v in t if min(t) < v < max(t)]
            x.sort()
            try:
                llrf_handler_base.logger.message(trace + ' lo max =  ' + str(x[-1]))
                llrf_handler_base.logger.message(trace + ' lo max =  ' + str(x[0]))
            except:
                llrf_handler_base.logger.message(trace + ' lo max except =  ' + str(max(t)))

    def get_hi_masks_max(self):
        for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:
            # x.append(trace)
            t = llrf_handler_base.llrf_control.getHiMask(trace)
            ##sort([v for v in t if v < max(t)][-1]
            x = [v for v in t if min(t) < v < max(t)]
            x.sort()
            try:
                llrf_handler_base.logger.message(trace + ' hi max =  ' + str(x[-1]))
                llrf_handler_base.logger.message(trace + ' hi min =  ' + str(x[0]))
            except:
                llrf_handler_base.logger.message(trace + ' hi max except =  ' + str(max(t)))

    def clear_all_rolling_average(self):
        llrf_handler_base.llrf_control.clearAllRollingAverage()

    def set_amp(self, val):
        #llrf_handler_base.llrf_control.trigOff()
        # for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:#MAGIC_STRING:
        #     llrf_handler_base.llrf_control.setTraceSCAN(trace, LLRF_SCAN.PASSIVE)  # SHOULD BE INPUT Parameter
        llrf_handler_base.llrf_control.setAmpSP(val)
        self.mask_set = False
        start = timer()
        end = start
        success = True
        while llrf_handler_base.llrfObj[0].amp_sp != val:
            end = timer()
            if start - end > 3.0:#MAGIC_NUMBER
                success = False
                break
        if success:
            llrf_handler_base.logger.message('set_amp = ' + str(val) + ', took ' + str(end - start)+\
                                         ' time,  averages NOT reset, mask_set = False', True)
        else:
            llrf_handler_base.logger.message('set_amp = ' + str(val) + ', FAILED to set amp in less than 3 seconds '
                                                                       'averages NOT reset, mask_set = False', True)

        #llrf_handler_base.llrf_control.trigExt()
        # start = timer()
        # end = start
        # while llrf_handler_base.llrfObj[0].trig_source != TRIG.EXTERNAL:
        #     end = timer()
        #     if start - end > 3.0:#MAGIC_NUMBER
        #         success = False
        #         break
        # traces get added to the average when they pass the mask
        #self.start_trace_average_no_reset(True)
        # for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:#MAGIC_STRING:
        #     llrf_handler_base.llrf_control.setTraceSCAN(trace, LLRF_SCAN.ZERO_POINT_ONE) # SHOULD BE INPUIT Parameter



    def set_amp_hp(self, val):
        llrf_handler_base.llrf_control.setAmpHP(val)



    # NOT NEEDED ANYMORE ????
    # !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP!
    def set_mask(self):
        if self.mask_set:
            pass
        else:
            #
            r = True
            #if llrf_handler_base.llrfObj[0].amp_sp > 100: #'MAGIC'
            if self.have_averages():
            # cancerous name, change !!!!!
               if llrf_handler_base.llrfObj[0].kly_fwd_power_max > llrf_handler_base.config.llrf_config['KLY_PWR_FOR_ACTIVE_PULSE']:
                    self.set_trace_masks()
                    for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:
                            if llrf_handler_base.llrfObj[0].trace_data[trace].check_mask:
                                pass
                            else:
                                llrf_handler_base.logger.message(self.my_name + ' check_mask = False ' + trace, True)
                                r = False
               else:
                   llrf_handler_base.logger.message(self.my_name + ' cant set mask - kly fwd power low', True)
            else:
                if self.mask_not_set_message:
                    llrf_handler_base.logger.message(self.my_name + ' cant set mask, NO AVERAGE Traces', True)
                self.mask_not_set_message = False
                r = False
                # pass
            if r:
                llrf_handler_base.logger.message(self.my_name + ' has set mask ', True)
                self.mask_not_set_message = True
            self.mask_set = r

    # NOT NEEDED ANYMORE ????
    def force_new_mask(self):
        if self.have_averages():
            # cancerous name, chnage !!!!!
            self.set_trace_masks()
            # for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:
            #     if llrf_handler_base.llrfObj[0].trace_data[trace].check_mask:
            #         pass
            #     else:
            #         llrf_handler_base.logger.message(self.my_name + ' check_mask = False ' + trace, True)
            #         r = False
