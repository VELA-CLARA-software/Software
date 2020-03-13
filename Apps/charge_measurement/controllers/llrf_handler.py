from controllers.llrf_handler_base import llrf_handler_base
import data.charge_measurement_data_base as dat
import numpy

class llrf_handler(llrf_handler_base):
    #whoami
    my_name= 'llrf_handler'
    def __init__(self):
        llrf_handler_base.__init__(self)

    def set_llrf_buffer(self, value):
        llrf_handler_base.llrf_control.setBufferSize(value)
        llrf_handler_base.logger.message('setting llrf buffer = ' + str(value), True)

    def get_gun_fwd_pwr_mean_vals(self,value):
        pass
        # llrf_handler_base.llrf_control.setBufferSize(value)
        # llrf_handler_base.logger.message('setting buffer = ' + str(value), True)

    def get_gun_fwd_pha_mean_vals(self,value):
        pass
        # llrf_handler_base.llrf_control.setBufferSize(value)
        # llrf_handler_base.logger.message('setting buffer = ' + str(value), True)

    def set_gun_fwd_pwr_mean(self, pv, value):
        pass
        # llrf_handler_base.bpm_control.setSA1(pv, value)
        # llrf_handler_base.data.values[dat.set_sa2_current] = value
        # llrf_handler_base.logger.message('setting SA1 = SA2 = ' + str(value) + ' for ' + pv, True)

    def set_gun_fwd_pha_mean(self,pv,value):
        pass
        # llrf_handler_base.bpm_control.setSA1(pv,value)
        # llrf_handler_base.data.values[dat.set_sa2_current] = value
        # llrf_handler_base.logger.message('setting SA1 = SA2 = ' + str(value) + ' for ' + pv, True)

    def get_gun_fwd_pwr_traces(self,pv,value):
        pass
        # llrf_handler_base.bpm_control.setSA1(pv,value)
        # llrf_handler_base.data.values[dat.set_sa2_current] = value
        # llrf_handler_base.logger.message('setting SA1 = SA2 = ' + str(value) + ' for ' + pv, True)

    def get_gun_fwd_pha_traces(self, pv, value):
        pass
        # llrf_handler_base.bpm_control.setSA1(pv, value)
        # llrf_handler_base.data.values[dat.set_sa2_current] = value
        # llrf_handler_base.logger.message('setting SA1 = SA2 = ' + str(value) + ' for ' + pv, True)