# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from controller_base import controller_base
from gui.bpm_attenuation_gui import bpm_attenuation_gui
import data.bpm_attenuation_calibrate_data_base as dat
import sys
import time
from timeit import default_timer as timer


class main_controller(controller_base):
    # whoami
    my_name = 'main_controller'
    #
    # other attributes will be initiliased in base-class

    def __init__(self, argv, config_file):
        controller_base.__init__(self,argv, config_file)
        # start monitoring data
        self.data_monitor.start_monitors()
        # build the gui and pass in the data
        #
        # build the gui
        self.gui = bpm_attenuation_gui()
        self.gui.closing.connect(self.connectCloseEvents)
        self.gui.show()
        self.gui.activateWindow()
        QApplication.processEvents()

        # set up main_loop main states
        self.monitor_states = self.data.main_monitor_states
        QApplication.processEvents()

        # start data recording
        self.data.start_logging()
        QApplication.processEvents()

        # everything now runs from the main_loop
        self.main_loop()

    def main_loop(self):
        self.logger.header(self.my_name + ' BPM attenuation calibration is entering main_loop !',True)

        self.data_monitor.init_monitor_states()
    #     #
        time.sleep(1)
        while 1:
            while 1:
                if controller_base.data.values[dat.ready_to_go]:
                    self.clear_values()
                    controller_base.data.values[dat.scan_status] = 'scanning'
                    self.set_attenuations_and_record()
                    controller_base.data.values[dat.scan_status] = 'complete'
                    break
                else:
                    QApplication.processEvents()

            self.gui.plot_bpm_vs_sa()

            if controller_base.data.values[dat.plots_done]:
                att1_v1_cal = controller_base.data_monitor.bpm_monitor.find_nearest(controller_base.data.values[dat.bpm_v11_v12_sum], 1.0)
                att2_v2_cal = controller_base.data_monitor.bpm_monitor.find_nearest(controller_base.data.values[dat.bpm_v21_v22_sum], 1.0)
                controller_base.data.values[dat.att_1_cal] = att1_v1_cal[0]
                controller_base.data.values[dat.v_1_cal] = att1_v1_cal[1]
                controller_base.data.values[dat.att_2_cal] = att2_v2_cal[0]
                controller_base.data.values[dat.v_2_cal] = att2_v2_cal[1]
                controller_base.data.values[dat.q_cal] = controller_base.data.values[dat.bunch_charge]

            controller_base.data.values[dat.ready_to_go] = False

    def set_attenuations_and_record(self):
        if controller_base.data.values[dat.ready_to_go]:
            print controller_base.data.values[dat.set_sa_start]
            for i in range(controller_base.data.values[dat.set_sa_start], controller_base.data.values[dat.set_sa_end]):
                controller_base.bpm_handler.set_attenuation(controller_base.data.values[dat.bpm_name], i)
                controller_base.data_monitor.bpm_monitor.update_bpm_attenuations()
                if controller_base.data_monitor.bpm_monitor.check_sa_equals_ra():
                    controller_base.data_monitor.bpm_monitor.update_bpm_raw_data()
                    controller_base.data_monitor.scope_monitor.update_bunch_charge()

    def clear_values(self):
        controller_base.data.values[dat.bpm_v11_v12_sum] = {}
        controller_base.data.values[dat.bpm_v21_v22_sum] = {}

    # over load close
    def connectCloseEvents(self):
        self.gui.close()
        sys.exit()

    def set_last_mask_epoch(self):
        self.epoch = time.time()

    def seconds_passed(self,secs):
        return time.time() - self.epoch >= secs
