from monitor import monitor
from PyQt4.QtCore import QTimer
import data.blm_plotter_data_base as dat
import numpy, random
import time

class blm_monitor(monitor):
    # whoami
    my_name = 'blm_monitor'
    set_success = False

    def __init__(self):
        self.my_name = 'blm_monitor'
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=100)

        self.timer = QTimer()
        self.set_success = True
        self.timer.start(self.update_time)

        self.check_blm_is_monitoring()
        self.run()

    def run(self):
        # now we're ready to start the timer, (could be called from a function)
        # item = [self.bunch_charge]
        # if self.sanity_checks(item):
        #     self.timer.start(self.update_time)
        #     monitor.logger.message(self.my_name, ' STARTED running')
        #     self.set_good()
        # else:
        monitor.logger.message(self.my_name, ' running')

    def check_blm_is_monitoring(self):
        # blm_data_buffer = monitor.blm_control.getBLMRawDataBuffer(monitor.data.values[dat.bpm_names[0]])
        # if len(blm_data_buffer) > 1:
        #     if blm_data_buffer[-1] != blm_data_buffer[-2]:
        #         monitor.data.values[dat.blm_status] = True
        # else:
        #     monitor.data.values[dat.blm_status] = False
        monitor.data.values[dat.blm_status] = True

    def update_blm_voltages(self):
        self.check_blm_is_monitoring()
        if monitor.data.values[dat.blm_status] and monitor.data.values[dat.charge_status]:
            for i in monitor.data.values[dat.blm_names]:
                monitor.data.values[dat.blm_voltages][i] = monitor.bpm_control.getBLMDataBuffer(i)[-1]