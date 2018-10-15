from blm_handler_base import blm_handler_base
import data.blm_plotter_data_base as dat
import numpy, collections

class blm_handler(blm_handler_base):
    #whoami
    my_name= 'blm_handler'
    def __init__(self):
        blm_handler_base.__init__(self)

    def set_blm_buffer(self,value):
        blm_handler_base.blm_control.setBufferSize(value)
        blm_handler_base.logger.message('setting buffer = ' + str(value), True)
        for i in blm_handler_base.data.values[dat.blm_waveform_pvs]:
            blm_handler_base.data.values[dat.blm_voltages][i] = collections.deque(maxlen = value)
            for j in range(0,value-1):
                blm_handler_base.data.values[dat.blm_voltages][i].append([])