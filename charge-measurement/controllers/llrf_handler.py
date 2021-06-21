from controllers.llrf_handler_base import llrf_handler_base
import data.charge_measurement_data_base as dat

class llrf_handler(llrf_handler_base):
    #whoami
    my_name= 'llrf_handler'
    def __init__(self):
        llrf_handler_base.__init__(self)
        self.llrf_key_to_pv = {}
        self.llrf_key_to_pv.update({llrf_handler_base.config.llrf_config['GUN_KLYSTRON_POWER']: dat.kly_fwd_pwr_values})
        self.llrf_key_to_pv.update({llrf_handler_base.config.llrf_config['GUN_CAVITY_POWER']: dat.gun_fwd_pwr_values})
        self.llrf_key_to_pv.update({llrf_handler_base.config.llrf_config['GUN_PHASE_SP']: dat.gun_pha_sp_values})
        self.llrf_key_to_pv.update({llrf_handler_base.config.llrf_config['GUN_PHASE_FF']: dat.gun_pha_ff_values})
        self.llrf_key_to_pv.update(
            {llrf_handler_base.config.llrf_config['GUN_PHASE_FF_LOCK_STATE']: dat.gun_pha_ff_lock_values})

    def set_llrf_buffer(self, val):
        for key, value in llrf_handler_base.llrf_objects.items():
            llrf_handler_base.llrf_objects[key].setBufferSize(val)
        llrf_handler_base.logger.message('setting llrf buffer = ' + str(val), True)

    def enable_rf_output(self):
        llrf_handler_base.llrf_control.enableRFOutput()
        llrf_handler_base.logger.message('enabling rf output', True)

    def disable_rf_output(self):
        llrf_handler_base.llrf_control.disableRFOutput()
        llrf_handler_base.logger.message('enabling rf output', True)