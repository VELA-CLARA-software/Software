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
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=1000)

        self.timer = QTimer()
        self.set_success = True
        self.timer.start(self.update_time)
        self.ophir_pv_name = "CLA-LAS-DIA-EM-06:E_RB"
        self.wcm_pv_name = "CLA-S01-DIA-WCM-01:Q"
        self.vc_x_pv_name = "CLA-VCA-DIA-CAM-01:ANA:X_RBV"
        self.vc_y_pv_name = "CLA-VCA-DIA-CAM-01:ANA:Y_RBV"
        self.vc_sig_x_pv_name = "CLA-VCA-DIA-CAM-01:ANA:SigmaX_RBV"
        self.vc_sig_y_pv_name = "CLA-VCA-DIA-CAM-01:ANA:SigmaY_RBV"

        self.run()

    def run(self):
        # now we're ready to start the timer, (could be called from a function)
        # item = [self.bunch_charge]
        # if self.sanity_checks(item):
        #     self.timer.start(self.update_time)
        #     monitor.logger.message(self.my_name, ' STARTED running')
        #     self.set_good()
        # else:
        monitor.cam_control.startAcquireAndAnalysis_VC()
        monitor.logger.message(self.my_name, ' running')

    def check_set_equals_read(self):
        return True

    def read_from_archiver(self,pv,time_from,time_to,hwp):
        # READ FROM ARCHIVER OVER 1s
        self.wcm_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.wcm_pv_name + "&from=" + time_from + "&to=" + time_to
        self.ophir_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.ophir_pv_name + "&from=" + time_from + "&to=" + time_to
        self.vc_x_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.vc_x_pv_name + "&from=" + time_from + "&to=" + time_to
        self.vc_y_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.vc_y_pv_name + "&from=" + time_from + "&to=" + time_to
        self.vc_sig_x_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.vc_sig_x_pv_name + "&from=" + time_from + "&to=" + time_to
        self.vc_sig_y_url = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=" + self.vc_sig_y_pv_name + "&from=" + time_from + "&to=" + time_to
        self.wcmr = requests.get(self.wcm_url)
        self.wcmdata = self.wcmr.json()
        self.wcmevent = []
        self.wcmtimestamp = []
        for i in range(len(self.wcmdata[0]["data"])):
            self.wcmevent.append(self.wcmdata[0]["data"][i]["val"])
            self.wcmtimestamp.append(float(str(self.wcmdata[0]["data"][i]["secs"])+"."+str(self.wcmdata[0]["data"][i]["nanos"])))
        self.ophirr = requests.get(self.ophir_url)
        self.ophirdata = self.ophirr.json()
        self.ophirevent = []
        self.ophirtimestamp = []
        for i in range(0, len(self.ophirdata[0]["data"])):
            self.ophirevent.append(self.ophirdata[0]["data"][i]["val"])
            self.ophirtimestamp.append(float(str(self.ophirdata[0]["data"][i]["secs"])+"."+str(self.ophirdata[0]["data"][i]["nanos"])))
        self.vcxr = requests.get(self.vc_x_url)
        self.vcxdata = self.vcxr.json()
        self.vcxevent = []
        self.vcxtimestamp = []
        for i in range(0, len(self.vcxdata[0]["data"])):
            self.vcxevent.append(self.vcxdata[0]["data"][i]["val"])
            self.vcxtimestamp.append(float(str(self.vcxdata[0]["data"][i]["secs"])+"."+str(self.vcxdata[0]["data"][i]["nanos"])))
        self.vcyr = requests.get(self.vc_y_url)
        self.vcydata = self.vcyr.json()
        self.vcyevent = []
        self.vcytimestamp = []
        for i in range(0, len(self.vcydata[0]["data"])):
            self.vcyevent.append(self.vcydata[0]["data"][i]["val"])
            self.vcytimestamp.append(float(str(self.vcydata[0]["data"][i]["secs"])+"."+str(self.vcydata[0]["data"][i]["nanos"])))
        self.vcsigxr = requests.get(self.vc_sig_x_url)
        self.vcsigxdata = self.vcsigxr.json()
        self.vcsigxevent = []
        self.vcsigxtimestamp = []
        for i in range(0, len(self.vcsigxdata[0]["data"])):
            self.vcsigxevent.append(self.vcsigxdata[0]["data"][i]["val"])
            self.vcsigxtimestamp.append(float(str(self.vcsigxdata[0]["data"][i]["secs"])+"."+str(self.vcsigxdata[0]["data"][i]["nanos"])))
        self.vcsigyr = requests.get(self.vc_sig_y_url)
        self.vcsigydata = self.vcsigyr.json()
        self.vcsigyevent = []
        self.vcsigytimestamp = []
        for i in range(0, len(self.vcsigydata[0]["data"])):
            self.vcsigyevent.append(self.vcsigydata[0]["data"][i]["val"])
            self.vcsigytimestamp.append(float(str(self.vcsigydata[0]["data"][i]["secs"])+"."+str(self.vcsigydata[0]["data"][i]["nanos"])))
        monitor.data.values[dat.charge_values][hwp] = self.wcmevent
        monitor.data.values[dat.ophir_values][hwp] = self.ophirevent
        monitor.data.values[dat.vc_x_pix_values][hwp] = self.vcxevent
        monitor.data.values[dat.vc_y_pix_values][hwp] = self.vcyevent
        monitor.data.values[dat.vc_sig_x_pix_values][hwp] = self.vcsigxevent
        monitor.data.values[dat.vc_sig_y_pix_values][hwp] = self.vcsigyevent
        monitor.data.values[dat.charge_time_stamp][hwp] = self.wcmtimestamp
        monitor.data.values[dat.ophir_time_stamp][hwp] = self.ophirtimestamp
        monitor.data.values[dat.vc_x_pix_time_stamp][hwp] = self.vcxtimestamp
        monitor.data.values[dat.vc_y_pix_time_stamp][hwp] = self.vcytimestamp
        monitor.data.values[dat.vc_sig_x_pix_time_stamp][hwp] = self.vcsigxtimestamp
        monitor.data.values[dat.vc_sig_y_pix_time_stamp][hwp] = self.vcsigytimestamp

    def save_vc_image(self, i):
        monitor.cam_control.collectAndSave_VC(1)
        monitor.data.values[dat.vc_image_name][i] = monitor.cam_control.getLatestFilename_VC()
        monitor.data.values[dat.vc_image_directory][i] = monitor.cam_control.getLatestDirectory_VC()

    def update_bpm_delays(self):
        pass
        # monitor.data.values[dat.get_rd1] = monitor.bpm_control.getRD1(monitor.data.values[dat.bpm_name])
        # monitor.data.values[dat.get_rd2] = monitor.bpm_control.getRD2(monitor.data.values[dat.bpm_name])