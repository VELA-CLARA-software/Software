# base class
from data.config_reader import config_reader
from data.data_logger import data_logger
from data.rf_condition_data import rf_condition_data
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_LLRF_Control
import VELA_CLARA_Vac_Valve_Control
import VELA_CLARA_RF_Modulator_Control
import VELA_CLARA_RF_Protection_Control


#class base(config_reader,data_logger,rf_condition_data):
class base(object):
    #whoami
    my_name= 'base'
    # config reader
    config = config_reader()

    logger = data_logger()
    data = rf_condition_data()

    # pass logger to base classes
    data.logger = logger
    config.logger = logger

    #def __init__(self):
    llrf_type = LLRF_TYPE.UNKNOWN_TYPE

    # init LLRF Hardware Controllers
    llrf_init = VELA_CLARA_LLRF_Control.init()
    llrf_init.setVerbose()
    #llrf_init.setQuiet()
    _llrf_control = None  # LLRF HWC
    _llrfObj = None  # LLRF HWC
    _llrf_handler = None
    #
    # other attributes that need default values
    # they are used in function below
    # config file read successfully
    #
    # vaccume valves
    valve_init = VELA_CLARA_Vac_Valve_Control.init()
    valve_init.setQuiet()
    #valve_init.setVerbose()
    valve_control = None
    #
    mod_init = VELA_CLARA_RF_Modulator_Control.init()
    mod_init.setQuiet()
    mod_control = None
    #
    # RF protection
    prot_init = VELA_CLARA_RF_Protection_Control.init()
    prot_init.setQuiet()
    #rot_init.setVerbose()
    prot_control = None
    # def __init__(self):
    #     print('Base init')
        # super(config_reader, self).__init__()
        # super(data_logger, self).__init__()
        # super(rf_condition_data, self).__init__()

    @property
    def llrf_control(self):
        return base._llrf_control

    @llrf_control.setter
    def llrf_control(self,value):
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

    def set_config(self):
        base.data.llrf_config = base.config.llrf_config
        base.logger.log_config = base.config.log_config