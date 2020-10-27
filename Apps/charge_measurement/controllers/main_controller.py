# THE main_controller
# holds everything
import os
import sys
from PyQt5.QtWidgets import QApplication
from controllers.controller_base import controller_base
from gui.charge_measurement_gui import charge_measurement_gui
import data.charge_measurement_data_base as dat
import sys
import time
import numpy
import datetime
import shutil
import pyqtgraph.exporters
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
                    controller_base.llrf_handler.enable_rf_output()
                    self.set_hwp_and_record()
                    controller_base.llrf_handler.disable_rf_output()
                    controller_base.data.values[dat.scan_status] = 'complete'
            else:
                QApplication.processEvents()

            if controller_base.data.values[dat.measurement_type] == 'wcm_vs_ophir' and controller_base.data.values[dat.scan_status] == "complete":
                self.plot = self.gui.plot_wcm_vs_ophir()

            if controller_base.data.values[dat.plots_done]:
                self.json_data = {"pil_name": self.data.values[dat.pil_name],
                                  "comments": self.data.values[dat.comments],
                                  "measurement_type": self.data.values[dat.measurement_type],
                                  "time_stamp": self.data.values[dat.time_stamp],
                                  "charge_time_stamp": self.data.values[dat.charge_time_stamp],
                                  "ophir_time_stamp": self.data.values[dat.ophir_time_stamp],
                                  "gun_fwd_pwr_mean_time_stamp": self.data.values[dat.gun_fwd_pwr_mean_time_stamp],
                                  "gun_fwd_pha_mean_time_stamp": self.data.values[dat.gun_fwd_pha_mean_time_stamp],
                                  "vc_intensity_time_stamp": self.data.values[dat.vc_intensity_time_stamp],
                                  "vc_x_pix_time_stamp": self.data.values[dat.vc_x_pix_time_stamp],
                                  "vc_y_pix_time_stamp": self.data.values[dat.vc_y_pix_time_stamp],
                                  "vc_sig_x_pix_time_stamp": self.data.values[dat.vc_sig_x_pix_time_stamp],
                                  "vc_sig_y_pix_time_stamp": self.data.values[dat.vc_sig_y_pix_time_stamp],
                                  "charge_values": self.data.values[dat.charge_values],
                                  "ophir_values": self.data.values[dat.ophir_values],
                                  "gun_fwd_pwr_trace_mean": self.data.values[dat.gun_fwd_pwr_trace_mean],
                                  "gun_fwd_pha_trace_mean": self.data.values[dat.gun_fwd_pha_trace_mean],
                                  "gun_fwd_pwr_traces": self.data.values[dat.gun_fwd_pwr_traces],
                                  "gun_fwd_pha_traces": self.data.values[dat.gun_fwd_pha_traces],
                                  "kly_fwd_pwr_trace_mean": self.data.values[dat.kly_fwd_pwr_trace_mean],
                                  "kly_fwd_pha_trace_mean": self.data.values[dat.kly_fwd_pha_trace_mean],
                                  "kly_fwd_pwr_traces": self.data.values[dat.kly_fwd_pwr_traces],
                                  "kly_fwd_pha_traces": self.data.values[dat.kly_fwd_pha_traces],
                                  "vc_intensity_values": self.data.values[dat.vc_intensity_values],
                                  "vc_x_pix_values": self.data.values[dat.vc_x_pix_values],
                                  "vc_y_pix_values": self.data.values[dat.vc_y_pix_values],
                                  "vc_sig_x_pix_values": self.data.values[dat.vc_sig_x_pix_values],
                                  "vc_sig_y_pix_values": self.data.values[dat.vc_sig_y_pix_values],
                                  "hwp_values": self.data.values[dat.hwp_values],
                                  "sol_values": self.data.values[dat.sol_values],
                                  "bsol_values": self.data.values[dat.bsol_values],
                                  "kly_sp_values": self.data.values[dat.kly_sp_values],
                                  "kly_fwd_pwr_values": self.data.values[dat.kly_fwd_pwr_values],
                                  "kly_sp_time_stamp": self.data.values[dat.kly_sp_time_stamp],
                                  "kly_fwd_pwr_time_stamp": self.data.values[dat.kly_fwd_pwr_time_stamp],
                                  "off_crest_phase": self.data.values[dat.off_crest_phase_dict],
                                  "vc_image_name": self.data.values[dat.vc_image_name],
                                  "vc_image_directory": self.data.values[dat.vc_image_directory]
                                  }
                if not controller_base.data.values[dat.data_written]:
                    self.logger.message('Scan complete', True)
                    self.m, self.cross, self.qe, self.filename = self.logger.add_to_scan_json(self.json_data)
                    controller_base.data.values[dat.file_names].append(self.filename)
                    controller_base.data.values[dat.data_written] = True
                    self.logger.message('Data saved to' + self.filename, True)
                    self.gui.set_results_label(self.m, self.cross, self.qe)
                    # self.gui.legend.addItem(self.gui.plot, "fit = "+ self.data.values[dat.fit] + " x + " + self.data.values[dat.cross] +
                    #                              "; QE = " + self.data.values[dat.qe] + "; kly_fwd_pwr = " +
                    #                              self.data.values[dat.kly_fwd_mean_all])
                    # self.exporter = pyqtgraph.exporters.ImageExporter(self.gui.plot)
                    # self.exporter.export(str(os.path.split(self.filename)[1])[0:-5]+".png")
                    # self.exporter.export("\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\Measurements\\Charge_Measurements\\"+os.path.split(self.filename)[1]+".png")
                    # self.year = str(datetime.datetime.now().year)
                    # self.month = datetime.datetime.now().strftime('%m')
                    # self.day = datetime.datetime.now().strftime('%d')
                    # self.scandir =  "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\"+self.year+"\\"+self.month+"\\"+self.day
                    # if not os.path.isdir(self.scandir):
                    #     os.makedirs(self.scandir)
                    # shutil.copyfile(self.filename,self.scandir)
                    # self.exporter.export(self.scandir+os.path.split(self.filename)[1]+".png")
            controller_base.data.values[dat.plots_done] = False

    def set_hwp_and_record(self):
        if controller_base.data.values[dat.ready_to_go]:
            self.logger.message('entering set_hwp_and_record', True)
            self.laser_energy_range = controller_base.pil_handler.set_laser_energy_range(3)
            controller_base.pil_handler.set_pil_buffer(controller_base.data.values[dat.num_shots])
            controller_base.llrf_handler.enable_rf_output()
            controller_base.llrf_handler.set_llrf_buffer(controller_base.data.values[dat.num_shots])
            self.stepprog = (controller_base.data.values[dat.set_hwp_end]-controller_base.data.values[dat.set_hwp_start])/controller_base.data.values[dat.num_steps]
            self.stepspace = numpy.linspace(0,self.stepprog,controller_base.data.values[dat.num_steps])
            self.iterate = 0
            self.hwp_start = controller_base.pil_handler.get_hwp()
            self.has_been_overrange = False
            for i in numpy.linspace(controller_base.data.values[dat.set_hwp_start], controller_base.data.values[dat.set_hwp_end],
                                    controller_base.data.values[dat.num_steps]):
                if controller_base.data.values[dat.cancel]:
                    self.clear_values()
                    controller_base.data.values[dat.cancel] = False
                    break
                self.logger.message('Setting HWP to '+str(i), True)
                self.gui.progressBar.setValue(self.stepspace[self.iterate]*100)
                self.iterate +=1
                controller_base.data.values[dat.hwp_values].append(i)
                controller_base.pil_handler.set_hwp(i)
                time.sleep(1)
                if controller_base.data_monitor.pil_monitor.check_set_equals_read():
                    if controller_base.pil_handler.get_laser_energy_overrange():
                        time.sleep(0.5)
                        self.range = controller_base.pil_handler.get_laser_energy_range()
                        time.sleep(0.5)
                        self.laser_energy_range = controller_base.pil_handler.set_laser_energy_range(self.range-1)
                        time.sleep(0.5)
                        if controller_base.shutter_handler.is_shutter_closed():
                            controller_base.shutter_handler.open_shutter()
                            time.sleep(1)
                        self.has_been_overrange = True
                time.sleep(1)
                QApplication.processEvents()
                if not self.has_been_overrange:
                    if controller_base.shutter_handler.is_shutter_closed():
                        controller_base.shutter_handler.open_shutter()
                        time.sleep(1)
                    if controller_base.shutter_handler.is_shutter_open():
                        self.time_from = datetime.datetime.now().isoformat() + "Z"
                        self.time_to = (datetime.datetime.now() + datetime.timedelta(seconds=controller_base.data.values[dat.num_shots]/10)).isoformat() + "Z"
                        self.time_flo = datetime.datetime.now() + datetime.timedelta(seconds=controller_base.data.values[dat.num_shots]/10)
                        while datetime.datetime.now() < self.time_flo:
                            QApplication.processEvents()
                            time.sleep(0.1)
                        controller_base.data_monitor.pil_monitor.read_from_archiver("pv",self.time_from,self.time_to,i)
                        controller_base.data_monitor.mag_monitor.update_mag_values("pv",self.time_from,self.time_to,i)
                        controller_base.data_monitor.llrf_monitor.update_rf_values("pv",self.time_from,self.time_to,i)
                        controller_base.data_monitor.pil_monitor.save_vc_image(i)
                        # controller_base.data.values[dat.charge_values][i] = numpy.random.rand(10).tolist()
                        # controller_base.data.values[dat.ophir_values][i] = numpy.random.rand(10).tolist()
                        self.gui.update_plot()
                        self.has_been_overrange = False
                    else:
                        self.logger.message('Shutter not open!!!!!!!!!!!!!!!!!!!!', True)
                else:
                    self.has_been_overrange = False
            self.gui.progressBar.setValue(100)
            controller_base.llrf_handler.disable_rf_output()
            controller_base.pil_handler.set_hwp(self.hwp_start)

    def clear_values(self):
        controller_base.data.values[dat.charge_values] = {}
        controller_base.data.values[dat.ophir_values] = {}
        controller_base.data.values[dat.kly_fwd_pwr_values] = {}
        controller_base.data.values[dat.kly_sp_values] = {}
        controller_base.data.values[dat.gun_fwd_pwr_trace_mean] = {}
        controller_base.data.values[dat.gun_fwd_pha_trace_mean] = {}
        controller_base.data.values[dat.gun_fwd_pwr_traces] = {}
        controller_base.data.values[dat.gun_fwd_pha_traces] = {}
        controller_base.data.values[dat.kly_fwd_pwr_trace_mean] = {}
        controller_base.data.values[dat.kly_fwd_pha_trace_mean] = {}
        controller_base.data.values[dat.kly_fwd_pwr_traces] = {}
        controller_base.data.values[dat.kly_fwd_pha_traces] = {}
        controller_base.data.values[dat.vc_intensity_values] = {}
        controller_base.data.values[dat.vc_x_pix_values] = {}
        controller_base.data.values[dat.vc_y_pix_values] = {}
        controller_base.data.values[dat.vc_sig_x_pix_values] = {}
        controller_base.data.values[dat.vc_sig_y_pix_values] = {}
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

    # over load close
    def connectCloseEvents(self):
        self.gui.close()
        sys.exit()

    def set_last_mask_epoch(self):
        self.epoch = time.time()

    def seconds_passed(self,secs):
        return time.time() - self.epoch >= secs
