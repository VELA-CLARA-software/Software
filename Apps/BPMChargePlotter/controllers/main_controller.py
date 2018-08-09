# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from controller_base import controller_base
from gui.bpm_charge_gui import bpm_charge_plotter_gui
import data.bpm_charge_plotter_data_base as dat
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
        self.gui = bpm_charge_plotter_gui()
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
                    for i in controller_base.data.values[dat.bpm_names]:
                        controller_base.data_monitor.bpm_monitor.update_bpm_charge(i)
                    controller_base.data_monitor.charge_monitor.update_bunch_charge()
                    QApplication.processEvents()
                else:
                    QApplication.processEvents()

                if controller_base.data.values[dat.recalibrate_go]:
                    controller_base.bpm_handler.recalibrate_attenuation()

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
