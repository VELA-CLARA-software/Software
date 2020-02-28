from controllers.mag_handler_base import mag_handler_base
import data.charge_measurement_data_base as dat
import numpy

class mag_handler(mag_handler_base):
    #whoami
    my_name= 'mag_handler'
    def __init__(self):
        mag_handler_base.__init__(self)

    def read_magnet(self,pv,value):
        pass
        # bpm_handler_base.bpm_control.setSA1(pv,value)
        # bpm_handler_base.bpm_control.setSA2(pv,value)
        # bpm_handler_base.data.values[dat.set_sa1_current] = value
        # bpm_handler_base.data.values[dat.set_sa2_current] = value
        # bpm_handler_base.logger.message('setting SA1 = SA2 = ' + str(value) + ' for ' + pv, True)