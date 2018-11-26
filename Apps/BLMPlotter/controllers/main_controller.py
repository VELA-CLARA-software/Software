# THE main_controller
# holds everything
from PyQt4.QtGui import QApplication
from controller_base import controller_base
from gui.blm_plotter_gui import blm_plotter_gui
import data.blm_plotter_data_base as dat
import sys,os
import time
from logs.dict_to_h5 import save_dict_to_hdf5
import numpy, os, datetime
from timeit import default_timer as timer


class main_controller(controller_base):
    # whoami
    my_name = 'main_controller'
    #
    # other attributes will be initiliased in base-class

    def __init__(self, argv, machine_mode, machine_area, blm_name):
        controller_base.__init__(self,argv, machine_mode, machine_area)
        # start monitoring data
        self.data_monitor.start_monitors()
        self.blm_name = blm_name
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
        self.logger.header(self.my_name + ' BLM plotter GUI is entering main_loop !',True)
        controller_base.data.values[dat.blm_name] = self.blm_name
        controller_base.data.values[dat.ready_to_go] = self.data_monitor.init_monitor_states()
        controller_base.blm_handler.set_blm_buffer(controller_base.data.values[dat.num_shots])
        controller_base.blm_handler.get_noise_data()
        controller_base.blm_handler.get_single_photon_data()
        controller_base.data_monitor.blm_monitor.check_blm_is_monitoring()
        self.blm_scan_log = self.logger.get_blm_scan_log()
    #     #
        time.sleep(1)
        while 1:
            while 1:
                if controller_base.data.values[dat.ready_to_go]:
                    if controller_base.data.values[dat.num_shots_request]:
                        self.clear_values()
                        controller_base.blm_handler.set_blm_buffer(controller_base.data.values[dat.num_shots])
                        controller_base.charge_handler.set_charge_buffer(controller_base.data.values[dat.num_shots])
                        controller_base.data.values[dat.num_shots_request] = False
                        time.sleep(0.1)
                        # while controller_base.data.values[dat.buffers_full] == False:
                    controller_base.data.values[dat.has_blm_data] = False
                    self.check_buffers()
                    self.get_charge_values()
                    self.get_blm_values()
                    if controller_base.data.values[dat.calibrate_request]:
                        controller_base.blm_handler.calibrate_blm()
                        self.get_blm_buffer()
                        self.str_to_pv_1 = controller_base.data.values[dat.str_to_pv][
                            controller_base.data.values[dat.calibrate_channel_names][0]]
                        self.str_to_pv_2 = controller_base.data.values[dat.str_to_pv][
                            controller_base.data.values[dat.calibrate_channel_names][1]]
                        self.blm_voltages = {self.str_to_pv_1: controller_base.data.values[dat.blm_voltages][self.str_to_pv_1],
                                             self.str_to_pv_2: controller_base.data.values[dat.blm_voltages][self.str_to_pv_2]}
                        self.time_stamps = {self.str_to_pv_1: controller_base.data.values[dat.time_stamps][self.str_to_pv_1],
                                             self.str_to_pv_2: controller_base.data.values[dat.time_stamps][self.str_to_pv_2]}
                        self.data = {"calibrate_channel_names": controller_base.data.values[dat.calibrate_channel_names],
                                     "delta_x": controller_base.data.values[dat.delta_x],
                                     "calibration_time": controller_base.data.values[dat.calibration_time],
                                     "blm_voltages": self.blm_voltages,
                                     "chg_data": controller_base.data.values[dat.charge_values],
                                     "filter_applied": controller_base.data.values[dat.apply_filter],
                                     "filter_size": controller_base.data.values[dat.blackman_size],
                                     "time_stamps": self.time_stamps
                                     }
                        self.writetohdf5(filename=self.calibratefilename([self.str_to_pv_1,self.str_to_pv_2]), data=self.data)
                        controller_base.data.values[dat.calibrate_request] = False
                    break
                else:
                    QApplication.processEvents()

            if controller_base.data.values[dat.has_blm_data]:
                self.gui.plot_blm_values()

            if controller_base.data.values[dat.save_request]:
                self.blm_scan_log = self.logger.get_blm_scan_log()[0]
                self.get_blm_buffer()
                self.voltages = {}
                if controller_base.data.values[dat.apply_filter]:
                    for i in controller_base.data.values[dat.blm_waveform_pvs]:
                        controller_base.data.values[dat.blm_voltages][str(i)] = \
                            controller_base.data.values[dat.blm_voltages][str(i)] * abs(
                                controller_base.data.values[dat.deconvolution_filter])
                else:
                    for i, j in zip(controller_base.data.values[dat.blm_waveform_pvs],controller_base.data.values[dat.blm_time_pvs]):
                        self.voltages[str(i)] = controller_base.data.values[dat.blm_voltages][str(i)]
                        self.voltages[str(j)] = controller_base.data.values[dat.blm_time][str(j)]
                self.data = {"chg_data": controller_base.data.values[dat.charge_values],
                             "blm_voltages": controller_base.data.values[dat.blm_buffer],#self.voltages,
                             "filter_applied": controller_base.data.values[dat.apply_filter],
                             "filter_size": controller_base.data.values[dat.blackman_size],
                             "calibrate_channel_names": controller_base.data.values[dat.calibrate_channel_names],
                             "delta_x": controller_base.data.values[dat.delta_x],
                             "calibration_time": controller_base.data.values[dat.calibration_time],
                             "time_stamps": controller_base.data.values[dat.time_stamps]
                             }
                self.writetohdf5(filename=self.blm_scan_log,data=self.data)
                controller_base.data.values[dat.save_request] = False
                controller_base.data.values[dat.buffer_message] = ""

    def writetohdf5(self, filename=None, data=None):
        self.data = data
        self.filename = filename
        self.fullname = self.filename
        save_dict_to_hdf5(self.data, self.fullname)

    def setfilename(self, filename=None, directory=None):
        self.filename = filename
        self.directory = directory
        self.timestamp = time.time()
        self.st = datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d-%H-%M-%S')
        self.now = datetime.datetime.now()
        if self.filename == None:
            self.filename = "blm_scan-" + self.st
        return self.filename

    def calibratefilename(self, channelnames=None):
        self.channelnames = channelnames
        self.timestamp = time.time()
        self.st = datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d-%H-%M-%S')
        self.now = datetime.datetime.now()
        self.filename = self.logger.get_blm_scan_log()[1] + str(self.channelnames[0]) + "_" + str(self.channelnames[1]) + self.st + ".hdf5"
        return self.filename

    def get_blm_values(self):
        controller_base.data_monitor.blm_monitor.update_blm_voltages()
        controller_base.data_monitor.blm_monitor.update_blm_distance()
        if controller_base.data.values[dat.apply_filter]:
            for i in controller_base.data.values[dat.blm_waveform_pvs]:
                if not controller_base.data.values[dat.has_sparsified]:
                    controller_base.data.values[dat.noise_data] = controller_base.blm_handler.sparsify_list(controller_base.data.values[dat.all_noise_data][i],
                                                                                                            controller_base.data.values[dat.blm_voltages][str(i)])
                    controller_base.data.values[dat.single_photon_data] = controller_base.blm_handler.sparsify_list(controller_base.data.values[dat.all_single_photon_data][i],
                                                                                                                    controller_base.data.values[dat.blm_voltages][str(i)])
                controller_base.blm_handler.deconvolution_filter(controller_base.data.values[dat.noise_data],controller_base.data.values[dat.single_photon_data])
                controller_base.blm_handler.set_filters()
        QApplication.processEvents()

    def get_charge_values(self):
        controller_base.data_monitor.charge_monitor.update_bunch_charge()
        QApplication.processEvents()

    def get_blm_buffer(self):
        controller_base.data_monitor.blm_monitor.update_blm_buffer()
        QApplication.processEvents()

    def check_buffers(self):
        if controller_base.data_monitor.charge_monitor.check_buffer() == True and controller_base.data_monitor.blm_monitor.check_buffer() == True:
            controller_base.data.values[dat.buffers_full] = True

    def clear_values(self):
        controller_base.data.values[dat.blm_voltages] = {}
        for i in controller_base.data.values[dat.blm_waveform_pvs]:
            controller_base.data.values[dat.blm_voltages][i] = []
        for i in controller_base.data.values[dat.blm_time_pvs]:
            controller_base.data.values[dat.blm_time][i] = []
        controller_base.data.values[dat.charge_values] = []

    # over load close
    def connectCloseEvents(self):
        self.gui.close()
        sys.exit()

    def set_last_mask_epoch(self):
        self.epoch = time.time()

    def seconds_passed(self,secs):
        return time.time() - self.epoch >= secs
