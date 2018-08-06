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
ready_to_go = 'ready_to_go'
charge_values = 'charge_values'
machine_mode = 'machine_mode'
scan_log = 'scan_log'
scan_type = 'scan_type'
num_bpms = 'num_bpms'
bpm_names = 'bpm_names'
bpm_charge = 'bpm_charge'
recalibrate_go = 'recalibrate_go'
bpm_positions = 'bpm_positions'

all_value_keys = [time_stamp,
                  calibration_type,
                  bunch_charge,
                  bpm_name,
                  bpm_status,
                  charge_name,
                  charge_status,
                  scan_status,
                  charge_monitoring,
                  ready_to_go,
                  charge_values,
                  machine_mode,
                  scan_log,
                  scan_type,
                  num_bpms,
                  bpm_names,
                  bpm_charge,
                  recalibrate_go,
                  bpm_positions
                  ]

class bpm_charge_plotter_data_base(QObject):
    # whoami
    my_name = 'bpm_charge_plotter_data'
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
    values[ready_to_go] = False
    values[charge_values] = []
    values[machine_mode] = dummy_str
    values[scan_log] = dummy_str
    values[scan_type] = dummy_str
    values[num_bpms] = dummy_int
    values[bpm_names] = []
    values[bpm_charge] = {}
    values[recalibrate_go] = False
    values[bpm_positions] = {}
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
        return bpm_charge_plotter_data_base._logger
    @logger.setter
    def logger(self,value):
        bpm_charge_plotter_data_base._logger = value

    @property
    def bpm_config(self):
        return bpm_charge_plotter_data_base._bpm_config
    @bpm_config.setter
    def bpm_config(self,value):
        bpm_charge_plotter_data_base._bpm_config = value

    @property
    def charge_config(self):
        return bpm_charge_plotter_data_base._charge_config
    @charge_config.setter
    def charge_config(self,value):
        bpm_charge_plotter_data_base._charge_config = value

    def start_logging(self):
        self.logger.start_data_logging()
        self.data_log_timer.timeout.connect(self.data_log)
        self.data_log_timer.start(bpm_charge_plotter_data_base.config.log_config['DATA_LOG_TIME'])

    def timestamp(self):
        ts = datetime.datetime.now() - self.logger.log_start
        #print 'time = ' + str(ts.total_seconds())
        bpm_charge_plotter_data_base.values[time_stamp] = ts.total_seconds()

    def data_log(self):
        self.timestamp()
        if self.should_write_header:
            self.logger.write_data_log_header(bpm_charge_plotter_data_base.values)
            self.should_write_header = False
        self.logger.write_data(bpm_charge_plotter_data_base.values)