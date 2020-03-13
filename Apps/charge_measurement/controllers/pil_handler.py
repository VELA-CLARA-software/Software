from controllers.pil_handler_base import pil_handler_base
import data.charge_measurement_data_base as dat
import numpy
import datetime
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

    def set_laser_energy_range(self, value):
        pil_handler_base.las_em_control.setStop()
        time.sleep(0.5)
        pil_handler_base.las_em_control.setRange(int(value))
        time.sleep(0.5)
        pil_handler_base.las_em_control.setStart()
        return value

    def get_laser_energy_overrange(self):
        return pil_handler_base.las_em_control.getOverRange()

    def get_laser_energy_range(self):
        self.value = pil_handler_base.las_em_control.getRange()
        return self.value

    def set_pil_buffer(self,value):
        pass
        # pil_handler_base.pil_control.setBufferSize(value)
        # pil_handler_base.logger.message('setting PIL buffer = ' + str(value), True)

    def set_hwp(self,value):
        pil_handler_base.hwp_control.setHWP(value)
        if value - 0.1 < pil_handler_base.hwp_control.getHWPRead() < value + 0.1:
            time.sleep(0.2)