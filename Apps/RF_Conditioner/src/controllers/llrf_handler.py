# llrf_handler.py
from llrf_handler_base import llrf_handler_base
from VELA_CLARA_LLRF_Control import TRIG
from time import sleep
from timeit import default_timer as timer
import src.data.rf_condition_data_base as dat
from src.data.state import state

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

        self.set_iointr_counter = 0


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
        if val != llrf_handler_base.llrfObj[0].amp_sp:
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

    def enable_llrf(self):
        # go through each possible LLRF paramter (except HOLD_RF_ON_COM mod / protection parmaters
        # and try and reset them
        #llrf_handler_base.logger.message('enable_llrf trying to enable LLRF parmeters ', True)
        #
        #print('enable RF is setting amp_sp = 0')

        #
        #print("llrf_handler_base.llrf_control.isInterlockActive() = ", llrf_handler_base.llrf_control.isInterlockActive())
        if llrf_handler_base.llrf_control.isInterlockActive():
            #print('Interlock active')
            llrf_handler_base.llrf_control.setInterlockNonActive()
            sleep(0.02)
        else:
            pass
            #print('interlock not active')
        #
        #print("llrf_handler_base.llrf_control.isTrigExternal() = ", llrf_handler_base.llrf_control.isTrigExternal())
        if llrf_handler_base.llrf_control.isTrigExternal():
            pass
            #print('TRIG IS IN EXTERNAL')
        else:
            #print('trigExt')
            llrf_handler_base.llrf_control.trigExt()
            sleep(0.02)
        #

        #print("llrf_handler_base.llrf_control.isRFOutput() = ", llrf_handler_base.llrf_control.isRFOutput())

        if llrf_handler_base.llrf_control.isRFOutput():
            #print('RF OUTPUT IS GOOD')
            pass
        else:
            #print('enableRFOutput')
            llrf_handler_base.llrf_control.enableRFOutput()
            sleep(0.02)


        #print("llrf_handler_base.llrf_control.isAmpFFLocked() = ", llrf_handler_base.llrf_control.isAmpFFLocked())
        if llrf_handler_base.llrf_control.isAmpFFLocked():
            #print('AMP FF LOCKED')
            pass
        else:
            #print('lockPhaseFF')
            llrf_handler_base.llrf_control.lockAmpFF()
            sleep(0.02)

        #print("llrf_handler_base.llrf_control.isPhaseFFLocked() = ", llrf_handler_base.llrf_control.isPhaseFFLocked())
        if llrf_handler_base.llrf_control.isPhaseFFLocked():
            #print('PHASE FF LOCKED')
            pass
        else:
            #print('lockPhaseFF')
            llrf_handler_base.llrf_control.lockPhaseFF()
            sleep(0.02)

        # this is sketchy AF

    def reset_daq_freg(self):
        if llrf_handler_base.data.values[dat.llrf_DAQ_rep_rate_status]  == state.BAD:
            # for a
            if llrf_handler_base.llrfObj[0].amp_sp != 0:
                print("reset_daq_freg set_amp(0)")
                self.set_amp(0)
            self.set_iointr_counter += 1
            #print('reset_daq_freg = ', self.set_iointr_counter)
            if self.set_iointr_counter == 100000:
                print('self.set_iointr_counter == 10000')
                llrf_handler_base.llrf_control.resetTORSCANToIOIntr()
                sleep(0.02)
                llrf_handler_base.llrf_control.setTORACQMEvent()
                self.set_iointr_counter = 0



    def disableRFOutput(self):
        llrf_handler_base.llrf_control.disableRFOutput()

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
