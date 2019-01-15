# base class
from data.config_reader import config_reader
from data.data_logger import data_logger
from data.blm_plotter_data import blm_plotter_data
import sys, os
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
#import VELA_CLARA_enums
import VELA_CLARA_BLM_Control
import VELA_CLARA_Charge_Control

class base(object):
    #whoami
    my_name= 'base'
    # config reader
    config = config_reader()

    logger = data_logger()
    data = blm_plotter_data()

    # pass logger to base classes
    data.logger = logger
    config.logger = logger
    # init LLRF Hardware Controllers
    blm_cont = VELA_CLARA_BLM_Control
    blm_init = VELA_CLARA_BLM_Control.init()
    blm_init.setVerbose()

    _blm_control = None
    _blmObj = None
    _blm_handler = None
    #
    charge_cont = VELA_CLARA_Charge_Control
    charge_init = VELA_CLARA_Charge_Control.init()
    charge_init.setVerbose()

    _charge_control = None
    _chargeObj = None
    _charge_handler = None

    def __init__(self):
        pass

    @property
    def blm_control(self):
        return base._blm_control

    @blm_control.setter
    def blm_control(self,value):
        base._blm_control = value

    @property
    def blmObj(self):
        return base._blmObj

    @blmObj.setter
    def blmObj(self, value):
        base._blmObj = value

    @property
    def blm_handler(self):
        return base._blm_handler

    @blm_handler.setter
    def blm_handler(self, value):
        base._blm_handler = value

    @property
    def charge_handler(self):
        return base._charge_handler

    @charge_handler.setter
    def charge_handler(self, value):
        base._charge_handler = value

    @property
    def charge_control(self):
        return base._charge_control

    @charge_control.setter
    def charge_control(self,value):
        base._charge_control = value

    @property
    def chargeObj(self):
        return base._chargeObj

    @chargeObj.setter
    def chargeObj(self, value):
        base._chargeObj = value

    def set_config(self):
        base.data.blm_config = base.config.blm_config
        base.logger.log_config = base.config.log_config
        base.data.charge_config = base.config.charge_config