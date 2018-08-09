from monitor import monitor
from PyQt4.QtCore import QTimer
import data.bpm_charge_plotter_data_base as dat
import numpy, random
import time

class bpm_monitor(monitor):
    # whoami
    my_name = 'bpm_monitor'
    set_success = False

    def __init__(self):
        self.my_name = 'bpm_monitor'
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=1000)

        self.timer = QTimer()
        self.set_success = True
        self.timer.start(self.update_time)

        self.check_bpm_is_monitoring()
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

    def check_bpm_is_monitoring(self):
        bpm_data_buffer = monitor.bpm_control.getBPMRawDataBuffer(monitor.data.values[dat.bpm_name])
        if len(bpm_data_buffer) > 1:
            if bpm_data_buffer[-1] != bpm_data_buffer[-2]:
                monitor.data.values[dat.bpm_status] = True
        else:
            monitor.data.values[dat.bpm_status] = False

    def update_bpm_charge(self, bpm_name):
        monitor.data.values[dat.bpm_charge][bpm_name] = numpy.mean(monitor.bpm_control.getBPMQBuffer(bpm_name))