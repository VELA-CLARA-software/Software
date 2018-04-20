# base class
from data.config_reader import config_reader
from data.data_logger import data_logger
from data.bpm_attenuation_calibrate_data import bpm_attenuation_calibrate_data
import VELA_CLARA_BPM_Control
import VELA_CLARA_Scope_Control

class base(object):
    #whoami
    my_name= 'base'
    # config reader
    config = config_reader()

    logger = data_logger()
    data = bpm_attenuation_calibrate_data()

    # pass logger to base classes
    data.logger = logger
    config.logger = logger
    # init LLRF Hardware Controllers
    bpm_init = VELA_CLARA_BPM_Control.init()
    bpm_init.setVerbose()

    _bpm_control = None
    _bpmObj = None
    _bpm_handler = None
    #
    scope_init = VELA_CLARA_Scope_Control.init()
    scope_init.setVerbose()
    #valve_init.setVerbose()
    _scope_control = None
    _scopeObj = None

    def __init__(self):
        pass

    @property
    def bpm_control(self):
        return base._bpm_control

    @bpm_control.setter
    def bpm_control(self,value):
        base._bpm_control = value

    @property
    def bpmObj(self):
        return base._bpmObj

    @bpmObj.setter
    def bpmObj(self, value):
        base._bpmObj = value

    @property
    def bpm_handler(self):
        return base._bpm_handler

    @bpm_handler.setter
    def bpm_handler(self, value):
        base._bpm_handler = value

    @property
    def scope_control(self):
        return base._scope_control

    @scope_control.setter
    def scope_control(self,value):
        base._scope_control = value

    @property
    def scopeObj(self):
        return base._scopeObj

    @scopeObj.setter
    def scopeObj(self, value):
        base._scopeObj = value

    def set_config(self):
        base.data.bpm_config = base.config.bpm_config
        base.logger.log_config = base.config.log_config
        base.data.scope_config = base.config.scope_config