from data_monitors.monitor import monitor
from PyQt5.QtCore import QTimer
import data.charge_measurement_data_base as dat
import numpy, random
import time
import requests
import json

class pil_monitor(monitor):
    # whoami
    my_name = 'pil_monitor'
    set_success = False

    def __init__(self):
        self.my_name = 'pil_monitor'
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
        # monitor.cam_control.startAcquireAndAnalysis_VC()
        monitor.logger.message(self.my_name, ' running')

    def check_set_equals_read(self):
        return True

    def update_vc_values(self, hwp):
        monitor.data.values[dat.vc_x_pix_values][hwp] = monitor.vc_objects[
            monitor.config.vc_config['VC_XPIX']].getBuffer()
        monitor.data.values[dat.vc_y_pix_values][hwp] = monitor.vc_objects[
            monitor.config.vc_config['VC_YPIX']].getBuffer()
        monitor.data.values[dat.vc_sig_x_pix_values][hwp] = monitor.vc_objects[
            monitor.config.vc_config['VC_SIGXPIX']].getBuffer()
        monitor.data.values[dat.vc_sig_y_pix_values][hwp] = monitor.vc_objects[
            monitor.config.vc_config['VC_SIGYPIX']].getBuffer()
        monitor.data.values[dat.vc_intensity_values][hwp] = monitor.vc_objects[
            monitor.config.vc_config['VC_AVGINTENSITY']].getBuffer()

    def get_laser_energy(self, hwp):
        monitor.data.values[dat.ophir_values][hwp] = monitor.las_em_factory.getEnergyBuffer(
            monitor.config.las_em_config['LAS_EM_NAME'])
        if monitor.data.values[dat.charge_mean][-1] > monitor.config.charge_config['MIN_CHARGE_ACCEPTED']:
            monitor.data.values[dat.ophir_mean].append(numpy.mean(list(monitor.data.values[dat.ophir_values][hwp])))
            monitor.data.values[dat.ophir_stderr].append(
                numpy.std(list(monitor.data.values[dat.ophir_values][hwp])) / numpy.sqrt(
                    len(list(monitor.data.values[dat.ophir_values][hwp]))))