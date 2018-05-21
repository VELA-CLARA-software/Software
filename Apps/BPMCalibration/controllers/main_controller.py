# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from controller_base import controller_base
from gui.bpm_calibration_gui import bpm_calibration_gui
import data.bpm_calibrate_data_base as dat
import sys
import time
import numpy
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
        self.gui = bpm_calibration_gui()
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
                    self.logger.bpm_name = controller_base.data.values[dat.bpm_name]
                    self.logger.scan_type = controller_base.data.values[dat.calibration_type]
                    self.logger.get_bpm_scan_log()
                    self.clear_values()
                    controller_base.data.values[dat.scan_status] = 'scanning'
                    if controller_base.data.values[dat.calibration_type] == 'attenuation':
                        self.set_attenuations_and_record()
                        controller_base.data.values[dat.scan_status] = 'complete'
                    elif controller_base.data.values[dat.calibration_type] == 'delay':
                        self.set_delays_and_record()
                        controller_base.data.values[dat.scan_status] = 'complete'
                    break
                else:
                    QApplication.processEvents()

            if controller_base.data.values[dat.calibration_type] == 'attenuation':
                self.gui.plot_bpm_vs_sa()

                if controller_base.data.values[dat.plots_done]:
                    att1_v1_cal = controller_base.data_monitor.bpm_monitor.find_nearest(controller_base.data.values[dat.bpm_v11_v12_sum], 1.0)
                    att2_v2_cal = controller_base.data_monitor.bpm_monitor.find_nearest(controller_base.data.values[dat.bpm_v21_v22_sum], 1.0)
                    controller_base.data.values[dat.att_1_cal] = att1_v1_cal[0]
                    controller_base.data.values[dat.v_1_cal] = att1_v1_cal[1]
                    controller_base.data.values[dat.att_2_cal] = att2_v2_cal[0]
                    controller_base.data.values[dat.v_2_cal] = att2_v2_cal[1]
                    controller_base.data.values[dat.q_cal] = controller_base.data.values[dat.bunch_charge]
                    controller_base.bpm_handler.set_sa1(controller_base.data.values[dat.bpm_name],
                                                        controller_base.data.values[dat.att_1_cal])
                    controller_base.bpm_handler.set_sa2(controller_base.data.values[dat.bpm_name],
                                                        controller_base.data.values[dat.att_2_cal])
                    self.json_data = {"bpm_name": self.data.values[dat.bpm_name],
                                      "bpm_v11_v12_sum": self.data.values[dat.bpm_v11_v12_sum],
                                      "bpm_v21_v22_sum": self.data.values[dat.bpm_v21_v22_sum],
                                      "att_1_cal": self.data.values[dat.att_1_cal],
                                      "v_1_cal": self.data.values[dat.v_1_cal],
                                      "att_2_cal": self.data.values[dat.att_2_cal],
                                      "v_2_cal": self.data.values[dat.v_2_cal],
                                      "q_cal": self.data.values[dat.q_cal]}
                    self.logger.add_to_bpm_scan_json(self.json_data)

            elif controller_base.data.values[dat.calibration_type] == 'delay':
                self.gui.plot_bpm_vs_sd()

                self.json_data = {"bpm_name": self.data.values[dat.bpm_name],
                             "dv1_dly1_min_val": self.data.values[dat.dv1_dly1_min_val],
                             "dv2_dly1_min_val": self.data.values[dat.dv2_dly1_min_val],
                             "dv1_dly2_min_val": self.data.values[dat.dv1_dly2_min_val],
                             "dv2_dly2_min_val": self.data.values[dat.dv2_dly2_min_val],
                             "dv1_dly1": self.data.values[dat.dv1_dly1],
                             "dv2_dly1": self.data.values[dat.dv2_dly1],
                             "dv1_dly2": self.data.values[dat.dv1_dly2],
                             "dv2_dly2": self.data.values[dat.dv2_dly2]}
                self.logger.add_to_bpm_scan_json(self.json_data)

            controller_base.data.values[dat.ready_to_go] = False

    def set_attenuations_and_record(self):
        if controller_base.data.values[dat.ready_to_go]:
            controller_base.bpm_handler.set_bpm_buffer(controller_base.data.values[dat.num_shots])
            for i in range(controller_base.data.values[dat.set_start], controller_base.data.values[dat.set_end]):
                controller_base.bpm_handler.set_attenuation(controller_base.data.values[dat.bpm_name], i)
                time.sleep(1)
                controller_base.data_monitor.bpm_monitor.update_bpm_attenuations()
                if controller_base.data_monitor.bpm_monitor.check_sa_equals_ra():
                    # controller_base.data_monitor.bpm_monitor.update_bpm_raw_data()
                    time.sleep(1)
                    QApplication.processEvents()
                    controller_base.data_monitor.bpm_monitor.update_bpm_voltages()
                    controller_base.data_monitor.charge_monitor.update_bunch_charge()
                    controller_base.bpm_handler.update_bpm_att_voltages()

    def set_delays_and_record(self):
        if controller_base.data.values[dat.ready_to_go]:
            for i in range(controller_base.data.values[dat.set_start],
                           controller_base.data.values[dat.set_end]):
                time.sleep(1)
                QApplication.processEvents()
                controller_base.data_monitor.bpm_monitor.update_bpm_voltages()
                controller_base.bpm_handler.scan_dly(i)
                controller_base.data_monitor.charge_monitor.update_bunch_charge()
            controller_base.bpm_handler.find_min_dly_1()
            controller_base.bpm_handler.find_min_dly_2()

    # def set_delays_and_record(self):
    #     if controller_base.data.values[dat.ready_to_go]:
    #         for i in range(controller_base.data.values[dat.set_start], controller_base.data.values[dat.set_end]):
    #             controller_base.bpm_handler.set_bpm_buffer(controller_base.data.values[dat.num_shots])
    #             time.sleep(1)
    #             QApplication.processEvents()
    #             controller_base.data_monitor.bpm_monitor.update_bpm_voltages()
    #             controller_base.bpm_handler.scan_dly1(i)
    #             controller_base.data_monitor.charge_monitor.update_bunch_charge()
    #         controller_base.bpm_handler.find_min_dly_1()
    #         if controller_base.data.values[dat.new_dly_1_set]:
    #             for i in range(controller_base.data.values[dat.new_dly_1] - 20, controller_base.data.values[dat.new_dly_1] + 20):
    #                 controller_base.bpm_handler.set_bpm_buffer(controller_base.data.values[dat.num_shots])
    #                 time.sleep(1)
    #                 QApplication.processEvents()
    #                 controller_base.data_monitor.bpm_monitor.update_bpm_voltages()
    #                 controller_base.bpm_handler.scan_dly2(i)
    #                 controller_base.data_monitor.charge_monitor.update_bunch_charge()
    #             controller_base.bpm_handler.find_min_dly_2()

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
