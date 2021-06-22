from controllers.pil_handler_base import pil_handler_base
import data.charge_measurement_data_base as dat
import time

class pil_handler(pil_handler_base):
    #whoami
    my_name= 'pil_handler'
    def __init__(self):
        pil_handler_base.__init__(self)
        self.laser_energy_overrange_pv = "CLA-LAS-DIA-EM-06:OverRange_RB"
        self.laser_energy_start_stop_pv = "CLA-LAS-DIA-EM-06:Run_SP"
        self.laser_energy_range_pv = "CLA-LAS-DIA-EM-06:Range_SP"
        self.hwp_pv_name = "EBT-LAS-OPT-HWP-2:ROT:MABS"
        self.hwp_get_pv_name = "EBT-LAS-OPT-HWP-2:ROT:RPOS"
        self.vc_key_to_pv = {}
        self.vc_key_to_pv.update({pil_handler_base.config.vc_config['VC_AVGINTENSITY']: dat.vc_intensity_values})
        self.vc_key_to_pv.update({pil_handler_base.config.vc_config['VC_XPIX']: dat.vc_x_pix_values})
        self.vc_key_to_pv.update({pil_handler_base.config.vc_config['VC_YPIX']: dat.vc_y_pix_values})
        self.vc_key_to_pv.update({pil_handler_base.config.vc_config['VC_SIGXPIX']: dat.vc_sig_x_pix_values})
        self.vc_key_to_pv.update({pil_handler_base.config.vc_config['VC_SIGYPIX']: dat.vc_sig_y_pix_values})

    def set_laser_energy_range(self, value):
        pil_handler_base.las_em_control.setStop()
        time.sleep(0.5)
        pil_handler_base.las_em_control.setRange(int(value))
        time.sleep(0.5)
        pil_handler_base.las_em_control.setStart()
        return value

    def get_laser_energy_overrange(self):
        return pil_handler_base.las_em_control.getOverRange()

    def get_laser_energy_range(self):
        self.value = pil_handler_base.las_em_control.getRange()
        return self.value

    def set_pil_buffer(self,value):
        pil_handler_base.las_em_control.setBufferSize(value)
        pil_handler_base.logger.message('setting PIL buffer = ' + str(value), True)

    def set_vc_buffer(self, val):
        for key, value in pil_handler_base.vc_objects.items():
            pil_handler_base.vc_objects[key].setBufferSize(val)

    def set_hwp(self, value):
        pil_handler_base.hwp_control.setHWP(value)
        while value - 0.1 < pil_handler_base.hwp_control.getHWPRead() < value + 0.1:
            time.sleep(0.2)

    def get_hwp(self):
        return pil_handler_base.hwp_control.getHWPRead()