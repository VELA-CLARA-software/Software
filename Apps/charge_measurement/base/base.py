# base class
from data.config_reader import config_reader
from data.data_logger import data_logger
from data.charge_measurement_data import charge_measurement_data
import sys, os
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64')
#import VELA_CLARA_enums
import CATAP.HardwareFactory
import VELA_CLARA_Camera_Control
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

    hardware_factory = CATAP.HardwareFactory.HardwareFactory(CATAP.HardwareFactory.STATE.PHYSICAL)

    pil_cont = 1  # VELA_CLARA_PILaser_Control
    pil_init = 1  # VELA_CLARA_PILaser_Control.init()
    # pil_init.setVerbose()

    cam_cont = VELA_CLARA_Camera_Control
    cam_init = VELA_CLARA_Camera_Control.init()
    cam_init.setVerbose()

    _pil_factory = None
    _pilFactoryObj = None

    _pil_control = None
    _pilObj = None
    _pil_handler = None

    _las_hwp_factory = None
    _lasHWPFactoryObj = None

    _las_em_factory = None
    _lasEMFactoryObj = None

    _hwp_control = None
    _hwpObj = None
    _las_em_control = None
    _lasEMObj = None

    _las_hwp_control = None
    _lasHWPObj = None
    _las_hwp_handler = None

    _las_em_control = None
    _lasEMObj = None
    _las_em_handler = None

    _hwp_control = None
    _hwpObj = None
    _las_em_control = None
    _lasEMObj = None

    _cam_control = None
    _camObj = None
    _cam_handler = None
    #
    llrf_cont = VELA_CLARA_LLRF_Control
    llrf_init = VELA_CLARA_LLRF_Control.init()
    llrf_init.setVerbose()

    _llrf_control = None
    _llrfObj = None
    _llrf_handler = None

    _shutter_control_1 = None
    _shutter_control_2 = None
    _shutterObj = None
    _shutter_handler = None

    mag_cont = 1#VELA_CLARA_Magnet_Control
    mag_init = 1#VELA_CLARA_Magnet_Control.init()
    #mag_init.setVerbose()

    _mag_control = None
    _magObj = None
    _mag_handler = None

    def __init__(self):
        pass

    @property
    def pil_factory(self):
        return base._pil_factory

    @pil_factory.setter
    def pil_factory(self, value):
        base._pil_factory = value

    @property
    def pilFactoryObj(self):
        return base._pilFactoryObj

    @property
    def las_em_factory(self):
        return base._las_em_factory

    @las_em_factory.setter
    def las_em_factory(self, value):
        base._las_em_factory = value

    @property
    def lasEMFactoryObj(self):
        return base._lasEMFactoryObj

    @property
    def las_hwp_factory(self):
        return base._las_hwp_factory

    @las_hwp_factory.setter
    def las_hwp_factory(self, value):
        base._las_hwp_factory = value

    @property
    def lasHWPFactoryObj(self):
        return base._lasHWPFactoryObj

    @property
    def hwp_control(self):
        return base._hwp_control

    @hwp_control.setter
    def hwp_control(self, value):
        base._hwp_control = value

    @property
    def hwpObj(self):
        return base._hwpObj

    @property
    def las_em_control(self):
        return base._las_em_control

    @las_em_control.setter
    def las_em_control(self, value):
        base._las_em_control = value

    @property
    def lasEMObj(self):
        return base._lasEMObj

    @property
    def pil_control(self):
        return base._pil_control

    @pil_control.setter
    def pil_control(self, value):
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
    def cam_control(self):
        return base._cam_control

    @cam_control.setter
    def cam_control(self, value):
        base._cam_control = value

    @property
    def camObj(self):
        return base._camObj

    @camObj.setter
    def camObj(self, value):
        base._camObj = value

    @property
    def cam_handler(self):
        return base._cam_handler

    @cam_handler.setter
    def cam_handler(self, value):
        base._cam_handler = value

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
    def shutter_control_1(self):
        return base._shutter_control_1

    @shutter_control_1.setter
    def shutter_control_1(self, value):
        base._shutter_control_1 = value

    @property
    def shutter_control_2(self):
        return base._shutter_control_2

    @shutter_control_2.setter
    def shutter_control_2(self, value):
        base._shutter_control_2 = value

    @property
    def shutterObj(self):
        return base._shutterObj

    @shutterObj.setter
    def shutterObj(self, value):
        base._shutterObj = value

    @property
    def shutter_handler(self):
        return base._shutter_handler

    @shutter_handler.setter
    def shutter_handler(self, value):
        base._shutter_handler = value

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
        base.data.las_hwp_config = base.config.las_hwp_config
        base.data.las_em_config = base.config.las_em_config
        base.logger.log_config = base.config.log_config
        base.data.llrf_config = base.config.llrf_config
        base.data.mag_config = base.config.mag_config