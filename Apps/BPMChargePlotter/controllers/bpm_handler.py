from bpm_handler_base import bpm_handler_base
import data.bpm_charge_plotter_data_base as dat
import numpy

class bpm_handler(bpm_handler_base):
    #whoami
    my_name= 'bpm_handler'
    def __init__(self):
        bpm_handler_base.__init__(self)

    def recalibrate_attenuation(self,value):
        for i in bpm_handler_base.data.values[dat.bpm_names]:
            bpm_handler_base.bpm_control.reCalAttenuation(i,bpm_handler_base.data.values[dat.bunch_charge])
            bpm_handler_base.data.values[dat.recalibrate_go] = False