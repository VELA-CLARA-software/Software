# llrf_handler.py
from llrf_handler_base import llrf_handler_base
from VELA_CLARA_LLRF_Control import TRIG
from time import sleep
from timeit import default_timer as timer
import src.data.rf_condition_data_base as dat
from src.data.state import state
import inspect

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

        self.should_show_llrf_interlock_active = True
        self.should_show_llrf_trig_external = True
        self.should_show_llrf_rf_output = True
        self.should_show_llrf_amp_ff_locked = True
        self.should_show_llrf_pha_ff_locked = True
        self.should_show_reset_daq_freg = True


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

    def set_amp(self, val1):
        val = float(val1)
        llrf_handler_base.logger.message('set_amp(' + str(val) + ') called from ' + str(inspect.stack()[1][3]), True)

        #llrf_handler_base.llrf_control.trigOff()
        # for trace in llrf_handler_base.config.breakdown_config['BREAKDOWN_TRACES']:#MAGIC_STRING:
        #     llrf_handler_base.llrf_control.setTraceSCAN(trace, LLRF_SCAN.PASSIVE)  # SHOULD BE INPUT Parameter
        success = False
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
                llrf_handler_base.logger.message('set_amp(' + str(val) + '), took ' + str(end - start)+\
                                             ' time,  averages NOT reset, mask_set = False', True)
            else:
                llrf_handler_base.logger.message('set_amp(' + str(val) + '), FAILED to set amp in less than 3 seconds '
                                                                           'averages NOT reset, mask_set = False', True)

        self.set_last_sp_above_100()

        return success


    def set_last_sp_above_100(self):
        llrf_handler_base.data.values[dat.amp_sp] = llrf_handler_base.llrfObj[0].amp_sp
        if llrf_handler_base.llrfObj[0].amp_sp > 100: #MAGIC_NUMBER
            llrf_handler_base.data.values[dat.last_sp_above_100] =  llrf_handler_base.llrfObj[0].amp_sp
            llrf_handler_base.logger.message('last_sp_above_100 = ' + str(llrf_handler_base.data.values[dat.last_sp_above_100]), True)



    def enable_llrf(self):
        # go through each possible LLRF paramter (except HOLD_RF_ON_COM mod / protection parmaters
        # and try and reset them
        # cancer cancer cancer
        #
        if llrf_handler_base.llrf_control.isInterlockActive():

            if self.should_show_llrf_interlock_active:
                llrf_handler_base.logger.message('enable_llrf, isInterlockActive = True, attempting setInterlockNonActive()', True)
                self.should_show_llrf_interlock_active = False
            # try and reset
            llrf_handler_base.llrf_control.setInterlockNonActive()
            # meh
            sleep(0.02)
        else:
            if self.should_show_llrf_interlock_active == False:
                llrf_handler_base.logger.message('enable_llrf, isInterlockActive = False', True)
                self.should_show_llrf_interlock_active = True
        #
        #print("llrf_handler_base.llrf_control.isTrigExternal() = ", llrf_handler_base.llrf_control.isTrigExternal())
        if llrf_handler_base.llrf_control.isTrigExternal():
            if self.should_show_llrf_trig_external == False:
                llrf_handler_base.logger.message('enable_llrf, isTrigExternal = True', True)
                self.should_show_llrf_trig_external = True
        else:
            if self.should_show_llrf_trig_external:
                llrf_handler_base.logger.message('enable_llrf, isTrigExternal = False, attempting trigExt()', True)
                self.should_show_llrf_trig_external = False
            # try and reset
            llrf_handler_base.llrf_control.trigExt()
            # meh
            sleep(0.02)
        #
        #
        if llrf_handler_base.llrf_control.isRFOutput():
            if self.should_show_llrf_rf_output == False:
                llrf_handler_base.logger.message('enable_llrf, isRFOutput = True', True)
                self.should_show_llrf_rf_output = True
        else:
            if self.should_show_llrf_rf_output:
                llrf_handler_base.logger.message('enable_llrf, isRFOutput = False, attempting enableRFOutput()', True)
                self.should_show_llrf_rf_output = False
            # reset
            llrf_handler_base.llrf_control.enableRFOutput()
            # meh
            sleep(0.02)
        #
        #
        if llrf_handler_base.llrf_control.isAmpFFLocked():
            if self.should_show_llrf_amp_ff_locked == False:
                llrf_handler_base.logger.message('enable_llrf, isAmpFFLocked = True', True)
                self.should_show_llrf_rf_output = True
        else:
            if self.should_show_llrf_amp_ff_locked:
                llrf_handler_base.logger.message('enable_llrf, isAmpFFLocked = False, attempting lockAmpFF()', True)
                self.should_show_llrf_rf_output = False
            # reset
            llrf_handler_base.llrf_control.lockAmpFF()
            # meh
            sleep(0.02)
        #
        #should_show_llrf_pha_ff_locked
        if llrf_handler_base.llrf_control.isPhaseFFLocked():
            if self.should_show_llrf_pha_ff_locked == False:
                llrf_handler_base.logger.message('enable_llrf, isPhaseFFLocked = True', True)
                self.should_show_llrf_pha_ff_locked = True
        else:
            if self.should_show_llrf_pha_ff_locked:
                llrf_handler_base.logger.message('enable_llrf, isPhaseFFLocked = False, attempting lockPhaseFF()', True)
                self.should_show_llrf_pha_ff_locked = False
            llrf_handler_base.llrf_control.lockPhaseFF()
            sleep(0.02)

        # this is sketchy AF

    def update_amp_vs_kfpow_running_stat(self):
        llrf_handler_base.data.amp_vs_kfpow_running_stat[llrf_handler_base.data.values[dat.amp_sp]] = \
            llrf_handler_base.llrf_control.getKlyFwdPwrRSState(int(llrf_handler_base.data.values[dat.amp_sp]))

    def reset_daq_freg(self):
        if llrf_handler_base.data.values[dat.llrf_DAQ_rep_rate_status]  == state.BAD:

            if self.should_show_reset_daq_freg:
                llrf_handler_base.logger.message('reset_daq_freg, llrf_DAQ_rep_rate_status == BAD', True)
                self.should_show_reset_daq_freg = False

            # for a
            if llrf_handler_base.llrfObj[0].amp_sp != 0:
                llrf_handler_base.logger.message('reset_daq_freg forcing set_amp(0)', True)
                self.set_amp(0)
            self.set_iointr_counter += 1
            #print('reset_daq_freg = ', self.set_iointr_counter)
            if self.set_iointr_counter == 100000: # MAGIC_NUMBER
                llrf_handler_base.logger.message('reset_daq_freg, set_iointr_counter = 100000', True)

                llrf_handler_base.llrf_control.resetTORSCANToIOIntr()
                sleep(0.02)
                llrf_handler_base.llrf_control.setTORACQMEvent()
                self.set_iointr_counter = 0
        else:
            if self.should_show_reset_daq_freg == False:
                llrf_handler_base.logger.message('reset_daq_freg, llrf_DAQ_rep_rate_status != BAD', True)
                self.should_show_reset_daq_freg = True




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
                    self.set_tracmasks()
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
