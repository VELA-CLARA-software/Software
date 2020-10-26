from controllers.shutter_handler_base import shutter_handler_base
import data.charge_measurement_data_base as dat
import numpy
import datetime
import time
import requests

class shutter_handler(shutter_handler_base):
    #whoami
    my_name= 'pil_handler'
    def __init__(self):
        shutter_handler_base.__init__(self)

    def open_shutter(self):
        return shutter_handler_base.shutter_control_1.open() and shutter_handler_base.shutter_control_2.open()

    def close_shutter(self):
        return shutter_handler_base.shutter_control_1.close() and shutter_handler_base.shutter_control_2.close()

    def is_shutter_open(self):
        return shutter_handler_base.shutter_control_1.isOpen() and shutter_handler_base.shutter_control_2.isOpen()

    def is_shutter_closed(self):
        return shutter_handler_base.shutter_control_1.isClosed() and shutter_handler_base.shutter_control_2.isClosed()