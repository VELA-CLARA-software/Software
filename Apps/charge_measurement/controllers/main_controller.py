# THE main_controller
# holds everything
from PyQt5.QtWidgets import QApplication
from controllers.controller_base import controller_base
from gui.charge_measurement_gui import charge_measurement_gui
import data.charge_measurement_data_base as dat
import sys
import time
import numpy
import datetime

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
        self.gui = charge_measurement_gui()
        self.gui.closing.connect(self.connectCloseEvents)
        self.gui.show()
        self.gui.activateWindow()
        #QApplication.processEvents()

        # set up main_loop main states
        self.monitor_states = self.data.main_monitor_states
        #QApplication.processEvents()

        # start data recording
        self.data.start_logging()
        #QApplication.processEvents()

        # everything now runs from the main_loop
        self.main_loop()

    def main_loop(self):
        self.logger.header(self.my_name + ' charge measurement is entering main_loop !',True)

        self.data_monitor.init_monitor_states()
        self.fitdone = False
    #     #
        time.sleep(1)

        while 1:
            if controller_base.data.values[dat.ready_to_go]:
                self.logger.pil_name = controller_base.data.values[dat.pil_name]
                self.logger.measurement_type = controller_base.data.values[dat.measurement_type]
                self.logger.get_scan_log()
                self.clear_values()
                controller_base.data.values[dat.scan_status] = 'scanning'
                controller_base.data.values[dat.measurement_type] = "wcm_vs_ophir"
                if controller_base.data.values[dat.measurement_type] == 'wcm_vs_ophir':
                    self.fitdone = False
                    # controller_base.llrf_handler.enable_rf_output()
                    self.set_hwp_and_record()
                    controller_base.data.values[dat.scan_status] = 'complete'
                    controller_base.data.values[dat.ready_to_go] = False
                    self.gui.scanButton.setEnabled(True)
                    self.gui.messageLabel.setText('Scan complete')
                    self.gui.scanButton.setText("Scan laser attenuator")
                    self.gui.newVals.setEnabled(True)
            else:
                QApplication.processEvents()

            if controller_base.data.values[dat.scan_status] == "complete":
                controller_base.data.values[dat.plots_done] = True
                self.calculate_fit()
                self.gui.plot_fit()
                # self.gui.set_results_label()
                self.gui.saveButton.setEnabled(True)
                self.fitdone = True

            if controller_base.data.values[dat.save_clicked]:
                self.json_data = {"pil_name": self.data.values[dat.pil_name],
                                  "comments": self.data.values[dat.comments],
                                  "vc_intensity_mean": self.data.values[dat.vc_intensity_mean],
                                  "vc_intensity_stderr": self.data.values[dat.vc_intensity_stderr],
                                  "vc_x_pix_mean": self.data.values[dat.vc_x_pix_mean],
                                  "vc_x_pix_stderr": self.data.values[dat.vc_x_pix_stderr],
                                  "vc_y_pix_mean": self.data.values[dat.vc_y_pix_mean],
                                  "vc_y_pix_stderr": self.data.values[dat.vc_y_pix_stderr],
                                  "vc_sig_x_pix_mean": self.data.values[dat.vc_sig_x_pix_mean],
                                  "vc_sig_x_pix_stderr": self.data.values[dat.vc_sig_x_pix_stderr],
                                  "vc_sig_y_pix_mean": self.data.values[dat.vc_sig_y_pix_mean],
                                  "vc_sig_y_pix_stderr": self.data.values[dat.vc_sig_y_pix_stderr],
                                  "charge_values": self.data.values[dat.charge_values],
                                  "charge_mean": self.data.values[dat.charge_mean],
                                  "charge_stderr": self.data.values[dat.charge_stderr],
                                  "ophir_values": self.data.values[dat.ophir_values],
                                  "ophir_mean": self.data.values[dat.ophir_mean],
                                  "ophir_stderr": self.data.values[dat.ophir_stderr],
                                  "fit": self.data.values[dat.fit],
                                  "cross": self.data.values[dat.cross],
                                  "qe": self.data.values[dat.qe],
                                  "kly_fwd_pwr_mean": self.data.values[dat.kly_fwd_pwr_mean],
                                  "kly_fwd_pwr_stderr": self.data.values[dat.kly_fwd_pwr_stderr],
                                  "gun_fwd_pwr_mean": self.data.values[dat.gun_fwd_pwr_mean],
                                  "gun_fwd_pwr_stderr": self.data.values[dat.gun_fwd_pwr_stderr],
                                  "gun_pha_sp_mean": self.data.values[dat.gun_pha_sp_mean],
                                  "gun_pha_sp_stderr": self.data.values[dat.gun_pha_sp_stderr],
                                  "gun_pha_ff_mean": self.data.values[dat.gun_pha_ff_mean],
                                  "gun_pha_ff_stderr": self.data.values[dat.gun_pha_ff_stderr],
                                  "off_crest_phase_dict": self.data.values[dat.off_crest_phase_dict],
                                  "sol_values": self.data.values[dat.sol_values],
                                  "bsol_values": self.data.values[dat.bsol_values],
                                  "kly_fwd_pwr_values": self.data.values[dat.kly_fwd_pwr_values],
                                  "kly_sp_time_stamp": self.data.values[dat.kly_sp_time_stamp],
                                  "kly_fwd_pwr_time_stamp": self.data.values[dat.kly_fwd_pwr_time_stamp],
                                  "off_crest_phase": self.data.values[dat.off_crest_phase_dict],
                                  "vc_image_name": self.data.values[dat.vc_image_name],
                                  "vc_image_directory": self.data.values[dat.vc_image_directory]
                                  }
                self.filename = self.logger.add_to_scan_json(self.json_data)
                controller_base.data.values[dat.file_names].append(self.filename)
                self.logger.message('Data saved to' + self.filename, True)
                controller_base.data.values[dat.save_clicked] = False
                controller_base.data.values[dat.scan_status] = "incomplete"
                self.gui.saveButton.setEnabled(False)
            controller_base.data.values[dat.plots_done] = False

    def set_hwp_and_record(self):
        if controller_base.data.values[dat.ready_to_go]:
            controller_base.data.values[dat.first_measurement] = True
            if controller_base.shutter_handler.is_shutter_closed():
                controller_base.shutter_handler.open_shutter()
                time.sleep(1)
            self.logger.message('entering set_hwp_and_record', True)
            self.laser_energy_range = controller_base.pil_handler.set_laser_energy_range(3)
            self.stepprog = (controller_base.data.values[dat.set_hwp_end] - controller_base.data.values[
                dat.set_hwp_start]) / controller_base.data.values[dat.num_steps]
            self.stepspace = numpy.linspace(0,self.stepprog,controller_base.data.values[dat.num_steps])
            self.iterate = 0
            self.hwp_start = controller_base.pil_handler.get_hwp()
            self.has_been_overrange = False
            self.hwp_settings = numpy.linspace(controller_base.data.values[dat.set_hwp_start],
                                    controller_base.data.values[dat.set_hwp_end],
                                    controller_base.data.values[dat.num_steps])
            for i in range(0, len(self.hwp_settings)-1):
                if controller_base.data.values[dat.cancel]:
                    self.clear_values()
                    controller_base.data.values[dat.cancel] = False
                    break
                controller_base.data.values[dat.data_point_success].update({self.hwp_settings[i]: False})
                self.logger.message('Setting HWP to '+str(self.hwp_settings[i]), True)
                self.gui.progressBar.setValue(self.stepspace[self.iterate]*100)
                self.iterate +=1
                controller_base.data.values[dat.hwp_values].append(self.hwp_settings[i])
                controller_base.pil_handler.set_hwp(self.hwp_settings[i])
                time.sleep(1)
                while not controller_base.data.values[dat.data_point_success][self.hwp_settings[i]]:
                    if controller_base.data_monitor.pil_monitor.check_set_equals_read():
                        while controller_base.pil_handler.get_laser_energy_overrange():
                            time.sleep(1)
                            self.range = controller_base.pil_handler.get_laser_energy_range()
                            time.sleep(1)
                            self.laser_energy_range = controller_base.pil_handler.set_laser_energy_range(self.range-1)
                            time.sleep(1)
                            self.has_been_overrange = True
                            controller_base.shutter_handler.open_shutter()
                            time.sleep(1)
                    #time.sleep(1)
                    QApplication.processEvents()
                    # if not self.has_been_overrange:
                    if controller_base.shutter_handler.is_shutter_closed():
                        controller_base.shutter_handler.open_shutter()
                        time.sleep(1)
                    if controller_base.shutter_handler.is_shutter_open():
                        controller_base.pil_handler.set_pil_buffer(controller_base.data.values[dat.num_shots])
                        controller_base.pil_handler.set_vc_buffer(controller_base.data.values[dat.num_shots])
                        controller_base.charge_handler.set_charge_buffer(controller_base.data.values[dat.num_shots])
                        # controller_base.llrf_handler.enable_rf_output()
                        controller_base.llrf_handler.set_llrf_buffer(controller_base.data.values[dat.num_shots])
                        self.time_flo = datetime.datetime.now() + datetime.timedelta(seconds=3) + datetime.timedelta(
                            seconds=controller_base.data.values[dat.num_shots] / 10)
                        # while datetime.datetime.now() < self.time_flo:
                        while not controller_base.data_monitor.pil_monitor.is_energy_buffer_full():
                            QApplication.processEvents()
                            time.sleep(0.1)
                        if not controller_base.data.values[dat.first_measurement]:
                            self.hwp_prev = self.hwp_settings[i - 1]
                        else:
                            self.hwp_prev = None
                        self.success = controller_base.data_monitor.charge_monitor.update_charge_values(
                            self.hwp_settings[i],
                            self.hwp_prev)
                        if self.success:
                            controller_base.data_monitor.mag_monitor.update_mag_values(self.hwp_settings[i])
                            controller_base.data_monitor.pil_monitor.update_vc_values(self.hwp_settings[i])
                            controller_base.data_monitor.llrf_monitor.update_rf_values(self.hwp_settings[i])
                            controller_base.data_monitor.pil_monitor.get_laser_energy(self.hwp_settings[i])
                            controller_base.data.values[dat.data_point_success][self.hwp_settings[i]] = True
                        controller_base.data.values[dat.first_measurement] = False
                        self.gui.update_plot()
                        QApplication.processEvents()
                        self.has_been_overrange = False
                    else:
                        self.logger.message('Shutter not open!!!!!!!!!!!!!!!!!!!!', True)
                # else:
                #     self.has_been_overrange = False
            self.gui.progressBar.setValue(100)
            # controller_base.llrf_handler.disable_rf_output()
            controller_base.pil_handler.set_hwp(self.hwp_start)

    def clear_values(self):
        controller_base.data.values[dat.charge_mean] = {}
        controller_base.data.values[dat.ophir_mean] = {}
        controller_base.data.values[dat.charge_stderr] = {}
        controller_base.data.values[dat.ophir_stderr] = {}
        controller_base.data.values[dat.charge_values] = {}
        controller_base.data.values[dat.ophir_values] = {}
        controller_base.data.values[dat.kly_fwd_pwr_values] = {}
        controller_base.data.values[dat.gun_fwd_pwr_values] = {}
        controller_base.data.values[dat.gun_pha_sp_values] = {}
        controller_base.data.values[dat.gun_pha_ff_values] = {}
        controller_base.data.values[dat.kly_fwd_pwr_mean] = {}
        controller_base.data.values[dat.gun_fwd_pwr_mean] = {}
        controller_base.data.values[dat.gun_pha_sp_mean] = {}
        controller_base.data.values[dat.gun_pha_ff_mean] = {}
        controller_base.data.values[dat.kly_fwd_pwr_stderr] = {}
        controller_base.data.values[dat.gun_fwd_pwr_stderr] = {}
        controller_base.data.values[dat.gun_pha_sp_stderr] = {}
        controller_base.data.values[dat.gun_pha_ff_stderr] = {}
        controller_base.data.values[dat.gun_pha_ff_lock_values] = {}
        controller_base.data.values[dat.vc_intensity_values] = {}
        controller_base.data.values[dat.vc_x_pix_values] = {}
        controller_base.data.values[dat.vc_y_pix_values] = {}
        controller_base.data.values[dat.vc_sig_x_pix_values] = {}
        controller_base.data.values[dat.vc_sig_y_pix_values] = {}
        controller_base.data.values[dat.vc_intensity_mean] = {}
        controller_base.data.values[dat.vc_x_pix_mean] = {}
        controller_base.data.values[dat.vc_y_pix_mean] = {}
        controller_base.data.values[dat.vc_sig_x_pix_mean] = {}
        controller_base.data.values[dat.vc_sig_y_pix_mean] = {}
        controller_base.data.values[dat.vc_intensity_stderr] = {}
        controller_base.data.values[dat.vc_x_pix_stderr] = {}
        controller_base.data.values[dat.vc_y_pix_stderr] = {}
        controller_base.data.values[dat.vc_sig_x_pix_stderr] = {}
        controller_base.data.values[dat.vc_sig_y_pix_stderr] = {}
        controller_base.data.values[dat.sol_values] = {}
        controller_base.data.values[dat.bsol_values] = {}
        controller_base.data.values[dat.charge_time_stamp] = {}
        controller_base.data.values[dat.ophir_time_stamp] = {}
        controller_base.data.values[dat.gun_fwd_pwr_mean_time_stamp] = {}
        controller_base.data.values[dat.gun_fwd_pha_mean_time_stamp] = {}
        controller_base.data.values[dat.kly_fwd_pwr_time_stamp] = {}
        controller_base.data.values[dat.kly_sp_time_stamp] = {}
        controller_base.data.values[dat.vc_intensity_time_stamp] = {}
        controller_base.data.values[dat.vc_x_pix_time_stamp] = {}
        controller_base.data.values[dat.vc_y_pix_time_stamp] = {}
        controller_base.data.values[dat.vc_sig_x_pix_time_stamp] = {}
        controller_base.data.values[dat.vc_sig_y_pix_time_stamp] = {}
        controller_base.data.values[dat.off_crest_phase_dict] = {}
        controller_base.data.values[dat.vc_image_name] = {}
        controller_base.data.values[dat.vc_image_directory] = {}

    def calculate_fit(self):
        if self.fitdone == False:
            self.wcmmean = []
            self.ophirmean = []
            self.wcmstderr = []
            self.ophirstderr = []
            self.wcmmeanall = []
            self.ophirmeanall = []
            self.wcmstderrall = []
            self.ophirstderrall = []
            self.x, self.y = list(controller_base.data.values[dat.ophir_mean].values()), list(
                controller_base.data.values[dat.charge_mean].values())
            try:
                self.m, self.c = numpy.around(numpy.polyfit(self.x, self.y, 1), 2)
            except:
                self.m, self.c = 0, 0
            self.fit = self.m
            self.cross = self.c
            self.QE = numpy.around(4.66e-6 * self.m / 15.4, 6)
            self.qeall = self.QE
            controller_base.data.values[dat.fit] = self.fit
            controller_base.data.values[dat.cross] = self.cross
            controller_base.data.values[dat.qe] = self.qeall
            return self.fit, self.cross, self.qeall

    # over load close
    def connectCloseEvents(self):
        self.gui.close()
        sys.exit()

    def set_last_mask_epoch(self):
        self.epoch = time.time()

    def seconds_passed(self,secs):
        return time.time() - self.epoch >= secs
