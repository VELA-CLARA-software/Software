from monitor import monitor
from VELA_CLARA_enums import STATE
from PyQt4.QtCore import QTimer
import data.bpm_attenuation_calibrate_data_base as dat
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

    def update_bpm_raw_data(self):
        if monitor.data.values[dat.bpm_status] and monitor.data.values[dat.scope_status]:
            monitor.data.values[dat.bpm_raw_data] = monitor.bpm_control.getBPMRawDataBuffer(monitor.data.values[dat.bpm_name])
            monitor.data.values[dat.bpm_u11] = monitor.data.values[dat.bpm_raw_data][1]
            monitor.data.values[dat.bpm_u12] = monitor.data.values[dat.bpm_raw_data][2]
            monitor.data.values[dat.bpm_u14] = monitor.data.values[dat.bpm_raw_data][4]
            monitor.data.values[dat.bpm_u21] = monitor.data.values[dat.bpm_raw_data][5]
            monitor.data.values[dat.bpm_u22] = monitor.data.values[dat.bpm_raw_data][6]
            monitor.data.values[dat.bpm_u24] = monitor.data.values[dat.bpm_raw_data][8]
            monitor.data.values[dat.bpm_raw_data_mean_v11] = abs(numpy.mean(monitor.data.values[dat.bpm_u11]) - numpy.mean(monitor.data.values[dat.bpm_u14]))
            monitor.data.values[dat.bpm_raw_data_mean_v12] = abs(numpy.mean(monitor.data.values[dat.bpm_u12]) - numpy.mean(monitor.data.values[dat.bpm_u14]))
            monitor.data.values[dat.bpm_raw_data_mean_v21] = abs(numpy.mean(monitor.data.values[dat.bpm_u21]) - numpy.mean(monitor.data.values[dat.bpm_u24]))
            monitor.data.values[dat.bpm_raw_data_mean_v22] = abs(numpy.mean(monitor.data.values[dat.bpm_u22]) - numpy.mean(monitor.data.values[dat.bpm_u24]))
            monitor.data.values[dat.bpm_v11_v12_sum][monitor.data.values[dat.set_sa1_current]] = (monitor.data.values[dat.bpm_raw_data_mean_v11] + monitor.data.values[dat.bpm_raw_data_mean_v12]) / 2
            monitor.data.values[dat.bpm_v21_v22_sum][monitor.data.values[dat.set_sa2_current]] = (monitor.data.values[dat.bpm_raw_data_mean_v21] + monitor.data.values[dat.bpm_raw_data_mean_v22]) / 2
        else:
            monitor.data.values[dat.bpm_v11_v12_sum][monitor.data.values[dat.set_sa1_current]] = random.uniform(-2,2)
            monitor.data.values[dat.bpm_v21_v22_sum][monitor.data.values[dat.set_sa2_current]] = random.uniform(-2,2)
        # monitor.data.logger.message(monitor.data.values[dat.bpm_name] + ' V11 + V12 for SA1 = ' + str(
        #     monitor.data.values[dat.set_sa1_current]) + ' + = ' + str(monitor.data.values[dat.bpm_v11_v12_sum]), True)
        # monitor.data.logger.message(monitor.data.values[dat.bpm_name] + ' V21 + V22 for SA2 = ' + str(
        #     monitor.data.values[dat.set_sa2_current]) + ' + = ' + str(monitor.data.values[dat.bpm_v21_v22_sum]), True)

    def update_bpm_attenuations(self):
        monitor.data.values[dat.get_ra1] = monitor.bpm_control.getRA1(monitor.data.values[dat.bpm_name])
        monitor.data.values[dat.get_ra2] = monitor.bpm_control.getRA2(monitor.data.values[dat.bpm_name])

    def check_sa_equals_ra(self):
        r = False
        if (monitor.data.values[dat.get_ra1] == monitor.data.values[dat.
                set_sa1_current]
            and monitor.data.values[dat.get_ra2] == monitor.data.values[dat.
                        set_sa2_current]):
            r = True
        else:
            r = True
            monitor.data.values[dat.set_sa1_current] = monitor.data.values[dat.set_sa1_current] + 1
            monitor.data.values[dat.set_sa2_current] = monitor.data.values[dat.set_sa2_current] + 1
            # self.logger.message('SA1 ' + str(monitor.data.values[dat.
            #                     set_sa1_current]) + ' != RA1 ' + str(monitor.data.values[
            #                         dat.get_ra1]), True)
            # self.logger.message('or SA2 ' + str(monitor.data.values[dat.
            #                     set_sa2_current]) + ' != RA2 ' + str(monitor.data.values[
            #                         dat.get_ra2]), True)
        return r

    def find_nearest(self, dict, value):
        # Finds the value for V1 - V2 = 0V for both horizontal and vertical planes
        self.vals = numpy.array(dict.values())
        self.keys = numpy.array(dict.keys())
        self.idx = numpy.abs(self.vals - value).argmin()
        return (self.keys[self.idx], self.vals[self.idx])