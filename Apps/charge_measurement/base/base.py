# base class
from data.config_reader import config_reader
from data.data_logger import data_logger
from data.charge_measurement_data import charge_measurement_data
import sys, os
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64')
#import VELA_CLARA_enums
#import VELA_CLARA_PILaser_Control
#import VELA_CLARA_Magnet_Control
import VELA_CLARA_LLRF_Control

class base(object):
    #whoami
    my_name= 'base'
    # config reader
    config = config_reader()

    logger = data_logger()
    data = charge_measurement_data()

    # pass logger to base classes
    data.logger = logger
    config.logger = logger
    # init LLRF Hardware Controllers
    pil_cont = 1#VELA_CLARA_PILaser_Control
    pil_init = 1#VELA_CLARA_PILaser_Control.init()
    #pil_init.setVerbose()

    _pil_control = None
    _pilObj = None
    _pil_handler = None
    #
    llrf_cont = VELA_CLARA_LLRF_Control
    llrf_init = VELA_CLARA_LLRF_Control.init()
    llrf_init.setVerbose()

    _llrf_control = None
    _llrfObj = None
    _llrf_handler = None

    mag_cont = 1#VELA_CLARA_Magnet_Control
    mag_init = 1#VELA_CLARA_Magnet_Control.init()
    #mag_init.setVerbose()

    _mag_control = None
    _magObj = None
    _mag_handler = None

    def __init__(self):
        pass

    @property
    def pil_control(self):
        return base._pil_control

    @pil_control.setter
    def pil_control(self,value):
        base._pil_control = value

    @property
    def pilObj(self):
        return base._pilObj

    @pilObj.setter
    def pilObj(self, value):
        base._pilObj = value

    @property
    def pil_handler(self):
        return base._pil_handler

    @pil_handler.setter
    def pil_handler(self, value):
        base._pil_handler = value

    @property
    def llrf_control(self):
        return base._llrf_control

    @llrf_control.setter
    def llrf_control(self, value):
        base._llrf_control = value

    @property
    def llrfObj(self):
        return base._llrfObj

    @llrfObj.setter
    def llrfObj(self, value):
        base._llrfObj = value

    @property
    def llrf_handler(self):
        return base._llrf_handler

    @llrf_handler.setter
    def llrf_handler(self, value):
        base._llrf_handler = value

    @property
    def mag_control(self):
        return base._mag_control

    @mag_control.setter
    def mag_control(self, value):
        base._mag_control = value

    @property
    def magObj(self):
        return base._magObj

    @magObj.setter
    def magObj(self, value):
        base._magObj = value

    @property
    def mag_handler(self):
        return base._mag_handler

    @mag_handler.setter
    def mag_handler(self, value):
        base._mag_handler = value

    def set_config(self):
        base.data.pil_config = base.config.pil_config
        base.logger.log_config = base.config.log_config
        base.data.llrf_config = base.config.llrf_config
        base.data.mag_config = base.config.mag_config