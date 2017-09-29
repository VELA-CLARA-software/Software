import epics, time, math, numpy, sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LC automtic linac conditioning SCRIPT, July 2017
# v0.1 - Proof-of-principle cobbled together from gun conditioning SCRIPT
# v0.2 - Tested working on machine for LINAC conditioning
# v0.3 - Fixed some bugs (lots of "selfs") and made reverse power fractional error

class linac_condition(QObject):

    monitor_Signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent = None):
        super(linac_condition, self).__init__()
        self.last_10_img_values = []
        self.last_10_rev_pwr_values = []
        # where to write the log
        self.log_file = "breakdowns.txt"
        self.trace_log = "breakdown_trace.txt"
        # toggle actualy doing conditioning!
        self.doConditioning = False

        # tweakable parameters
        self.normal_RF_increase = 40;  # RF step increment
        self.increase_wait_time = self.wait_time = 15*60; # Time between RF step increments (in seconds)
        self.permit_RF_drop    = 1000; # RF step drop if RF permit lost
        self.rf_upper_limit    = 100000 # AW suggestion
        self.maximum_pulse_width = 2; # Absolute max pulse length
        self.nominal_pulse_width = 0.25; # Pulse width we should be at if all is well
        self.pulse_width_tolerance = 0.005  # Pulse width error we can tolerate due to Libera granularity
        self.time_of_last_increase = self.time_of_last_increase_pulse_width = time.time()
        self.dont_panic_text = "Normal Running"
        self.rep_rate = 10

        # ramp_pause_time times (seconds)
        self.ramp_pause_time = {
            'IMG_1'                 : 1,    # vac_spike NOT LESS THAN 1 !!
            'DC'                    : 1,    # DC_spike_ NOT LESS THAN 1 !!
            'LLRF_CAVITY_REV_POWER' : 1,    # REV_power_spike    NOT LESS THAN 1 !!
            'RF_PERMIT'             : 30,       # permit     NOT LESS THAN 1 !!
            'RF_PERMIT_RETURN'      : 1,        # permit     NOT LESS THAN 1 !!
        }

        # timer reset cooldown  times (seconds)
        self.event_timer_cooldown = {
            'IMG_1': 2,  # vac_spike_cooldown_time  NOT LESS THAN 1 !!
            'RF_PERMIT': 2  # permit_cooldown_time      NOT LESS THAN 1 !!
        }

        # the PVs to "continuously" monitor (for now via acquisition)
        self.pv_to_monitor = {
            'RF_PERMIT'             : epics.PV('CLA-L01-RF-PROTE-01:Cmi'),
            'RF_TRIG'               : epics.PV('CLA-L01-HRF-MOD-01:FAULT'),
            'LLRF_CAVITY_REV_POWER' : epics.PV('CLA-L01-LRF-CTRL-01:ad1:ch4:power_remote.POWER'),
            'RF_PULSE_LENGTH'       : epics.PV('CLA-L01-LRF-CTRL-01:vm:feed_fwd:duration'),
            'IMG_1'                 : epics.PV('CLA-S01-VAC-IMG-01:PRES'), #needs changing to correct IMG
            'RF_AMPLITUDE'          : epics.PV('CLA-L01-LRF-CTRL-01:vm:dsp:sp_amp:amplitude'),
            'LLRF_KLY_FWD_PWR'      : epics.PV('CLA-L01-LRF-CTRL-01:ad1:ch1:power_remote.POWER'),
            'LLRF_CAV_FWD_PWR'      : epics.PV('CLA-L01-LRF-CTRL-01:ad1:ch3:power_remote.POWER'),
            'TIM_MAINS_DIVIDER'     : epics.PV('CLA-C16-TIM-EVG-01:AcTrig-Divider-SP'),
            'TIM__EVTCODE_SP'       : epics.PV('CLA-C16-TIM-EVG-01:SoftSeq-2-EvtCode-SP'),
        }

        # these are the PVs that we sometimes get / set
        self.pv_monitor_not_alarm_values= {
            'RF_PERMIT': 65535,
            'RF_TRIG': 0,
            'LLRF_CAVITY_REV_POWER': 1.5, #factor x background for reflected power spike to be detected
            'IMG_1': 2E-9  # This is the level above background at which the pulse width drops
        }

        # keep a record of when the last alarm was
        self.pv_time_of_last_alarm = {
            'IMG_1'                 : time.time() - self.ramp_pause_time['IMG_1'],
            'RF_PERMIT'             : time.time() - self.ramp_pause_time['RF_PERMIT'],
            'LLRF_CAVITY_REV_POWER' : time.time()
        }

        # to spot a vacuum spike we have a history buffer
        self.getInitialValues()

        self.rf_dropped = False
        self.rf_permit_lost = False
        self.rf_trig_lost = False

        self.time_of_last_increase = time.time() - self.wait_time
        self.loop_start_time = time.time()
        self.breakdown_count = 0
        self.breakdown_per_minute = 0
        self.breakdown_rate = 0
        self.reset_rf_value = 100
        self.reset_rf_decrease = self.normal_RF_increase #amount to decrease from previous rf value when coming back on after breakdown

    def getInitialValues(self):
        self.pre_spike_img_mean = epics.PV('CLA-S01-VAC-IMG-01:PRES').get()
        self.rev_pwr_mean = max( epics.PV('CLA-L01-LRF-CTRL-01:ad1:ch4:power_remote.POWER').get() )
        for i in range(11):
            self.last_10_img_values.append(self.pre_spike_img_mean)
            self.last_10_rev_pwr_values.append(self.rev_pwr_mean)

    def getCurrentValues(self, pv_dictionary ):
        returndict = {}
        for name,pv in pv_dictionary.iteritems():
            #print name, '  ', pv.get()
            returndict[name] = pv.get()
        return returndict

    def currentTimeStr(self):
        return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

    # check if the time since the last alarm is greater than the cool-down time, if so return True
    def is_not_in_cool_down(self, signal):
        return True

    # check if the time since the last alarm is greater than the cool-down time, if so return True
    def is_not_in_pause_ramp(self, signal ):
        if time.time() - self.pv_time_of_last_alarm[signal] > self.ramp_pause_time[signal]:
            return True
        else:
            return False

    def check_RF_permit_is_good(self, rf_permit_signal, rf_trig_signal, rf_amp_signal):
        global permit_RF_drop, is_not_in_cool_down, rf_dropped, rf_permit_lost, rf_trig_lost

        if (self.latest_values[rf_permit_signal] != self.pv_monitor_not_alarm_values[rf_permit_signal]):
            self.rf_dropped = True
            self.rf_permit_lost = True
            print 'RF Permit Lost!'
        elif (self.latest_values[rf_trig_signal] != self.pv_monitor_not_alarm_values[rf_trig_signal]):
            self.rf_dropped = True
            self.rf_trig_lost = True
            print 'RF Trigger Lost!'
        else:
            self.rf_dropped = False
            self.rf_trig_lost = False
        if self.rf_dropped:
            self.monitor_Signal.emit(['dont_panic_text', "RF DROPPED!"])
            if self.is_not_in_cool_down(rf_permit_signal):
                self.pv_time_of_last_alarm[rf_permit_signal] = time.time()
                if self.rf_permit_lost:
                    print 'RF Permit Lost, Dropping RF amplitude by ' + str(self.permit_RF_drop) + ' and pausing RF Amplitude Ramp for ' \
                          + str(self.ramp_pause_time[rf_permit_signal]) + ' seconds'
                    self.change_RF_amp(rf_amp_signal, self.latest_values[rf_amp_signal] - self.permit_RF_drop)
            elif self.rf_trig_lost:
                self.pv_time_of_last_alarm[rf_permit_signal] = time.time()
                print 'RF Trig Lost - Please manually re-enable TRIG'
        else:
            self.monitor_Signal.emit(['dont_panic_text', "Normal Running"])

    def writelog(self, type):
        if type == 'vacuum':
            with open(self.log_file,"a") as logfile:
                logfile.write( str(time.time()) + '\t' + 'Vacuum spike' + '\t' + str(self.breakdown_count) + '\t' + str(self.breakdown_per_minute) + '\t' + str(self.normal_RF_increase) + '\n')
        elif type == 'ref':
            with open(self.log_file,"a") as logfile:
                logfile.write( str(time.time()) + '\t' + 'Reflected power spike' + '\t' + str(self.breakdown_count) + '\t' + str(self.breakdown_per_minute) + '\t' + str(self.normal_RF_increase) + '\n')

    def writetrace(self,ref_signal):
        tracestring = ""
        for i in self.latest_values[ref_signal]:
            tracestring+=str(i) +'\t'
        with open(self.trace_log,"a") as logfile:
                logfile.write( str(time.time()) + '\t' + tracestring + '\n')

    def change_RF_amp(self, rf_amp_signal, value):
        self.pv_to_monitor[rf_amp_signal].put(value)

    def check_IMG_change_is_small(self, img_signal, rf_amp_signal, rf_pulse_width_signal):
        global vac_spike_RF_drop, vac_spike_RF_pulse_width_drop, nominal_pulse_width, pre_spike_img_mean, last_10_img_values, breakdown_count, reset_rf_value
        if len(self.last_10_img_values) > 10:
           self.last_10_img_values.pop(0)
        #print 'img signal = ', latest_values[img_signal], '  pre_spike_img_mean = ', pre_spike_img_mean
        self.delta_IMG = self.latest_values[img_signal] - self.pre_spike_img_mean
        if self.delta_IMG > self.pv_monitor_not_alarm_values[img_signal]:
            self.pv_time_of_last_alarm[img_signal] = time.time()
            print 'Vac Spike, Dropping RF power to zero '
            self.dont_panic_text = "Vac Spike Detected!"
            # Changing RF Pulse Width
            self.breakdown_count += 1
            self.reset_rf_value = self.latest_values['RF_AMPLITUDE'] - self.reset_rf_decrease
            self.change_RF_amp(rf_amp_signal, 0)

            while self.delta_IMG > self.pv_monitor_not_alarm_values[img_signal]:
                print 'Sleeping for 2 seconds due to VAC spike'
                time.sleep(2)
                self.latest_values = self.getCurrentValues(self.pv_to_monitor)
                self.delta_IMG = self.latest_values[img_signal] - self.pre_spike_img_mean
            self.change_RF_amp(rf_amp_signal, self.reset_rf_value)
            writelog('vacuum')
            self.monitor_Signal.emit(['dont_panic_text', "Normal Running"])
            time.sleep(0.3)  # delays for 0.2 seconds
        else:
            # print 'new IMG mean' + str(delta_IMG)
            self.last_10_img_values.append(self.latest_values[img_signal])
            self.pre_spike_img_mean = numpy.mean(self.last_10_img_values)
            self.monitor_Signal.emit(['pre_spike_img_mean', self.pre_spike_img_mean])

    def check_LLRF_rev_power_is_low(self, ref_signal, rf_amp_signal, rf_pulse_width_signal):
        global vac_spike_RF_pulse_width_drop, nominal_pulse_width, pre_spike_dc_mean, last_10_dc_values, pv_monitor_alarm_values, breakdown_count
        if self.latest_values[ref_signal] is not None:
            #print 'latest values ref power', max( latest_values['LLRF_CAVITY_REV_POWER'])
            max_rev_power = max( self.latest_values[ref_signal] )
            if max_rev_power  > self.pv_monitor_not_alarm_values[ref_signal]*self.rev_pwr_mean:
                if self.is_not_in_cool_down(ref_signal):
                    self.dont_panic_text = "Breakdown Detected!"
                    self.pv_time_of_last_alarm[ref_signal] =  time.time()
                    print 'Reflected power spike, Dropping RF power to 0 for 3s'
                    print 'max_rev_power ' + str(max_rev_power) + ' rev_pwr_mean ' + str(self.rev_pwr_mean) + 'limit =' + str(self.pv_monitor_not_alarm_values[ref_signal]*self.rev_pwr_mean)
                    print 'self.pv_monitor_not_alarm_values[ref_signal] '  + str(self.pv_monitor_not_alarm_values[ref_signal])
                    self.breakdown_count += 1
                    self.monitor_Signal.emit(['breakdown_count', self.breakdown_count])
                    self.reset_rf_value = self.latest_values[rf_amp_signal]- self.reset_rf_decrease
                    self.change_RF_amp(rf_amp_signal, 0)
                    print 'Sleeping for 3 seconds'
                    time.sleep(3.0)
                    self.change_RF_amp(rf_amp_signal, self.reset_rf_value)
                    self.writelog('ref')
                    self.writetrace(ref_signal)
                    self.dont_panic_text = "Normal Running"
                    time.sleep(0.3) # delays for 0.3 second
            else:
                self.last_10_rev_pwr_values.append(max_rev_power)
                self.rev_pwr_mean = numpy.mean(self.last_10_rev_pwr_values)
                self.monitor_Signal.emit(['rev_pwr_mean', self.rev_pwr_mean])

    def can_increase_rf(self):
        if self.latest_values['RF_PULSE_LENGTH'] > self.nominal_pulse_width - self.pulse_width_tolerance:
            if self.pv_time_of_last_alarm['RF_PERMIT'] > self.ramp_pause_time['RF_PERMIT']:
                if time.time() - self.time_of_last_increase > self.wait_time:
                    return True
            else:
                print 'can_increase_rf thinks we are in RF permit lost cooldown '
        return False

    def getRepRate(self):
        self.rep_rate = 50 / self.latest_values['TIM_MAINS_DIVIDER'] * len(self.latest_values['TIM__EVTCODE_SP'])
        self.monitor_Signal.emit(['rep_rate', self.rep_rate])
        self.wait_time = self.increase_wait_time / (self.rep_rate / 10)
        self.monitor_Signal.emit(['wait_time', self.wait_time])

    def get_breakdown_rate(self):
        if self.breakdown_count > 0:
            self.breakdown_per_minute = self.breakdown_count / ((time.time() - self.loop_start_time) / 60)
        else:
            self.breakdown_per_minute = 0
        self.breakdown_rate = self.breakdown_per_minute * 30 / (self.rep_rate / 10)
        self.monitor_Signal.emit(['breakdown_rate', self.breakdown_rate])
        self.monitor_Signal.emit(['breakdown_per_minute', self.breakdown_per_minute])

    def updateLatestValues(self):
        self.latest_values = self.getCurrentValues( self.pv_to_monitor )

    def main_loop(self):

        self.updateLatestValues()
        self.get_breakdown_rate()
        self.getRepRate()

        if self.doConditioning:

            if self.latest_values['RF_AMPLITUDE'] > self.rf_upper_limit:  # Upper RF limit
                sys.exit()

            self.check_RF_permit_is_good('RF_PERMIT', 'RF_TRIG', 'RF_AMPLITUDE')

            self.check_IMG_change_is_small('IMG_1', 'RF_AMPLITUDE', 'RF_PULSE_LENGTH')

            self.check_LLRF_rev_power_is_low('LLRF_CAVITY_REV_POWER','RF_AMPLITUDE', 'RF_PULSE_LENGTH')

            if self.rf_dropped == True or self.rf_permit_lost == True or self.rf_trig_lost == True:
                print 'Sleeping for 2 seconds due to RF dropped'
                time.sleep(2)

            if self.can_increase_rf():
                self.increase = self.latest_values['RF_AMPLITUDE'] + self.normal_RF_increase
                self.change_RF_amp('RF_AMPLITUDE', self.increase)
                print 'Increasing RF amplitude to ' + str(self.increase) + ' - Last Power Reading was ' + str(max(self.latest_values['LLRF_CAV_FWD_PWR'])/1e6) + 'MW'
                #print 'No Events for ' + str(time.time() - time_of_last_increase) + '  RF Amp = ' + str(increase)
                self.time_of_last_increase = time.time()
            # else:
            # print 'cannot increase RF '

            self.last_pulse_length = self.latest_values['RF_PULSE_LENGTH']

            if (time.time() - self.loop_start_time) % 60 < 0.01:
                print 'Breakdown rate is ' + str(self.breakdown_per_minute) + ' breakdowns/minute (' + str(self.breakdown_per_minute * 30) + ' breakdowns/30mins with ' + str(self.breakdown_count) + ' breakdowns)'
