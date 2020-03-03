from data_monitors.monitor import monitor
from PyQt5.QtCore import QTimer
import data.charge_measurement_data_base as dat
import numpy
import time
import requests
import json
import epics

class llrf_monitor(monitor):
    # whoami
    my_name = 'llrf_monitor'
    set_success = False
    # a history of the values when not in cooldown
    # (beware: during startup, all values are added to this list!)
    _value_history = []
    # the latest signal value

    def __init__(self):
        self.my_name = 'llrf_monitor'
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=1000)

        self.check_llrf_is_monitoring()
        self.timer = QTimer()
        #self.timer.timeout.connect(self.update_rf_values)

        self.set_success = True
        #self.timer.start(self.update_time)

        self.run()
        self.kly_pwr_pv = "CLA-GUN-LRF-CTRL-01:ad1:ch1:Power:Wnd:Avg"
        self.kly_sp_pv = "CLA-GUN-LRF-CTRL-01:vm:dsp:sp_amp:amplitude"
        self.gun_phase_pv = "CLA-GUN-LRF-CTRL-01:vm:dsp:sp_ph:phase"

    def run(self):
        # now we're ready to start the timer, (could be called from a function)
        # item = [self.bunch_charge]
        # if self.sanity_checks(item):
        #     self.timer.start(self.update_time)
        #     monitor.logger.message(self.my_name, ' STARTED running')
        #     self.set_good()
        # else:
        monitor.logger.message(self.my_name, ' NOT STARTED running')

    def update_rf_values(self, pv, time_from, time_to, hwp):
        self.kly_fwd_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.kly_pwr_pv + "&from=" + time_from + "&to=" + time_to
        self.kly_sp_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.kly_sp_pv + "&from=" + time_from + "&to=" + time_to
        self.klyfwdr = requests.get(self.kly_fwd_url)
        self.klyfwddata = self.klyfwdr.json()
        self.klyfwdevent = []
        self.klyfwdtimestamp = []
        for i in range(len(self.klyfwddata[0]["data"])):
            self.klyfwdevent.append(self.klyfwddata[0]["data"][i]["val"])
            self.klyfwdtimestamp.append(
                float(str(self.klyfwddata[0]["data"][i]["secs"]) + "." + str(self.klyfwddata[0]["data"][i]["nanos"])))
        self.klyspr = requests.get(self.kly_sp_url)
        self.klyspdata = self.klyspr.json()
        self.klyspevent = []
        self.klysptimestamp = []
        for i in range(len(self.klyspdata[0]["data"])):
            self.klyspevent.append(self.klyspdata[0]["data"][i]["val"])
            self.klysptimestamp.append(
                float(str(self.klyspdata[0]["data"][i]["secs"]) + "." + str(self.klyspdata[0]["data"][i]["nanos"])))
        monitor.data.values[dat.kly_fwd_pwr_time_stamp][hwp] = self.klyfwdtimestamp
        monitor.data.values[dat.kly_sp_time_stamp][hwp] = self.klysptimestamp
        monitor.data.values[dat.kly_fwd_pwr_values][hwp] = self.klyfwdevent
        monitor.data.values[dat.kly_sp_values][hwp] = self.klyspevent
        self.off_crest_phase = epics.caget(self.gun_phase_pv) - monitor.data.values[dat.off_crest_phase]
        monitor.data.values[dat.off_crest_phase_dict][hwp] = self.off_crest_phase

    def check_llrf_is_monitoring(self):
        pass
        # charge_buffer = monitor.charge_control.getChargeBuffer(monitor.config.charge_config['CHARGE_DIAG_TYPE'])
        # if len(charge_buffer) > 1:
        #     if charge_buffer[-1] != charge_buffer[-2]:
        #         monitor.data.values[dat.charge_status] = True
        # else:
        #     monitor.data.values[dat.charge_status] = False
