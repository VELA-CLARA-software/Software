# base class
from data.config_reader import config_reader
from data.data_logger import data_logger
from data.rf_condition_data import rf_condition_data
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_LLRF_Control
import VELA_CLARA_Vac_Valve_Control
import VELA_CLARA_RF_Modulator_Control
import VELA_CLARA_RF_Protection_Control
import subprocess


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

    alarm_process = subprocess.Popen('pause', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)



    def __init__(self):
        #self.alarm_process = subprocess.Popen('', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        pass
    #     print('Base init')
        # super(config_reader, self).__init__()
        # super(data_logger, self).__init__()
        # super(rf_condition_data, self).__init__()

    def __del__(self):
        base.alarm_process.stdin.write('a')



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

    def is_forward(self,str):
        return 'FORWARD' in str
    def is_reverse(self,str):
        return 'REVERSE' in str
    def is_probe(self,str):
        return 'PROBE' in str
    def is_kly_forward(self,str):
       #base.logger.message('is_kly_forward looking in ' + str , True)
       return 'KLYSTRON_FORWARD' in str
    def is_kly_reverse(self,str):
        #base.logger.message('is_kly_reverse looking in ' + str, True)
        return 'KLYSTRON_REVERSE' in str
    def is_cav_forward(self,str):
        #base.logger.message('is_cav_forward looking in ' + str, True)
        return 'CAVITY_FORWARD' in str
    def is_cav_reverse(self,str):
        #base.logger.message('is_cav_reverse looking in ' + str, True)
        return 'CAVITY_REVERSE' in str


    def is_kly_forward_power(self,str):
        return 'KLYSTRON_FORWARD_POWER' in str

    def is_kly_reverse_power(self,str):
        return 'KLYSTRON_REVERSE_POWER' in str

    def is_cav_forward_power(self,str):
        return 'CAVITY_FORWARD_POWER' in str

    def is_cav_reverse_power(self,str):
        return 'CAVITY_REVERSE_POWER' in str

    def is_probe_power(self, str):
        return 'PROBE_POWER' in str

    def is_kly_forward_phase(self,str):
        return 'KLYSTRON_FORWARD_PHASE' in str

    def is_kly_reverse_phase(self,str):
        return 'KLYSTRON_REVERSE_PHASE' in str

    def is_cav_forward_phase(self,str):
        return 'CAVITY_FORWARD_PHASE' in str

    def is_cav_reverse_phase(self,str):
        return 'CAVITY_REVERSE_PHASE' in str

    def is_probe_phase(self,str):
        return 'PROBE_PHASE' in str








    def alarm(self, alarm):
        pass
        #subprocess.call('espeak -ven+f5 ' + alarm)
        #base.alarm_process.stdin.write('espeak -ven+f5 ' + alarm )
        # p = subprocess.Popen('espeak '+alarm, shell=True)
