# llrf_handler.py
from llrf_handler_base import llrf_handler_base
from VELA_CLARA_LLRF_Control import TRIG
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
        self.mask_set = False



    #
    # def check_masks_OLD(self):
    #     for trace in self.outside_mask_traces:
    #         a = llrf_handler_base.llrf_control.setShouldCheckMask(trace)
    #         if a:
    #             print('mask checking  for ' + trace)
    #         else:
    #             print('mask NOT checking for ' + trace)
    #     llrf_handler_base.llrf_control.setGlobalCheckMask(True)

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


    def set_amp(self, val):
        llrf_handler_base.llrf_control.setAmpSP(val)
        self.mask_set = False
        print('set_amp = ' + str(val) + ' averages reset, mask_set = False')
        llrf_handler_base.llrf_control.resetAverageTraces()

    def set_amp_hp(self, val):
        llrf_handler_base.llrf_control.setAmpHP(val)
        ## ???


    # !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP! !NEATEN UP!
    def set_mask(self):
        if self.mask_set:
            pass
        else:
            #
            r = True
            if self.have_averages():
                # cancerous name, chnage !!!!!
                self.set_trace_masks()
                #self.reverse_mask_dict['update_func'](self.reverse_mask_dict)
                #self.forward_mask_dict['update_func'](self.forward_mask_dict)
                #self.probe_mask_dict['update_func'](self.probe_mask_dict)

                # paranoia

                for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:
                #     #print(trace)
                #     if 'REVERSE' in trace:
                #         a = llrf_handler_base.llrf_control.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
                #                                              self.mask_4[trace],
                #                                              llrf_handler_base.config.breakdown_config['CRP_MASK_LEVEL'], trace)
                #     elif 'FORWARD' in trace:
                #         a = llrf_handler_base.llrf_control.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
                #                                              self.mask_4[trace],
                #                                              llrf_handler_base.config.breakdown_config['CFP_MASK_LEVEL'], trace)
                #     elif 'PROBE' in trace:
                #         a = llrf_handler_base.llrf_control.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
                #                                              self.mask_4[trace],
                #                                              llrf_handler_base.config.breakdown_config['CPP_MASK_LEVEL'], trace)
                #    if a == False:
                #        llrf_handler_base.logger.message(self.my_name + ' ERROR SETTING MASK for ' + trace, True)
                #        r = False
                #   else:
                        if llrf_handler_base.llrfObj[0].trace_data[trace].check_mask:
                            pass
                        else:
                            llrf_handler_base.logger.message(self.my_name + ' check_mask = False ' + trace, True)
                            r = False
            else:
                #llrf_handler_base.logger.message(self.my_name + ' cant set mask, NO AVERAGE Traces')
                r = False
                pass
            if r:
                llrf_handler_base.logger.message(self.my_name + ' has set mask ')

            self.mask_set = r
