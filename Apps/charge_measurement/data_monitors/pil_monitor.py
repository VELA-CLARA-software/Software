from data_monitors.monitor import monitor
from PyQt5.QtCore import QTimer
import data.charge_measurement_data_base as dat
import numpy, random
import time

class pil_monitor(monitor):
    # whoami
    my_name = 'pil_monitor'
    set_success = False

    def __init__(self):
        self.my_name = 'mag_monitor'
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=1000)

        self.timer = QTimer()
        self.set_success = True
        self.timer.start(self.update_time)

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

    def update_mag_readi(self):
        pass

    def update_bpm_attenuations(self):
        pass
        # monitor.data.values[dat.get_ra1] = monitor.bpm_control.getRA1(monitor.data.values[dat.bpm_name])
        # monitor.data.values[dat.get_ra2] = monitor.bpm_control.getRA2(monitor.data.values[dat.bpm_name])

    def check_sa_equals_ra(self):
        r = False
        # if (monitor.data.values[dat.get_ra1] == monitor.data.values[dat.
        #         set_sa1_current]
        #     and monitor.data.values[dat.get_ra2] == monitor.data.values[dat.
        #                 set_sa2_current]):
        #     r = True
        # else:
        #     # r = True
        #     monitor.data.values[dat.set_sa1_current] = monitor.data.values[dat.set_sa1_current] + 1
        #     monitor.data.values[dat.set_sa2_current] = monitor.data.values[dat.set_sa2_current] + 1
        #     self.logger.message('SA1 ' + str(monitor.data.values[dat.
        #                         set_sa1_current]) + ' != RA1 ' + str(monitor.data.values[
        #                             dat.get_ra1]), True)
        #     self.logger.message('or SA2 ' + str(monitor.data.values[dat.
        #                         set_sa2_current]) + ' != RA2 ' + str(monitor.data.values[
        #                             dat.get_ra2]), True)
        return r

    def update_bpm_delays(self):
        pass
        # monitor.data.values[dat.get_rd1] = monitor.bpm_control.getRD1(monitor.data.values[dat.bpm_name])
        # monitor.data.values[dat.get_rd2] = monitor.bpm_control.getRD2(monitor.data.values[dat.bpm_name])