# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from controller_base import controller_base
from gui.blm_plotter_gui import blm_plotter_gui
import data.blm_plotter_data_base as dat
import sys
import time
import numpy
from timeit import default_timer as timer


class main_controller(controller_base):
    # whoami
    my_name = 'main_controller'
    #
    # other attributes will be initiliased in base-class

    def __init__(self, argv, machine_mode, machine_area):
        controller_base.__init__(self,argv, machine_mode, machine_area)
        # start monitoring data
        self.data_monitor.start_monitors()
        # build the gui and pass in the data
        #
        # build the gui
        self.gui = blm_plotter_gui()
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
                    self.logger.get_blm_scan_log()
                    self.clear_values()
                    self.get_charge_values()
                    self.get_blm_values()
                    break
                else:
                    QApplication.processEvents()

            if controller_base.data.values[dat.has_blm_data]:
                self.gui.plot_blm_values()

    def get_blm_values(self):
        controller_base.blm_handler.set_blm_buffer(controller_base.data.values[dat.num_shots])
        controller_base.data_monitor.blm_monitor.update_blm_voltages()
        QApplication.processEvents()

    def get_charge_values(self):
        controller_base.data_monitor.charge_monitor.update_bunch_charge()
        QApplication.processEvents()

    def clear_values(self):
        controller_base.data.values[dat.blm_values] = {}
        controller_base.data.values[dat.charge_values] = []

    # over load close
    def connectCloseEvents(self):
        self.gui.close()
        sys.exit()

    def set_last_mask_epoch(self):
        self.epoch = time.time()

    def seconds_passed(self,secs):
        return time.time() - self.epoch >= secs
