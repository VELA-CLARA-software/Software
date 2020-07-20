#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify  //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Controllers is distributed in the hope that it will be useful,       //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   03-07-2019
//  FileName:    main_controller.py
//  Description: The main_controller, holds all objects adn passes data/messsages betwen them
//
//
//
//
//*/
'''
#from PyQt4.QtGui import QApplication
#from PyQt4.QtCore import QTimer
#from controller_base import controller_base
#from src.gui.gui_conditioning import gui_conditioning
#import src.data.rf_condition_data_base as dat
#from src.data.state import state
import sys
import time
import os

print('main_controller: import hardware_control_hub')
from src.controllers.hardware_control_hub import hardware_control_hub
print('main_controller: import config')
from src.data.config import config
print('main_controller: import rf_conditioning_logger')
from src.data.rf_conditioning_logger import rf_conditioning_logger
print('main_controller: import rf_conditioning_data')
from src.data.rf_conditioning_data import rf_conditioning_data
print('main_controller: import monitor_hub')
from src.monitors.monitor_hub import monitor_hub
from src.view.rf_condition_view import rf_condition_view

from PyQt4.QtGui import QApplication


#class main_controller(controller_base):
class main_controller(object):


    #
    # other attributes will be initialised in base-class
    #
    # We are going to have multiple debug modes so that you can set it from the command line,
    # hardcoded in to the source code, etc, PLUS in the config file
    def __init__(self, argv, config_file, debug=True, debug2=True):
        print(__name__, " init ")
        self.debug = True
        if debug == False:
            if debug2 == False:
                self.debug = False

        # args passed in from command line
        self.argv = argv

        # pop the view so we can display startup messages
        #
        self.view = rf_condition_view()
        self.view.show()


        QApplication.processEvents()
        #
        # Create config reader, and get configuration
        print(__name__ + ', attempting to read config: ' + config_file)
        self.config = config()
        self.get_config(config_file)
        print(__name__ + ', got Config, starting Logging\n')

        # Set the config for the GUI
        self.view.config = self.config
        self.view.start_gui_update()

        #
        # start logging, sets up main text file logging, and logs the config
        self.logger = rf_conditioning_logger(debug=self.debug, column_width=80)
        self.logger.setup_text_log_files()
        self.logger.log_config()

        #
        # create a data object
        self.logger.message_header(__name__ + ', create rf_conditioning_data object',
                                   add_to_text_log=True, show_time_stamp=True)
        self.data = rf_conditioning_data(debug=self.debug)
        self.data.initialise()
        self.values = self.data.values


        # should thios happen here, or in the view?
        self.view.data = self.data
        self.view.values = self.data.values
        self.view.start_gui_update()
        #
        # CATAP hardware controllers, these live here and are passed to where they are needed
        # self.hardware.start_up() actually creates the objects, this should only be done once,
        # here! so that we don't create multiple controllers
        self.logger.message_header(__name__ + ', create hardware_control_hub object',
                                   add_to_text_log=True,show_time_stamp=True)
        self.hardware = hardware_control_hub()
        self.hardware.start_up()

        self.hardware.llrf_controller.set_trace_mean_positions()
        # SET TRACE SCAN Paramaters
        self.hardware.llrf_controller.set_trace_SCAN()



        #
        # CATAP hardware controllers, these live here and are passed to where they are needed
        self.logger.message_header(__name__ + ', create monitor_hub object',
                                   add_to_text_log=True,show_time_stamp=True)
        self.monitor_hub = monitor_hub()
        self.monitor_hub.start_monitors()


        # connect buttons

        self.view.update_expert_values_button.clicked.connect(self.update_expert_values) # MUST
        # BE CONNECTED AFTER MONITOR_HUB is created


        #print("manual pause here!!!")
        #raw_input()
        #
        # Start Data Logging
        self.logger.start_binary_data_logging(self.data.values)
        self.main_loop()

    def main_loop(self):
        self.values[rf_conditioning_data.required_pulses] = self.config.raw_config_data[
            'DEFAULT_PULSE_COUNT']


        '''
            check states and apply power (need RFR)
            start averaging
            start checking OMED

            check all the relevant states and set a combined state
            update_enable_LLRF_state() sets a flag for "can_rf_output"

            update the main_monitor states
            more flags for the state of each main monitor that can cause a switch off

            if new_bad() (in monitors vac, and BD (
                print / log a message

            elif enable_RF_bad(): # checks can_rf_output
                if user gui buttons enable RF:
                    enable RF

            elif daq_freq_bad:
                reset daq_freq_bad
            elif daq_freq_new_good
                reset daq_freq states to good

            elif new_good:
                ramp_down()

            elif all_good

                if reached_min_pulse_count_for_this_step()

                    if gui_can_ramp()

                        if breakdown_rate_low
                            print a message

                        elif vac_level_hi:
                            print a message

                        else:
                            ramp_up()
                else:

                    continue (do some logging)
        '''
        self.logger.message_header(
            __name__ + ' The RF Conditioning is Preparing to Entering Main_Loop !',
            add_to_text_log=True, show_time_stamp=True)



        self.hardware.llrf_control.keepKlyFwdPwrRS()
        self.hardware.llrf_controller.enable_trigger()

        #  enable the RF
        self.hardware.llrf_controller.enable_llrf()


        # continue on the last but entry from the pusle_breakdown_log
        # pulse_breakdown has chosen start values, so continue, see get_pulse_count_breakdown_log()
        #

        print(self.data.amp_sp_history[-1])

        # This needs to be the RELATIVELY-FAST-RAMP FUNCTiION
        self.hardware.llrf_controller.set_amp( self.data.amp_sp_history[-1] )
        #self.hardware.llrf_control.set_amp( self.data.amp_sp_history[-1] )


        while 1:
            QApplication.processEvents()
            # check all the relevant states and set a combined state
            # update_enable_LLRF_state() sets a flag for "can_rf_output"

            # update the main_monitor states
            # more flags for the state of each main monitor that can cause a switch off

            # if new_bad() (in monitors vac, and BD (
            # print / log a message
            #
            # elif enable_RF_bad(): # checks can_rf_output
            #     if user gui buttons enable RF:
            # enable RF
            #
            # elif daq_freq_bad:
            # reset daq_freq_bad
            # elif daq_freq_new_good
            # reset daq_freq states to good
            #
            # elif new_good:
            # ramp_down()
            #
            # elif all_good
            time.sleep(2)

            if self.reached_min_pulse_count_for_this_step():
                if self.values[rf_conditioning_data.gui_can_ramp]:
                    if  self.values[rf_conditioning_data.vac_level_can_ramp]:
                        if self.values[rf_conditioning_data.breakdown_rate_low]:
                            self.ramp_up() # TODO better name??, ramp_up from a normal stae
                        else:
                            print("can;t ramp BD rate  hi")
                    else:
                        print("can;t ramp vac level hi")
                else:
                    print("main loop can't ramp: GUI DISABLED RAMPING")
            else:
                # continue (do some logging)
                print("do some logging")
                self.monitor_hub.llrf_monitor.update_amp_vs_kfpow_running_stat()


    def ramp_up(self):
        self.logger.message_header(' Ramp Up ')

        setpoint_before_ramp =  self.hardware.llrf_obj[0].amp_sp
        if setpoint_before_ramp < 100:
            self.logger.message('!!WARNING!! Current setpoint before Ramp Up = ' + str(
                setpoint_before_ramp) + ' suspect a breakdown has very recently occurred! ')
        #
        # update pulse breakdown log
        self.data.add_to_pulse_breakdown_log(self.hardware.llrf_obj[0].amp_sp)

        # GET NEW SET_POINT
        # new amp always returns a value!!


        new_amp = self.data.get_new_set_point(  10000 ) # value from ramp.py and ramp_index

        # #
        # # set new_amp
        # if controller_base.llrf_handler.set_amp(new_amp):
        #     pass
        # else:
        #     # we failed to set the requested amplitude .... erm.... not sure what to do ????
        #     pass
        #
        # #
        # # log data at the new setpoint MUST BE BEFORE  move_up_ramp_curve()
        # #
        # controller_base.llrf_handler.update_amp_vs_kfpow_running_stat()
        # self.data.log_kly_fwd_power_vs_amp()
        # #
        # # move up curve (when below ~1MW
        # ''' !!! also calls set_next_sp_decrease !!!'''
        # controller_base.data.move_up_ramp_curve()
        # #
        # '''Sanity Check '''
        # if setpoint_before_ramp != controller_base.data.values[dat.next_sp_decrease]:
        #     self.logger.message('!!! Warning Unexpected next_sp_decrease ' + str(
        #         setpoint_before_ramp) + ' != ' + str(
        #         controller_base.data.values[dat.next_sp_decrease]), True)
        # #
        # # update the plot with new values
        # self.gui.update_plot()
        # QApplication.processEvents()
        # #
        # # reset active pulse counters
        # self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
        # #
        # self.logger.message(
        #     'ramp_up FINISHED, we went from ' + str(setpoint_before_ramp) + ' to ' + str(new_amp),
        #     True)




    def reached_min_pulse_count_for_this_step(self):
        return self.values[rf_conditioning_data.event_pulse_count] >= self.values[rf_conditioning_data.required_pulses]

    def toggle_RF_output(self):
        ''' this function should be connected to the GUI enable / diasable LLRF, but MUST be run
        AFTER rf_conditioning_data.gui_can_rf_output is changed to the requested value '''
        if self.values[rf_conditioning_data.gui_can_rf_output]:
            print("toggle_RF_output(), gui.can_rf_output, so calling enable_llrf ")
            self.hardware.llrf_controller.enable_llrf()
        else:
            self.hardware.llrf_controller.disableRFOutput()

#
#
# '''
#         # reset trigger
#         controller_base.llrf_handler.enable_trigger()
#         #
#         self.llrf_control.setGlobalCheckMask(False)
#         #
#         # this sets up main monitors, based on what was successfully connected
#         # they are, vac, dc, breakdown, rf_on, rf_mod , .. any more ?
#         self.data_monitor.init_monitor_states()
#
#         #
#         # remove this time.sleep(1) at your peril
#         time.sleep(1)
#         #
#         # RESET TH EEVNT PULSE COUNT TO ZERO
#         self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
#
#         #  enable the RF
#         self.toggle_RF_output()
#
#         controller_base.data_monitor.update_states()
#         controller_base.data_monitor.update_enable_LLRF_state(gui_enable_rf=self.gui.can_rf_output)
#
#         #
#         # This enables keeping the amp_sp vs KFP map in c++
#         #
#         # remove this time.sleep(1) at your peril
#         controller_base.llrf_control.keepKlyFwdPwrRS()
#
#         # continu eon the last but entry from the pusle_breakdown_log
#         # pulse_breakdown has chosen start values, so continue, see get_pulse_count_breakdown_log()
#
#         #
#         controller_base.llrf_handler.set_amp(controller_base.data.amp_sp_history[-1])
#
#         # controller_base.data.values[dat.latest_ramp_up_sp] =
#         # controller_base.data.amp_sp_history[-1]
#
#         # enforced pause
#         # time.sleep(1)
#         # start trace averaging, power should be on by now
#         controller_base.llrf_handler.start_trace_average()
#         if controller_base.llrfObj[0].kly_fwd_power_max < controller_base.config.llrf_config[
#             'KLY_PWR_FOR_ACTIVE_PULSE']:
#             controller_base.logger.message('WARNING Expecting RF power by now, kly_fwd_power_max '
#                                            '= '
#                                            '' + str(controller_base.llrfObj[0].kly_fwd_power_max),
#                                            True)  # raw_input()
#         else:
#             controller_base.logger.message('Found RF power, kly_fwd_power_max = ' + str(
#                 controller_base.llrfObj[0].kly_fwd_power_max), True)
#
#         # get some good masks
#         start_time = time.clock()
#         controller_base.llrf_handler.clear_all_rolling_average()
#         while 1:
#             now_time = time.clock()
#             if now_time - start_time > 1.5:
#                 break
#
#         controller_base.llrf_handler.set_global_check_mask(True)
#
#         # start main loop
#         controller_base.logger.header('***** ENTERING MAIN LOOP *****')
#
#         # start_time  = time.clock()
#         # counter = 0
#         controller_base.data.values[dat.event_pulse_count] = 0
# '''




    def quit_app(self, message=""):
        print(message)
        quit()


    def get_config(self, config_file):
        self.config.config_file = config_file
        self.config.read_config()

    def update_expert_values(self):
        # get all teh expert values from the various places that want them
        print("self.update_expert_values called")
        self.monitor_hub.llrf_monitor.get_llrf_expert_values()
        # update the gui with the latest values
        self.view.update_expert_values_in_gui()





















    #
    #     # flag for message in main loop
    #     self.has_not_shown_br_hi = True
    #     self.has_power = False
    #     #
    #     # timer to keep gui going durign startup
    #     # update timer does nothin gnow
    #     self.start_up_update()
    #     #
    #     # set base class llrf_types
    #     controller_base.data.llrf_type = self.llrf_type
    #     controller_base.data_monitor.llrf_type = self.llrf_type
    #     #
    #     # more set-up after config read
    #     QApplication.processEvents()
    #     self.data.init_after_config_read()
    #     # once we have parsed the the pulse_breakdown_log we need ot set the active pulse count!!!
    #     controller_base.llrf_control.setActivePulseCount(self.data.values[dat.log_pulse_count])
    #     QApplication.processEvents()
    #     #
    #     # start monitoring data
    #     QApplication.processEvents()
    #
    #     self.data_monitor.start_monitors()
    #
    #     QApplication.processEvents()
    #     # build the gui and pass in the data
    #     #
    #     # build the gui, atm, the gui gets built last, which means many init messages are not
    #     # displayed to the gui text box
    #     self.gui = gui_conditioning()
    #
    #     # self.gui = main_controller.gui
    #     self.gui.closing.connect(self.connectCloseEvents)
    #     self.gui.gui_start_up()
    #     self.gui.show()
    #     self.gui.activateWindow()
    #
    #     QApplication.processEvents()
    #     #
    #     # number of pulses from pulse log
    #     controller_base.llrf_control.setActivePulseCount(self.data.values[dat.log_pulse_count])
    #     #
    #     # load the amp_set vs Kly_fwd_pow dictionary into c++
    #     self.logger.header(self.my_name + ' Loading amp_set vs Kly_fwd_pow dictionary', True)
    #     for key, value in controller_base.data.amp_vs_kfpow_running_stat.iteritems():
    #         # print key
    #         # print 'key type = ' + str(type(key))
    #         # print key
    #         # print key,value[0],value[1],value[2]
    #         # print 'value[0] type = ' + str(type(value[0]))
    #         # print 'value[1] type = ' + str(type(value[1]))
    #         # print 'value[2] type = ' + str(type(value[2]))
    #         self.logger.message(
    #             'Data: ' + str(key) + ' ' + str(value[0]) + ' ' + str(value[1]) + ' ' + str(
    #                 value[2]), True)
    #         controller_base.llrf_control.setKlyFwdPwrRSState(int(key), value[0], value[1],
    #                                                          value[2])
    #
    #     self.logger.header(self.my_name + ' set_mean_pwr_position', True)
    #     controller_base.llrf_handler.set_mean_pwr_position()
    #     QApplication.processEvents()
    #     # and mask positions!
    #     self.logger.header(self.my_name + ' setup_outside_mask_trace_param', True)
    #     controller_base.llrf_handler.setup_outside_mask_trace_param()
    #     QApplication.processEvents()
    #     #
    #     #
    #     QApplication.processEvents()
    #     #
    #     # set up main_loop main states
    #     self.monitor_states = self.data.main_monitor_states
    #     QApplication.processEvents()
    #     #
    #     # start data recording
    #     self.logger.header(self.my_name + ' start_logging', True)
    #     self.data.start_logging()
    #     QApplication.processEvents()
    #
    #     #
    #     controller_base.logger.header('Show Plot')
    #     self.gui.update_plot()
    #     #
    #     # everything now runs from  main_loop
    #     #
    #     self.gui.llrf_enable_button.clicked.connect(self.toggle_RF_output)
    #     #
    #     self.main_loop()
    #
    # def toggle_RF_output(self):
    #     if self.gui.can_rf_output:
    #         print("toggle_RF_output(), gui.can_rf_output, so calling enable_llrf ")
    #         controller_base.llrf_handler.enable_llrf()
    #     else:
    #         self.llrf_control.disableRFOutput()
    #
    # def main_loop(self):
    #     self.logger.header(
    #         self.my_name + ' The RF Conditioning is Preparing to Entering Main_Loop !', True)
    #
    #     # reset trigger
    #     controller_base.llrf_handler.enable_trigger()
    #     #
    #     self.llrf_control.setGlobalCheckMask(False)
    #     #
    #     # this sets up main monitors, based on what was successfully connected
    #     # they are, vac, dc, breakdown, rf_on, rf_mod , .. any more ?
    #     self.data_monitor.init_monitor_states()
    #
    #     #
    #     # remove this time.sleep(1) at your peril
    #     time.sleep(1)
    #     #
    #     # RESET TH EEVNT PULSE COUNT TO ZERO
    #     self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
    #
    #     #  enable the RF
    #     self.toggle_RF_output()
    #
    #     controller_base.data_monitor.update_states()
    #     controller_base.data_monitor.update_enable_LLRF_state(gui_enable_rf=self.gui.can_rf_output)
    #
    #     #
    #     # This enables keeping the amp_sp vs KFP map in c++
    #     #
    #     # remove this time.sleep(1) at your peril
    #     controller_base.llrf_control.keepKlyFwdPwrRS()
    #
    #     # continu eon the last but entry from the pusle_breakdown_log
    #     # pulse_breakdown has chosen start values, so continue, see get_pulse_count_breakdown_log()
    #
    #     #
    #     controller_base.llrf_handler.set_amp(controller_base.data.amp_sp_history[-1])
    #
    #     # controller_base.data.values[dat.latest_ramp_up_sp] =
    #     # controller_base.data.amp_sp_history[-1]
    #
    #     # enforced pause
    #     # time.sleep(1)
    #     # start trace averaging, power should be on by now
    #     controller_base.llrf_handler.start_trace_average()
    #     if controller_base.llrfObj[0].kly_fwd_power_max < controller_base.config.llrf_config[
    #         'KLY_PWR_FOR_ACTIVE_PULSE']:
    #         controller_base.logger.message('WARNING Expecting RF power by now, kly_fwd_power_max '
    #                                        '= '
    #                                        '' + str(controller_base.llrfObj[0].kly_fwd_power_max),
    #                                        True)  # raw_input()
    #     else:
    #         controller_base.logger.message('Found RF power, kly_fwd_power_max = ' + str(
    #             controller_base.llrfObj[0].kly_fwd_power_max), True)
    #
    #     # get some good masks
    #     start_time = time.clock()
    #     controller_base.llrf_handler.clear_all_rolling_average()
    #     while 1:
    #         now_time = time.clock()
    #         if now_time - start_time > 1.5:
    #             break
    #
    #     controller_base.llrf_handler.set_global_check_mask(True)
    #
    #     # start main loop
    #     controller_base.logger.header('***** ENTERING MAIN LOOP *****')
    #
    #     # start_time  = time.clock()
    #     # counter = 0
    #     controller_base.data.values[dat.event_pulse_count] = 0
    #     while 1:
    #         QApplication.processEvents()
    #
    #         #
    #         # update main monitor states
    #         # update states, main_monitor_states, AND enable_RF_monitor_states, if any of the
    #         # enable_RF_monitor_states
    #         # are bad then controller_base.data_monitor.main_monitor_states[dat.can_rf_output]
    #         # will go bad
    #         controller_base.data_monitor.update_enable_LLRF_state(
    #             gui_enable_rf=self.gui.can_rf_output)
    #         controller_base.data_monitor.update_states()
    #
    #         # # if new_bad drop SP
    #         if controller_base.data_monitor.new_bad():
    #             # self.logger.message('PYTHON MAIN LOOP: in state new_bad', True)
    #             #
    #             # for key,value in controller_base.data_monitor.main_monitor_states.iteritems():
    #             #     print(key,value)
    #             # disable checking masks,(precautionary)
    #             # controller_base.llrf_handler.set_global_check_mask(False)all
    #             # check if spike was vac or DC
    #             controller_base.data_monitor.check_if_new_bad_is_vac_or_DC()
    #
    #
    #         elif controller_base.data_monitor.enable_RF_bad():
    #             if self.gui.can_rf_output:
    #                 # self.logger.message('PYTHON MAIN LOOP: in state enable_RF_bad,
    #                 # gui.can_rf_output = True, calling enable_llrf', True)
    #                 controller_base.llrf_handler.enable_llrf()
    #
    #         elif controller_base.data_monitor.daq_freq_bad():
    #             # print("MAIN LOOP: daq_freq_bad")
    #             controller_base.llrf_handler.reset_daq_freg()
    #
    #         elif controller_base.data_monitor.daq_freq_new_good():
    #             # print("MAIN LOOP: daq_freq_new_good")
    #             self.data.values[dat.llrf_DAQ_rep_rate_status] = state.GOOD
    #             self.data.values[dat.llrf_DAQ_rep_rate_status_previous] = state.GOOD
    #             self.continue_ramp_from_DAQ_freq_error()
    #
    #
    #         elif controller_base.data_monitor.new_good_no_bad():
    #             # ]self.logger.message('PYTHON MAIN LOOP: in state new_good_no_bad',True)
    #             # This switch may get set when manually disabling then enabling rf via the GUI
    #             # button
    #             # WE now always ramp down when coming back from an off state ((do we want that
    #             # when manually disableing RF???)
    #
    #             # SHOULD THE SEE BEFORE RAMPDOWN???  DEBUG DEBUG
    #             controller_base.llrf_handler.set_global_check_mask(True)
    #             self.ramp_down()  # self.logger.message('PYTHON MAIN LOOP: in state   #
    #         # new_good_no_bad, setting Global Check Mask to TRUE',True)  #   #
    #         # controller_base.llrf_handler.set_global_check_mask(True)
    #
    #         # if everything is good carry on increasing
    #         elif controller_base.data_monitor.all_good():
    #             # self.logger.message('PYTHON MAIN LOOP: in state all_good', True)
    #             # set new mask, if changed power
    #             # controller_base.llrf_handler.set_mask()
    #
    #             # make sure global mask checking is enabled (this can probably go...)
    #             controller_base.llrf_handler.set_global_check_mask(True)
    #
    #             # if there has been enough time since
    #             # the last increase get the new llrf sp
    #             # now we update based on pulses
    #             if controller_base.data.reached_min_pulse_count_for_this_step():  # check this
    #                 # number in the look up
    #                 if self.gui.can_ramp:
    #                     if controller_base.data.values[dat.breakdown_rate_low]:
    #                         if self.has_not_shown_br_hi:
    #                             self.logger.message(
    #                                 'MAIN: continue ramp LOOP all good, but breakdown rate too '
    #                                 'high: '
    #                                 'Rate = ' + str(
    #                                     controller_base.data.values[dat.breakdown_rate]))
    #                             self.has_not_shown_br_hi = False
    #                     elif controller_base.data.values[dat.vac_level_can_ramp] == state.BAD:
    #                         pass
    #                     else:
    #                         self.ramp_up()
    #                         self.has_not_shown_br_hi = True
    #                 else:  # gui disabled ramp
    #                     pass  # self.logger.message('MAIN LOOP allgood, pulse count good gui in
    #                 # pause ramp mode')
    #             else:  # not reached min count
    #                 # self.logger.message('MAIN LOOP all good, but pulse count low, ' +
    #                 #                     str(controller_base.data.values[dat.event_pulse_count]) +
    #                 #                     ' \ '+str(controller_base.data.values[
    #                 #                     dat.required_pulses]))
    #                 self.continue_ramp()
    #                 pass
    #         else:
    #             # self.logger.message('PYTHON MAIN LOOP: in state PASS', True)
    #             # print "not all good"
    #             pass  # raw_input()  # end = timer()  # print(end - start)  # print(
    #         # controller_base.llrfObj[0].amp_sp,   # controller_base.data.amp_sp_history[-1])
    #
    # def continue_ramp_from_DAQ_freq_error(self):
    #     self.logger.header(' continue ramp from DAQ freq error ', True)
    #     controller_base.llrf_handler.set_amp(controller_base.data.values[dat.last_sp_above_100])
    #
    #     self.data.log_kly_fwd_power_vs_amp()
    #
    # def continue_ramp(self):
    #     self.data.log_kly_fwd_power_vs_amp()
    #
    # def ramp_up(self):
    #     self.logger.header(' Ramp Up ', True)
    #     setpoint_before_ramp = controller_base.llrfObj[0].amp_sp
    #     if setpoint_before_ramp < 100:
    #         self.logger.message('!!WARNING!! Current setpoint before Ramp Up = ' + str(
    #             setpoint_before_ramp) + ' suspect a breakdown has very recently occurred! ', True)
    #     #
    #     # Add
    #     self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
    #
    #     # GET NEW SET_POINT
    #     # new amp always returns a value!!
    #     new_amp = controller_base.data.get_new_set_point(
    #         controller_base.data.values[dat.next_power_increase])
    #
    #     #
    #     # set new_amp
    #     if controller_base.llrf_handler.set_amp(new_amp):
    #         pass
    #     else:
    #         # we failed to set the requested amplitude .... erm.... not sure what to do ????
    #         pass
    #
    #     #
    #     # log data at the new setpoint MUST BE BEFORE  move_up_ramp_curve()
    #     #
    #     controller_base.llrf_handler.update_amp_vs_kfpow_running_stat()
    #     self.data.log_kly_fwd_power_vs_amp()
    #     #
    #     # move up curve (when below ~1MW
    #     ''' !!! also calls set_next_sp_decrease !!!'''
    #     controller_base.data.move_up_ramp_curve()
    #     #
    #     '''Sanity Check '''
    #     if setpoint_before_ramp != controller_base.data.values[dat.next_sp_decrease]:
    #         self.logger.message('!!! Warning Unexpected next_sp_decrease ' + str(
    #             setpoint_before_ramp) + ' != ' + str(
    #             controller_base.data.values[dat.next_sp_decrease]), True)
    #     #
    #     # update the plot with new values
    #     self.gui.update_plot()
    #     QApplication.processEvents()
    #     #
    #     # reset active pulse counters
    #     self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
    #     #
    #     self.logger.message(
    #         'ramp_up FINISHED, we went from ' + str(setpoint_before_ramp) + ' to ' + str(new_amp),
    #         True)
    #
    # def ramp_down(self):
    #     self.logger.header(' Ramp Down ', True)
    #
    #     setpoint_before_ramp = controller_base.llrfObj[0].amp_sp
    #
    #     next_step = 0
    #
    #     if setpoint_before_ramp < 100:
    #         pass
    #     else:
    #         self.logger.message('!!WARNING!! Current setpoint before Ramp Down = ' + str(
    #             setpoint_before_ramp) + ' This might be high if we are here due to a breakdown '
    #                                     '.... ! ',
    #                             True)
    #
    #     if controller_base.data.values[dat.last_106_bd_count] > 30:  # MAGIC_NUMBER
    #         self.logger.message(str(controller_base.data.values[
    #                                     dat.last_106_bd_count]) + ' is Too many breakdowns in last '
    #                                                               'million setting sp = 0, '
    #                                                               'and disabling ramping',
    #                             True)
    #         controller_base.llrf_handler.set_amp(0)  # MAGIC_NUMBER
    #         self.gui.can_ramp = False
    #
    #     elif controller_base.data.values[dat.last_106_bd_count] > 10:  # MAGIC_NUMBER
    #         # force a known step-down if breakdown rate is high
    #
    #         next_step = controller_base.data.values[dat.last_sp_above_100] - 20.0
    #         if controller_base.data.values[dat.next_sp_decrease] < next_step:
    #             next_step = controller_base.data.values[dat.next_sp_decrease]
    #         elif next_step < 0:
    #             next_step = 0
    #         self.logger.message('> 10 breakdowns in last million, ramp down to = ' + str(
    #             next_step),
    #                             True)
    #
    #     else:
    #         controller_base.llrf_handler.enable_llrf()
    #         next_step = controller_base.data.values[dat.next_sp_decrease]
    #
    #     controller_base.llrf_handler.set_amp(next_step)  # MAGIC_NUMBER
    #
    #     self.data_monitor.outside_mask_trace_monitor.reset_event_pulse_count()
    #     # reset values RENAME
    #     self.data.move_down_ramp_curve()
    #     self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
    #
    #     self.logger.message(
    #         'ramp_down FINISHED, we went from ' + str(setpoint_before_ramp) + ' to ' + str(
    #             next_step), True)
    #
    # # over load close to get one final data point before destruction
    # def connectCloseEvents(self):
    #     self.gui.close()
    #     self.data.close()
    #     self.data.add_to_pulse_breakdown_log(controller_base.llrfObj[0].amp_sp)
    #     self.logger.message('Fin - RF conditioning closing down, goodbye.')
    #     sys.exit()
    #
    # # not used
    # def start_up_update(self):
    #     pass  # self.timer = QTimer()  # self.timer.setSingleShot(False)  #   #
    # # self.timer.timeout.connect(self.qt_process_events)  # self.timer.start(200)
    #
    # # not used
    # def qt_process_events(self):
    #     pass  # QApplication.processEvents()
    #
    # # not used
    # def set_last_mask_epoch(self):
    #     self.epoch = time.time()
    #
    # # not used
    # def seconds_passed(self, secs):
    #     return time.time() - self.epoch >= secs
