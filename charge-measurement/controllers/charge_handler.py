from controllers.charge_handler_base import charge_handler_base
import data.charge_measurement_data_base as dat
import time
#import requests

class charge_handler(charge_handler_base):
    #whoami
    my_name= 'charge_handler'
    def __init__(self):
        charge_handler_base.__init__(self)

    def set_charge_buffer(self,value):
        charge_handler_base.charge_control.setBufferSize(value)
        charge_handler_base.logger.message('setting charge buffer = ' + str(value), True)
