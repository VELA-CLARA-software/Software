# base class
from data.config_reader import config_reader
from data.data_logger import data_logger
from data.bpm_calibrate_data import bpm_calibrate_data
import sys, os
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
#import VELA_CLARA_enums
import VELA_CLARA_BPM_Control
import VELA_CLARA_Charge_Control

class base(object):
    #whoami
    my_name= 'base'
    # config reader
    config = config_reader()

    logger = data_logger()
    data = bpm_calibrate_data()

    # pass logger to base classes
    data.logger = logger
    config.logger = logger
    # init LLRF Hardware Controllers
    bpm_cont = VELA_CLARA_BPM_Control
    bpm_init = VELA_CLARA_BPM_Control.init()
    bpm_init.setVerbose()

    _bpm_control = None
    _bpmObj = None
    _bpm_handler = None
    #
    charge_cont = VELA_CLARA_Charge_Control
    charge_init = VELA_CLARA_Charge_Control.init()
    charge_init.setVerbose()
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
        base.data.bpm_config = base.config.bpm_config
        base.logger.log_config = base.config.log_config
        base.data.charge_config = base.config.charge_config