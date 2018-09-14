from monitor import monitor
from PyQt4.QtCore import QTimer
import data.blm_plotter_data_base as dat
import numpy, random
import time, collections

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
        monitor.logger.message(self.my_name, ' running')

    def check_blm_is_monitoring(self):
        # PLACEHOLDER
        # blm_data_buffer = monitor.blm_control.getBLMRawDataBuffer(monitor.data.values[dat.bpm_names[0]])
        # if len(blm_data_buffer) > 1:
        #     if blm_data_buffer[-1] != blm_data_buffer[-2]:
        #         monitor.data.values[dat.blm_status] = True
        # else:
        #     monitor.data.values[dat.blm_status] = False
        monitor.data.values[dat.blm_status] = True
        monitor.data.values[dat.blm_distance_start] = 0.0
        monitor.data.values[dat.blm_distance_end] = 1.0
        monitor.data.values[dat.blm_names] = monitor.blm_control.getBLMNames()

    def update_blm_voltages(self):
        # PLACEHOLDER: CHANGE FOR BLM DATA ACQUISITION FUNCTION
        for i in monitor.data.values[dat.blm_names]:
            monitor.data.values[dat.blm_voltages][i].append(numpy.random.rand(1,10)[0])
        monitor.data.values[dat.has_blm_data] = True

    def update_blm_distance(self):
        monitor.data.values[dat.blm_distance_start] = 0
        monitor.data.values[dat.blm_distance_end] = 1
        monitor.data.values[dat.blm_num_values] = numpy.linspace(monitor.data.values[dat.blm_distance_start],monitor.data.values[dat.blm_distance_end],
                                                                 len(monitor.data.values[dat.blm_voltages][monitor.data.values[dat.blm_names][0]][-1]))
        monitor.data.values[dat.has_blm_data] = True

    def check_buffer(self):
        # PLACEHOLDER: REPLACE WITH REAL BLM BUFFER CHECK FUNCTION
        return True