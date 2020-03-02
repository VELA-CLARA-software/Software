from controllers.pil_handler_base import pil_handler_base
import data.charge_measurement_data_base as dat
import numpy
import datetime
import epics
import time
import requests

class pil_handler(pil_handler_base):
    #whoami
    my_name= 'pil_handler'
    def __init__(self):
        pil_handler_base.__init__(self)
        self.laser_energy_overrange_pv = "CLA-LAS-DIA-EM-06:OverRange_RB"
        self.laser_energy_start_stop_pv = "CLA-LAS-DIA-EM-06:Run_SP"
        self.laser_energy_range_pv = "CLA-LAS-DIA-EM-06:Range_SP"
        self.hwp_pv_name = "EBT-LAS-OPT-HWP-2:ROT:MABS"
        self.hwp_get_pv_name = "EBT-LAS-OPT-HWP-2:ROT:RPOS"

    def set_laser_energy_range(self,value):
        epics.caput(self.laser_energy_start_stop_pv, 0)
        epics.caput(self.laser_energy_range_pv, value)
        epics.caput(self.laser_energy_start_stop_pv, 1)

    def set_pil_buffer(self,value):
        pass
        # pil_handler_base.pil_control.setBufferSize(value)
        # pil_handler_base.logger.message('setting PIL buffer = ' + str(value), True)

    def set_hwp(self,value):
        pass
        # epics.caput(self.hwp_pv_name, value)
        # if value - 0.5 < epics.caget(self.hwp_get_pv_name) < value + 0.5:
        #     time.sleep(2)

    def set_sa1(self,pv,value):
        pass
        # bpm_handler_base.bpm_control.setSA1(pv,value)
        # bpm_handler_base.data.values[dat.set_sa1_current] = value
        # bpm_handler_base.logger.message('setting SA1 = ' + str(value) + ' for ' + pv, True)

    def set_sa2(self,pv,value):
        pass
        # bpm_handler_base.bpm_control.setSA2(pv,value)
        # bpm_handler_base.data.values[dat.set_sa2_current] = value
        # bpm_handler_base.logger.message('setting SA2 = ' + str(value) + ' for ' + pv, True)

    def read_attenuation(self, pv):
        pass
        # bpm_handler_base.data.values[dat.get_ra1] = bpm_handler_base.bpm_control.getRA1(pv)
        # bpm_handler_base.data.values[dat.get_ra2] = bpm_handler_base.bpm_control.getRA2(pv)
        # bpm_handler_base.logger.message('RA1 = ' + str(bpm_handler_base.data.values[dat.get_ra1]) + ' for ' + pv, True)
        # bpm_handler_base.logger.message('RA2 = ' + str(bpm_handler_base.data.values[dat.get_ra2]) + ' for ' + pv, True)