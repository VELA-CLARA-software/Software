from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
from VELA_CLARA_enums import STATE
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import datetime
import numpy as np
import matplotlib.pyplot as plt
from data.config_reader import config_reader


# keys for all the data we monitor
time_stamp = 'time_stamp'
#vacuum_level = 'vacuum_level'
bunch_charge = 'bunch_charge'
bpm_name = 'bpm_name'
bpm_status = 'bpm_status'
scope_name = 'scope_name'
scope_status = 'scope_status'
scan_status = 'scan_status'
scope_monitoring = 'scope_monitoring'
all_values_set = 'all_values_set'
ready_to_go = 'ready_to_go'
scope_values = 'scope_values'
scope_channel = 'scope_channel'
set_sa_start = 'set_sa_start'
set_sa_end = 'set_sa_end'
get_ra1 = 'get_ra1'
get_ra2 = 'get_ra2'
set_sa1_current = 'set_sa1_current'
set_sa2_current = 'set_sa2_current'
num_shots = 'num_shots'
bpm_raw_data = 'bpm_raw_data'
bpm_u11 = 'bpm_u11'
bpm_u12 = 'bpm_u12'
bpm_u13 = 'bpm_u13'
bpm_u14 = 'bpm_u14'
bpm_u21 = 'bpm_u21'
bpm_u22 = 'bpm_u22'
bpm_u23 = 'bpm_u23'
bpm_u24 = 'bpm_u24'
bpm_raw_data_mean_v11 = 'bpm_raw_data_mean_v11'
bpm_raw_data_mean_v12 = 'bpm_raw_data_mean_v12'
bpm_raw_data_mean_v21 = 'bpm_raw_data_mean_v21'
bpm_raw_data_mean_v22 = 'bpm_raw_data_mean_v22'
bpm_v11_v12_sum = 'bpm_v11_v12_sum'
bpm_v21_v22_sum = 'bpm_v21_v22_sum'
att_1_cal = 'att_1_cal'
att_2_cal = 'att_2_cal'
v_1_cal = 'v_1_cal'
v_2_cal = 'v_2_cal'
q_cal = 'q_cal'
plots_done = 'plots_done'
values_saved = 'values_saved'

all_value_keys = [time_stamp,
                  bunch_charge,
                  bpm_name,
                  bpm_status,
                  scope_name,
                  scope_status,
                  scan_status,
                  scope_monitoring,
                  all_values_set,
                  ready_to_go,
                  scope_values,
                  scope_channel,
                  set_sa_start,
                  set_sa_end,
                  set_sa1_current,
                  set_sa2_current,
                  get_ra1,
                  get_ra2,
                  num_shots,
                  bpm_raw_data,
                  bpm_u11,
                  bpm_u12,
                  bpm_u13,
                  bpm_u14,
                  bpm_u21,
                  bpm_u22,
                  bpm_u23,
                  bpm_u24,
                  bpm_raw_data_mean_v11,
                  bpm_raw_data_mean_v12,
                  bpm_raw_data_mean_v21,
                  bpm_raw_data_mean_v22,
                  bpm_v11_v12_sum,
                  bpm_v21_v22_sum,
                  att_1_cal,
                  att_2_cal,
                  v_1_cal,
                  v_2_cal,
                  q_cal,
                  plots_done,
                  values_saved
                  ]

class bpm_attenuation_calibrate_data_base(QObject):
    # whoami
    my_name = 'bpm_attenuation_calibrate_data'
    # config
    config = config_reader()
    # for logging
    log_param = None
    path = None
    time = None
    log_start = None
    should_write_header = True

    values = {}
    dummy_dbl = -999.0
    dummy_str = "dummy_str"
    dummy_int = int(-999)
    dummy_long = long(-999)
    [values.update({x: 0}) for x in all_value_keys]
    values[time_stamp] = dummy_dbl
    values[bunch_charge] = dummy_dbl + 1
    values[bpm_name] = dummy_str
    values[bpm_status] = False
    values[scope_name] = dummy_str
    values[scope_channel] = dummy_str
    values[scope_status] = False
    values[scan_status] = 'dummy_str'
    values[scope_monitoring] = dummy_str
    values[all_values_set] = False
    values[ready_to_go] = False
    values[scope_values] = []
    values[set_sa_start] = dummy_long
    values[set_sa_end] = dummy_long + 1
    values[set_sa1_current] = dummy_long + 2
    values[set_sa2_current] = dummy_long + 3
    values[get_ra1] = dummy_long + 4
    values[get_ra2] = dummy_long + 5
    values[num_shots] = dummy_int
    values[bpm_raw_data] = [[] for i in range(8)]
    values[bpm_u11] = []
    values[bpm_u12] = []
    values[bpm_u13] = []
    values[bpm_u14] = []
    values[bpm_u21] = []
    values[bpm_u22] = []
    values[bpm_u23] = []
    values[bpm_u24] = []
    values[bpm_raw_data_mean_v11] = dummy_dbl + 10
    values[bpm_raw_data_mean_v12] = dummy_dbl + 11
    values[bpm_raw_data_mean_v21] = dummy_dbl + 12
    values[bpm_raw_data_mean_v22] = dummy_dbl + 13
    values[bpm_v11_v12_sum] = {}
    values[bpm_v21_v22_sum] = {}
    values[att_1_cal] = dummy_long + 6
    values[att_2_cal] = dummy_long + 7
    values[v_1_cal] = dummy_dbl + 16
    values[v_2_cal] = dummy_dbl + 17
    values[q_cal] = dummy_dbl + 18
    values[plots_done] = False
    values[values_saved] = False
    # amp_pwr_mean_data = {}

    #logger
    logger = None
    _bpm_config = None
    _log_config = None
    _scope_config = None

    last_fwd_kly_pwr = None
    last_amp = None

    def __init__(self):
        QObject.__init__(self)
        self.data_log_timer = QTimer()
        # self.amp_pwr_log_timer = QTimer()
        # matplot lib bplot set-up, plotting needs improving for speed...
        plt.ion()
        plt.show()

    @property
    def logger(self):
        return bpm_attenuation_calibrate_data_base._logger
    @logger.setter
    def logger(self,value):
        bpm_attenuation_calibrate_data_base._logger = value

    @property
    def bpm_config(self):
        return bpm_attenuation_calibrate_data_base._bpm_config
    @bpm_config.setter
    def bpm_config(self,value):
        bpm_attenuation_calibrate_data_base._bpm_config = value

    @property
    def scope_config(self):
        return bpm_attenuation_calibrate_data_base._scope_config
    @scope_config.setter
    def scope_config(self,value):
        bpm_attenuation_calibrate_data_base._scope_config = value

    def start_logging(self):
        self.logger.start_data_logging()
        self.data_log_timer.timeout.connect(self.data_log)
        self.data_log_timer.start(bpm_attenuation_calibrate_data_base.config.log_config['DATA_LOG_TIME'])

    def timestamp(self):
        ts = datetime.datetime.now() - self.logger.log_start
        #print 'time = ' + str(ts.total_seconds())
        bpm_attenuation_calibrate_data_base.values[time_stamp] = ts.total_seconds()

    def data_log(self):
        self.timestamp()
        if self.should_write_header:
            self.logger.write_data_log_header(bpm_attenuation_calibrate_data_base.values)
            self.should_write_header = False
        self.logger.write_data(bpm_attenuation_calibrate_data_base.values)