from controllers.pil_handler_base import pil_handler_base
import data.charge_measurement_data_base as dat
import numpy

class pil_handler(pil_handler_base):
    #whoami
    my_name= 'bpm_handler'
    def __init__(self):
        bpm_handler_base.__init__(self)

    def set_pil_buffer(self,value):
        pass
        # pil_handler_base.pil_control.setBufferSize(value)
        # pil_handler_base.logger.message('setting PIL buffer = ' + str(value), True)

    def set_hwp(self,pv,value):
        pass
        # bpm_handler_base.bpm_control.setSA1(pv,value)
        # bpm_handler_base.bpm_control.setSA2(pv,value)
        # bpm_handler_base.data.values[dat.set_sa1_current] = value
        # bpm_handler_base.data.values[dat.set_sa2_current] = value
        # bpm_handler_base.logger.message('setting SA1 = SA2 = ' + str(value) + ' for ' + pv, True)

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