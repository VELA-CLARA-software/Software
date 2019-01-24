# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTimer
from controller_base import controller_base
from src.gui.gui_conditioning import gui_conditioning
import src.data.rf_condition_data_base as dat
import sys
import time
import os


class main_controller(controller_base):
    # whoami
    my_name = 'main_controller'
    #
    # other attributes will be initialised in base-class
    def __init__(self, argv, config_file):
        controller_base.__init__(self,argv, config_file)
        # flag for message in main loop
        self.has_not_shown_br_hi = True
        self.has_power = False
        #
        # timer to keep gui going durign startup
        # update timer
        self.start_up_update()

        #
        # set base class llrf_types
        controller_base.data.llrf_type = self.llrf_type
        controller_base.data_monitor.llrf_type = self.llrf_type
        #
        # more set-up after config read
        QApplication.processEvents()
        self.data.init_after_config_read()
        # once we have parsed the the pulse_breakdown_log we need ot set the active pulse count!!!
        controller_base.llrf_control.setActivePulseCount(self.data.values[dat.log_pulse_count])
        QApplication.processEvents()
        #
        # start monitoring data
        QApplication.processEvents()
        self.data_monitor.start_monitors()
        QApplication.processEvents()
        # build the gui and pass in the data
        #
        # build the gui, atm, the gui gets built last, which means many init messages are not
        # displayed to the gui text box
        self.gui = gui_conditioning()

        #self.gui = main_controller.gui
        self.gui.closing.connect(self.connectCloseEvents)
        self.gui.gui_start_up()
        self.gui.show()
        self.gui.activateWindow()
        QApplication.processEvents()
        #
        # number of pulses from pulse log
        controller_base.llrf_control.setActivePulseCount(self.data.values[dat.log_pulse_count])
        #
        # load the amp_set vs Kly_fwd_pow dictionary into c++
        self.logger.header(self.my_name + ' Loading amp_set vs Kly_fwd_pow dictionary', True)
        for key, value in controller_base.data.amp_vs_kfpow_running_stat.iteritems():
            # print key
            # print 'key type = ' + str(type(key))
            # print key
            # print key,value[0],value[1],value[2]
            # print 'value[0] type = ' + str(type(value[0]))
            # print 'value[1] type = ' + str(type(value[1]))
            # print 'value[2] type = ' + str(type(value[2]))
            self.logger.message('Data: ' + str(key)+' '+str(value[0])+' '+str(value[1])+' '+str(value[2]),True)
            controller_base.llrf_control.setKlyFwdPwrRSState(int(key),value[0],value[1],value[2])

        self.logger.header(self.my_name + ' set_mean_pwr_position', True)
        controller_base.llrf_handler.set_mean_pwr_position()
        QApplication.processEvents()
        # and mask positions!
        self.logger.header(self.my_name + ' setup_outside_mask_trace_param', True)
        controller_base.llrf_handler.setup_outside_mask_trace_param()
        QApplication.processEvents()
        #
        #
        QApplication.processEvents()
        #
        # set up main_loop main states
        self.monitor_states = self.data.main_monitor_states
        QApplication.processEvents()
        #
        # start data recording
        self.logger.header(self.my_name + ' start_logging', True)
        self.data.start_logging()
        QApplication.processEvents()

        #
        controller_base.logger.header('Show Plot')
        self.gui.update_plot()
        #
        # everything now runs from  main_loop
        #
        self.gui.llrf_enable_button.clicked.connect(self.toggle_RF_output)
        #
        self.main_loop()

    def toggle_RF_output(self):
        if self.gui.can_rf_output:
            self.llrf_control.enable_llrf()
        else:
            self.llrf_control.disableRFOutput()

    def main_loop(self):
        self.logger.header(self.my_name + ' The RF Conditioning is Preparing to Entering Main_Loop !',True)

        # reset trigger
        controller_base.llrf_handler.enable_trigger()
        #
        self.llrf_control.setGlobalCheckMask(False)
        #
        # this sets up main monitors, based on what was successfully connected
        # they are, vac, dc, breakdown, rf_on, rf_mod , .. any more ?
        self.data_monitor.init_monitor_states()

        #
        # remove this time.sleep(1) at your peril
        time.sleep(1)
        # pulse_breakdown has chosen start values, so continue, see get_pulse_count_breakdown_log()
        self.continue_ramp()
        #
        # This enables keeping the amp_sp vs KFP map in c++
        #
        # remove this time.sleep(1) at your peril
        time.sleep(1)
        controller_base.llrf_control.keepKlyFwdPwrRS()


        # enforced pause
        #time.sleep(1)
        # start trace averaging, power should be on by now
        controller_base.llrf_handler.start_trace_average()
        if controller_base.llrfObj[0].kly_fwd_power_max < controller_base.config.llrf_config['KLY_PWR_FOR_ACTIVE_PULSE']:
            controller_base.logger.message('WARNING Expecting RF power by now, kly_fwd_power_max = '
                                           '' + \
                                           str(controller_base.llrfObj[0].kly_fwd_power_max),True)
            #raw_input()
        else:
            controller_base.logger.message('Found RF power, kly_fwd_power_max = ' + \
                                           str(controller_base.llrfObj[0].kly_fwd_power_max),True)

        # get some good masks
        start_time = time.clock()
        controller_base.llrf_handler.clear_all_rolling_average()
        while 1:
            now_time = time.clock()
            if now_time  - start_time > 1.5:
                break

        controller_base.llrf_handler.set_global_check_mask(True)

        # start main loop
        controller_base.logger.header('***** ENTERING MAIN LOOP *****')

        #start_time  = time.clock()
        #counter = 0
        controller_base.data.values[dat.event_pulse_count] = 0
        while 1:
            QApplication.processEvents()

            #
            # update main monitor states

            # update states, main_monitor_states, AND enable_RF_monitor_states, if any of the enable_RF_monitor_states
            # are bad then controller_base.data_monitor.main_monitor_states[dat.can_rf_output]
            # will go bad
            controller_base.data_monitor.update_states()
            controller_base.data_monitor.update_enable_LLRF_state(gui_enable_rf = self.gui.can_rf_output)

            # # if new_bad drop SP
            if controller_base.data_monitor.new_bad():
                # disable checking masks,(precautionary)
                # controller_base.llrf_handler.set_global_check_mask(False)
                # check if spike was vac or DC
                controller_base.data_monitor.check_if_new_bad_is_vac_or_DC()

            elif controller_base.data_monitor.enable_RF_bad():
                controller_base.llrf_handler.enable_llrf()


            elif controller_base.data_monitor.new_good_no_bad():
                # start checking masks again
                if controller_base.data.values[dat.breakdown_rate_hi]:
                    self.ramp_down()
                else:
                    self.continue_ramp()
                #controller_base.llrf_handler.enable_trigger()
                self.logger.message('PYTHON MAIN LOOP: in state new_good_no_bad, setting Global Check Mask to TRUE',True)
                controller_base.llrf_handler.set_global_check_mask(True)


            # if everything is good carry on increasing
            elif controller_base.data_monitor.all_good():
                # set new mask, if changed power
                #controller_base.llrf_handler.set_mask()

                # make sure global mask checking is enabled
                controller_base.llrf_handler.set_global_check_mask(True)

                # if there has been enough time since
                # the last increase get the new llrf sp
                # now we update based on pulses
                if controller_base.data.reached_min_pulse_count_for_this_step(): # check this number in the look up
                    if self.gui.can_ramp:
                        if controller_base.data.values[dat.breakdown_rate_hi]:
                            if self.has_not_shown_br_hi:
                                self.logger.message('MAIN LOOP all good, but breakdown rate too high: Rate = ' + str(controller_base.data.values[dat.breakdown_rate]))
                                self.has_not_shown_br_hi = False
                        else:
                            self.ramp_up()
                            self.has_not_shown_br_hi = True
                    else:# gui disabled ramp
                        pass
                        #self.logger.message('MAIN LOOP allgood, pulse count good gui in pause ramp mode')
                else:# not reached min count
                    # self.logger.message('MAIN LOOP all good, but pulse count low, ' +
                    #                     str(controller_base.data.values[dat.event_pulse_count]) +
                    #                     ' \ '+str(controller_base.data.values[dat.required_pulses]))
                    pass

            else:
                #print "not all good"
                pass
            #raw_input()
            # end = timer()
            # print(end - start)

    def continue_ramp(self):

        ## this bit will be broke
        ##

        self.logger.message('continue_ramp ' + str(controller_base.data.amp_sp_history[-1]))
        # apply the old settings
        print ('continue_ramp',controller_base.data.amp_sp_history[-1])

        controller_base.llrf_handler.set_amp(controller_base.data.amp_sp_history[-1])
        self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
        #self.llrf_control.resetAverageTraces()
        self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()

    def ramp_up(self):

        self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)

        new_amp = controller_base.data.get_new_set_point( controller_base.data.values[dat.next_power_increase]  )

        # update the plot with new values
        self.gui.update_plot()
        QApplication.processEvents()

        # move this in
        # new_amp = controller_base.data.get_new_set_point_DEV( controller_base.data.values[dat.next_power_increase]  )
        if new_amp:
            controller_base.llrf_handler.set_amp(new_amp)
            controller_base.data.move_up_ramp_curve()
            #self.gui.plot_amp_sp_pwr()
        else:
            # do nomminal increase
            controller_base.llrf_handler.set_amp(self.llrf_control.getAmpSP() + controller_base.config.llrf_config['DEFAULT_RF_INCREASE_LEVEL'])
            # update the next sp decrease
            controller_base.data.set_next_sp_decrease()
        self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()

    def ramp_down(self):
        controller_base.llrf_handler.enable_llrf()
        controller_base.llrf_handler.set_amp(controller_base.data.values[dat.next_sp_decrease])
        self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
        self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
        # reset values RENAME
        self.data.move_down_ramp_curve()




    # over load close
    def connectCloseEvents(self):
        self.gui.close()
        self.data.close()
        self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
        self.logger.message('Fin - RF conditioning closing down, goodbye.')
        sys.exit()

    def start_up_update(self):
        pass
        #self.timer = QTimer()
        #self.timer.setSingleShot(False)
        #self.timer.timeout.connect(self.qt_process_events)
        #self.timer.start(200)

    def qt_process_events(self):
        pass
        #QApplication.processEvents()

    def set_last_mask_epoch(self):
        self.epoch = time.time()

    def seconds_passed(self,secs):
        return time.time() - self.epoch >= secs
