from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
import datetime
import numpy as np
import matplotlib.pyplot as plt
from data.config_reader import config_reader


# keys for all the data we monitor
time_stamp = 'time_stamp'
calibration_type = 'calibration_type'
#vacuum_level = 'vacuum_level'
bunch_charge = 'bunch_charge'
bpm_name = 'bpm_name'
bpm_status = 'bpm_status'
charge_name = 'charge_name'
charge_status = 'charge_status'
scan_status = 'scan_status'
charge_monitoring = 'charge_monitoring'
all_values_set = 'all_values_set'
ready_to_go = 'ready_to_go'
charge_values = 'charge_values'
set_start = 'set_start'
set_end = 'set_end'
get_ra1 = 'get_ra1'
get_ra2 = 'get_ra2'
set_sa1_current = 'set_sa1_current'
set_sa2_current = 'set_sa2_current'
get_rd1 = 'get_rd1'
get_rd2 = 'get_rd2'
set_sd1_current = 'set_sd1_current'
set_sd2_current = 'set_sd2_current'
dv1_dly1 = 'dv1_dly1'
dv2_dly1 = 'dv2_dly1'
dv1_dly1_min_val = 'dv1_dly1_min_val'
dv2_dly1_min_val = 'dv2_dly1_min_val'
dv1_dly2 = 'dv1_dly2'
dv2_dly2 = 'dv2_dly2'
dv1_dly2_min_val = 'dv1_dly2_min_val'
dv2_dly2_min_val = 'dv2_dly2_min_val'
new_dly_1 = 'new_dly_1'
new_dly_2 = 'new_dly_2'
new_dly_1_set = 'new_dly_1_set'
new_dly_2_set = 'new_dly_2_set'
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
machine_mode = 'machine_mode'
scan_log = 'scan_log'
scan_type = 'scan_type'

all_value_keys = [time_stamp,
                  calibration_type,
                  bunch_charge,
                  bpm_name,
                  bpm_status,
                  charge_name,
                  charge_status,
                  scan_status,
                  charge_monitoring,
                  all_values_set,
                  ready_to_go,
                  charge_values,
                  set_start,
                  set_end,
                  set_sa1_current,
                  set_sa2_current,
                  get_ra1,
                  get_ra2,
                  set_sd1_current,
                  set_sd2_current,
                  dv1_dly1,
                  dv2_dly1,
                  dv1_dly1_min_val,
                  dv2_dly1_min_val,
                  dv1_dly2,
                  dv2_dly2,
                  dv1_dly2_min_val,
                  dv2_dly2_min_val,
                  new_dly_1,
                  new_dly_2,
                  new_dly_1_set,
                  new_dly_2_set,
                  get_rd1,
                  get_rd2,
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
                  values_saved,
                  machine_mode,
                  scan_log,
                  scan_type
                  ]

class bpm_calibrate_data_base(QObject):
    # whoami
    my_name = 'bpm_calibrate_data'
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
    values[calibration_type] = dummy_str
    values[bunch_charge] = dummy_dbl + 1
    values[bpm_name] = dummy_str
    values[bpm_status] = False
    values[charge_name] = dummy_str
    values[charge_status] = False
    values[scan_status] = 'dummy_str'
    values[charge_monitoring] = dummy_str
    values[all_values_set] = False
    values[ready_to_go] = False
    values[charge_values] = []
    values[set_start] = dummy_long
    values[set_end] = dummy_long + 1
    values[set_sa1_current] = dummy_long + 2
    values[set_sa2_current] = dummy_long + 3
    values[get_ra1] = dummy_long + 4
    values[get_ra2] = dummy_long + 5
    values[set_sd1_current] = dummy_long + 2
    values[set_sd2_current] = dummy_long + 3
    values[get_rd1] = dummy_long + 4
    values[get_rd2] = dummy_long + 5
    values[dv1_dly1] = {}
    values[dv2_dly1] = {}
    values[dv1_dly1_min_val] = dummy_dbl
    values[dv2_dly1_min_val] = dummy_dbl
    values[dv1_dly2] = {}
    values[dv2_dly2] = {}
    values[dv1_dly2_min_val] = dummy_dbl
    values[dv2_dly2_min_val] = dummy_dbl
    values[new_dly_1] = dummy_long
    values[new_dly_2] = dummy_long
    values[new_dly_1_set] = False
    values[new_dly_2_set] = False
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
    values[machine_mode] = dummy_str
    values[scan_log] = dummy_str
    values[scan_type] = dummy_str
    # amp_pwr_mean_data = {}

    #logger
    logger = None
    _bpm_config = None
    _log_config = None
    _charge_config = None

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
        return bpm_calibrate_data_base._logger
    @logger.setter
    def logger(self,value):
        bpm_calibrate_data_base._logger = value

    @property
    def bpm_config(self):
        return bpm_calibrate_data_base._bpm_config
    @bpm_config.setter
    def bpm_config(self,value):
        bpm_calibrate_data_base._bpm_config = value

    @property
    def charge_config(self):
        return bpm_calibrate_data_base._charge_config
    @charge_config.setter
    def charge_config(self,value):
        bpm_calibrate_data_base._charge_config = value

    def start_logging(self):
        self.logger.start_data_logging()
        self.data_log_timer.timeout.connect(self.data_log)
        self.data_log_timer.start(bpm_calibrate_data_base.config.log_config['DATA_LOG_TIME'])

    def timestamp(self):
        ts = datetime.datetime.now() - self.logger.log_start
        #print 'time = ' + str(ts.total_seconds())
        bpm_calibrate_data_base.values[time_stamp] = ts.total_seconds()

    def data_log(self):
        self.timestamp()
        if self.should_write_header:
            self.logger.write_data_log_header(bpm_calibrate_data_base.values)
            self.should_write_header = False
        self.logger.write_data(bpm_calibrate_data_base.values)