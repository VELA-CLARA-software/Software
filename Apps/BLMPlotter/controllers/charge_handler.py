from charge_handler_base import charge_handler_base
import data.blm_plotter_data_base as dat
import numpy, collections

class charge_handler(charge_handler_base):
    #whoami
    my_name= 'charge_handler'
    def __init__(self):
        charge_handler_base.__init__(self)

    def set_charge_buffer(self,value):
        charge_handler_base.charge_control.setBufferSize(value)