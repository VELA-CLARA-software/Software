from blm_handler_base import blm_handler_base
import data.blm_plotter_data_base as dat
import numpy

class blm_handler(blm_handler_base):
    #whoami
    my_name= 'blm_handler'
    def __init__(self):
        blm_handler_base.__init__(self)

    def set_bpm_buffer(self,value):
        blm_handler_base.bpm_control.setBufferSize(value)
        blm_handler_base.logger.message('setting buffer = ' + str(value), True)

    def update_blm_voltages(self):
        if blm_handler_base.data.values[dat.blm_status] and blm_handler_base.data.values[dat.charge_status]:
            for i in blm_handler_base.data.values[dat.blm_names]:
                blm_handler_base.data.values[dat.blm_voltages][i] = abs(numpy.mean(1.0))