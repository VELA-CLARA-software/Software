from data_monitors.monitor import monitor
from PyQt5.QtCore import QTimer
import data.charge_measurement_data_base as dat
import numpy, random
import time
import requests
import json

class mag_monitor(monitor):
    # whoami
    my_name = 'mag_monitor'
    set_success = False
    # a history of the values when not in cooldown
    # (beware: during startup, all values are added to this list!)
    _value_history = []
    # the latest signal value

    def __init__(self):
        self.my_name = 'mag_monitor'
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=1000)

        self.check_mag_is_monitoring()
        self.timer = QTimer()
        #self.timer.timeout.connect(self.update_mag_values)

        self.set_success = True
        #self.timer.start(self.update_time)

        self.run()

        monitor.__init__(self, update_time=1000)

        self.timer = QTimer()
        self.set_success = True
        self.timer.start(self.update_time)
        self.bsol_pv_name = "CLA-LRG1-MAG-SOL-01:READI"
        self.sol_pv_name = "CLA-GUN-MAG-SOL-02:READI"

    def run(self):
        # now we're ready to start the timer, (could be called from a function)
        # item = [self.bunch_charge]
        # if self.sanity_checks(item):
        #     self.timer.start(self.update_time)
        #     monitor.logger.message(self.my_name, ' STARTED running')
        #     self.set_good()
        # else:
        monitor.logger.message(self.my_name, ' NOT STARTED running')

    def check_mag_is_monitoring(self):
        pass
        # charge_buffer = monitor.charge_control.getChargeBuffer(monitor.config.charge_config['CHARGE_DIAG_TYPE'])
        # if len(charge_buffer) > 1:
        #     if charge_buffer[-1] != charge_buffer[-2]:
        #         monitor.data.values[dat.charge_status] = True
        # else:
        #     monitor.data.values[dat.charge_status] = False

    def update_mag_values(self,pv,time_from,time_to,hwp):
        self.sol_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.sol_pv_name + "&from=" + time_from + "&to=" + time_to
        self.bsol_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.bsol_pv_name + "&from=" + time_from + "&to=" + time_to
        self.solr = requests.get(self.sol_url)
        self.soldata = self.solr.json()
        self.solevent = []
        self.soltimestamp = []
        for i in range(len(self.soldata[0]["data"])):
            self.solevent.append(self.soldata[0]["data"][i]["val"])
            self.soltimestamp.append(
                float(str(self.soldata[0]["data"][i]["secs"]) + "." + str(self.soldata[0]["data"][i]["nanos"])))
        self.bsolr = requests.get(self.bsol_url)
        self.bsoldata = self.bsolr.json()
        self.bsolevent = []
        self.bsoltimestamp = []
        for i in range(len(self.bsoldata[0]["data"])):
            self.bsolevent.append(self.bsoldata[0]["data"][i]["val"])
            self.bsoltimestamp.append(
                float(str(self.bsoldata[0]["data"][i]["secs"]) + "." + str(self.bsoldata[0]["data"][i]["nanos"])))
        monitor.data.values[dat.bsol_time_stamp][hwp] = self.bsoltimestamp
        monitor.data.values[dat.sol_time_stamp][hwp] = self.soltimestamp
        monitor.data.values[dat.bsol_values][hwp] = self.bsolevent
        monitor.data.values[dat.sol_values][hwp] = self.solevent
